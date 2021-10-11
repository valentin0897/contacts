from flask_restful import Resource
from flask import request
from marshmallow.exceptions import ValidationError
from app.resources.email import EMAIL_NOT_FOUND
from schemas.phone import PhoneSchema
from models.phone import PhoneModel
import validators

phone_schema = PhoneSchema(partial=True)
phone_list_schema = PhoneSchema(many=True)

PHONE_NOT_FOUND = "Phone not found"
PHONE_DELETED = "Phone deleted"
PHONE_ERROR_INSERTING = "An error occured while inserting the phone"
PHONE_ERROR_UPDATING = "An error occured while updating the phone"

class Phone(Resource):

    def post(self):
        id_ = request.get_json()['id']
        errors = phone_schema.validate({"id": id_})
        if errors:
            return {"message": PHONE_NOT_FOUND, "errors": errors}, 400
        else:
            phone = PhoneModel.get_phone_by_id(id_)
            return phone_schema.dump(phone), 200

    def put(self):
        try:
            phone = phone_schema.load(request.get_json())
        except ValidationError as errors:
            return {"message": PHONE_ERROR_INSERTING, "errors": errors.messages}, 400
        phone.save()
        return phone_schema.dump(phone), 201

    def patch(self):
        requested_data = request.get_json()
        errors = phone_schema.validate(requested_data)
        if errors:
            return {"message": PHONE_ERROR_UPDATING, "errors": errors}, 400

        phone = PhoneModel.get_phone_by_id(requested_data["id"])
        phone.user_id = requested_data["user_id"]
        phone.category = requested_data["category"]
        phone.number = requested_data["number"]
        phone.save()
        return phone_schema.dump(phone), 202

    def delete(self):
        requested_data = request.get_json()
        phone = PhoneModel.get_phone_by_id(requested_data["id"])
        if phone:
            phone.delete()
            return {"message": PHONE_DELETED}, 201
        else:
            return {"message": EMAIL_NOT_FOUND}, 404

class PhoneList(Resource):
    
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            phones = PhoneModel.get_all_phones(sort_by=reqested_data["sort_by"])
        else:
            phones = PhoneModel.get_all_phones()
        return phone_list_schema.dump(phones)