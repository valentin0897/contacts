from flask import Flask
from extensions import db, migrate
from config import Config
from flask import request, Response, jsonify
import models, generate, validators

def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    register_extensions(app)
    return app

app = create_app(Config)

# -----User------
@app.route('/users', methods=['POST'])
def get_users():
    reqested_data = request.get_json()
    if "field" in reqested_data:
        json = jsonify({'Users': models.User.get_all_users(field=reqested_data['field'],
        order=reqested_data['order'])})
    else:
        json = jsonify({'Users': models.User.get_all_users()})
    return json

@app.route('/user', methods=['POST'])
def get_user_by_id():
    requested_data = request.get_json()
    user = models.User.get_user(requested_data['id'])
    json = jsonify(user)
    return json 

@app.route('/user', methods=['PUT'])
def add_user():
    requested_data = request.get_json()

    if(validators.check_user(requested_data['fio'],
    requested_data['avatar_path'], requested_data['sex'], 
    requested_data['birthday'], requested_data['address'])):

        new_user = models.User.add_user(requested_data['fio'], requested_data['avatar_path'],
        requested_data['sex'], requested_data['birthday'],
        requested_data['address'])

        if("phones" in requested_data):
            for phone in requested_data['phones']:
                if(validators.check_phone(phone['number'])):
                    models.Phone.add_phone(new_user.id,
                    phone['type'], phone['number'])
                
        if("emails" in requested_data):
            for email in requested_data['emails']:
                if(validators.check_email(email['email'])):
                    models.Email.add_email(new_user.id,
                    email['type'], email['email'])
        
        response = Response('Пользователь добавлен', 201, mimetype='application/json')
        return response
    else:
        response = Response('Пользователь не добавлен', 400, mimetype='application/json')
        return response

@app.route('/user', methods=['PATCH'])
def update_user():
    requested_data = request.get_json()
    if(validators.check_user(requested_data['fio'],
    requested_data['avatar_path'], requested_data['sex'], 
    requested_data['birthday'], requested_data['address'])):
        models.User.update_user(requested_data['id'], requested_data['fio'], requested_data['avatar_path'],
        requested_data['sex'], requested_data['birthday'],
        requested_data['address'])
        response = Response('Пользователь обновлен', 202, mimetype='application/json')
        return response
    else:
        response = Response('Пользователь не обновлен', 400, mimetype='application/json')
        return response

@app.route('/user', methods=['DELETE'])
def delete_user():
    requested_data = request.get_json()
    models.User.delete_user(requested_data['id'])
    response = Response('Пользователь удален', 200, mimetype='application/json')
    return response

# -----Phone-----
@app.route('/phones', methods=['POST'])
def get_phones():
    reqested_data = request.get_json()
    if "field" in reqested_data:
        json = jsonify({'Phones': models.Phone.get_all_phones(field=reqested_data['field'],
        order=reqested_data['order'])})
    else:
        json = jsonify({'Phones': models.Phone.get_all_phones()})
    return json

@app.route('/phone', methods=['POST'])
def get_phone():
    requested_data = request.get_json()
    phone = models.Phone.get_phone(requested_data['id'])
    json = jsonify(phone)
    return json

@app.route('/phone', methods=['PUT'])
def add_phone():
    requested_data = request.get_json()
    if(validators.check_phone(requested_data['number'])):
        models.Phone.add_phone(requested_data['user_id'],
        requested_data['type'], requested_data['number'])
        response = Response('Телефон добавлен', 201, mimetype='application/json')
        return response
    else:
        response = Response('Телефон не добавлен', 400, mimetype='application/json')
        return response

@app.route('/phone', methods=['PATCH'])
def update_phone():
    requested_data = request.get_json()
    if(validators.check_phone(requested_data['number'])):
        models.Phone.update_phone(requested_data['id'],
        requested_data['user_id'], requested_data['type'], requested_data['number'])
        response = Response('Телефон обновлен', 202, mimetype='application/json')
        return response
    else:
        response = Response('Телефон не обновлен', 400, mimetype='application/json')
        return response

@app.route('/phone', methods=['DELETE'])
def delete_phone():
    requested_data = request.get_json()
    models.Phone.delete_phone(requested_data['id'])
    response = Response('Телефон удален', 200, mimetype='application/json')
    return response


# -----Email------
@app.route('/emails', methods=['POST'])
def get_emails():
    reqested_data = request.get_json()
    if "field" in reqested_data:
        json = jsonify({'Emails': models.Email.get_all_emails(field=reqested_data['field'],
        order=reqested_data['order'])})
    else:
        json = jsonify({'Emails': models.Email.get_all_emails()})
    return json

@app.route('/email', methods=['POST'])
def get_email():
    requested_data = request.get_json()
    email = models.Email.get_email(requested_data['id'])
    json = jsonify(email)
    return json

@app.route('/email', methods=['PUT'])
def add_email():
    requested_data = request.get_json()
    if(validators.check_email(requested_data['email'])):
        models.Email.add_email(requested_data['user_id'],
        requested_data['type'], requested_data['email'])
        response = Response('Email добавлен', 201, mimetype='application/json')
        return response
    else:
        response = Response('Email не добавлен', 400, mimetype='application/json')
        return response


@app.route('/email', methods=['PATCH'])
def update_email():
    requested_data = request.get_json()
    if(validators.check_email(requested_data['email'])):
        models.Email.update_email(requested_data['id'],
        requested_data['user_id'], requested_data['type'], requested_data['email'])
        response = Response('Email обновлен', 202, mimetype='application/json')
        return response
    else:
        response = Response('Email не обновлен', 400, mimetype='application/json')
        return response


@app.route('/email', methods=['DELETE'])
def delete_email():
    requested_data = request.get_json()
    models.Email.delete_email(requested_data['id'])
    response = Response('Email удален', 200, mimetype='application/json')
    return response


app.run()