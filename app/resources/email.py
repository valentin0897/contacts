from flask_restful import Resource
from models.email import EmailModel
from flask import Response, request, jsonify
from extensions import api
import validators

class Email(Resource):

    def post(self):
        requested_data = request.get_json()
        email = EmailModel.get_email_by_id(requested_data['id'])
        json = jsonify(email)
        return json

    def put(self):
        requested_data = request.get_json()
        if(validators.check_email(requested_data['email'])):
            EmailModel.add_email_to_db(requested_data['user_id'],
            requested_data['type'], requested_data['email'])
            response = Response('Email добавлен', 201, mimetype='application/json')
            return response
        else:
            response = Response('Email не добавлен', 400, mimetype='application/json')
            return response


    def patch(self):
        requested_data = request.get_json()
        if(validators.check_email(requested_data['email'])):
            EmailModel.update_email(requested_data['id'],
            requested_data['user_id'], requested_data['type'], requested_data['email'])
            response = Response('Email обновлен', 202, mimetype='application/json')
            return response
        else:
            response = Response('Email не обновлен', 400, mimetype='application/json')
            return response


    def delete(self):
        requested_data = request.get_json()
        EmailModel.delete_email(requested_data['id'])
        response = Response('Email удален', 200, mimetype='application/json')
        return response

class EmailList(Resource):
    
    def post(self):
        reqested_data = request.get_json()
        if "sort_by" in reqested_data:
            json = jsonify({'Emails': EmailModel.get_all_emails(sort_by=reqested_data["sort_by"])})
        else:
            json = jsonify({'Emails': EmailModel.get_all_emails()})
        return json