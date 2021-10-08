from flask_restful import Resource
from flask import request, Response, jsonify
from schemas.phone import PhoneSchema
from models.phone import PhoneModel
from extensions import api
import validators

phone_schema = PhoneSchema(partial=True)
phone_list_schema = PhoneSchema(many=True)

class Phone(Resource):

    def post(self):
        requested_data = request.get_json()
        phone = PhoneModel.get_phone_by_id(requested_data['id'])
        return phone_schema.dump(phone), 200

    def put(self):
        phone = phone_schema.load(request.get_json())
        if(validators.check_phone(phone.number)):
            phone.save()
            return {"message": "Телефон добавлен"}, 201
        else:
            return {"message": "Телефон не добавлен"}, 400

    def patch(self):
        requested_data = request.get_json()
        phone = PhoneModel.get_phone_by_id(requested_data["id"])
        phone.user_id = requested_data["user_id"]
        phone.category = requested_data["category"]
        phone.number = requested_data["number"]
        if(validators.check_phone(phone.number)):
            phone.save()
            return {"message": "Телефон обновлен"}, 201
        else:
            return {"message": "Телефон не обновлен"}, 400

    def delete(self):
        requested_data = request.get_json()
        phone = PhoneModel.get_phone_by_id(requested_data["id"])
        phone.delete()
        return {"message": "Телефон удален"}, 201

class PhoneList(Resource):
    
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            phones = PhoneModel.get_all_phones(sort_by=reqested_data["sort_by"])
        else:
            phones = PhoneModel.get_all_phones()
        return phone_list_schema.dump(phones)