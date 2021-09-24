from extensions import db

class PhoneModel(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    number = db.Column(db.String(11))

    def __init__(self, user_id, type, number):
        self.user_id = user_id
        self.type = type
        self.number = number
        
    def __repr__(self):
        return f'PhoneModel: {self.user_id}, {self.type}, {self.number}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'type': self.type, 'number': self.number}

    def add_phone(user_id, type, number):
        new_phone = PhoneModel(user_id, type, number)
        db.session.add(new_phone)
        db.session.commit()

    def get_phone(id):
        phone = PhoneModel.query.filter_by(id=id).first()
        json = phone.json()
        return json

    def get_all_phones(field=None, order="asc"):
        if(field != None):
            json = [PhoneModel.json(phone) for phone in (PhoneModel.query.order_by(getattr(PhoneModel, field).asc())).all()] if order == "asc" else \
            [PhoneModel.json(phone) for phone in (PhoneModel.query.order_by(getattr(PhoneModel, field).desc())).all()]
        else:
            json = [PhoneModel.json(phone) for phone in PhoneModel.query.all()]
        return json

    def update_phone(id, user_id, type, number):
        update_phone = PhoneModel.query.filter_by(id=id).first()
        update_phone.user_id = user_id
        update_phone.type = type
        update_phone.number = number
        db.session.commit()

    def delete_phone(id):
        deleted_phone = PhoneModel.query.filter_by(id=id).delete()
        db.session.commit()