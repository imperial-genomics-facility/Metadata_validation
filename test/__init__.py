import os.path, unittest

def get_tests():
  return full_suite()

def full_suite():
  from test.covcalculator_test import Covcalculator_utils1
  return unittest.TestSuite([\
    unittest.TestLoader().loadTestsFromTestCase(Covcalculator_utils1)
  ])