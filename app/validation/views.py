import os,logging
from flask import render_template,flash,request
from . import validation
from .forms import ValidationForm
from flask import current_app as app
from werkzeug.utils import secure_filename
from igf_data.utils.fileutils import get_temp_dir,remove_dir
from igf_data.utils.validation_check.metadata_validation import Validate_project_and_samplesheet_metadata


@validation.route('/',methods=['GET','POST'])
def validation_home():
  form = ValidationForm()
  if form.validate_on_submit():
    temp_dir = get_temp_dir()
    new_metadata_list = list()
    counter = 0
    for file in form.metadata_file.data:
      counter += 1
      filename = secure_filename(file.filename)
      file.save(\
        os.path.join(\
          temp_dir,
          '{0}_{1}'.format(counter,filename)))
      new_metadata_list.\
        append(\
          os.path.join(\
            temp_dir,
            '{0}_{1}'.format(counter,filename)))
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

