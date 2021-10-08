from extensions import db
from sqlalchemy import asc, desc

class PhoneModel(db.Model):
    __tablename__ = 'phone'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Boolean, nullable=False)
    number = db.Column(db.String(11), nullable=False)

    def __init__(self, user_id, category, number):
        self.user_id = user_id
        self.category = category
        self.number = number
        
    def __repr__(self):
        return f'PhoneModel: {self.user_id}, {self.category}, {self.number}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'category': self.category, 'number': self.number}

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_phone_by_id(cls, id_):
        phone = cls.query.filter_by(id=id_).first()
        return phone

    @classmethod
    def get_all_phones(cls, sort_by=None):
        order_funcs = {
        "asc": asc, 
        "desc": desc
        }
        if sort_by:
            field, order = sort_by.split('.')
            emails = cls.query.order_by(order_funcs[order](field)).all()
        else:
            emails = cls.query.all()
        return emails

    def delete(self):
        db.session.delete(self)
        db.session.commit()