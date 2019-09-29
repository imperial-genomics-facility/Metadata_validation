import os,uuid

BASEDIR = os.path.dirname(__file__)

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or uuid.uuid4().hex         # default uuid, if not provided
  FLASK_INSTANCE_PATH = os.environ.get('FLASK_INSTANCE_PATH') or BASEDIR
  SAMPLESHEET_SCHEMA = os.environ.get('SAMPLESHEET_SCHEMA') or None
  METADATA_SCHEMA = os.environ.get('METADATA_SCHEMA') or None
  RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or None
  RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or None
  RECAPTCHA_API_SERVER = os.environ.get('RECAPTCHA_API_SERVER') or 'https://www.google.com/recaptcha/api/siteverify'
  SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False

  @staticmethod
  def init_app(app):
    pass

class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                            'sqlite:////{0}/dev_database.sqlite'.format(BASEDIR)

class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                            'sqlite:////{0}/dev_database.sqlite'.format(BASEDIR)


class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or None

class CloudConfiig(ProdConfig):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or None

  @classmethod
  def init_app(cls,app):
    import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

config = {'development':DevConfig,
          'testing':TestConfig,
          'production':ProdConfig,
          'cloud':CloudConfiig
          }