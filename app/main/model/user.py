from .. import db
from .user_word import UserWord

import datetime


class User(db.Model):
    """ User statistics model """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    chats_num = db.Column(db.Integer)
    dialogs_num = db.Column(db.Integer)
    groups_num = db.Column(db.Integer)
    days_with = db.Column(db.Integer)
    mess_num = db.Column(db.Integer)
    words_num = db.Column(db.Integer)
    chars_num = db.Column(db.Integer)
    active_period = db.Column(db.String(100))
    act_mess_num = db.Column(db.Integer)
    act_words_num = db.Column(db.Integer)
    act_chars_num = db.Column(db.Integer)

    words = db.relationship("UserWord")
