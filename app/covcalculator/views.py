import logging
import pandas as pd
from flask import render_template,flash,redirect,url_for,request
from . import covcalculator
from .forms import SeqrunForm,platform_check,assay_check
from .utils import calculate_expected_lanes,calculate_expected_lanes_for_known_library
from .utils import calculate_expected_samples,calculate_expected_samples_for_known_library,calculate_coverage_output


@covcalculator.route('/',methods=['GET','POST'])
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
    is_sc = 0
    max_samples = 0
    form = SeqrunForm()
    col_order = ['Platform name']
    if form.validate_on_submit():
      platform = form.platform.data
      genome_size = form.genome_size.data
      coverage = form.coverage.data
      samples = form.samples.data
      assay_type = form.assay_type.data
      choose_sample_or_lane = form.choose_sample_or_lane.data
      cluster_size = platform.clusters
      is_pe = platform.is_pe
      is_sc = assay_type.is_sc
      choose_assay = form.choose_assay.data
      expected_read_count = form.expected_read_count.data
      recommended_clusters = assay_type.read_count
      max_samples = form.max_samples.data
      platform_read_length = int(platform.read_length)
      data_table = dict()
      if choose_assay == 'library_type':
        if genome_size >0 or \
           coverage > 0 or \
           expected_read_count > 0:
          flash('Ignoring genome size, coverage and expected read counts for known library type')

        data_table,col_order,formatted_header_list = \
          calculate_coverage_output(
            platform_name=platform.name,
            cluster_size=cluster_size,
            platform_read_length=platform_read_length,
            choose_assay=choose_assay,
            choose_sample_or_lane=choose_sample_or_lane,
            recommended_clusters=recommended_clusters,
            samples=samples,
            is_sc=is_sc,
            max_samples=max_samples,
            assay_type_assay_name=assay_type.assay_name,
            expected_read_count=expected_read_count,
            genome_size=genome_size,
            coverage=coverage,
            is_pe=is_pe)
        flash('Success')
      elif choose_assay == 'genome_cov':
        if expected_read_count > 0:
          flash('Ignoring costom read count per sample')

        if genome_size==0 or coverage==0:
          flash('Failed: Missing genome size and coverage')
        else:
          data_table,col_order,formatted_header_list = \
            calculate_coverage_output(
              platform_name=platform.name,
              cluster_size=cluster_size,
              platform_read_length=platform_read_length,
              choose_assay=choose_assay,
              choose_sample_or_lane=choose_sample_or_lane,
              recommended_clusters=recommended_clusters,
              samples=samples,
              is_sc=is_sc,
              max_samples=max_samples,
              assay_type_assay_name=assay_type.assay_name,
              expected_read_count=expected_read_count,
              genome_size=genome_size,
              coverage=coverage,
              is_pe=is_pe)
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
            data_table,col_order,formatted_header_list = \
              calculate_coverage_output(
                platform_name=platform.name,
                cluster_size=cluster_size,
                platform_read_length=platform_read_length,
                choose_assay=choose_assay,
                choose_sample_or_lane=choose_sample_or_lane,
                recommended_clusters=recommended_clusters,
                samples=samples,
                is_sc=is_sc,
                max_samples=max_samples,
                assay_type_assay_name=assay_type.assay_name,
                expected_read_count=expected_read_count,
                genome_size=genome_size,
                coverage=coverage,
                is_pe=is_pe)
            flash('Success')
          else:
            flash('Failed: Select output mode as sample, for custom read count per sample')
    else:
      if request.method=='POST':
        flash('Failed: Input validation failed')
        return redirect(url_for('covcalculator.covcalculator_home'))

    if data_table !='' and \
       isinstance(data_table,dict) and \
       len(data_table) > 0:
      data_table = [data_table]
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