from extensions import db

class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fio = db.Column(db.String(64), index=True, nullable=False)
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
    
    def add_user(fio, avatar_path, sex, birthday, address):
        new_user = UserModel(fio, avatar_path, sex, birthday, address)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    def get_user(id):
        user = UserModel.query.filter_by(id=id).first()
        json = user.json()
        return json

    def get_all_users(field=None, order="asc"):
        if(field != None):
            json = [UserModel.json(user) for user in (UserModel.query.order_by(getattr(UserModel, field).asc())).all()] if order == "asc" else \
            [UserModel.json(user) for user in (UserModel.query.order_by(getattr(UserModel, field).desc())).all()]
        else:
            json = [UserModel.json(user) for user in UserModel.query.all()]
        return json

    def update_user(id, fio, avatar_path, sex, birthday, address):
        update_user = UserModel.query.filter_by(id=id).first()
        update_user.fio = fio
        update_user.avatar_path = avatar_path
        update_user.sex = sex
        update_user.birthday = birthday
        update_user.address = address
        db.session.commit()

    def delete_user(id):
        deleted_user = UserModel.query.filter_by(id=id).delete()
        db.session.commit()