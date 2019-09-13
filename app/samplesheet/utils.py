import io,os
from igf_data.process.metadata_reformat.reformat_samplesheet_file import Reformat_samplesheet_file

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

def run_samplesheet_reformatting(samplesheet_file,output_dir,revcomp_index1,
                                 revcomp_index2,remove_adapters):
  try:
    csv_data = ''
    samplesheet_output = \
      os.path.join(\
        output_dir,
        'reformatted_samplesheet.csv')
    re_samplesheet = \
      Reformat_samplesheet_file( \
        infile=samplesheet_file,
        revcomp_index1=revcomp_index1,
        revcomp_index2=revcomp_index2,
        remove_adapters=remove_adapters)
    re_samplesheet.\
      reformat_raw_samplesheet_file(\
        output_file=samplesheet_output)
    csv_data = \
      convert_file_to_stream(infile=samplesheet_output)
    return csv_data
  except Exception as e:
    raise ValueError('Failed running samplesheet reformatting, error: {0}'.format(e))