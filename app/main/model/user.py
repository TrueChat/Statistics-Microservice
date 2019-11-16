from .. import db
from .user_word import UserWord

import datetime


class User(db.Model):
    """ User statistics model """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    update_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    chats_num = db.Column(db.Integer, nullable=False)
    groups_num = db.Column(db.Integer, nullable=False)

    days_with = db.Column(db.Integer, nullable=False)
    message_num = db.Column(db.Integer, nullable=False)

    response_time = db.Column(db.Integer, nullable=False)

    day_period = db.Column(db.String(100), nullable=False)
    period_mes_num = db.Column(db.Integer, nullable=False)
    period_symbol_num = db.Column(db.Integer, nullable=False)

    words = db.relationship("Word")
