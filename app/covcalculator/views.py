from flask import render_template
from . import covcalculator

@covcalculator.route('/')
def covcalculator_home():
  return render_template('covcalculator/sequencing_coverage_calculator.html')