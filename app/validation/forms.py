from flask_wtf import FlaskForm,RecaptchaField
from wtforms.fields import FileField,SubmitField,MultipleFileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed,FileRequired

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