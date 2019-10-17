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
    platform_data = \
      {'id':1,
       'name':'HiSeq 4000 50 SR',
       'm_reads':270,
       'm_bases':13500,
       'm_clusters':312,
       'm_output':15600,
       'clusters':312500000,
       'lanes':8,
       'max_samples':96,
       'is_pe':0,
       'read_length':50}
    platform = Platform(platform_data)
    db.session.add(platform)
  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
if __name__ == '__main__':
  unittest.main()