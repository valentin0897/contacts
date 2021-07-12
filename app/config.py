username = "valentin"
password = "1234"
db_name = "contacts"

class Config():
    DEBUG = True
    SECRET_KEY = 'S65p4oeVQRRY8n'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{username}:{password}@localhost/{db_name}" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False