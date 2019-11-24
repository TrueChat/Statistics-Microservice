import base64
from collections import Counter
from datetime import date
from datetime import datetime
from datetime import time
from functools import reduce
import io
from json import loads
from re import sub

from flask import send_file
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from requests import get

from .. import BASE_URL
from .. import db
from ..model.user import User
from ..model.user_word import UserWord


def get_user_statistics(token):
    user_info = get_user_info(token)
    user = User.query.filter_by(id=user_info['id']).first()

    if user:
        if time_to_update(user.update_time):
            update_statistics(user_info, token, user)
    else:
        update_statistics(user_info, token, user)

    return User.query.filter_by(id=user_info['id']).first()


def get_user_barchart(token):
    user_info = get_user_info(token)
    user = User.query.filter_by(id=user_info['id']).first()

    if not user:
        response_object = {
            'message': 'User not found'
        }
        return response_object, 404
    
    plt.rcdefaults()
    fig, ax = plt.subplots()

    names = [word.word for word in user.words]
    y_pos = np.arange(0, len(names) * 2, 2)
    performance = [word.count for word in user.words]

    ax.barh(y_pos, performance, height=1.5, left=0.3, align='center', color=(0.11, 0.11, 0.14, 1.0))
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

    coord = user.words[0].count
    for i, v in enumerate(user.words):
        plt.text(coord+0.2, i * 2, str(round(v.count, 2)), color=(0.64, 0.64, 0.648, 1.0), va="center", fontsize=14)

    plt.tight_layout()

    img = io.BytesIO()

    plt.savefig(img, transparent=True, dpi=199, format='png')
    img.seek(0)

    response = send_file(img, attachment_filename='barchart.png',
                 mimetype='image/png')
    return response


def get_user_words(token):
    user_info = get_user_info(token)
    return User.query.filter_by(id=user_info['id']).first()


def update_statistics(user_info, token, user):
    if not user:
        user = User(
            id=user_info['id'],
            update_time=datetime.utcnow()
        )
        db.session.add(user)

    chats = get_user_chats(token)

    dialogs = [chat for chat in chats if chat['is_dialog']]
    messages = get_user_messages(chats, user_info['id'], token)
    words, chars = get_all_words([_['content'] for _ in messages])

    period, counter, sent = most_active_period(messages)
    act_words, act_chars = get_all_words(sent)

    chat_num = len(chats)
    dialog_num = len(dialogs)

    user.chats_num = chat_num
    user.dialogs_num = dialog_num
    user.groups_num = chat_num - dialog_num
    user.days_with = count_days(user_info.get('date_joined'))
    user.mess_num = len(messages)
    user.words_num = len(words)
    user.chars_num = chars
    user.active_period = period
    user.act_mess_num = len(sent)
    user.act_words_num = len(act_words)
    user.act_chars_num = act_chars
    user.words = get_top_words(words)

    db.session.commit()


def time_to_update(update_time):
    delta = datetime.utcnow() - update_time
    return (24 * delta.days + delta.seconds // 3600) > 24


def get_user_info(token):
    return loads(
        get(
            BASE_URL + '/profile/',
            headers={'Authorization': token}
        ).content
    )


def get_user_chats(token):
    return loads(
        get(
            BASE_URL + '/chats/', 
            headers={'Authorization': token}
        ).content
    )


def get_user_messages(chats, user_id, token):
    return reduce(lambda x,y :x+y , [
            [
                message for message in get_chat_messages(
                    token, chat['id']
                ) if message['user']['id'] == user_id
            ] for chat in chats
        ]
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


def get_all_words(messages):
    joined = ' '.join(messages)
    return [word for word in joined.split(' ') if len(word) > 2], \
    len(sub('($% #*^-":;)\'/+\\_&.@?!=', '', joined))


def most_active_period(messages):
    PERIODS = [
        'Night (0.00 - 4.00)',
        'Early morning (4.00 - 7.00)',
        'Morning (7.00 - 12.00)',
        'Daytime (12.00 - 16.00)',
        'Early evening (16.00 - 20.00)',
        'Evening (20.00 - 0.00)'
    ]

    temp = group_messages(messages)
    grouped = {}
    for dct in temp:
        grouped.update(dct)

    periods_counters = [0] * len(PERIODS)
    periods_grouped = [[]] * len(PERIODS)

    for key, value in grouped.items():
        if time_in_range(0, 4, key):
            periods_counters[0] += len(value)
            periods_grouped[0] += value
        elif time_in_range(4, 7, key):
            periods_counters[1] += len(value)
            periods_grouped[1] += value
        elif time_in_range(7, 12, key):
            periods_counters[2] += len(value)
            periods_grouped[2] += value
        elif time_in_range(12, 16, key):
            periods_counters[3] += len(value)
            periods_grouped[3] += value
        elif time_in_range(16, 20, key):
            periods_counters[4] += len(value)
            periods_grouped[4] += value
        elif time_in_range(20, 0, key):
            periods_counters[5] += len(value)
            periods_grouped[5] += value
    
    ind = periods_counters.index(max(periods_counters))

    return (
        PERIODS[ind],
        periods_counters[ind],
        periods_grouped[ind]
    )


def group_messages(messages):
    try:
        groups = set(
            map(
                lambda x: datetime.strptime(
                    x['date_created'], 
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ).time().hour, 
                messages
            )
        )

        return [{x: [y['content'] for y in messages if datetime.strptime(
                    y['date_created'], 
                    "%Y-%m-%dT%H:%M:%S.%fZ"
                ).time().hour == x]} for x in groups]
    except:
        groups = set(
            map(
                lambda x: datetime.strptime(
                    x['date_created'], 
                    "%Y-%m-%dT%H:%M:%SZ"
                ).time().hour, 
                messages
            )
        )

        return [{x: [y['content'] for y in messages if datetime.strptime(
                    y['date_created'], 
                    "%Y-%m-%dT%H:%M:%SZ"
                ).time().hour == x]} for x in groups]


def time_in_range(start, end, x):
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x < end


def get_top_words(words):
    top_words = Counter(words).most_common(10)
    return [
        UserWord(
            word=word[0],
            count=word[1]
        ) for word in top_words
    ]
