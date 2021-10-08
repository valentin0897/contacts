from extensions import ma
from models.phone import PhoneModel

class PhoneSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PhoneModel
        load_instance = True
        include_fk = True

    id = ma.auto_field()
    user_id = ma.auto_field()
    category = ma.auto_field()
    number = ma.auto_field()