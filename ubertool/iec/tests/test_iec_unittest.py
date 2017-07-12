import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import sys
from tabulate import tabulate
import unittest

# #find parent directory and import model
# parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(parentddir)
from ..iec_exe import Iec

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
iec_empty = Iec(df_empty, df_empty)

rtol = 1e-4 # set relative tolerance level for npt.assert_allclose assertion tests
test = {}

class TestIEC(unittest.TestCase):
    """
    IEC unit tests.
    """
    print("iec unittests conducted at " + str(datetime.datetime.today()))

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

    def create_iec_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty iec object
        iec_empty = Iec(df_empty, df_empty)
        return iec_empty

    def test_iec_z_score_f(self):
        """
        unittest for function iec.z_score_f:
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        iec_empty = self.create_iec_object()

        expected_results = pd.Series([-0.5546622, 0.1524928, 5.861204], dtype='float')
        try:
            iec_empty.threshold = pd.Series([0.6, 1.45, 4.39], dtype='float')
            iec_empty.lc50 = pd.Series([3.0, 1.834, 6.83], dtype='float')
            iec_empty.dose_response = pd.Series([2.5, 0.945, 9.123], dtype='float')
            result = iec_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_iec_f8_f(self):
        """
        unittest for function iec.f8_f:
        """
        expected_results = pd.Series([0.19215, 0.674726, 0.130719], dtype='float')
        try:
            iec_empty.out_z_score_f = pd.Series([-0.87, 0.453, -1.123], dtype='float')
            result = iec_empty.f8_f()
            #npt.assert_array_almost_equal(result, 0.19215, 4, '', True)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_iec_chance_f(self):
        """
        unittest for function iec.chance_f:
        """
        expected_results = pd.Series([2.941176, 0.722543, 0.0881678], dtype='float')
        try:
            iec_empty.out_f8_f = pd.Series([0.34, 1.384, 11.342], dtype='float')
            result = iec_empty.chance_f()
            #npt.assert_array_almost_equal(result, 2.941176, 4, '', True)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

