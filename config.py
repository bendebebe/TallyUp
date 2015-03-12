import os

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = "postgresql://bendebebe:@localhost/tally-up"
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SECRET_KEY = '48205hrjf0238'

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

print(os.environ['DATABASE_URL'])
