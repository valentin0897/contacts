from extensions import ma
from models.phone import PhoneModel

class PhoneSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PhoneModel
        include_fk = True