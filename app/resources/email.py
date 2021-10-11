from marshmallow.exceptions import ValidationError
from models.email import EmailModel
from schemas.email import EmailSchema
from flask_restful import Resource
from flask import request

email_schema = EmailSchema(partial=True)
email_list_schema = EmailSchema(many=True)

EMAIL_NOT_FOUND = "Email not found"
EMAIL_DELETED = "Email deleted"
EMAIL_ERROR_INSERTING = "An error occured while inserting the email"
EMAIL_ERROR_UPDATING = "An error occured while updating the email"

class Email(Resource):

    def post(self):
        id_ = request.get_json()['id']
        errors = email_schema.validate({"id": id_})
        if errors:
            return {"message": EMAIL_NOT_FOUND, "errors": errors}, 400
        else:
            email = EmailModel.get_email_by_id(id_)
            return email_schema.dump(email), 200

    def put(self):
        try:
            email = email_schema.load(request.get_json())
        except ValidationError as errors:
            return {"message": EMAIL_ERROR_INSERTING, "errors": errors.messages}

        email.save()
        return email_schema.dump(email), 201

    def patch(self):
        requested_data = request.get_json()
        errors = email_schema.validate(requested_data)
        if errors:
            return {"message": EMAIL_ERROR_UPDATING, "errors": errors}

        email = EmailModel.get_email_by_id(requested_data['id'])
        email.user_id = requested_data["user_id"]
        email.category = requested_data["category"]
        email.email = requested_data["email"]
        email.save()
        return email_schema.dump(email), 202

    def delete(self):
        requested_data = request.get_json()
        email = EmailModel.get_email_by_id(requested_data['id'])
        if email:
            email.delete()
            return {"message": EMAIL_DELETED}, 200
        else:
            return {"message": EMAIL_NOT_FOUND}, 404

class EmailList(Resource):
    
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            emails = EmailModel.get_all_emails(sort_by=reqested_data["sort_by"])
        else:
            emails = EmailModel.get_all_emails()
        return email_list_schema.dump(emails)