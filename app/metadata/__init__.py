from flask import Blueprint

metadata = Blueprint('metadata',__name__)

from . import views