import os,uuid

BASEDIR = os.path.dirname(__file__)

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or uuid.uuid4().hex()         # default uuid, if not provided

  @staticmethod
  def init_app(app):
    pass

class DevConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
                            os.path.join(BASEDIR,'dev_database.sqlite')

class TestConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or \
                            os.path.join(BASEDIR,'test_database.sqlite')

class ProdConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI') or None
  USE_RECAPTCHA = os.environ.get('USE_RECAPTCHA') or False                # reCAPTCHA is optional for prod
  RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or None
  RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or None
  RECAPTCHA_API_SERVER = os.environ.get('RECAPTCHA_API_SERVER') or 'https://www.google.com/recaptcha/api/siteverify'

class CloudConfiig(ProdConfig):
  USE_RECAPTCHA = True                                                     # use reCAPTCHA on cloud

config = {'development':DevConfig,
          'testing':TestConfig,
          'production':ProdConfig,
          'cloud':CloudConfiig
          }