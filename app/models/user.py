from extensions import db
from sqlalchemy import asc, desc

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(64), nullable=False)
    avatar_path = db.Column(db.String(260))
    sex = db.Column(db.String(1))
    birthday = db.Column(db.Date())
    address = db.Column(db.String(150))
    phones = db.relationship('PhoneModel', backref='user', lazy='dynamic')
    emails = db.relationship('EmailModel', backref='user', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_user_by_id(cls, id_):
        user = cls.query.filter_by(id=id_).first()
        return user

    @classmethod
    def get_all_users(cls, sort_by):
        order_funcs = {
        "asc": asc, 
        "desc": desc
        }
        if sort_by:
            field, order = sort_by.split('.')
            users = cls.query.order_by(order_funcs[order](field)).all()
        else:
            users = cls.query.all()
        return users

    def delete(self):
        db.session.delete(self)
        db.session.commit()