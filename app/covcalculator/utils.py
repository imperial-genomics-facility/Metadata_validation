def calculate_expected_lanes(genome_size,coverage,samples_count,is_pe,cluster_size,
                             read_length,max_samples=96,min_required_lane_per_sample=0.003):
  '''
  A function to calculate expected number of lanes for sequencing

  :param genome_size: Genome size in Mb
  :param coverage: Requested genome coverage
  :param samples_count: Number of samples requested
  :param is_pe: Toggle for paired end run
  :param cluster_size: Available cluster size per lane
  :param read_length: Read length
  :param max_samples: Max number of allowed samples, default 96
  :param min_required_lane_per_sample: Minumum required lane per sample, default 0.003
  :returns: A dictionary with following keys
                  * output_per_unit
                  * required_lane_per_sample
                  * samples_per_lanes
                  * samples_count
                  * expected_lanes
                  * expected_bases_per_sample
  '''
  try:
    genome_size *= 1000000
    expected_bases_per_sample = genome_size * coverage
    if is_pe > 0:
        read_length *= 2
    output_per_unit = cluster_size * read_length
    required_lane_per_sample = expected_bases_per_sample / output_per_unit
    samples_per_lanes = output_per_unit / expected_bases_per_sample
    if required_lane_per_sample < min_required_lane_per_sample:
      required_lane_per_sample = min_required_lane_per_sample
    if samples_per_lanes > max_samples:
        samples_per_lanes = max_samples
    if int(samples_per_lanes) < 1:
        samples_per_lanes = 1
    expected_lanes = samples_count / samples_per_lanes
    if expected_lanes > int(expected_lanes):
        expected_lanes = int(expected_lanes) + 1
    output_dict = dict()
    output_dict.\
      update({\
        'output_per_unit':output_per_unit,
        'required_lane_per_sample': round(required_lane_per_sample,4),
        'samples_per_lanes':int(samples_per_lanes),
        'samples_count':samples_count,
        'expected_lanes':int(expected_lanes),
        'expected_bases_per_sample':int(expected_bases_per_sample)
        })
    return output_dict
  except Exception as e:
    raise ValueError('Failed to calculate expected lanes, error: {0}'.format(e))

def calculate_expected_samples(genome_size,coverage,lanes_count,is_pe,cluster_size,
                               read_length,max_samples=96,min_required_lane_per_sample=0.003):
  '''
  A function to calculate expected sample counts for sequencing

  :param genome_size: Genome size in Mb
  :param coverage: Genome coverage
  :param lanes_count: Number of lanes to sequence
  :param is_pe: Toggle for paired-end reads
  :param cluster_size: Cluster size per lane on flowcell
  :param read_length: Read length in bp
  :param max_samples: Max number of allowed samples, default 96
  :param min_required_lane_per_sample: Minimum number of required lane per sample, default 0.003
  :returns: A dictionary with following keys
                  * output_per_unit
                  * required_lane_per_sample
                  * samples_per_lanes
                  * lanes_count
                  * expected_samples
                  * expected_bases_per_sample
  '''
  try:
    genome_size *= 1000000
    if is_pe > 0:
        read_length *= 2
    output_per_unit = cluster_size * read_length
    expected_bases_per_sample = genome_size * coverage
    required_lane_per_sample = expected_bases_per_sample / output_per_unit
    if required_lane_per_sample < min_required_lane_per_sample:
      required_lane_per_sample = min_required_lane_per_sample
    samples_per_lanes = output_per_unit / expected_bases_per_sample
    if samples_per_lanes > max_samples:
        samples_per_lanes = max_samples
    expected_samples = samples_per_lanes * lanes_count
    output_dict = dict()
    output_dict.\
      update({\
        'output_per_unit':output_per_unit,
        'required_lane_per_sample': round(required_lane_per_sample,4),
        'samples_per_lanes':int(samples_per_lanes),
        'lanes_count':lanes_count,
        'expected_samples':int(expected_samples),
        'expected_bases_per_sample':int(expected_bases_per_sample)
        })
    return output_dict
  except Exception as e:
    raise ValueError('Failed to calculate expected samples, error: {0}'.format(e))

def calculate_expected_lanes_for_known_library(recommended_clusters,samples_count,cluster_size,is_sc,read_length,
                                               is_pe=0,max_samples=96,min_required_lane_per_sample=0.003):
  '''
  A function for calculating expected lane counts for known library

  :param recommended_clusters: Recommended cluster counts for known assay types
  :param samples_count: Number of samples to sequence
  :param cluster_size: Per lane cluster size on flowcell
  :param is_sc: A toggle for single cell assay type
  :param read_length: Read length in bp
  :param is_pe: A toggle for paired-end reads, default 0
  :param max_samples: Max number of allowed samples per lane, default 96
  :param min_required_lane_per_sample: Minimum number of required lane per sample, default 0.003
  :return: A dictionary with following keys
             * required_lane_per_sample
             * samples_per_lanes
             * samples_count
             * expected_lanes
             * output_per_unit
  '''
  try:
    samples_per_lanes = cluster_size / recommended_clusters
    required_lane_per_sample = recommended_clusters / cluster_size
    if required_lane_per_sample < min_required_lane_per_sample:
      required_lane_per_sample = min_required_lane_per_sample
    if is_pe > 0:
      read_length *= 2
    output_per_unit = cluster_size * read_length
    if samples_per_lanes > max_samples and is_sc==0:
        samples_per_lanes = max_samples
    expected_lanes = samples_count / int(samples_per_lanes)
    if expected_lanes > int(expected_lanes):
      expected_lanes = int(expected_lanes) + 1
    output_dict = dict()
    output_dict.\
      update({ \
        'required_lane_per_sample': round(required_lane_per_sample,4),
        'samples_per_lanes':int(samples_per_lanes),
        'samples_count':samples_count,
        'expected_lanes':expected_lanes,
        'output_per_unit':output_per_unit
      })
    return output_dict
  except Exception as e:
    raise ValueError('Failed to calculate expected lanes for know library, error: {0}'.format(e))

def calculate_expected_samples_for_known_library(recommended_clusters,lanes_count,cluster_size,is_sc,read_length,
                                                 is_pe=0,max_samples=96,min_required_lane_per_sample=0.003):
  '''
  A function for calculating expected sample number for known library type for sequencing

  :param recommended_clusters: Recommended cluster counts for known assay types
  :param lanes_count: Number of lanes to sequence
  :param cluster_size: Per lane cluster size on flowcell
  :param is_sc: A toggle for single cell assay type
  :param read_length: Read length in bp
  :param is_pe: A toggle for paired-end reads, default 0
  :param max_samples: Max number of allowed samples per lane, default 96
  :param min_required_lane_per_sample: Minimum number of required lane per sample, default 0.003
  :return: A dictionary with following keys
               * required_lane_per_sample
               * samples_per_lanes
               * lanes_count
               * expected_samples
               * output_per_unit
  '''
  try:
    samples_per_lanes = cluster_size / recommended_clusters
    required_lane_per_sample = recommended_clusters / cluster_size
    if required_lane_per_sample < min_required_lane_per_sample:
      required_lane_per_sample = min_required_lane_per_sample
    if is_pe > 0:
      read_length *= 2
    output_per_unit = cluster_size * read_length
    if samples_per_lanes > max_samples and is_sc==0:
        samples_per_lanes = max_samples
    expected_samples = samples_per_lanes * lanes_count
    output_dict = dict()
    output_dict.\
      update({\
        'required_lane_per_sample': round(required_lane_per_sample,4),
        'samples_per_lanes':int(samples_per_lanes),
        'lanes_count':lanes_count,
        'expected_samples':int(expected_samples),
        'output_per_unit':output_per_unit
        })
    return output_dict
  except Exception as e:
    raise ValueError('Failed to calculate expected samples for know library, error: {0}'.format(e))

def calculate_coverage_output(platform_name,cluster_size,platform_read_length,choose_assay,choose_sample_or_lane,
                              recommended_clusters,samples,is_sc,max_samples,assay_type_assay_name,expected_read_count,
                              genome_size,coverage,is_pe):
  '''
  A function for formatting coverage output

  :param platform_name: A string containing the platform name
  :param cluster_size: A long int value of the platform cluster size
  :param platform_read_length: A int value for the target read lengthe of the platform
  :param choose_assay: A string containing the toggle for assay name
  :param choose_sample_or_lane: A string containing the toggle for sample or lane count
  :param recommended_clusters: A int value for recommended clusters for known assay types
  :param samples: An int value for target number of samples or lanes
  :param is_sc: A toggle for single cell assay types
  :param max_samples: An int value for the max samples per lane
  :param assay_type_assay_name: A string for assay name
  :param expected_read_count: An long int for custom read counts
  :param genome_size: An int value for genome size in Mb
  :param coverage: An int value for target genome coverage
  :param is_pe: A toggle for paired end library type
  :returns: A dictionary containing data, list containing the output column order and a list containing the formatted headers
  '''
  try:
    data_table = dict()
    default_data_table = {
      'Platform name':platform_name,
      'Platform cluster count':cluster_size,
      'Read length': platform_read_length}
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
    ################################################
    if choose_assay == 'library_type' and \
       recommended_clusters > 0:
      if choose_sample_or_lane == 'sample_number':
        output_dict = \
          calculate_expected_lanes_for_known_library(\
            recommended_clusters=recommended_clusters,
            samples_count=samples,
            cluster_size=cluster_size,
            read_length=platform_read_length,
            is_sc=is_sc,
            max_samples=max_samples)
        required_lane_per_sample = output_dict.get('required_lane_per_sample')
        samples_per_lanes = output_dict.get('samples_per_lanes')
        samples_count = output_dict.get('samples_count')
        expected_lanes = output_dict.get('expected_lanes')
        output_per_unit = output_dict.get('output_per_unit')
        if is_sc==0:
          data_table.\
            update(default_data_table)
          data_table.\
            update({
              'Library type': assay_type_assay_name,
              'Output per unit': output_per_unit,
              'Recommended cluster count per sample': recommended_clusters,
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
            update(default_data_table)
          data_table.\
            update({\
              'Library type': assay_type_assay_name,
              'Output per unit': output_per_unit,
              'Recommended cluster count per cell': recommended_clusters,
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
      elif choose_sample_or_lane == 'lane_number':
        output_dict = \
          calculate_expected_samples_for_known_library(\
            recommended_clusters=recommended_clusters,
            lanes_count=samples,
            cluster_size=cluster_size,
            read_length=platform_read_length,
            is_sc=is_sc,
            max_samples=max_samples)
        required_lane_per_sample = output_dict.get('required_lane_per_sample')
        samples_per_lanes = output_dict.get('samples_per_lanes')
        lanes_count = output_dict.get('lanes_count')
        expected_samples = output_dict.get('expected_samples')
        output_per_unit = output_dict.get('output_per_unit')
        if is_sc==0:
          data_table.\
            update(default_data_table)
          data_table.\
            update({\
              'Library type': assay_type_assay_name,
              'Output per unit': output_per_unit,
              'Recommended cluster count per sample': recommended_clusters,
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
            update(default_data_table)
          data_table.\
            update({\
              'Library type': assay_type_assay_name,
              'Output per unit': output_per_unit,
              'Recommended cluster count per cell': recommended_clusters,
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
    elif choose_assay == 'genome_cov' and \
         genome_size > 0 and coverage > 0:
      if choose_sample_or_lane == 'sample_number':
        output_dict = \
          calculate_expected_lanes(\
            genome_size=genome_size,
            coverage=coverage,
            samples_count=int(samples),
            cluster_size=int(cluster_size),
            is_pe=int(is_pe),
            read_length=int(platform_read_length),
            max_samples=max_samples)
        output_per_unit = output_dict.get('output_per_unit')
        required_lane_per_sample = output_dict.get('required_lane_per_sample')
        samples_per_lanes = output_dict.get('samples_per_lanes')
        samples_count = output_dict.get('samples_count')
        expected_lanes = output_dict.get('expected_lanes')
        data_table.\
          update(default_data_table)
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
      elif choose_sample_or_lane == 'lane_number':
        output_dict = \
          calculate_expected_samples(\
            genome_size=genome_size,
            coverage=coverage,
            lanes_count=samples,
            cluster_size=cluster_size,
            read_length=platform_read_length,
            is_pe=is_pe,
            max_samples=max_samples)
        output_per_unit = output_dict.get('output_per_unit')
        required_lane_per_sample = output_dict.get('required_lane_per_sample')
        samples_per_lanes = output_dict.get('samples_per_lanes')
        lanes_count = output_dict.get('lanes_count')
        expected_samples = output_dict.get('expected_samples')
        data_table.\
          update(default_data_table)
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
    elif choose_assay == 'custom_read' and \
        (expected_read_count is not None or \
         expected_read_count != '') and \
        expected_read_count > 0:
      if choose_sample_or_lane == 'sample_number':
        output_dict = \
          calculate_expected_lanes_for_known_library(\
            recommended_clusters=expected_read_count,
            samples_count=samples,
            is_sc=0,
            read_length=platform_read_length,
            cluster_size=cluster_size,
            max_samples=max_samples)
        required_lane_per_sample = output_dict.get('required_lane_per_sample')
        samples_per_lanes = output_dict.get('samples_per_lanes')
        samples_count = output_dict.get('samples_count')
        expected_lanes = output_dict.get('expected_lanes')
        output_per_unit = output_dict.get('output_per_unit')
        data_table.\
          update(default_data_table)
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
    return data_table,col_order,formatted_header_list
  except Exception as e:
    raise ValueError(e)