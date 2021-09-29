from flask_restful import Resource
from flask import request, jsonify, Response
from models.user import UserModel
from models.phone import PhoneModel
from models.email import EmailModel
from extensions import api
import validators

class User(Resource):
    def post(self):
        requested_data = request.get_json()
        user = UserModel.get_user(requested_data['id'])
        json = jsonify(user)
        return json 


    def put(self):
        requested_data = request.get_json()

        if(validators.check_user(requested_data['fio'],
        requested_data['avatar_path'], requested_data['sex'], 
        requested_data['birthday'], requested_data['address'])):

            new_user = UserModel.add_user(requested_data['fio'], requested_data['avatar_path'],
            requested_data['sex'], requested_data['birthday'],
            requested_data['address'])

            if("phones" in requested_data):
                for phone in requested_data['phones']:
                    if(validators.check_phone(phone['number'])):
                        PhoneModel.add_phone(new_user.id,
                        phone['type'], phone['number'])

            if("emails" in requested_data):
                for email in requested_data['emails']:
                    if(validators.check_email(email['email'])):
                        EmailModel.add_email_to_db(new_user.id,
                        email['type'], email['email'])

            response = Response('Пользователь добавлен', 201, mimetype='application/json')
            return response
        else:
            response = Response('Пользователь не добавлен', 400, mimetype='application/json')
            return response

    def patch(self):
        requested_data = request.get_json()
        if(validators.check_user(requested_data['fio'],
        requested_data['avatar_path'], requested_data['sex'], 
        requested_data['birthday'], requested_data['address'])):
            UserModel.update_user(requested_data['id'], requested_data['fio'], requested_data['avatar_path'],
            requested_data['sex'], requested_data['birthday'],
            requested_data['address'])
            response = Response('Пользователь обновлен', 202, mimetype='application/json')
            return response
        else:
            response = Response('Пользователь не обновлен', 400, mimetype='application/json')
            return response

    def delete(self):
        requested_data = request.get_json()
        UserModel.delete_user(requested_data['id'])
        response = Response('Пользователь удален', 200, mimetype='application/json')
        return response

class UserList(Resource):
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            json = jsonify({'Users': UserModel.get_all_users(sort_by=reqested_data['sort_by'])})
        else:
            json = jsonify({'Users': UserModel.get_all_users()})
        return json