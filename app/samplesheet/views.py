from flask import render_template
from . import samplesheet 

@samplesheet.route('/')
def samplesheet_home():
  return render_template('samplesheet/samplesheet_reformat.html')