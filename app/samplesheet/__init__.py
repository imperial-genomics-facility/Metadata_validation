from flask import Blueprint

samplesheet = Blueprint('samplesheet',__name__)

from . import views