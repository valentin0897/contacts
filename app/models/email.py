from extensions import db

class EmailModel(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    email = db.Column(db.String(320))

    def __init__(self, user_id, type_, email):
        self.user_id = user_id
        self.type = type_
        self.email = email

    def __repr__(self):
        return f'EmailModel: {self.user_id}, {self.type}, {self.email}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'type': self.type, 'email': self.email}

    @classmethod
    def add_email_to_db(cls, user_id, type_, email):
        new_email = cls(user_id, type_, email)
        db.session.add(new_email)
        db.session.commit()

    @classmethod
    def get_email_by_id(cls, id_):
        email = cls.query.filter_by(id=id_).first()
        return email.json()
    
    @classmethod
    def get_all_emails(cls, field=None, order="asc"):
        if(field != None):
            json = [cls.json(email) for email in (cls.query.order_by(getattr(cls, field).asc())).all()] if order == "asc" else \
            [cls.json(email) for email in (cls.query.order_by(getattr(cls, field).desc())).all()]
        else:
            json = [cls.json(email) for email in cls.query.all()]
        return json

    @classmethod
    def update_email(cls, id_, user_id, type_, email):
        update_email = cls.query.filter_by(id=id_).first()
        update_email.user_id = user_id
        update_email.type = type_
        update_email.email = email
        db.session.commit()

    @classmethod
    def delete_email(cls, id_):
        cls.query.filter_by(id=id_).delete()
        db.session.commit()
