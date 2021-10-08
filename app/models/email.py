from extensions import db
from sqlalchemy import asc, desc

class EmailModel(db.Model):
    __tablename__ = 'email'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String(320), nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_email_by_id(cls, id_):
        email = cls.query.filter_by(id=id_).first()
        return email
    
    @classmethod
    def get_all_emails(cls, sort_by=None):
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