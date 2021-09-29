from extensions import ma
from models.email import EmailModel

class EmailSchema(ma.SQLAlchemySchema):
    class Meta:
        model = EmailModel
        include_fk = True