import datetime
import inspect
import numpy as np
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
from tabulate import tabulate
import unittest

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
#from beerex_exe import Beerex
from ..beerex_exe import Beerex

# load transposed qaqc data for inputs and expected outputs
# csv_transpose_path_in = "./beerex_qaqc_in_transpose.csv"
# pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
# print(pd_obj_inputs)
# csv_transpose_path_exp = "./beerex_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)

# create empty pandas dataframes to create empty beerex object
df_empty = pd.DataFrame()
beerex_empty = Beerex(df_empty, df_empty)

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

    # each of these functions are queued by "run_methods" and have
    # outputs defined as properties in the beerex qaqc csv
    def test_eec_spray(self):
        """
        unittest for function beerex.eec_spray
        """
        # self.out_eec_spray = (110 * self.application_rate) / 1000
        try:
            expected_results = [1.1, 0.2750]
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.application_rate = pd.Series([10., 2.5])
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
            result = beerex_empty.out_eec_spray
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_eec_soil(self):
        """
        unittest for function beerex.eec_soil
        """
        # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
        #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
        #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        try:
            expected_results = [0.022253436, 0.0037878124]
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.log_kow = pd.Series([3., 2.2])
            beerex_empty.koc = pd.Series([10., 1.3])
            beerex_empty.application_rate = pd.Series([2., 0.72])
            for i in range(len(expected_results)):
                beerex_empty.eec_soil(i)
            result = beerex_empty.out_eec_soil
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_eec_seed(self):
        """
        unittest for function beerex.eec_seed
        """
        # self.out_eec_seed = 1./1000. ??
        # self.out_eec_seed = 1 * (self.lw4_pollen + self.lw4_nectar)/1000
        try:
            expected_results = [0.0010, 0.001]
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.lw4_pollen = pd.Series([4., 0.3])
            beerex_empty.lw4_nectar = pd.Series([120., 2.8])
            for i in range(len(expected_results)):
                beerex_empty.eec_seed(i)
            result = beerex_empty.out_eec_seed
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(str(tab), headers='keys', tablefmt='rst'))
        return

    def test_beerex_eec_tree(self):
        """
        unittest for function beerex.eec_tree
        """
        # self.out_eec_tree = (self.application_rate/self.mass_tree_vegetation) / 1000
        try:
            expected_results = [0.0100, 0.00011157]
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.application_rate = pd.Series([5., 2.7])
            beerex_empty.mass_tree_vegetation = pd.Series([0.5, 24.2])
            for i in range(len(expected_results)):
                beerex_empty.eec_tree(i)
            results = beerex_empty.out_eec_tree
            npt.assert_array_almost_equal(results, expected_results, 4, '', True)
        finally:
            tab = [results, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # def test_beerex_eec_method(self):
    #     """
    #     unittest for function beerex.eec_method
    #     """
    #     # if self.application_method == "foliar spray":
    #     #     self.out_eec_method = self.out_eec_spray
    #     # elif self.application_method == "soil application":
    #     #     self.out_eec_method = self.out_eec_soil
    #     # elif self.application_method == "seed treatment":
    #     #     self.out_eec_method = self.out_eec_seed
    #     # elif self.application_method == "tree trunk":
    #     #     self.out_eec_method = self.out_eec_tree
    #     # return self.out_eec_method
    #
    #     # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
    #     #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
    #     #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
    #     try:
    #         expected_results = [0.0010, 0.0031858]
    #         beerex_empty.application_method = pd.Series(['seed treatment', 'soil application'])
    #         beerex_empty.koc = pd.Series([0.76, 0.76])
    #         beerex_empty.log_kow = pd.Series([1.6, 1.6])
    #         beerex_empty.application_rate = pd.Series([1., 1.])
    #         beerex_empty.out_eec_method = pd.Series([3., 3.])
    #         beerex_empty.eec_method()
    #         result = beerex_empty.out_eec_method
    #         npt.assert_array_almost_equal(result, expected_results, 4, '', True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(str(tab), headers='keys', tablefmt='rst'))
    #     return

    def test_beerex_lw1_total_dose(self):
        """
        unittest for function beerex.lw1_total_dose
        """
        # self.out_lw1_total_dose = (self.out_eec_method/100.) * self.lw1_jelly
        try:
            expected_results = [0.0550, 0.006765]
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.lw1_jelly = pd.Series([12.5, 8.2])
            beerex_empty.application_rate = pd.Series([4., 0.75])
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lw1_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
                beerex_empty.out_eec = beerex_empty.out_eec_spray
                beerex_empty.lw1_total_dose()
            result = beerex_empty.out_lw1_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw2_total_dose(self):
        """
        unittest for function beerex.lw2_total_dose
        """
        # self.out_lw2_total_dose = (self.out_eec_method/100.) * self.lw2_jelly
        try:
            expected_results = [0.000001784, 0.000007386]
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.lw2_jelly = pd.Series([0.223, 2.5])
            beerex_empty.application_rate = pd.Series([10., 6.5])
            beerex_empty.mass_tree_vegetation = pd.Series([12.5, 22.])
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lw2_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_tree(i)
                beerex_empty.out_eec = beerex_empty.out_eec_tree
                beerex_empty.lw2_total_dose()
            result = beerex_empty.out_lw2_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw3_total_dose(self):
        """
        unittest for function beerex.lw3_total_dose
        """
        # self.out_lw3_total_dose = (self.out_eec_method/100.) * self.lw3_jelly
        # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
        #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
        #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        try:
            expected_results = [0.00058199, 0.000220323]
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.lw3_jelly = pd.Series([15.2, 3.2])
            beerex_empty.application_rate = pd.Series([1.6, 2.1])
            beerex_empty.log_kow = pd.Series([2., 2.1])
            beerex_empty.koc = pd.Series([12.5, 7.6])
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lw3_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_soil(i)
                beerex_empty.out_eec = beerex_empty.out_eec_soil
                beerex_empty.lw3_total_dose()
            result = beerex_empty.out_lw3_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw4_total_dose(self):
        """
        unittest for function beerex.lw4_total_dose
        """
        #if self.empirical_residue[0] == True:
        #   self.out_lw4_total_dose = ((self.empirical_pollen/1000.) * self.lw4_pollen) + ((self.empirical_nectar/1000.) * self.lw4_nectar)
        #else:
        #    self.out_lw4_total_dose = (self.out_eec_method * self.lw4_pollen) + (self.out_eec_method * self.lw4_nectar)

        # self.out_eec_spray = (110 * self.application_rate) / 1000
        try:
            expected_results = [0.04387, 0.011578]
            beerex_empty.empirical_residue = pd.Series(["yes", "yes"])
            beerex_empty.empirical_pollen = pd.Series([3.7, 4.3])
            beerex_empty.empirical_nectar = pd.Series([5.4, 1.2])
            beerex_empty.lw4_pollen = pd.Series([8.5, 2.5])
            beerex_empty.lw4_nectar = pd.Series([2.3, 0.69])
            beerex_empty.application_rate = pd.Series([0.75, 0.48])
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lw4_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
                beerex_empty.out_eec = beerex_empty.out_eec_spray
                beerex_empty.lw4_total_dose()
            result = beerex_empty.out_lw4_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw5_total_dose(self):
        """
        unittest for function beerex.lw5_total_dose
        """
        #if self.empirical_residue[0] == True:
        #    self.out_lw5_total_dose = ((self.empirical_pollen/1000.) * self.lw5_pollen) + ((self.empirical_nectar/1000.) * self.lw5_nectar)
        #else:
        #    self.out_lw5_total_dose = (self.out_eec_method * self.lw5_pollen) + (self.out_eec_method * self.lw5_nectar)
        try:
            expected_results = [0.032169, 0.07042]
            beerex_empty.empirical_residue = pd.Series(["yes", "yes"])
            beerex_empty.empirical_pollen = pd.Series([7.2, 12.2])
            beerex_empty.empirical_nectar = pd.Series([2.1, 1.6])
            beerex_empty.lw5_pollen = pd.Series([2.75, 5.3])
            beerex_empty.lw5_nectar = pd.Series([5.89, 3.6])
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lw5_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_seed(i)
                beerex_empty.out_eec = beerex_empty.out_eec_seed
                beerex_empty.lw5_total_dose()
            result = beerex_empty.out_lw5_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_ld6_total_dose(self):
        """
        unittest for function beerex.ld6_total_dose
        """
        #if self.empirical_residue[0] == True:
        #    self.out_ld6_total_dose = ((self.empirical_pollen/1000.) * self.ld6_pollen) + ((self.empirical_nectar/1000.) * self.ld6_nectar)
        #else:
        #    self.out_ld6_total_dose = (self.out_eec_method * self.ld6_pollen) + (self.out_eec_method * self.ld6_nectar)
        try:
            expected_results = [0.03708036, 0.0437]
            beerex_empty.empirical_residue = pd.Series(["yes", "yes"])
            beerex_empty.empirical_pollen = pd.Series([7.3, 4.5])
            beerex_empty.empirical_nectar = pd.Series([2.5, 11.])
            beerex_empty.ld6_pollen = pd.Series([0.8432, 3.6])
            beerex_empty.ld6_nectar = pd.Series([12.37, 2.5])
            beerex_empty.application_rate = pd.Series([5., 4.2])
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_ld6_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
                beerex_empty.out_eec = beerex_empty.out_eec_spray
                beerex_empty.ld6_total_dose()
            result = beerex_empty.out_ld6_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq1_total_dose(self):
        """
        unittest for function beerex.lq1_total_dose
        """
        # self.out_lq1_total_dose = (self.out_eec_method/100.) * self.lq1_jelly
        try:
            expected_results = [0.00000550588235, 0.00000177455]
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.lq1_jelly = pd.Series([1.35, 5.3])
            beerex_empty.application_rate = pd.Series([5.2, 0.75])
            beerex_empty.mass_tree_vegetation = pd.Series([12.75, 22.4])
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lq1_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_tree(i)
                beerex_empty.out_eec = beerex_empty.out_eec_tree
                beerex_empty.lq1_total_dose()
            result = beerex_empty.out_lq1_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq2_total_dose(self):
        """
        unittest for function beerex.lq2_total_dose
        """
        # self.out_lq2_total_dose = (self.out_eec_method/100.) * self.lq2_jelly
        try:
            expected_results = [0.000065, 0.000028]
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.lq2_jelly = pd.Series([6.5, 2.8])
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lq2_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_seed(i)
                beerex_empty.out_eec = beerex_empty.out_eec_seed
                beerex_empty.lq2_total_dose()
            result = beerex_empty.out_lq2_total_dose
            npt.assert_array_almost_equal(result, expected_results)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq3_total_dose(self):
        """
        unittest for function beerex.lq3_total_dose
        """
        # self.out_lq3_total_dose = (self.out_eec_method/100.) * self.lq3_jelly
        try:
            expected_results = [0.055055, 0.0132]
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.lq3_jelly = pd.Series([14.3, 7.5])
            beerex_empty.application_rate = pd.Series([3.5, 1.6])
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lq3_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
                beerex_empty.out_eec = beerex_empty.out_eec_spray
                beerex_empty.lq3_total_dose()
            result = beerex_empty.out_lq3_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq4_total_dose(self):
        """
        unittest for function beerex.lq4_total_dose
        """
        #if self.empirical_residue[0] == True:
        #    self.out_lq4_total_dose = (self.empirical_jelly/1000.) * self.lq4_jelly
        #else:
        #    self.out_lq4_total_dose = (self.out_eec_method/100.) * self.lq4_jelly
        try:
            expected_results = [0.15136, 0.48521]
            beerex_empty.empirical_residue = pd.Series(["yes", "yes"])
            beerex_empty.empirical_jelly = pd.Series([6.4, 12.1])
            beerex_empty.lq4_jelly = pd.Series([23.65, 40.1])
            beerex_empty.application_rate = pd.Series([1.45, 2.3])
            beerex_empty.log_kow = pd.Series([5., 3.1])
            beerex_empty.koc = pd.Series([24.1, 12.4])
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_lq4_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_soil(i)
                beerex_empty.out_eec = beerex_empty.out_eec_soil
                beerex_empty.lq4_total_dose()
            result = beerex_empty.out_lq4_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_cell_total_dose(self):
        """
        unittest for function beerex.aw_cell_total_dose
        """
        # self.out_aw_cell_total_dose = (self.out_eec_method * self.aw_cell_nectar) + (self.out_eec_method * self.aw_cell_pollen)
        try:
            expected_results = [0.0037, 0.0176]
            beerex_empty.aw_cell_pollen = pd.Series([2.4, 12.3])
            beerex_empty.aw_cell_nectar = pd.Series([1.3, 5.3])
            beerex_empty.empirical_residue = (["no", "no"])
            beerex_empty.out_aw_cell_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_seed(i)
                beerex_empty.out_eec = beerex_empty.out_eec_seed
                beerex_empty.aw_cell_total_dose()
            result = beerex_empty.out_aw_cell_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_brood_total_dose(self):
        """
        unittest for function beerex.aw_brood_total_dose
        """
        # self.out_aw_brood_total_dose = (self.out_eec_method * self.aw_brood_nectar) + (self.out_eec_method * self.aw_brood_pollen)
        try:
            expected_results = [23.0725, 6.5472]
            beerex_empty.out_aw_brood_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.aw_brood_pollen = pd.Series([5.7, 6.5])
            beerex_empty.aw_brood_nectar = pd.Series([78.2, 43.1])
            beerex_empty.application_rate = pd.Series([2.5, 1.2])
            beerex_empty.n_runs = len(expected_results)
            beerex_empty.empirical_residue = (["no", "no"])
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
                beerex_empty.out_eec = beerex_empty.out_eec_spray
                beerex_empty.aw_brood_total_dose()
            result = beerex_empty.out_aw_brood_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_comb_total_dose(self):
        """
        unittest for function beerex.aw_comb_total_dose
        """
        # self.out_aw_comb_total_dose = (self.out_eec_method * self.aw_comb_nectar) + (self.out_eec_method * self.aw_comb_pollen)
        # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
        #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
        #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        try:
            expected_results = [1.2011859, 0.118363]
            beerex_empty.aw_comb_pollen = pd.Series([6.2, 35.1])
            beerex_empty.aw_comb_nectar = pd.Series([25.9, 12.4])
            beerex_empty.log_kow = pd.Series([3.4, 0.63])
            beerex_empty.koc = pd.Series([16.2, 2.5])
            beerex_empty.application_rate = pd.Series([2.1, 1.3])
            beerex_empty.empirical_residue = (["no", "no"])
            beerex_empty.out_aw_comb_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_soil(i)
                beerex_empty.out_eec = beerex_empty.out_eec_soil
                beerex_empty.aw_comb_total_dose()
            result = beerex_empty.out_aw_comb_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_pollen_total_dose(self):
        """
        unittest for function beerex.aw_pollen_total_dose
        """
        # self.out_aw_pollen_total_dose = (self.out_eec_method * self.aw_fpollen_nectar) + (self.out_eec_method * self.aw_fpollen_pollen)
        try:
            expected_results = [0.015225, 0.000689367]
            beerex_empty.aw_fpollen_pollen = pd.Series([6.7, 12.4])
            beerex_empty.aw_fpollen_nectar = pd.Series([54.2, 26.5])
            beerex_empty.application_rate = pd.Series([4.2, 0.98])
            beerex_empty.mass_tree_vegetation = pd.Series([16.8, 55.3])
            beerex_empty.n_runs = len(expected_results)
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_aw_pollen_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            for i in range(len(expected_results)):
                beerex_empty.eec_tree(i)
                beerex_empty.out_eec = beerex_empty.out_eec_tree
                beerex_empty.aw_pollen_total_dose()
            result = beerex_empty.out_aw_pollen_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_nectar_total_dose(self):
        """
        unittest for function beerex.aw_nectar_total_dose
        """
        # self.out_aw_nectar_total_dose = (self.out_eec_method * self.aw_fnectar_nectar) + (self.out_eec_method * self.aw_fnectar_pollen)
        try:
            expected_results = [0.0273, 0.0296]
            beerex_empty.aw_fnectar_pollen = pd.Series([3.8, 16.9])
            beerex_empty.aw_fnectar_nectar = pd.Series([23.5, 12.7])
            beerex_empty.out_aw_nectar_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            beerex_empty.empirical_residue = (["no", "no"])
            for i in range(len(expected_results)):
                beerex_empty.eec_seed(i)
                beerex_empty.out_eec = beerex_empty.out_eec_seed
                beerex_empty.aw_nectar_total_dose()
            result = beerex_empty.out_aw_nectar_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_winter_total_dose(self):
        """
        unittest for function beerex.aw_winter_total_dose
        """
        # self.out_aw_winter_total_dose = (self.out_eec_method * self.aw_winter_nectar) + (self.out_eec_method * self.aw_winter_pollen)
        try:
            expected_results = [0.013073320537, 0.0016036363]
            beerex_empty.aw_winter_pollen = pd.Series([8.2, 6.9])
            beerex_empty.aw_winter_nectar = pd.Series([86.4, 22.5])
            beerex_empty.application_rate = pd.Series([7.2, 1.5])
            beerex_empty.mass_tree_vegetation = pd.Series([52.1, 27.5])
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_aw_winter_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            for i in range(len(expected_results)):
                beerex_empty.eec_tree(i)
                beerex_empty.out_eec = beerex_empty.out_eec_tree
                beerex_empty.aw_winter_total_dose()
            result = beerex_empty.out_aw_winter_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_ad_total_dose(self):
        """
        unittest for function beerex.ad_total_dose
        """
        #if self.empirical_residue[0] == True:
        #    self.out_ad_total_dose = ((self.empirical_nectar/1000.) * self.ad_nectar) + ((self.empirical_pollen/1000.) * self.ad_pollen)
        #else:
        #    self.out_ad_total_dose = (self.out_eec_method * self.ad_nectar) + (self.out_eec_method * self.ad_pollen)

        try:
            expected_results = [0.02904, 0.10844]
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_ad_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.empirical_residue = pd.Series(["yes", "yes"])
            beerex_empty.ad_pollen = pd.Series([2.4, 36.5])
            beerex_empty.ad_nectar = pd.Series([22.8, 2.1])
            beerex_empty.application_rate = pd.Series([8.9, 0.88])
            beerex_empty.empirical_nectar = pd.Series([1.2, 13.4])
            beerex_empty.empirical_pollen = pd.Series([0.7, 2.2])
            beerex_empty.n_runs = len(expected_results)
            for i in range(len(expected_results)):
                beerex_empty.eec_spray(i)
                beerex_empty.ad_total_dose()
            result = beerex_empty.out_ad_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
            tab = [result, expected_results]
        except ValueError:
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aq_total_dose(self):
        """
        unittest for function beerex.aq_total_dose
        """
        # self.out_aq_total_dose = (self.out_eec_method/100.) * self.aq_jelly
        # self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
        #                     (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
        #                     (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        try:
            expected_results = [-85.7931737, 0.021943272]
            beerex_empty.out_eec_soil = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_spray = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_seed = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec_tree = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_eec = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.out_aq_total_dose = pd.Series(np.nan, index=range(len(expected_results)), dtype="float")
            beerex_empty.n_runs = len(expected_results)
            beerex_empty.empirical_residue = pd.Series(["no", "no"])
            beerex_empty.aq_jelly = pd.Series([223., 68.7])
            beerex_empty.log_kow = pd.Series([6.3, 2.4])
            beerex_empty.koc = pd.Series([4.1, 25.4])
            beerex_empty.application_rate = pd.Series([3.4, 12.4])
            for i in range(len(expected_results)):
                print(i)
                beerex_empty.eec_soil(i)
                beerex_empty.out_eec = beerex_empty.out_eec_soil
                beerex_empty.aq_total_dose()
            result = beerex_empty.out_aq_total_dose
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw1_acute_rq(self):
        """
        unittest for function beerex.lw1_acute_rq
        """
        # self.out_lw1_acute_rq = self.out_lw1_total_dose/self.larval_ld50
        try:
            expected_results = [5.259259, 0.34929577]
            beerex_empty.out_lw1_total_dose = pd.Series([14.2, 12.4])
            beerex_empty.larval_ld50 = pd.Series([2.7, 35.5])
            result = beerex_empty.lw1_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw2_acute_rq(self):
        """
        unittest for function beerex.lw2_acute_rq
        """
        # self.out_lw2_acute_rq = self.out_lw2_total_dose/self.larval_ld50
        try:
            expected_results = [0.35570469, 2.13461538]
            beerex_empty.out_lw2_total_dose = pd.Series([5.3, 22.2])
            beerex_empty.larval_ld50 = pd.Series([14.9, 10.4])
            result = beerex_empty.lw2_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw3_acute_rq(self):
        """
        unittest for function beerex.lw3_acute_rq
        """
        # self.out_lw3_acute_rq = self.out_lw3_total_dose/self.larval_ld50
        try:
            expected_results = [3.373563, 0.20754717]
            beerex_empty.out_lw3_total_dose = pd.Series([58.7, 1.1])
            beerex_empty.larval_ld50 = pd.Series([17.4, 5.3])
            result = beerex_empty.lw3_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw4_acute_rq(self):
        """
        unittest for function beerex.lw4_acute_rq
        """
        # self.out_lw4_acute_rq = self.out_lw4_total_dose/self.larval_ld50
        try:
            expected_results = [3.782608, 1.57142857]
            beerex_empty.out_lw4_total_dose = pd.Series([8.7, 2.2])
            beerex_empty.larval_ld50 = pd.Series([2.3, 1.4])
            result = beerex_empty.lw4_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw5_acute_rq(self):
        """
        unittest for function beerex.lw5_acute_rq
        """
        # self.out_lw5_acute_rq = self.out_lw5_total_dose/self.larval_ld50
        try:
            expected_results = [20.08333, 2.672727273]
            beerex_empty.out_lw5_total_dose = pd.Series([24.1, 14.7])
            beerex_empty.larval_ld50 = pd.Series([1.2, 5.5])
            result = beerex_empty.lw5_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_ld6_acute_rq(self):
        """
        unittest for function beerex.ld6_acute_rq
        """
        # self.out_ld6_acute_rq = self.out_ld6_total_dose/self.larval_ld50
        try:
            expected_results = [0.782258, 5.82142857]
            beerex_empty.out_ld6_total_dose = pd.Series([9.7, 16.3])
            beerex_empty.larval_ld50 = pd.Series([12.4, 2.8])
            result = beerex_empty.ld6_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq1_acute_rq(self):
        """
        unittest for function beerex.lq1_acute_rq
        """
        # self.out_lq1_acute_rq = self.out_lq1_total_dose/self.larval_ld50
        try:
            expected_results = [1.7420, 0.2068966]
            beerex_empty.out_lq1_total_dose = pd.Series([174.2, 3.6])
            beerex_empty.larval_ld50 = pd.Series([100., 17.4])
            result = beerex_empty.lq1_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq2_acute_rq(self):
        """
        unittest for function beerex.lq2_acute_rq
        """
        # self.out_lq2_acute_rq = self.out_lq2_total_dose/self.larval_ld50
        try:
            expected_results = [1.77011, 0.5789474]
            beerex_empty.out_lq2_total_dose = pd.Series([15.4, 2.2])
            beerex_empty.larval_ld50 = pd.Series([8.7, 3.8])
            result = beerex_empty.lq2_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq3_acute_rq(self):
        """
        unittest for function beerex.lq3_acute_rq
        """
        # self.out_lq3_acute_rq = self.out_lq3_total_dose/self.larval_ld50
        try:
            expected_results = [7.659793, 1.6623377]
            beerex_empty.out_lq3_total_dose = pd.Series([74.3, 25.6])
            beerex_empty.larval_ld50 = pd.Series([9.7, 15.4])
            result = beerex_empty.lq3_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq4_acute_rq(self):
        """
        unittest for function beerex.lq4_acute_rq
        """
        # self.out_lq4_acute_rq = self.out_lq4_total_dose/self.larval_ld50
        try:
            expected_results = [0.3620689, 9.782608696]
            beerex_empty.out_lq4_total_dose = pd.Series([6.3, 22.5])
            beerex_empty.larval_ld50 = pd.Series([17.4, 2.3])
            result = beerex_empty.lq4_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_cell_acute_rq(self):
        """
        unittest for function beerex.aw_cell_acute_rq
        """
        # self.out_aw_cell_total_dose self.out_aw_cell_total_dose/self.adult_oral_ld50
        try:
            expected_results = [6.154929, 2.48]
            beerex_empty.out_aw_cell_total_dose = pd.Series([87.4, 18.6])
            beerex_empty.adult_oral_ld50 = pd.Series([14.2, 7.5])
            result = beerex_empty.aw_cell_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_brood_acute_rq(self):
        """
        unittest for function beerex.aw_brood_acute_rq
        """
        # self.out_aw_brood_total_dose self.out_aw_brood_total_dose/self.adult_oral_ld50
        try:
            expected_results = [10.68181, 1.823529412]
            beerex_empty.out_aw_brood_total_dose = pd.Series([23.5, 12.4])
            beerex_empty.adult_oral_ld50 = pd.Series([2.2, 6.8])
            result = beerex_empty.aw_brood_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_comb_acute_rq(self):
        """
        unittest for function beerex.aw_comb_acute_rq
        """
        # self.out_aw_comb_total_dose self.out_aw_comb_total_dose/self.adult_oral_ld50
        try:
            expected_results = [1.95031, 1.2378378]
            beerex_empty.out_aw_comb_total_dose = pd.Series([62.8, 22.9])
            beerex_empty.adult_oral_ld50 = pd.Series([32.2, 18.5])
            result = beerex_empty.aw_comb_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_pollen_acute_rq(self):
        """
        unittest for function beerex.aw_pollen_acute_rq
        """
        # self.out_aw_pollen_total_dose self.out_aw_pollen_total_dose/self.adult_oral_ld50
        try:
            expected_results = [0.884615, 2.6377953]
            beerex_empty.out_aw_pollen_total_dose = pd.Series([6.9, 33.5])
            beerex_empty.adult_oral_ld50 = pd.Series([7.8, 12.7])
            result = beerex_empty.aw_pollen_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_nectar_acute_rq(self):
        """
        unittest for function beerex.aw_nectar_acute_rq
        """
        # self.out_aw_nectar_total_dose self.out_aw_nectar_total_dose/self.adult_oral_ld50
        try:
            expected_results = [4.83333, 0.187919463]
            beerex_empty.out_aw_nectar_total_dose = pd.Series([124.7, 2.8])
            beerex_empty.adult_oral_ld50 = pd.Series([25.8, 14.9])
            result = beerex_empty.aw_nectar_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_winter_acute_rq(self):
        """
        unittest for function beerex.aw_winter_acute_rq
        """
        # self.out_aw_winter_total_dose self.out_aw_winter_total_dose/self.adult_oral_ld50
        try:
            expected_results = [0.079411, 1.1414141414]
            beerex_empty.out_aw_winter_total_dose = pd.Series([0.54, 22.6])
            beerex_empty.adult_oral_ld50 = pd.Series([6.8, 19.8])
            result = beerex_empty.aw_winter_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_ad_acute_rq(self):
        """
        unittest for function beerex.ad_acute_rq
        """
        # self.out_ad_acute_rq = self.out_ad_total_dose/self.adult_oral_ld50
        try:
            expected_results = [4.438596, 0.1464968]
            beerex_empty.out_ad_total_dose = pd.Series([25.3, 2.3])
            beerex_empty.adult_oral_ld50 = pd.Series([5.7, 15.7])
            result = beerex_empty.ad_acute_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aq_acute_rq(self):
        """
        unittest for function beerex.aq_acute_rq
        """
        # self.out_aq_acute_rq = self.out_aq_total_dose/self.adult_oral_ld50
        try:
            expected_results = [5.266129, 0.01744186]
            beerex_empty.out_aq_total_dose = pd.Series([65.3, 0.15])
            beerex_empty.adult_oral_ld50 = pd.Series([12.4, 8.6])
            result = beerex_empty.aq_acute_rq()
            npt.assert_array_almost_equal(result, expected_results)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw1_chronic_rq(self):
        """
        unittest for function beerex.lw1_chronic_rq
        """
        # self.out_lw1_chronic_rq = self.out_lw1_total_dose/self.larval_noael
        try:
            expected_results = [3.22222, 0.220125786]
            beerex_empty.out_lw1_total_dose = pd.Series([23.2, 3.5])
            beerex_empty.larval_noael = pd.Series([7.2, 15.9])
            result = beerex_empty.lw1_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw2_chronic_rq(self):
        """
        unittest for function beerex.lw2_chronic_rq
        """
        # self.out_lw2_chronic_rq = self.out_lw2_total_dose/self.larval_noael
        try:
            expected_results = [11.369565, 2.76712329]
            beerex_empty.out_lw2_total_dose = pd.Series([52.3, 20.2])
            beerex_empty.larval_noael = pd.Series([4.6, 7.3])
            result = beerex_empty.lw2_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw3_chronic_rq(self):
        """
        unittest for function beerex.lw3_chronic_rq
        """
        # self.out_lw3_chronic_rq = self.out_lw3_total_dose/self.larval_noael
        try:
            expected_results = [2.47826, 1.03164557]
            beerex_empty.out_lw3_total_dose = pd.Series([5.7, 16.3])
            beerex_empty.larval_noael = pd.Series([2.3, 15.8])
            result = beerex_empty.lw3_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw4_chronic_rq(self):
        """
        unittest for function beerex.lw4_chronic_rq
        """
        # self.out_lw4_chronic_rq = self.out_lw4_total_dose/self.larval_noael
        try:
            expected_results = [1.237069, 32.625]
            beerex_empty.out_lw4_total_dose = pd.Series([28.7, 78.3])
            beerex_empty.larval_noael = pd.Series([23.2, 2.4])
            result = beerex_empty.lw4_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lw5_chronic_rq(self):
        """
        unittest for function beerex.lw5_chronic_rq
        """
        # self.out_lw5_chronic_rq = self.out_lw5_total_dose/self.larval_noael
        try:
            expected_results = [0.1750, 0.01688889]
            beerex_empty.out_lw5_total_dose = pd.Series([2.1, 0.38])
            beerex_empty.larval_noael = pd.Series([12., 22.5])
            result = beerex_empty.lw5_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_ld6_chronic_rq(self):
        """
        unittest for function beerex.ld6_chronic_rq
        """
        # self.out_ld6_chronic_rq = self.out_ld6_total_dose/self.larval_noael
        try:
            expected_results = [1.3406432, 0.28125]
            beerex_empty.out_ld6_total_dose = pd.Series([91.7, 3.6])
            beerex_empty.larval_noael = pd.Series([68.4, 12.8])
            result = beerex_empty.ld6_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq1_chronic_rq(self):
        """
        unittest for function beerex.lq1_chronic_rq
        """
        # self.out_lq1_chronic_rq = self.out_lq1_total_dose/self.larval_noael
        try:
            expected_results = [0.078947, 272.0833333]
            beerex_empty.out_lq1_total_dose = pd.Series([1.2, 65.3])
            beerex_empty.larval_noael = pd.Series([15.2, 0.24])
            result = beerex_empty.lq1_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq2_chronic_rq(self):
        """
        unittest for function beerex.lq2_chronic_rq
        """
        # self.out_lq2_chronic_rq = self.out_lq2_total_dose/self.larval_noael
        try:
            expected_results = [0.0588235, 0.01617647]
            beerex_empty.out_lq2_total_dose = pd.Series([4.2, 0.11])
            beerex_empty.larval_noael = pd.Series([71.4, 6.8])
            result = beerex_empty.lq2_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq3_chronic_rq(self):
        """
        unittest for function beerex.lq3_chronic_rq
        """
        # self.out_lq3_chronic_rq = self.out_lq3_total_dose/self.larval_noael
        try:
            expected_results = [0.503448, 0.44072165]
            beerex_empty.out_lq3_total_dose = pd.Series([7.3, 34.2])
            beerex_empty.larval_noael = pd.Series([14.5, 77.6])
            result = beerex_empty.lq3_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_lq4_chronic_rq(self):
        """
        unittest for function beerex.lq4_chronic_rq
        """
        # self.out_lq4_chronic_rq = self.out_lq4_total_dose/self.larval_noael
        try:
            expected_results = [0.169863, 0.19411765]
            beerex_empty.out_lq4_total_dose = pd.Series([6.2, 0.33])
            beerex_empty.larval_noael = pd.Series([36.5, 1.7])
            result = beerex_empty.lq4_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_cell_chronic_rq(self):
        """
        unittest for function beerex.aw_cell_chronic_rq
        """
        # self.out_aw_cell_total_dose = self.out_aw_cell_total_dose/self.adult_oral_noael
        try:
            expected_results = [3.652174, 5.1206897]
            beerex_empty.out_aw_cell_total_dose = pd.Series([8.4, 29.7])
            beerex_empty.adult_oral_noael = pd.Series([2.3, 5.8])
            result = beerex_empty.aw_cell_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_brood_chronic_rq(self):
        """
        unittest for function beerex.aw_brood_chronic_rq
        """
        # self.out_aw_brood_total_dose = self.out_aw_brood_total_dose/self.adult_oral_noael
        try:
            expected_results = [0.22727, 2.8023256]
            beerex_empty.out_aw_brood_total_dose = pd.Series([0.5, 24.1])
            beerex_empty.adult_oral_noael = pd.Series([2.2, 8.6])
            result = beerex_empty.aw_brood_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_comb_chronic_rq(self):
        """
        unittest for function beerex.aw_comb_chronic_rq
        """
        # self.out_aw_comb_total_dose = self.out_aw_comb_total_dose/self.adult_oral_noael
        try:
            expected_results = [4.00000, 0.74712644]
            beerex_empty.out_aw_comb_total_dose = pd.Series([12.8, 0.65])
            beerex_empty.adult_oral_noael = pd.Series([3.2, 0.87])
            result = beerex_empty.aw_comb_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_pollen_chronic_rq(self):
        """
        unittest for function beerex.aw_pollen_chronic_rq
        """
        # self.out_aw_pollen_total_dose = self.out_aw_pollen_total_dose/self.adult_oral_noael
        try:
            expected_results = [1.724489, 4.1627907]
            beerex_empty.out_aw_pollen_total_dose = pd.Series([16.9, 17.9])
            beerex_empty.adult_oral_noael = pd.Series([9.8, 4.3])
            result = beerex_empty.aw_pollen_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_nectar_chronic_rq(self):
        """
        unittest for function beerex.aw_nectar_chronic_rq
        """
        # self.out_aw_nectar_total_dose = self.out_aw_nectar_total_dose/self.adult_oral_noael
        try:
            expected_results = [0.1821705, 0.05147059]
            beerex_empty.out_aw_nectar_total_dose = pd.Series([4.7, 0.35])
            beerex_empty.adult_oral_noael = pd.Series([25.8, 6.8])
            result = beerex_empty.aw_nectar_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aw_winter_chronic_rq(self):
        """
        unittest for function beerex.aw_winter_chronic_rq
        """
        # self.out_aw_winter_total_dose = self.out_aw_winter_total_dose/self.adult_oral_noael
        try:
            expected_results = [7.941176, 7.5080645]
            beerex_empty.out_aw_winter_total_dose = pd.Series([54., 93.1])
            beerex_empty.adult_oral_noael = pd.Series([6.8, 12.4])
            result = beerex_empty.aw_winter_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_ad_chronic_rq(self):
        """
        unittest for function beerex.ad_acute_rq
        """
        # self.out_ad_chronic_rq = self.out_ad_total_dose/self.adult_oral_noael
        try:
            expected_results = [0.44094488, 0.41176471]
            beerex_empty.out_ad_total_dose = pd.Series([5.6, 1.4])
            beerex_empty.adult_oral_noael = pd.Series([12.7, 3.4])
            result = beerex_empty.ad_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_beerex_aq_chronic_rq(self):
        """
        unittest for function beerex.aq_chronic_rq
        """
        # self.out_aq_chronic_rq = self.out_aq_total_dose/self.adult_oral_noael
        try:
            expected_results = [0.226496, 29.0000]
            beerex_empty.out_aq_total_dose = pd.Series([5.3, 11.6])
            beerex_empty.adult_oral_noael = pd.Series([23.4, 0.4])
            result = beerex_empty.aq_chronic_rq()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return
