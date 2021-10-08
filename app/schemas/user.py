from extensions import ma
from models.user import UserModel

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        load_instance = True
    
    id = ma.auto_field()
    fio = ma.auto_field()
    avatar_path = ma.auto_field()
    sex = ma.auto_field()
    birthday = ma.auto_field()
    address = ma.auto_field()