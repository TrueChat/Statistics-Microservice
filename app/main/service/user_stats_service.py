from collections import Counter
from datetime import date
from datetime import datetime
from datetime import time
from functools import reduce
from json import loads
from re import sub

from requests import get

from .. import BASE_URL
from ..model.user import User
from ..model.user_word import UserWord


def get_user_statistics(token):
    user = get_user_info(token)
    chats = get_user_chats(token)

    dialogs = [chat for chat in chats if chat['is_dialog']]
    messages = get_user_messages(chats, user['id'], token)
    words, chars = get_all_words([_['content'] for _ in messages])

    period, counter, sent = most_active_period(messages)
    act_words, act_chars = get_all_words(sent)

    response_object = {
        'status': 'success',
        'message': 'Statistics was gathered',
        'data': {
            'chats_num': len(chats),
            'dialogs_num': len(dialogs),
            'groups_num': len(chats) - len(dialogs),
            'days_with': count_days(user.get('date_joined')),
            'messages_num': len(messages),
            'words_num': len(words),
            'chars_num': chars,
            'most_active_period': period,
            'most_active_mess_num': counter,
            'most_active_words_num': len(act_words),
            'most_active_chars_num': act_chars,
            'top_words': get_top_words(words)
        }
    }

    return response_object, 200


def get_user_info(token):
    return loads(
        get(
            BASE_URL + '/profile/{}/'.format(
                loads(
                    get(
                        BASE_URL + '/rest-auth/user/',
                        headers={'Authorization': token}
                    ).content
                ).get('username')
            ),
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
    delta = date.today() - datetime.strptime(registered_date, "%Y-%m-%dT%H:%M:%SZ").date()
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


def time_in_range(start, end, x):
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x < end


def get_top_words(words):
    return [
        {
            'word': word[0],
            'count': word[1]
        } for word in Counter(words).most_common(10)
    ]
