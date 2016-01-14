import unittest
import pandas as pd
import numpy.testing as npt
import pandas.util.testing as pdt
# the following works when running test script in parent directory as package:
# python -m tests.test_beerex_unittest
# the following works for running as nosetests from parent directory:
from .. import beerex as beerex_model

# load transposed qaqc data for inputs and expected outputs
# csv_transpose_path_in = "./beerex_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# csv_transpose_path_exp = "./beerex_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create empty pandas dataframes to create empty beerex object
df_empty = pd.DataFrame()
beerex_empty = beerex_model.Beerex(df_empty, df_empty)

test = {}


class TestBeerex(unittest.TestCase):
    """
    Unit tests for Beerex.
    """
    def setup(self):
        """
        Setup routine for terrplant unit tests.
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open beerex qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        """
        Teardown routine for terrplant unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

# each of these functions are queued by "run_methods" and have outputs defined as properties in the beerex qaqc csv
    def test_eec_spray(self):
        """
        unittest for function beerex.eec_spray
        """
        # self.out_eec_spray = (110 * self.application_rate) / 1000
        try:
            beerex_empty.application_rate = pd.Series([10.], dtype='int')
            result = beerex_empty.eec_spray()
            npt.assert_array_almost_equal(result, 1.1, 4, '', True)
        finally:
            pass
        return

    def test_eec_soil(self):
        """
        unittest for function beerex.eec_soil
        """
        # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
        #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
        #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        try:
            beerex_empty.log_kow = pd.Series([3.])
            beerex_empty.koc = pd.Series([10.])
            beerex_empty.application_rate = pd.Series([2.])
            result = beerex_empty.eec_soil()
            npt.assert_array_almost_equal(result, 0.022253436, 4, '', True)
        finally:
            pass
        return

    def test_eec_seed(self):
        """
        unittest for function beerex.eec_seed
        """
        # self.out_eec_seed = 1 * (self.lw4_pollen + self.lw4_nectar)/1000
        try:
            beerex_empty.lw4_pollen = pd.Series([4.])
            beerex_empty.lw4_nectar = pd.Series([120.])
            result = beerex_empty.eec_seed()
            npt.assert_array_almost_equal(result, 0.1240, 4, '', True)
        finally:
            pass
        return

    def test_eec_tree(self):
        """
        unittest for function beerex.eec_tree
        """
        # self.out_eec_tree = (self.application_rate/self.mass_tree_vegetation) / 1000
        try:
            beerex_empty.application_rate = pd.Series([5.])
            beerex_empty.mass_tree_vegetation = pd.Series(0.5)
            result = beerex_empty.eec_tree()
            npt.assert_array_almost_equal(result, 0.0100, 4, '', True)
        finally:
            pass
        return

    def test_eec_method(self):
        """
        unittest for function beerex.eec_method
        """
        # if self.application_method == "foliar spray":
        #     self.out_eec_method = self.out_eec_spray
        # elif self.application_method == "soil application":
        #     self.out_eec_method = self.out_eec_soil
        # elif self.application_method == "seed treatment":
        #     self.out_eec_method = self.out_eec_seed
        # elif self.application_method == "tree trunk":
        #     self.out_eec_method = self.out_eec_tree
        # return self.out_eec_method
        try:
            beerex_empty.application_method = pd.Series(["soil application"])
            result = beerex_empty.eec_method()
            npt.assert_string_equal(result, "soil application")