import os
from flask_migrate import Migrate, upgrade
from app import create_app, db

flask_config_name = os.environ.get('FLASK_CONFIG') or 'testing'
app = create_app(config_name=flask_config_name)
migrate = Migrate(app, db)