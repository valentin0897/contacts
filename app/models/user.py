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

    def __init__(self, fio, avatar_path, sex, birthday, address):
        self.fio = fio
        self.avatar_path = avatar_path
        self.sex = sex
        self.birthday = birthday
        self.address = address

    def __repr__(self):
        return f"User:{self.id} {self.fio}, {self.avatar_path}, {self.sex}, \
         {self.birthday}, {self.address}"

    def json(self):
        return {'id': self.id, 'fio': self.fio,
        'avatar_path': self.avatar_path, 'sex': self.sex,
        'birthday': self.birthday, 'address': self.address}
    
    @classmethod
    def add_user(cls, fio, avatar_path, sex, birthday, address):
        new_user = cls(fio, avatar_path, sex, birthday, address)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_user(cls, id_):
        user = cls.query.filter_by(id=id_).first()
        return user.json()

    @classmethod
    def get_all_users(cls, sort_by):
        order_funcs = {
        "asc": asc, 
        "desc": desc
        }
        if sort_by:
            field, order = sort_by.split('.')
            json = [cls.json(email) for email in (cls.query.order_by(order_funcs[order](field))).all()]
        else:
            json = [cls.json(user) for user in cls.query.all()]
        return json

    @classmethod
    def update_user(cls, id_, fio, avatar_path, sex, birthday, address):
        update_user = cls.query.filter_by(id=id_).first()
        update_user.fio = fio
        update_user.avatar_path = avatar_path
        update_user.sex = sex
        update_user.birthday = birthday
        update_user.address = address
        db.session.commit()

    @classmethod
    def delete_user(cls, id_):
        cls.query.filter_by(id=id_).delete()
        db.session.commit()