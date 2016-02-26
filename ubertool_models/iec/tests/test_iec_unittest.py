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
        try:
            iec_empty.threshold = pd.Series([0.6])
            iec_empty.lc50 = pd.Series([3])
            iec_empty.dose_response = pd.Series([2.5])
            result = iec_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_f8_f(self):
        """
        unittest for function iec.f8_f:
        """
        try:
            iec_empty.z_score_f_out = pd.Series([-0.87])
            result = iec_empty.f8_f()
            #npt.assert_array_almost_equal(result, 0.19215, 4, '', True)
            npt.assert_allclose(result,0.19215,rtol,0,'',True)
        finally:
            pass
        return

    def test_chance_f(self):
        """
        unittest for function iec.chance_f:
        """
        try:
            iec_empty.f8_f_out = pd.Series([0.34])
            result = iec_empty.chance_f()
            #npt.assert_array_almost_equal(result, 2.941176, 4, '', True)
            npt.assert_allclose(result,2.941176,rtol,0,'',True)
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
