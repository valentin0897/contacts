from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(64), index=True, nullable=False)
    avatar_path = db.Column(db.String(260))
    sex = db.Column(db.String(1))
    birthday = db.Column(db.Date())
    address = db.Column(db.String(150))
    phones = db.relationship('Phone', backref='user', lazy='dynamic')
    emails = db.relationship('Email', backref='user', lazy='dynamic')


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    number = db.Column(db.String(11))

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    email = db.Column(db.String(320))