import numpy.testing as npt
import os.path
import pandas as pd
import sys
import unittest
#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from iec_exe import Iec

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
iec_empty = Iec(df_empty, df_empty)

rtol = 1e-5 # set relative tolerance level for npt.assert_allclose assertion tests
test = {}

class TestIEC(unittest.TestCase):
    """
    IEC unit tests.
    """
    def setUp(self):
        """
        setup the test as needed
        e.g. pandas to open sip qaqc csv
        Read qaqc csv and create pandas DataFrames for inputs and expected outputs
        :return:
        """
        pass

    def tearDown(self):
        """
        teardown called after each test
        e.g. maybe write test results to some text file
        :return:
        """
        pass


    def test_z_score_f(self):
        """
        unittest for function iec.z_score_f:
        :return:
        """
        expected_results = [-0.5546622, 0.1524928, 5.861204]
        try:
            iec_empty.threshold = pd.Series([0.6, 1.45, 4.39], dtype='float')
            iec_empty.lc50 = pd.Series([3.0, 1.834, 6.83], dtype='float')
            iec_empty.dose_response = pd.Series([2.5, 0.945, 9.123], dtype='float')
            result = iec_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_f8_f(self):
        """
        unittest for function iec.f8_f:
        """
        expected_results = [0.19215, 0.674726, 0.130719]
        try:
            iec_empty.out_z_score_f = pd.Series([-0.87, 0.453, -1.123])
            result = iec_empty.f8_f()
            #npt.assert_array_almost_equal(result, 0.19215, 4, '', True)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_chance_f(self):
        """
        unittest for function iec.chance_f:
        """
        expected_results = [2.941176, 0.722543, 0.0816787]
        try:
            iec_empty.out_f8_f = pd.Series([0.34, 1.384, 11.342])
            result = iec_empty.chance_f()
            #npt.assert_array_almost_equal(result, 2.941176, 4, '', True)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
