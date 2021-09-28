dialect_driver = "postgresql+psycopg2"
username = "username"
password = "1234"
db_name = "contacts"
host = "localhost"
port = "5432"
secret_key = "1234"

class Config():
    DEBUG = True
    SECRET_KEY = secret_key
    SQLALCHEMY_DATABASE_URI = f"{dialect_driver}://{username}:{password}@{host}:{port}/{db_name}" 
    SQLALCHEMY_TRACK_MODIFICATIONS = False