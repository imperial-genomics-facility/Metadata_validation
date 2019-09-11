from . import metadata
from flask import render_template

@metadata.route('/')
def metadata_home():
  return render_template('metadata/metadata_reformat.html')