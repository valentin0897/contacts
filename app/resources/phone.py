from flask_restful import Resource
from flask import request, Response, jsonify
from models.phone import PhoneModel
from extensions import api
import validators

class Phone(Resource):
    def post(self):
        requested_data = request.get_json()
        phone = PhoneModel.get_phone(requested_data['id'])
        json = jsonify(phone)
        return json

    def put(self):
        requested_data = request.get_json()
        if(validators.check_phone(requested_data['number'])):
            PhoneModel.add_phone(requested_data['user_id'],
            requested_data['type'], requested_data['number'])
            response = Response('Телефон добавлен', 201, mimetype='application/json')
            return response
        else:
            response = Response('Телефон не добавлен', 400, mimetype='application/json')
            return response

    def patch(self):
        requested_data = request.get_json()
        if(validators.check_phone(requested_data['number'])):
            PhoneModel.update_phone(requested_data['id'],
            requested_data['user_id'], requested_data['type'], requested_data['number'])
            response = Response('Телефон обновлен', 202, mimetype='application/json')
            return response
        else:
            response = Response('Телефон не обновлен', 400, mimetype='application/json')
            return response

    def delete(self):
        requested_data = request.get_json()
        PhoneModel.delete_phone(requested_data['id'])
        response = Response('Телефон удален', 200, mimetype='application/json')
        return response

class PhoneList(Resource):
    
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            json = jsonify({'Phones': PhoneModel.get_all_phones(sort_by=reqested_data['sort_by'])})
        else:
            json = jsonify({'Phones': PhoneModel.get_all_phones()})
        return json