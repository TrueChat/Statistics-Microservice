from .. import db


class ChatMember(db.Model):
    """ Word statistics model """
    __tablename__ = "chat_member"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200))
    mean_char = db.Column(db.Float)
    mean_word = db.Column(db.Float)
    num_mess = db.Column(db.Integer)
    num_words = db.Column(db.Integer)
    num_chars = db.Column(db.Integer)
    percent = db.Column(db.Float)
    days_in = db.Column(db.Integer)

    entity_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
