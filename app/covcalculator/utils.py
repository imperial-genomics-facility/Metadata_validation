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
    return output_per_unit,required_lane_per_sample,int(samples_per_lanes),samples_count,int(expected_lanes),int(expected_bases_per_sample)
  except Exception as e:
    raise ValueError('Failed to calculate expected lanes, error: {0}'.format(e))

def calculate_expected_samples(genome_size,coverage,lanes_count,is_pe,cluster_size,
                               read_length,max_samples=96,min_required_lane_per_sample=0.003):
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
    return output_per_unit,required_lane_per_sample,int(samples_per_lanes),lanes_count,int(expected_samples),int(expected_bases_per_sample)
  except Exception as e:
    raise ValueError('Failed to calculate expected samples, error: {0}'.format(e))

def calculate_expected_lanes_for_known_library(recommended_clusters,samples_count,cluster_size,
                                               is_sc,read_length,is_pe=0,max_samples=96,min_required_lane_per_sample=0.003):
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
    return required_lane_per_sample,int(samples_per_lanes),samples_count,expected_lanes,output_per_unit
  except Exception as e:
    raise ValueError('Failed to calculate expected lanes for know library, error: {0}'.format(e))

def calculate_expected_samples_for_known_library(recommended_clusters,lanes_count,cluster_size,
                                                 is_sc,read_length,is_pe=0,max_samples=96,min_required_lane_per_sample=0.003):
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
    return required_lane_per_sample,int(samples_per_lanes),lanes_count,int(expected_samples),output_per_unit
  except Exception as e:
    raise ValueError('Failed to calculate expected samples for know library, error: {0}'.format(e))
