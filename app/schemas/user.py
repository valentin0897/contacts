from marshmallow.decorators import validates
from marshmallow.exceptions import ValidationError
from marshmallow import validate
from extensions import ma
from models.user import UserModel

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_instance = True
    
    id = ma.auto_field(validate=validate.Range(min=1))
    fio = ma.auto_field(validate=validate.Length(min=5, max=64))
    avatar_path = ma.auto_field(validate=validate.Regexp(r".{1,64}(\.jpg|\.png)"))
    sex = ma.auto_field(validate=validate.ContainsOnly(["М", "Ж"]))
    birthday = ma.auto_field()
    address = ma.auto_field()

