from flask import render_template
from . import validation

@validation.route('/')
def validation_home():
  return render_template('validation/validate_metadata.html')