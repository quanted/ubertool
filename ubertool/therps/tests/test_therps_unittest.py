from __future__ import division  #brings in Python 3.0 mixed type calculation rules
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

print("Python version: " + sys.version)
print("Numpy version: " + np.__version__)

#find parent directory and import model
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)
from therps_exe import THerps

# create empty pandas dataframes to create empty object for testing
df_empty = pd.DataFrame()
# create an empty therps object
therps_empty = THerps(df_empty, df_empty)

test = {}

class Testtherps(unittest.TestCase):
    """
    Unit tests for T-Rex model.
    """
    print("THerps unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for therps unit tests.
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open therps qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for therps unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_convert_app_intervals(self):
        """
        unit test for function convert_app_intervals
        the method converts number of applications and application interval into application rates and day of year number
        this is so that the same concentration timeseries method from trex_functions can be reused here
        :return:
        """
        result_day_out = pd.Series([], dtype="object")
        result_app_rates = pd.Series([], dtype="object")

        expected_result_day_out = pd.Series([[0,6,13], [0], [0,20,41,62], [0,6,13]], dtype = 'object')
        expected_result_app_rates = pd.Series([[1.2,1.2,1.2], [2.3], [2.5,2.5,2.5,2.5], [5.1,5.1,5.1]], dtype = 'object')
        try:
            therps_empty.num_apps = [3,1,4,3]
            therps_empty.app_interval = [7,1,21,7]
            therps_empty.application_rate = [1.2, 2.3, 2.5,5.1]
            result_day_out, result_app_rates = therps_empty.convert_app_intervals()
                #using pdt.assert_series_equal assertion instead of npt.assert_allclose
                #because npt.assert_allclose does not handle uneven object/series lists
                #Note that pdt.assert_series_equal requires object/series to be exactly equal
                #this is ok in this instance because we are not "calculating" real numbers
                #but rather simply distributing them from an input value into a new object/series
            pdt.assert_series_equal(result_app_rates,expected_result_app_rates)
            pdt.assert_series_equal(result_day_out,expected_result_day_out)
        finally:
            tab1 = [result_app_rates, expected_result_app_rates]
            tab2 = [result_day_out, expected_result_day_out]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    # def test_app_rate_parsing(self):
    #     """
    #     unittest for function app_rate_testing:
    #     method extracts 1st and maximum from each list in a series of lists of app rates
    #     """
    #     expected_results = pd.Series([], dtype="object")
    #     result = pd.Series([], dtype="object")
    #     expected_results = [[0.34, 0.78, 2.34], [0.34, 3.54, 2.34]]
    #     try:
    #         therps_empty.app_rates = pd.Series([[0.34], [0.78, 3.54], [2.34, 1.384, 2.22]], dtype='object')
    #         # parse app_rates Series of lists
    #         therps_empty.app_rate_parsing()
    #         result = [therps_empty.first_app_rate, therps_empty.max_app_rate]
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    def test_conc_initial(self):
        """
        unittest for function conc_initial:
        conc_0 = (app_rate * self.frac_act_ing * food_multiplier)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = [12.7160, 9.8280, 11.2320]
        try:
                # specify an app_rates Series (that is a series of lists, each list representing
                # a set of application rates for 'a' model simulation)
            therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
                                              [2.34, 1.384, 3.4]], dtype='float')
            therps_empty.food_multiplier_init_sg = pd.Series([110., 15., 240.], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
            for i in range(len(therps_empty.frac_act_ing)):
                result[i] = therps_empty.conc_initial(i, therps_empty.app_rates[i][0], therps_empty.food_multiplier_init_sg[i])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_timestep(self):
        """
        unittest for function conc_timestep:
        """
        result = pd.Series([], dtype = 'float')
        expected_results = [6.25e-5, 0.039685, 7.8886e-30]
        try:
            therps_empty.foliar_diss_hlife = pd.Series([.25, 0.75, 0.01], dtype='float')
            conc_0 = pd.Series([0.001, 0.1, 10.0])
            for i in range(len(conc_0)):
                result[i] = therps_empty.conc_timestep(i, conc_0[i])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_percent_to_frac(self):
        """
        unittest for function percent_to_frac:
        """
        result = pd.Series([], dtype = 'float')
        expected_results = [.04556, .1034, .9389]
        try:
            therps_empty.percent_incorp = pd.Series([4.556, 10.34, 93.89], dtype='float')
            result = therps_empty.percent_to_frac(therps_empty.percent_incorp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # def test_inches_to_feet(self):
    #     """
    #     unittest for function inches_to_feet:
    #     """
    #     expected_results = [0.37966, 0.86166, 7.82416]
    #     try:
    #         therps_empty.bandwidth = pd.Series([4.556, 10.34, 93.89], dtype='float')
    #         result = therps_empty.inches_to_feet(therps_empty.bandwidth)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_at_bird(self):
    #     """
    #     unittest for function at_bird:
    #     adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
    #     """
    #     result = pd.Series([], dtype = 'float')
    #     expected_results = [69.17640, 146.8274, 56.00997]
    #     try:
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         # following variable is unique to at_bird and is thus sent via arg list
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #         for i in range(len(therps_empty.aw_bird_sm)):
    #             result[i] = therps_empty.at_bird(i, therps_empty.aw_bird_sm[i])
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    def test_at_bird(aw_herp):
        """
        unittest for function at_bird1; alternative approach using more vectorization:
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = [69.17640, 146.8274, 56.00997]
        try:
            therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([15., 20., 30.], dtype='float')

            result = therps_empty.at_bird(therps_empty.aw_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

#     def test_fi_bird(self):
#         """
#         unittest for function fi_bird:
#         food_intake = (0.648 * (aw_bird ** 0.651)) / (1 - mf_w_bird)
#         """
#         expected_results = [4.19728, 22.7780, 59.31724]
#         try:
# #?? 'mf_w_bird_1' is a constant (i.e., not an input whose value changes per model simulation run); thus it should
# #?? be specified here as a constant and not a pd.series -- if this is correct then go ahead and change next line
#             therps_empty.mf_w_bird_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
#             therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
#             result = therps_empty.fi_bird(therps_empty.aw_bird_sm, therps_empty.mf_w_bird_2)
#             npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_results]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#       return

    # def test_sc_bird(self):
    #     """
    #     unittest for function sc_bird:
    #     m_s_a_r = ((self.app_rate * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
    #     risk_quotient = m_s_a_r / self.noaec_bird
    #     """
    #
    #     expected_results = [6.637969, 77.805, 34.96289, np.nan]
    #     try:
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                             [2.34, 1.384, 3.4], [3.]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'first_app_rate' per model simulation run
    #         therps_empty.frac_act_ing = pd.Series([0.15, 0.20, 0.34, np.nan], dtype='float')
    #         therps_empty.density = pd.Series([8.33, 7.98, 6.75, np.nan], dtype='float')
    #         therps_empty.noaec_bird = pd.Series([5., 1.25, 12., np.nan], dtype='float')
    #         result = therps_empty.sc_bird()
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_sa_bird_1(self):
    #     """
    #     # unit test for function sa_bird_1
    #     """
    #     result_sm = pd.Series([], dtype = 'float')
    #     result_md = pd.Series([], dtype = 'float')
    #     result_lg = pd.Series([], dtype = 'float')
    #
    #     expected_results_sm = pd.Series([0.228229, 0.704098, 0.145205], dtype = 'float')
    #     expected_results_md = pd.Series([0.126646, 0.540822, 0.052285], dtype = 'float')
    #     expected_results_lg = pd.Series([0.037707, 0.269804, 0.01199], dtype = 'float')
    #
    #     try:
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='float')
    #         therps_empty.app_rate_parsing()  #get 'first_app_rate' per model simulation run
    #         therps_empty.density = pd.Series([8.33, 7.98, 6.75], dtype='float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #         therps_empty.aw_bird_md = pd.Series([115., 120., 130.], dtype='float')
    #         therps_empty.aw_bird_lg = pd.Series([1015., 1020., 1030.], dtype='float')
    #
    #         #reitierate constants here (they have been set in 'therps_inputs'; repeated here for clarity)
    #         therps_empty.mf_w_bird_1 = 0.1
    #         therps_empty.nagy_bird_coef_sm = 0.02
    #         therps_empty.nagy_bird_coef_md = 0.1
    #         therps_empty.nagy_bird_coef_lg = 1.0
    #
    #         result_sm = therps_empty.sa_bird_1("small")
    #         npt.assert_allclose(result_sm,expected_results_sm,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_md = therps_empty.sa_bird_1("medium")
    #         npt.assert_allclose(result_md,expected_results_md,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_lg = therps_empty.sa_bird_1("large")
    #         npt.assert_allclose(result_lg,expected_results_lg,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab_sm = [result_sm, expected_results_sm]
    #         tab_md = [result_md, expected_results_md]
    #         tab_lg = [result_lg, expected_results_lg]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab_sm, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_md, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_lg, headers='keys', tablefmt='rst'))
    #     return

    # def test_sa_bird_2(self):
    #     """
    #     # unit test for function sa_bird_2
    #     """
    #     result_sm = pd.Series([], dtype = 'float')
    #     result_md = pd.Series([], dtype = 'float')
    #     result_lg = pd.Series([], dtype = 'float')
    #
    #     expected_results_sm =pd.Series([0.018832, 0.029030, 0.010483], dtype = 'float')
    #     expected_results_md = pd.Series([2.774856e-3, 6.945353e-3, 1.453192e-3], dtype = 'float')
    #     expected_results_lg =pd.Series([2.001591e-4, 8.602729e-4, 8.66163e-5], dtype = 'float')
    #
    #     try:
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'first_app_rate' per model simulation run
    #         therps_empty.density = pd.Series([8.33, 7.98, 6.75], dtype='float')
    #         therps_empty.max_seed_rate = pd.Series([33.19, 20.0, 45.6])
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #         therps_empty.aw_bird_md = pd.Series([115., 120., 130.], dtype='float')
    #         therps_empty.aw_bird_lg = pd.Series([1015., 1020., 1030.], dtype='float')
    #
    #         #reitierate constants here (they have been set in 'therps_inputs'; repeated here for clarity)
    #         therps_empty.nagy_bird_coef_sm = 0.02
    #         therps_empty.nagy_bird_coef_md = 0.1
    #         therps_empty.nagy_bird_coef_lg = 1.0
    #
    #         result_sm = therps_empty.sa_bird_2("small")
    #         npt.assert_allclose(result_sm,expected_results_sm,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_md = therps_empty.sa_bird_2("medium")
    #         npt.assert_allclose(result_md,expected_results_md,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_lg = therps_empty.sa_bird_2("large")
    #         npt.assert_allclose(result_lg,expected_results_lg,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab_sm = [result_sm, expected_results_sm]
    #         tab_md = [result_md, expected_results_md]
    #         tab_lg = [result_lg, expected_results_lg]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab_sm, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_md, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_lg, headers='keys', tablefmt='rst'))
    #     return

    # def test_sa_mamm_1(self):
    #     """
    #     # unit test for function sa_mamm_1
    #     """
    #     result_sm = pd.Series([], dtype = 'float')
    #     result_md = pd.Series([], dtype = 'float')
    #     result_lg = pd.Series([], dtype = 'float')
    #
    #     expected_results_sm =pd.Series([0.022593, 0.555799, 0.010178], dtype = 'float')
    #     expected_results_md = pd.Series([0.019298, 0.460911, 0.00376], dtype = 'float')
    #     expected_results_lg =pd.Series([0.010471, 0.204631, 0.002715], dtype = 'float')
    #
    #     try:
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'first_app_rate' per model simulation run
    #         therps_empty.density = pd.Series([8.33, 7.98, 6.75], dtype='float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.tw_mamm = pd.Series([350., 225., 390.], dtype='float')
    #         therps_empty.ld50_mamm = pd.Series([321., 100., 400.], dtype='float')
    #
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #         therps_empty.aw_mamm_md = pd.Series([35., 45., 25.], dtype='float')
    #         therps_empty.aw_mamm_lg = pd.Series([1015., 1020., 1030.], dtype='float')
    #
    #         #reitierate constants here (they have been set in 'therps_inputs'; repeated here for clarity)
    #         therps_empty.mf_w_mamm_1 = 0.1
    #         therps_empty.nagy_mamm_coef_sm = 0.015
    #         therps_empty.nagy_mamm_coef_md = 0.035
    #         therps_empty.nagy_mamm_coef_lg = 1.0
    #
    #         result_sm = therps_empty.sa_mamm_1("small")
    #         npt.assert_allclose(result_sm,expected_results_sm,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_md = therps_empty.sa_mamm_1("medium")
    #         npt.assert_allclose(result_md,expected_results_md,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_lg = therps_empty.sa_mamm_1("large")
    #         npt.assert_allclose(result_lg,expected_results_lg,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab_sm = [result_sm, expected_results_sm]
    #         tab_md = [result_md, expected_results_md]
    #         tab_lg = [result_lg, expected_results_lg]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab_sm, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_md, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_lg, headers='keys', tablefmt='rst'))
    #     return

    # def test_sa_mamm_2(self):
    #     """
    #     # unit test for function sa_mamm_2
    #     """
    #     result_sm = pd.Series([], dtype = 'float')
    #     result_md = pd.Series([], dtype = 'float')
    #     result_lg = pd.Series([], dtype = 'float')
    #
    #     expected_results_sm =pd.Series([2.46206e-3, 3.103179e-2, 1.03076e-3], dtype = 'float')
    #     expected_results_md = pd.Series([1.304116e-3, 1.628829e-2, 4.220702e-4], dtype = 'float')
    #     expected_results_lg =pd.Series([1.0592147e-4, 1.24391489e-3, 3.74263186e-5], dtype = 'float')
    #
    #     try:
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'first_app_rate' per model simulation run
    #         therps_empty.density = pd.Series([8.33, 7.98, 6.75], dtype='float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.tw_mamm = pd.Series([350., 225., 390.], dtype='float')
    #         therps_empty.ld50_mamm = pd.Series([321., 100., 400.], dtype='float')
    #
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #         therps_empty.aw_mamm_md = pd.Series([35., 45., 25.], dtype='float')
    #         therps_empty.aw_mamm_lg = pd.Series([1015., 1020., 1030.], dtype='float')
    #
    #         #reitierate constants here (they have been set in 'therps_inputs'; repeated here for clarity)
    #         therps_empty.mf_w_mamm_1 = 0.1
    #         therps_empty.nagy_mamm_coef_sm = 0.015
    #         therps_empty.nagy_mamm_coef_md = 0.035
    #         therps_empty.nagy_mamm_coef_lg = 1.0
    #
    #         result_sm = therps_empty.sa_mamm_2("small")
    #         npt.assert_allclose(result_sm,expected_results_sm,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_md = therps_empty.sa_mamm_2("medium")
    #         npt.assert_allclose(result_md,expected_results_md,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_lg = therps_empty.sa_mamm_2("large")
    #         npt.assert_allclose(result_lg,expected_results_lg,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab_sm = [result_sm, expected_results_sm]
    #         tab_md = [result_md, expected_results_md]
    #         tab_lg = [result_lg, expected_results_lg]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab_sm, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_md, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_lg, headers='keys', tablefmt='rst'))
    #     return

    # def test_sc_mamm(self):
    #     """
    #     # unit test for function sc_mamm
    #     """
    #     result_sm = pd.Series([], dtype = 'float')
    #     result_md = pd.Series([], dtype = 'float')
    #     result_lg = pd.Series([], dtype = 'float')
    #
    #     expected_results_sm =pd.Series([2.90089, 15.87995, 8.142130], dtype = 'float')
    #     expected_results_md = pd.Series([2.477926, 13.16889, 3.008207], dtype = 'float')
    #     expected_results_lg =pd.Series([1.344461, 5.846592, 2.172211], dtype = 'float')
    #
    #     try:
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'first_app_rate' per model simulation run
    #         therps_empty.density = pd.Series([8.33, 7.98, 6.75], dtype='float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.tw_mamm = pd.Series([350., 225., 390.], dtype='float')
    #         therps_empty.noael_mamm = pd.Series([2.5, 3.5, 0.5], dtype='float')
    #
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #         therps_empty.aw_mamm_md = pd.Series([35., 45., 25.], dtype='float')
    #         therps_empty.aw_mamm_lg = pd.Series([1015., 1020., 1030.], dtype='float')
    #
    #         #reitierate constants here (they have been set in 'therps_inputs'; repeated here for clarity)
    #         therps_empty.mf_w_mamm_1 = 0.1
    #         therps_empty.nagy_mamm_coef_sm = 0.015
    #         therps_empty.nagy_mamm_coef_md = 0.035
    #         therps_empty.nagy_mamm_coef_lg = 1.0
    #
    #         result_sm = therps_empty.sc_mamm("small")
    #         npt.assert_allclose(result_sm,expected_results_sm,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_md = therps_empty.sc_mamm("medium")
    #         npt.assert_allclose(result_md,expected_results_md,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #
    #         result_lg = therps_empty.sc_mamm("large")
    #         npt.assert_allclose(result_lg,expected_results_lg,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab_sm = [result_sm, expected_results_sm]
    #         tab_md = [result_md, expected_results_md]
    #         tab_lg = [result_lg, expected_results_lg]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab_sm, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_md, headers='keys', tablefmt='rst'))
    #         print(tabulate(tab_lg, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_rg_bird(self):
    #     """
    #     # unit test for function ld50_rg_bird (LD50ft-2 for Row/Band/In-furrow granular birds)
    #     """
    #     result = pd.Series([], dtype = 'float')
    #     expected_results = [346.4856, 25.94132, np.nan]
    #     try:
    #         # following parameter values are unique for ld50_bg_bird
    #         therps_empty.application_type = pd.Series(['Row/Band/In-furrow-Granular',
    #                                                  'Row/Band/In-furrow-Granular',
    #                                                  'Row/Band/In-furrow-Liquid'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'max app rate' per model simulation run
    #         therps_empty.frac_incorp = pd.Series([0.25, 0.76, 0.05], dtype= 'float')
    #         therps_empty.bandwidth = pd.Series([2., 10., 30.], dtype = 'float')
    #         therps_empty.row_spacing = pd.Series([20., 32., 50.], dtype = 'float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_rg_bird(therps_empty.aw_bird_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             equal_nan=True, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_rg_bird1(self):
    #     """
    #     # unit test for function ld50_rg_bird1 (LD50ft-2 for Row/Band/In-furrow granular birds)
    #
    #     this is a duplicate of the 'test_ld50_rg_bird' method using a more vectorized approach to the
    #     calculations; if desired other routines could be modified similarly
    #     --comparing this method with 'test_ld50_rg_bird' it appears (for this test) that both run in the same time
    #     --but I don't think this would be the case when 100's of model simulation runs are executed (and only a small
    #     --number of the application_types apply to this method; thus I conclude we continue to use the non-vectorized
    #     --approach  -- should be revisited when we have a large run to execute
    #     """
    #     result = pd.Series([], dtype = 'float')
    #     expected_results = [346.4856, 25.94132, np.nan]
    #     try:
    #         # following parameter values are unique for ld50_bg_bird
    #         therps_empty.application_type = pd.Series(['Row/Band/In-furrow-Granular',
    #                                                  'Row/Band/In-furrow-Granular',
    #                                                  'Row/Band/In-furrow-Liquid'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.app_rate_parsing()  #get 'max app rate' per model simulation run
    #         therps_empty.frac_incorp = pd.Series([0.25, 0.76, 0.05], dtype= 'float')
    #         therps_empty.bandwidth = pd.Series([2., 10., 30.], dtype = 'float')
    #         therps_empty.row_spacing = pd.Series([20., 32., 50.], dtype = 'float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_rg_bird1(therps_empty.aw_bird_sm)
    #         npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, equal_nan=True, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_bl_bird(self):
    #     """
    #     # unit test for function ld50_bl_bird (LD50ft-2 for broadcast liquid birds)
    #     """
    #     expected_results = [46.19808, 33.77777, np.nan]
    #     try:
    #         # following parameter values are unique for ld50_bl_bird
    #         therps_empty.application_type = pd.Series(['Broadcast-Liquid', 'Broadcast-Liquid',
    #                                                  'Non-Broadcast'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_bl_bird(therps_empty.aw_bird_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             err_msg='', verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_bg_bird(self):
    #     """
    #     # unit test for function ld50_bg_bird (LD50ft-2 for broadcast granular)
    #     """
    #     expected_results = [46.19808, np.nan, 0.4214033]
    #     try:
    #         # following parameter values are unique for ld50_bg_bird
    #         therps_empty.application_type = pd.Series(['Broadcast-Granular', 'Broadcast-Liquid',
    #                                                  'Broadcast-Granular'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_bg_bird(therps_empty.aw_bird_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             err_msg='', verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_rl_bird(self):
    #     """
    #     # unit test for function ld50_rl_bird (LD50ft-2 for Row/Band/In-furrow liquid birds)
    #     """
    #     expected_results = [np.nan, 2.20701, 0.0363297]
    #     try:
    #         # following parameter values are unique for ld50_bg_bird
    #         therps_empty.application_type = pd.Series(['Broadcast-Granular', 'Row/Band/In-furrow-Liquid',
    #                                                  'Row/Band/In-furrow-Liquid'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.frac_incorp = pd.Series([0.25, 0.76, 0.05], dtype= 'float')
    #         therps_empty.bandwidth = pd.Series([2., 10., 30.], dtype = 'float')
    #
    #         # following parameter values are needed for internal call to "test_at_bird"
    #         # results from "test_at_bird"  test using these values are [69.17640, 146.8274, 56.00997]
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_rl_bird(therps_empty.aw_bird_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             err_msg='', verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_at_mamm(self):
    #     """
    #     unittest for function at_mamm:
    #     adjusted_toxicity = self.ld50_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
    #     """
    #     result = pd.Series([], dtype = 'float')
    #     expected_results = [705.5036, 529.5517, 830.6143]
    #     try:
    #         therps_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #         for i in range(len(therps_empty.ld50_mamm)):
    #             result[i] = therps_empty.at_mamm(i, therps_empty.aw_mamm_sm[i])
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_anoael_mamm(self):
    #     """
    #     unittest for function anoael_mamm:
    #     adjusted_toxicity = self.noael_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
    #     """
    #     expected_results = [5.49457, 9.62821, 2.403398]
    #     try:
    #         therps_empty.noael_mamm = pd.Series([2.5, 5.0, 1.25], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #         result = therps_empty.anoael_mamm(therps_empty.aw_mamm_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    def test_fi_mamm(self):
        """
        unittest for function fi_mamm:
        food_intake = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = [3.17807, 16.8206, 42.28516]
        try:
            therps_empty.mf_w_mamm_1 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
            result = therps_empty.fi_mamm(therps_empty.aw_mamm_sm, therps_empty.mf_w_mamm_1)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # def test_ld50_bl_mamm(self):
    #     """
    #     # unit test for function ld50_bl_mamm (LD50ft-2 for broadcast liquid)
    #     """
    #     expected_results = [4.52983, 9.36547, np.nan]
    #     try:
    #         # following parameter values are unique for ld50_bl_mamm
    #         therps_empty.application_type = pd.Series(['Broadcast-Liquid', 'Broadcast-Liquid',
    #                                                  'Non-Broadcast'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #
    #         # following parameter values are needed for internal call to "test_at_mamm"
    #         # results from "test_at_mamm"  test using these values are [705.5036, 529.5517, 830.6143]
    #         therps_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_bl_mamm(therps_empty.aw_mamm_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='',
    #                             verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_bg_mamm(self):
    #     """
    #     # unit test for function ld50_bg_mamm (LD50ft-2 for broadcast granular)
    #     """
    #     expected_results = [4.52983, 9.36547, np.nan]
    #     try:
    #         # following parameter values are unique for ld50_bl_mamm
    #         therps_empty.application_type = pd.Series(['Broadcast-Granular', 'Broadcast-Granular',
    #                                                  'Broadcast-Liquid'], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #
    #         # following parameter values are needed for internal call to "at_mamm"
    #         # results from "test_at_mamm"  test using these values are [705.5036, 529.5517, 830.6143]
    #         therps_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_bg_mamm(therps_empty.aw_mamm_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             err_msg='', verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_rl_mamm(self):
    #     """
    #     # unit test for function ld50_rl_mamm (LD50ft-2 for Row/Band/In-furrow liquid mammals)
    #     """
    #     expected_results = [np.nan, 0.6119317, 0.0024497]
    #     try:
    #         # following parameter values are unique for ld50_bl_mamm
    #         therps_empty.application_type = pd.Series(['Broadcast-Granular',
    #                                                  'Row/Band/In-furrow-Liquid',
    #                                                  'Row/Band/In-furrow-Liquid',], dtype='object')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.frac_incorp = pd.Series([0.25, 0.76, 0.05], dtype= 'float')
    #
    #         # following parameter values are needed for internal call to "at_mamm"
    #         # results from "test_at_mamm"  test using these values are [705.5036, 529.5517, 830.6143]
    #         therps_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #         therps_empty.bandwidth = pd.Series([2., 10., 30.], dtype = 'float')
    #
    #         result = therps_empty.ld50_rl_mamm(therps_empty.aw_mamm_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             err_msg='', verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_ld50_rg_mamm(self):
    #     """
    #     # unit test for function ld50_rg_mamm
    #     """
    #     expected_results = [33.9737, 7.192681, np.nan]
    #     try:
    #         # following parameter values are unique for ld50_bl_mamm
    #         therps_empty.application_type = pd.Series(['Row/Band/In-furrow-Granular',
    #                                                  'Row/Band/In-furrow-Granular',
    #                                                  'Row/Band/In-furrow-Liquid',], dtype='object')
    #         therps_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
    #                                       [2.34, 1.384, 3.4]], dtype='object')
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         therps_empty.frac_incorp = pd.Series([0.25, 0.76, 0.05], dtype= 'float')
    #         therps_empty.bandwidth = pd.Series([2., 10., 30.], dtype = 'float')
    #         therps_empty.row_spacing = pd.Series([20., 32., 50.], dtype = 'float')
    #
    #         # following parameter values are needed for internal call to "at_mamm"
    #         # results from "test_at_mamm"  test using these values are [705.5036, 529.5517, 830.6143]
    #         therps_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         result = therps_empty.ld50_rg_mamm(therps_empty.aw_mamm_sm)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0,
    #                             err_msg='', verbose=True, equal_nan=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    def test_eec_diet_max(self):
        """
        combined unit test for methods eec_diet_max & eec_diet_timeseries;

        * this test calls eec_diet_max, which in turn calls eec_diet_timeseries (which produces
          concentration timeseries), which in turn calls conc_initial and conc_timestep
        * eec_diet_max processes the timeseries and extracts the maximum values

        * this test tests both eec_diet_max & eec_diet_timeseries together (ok, so this violates the exact definition
        * of 'unittest', get over it)
        * the assertion check is that the maximum values from the timeseries match expectations
        * this assumes that for the maximums to be 'as expected' then the timeseries are as well
        * note: the 1st application day ('day_out') for the 2nd model simulation run is set to 0 here
        * to make sure the timeseries processing works when an application occurs on 1st day of year
        """

        expected_results = [1.734, 145.3409, 0.702]
        num_app_days = pd.Series([], dtype='int')
        try:
            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [0, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])

            result = therps_empty.eec_diet_max(therps_empty.food_multiplier_init_sg)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # def test_eec_dose_bird(self):
    #     """
    #     unit test for function eec_dose_bird;
    #     internal call to 'eec_diet_max' --> 'eed_diet_timeseries' --> conc_initial' and 'conc_timestep' are included;
    #     internal call  to 'fi_bird' included
    #
    #     unit tests of this routine include the following approach:
    #     * this test verifies that the logic & calculations performed within the 'eec_dose_bird' are correctly implemented
    #     * methods called inside of 'eec_dose_bird' are not retested/recalculated
    #     * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
    #     """
    #     expected_results = [7.763288, 2693.2339, 22.20837]
    #     num_app_days = pd.Series([], dtype='int')
    #     try:
    #         therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
    #         therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
    #         for i in range(len(therps_empty.app_rates)):
    #             therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
    #             num_app_days[i] = len(therps_empty.day_out[i])
    #             assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
    #         therps_empty.food_multiplier_init_sg = 240.
    #         therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
    #
    #         # variables for 'fi_bird'  (values reflect unittest for 'at_bird'
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         therps_empty.mf_w_bird_1 = pd.Series([0.1, 0.8, 0.9], dtype='float')
    #
    #         result = therps_empty.eec_dose_bird(therps_empty.aw_bird_sm, therps_empty.mf_w_bird_1,
    #                                           therps_empty.food_multiplier_init_sg)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_arq_dose_bird(self):
    #     """
    #     unit test for function arq_dose_bird;
    #     internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
    #
    #     unit tests of this routine include the following approach:
    #     * this test verifies that the logic & calculations performed within the 'arq_dose_bird' are correctly implemented
    #     * methods called inside of 'arq_dose_bird' are not retested/recalculated
    #     * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
    #     """
    #     expected_results = [0.007014, 1.146429, 0.02478172]
    #     num_app_days = pd.Series([], dtype='int')
    #     try:
    #         #specifying 3 different application scenarios of 1, 4, and 2 applications
    #         therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
    #         therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
    #         for i in range(len(therps_empty.app_rates)):
    #             therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
    #             num_app_days[i] = len(therps_empty.day_out[i])
    #             assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
    #         therps_empty.food_multiplier_init_sg = 15.
    #         therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
    #
    #         # variables for 'at_bird'  (values reflect unittest for 'fi_bird'
    #         therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
    #         therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
    #         therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
    #         therps_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         therps_empty.mf_w_bird_1 = pd.Series([0.1, 0.8, 0.9], dtype='float')
    #
    #         result = therps_empty.arq_dose_bird(therps_empty.aw_bird_sm, therps_empty.mf_w_bird_1,
    #                                           therps_empty.food_multiplier_init_sg)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_arq_diet_bird(self):
    #     """
    #     unit test for function arq_diet_bird;
    #     internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
    #
    #     unit tests of this routine include the following approach:
    #     * this test verifies that the logic & calculations performed within the 'arq_diet_bird' are correctly implemented
    #     * methods called inside of 'arq_diet_bird' are not retested/recalculated
    #     * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
    #     """
    #     expected_results = pd.Series([0.019563, 1.509543, 0.0046715], dtype='float')
    #     result = pd.Series([], dtype = 'float')
    #     num_app_days = pd.Series([], dtype='int')
    #     try:
    #          #specifying 3 different application scenarios of 1, 4, and 2 applications
    #         therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
    #         therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
    #         for i in range(len(therps_empty.app_rates)):
    #             therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
    #             num_app_days[i] = len(therps_empty.day_out[i])
    #             assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
    #         #therps_empty.food_multiplier_init_sg = pd.Series([110., 15., 240.], dtype='float')
    #         therps_empty.food_multiplier_init_sg = 110.
    #         therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype='float')
    #         therps_empty.lc50_bird = pd.Series([650., 718., 1102.], dtype='float')
    #         #for i in range (len(therps_empty.food_multiplier_init_sg)):
    #         #    result[i] = therps_empty.arq_diet_bird(therps_empty.food_multiplier_init_sg[i])
    #         result = therps_empty.arq_diet_bird(therps_empty.food_multiplier_init_sg)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    # def test_crq_diet_bird(self):
    #     """
    #     unit test for function crq_diet_bird;
    #     internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
    #
    #     unit tests of this routine include the following approach:
    #     * this test verifies that the logic & calculations performed within the 'crq_diet_bird' are correctly implemented
    #     * methods called inside of 'crq_diet_bird' are not retested/recalculated
    #     * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
    #     """
    #     expected_results = [2.5432, 60.214, 0.050471]
    #     num_app_days = pd.Series([], dtype='int')
    #     try:
    #          #specifying 3 different application scenarios of 1, 4, and 2 applications
    #         therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
    #         therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
    #         for i in range(len(therps_empty.app_rates)):
    #             therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
    #             num_app_days[i] = len(therps_empty.day_out[i])
    #             assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
    #         therps_empty.food_multiplier_init_sg = 110.
    #         therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
    #
    #         therps_empty.noaec_bird = pd.Series([5., 18., 102.])
    #
    #         result = therps_empty.crq_diet_bird(therps_empty.food_multiplier_init_sg)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    def test_eec_dose_mamm(self):
        """
        unit test for function eec_dose_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'eec_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
       """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.36738, 124.3028, 0.989473], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])

#the following values were just copied from below  --  they need to be
#changed to reflect actual variable values  --  calculations also need to be redone
            therps_empty.aw_herp_sm = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.bw_frog_prey_mamm = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            result = therps_empty.eec_dose_mamm(therps_empty.food_multiplier_init_sg, therps_empty.aw_herp_sm,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_dose_mamm(self):
        """
        unit test for function arq_dose_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'arq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_dose_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        """
        expected_results = [0.0083319, 3.755716, 0.01906]
        num_app_days = pd.Series([], dtype='int')
        try:
             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
            therps_empty.ld50_bird = pd.Series([2000., 5., 45.])
            therps_empty.tw_bird_ld50 = pd.Series([180., 5., 45.])
            therps_empty.mineau_sca_fact = pd.Series([1.15, 1., 1.5])

            therps_empty.food_multiplier_init_sg = 240.
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.bw_frog_prey_mamm = pd.Series([0.1, 0.8, 0.9], dtype='float')

            result = therps_empty.arq_dose_mamm(therps_empty.food_multiplier_init_sg, therps_empty.aw_herp_sm,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    # def test_crq_dose_mamm(self):
    #     """
    #     unit test for function crq_dose_mamm;
    #     internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
    #
    #     unit tests of this routine include the following approach:
    #     * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
    #     * methods called inside of 'crq_dose_mamm' are not retested/recalculated
    #     * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
    #     """
    #     expected_results = [0.49033, 94.67533, 3.019115]
    #     num_app_days = pd.Series([], dtype='int')
    #     try:
    #          #specifying 3 different application scenarios of 1, 4, and 2 applications
    #         therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
    #         therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
    #         for i in range(len(therps_empty.app_rates)):
    #             therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
    #             num_app_days[i] = len(therps_empty.day_out[i])
    #             assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
    #         therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
    #         therps_empty.food_multiplier_init_sg = 110.
    #         therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
    #
    #         therps_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
    #         therps_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
    #         therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
    #
    #         therps_empty.mf_w_mamm_1 = pd.Series([0.1, 0.8, 0.9], dtype='float')
    #
    #         result = therps_empty.crq_dose_mamm(therps_empty.aw_mamm_sm, therps_empty.mf_w_mamm_1,
    #                                           therps_empty.food_multiplier_init_sg)
    #         npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_results]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return

    def test_arq_diet_mamm(self):
        """
        unit test for function arq_diet_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'arq_diet_mamm' are correctly implemented
        * methods called inside of 'arq_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)

        """
        expected_results = [0.0266769, 20.81662, 0.0068823]
        num_app_days = pd.Series([], dtype='int')
        try:
             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
            therps_empty.lc50_bird = pd.Series([65., 7.1, 102.])
            therps_empty.bw_frog_prey_mamm = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

            result = therps_empty.arq_diet_mamm(therps_empty.food_multiplier_init_sg,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_crq_diet_mamm(self):
        """
        unit test for function crq_diet_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_diet_mamm' are correctly implemented
        * methods called inside of 'crq_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        """
        expected_results = [0.426831, 47.29536, 0.110118]
        num_app_days = pd.Series([], dtype='int')
        try:
             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02])
            therps_empty.food_multiplier_init_sg = 240.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.])
            therps_empty.noaec_bird = pd.Series([65., 50., 102.])
            therps_empty.bw_frog_prey_mamm = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            result = therps_empty.crq_diet_mamm(therps_empty.food_multiplier_init_sg,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2 )
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_ crq_diet_tp(self, food_multiplier, bw_frog_prey, awc_herp):
        """
        amphibian chronic dietary-based risk quotients for tp

        :return:
        """
        eec_diet_tp_temp = pd.Series([], dtype = 'float')
        amphibian_chronic_rq = pd.Series([], dtype = 'float')

        eec_diet_tp_temp = self.eec_diet_tp(food_multiplier, bw_frog_prey, awc_herp)
        amphibian_chronic_rq = eec_diet_tp_temp / self.noaec_bird
        return amphibian_chronic_rq

    def test_crq_diet_herp(self, food_multiplier):
        """
        amphibian chronic dietary-based risk quotients

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibain_chronic_rq = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        ##??assert isinstance(eec_diet, object)
        amphibain_chronic_rq = eec_diet_temp / self.noaec_bird
        return

    def test_arq_diet_tp(self, food_multiplier, bw_frog_prey, awc_herp):
        """
        # amphibian acute dietary-based risk quotients for tp

        :return:
        """
        eec_diet_tp_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_diet_tp_temp = self.eec_diet_tp(food_multiplier, bw_frog_prey, awc_herp)
        amphibian_acute_rq = eec_diet_tp_temp / self.lc50_bird
        return (eec_diet_tp_temp / self.lc50_bird)

    def test_arq_diet_herp(self, food_multiplier):
        """
        amphibian acute dietary-based risk quotients

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        amphibian_acute_rq = eec_diet_temp / self.lc50_bird
        return amphibian_acute_rq

    def test_arq_dose_tp(self, food_multiplier, aw_herp, bw_frog_prey, awc_herp_sm, awc_herp_md):
        """
        amphibian acute dose-based risk quotients for tp

        :return:
        """
        eec_dose_tp_temp = pd.Series([], 'float')
        at_bird_temp = pd.Series([], 'float')
        amphibian_acute_rq = pd.Series([], 'float')

        eec_dose_tp_temp = self.eec_dose_tp(food_multiplier, aw_herp, bw_frog_prey, awc_herp_sm, awc_herp_md)
        at_bird_temp = self.at_bird(aw_herp)
        amphibian_acute_rq = eec_dose_tp_temp / at_bird_temp
        return amphibian_acute_rq

    def test_arq_dose_herp(self, aw_herp, awc_herp, food_multiplier):
        """
        amphibian acute dose-based risk quotients

        :return:
        """
        at_bird_temp = pd.Series([], dtype = 'float')
        eec_dose_herp_temp = pd.Series([], dtype = 'float')
        amphibian_arq = pd.Series([], dtype = 'float')

        eec_dose_herp_temp = self.eec_dose_herp(aw_herp, awc_herp, food_multiplier)
        at_bird_temp = self.at_bird(aw_herp)
        amphibian_arq = (eec_dose_herp_temp / at_bird_temp)
        return amphibian_arq

    def test_eec_dose_tp(self, food_multiplier, aw_herp, bw_frog_prey, awc_herp_sm, awc_herp_md):
        """
        amphibian Dose based eecs for terrestrial

        :return:
        """

        eec_diet_tp_temp = pd.Series([], dtype = 'float')
        fi_herp_temp = pd.Series([], dtype = 'float')
        amphibian_dose_eec = pd.Series([], dtype = 'float')

        eec_diet_tp_temp = self.eec_diet_tp(food_multiplier, bw_frog_prey, awc_herp_sm)
        fi_herp_temp = self.fi_herp(aw_herp, awc_herp_md)
        amphibian_dose_eec = eec_diet_tp_temp * fi_herp_temp / aw_herp
        return amphibian_dose_eec

    def test_eec_dose_herp(self, aw_herp, awc_herp, food_multiplier):
        """
        amphibian Dose based eecs

        :return:
        """
        fi_herp_temp = pd.Series([], dtype = 'float')
        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibian_dose = pd.Series([], dtype = 'float')

        fi_herp_temp = self.fi_herp(aw_herp, awc_herp)
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        amphibian_dose = (eec_diet_temp * fi_herp_temp / aw_herp)
        return amphibian_dose

    def test_eec_diet_tp(self, food_multiplier, bw_frog_prey, awc_herp):
        """
        Dietary terrestrial phase based eecs

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        tp_dietary_eec = pd.Series([], dtype = 'float')
        fi_herp_temp = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        fi_herp_temp = self.fi_herp(bw_frog_prey, awc_herp)
        tp_dietary_eec = (eec_diet_temp * fi_herp_temp / (bw_frog_prey))
        return tp_dietary_eec

    def test_eec_diet_mamm(self, food_multiplier, bw_frog_prey, mf_w_mamm):
        """
        Dietary_mammal based eecs

        :return:
        """
        eec_diet_temp = pd.Series([], dtype = 'float')
        fi_mamm_temp = pd.Series([], dtype = 'float')
        mammal_dietary_eec = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        fi_mamm_temp = self.fi_mamm(bw_frog_prey, mf_w_mamm)
        mammal_dietary_eec = eec_diet_temp * fi_mamm_temp / bw_frog_prey
        return mammal_dietary_eec


# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass