from flask import request
from flask_restplus import Resource

from ..util.dto import ChatDto
from ..util.decorator import token_required
from ..service.chat_stats_service import get_chat_statistics

from .. import BASE_URL


api = ChatDto.api
_chat = ChatDto.chat


@api.route('/<chat_id>/')
class Chat(Resource):
    @api.doc('get a chat statistics by its id')
    @api.marshal_with(_chat)
    @token_required
    def get(self, chat_id):
        return get_chat_statistics(request.headers.get('Authorization'), chat_id)


@api.route('/<chat_id>/plot')
class ChatPlot(Resource):
    @api.doc('get a chat words plot by its id')
    @token_required
    def get(self, chat_id):
        pass
