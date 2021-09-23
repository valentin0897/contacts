from extensions import db
from sqlalchemy import asc, desc


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(64), index=True, nullable=False)
    avatar_path = db.Column(db.String(260))
    sex = db.Column(db.String(1))
    birthday = db.Column(db.Date())
    address = db.Column(db.String(150))
    phones = db.relationship('Phone', backref='user', lazy='dynamic')
    emails = db.relationship('Email', backref='user', lazy='dynamic')

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
    
    def add_user(fio, avatar_path, sex, birthday, address):
        new_user = User(fio, avatar_path, sex, birthday, address)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user(id):
        user = User.query.filter_by(id=id).first()
        json = user.json()
        return json

    def get_all_users(field=None, order="asc"):
        if(field != None):
            json = [User.json(user) for user in (User.query.order_by(getattr(User, field).asc())).all()] if order == "asc" else \
            [User.json(user) for user in (User.query.order_by(getattr(User, field).desc())).all()]
        else:
            json = [User.json(user) for user in User.query.all()]
        return json

    def update_user(id, fio, avatar_path, sex, birthday, address):
        update_user = User.query.filter_by(id=id).first()
        update_user.fio = fio
        update_user.avatar_path = avatar_path
        update_user.sex = sex
        update_user.birthday = birthday
        update_user.address = address
        db.session.commit()

    def delete_user(id):
        deleted_user = User.query.filter_by(id=id).delete()
        db.session.commit()


class Phone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    number = db.Column(db.String(11))

    def __init__(self, user_id, type, number):
        self.user_id = user_id
        self.type = type
        self.number = number
        
    def __repr__(self):
        return f'Phone: {self.user_id}, {self.type}, {self.number}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'type': self.type, 'number': self.number}

    def add_phone(user_id, type, number):
        new_phone = Phone(user_id, type, number)
        db.session.add(new_phone)
        db.session.commit()

    def get_phone(id):
        phone = Phone.query.filter_by(id=id).first()
        json = phone.json()
        return json

    def get_all_phones(field=None, order="asc"):
        if(field != None):
            json = [Phone.json(phone) for phone in (Phone.query.order_by(getattr(Phone, field).asc())).all()] if order == "asc" else \
            [Phone.json(phone) for phone in (Phone.query.order_by(getattr(Phone, field).desc())).all()]
        else:
            json = [Phone.json(phone) for phone in Phone.query.all()]
        return json

    def update_phone(id, user_id, type, number):
        update_phone = Phone.query.filter_by(id=id).first()
        update_phone.user_id = user_id
        update_phone.type = type
        update_phone.number = number
        db.session.commit()

    def delete_phone(id):
        deleted_phone = Phone.query.filter_by(id=id).delete()
        db.session.commit()

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    email = db.Column(db.String(320))

    def __init__(self, user_id, type, email):
        self.user_id = user_id
        self.type = type
        self.email = email

    def __repr__(self):
        return f'Email: {self.user_id}, {self.type}, {self.email}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'type': self.type, 'email': self.email}

    def add_email(user_id, type, email):
        new_email = Email(user_id, type, email)
        db.session.add(new_email)
        db.session.commit()

    def get_email(id):
        email = Email.query.filter_by(id=id).first()
        json = email.json()
        return 
    
    def get_all_emails(field=None, order="asc"):
        if(field != None):
            json = [Email.json(email) for email in (Email.query.order_by(getattr(Email, field).asc())).all()] if order == "asc" else \
            [Email.json(email) for email in (Email.query.order_by(getattr(Email, field).desc())).all()]
        else:
            json = [Email.json(email) for email in Email.query.all()]
        return json

    def update_email(id, user_id, type, email):
        update_email = Email.query.filter_by(id=id).first()
        update_email.user_id = user_id
        update_email.type = type
        update_email.email = email
        db.session.commit()

    def delete_email(id):
        deleted_email = Email.query.filter_by(id=id).delete()
        db.session.commit()