from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('', description='''
        User statistics related operations. Pass auth token to get result.
    ''')
    user = api.model('Model', {
        'chats_num': fields.Integer(description='user chats number'),
    })
