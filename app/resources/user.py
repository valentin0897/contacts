from flask_restful import Resource
from flask import request
from schemas.user import UserSchema
from schemas.phone import PhoneSchema
from schemas.email import EmailSchema
from models.user import UserModel
from models.phone import PhoneModel
from models.email import EmailModel
import validators

user_schema = UserSchema(partial=True)
user_list_schema = UserSchema(many=True)
phone_schema = PhoneSchema(partial=True)
email_shcema = EmailSchema(partial=True)

class User(Resource):
    def post(self):
        requested_data = request.get_json()
        user = UserModel.get_user_by_id(requested_data['id'])
        return user_schema.dump(user), 200 


    def put(self):
        requested_data = request.get_json()
        phones = requested_data.pop("phones")
        emails = requested_data.pop("emails")
        user = user_schema.load(requested_data)

        if(user):
            user.save()
            if (phones):
                for number in phones:
                    phone = phone_schema.load({"user_id": user.id, "number": number, "category": True})
                    phone.save()
            
            if (emails):
                for email_name in emails:
                    email = phone_schema.load({"user_id": user.id, "email": email_name, "category": True})
                    email.save()

            return {"message": "Пользователь добавлен"}, 201
        else:
            return {"message": "Пользователь не добавлен"}, 400

    def patch(self):
        requested_data = request.get_json()
        user = UserModel.get_user_by_id(requested_data["id"])
        user.fio = requested_data["fio"]
        user.avatar_path = requested_data["avatar_path"]
        user.sex = requested_data["sex"]
        user.birthday = requested_data["birthday"]
        user.address = requested_data["address"]
        if(user):
            user.save()
            return {"message": "Пользователь обновлен"}, 201
        else:
            return {"message": "Пользователь не обновлен"}, 201

    def delete(self):
        requested_data = request.get_json()
        user = UserModel.get_user_by_id(requested_data['id'])
        user.delete()
        return {"message": "Пользователь удален"}, 201

class UserList(Resource):
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            users = UserModel.get_all_users(sort_by=reqested_data['sort_by'])
        else:
            users = UserModel.get_all_users()
        return user_list_schema.dump(users)