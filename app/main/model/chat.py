from .. import db
from .chat_word import ChatWord
from .chat_member import ChatMember

import datetime


class Chat(db.Model):
    """ Chat statistics model """
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    mess_num = db.Column(db.Integer)
    users_num = db.Column(db.Integer)
    days_exist = db.Column(db.Integer)
    mean_mess_chars = db.Column(db.Float)
    mean_mess_words = db.Column(db.Float)
    act_users_num = db.Column(db.Integer)
    afk_users_num = db.Column(db.Integer)

    words = db.relationship("ChatWord")
    members = db.relationship("ChatMember")
