from decouple import config

class Config:
    SECRET_KEY = 'raypulido'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:cocacola09@localhost/web_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST_PORT = 9000
    
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Cocacola09@localhost/web_flask_test2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEST = True
    
config = {
    'development' : DevelopmentConfig,
    'default' : DevelopmentConfig,
    'test':TestConfig
}
