import os,logging
from flask import render_template,flash,request
from . import validation
from flask import current_app as app
from flask_wtf import FlaskForm,RecaptchaField
from wtforms.fields import FileField,SubmitField,MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed,FileRequired
from werkzeug.utils import secure_filename
from igf_data.utils.fileutils import get_temp_dir,remove_dir
from igf_data.utils.validation_check.metadata_validation import Validate_project_and_samplesheet_metadata

class ValidationForm(FlaskForm):
  metadata_file = \
    MultipleFileField(\
      'Metadata csv file(s)',
      validators=[DataRequired(),FileAllowed(['csv'])])
  samplesheet_file = \
    FileField(\
      'Samplesheet csv file',
      validators=[FileAllowed(['csv']),FileRequired()])
  recaptcha = RecaptchaField()
  submit = SubmitField('Validate metadata')

@validation.route('/',methods=['GET','POST'])
def validation_home():
  form = ValidationForm()
  if form.validate_on_submit():
    temp_dir = get_temp_dir()
    new_metadata_list = list()
    for file in form.metadata_file.data:
      filename = secure_filename(file.filename)
      file.save(\
        os.path.join(\
          temp_dir,
          filename))
      new_metadata_list.\
        append(\
          os.path.join(\
            temp_dir,
            filename))
      samplesheet_filename = \
        secure_filename(form.samplesheet_file.data.filename)
      form.samplesheet_file.\
        data.save(\
          os.path.join(\
            temp_dir,
            samplesheet_filename))
      new_samplesheet = \
        os.path.join(\
          temp_dir,
          samplesheet_filename)
      logging.warning(form.recaptcha.errors)
      vp = \
        Validate_project_and_samplesheet_metadata(\
          samplesheet_file=new_samplesheet,
          metadata_files=new_metadata_list,
          samplesheet_schema=app.config.get('SAMPLESHEET_SCHEMA'),
          metadata_schema=app.config.get('METADATA_SCHEMA'))
      json_data = vp.convert_errors_to_gviz()
      remove_dir(temp_dir)
      return render_template('validation/results.html',jsonData=json_data)
  else:
    if request.method=='POST':
      flash('Failed input validation check')
  return render_template('validation/validate_metadata.html',form=form)

