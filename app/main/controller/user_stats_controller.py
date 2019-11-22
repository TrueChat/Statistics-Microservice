from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..util.decorator import token_required

from .. import BASE_URL

from ..service.user_stats_service import get_user_statistics, \
    get_user_barchart, get_user_words


api = UserDto.api
_user = UserDto.user
_words = UserDto.words


"""
User statistics:
    1) Chats number
    2) Groups number
    3) One-to-one number
    4) Days with TrueChat
    5) Number of messages
    6) Response time
    7) Most active period of day
    8) Messages statistics:
        8.1) Most popular meaningful words
"""


@api.route('/')
@api.response(200, 'Statistics gathered', _user)
@api.response(404, 'User not found')
class User(Resource):
    @api.doc('get a user statistics')
    @api.marshal_with(_user)
    @token_required
    def get(self):
        """get a user statistics given token (*token required)"""
        return get_user_statistics(request.headers.get('Authorization'))


@api.route('/plot/')
class UserPlot(Resource):
    @api.doc('get user top words chart')
    @token_required
    def get(self):
        """get a user top words chart given token (*token required)"""
        return get_user_barchart(request.headers.get('Authorization'))


@api.route('/words/')
class UserWords(Resource):
    @api.doc('get user top words in json')
    @api.marshal_with(_words)
    @token_required
    def get(self):
        """get a user top words given token (*token required)"""
        return get_user_words(request.headers.get('Authorization'))
