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

    def test_conc_initial(self):
        """
        unittest for function conc_initial:
        conc_0 = (app_rate * self.frac_act_ing * food_multiplier)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([12.7160, 9.8280, 11.2320], dtype = 'float')
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
        expected_results = pd.Series([6.25e-5, 0.039685, 7.8886e-30], dtype = 'float')
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
        expected_results = pd.Series([.04556, .1034, .9389], dtype = 'float')
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

    def test_at_bird(aw_herp):
        """
        unittest for function at_bird1; alternative approach using more vectorization:
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([69.17640, 146.8274, 56.00997], dtype = 'float')
        try:
            therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')

            result = therps_empty.at_bird(therps_empty.aw_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_fi_mamm(self):
        """
        unittest for function fi_mamm:
        food_intake = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([3.17807, 16.8206, 42.28516], dtype = 'float')
        try:
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')

            result = therps_empty.fi_mamm(therps_empty.aw_mamm_sm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_fi_herp(self):
        """
        unittest for function fi_herp: Food intake for herps.
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([3.17807, 16.8206, 42.28516], dtype = 'float')

        try:
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([15., 20., 30.], dtype='float')

            result = therps_empty.fi_herp(therps_empty.aw_herp_sm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

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

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([1.734, 145.3409, 0.702], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [0, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'

            result = therps_empty.eec_diet_max(therps_empty.food_multiplier_init_sg)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

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
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

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

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.0083319, 3.755716, 0.01906], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            therps_empty.ld50_bird = pd.Series([2000., 5., 45.], dtype = 'float')
            therps_empty.tw_bird_ld50 = pd.Series([180., 5., 45.], dtype = 'float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 1., 1.5], dtype = 'float')

            therps_empty.food_multiplier_init_sg = 240.
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.arq_dose_mamm(therps_empty.food_multiplier_init_sg, therps_empty.aw_herp_sm,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_diet_mamm(self):
        """
        unit test for function arq_diet_mamm;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'arq_diet_mamm' are correctly implemented
        * methods called inside of 'arq_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)

        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.0266769, 20.81662, 0.0068823], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

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

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 240.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.crq_diet_mamm(therps_empty.food_multiplier_init_sg,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2 )
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_crq_diet_tp(self):
        """
        unit test for function crq_diet_tp;  amphibian chronic dietary-based risk quotients for tp
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'crq_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_init_blp = 135.
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.crq_diet_tp(therps_empty.food_multiplier_init_blp,
                                              therps_empty.bw_frog_prey_herp, therps_empty.awc_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_crq_diet_herp(self):
        """
        amphibian chronic dietary-based risk quotients


        unit test for function crq_diet_herp;  amphibian acute dietary-based risk quotients for tp
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'crq_diet_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_init_blp = 135.
            therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.crq_diet_herp(therps_empty.food_multiplier_init_blp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_diet_tp(self):
        """
        unit test for function arq_diet_tp;  amphibian acute dietary-based risk quotients for tp
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
                            'fi_herp'
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            therps_empty.food_multiplier_init_blp = 135.
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.arq_diet_tp(therps_empty.food_multiplier_init_blp,
                                              therps_empty.bw_frog_prey_herp, therps_empty.awc_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_diet_herp(self):
        """
        unit test for function arq_diet_herp;  amphibian acute dietary-based risk quotients
        internal calls to : 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_diet_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_fp = 15.
            therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.arq_diet_herp(therps_empty.food_multiplier_mean_fp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_dose_tp(self):
        """
        unit test for function arq_dose_tp; amphibian acute dose-based risk quotients for tp
        internal calls to : 'eec_dose_herp' --> 'fi_herp'  --> ;
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
                            'at_bird'
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_dose_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_init_blp = 135.
            therps_empty.aw_herp_lg = pd.Series([200., 250., 300.], dtype = 'float')
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.awc_herp_md = pd.Series([105., 125., 145.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.arq_dose_tp(therps_empty.food_multiplier_init_blp,
                                              therps_empty.aw_herp_lg, therps_empty.bw_frog_prey_herp,
                                              therps_empty.awc_herp_sm, therps_empty.awc_herp_md)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_arq_dose_herp(self):
        """
        unit test for function arq_dose_herp; amphibian acute dose-based risk quotients
        internal calls to : 'eec_dose_herp' --> 'fi_herp'  --> ;
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included
                            'at_bird'
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'arq_dose_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.food_multiplier_mean_blp = 45.
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.arq_dose_herp(therps_empty.aw_herp_sm, therps_empty.awc_herp_sm,
                                                therps_empty.food_multiplier_mean_blp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_dose_tp(self):
        """
        unit test for function eec_dose_tp; amphibian Dose based eecs for terrestrial
        internal calls to : "fi_herp";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_blp = 45.
            therps_empty.aw_herp_md = pd.Series([20., 40., 60.], dtype = 'float')
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.awc_herp_md = pd.Series([105., 125., 145.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.eec_dose_tp(therps_empty.food_multiplier_mean_blp,
                                              therps_empty.aw_herp_md, therps_empty.bw_frog_prey_herp,
                                              therps_empty.awc_herp_sm, therps_empty.awc_herp_md)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_dose_herp(self):
        """
        unit test for function eec_dose_herp; amphibian Dose based eecs
        internal calls to : "fi_herp";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.aw_herp_sm = pd.Series([1.5, 2.5, 3.0], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.food_multiplier_init_blp = 135.
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.eec_dose_herp(therps_empty.aw_herp_sm, therps_empty.awc_herp_sm,
                                                therps_empty.food_multiplier_init_blp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_tp(self):
        """

        unit test for function eec_diet_tp; Dietary terrestrial phase based eecs
        internal calls to : "fi_herp";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_sg = 240.
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 15., 25.], dtype = 'float')
            therps_empty.awc_herp_sm = pd.Series([70., 85., 105.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.eec_diet_tp(therps_empty.food_multiplier_mean_sg,
                                              therps_empty.bw_frog_prey_herp, therps_empty.awc_herp_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_mamm(self):
        """
        unit test for function eec_diet_mamm; Dietary_mammal based eecs
        internal calls to : "fi_mamm";
                            'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep' are included

        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'crq_dose_mamm' are correctly implemented
        * methods called inside of 'eec_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """
        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.426831, 47.29536, 0.110118], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_sg = 240.
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [5, 10, 20, 50], [150, 250]], dtype='object')
            therps_empty.num_apps = range(0, len(therps_empty.app_rates[:])) #set length of num_apps list (may have values from previous test)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.eec_diet_mamm(therps_empty.food_multiplier_mean_sg,
                                                therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
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