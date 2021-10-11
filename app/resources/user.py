from flask_restful import Resource
from flask import request
from marshmallow.exceptions import ValidationError
from app.resources.email import EMAIL_NOT_FOUND
from schemas.user import UserSchema
from schemas.phone import PhoneSchema
from schemas.email import EmailSchema
from models.user import UserModel
from models.phone import PhoneModel
from models.email import EmailModel

user_schema = UserSchema(partial=True)
user_list_schema = UserSchema(many=True)
phone_schema = PhoneSchema(partial=True)
email_schema = EmailSchema(partial=True)

USER_NOT_FOUND = "User not found"
USER_DELETED = "User deleted"
USER_ERROR_INSERTING = "An error occured while inserting the user"
USER_ERROR_UPDATING = "An error occured while updating the user"


class User(Resource):
    def post(self):
        id_ = request.get_json()['id']
        errors = user_schema.validate({"id": id_})
        if errors:
            return {"message": USER_NOT_FOUND, "errors": errors}
        else:
            user = UserModel.get_user_by_id(id_)
            return user_schema.dump(user), 200 


    def put(self):
        requested_data = request.get_json()
        phones = requested_data.pop("phones")
        emails = requested_data.pop("emails")
        try:
            user = user_schema.load(requested_data)
        except ValidationError as errors:
            return {"message": USER_ERROR_INSERTING, "errors": errors.messages}, 400
        
        user.save()
        if (phones):
            for number in phones:
                try:
                    phone = phone_schema.load({"user_id": user.id, "number": number, "category": True})
                except ValidationError as errors:
                    user.delete()
                    return {"message": USER_ERROR_INSERTING, "errors": errors.messages}

                phone.save()
        
        if (emails):
            for email_name in emails:
                try:
                    email = email_schema.load({"user_id": user.id, "email": email_name, "category": True})
                except ValidationError as errors:
                    user.delete()
                    return {"message": USER_ERROR_INSERTING, "errors": errors.messages}

                email.save()

        return user_schema.dump(user), 201

    def patch(self):
        requested_data = request.get_json()
        errors = user_schema.validate(requested_data)
        if errors:
            return {"message": USER_ERROR_UPDATING, "errors": errors}, 400

        user = UserModel.get_user_by_id(requested_data["id"])
        user.fio = requested_data["fio"]
        user.avatar_path = requested_data["avatar_path"]
        user.sex = requested_data["sex"]
        user.birthday = requested_data["birthday"]
        user.address = requested_data["address"]
        user.save()
        return user_schema.dump(user), 202

    def delete(self):
        requested_data = request.get_json()
        user = UserModel.get_user_by_id(requested_data['id'])
        if user:
            user.delete()
            return {"message": USER_DELETED}, 201
        else:
            return {"message": EMAIL_NOT_FOUND}, 404


class UserList(Resource):
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            users = UserModel.get_all_users(sort_by=reqested_data['sort_by'])
        else:
            users = UserModel.get_all_users()
        return user_list_schema.dump(users)