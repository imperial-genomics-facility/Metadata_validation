import os,logging
from . import metadata
from .utils import run_metadata_reformatting
from flask import render_template,flash,Response,request
from flask_wtf import FlaskForm,RecaptchaField
from wtforms.fields import FileField,SubmitField,MultipleFileField
from flask_wtf.file import FileAllowed,FileRequired
from werkzeug.utils import secure_filename
from igf_data.utils.fileutils import get_temp_dir,remove_dir


class MetadataForm(FlaskForm):
  metadata_file = \
    FileField(\
      'Metadata csv file',
      validators=[FileAllowed(['csv']),FileRequired()])
  recaptcha = RecaptchaField()
  submit = SubmitField('Reformat metadata')


@metadata.route('/',methods=['GET','POST'])
def metadata_home():
  try:
    csv_data = ''
    form = MetadataForm()
    if form.validate_on_submit():
      temp_dir = get_temp_dir()
      metadata_filename = \
        secure_filename(form.metadata_file.data.filename)
      form.metadata_file.\
        data.save(\
          os.path.join(\
            temp_dir,
            metadata_filename))
      new_metadata_file = \
        os.path.join(\
          temp_dir,
          metadata_filename)
      try:
        csv_data = \
          run_metadata_reformatting(\
            metadata_file=new_metadata_file,\
            output_dir=temp_dir)
      except Exception as e:
        flash('Failed metadata file reformatting')
        logging.warning(e)
      remove_dir(temp_dir)
      if csv_data != '':
        return \
          Response(\
            csv_data,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=reformatted_metadata.csv"})
    else:
      if request.method=='POST':
        flash('Failed file type validation check')
  except Exception as e:
    logging.warning('Failed metadata reformatting, error: {0}'.format(e))

  return render_template('metadata/metadata_reformat.html',form=form)