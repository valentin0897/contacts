from extensions import db

class EmailModel(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Boolean)
    email = db.Column(db.String(320))

    def __init__(self, user_id, type, email):
        self.user_id = user_id
        self.type = type
        self.email = email

    def __repr__(self):
        return f'EmailModel: {self.user_id}, {self.type}, {self.email}'

    def json(self):
        return {'id': self.id, 'user_id': self.user_id,
        'type': self.type, 'email': self.email}

    def add_email(user_id, type, email):
        new_email = EmailModel(user_id, type, email)
        db.session.add(new_email)
        db.session.commit()

    def get_email(id):
        email = EmailModel.query.filter_by(id=id).first()
        json = email.json()
        return 
    
    def get_all_emails(field=None, order="asc"):
        if(field != None):
            json = [EmailModel.json(email) for email in (EmailModel.query.order_by(getattr(EmailModel, field).asc())).all()] if order == "asc" else \
            [EmailModel.json(email) for email in (EmailModel.query.order_by(getattr(EmailModel, field).desc())).all()]
        else:
            json = [EmailModel.json(email) for email in EmailModel.query.all()]
        return json

    def update_email(id, user_id, type, email):
        update_email = EmailModel.query.filter_by(id=id).first()
        update_email.user_id = user_id
        update_email.type = type
        update_email.email = email
        db.session.commit()

    def delete_email(id):
        deleted_email = EmailModel.query.filter_by(id=id).delete()
        db.session.commit()
