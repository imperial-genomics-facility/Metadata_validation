import os.path, unittest

def get_tests():
  return full_suite()

def full_suite():
  from test.covcalculator_utils_test import Covcalculator_utils1
  from test.app_test import IgftoolsApp_test
  from test.covcalculator_view_test import CovcalculatorView_test
  return unittest.TestSuite([\
    unittest.TestLoader().loadTestsFromTestCase(Covcalculator_utils1),
    unittest.TestLoader().loadTestsFromTestCase(IgftoolsApp_test),
    unittest.TestLoader().loadTestsFromTestCase(CovcalculatorView_test),
  ])