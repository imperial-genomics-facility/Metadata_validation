from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
moment = Moment()
csrfprotect = CSRFProtect()
db = SQLAlchemy()

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  bootstrap.init_app(app)
  moment.init_app(app)
  csrfprotect.init_app(app)
  db.init_app(app)
  
  ## Load Blueprint modules
  from .metadata import metadata as metadata_blueprint
  app.register_blueprint(metadata_blueprint)
  from .samplesheet import samplesheet as samplesheet_blueprint
  app.register_blueprint(samplesheet_blueprint)
  from .validation import validation as validation_blueprint
  app.register_blueprint(validation_blueprint)
  from .covcalculator import covcalculator as covcalculator_blueprint
  app.register_blueprint(covcalculator_blueprint)

  return app