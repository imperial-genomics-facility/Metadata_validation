import unittest
from app import create_app,db
from app.models import Platform,Assay_type

class IgftoolsApp_test(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.drop_all()
    db.create_all()
    self.client = self.app.test_client(use_cookies=True)
    platform_data_list = [\
      {'name':'HiSeq 4000 50 SR',
       'm_reads':270,
       'm_bases':13500,
       'm_clusters':312,
       'm_output':15600,
       'clusters':312500000,
       'lanes':8,
       'max_samples':96,
       'is_pe':0,
       'read_length':50},
       {'name':'HiSeq 4000 150 PE',
       'm_reads':270,
       'm_bases':8100,
       'm_clusters':312,
       'm_output':93600,
       'clusters':312500000,
       'lanes':8,
       'max_samples':96,
       'is_pe':1,
       'read_length':150}]
    platform_lists =\
       [Platform(**platform_data) 
          for platform_data in platform_data_list]
    db.session.add_all(platform_lists)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()

  def test_igftools_home(self):
    home_response = self.client.get('/')
    self.assertEqual(home_response.status_code,200)
    covcalculator_response = self.client.get('/covcalculator/')
    self.assertEqual(covcalculator_response.status_code,200)
    metadata_response = self.client.get('/metadata/')
    self.assertEqual(metadata_response.status_code,200)
    samplesheet_response = self.client.get('/samplesheet/')
    self.assertEqual(samplesheet_response.status_code,200)
    validation_response = self.client.get('/validation/')
    self.assertEqual(validation_response.status_code,200)

if __name__ == '__main__':
  unittest.main()

