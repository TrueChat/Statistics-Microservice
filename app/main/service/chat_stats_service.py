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
from ..model.user import User
from ..model.user_word import UserWord


'''
    1) Number of messages
    2) How many days exists
    3) How many users
    4) How many actie users (more than 5% messages)
    5) Number of words
    6) Number of chars
    7) Members stats
    8) Top words plot
'''


def get_chat_statistics(token, chat_id):
    chat_info = get_chat_info(token, chat_id)
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
            'username': k,
            'mean_char': mean_char(v),
            'mean_word': mean_word(v),
            'num_mess': num_mess(v),
            'num_words': num_words(v),
            'num_chars': num_chars(v),
            'percent': num_mess(v) / nm_mess * 100
        }
        
        if result[k]['percent'] > 5.0:
            act_num += 1

    for user in chat_info['users']:
        if not result.get(user['username']):
            result[user['username']] = {
                'username': user['username'],
                'mean_char': 0,
                'mean_word': 0,
                'num_mess': 0,
                'num_words': 0,
                'num_chars': 0,
                'percent': 0,
                'days_in': count_days(user['date_joined'])
            }
        else:
            result[user['username']]['days_in'] = count_days(user['date_joined'])

    if temp_nm_mess == 0:
        nm_mess = 0

    return {
        'num_mess': nm_mess,
        'num_users': num_users,
        'days': days,
        'mean_mess_char_length': mean_char(messages),
        'mean_mess_word_length': mean_word(messages),
        'num_act_users': act_num,
        'num_afk_users': num_users - len(grouped),
        'grouped': result
    }, 200


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
