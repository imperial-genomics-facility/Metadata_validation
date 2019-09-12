from . import samplesheet
import io,os,logging
from flask import render_template,flash,Response,request
from flask_wtf import FlaskForm
from wtforms.fields import FileField,SubmitField,MultipleFileField
from flask_wtf.file import FileAllowed,FileRequired
from werkzeug.utils import secure_filename
from igf_data.utils.fileutils import get_temp_dir,remove_dir
from igf_data.process.metadata_reformat.reformat_samplesheet_file import Reformat_samplesheet_file

class SamplesheetForm(FlaskForm):
  samplesheet_file = \
    FileField(\
      'Samplesheet csv file',
      validators=[FileAllowed(['csv']),FileRequired()])
  submit = SubmitField('Reformat samplesheet')


def convert_file_to_stream(infile):
  try:
    data = ''
    with open(infile,'r') as file_i:
      with io.StringIO() as file_o:
        for line in file_i:
          file_o.write(line)

        data = file_o.getvalue()
    return data
  except Exception as e:
    raise ValueError('Failedto convert file to stream, error: {0}'.format(e))

@samplesheet.route('/',methods=['GET','POST'])
def samplesheet_home():
  try:
    form = SamplesheetForm()
    if form.validate_on_submit():
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
      re_samplesheet = \
        Reformat_samplesheet_file(\
          infile=new_samplesheet_file)
      re_samplesheet.\
      reformat_raw_samplesheet_file(\
        output_file=samplesheet_output)
      csv_data = \
        convert_file_to_stream(infile=samplesheet_output)
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
