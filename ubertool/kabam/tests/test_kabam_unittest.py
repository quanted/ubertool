from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy as np
import numpy.testing as npt
import os.path
import pandas as pd
import sys
from tabulate import tabulate
import unittest

print("Python version: " + sys.version)
print("Numpy version: " + np.__version__)

#find parent directory and import model
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)
from kabam_exe import Kabam

# create empty pandas dataframes to create empty object for testing
df_empty = pd.DataFrame()
# create an empty trex object
kabam_empty = Kabam(df_empty, df_empty)

test = {}

class TestKabam(unittest.TestCase):
    """
    Unit tests for Kabam model.
    """
    print("kabam unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for trex unit tests.
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open trex qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for trex unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file


    def test_phi_x(self):
        """
        unittest for function phi_x;
        """
        result = pd.Series([], dtype='float')
        expected_results = [69.17640, 146.8274, 56.00997]
        try:
            kabam_empty.x_poc = pd.Series([100., 125., 90.], dtype='float')
            kabam_empty.k_ow = pd.Series([100., 125., 90.], dtype='float')
            kabam_empty.x_doc = pd.Series([100., 125., 90.], dtype='float')
            result = kabam_empty.phi_f()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
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
    #pass