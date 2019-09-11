import logging
import pandas as pd
from flask import render_template,flash,redirect,url_for,request
from . import covcalculator
from ..models import Platform,Assay_type
from flask_wtf import FlaskForm
from wtforms.fields import StringField,SubmitField,IntegerField,RadioField,DecimalField
from wtforms.validators import DataRequired,InputRequired,NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .utils import calculate_expected_lanes,calculate_expected_lanes_for_known_library
from .utils import calculate_expected_samples,calculate_expected_samples_for_known_library

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
				('sample_number','I have fixed number of samples')],
			default='lane_number',
			id='choose_sample_or_lane')
	samples = \
		IntegerField(\
			label='sample or lane number',
			default=1,
			validators=[DataRequired(),NumberRange()],
			id='samples')
	submit = SubmitField('Get info')


@covcalculator.route('/')
def covcalculator_home():
  try:
    platform = ''
    choose_assay = ''
    genome_size = 0
    coverage = 0
    samples = 0
    choose_sample_or_lane = ''
    output_per_unit = 0
    required_lane_per_sample = 0
    samples_per_lanes = 0
    expected_lanes = 0
    expected_samples = 0
    expected_read_count = 0
    recommended_clusters = 0
    data_table = ''
    form = SeqrunForm()
    if form.validate_on_submit():
      platform = form.platform.data
      genome_size = form.genome_size.data
      coverage = form.coverage.data
      samples = form.samples.data
      assay_type = form.assay_type.data
      choose_sample_or_lane = form.choose_sample_or_lane.data
      cluster_size = platform.clusters
      is_pe = platform.is_pe
      read_length = platform.read_length
      choose_assay = form.choose_assay.data
      expected_read_count = form.expected_read_count.data
      recommended_clusters = assay_type.read_count
      col_order = ['Platform name']
      if choose_assay == 'library_type':
        if genome_size >0 or \
           coverage > 0 or \
           expected_read_count > 0:
          flash('Ignoring genome size, coverage and expected read counts for known library type')

        if choose_sample_or_lane == 'sample_number':
          required_lane_per_sample,samples_per_lanes,samples_count,expected_lanes = \
            calculate_expected_lanes_for_known_library(\
              recommended_clusters=recommended_clusters,
              samples_count=samples,
              cluster_size=cluster_size)
          data_table = \
            [{'Platform name':platform.name,
              'Library type': assay_type.assay_name,
              'Recommended cluster count per sample': assay_type.read_count,
              'Required lane per sample':required_lane_per_sample,
              'Samples per lane':samples_per_lanes,
              'Requested samples':samples_count,
              'Expected lanes':expected_lanes}]
          col_order = \
            ['Library type',
             'Recommended cluster count per sample',
             'Required lane per sample',
             'Samples per lane',
             'Requested samples',
             'Expected lanes']
          flash('Success')
        elif choose_sample_or_lane == 'lane_number':
          required_lane_per_sample,samples_per_lanes,lanes_count,expected_samples = \
            calculate_expected_samples_for_known_library(\
              recommended_clusters=recommended_clusters,
              lanes_count=samples,
              cluster_size=cluster_size)
          data_table = \
            [{'Platform name':platform.name,
              'Library type': assay_type.assay_name,
              'Recommended cluster count per sample': assay_type.read_count,
              'Required lane per sample':required_lane_per_sample,
              'Samples per lane':samples_per_lanes,
              'Requested lanes':lanes_count,
              'Expected samples':expected_samples}]
          col_order = \
            ['Library type',
             'Recommended cluster count per sample',
             'Required lane per sample',
             'Samples per lane',
             'Requested lanes',
             'Expected samples']
          flash('Success')
      elif choose_assay == 'genome_cov':
        if expected_read_count > 0:
          flash('Ignoring costom read count per sample')

        if genome_size==0 or coverage==0:
          flash('Failed: Missing genome size and coverage')
        else:
          if choose_sample_or_lane == 'sample_number':
            output_per_unit,required_lane_per_sample,samples_per_lanes,samples_count,expected_lanes = \
              calculate_expected_lanes(\
                genome_size=genome_size,
                coverage=coverage,
                samples_count=int(samples),
                cluster_size=int(cluster_size),
                is_pe=int(is_pe),
                read_length=int(read_length))
            data_table = \
              [{'Platform name':platform.name,
                'Genome size (MB)': genome_size,
                'Output per unit':output_per_unit,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested samples':samples_count,
                'Expected lanes':expected_lanes}]
            col_order = \
              ['Genome size (MB)',
               'Output per unit',
               'Required lane per sample',
               'Samples per lane',
               'Requested samples',
               'Expected lanes']
            flash('Success')
          elif choose_sample_or_lane == 'lane_number':
            output_per_unit,required_lane_per_sample,samples_per_lanes,lanes_count,expected_samples = \
              calculate_expected_samples(\
                genome_size=genome_size,
                coverage=coverage,
                lanes_count=samples,
                cluster_size=cluster_size,
                read_length=read_length,
                is_pe=is_pe)
            data_table = \
              [{'Platform name':platform.name,
                'Genome size (MB)': genome_size,
                'Output per unit':output_per_unit,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested lanes':lanes_count,
                'Expected samples':expected_samples}]
            col_order = \
              ['Genome size (MB)',
               'Output per unit',
               'Required lane per sample',
               'Samples per lane',
               'Requested lanes',
               'Expected samples']
            flash('Success')
      elif choose_assay == 'custom_read':
        if genome_size > 0 or \
           coverage > 0 :
          flash('Ignoring genome size, coverage for custom read library')

        if expected_read_count == 0 or \
           expected_read_count is None or \
           expected_read_count == '':
          flash('Failed: Missing required read counts per sample')
        else:
          if choose_sample_or_lane == 'sample_number':
            required_lane_per_sample,samples_per_lanes,samples_count,expected_lanes = \
              calculate_expected_lanes_for_known_library(\
                recommended_clusters=expected_read_count,
                samples_count=samples,
                cluster_size=cluster_size)
            data_table = \
              [{'Platform name':platform.name,
                'Requested cluster count per sample':expected_read_count,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested lanes':samples_count,
                'Expected samples':expected_lanes}]
            col_order = \
              ['Requested cluster count per sample',
               'Required lane per sample',
               'Samples per lane',
               'Requested lanes',
               'Expected samples']
            flash('Success')
          else:
            flash('Failed: Select output mode as sample, for custom read count per sample')
    else:
      if request.method=='POST':
        flash('Failed: Input validation failed')
        return redirect(url_for('covcalculator_home'))

    formatted_header_list = \
      ['Output per unit',
       'Requested cluster count per sample',
       'Recommended cluster count per sample']
    if data_table !='' and isinstance(data_table,list):
      data_table = pd.DataFrame(data_table).set_index('Platform name')
      for header in formatted_header_list:
        if header in data_table.columns:
          data_table[header] = data_table[header].astype(int).map(lambda x: '{0:,}'.format(x))

      data_table = \
        data_table[col_order].\
        T.\
        to_html(\
          classes='table table-striped table-hover',
          border=0,
          justify='left')
    return render_template(\
             'covcalculator/sequencing_coverage_calculator.html',
             form=form,
             platform=platform,
             output_per_unit=output_per_unit,
             required_lane_per_sample=required_lane_per_sample,
             samples_per_lanes=samples_per_lanes,
             samples_count=samples,
             lanes_count=samples,
             expected_lanes=expected_lanes,
             expected_samples=expected_samples,
             coverage=coverage,
             genome_size=genome_size,
             choose_assay=choose_assay,
             data_table=data_table,
             choose_sample_or_lane=choose_sample_or_lane)
  except Exception as e:
    logging.warning('Failed to claculate coverage, error: {0}'.format(e))