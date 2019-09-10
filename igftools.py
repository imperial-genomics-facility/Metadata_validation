import os
from app import create_app

flask_config_name = os.environ.get('FLASK_CONFIG') or 'testing'
app = create_app(config_name=flask_config_name)