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
            npt.assert_array_almost_equal(result, 0.0010, 4, '', True)
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
        finally:
            pass
        return
    def test_lw1_total_dose(self):
        """
        unittest for function beerex.lw1_total_dose
        """
        # self.out_lw1_total_dose = (self.out_eec_method/100.) * self.lw1_jelly
        try:
            beerex_empty.lw1_jelly = pd.Series([12.5])
            beerex_empty.application_rate = pd.Series([4.])
            beerex_empty.out_eec_method = beerex_empty.eec_spray()
            result = beerex_empty.lw1_total_dose()
            npt.assert_array_almost_equal(result, 0.0550, 4, '', True)
        finally:
            pass
        return

    def test_lw2_total_dose(self):
        """
        unittest for function beerex.lw2_total_dose
        """
        # self.out_lw2_total_dose = (self.out_eec_method/100.) * self.lw2_jelly
        try:
            beerex_empty.lw2_jelly = pd.Series([0.223])
            beerex_empty.application_rate = pd.Series([10.])
            beerex_empty.mass_tree_vegetation = pd.Series([12.5])
            beerex_empty.out_eec_method = beerex_empty.eec_tree()
            result = beerex_empty.lw2_total_dose()
            npt.assert_array_almost_equal(result, 0.000001784, 4, '', True)
        finally:
            pass
        return

    def test_lw3_total_dose(self):
        """
        unittest for function beerex.lw3_total_dose
        """
        # self.out_lw3_total_dose = (self.out_eec_method/100.) * self.lw3_jelly
        try:
            beerex_empty.lw3_jelly = pd.Series([15.2])
            beerex_empty.application_rate = pd.Series([1.6])
            beerex_empty.log_kow = pd.Series([2.])
            beerex_empty.koc = pd.Series([12.5])
            beerex_empty.out_eec_method = beerex_empty.eec_soil()
            result = beerex_empty.lw3_total_dose()
            npt.assert_array_almost_equal(result, 0.0038289, 4, '', True)
        finally:
            pass
        return

    def test_lw4_total_dose(self):
        """
        unittest for function beerex.lw4_total_dose
        """
        # self.out_lw4_total_dose = (self.out_eec_method * self.lw4_pollen) + (self.out_eec_method * self.lw4_nectar)
        try:
            beerex_empty.lw4_pollen = pd.Series([8.5])
            beerex_empty.lw4_nectar = pd.Series([2.3])
            beerex_empty.application_rate = pd.Series([0.75])
            beerex_empty.out_eec_method = beerex_empty.eec_spray()
            result = beerex_empty.lw4_total_dose()
            npt.assert_array_almost_equal(result, 8.9100, 4, '', True)
        finally:
            pass
        return

    def test_lw5_total_dose(self):
        """
        unittest for function beerex.lw5_total_dose
        """
        # self.out_lw5_total_dose = (self.out_eec_method * self.lw5_pollen) + (self.out_eec_method * self.lw5_nectar)
        try:
            beerex_empty.lw5_pollen = pd.Series([2.75])
            beerex_empty.lw5_nectar = pd.Series([5.89])
            beerex_empty.out_eec_method = beerex_empty.eec_seed()
            result = beerex_empty.lw5_total_dose()
            npt.assert_array_almost_equal(result, 0.00864, 4, '', True)
        finally:
            pass
        return

    def test_ld6_total_dose(self):
        """
        unittest for function beerex.ld6_total_dose
        """
        # self.out_ld6_total_dose = (self.out_eec_method * self.ld6_pollen) + (self.out_eec_method * self.ld6_nectar)
        try:
            beerex_empty.ld6_pollen = pd.Series([0.8432])
            beerex_empty.ld6_nectar = pd.Series([12.37])
            beerex_empty.application_rate = pd.Series([5.])
            beerex_empty.out_eec_method = beerex_empty.eec_spray()
            result = beerex_empty.ld6_total_dose()
            npt.assert_array_almost_equal(result,7.26726, 4, '', True)
        finally:
            pass
        return

    def test_lq1_total_dose(self):
        """
        unittest for function beerex.lq1_total_dose
        """
        # self.out_lq1_total_dose = (self.out_eec_method/100.) * self.lq1_jelly
        try:
            beerex_empty.lq1_jelly = pd.Series([1.35])
            beerex_empty.application_rate = pd.Series([5.2])
            beerex_empty.mass_tree_vegetation = pd.Series([12.75])
            beerex_empty.out_eec_method = beerex_empty.eec_tree()
            result = beerex_empty.lq1_total_dose()
            npt.assert_array_almost_equal(result, 0.00000550588235, 4, '', True)
        finally:
            pass
        return

    def test_lq2_total_dose(self):
        """
        unittest for function beerex.lq2_total_dose
        """
        # self.out_lq2_total_dose = (self.out_eec_method/100.) * self.lq2_jelly
        try:
            beerex_empty.lq2_jelly = pd.Series([6.5])
            beerex_empty.out_eec_method = beerex_empty.eec_seed()
            result = beerex_empty.lq2_total_dose()
            npt.assert_array_almost_equal(result, 0.000065)
        finally:
            pass
        return

    def test_lq3_total_dose(self):
        """
        unittest for function beerex.lq3_total_dose
        """
        # self.out_lq3_total_dose = (self.out_eec_method/100.) * self.lq3_jelly
        try:
            beerex_empty.lq3_jelly = pd.Series([14.3])
            beerex_empty.application_rate = pd.Series([3.5])
            beerex_empty.out_eec_method = beerex_empty.eec_spray()
            result = beerex_empty.lq3_total_dose()
            npt.assert_array_almost_equal(result, 0.055055, 4, '', True)
        finally:
            pass
        return

    def test_lq4_total_dose(self):
        """
        unittest for function beerex.lq4_total_dose
        """
        # self.out_lq4_total_dose = (self.out_eec_method/100.) * self.lq4_jelly
        # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
        #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
        #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        try:
            beerex_empty.lq4_jelly = pd.Series([23.65])
            beerex_empty.application_rate = pd.Series([1.45])
            beerex_empty.log_kow = pd.Series([5.])
            beerex_empty.koc = pd.Series([24.1])
            beerex_empty.out_eec_method = beerex_empty.eec_soil()
            result = beerex_empty.lq4_total_dose()
            npt.assert_array_almost_equal(result, 0.172773411, 4, '', True)
        finally:
            pass
        return
