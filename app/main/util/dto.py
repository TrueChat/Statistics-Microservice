from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('', description='''
        User statistics related operations. Pass auth token to get result.
    ''')

    user_word = api.model('UserWord', {
        'word': fields.String,
        'count': fields.Integer
    })

    words = api.model('Words', {
        'words': fields.List(fields.Nested(user_word)),
    })
    
    user = api.model('User', {
        'chats_num': fields.Integer(description='Number of chats'),
        'dialogs_num': fields.Integer(description='Number of dialogs'),
        'groups_num': fields.Integer(description='Number of groups'),
        'days_with': fields.Integer(description='Days with TrueChat'),
        'mess_num': fields.Integer(description='Number of messages'),
        'words_num': fields.Integer(description='Number of words'),
        'chars_num': fields.Integer(description='Number of chars'),
        'active_period': fields.String(
            description='Most active period of a day'
            ),
        'act_mess_num': fields.Integer(
            description='Number of messages in most active period'
            ),
        'act_words_num': fields.Integer(
            description='Number of words in most active period'
            ),
        'act_chars_num': fields.Integer(
            description='Number of chars in most active period'
            )
    })


class ChatDto:
    api = Namespace('Chat', description='''
        Chat statistics related operations. Pass auth token and chat id
         to get result.
    ''')
    
    chat_member = api.model('ChatMember', {
        'username': fields.String(),
        'mean_char': fields.Float(),
        'mean_word': fields.Float(),
        'num_mess': fields.Integer(),
        'num_words': fields.Integer(),
        'num_chars': fields.Integer(),
        'percent': fields.Float(),
        'days_in': fields.Integer()
    })

    chat = api.model('Chat', {
        'mess_num': fields.Integer(description='Number of messages'),
        'users_num': fields.Integer(description='Number of users'),
        'days_exist': fields.Integer(description='Number of days it exists'),
        'mean_mess_chars': fields.Float(description='Mean of messages chars'),
        'mean_mess_words': fields.Float(description='Mean of messages words'),
        'act_users_num': fields.Integer(description='Number of active ones'),
        'afk_users_num': fields.Integer(description='Number of afk users'),
        'members': fields.List(fields.Nested(chat_member))
    })
