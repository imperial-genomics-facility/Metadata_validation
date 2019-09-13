import io,os
from igf_data.process.metadata_reformat.reformat_metadata_file import Reformat_metadata_file,EXPERIMENT_TYPE_LOOKUP,SPECIES_LOOKUP,METADATA_COLUMNS

def convert_file_to_stream(infile):
  '''
  A function for converting trext file to string

  :param infile: An input file
  '''
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

def run_metadata_reformatting(metadata_file,output_dir):
  try:
    metadata_output = \
      os.path.join(\
        output_dir,
        'temp_metadata.csv')
    csv_data = ''
    re_metadata = \
      Reformat_metadata_file(\
        infile=metadata_file,
        experiment_type_lookup=EXPERIMENT_TYPE_LOOKUP,
        species_lookup=SPECIES_LOOKUP,
        metadata_columns=METADATA_COLUMNS)
    re_metadata.\
      reformat_raw_metadata_file(output_file=metadata_output)
    csv_data = convert_file_to_stream(infile=metadata_output)
    return csv_data
  except Exception as e:
    raise ValueError('Failed to run metadata formatter, error: {0}'.format(e))