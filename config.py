import os

SQLALCHEMY_DATABASE_URI = "postgresql://bendebebe:chelsea@localhost/tally-up"
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