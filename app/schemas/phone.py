from marshmallow.decorators import validates
from marshmallow.exceptions import ValidationError
from marshmallow import validate
from extensions import ma
from models.email import EmailModel
from models.phone import PhoneModel
from models.user import UserModel

class PhoneSchema(ma.SQLAlchemySchema):
    class Meta:
        model = PhoneModel
        load_instance = True
        include_fk = True

    id = ma.auto_field(validate=validate.Range(min=1))
    user_id = ma.auto_field(validate=validate.Range(min=1))
    category = ma.auto_field()
    number = ma.auto_field(validate.Length(equal=11))

    @validates("id")
    def validate_phone_id(self, value):
        is_phone_exist = PhoneModel.get_phone_by_id(value)
        if not(is_phone_exist):
            raise ValidationError("There is no phone with that id")

    @validates("user_id")
    def validate_user_id(self, value):
        is_user_exist = UserModel.get_user_by_id(value)
        if not(is_user_exist):
            raise ValidationError("There is no user with that id")