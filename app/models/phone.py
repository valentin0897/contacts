from extensions import db
from sqlalchemy import asc, desc

class PhoneModel(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    number = db.Column(db.String(11))

    def __init__(self, user_id, type_, number):
        self.user_id = user_id
        self.type = type_
        self.number = number
        
    def __repr__(self):
        return f'PhoneModel: {self.user_id}, {self.type}, {self.number}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'type': self.type, 'number': self.number}

    @classmethod
    def add_phone(cls, user_id, type_, number):
        new_phone = cls(user_id, type_, number)
        db.session.add(new_phone)
        db.session.commit()

    @classmethod
    def get_phone(cls, id_):
        phone = cls.query.filter_by(id=id_).first()
        return phone.json()

    @classmethod
    def get_all_phones(cls, sort_by=None):
        order_funcs = {
        "asc": asc, 
        "desc": desc
        }
        if sort_by:
            field, order = sort_by.split('.')
            json = [cls.json(phone) for phone in (cls.query.order_by(order_funcs[order](field))).all()]
        else:
            json = [cls.json(phone) for phone in cls.query.all()]
        return json

    @classmethod
    def update_phone(cls, id_, user_id, type_, number):
        update_phone = cls.query.filter_by(id=id_).first()
        update_phone.user_id = user_id
        update_phone.type = type_
        update_phone.number = number
        db.session.commit()

    @classmethod
    def delete_phone(cls, id_):
        cls.query.filter_by(id=id_).delete()
        db.session.commit()