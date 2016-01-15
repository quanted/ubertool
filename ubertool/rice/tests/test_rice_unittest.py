import unittest

import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt

#following works when running test script in parent directory as package:
# python -m tests.stir_unit_test
# following works for running as nosetests from parent directory:
#importing as a package (specified in ../../setup.py)
from .. import rice as rice_model

# create empty pandas dataframes to create empty rice object for testing
df_empty = pd.DataFrame()
# create an empty rice object
rice_empty = rice_model.Rice("empty", df_empty, df_empty)

test = {}


class TestRice(unittest.TestCase):
    """
    Unit tests for Rice.
    """
    def setup(self):
        """
        Setup routine for rice tests
        :return:
        """
        pass
        # sip2 = sip_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

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
    def test_unit_calcmsed(self):
        """
        Unit tests for calcmsed
        :return:
        """
        try:
            rice_empty.dsed = pd.Series([2.2], dtype='float')
            rice_empty.area = pd.Series([3.3], dtype='float')
            rice_empty.pb = pd.Series([4.4], dtype='float')

            result = rice_empty.calc_msed()
            npt.assert_array_almost_equal(result, 31.944, 4, '', True)
        finally:
            pass
        return

    # (self.dw * self.area) + (self.dsed * self.osed * self.area)
    def test_unit_calcvw(self):
        """
        Unit tests for calcvw
        :return:
        """
        try:
            rice_empty.dw = pd.Series([2.2], dtype='float')
            rice_empty.area = pd.Series([3.3], dtype='float')
            rice_empty.dsed = pd.Series([4.4], dtype='float')
            rice_empty.osed = pd.Series([5.5], dtype='float')

            result = rice_empty.calc_vw()
            npt.assert_array_almost_equal(result, 87.12, 4, '', True)
        finally:
            pass
        return

    # (self.mai/self.area)*10000
    def test_unit_calcmass_area(self):
        """
        Unittests for calcmass_area
        :return:
        """
        try:
            rice_empty.area = pd.Series([100.0], dtype='float')
            rice_empty.mai = pd.Series([90.0], dtype='float')
            result = rice_empty.calc_mass_area()
            npt.assert_array_almost_equal(result, 9000.0, 4, '', True)
        finally:
            pass
        return

    # (self.out_mass_area / (self.dw + (self.dsed * (self.osed + (self.pb * self.Kd*1e-5)))))*100
    def test_unit_calccw(self):
        """
        unittests for calccw
        :return:
        """
        try:
            rice_empty.dw = pd.Series([5.0], dtype='float')
            rice_empty.dsed = pd.Series([4.0], dtype='float')
            rice_empty.osed = pd.Series([3.0], dtype='float')
            rice_empty.pb = pd.Series([2.0], dtype='float')
            rice_empty.kd = pd.Series([100000.0], dtype='float')
            rice_empty.out_mass_area = pd.Series([400.0], dtype='float')
            result = rice_empty.calc_cw()
            npt.assert_array_almost_equal(result, 1600.0, 4, '', True)
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