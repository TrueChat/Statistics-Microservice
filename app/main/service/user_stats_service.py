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

    print(user)

    dialogs = [chat for chat in chats if chat['is_dialog']]
    messages = get_user_messages(chats, user['id'], token)
    words, chars = get_all_words(messages)

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
            'groups': group_messages(messages)
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
    joined = ' '.join([_['content'] for _ in messages])
    return joined.split(' '), len(sub('($% #*^-":;)\'/+\\_&.@?!=', '', joined))


def most_active_period(messages):
    PERIODS = {
        'Night (0.00 - 4.00)': (time(0, 0, 0), time(4, 0, 0)),
        'Early morning (4.00 - 7.00)': (time(4, 0, 0), time(7, 0, 0)),
        'Morning (7.00 - 12.00)': (time(7, 0, 0), time(12, 0, 0)),
        'Daytime (12.00 - 16.00)': (time(12, 0, 0), time(16, 0, 0)),
        'Early evening (16.00 - 20.00)': (time(16, 0, 0), time(20, 0, 0)),
        'Evening (20.00 - 0.00)': (time(20, 0, 0), time(0, 0, 0))
    }


'''
def group_messages(messages):
    groups = set(
        map(
            lambda x: datetime.strptime(
                x['date_created'], 
                "%Y-%m-%dT%H:%M:%S.983527Z"
            ).time().hour, 
            messages
        )
    )
    return [len([y for y in messages if datetime.strptime(
                y['date_created'], 
                "%Y-%m-%dT%H:%M:%S.983527Z"
            ).time().hour == x]) for x in groups]
'''


def time_in_range(start, end, x):
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x < end
