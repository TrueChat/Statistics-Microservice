from .. import db


class ChatWord(db.Model):
    """ Word statistics model """
    __tablename__ = "chat_word"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(200), nullable=True)
    count = db.Column(db.Integer, nullable=False)

    entity_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
