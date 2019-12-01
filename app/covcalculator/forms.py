from ..models import Platform,Assay_type
from flask_wtf import FlaskForm
from wtforms.fields import StringField,SubmitField,IntegerField,RadioField,DecimalField
from wtforms.validators import DataRequired,InputRequired,NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField

def platform_check():
  return Platform.query

def assay_check():
  return Assay_type.query

class SeqrunForm(FlaskForm):
  platform = \
    QuerySelectField(\
      query_factory=platform_check,
      get_label='name',
      id='platform')
  choose_assay = \
    RadioField(\
      choices = [ \
        ('library_type','Use recommended clusters for known library type'),
        ('genome_cov','Calculate output based on genome coverage'),
        ('custom_read','Use custom read counts per sample')],
      id='choose_assay')
  assay_type = \
    QuerySelectField(\
      query_factory=assay_check,
      label='select assay',
      get_label='assay_name',
      id='assay_type')
  genome_size = \
    DecimalField(\
      label='Genome size (MB)',
      default=0.0,
      places=1,
      validators=[NumberRange(min=0)],
      id='genome_size')
  coverage = \
    IntegerField(\
      label='coverage',
      default=0,
      validators=[NumberRange()],
      id='coverage')
  expected_read_count = \
    IntegerField(\
      label='Expected read count (million)',
      default=0,
      validators=[NumberRange()],
      id='expected_read_count')
  choose_sample_or_lane = \
    RadioField(\
      choices=[\
        ('lane_number','I will sequence following lanes'),
        ('sample_number','I have fixed number of samples (or cells)')],
      default='lane_number',
      id='choose_sample_or_lane')
  samples = \
    IntegerField(\
      label='sample or lane number',
      default=1,
      validators=[DataRequired(),NumberRange()],
      id='samples')
  max_samples = \
    IntegerField(\
      label='max samples per flowcell',
      default=96,
      validators=[DataRequired(),NumberRange()],
      id='max_samples')
  submit = SubmitField('Get info')