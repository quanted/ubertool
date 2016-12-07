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


#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from therps_exe import THerps

print("Python version: " + sys.version)
print("Numpy version: " + np.__version__)

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

        test = {}
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

    def create_therps_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty kabam object
        therps_empty = THerps(df_empty, df_empty)
        return therps_empty

    def test_convert_app_intervals(self):
        """
        unit test for function convert_app_intervals
        the method converts number of applications and application interval into application rates and day of year number
        this is so that the same concentration timeseries method from trex_functions can be reused here
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result_day_out = pd.Series([], dtype="object")
        result_app_rates = pd.Series([], dtype="object")

        expected_result_day_out = pd.Series([[1,8,15], [1], [1,22,43,64], [1,8,15]], dtype = 'object')
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([1.734, 9.828, 0.702], dtype = 'float')
        try:
                # specify an app_rates Series (that is a series of lists, each list representing
                # a set of application rates for 'a' model simulation)
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
            for i in range(len(therps_empty.frac_act_ing)):
                result[i] = therps_empty.conc_initial(i, therps_empty.app_rates[i][0], therps_empty.food_multiplier_init_sg)
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([9.726549e-4, 0.08705506, 9.8471475], dtype = 'float')
        try:
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

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

    def test_at_bird(self):
        """
        unittest for function at_bird1; alternative approach using more vectorization:
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([48.97314, 136.99477, 95.16341], dtype = 'float')
        try:
            therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test

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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([3.178078, 23.06301, 53.15002], dtype = 'float')
        try:
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')


            result = therps_empty.fi_mamm(therps_empty.bw_frog_prey_mamm, therps_empty.mf_w_mamm_2)
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.02932976, 0.3854015, 1.054537], dtype = 'float')

        try:
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 10., 15.], dtype='float')

            result = therps_empty.fi_herp(therps_empty.bw_frog_prey_herp, therps_empty.mf_w_mamm_2)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_timeseriesA(self):
        """
        combined unit test for methods eec_diet_timeseries;

        * this test calls eec_diet_timeseries, which in turn calls conc_initial and conc_timestep

        * this unittest executes the timeseries method for three sets of inputs (i.e., model simulations)
        * each timeseries is the target of an assertion test
        * the complete timeseries is not compared between actual and expected results
        * rather selected values from each series are extracted and placed into a list for comparison
        * the values extracted include the first and last entry in the timeseries (first and last day of simulated year)
        * additional values are extracted on each day of the year for which there is a pesticide application
        * the code here is not elegant (each simulation timeseries is checked within it own code segment; as opposed to
        * getting the indexing squared away so that a single piece of code would loop through all simulations
        * (perhaps at a later time this can be revisited and made more elegant)
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        conc_timeseries = pd.Series([], dtype = 'object')
        result1 = pd.Series([], dtype = 'float')
        result2 = pd.Series([], dtype = 'float')
        result3 = pd.Series([], dtype = 'float')
        expected_results1 = [0.0, 1.734, 6.791566e-5]
        expected_results2 = [9.828, 145.341, 80.93925, 20.6686758, 1.120451e-18]
        expected_results3 = [0.0, 0.702, 0.5656463, 0.087722]
        num_app_days = pd.Series([], dtype='int')

        try:
            #define needed inputs for method
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios (i.e., model simulations) of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            #therps_empty.num_apps = [0] * len(therps_empty.app_rates) #set length of num_apps list (no longer needed)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'

            #run method and get timeseries (all simulations will be executed here)
            conc_timeseries = therps_empty.eec_diet_timeseries(therps_empty.food_multiplier_init_sg)

            #let's extract from each timeseries values on the first day, each day of an application, and the last day
            #these will be placed into the 'result#' and used for the allclose assertion
            #need to execute this extraction for each simulation timeseries because 'allclose' will not handle uneven series lists

            #first simulation result
            num_values_to_check = len(therps_empty.app_rates[0]) + 2 #number of applications plus first and last timeseries elements
            if (therps_empty.day_out[0][0] == 1):  #if first app day is first day of year
                num_values_to_check = num_values_to_check - 1
            result1 = [0.] * num_values_to_check
            result1[0] = float(conc_timeseries[0][0])  #first day of timeseries
            result1[-1] = float(conc_timeseries[0][370])  #last day of timeseries
            num_values_to_check = len(therps_empty.app_rates[0])
            if ((num_values_to_check) >= 1):
                result_index = 1
                for i in range(0 ,num_values_to_check):
                    if(therps_empty.day_out[0][i] != 1):
                        series_index = therps_empty.day_out[0][i] - 1
                        result1[result_index] = float(conc_timeseries[0][series_index])
                        result_index = result_index + 1
            npt.assert_allclose(result1,expected_results1,rtol=1e-4, atol=0, err_msg='', verbose=True)

            #second simulation result
            num_values_to_check = len(therps_empty.app_rates[1]) + 2
            if (therps_empty.day_out[1][0] == 1):  #if first app day is first day of year
                num_values_to_check = num_values_to_check - 1
            result2 = [0.] * num_values_to_check
            result2[0] = float(conc_timeseries[1][0])  #first day of timeseries
            result2[-1] = float(conc_timeseries[1][370])  #last day of timeseries
            num_values_to_check = len(therps_empty.app_rates[1])
            if ((num_values_to_check) >= 1):
                result_index = 1
                for i in range(0 ,num_values_to_check):
                    if(therps_empty.day_out[1][i] != 1):
                        series_index = therps_empty.day_out[1][i] - 1
                        result2[result_index] = float(conc_timeseries[1][series_index])
                        result_index = result_index + 1
            npt.assert_allclose(result2,expected_results2,rtol=1e-4, atol=0, err_msg='', verbose=True)

            #3rd simulation result
            num_values_to_check = len(therps_empty.app_rates[2]) + 2
            if (therps_empty.day_out[2][0] == 1):  #if first app day is first day of year
                num_values_to_check = num_values_to_check - 1
            result3 = [0.] * num_values_to_check
            result3[0] = float(conc_timeseries[2][0])  #first day of timeseries
            result3[-1] = float(conc_timeseries[2][370])  #last day of timeseries
            num_values_to_check = len(therps_empty.app_rates[2])
            if ((num_values_to_check) >= 1):
                result_index = 1
                for i in range(0 ,num_values_to_check):
                    if(therps_empty.day_out[2][i] != 1):
                        series_index = therps_empty.day_out[2][i] - 1
                        result3[result_index] = float(conc_timeseries[2][series_index])
                        result_index = result_index + 1
            npt.assert_allclose(result3,expected_results3,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab1 = [result1, expected_results1]
            tab2 = [result2, expected_results2]
            tab3 = [result3, expected_results3]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
            print(tabulate(tab3, headers='keys', tablefmt='rst'))
        return

    def test_eec_diet_timeseries(self):
        """
        combined unit test for  methods eec_diet_timeseries;

        * this test calls eec_diet_timeseries, which in turn calls conc_initial and conc_timestep

        * this unittest executes the timeseries method for three sets of inputs (i.e., model simulations)
        * each timeseries (i.e., simulation result) is the target of an assertion test
        * the complete timeseries is not compared between actual and expected results
        * rather selected values from each series are extracted and placed into a list for comparison
        * the values extracted include the first and last entry in the timeseries (first and last day of simulated year)
        * additional values are extracted on each day of the year for which there is a pesticide application
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        conc_timeseries = pd.Series([], dtype = 'object')
        result = pd.Series([], dtype = 'object')
        expected_results = pd.Series([[0.0, 1.734, 6.791566e-5], [9.828, 145.341, 80.93925, 20.6686758, 1.120451e-18],
                                      [0.0, 0.702, 0.5656463, 0.087722]], dtype = 'object')
        num_app_days = pd.Series([], dtype='int')

        try:
            #define needed inputs for method
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios (i.e., model simulations) of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            #therps_empty.num_apps = [0] * len(therps_empty.app_rates) #set length of num_apps list (no longer needed)
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'series of app-rates and app_days do not match'

            #run method and get timeseries (all simulations will be executed here)
            conc_timeseries = therps_empty.eec_diet_timeseries(therps_empty.food_multiplier_init_sg)

            #let's extract from each timeseries values on the first day, each day of an application, and the last day
            #these will be placed into 'result' and used for the allclose assertion

            #loop through simulation results extracting values of interest per timeseries
            for isim in range(len(therps_empty.app_rates)):
                num_values_to_check = len(therps_empty.app_rates[isim]) + 2 #number of applications plus first and last timeseries elements
                if (therps_empty.day_out[isim][0] == 1):  #if first app day is first day of year
                    num_values_to_check = num_values_to_check - 1
                result[isim] = [0.] * num_values_to_check  #initialize result list for this simulation
                result[isim][0] = float(conc_timeseries[isim][0])  #first day of timeseries
                result[isim][-1] = float(conc_timeseries[isim][370])  #last day of timeseries
                num_values_to_check = len(therps_empty.app_rates[isim]) #just the application days for this loop
                if ((num_values_to_check) >= 1):
                    result_index = 1
                    for i in range(0 ,num_values_to_check):
                        if(therps_empty.day_out[isim][i] != 1):  #application day of 1 has been processed above
                            series_index = therps_empty.day_out[isim][i] - 1
                            result[isim][result_index] = float(conc_timeseries[isim][series_index])
                            result_index = result_index + 1
                npt.assert_allclose(result[isim][:],expected_results[isim][:],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            for isim in range(len(therps_empty.app_rates)):
                tab1 = [result[isim], expected_results[isim]]
                print(tabulate(tab1, headers='keys', tablefmt='rst'))
        return


    def test_eec_diet_max(self):
        """
        unit test for method eec_diet_max;
        internal calls to 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep'

        * this test calls eec_diet_max, which in turn calls eec_diet_timeseries (which produces
          concentration timeseries), which in turn calls conc_initial and conc_timestep
        * eec_diet_max processes the timeseries and extracts the maximum values

        * the assertion check is that the maximum values from each timeseries is correctly identified
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([1.734, 145.3409, 0.702], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            #therps_empty.num_apps = [0] * len(therps_empty.app_rates) #set length of num_apps list (no longer needed)
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
        internal calls to 'eec_diet_mamm' --> 'eec_diet_max'  --> 'eec_diet_timeseries' --> 'conc_initial' and 'conc_timestep'
                                          --> fi_mamm
        unit tests of this routine include the following approach:
        * this test verifies that the logic & calculations performed within the 'eec_dose_mamm' are correctly implemented
        * methods called inside of 'eec_dose_mamm' are not retested/recalculated
        * for methods inside of 'eec_dose_mamm' the same values were used here that were used in the unit tests for that method
        * thus, only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        * only calculations done for this test are for those unique to this method
       """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([3.673858, 83.80002, 0.1492452], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            #therps_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')

            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.07501781, 0.6117023, 0.0015683], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')

            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.00293908, 0.03830858, 0.00165828], dtype = 'float')
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
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.01469543, 0.9577145, 0.01507527], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')
        try:
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.food_multiplier_init_sg = 15.
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')
            therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')

             #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'crq_diet_tp' are correctly implemented
        * methods called inside of 'crq_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([8.1372e-4, 0.05601463, 8.973091e-4], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_init_blp = 15.
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 10., 15.], dtype='float')
            therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'crq_diet_herp' are correctly implemented
        * methods called inside of 'crq_diet_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.06936, 1.4534, 0.01276364], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_init_blp = 15.
            therps_empty.noaec_bird = pd.Series([25., 100., 55.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'arq_diet_tp' are correctly implemented
        * methods called inside of 'arq_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([1.62745e-4, 0.002240583, 9.870466e-5], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            therps_empty.food_multiplier_init_blp = 15.
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 10., 15.], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'arq_diet_herp' are correctly implemented
        * methods called inside of 'arq_diet_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.013872, 0.0581364, 0.001404], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_fp = 15.
            therps_empty.lc50_bird = pd.Series([125., 2500., 500.], dtype = 'float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'arq_dose_tp' are correctly implemented
        * methods called inside of 'arq_dose_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([1.641716e-5, 0.001533847, 1.92511e-5], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')

            therps_empty.food_multiplier_init_blp = 15.
            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 10., 15.], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content
            therps_empty.awc_herp_md = pd.Series([70., 85., 90.], dtype = 'float')
            therps_empty.awc_herp_md = therps_empty.percent_to_frac(therps_empty.awc_herp_md)

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.arq_dose_tp(therps_empty.food_multiplier_init_blp,
                                              therps_empty.aw_herp_sm, therps_empty.bw_frog_prey_herp,
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
        * this test verifies that the logic & calculations performed within the 'arq_dose_herp' are correctly implemented
        * methods called inside of 'arq_dose_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([4.664597e-4, 0.02984901, 2.738237e-4], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            therps_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            therps_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')

            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test
            therps_empty.food_multiplier_mean_blp = 15.
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'eec_dose_tp' are correctly implemented
        * methods called inside of 'eec_dose_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([8.040096e-4, 0.2101289, 0.001831959], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_blp = 15.
            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 10., 15.], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content
            therps_empty.awc_herp_md = pd.Series([70., 85., 90.], dtype = 'float')
            therps_empty.awc_herp_md = therps_empty.percent_to_frac(therps_empty.awc_herp_md)

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
            for i in range(len(therps_empty.app_rates)):
                therps_empty.num_apps[i] = len(therps_empty.app_rates[i])
                num_app_days[i] = len(therps_empty.day_out[i])
                assert (therps_empty.num_apps[i] == num_app_days[i]), 'list of app-rates and app_days do not match'

            result = therps_empty.eec_dose_tp(therps_empty.food_multiplier_mean_blp,
                                              therps_empty.aw_herp_sm, therps_empty.bw_frog_prey_herp,
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
        * this test verifies that the logic & calculations performed within the 'ceec_dose_herp' are correctly implemented
        * methods called inside of 'eec_dose_herp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.02284427, 4.089158, 0.02605842], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.aw_herp_sm = pd.Series([1.5, 40., 250.], dtype = 'float') # use values for small, medium, large in this test
            therps_empty.food_multiplier_init_blp = 15.
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'eec_diet_tp' are correctly implemented
        * methods called inside of 'eec_diet_tp' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.02034312, 5.601457, 0.04935233], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_sg = 15.
            therps_empty.bw_frog_prey_herp = pd.Series([2.5, 10., 15.], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            therps_empty.awc_herp_sm = pd.Series([10., 80., 90.], dtype = 'float') # initialize as percent to match model input
            therps_empty.awc_herp_sm = therps_empty.percent_to_frac(therps_empty.awc_herp_sm) # convert to mass fraction water content

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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
        * this test verifies that the logic & calculations performed within the 'eec_diet_mamm' are correctly implemented
        * methods called inside of 'eec_diet_mamm' are not retested/recalculated
        * only the correct passing of variables/values is verified (calculations having been verified in previous unittests)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        therps_empty = self.create_therps_object()

        result = pd.Series([], dtype = 'float')
        expected_results = pd.Series([0.3673858, 95.771454, 0.829140], dtype = 'float')
        num_app_days = pd.Series([], dtype='int')

        try:
            therps_empty.food_multiplier_mean_sg = 15.
            therps_empty.bw_frog_prey_mamm = pd.Series([15., 35., 45.], dtype='float')
            therps_empty.mf_w_mamm_2 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            therps_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype = 'float')
            therps_empty.foliar_diss_hlife = pd.Series([25., 5., 45.], dtype = 'float')

            #specifying 3 different application scenarios of 1, 4, and 2 applications
            therps_empty.app_rates = pd.Series([[0.34], [0.78, 11.34, 3.54, 1.54], [2.34, 1.384]], dtype='object')
            therps_empty.day_out = pd.Series([[5], [1, 11, 21, 51], [150, 250]], dtype='object')
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