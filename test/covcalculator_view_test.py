import unittest
from app import create_app,db
from app.models import Platform,Assay_type

class CovcalculatorView_test(unittest.TestCase):
  def setUp(self):
    self.app = create_app('testing')
    self.app.config['TESTING'] = True
    self.app.config['WTF_CSRF_ENABLED'] = False
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.drop_all()
    db.create_all()
    self.client = self.app.test_client(use_cookies=False)
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
    assay_data_list = [\
      {'assay_name':'mRNA-Seq DE profiling',
       'read_count':25000000,
       'is_sc':0},
      {'assay_name':'TenX genomics 3\' RNA-seq',
       'read_count':50000,
       'is_sc':1}]
    assay_lists =\
       [Assay_type(**assay_data) 
          for assay_data in assay_data_list]
    db.session.add_all(assay_lists)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  def test1(self):
    self.assertTrue('HiSeq 4000 150 PE' in [i.name for i in Platform.query.all()])
  
  def test2(self):
    self.assertTrue('mRNA-Seq DE profiling' in [i.assay_name for i in Assay_type.query.all()])

  def test_get_page(self):
    covcalculator_response = self.client.get('/covcalculator/')
    self.assertEqual(covcalculator_response.status_code,200)
    #print(covcalculator_response.get_data(as_text=True))

  def test_post_page(self):
    platform = [i for i in Platform.query.all() if i.name == 'HiSeq 4000 150 PE'][0]
    assay = [i for i in Assay_type.query.all() if i.assay_name == 'mRNA-Seq DE profiling'][0]
    print('UT', platform)
    print('UT', assay)
    covcalculator_response = \
      self.client.post(\
        '/covcalculator/',
        data=dict(
          platform=platform,
          choose_assay='Use recommended clusters for known library type',
          assay_type=assay,
          choose_sample_or_lane='I will sequence following lanes',
          samples=1,
          max_samples=96
        ),
        follow_redirects=True)
    #print(covcalculator_response.get_data(as_text=True))

if __name__ == '__main__':
  unittest.main()