from flask import Blueprint

covcalculator = Blueprint('covcalculator',__name__)

from . import views