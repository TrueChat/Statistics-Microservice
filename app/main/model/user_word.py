from .. import db


class UserWord(db.Model):
    """ Word statistics model """
    __tablename__ = "word"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(200), nullable=True)
    count = db.Column(db.Integer, nullable=False)

    entity_id = db.Column(db.Integer, db.ForeignKey('user.id'))
