import io,os,logging
from . import metadata
from flask import render_template,flash,Response,request
from flask_wtf import FlaskForm
from wtforms.fields import FileField,SubmitField,MultipleFileField
from flask_wtf.file import FileAllowed,FileRequired
from werkzeug.utils import secure_filename
from igf_data.utils.fileutils import get_temp_dir,remove_dir
from igf_data.process.metadata_reformat.reformat_metadata_file import Reformat_metadata_file,EXPERIMENT_TYPE_LOOKUP,SPECIES_LOOKUP,METADATA_COLUMNS

class MetadataForm(FlaskForm):
  metadata_file = \
    FileField(\
      'Metadata csv file',
      validators=[FileAllowed(['csv']),FileRequired()])
  submit = SubmitField('Reformat metadata')


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

@metadata.route('/',methods=['GET','POST'])
def metadata_home():
  try:
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
      metadata_output = \
        os.path.join(\
          temp_dir,
          'reformatted_metadata.csv')
      re_metadata = \
        Reformat_metadata_file(\
          infile=new_metadata_file,
          experiment_type_lookup=EXPERIMENT_TYPE_LOOKUP,
          species_lookup=SPECIES_LOOKUP,
          metadata_columns=METADATA_COLUMNS)
      re_metadata.\
        reformat_raw_metadata_file(output_file=metadata_output)
      csv_data = convert_file_to_stream(infile=metadata_output)
      remove_dir(temp_dir)
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