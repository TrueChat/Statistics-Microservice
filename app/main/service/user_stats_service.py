from requests import get
from json import loads

from .. import BASE_URL
from ..model.user import User
from ..model.user_word import UserWord


def get_user_statistics(token):
    chats = get_user_chats(token)

    chat_num = len(chats)
    group_num = len([chat for chat in chats if not chat['is_dialog']])

    return {
        'chats_num': chat_num,
        'groups_num': group_num,
        'dialogs_num': chat_num - group_num
    }, 200


def get_user_chats(token):
    return loads(
        get(
            BASE_URL + '/chats/', 
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
