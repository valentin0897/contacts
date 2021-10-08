from flask_restful import Resource
from models.email import EmailModel
from flask import Response, request, jsonify
import validators
from schemas.email import EmailSchema

email_schema = EmailSchema(partial=True)
email_list_schema = EmailSchema(many=True)

class Email(Resource):

    def post(self):
        requested_data = request.get_json()
        email = EmailModel.get_email_by_id(requested_data['id'])
        return email_schema.dump(email), 200

    def put(self):
        email = email_schema.load(request.get_json())
        if(validators.check_email(email.email)):
            email.save()
            return {"message": "Email добавлен"}, 201
        else:
            return {"message": "Email не добавлен"}, 400


    def patch(self):
        requested_data = request.get_json()
        email = EmailModel.get_email_by_id(requested_data['id'])
        email.user_id = requested_data["user_id"]
        email.category = requested_data["category"]
        email.email = requested_data["email"]
        if(validators.check_email(email.email)):
            email.save()
            return {"message": "Email обновлен"}, 202
        else:
            return {"message": "Email не обновлен"}, 400


    def delete(self):
        requested_data = request.get_json()
        email = EmailModel.get_email_by_id(requested_data['id'])
        email.delete()
        return {"message": "Email удален"}, 200

class EmailList(Resource):
    
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            emails = EmailModel.get_all_emails(sort_by=reqested_data["sort_by"])
        else:
            emails = EmailModel.get_all_emails()
        return email_list_schema.dump(emails)