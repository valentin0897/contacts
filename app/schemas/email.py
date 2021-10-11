from marshmallow.decorators import validates
from extensions import ma
from models.email import EmailModel
from models.phone import PhoneModel
from models.user import UserModel
from marshmallow import validate
from marshmallow.exceptions import ValidationError

class EmailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EmailModel
        load_instance = True
        include_fk = True
    
    id = ma.auto_field(validate=validate.Range(min=1))
    user_id = ma.auto_field(validate=validate.Range(min=1))
    category = ma.auto_field()
    email = ma.auto_field(validate=validate.Email())

    @validates("id")
    def validate_email_id(self, value):
        is_email_exist = EmailModel.get_email_by_id(value)
        if not(is_email_exist):
            raise ValidationError("There is no email with that id")

    @validates("user_id")
    def validate_user_id(self, value):
        is_user_exist = UserModel.get_user_by_id(value)
        if not(is_user_exist):
            raise ValidationError("There is no user with that id")