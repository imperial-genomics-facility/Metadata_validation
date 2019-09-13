from . import samplesheet
from .utils import run_samplesheet_reformatting
import os,logging
from flask import render_template,flash,Response,request
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import widgets
from wtforms.fields import FileField,SubmitField,SelectMultipleField
from flask_wtf.file import FileAllowed,FileRequired
from werkzeug.utils import secure_filename
from igf_data.utils.fileutils import get_temp_dir,remove_dir


class MultiCheckboxField(SelectMultipleField):
  widget = widgets.TableWidget()
  option_widget = widgets.CheckboxInput()


class SamplesheetForm(FlaskForm):
  samplesheet_file = \
    FileField(\
      'Samplesheet csv file',
      validators=[FileAllowed(['csv']),FileRequired()])
  select_opts = \
    MultiCheckboxField(\
      label='Additional options',\
        choices=[('revcomp_index1','Rev comp I7'),
                 ('revcomp_index2','Rev comp I5'),
                 ('remove_adapters','Remove Adapters')])
  recaptcha = RecaptchaField()
  submit = SubmitField('Reformat samplesheet')



@samplesheet.route('/',methods=['GET','POST'])
def samplesheet_home():
  try:
    csv_data = ''
    form = SamplesheetForm()
    selected_options = ''
    revcomp_index1 = False
    revcomp_index2 = False
    remove_adapters = False
    if form.validate_on_submit():
      selected_options = form.select_opts.data
      for opts in selected_options:
        if opts == 'revcomp_index1':
          revcomp_index1 = True
        if opts == 'revcomp_index2':
          revcomp_index2 = True
        if opts == 'remove_adapters':
          remove_adapters = True
      temp_dir = get_temp_dir()
      samplesheet_filename = \
        secure_filename(form.samplesheet_file.data.filename)
      form.samplesheet_file.\
        data.save(\
          os.path.join(\
            temp_dir,
            samplesheet_filename))
      new_samplesheet_file = \
        os.path.join(\
          temp_dir,
          samplesheet_filename)
      samplesheet_output = \
        os.path.join(\
          temp_dir,
          'reformatted_samplesheet.csv')
      logging.warning(\
        {'rev comp i7':revcomp_index1,
         'rev comp i5':revcomp_index2,
         'remove adaptors':remove_adapters
        })
      try:
        csv_data = \
          run_samplesheet_reformatting(\
            samplesheet_file=new_samplesheet_file,
            output_dir=temp_dir,
            revcomp_index1=revcomp_index1,
            revcomp_index2=revcomp_index2,
            remove_adapters=remove_adapters)
      except Exception as e:
        flash('Failed samplesheet reformatting')
        logging.warning(e)
      return \
        Response(\
               csv_data,
               mimetype="text/csv",
               headers={"Content-disposition":
                        "attachment; filename=reformatted_samplesheet.csv"})
    else:
      if request.method=='POST':
        flash('Failed file type validation check')
  except Exception as e:
    logging.warning('Failed samplesheet reformatting, error: {0}'.format(e))

  return render_template('samplesheet/samplesheet_reformat.html',form=form)
