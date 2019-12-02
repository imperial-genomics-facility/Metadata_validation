import unittest
from app.covcalculator.utils import calculate_expected_lanes,calculate_expected_samples,calculate_coverage_output
from app.covcalculator.utils import calculate_expected_lanes_for_known_library,calculate_expected_samples_for_known_library

class Covcalculator_utils1(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass
  def test_calculate_expected_lanes_for_known_library(self):
    output_dict = \
      calculate_expected_lanes_for_known_library(\
        recommended_clusters=25000000,
        samples_count=16,
        cluster_size=400000000,
        read_length=150,
        is_sc=0,
        is_pe=1,
        max_samples=96)
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    samples_count = output_dict.get('samples_count')
    expected_lanes = output_dict.get('expected_lanes')
    output_per_unit = output_dict.get('output_per_unit')
    self.assertTrue(\
      (required_lane_per_sample==0.0625) & \
      (samples_per_lanes==16) & \
      (samples_count==16) & \
      (expected_lanes==1) & \
      (output_per_unit==400000000*300))
    output_dict = \
      calculate_expected_lanes_for_known_library(\
        recommended_clusters=50000,
        samples_count=6000,
        cluster_size=400000000,
        read_length=150,
        is_sc=1,
        is_pe=1,
        max_samples=96)
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    samples_count = output_dict.get('samples_count')
    expected_lanes = output_dict.get('expected_lanes')
    output_per_unit = output_dict.get('output_per_unit')
    self.assertTrue(\
      (required_lane_per_sample==0.003) & \
      (samples_per_lanes==8000) & \
      (samples_count==6000) & \
      (expected_lanes==1) & \
      (output_per_unit==400000000*300))

  def test_calculate_expected_samples_for_known_library(self):
    output_dict = \
      calculate_expected_samples_for_known_library(\
        recommended_clusters=25000000,
        lanes_count=1,
        cluster_size=400000000,
        read_length=150,
        is_sc=0,
        is_pe=1,
        max_samples=96)
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    lanes_count = output_dict.get('lanes_count')
    expected_samples = output_dict.get('expected_samples')
    output_per_unit = output_dict.get('output_per_unit')
    self.assertTrue(\
      (required_lane_per_sample==0.0625) & \
      (samples_per_lanes==16) & \
      (lanes_count==1) & \
      (expected_samples==16) & \
      (output_per_unit==400000000*300))
    output_dict = \
      calculate_expected_samples_for_known_library(\
        recommended_clusters=50000,
        lanes_count=1,
        cluster_size=400000000,
        read_length=150,
        is_sc=1,
        is_pe=1,
        max_samples=96)
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    lanes_count = output_dict.get('lanes_count')
    expected_samples = output_dict.get('expected_samples')
    output_per_unit = output_dict.get('output_per_unit')
    self.assertTrue(\
      (required_lane_per_sample==0.003) & \
      (samples_per_lanes==8000) & \
      (lanes_count==1) & \
      (expected_samples==8000) & \
      (output_per_unit==400000000*300))

  def test_calculate_expected_samples(self):
    output_dict = \
      calculate_expected_samples(\
        genome_size=3200,
        coverage=10,
        lanes_count=2,
        cluster_size=312500000,
        read_length=150,
        is_pe=1,
        max_samples=96)
    output_per_unit = output_dict.get('output_per_unit')
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    lanes_count = output_dict.get('lanes_count')
    expected_samples = output_dict.get('expected_samples')
    expected_bases_per_sample = output_dict.get('expected_bases_per_sample')
    self.assertTrue(\
      (output_per_unit==312500000*150*2) & \
      (round(required_lane_per_sample,2)==0.34) & \
      (samples_per_lanes==2) & \
      (lanes_count==2) & \
      (expected_samples==5) & \
      (expected_bases_per_sample==3200*1000000*10))
    output_dict = \
      calculate_expected_samples(\
        genome_size=3.5,
        coverage=10,
        lanes_count=1,
        cluster_size=312500000,
        read_length=150,
        is_pe=1,
        max_samples=96)
    output_per_unit = output_dict.get('output_per_unit')
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    lanes_count = output_dict.get('lanes_count')
    expected_samples = output_dict.get('expected_samples')
    expected_bases_per_sample = output_dict.get('expected_bases_per_sample')
    self.assertTrue(\
      (output_per_unit==312500000*150*2) & \
      (round(required_lane_per_sample,4)==0.003) & \
      (samples_per_lanes==96) & \
      (lanes_count==1) & \
      (expected_samples==96) & \
      (expected_bases_per_sample==3.5*1000000*10))

  def test_calculate_expected_lanes(self):
    output_dict = \
      calculate_expected_lanes(\
        genome_size=3200,
        coverage=10,
        samples_count=10,
        cluster_size=312500000,
        is_pe=1,
        read_length=150,
        max_samples=96)
    output_per_unit = output_dict.get('output_per_unit')
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    samples_count = output_dict.get('samples_count')
    expected_lanes = output_dict.get('expected_lanes')
    expected_bases_per_sample = output_dict.get('expected_bases_per_sample')
    self.assertTrue(\
      (output_per_unit==312500000*150*2) & \
      (round(required_lane_per_sample,2)==0.34) & \
      (samples_per_lanes==2) & \
      (samples_count==10) & \
      (expected_lanes==4) & \
      (expected_bases_per_sample==3200*1000000*10))
    output_dict = \
      calculate_expected_lanes(\
        genome_size=3.5,
        coverage=10,
        samples_count=96,
        cluster_size=312500000,
        is_pe=1,
        read_length=150,
        max_samples=96)
    output_per_unit = output_dict.get('output_per_unit')
    required_lane_per_sample = output_dict.get('required_lane_per_sample')
    samples_per_lanes = output_dict.get('samples_per_lanes')
    samples_count = output_dict.get('samples_count')
    expected_lanes = output_dict.get('expected_lanes')
    expected_bases_per_sample = output_dict.get('expected_bases_per_sample')
    self.assertTrue(\
      (output_per_unit==312500000*150*2) & \
      (round(required_lane_per_sample,3)==0.003) & \
      (samples_per_lanes==96) & \
      (samples_count==96) & \
      (expected_lanes==1) & \
      (expected_bases_per_sample==3.5*1000000*10))

  def test_calculate_coverage_output(self):
    data_table,col_order,formatted_header = \
      calculate_coverage_output(
        platform_name='HiSeq 4000 50 SR',
        cluster_size=312500000,
        platform_read_length=50,
        choose_assay='library_type',
        choose_sample_or_lane='lane_number',
        recommended_clusters=2220000,
        samples=1,
        is_sc=0,
        max_samples=96,
        assay_type_assay_name='Small RNA DE profiling',
        expected_read_count=0,
        genome_size=0,
        coverage=0,
        is_pe=0
      )
    self.assertEqual(data_table.get('Expected samples'),96)
    self.assertTrue('Output per unit' in col_order)
    self.assertTrue('Output per unit' in formatted_header)
    data_table,col_order,formatted_header = \
      calculate_coverage_output(
        platform_name='HiSeq 4000 50 SR',
        cluster_size=312500000,
        platform_read_length=50,
        choose_assay='genome_cov',
        choose_sample_or_lane='lane_number',
        recommended_clusters=2220000,
        samples=1,
        is_sc=0,
        max_samples=96,
        assay_type_assay_name='Small RNA DE profiling',
        expected_read_count=0,
        genome_size=0,
        coverage=0,
        is_pe=0
      )
    self.assertEqual(len(data_table),0)
    data_table,col_order,formatted_header = \
      calculate_coverage_output(
        platform_name='HiSeq 4000 50 SR',
        cluster_size=312500000,
        platform_read_length=50,
        choose_assay='custom_read',
        choose_sample_or_lane='lane_number',
        recommended_clusters=2220000,
        samples=1,
        is_sc=0,
        max_samples=96,
        assay_type_assay_name='Small RNA DE profiling',
        expected_read_count=0,
        genome_size=0,
        coverage=0,
        is_pe=0
      )
    self.assertEqual(len(data_table),0)
    data_table,col_order,formatted_header = \
      calculate_coverage_output(
        platform_name='HiSeq 4000 50 SR',
        cluster_size=312500000,
        platform_read_length=50,
        choose_assay='library_type',
        choose_sample_or_lane='lane_number',
        recommended_clusters=0,
        samples=1,
        is_sc=0,
        max_samples=96,
        assay_type_assay_name='Small RNA DE profiling',
        expected_read_count=10000000,
        genome_size=3200,
        coverage=10,
        is_pe=0
      )
    self.assertEqual(len(data_table),0)
    data_table,col_order,formatted_header = \
      calculate_coverage_output(
        platform_name='HiSeq 4000 150 PE',
        cluster_size=312500000,
        platform_read_length=150,
        choose_assay='library_type',
        choose_sample_or_lane='sample_number',
        recommended_clusters=25000000,
        samples=100,
        is_sc=0,
        max_samples=96,
        assay_type_assay_name='mRNA-Seq DE profiling',
        expected_read_count=10000000,
        genome_size=3200,
        coverage=10,
        is_pe=1
    )
    self.assertEqual(data_table.get('Expected lanes'),9)
    data_table,col_order,formatted_header = \
      calculate_coverage_output(
        platform_name='HiSeq 4000 150 PE',
        cluster_size=312500000,
        platform_read_length=150,
        choose_assay='library_type',
        choose_sample_or_lane='sample_number',
        recommended_clusters=50000,
        samples=5000,
        is_sc=1,
        max_samples=96,
        assay_type_assay_name="TenX genomics 3' RNA-seq",
        expected_read_count=10000000,
        genome_size=3200,
        coverage=10,
        is_pe=1
    )
    self.assertEqual(data_table.get('Expected lanes'),1)
    self.assertEqual(data_table.get('Cells per lane'),6250)
if __name__ == '__main__':
  unittest.main()