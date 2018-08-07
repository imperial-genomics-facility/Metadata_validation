import os
from flask import Flask
from flask import request
from flask import session
from flask import render_template
from flask import redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField,SubmitField,MultipleFileField
from wtforms.validators import DataRequired,Regexp
from igf_data.utils.fileutils import get_temp_dir,remove_dir
from igf_data.utils.tools.metadata_validation import Validate_project_and_samplesheet_metadata

app=Flask(__name__,instance_path=os.environ['FLASK_INSTANCE_PATH'])
app.config['SECRET_KEY']=os.environ['FLASK_SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY']=os.environ['FLASK_CSRF_SECRET_KEY']
bootstrap=Bootstrap(app)

class ValidationForm(FlaskForm):
  metadata_file=MultipleFileField(\
                  'Metadata csv file',
                  validators=[DataRequired()]
                )
  samplesheet_file=FileField(\
                     'Samplesheet csv file',
                     validators=[DataRequired()]
                   )
  submit = SubmitField('Validate metadata')

@app.route('/results',methods=['GET','POST'])
def results(json_data):
  return render_template('results.html',jsonData=json_data)

@app.route('/',methods=['GET','POST'])
def index():
  metadata_files=None
  samplesheet_file=None
  form=ValidationForm()
  if form.validate_on_submit():
    temp_dir=get_temp_dir(work_dir=app.instance_path)
    new_metadata_list=list()
    for file in form.metadata_file.data:
      filename=secure_filename(file.filename)
      file.save(os.path.join(temp_dir,
                             filename
                            ))
      new_metadata_list.append(os.path.join(temp_dir,
                                            filename))

    samplesheet_filename=secure_filename(form.samplesheet_file.data.filename)
    form.samplesheet_file.data.save(os.path.join(temp_dir,
                                                 samplesheet_filename
                                                ))
    new_samplesheet=os.path.join(temp_dir,
                                 samplesheet_filename)
    vp=Validate_project_and_samplesheet_metadata(\
         samplesheet_file=new_samplesheet,
         metadata_files=new_metadata_list,
         samplesheet_schema=os.environ['SAMPLESHEET_SCHEMA'],
         metadata_schema=os.environ['METADATA_SCHEMA']
       )
    json_data=vp.convert_errors_to_gviz()
    remove_dir(temp_dir)
    return render_template('results.html',
                           jsonData=json_data)
  return render_template('index.html',
                         form=form,
                         title_name='Hello!')