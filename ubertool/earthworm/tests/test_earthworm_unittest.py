import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import sys
from tabulate import tabulate
import unittest

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from earthworm_exe import Earthworm

test = {}


class TestEarthworm(unittest.TestCase):
    """
    Unit tests for earthworm model.
    """
    print("earthworm unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        setup the test as needed
        e.g. pandas to open stir qaqc csv
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

    def create_earthworm_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty earthworm object
        earthworm_empty = Earthworm(df_empty, df_empty)
        return earthworm_empty

    def test_earthworm_fugacity_unit(self):
        """
        Test the only real earthworm method.
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        earthworm_empty = self.create_earthworm_object()

        try:
            expected_results = pd.Series([0.73699363, 1.908571, 5.194805], dtype='float')
            earthworm_empty.k_ow = pd.Series([10.0, 100.0, 1000.0], dtype='float')
            earthworm_empty.l_f_e = pd.Series([0.01, 0.02, 0.03], dtype='float')
            earthworm_empty.c_s = pd.Series([0.038692165, 0.05344, 0.10], dtype='float')
            earthworm_empty.k_d = pd.Series([0.0035, 0.035, 0.35], dtype='float')
            earthworm_empty.p_s = pd.Series([1.5, 1.60, 1.65], dtype='float')
            result = earthworm_empty.earthworm_fugacity()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()