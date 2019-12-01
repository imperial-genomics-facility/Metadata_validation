import logging
import pandas as pd
from flask import render_template,flash,redirect,url_for,request
from . import covcalculator
from .forms import SeqrunForm,platform_check,assay_check
from .utils import calculate_expected_lanes,calculate_expected_lanes_for_known_library
from .utils import calculate_expected_samples,calculate_expected_samples_for_known_library


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
      read_length = platform.read_length
      choose_assay = form.choose_assay.data
      expected_read_count = form.expected_read_count.data
      recommended_clusters = assay_type.read_count
      max_samples = form.max_samples.data
      platform_read_length = int(read_length)
      if int(is_pe) > 0:
        platform_read_length *= 2
      data_table = dict()
      data_table.\
        update({
          'Platform name':platform.name,
          'Platform cluster count':cluster_size,
          'Read length': platform_read_length })
      col_order = [\
        'Platform cluster count',
        'Read length']
      formatted_header_list = [\
        'Output per unit',
        'Platform cluster count',
        'Requested cluster count per sample',
        'Recommended cluster count per sample',
        'Cells per lane',
        'Expected cells',
        'Requested cluster count per cell',
        'Recommended cluster count per cell' ]
      if choose_assay == 'library_type':
        if genome_size >0 or \
           coverage > 0 or \
           expected_read_count > 0:
          flash('Ignoring genome size, coverage and expected read counts for known library type')

        if choose_sample_or_lane == 'sample_number':
          output_dict = \
            calculate_expected_lanes_for_known_library(\
              recommended_clusters=recommended_clusters,
              samples_count=samples,
              cluster_size=cluster_size,
              read_length=read_length,
              is_sc=is_sc,
              max_samples=max_samples)
          required_lane_per_sample = output_dict.get('required_lane_per_sample')
          samples_per_lanes = output_dict.get('samples_per_lanes')
          samples_count = output_dict.get('samples_count')
          expected_lanes = output_dict.get('expected_lanes')
          output_per_unit = output_dict.get('output_per_unit')
          if is_sc==0:
            data_table.\
              update({\
                'Library type': assay_type.assay_name,
                'Output per unit': output_per_unit,
                'Recommended cluster count per sample': assay_type.read_count,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested samples':samples_count,
                'Expected lanes':expected_lanes})
            col_order.\
              extend([\
               'Output per unit',
               'Library type',
               'Recommended cluster count per sample',
               'Required lane per sample',
               'Samples per lane',
               'Requested samples',
               'Expected lanes'])
          else:
            data_table.\
              update({\
                'Library type': assay_type.assay_name,
                'Output per unit': output_per_unit,
                'Recommended cluster count per cell': assay_type.read_count,
                'Required lane per cell':required_lane_per_sample,
                'Cells per lane':samples_per_lanes,
                'Requested cells':samples_count,
                'Expected lanes':expected_lanes})
            col_order.\
              extend([\
               'Output per unit',
               'Library type',
               'Recommended cluster count per cell',
               'Required lane per cell',
               'Cells per lane',
               'Requested cells',
               'Expected lanes'])
          flash('Success')
        elif choose_sample_or_lane == 'lane_number':
          output_dict = \
            calculate_expected_samples_for_known_library(\
              recommended_clusters=recommended_clusters,
              lanes_count=samples,
              cluster_size=cluster_size,
              read_length=read_length,
              is_sc=is_sc,
              max_samples=max_samples)
          required_lane_per_sample = output_dict.get('required_lane_per_sample')
          samples_per_lanes = output_dict.get('samples_per_lanes')
          lanes_count = output_dict.get('lanes_count')
          expected_samples = output_dict.get('expected_samples')
          output_per_unit = output_dict.get('output_per_unit')
          if is_sc==0:
            data_table.\
              update({\
                'Library type': assay_type.assay_name,
                'Output per unit': output_per_unit,
                'Recommended cluster count per sample': assay_type.read_count,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested lanes':lanes_count,
                'Expected samples':expected_samples})
            col_order.\
              extend([\
               'Output per unit',
               'Library type',
               'Recommended cluster count per sample',
               'Required lane per sample',
               'Samples per lane',
               'Requested lanes',
               'Expected samples'])
          else:
            data_table.\
              update({\
                'Library type': assay_type.assay_name,
                'Output per unit': output_per_unit,
                'Recommended cluster count per cell': assay_type.read_count,
                'Required lane per cell':required_lane_per_sample,
                'Cells per lane':samples_per_lanes,
                'Requested lanes':lanes_count,
                'Expected cells':expected_samples})
            col_order.\
              extend([\
               'Output per unit',
               'Library type',
               'Recommended cluster count per cell',
               'Required lane per cell',
               'Cells per lane',
               'Requested lanes',
               'Expected cells'])
          flash('Success')
      elif choose_assay == 'genome_cov':
        if expected_read_count > 0:
          flash('Ignoring costom read count per sample')

        if genome_size==0 or coverage==0:
          flash('Failed: Missing genome size and coverage')
        else:
          if choose_sample_or_lane == 'sample_number':
            output_dict = \
              calculate_expected_lanes(\
                genome_size=genome_size,
                coverage=coverage,
                samples_count=int(samples),
                cluster_size=int(cluster_size),
                is_pe=int(is_pe),
                read_length=int(read_length),
                max_samples=max_samples)
            output_per_unit = output_dict.get('output_per_unit')
            required_lane_per_sample = output_dict.get('required_lane_per_sample')
            samples_per_lanes = output_dict.get('samples_per_lanes')
            samples_count = output_dict.get('samples_count')
            expected_lanes = output_dict.get('expected_lanes')
            data_table.\
              update({\
                'Output per unit': output_per_unit,
                'Genome size (MB)': genome_size,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested samples':samples_count,
                'Expected lanes':expected_lanes})
            col_order.\
              extend([\
               'Output per unit',
               'Genome size (MB)',
               'Required lane per sample',
               'Samples per lane',
               'Requested samples',
               'Expected lanes'])
            flash('Success')
          elif choose_sample_or_lane == 'lane_number':
            output_dict = \
              calculate_expected_samples(\
                genome_size=genome_size,
                coverage=coverage,
                lanes_count=samples,
                cluster_size=cluster_size,
                read_length=read_length,
                is_pe=is_pe,
                max_samples=max_samples)
            output_per_unit = output_dict.get('output_per_unit')
            required_lane_per_sample = output_dict.get('required_lane_per_sample')
            samples_per_lanes = output_dict.get('samples_per_lanes')
            lanes_count = output_dict.get('lanes_count')
            expected_samples = output_dict.get('expected_samples')
            data_table.\
              update({\
                'Output per unit': output_per_unit,
                'Genome size (MB)': genome_size,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested lanes':lanes_count,
                'Expected samples':expected_samples})
            col_order.\
              extend([\
               'Output per unit',
               'Genome size (MB)',
               'Required lane per sample',
               'Samples per lane',
               'Requested lanes',
               'Expected samples'])
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
            output_dict = \
              calculate_expected_lanes_for_known_library(\
                recommended_clusters=expected_read_count,
                samples_count=samples,
                is_sc=0,
                read_length=read_length,
                cluster_size=cluster_size,
                max_samples=max_samples)
            required_lane_per_sample = output_dict.get('required_lane_per_sample')
            samples_per_lanes = output_dict.get('samples_per_lanes')
            samples_count = output_dict.get('samples_count')
            expected_lanes = output_dict.get('expected_lanes')
            output_per_unit = output_dict.get('output_per_unit')
            data_table.\
              update({\
                'Output per unit': output_per_unit,
                'Requested cluster count per sample':expected_read_count,
                'Required lane per sample':required_lane_per_sample,
                'Samples per lane':samples_per_lanes,
                'Requested samples':samples_count,
                'Expected lanes':expected_lanes})
            col_order.\
              extend([\
               'Output per unit',
               'Requested cluster count per sample',
               'Required lane per sample',
               'Samples per lane',
               'Requested samples',
               'Expected lanes'])
            flash('Success')
          else:
            flash('Failed: Select output mode as sample, for custom read count per sample')
    else:
      if request.method=='POST':
        flash('Failed: Input validation failed')
        return render_template(\
             'covcalculator/sequencing_coverage_calculator.html',
             form=form)

    if data_table !='' and isinstance(data_table,dict):
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