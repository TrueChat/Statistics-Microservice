from collections import Counter
from datetime import date
from datetime import datetime
from datetime import time
from functools import reduce
import io, string
from json import loads
from re import sub
from statistics import mean

from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from requests import get

from .. import BASE_URL
from .. import db
from ..model.chat import Chat
from ..model.chat_word import ChatWord
from ..model.chat_member import ChatMember


def get_chat_statistics(token, chat_id):
    chat_info = get_chat_info(token, chat_id)
    chat = Chat.query.filter_by(id=chat_info['id']).first()

    if chat:
        if time_to_update(chat.update_time):
            gather(token, chat_id, chat_info, chat)
    else:
        gather(token, chat_id, chat_info, chat)

    return Chat.query.filter_by(id=chat_info['id']).first()

def gather(token, chat_id, chat_info, chat):
    if not chat:
        chat = Chat(
            id=chat_info['id'],
            update_time=datetime.utcnow()
        )
        db.session.add(chat)

    messages = get_chat_messages(token, chat_id)
    
    nm_mess = len(messages)
    temp_nm_mess = nm_mess

    if nm_mess == 0:
        nm_mess = 1

    chat_info['users'].append(chat_info['creator'])

    num_users = len(chat_info['users'])
    days = count_days(chat_info['date_created'])

    grouped = group_messages(messages)
    result = {}
    for d in grouped:
        result.update(d)
    
    act_num = 0

    for k, v in result.items():
        result[k] = {
            'mean_char': mean_char(v),
            'mean_word': mean_word(v),
            'num_mess': num_mess(v),
            'num_words': num_words(v),
            'num_chars': num_chars(v),
            'percent': num_mess(v) / nm_mess * 100
        }
        
        if result[k]['percent'] > 5.0:
            act_num += 1

    res = []
    
    for user in chat_info['users']:
        if not result.get(user['username']):
            res.append(ChatMember(
                username=user['username'],
                mean_char=0,
                mean_word=0,
                num_mess=0,
                num_words=0,
                num_chars=0,
                percent=0,
                days_in=count_days(user['date_joined'])
            ))
        else:
            temp = result.get(user['username'])
            
            res.append(ChatMember(
                username=user['username'],
                mean_char=temp['mean_char'],
                mean_word=temp['mean_word'],
                num_mess=temp['num_mess'],
                num_words=temp['num_words'],
                num_chars=temp['num_chars'],
                percent=temp['percent'],
                days_in=count_days(user['date_joined'])
            ))
            result[user['username']]['days_in'] = count_days(user['date_joined'])

    if temp_nm_mess == 0:
        nm_mess = 0
    
    afk = 0
    for mem in res:
        if mem.num_mess == 0:
            afk += 1

    chat.mess_num = nm_mess
    chat.users_num = num_users
    chat.days_exist = days
    chat.mean_mess_chars = mean_char(messages)
    chat.mean_mess_words = mean_word(messages)
    chat.act_users_num = act_num
    chat.afk_users_num =  afk
    chat.members = res
    chat.words = get_top_words(' '.join(
        [m['content'] for m in messages]
    ).split(' '))

    db.session.commit()


def num_mess(messages):
    return len(messages)


def num_words(messages):
    return len(' '.join(messages).split(' '))


def num_chars(messages):
    return len(''.join(messages))


def mean_char(messages):
    try:
        return mean([len(message['content']) for message in messages])
    except:
        try:
            return mean([len(message) for message in messages])
        except:
            return 0


def mean_word(messages):
    try:
        return mean([len(message['content'].split(' ')) for message in messages])
    except:
        try:
            return mean([len(message.split(' ')) for message in messages])
        except:
            return 0


def time_to_update(update_time):
    delta = datetime.utcnow() - update_time
    return (24 * delta.days + delta.seconds // 3600) > 24


def get_chat_info(token, chat_id):
    return loads(
        get(
            BASE_URL + '/chats/{}/'.format(
                str(chat_id)
            ),
            headers={'Authorization': token}
        ).content
    )


def get_chat_messages(token, chat_id):
    return loads(
        get(
            BASE_URL + f'/chats/{chat_id}/messages/',
            headers={'Authorization': token}
        ).content
    )


def count_days(registered_date):
    try:
        delta = date.today() - datetime.strptime(registered_date, "%Y-%m-%dT%H:%M:%SZ").date()
    except:
        delta = date.today() - datetime.strptime(registered_date, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    return delta.days


def group_messages(messages):
    groups = set(
        map(
            lambda x: x['user']['username'], 
            messages
        )
    )

    return [{x: [y['content'] for y in messages if 
    y['user']['username'] == x]} for x in groups]


def get_top_words(words):
    top_words = Counter(words).most_common(10)
    return [
        ChatWord(
            word=word[0],
            count=word[1]
        ) for word in top_words
    ]


def get_chat_barchart(token, chat_id):
    chat = Chat.query.filter_by(id=chat_id).first()

    if not chat:
        response_object = {
            'message': 'Chat not found'
        }
        return response_object, 404
    
    plt.rcdefaults()
    fig, ax = plt.subplots()

    names = [word.word for word in chat.words]
    y_pos = np.arange(len(names))
    performance = [word.count for word in chat.words]

    ax.barh(y_pos, performance, align='center', color=(0.11, 0.11, 0.14, 1.0))
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, ha='left', fontsize=14)
    ax.invert_yaxis()  # labels read top-to-bottom

    plt.tick_params(
        axis='x',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.tick_params(axis='x', colors=(0.64, 0.64, 0.648, 1.0))
    ax.tick_params(axis='y', colors=(0.11, 0.11, 0.14, 1.0))

    ax.tick_params(axis="y",direction="in", pad=-10)

    [i.set_color(color=(0.64, 0.64, 0.648, 1.0)) for i in plt.gca().get_yticklabels()]
    [i.set_color(color=(0.64, 0.64, 0.648, 1.0)) for i in plt.gca().get_xticklabels()]

    for i, v in enumerate(chat.words):
        plt.text(
            v.count+0.2, i, 
            str(round(v.count, 2)), 
            color=(0.64, 0.64, 0.648, 1.0), 
            va="center",
            fontsize=14
        )

    plt.tight_layout()

    img = io.BytesIO()

    plt.savefig(img, transparent=True, dpi=199, format='png')
    img.seek(0)

    response = send_file(img, attachment_filename='barchart.png',
                 mimetype='image/png')
    return response
