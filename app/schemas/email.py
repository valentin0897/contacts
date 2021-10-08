from extensions import ma
from models.email import EmailModel

class EmailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EmailModel
        load_instance = True
        include_fk = True
    
    id = ma.auto_field()
    user_id = ma.auto_field()
    category = ma.auto_field()
    email = ma.auto_field()