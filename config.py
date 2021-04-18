import os


class Config():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'key'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///static/db/test.db'
    WTF_CSRF_ENABLED = False
    UPLOAD_FOLDER = './app/static/files'

config = {
    'default': DevelopmentConfig
}