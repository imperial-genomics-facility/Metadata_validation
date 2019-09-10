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

  return app