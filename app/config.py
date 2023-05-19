import os 
from dotenv import load_dotenv

load_dotenv() 

class Config:
    API_TITLE = "USER API"
    API_VERSION = "1.0.0"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/apidocs"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False