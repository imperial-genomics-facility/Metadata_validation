import unittest
from app import create_app,db
from app.models import Platform,Assay_type

class CovcalculatorView_test(unittest.TestCase):
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

if __name__ == '__main__':
  unittest.main()