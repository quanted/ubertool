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
from ..rice_exe import Rice

test = {}


class TestRice(unittest.TestCase):
    """
    Unit tests for Rice.
    """
    print("rice unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for rice tests
        :return:
        """
        pass

    def teardown(self):
        """
        Teardown routine for rice tests
        :return:
        """

        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    #   dsed * area * pb
    #   (self.dsed * self.area * self.pb)

    def create_rice_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty rice object
        rice_empty = Rice(df_empty, df_empty)
        return rice_empty

    def test_rice_msed_unit(self):
        """
        Unit tests for calcmsed
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        rice_empty = self.create_rice_object()

        try:
            expected_results = [10.0, 2745.135 , 386.7105]
            rice_empty.dsed = pd.Series([1.0, 5.3, 8.25], dtype='float')
            rice_empty.area = pd.Series([10.0, 345.3, 23.437], dtype='float')
            rice_empty.pb = pd.Series([1.0, 1.5, 2.0], dtype='float')
            result = rice_empty.calc_msed()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # (self.dw * self.area) + (self.dsed * self.osed * self.area)
    def test_rice_vw_unit(self):
        """
        Unit tests for calcvw
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        rice_empty = self.create_rice_object()

        try:
            expected_results = [25.89, 2414.5793, 415.6669]
            rice_empty.dw = pd.Series([2.2, 4.56, 12.934], dtype='float')
            rice_empty.area = pd.Series([10.0, 345.3, 23.437], dtype='float')
            rice_empty.dsed = pd.Series([1.0, 5.3, 8.25], dtype='float')
            rice_empty.osed = pd.Series([0.389, 0.459, 0.582], dtype='float')
            result = rice_empty.calc_vw()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # (self.mai/self.area)*10000
    def test_rice_mass_area_unit(self):
        """
        Unittests for calcmass_area
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        rice_empty = self.create_rice_object()

        try:
            expected_results = [8960.0, 2606.4292, 138567.2228]
            rice_empty.area = pd.Series([10.0, 345.3, 23.437], dtype='float')
            rice_empty.mai = pd.Series([8.96, 90.0, 324.76], dtype='float')
            result = rice_empty.calc_mass_area()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # (self.out_mass_area / (self.dw + (self.dsed * (self.osed + (self.pb * self.Kd*1e-5)))))*100
    def test_rice_cw_unit(self):
        """
        unittests for calccw
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        rice_empty = self.create_rice_object()

        try:
            expected_results = [346.0662, 1155.6686, 948.6060]
            rice_empty.dw = pd.Series([2.2, 4.56, 12.934], dtype='float')
            rice_empty.dsed = pd.Series([1.0, 5.3, 8.25], dtype='float')
            rice_empty.osed = pd.Series([0.389, 0.459, 0.582], dtype='float')
            rice_empty.pb = pd.Series([1.0, 1.5, 2.0], dtype='float')
            rice_empty.kd = pd.Series([10.0, 10000.0, 100000.0], dtype='float')
            rice_empty.out_mass_area = pd.Series([8.96, 90.0, 324.76], dtype='float')
            result = rice_empty.calc_cw()
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
    #pass