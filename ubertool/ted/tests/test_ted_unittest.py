from __future__ import division  # brings in Python 3.0 mixed type calculation rules
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

from ..ted_exe import Ted

test = {}

class TestTed(unittest.TestCase):
    """
    Unit tests for TED model.
    """
    print("ted unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for ted unit tests.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for ted unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def create_ted_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty ted object
        ted_empty = Ted(df_empty, df_empty)
        return ted_empty

    def test_daily_app_flag(self):
        """
        :description generates a daily flag to denote whether a pesticide is applied that day or not (1 - applied, 0 - anot applied)
        :param num_apps; number of applications
        :param app_interval; number of days between applications

        :NOTE in TED model there are two application scenarios per simulation (one for a min/max exposure scenario)
              (this is why the parameters are passed in)
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='bool')
        result = pd.Series([[]], dtype='bool')
        expected_results = [[True, False, False, True, False, False, True, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                             [True, False, False, False, False, False, False, True, False, False,
                              False, False, False, False, True, False, False, False, False, False,
                              False, True, False, False, False, False, False, False, True, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False],
                              [True, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366

            # input varialbles that change per simulation
            ted_empty.num_apps_min = pd.Series([3, 5, 1])
            ted_empty.app_interval_min = pd.Series([3, 7, 1])

            for i in range (3):
                result[i] = ted_empty.daily_app_flag(ted_empty.num_apps_min[i], ted_empty.app_interval_min[i])
                np.array_equal(result[i],expected_results[i])
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_set_drift_parameters(self):
        """
        :description provides parmaeter values to use when calculating distances from edge of application source area to
                     concentration of interest
        :param app_method; application method (aerial/ground/airblast)
        :param boom_hgt; height of boom (low/high) - 'NA' if not ground application
        :param drop_size; droplet spectrum for application (see list below for aerial/ground - 'NA' if airblast)
        :param param_a (result[i][0]; parameter a for spray drift distance calculation
        :param param_b (result[i][1]; parameter b for spray drift distance calculation
        :param param_c (result[i][2]; parameter c for spray drift distance calculation

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series(9*[[0.,0.,0.]], dtype='float')
        expected_results = [[0.0292,0.822,0.6539],[0.043,1.03,0.5],[0.0721,1.0977,0.4999],[0.1014,1.1344,0.4999],
                            [1.0063,0.9998,1.0193],[5.5513,0.8523,1.0079],[0.1913,1.2366,1.0552],
                            [2.4154,0.9077,1.0128],[0.0351,2.4586,0.4763]]

        try:

            # input variable that change per simulation
            ted_empty.app_method_min = pd.Series(['aerial','aerial','aerial','aerial','ground','ground','ground','ground','airblast'])
            ted_empty.boom_hgt_min = pd.Series(['','','','','low','low','high','high',''])
            ted_empty.droplet_spec_min = pd.Series(['very_fine_to_fine','fine_to_medium','medium_to_coarse','coarse_to_very_coarse',
                                                    'very_fine_to_fine','fine_to_medium-coarse','very_fine_to_fine','fine_to_medium-coarse',''])


            for i in range (9):  # test that the nine combinations are accessed
                result[i][0], result[i][1], result[i][2] = ted_empty.set_drift_parameters(ted_empty.app_method_min[i], ted_empty.boom_hgt_min[i], ted_empty.droplet_spec_min[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range (9):
                tab = [result, expected_results]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return


    def test_drift_distance_calc(self):
        """
        :description provides parmaeter values to use when calculating distances from edge of application source area to
                     concentration of interest
        :param app_rate_frac; fraction of active ingredient application rate equivalent to the health threshold of concern
        :param param_a; parameter a for spray drift distance calculation
        :param param_b; parameter b for spray drift distance calculation
        :param param_c; parameter c for spray drift distance calculation

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [302.050738, 11.484378, 0.0]

        try:

            # internal model constants
            ted_empty.max_distance_from_source = 1000.

            # input variable that is internally specified from among options
            param_a = pd.Series([0.0292, 0.1913, 0.0351], dtype='float')
            param_b = pd.Series([0.822, 1.2366, 2.4586], dtype='float')
            param_c = pd.Series([0.6539, 1.0522, 0.4763], dtype='float')

            # internally calculated variables
            app_rate_frac = pd.Series([0.1,0.25,0.88], dtype='float')

            for i in range(3):
                result[i] = ted_empty.drift_distance_calc(app_rate_frac[i], param_a[i], param_b[i], param_c[i], ted_empty.max_distance_from_source)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_timestep(self):
        """
        :description unittest for function conc_timestep:

        :param conc_ini; initial concentration for day (actually previous day concentration)
        :param half_life; halflife of pesiticde representing either foliar dissipation halflife or aerobic soil metabolism halflife (days)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [9.803896e-4, 0.106066, 1.220703e-3]

        try:

            # input variable that is internally specified from among options
            half_life = pd.Series([35., 2., .1])

            # internally calculated variables
            conc_ini = pd.Series([1.e-3, 0.15, 1.25])

            result = ted_empty.conc_timestep(conc_ini, half_life)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_initial_canopy_air(self):
        """
        :description calculates initial (1st application day) air concentration of pesticide within plant canopy (ug/mL)
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param mass_pest; mass of pesticide on treated field (mg)
        :param volume_air; volume of air in 1 hectare to a height equal to the height of the crop canopy
        :param biotransfer_factor; the volume_based biotransfer factor; function of Henry's las constant and Log Kow

        NOTE: this represents Eq 24 (and supporting eqs 25,26,27) of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [1.152526e-7, 1.281910e-5, 7.925148e-8]

        try:
            # internal model constants
            ted_empty.hectare_to_acre = 2.47105
            ted_empty.gms_to_mg = 1000.
            ted_empty.lbs_to_gms = 453.592
            ted_empty.crop_hgt = 1. #m
            ted_empty.hectare_area = 10000.  #m2
            ted_empty.m3_to_liters = 1000.
            ted_empty.mass_plant = 25000. # kg/hectare
            ted_empty.density_plant = 0.77 #kg/L

            # input variables that change per simulation
            ted_empty.log_kow = pd.Series([2., 4., 6.], dtype='float')
            ted_empty.log_unitless_hlc = pd.Series([-5., -3., -4.], dtype='float')
            ted_empty.app_rate_min = pd.Series([1.e-3, 0.15, 1.25]) # lbs a.i./acre

            for i in range(3):  #let's do 3 iterations
                result[i] = ted_empty.conc_initial_canopy_air(i, ted_empty.app_rate_min[i])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_initial_soil_h2o(self):
        """
        :description calculates initial (1st application day) concentration in soil pore water or surface puddles(ug/L)
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param soil_depth
        :param soil_bulk_density; kg/L
        :param porosity; soil porosity
        :param frac_org_cont_soil; fraction organic carbon in soil
        :param app_rate_conv;  conversion factor used to convert units of application rate (lbs a.i./acre) to (ug a.i./mL)

        :NOTE this represents Eq 3 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
              (the depth of water in this equation is assumed to be 0.0 and therefore not included here)

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [5.067739e-3, 1.828522, 6.13194634]

        try:
            # internal model constants
            ted_empty.app_rate_conv = 11.2
            ted_empty.soil_depth = 2.6 # cm
            ted_empty.soil_porosity = 0.35
            ted_empty.soil_bulk_density = 1.5 # kg/L
            ted_empty.soil_foc = 0.015
            ted_empty.h2o_depth_soil = 0.0
            ted_empty.h2o_depth_puddles = 1.3

            # internally specified variable
            ted_empty.water_type = pd.Series(["puddles", "pore_water", "puddles"])

            # input variables that change per simulation
            ted_empty.koc = pd.Series([1.e-3, 0.15, 1.25])
            ted_empty.app_rate_min = pd.Series([1.e-3, 0.15, 1.25]) # lbs a.i./acre

            for i in range(3):  #let's do 3 iterations
                result[i] = ted_empty.conc_initial_soil_h2o(i, ted_empty.app_rate_min[i], ted_empty.water_type[i])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_initial_plant(self):
        """
        :description calculates initial (1st application day) dietary based EEC (residue concentration) from pesticide application
                    (mg/kg-diet for food items including short/tall grass, broadleaf plants, seeds/fruit/pods, and above ground arthropods)
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs

        :return:

        """
        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [1.5e-2, 22.5, 300.]

        try:
            # input variables that change per simulation
            ted_empty.food_multiplier = pd.Series([15., 150., 240.])
            ted_empty.app_rate_min = pd.Series([1.e-3, 0.15, 1.25]) # lbs a.i./acre

            result = ted_empty.conc_initial_plant(ted_empty.app_rate_min, ted_empty.food_multiplier)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_animal_dietary_intake(self):
        """
        :description generates pesticide intake via consumption of diet containing pesticide for animals (mammals, birds, amphibians, reptiles)
        :param a1; coefficient of allometric expression
        :param b1; exponent of allometric expression
        :param body_wgt; body weight of species (g)
        :param frac_h2o; fraction of water in food item

               # this represents Eqs 6 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [8.050355, 3.507997, 64.92055]

        try:
            # internally specified parameters
            a1 = pd.Series([.398, .013, .621], dtype='float')
            b1 = pd.Series([.850, .773, .564], dtype='float')

            # variables from external database
            body_wgt = pd.Series([10., 120., 450.], dtype='float')
            frac_h2o = pd.Series([0.65, 0.85, 0.7], dtype='float')

            result = ted_empty.animal_dietary_intake(a1, b1, body_wgt, frac_h2o)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_animal_dietary_dose(self):
        """
        :description generates pesticide dietary-based dose for animals (mammals, birds, amphibians, reptiles)
        :param body_wgt; body weight of species (g)
        :param frac_h2o; fraction of water in food item
        :param food_intake_rate; ingestion rate of food item (g/day-ww)
        :param food_pest_conc; pesticide concentration in food item (mg a.i./kg)

               # this represents Eqs 5 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [3.e-4, 3.45e-2, 4.5]

        try:
            # variables from external database
            body_wgt = pd.Series([10., 120., 450.], dtype='float')

            # internally calculated variables
            food_intake_rate = pd.Series([3., 12., 45.], dtype='float')
            food_pest_conc = pd.Series([1.e-3, 3.45e-1, 4.50e+1], dtype='float')

            result = ted_empty.animal_dietary_dose(body_wgt, food_intake_rate, food_pest_conc)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_plant_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide residue concentration (EECs) for a food item
        :param i; simulation number/index
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs
        :param daily_flag; daily flag denoting if pesticide is applied (0 - not applied, 1 - applied)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               #expected results generated by running OPP spreadsheet with appropriate inputs
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [[2.700000E+00,2.578072E+00,2.461651E+00,5.050487E+00,4.822415E+00,4.604642E+00,7.096704E+00,
                            6.776228E+00,6.470225E+00,6.178040E+00,5.899049E+00,5.632658E+00,5.378296E+00,5.135421E+00,
                            4.903513E+00,4.682078E+00,4.470643E+00,4.268756E+00,4.075986E+00,3.891921E+00,3.716168E+00,
                            3.548352E+00,3.388114E+00,3.235112E+00,3.089020E+00,2.949525E+00,2.816329E+00,2.689148E+00,
                            2.567710E+00,2.451757E+00,2.341039E+00,2.235322E+00,2.134378E+00,2.037993E+00,1.945961E+00,
                            1.858084E+00,1.774176E+00,1.694057E+00,1.617556E+00,1.544510E+00,1.474762E+00,1.408164E+00,
                            1.344574E+00,1.283855E+00,1.225878E+00,1.170520E+00,1.117661E+00,1.067189E+00,1.018997E+00,
                            9.729803E-01,9.290420E-01,8.870880E-01,8.470285E-01,8.087781E-01,7.722549E-01,7.373812E-01,
                            7.040822E-01,6.722870E-01,6.419276E-01,6.129392E-01,5.852598E-01,5.588304E-01,5.335945E-01,
                            5.094983E-01,4.864901E-01,4.645210E-01,4.435440E-01,4.235143E-01,4.043890E-01,3.861275E-01,
                            3.686906E-01,3.520411E-01,3.361435E-01,3.209638E-01,3.064696E-01,2.926299E-01,2.794152E-01,
                            2.667973E-01,2.547491E-01,2.432451E-01,2.322605E-01,2.217720E-01,2.117571E-01,2.021945E-01,
                            1.930637E-01,1.843453E-01,1.760206E-01,1.680717E-01,1.604819E-01,1.532348E-01,1.463150E-01,
                            1.397076E-01,1.333986E-01,1.273746E-01,1.216225E-01,1.161303E-01,1.108860E-01,1.058786E-01,
                            1.010973E-01,9.653187E-02,9.217264E-02,8.801028E-02,8.403587E-02,8.024095E-02,7.661739E-02,
                            7.315748E-02,6.985380E-02,6.669932E-02,6.368728E-02,6.081127E-02,5.806513E-02,5.544300E-02,
                            5.293928E-02,5.054863E-02,4.826593E-02,4.608632E-02,4.400514E-02,4.201794E-02,4.012047E-02,
                            3.830870E-02,3.657874E-02,3.492690E-02,3.334966E-02,3.184364E-02,3.040563E-02,2.903256E-02,
                            2.772150E-02,2.646964E-02,2.527431E-02,2.413297E-02,2.304316E-02,2.200257E-02,2.100897E-02,
                            2.006024E-02,1.915435E-02,1.828937E-02,1.746345E-02,1.667483E-02,1.592182E-02,1.520282E-02,
                            1.451628E-02,1.386075E-02,1.323482E-02,1.263716E-02,1.206648E-02,1.152158E-02,1.100128E-02,
                            1.050448E-02,1.003012E-02,9.577174E-03,9.144684E-03,8.731725E-03,8.337415E-03,7.960910E-03,
                            7.601408E-03,7.258141E-03,6.930375E-03,6.617410E-03,6.318579E-03,6.033242E-03,5.760790E-03,
                            5.500642E-03,5.252242E-03,5.015059E-03,4.788587E-03,4.572342E-03,4.365863E-03,4.168707E-03,
                            3.980455E-03,3.800704E-03,3.629070E-03,3.465187E-03,3.308705E-03,3.159289E-03,3.016621E-03,
                            2.880395E-03,2.750321E-03,2.626121E-03,2.507530E-03,2.394294E-03,2.286171E-03,2.182931E-03,
                            2.084354E-03,1.990228E-03,1.900352E-03,1.814535E-03,1.732594E-03,1.654353E-03,1.579645E-03,
                            1.508310E-03,1.440198E-03,1.375161E-03,1.313061E-03,1.253765E-03,1.197147E-03,1.143086E-03,
                            1.091466E-03,1.042177E-03,9.951138E-04,9.501760E-04,9.072676E-04,8.662969E-04,8.271763E-04,
                            7.898223E-04,7.541552E-04,7.200988E-04,6.875803E-04,6.565303E-04,6.268824E-04,5.985734E-04,
                            5.715428E-04,5.457328E-04,5.210884E-04,4.975569E-04,4.750880E-04,4.536338E-04,4.331484E-04,
                            4.135881E-04,3.949112E-04,3.770776E-04,3.600494E-04,3.437901E-04,3.282651E-04,3.134412E-04,
                            2.992867E-04,2.857714E-04,2.728664E-04,2.605442E-04,2.487784E-04,2.375440E-04,2.268169E-04,
                            2.165742E-04,2.067941E-04,1.974556E-04,1.885388E-04,1.800247E-04,1.718951E-04,1.641326E-04,
                            1.567206E-04,1.496433E-04,1.428857E-04,1.364332E-04,1.302721E-04,1.243892E-04,1.187720E-04,
                            1.134085E-04,1.082871E-04,1.033970E-04,9.872779E-05,9.426940E-05,9.001235E-05,8.594753E-05,
                            8.206628E-05,7.836030E-05,7.482167E-05,7.144285E-05,6.821660E-05,6.513605E-05,6.219461E-05,
                            5.938600E-05,5.670423E-05,5.414355E-05,5.169852E-05,4.936390E-05,4.713470E-05,4.500617E-05,
                            4.297377E-05,4.103314E-05,3.918015E-05,3.741084E-05,3.572142E-05,3.410830E-05,3.256803E-05,
                            3.109731E-05,2.969300E-05,2.835211E-05,2.707178E-05,2.584926E-05,2.468195E-05,2.356735E-05,
                            2.250309E-05,2.148688E-05,2.051657E-05,1.959007E-05,1.870542E-05,1.786071E-05,1.705415E-05,
                            1.628401E-05,1.554865E-05,1.484650E-05,1.417606E-05,1.353589E-05,1.292463E-05,1.234097E-05,
                            1.178368E-05,1.125154E-05,1.074344E-05,1.025829E-05,9.795037E-06,9.352709E-06,8.930356E-06,
                            8.527075E-06,8.142006E-06,7.774326E-06,7.423250E-06,7.088028E-06,6.767944E-06,6.462315E-06,
                            6.170487E-06,5.891838E-06,5.625772E-06,5.371721E-06,5.129143E-06,4.897519E-06,4.676355E-06,
                            4.465178E-06,4.263538E-06,4.071003E-06,3.887163E-06,3.711625E-06,3.544014E-06,3.383972E-06,
                            3.231157E-06,3.085243E-06,2.945919E-06,2.812886E-06,2.685860E-06,2.564571E-06,2.448759E-06,
                            2.338177E-06,2.232589E-06,2.131769E-06,2.035502E-06,1.943582E-06,1.855813E-06,1.772007E-06,
                            1.691986E-06,1.615579E-06,1.542622E-06,1.472959E-06,1.406443E-06,1.342930E-06,1.282286E-06,
                            1.224380E-06,1.169089E-06,1.116294E-06,1.065884E-06,1.017751E-06,9.717908E-07,9.279063E-07,
                            8.860035E-07,8.459930E-07,8.077893E-07,7.713109E-07,7.364797E-07,7.032215E-07,6.714651E-07,
                            6.411428E-07,6.121898E-07,5.845443E-07,5.581472E-07,5.329422E-07,5.088754E-07,4.858954E-07,
                            4.639531E-07,4.430018E-07],
                            [5.500000E+01,5.349602E+01,5.203317E+01,5.061032E+01,4.922638E+01,4.788028E+01,4.657099E+01,
                            1.002975E+02,9.755487E+01,9.488722E+01,9.229253E+01,8.976878E+01,8.731405E+01,8.492644E+01,
                            1.376041E+02,1.338413E+02,1.301814E+02,1.266216E+02,1.231591E+02,1.197913E+02,1.165156E+02,
                            1.683295E+02,1.637265E+02,1.592494E+02,1.548947E+02,1.506591E+02,1.465394E+02,1.425322E+02,
                            1.936347E+02,1.883397E+02,1.831896E+02,1.781802E+02,1.733079E+02,1.685688E+02,1.639593E+02,
                            1.594758E+02,1.551149E+02,1.508733E+02,1.467476E+02,1.427348E+02,1.388317E+02,1.350354E+02,
                            1.313428E+02,1.277512E+02,1.242579E+02,1.208600E+02,1.175551E+02,1.143406E+02,1.112139E+02,
                            1.081728E+02,1.052148E+02,1.023377E+02,9.953925E+01,9.681734E+01,9.416987E+01,9.159479E+01,
                            8.909012E+01,8.665395E+01,8.428439E+01,8.197963E+01,7.973789E+01,7.755746E+01,7.543664E+01,
                            7.337382E+01,7.136741E+01,6.941587E+01,6.751769E+01,6.567141E+01,6.387562E+01,6.212894E+01,
                            6.043002E+01,5.877756E+01,5.717028E+01,5.560696E+01,5.408638E+01,5.260739E+01,5.116884E+01,
                            4.976962E+01,4.840867E+01,4.708493E+01,4.579739E+01,4.454506E+01,4.332697E+01,4.214220E+01,
                            4.098981E+01,3.986895E+01,3.877873E+01,3.771832E+01,3.668691E+01,3.568371E+01,3.470793E+01,
                            3.375884E+01,3.283571E+01,3.193781E+01,3.106447E+01,3.021501E+01,2.938878E+01,2.858514E+01,
                            2.780348E+01,2.704319E+01,2.630369E+01,2.558442E+01,2.488481E+01,2.420434E+01,2.354247E+01,
                            2.289870E+01,2.227253E+01,2.166349E+01,2.107110E+01,2.049491E+01,1.993447E+01,1.938936E+01,
                            1.885916E+01,1.834346E+01,1.784185E+01,1.735397E+01,1.687942E+01,1.641785E+01,1.596891E+01,
                            1.553224E+01,1.510751E+01,1.469439E+01,1.429257E+01,1.390174E+01,1.352160E+01,1.315185E+01,
                            1.279221E+01,1.244241E+01,1.210217E+01,1.177123E+01,1.144935E+01,1.113627E+01,1.083174E+01,
                            1.053555E+01,1.024745E+01,9.967237E+00,9.694682E+00,9.429580E+00,9.171728E+00,8.920927E+00,
                            8.676983E+00,8.439711E+00,8.208926E+00,7.984453E+00,7.766118E+00,7.553753E+00,7.347195E+00,
                            7.146286E+00,6.950870E+00,6.760798E+00,6.575924E+00,6.396105E+00,6.221203E+00,6.051084E+00,
                            5.885617E+00,5.724674E+00,5.568133E+00,5.415872E+00,5.267774E+00,5.123727E+00,4.983618E+00,
                            4.847341E+00,4.714790E+00,4.585864E+00,4.460463E+00,4.338492E+00,4.219855E+00,4.104463E+00,
                            3.992226E+00,3.883059E+00,3.776876E+00,3.673597E+00,3.573143E+00,3.475435E+00,3.380399E+00,
                            3.287962E+00,3.198052E+00,3.110601E+00,3.025542E+00,2.942808E+00,2.862337E+00,2.784066E+00,
                            2.707936E+00,2.633887E+00,2.561863E+00,2.491809E+00,2.423670E+00,2.357395E+00,2.292932E+00,
                            2.230232E+00,2.169246E+00,2.109928E+00,2.052232E+00,1.996113E+00,1.941529E+00,1.888438E+00,
                            1.836799E+00,1.786571E+00,1.737718E+00,1.690200E+00,1.643981E+00,1.599026E+00,1.555301E+00,
                            1.512771E+00,1.471404E+00,1.431169E+00,1.392033E+00,1.353968E+00,1.316944E+00,1.280932E+00,
                            1.245905E+00,1.211835E+00,1.178698E+00,1.146466E+00,1.115116E+00,1.084623E+00,1.054964E+00,
                            1.026116E+00,9.980566E-01,9.707647E-01,9.442191E-01,9.183994E-01,8.932857E-01,8.688588E-01,
                            8.450998E-01,8.219905E-01,7.995131E-01,7.776504E-01,7.563855E-01,7.357021E-01,7.155843E-01,
                            6.960166E-01,6.769840E-01,6.584718E-01,6.404659E-01,6.229523E-01,6.059176E-01,5.893488E-01,
                            5.732330E-01,5.575579E-01,5.423115E-01,5.274819E-01,5.130579E-01,4.990283E-01,4.853824E-01,
                            4.721095E-01,4.591997E-01,4.466428E-01,4.344294E-01,4.225499E-01,4.109952E-01,3.997565E-01,
                            3.888252E-01,3.781927E-01,3.678510E-01,3.577921E-01,3.480083E-01,3.384920E-01,3.292359E-01,
                            3.202329E-01,3.114761E-01,3.029588E-01,2.946744E-01,2.866165E-01,2.787790E-01,2.711557E-01,
                            2.637410E-01,2.565290E-01,2.495142E-01,2.426912E-01,2.360548E-01,2.295998E-01,2.233214E-01,
                            2.172147E-01,2.112749E-01,2.054976E-01,1.998783E-01,1.944126E-01,1.890964E-01,1.839255E-01,
                            1.788961E-01,1.740041E-01,1.692460E-01,1.646180E-01,1.601165E-01,1.557381E-01,1.514794E-01,
                            1.473372E-01,1.433082E-01,1.393895E-01,1.355779E-01,1.318705E-01,1.282645E-01,1.247571E-01,
                            1.213456E-01,1.180274E-01,1.147999E-01,1.116607E-01,1.086073E-01,1.056375E-01,1.027488E-01,
                            9.993914E-02,9.720630E-02,9.454818E-02,9.196276E-02,8.944803E-02,8.700207E-02,8.462300E-02,
                            8.230898E-02,8.005823E-02,7.786904E-02,7.573970E-02,7.366860E-02,7.165412E-02,6.969474E-02,
                            6.778893E-02,6.593524E-02,6.413224E-02,6.237854E-02,6.067279E-02,5.901369E-02,5.739996E-02,
                            5.583036E-02,5.430367E-02,5.281874E-02,5.137440E-02,4.996957E-02,4.860315E-02,4.727409E-02,
                            4.598138E-02,4.472402E-02,4.350104E-02,4.231150E-02,4.115449E-02,4.002912E-02,3.893452E-02,
                            3.786985E-02,3.683430E-02,3.582706E-02,3.484737E-02,3.389447E-02,3.296762E-02,3.206612E-02,
                            3.118927E-02,3.033640E-02,2.950685E-02,2.869998E-02,2.791518E-02,2.715184E-02,2.640937E-02,
                            2.568720E-02,2.498478E-02,2.430157E-02,2.363705E-02,2.299069E-02,2.236201E-02,2.175052E-02,
                            2.115575E-02,2.057724E-02,2.001456E-02,1.946726E-02,1.893493E-02,1.841715E-02,1.791353E-02,
                            1.742368E-02,1.694723E-02],
                            [3.000000E+02,2.941172E+02,2.883497E+02,2.826954E+02,2.771519E+02,2.717171E+02,2.663889E+02,
                            2.611652E+02,2.560439E+02,2.510230E+02,2.461006E+02,2.412747E+02,2.365435E+02,2.319050E+02,
                            2.273575E+02,2.228991E+02,2.185282E+02,2.142430E+02,2.100418E+02,2.059231E+02,2.018850E+02,
                            1.979262E+02,1.940450E+02,1.902399E+02,1.865094E+02,1.828520E+02,1.792664E+02,1.757511E+02,
                            1.723048E+02,1.689260E+02,1.656134E+02,1.623658E+02,1.591820E+02,1.560605E+02,1.530002E+02,
                            1.500000E+02,1.470586E+02,1.441749E+02,1.413477E+02,1.385759E+02,1.358585E+02,1.331944E+02,
                            1.305826E+02,1.280219E+02,1.255115E+02,1.230503E+02,1.206374E+02,1.182717E+02,1.159525E+02,
                            1.136787E+02,1.114496E+02,1.092641E+02,1.071215E+02,1.050209E+02,1.029615E+02,1.009425E+02,
                            9.896309E+01,9.702249E+01,9.511994E+01,9.325469E+01,9.142602E+01,8.963322E+01,8.787556E+01,
                            8.615238E+01,8.446298E+01,8.280671E+01,8.118292E+01,7.959098E+01,7.803025E+01,7.650012E+01,
                            7.500000E+01,7.352930E+01,7.208743E+01,7.067384E+01,6.928797E+01,6.792927E+01,6.659722E+01,
                            6.529129E+01,6.401097E+01,6.275575E+01,6.152515E+01,6.031868E+01,5.913587E+01,5.797625E+01,
                            5.683937E+01,5.572479E+01,5.463206E+01,5.356076E+01,5.251046E+01,5.148076E+01,5.047126E+01,
                            4.948155E+01,4.851124E+01,4.755997E+01,4.662735E+01,4.571301E+01,4.481661E+01,4.393778E+01,
                            4.307619E+01,4.223149E+01,4.140336E+01,4.059146E+01,3.979549E+01,3.901512E+01,3.825006E+01,
                            3.750000E+01,3.676465E+01,3.604372E+01,3.533692E+01,3.464398E+01,3.396464E+01,3.329861E+01,
                            3.264565E+01,3.200548E+01,3.137788E+01,3.076258E+01,3.015934E+01,2.956793E+01,2.898813E+01,
                            2.841969E+01,2.786239E+01,2.731603E+01,2.678038E+01,2.625523E+01,2.574038E+01,2.523563E+01,
                            2.474077E+01,2.425562E+01,2.377998E+01,2.331367E+01,2.285651E+01,2.240830E+01,2.196889E+01,
                            2.153809E+01,2.111575E+01,2.070168E+01,2.029573E+01,1.989774E+01,1.950756E+01,1.912503E+01,
                            1.875000E+01,1.838232E+01,1.802186E+01,1.766846E+01,1.732199E+01,1.698232E+01,1.664931E+01,
                            1.632282E+01,1.600274E+01,1.568894E+01,1.538129E+01,1.507967E+01,1.478397E+01,1.449406E+01,
                            1.420984E+01,1.393120E+01,1.365801E+01,1.339019E+01,1.312762E+01,1.287019E+01,1.261781E+01,
                            1.237039E+01,1.212781E+01,1.188999E+01,1.165684E+01,1.142825E+01,1.120415E+01,1.098445E+01,
                            1.076905E+01,1.055787E+01,1.035084E+01,1.014787E+01,9.948872E+00,9.753781E+00,9.562515E+00,
                            9.375000E+00,9.191162E+00,9.010929E+00,8.834230E+00,8.660996E+00,8.491159E+00,8.324653E+00,
                            8.161412E+00,8.001371E+00,7.844469E+00,7.690644E+00,7.539835E+00,7.391984E+00,7.247031E+00,
                            7.104921E+00,6.965598E+00,6.829007E+00,6.695094E+00,6.563808E+00,6.435095E+00,6.308907E+00,
                            6.185193E+00,6.063905E+00,5.944996E+00,5.828418E+00,5.714127E+00,5.602076E+00,5.492223E+00,
                            5.384524E+00,5.278936E+00,5.175420E+00,5.073933E+00,4.974436E+00,4.876890E+00,4.781258E+00,
                            4.687500E+00,4.595581E+00,4.505464E+00,4.417115E+00,4.330498E+00,4.245580E+00,4.162326E+00,
                            4.080706E+00,4.000686E+00,3.922235E+00,3.845322E+00,3.769918E+00,3.695992E+00,3.623516E+00,
                            3.552461E+00,3.482799E+00,3.414504E+00,3.347547E+00,3.281904E+00,3.217548E+00,3.154454E+00,
                            3.092597E+00,3.031953E+00,2.972498E+00,2.914209E+00,2.857063E+00,2.801038E+00,2.746111E+00,
                            2.692262E+00,2.639468E+00,2.587710E+00,2.536966E+00,2.487218E+00,2.438445E+00,2.390629E+00,
                            2.343750E+00,2.297790E+00,2.252732E+00,2.208558E+00,2.165249E+00,2.122790E+00,2.081163E+00,
                            2.040353E+00,2.000343E+00,1.961117E+00,1.922661E+00,1.884959E+00,1.847996E+00,1.811758E+00,
                            1.776230E+00,1.741400E+00,1.707252E+00,1.673774E+00,1.640952E+00,1.608774E+00,1.577227E+00,
                            1.546298E+00,1.515976E+00,1.486249E+00,1.457105E+00,1.428532E+00,1.400519E+00,1.373056E+00,
                            1.346131E+00,1.319734E+00,1.293855E+00,1.268483E+00,1.243609E+00,1.219223E+00,1.195314E+00,
                            1.171875E+00,1.148895E+00,1.126366E+00,1.104279E+00,1.082625E+00,1.061395E+00,1.040582E+00,
                            1.020176E+00,1.000171E+00,9.805587E-01,9.613305E-01,9.424794E-01,9.239979E-01,9.058789E-01,
                            8.881152E-01,8.706998E-01,8.536259E-01,8.368868E-01,8.204760E-01,8.043869E-01,7.886134E-01,
                            7.731492E-01,7.579882E-01,7.431245E-01,7.285523E-01,7.142658E-01,7.002595E-01,6.865278E-01,
                            6.730654E-01,6.598670E-01,6.469274E-01,6.342416E-01,6.218045E-01,6.096113E-01,5.976572E-01,
                            5.859375E-01,5.744476E-01,5.631831E-01,5.521394E-01,5.413123E-01,5.306975E-01,5.202908E-01,
                            5.100882E-01,5.000857E-01,4.902793E-01,4.806652E-01,4.712397E-01,4.619990E-01,4.529395E-01,
                            4.440576E-01,4.353499E-01,4.268129E-01,4.184434E-01,4.102380E-01,4.021935E-01,3.943067E-01,
                            3.865746E-01,3.789941E-01,3.715622E-01,3.642761E-01,3.571329E-01,3.501297E-01,3.432639E-01,
                            3.365327E-01,3.299335E-01,3.234637E-01,3.171208E-01,3.109023E-01,3.048056E-01,2.988286E-01,
                            2.929687E-01,2.872238E-01,2.815915E-01,2.760697E-01,2.706561E-01,2.653487E-01,2.601454E-01,
                            2.550441E-01,2.500429E-01,2.451397E-01,2.403326E-01,2.356198E-01,2.309995E-01,2.264697E-01,
                            2.220288E-01,2.176749E-01]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366

            # internally specified variable (from internal database)
            food_multiplier = pd.Series([15., 110., 240.])

            # input variables that change per simulation
            ted_empty.foliar_diss_hlife = pd.Series([15., 25., 35.])
            ted_empty.app_rate_min = pd.Series([0.18, 0.5, 1.25]) # lbs a.i./acre

            # application scenarios generated from 'daily_app_flag' tests and reused here
            daily_flag = pd.Series([[True, False, False, True, False, False, True, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                             [True, False, False, False, False, False, False, True, False, False,
                              False, False, False, False, True, False, False, False, False, False,
                              False, True, False, False, False, False, False, False, True, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False],
                              [True, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False]], dtype='bool')


            for i in range(3):
                result[i] = ted_empty.daily_plant_timeseries(i, ted_empty.app_rate_min[i], food_multiplier[i], daily_flag[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_soil_h2o_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil pore water and surface puddles
        :param i; simulation number/index
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs
        :param daily_flag; daily flag denoting if pesticide is applied (0 - not applied, 1 - applied)
        :param water_type; type of water (pore water or surface puddles)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [[2.235571E-02,2.134616E-02,2.038220E-02,4.181749E-02,3.992908E-02,3.812594E-02,
                             5.875995E-02,5.610644E-02,5.357277E-02,5.115350E-02,4.884349E-02,4.663780E-02,
                             4.453171E-02,4.252073E-02,4.060056E-02,3.876711E-02,3.701645E-02,3.534484E-02,
                             3.374873E-02,3.222469E-02,3.076947E-02,2.937997E-02,2.805322E-02,2.678638E-02,
                             2.557675E-02,2.442175E-02,2.331890E-02,2.226586E-02,2.126037E-02,2.030028E-02,
                             1.938355E-02,1.850822E-02,1.767242E-02,1.687436E-02,1.611234E-02,1.538474E-02,
                             1.468999E-02,1.402661E-02,1.339319E-02,1.278838E-02,1.221087E-02,1.165945E-02,
                             1.113293E-02,1.063018E-02,1.015014E-02,9.691777E-03,9.254112E-03,8.836211E-03,
                             8.437182E-03,8.056172E-03,7.692368E-03,7.344993E-03,7.013305E-03,6.696596E-03,
                             6.394188E-03,6.105437E-03,5.829725E-03,5.566464E-03,5.315091E-03,5.075070E-03,
                             4.845888E-03,4.627056E-03,4.418105E-03,4.218591E-03,4.028086E-03,3.846184E-03,
                             3.672497E-03,3.506653E-03,3.348298E-03,3.197094E-03,3.052718E-03,2.914863E-03,
                             2.783232E-03,2.657546E-03,2.537535E-03,2.422944E-03,2.313528E-03,2.209053E-03,
                             2.109295E-03,2.014043E-03,1.923092E-03,1.836248E-03,1.753326E-03,1.674149E-03,
                             1.598547E-03,1.526359E-03,1.457431E-03,1.391616E-03,1.328773E-03,1.268768E-03,
                             1.211472E-03,1.156764E-03,1.104526E-03,1.054648E-03,1.007022E-03,9.615460E-04,
                             9.181242E-04,8.766632E-04,8.370745E-04,7.992735E-04,7.631796E-04,7.287156E-04,
                             6.958080E-04,6.643864E-04,6.343838E-04,6.057361E-04,5.783820E-04,5.522632E-04,
                             5.273239E-04,5.035108E-04,4.807730E-04,4.590621E-04,4.383316E-04,4.185372E-04,
                             3.996368E-04,3.815898E-04,3.643578E-04,3.479040E-04,3.321932E-04,3.171919E-04,
                             3.028680E-04,2.891910E-04,2.761316E-04,2.636619E-04,2.517554E-04,2.403865E-04,
                             2.295310E-04,2.191658E-04,2.092686E-04,1.998184E-04,1.907949E-04,1.821789E-04,
                             1.739520E-04,1.660966E-04,1.585960E-04,1.514340E-04,1.445955E-04,1.380658E-04,
                             1.318310E-04,1.258777E-04,1.201933E-04,1.147655E-04,1.095829E-04,1.046343E-04,
                             9.990919E-05,9.539745E-05,9.108945E-05,8.697600E-05,8.304830E-05,7.929798E-05,
                             7.571701E-05,7.229775E-05,6.903290E-05,6.591548E-05,6.293885E-05,6.009663E-05,
                             5.738276E-05,5.479145E-05,5.231715E-05,4.995459E-05,4.769873E-05,4.554473E-05,
                             4.348800E-05,4.152415E-05,3.964899E-05,3.785850E-05,3.614887E-05,3.451645E-05,
                             3.295774E-05,3.146942E-05,3.004831E-05,2.869138E-05,2.739572E-05,2.615858E-05,
                             2.497730E-05,2.384936E-05,2.277236E-05,2.174400E-05,2.076208E-05,1.982449E-05,
                             1.892925E-05,1.807444E-05,1.725822E-05,1.647887E-05,1.573471E-05,1.502416E-05,
                             1.434569E-05,1.369786E-05,1.307929E-05,1.248865E-05,1.192468E-05,1.138618E-05,
                             1.087200E-05,1.038104E-05,9.912247E-06,9.464626E-06,9.037219E-06,8.629112E-06,
                             8.239435E-06,7.867356E-06,7.512079E-06,7.172845E-06,6.848931E-06,6.539644E-06,
                             6.244324E-06,5.962341E-06,5.693091E-06,5.436000E-06,5.190519E-06,4.956124E-06,
                             4.732313E-06,4.518609E-06,4.314556E-06,4.119718E-06,3.933678E-06,3.756039E-06,
                             3.586423E-06,3.424465E-06,3.269822E-06,3.122162E-06,2.981170E-06,2.846545E-06,
                             2.718000E-06,2.595260E-06,2.478062E-06,2.366156E-06,2.259305E-06,2.157278E-06,
                             2.059859E-06,1.966839E-06,1.878020E-06,1.793211E-06,1.712233E-06,1.634911E-06,
                             1.561081E-06,1.490585E-06,1.423273E-06,1.359000E-06,1.297630E-06,1.239031E-06,
                             1.183078E-06,1.129652E-06,1.078639E-06,1.029929E-06,9.834195E-07,9.390098E-07,
                             8.966056E-07,8.561164E-07,8.174555E-07,7.805405E-07,7.452926E-07,7.116364E-07,
                             6.795000E-07,6.488149E-07,6.195154E-07,5.915391E-07,5.648262E-07,5.393195E-07,
                             5.149647E-07,4.917097E-07,4.695049E-07,4.483028E-07,4.280582E-07,4.087278E-07,
                             3.902703E-07,3.726463E-07,3.558182E-07,3.397500E-07,3.244074E-07,3.097577E-07,
                             2.957696E-07,2.824131E-07,2.696598E-07,2.574824E-07,2.458549E-07,2.347525E-07,
                             2.241514E-07,2.140291E-07,2.043639E-07,1.951351E-07,1.863231E-07,1.779091E-07,
                             1.698750E-07,1.622037E-07,1.548789E-07,1.478848E-07,1.412065E-07,1.348299E-07,
                             1.287412E-07,1.229274E-07,1.173762E-07,1.120757E-07,1.070145E-07,1.021819E-07,
                             9.756757E-08,9.316157E-08,8.895455E-08,8.493750E-08,8.110186E-08,7.743943E-08,
                             7.394239E-08,7.060327E-08,6.741494E-08,6.437059E-08,6.146372E-08,5.868811E-08,
                             5.603785E-08,5.350727E-08,5.109097E-08,4.878378E-08,4.658079E-08,4.447727E-08,
                             4.246875E-08,4.055093E-08,3.871971E-08,3.697119E-08,3.530163E-08,3.370747E-08,
                             3.218529E-08,3.073186E-08,2.934406E-08,2.801893E-08,2.675364E-08,2.554549E-08,
                             2.439189E-08,2.329039E-08,2.223864E-08,2.123438E-08,2.027546E-08,1.935986E-08,
                             1.848560E-08,1.765082E-08,1.685373E-08,1.609265E-08,1.536593E-08,1.467203E-08,
                             1.400946E-08,1.337682E-08,1.277274E-08,1.219595E-08,1.164520E-08,1.111932E-08,
                             1.061719E-08,1.013773E-08,9.679929E-09,9.242799E-09,8.825409E-09,8.426867E-09,
                             8.046324E-09,7.682965E-09,7.336014E-09,7.004732E-09,6.688409E-09,6.386371E-09,
                             6.097973E-09,5.822598E-09,5.559659E-09,5.308594E-09,5.068866E-09,4.839964E-09,
                             4.621399E-09,4.412704E-09,4.213434E-09,4.023162E-09,3.841482E-09,3.668007E-09],
                             [9.391514E-02,8.762592E-02,8.175787E-02,7.628279E-02,7.117436E-02,6.640803E-02,
                              6.196088E-02,1.517267E-01,1.415660E-01,1.320858E-01,1.232404E-01,1.149873E-01,
                              1.072870E-01,1.001023E-01,1.873139E-01,1.747700E-01,1.630662E-01,1.521461E-01,
                              1.419574E-01,1.324509E-01,1.235811E-01,2.092203E-01,1.952095E-01,1.821369E-01,
                              1.699397E-01,1.585594E-01,1.479411E-01,1.380340E-01,2.227054E-01,2.077915E-01,
                              1.938763E-01,1.808930E-01,1.687791E-01,1.574765E-01,1.469307E-01,1.370912E-01,
                              1.279106E-01,1.193449E-01,1.113527E-01,1.038957E-01,9.693814E-02,9.044648E-02,
                              8.438955E-02,7.873824E-02,7.346537E-02,6.854562E-02,6.395532E-02,5.967242E-02,
                              5.567634E-02,5.194786E-02,4.846907E-02,4.522324E-02,4.219478E-02,3.936912E-02,
                              3.673269E-02,3.427281E-02,3.197766E-02,2.983621E-02,2.783817E-02,2.597393E-02,
                              2.423454E-02,2.261162E-02,2.109739E-02,1.968456E-02,1.836634E-02,1.713640E-02,
                              1.598883E-02,1.491811E-02,1.391909E-02,1.298697E-02,1.211727E-02,1.130581E-02,
                              1.054869E-02,9.842280E-03,9.183172E-03,8.568202E-03,7.994415E-03,7.459053E-03,
                              6.959543E-03,6.493483E-03,6.058634E-03,5.652905E-03,5.274347E-03,4.921140E-03,
                              4.591586E-03,4.284101E-03,3.997208E-03,3.729527E-03,3.479771E-03,3.246741E-03,
                              3.029317E-03,2.826453E-03,2.637174E-03,2.460570E-03,2.295793E-03,2.142051E-03,
                              1.998604E-03,1.864763E-03,1.739886E-03,1.623371E-03,1.514658E-03,1.413226E-03,
                              1.318587E-03,1.230285E-03,1.147896E-03,1.071025E-03,9.993019E-04,9.323816E-04,
                              8.699428E-04,8.116854E-04,7.573292E-04,7.066131E-04,6.592934E-04,6.151425E-04,
                              5.739482E-04,5.355126E-04,4.996509E-04,4.661908E-04,4.349714E-04,4.058427E-04,
                              3.786646E-04,3.533066E-04,3.296467E-04,3.075712E-04,2.869741E-04,2.677563E-04,
                              2.498255E-04,2.330954E-04,2.174857E-04,2.029213E-04,1.893323E-04,1.766533E-04,
                              1.648233E-04,1.537856E-04,1.434871E-04,1.338782E-04,1.249127E-04,1.165477E-04,
                              1.087429E-04,1.014607E-04,9.466615E-05,8.832664E-05,8.241167E-05,7.689281E-05,
                              7.174353E-05,6.693908E-05,6.245637E-05,5.827385E-05,5.437143E-05,5.073034E-05,
                              4.733308E-05,4.416332E-05,4.120584E-05,3.844640E-05,3.587176E-05,3.346954E-05,
                              3.122818E-05,2.913693E-05,2.718571E-05,2.536517E-05,2.366654E-05,2.208166E-05,
                              2.060292E-05,1.922320E-05,1.793588E-05,1.673477E-05,1.561409E-05,1.456846E-05,
                              1.359286E-05,1.268258E-05,1.183327E-05,1.104083E-05,1.030146E-05,9.611601E-06,
                              8.967941E-06,8.367385E-06,7.807046E-06,7.284232E-06,6.796428E-06,6.341292E-06,
                              5.916635E-06,5.520415E-06,5.150730E-06,4.805801E-06,4.483971E-06,4.183692E-06,
                              3.903523E-06,3.642116E-06,3.398214E-06,3.170646E-06,2.958317E-06,2.760208E-06,
                              2.575365E-06,2.402900E-06,2.241985E-06,2.091846E-06,1.951762E-06,1.821058E-06,
                              1.699107E-06,1.585323E-06,1.479159E-06,1.380104E-06,1.287682E-06,1.201450E-06,
                              1.120993E-06,1.045923E-06,9.758808E-07,9.105289E-07,8.495535E-07,7.926615E-07,
                              7.395793E-07,6.900519E-07,6.438412E-07,6.007251E-07,5.604963E-07,5.229616E-07,
                              4.879404E-07,4.552645E-07,4.247768E-07,3.963307E-07,3.697897E-07,3.450260E-07,
                              3.219206E-07,3.003625E-07,2.802482E-07,2.614808E-07,2.439702E-07,2.276322E-07,
                              2.123884E-07,1.981654E-07,1.848948E-07,1.725130E-07,1.609603E-07,1.501813E-07,
                              1.401241E-07,1.307404E-07,1.219851E-07,1.138161E-07,1.061942E-07,9.908269E-08,
                              9.244741E-08,8.625649E-08,8.048015E-08,7.509063E-08,7.006204E-08,6.537019E-08,
                              6.099255E-08,5.690806E-08,5.309710E-08,4.954134E-08,4.622371E-08,4.312824E-08,
                              4.024007E-08,3.754532E-08,3.503102E-08,3.268510E-08,3.049627E-08,2.845403E-08,
                              2.654855E-08,2.477067E-08,2.311185E-08,2.156412E-08,2.012004E-08,1.877266E-08,
                              1.751551E-08,1.634255E-08,1.524814E-08,1.422702E-08,1.327427E-08,1.238534E-08,
                              1.155593E-08,1.078206E-08,1.006002E-08,9.386329E-09,8.757755E-09,8.171274E-09,
                              7.624068E-09,7.113507E-09,6.637137E-09,6.192668E-09,5.777963E-09,5.391030E-09,
                              5.030009E-09,4.693165E-09,4.378877E-09,4.085637E-09,3.812034E-09,3.556754E-09,
                              3.318569E-09,3.096334E-09,2.888982E-09,2.695515E-09,2.515005E-09,2.346582E-09,
                              2.189439E-09,2.042819E-09,1.906017E-09,1.778377E-09,1.659284E-09,1.548167E-09,
                              1.444491E-09,1.347758E-09,1.257502E-09,1.173291E-09,1.094719E-09,1.021409E-09,
                              9.530086E-10,8.891884E-10,8.296421E-10,7.740835E-10,7.222454E-10,6.738788E-10,
                              6.287512E-10,5.866456E-10,5.473597E-10,5.107046E-10,4.765043E-10,4.445942E-10,
                              4.148211E-10,3.870417E-10,3.611227E-10,3.369394E-10,3.143756E-10,2.933228E-10,
                              2.736798E-10,2.553523E-10,2.382521E-10,2.222971E-10,2.074105E-10,1.935209E-10,
                              1.805614E-10,1.684697E-10,1.571878E-10,1.466614E-10,1.368399E-10,1.276762E-10,
                              1.191261E-10,1.111486E-10,1.037053E-10,9.676043E-11,9.028068E-11,8.423485E-11,
                              7.859390E-11,7.333070E-11,6.841996E-11,6.383808E-11,5.956303E-11,5.557428E-11,
                              5.185263E-11,4.838022E-11,4.514034E-11,4.211743E-11,3.929695E-11,3.666535E-11,
                              3.420998E-11,3.191904E-11,2.978152E-11,2.778714E-11,2.592632E-11,2.419011E-11,
                              2.257017E-11,2.105871E-11,1.964847E-11,1.833267E-11,1.710499E-11,1.595952E-11],
                              [1.172251E-01,1.132320E-01,1.093749E-01,1.056492E-01,1.020504E-01,9.857420E-02,
                               9.521640E-02,9.197298E-02,8.884005E-02,8.581383E-02,8.289069E-02,8.006713E-02,
                               7.733975E-02,7.470528E-02,7.216054E-02,6.970249E-02,6.732817E-02,6.503472E-02,
                               6.281940E-02,6.067954E-02,5.861257E-02,5.661601E-02,5.468746E-02,5.282461E-02,
                               5.102521E-02,4.928710E-02,4.760820E-02,4.598649E-02,4.442002E-02,4.290691E-02,
                               4.144535E-02,4.003357E-02,3.866988E-02,3.735264E-02,3.608027E-02,3.485124E-02,
                               3.366408E-02,3.251736E-02,3.140970E-02,3.033977E-02,2.930629E-02,2.830801E-02,
                               2.734373E-02,2.641230E-02,2.551260E-02,2.464355E-02,2.380410E-02,2.299325E-02,
                               2.221001E-02,2.145346E-02,2.072267E-02,2.001678E-02,1.933494E-02,1.867632E-02,
                               1.804014E-02,1.742562E-02,1.683204E-02,1.625868E-02,1.570485E-02,1.516989E-02,
                               1.465314E-02,1.415400E-02,1.367187E-02,1.320615E-02,1.275630E-02,1.232178E-02,
                               1.190205E-02,1.149662E-02,1.110501E-02,1.072673E-02,1.036134E-02,1.000839E-02,
                               9.667469E-03,9.338160E-03,9.020068E-03,8.712811E-03,8.416021E-03,8.129340E-03,
                               7.852425E-03,7.584943E-03,7.326572E-03,7.077002E-03,6.835933E-03,6.603076E-03,
                               6.378151E-03,6.160888E-03,5.951025E-03,5.748312E-03,5.552503E-03,5.363364E-03,
                               5.180668E-03,5.004196E-03,4.833735E-03,4.669080E-03,4.510034E-03,4.356406E-03,
                               4.208010E-03,4.064670E-03,3.926212E-03,3.792471E-03,3.663286E-03,3.538501E-03,
                               3.417966E-03,3.301538E-03,3.189075E-03,3.080444E-03,2.975513E-03,2.874156E-03,
                               2.776251E-03,2.681682E-03,2.590334E-03,2.502098E-03,2.416867E-03,2.334540E-03,
                               2.255017E-03,2.178203E-03,2.104005E-03,2.032335E-03,1.963106E-03,1.896236E-03,
                               1.831643E-03,1.769250E-03,1.708983E-03,1.650769E-03,1.594538E-03,1.540222E-03,
                               1.487756E-03,1.437078E-03,1.388126E-03,1.340841E-03,1.295167E-03,1.251049E-03,
                               1.208434E-03,1.167270E-03,1.127508E-03,1.089101E-03,1.052003E-03,1.016168E-03,
                               9.815531E-04,9.481178E-04,9.158214E-04,8.846252E-04,8.544916E-04,8.253845E-04,
                               7.972689E-04,7.701110E-04,7.438782E-04,7.185389E-04,6.940629E-04,6.704205E-04,
                               6.475836E-04,6.255245E-04,6.042168E-04,5.836350E-04,5.637542E-04,5.445507E-04,
                               5.260013E-04,5.080838E-04,4.907766E-04,4.740589E-04,4.579107E-04,4.423126E-04,
                               4.272458E-04,4.126923E-04,3.986344E-04,3.850555E-04,3.719391E-04,3.592695E-04,
                               3.470314E-04,3.352103E-04,3.237918E-04,3.127622E-04,3.021084E-04,2.918175E-04,
                               2.818771E-04,2.722753E-04,2.630006E-04,2.540419E-04,2.453883E-04,2.370295E-04,
                               2.289554E-04,2.211563E-04,2.136229E-04,2.063461E-04,1.993172E-04,1.925277E-04,
                               1.859695E-04,1.796347E-04,1.735157E-04,1.676051E-04,1.618959E-04,1.563811E-04,
                               1.510542E-04,1.459087E-04,1.409386E-04,1.361377E-04,1.315003E-04,1.270209E-04,
                               1.226941E-04,1.185147E-04,1.144777E-04,1.105782E-04,1.068115E-04,1.031731E-04,
                               9.965861E-05,9.626387E-05,9.298477E-05,8.981737E-05,8.675786E-05,8.380257E-05,
                               8.094794E-05,7.819056E-05,7.552710E-05,7.295437E-05,7.046928E-05,6.806884E-05,
                               6.575016E-05,6.351047E-05,6.134707E-05,5.925736E-05,5.723884E-05,5.528908E-05,
                               5.340573E-05,5.158653E-05,4.982930E-05,4.813194E-05,4.649239E-05,4.490868E-05,
                               4.337893E-05,4.190128E-05,4.047397E-05,3.909528E-05,3.776355E-05,3.647719E-05,
                               3.523464E-05,3.403442E-05,3.287508E-05,3.175523E-05,3.067354E-05,2.962868E-05,
                               2.861942E-05,2.764454E-05,2.670286E-05,2.579327E-05,2.491465E-05,2.406597E-05,
                               2.324619E-05,2.245434E-05,2.168946E-05,2.095064E-05,2.023699E-05,1.954764E-05,
                               1.888178E-05,1.823859E-05,1.761732E-05,1.701721E-05,1.643754E-05,1.587762E-05,
                               1.533677E-05,1.481434E-05,1.430971E-05,1.382227E-05,1.335143E-05,1.289663E-05,
                               1.245733E-05,1.203298E-05,1.162310E-05,1.122717E-05,1.084473E-05,1.047532E-05,
                               1.011849E-05,9.773820E-06,9.440888E-06,9.119297E-06,8.808660E-06,8.508605E-06,
                               8.218770E-06,7.938809E-06,7.668384E-06,7.407170E-06,7.154855E-06,6.911134E-06,
                               6.675716E-06,6.448316E-06,6.228663E-06,6.016492E-06,5.811548E-06,5.613585E-06,
                               5.422366E-06,5.237660E-06,5.059247E-06,4.886910E-06,4.720444E-06,4.559648E-06,
                               4.404330E-06,4.254302E-06,4.109385E-06,3.969404E-06,3.834192E-06,3.703585E-06,
                               3.577428E-06,3.455567E-06,3.337858E-06,3.224158E-06,3.114332E-06,3.008246E-06,
                               2.905774E-06,2.806793E-06,2.711183E-06,2.618830E-06,2.529623E-06,2.443455E-06,
                               2.360222E-06,2.279824E-06,2.202165E-06,2.127151E-06,2.054693E-06,1.984702E-06,
                               1.917096E-06,1.851793E-06,1.788714E-06,1.727784E-06,1.668929E-06,1.612079E-06,
                               1.557166E-06,1.504123E-06,1.452887E-06,1.403396E-06,1.355592E-06,1.309415E-06,
                               1.264812E-06,1.221728E-06,1.180111E-06,1.139912E-06,1.101082E-06,1.063576E-06,
                               1.027346E-06,9.923511E-07,9.585480E-07,9.258963E-07,8.943569E-07,8.638918E-07,
                               8.344645E-07,8.060396E-07,7.785829E-07,7.520615E-07,7.264435E-07,7.016982E-07,
                               6.777958E-07,6.547076E-07,6.324058E-07,6.108638E-07,5.900555E-07,5.699560E-07,
                               5.505412E-07,5.317878E-07,5.136731E-07,4.961755E-07,4.792740E-07,4.629482E-07,
                               4.471784E-07,4.319459E-07,4.172322E-07,4.030198E-07,3.892914E-07,3.760307E-07]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366
            ted_empty.app_rate_conv = 11.2
            ted_empty.h2o_depth_puddles = 1.3
            ted_empty.soil_depth = 2.6
            ted_empty.soil_porosity = 0.4339623
            ted_empty.soil_bulk_density = 1.5
            ted_empty.h2o_depth_soil = 0.0
            ted_empty.soil_foc = 0.015

            # internally specified variable
            water_type = ['puddles', 'pore_water', 'puddles']

            # input variables that change per simulation
            ted_empty.aerobic_soil_meta_hlife = pd.Series([15., 10., 20.], dtype='float')
            ted_empty.koc = pd.Series([1500., 1000., 2000.], dtype='float')
            ted_empty.app_rate_min = pd.Series([0.18, 0.5, 1.25]) # lbs a.i./acre

            # application scenarios generated from 'daily_app_flag' tests and reused here
            daily_flag = pd.Series([[True, False, False, True, False, False, True, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                             [True, False, False, False, False, False, False, True, False, False,
                              False, False, False, False, True, False, False, False, False, False,
                              False, True, False, False, False, False, False, False, True, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False],
                              [True, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False]], dtype='bool')


            for i in range(3):
                result[i] = ted_empty.daily_soil_h2o_timeseries(i, ted_empty.app_rate_min[i], daily_flag[i], water_type[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_plant_dew_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide concentrations in dew that resides on broad leaf plants
        :param i; simulation number/index
        :param blp_conc; daily values of pesticide concentration in broad leaf plant dew

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               #this represents Eq 11 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([[]], dtype='float')
        expected_results = [[6.201749E+00,6.080137E+00,5.960909E+00,5.844019E+00,5.729422E+00,5.617071E+00,
                             5.506924E+00,1.160069E+01,1.137320E+01,1.115018E+01,1.093153E+01,1.071717E+01,
                             1.050702E+01,1.030098E+01,1.630073E+01,1.598109E+01,1.566771E+01,1.536047E+01,
                             1.505926E+01,1.476396E+01,1.447445E+01,2.039236E+01,1.999248E+01,1.960044E+01,
                             1.921609E+01,1.883927E+01,1.846984E+01,1.810766E+01,2.395433E+01,2.348460E+01,
                             2.302408E+01,2.257259E+01,2.212996E+01,2.169600E+01,2.127056E+01,2.085346E+01,
                             2.044453E+01,2.004363E+01,1.965059E+01,1.926525E+01,1.888747E+01,1.851710E+01,
                             1.815399E+01,1.779800E+01,1.744899E+01,1.710683E+01,1.677137E+01,1.644250E+01,
                             1.612007E+01,1.580396E+01,1.549406E+01,1.519023E+01,1.489236E+01,1.460033E+01,
                             1.431403E+01,1.403334E+01,1.375815E+01,1.348836E+01,1.322386E+01,1.296455E+01,
                             1.271032E+01,1.246108E+01,1.221673E+01,1.197717E+01,1.174230E+01,1.151204E+01,
                             1.128630E+01,1.106498E+01,1.084800E+01,1.063528E+01,1.042673E+01,1.022227E+01,
                             1.002181E+01,9.825293E+00,9.632625E+00,9.443735E+00,9.258549E+00,9.076994E+00,
                             8.899000E+00,8.724496E+00,8.553414E+00,8.385687E+00,8.221249E+00,8.060035E+00,
                             7.901982E+00,7.747029E+00,7.595115E+00,7.446179E+00,7.300164E+00,7.157013E+00,
                             7.016668E+00,6.879075E+00,6.744181E+00,6.611932E+00,6.482276E+00,6.355162E+00,
                             6.230541E+00,6.108364E+00,5.988583E+00,5.871150E+00,5.756021E+00,5.643149E+00,
                             5.532490E+00,5.424001E+00,5.317640E+00,5.213364E+00,5.111133E+00,5.010907E+00,
                             4.912646E+00,4.816312E+00,4.721867E+00,4.629274E+00,4.538497E+00,4.449500E+00,
                             4.362248E+00,4.276707E+00,4.192843E+00,4.110624E+00,4.030017E+00,3.950991E+00,
                             3.873515E+00,3.797557E+00,3.723090E+00,3.650082E+00,3.578506E+00,3.508334E+00,
                             3.439538E+00,3.372090E+00,3.305966E+00,3.241138E+00,3.177581E+00,3.115271E+00,
                             3.054182E+00,2.994291E+00,2.935575E+00,2.878010E+00,2.821574E+00,2.766245E+00,
                             2.712001E+00,2.658820E+00,2.606682E+00,2.555567E+00,2.505454E+00,2.456323E+00,
                             2.408156E+00,2.360934E+00,2.314637E+00,2.269249E+00,2.224750E+00,2.181124E+00,
                             2.138353E+00,2.096422E+00,2.055312E+00,2.015009E+00,1.975496E+00,1.936757E+00,
                             1.898779E+00,1.861545E+00,1.825041E+00,1.789253E+00,1.754167E+00,1.719769E+00,
                             1.686045E+00,1.652983E+00,1.620569E+00,1.588791E+00,1.557635E+00,1.527091E+00,
                             1.497146E+00,1.467788E+00,1.439005E+00,1.410787E+00,1.383122E+00,1.356000E+00,
                             1.329410E+00,1.303341E+00,1.277783E+00,1.252727E+00,1.228162E+00,1.204078E+00,
                             1.180467E+00,1.157319E+00,1.134624E+00,1.112375E+00,1.090562E+00,1.069177E+00,
                             1.048211E+00,1.027656E+00,1.007504E+00,9.877478E-01,9.683787E-01,9.493894E-01,
                             9.307724E-01,9.125205E-01,8.946266E-01,8.770835E-01,8.598844E-01,8.430226E-01,
                             8.264914E-01,8.102845E-01,7.943953E-01,7.788177E-01,7.635455E-01,7.485729E-01,
                             7.338938E-01,7.195026E-01,7.053936E-01,6.915612E-01,6.780002E-01,6.647050E-01,
                             6.516705E-01,6.388917E-01,6.263634E-01,6.140808E-01,6.020390E-01,5.902334E-01,
                             5.786593E-01,5.673121E-01,5.561875E-01,5.452810E-01,5.345884E-01,5.241054E-01,
                             5.138280E-01,5.037522E-01,4.938739E-01,4.841893E-01,4.746947E-01,4.653862E-01,
                             4.562603E-01,4.473133E-01,4.385417E-01,4.299422E-01,4.215113E-01,4.132457E-01,
                             4.051422E-01,3.971976E-01,3.894088E-01,3.817728E-01,3.742864E-01,3.669469E-01,
                             3.597513E-01,3.526968E-01,3.457806E-01,3.390001E-01,3.323525E-01,3.258353E-01,
                             3.194458E-01,3.131817E-01,3.070404E-01,3.010195E-01,2.951167E-01,2.893296E-01,
                             2.836561E-01,2.780937E-01,2.726405E-01,2.672942E-01,2.620527E-01,2.569140E-01,
                             2.518761E-01,2.469370E-01,2.420947E-01,2.373473E-01,2.326931E-01,2.281301E-01,
                             2.236566E-01,2.192709E-01,2.149711E-01,2.107557E-01,2.066229E-01,2.025711E-01,
                             1.985988E-01,1.947044E-01,1.908864E-01,1.871432E-01,1.834735E-01,1.798756E-01,
                             1.763484E-01,1.728903E-01,1.695000E-01,1.661762E-01,1.629176E-01,1.597229E-01,
                             1.565908E-01,1.535202E-01,1.505098E-01,1.475584E-01,1.446648E-01,1.418280E-01,
                             1.390469E-01,1.363202E-01,1.336471E-01,1.310264E-01,1.284570E-01,1.259380E-01,
                             1.234685E-01,1.210473E-01,1.186737E-01,1.163466E-01,1.140651E-01,1.118283E-01,
                             1.096354E-01,1.074856E-01,1.053778E-01,1.033114E-01,1.012856E-01,9.929941E-02,
                             9.735221E-02,9.544319E-02,9.357161E-02,9.173673E-02,8.993782E-02,8.817420E-02,
                             8.644516E-02,8.475002E-02,8.308812E-02,8.145882E-02,7.986146E-02,7.829542E-02,
                             7.676010E-02,7.525488E-02,7.377918E-02,7.233241E-02,7.091402E-02,6.952344E-02,
                             6.816012E-02,6.682355E-02,6.551318E-02,6.422850E-02,6.296902E-02,6.173424E-02,
                             6.052367E-02,5.933684E-02,5.817328E-02,5.703253E-02,5.591416E-02,5.481772E-02,
                             5.374278E-02,5.268891E-02,5.165572E-02,5.064278E-02,4.964970E-02,4.867610E-02,
                             4.772160E-02,4.678580E-02,4.586836E-02,4.496891E-02,4.408710E-02,4.322258E-02,
                             4.237501E-02,4.154406E-02,4.072941E-02,3.993073E-02,3.914771E-02,3.838005E-02,
                             3.762744E-02,3.688959E-02,3.616621E-02,3.545701E-02,3.476172E-02,3.408006E-02,
                             3.341177E-02,3.275659E-02,3.211425E-02,3.148451E-02,3.086712E-02,3.026183E-02],
                             [3.487500E-01,3.419112E-01,3.352066E-01,3.286334E-01,3.221891E-01,3.158711E-01,
                             3.096771E-01,6.523545E-01,6.395622E-01,6.270208E-01,6.147253E-01,6.026709E-01,
                             5.908529E-01,5.792667E-01,9.166576E-01,8.986825E-01,8.810599E-01,8.637828E-01,
                             8.468446E-01,8.302385E-01,8.139580E-01,1.000000E+00,1.000000E+00,1.000000E+00,
                             1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,
                             1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,
                             1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,1.000000E+00,
                             1.000000E+00,1.000000E+00,9.812289E-01,9.619876E-01,9.431236E-01,9.246296E-01,
                             9.064981E-01,8.887223E-01,8.712950E-01,8.542094E-01,8.374589E-01,8.210368E-01,
                             8.049368E-01,7.891525E-01,7.736777E-01,7.585063E-01,7.436325E-01,7.290503E-01,
                             7.147541E-01,7.007382E-01,6.869971E-01,6.735255E-01,6.603181E-01,6.473697E-01,
                             6.346751E-01,6.222295E-01,6.100280E-01,5.980657E-01,5.863380E-01,5.748403E-01,
                             5.635680E-01,5.525168E-01,5.416823E-01,5.310602E-01,5.206465E-01,5.104369E-01,
                             5.004275E-01,4.906145E-01,4.809938E-01,4.715618E-01,4.623148E-01,4.532491E-01,
                             4.443611E-01,4.356475E-01,4.271047E-01,4.187294E-01,4.105184E-01,4.024684E-01,
                             3.945762E-01,3.868388E-01,3.792532E-01,3.718162E-01,3.645251E-01,3.573770E-01,
                             3.503691E-01,3.434986E-01,3.367628E-01,3.301591E-01,3.236848E-01,3.173376E-01,
                             3.111148E-01,3.050140E-01,2.990329E-01,2.931690E-01,2.874201E-01,2.817840E-01,
                             2.762584E-01,2.708411E-01,2.655301E-01,2.603232E-01,2.552184E-01,2.502138E-01,
                             2.453072E-01,2.404969E-01,2.357809E-01,2.311574E-01,2.266245E-01,2.221806E-01,
                             2.178237E-01,2.135523E-01,2.093647E-01,2.052592E-01,2.012342E-01,1.972881E-01,
                             1.934194E-01,1.896266E-01,1.859081E-01,1.822626E-01,1.786885E-01,1.751845E-01,
                             1.717493E-01,1.683814E-01,1.650795E-01,1.618424E-01,1.586688E-01,1.555574E-01,
                             1.525070E-01,1.495164E-01,1.465845E-01,1.437101E-01,1.408920E-01,1.381292E-01,
                             1.354206E-01,1.327651E-01,1.301616E-01,1.276092E-01,1.251069E-01,1.226536E-01,
                             1.202485E-01,1.178905E-01,1.155787E-01,1.133123E-01,1.110903E-01,1.089119E-01,
                             1.067762E-01,1.046824E-01,1.026296E-01,1.006171E-01,9.864406E-02,9.670971E-02,
                             9.481329E-02,9.295406E-02,9.113129E-02,8.934426E-02,8.759227E-02,8.587464E-02,
                             8.419069E-02,8.253976E-02,8.092121E-02,7.933439E-02,7.777869E-02,7.625350E-02,
                             7.475822E-02,7.329225E-02,7.185504E-02,7.044600E-02,6.906460E-02,6.771029E-02,
                             6.638253E-02,6.508081E-02,6.380461E-02,6.255344E-02,6.132681E-02,6.012423E-02,
                             5.894523E-02,5.778935E-02,5.665613E-02,5.554514E-02,5.445593E-02,5.338809E-02,
                             5.234118E-02,5.131480E-02,5.030855E-02,4.932203E-02,4.835485E-02,4.740664E-02,
                             4.647703E-02,4.556564E-02,4.467213E-02,4.379614E-02,4.293732E-02,4.209535E-02,
                             4.126988E-02,4.046060E-02,3.966720E-02,3.888935E-02,3.812675E-02,3.737911E-02,
                             3.664613E-02,3.592752E-02,3.522300E-02,3.453230E-02,3.385514E-02,3.319126E-02,
                             3.254040E-02,3.190231E-02,3.127672E-02,3.066340E-02,3.006211E-02,2.947261E-02,
                             2.889467E-02,2.832807E-02,2.777257E-02,2.722797E-02,2.669404E-02,2.617059E-02,
                             2.565740E-02,2.515427E-02,2.466101E-02,2.417743E-02,2.370332E-02,2.323851E-02,
                             2.278282E-02,2.233606E-02,2.189807E-02,2.146866E-02,2.104767E-02,2.063494E-02,
                             2.023030E-02,1.983360E-02,1.944467E-02,1.906338E-02,1.868955E-02,1.832306E-02,
                             1.796376E-02,1.761150E-02,1.726615E-02,1.692757E-02,1.659563E-02,1.627020E-02,
                             1.595115E-02,1.563836E-02,1.533170E-02,1.503106E-02,1.473631E-02,1.444734E-02,
                             1.416403E-02,1.388629E-02,1.361398E-02,1.334702E-02,1.308529E-02,1.282870E-02,
                             1.257714E-02,1.233051E-02,1.208871E-02,1.185166E-02,1.161926E-02,1.139141E-02,
                             1.116803E-02,1.094903E-02,1.073433E-02,1.052384E-02,1.031747E-02,1.011515E-02,
                             9.916799E-03,9.722337E-03,9.531688E-03,9.344777E-03,9.161532E-03,8.981880E-03,
                             8.805750E-03,8.633075E-03,8.463786E-03,8.297816E-03,8.135101E-03,7.975577E-03,
                             7.819180E-03,7.665851E-03,7.515528E-03,7.368153E-03,7.223668E-03,7.082017E-03,
                             6.943143E-03,6.806992E-03,6.673511E-03,6.542647E-03,6.414350E-03,6.288569E-03,
                             6.165254E-03,6.044357E-03,5.925831E-03,5.809629E-03,5.695705E-03,5.584016E-03,
                             5.474517E-03,5.367165E-03,5.261918E-03,5.158735E-03,5.057576E-03,4.958400E-03,
                             4.861168E-03,4.765844E-03,4.672389E-03,4.580766E-03,4.490940E-03,4.402875E-03,
                             4.316538E-03,4.231893E-03,4.148908E-03,4.067550E-03,3.987788E-03,3.909590E-03,
                             3.832926E-03,3.757764E-03,3.684077E-03,3.611834E-03,3.541008E-03,3.471571E-03,
                             3.403496E-03,3.336755E-03,3.271324E-03,3.207175E-03,3.144284E-03,3.082627E-03,
                             3.022178E-03,2.962915E-03,2.904814E-03,2.847853E-03,2.792008E-03,2.737258E-03,
                             2.683583E-03,2.630959E-03,2.579368E-03,2.528788E-03,2.479200E-03,2.430584E-03,
                             2.382922E-03,2.336194E-03,2.290383E-03,2.245470E-03,2.201438E-03,2.158269E-03,
                             2.115946E-03,2.074454E-03,2.033775E-03,1.993894E-03,1.954795E-03,1.916463E-03,
                             1.878882E-03,1.842038E-03,1.805917E-03,1.770504E-03,1.735786E-03,1.701748E-03],
                             [8.718750E-02,8.547781E-02,8.380164E-02,8.215834E-02,8.054726E-02,7.896778E-02,
                              7.741927E-02,1.630886E-01,1.598906E-01,1.567552E-01,1.536813E-01,1.506677E-01,
                              1.477132E-01,1.448167E-01,2.291644E-01,2.246706E-01,2.202650E-01,2.159457E-01,
                              2.117111E-01,2.075596E-01,2.034895E-01,2.866867E-01,2.810649E-01,2.755534E-01,
                              2.701500E-01,2.648525E-01,2.596589E-01,2.545672E-01,3.367628E-01,3.301591E-01,
                              3.236848E-01,3.173376E-01,3.111148E-01,3.050140E-01,2.990329E-01,3.803565E-01,
                              3.728980E-01,3.655857E-01,3.584167E-01,3.513884E-01,3.444979E-01,3.377425E-01,
                              4.183071E-01,4.101043E-01,4.020624E-01,3.941782E-01,3.864486E-01,3.788706E-01,
                              3.714412E-01,3.641575E-01,3.570166E-01,3.500157E-01,3.431521E-01,3.364231E-01,
                              3.298260E-01,3.233583E-01,3.170175E-01,3.108010E-01,3.047063E-01,2.987312E-01,
                              2.928733E-01,2.871302E-01,2.814998E-01,2.759797E-01,2.705680E-01,2.652623E-01,
                              2.600606E-01,2.549610E-01,2.499614E-01,2.450598E-01,2.402543E-01,2.355431E-01,
                              2.309242E-01,2.263959E-01,2.219565E-01,2.176040E-01,2.133369E-01,2.091535E-01,
                              2.050522E-01,2.010312E-01,1.970891E-01,1.932243E-01,1.894353E-01,1.857206E-01,
                              1.820787E-01,1.785083E-01,1.750078E-01,1.715760E-01,1.682115E-01,1.649130E-01,
                              1.616792E-01,1.585087E-01,1.554005E-01,1.523532E-01,1.493656E-01,1.464367E-01,
                              1.435651E-01,1.407499E-01,1.379899E-01,1.352840E-01,1.326311E-01,1.300303E-01,
                              1.274805E-01,1.249807E-01,1.225299E-01,1.201272E-01,1.177715E-01,1.154621E-01,
                              1.131980E-01,1.109782E-01,1.088020E-01,1.066685E-01,1.045768E-01,1.025261E-01,
                              1.005156E-01,9.854456E-02,9.661216E-02,9.471765E-02,9.286030E-02,9.103937E-02,
                              8.925414E-02,8.750392E-02,8.578802E-02,8.410577E-02,8.245651E-02,8.083959E-02,
                              7.925437E-02,7.770024E-02,7.617659E-02,7.468281E-02,7.321833E-02,7.178256E-02,
                              7.037495E-02,6.899494E-02,6.764199E-02,6.631557E-02,6.501516E-02,6.374025E-02,
                              6.249035E-02,6.126495E-02,6.006358E-02,5.888577E-02,5.773106E-02,5.659899E-02,
                              5.548911E-02,5.440101E-02,5.333424E-02,5.228838E-02,5.126304E-02,5.025780E-02,
                              4.927228E-02,4.830608E-02,4.735883E-02,4.643015E-02,4.551968E-02,4.462707E-02,
                              4.375196E-02,4.289401E-02,4.205289E-02,4.122825E-02,4.041979E-02,3.962719E-02,
                              3.885012E-02,3.808829E-02,3.734141E-02,3.660916E-02,3.589128E-02,3.518747E-02,
                              3.449747E-02,3.382099E-02,3.315779E-02,3.250758E-02,3.187013E-02,3.124517E-02,
                              3.063247E-02,3.003179E-02,2.944289E-02,2.886553E-02,2.829949E-02,2.774456E-02,
                              2.720050E-02,2.666712E-02,2.614419E-02,2.563152E-02,2.512890E-02,2.463614E-02,
                              2.415304E-02,2.367941E-02,2.321507E-02,2.275984E-02,2.231353E-02,2.187598E-02,
                              2.144701E-02,2.102644E-02,2.061413E-02,2.020990E-02,1.981359E-02,1.942506E-02,
                              1.904415E-02,1.867070E-02,1.830458E-02,1.794564E-02,1.759374E-02,1.724873E-02,
                              1.691050E-02,1.657889E-02,1.625379E-02,1.593506E-02,1.562259E-02,1.531624E-02,
                              1.501590E-02,1.472144E-02,1.443276E-02,1.414975E-02,1.387228E-02,1.360025E-02,
                              1.333356E-02,1.307210E-02,1.281576E-02,1.256445E-02,1.231807E-02,1.207652E-02,
                              1.183971E-02,1.160754E-02,1.137992E-02,1.115677E-02,1.093799E-02,1.072350E-02,
                              1.051322E-02,1.030706E-02,1.010495E-02,9.906796E-03,9.712530E-03,9.522073E-03,
                              9.335351E-03,9.152291E-03,8.972820E-03,8.796868E-03,8.624367E-03,8.455249E-03,
                              8.289446E-03,8.126895E-03,7.967532E-03,7.811293E-03,7.658119E-03,7.507948E-03,
                              7.360721E-03,7.216382E-03,7.074873E-03,6.936139E-03,6.800126E-03,6.666780E-03,
                              6.536048E-03,6.407880E-03,6.282226E-03,6.159035E-03,6.038260E-03,5.919853E-03,
                              5.803769E-03,5.689960E-03,5.578384E-03,5.468995E-03,5.361751E-03,5.256611E-03,
                              5.153532E-03,5.052474E-03,4.953398E-03,4.856265E-03,4.761037E-03,4.667676E-03,
                              4.576145E-03,4.486410E-03,4.398434E-03,4.312184E-03,4.227624E-03,4.144723E-03,
                              4.063448E-03,3.983766E-03,3.905647E-03,3.829059E-03,3.753974E-03,3.680361E-03,
                              3.608191E-03,3.537437E-03,3.468070E-03,3.400063E-03,3.333390E-03,3.268024E-03,
                              3.203940E-03,3.141113E-03,3.079517E-03,3.019130E-03,2.959927E-03,2.901884E-03,
                              2.844980E-03,2.789192E-03,2.734497E-03,2.680876E-03,2.628305E-03,2.576766E-03,
                              2.526237E-03,2.476699E-03,2.428133E-03,2.380518E-03,2.333838E-03,2.288073E-03,
                              2.243205E-03,2.199217E-03,2.156092E-03,2.113812E-03,2.072362E-03,2.031724E-03,
                              1.991883E-03,1.952823E-03,1.914530E-03,1.876987E-03,1.840180E-03,1.804096E-03,
                              1.768718E-03,1.734035E-03,1.700031E-03,1.666695E-03,1.634012E-03,1.601970E-03,
                              1.570556E-03,1.539759E-03,1.509565E-03,1.479963E-03,1.450942E-03,1.422490E-03,
                              1.394596E-03,1.367249E-03,1.340438E-03,1.314153E-03,1.288383E-03,1.263119E-03,
                              1.238350E-03,1.214066E-03,1.190259E-03,1.166919E-03,1.144036E-03,1.121602E-03,
                              1.099609E-03,1.078046E-03,1.056906E-03,1.036181E-03,1.015862E-03,9.959415E-04,
                              9.764117E-04,9.572648E-04,9.384935E-04,9.200902E-04,9.020478E-04,8.843592E-04,
                              8.670174E-04,8.500157E-04,8.333474E-04,8.170060E-04,8.009850E-04,7.852782E-04,
                              7.698794E-04,7.547825E-04,7.399817E-04,7.254711E-04,7.112450E-04,6.972980E-04]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366
            ted_empty.frac_pest_on_surface = 0.62
            ted_empty.density_h2o = 1.0
            ted_empty.mass_wax = 0.012

            # input variables that change per simulation
            ted_empty.solubility = pd.Series([145., 1., 20.], dtype='float')
            ted_empty.log_kow = pd.Series([2.75, 4., 5.], dtype='float')

            # internally calculated variables
            blp_conc = pd.Series([[6.750000E+01,6.617637E+01,6.487869E+01,6.360646E+01,6.235917E+01,6.113635E+01,5.993750E+01,
                             1.262622E+02,1.237862E+02,1.213589E+02,1.189791E+02,1.166460E+02,1.143586E+02,1.121161E+02,
                             1.774176E+02,1.739385E+02,1.705277E+02,1.671838E+02,1.639054E+02,1.606913E+02,1.575403E+02,
                             2.219510E+02,2.175987E+02,2.133317E+02,2.091484E+02,2.050471E+02,2.010263E+02,1.970843E+02,
                             2.607196E+02,2.556070E+02,2.505947E+02,2.456807E+02,2.408631E+02,2.361399E+02,2.315093E+02,
                             2.269696E+02,2.225188E+02,2.181554E+02,2.138775E+02,2.096835E+02,2.055717E+02,2.015406E+02,
                             1.975885E+02,1.937139E+02,1.899153E+02,1.861912E+02,1.825401E+02,1.789606E+02,1.754513E+02,
                             1.720108E+02,1.686377E+02,1.653309E+02,1.620888E+02,1.589104E+02,1.557942E+02,1.527392E+02,
                             1.497441E+02,1.468077E+02,1.439289E+02,1.411065E+02,1.383395E+02,1.356267E+02,1.329672E+02,
                             1.303598E+02,1.278035E+02,1.252974E+02,1.228404E+02,1.204315E+02,1.180699E+02,1.157547E+02,
                             1.134848E+02,1.112594E+02,1.090777E+02,1.069387E+02,1.048417E+02,1.027859E+02,1.007703E+02,
                             9.879424E+01,9.685694E+01,9.495764E+01,9.309558E+01,9.127003E+01,8.948028E+01,8.772563E+01,
                             8.600538E+01,8.431887E+01,8.266543E+01,8.104441E+01,7.945518E+01,7.789711E+01,7.636959E+01,
                             7.487203E+01,7.340384E+01,7.196443E+01,7.055325E+01,6.916975E+01,6.781337E+01,6.648359E+01,
                             6.517989E+01,6.390175E+01,6.264868E+01,6.142018E+01,6.021576E+01,5.903497E+01,5.787733E+01,
                             5.674239E+01,5.562971E+01,5.453884E+01,5.346937E+01,5.242087E+01,5.139293E+01,5.038514E+01,
                             4.939712E+01,4.842847E+01,4.747882E+01,4.654779E+01,4.563501E+01,4.474014E+01,4.386281E+01,
                             4.300269E+01,4.215943E+01,4.133271E+01,4.052220E+01,3.972759E+01,3.894855E+01,3.818480E+01,
                             3.743602E+01,3.670192E+01,3.598222E+01,3.527663E+01,3.458487E+01,3.390669E+01,3.324180E+01,
                             3.258994E+01,3.195088E+01,3.132434E+01,3.071009E+01,3.010788E+01,2.951748E+01,2.893866E+01,
                             2.837119E+01,2.781485E+01,2.726942E+01,2.673468E+01,2.621043E+01,2.569646E+01,2.519257E+01,
                             2.469856E+01,2.421424E+01,2.373941E+01,2.327389E+01,2.281751E+01,2.237007E+01,2.193141E+01,
                             2.150135E+01,2.107972E+01,2.066636E+01,2.026110E+01,1.986379E+01,1.947428E+01,1.909240E+01,
                             1.871801E+01,1.835096E+01,1.799111E+01,1.763831E+01,1.729244E+01,1.695334E+01,1.662090E+01,
                             1.629497E+01,1.597544E+01,1.566217E+01,1.535504E+01,1.505394E+01,1.475874E+01,1.446933E+01,
                             1.418560E+01,1.390743E+01,1.363471E+01,1.336734E+01,1.310522E+01,1.284823E+01,1.259629E+01,
                             1.234928E+01,1.210712E+01,1.186970E+01,1.163695E+01,1.140875E+01,1.118503E+01,1.096570E+01,
                             1.075067E+01,1.053986E+01,1.033318E+01,1.013055E+01,9.931897E+00,9.737138E+00,9.546199E+00,
                             9.359004E+00,9.175480E+00,8.995554E+00,8.819157E+00,8.646218E+00,8.476671E+00,8.310449E+00,
                             8.147486E+00,7.987719E+00,7.831085E+00,7.677522E+00,7.526970E+00,7.379371E+00,7.234666E+00,
                             7.092799E+00,6.953713E+00,6.817355E+00,6.683671E+00,6.552608E+00,6.424116E+00,6.298143E+00,
                             6.174640E+00,6.053559E+00,5.934852E+00,5.818474E+00,5.704377E+00,5.592517E+00,5.482852E+00,
                             5.375336E+00,5.269929E+00,5.166589E+00,5.065275E+00,4.965948E+00,4.868569E+00,4.773100E+00,
                             4.679502E+00,4.587740E+00,4.497777E+00,4.409578E+00,4.323109E+00,4.238336E+00,4.155225E+00,
                             4.073743E+00,3.993859E+00,3.915542E+00,3.838761E+00,3.763485E+00,3.689686E+00,3.617333E+00,
                             3.546399E+00,3.476857E+00,3.408678E+00,3.341835E+00,3.276304E+00,3.212058E+00,3.149071E+00,
                             3.087320E+00,3.026779E+00,2.967426E+00,2.909237E+00,2.852188E+00,2.796259E+00,2.741426E+00,
                             2.687668E+00,2.634965E+00,2.583295E+00,2.532638E+00,2.482974E+00,2.434285E+00,2.386550E+00,
                             2.339751E+00,2.293870E+00,2.248889E+00,2.204789E+00,2.161555E+00,2.119168E+00,2.077612E+00,
                             2.036872E+00,1.996930E+00,1.957771E+00,1.919380E+00,1.881743E+00,1.844843E+00,1.808667E+00,
                             1.773200E+00,1.738428E+00,1.704339E+00,1.670918E+00,1.638152E+00,1.606029E+00,1.574536E+00,
                             1.543660E+00,1.513390E+00,1.483713E+00,1.454618E+00,1.426094E+00,1.398129E+00,1.370713E+00,
                             1.343834E+00,1.317482E+00,1.291647E+00,1.266319E+00,1.241487E+00,1.217142E+00,1.193275E+00,
                             1.169876E+00,1.146935E+00,1.124444E+00,1.102395E+00,1.080777E+00,1.059584E+00,1.038806E+00,
                             1.018436E+00,9.984649E-01,9.788856E-01,9.596902E-01,9.408713E-01,9.224214E-01,9.043333E-01,
                             8.865998E-01,8.692142E-01,8.521694E-01,8.354589E-01,8.190760E-01,8.030145E-01,7.872678E-01,
                             7.718300E-01,7.566949E-01,7.418565E-01,7.273092E-01,7.130471E-01,6.990647E-01,6.853565E-01,
                             6.719170E-01,6.587411E-01,6.458236E-01,6.331594E-01,6.207436E-01,6.085712E-01,5.966374E-01,
                             5.849378E-01,5.734675E-01,5.622221E-01,5.511973E-01,5.403887E-01,5.297920E-01,5.194031E-01,
                             5.092179E-01,4.992324E-01,4.894428E-01,4.798451E-01,4.704356E-01,4.612107E-01,4.521666E-01,
                             4.432999E-01,4.346071E-01,4.260847E-01,4.177294E-01,4.095380E-01,4.015072E-01,3.936339E-01,
                             3.859150E-01,3.783474E-01,3.709283E-01,3.636546E-01,3.565236E-01,3.495323E-01,3.426782E-01,
                             3.359585E-01,3.293706E-01],
                             [6.750000E+01,6.617637E+01,6.487869E+01,6.360646E+01,6.235917E+01,6.113635E+01,5.993750E+01,
                             1.262622E+02,1.237862E+02,1.213589E+02,1.189791E+02,1.166460E+02,1.143586E+02,1.121161E+02,
                             1.774176E+02,1.739385E+02,1.705277E+02,1.671838E+02,1.639054E+02,1.606913E+02,1.575403E+02,
                             2.219510E+02,2.175987E+02,2.133317E+02,2.091484E+02,2.050471E+02,2.010263E+02,1.970843E+02,
                             2.607196E+02,2.556070E+02,2.505947E+02,2.456807E+02,2.408631E+02,2.361399E+02,2.315093E+02,
                             2.269696E+02,2.225188E+02,2.181554E+02,2.138775E+02,2.096835E+02,2.055717E+02,2.015406E+02,
                             1.975885E+02,1.937139E+02,1.899153E+02,1.861912E+02,1.825401E+02,1.789606E+02,1.754513E+02,
                             1.720108E+02,1.686377E+02,1.653309E+02,1.620888E+02,1.589104E+02,1.557942E+02,1.527392E+02,
                             1.497441E+02,1.468077E+02,1.439289E+02,1.411065E+02,1.383395E+02,1.356267E+02,1.329672E+02,
                             1.303598E+02,1.278035E+02,1.252974E+02,1.228404E+02,1.204315E+02,1.180699E+02,1.157547E+02,
                             1.134848E+02,1.112594E+02,1.090777E+02,1.069387E+02,1.048417E+02,1.027859E+02,1.007703E+02,
                             9.879424E+01,9.685694E+01,9.495764E+01,9.309558E+01,9.127003E+01,8.948028E+01,8.772563E+01,
                             8.600538E+01,8.431887E+01,8.266543E+01,8.104441E+01,7.945518E+01,7.789711E+01,7.636959E+01,
                             7.487203E+01,7.340384E+01,7.196443E+01,7.055325E+01,6.916975E+01,6.781337E+01,6.648359E+01,
                             6.517989E+01,6.390175E+01,6.264868E+01,6.142018E+01,6.021576E+01,5.903497E+01,5.787733E+01,
                             5.674239E+01,5.562971E+01,5.453884E+01,5.346937E+01,5.242087E+01,5.139293E+01,5.038514E+01,
                             4.939712E+01,4.842847E+01,4.747882E+01,4.654779E+01,4.563501E+01,4.474014E+01,4.386281E+01,
                             4.300269E+01,4.215943E+01,4.133271E+01,4.052220E+01,3.972759E+01,3.894855E+01,3.818480E+01,
                             3.743602E+01,3.670192E+01,3.598222E+01,3.527663E+01,3.458487E+01,3.390669E+01,3.324180E+01,
                             3.258994E+01,3.195088E+01,3.132434E+01,3.071009E+01,3.010788E+01,2.951748E+01,2.893866E+01,
                             2.837119E+01,2.781485E+01,2.726942E+01,2.673468E+01,2.621043E+01,2.569646E+01,2.519257E+01,
                             2.469856E+01,2.421424E+01,2.373941E+01,2.327389E+01,2.281751E+01,2.237007E+01,2.193141E+01,
                             2.150135E+01,2.107972E+01,2.066636E+01,2.026110E+01,1.986379E+01,1.947428E+01,1.909240E+01,
                             1.871801E+01,1.835096E+01,1.799111E+01,1.763831E+01,1.729244E+01,1.695334E+01,1.662090E+01,
                             1.629497E+01,1.597544E+01,1.566217E+01,1.535504E+01,1.505394E+01,1.475874E+01,1.446933E+01,
                             1.418560E+01,1.390743E+01,1.363471E+01,1.336734E+01,1.310522E+01,1.284823E+01,1.259629E+01,
                             1.234928E+01,1.210712E+01,1.186970E+01,1.163695E+01,1.140875E+01,1.118503E+01,1.096570E+01,
                             1.075067E+01,1.053986E+01,1.033318E+01,1.013055E+01,9.931897E+00,9.737138E+00,9.546199E+00,
                             9.359004E+00,9.175480E+00,8.995554E+00,8.819157E+00,8.646218E+00,8.476671E+00,8.310449E+00,
                             8.147486E+00,7.987719E+00,7.831085E+00,7.677522E+00,7.526970E+00,7.379371E+00,7.234666E+00,
                             7.092799E+00,6.953713E+00,6.817355E+00,6.683671E+00,6.552608E+00,6.424116E+00,6.298143E+00,
                             6.174640E+00,6.053559E+00,5.934852E+00,5.818474E+00,5.704377E+00,5.592517E+00,5.482852E+00,
                             5.375336E+00,5.269929E+00,5.166589E+00,5.065275E+00,4.965948E+00,4.868569E+00,4.773100E+00,
                             4.679502E+00,4.587740E+00,4.497777E+00,4.409578E+00,4.323109E+00,4.238336E+00,4.155225E+00,
                             4.073743E+00,3.993859E+00,3.915542E+00,3.838761E+00,3.763485E+00,3.689686E+00,3.617333E+00,
                             3.546399E+00,3.476857E+00,3.408678E+00,3.341835E+00,3.276304E+00,3.212058E+00,3.149071E+00,
                             3.087320E+00,3.026779E+00,2.967426E+00,2.909237E+00,2.852188E+00,2.796259E+00,2.741426E+00,
                             2.687668E+00,2.634965E+00,2.583295E+00,2.532638E+00,2.482974E+00,2.434285E+00,2.386550E+00,
                             2.339751E+00,2.293870E+00,2.248889E+00,2.204789E+00,2.161555E+00,2.119168E+00,2.077612E+00,
                             2.036872E+00,1.996930E+00,1.957771E+00,1.919380E+00,1.881743E+00,1.844843E+00,1.808667E+00,
                             1.773200E+00,1.738428E+00,1.704339E+00,1.670918E+00,1.638152E+00,1.606029E+00,1.574536E+00,
                             1.543660E+00,1.513390E+00,1.483713E+00,1.454618E+00,1.426094E+00,1.398129E+00,1.370713E+00,
                             1.343834E+00,1.317482E+00,1.291647E+00,1.266319E+00,1.241487E+00,1.217142E+00,1.193275E+00,
                             1.169876E+00,1.146935E+00,1.124444E+00,1.102395E+00,1.080777E+00,1.059584E+00,1.038806E+00,
                             1.018436E+00,9.984649E-01,9.788856E-01,9.596902E-01,9.408713E-01,9.224214E-01,9.043333E-01,
                             8.865998E-01,8.692142E-01,8.521694E-01,8.354589E-01,8.190760E-01,8.030145E-01,7.872678E-01,
                             7.718300E-01,7.566949E-01,7.418565E-01,7.273092E-01,7.130471E-01,6.990647E-01,6.853565E-01,
                             6.719170E-01,6.587411E-01,6.458236E-01,6.331594E-01,6.207436E-01,6.085712E-01,5.966374E-01,
                             5.849378E-01,5.734675E-01,5.622221E-01,5.511973E-01,5.403887E-01,5.297920E-01,5.194031E-01,
                             5.092179E-01,4.992324E-01,4.894428E-01,4.798451E-01,4.704356E-01,4.612107E-01,4.521666E-01,
                             4.432999E-01,4.346071E-01,4.260847E-01,4.177294E-01,4.095380E-01,4.015072E-01,3.936339E-01,
                             3.859150E-01,3.783474E-01,3.709283E-01,3.636546E-01,3.565236E-01,3.495323E-01,3.426782E-01,
                             3.359585E-01,3.293706E-01],
                             [1.687500E+02,1.654409E+02,1.621967E+02,1.590161E+02,1.558979E+02,1.528409E+02,1.498438E+02,
                              3.156554E+02,3.094656E+02,3.033972E+02,2.974477E+02,2.916150E+02,2.858966E+02,2.802903E+02,
                              4.435440E+02,4.348464E+02,4.263193E+02,4.179594E+02,4.097635E+02,4.017283E+02,3.938506E+02,
                              5.548775E+02,5.439967E+02,5.333292E+02,5.228710E+02,5.126178E+02,5.025657E+02,4.927107E+02,
                              6.517989E+02,6.390175E+02,6.264868E+02,6.142018E+02,6.021576E+02,5.903497E+02,5.787733E+02,
                              7.361739E+02,7.217380E+02,7.075851E+02,6.937098E+02,6.801066E+02,6.667701E+02,6.536952E+02,
                              8.096266E+02,7.937503E+02,7.781854E+02,7.629256E+02,7.479651E+02,7.332980E+02,7.189184E+02,
                              7.048209E+02,6.909998E+02,6.774497E+02,6.641653E+02,6.511414E+02,6.383730E+02,6.258549E+02,
                              6.135822E+02,6.015503E+02,5.897542E+02,5.781895E+02,5.668516E+02,5.557359E+02,5.448383E+02,
                              5.341544E+02,5.236799E+02,5.134109E+02,5.033432E+02,4.934729E+02,4.837962E+02,4.743093E+02,
                              4.650084E+02,4.558898E+02,4.469501E+02,4.381857E+02,4.295931E+02,4.211691E+02,4.129102E+02,
                              4.048133E+02,3.968752E+02,3.890927E+02,3.814628E+02,3.739826E+02,3.666490E+02,3.594592E+02,
                              3.524104E+02,3.454999E+02,3.387249E+02,3.320827E+02,3.255707E+02,3.191865E+02,3.129274E+02,
                              3.067911E+02,3.007751E+02,2.948771E+02,2.890947E+02,2.834258E+02,2.778680E+02,2.724191E+02,
                              2.670772E+02,2.618400E+02,2.567054E+02,2.516716E+02,2.467365E+02,2.418981E+02,2.371546E+02,
                              2.325042E+02,2.279449E+02,2.234751E+02,2.190929E+02,2.147966E+02,2.105845E+02,2.064551E+02,
                              2.024067E+02,1.984376E+02,1.945463E+02,1.907314E+02,1.869913E+02,1.833245E+02,1.797296E+02,
                              1.762052E+02,1.727499E+02,1.693624E+02,1.660413E+02,1.627854E+02,1.595932E+02,1.564637E+02,
                              1.533956E+02,1.503876E+02,1.474386E+02,1.445474E+02,1.417129E+02,1.389340E+02,1.362096E+02,
                              1.335386E+02,1.309200E+02,1.283527E+02,1.258358E+02,1.233682E+02,1.209491E+02,1.185773E+02,
                              1.162521E+02,1.139725E+02,1.117375E+02,1.095464E+02,1.073983E+02,1.052923E+02,1.032276E+02,
                              1.012033E+02,9.921879E+01,9.727317E+01,9.536570E+01,9.349564E+01,9.166225E+01,8.986481E+01,
                              8.810261E+01,8.637497E+01,8.468121E+01,8.302067E+01,8.139268E+01,7.979662E+01,7.823186E+01,
                              7.669778E+01,7.519378E+01,7.371928E+01,7.227369E+01,7.085644E+01,6.946699E+01,6.810479E+01,
                              6.676929E+01,6.545999E+01,6.417636E+01,6.291790E+01,6.168412E+01,6.047453E+01,5.928866E+01,
                              5.812605E+01,5.698623E+01,5.586876E+01,5.477321E+01,5.369914E+01,5.264614E+01,5.161378E+01,
                              5.060166E+01,4.960939E+01,4.863658E+01,4.768285E+01,4.674782E+01,4.583112E+01,4.493240E+01,
                              4.405131E+01,4.318749E+01,4.234061E+01,4.151033E+01,4.069634E+01,3.989831E+01,3.911593E+01,
                              3.834889E+01,3.759689E+01,3.685964E+01,3.613684E+01,3.542822E+01,3.473350E+01,3.405239E+01,
                              3.338465E+01,3.272999E+01,3.208818E+01,3.145895E+01,3.084206E+01,3.023726E+01,2.964433E+01,
                              2.906302E+01,2.849312E+01,2.793438E+01,2.738661E+01,2.684957E+01,2.632307E+01,2.580689E+01,
                              2.530083E+01,2.480470E+01,2.431829E+01,2.384143E+01,2.337391E+01,2.291556E+01,2.246620E+01,
                              2.202565E+01,2.159374E+01,2.117030E+01,2.075517E+01,2.034817E+01,1.994916E+01,1.955796E+01,
                              1.917444E+01,1.879845E+01,1.842982E+01,1.806842E+01,1.771411E+01,1.736675E+01,1.702620E+01,
                              1.669232E+01,1.636500E+01,1.604409E+01,1.572947E+01,1.542103E+01,1.511863E+01,1.482217E+01,
                              1.453151E+01,1.424656E+01,1.396719E+01,1.369330E+01,1.342479E+01,1.316153E+01,1.290344E+01,
                              1.265042E+01,1.240235E+01,1.215915E+01,1.192071E+01,1.168695E+01,1.145778E+01,1.123310E+01,
                              1.101283E+01,1.079687E+01,1.058515E+01,1.037758E+01,1.017409E+01,9.974578E+00,9.778982E+00,
                              9.587222E+00,9.399223E+00,9.214910E+00,9.034211E+00,8.857056E+00,8.683374E+00,8.513098E+00,
                              8.346162E+00,8.182499E+00,8.022045E+00,7.864737E+00,7.710515E+00,7.559316E+00,7.411083E+00,
                              7.265756E+00,7.123279E+00,6.983596E+00,6.846652E+00,6.712393E+00,6.580767E+00,6.451722E+00,
                              6.325208E+00,6.201174E+00,6.079573E+00,5.960356E+00,5.843477E+00,5.728890E+00,5.616550E+00,
                              5.506413E+00,5.398436E+00,5.292576E+00,5.188792E+00,5.087043E+00,4.987289E+00,4.889491E+00,
                              4.793611E+00,4.699611E+00,4.607455E+00,4.517105E+00,4.428528E+00,4.341687E+00,4.256549E+00,
                              4.173081E+00,4.091249E+00,4.011022E+00,3.932369E+00,3.855257E+00,3.779658E+00,3.705541E+00,
                              3.632878E+00,3.561639E+00,3.491798E+00,3.423326E+00,3.356196E+00,3.290383E+00,3.225861E+00,
                              3.162604E+00,3.100587E+00,3.039787E+00,2.980178E+00,2.921739E+00,2.864445E+00,2.808275E+00,
                              2.753207E+00,2.699218E+00,2.646288E+00,2.594396E+00,2.543521E+00,2.493644E+00,2.444746E+00,
                              2.396806E+00,2.349806E+00,2.303727E+00,2.258553E+00,2.214264E+00,2.170844E+00,2.128275E+00,
                              2.086540E+00,2.045625E+00,2.005511E+00,1.966184E+00,1.927629E+00,1.889829E+00,1.852771E+00,
                              1.816439E+00,1.780820E+00,1.745899E+00,1.711663E+00,1.678098E+00,1.645192E+00,1.612931E+00,
                              1.581302E+00,1.550294E+00,1.519893E+00,1.490089E+00,1.460869E+00,1.432223E+00,1.404138E+00,
                              1.376603E+00,1.349609E+00]], dtype='float')

            for i in range(3):
                result[i] = ted_empty.daily_plant_dew_timeseries(i, blp_conc[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_soil_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil
        :param i; simulation number/index
        :param pore_h2o_conc; daily values of pesticide concentration in soil pore water

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([[]], dtype='float')
        expected_results = [[3.521818E+00,3.285972E+00,3.065920E+00,2.860605E+00,2.669039E+00,2.490301E+00,2.323533E+00,
                             5.689751E+00,5.308725E+00,4.953216E+00,4.621514E+00,4.312025E+00,4.023261E+00,3.753835E+00,
                             7.024270E+00,6.553876E+00,6.114982E+00,5.705480E+00,5.323401E+00,4.966909E+00,4.634290E+00,
                             7.845763E+00,7.320356E+00,6.830133E+00,6.372740E+00,5.945976E+00,5.547792E+00,5.176273E+00,
                             8.351451E+00,7.792179E+00,7.270360E+00,6.783486E+00,6.329216E+00,5.905368E+00,5.509903E+00,
                             8.662739E+00,8.082621E+00,7.541352E+00,7.036330E+00,6.565128E+00,6.125481E+00,5.715276E+00,
                             8.854359E+00,8.261409E+00,7.708167E+00,7.191974E+00,6.710349E+00,6.260977E+00,5.841698E+00,
                             5.450497E+00,5.085494E+00,4.744933E+00,4.427179E+00,4.130704E+00,3.854083E+00,3.595987E+00,
                             3.355175E+00,3.130489E+00,2.920849E+00,2.725249E+00,2.542747E+00,2.372467E+00,2.213590E+00,
                             2.065352E+00,1.927042E+00,1.797994E+00,1.677587E+00,1.565244E+00,1.460425E+00,1.362624E+00,
                             1.271373E+00,1.186233E+00,1.106795E+00,1.032676E+00,9.635209E-01,8.989968E-01,8.387936E-01,
                             7.826221E-01,7.302123E-01,6.813121E-01,6.356867E-01,5.931167E-01,5.533974E-01,5.163381E-01,
                             4.817604E-01,4.494984E-01,4.193968E-01,3.913111E-01,3.651061E-01,3.406561E-01,3.178434E-01,
                             2.965583E-01,2.766987E-01,2.581690E-01,2.408802E-01,2.247492E-01,2.096984E-01,1.956555E-01,
                             1.825531E-01,1.703280E-01,1.589217E-01,1.482792E-01,1.383494E-01,1.290845E-01,1.204401E-01,
                             1.123746E-01,1.048492E-01,9.782777E-02,9.127653E-02,8.516402E-02,7.946084E-02,7.413958E-02,
                             6.917468E-02,6.454226E-02,6.022005E-02,5.618730E-02,5.242460E-02,4.891388E-02,4.563827E-02,
                             4.258201E-02,3.973042E-02,3.706979E-02,3.458734E-02,3.227113E-02,3.011003E-02,2.809365E-02,
                             2.621230E-02,2.445694E-02,2.281913E-02,2.129100E-02,1.986521E-02,1.853490E-02,1.729367E-02,
                             1.613556E-02,1.505501E-02,1.404682E-02,1.310615E-02,1.222847E-02,1.140957E-02,1.064550E-02,
                             9.932605E-03,9.267448E-03,8.646835E-03,8.067782E-03,7.527507E-03,7.023412E-03,6.553075E-03,
                             6.114235E-03,5.704783E-03,5.322751E-03,4.966302E-03,4.633724E-03,4.323417E-03,4.033891E-03,
                             3.763753E-03,3.511706E-03,3.276538E-03,3.057118E-03,2.852392E-03,2.661376E-03,2.483151E-03,
                             2.316862E-03,2.161709E-03,2.016946E-03,1.881877E-03,1.755853E-03,1.638269E-03,1.528559E-03,
                             1.426196E-03,1.330688E-03,1.241576E-03,1.158431E-03,1.080854E-03,1.008473E-03,9.409384E-04,
                             8.779265E-04,8.191344E-04,7.642794E-04,7.130979E-04,6.653439E-04,6.207878E-04,5.792155E-04,
                             5.404272E-04,5.042364E-04,4.704692E-04,4.389633E-04,4.095672E-04,3.821397E-04,3.565490E-04,
                             3.326719E-04,3.103939E-04,2.896077E-04,2.702136E-04,2.521182E-04,2.352346E-04,2.194816E-04,
                             2.047836E-04,1.910699E-04,1.782745E-04,1.663360E-04,1.551970E-04,1.448039E-04,1.351068E-04,
                             1.260591E-04,1.176173E-04,1.097408E-04,1.023918E-04,9.553493E-05,8.913724E-05,8.316799E-05,
                             7.759848E-05,7.240194E-05,6.755340E-05,6.302955E-05,5.880865E-05,5.487041E-05,5.119590E-05,
                             4.776746E-05,4.456862E-05,4.158399E-05,3.879924E-05,3.620097E-05,3.377670E-05,3.151477E-05,
                             2.940432E-05,2.743520E-05,2.559795E-05,2.388373E-05,2.228431E-05,2.079200E-05,1.939962E-05,
                             1.810048E-05,1.688835E-05,1.575739E-05,1.470216E-05,1.371760E-05,1.279898E-05,1.194187E-05,
                             1.114216E-05,1.039600E-05,9.699809E-06,9.050242E-06,8.444175E-06,7.878693E-06,7.351081E-06,
                             6.858801E-06,6.399488E-06,5.970933E-06,5.571078E-06,5.197999E-06,4.849905E-06,4.525121E-06,
                             4.222087E-06,3.939347E-06,3.675540E-06,3.429400E-06,3.199744E-06,2.985467E-06,2.785539E-06,
                             2.599000E-06,2.424952E-06,2.262561E-06,2.111044E-06,1.969673E-06,1.837770E-06,1.714700E-06,
                             1.599872E-06,1.492733E-06,1.392769E-06,1.299500E-06,1.212476E-06,1.131280E-06,1.055522E-06,
                             9.848367E-07,9.188851E-07,8.573501E-07,7.999360E-07,7.463666E-07,6.963847E-07,6.497499E-07,
                             6.062381E-07,5.656401E-07,5.277609E-07,4.924183E-07,4.594426E-07,4.286751E-07,3.999680E-07,
                             3.731833E-07,3.481923E-07,3.248749E-07,3.031190E-07,2.828201E-07,2.638805E-07,2.462092E-07,
                             2.297213E-07,2.143375E-07,1.999840E-07,1.865917E-07,1.740962E-07,1.624375E-07,1.515595E-07,
                             1.414100E-07,1.319402E-07,1.231046E-07,1.148606E-07,1.071688E-07,9.999199E-08,9.329583E-08,
                             8.704809E-08,8.121874E-08,7.577976E-08,7.070502E-08,6.597011E-08,6.155229E-08,5.743032E-08,
                             5.358438E-08,4.999600E-08,4.664791E-08,4.352404E-08,4.060937E-08,3.788988E-08,3.535251E-08,
                             3.298506E-08,3.077615E-08,2.871516E-08,2.679219E-08,2.499800E-08,2.332396E-08,2.176202E-08,
                             2.030468E-08,1.894494E-08,1.767625E-08,1.649253E-08,1.538807E-08,1.435758E-08,1.339610E-08,
                             1.249900E-08,1.166198E-08,1.088101E-08,1.015234E-08,9.472470E-09,8.838127E-09,8.246264E-09,
                             7.694037E-09,7.178790E-09,6.698048E-09,6.249500E-09,5.830989E-09,5.440505E-09,5.076171E-09,
                             4.736235E-09,4.419064E-09,4.123132E-09,3.847018E-09,3.589395E-09,3.349024E-09,3.124750E-09,
                             2.915495E-09,2.720253E-09,2.538086E-09,2.368118E-09,2.209532E-09,2.061566E-09,1.923509E-09,
                             1.794697E-09,1.674512E-09],
                             [3.544172E+00,3.306830E+00,3.085381E+00,2.878762E+00,2.685980E+00,2.506108E+00,2.338282E+00,
                             5.725866E+00,5.342422E+00,4.984656E+00,4.650848E+00,4.339395E+00,4.048799E+00,3.777663E+00,
                             7.068856E+00,6.595476E+00,6.153797E+00,5.741695E+00,5.357191E+00,4.998436E+00,4.663706E+00,
                             7.895563E+00,7.366821E+00,6.873487E+00,6.413190E+00,5.983718E+00,5.583006E+00,5.209129E+00,
                             8.404462E+00,7.841640E+00,7.316509E+00,6.826544E+00,6.369391E+00,5.942852E+00,5.544877E+00,
                             8.717725E+00,8.133925E+00,7.589220E+00,7.080993E+00,6.606800E+00,6.164363E+00,5.751554E+00,
                             8.910561E+00,8.313848E+00,7.757094E+00,7.237625E+00,6.752943E+00,6.300718E+00,5.878778E+00,
                             5.485094E+00,5.117774E+00,4.775052E+00,4.455281E+00,4.156924E+00,3.878547E+00,3.618812E+00,
                             3.376471E+00,3.150359E+00,2.939389E+00,2.742547E+00,2.558887E+00,2.387526E+00,2.227640E+00,
                             2.078462E+00,1.939274E+00,1.809406E+00,1.688236E+00,1.575180E+00,1.469695E+00,1.371273E+00,
                             1.279443E+00,1.193763E+00,1.113820E+00,1.039231E+00,9.696368E-01,9.047031E-01,8.441178E-01,
                             7.875898E-01,7.348473E-01,6.856367E-01,6.397217E-01,5.968815E-01,5.569101E-01,5.196155E-01,
                             4.848184E-01,4.523516E-01,4.220589E-01,3.937949E-01,3.674236E-01,3.428184E-01,3.198608E-01,
                             2.984407E-01,2.784550E-01,2.598077E-01,2.424092E-01,2.261758E-01,2.110295E-01,1.968974E-01,
                             1.837118E-01,1.714092E-01,1.599304E-01,1.492204E-01,1.392275E-01,1.299039E-01,1.212046E-01,
                             1.130879E-01,1.055147E-01,9.844872E-02,9.185591E-02,8.570459E-02,7.996521E-02,7.461018E-02,
                             6.961376E-02,6.495194E-02,6.060230E-02,5.654394E-02,5.275737E-02,4.922436E-02,4.592795E-02,
                             4.285230E-02,3.998261E-02,3.730509E-02,3.480688E-02,3.247597E-02,3.030115E-02,2.827197E-02,
                             2.637868E-02,2.461218E-02,2.296398E-02,2.142615E-02,1.999130E-02,1.865255E-02,1.740344E-02,
                             1.623798E-02,1.515057E-02,1.413599E-02,1.318934E-02,1.230609E-02,1.148199E-02,1.071307E-02,
                             9.995652E-03,9.326273E-03,8.701720E-03,8.118992E-03,7.575287E-03,7.067993E-03,6.594671E-03,
                             6.153045E-03,5.740994E-03,5.356537E-03,4.997826E-03,4.663136E-03,4.350860E-03,4.059496E-03,
                             3.787644E-03,3.533997E-03,3.297335E-03,3.076523E-03,2.870497E-03,2.678269E-03,2.498913E-03,
                             2.331568E-03,2.175430E-03,2.029748E-03,1.893822E-03,1.766998E-03,1.648668E-03,1.538261E-03,
                             1.435249E-03,1.339134E-03,1.249456E-03,1.165784E-03,1.087715E-03,1.014874E-03,9.469109E-04,
                             8.834991E-04,8.243338E-04,7.691307E-04,7.176243E-04,6.695671E-04,6.247282E-04,5.828920E-04,
                             5.438575E-04,5.074370E-04,4.734555E-04,4.417496E-04,4.121669E-04,3.845653E-04,3.588121E-04,
                             3.347836E-04,3.123641E-04,2.914460E-04,2.719288E-04,2.537185E-04,2.367277E-04,2.208748E-04,
                             2.060835E-04,1.922827E-04,1.794061E-04,1.673918E-04,1.561821E-04,1.457230E-04,1.359644E-04,
                             1.268592E-04,1.183639E-04,1.104374E-04,1.030417E-04,9.614133E-05,8.970304E-05,8.369589E-05,
                             7.809103E-05,7.286151E-05,6.798219E-05,6.342962E-05,5.918193E-05,5.521870E-05,5.152086E-05,
                             4.807067E-05,4.485152E-05,4.184795E-05,3.904551E-05,3.643075E-05,3.399109E-05,3.171481E-05,
                             2.959097E-05,2.760935E-05,2.576043E-05,2.403533E-05,2.242576E-05,2.092397E-05,1.952276E-05,
                             1.821538E-05,1.699555E-05,1.585741E-05,1.479548E-05,1.380467E-05,1.288022E-05,1.201767E-05,
                             1.121288E-05,1.046199E-05,9.761378E-06,9.107688E-06,8.497774E-06,7.928703E-06,7.397742E-06,
                             6.902337E-06,6.440108E-06,6.008833E-06,5.606440E-06,5.230993E-06,4.880689E-06,4.553844E-06,
                             4.248887E-06,3.964352E-06,3.698871E-06,3.451168E-06,3.220054E-06,3.004417E-06,2.803220E-06,
                             2.615497E-06,2.440345E-06,2.276922E-06,2.124443E-06,1.982176E-06,1.849435E-06,1.725584E-06,
                             1.610027E-06,1.502208E-06,1.401610E-06,1.307748E-06,1.220172E-06,1.138461E-06,1.062222E-06,
                             9.910879E-07,9.247177E-07,8.627921E-07,8.050135E-07,7.511042E-07,7.008050E-07,6.538742E-07,
                             6.100862E-07,5.692305E-07,5.311108E-07,4.955439E-07,4.623588E-07,4.313961E-07,4.025068E-07,
                             3.755521E-07,3.504025E-07,3.269371E-07,3.050431E-07,2.846153E-07,2.655554E-07,2.477720E-07,
                             2.311794E-07,2.156980E-07,2.012534E-07,1.877760E-07,1.752012E-07,1.634685E-07,1.525215E-07,
                             1.423076E-07,1.327777E-07,1.238860E-07,1.155897E-07,1.078490E-07,1.006267E-07,9.388802E-08,
                             8.760062E-08,8.173427E-08,7.626077E-08,7.115381E-08,6.638886E-08,6.194299E-08,5.779486E-08,
                             5.392451E-08,5.031334E-08,4.694401E-08,4.380031E-08,4.086713E-08,3.813038E-08,3.557691E-08,
                             3.319443E-08,3.097150E-08,2.889743E-08,2.696225E-08,2.515667E-08,2.347201E-08,2.190016E-08,
                             2.043357E-08,1.906519E-08,1.778845E-08,1.659721E-08,1.548575E-08,1.444871E-08,1.348113E-08,
                             1.257834E-08,1.173600E-08,1.095008E-08,1.021678E-08,9.532596E-09,8.894227E-09,8.298607E-09,
                             7.742874E-09,7.224357E-09,6.740563E-09,6.289168E-09,5.868001E-09,5.475039E-09,5.108392E-09,
                             4.766298E-09,4.447113E-09,4.149303E-09,3.871437E-09,3.612178E-09,3.370282E-09,3.144584E-09,
                             2.934001E-09,2.737519E-09,2.554196E-09,2.383149E-09,2.223557E-09,2.074652E-09,1.935719E-09,
                             1.806089E-09,1.685141E-09],
                             [3.555456E+00,3.317358E+00,3.095204E+00,2.887928E+00,2.694532E+00,2.514087E+00,2.345726E+00,
                             5.744096E+00,5.359431E+00,5.000526E+00,4.665656E+00,4.353211E+00,4.061689E+00,3.789690E+00,
                             7.091362E+00,6.616475E+00,6.173389E+00,5.759976E+00,5.374248E+00,5.014350E+00,4.678554E+00,
                             7.920702E+00,7.390276E+00,6.895371E+00,6.433609E+00,6.002769E+00,5.600782E+00,5.225714E+00,
                             8.431220E+00,7.866606E+00,7.339803E+00,6.848279E+00,6.389670E+00,5.961773E+00,5.562531E+00,
                             8.745481E+00,8.159822E+00,7.613383E+00,7.103538E+00,6.627835E+00,6.183989E+00,5.769866E+00,
                             8.938931E+00,8.340318E+00,7.781792E+00,7.260668E+00,6.774443E+00,6.320779E+00,5.897495E+00,
                             5.502558E+00,5.134068E+00,4.790255E+00,4.469466E+00,4.170159E+00,3.890896E+00,3.630334E+00,
                             3.387221E+00,3.160389E+00,2.948748E+00,2.751279E+00,2.567034E+00,2.395127E+00,2.234733E+00,
                             2.085079E+00,1.945448E+00,1.815167E+00,1.693611E+00,1.580195E+00,1.474374E+00,1.375639E+00,
                             1.283517E+00,1.197564E+00,1.117366E+00,1.042540E+00,9.727239E-01,9.075835E-01,8.468054E-01,
                             7.900974E-01,7.371869E-01,6.878197E-01,6.417585E-01,5.987818E-01,5.586832E-01,5.212699E-01,
                             4.863620E-01,4.537918E-01,4.234027E-01,3.950487E-01,3.685934E-01,3.439098E-01,3.208792E-01,
                             2.993909E-01,2.793416E-01,2.606349E-01,2.431810E-01,2.268959E-01,2.117013E-01,1.975243E-01,
                             1.842967E-01,1.719549E-01,1.604396E-01,1.496955E-01,1.396708E-01,1.303175E-01,1.215905E-01,
                             1.134479E-01,1.058507E-01,9.876217E-02,9.214836E-02,8.597746E-02,8.021981E-02,7.484773E-02,
                             6.983540E-02,6.515873E-02,6.079525E-02,5.672397E-02,5.292534E-02,4.938108E-02,4.607418E-02,
                             4.298873E-02,4.010990E-02,3.742386E-02,3.491770E-02,3.257937E-02,3.039762E-02,2.836199E-02,
                             2.646267E-02,2.469054E-02,2.303709E-02,2.149437E-02,2.005495E-02,1.871193E-02,1.745885E-02,
                             1.628968E-02,1.519881E-02,1.418099E-02,1.323133E-02,1.234527E-02,1.151855E-02,1.074718E-02,
                             1.002748E-02,9.355966E-03,8.729425E-03,8.144841E-03,7.599406E-03,7.090496E-03,6.615667E-03,
                             6.172636E-03,5.759273E-03,5.373591E-03,5.013738E-03,4.677983E-03,4.364712E-03,4.072421E-03,
                             3.799703E-03,3.545248E-03,3.307833E-03,3.086318E-03,2.879636E-03,2.686796E-03,2.506869E-03,
                             2.338991E-03,2.182356E-03,2.036210E-03,1.899851E-03,1.772624E-03,1.653917E-03,1.543159E-03,
                             1.439818E-03,1.343398E-03,1.253435E-03,1.169496E-03,1.091178E-03,1.018105E-03,9.499257E-04,
                             8.863120E-04,8.269584E-04,7.715794E-04,7.199091E-04,6.716989E-04,6.267173E-04,5.847479E-04,
                             5.455891E-04,5.090526E-04,4.749629E-04,4.431560E-04,4.134792E-04,3.857897E-04,3.599545E-04,
                             3.358495E-04,3.133586E-04,2.923739E-04,2.727945E-04,2.545263E-04,2.374814E-04,2.215780E-04,
                             2.067396E-04,1.928949E-04,1.799773E-04,1.679247E-04,1.566793E-04,1.461870E-04,1.363973E-04,
                             1.272631E-04,1.187407E-04,1.107890E-04,1.033698E-04,9.644743E-05,8.998863E-05,8.396236E-05,
                             7.833966E-05,7.309348E-05,6.819863E-05,6.363157E-05,5.937036E-05,5.539450E-05,5.168490E-05,
                             4.822372E-05,4.499432E-05,4.198118E-05,3.916983E-05,3.654674E-05,3.409932E-05,3.181579E-05,
                             2.968518E-05,2.769725E-05,2.584245E-05,2.411186E-05,2.249716E-05,2.099059E-05,1.958491E-05,
                             1.827337E-05,1.704966E-05,1.590789E-05,1.484259E-05,1.384863E-05,1.292122E-05,1.205593E-05,
                             1.124858E-05,1.049530E-05,9.792457E-06,9.136686E-06,8.524829E-06,7.953947E-06,7.421295E-06,
                             6.924313E-06,6.460612E-06,6.027964E-06,5.624290E-06,5.247648E-06,4.896229E-06,4.568343E-06,
                             4.262415E-06,3.976973E-06,3.710647E-06,3.462156E-06,3.230306E-06,3.013982E-06,2.812145E-06,
                             2.623824E-06,2.448114E-06,2.284171E-06,2.131207E-06,1.988487E-06,1.855324E-06,1.731078E-06,
                             1.615153E-06,1.506991E-06,1.406072E-06,1.311912E-06,1.224057E-06,1.142086E-06,1.065604E-06,
                             9.942433E-07,9.276618E-07,8.655391E-07,8.075765E-07,7.534956E-07,7.030362E-07,6.559560E-07,
                             6.120286E-07,5.710428E-07,5.328018E-07,4.971217E-07,4.638309E-07,4.327695E-07,4.037883E-07,
                             3.767478E-07,3.515181E-07,3.279780E-07,3.060143E-07,2.855214E-07,2.664009E-07,2.485608E-07,
                             2.319155E-07,2.163848E-07,2.018941E-07,1.883739E-07,1.757591E-07,1.639890E-07,1.530071E-07,
                             1.427607E-07,1.332005E-07,1.242804E-07,1.159577E-07,1.081924E-07,1.009471E-07,9.418694E-08,
                             8.787953E-08,8.199450E-08,7.650357E-08,7.138036E-08,6.660023E-08,6.214021E-08,5.797886E-08,
                             5.409619E-08,5.047353E-08,4.709347E-08,4.393976E-08,4.099725E-08,3.825179E-08,3.569018E-08,
                             3.330011E-08,3.107010E-08,2.898943E-08,2.704810E-08,2.523677E-08,2.354674E-08,2.196988E-08,
                             2.049862E-08,1.912589E-08,1.784509E-08,1.665006E-08,1.553505E-08,1.449472E-08,1.352405E-08,
                             1.261838E-08,1.177337E-08,1.098494E-08,1.024931E-08,9.562946E-09,8.922544E-09,8.325028E-09,
                             7.767526E-09,7.247358E-09,6.762024E-09,6.309192E-09,5.886684E-09,5.492470E-09,5.124656E-09,
                             4.781473E-09,4.461272E-09,4.162514E-09,3.883763E-09,3.623679E-09,3.381012E-09,3.154596E-09,
                             2.943342E-09,2.746235E-09,2.562328E-09,2.390737E-09,2.230636E-09,2.081257E-09,1.941882E-09,
                             1.811840E-09,1.690506E-09]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366
            ted_empty.soil_foc = 0.015

            # input variables that change per simulation
            ted_empty.koc = pd.Series([1000., 1500., 2000.], dtype='float')

            # internally calculated variables
            pore_h2o_conc  = pd.Series([[2.347878E-01,2.190648E-01,2.043947E-01,1.907070E-01,1.779359E-01,1.660201E-01,
                                         1.549022E-01,3.793167E-01,3.539150E-01,3.302144E-01,3.081009E-01,2.874683E-01,
                                         2.682174E-01,2.502557E-01,4.682847E-01,4.369250E-01,4.076655E-01,3.803653E-01,
                                         3.548934E-01,3.311273E-01,3.089527E-01,5.230509E-01,4.880237E-01,4.553422E-01,
                                         4.248493E-01,3.963984E-01,3.698528E-01,3.450849E-01,5.567634E-01,5.194786E-01,
                                         4.846907E-01,4.522324E-01,4.219478E-01,3.936912E-01,3.673269E-01,5.775159E-01,
                                         5.388414E-01,5.027568E-01,4.690887E-01,4.376752E-01,4.083654E-01,3.810184E-01,
                                         5.902906E-01,5.507606E-01,5.138778E-01,4.794649E-01,4.473566E-01,4.173985E-01,
                                         3.894465E-01,3.633665E-01,3.390329E-01,3.163289E-01,2.951453E-01,2.753803E-01,
                                         2.569389E-01,2.397325E-01,2.236783E-01,2.086992E-01,1.947233E-01,1.816832E-01,
                                         1.695165E-01,1.581644E-01,1.475726E-01,1.376901E-01,1.284694E-01,1.198662E-01,
                                         1.118392E-01,1.043496E-01,9.736164E-02,9.084162E-02,8.475823E-02,7.908222E-02,
                                         7.378632E-02,6.884507E-02,6.423472E-02,5.993312E-02,5.591958E-02,5.217481E-02,
                                         4.868082E-02,4.542081E-02,4.237911E-02,3.954111E-02,3.689316E-02,3.442254E-02,
                                         3.211736E-02,2.996656E-02,2.795979E-02,2.608740E-02,2.434041E-02,2.271040E-02,
                                         2.118956E-02,1.977056E-02,1.844658E-02,1.721127E-02,1.605868E-02,1.498328E-02,
                                         1.397989E-02,1.304370E-02,1.217020E-02,1.135520E-02,1.059478E-02,9.885278E-03,
                                         9.223290E-03,8.605634E-03,8.029341E-03,7.491640E-03,6.989947E-03,6.521851E-03,
                                         6.085102E-03,5.677601E-03,5.297389E-03,4.942639E-03,4.611645E-03,4.302817E-03,
                                         4.014670E-03,3.745820E-03,3.494973E-03,3.260926E-03,3.042551E-03,2.838801E-03,
                                         2.648695E-03,2.471319E-03,2.305823E-03,2.151409E-03,2.007335E-03,1.872910E-03,
                                         1.747487E-03,1.630463E-03,1.521276E-03,1.419400E-03,1.324347E-03,1.235660E-03,
                                         1.152911E-03,1.075704E-03,1.003668E-03,9.364550E-04,8.737434E-04,8.152314E-04,
                                         7.606378E-04,7.097001E-04,6.621737E-04,6.178299E-04,5.764556E-04,5.378521E-04,
                                         5.018338E-04,4.682275E-04,4.368717E-04,4.076157E-04,3.803189E-04,3.548501E-04,
                                         3.310868E-04,3.089149E-04,2.882278E-04,2.689261E-04,2.509169E-04,2.341137E-04,
                                         2.184358E-04,2.038078E-04,1.901594E-04,1.774250E-04,1.655434E-04,1.544575E-04,
                                         1.441139E-04,1.344630E-04,1.254584E-04,1.170569E-04,1.092179E-04,1.019039E-04,
                                         9.507972E-05,8.871252E-05,8.277171E-05,7.722873E-05,7.205696E-05,6.723152E-05,
                                         6.272922E-05,5.852844E-05,5.460896E-05,5.095196E-05,4.753986E-05,4.435626E-05,
                                         4.138585E-05,3.861437E-05,3.602848E-05,3.361576E-05,3.136461E-05,2.926422E-05,
                                         2.730448E-05,2.547598E-05,2.376993E-05,2.217813E-05,2.069293E-05,1.930718E-05,
                                         1.801424E-05,1.680788E-05,1.568231E-05,1.463211E-05,1.365224E-05,1.273799E-05,
                                         1.188497E-05,1.108906E-05,1.034646E-05,9.653592E-06,9.007119E-06,8.403940E-06,
                                         7.841153E-06,7.316054E-06,6.826120E-06,6.368995E-06,5.942483E-06,5.544532E-06,
                                         5.173232E-06,4.826796E-06,4.503560E-06,4.201970E-06,3.920576E-06,3.658027E-06,
                                         3.413060E-06,3.184498E-06,2.971241E-06,2.772266E-06,2.586616E-06,2.413398E-06,
                                         2.251780E-06,2.100985E-06,1.960288E-06,1.829014E-06,1.706530E-06,1.592249E-06,
                                         1.485621E-06,1.386133E-06,1.293308E-06,1.206699E-06,1.125890E-06,1.050492E-06,
                                         9.801441E-07,9.145068E-07,8.532650E-07,7.961244E-07,7.428103E-07,6.930666E-07,
                                         6.466540E-07,6.033495E-07,5.629450E-07,5.252462E-07,4.900721E-07,4.572534E-07,
                                         4.266325E-07,3.980622E-07,3.714052E-07,3.465333E-07,3.233270E-07,3.016747E-07,
                                         2.814725E-07,2.626231E-07,2.450360E-07,2.286267E-07,2.133163E-07,1.990311E-07,
                                         1.857026E-07,1.732666E-07,1.616635E-07,1.508374E-07,1.407362E-07,1.313116E-07,
                                         1.225180E-07,1.143133E-07,1.066581E-07,9.951555E-08,9.285129E-08,8.663332E-08,
                                         8.083174E-08,7.541868E-08,7.036812E-08,6.565578E-08,6.125901E-08,5.715667E-08,
                                         5.332906E-08,4.975778E-08,4.642565E-08,4.331666E-08,4.041587E-08,3.770934E-08,
                                         3.518406E-08,3.282789E-08,3.062950E-08,2.857834E-08,2.666453E-08,2.487889E-08,
                                         2.321282E-08,2.165833E-08,2.020794E-08,1.885467E-08,1.759203E-08,1.641394E-08,
                                         1.531475E-08,1.428917E-08,1.333227E-08,1.243944E-08,1.160641E-08,1.082916E-08,
                                         1.010397E-08,9.427336E-09,8.796015E-09,8.206972E-09,7.657376E-09,7.144584E-09,
                                         6.666133E-09,6.219722E-09,5.803206E-09,5.414582E-09,5.051984E-09,4.713668E-09,
                                         4.398008E-09,4.103486E-09,3.828688E-09,3.572292E-09,3.333066E-09,3.109861E-09,
                                         2.901603E-09,2.707291E-09,2.525992E-09,2.356834E-09,2.199004E-09,2.051743E-09,
                                         1.914344E-09,1.786146E-09,1.666533E-09,1.554930E-09,1.450801E-09,1.353646E-09,
                                         1.262996E-09,1.178417E-09,1.099502E-09,1.025872E-09,9.571720E-10,8.930730E-10,  
                                         8.332666E-10,7.774652E-10,7.254007E-10,6.768228E-10,6.314980E-10,5.892085E-10,
                                         5.497509E-10,5.129358E-10,4.785860E-10,4.465365E-10,4.166333E-10,3.887326E-10,
                                         3.627004E-10,3.384114E-10,3.157490E-10,2.946042E-10,2.748755E-10,2.564679E-10,
                                         2.392930E-10,2.232683E-10,2.083167E-10,1.943663E-10,1.813502E-10,1.692057E-10,
                                         1.578745E-10,1.473021E-10,1.374377E-10,1.282339E-10,1.196465E-10,1.116341E-10],
                                         [1.575188E-01,1.469702E-01,1.371280E-01,1.279450E-01,1.193769E-01,1.113826E-01,
                                          1.039236E-01,2.544829E-01,2.374410E-01,2.215403E-01,2.067044E-01,1.928620E-01,
                                          1.799466E-01,1.678961E-01,3.141714E-01,2.931323E-01,2.735021E-01,2.551865E-01,
                                          2.380974E-01,2.221527E-01,2.072758E-01,3.509139E-01,3.274143E-01,3.054883E-01,
                                          2.850307E-01,2.659430E-01,2.481336E-01,2.315169E-01,3.735316E-01,3.485173E-01,
                                          3.251782E-01,3.034020E-01,2.830840E-01,2.641267E-01,2.464390E-01,3.874544E-01,
                                          3.615078E-01,3.372987E-01,3.147108E-01,2.936356E-01,2.739717E-01,2.556246E-01,
                                          3.960250E-01,3.695043E-01,3.447597E-01,3.216722E-01,3.001308E-01,2.800319E-01,
                                          2.612790E-01,2.437820E-01,2.274566E-01,2.122245E-01,1.980125E-01,1.847522E-01,
                                          1.723799E-01,1.608361E-01,1.500654E-01,1.400160E-01,1.306395E-01,1.218910E-01,
                                          1.137283E-01,1.061123E-01,9.900624E-02,9.237609E-02,8.618994E-02,8.041805E-02,
                                          7.503270E-02,7.000798E-02,6.531976E-02,6.094549E-02,5.686415E-02,5.305613E-02,
                                          4.950312E-02,4.618804E-02,4.309497E-02,4.020903E-02,3.751635E-02,3.500399E-02,
                                          3.265988E-02,3.047274E-02,2.843208E-02,2.652806E-02,2.475156E-02,2.309402E-02,
                                          2.154748E-02,2.010451E-02,1.875817E-02,1.750200E-02,1.632994E-02,1.523637E-02,
                                          1.421604E-02,1.326403E-02,1.237578E-02,1.154701E-02,1.077374E-02,1.005226E-02,
                                          9.379087E-03,8.750998E-03,8.164970E-03,7.618186E-03,7.108019E-03,6.632016E-03,
                                          6.187890E-03,5.773505E-03,5.386871E-03,5.026128E-03,4.689544E-03,4.375499E-03,
                                          4.082485E-03,3.809093E-03,3.554009E-03,3.316008E-03,3.093945E-03,2.886753E-03,
                                          2.693435E-03,2.513064E-03,2.344772E-03,2.187749E-03,2.041242E-03,1.904547E-03,
                                          1.777005E-03,1.658004E-03,1.546972E-03,1.443376E-03,1.346718E-03,1.256532E-03,
                                          1.172386E-03,1.093875E-03,1.020621E-03,9.522733E-04,8.885024E-04,8.290020E-04,
                                          7.734862E-04,7.216882E-04,6.733589E-04,6.282660E-04,5.861929E-04,5.469374E-04,
                                          5.103106E-04,4.761366E-04,4.442512E-04,4.145010E-04,3.867431E-04,3.608441E-04,
                                          3.366794E-04,3.141330E-04,2.930965E-04,2.734687E-04,2.551553E-04,2.380683E-04,
                                          2.221256E-04,2.072505E-04,1.933716E-04,1.804220E-04,1.683397E-04,1.570665E-04,
                                          1.465482E-04,1.367343E-04,1.275777E-04,1.190342E-04,1.110628E-04,1.036253E-04,
                                          9.668578E-05,9.021102E-05,8.416986E-05,7.853326E-05,7.327412E-05,6.836717E-05,
                                          6.378883E-05,5.951708E-05,5.553140E-05,5.181263E-05,4.834289E-05,4.510551E-05,
                                          4.208493E-05,3.926663E-05,3.663706E-05,3.418358E-05,3.189441E-05,2.975854E-05,
                                          2.776570E-05,2.590631E-05,2.417144E-05,2.255276E-05,2.104246E-05,1.963331E-05,
                                          1.831853E-05,1.709179E-05,1.594721E-05,1.487927E-05,1.388285E-05,1.295316E-05,
                                          1.208572E-05,1.127638E-05,1.052123E-05,9.816657E-06,9.159265E-06,8.545896E-06,
                                          7.973603E-06,7.439635E-06,6.941425E-06,6.476578E-06,6.042861E-06,5.638189E-06,
                                          5.260616E-06,4.908328E-06,4.579632E-06,4.272948E-06,3.986802E-06,3.719817E-06,
                                          3.470712E-06,3.238289E-06,3.021431E-06,2.819094E-06,2.630308E-06,2.454164E-06,
                                          2.289816E-06,2.136474E-06,1.993401E-06,1.859909E-06,1.735356E-06,1.619145E-06,
                                          1.510715E-06,1.409547E-06,1.315154E-06,1.227082E-06,1.144908E-06,1.068237E-06,
                                          9.967004E-07,9.299543E-07,8.676781E-07,8.095723E-07,7.553576E-07,7.047736E-07,
                                          6.575770E-07,6.135411E-07,5.724540E-07,5.341185E-07,4.983502E-07,4.649772E-07,
                                          4.338390E-07,4.047861E-07,3.776788E-07,3.523868E-07,3.287885E-07,3.067705E-07,
                                          2.862270E-07,2.670593E-07,2.491751E-07,2.324886E-07,2.169195E-07,2.023931E-07,
                                          1.888394E-07,1.761934E-07,1.643943E-07,1.533853E-07,1.431135E-07,1.335296E-07,
                                          1.245875E-07,1.162443E-07,1.084598E-07,1.011965E-07,9.441971E-08,8.809670E-08,
                                          8.219713E-08,7.669263E-08,7.155676E-08,6.676481E-08,6.229377E-08,5.812215E-08,
                                          5.422988E-08,5.059827E-08,4.720985E-08,4.404835E-08,4.109856E-08,3.834632E-08,
                                          3.577838E-08,3.338241E-08,3.114689E-08,2.906107E-08,2.711494E-08,2.529913E-08,
                                          2.360493E-08,2.202418E-08,2.054928E-08,1.917316E-08,1.788919E-08,1.669120E-08,
                                          1.557344E-08,1.453054E-08,1.355747E-08,1.264957E-08,1.180246E-08,1.101209E-08,
                                          1.027464E-08,9.586579E-09,8.944595E-09,8.345602E-09,7.786722E-09,7.265268E-09,
                                          6.778735E-09,6.324783E-09,5.901232E-09,5.506044E-09,5.137321E-09,4.793290E-09,
                                          4.472297E-09,4.172801E-09,3.893361E-09,3.632634E-09,3.389368E-09,3.162392E-09,
                                          2.950616E-09,2.753022E-09,2.568660E-09,2.396645E-09,2.236149E-09,2.086400E-09,
                                          1.946680E-09,1.816317E-09,1.694684E-09,1.581196E-09,1.475308E-09,1.376511E-09,
                                          1.284330E-09,1.198322E-09,1.118074E-09,1.043200E-09,9.733402E-10,9.081585E-10,
                                          8.473419E-10,7.905979E-10,7.376540E-10,6.882555E-10,6.421651E-10,5.991612E-10,
                                          5.590372E-10,5.216001E-10,4.866701E-10,4.540793E-10,4.236709E-10,3.952990E-10,
                                          3.688270E-10,3.441277E-10,3.210825E-10,2.995806E-10,2.795186E-10,2.608001E-10,
                                          2.433351E-10,2.270396E-10,2.118355E-10,1.976495E-10,1.844135E-10,1.720639E-10,
                                          1.605413E-10,1.497903E-10,1.397593E-10,1.304000E-10,1.216675E-10,1.135198E-10,
                                          1.059177E-10,9.882474E-11,9.220674E-11,8.603193E-11,8.027063E-11,7.489515E-11],
                                          [1.185152E-01,1.105786E-01,1.031735E-01,9.626426E-02,8.981773E-02,8.380291E-02,
                                          7.819088E-02,1.914699E-01,1.786477E-01,1.666842E-01,1.555219E-01,1.451070E-01,
                                          1.353896E-01,1.263230E-01,2.363787E-01,2.205492E-01,2.057796E-01,1.919992E-01,
                                          1.791416E-01,1.671450E-01,1.559518E-01,2.640234E-01,2.463425E-01,2.298457E-01,
                                          2.144536E-01,2.000923E-01,1.866927E-01,1.741905E-01,2.810407E-01,2.622202E-01,
                                          2.446601E-01,2.282760E-01,2.129890E-01,1.987258E-01,1.854177E-01,2.915160E-01,
                                          2.719941E-01,2.537794E-01,2.367846E-01,2.209278E-01,2.061330E-01,1.923289E-01,
                                          2.979644E-01,2.780106E-01,2.593931E-01,2.420223E-01,2.258148E-01,2.106926E-01,
                                          1.965832E-01,1.834186E-01,1.711356E-01,1.596752E-01,1.489822E-01,1.390053E-01,
                                          1.296965E-01,1.210111E-01,1.129074E-01,1.053463E-01,9.829159E-02,9.170929E-02,
                                          8.556780E-02,7.983758E-02,7.449109E-02,6.950265E-02,6.484826E-02,6.050557E-02,
                                          5.645369E-02,5.267316E-02,4.914579E-02,4.585465E-02,4.278390E-02,3.991879E-02,
                                          3.724555E-02,3.475132E-02,3.242413E-02,3.025278E-02,2.822685E-02,2.633658E-02,
                                          2.457290E-02,2.292732E-02,2.139195E-02,1.995939E-02,1.862277E-02,1.737566E-02,
                                          1.621207E-02,1.512639E-02,1.411342E-02,1.316829E-02,1.228645E-02,1.146366E-02,
                                          1.069597E-02,9.979697E-03,9.311387E-03,8.687831E-03,8.106033E-03,7.563196E-03,
                                          7.056711E-03,6.584145E-03,6.143224E-03,5.731831E-03,5.347987E-03,4.989849E-03,
                                          4.655693E-03,4.343915E-03,4.053016E-03,3.781598E-03,3.528356E-03,3.292072E-03,
                                          3.071612E-03,2.865915E-03,2.673994E-03,2.494924E-03,2.327847E-03,2.171958E-03,
                                          2.026508E-03,1.890799E-03,1.764178E-03,1.646036E-03,1.535806E-03,1.432958E-03,
                                          1.336997E-03,1.247462E-03,1.163923E-03,1.085979E-03,1.013254E-03,9.453995E-04,
                                          8.820889E-04,8.230181E-04,7.679030E-04,7.164788E-04,6.684984E-04,6.237311E-04,
                                          5.819617E-04,5.429894E-04,5.066271E-04,4.726998E-04,4.410445E-04,4.115090E-04,
                                          3.839515E-04,3.582394E-04,3.342492E-04,3.118655E-04,2.909808E-04,2.714947E-04,
                                          2.533135E-04,2.363499E-04,2.205222E-04,2.057545E-04,1.919758E-04,1.791197E-04,
                                          1.671246E-04,1.559328E-04,1.454904E-04,1.357474E-04,1.266568E-04,1.181749E-04,
                                          1.102611E-04,1.028773E-04,9.598788E-05,8.955986E-05,8.356230E-05,7.796638E-05,
                                          7.274521E-05,6.787368E-05,6.332838E-05,5.908747E-05,5.513056E-05,5.143863E-05,
                                          4.799394E-05,4.477993E-05,4.178115E-05,3.898319E-05,3.637260E-05,3.393684E-05,
                                          3.166419E-05,2.954373E-05,2.756528E-05,2.571931E-05,2.399697E-05,2.238996E-05,
                                          2.089058E-05,1.949160E-05,1.818630E-05,1.696842E-05,1.583210E-05,1.477187E-05,
                                          1.378264E-05,1.285966E-05,1.199848E-05,1.119498E-05,1.044529E-05,9.745798E-06,
                                          9.093151E-06,8.484210E-06,7.916048E-06,7.385934E-06,6.891320E-06,6.429829E-06,
                                          5.999242E-06,5.597491E-06,5.222644E-06,4.872899E-06,4.546575E-06,4.242105E-06,
                                          3.958024E-06,3.692967E-06,3.445660E-06,3.214914E-06,2.999621E-06,2.798745E-06,
                                          2.611322E-06,2.436449E-06,2.273288E-06,2.121052E-06,1.979012E-06,1.846483E-06,
                                          1.722830E-06,1.607457E-06,1.499811E-06,1.399373E-06,1.305661E-06,1.218225E-06,
                                          1.136644E-06,1.060526E-06,9.895060E-07,9.232417E-07,8.614150E-07,8.037286E-07,
                                          7.499053E-07,6.996864E-07,6.528305E-07,6.091124E-07,5.683219E-07,5.302631E-07,
                                          4.947530E-07,4.616209E-07,4.307075E-07,4.018643E-07,3.749526E-07,3.498432E-07,
                                          3.264152E-07,3.045562E-07,2.841610E-07,2.651316E-07,2.473765E-07,2.308104E-07,
                                          2.153537E-07,2.009321E-07,1.874763E-07,1.749216E-07,1.632076E-07,1.522781E-07,
                                          1.420805E-07,1.325658E-07,1.236882E-07,1.154052E-07,1.076769E-07,1.004661E-07,
                                          9.373816E-08,8.746080E-08,8.160381E-08,7.613905E-08,7.104024E-08,6.628289E-08,
                                          6.184412E-08,5.770261E-08,5.383844E-08,5.023304E-08,4.686908E-08,4.373040E-08,
                                          4.080190E-08,3.806952E-08,3.552012E-08,3.314144E-08,3.092206E-08,2.885130E-08,
                                          2.691922E-08,2.511652E-08,2.343454E-08,2.186520E-08,2.040095E-08,1.903476E-08,
                                          1.776006E-08,1.657072E-08,1.546103E-08,1.442565E-08,1.345961E-08,1.255826E-08,
                                          1.171727E-08,1.093260E-08,1.020048E-08,9.517381E-09,8.880030E-09,8.285361E-09,
                                          7.730515E-09,7.212826E-09,6.729804E-09,6.279130E-09,5.858635E-09,5.466300E-09,
                                          5.100238E-09,4.758690E-09,4.440015E-09,4.142681E-09,3.865258E-09,3.606413E-09,
                                          3.364902E-09,3.139565E-09,2.929318E-09,2.733150E-09,2.550119E-09,2.379345E-09,
                                          2.220008E-09,2.071340E-09,1.932629E-09,1.803206E-09,1.682451E-09,1.569782E-09,
                                          1.464659E-09,1.366575E-09,1.275060E-09,1.189673E-09,1.110004E-09,1.035670E-09,
                                          9.663144E-10,9.016032E-10,8.412256E-10,7.848912E-10,7.323294E-10,6.832875E-10,
                                          6.375298E-10,5.948363E-10,5.550019E-10,5.178351E-10,4.831572E-10,4.508016E-10,
                                          4.206128E-10,3.924456E-10,3.661647E-10,3.416437E-10,3.187649E-10,2.974181E-10,
                                          2.775009E-10,2.589175E-10,2.415786E-10,2.254008E-10,2.103064E-10,1.962228E-10,
                                          1.830823E-10,1.708219E-10,1.593824E-10,1.487091E-10,1.387505E-10,1.294588E-10,
                                          1.207893E-10,1.127004E-10,1.051532E-10,9.811140E-11,9.154117E-11,8.541093E-11,
                                          7.969122E-11,7.435454E-11,6.937524E-11,6.472938E-11,6.039465E-11,5.635020E-11]], dtype='float')

            for i in range(3):
                result[i] = ted_empty.daily_soil_timeseries(i, pore_h2o_conc[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_soil_inv_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil invertebrates (earthworms)
        :param i; simulation number/index
        :param pore_h2o_conc; daily values of pesticide concentration in soil pore water

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               # this represents Eq 2 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([[]], dtype='float')
        expected_results = [[2.347878E+02,2.190648E+02,2.043947E+02,1.907070E+02,1.779359E+02,1.660201E+02,
                             1.549022E+02,3.793167E+02,3.539150E+02,3.302144E+02,3.081009E+02,2.874683E+02,
                             2.682174E+02,2.502557E+02,4.682847E+02,4.369250E+02,4.076655E+02,3.803653E+02,
                             3.548934E+02,3.311273E+02,3.089527E+02,5.230509E+02,4.880237E+02,4.553422E+02,
                             4.248493E+02,3.963984E+02,3.698528E+02,3.450849E+02,5.567634E+02,5.194786E+02,
                             4.846907E+02,4.522324E+02,4.219478E+02,3.936912E+02,3.673269E+02,5.775159E+02,
                             5.388414E+02,5.027568E+02,4.690887E+02,4.376752E+02,4.083654E+02,3.810184E+02,
                             5.902906E+02,5.507606E+02,5.138778E+02,4.794649E+02,4.473566E+02,4.173985E+02,
                             3.894465E+02,3.633665E+02,3.390329E+02,3.163289E+02,2.951453E+02,2.753803E+02,
                             2.569389E+02,2.397325E+02,2.236783E+02,2.086992E+02,1.947233E+02,1.816832E+02,
                             1.695165E+02,1.581644E+02,1.475726E+02,1.376901E+02,1.284694E+02,1.198662E+02,
                             1.118392E+02,1.043496E+02,9.736164E+01,9.084162E+01,8.475823E+01,7.908222E+01,
                             7.378632E+01,6.884507E+01,6.423472E+01,5.993312E+01,5.591958E+01,5.217481E+01,
                             4.868082E+01,4.542081E+01,4.237911E+01,3.954111E+01,3.689316E+01,3.442254E+01,
                             3.211736E+01,2.996656E+01,2.795979E+01,2.608740E+01,2.434041E+01,2.271040E+01,
                             2.118956E+01,1.977056E+01,1.844658E+01,1.721127E+01,1.605868E+01,1.498328E+01,
                             1.397989E+01,1.304370E+01,1.217020E+01,1.135520E+01,1.059478E+01,9.885278E+00,
                             9.223290E+00,8.605634E+00,8.029341E+00,7.491640E+00,6.989947E+00,6.521851E+00,
                             6.085102E+00,5.677601E+00,5.297389E+00,4.942639E+00,4.611645E+00,4.302817E+00,
                             4.014670E+00,3.745820E+00,3.494973E+00,3.260926E+00,3.042551E+00,2.838801E+00,
                             2.648695E+00,2.471319E+00,2.305823E+00,2.151409E+00,2.007335E+00,1.872910E+00,
                             1.747487E+00,1.630463E+00,1.521276E+00,1.419400E+00,1.324347E+00,1.235660E+00,
                             1.152911E+00,1.075704E+00,1.003668E+00,9.364550E-01,8.737434E-01,8.152314E-01,
                             7.606378E-01,7.097001E-01,6.621737E-01,6.178299E-01,5.764556E-01,5.378521E-01,
                             5.018338E-01,4.682275E-01,4.368717E-01,4.076157E-01,3.803189E-01,3.548501E-01,
                             3.310868E-01,3.089149E-01,2.882278E-01,2.689261E-01,2.509169E-01,2.341137E-01,
                             2.184358E-01,2.038078E-01,1.901594E-01,1.774250E-01,1.655434E-01,1.544575E-01,
                             1.441139E-01,1.344630E-01,1.254584E-01,1.170569E-01,1.092179E-01,1.019039E-01,
                             9.507972E-02,8.871252E-02,8.277171E-02,7.722873E-02,7.205696E-02,6.723152E-02,
                             6.272922E-02,5.852844E-02,5.460896E-02,5.095196E-02,4.753986E-02,4.435626E-02,
                             4.138585E-02,3.861437E-02,3.602848E-02,3.361576E-02,3.136461E-02,2.926422E-02,
                             2.730448E-02,2.547598E-02,2.376993E-02,2.217813E-02,2.069293E-02,1.930718E-02,
                             1.801424E-02,1.680788E-02,1.568231E-02,1.463211E-02,1.365224E-02,1.273799E-02,
                             1.188497E-02,1.108906E-02,1.034646E-02,9.653592E-03,9.007119E-03,8.403940E-03,
                             7.841153E-03,7.316054E-03,6.826120E-03,6.368995E-03,5.942483E-03,5.544532E-03,
                             5.173232E-03,4.826796E-03,4.503560E-03,4.201970E-03,3.920576E-03,3.658027E-03,
                             3.413060E-03,3.184498E-03,2.971241E-03,2.772266E-03,2.586616E-03,2.413398E-03,
                             2.251780E-03,2.100985E-03,1.960288E-03,1.829014E-03,1.706530E-03,1.592249E-03,
                             1.485621E-03,1.386133E-03,1.293308E-03,1.206699E-03,1.125890E-03,1.050492E-03,
                             9.801441E-04,9.145068E-04,8.532650E-04,7.961244E-04,7.428103E-04,6.930666E-04,
                             6.466540E-04,6.033495E-04,5.629450E-04,5.252462E-04,4.900721E-04,4.572534E-04,
                             4.266325E-04,3.980622E-04,3.714052E-04,3.465333E-04,3.233270E-04,3.016747E-04,
                             2.814725E-04,2.626231E-04,2.450360E-04,2.286267E-04,2.133163E-04,1.990311E-04,
                             1.857026E-04,1.732666E-04,1.616635E-04,1.508374E-04,1.407362E-04,1.313116E-04,
                             1.225180E-04,1.143133E-04,1.066581E-04,9.951555E-05,9.285129E-05,8.663332E-05,
                             8.083174E-05,7.541868E-05,7.036812E-05,6.565578E-05,6.125901E-05,5.715667E-05,
                             5.332906E-05,4.975778E-05,4.642565E-05,4.331666E-05,4.041587E-05,3.770934E-05,
                             3.518406E-05,3.282789E-05,3.062950E-05,2.857834E-05,2.666453E-05,2.487889E-05,
                             2.321282E-05,2.165833E-05,2.020794E-05,1.885467E-05,1.759203E-05,1.641394E-05,
                             1.531475E-05,1.428917E-05,1.333227E-05,1.243944E-05,1.160641E-05,1.082916E-05,
                             1.010397E-05,9.427336E-06,8.796015E-06,8.206972E-06,7.657376E-06,7.144584E-06,
                             6.666133E-06,6.219722E-06,5.803206E-06,5.414582E-06,5.051984E-06,4.713668E-06,
                             4.398008E-06,4.103486E-06,3.828688E-06,3.572292E-06,3.333066E-06,3.109861E-06,
                             2.901603E-06,2.707291E-06,2.525992E-06,2.356834E-06,2.199004E-06,2.051743E-06,
                             1.914344E-06,1.786146E-06,1.666533E-06,1.554930E-06,1.450801E-06,1.353646E-06,
                             1.262996E-06,1.178417E-06,1.099502E-06,1.025872E-06,9.571720E-07,8.930730E-07,
                             8.332666E-07,7.774652E-07,7.254007E-07,6.768228E-07,6.314980E-07,5.892085E-07,
                             5.497509E-07,5.129358E-07,4.785860E-07,4.465365E-07,4.166333E-07,3.887326E-07,
                             3.627004E-07,3.384114E-07,3.157490E-07,2.946042E-07,2.748755E-07,2.564679E-07,
                             2.392930E-07,2.232683E-07,2.083167E-07,1.943663E-07,1.813502E-07,1.692057E-07,
                             1.578745E-07,1.473021E-07,1.374377E-07,1.282339E-07,1.196465E-07,1.116341E-07],
                             [2.347878E+01,2.190648E+01,2.043947E+01,1.907070E+01,1.779359E+01,1.660201E+01,
                             1.549022E+01,3.793167E+01,3.539150E+01,3.302144E+01,3.081009E+01,2.874683E+01,
                             2.682174E+01,2.502557E+01,4.682847E+01,4.369250E+01,4.076655E+01,3.803653E+01,
                             3.548934E+01,3.311273E+01,3.089527E+01,5.230509E+01,4.880237E+01,4.553422E+01,
                             4.248493E+01,3.963984E+01,3.698528E+01,3.450849E+01,5.567634E+01,5.194786E+01,
                             4.846907E+01,4.522324E+01,4.219478E+01,3.936912E+01,3.673269E+01,5.775159E+01,
                             5.388414E+01,5.027568E+01,4.690887E+01,4.376752E+01,4.083654E+01,3.810184E+01,
                             5.902906E+01,5.507606E+01,5.138778E+01,4.794649E+01,4.473566E+01,4.173985E+01,
                             3.894465E+01,3.633665E+01,3.390329E+01,3.163289E+01,2.951453E+01,2.753803E+01,
                             2.569389E+01,2.397325E+01,2.236783E+01,2.086992E+01,1.947233E+01,1.816832E+01,
                             1.695165E+01,1.581644E+01,1.475726E+01,1.376901E+01,1.284694E+01,1.198662E+01,
                             1.118392E+01,1.043496E+01,9.736164E+00,9.084162E+00,8.475823E+00,7.908222E+00,
                             7.378632E+00,6.884507E+00,6.423472E+00,5.993312E+00,5.591958E+00,5.217481E+00,
                             4.868082E+00,4.542081E+00,4.237911E+00,3.954111E+00,3.689316E+00,3.442254E+00,
                             3.211736E+00,2.996656E+00,2.795979E+00,2.608740E+00,2.434041E+00,2.271040E+00,
                             2.118956E+00,1.977056E+00,1.844658E+00,1.721127E+00,1.605868E+00,1.498328E+00,
                             1.397989E+00,1.304370E+00,1.217020E+00,1.135520E+00,1.059478E+00,9.885278E-01,
                             9.223290E-01,8.605634E-01,8.029341E-01,7.491640E-01,6.989947E-01,6.521851E-01,
                             6.085102E-01,5.677601E-01,5.297389E-01,4.942639E-01,4.611645E-01,4.302817E-01,
                             4.014670E-01,3.745820E-01,3.494973E-01,3.260926E-01,3.042551E-01,2.838801E-01,
                             2.648695E-01,2.471319E-01,2.305823E-01,2.151409E-01,2.007335E-01,1.872910E-01,
                             1.747487E-01,1.630463E-01,1.521276E-01,1.419400E-01,1.324347E-01,1.235660E-01,
                             1.152911E-01,1.075704E-01,1.003668E-01,9.364550E-02,8.737434E-02,8.152314E-02,
                             7.606378E-02,7.097001E-02,6.621737E-02,6.178299E-02,5.764556E-02,5.378521E-02,
                             5.018338E-02,4.682275E-02,4.368717E-02,4.076157E-02,3.803189E-02,3.548501E-02,
                             3.310868E-02,3.089149E-02,2.882278E-02,2.689261E-02,2.509169E-02,2.341137E-02,
                             2.184358E-02,2.038078E-02,1.901594E-02,1.774250E-02,1.655434E-02,1.544575E-02,
                             1.441139E-02,1.344630E-02,1.254584E-02,1.170569E-02,1.092179E-02,1.019039E-02,
                             9.507972E-03,8.871252E-03,8.277171E-03,7.722873E-03,7.205696E-03,6.723152E-03,
                             6.272922E-03,5.852844E-03,5.460896E-03,5.095196E-03,4.753986E-03,4.435626E-03,
                             4.138585E-03,3.861437E-03,3.602848E-03,3.361576E-03,3.136461E-03,2.926422E-03,
                             2.730448E-03,2.547598E-03,2.376993E-03,2.217813E-03,2.069293E-03,1.930718E-03,
                             1.801424E-03,1.680788E-03,1.568231E-03,1.463211E-03,1.365224E-03,1.273799E-03,
                             1.188497E-03,1.108906E-03,1.034646E-03,9.653592E-04,9.007119E-04,8.403940E-04,
                             7.841153E-04,7.316054E-04,6.826120E-04,6.368995E-04,5.942483E-04,5.544532E-04,
                             5.173232E-04,4.826796E-04,4.503560E-04,4.201970E-04,3.920576E-04,3.658027E-04,
                             3.413060E-04,3.184498E-04,2.971241E-04,2.772266E-04,2.586616E-04,2.413398E-04,
                             2.251780E-04,2.100985E-04,1.960288E-04,1.829014E-04,1.706530E-04,1.592249E-04,
                             1.485621E-04,1.386133E-04,1.293308E-04,1.206699E-04,1.125890E-04,1.050492E-04,
                             9.801441E-05,9.145068E-05,8.532650E-05,7.961244E-05,7.428103E-05,6.930666E-05,
                             6.466540E-05,6.033495E-05,5.629450E-05,5.252462E-05,4.900721E-05,4.572534E-05,
                             4.266325E-05,3.980622E-05,3.714052E-05,3.465333E-05,3.233270E-05,3.016747E-05,
                             2.814725E-05,2.626231E-05,2.450360E-05,2.286267E-05,2.133163E-05,1.990311E-05,
                             1.857026E-05,1.732666E-05,1.616635E-05,1.508374E-05,1.407362E-05,1.313116E-05,
                             1.225180E-05,1.143133E-05,1.066581E-05,9.951555E-06,9.285129E-06,8.663332E-06,
                             8.083174E-06,7.541868E-06,7.036812E-06,6.565578E-06,6.125901E-06,5.715667E-06,
                             5.332906E-06,4.975778E-06,4.642565E-06,4.331666E-06,4.041587E-06,3.770934E-06,
                             3.518406E-06,3.282789E-06,3.062950E-06,2.857834E-06,2.666453E-06,2.487889E-06,
                             2.321282E-06,2.165833E-06,2.020794E-06,1.885467E-06,1.759203E-06,1.641394E-06,
                             1.531475E-06,1.428917E-06,1.333227E-06,1.243944E-06,1.160641E-06,1.082916E-06,
                             1.010397E-06,9.427336E-07,8.796015E-07,8.206972E-07,7.657376E-07,7.144584E-07,
                             6.666133E-07,6.219722E-07,5.803206E-07,5.414582E-07,5.051984E-07,4.713668E-07,
                             4.398008E-07,4.103486E-07,3.828688E-07,3.572292E-07,3.333066E-07,3.109861E-07,
                             2.901603E-07,2.707291E-07,2.525992E-07,2.356834E-07,2.199004E-07,2.051743E-07,
                             1.914344E-07,1.786146E-07,1.666533E-07,1.554930E-07,1.450801E-07,1.353646E-07,
                             1.262996E-07,1.178417E-07,1.099502E-07,1.025872E-07,9.571720E-08,8.930730E-08,
                             8.332666E-08,7.774652E-08,7.254007E-08,6.768228E-08,6.314980E-08,5.892085E-08,
                             5.497509E-08,5.129358E-08,4.785860E-08,4.465365E-08,4.166333E-08,3.887326E-08,
                             3.627004E-08,3.384114E-08,3.157490E-08,2.946042E-08,2.748755E-08,2.564679E-08,
                             2.392930E-08,2.232683E-08,2.083167E-08,1.943663E-08,1.813502E-08,1.692057E-08,
                             1.578745E-08,1.473021E-08,1.374377E-08,1.282339E-08,1.196465E-08,1.116341E-08],
                             [6.664600E-01,6.218291E-01,5.801871E-01,5.413337E-01,5.050822E-01,4.712584E-01,
                             4.396996E-01,1.076714E+00,1.004610E+00,9.373342E-01,8.745637E-01,8.159968E-01,
                             7.613519E-01,7.103665E-01,1.329255E+00,1.240239E+00,1.157184E+00,1.079691E+00,
                             1.007387E+00,9.399255E-01,8.769815E-01,1.484713E+00,1.385286E+00,1.292517E+00,
                             1.205961E+00,1.125202E+00,1.049850E+00,9.795450E-01,1.580408E+00,1.474573E+00,
                             1.375825E+00,1.283690E+00,1.197725E+00,1.117517E+00,1.042680E+00,1.639315E+00,
                             1.529535E+00,1.427107E+00,1.331538E+00,1.242369E+00,1.159171E+00,1.081545E+00,
                             1.675577E+00,1.563368E+00,1.458674E+00,1.360991E+00,1.269850E+00,1.184812E+00,
                             1.105468E+00,1.031439E+00,9.623662E-01,8.979194E-01,8.377884E-01,7.816842E-01,
                             7.293372E-01,6.804956E-01,6.349249E-01,5.924059E-01,5.527342E-01,5.157193E-01,
                             4.811831E-01,4.489597E-01,4.188942E-01,3.908421E-01,3.646686E-01,3.402478E-01,
                             3.174624E-01,2.962029E-01,2.763671E-01,2.578596E-01,2.405915E-01,2.244798E-01,
                             2.094471E-01,1.954211E-01,1.823343E-01,1.701239E-01,1.587312E-01,1.481015E-01,
                             1.381836E-01,1.289298E-01,1.202958E-01,1.122399E-01,1.047235E-01,9.771053E-02,
                             9.116714E-02,8.506195E-02,7.936561E-02,7.405073E-02,6.909178E-02,6.446491E-02,
                             6.014788E-02,5.611996E-02,5.236177E-02,4.885526E-02,4.558357E-02,4.253098E-02,
                             3.968280E-02,3.702537E-02,3.454589E-02,3.223245E-02,3.007394E-02,2.805998E-02,
                             2.618089E-02,2.442763E-02,2.279179E-02,2.126549E-02,1.984140E-02,1.851268E-02,
                             1.727294E-02,1.611623E-02,1.503697E-02,1.402999E-02,1.309044E-02,1.221382E-02,
                             1.139589E-02,1.063274E-02,9.920701E-03,9.256341E-03,8.636472E-03,8.058113E-03,
                             7.518486E-03,7.014995E-03,6.545222E-03,6.106908E-03,5.697947E-03,5.316372E-03,
                             4.960351E-03,4.628171E-03,4.318236E-03,4.029057E-03,3.759243E-03,3.507498E-03,
                             3.272611E-03,3.053454E-03,2.848973E-03,2.658186E-03,2.480175E-03,2.314085E-03,
                             2.159118E-03,2.014528E-03,1.879621E-03,1.753749E-03,1.636305E-03,1.526727E-03,
                             1.424487E-03,1.329093E-03,1.240088E-03,1.157043E-03,1.079559E-03,1.007264E-03,
                             9.398107E-04,8.768744E-04,8.181527E-04,7.633635E-04,7.122433E-04,6.645465E-04,
                             6.200438E-04,5.785213E-04,5.397795E-04,5.036321E-04,4.699053E-04,4.384372E-04,
                             4.090764E-04,3.816817E-04,3.561217E-04,3.322733E-04,3.100219E-04,2.892607E-04,
                             2.698897E-04,2.518160E-04,2.349527E-04,2.192186E-04,2.045382E-04,1.908409E-04,
                             1.780608E-04,1.661366E-04,1.550110E-04,1.446303E-04,1.349449E-04,1.259080E-04,
                             1.174763E-04,1.096093E-04,1.022691E-04,9.542044E-05,8.903041E-05,8.306831E-05,
                             7.750548E-05,7.231517E-05,6.747244E-05,6.295401E-05,5.873817E-05,5.480465E-05,
                             5.113455E-05,4.771022E-05,4.451521E-05,4.153416E-05,3.875274E-05,3.615758E-05,
                             3.373622E-05,3.147701E-05,2.936908E-05,2.740232E-05,2.556727E-05,2.385511E-05,
                             2.225760E-05,2.076708E-05,1.937637E-05,1.807879E-05,1.686811E-05,1.573850E-05,
                             1.468454E-05,1.370116E-05,1.278364E-05,1.192755E-05,1.112880E-05,1.038354E-05,
                             9.688185E-06,9.039396E-06,8.434055E-06,7.869251E-06,7.342271E-06,6.850581E-06,
                             6.391818E-06,5.963777E-06,5.564401E-06,5.191770E-06,4.844092E-06,4.519698E-06,
                             4.217027E-06,3.934626E-06,3.671136E-06,3.425291E-06,3.195909E-06,2.981889E-06,
                             2.782200E-06,2.595885E-06,2.422046E-06,2.259849E-06,2.108514E-06,1.967313E-06,
                             1.835568E-06,1.712645E-06,1.597955E-06,1.490944E-06,1.391100E-06,1.297942E-06,
                             1.211023E-06,1.129924E-06,1.054257E-06,9.836564E-07,9.177839E-07,8.563226E-07,
                             7.989773E-07,7.454722E-07,6.955501E-07,6.489712E-07,6.055115E-07,5.649622E-07,
                             5.271284E-07,4.918282E-07,4.588919E-07,4.281613E-07,3.994886E-07,3.727361E-07,
                             3.477751E-07,3.244856E-07,3.027558E-07,2.824811E-07,2.635642E-07,2.459141E-07,
                             2.294460E-07,2.140807E-07,1.997443E-07,1.863680E-07,1.738875E-07,1.622428E-07,
                             1.513779E-07,1.412406E-07,1.317821E-07,1.229571E-07,1.147230E-07,1.070403E-07,
                             9.987216E-08,9.318402E-08,8.694376E-08,8.112140E-08,7.568894E-08,7.062028E-08,
                             6.589105E-08,6.147853E-08,5.736149E-08,5.352016E-08,4.993608E-08,4.659201E-08,
                             4.347188E-08,4.056070E-08,3.784447E-08,3.531014E-08,3.294553E-08,3.073926E-08,
                             2.868075E-08,2.676008E-08,2.496804E-08,2.329600E-08,2.173594E-08,2.028035E-08,
                             1.892224E-08,1.765507E-08,1.647276E-08,1.536963E-08,1.434037E-08,1.338004E-08,
                             1.248402E-08,1.164800E-08,1.086797E-08,1.014018E-08,9.461118E-09,8.827535E-09,
                             8.236382E-09,7.684816E-09,7.170187E-09,6.690021E-09,6.242010E-09,5.824001E-09,
                             5.433985E-09,5.070088E-09,4.730559E-09,4.413768E-09,4.118191E-09,3.842408E-09,
                             3.585093E-09,3.345010E-09,3.121005E-09,2.912001E-09,2.716993E-09,2.535044E-09,
                             2.365279E-09,2.206884E-09,2.059095E-09,1.921204E-09,1.792547E-09,1.672505E-09,
                             1.560502E-09,1.456000E-09,1.358496E-09,1.267522E-09,1.182640E-09,1.103442E-09,
                             1.029548E-09,9.606020E-10,8.962733E-10,8.362526E-10,7.802512E-10,7.280002E-10,
                             6.792482E-10,6.337609E-10,5.913199E-10,5.517209E-10,5.147738E-10,4.803010E-10,
                             4.481367E-10,4.181263E-10,3.901256E-10,3.640001E-10,3.396241E-10,3.168805E-10]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366
            ted_empty.lipid_earthworm = 0.01
            ted_empty.density_earthworm = 1.0

            # input variables that change per simulation
            ted_empty.log_kow = pd.Series([5.0, 4.0, 2.75], dtype='float')

            # internally calculated variables
            pore_h2o_conc  = pd.Series([[2.347878E-01,2.190648E-01,2.043947E-01,1.907070E-01,1.779359E-01,1.660201E-01,
                                         1.549022E-01,3.793167E-01,3.539150E-01,3.302144E-01,3.081009E-01,2.874683E-01,
                                         2.682174E-01,2.502557E-01,4.682847E-01,4.369250E-01,4.076655E-01,3.803653E-01,
                                         3.548934E-01,3.311273E-01,3.089527E-01,5.230509E-01,4.880237E-01,4.553422E-01,
                                         4.248493E-01,3.963984E-01,3.698528E-01,3.450849E-01,5.567634E-01,5.194786E-01,
                                         4.846907E-01,4.522324E-01,4.219478E-01,3.936912E-01,3.673269E-01,5.775159E-01,
                                         5.388414E-01,5.027568E-01,4.690887E-01,4.376752E-01,4.083654E-01,3.810184E-01,
                                         5.902906E-01,5.507606E-01,5.138778E-01,4.794649E-01,4.473566E-01,4.173985E-01,
                                         3.894465E-01,3.633665E-01,3.390329E-01,3.163289E-01,2.951453E-01,2.753803E-01,
                                         2.569389E-01,2.397325E-01,2.236783E-01,2.086992E-01,1.947233E-01,1.816832E-01,
                                         1.695165E-01,1.581644E-01,1.475726E-01,1.376901E-01,1.284694E-01,1.198662E-01,
                                         1.118392E-01,1.043496E-01,9.736164E-02,9.084162E-02,8.475823E-02,7.908222E-02,
                                         7.378632E-02,6.884507E-02,6.423472E-02,5.993312E-02,5.591958E-02,5.217481E-02,
                                         4.868082E-02,4.542081E-02,4.237911E-02,3.954111E-02,3.689316E-02,3.442254E-02,
                                         3.211736E-02,2.996656E-02,2.795979E-02,2.608740E-02,2.434041E-02,2.271040E-02,
                                         2.118956E-02,1.977056E-02,1.844658E-02,1.721127E-02,1.605868E-02,1.498328E-02,
                                         1.397989E-02,1.304370E-02,1.217020E-02,1.135520E-02,1.059478E-02,9.885278E-03,
                                         9.223290E-03,8.605634E-03,8.029341E-03,7.491640E-03,6.989947E-03,6.521851E-03,
                                         6.085102E-03,5.677601E-03,5.297389E-03,4.942639E-03,4.611645E-03,4.302817E-03,
                                         4.014670E-03,3.745820E-03,3.494973E-03,3.260926E-03,3.042551E-03,2.838801E-03,
                                         2.648695E-03,2.471319E-03,2.305823E-03,2.151409E-03,2.007335E-03,1.872910E-03,
                                         1.747487E-03,1.630463E-03,1.521276E-03,1.419400E-03,1.324347E-03,1.235660E-03,
                                         1.152911E-03,1.075704E-03,1.003668E-03,9.364550E-04,8.737434E-04,8.152314E-04,
                                         7.606378E-04,7.097001E-04,6.621737E-04,6.178299E-04,5.764556E-04,5.378521E-04,
                                         5.018338E-04,4.682275E-04,4.368717E-04,4.076157E-04,3.803189E-04,3.548501E-04,
                                         3.310868E-04,3.089149E-04,2.882278E-04,2.689261E-04,2.509169E-04,2.341137E-04,
                                         2.184358E-04,2.038078E-04,1.901594E-04,1.774250E-04,1.655434E-04,1.544575E-04,
                                         1.441139E-04,1.344630E-04,1.254584E-04,1.170569E-04,1.092179E-04,1.019039E-04,
                                         9.507972E-05,8.871252E-05,8.277171E-05,7.722873E-05,7.205696E-05,6.723152E-05,
                                         6.272922E-05,5.852844E-05,5.460896E-05,5.095196E-05,4.753986E-05,4.435626E-05,
                                         4.138585E-05,3.861437E-05,3.602848E-05,3.361576E-05,3.136461E-05,2.926422E-05,
                                         2.730448E-05,2.547598E-05,2.376993E-05,2.217813E-05,2.069293E-05,1.930718E-05,
                                         1.801424E-05,1.680788E-05,1.568231E-05,1.463211E-05,1.365224E-05,1.273799E-05,
                                         1.188497E-05,1.108906E-05,1.034646E-05,9.653592E-06,9.007119E-06,8.403940E-06,
                                         7.841153E-06,7.316054E-06,6.826120E-06,6.368995E-06,5.942483E-06,5.544532E-06,
                                         5.173232E-06,4.826796E-06,4.503560E-06,4.201970E-06,3.920576E-06,3.658027E-06,
                                         3.413060E-06,3.184498E-06,2.971241E-06,2.772266E-06,2.586616E-06,2.413398E-06,
                                         2.251780E-06,2.100985E-06,1.960288E-06,1.829014E-06,1.706530E-06,1.592249E-06,
                                         1.485621E-06,1.386133E-06,1.293308E-06,1.206699E-06,1.125890E-06,1.050492E-06,
                                         9.801441E-07,9.145068E-07,8.532650E-07,7.961244E-07,7.428103E-07,6.930666E-07,
                                         6.466540E-07,6.033495E-07,5.629450E-07,5.252462E-07,4.900721E-07,4.572534E-07,
                                         4.266325E-07,3.980622E-07,3.714052E-07,3.465333E-07,3.233270E-07,3.016747E-07,
                                         2.814725E-07,2.626231E-07,2.450360E-07,2.286267E-07,2.133163E-07,1.990311E-07,
                                         1.857026E-07,1.732666E-07,1.616635E-07,1.508374E-07,1.407362E-07,1.313116E-07,
                                         1.225180E-07,1.143133E-07,1.066581E-07,9.951555E-08,9.285129E-08,8.663332E-08,
                                         8.083174E-08,7.541868E-08,7.036812E-08,6.565578E-08,6.125901E-08,5.715667E-08,
                                         5.332906E-08,4.975778E-08,4.642565E-08,4.331666E-08,4.041587E-08,3.770934E-08,
                                         3.518406E-08,3.282789E-08,3.062950E-08,2.857834E-08,2.666453E-08,2.487889E-08,
                                         2.321282E-08,2.165833E-08,2.020794E-08,1.885467E-08,1.759203E-08,1.641394E-08,
                                         1.531475E-08,1.428917E-08,1.333227E-08,1.243944E-08,1.160641E-08,1.082916E-08,
                                         1.010397E-08,9.427336E-09,8.796015E-09,8.206972E-09,7.657376E-09,7.144584E-09,
                                         6.666133E-09,6.219722E-09,5.803206E-09,5.414582E-09,5.051984E-09,4.713668E-09,
                                         4.398008E-09,4.103486E-09,3.828688E-09,3.572292E-09,3.333066E-09,3.109861E-09,
                                         2.901603E-09,2.707291E-09,2.525992E-09,2.356834E-09,2.199004E-09,2.051743E-09,
                                         1.914344E-09,1.786146E-09,1.666533E-09,1.554930E-09,1.450801E-09,1.353646E-09,
                                         1.262996E-09,1.178417E-09,1.099502E-09,1.025872E-09,9.571720E-10,8.930730E-10,
                                         8.332666E-10,7.774652E-10,7.254007E-10,6.768228E-10,6.314980E-10,5.892085E-10,
                                         5.497509E-10,5.129358E-10,4.785860E-10,4.465365E-10,4.166333E-10,3.887326E-10,
                                         3.627004E-10,3.384114E-10,3.157490E-10,2.946042E-10,2.748755E-10,2.564679E-10,
                                         2.392930E-10,2.232683E-10,2.083167E-10,1.943663E-10,1.813502E-10,1.692057E-10,
                                         1.578745E-10,1.473021E-10,1.374377E-10,1.282339E-10,1.196465E-10,1.116341E-10],
                                         [2.347878E-01,2.190648E-01,2.043947E-01,1.907070E-01,1.779359E-01,1.660201E-01,
                                         1.549022E-01,3.793167E-01,3.539150E-01,3.302144E-01,3.081009E-01,2.874683E-01,
                                         2.682174E-01,2.502557E-01,4.682847E-01,4.369250E-01,4.076655E-01,3.803653E-01,
                                         3.548934E-01,3.311273E-01,3.089527E-01,5.230509E-01,4.880237E-01,4.553422E-01,
                                         4.248493E-01,3.963984E-01,3.698528E-01,3.450849E-01,5.567634E-01,5.194786E-01,
                                         4.846907E-01,4.522324E-01,4.219478E-01,3.936912E-01,3.673269E-01,5.775159E-01,
                                         5.388414E-01,5.027568E-01,4.690887E-01,4.376752E-01,4.083654E-01,3.810184E-01,
                                         5.902906E-01,5.507606E-01,5.138778E-01,4.794649E-01,4.473566E-01,4.173985E-01,
                                         3.894465E-01,3.633665E-01,3.390329E-01,3.163289E-01,2.951453E-01,2.753803E-01,
                                         2.569389E-01,2.397325E-01,2.236783E-01,2.086992E-01,1.947233E-01,1.816832E-01,
                                         1.695165E-01,1.581644E-01,1.475726E-01,1.376901E-01,1.284694E-01,1.198662E-01,
                                         1.118392E-01,1.043496E-01,9.736164E-02,9.084162E-02,8.475823E-02,7.908222E-02,
                                         7.378632E-02,6.884507E-02,6.423472E-02,5.993312E-02,5.591958E-02,5.217481E-02,
                                         4.868082E-02,4.542081E-02,4.237911E-02,3.954111E-02,3.689316E-02,3.442254E-02,
                                         3.211736E-02,2.996656E-02,2.795979E-02,2.608740E-02,2.434041E-02,2.271040E-02,
                                         2.118956E-02,1.977056E-02,1.844658E-02,1.721127E-02,1.605868E-02,1.498328E-02,
                                         1.397989E-02,1.304370E-02,1.217020E-02,1.135520E-02,1.059478E-02,9.885278E-03,
                                         9.223290E-03,8.605634E-03,8.029341E-03,7.491640E-03,6.989947E-03,6.521851E-03,
                                         6.085102E-03,5.677601E-03,5.297389E-03,4.942639E-03,4.611645E-03,4.302817E-03,
                                         4.014670E-03,3.745820E-03,3.494973E-03,3.260926E-03,3.042551E-03,2.838801E-03,
                                         2.648695E-03,2.471319E-03,2.305823E-03,2.151409E-03,2.007335E-03,1.872910E-03,
                                         1.747487E-03,1.630463E-03,1.521276E-03,1.419400E-03,1.324347E-03,1.235660E-03,
                                         1.152911E-03,1.075704E-03,1.003668E-03,9.364550E-04,8.737434E-04,8.152314E-04,
                                         7.606378E-04,7.097001E-04,6.621737E-04,6.178299E-04,5.764556E-04,5.378521E-04,
                                         5.018338E-04,4.682275E-04,4.368717E-04,4.076157E-04,3.803189E-04,3.548501E-04,
                                         3.310868E-04,3.089149E-04,2.882278E-04,2.689261E-04,2.509169E-04,2.341137E-04,
                                         2.184358E-04,2.038078E-04,1.901594E-04,1.774250E-04,1.655434E-04,1.544575E-04,
                                         1.441139E-04,1.344630E-04,1.254584E-04,1.170569E-04,1.092179E-04,1.019039E-04,
                                         9.507972E-05,8.871252E-05,8.277171E-05,7.722873E-05,7.205696E-05,6.723152E-05,
                                         6.272922E-05,5.852844E-05,5.460896E-05,5.095196E-05,4.753986E-05,4.435626E-05,
                                         4.138585E-05,3.861437E-05,3.602848E-05,3.361576E-05,3.136461E-05,2.926422E-05,
                                         2.730448E-05,2.547598E-05,2.376993E-05,2.217813E-05,2.069293E-05,1.930718E-05,
                                         1.801424E-05,1.680788E-05,1.568231E-05,1.463211E-05,1.365224E-05,1.273799E-05,
                                         1.188497E-05,1.108906E-05,1.034646E-05,9.653592E-06,9.007119E-06,8.403940E-06,
                                         7.841153E-06,7.316054E-06,6.826120E-06,6.368995E-06,5.942483E-06,5.544532E-06,
                                         5.173232E-06,4.826796E-06,4.503560E-06,4.201970E-06,3.920576E-06,3.658027E-06,
                                         3.413060E-06,3.184498E-06,2.971241E-06,2.772266E-06,2.586616E-06,2.413398E-06,
                                         2.251780E-06,2.100985E-06,1.960288E-06,1.829014E-06,1.706530E-06,1.592249E-06,
                                         1.485621E-06,1.386133E-06,1.293308E-06,1.206699E-06,1.125890E-06,1.050492E-06,
                                         9.801441E-07,9.145068E-07,8.532650E-07,7.961244E-07,7.428103E-07,6.930666E-07,
                                         6.466540E-07,6.033495E-07,5.629450E-07,5.252462E-07,4.900721E-07,4.572534E-07,
                                         4.266325E-07,3.980622E-07,3.714052E-07,3.465333E-07,3.233270E-07,3.016747E-07,
                                         2.814725E-07,2.626231E-07,2.450360E-07,2.286267E-07,2.133163E-07,1.990311E-07,
                                         1.857026E-07,1.732666E-07,1.616635E-07,1.508374E-07,1.407362E-07,1.313116E-07,
                                         1.225180E-07,1.143133E-07,1.066581E-07,9.951555E-08,9.285129E-08,8.663332E-08,
                                         8.083174E-08,7.541868E-08,7.036812E-08,6.565578E-08,6.125901E-08,5.715667E-08,
                                         5.332906E-08,4.975778E-08,4.642565E-08,4.331666E-08,4.041587E-08,3.770934E-08,
                                         3.518406E-08,3.282789E-08,3.062950E-08,2.857834E-08,2.666453E-08,2.487889E-08,
                                         2.321282E-08,2.165833E-08,2.020794E-08,1.885467E-08,1.759203E-08,1.641394E-08,
                                         1.531475E-08,1.428917E-08,1.333227E-08,1.243944E-08,1.160641E-08,1.082916E-08,
                                         1.010397E-08,9.427336E-09,8.796015E-09,8.206972E-09,7.657376E-09,7.144584E-09,
                                         6.666133E-09,6.219722E-09,5.803206E-09,5.414582E-09,5.051984E-09,4.713668E-09,
                                         4.398008E-09,4.103486E-09,3.828688E-09,3.572292E-09,3.333066E-09,3.109861E-09,
                                         2.901603E-09,2.707291E-09,2.525992E-09,2.356834E-09,2.199004E-09,2.051743E-09,
                                         1.914344E-09,1.786146E-09,1.666533E-09,1.554930E-09,1.450801E-09,1.353646E-09,
                                         1.262996E-09,1.178417E-09,1.099502E-09,1.025872E-09,9.571720E-10,8.930730E-10,
                                         8.332666E-10,7.774652E-10,7.254007E-10,6.768228E-10,6.314980E-10,5.892085E-10,
                                         5.497509E-10,5.129358E-10,4.785860E-10,4.465365E-10,4.166333E-10,3.887326E-10,
                                         3.627004E-10,3.384114E-10,3.157490E-10,2.946042E-10,2.748755E-10,2.564679E-10,
                                         2.392930E-10,2.232683E-10,2.083167E-10,1.943663E-10,1.813502E-10,1.692057E-10,
                                         1.578745E-10,1.473021E-10,1.374377E-10,1.282339E-10,1.196465E-10,1.116341E-10],
                                         [1.185152E-01,1.105786E-01,1.031735E-01,9.626426E-02,8.981773E-02,8.380291E-02,
                                          7.819088E-02,1.914699E-01,1.786477E-01,1.666842E-01,1.555219E-01,1.451070E-01,
                                          1.353896E-01,1.263230E-01,2.363787E-01,2.205492E-01,2.057796E-01,1.919992E-01,
                                          1.791416E-01,1.671450E-01,1.559518E-01,2.640234E-01,2.463425E-01,2.298457E-01,
                                          2.144536E-01,2.000923E-01,1.866927E-01,1.741905E-01,2.810407E-01,2.622202E-01,
                                          2.446601E-01,2.282760E-01,2.129890E-01,1.987258E-01,1.854177E-01,2.915160E-01,
                                          2.719941E-01,2.537794E-01,2.367846E-01,2.209278E-01,2.061330E-01,1.923289E-01,
                                          2.979644E-01,2.780106E-01,2.593931E-01,2.420223E-01,2.258148E-01,2.106926E-01,
                                          1.965832E-01,1.834186E-01,1.711356E-01,1.596752E-01,1.489822E-01,1.390053E-01,
                                          1.296965E-01,1.210111E-01,1.129074E-01,1.053463E-01,9.829159E-02,9.170929E-02,
                                          8.556780E-02,7.983758E-02,7.449109E-02,6.950265E-02,6.484826E-02,6.050557E-02,
                                          5.645369E-02,5.267316E-02,4.914579E-02,4.585465E-02,4.278390E-02,3.991879E-02,
                                          3.724555E-02,3.475132E-02,3.242413E-02,3.025278E-02,2.822685E-02,2.633658E-02,
                                          2.457290E-02,2.292732E-02,2.139195E-02,1.995939E-02,1.862277E-02,1.737566E-02,
                                          1.621207E-02,1.512639E-02,1.411342E-02,1.316829E-02,1.228645E-02,1.146366E-02,
                                          1.069597E-02,9.979697E-03,9.311387E-03,8.687831E-03,8.106033E-03,7.563196E-03,
                                          7.056711E-03,6.584145E-03,6.143224E-03,5.731831E-03,5.347987E-03,4.989849E-03,
                                          4.655693E-03,4.343915E-03,4.053016E-03,3.781598E-03,3.528356E-03,3.292072E-03,
                                          3.071612E-03,2.865915E-03,2.673994E-03,2.494924E-03,2.327847E-03,2.171958E-03,
                                          2.026508E-03,1.890799E-03,1.764178E-03,1.646036E-03,1.535806E-03,1.432958E-03,
                                          1.336997E-03,1.247462E-03,1.163923E-03,1.085979E-03,1.013254E-03,9.453995E-04,
                                          8.820889E-04,8.230181E-04,7.679030E-04,7.164788E-04,6.684984E-04,6.237311E-04,
                                          5.819617E-04,5.429894E-04,5.066271E-04,4.726998E-04,4.410445E-04,4.115090E-04,
                                          3.839515E-04,3.582394E-04,3.342492E-04,3.118655E-04,2.909808E-04,2.714947E-04,
                                          2.533135E-04,2.363499E-04,2.205222E-04,2.057545E-04,1.919758E-04,1.791197E-04,
                                          1.671246E-04,1.559328E-04,1.454904E-04,1.357474E-04,1.266568E-04,1.181749E-04,
                                          1.102611E-04,1.028773E-04,9.598788E-05,8.955986E-05,8.356230E-05,7.796638E-05,
                                          7.274521E-05,6.787368E-05,6.332838E-05,5.908747E-05,5.513056E-05,5.143863E-05,
                                          4.799394E-05,4.477993E-05,4.178115E-05,3.898319E-05,3.637260E-05,3.393684E-05,
                                          3.166419E-05,2.954373E-05,2.756528E-05,2.571931E-05,2.399697E-05,2.238996E-05,
                                          2.089058E-05,1.949160E-05,1.818630E-05,1.696842E-05,1.583210E-05,1.477187E-05,
                                          1.378264E-05,1.285966E-05,1.199848E-05,1.119498E-05,1.044529E-05,9.745798E-06,
                                          9.093151E-06,8.484210E-06,7.916048E-06,7.385934E-06,6.891320E-06,6.429829E-06,
                                          5.999242E-06,5.597491E-06,5.222644E-06,4.872899E-06,4.546575E-06,4.242105E-06,
                                          3.958024E-06,3.692967E-06,3.445660E-06,3.214914E-06,2.999621E-06,2.798745E-06,
                                          2.611322E-06,2.436449E-06,2.273288E-06,2.121052E-06,1.979012E-06,1.846483E-06,
                                          1.722830E-06,1.607457E-06,1.499811E-06,1.399373E-06,1.305661E-06,1.218225E-06,
                                          1.136644E-06,1.060526E-06,9.895060E-07,9.232417E-07,8.614150E-07,8.037286E-07,
                                          7.499053E-07,6.996864E-07,6.528305E-07,6.091124E-07,5.683219E-07,5.302631E-07,
                                          4.947530E-07,4.616209E-07,4.307075E-07,4.018643E-07,3.749526E-07,3.498432E-07,
                                          3.264152E-07,3.045562E-07,2.841610E-07,2.651316E-07,2.473765E-07,2.308104E-07,
                                          2.153537E-07,2.009321E-07,1.874763E-07,1.749216E-07,1.632076E-07,1.522781E-07,
                                          1.420805E-07,1.325658E-07,1.236882E-07,1.154052E-07,1.076769E-07,1.004661E-07,
                                          9.373816E-08,8.746080E-08,8.160381E-08,7.613905E-08,7.104024E-08,6.628289E-08,
                                          6.184412E-08,5.770261E-08,5.383844E-08,5.023304E-08,4.686908E-08,4.373040E-08,
                                          4.080190E-08,3.806952E-08,3.552012E-08,3.314144E-08,3.092206E-08,2.885130E-08,
                                          2.691922E-08,2.511652E-08,2.343454E-08,2.186520E-08,2.040095E-08,1.903476E-08,
                                          1.776006E-08,1.657072E-08,1.546103E-08,1.442565E-08,1.345961E-08,1.255826E-08,
                                          1.171727E-08,1.093260E-08,1.020048E-08,9.517381E-09,8.880030E-09,8.285361E-09,
                                          7.730515E-09,7.212826E-09,6.729804E-09,6.279130E-09,5.858635E-09,5.466300E-09,
                                          5.100238E-09,4.758690E-09,4.440015E-09,4.142681E-09,3.865258E-09,3.606413E-09,
                                          3.364902E-09,3.139565E-09,2.929318E-09,2.733150E-09,2.550119E-09,2.379345E-09,
                                          2.220008E-09,2.071340E-09,1.932629E-09,1.803206E-09,1.682451E-09,1.569782E-09,
                                          1.464659E-09,1.366575E-09,1.275060E-09,1.189673E-09,1.110004E-09,1.035670E-09,
                                          9.663144E-10,9.016032E-10,8.412256E-10,7.848912E-10,7.323294E-10,6.832875E-10,
                                          6.375298E-10,5.948363E-10,5.550019E-10,5.178351E-10,4.831572E-10,4.508016E-10,
                                          4.206128E-10,3.924456E-10,3.661647E-10,3.416437E-10,3.187649E-10,2.974181E-10,
                                          2.775009E-10,2.589175E-10,2.415786E-10,2.254008E-10,2.103064E-10,1.962228E-10,
                                          1.830823E-10,1.708219E-10,1.593824E-10,1.487091E-10,1.387505E-10,1.294588E-10,
                                          1.207893E-10,1.127004E-10,1.051532E-10,9.811140E-11,9.154117E-11,8.541093E-11,
                                          7.969122E-11,7.435454E-11,6.937524E-11,6.472938E-11,6.039465E-11,5.635020E-11]], dtype='float')

            for i in range(3):
                result[i] = ted_empty.daily_soil_inv_timeseries(i, pore_h2o_conc[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_animal_dose_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide concentrations in animals (mammals, birds, amphibians, reptiles)
        :param a1; coefficient of allometric expression
        :param b1; exponent of allometrice expression
        :param body_wgt; body weight of species (g)
        :param frac_h2o; fraction of water in food item
        :param intake_food_conc; pesticide concentration in food item (daily mg a.i./kg)
        :param frac_retained; fraction of ingested food retained by animal (mammals, birds, reptiles/amphibians)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               # this represents Eqs 5&6 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([[]], dtype='float')
        expected_results = [[2.860270E+02,3.090209E+02,3.058215E+02,3.001105E+02,2.942541E+02,2.884869E+02,2.828301E+02,
                             5.633110E+02,5.808675E+02,5.723374E+02,5.614002E+02,5.504201E+02,5.396295E+02,5.290480E+02,
                             8.047008E+02,8.175238E+02,8.043529E+02,7.888661E+02,7.734255E+02,7.582619E+02,7.433932E+02,
                             1.014843E+03,1.023545E+03,1.006334E+03,9.868866E+02,9.675630E+02,9.485925E+02,9.299915E+02,
                             1.197782E+03,1.202897E+03,1.182169E+03,1.159274E+03,1.136569E+03,1.114285E+03,1.092435E+03,
                             1.357040E+03,1.359032E+03,1.335242E+03,1.309345E+03,1.283698E+03,1.258528E+03,1.233850E+03,
                             1.495682E+03,1.494955E+03,1.468500E+03,1.439990E+03,1.411781E+03,1.384100E+03,1.356959E+03,
                             1.330350E+03,1.304262E+03,1.278687E+03,1.253612E+03,1.229030E+03,1.204929E+03,1.181301E+03,
                             1.158137E+03,1.135426E+03,1.113161E+03,1.091333E+03,1.069932E+03,1.048952E+03,1.028382E+03,
                             1.008217E+03,9.884460E+02,9.690632E+02,9.500604E+02,9.314303E+02,9.131655E+02,8.952589E+02,
                             8.777034E+02,8.604922E+02,8.436185E+02,8.270756E+02,8.108572E+02,7.949568E+02,7.793682E+02,
                             7.640852E+02,7.491020E+02,7.344125E+02,7.200112E+02,7.058922E+02,6.920501E+02,6.784794E+02,
                             6.651748E+02,6.521312E+02,6.393433E+02,6.268061E+02,6.145148E+02,6.024646E+02,5.906506E+02,
                             5.790683E+02,5.677131E+02,5.565806E+02,5.456664E+02,5.349662E+02,5.244759E+02,5.141912E+02,
                             5.041083E+02,4.942230E+02,4.845316E+02,4.750302E+02,4.657152E+02,4.565828E+02,4.476295E+02,
                             4.388517E+02,4.302461E+02,4.218092E+02,4.135378E+02,4.054286E+02,3.974784E+02,3.896841E+02,
                             3.820426E+02,3.745510E+02,3.672063E+02,3.600056E+02,3.529461E+02,3.460250E+02,3.392397E+02,
                             3.325874E+02,3.260656E+02,3.196716E+02,3.134031E+02,3.072574E+02,3.012323E+02,2.953253E+02,
                             2.895342E+02,2.838566E+02,2.782903E+02,2.728332E+02,2.674831E+02,2.622379E+02,2.570956E+02,
                             2.520541E+02,2.471115E+02,2.422658E+02,2.375151E+02,2.328576E+02,2.282914E+02,2.238147E+02,
                             2.194259E+02,2.151231E+02,2.109046E+02,2.067689E+02,2.027143E+02,1.987392E+02,1.948420E+02,
                             1.910213E+02,1.872755E+02,1.836031E+02,1.800028E+02,1.764730E+02,1.730125E+02,1.696198E+02,
                             1.662937E+02,1.630328E+02,1.598358E+02,1.567015E+02,1.536287E+02,1.506161E+02,1.476627E+02,
                             1.447671E+02,1.419283E+02,1.391452E+02,1.364166E+02,1.337416E+02,1.311190E+02,1.285478E+02,
                             1.260271E+02,1.235557E+02,1.211329E+02,1.187576E+02,1.164288E+02,1.141457E+02,1.119074E+02,
                             1.097129E+02,1.075615E+02,1.054523E+02,1.033845E+02,1.013571E+02,9.936960E+01,9.742102E+01,
                             9.551065E+01,9.363775E+01,9.180157E+01,9.000140E+01,8.823652E+01,8.650626E+01,8.480992E+01,
                             8.314685E+01,8.151639E+01,7.991791E+01,7.835077E+01,7.681436E+01,7.530807E+01,7.383133E+01,
                             7.238354E+01,7.096414E+01,6.957258E+01,6.820830E+01,6.687078E+01,6.555948E+01,6.427390E+01,
                             6.301353E+01,6.177787E+01,6.056645E+01,5.937878E+01,5.821440E+01,5.707285E+01,5.595368E+01,
                             5.485647E+01,5.378076E+01,5.272616E+01,5.169223E+01,5.067857E+01,4.968480E+01,4.871051E+01,
                             4.775533E+01,4.681887E+01,4.590078E+01,4.500070E+01,4.411826E+01,4.325313E+01,4.240496E+01,
                             4.157343E+01,4.075820E+01,3.995895E+01,3.917538E+01,3.840718E+01,3.765404E+01,3.691566E+01,
                             3.619177E+01,3.548207E+01,3.478629E+01,3.410415E+01,3.343539E+01,3.277974E+01,3.213695E+01,
                             3.150677E+01,3.088894E+01,3.028322E+01,2.968939E+01,2.910720E+01,2.853642E+01,2.797684E+01,
                             2.742823E+01,2.689038E+01,2.636308E+01,2.584611E+01,2.533929E+01,2.484240E+01,2.435526E+01,
                             2.387766E+01,2.340944E+01,2.295039E+01,2.250035E+01,2.205913E+01,2.162656E+01,2.120248E+01,
                             2.078671E+01,2.037910E+01,1.997948E+01,1.958769E+01,1.920359E+01,1.882702E+01,1.845783E+01,
                             1.809588E+01,1.774104E+01,1.739314E+01,1.705208E+01,1.671770E+01,1.638987E+01,1.606848E+01,
                             1.575338E+01,1.544447E+01,1.514161E+01,1.484469E+01,1.455360E+01,1.426821E+01,1.398842E+01,
                             1.371412E+01,1.344519E+01,1.318154E+01,1.292306E+01,1.266964E+01,1.242120E+01,1.217763E+01,
                             1.193883E+01,1.170472E+01,1.147520E+01,1.125017E+01,1.102957E+01,1.081328E+01,1.060124E+01,
                             1.039336E+01,1.018955E+01,9.989738E+00,9.793846E+00,9.601794E+00,9.413509E+00,9.228916E+00,
                             9.047942E+00,8.870518E+00,8.696572E+00,8.526038E+00,8.358848E+00,8.194936E+00,8.034238E+00,
                             7.876691E+00,7.722234E+00,7.570806E+00,7.422347E+00,7.276799E+00,7.134106E+00,6.994210E+00,
                             6.857058E+00,6.722595E+00,6.590769E+00,6.461528E+00,6.334822E+00,6.210600E+00,6.088814E+00,
                             5.969416E+00,5.852359E+00,5.737598E+00,5.625087E+00,5.514783E+00,5.406641E+00,5.300620E+00,
                             5.196678E+00,5.094775E+00,4.994869E+00,4.896923E+00,4.800897E+00,4.706755E+00,4.614458E+00,
                             4.523971E+00,4.435259E+00,4.348286E+00,4.263019E+00,4.179424E+00,4.097468E+00,4.017119E+00,
                             3.938346E+00,3.861117E+00,3.785403E+00,3.711174E+00,3.638400E+00,3.567053E+00,3.497105E+00,
                             3.428529E+00,3.361298E+00,3.295385E+00,3.230764E+00,3.167411E+00,3.105300E+00,3.044407E+00,
                             2.984708E+00,2.926180E+00,2.868799E+00,2.812544E+00,2.757391E+00,2.703321E+00,2.650310E+00,
                             2.598339E+00,2.547387E+00],
                             [4.583348E+01,4.951806E+01,4.900538E+01,4.809025E+01,4.715181E+01,4.622765E+01,4.532120E+01,
                              9.026597E+01,9.307926E+01,9.171236E+01,8.995977E+01,8.820030E+01,8.647120E+01,8.477560E+01,
                              1.289467E+02,1.310015E+02,1.288910E+02,1.264093E+02,1.239351E+02,1.215053E+02,1.191227E+02,
                              1.626202E+02,1.640147E+02,1.612568E+02,1.581405E+02,1.550440E+02,1.520042E+02,1.490235E+02,
                              1.919347E+02,1.927544E+02,1.894329E+02,1.857641E+02,1.821259E+02,1.785550E+02,1.750537E+02,
                              2.174545E+02,2.177737E+02,2.139616E+02,2.098118E+02,2.057021E+02,2.016689E+02,1.977143E+02,
                              2.396707E+02,2.395543E+02,2.353151E+02,2.307466E+02,2.262263E+02,2.217906E+02,2.174415E+02,
                              2.131776E+02,2.089973E+02,2.048990E+02,2.008811E+02,1.969419E+02,1.930800E+02,1.892938E+02,
                              1.855819E+02,1.819427E+02,1.783750E+02,1.748771E+02,1.714479E+02,1.680859E+02,1.647898E+02,
                              1.615584E+02,1.583904E+02,1.552844E+02,1.522394E+02,1.492541E+02,1.463273E+02,1.434579E+02,
                              1.406448E+02,1.378868E+02,1.351829E+02,1.325321E+02,1.299332E+02,1.273853E+02,1.248873E+02,
                              1.224384E+02,1.200374E+02,1.176836E+02,1.153759E+02,1.131134E+02,1.108953E+02,1.087208E+02,
                              1.065888E+02,1.044987E+02,1.024495E+02,1.004405E+02,9.847096E+01,9.654000E+01,9.464691E+01,
                              9.279094E+01,9.097137E+01,8.918748E+01,8.743857E+01,8.572395E+01,8.404295E+01,8.239492E+01,
                              8.077921E+01,7.919518E+01,7.764221E+01,7.611969E+01,7.462703E+01,7.316364E+01,7.172895E+01,
                              7.032239E+01,6.894341E+01,6.759147E+01,6.626604E+01,6.496660E+01,6.369265E+01,6.244367E+01,
                              6.121919E+01,6.001872E+01,5.884179E+01,5.768794E+01,5.655671E+01,5.544767E+01,5.436038E+01,
                              5.329440E+01,5.224933E+01,5.122475E+01,5.022027E+01,4.923548E+01,4.827000E+01,4.732346E+01,
                              4.639547E+01,4.548569E+01,4.459374E+01,4.371928E+01,4.286197E+01,4.202148E+01,4.119746E+01,
                              4.038960E+01,3.959759E+01,3.882110E+01,3.805985E+01,3.731352E+01,3.658182E+01,3.586447E+01,
                              3.516119E+01,3.447170E+01,3.379573E+01,3.313302E+01,3.248330E+01,3.184632E+01,3.122184E+01,
                              3.060960E+01,3.000936E+01,2.942090E+01,2.884397E+01,2.827836E+01,2.772384E+01,2.718019E+01,
                              2.664720E+01,2.612467E+01,2.561238E+01,2.511013E+01,2.461774E+01,2.413500E+01,2.366173E+01,
                              2.319774E+01,2.274284E+01,2.229687E+01,2.185964E+01,2.143099E+01,2.101074E+01,2.059873E+01,
                              2.019480E+01,1.979879E+01,1.941055E+01,1.902992E+01,1.865676E+01,1.829091E+01,1.793224E+01,
                              1.758060E+01,1.723585E+01,1.689787E+01,1.656651E+01,1.624165E+01,1.592316E+01,1.561092E+01,
                              1.530480E+01,1.500468E+01,1.471045E+01,1.442198E+01,1.413918E+01,1.386192E+01,1.359009E+01,
                              1.332360E+01,1.306233E+01,1.280619E+01,1.255507E+01,1.230887E+01,1.206750E+01,1.183086E+01,
                              1.159887E+01,1.137142E+01,1.114843E+01,1.092982E+01,1.071549E+01,1.050537E+01,1.029937E+01,
                              1.009740E+01,9.899397E+00,9.705276E+00,9.514962E+00,9.328379E+00,9.145455E+00,8.966118E+00,
                              8.790298E+00,8.617926E+00,8.448934E+00,8.283255E+00,8.120826E+00,7.961581E+00,7.805459E+00,
                              7.652399E+00,7.502340E+00,7.355224E+00,7.210992E+00,7.069589E+00,6.930959E+00,6.795047E+00,
                              6.661800E+00,6.531166E+00,6.403094E+00,6.277533E+00,6.154435E+00,6.033750E+00,5.915432E+00,
                              5.799434E+00,5.685711E+00,5.574217E+00,5.464910E+00,5.357747E+00,5.252685E+00,5.149683E+00,
                              5.048701E+00,4.949699E+00,4.852638E+00,4.757481E+00,4.664189E+00,4.572728E+00,4.483059E+00,
                              4.395149E+00,4.308963E+00,4.224467E+00,4.141628E+00,4.060413E+00,3.980791E+00,3.902730E+00,
                              3.826200E+00,3.751170E+00,3.677612E+00,3.605496E+00,3.534795E+00,3.465479E+00,3.397524E+00,
                              3.330900E+00,3.265583E+00,3.201547E+00,3.138767E+00,3.077217E+00,3.016875E+00,2.957716E+00,
                              2.899717E+00,2.842855E+00,2.787109E+00,2.732455E+00,2.678873E+00,2.626342E+00,2.574841E+00,
                              2.524350E+00,2.474849E+00,2.426319E+00,2.378740E+00,2.332095E+00,2.286364E+00,2.241530E+00,
                              2.197575E+00,2.154481E+00,2.112233E+00,2.070814E+00,2.030206E+00,1.990395E+00,1.951365E+00,
                              1.913100E+00,1.875585E+00,1.838806E+00,1.802748E+00,1.767397E+00,1.732740E+00,1.698762E+00,
                              1.665450E+00,1.632792E+00,1.600774E+00,1.569383E+00,1.538609E+00,1.508438E+00,1.478858E+00,
                              1.449859E+00,1.421428E+00,1.393554E+00,1.366228E+00,1.339437E+00,1.313171E+00,1.287421E+00,
                              1.262175E+00,1.237425E+00,1.213160E+00,1.189370E+00,1.166047E+00,1.143182E+00,1.120765E+00,
                              1.098787E+00,1.077241E+00,1.056117E+00,1.035407E+00,1.015103E+00,9.951976E-01,9.756824E-01,
                              9.565499E-01,9.377925E-01,9.194030E-01,9.013741E-01,8.836987E-01,8.663699E-01,8.493809E-01,
                              8.327250E-01,8.163958E-01,8.003868E-01,7.846917E-01,7.693044E-01,7.542188E-01,7.394290E-01,
                              7.249293E-01,7.107138E-01,6.967772E-01,6.831138E-01,6.697183E-01,6.565856E-01,6.437103E-01,
                              6.310876E-01,6.187123E-01,6.065798E-01,5.946851E-01,5.830237E-01,5.715909E-01,5.603824E-01,
                              5.493936E-01,5.386204E-01,5.280583E-01,5.177034E-01,5.075516E-01,4.975988E-01,4.878412E-01,
                              4.782749E-01,4.688963E-01,4.597015E-01,4.506870E-01,4.418493E-01,4.331849E-01,4.246904E-01,
                              4.163625E-01,4.081979E-01],
                              [1.338207E+02,1.378876E+02,1.355183E+02,1.328776E+02,1.302728E+02,1.277182E+02,1.252138E+02,
                               2.565791E+02,2.582388E+02,2.535095E+02,2.485550E+02,2.436818E+02,2.389034E+02,2.342187E+02,
                               3.634465E+02,3.630106E+02,3.562267E+02,3.492581E+02,3.424102E+02,3.356958E+02,3.291130E+02,
                               4.564800E+02,4.542198E+02,4.456473E+02,4.369252E+02,4.283582E+02,4.199584E+02,4.117233E+02,
                               5.374704E+02,5.336219E+02,5.234925E+02,5.132438E+02,5.031803E+02,4.933133E+02,4.836397E+02,
                               6.079765E+02,6.027455E+02,5.912606E+02,5.796831E+02,5.683167E+02,5.571724E+02,5.462466E+02,
                               6.693557E+02,6.629211E+02,6.502562E+02,6.375218E+02,6.250212E+02,6.127650E+02,6.007490E+02,
                               5.889687E+02,5.774194E+02,5.660965E+02,5.549957E+02,5.441126E+02,5.334429E+02,5.229824E+02,
                               5.127270E+02,5.026728E+02,4.928157E+02,4.831519E+02,4.736775E+02,4.643890E+02,4.552826E+02,
                               4.463548E+02,4.376021E+02,4.290210E+02,4.206081E+02,4.123602E+02,4.042741E+02,3.963465E+02,
                               3.885744E+02,3.809547E+02,3.734844E+02,3.661606E+02,3.589804E+02,3.519411E+02,3.450397E+02,
                               3.382737E+02,3.316404E+02,3.251371E+02,3.187613E+02,3.125106E+02,3.063825E+02,3.003745E+02,
                               2.944844E+02,2.887097E+02,2.830483E+02,2.774979E+02,2.720563E+02,2.667214E+02,2.614912E+02,
                               2.563635E+02,2.513364E+02,2.464078E+02,2.415759E+02,2.368388E+02,2.321945E+02,2.276413E+02,
                               2.231774E+02,2.188010E+02,2.145105E+02,2.103041E+02,2.061801E+02,2.021371E+02,1.981733E+02,
                               1.942872E+02,1.904774E+02,1.867422E+02,1.830803E+02,1.794902E+02,1.759705E+02,1.725199E+02,
                               1.691368E+02,1.658202E+02,1.625685E+02,1.593807E+02,1.562553E+02,1.531912E+02,1.501873E+02,
                               1.472422E+02,1.443548E+02,1.415241E+02,1.387489E+02,1.360282E+02,1.333607E+02,1.307456E+02,
                               1.281818E+02,1.256682E+02,1.232039E+02,1.207880E+02,1.184194E+02,1.160973E+02,1.138207E+02,
                               1.115887E+02,1.094005E+02,1.072552E+02,1.051520E+02,1.030901E+02,1.010685E+02,9.908664E+01,
                               9.714361E+01,9.523868E+01,9.337111E+01,9.154016E+01,8.974511E+01,8.798527E+01,8.625993E+01,
                               8.456842E+01,8.291009E+01,8.128427E+01,7.969034E+01,7.812766E+01,7.659562E+01,7.509363E+01,
                               7.362109E+01,7.217742E+01,7.076207E+01,6.937447E+01,6.801408E+01,6.668036E+01,6.537280E+01,
                               6.409088E+01,6.283410E+01,6.160196E+01,6.039398E+01,5.920969E+01,5.804863E+01,5.691033E+01,
                               5.579435E+01,5.470026E+01,5.362762E+01,5.257601E+01,5.154503E+01,5.053426E+01,4.954332E+01,
                               4.857180E+01,4.761934E+01,4.668555E+01,4.577008E+01,4.487256E+01,4.399263E+01,4.312996E+01,
                               4.228421E+01,4.145504E+01,4.064214E+01,3.984517E+01,3.906383E+01,3.829781E+01,3.754681E+01,
                               3.681054E+01,3.608871E+01,3.538103E+01,3.468723E+01,3.400704E+01,3.334018E+01,3.268640E+01,
                               3.204544E+01,3.141705E+01,3.080098E+01,3.019699E+01,2.960485E+01,2.902431E+01,2.845516E+01,
                               2.789718E+01,2.735013E+01,2.681381E+01,2.628801E+01,2.577252E+01,2.526713E+01,2.477166E+01,
                               2.428590E+01,2.380967E+01,2.334278E+01,2.288504E+01,2.243628E+01,2.199632E+01,2.156498E+01,
                               2.114211E+01,2.072752E+01,2.032107E+01,1.992258E+01,1.953191E+01,1.914891E+01,1.877341E+01,
                               1.840527E+01,1.804436E+01,1.769052E+01,1.734362E+01,1.700352E+01,1.667009E+01,1.634320E+01,
                               1.602272E+01,1.570852E+01,1.540049E+01,1.509850E+01,1.480242E+01,1.451216E+01,1.422758E+01,
                               1.394859E+01,1.367506E+01,1.340690E+01,1.314400E+01,1.288626E+01,1.263357E+01,1.238583E+01,
                               1.214295E+01,1.190484E+01,1.167139E+01,1.144252E+01,1.121814E+01,1.099816E+01,1.078249E+01,
                               1.057105E+01,1.036376E+01,1.016053E+01,9.961292E+00,9.765957E+00,9.574453E+00,9.386704E+00,
                               9.202636E+00,9.022178E+00,8.845259E+00,8.671808E+00,8.501760E+00,8.335045E+00,8.171600E+00,
                               8.011360E+00,7.854262E+00,7.700245E+00,7.549248E+00,7.401212E+00,7.256078E+00,7.113791E+00,
                               6.974294E+00,6.837532E+00,6.703452E+00,6.572002E+00,6.443129E+00,6.316783E+00,6.192915E+00,
                               6.071476E+00,5.952418E+00,5.835694E+00,5.721260E+00,5.609069E+00,5.499079E+00,5.391245E+00,
                               5.285526E+00,5.181880E+00,5.080267E+00,4.980646E+00,4.882979E+00,4.787226E+00,4.693352E+00,
                               4.601318E+00,4.511089E+00,4.422629E+00,4.335904E+00,4.250880E+00,4.167523E+00,4.085800E+00,
                               4.005680E+00,3.927131E+00,3.850122E+00,3.774624E+00,3.700606E+00,3.628039E+00,3.556896E+00,
                               3.487147E+00,3.418766E+00,3.351726E+00,3.286001E+00,3.221564E+00,3.158392E+00,3.096457E+00,
                               3.035738E+00,2.976209E+00,2.917847E+00,2.860630E+00,2.804535E+00,2.749540E+00,2.695623E+00,
                               2.642763E+00,2.590940E+00,2.540133E+00,2.490323E+00,2.441489E+00,2.393613E+00,2.346676E+00,
                               2.300659E+00,2.255544E+00,2.211315E+00,2.167952E+00,2.125440E+00,2.083761E+00,2.042900E+00,
                               2.002840E+00,1.963566E+00,1.925061E+00,1.887312E+00,1.850303E+00,1.814020E+00,1.778448E+00,
                               1.743573E+00,1.709383E+00,1.675863E+00,1.643000E+00,1.610782E+00,1.579196E+00,1.548229E+00,
                               1.517869E+00,1.488104E+00,1.458924E+00,1.430315E+00,1.402267E+00,1.374770E+00,1.347811E+00,
                               1.321382E+00,1.295470E+00,1.270067E+00,1.245162E+00,1.220745E+00,1.196807E+00,1.173338E+00,
                               1.150330E+00,1.127772E+00]]



        try:
            # internal model constants
            ted_empty.num_simulation_days = 366

            # internally specified variables
            a1 = pd.Series([.621, .621, .648], dtype='float')
            b1 = pd.Series([.564, .564, .651], dtype='float')

            # internally specified variables from external database
            body_wgt = pd.Series([15., 1000., 20.], dtype='float')
            frac_h2o = pd.Series([0.8, 0.8, 0.8], dtype='float')

            # input variables that change per simulation
            ted_empty.frac_retained_mamm = pd.Series([0.1, 0.1, 0.05], dtype='float')

            # internally calculated variables
            intake_food_conc  = pd.Series([[3.000000E+02,2.941172E+02,2.883497E+02,2.826954E+02,2.771519E+02,
                                            2.717171E+02,2.663889E+02,5.611652E+02,5.501611E+02,5.393727E+02,
                                            5.287960E+02,5.184266E+02,5.082606E+02,4.982939E+02,7.885227E+02,
                                            7.730602E+02,7.579010E+02,7.430390E+02,7.284684E+02,7.141836E+02,
                                            7.001789E+02,9.864488E+02,9.671052E+02,9.481408E+02,9.295484E+02,
                                            9.113205E+02,8.934501E+02,8.759300E+02,1.158754E+03,1.136031E+03,
                                            1.113754E+03,1.091914E+03,1.070502E+03,1.049511E+03,1.028930E+03,
                                            1.308754E+03,1.283090E+03,1.257929E+03,1.233262E+03,1.209078E+03,
                                            1.185369E+03,1.162125E+03,1.439336E+03,1.411112E+03,1.383441E+03,
                                            1.356312E+03,1.329716E+03,1.303641E+03,1.278077E+03,1.253015E+03,
                                            1.228444E+03,1.204355E+03,1.180738E+03,1.157585E+03,1.134885E+03,
                                            1.112631E+03,1.090813E+03,1.069423E+03,1.048452E+03,1.027892E+03,
                                            1.007736E+03,9.879750E+02,9.686014E+02,9.496077E+02,9.309865E+02,
                                            9.127304E+02,8.948323E+02,8.772852E+02,8.600822E+02,8.432165E+02,
                                            8.266816E+02,8.104708E+02,7.945780E+02,7.789968E+02,7.637211E+02,
                                            7.487450E+02,7.340626E+02,7.196681E+02,7.055558E+02,6.917203E+02,
                                            6.781561E+02,6.648579E+02,6.518204E+02,6.390386E+02,6.265075E+02,
                                            6.142220E+02,6.021775E+02,5.903692E+02,5.787924E+02,5.674426E+02,
                                            5.563154E+02,5.454064E+02,5.347113E+02,5.242260E+02,5.139462E+02,
                                            5.038680E+02,4.939875E+02,4.843007E+02,4.748039E+02,4.654933E+02,
                                            4.563652E+02,4.474162E+02,4.386426E+02,4.300411E+02,4.216083E+02,
                                            4.133408E+02,4.052354E+02,3.972890E+02,3.894984E+02,3.818606E+02,
                                            3.743725E+02,3.670313E+02,3.598340E+02,3.527779E+02,3.458602E+02,
                                            3.390781E+02,3.324289E+02,3.259102E+02,3.195193E+02,3.132537E+02,
                                            3.071110E+02,3.010888E+02,2.951846E+02,2.893962E+02,2.837213E+02,
                                            2.781577E+02,2.727032E+02,2.673557E+02,2.621130E+02,2.569731E+02,
                                            2.519340E+02,2.469938E+02,2.421504E+02,2.374019E+02,2.327466E+02,
                                            2.281826E+02,2.237081E+02,2.193213E+02,2.150205E+02,2.108041E+02,
                                            2.066704E+02,2.026177E+02,1.986445E+02,1.947492E+02,1.909303E+02,
                                            1.871863E+02,1.835157E+02,1.799170E+02,1.763890E+02,1.729301E+02,
                                            1.695390E+02,1.662145E+02,1.629551E+02,1.597597E+02,1.566269E+02,
                                            1.535555E+02,1.505444E+02,1.475923E+02,1.446981E+02,1.418607E+02,
                                            1.390789E+02,1.363516E+02,1.336778E+02,1.310565E+02,1.284866E+02,
                                            1.259670E+02,1.234969E+02,1.210752E+02,1.187010E+02,1.163733E+02,
                                            1.140913E+02,1.118540E+02,1.096607E+02,1.075103E+02,1.054021E+02,
                                            1.033352E+02,1.013089E+02,9.932225E+01,9.737460E+01,9.546514E+01,
                                            9.359313E+01,9.175783E+01,8.995851E+01,8.819448E+01,8.646504E+01,
                                            8.476951E+01,8.310723E+01,8.147755E+01,7.987983E+01,7.831343E+01,
                                            7.677775E+01,7.527219E+01,7.379615E+01,7.234905E+01,7.093033E+01,
                                            6.953943E+01,6.817580E+01,6.683892E+01,6.552825E+01,6.424328E+01,
                                            6.298351E+01,6.174844E+01,6.053759E+01,5.935048E+01,5.818666E+01,
                                            5.704565E+01,5.592702E+01,5.483033E+01,5.375514E+01,5.270103E+01,
                                            5.166760E+01,5.065443E+01,4.966112E+01,4.868730E+01,4.773257E+01,
                                            4.679657E+01,4.587891E+01,4.497926E+01,4.409724E+01,4.323252E+01,
                                            4.238476E+01,4.155362E+01,4.073878E+01,3.993991E+01,3.915672E+01,
                                            3.838888E+01,3.763609E+01,3.689807E+01,3.617452E+01,3.546516E+01,
                                            3.476971E+01,3.408790E+01,3.341946E+01,3.276412E+01,3.212164E+01,
                                            3.149175E+01,3.087422E+01,3.026879E+01,2.967524E+01,2.909333E+01,
                                            2.852283E+01,2.796351E+01,2.741516E+01,2.687757E+01,2.635052E+01,
                                            2.583380E+01,2.532721E+01,2.483056E+01,2.434365E+01,2.386629E+01,
                                            2.339828E+01,2.293946E+01,2.248963E+01,2.204862E+01,2.161626E+01,
                                            2.119238E+01,2.077681E+01,2.036939E+01,1.996996E+01,1.957836E+01,
                                            1.919444E+01,1.881805E+01,1.844904E+01,1.808726E+01,1.773258E+01,
                                            1.738486E+01,1.704395E+01,1.670973E+01,1.638206E+01,1.606082E+01,
                                            1.574588E+01,1.543711E+01,1.513440E+01,1.483762E+01,1.454666E+01,
                                            1.426141E+01,1.398176E+01,1.370758E+01,1.343878E+01,1.317526E+01,
                                            1.291690E+01,1.266361E+01,1.241528E+01,1.217183E+01,1.193314E+01,
                                            1.169914E+01,1.146973E+01,1.124481E+01,1.102431E+01,1.080813E+01,
                                            1.059619E+01,1.038840E+01,1.018469E+01,9.984978E+00,9.789179E+00,
                                            9.597219E+00,9.409024E+00,9.224518E+00,9.043631E+00,8.866291E+00,
                                            8.692429E+00,8.521975E+00,8.354865E+00,8.191031E+00,8.030410E+00,
                                            7.872938E+00,7.718555E+00,7.567199E+00,7.418810E+00,7.273332E+00,
                                            7.130706E+00,6.990878E+00,6.853791E+00,6.719392E+00,6.587629E+00,
                                            6.458450E+00,6.331803E+00,6.207641E+00,6.085913E+00,5.966571E+00,
                                            5.849571E+00,5.734864E+00,5.622407E+00,5.512155E+00,5.404065E+00,
                                            5.298095E+00,5.194202E+00,5.092347E+00,4.992489E+00,4.894590E+00,
                                            4.798610E+00,4.704512E+00,4.612259E+00,4.521816E+00,4.433146E+00,
                                            4.346214E+00,4.260988E+00,4.177432E+00,4.095515E+00,4.015205E+00,
                                            3.936469E+00,3.859277E+00,3.783599E+00,3.709405E+00,3.636666E+00,
                                            3.565353E+00,3.495439E+00,3.426895E+00,3.359696E+00,3.293814E+00,
                                            3.229225E+00,3.165902E+00,3.103820E+00,3.042956E+00,2.983286E+00,
                                            2.924785E+00,2.867432E+00,2.811203E+00,2.756077E+00,2.702032E+00,
                                            2.649047E+00,2.597101E+00,2.546174E+00,2.496245E+00,2.447295E+00,
                                            2.399305E+00],
                                            [3.000000E+02,2.941172E+02,2.883497E+02,2.826954E+02,2.771519E+02,
                                            2.717171E+02,2.663889E+02,5.611652E+02,5.501611E+02,5.393727E+02,
                                            5.287960E+02,5.184266E+02,5.082606E+02,4.982939E+02,7.885227E+02,
                                            7.730602E+02,7.579010E+02,7.430390E+02,7.284684E+02,7.141836E+02,
                                            7.001789E+02,9.864488E+02,9.671052E+02,9.481408E+02,9.295484E+02,
                                            9.113205E+02,8.934501E+02,8.759300E+02,1.158754E+03,1.136031E+03,
                                            1.113754E+03,1.091914E+03,1.070502E+03,1.049511E+03,1.028930E+03,
                                            1.308754E+03,1.283090E+03,1.257929E+03,1.233262E+03,1.209078E+03,
                                            1.185369E+03,1.162125E+03,1.439336E+03,1.411112E+03,1.383441E+03,
                                            1.356312E+03,1.329716E+03,1.303641E+03,1.278077E+03,1.253015E+03,
                                            1.228444E+03,1.204355E+03,1.180738E+03,1.157585E+03,1.134885E+03,
                                            1.112631E+03,1.090813E+03,1.069423E+03,1.048452E+03,1.027892E+03,
                                            1.007736E+03,9.879750E+02,9.686014E+02,9.496077E+02,9.309865E+02,
                                            9.127304E+02,8.948323E+02,8.772852E+02,8.600822E+02,8.432165E+02,
                                            8.266816E+02,8.104708E+02,7.945780E+02,7.789968E+02,7.637211E+02,
                                            7.487450E+02,7.340626E+02,7.196681E+02,7.055558E+02,6.917203E+02,
                                            6.781561E+02,6.648579E+02,6.518204E+02,6.390386E+02,6.265075E+02,
                                            6.142220E+02,6.021775E+02,5.903692E+02,5.787924E+02,5.674426E+02,
                                            5.563154E+02,5.454064E+02,5.347113E+02,5.242260E+02,5.139462E+02,
                                            5.038680E+02,4.939875E+02,4.843007E+02,4.748039E+02,4.654933E+02,
                                            4.563652E+02,4.474162E+02,4.386426E+02,4.300411E+02,4.216083E+02,
                                            4.133408E+02,4.052354E+02,3.972890E+02,3.894984E+02,3.818606E+02,
                                            3.743725E+02,3.670313E+02,3.598340E+02,3.527779E+02,3.458602E+02,
                                            3.390781E+02,3.324289E+02,3.259102E+02,3.195193E+02,3.132537E+02,
                                            3.071110E+02,3.010888E+02,2.951846E+02,2.893962E+02,2.837213E+02,
                                            2.781577E+02,2.727032E+02,2.673557E+02,2.621130E+02,2.569731E+02,
                                            2.519340E+02,2.469938E+02,2.421504E+02,2.374019E+02,2.327466E+02,
                                            2.281826E+02,2.237081E+02,2.193213E+02,2.150205E+02,2.108041E+02,
                                            2.066704E+02,2.026177E+02,1.986445E+02,1.947492E+02,1.909303E+02,
                                            1.871863E+02,1.835157E+02,1.799170E+02,1.763890E+02,1.729301E+02,
                                            1.695390E+02,1.662145E+02,1.629551E+02,1.597597E+02,1.566269E+02,
                                            1.535555E+02,1.505444E+02,1.475923E+02,1.446981E+02,1.418607E+02,
                                            1.390789E+02,1.363516E+02,1.336778E+02,1.310565E+02,1.284866E+02,
                                            1.259670E+02,1.234969E+02,1.210752E+02,1.187010E+02,1.163733E+02,
                                            1.140913E+02,1.118540E+02,1.096607E+02,1.075103E+02,1.054021E+02,
                                            1.033352E+02,1.013089E+02,9.932225E+01,9.737460E+01,9.546514E+01,
                                            9.359313E+01,9.175783E+01,8.995851E+01,8.819448E+01,8.646504E+01,
                                            8.476951E+01,8.310723E+01,8.147755E+01,7.987983E+01,7.831343E+01,
                                            7.677775E+01,7.527219E+01,7.379615E+01,7.234905E+01,7.093033E+01,
                                            6.953943E+01,6.817580E+01,6.683892E+01,6.552825E+01,6.424328E+01,
                                            6.298351E+01,6.174844E+01,6.053759E+01,5.935048E+01,5.818666E+01,
                                            5.704565E+01,5.592702E+01,5.483033E+01,5.375514E+01,5.270103E+01,
                                            5.166760E+01,5.065443E+01,4.966112E+01,4.868730E+01,4.773257E+01,
                                            4.679657E+01,4.587891E+01,4.497926E+01,4.409724E+01,4.323252E+01,
                                            4.238476E+01,4.155362E+01,4.073878E+01,3.993991E+01,3.915672E+01,
                                            3.838888E+01,3.763609E+01,3.689807E+01,3.617452E+01,3.546516E+01,
                                            3.476971E+01,3.408790E+01,3.341946E+01,3.276412E+01,3.212164E+01,
                                            3.149175E+01,3.087422E+01,3.026879E+01,2.967524E+01,2.909333E+01,
                                            2.852283E+01,2.796351E+01,2.741516E+01,2.687757E+01,2.635052E+01,
                                            2.583380E+01,2.532721E+01,2.483056E+01,2.434365E+01,2.386629E+01,
                                            2.339828E+01,2.293946E+01,2.248963E+01,2.204862E+01,2.161626E+01,
                                            2.119238E+01,2.077681E+01,2.036939E+01,1.996996E+01,1.957836E+01,
                                            1.919444E+01,1.881805E+01,1.844904E+01,1.808726E+01,1.773258E+01,
                                            1.738486E+01,1.704395E+01,1.670973E+01,1.638206E+01,1.606082E+01,
                                            1.574588E+01,1.543711E+01,1.513440E+01,1.483762E+01,1.454666E+01,
                                            1.426141E+01,1.398176E+01,1.370758E+01,1.343878E+01,1.317526E+01,
                                            1.291690E+01,1.266361E+01,1.241528E+01,1.217183E+01,1.193314E+01,
                                            1.169914E+01,1.146973E+01,1.124481E+01,1.102431E+01,1.080813E+01,
                                            1.059619E+01,1.038840E+01,1.018469E+01,9.984978E+00,9.789179E+00,
                                            9.597219E+00,9.409024E+00,9.224518E+00,9.043631E+00,8.866291E+00,
                                            8.692429E+00,8.521975E+00,8.354865E+00,8.191031E+00,8.030410E+00,
                                            7.872938E+00,7.718555E+00,7.567199E+00,7.418810E+00,7.273332E+00,
                                            7.130706E+00,6.990878E+00,6.853791E+00,6.719392E+00,6.587629E+00,
                                            6.458450E+00,6.331803E+00,6.207641E+00,6.085913E+00,5.966571E+00,
                                            5.849571E+00,5.734864E+00,5.622407E+00,5.512155E+00,5.404065E+00,
                                            5.298095E+00,5.194202E+00,5.092347E+00,4.992489E+00,4.894590E+00,
                                            4.798610E+00,4.704512E+00,4.612259E+00,4.521816E+00,4.433146E+00,
                                            4.346214E+00,4.260988E+00,4.177432E+00,4.095515E+00,4.015205E+00,
                                            3.936469E+00,3.859277E+00,3.783599E+00,3.709405E+00,3.636666E+00,
                                            3.565353E+00,3.495439E+00,3.426895E+00,3.359696E+00,3.293814E+00,
                                            3.229225E+00,3.165902E+00,3.103820E+00,3.042956E+00,2.983286E+00,
                                            2.924785E+00,2.867432E+00,2.811203E+00,2.756077E+00,2.702032E+00,
                                            2.649047E+00,2.597101E+00,2.546174E+00,2.496245E+00,2.447295E+00,
                                            2.399305E+00],
                                            [1.175000E+02,1.151959E+02,1.129370E+02,1.107224E+02,
                                             1.085512E+02,1.064225E+02,1.043356E+02,2.197897E+02,2.154797E+02,
                                             2.112543E+02,2.071118E+02,2.030504E+02,1.990687E+02,1.951651E+02,
                                             3.088380E+02,3.027819E+02,2.968445E+02,2.910236E+02,2.853168E+02,
                                             2.797219E+02,2.742367E+02,3.863591E+02,3.787829E+02,3.713552E+02,
                                             3.640731E+02,3.569339E+02,3.499346E+02,3.430726E+02,4.538452E+02,
                                             4.449455E+02,4.362204E+02,4.276664E+02,4.192801E+02,4.110583E+02,
                                             4.029977E+02,5.125952E+02,5.025435E+02,4.926889E+02,4.830276E+02,
                                             4.735557E+02,4.642696E+02,4.551655E+02,5.637400E+02,5.526854E+02,
                                             5.418476E+02,5.312223E+02,5.208053E+02,5.105927E+02,5.005803E+02,
                                             4.907642E+02,4.811406E+02,4.717057E+02,4.624559E+02,4.533874E+02,
                                             4.444967E+02,4.357804E+02,4.272350E+02,4.188572E+02,4.106437E+02,
                                             4.025912E+02,3.946966E+02,3.869569E+02,3.793689E+02,3.719297E+02,
                                             3.646364E+02,3.574861E+02,3.504760E+02,3.436034E+02,3.368655E+02,
                                             3.302598E+02,3.237836E+02,3.174344E+02,3.112097E+02,3.051071E+02,
                                             2.991241E+02,2.932585E+02,2.875079E+02,2.818700E+02,2.763427E+02,
                                             2.709238E+02,2.656111E+02,2.604027E+02,2.552963E+02,2.502901E+02,
                                             2.453821E+02,2.405703E+02,2.358529E+02,2.312279E+02,2.266937E+02,
                                             2.222484E+02,2.178902E+02,2.136175E+02,2.094286E+02,2.053218E+02,
                                             2.012956E+02,1.973483E+02,1.934784E+02,1.896844E+02,1.859648E+02,
                                             1.823182E+02,1.787430E+02,1.752380E+02,1.718017E+02,1.684328E+02,
                                             1.651299E+02,1.618918E+02,1.587172E+02,1.556049E+02,1.525535E+02,
                                             1.495621E+02,1.466292E+02,1.437539E+02,1.409350E+02,1.381714E+02,
                                             1.354619E+02,1.328056E+02,1.302013E+02,1.276482E+02,1.251451E+02,
                                             1.226910E+02,1.202851E+02,1.179264E+02,1.156140E+02,1.133468E+02,
                                             1.111242E+02,1.089451E+02,1.068088E+02,1.047143E+02,1.026609E+02,
                                             1.006478E+02,9.867416E+01,9.673922E+01,9.484222E+01,9.298242E+01,
                                             9.115910E+01,8.937152E+01,8.761900E+01,8.590085E+01,8.421638E+01,
                                             8.256495E+01,8.094590E+01,7.935860E+01,7.780243E+01,7.627677E+01,
                                             7.478103E+01,7.331462E+01,7.187696E+01,7.046750E+01,6.908568E+01,
                                             6.773095E+01,6.640279E+01,6.510067E+01,6.382408E+01,6.257253E+01,
                                             6.134552E+01,6.014257E+01,5.896321E+01,5.780698E+01,5.667342E+01,
                                             5.556209E+01,5.447255E+01,5.340438E+01,5.235715E+01,5.133046E+01,
                                             5.032390E+01,4.933708E+01,4.836961E+01,4.742111E+01,4.649121E+01,
                                             4.557955E+01,4.468576E+01,4.380950E+01,4.295042E+01,4.210819E+01,
                                             4.128248E+01,4.047295E+01,3.967930E+01,3.890121E+01,3.813839E+01,
                                             3.739051E+01,3.665731E+01,3.593848E+01,3.523375E+01,3.454284E+01,
                                             3.386547E+01,3.320139E+01,3.255033E+01,3.191204E+01,3.128627E+01,
                                             3.067276E+01,3.007129E+01,2.948161E+01,2.890349E+01,2.833671E+01,
                                             2.778105E+01,2.723628E+01,2.670219E+01,2.617858E+01,2.566523E+01,
                                             2.516195E+01,2.466854E+01,2.418480E+01,2.371056E+01,2.324561E+01,
                                             2.278977E+01,2.234288E+01,2.190475E+01,2.147521E+01,2.105410E+01,
                                             2.064124E+01,2.023648E+01,1.983965E+01,1.945061E+01,1.906919E+01,
                                             1.869526E+01,1.832865E+01,1.796924E+01,1.761688E+01,1.727142E+01,
                                             1.693274E+01,1.660070E+01,1.627517E+01,1.595602E+01,1.564313E+01,
                                             1.533638E+01,1.503564E+01,1.474080E+01,1.445175E+01,1.416836E+01,
                                             1.389052E+01,1.361814E+01,1.335109E+01,1.308929E+01,1.283261E+01,
                                             1.258098E+01,1.233427E+01,1.209240E+01,1.185528E+01,1.162280E+01,
                                             1.139489E+01,1.117144E+01,1.095238E+01,1.073761E+01,1.052705E+01,
                                             1.032062E+01,1.011824E+01,9.919825E+00,9.725304E+00,9.534596E+00,
                                             9.347629E+00,9.164327E+00,8.984620E+00,8.808438E+00,8.635709E+00,
                                             8.466368E+00,8.300348E+00,8.137583E+00,7.978010E+00,7.821566E+00,
                                             7.668190E+00,7.517822E+00,7.370402E+00,7.225873E+00,7.084178E+00,
                                             6.945261E+00,6.809069E+00,6.675547E+00,6.544644E+00,6.416307E+00,
                                             6.290488E+00,6.167135E+00,6.046201E+00,5.927639E+00,5.811402E+00,
                                             5.697443E+00,5.585720E+00,5.476188E+00,5.368803E+00,5.263524E+00,
                                             5.160309E+00,5.059119E+00,4.959913E+00,4.862652E+00,4.767298E+00,
                                             4.673814E+00,4.582164E+00,4.492310E+00,4.404219E+00,4.317855E+00,
                                             4.233184E+00,4.150174E+00,4.068792E+00,3.989005E+00,3.910783E+00,
                                             3.834095E+00,3.758911E+00,3.685201E+00,3.612936E+00,3.542089E+00,
                                             3.472631E+00,3.404535E+00,3.337774E+00,3.272322E+00,3.208154E+00,
                                             3.145244E+00,3.083567E+00,3.023101E+00,2.963819E+00,2.905701E+00,
                                             2.848722E+00,2.792860E+00,2.738094E+00,2.684401E+00,2.631762E+00,
                                             2.580155E+00,2.529559E+00,2.479956E+00,2.431326E+00,2.383649E+00,
                                             2.336907E+00,2.291082E+00,2.246155E+00,2.202109E+00,2.158927E+00,
                                             2.116592E+00,2.075087E+00,2.034396E+00,1.994503E+00,1.955392E+00,
                                             1.917048E+00,1.879455E+00,1.842600E+00,1.806468E+00,1.771044E+00,
                                             1.736315E+00,1.702267E+00,1.668887E+00,1.636161E+00,1.604077E+00,
                                             1.572622E+00,1.541784E+00,1.511550E+00,1.481910E+00,1.452850E+00,
                                             1.424361E+00,1.396430E+00,1.369047E+00,1.342201E+00,1.315881E+00,
                                             1.290077E+00,1.264780E+00,1.239978E+00,1.215663E+00,1.191825E+00,
                                             1.168454E+00,1.145541E+00,1.123078E+00,1.101055E+00,1.079464E+00,
                                             1.058296E+00,1.037544E+00,1.017198E+00,9.972513E-01,9.776958E-01,
                                             9.585238E-01,9.397277E-01]], dtype='float')

            for i in range(3):
                result[i] = ted_empty.daily_animal_dose_timeseries(a1[i], b1[i], body_wgt[i], frac_h2o[i], intake_food_conc[i], ted_empty.frac_retained_mamm[i])
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_daily_canopy_air_timeseries(self):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil pore water and surface puddles
        :param i; simulation number/index
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs
        :param daily_flag; daily flag denoting if pesticide is applied (0 - not applied, 1 - applied)
        :param water_type; type of water (pore water or surface puddles)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([], dtype='float')
        result = pd.Series([], dtype='float')
        expected_results = [[2.697542E-06,2.575726E-06,2.459410E-06,5.045889E-06,4.818025E-06,4.600451E-06,
                             7.090244E-06,6.770060E-06,6.464335E-06,6.172416E-06,5.893680E-06,5.627531E-06,
                             5.373400E-06,5.130746E-06,4.899050E-06,4.677817E-06,4.466574E-06,4.264871E-06,
                             4.072276E-06,3.888378E-06,3.712786E-06,3.545122E-06,3.385030E-06,3.232168E-06,
                             3.086208E-06,2.946840E-06,2.813765E-06,2.686700E-06,2.565373E-06,2.449525E-06,
                             2.338908E-06,2.233287E-06,2.132435E-06,2.036138E-06,1.944189E-06,1.856393E-06,
                             1.772561E-06,1.692515E-06,1.616084E-06,1.543104E-06,1.473420E-06,1.406883E-06,
                             1.343350E-06,1.282687E-06,1.224762E-06,1.169454E-06,1.116643E-06,1.066218E-06,
                             1.018069E-06,9.720946E-07,9.281964E-07,8.862805E-07,8.462575E-07,8.080419E-07,
                             7.715520E-07,7.367100E-07,7.034413E-07,6.716750E-07,6.413433E-07,6.123812E-07,
                             5.847271E-07,5.583217E-07,5.331088E-07,5.090345E-07,4.860473E-07,4.640982E-07,
                             4.431403E-07,4.231288E-07,4.040209E-07,3.857760E-07,3.683550E-07,3.517207E-07,
                             3.358375E-07,3.206716E-07,3.061906E-07,2.923635E-07,2.791609E-07,2.665544E-07,
                             2.545172E-07,2.430237E-07,2.320491E-07,2.215701E-07,2.115644E-07,2.020105E-07,
                             1.928880E-07,1.841775E-07,1.758603E-07,1.679188E-07,1.603358E-07,1.530953E-07,
                             1.461818E-07,1.395804E-07,1.332772E-07,1.272586E-07,1.215118E-07,1.160245E-07,
                             1.107851E-07,1.057822E-07,1.010052E-07,9.644400E-08,9.208875E-08,8.793017E-08,
                             8.395938E-08,8.016791E-08,7.654765E-08,7.309089E-08,6.979022E-08,6.663860E-08,
                             6.362931E-08,6.075591E-08,5.801227E-08,5.539253E-08,5.289110E-08,5.050262E-08,
                             4.822200E-08,4.604437E-08,4.396508E-08,4.197969E-08,4.008395E-08,3.827383E-08,
                             3.654544E-08,3.489511E-08,3.331930E-08,3.181466E-08,3.037796E-08,2.900614E-08,
                             2.769627E-08,2.644555E-08,2.525131E-08,2.411100E-08,2.302219E-08,2.198254E-08,
                             2.098985E-08,2.004198E-08,1.913691E-08,1.827272E-08,1.744755E-08,1.665965E-08,
                             1.590733E-08,1.518898E-08,1.450307E-08,1.384813E-08,1.322277E-08,1.262565E-08,
                             1.205550E-08,1.151109E-08,1.099127E-08,1.049492E-08,1.002099E-08,9.568457E-09,
                             9.136361E-09,8.723777E-09,8.329826E-09,7.953664E-09,7.594489E-09,7.251534E-09,
                             6.924067E-09,6.611387E-09,6.312827E-09,6.027750E-09,5.755547E-09,5.495635E-09,
                             5.247461E-09,5.010494E-09,4.784228E-09,4.568180E-09,4.361889E-09,4.164913E-09,
                             3.976832E-09,3.797245E-09,3.625767E-09,3.462033E-09,3.305693E-09,3.156414E-09,
                             3.013875E-09,2.877773E-09,2.747818E-09,2.623731E-09,2.505247E-09,2.392114E-09,
                             2.284090E-09,2.180944E-09,2.082456E-09,1.988416E-09,1.898622E-09,1.812884E-09,
                             1.731017E-09,1.652847E-09,1.578207E-09,1.506938E-09,1.438887E-09,1.373909E-09,
                             1.311865E-09,1.252624E-09,1.196057E-09,1.142045E-09,1.090472E-09,1.041228E-09,
                             9.942080E-10,9.493112E-10,9.064418E-10,8.655083E-10,8.264234E-10,7.891034E-10,
                             7.534688E-10,7.194433E-10,6.869544E-10,6.559327E-10,6.263118E-10,5.980286E-10,
                             5.710225E-10,5.452361E-10,5.206141E-10,4.971040E-10,4.746556E-10,4.532209E-10,
                             4.327542E-10,4.132117E-10,3.945517E-10,3.767344E-10,3.597217E-10,3.434772E-10,
                             3.279663E-10,3.131559E-10,2.990143E-10,2.855113E-10,2.726180E-10,2.603070E-10,
                             2.485520E-10,2.373278E-10,2.266104E-10,2.163771E-10,2.066058E-10,1.972759E-10,
                             1.883672E-10,1.798608E-10,1.717386E-10,1.639832E-10,1.565779E-10,1.495071E-10,
                             1.427556E-10,1.363090E-10,1.301535E-10,1.242760E-10,1.186639E-10,1.133052E-10,
                             1.081885E-10,1.033029E-10,9.863793E-11,9.418360E-11,8.993042E-11,8.586930E-11,
                             8.199158E-11,7.828897E-11,7.475357E-11,7.137782E-11,6.815451E-11,6.507676E-11,
                             6.213800E-11,5.933195E-11,5.665261E-11,5.409427E-11,5.165146E-11,4.931896E-11,
                             4.709180E-11,4.496521E-11,4.293465E-11,4.099579E-11,3.914449E-11,3.737678E-11,
                             3.568891E-11,3.407726E-11,3.253838E-11,3.106900E-11,2.966597E-11,2.832631E-11,
                             2.704714E-11,2.582573E-11,2.465948E-11,2.354590E-11,2.248260E-11,2.146733E-11,
                             2.049790E-11,1.957224E-11,1.868839E-11,1.784445E-11,1.703863E-11,1.626919E-11,
                             1.553450E-11,1.483299E-11,1.416315E-11,1.352357E-11,1.291287E-11,1.232974E-11,
                             1.177295E-11,1.124130E-11,1.073366E-11,1.024895E-11,9.786122E-12,9.344196E-12,
                             8.922227E-12,8.519314E-12,8.134595E-12,7.767250E-12,7.416493E-12,7.081576E-12,
                             6.761784E-12,6.456433E-12,6.164870E-12,5.886475E-12,5.620651E-12,5.366831E-12,
                             5.124474E-12,4.893061E-12,4.672098E-12,4.461114E-12,4.259657E-12,4.067298E-12,
                             3.883625E-12,3.708247E-12,3.540788E-12,3.380892E-12,3.228216E-12,3.082435E-12,
                             2.943237E-12,2.810325E-12,2.683416E-12,2.562237E-12,2.446530E-12,2.336049E-12,
                             2.230557E-12,2.129828E-12,2.033649E-12,1.941812E-12,1.854123E-12,1.770394E-12,
                             1.690446E-12,1.614108E-12,1.541218E-12,1.471619E-12,1.405163E-12,1.341708E-12,
                             1.281118E-12,1.223265E-12,1.168025E-12,1.115278E-12,1.064914E-12,1.016824E-12,
                             9.709062E-13,9.270617E-13,8.851971E-13,8.452230E-13,8.070541E-13,7.706088E-13,
                             7.358093E-13,7.025814E-13,6.708539E-13,6.405592E-13,6.116326E-13,5.840123E-13,
                             5.576392E-13,5.324571E-13,5.084122E-13,4.854531E-13,4.635308E-13,4.425985E-13],
                             [1.747062E-05,1.699289E-05,1.652822E-05,1.607625E-05,1.563665E-05,1.520906E-05,
                             1.479317E-05,3.185927E-05,3.098808E-05,3.014071E-05,2.931651E-05,2.851485E-05,
                             2.773511E-05,2.697669E-05,4.370963E-05,4.251439E-05,4.135183E-05,4.022106E-05,
                             3.912122E-05,3.805144E-05,3.701093E-05,5.346948E-05,5.200736E-05,5.058521E-05,
                             4.920196E-05,4.785653E-05,4.654789E-05,4.527503E-05,6.150761E-05,5.982568E-05,
                             5.818974E-05,5.659854E-05,5.505085E-05,5.354548E-05,5.208128E-05,5.065711E-05,
                             4.927189E-05,4.792455E-05,4.661405E-05,4.533939E-05,4.409958E-05,4.289367E-05,
                             4.172074E-05,4.057989E-05,3.947023E-05,3.839091E-05,3.734111E-05,3.632002E-05,
                             3.532684E-05,3.436083E-05,3.342123E-05,3.250733E-05,3.161841E-05,3.075380E-05,
                             2.991284E-05,2.909487E-05,2.829927E-05,2.752543E-05,2.677274E-05,2.604064E-05,
                             2.532856E-05,2.463595E-05,2.396227E-05,2.330703E-05,2.266969E-05,2.204979E-05,
                             2.144684E-05,2.086037E-05,2.028994E-05,1.973511E-05,1.919546E-05,1.867056E-05,
                             1.816001E-05,1.766342E-05,1.718041E-05,1.671062E-05,1.625366E-05,1.580921E-05,
                             1.537690E-05,1.495642E-05,1.454744E-05,1.414964E-05,1.376271E-05,1.338637E-05,
                             1.302032E-05,1.266428E-05,1.231797E-05,1.198114E-05,1.165351E-05,1.133485E-05,
                             1.102489E-05,1.072342E-05,1.043019E-05,1.014497E-05,9.867557E-06,9.597728E-06,
                             9.335278E-06,9.080004E-06,8.831711E-06,8.590207E-06,8.355308E-06,8.126831E-06,
                             7.904603E-06,7.688451E-06,7.478210E-06,7.273718E-06,7.074818E-06,6.881356E-06,
                             6.693185E-06,6.510160E-06,6.332139E-06,6.158987E-06,5.990569E-06,5.826756E-06,
                             5.667423E-06,5.512447E-06,5.361709E-06,5.215093E-06,5.072486E-06,4.933779E-06,
                             4.798864E-06,4.667639E-06,4.540002E-06,4.415856E-06,4.295104E-06,4.177654E-06,
                             4.063416E-06,3.952301E-06,3.844226E-06,3.739105E-06,3.636859E-06,3.537409E-06,
                             3.440678E-06,3.346593E-06,3.255080E-06,3.166070E-06,3.079493E-06,2.995284E-06,
                             2.913378E-06,2.833712E-06,2.756224E-06,2.680855E-06,2.607546E-06,2.536243E-06,
                             2.466889E-06,2.399432E-06,2.333819E-06,2.270001E-06,2.207928E-06,2.147552E-06,
                             2.088827E-06,2.031708E-06,1.976151E-06,1.922113E-06,1.869552E-06,1.818429E-06,
                             1.768704E-06,1.720339E-06,1.673296E-06,1.627540E-06,1.583035E-06,1.539747E-06,
                             1.497642E-06,1.456689E-06,1.416856E-06,1.378112E-06,1.340427E-06,1.303773E-06,
                             1.268121E-06,1.233445E-06,1.199716E-06,1.166910E-06,1.135001E-06,1.103964E-06,
                             1.073776E-06,1.044413E-06,1.015854E-06,9.880754E-07,9.610564E-07,9.347762E-07,
                             9.092147E-07,8.843522E-07,8.601696E-07,8.366482E-07,8.137700E-07,7.915174E-07,
                             7.698733E-07,7.488211E-07,7.283445E-07,7.084279E-07,6.890559E-07,6.702136E-07,
                             6.518866E-07,6.340607E-07,6.167223E-07,5.998580E-07,5.834549E-07,5.675003E-07,
                             5.519819E-07,5.368880E-07,5.222067E-07,5.079270E-07,4.940377E-07,4.805282E-07,
                             4.673881E-07,4.546074E-07,4.421761E-07,4.300848E-07,4.183241E-07,4.068850E-07,
                             3.957587E-07,3.849367E-07,3.744105E-07,3.641723E-07,3.542140E-07,3.445280E-07,
                             3.351068E-07,3.259433E-07,3.170304E-07,3.083612E-07,2.999290E-07,2.917274E-07,
                             2.837501E-07,2.759910E-07,2.684440E-07,2.611034E-07,2.539635E-07,2.470188E-07,
                             2.402641E-07,2.336941E-07,2.273037E-07,2.210881E-07,2.150424E-07,2.091620E-07,
                             2.034425E-07,1.978794E-07,1.924683E-07,1.872053E-07,1.820861E-07,1.771070E-07,
                             1.722640E-07,1.675534E-07,1.629717E-07,1.585152E-07,1.541806E-07,1.499645E-07,
                             1.458637E-07,1.418751E-07,1.379955E-07,1.342220E-07,1.305517E-07,1.269817E-07,
                             1.235094E-07,1.201320E-07,1.168470E-07,1.136518E-07,1.105440E-07,1.075212E-07,
                             1.045810E-07,1.017212E-07,9.893968E-08,9.623416E-08,9.360264E-08,9.104307E-08,
                             8.855349E-08,8.613199E-08,8.377671E-08,8.148583E-08,7.925759E-08,7.709029E-08,
                             7.498225E-08,7.293186E-08,7.093753E-08,6.899774E-08,6.711100E-08,6.527584E-08,
                             6.349087E-08,6.175471E-08,6.006602E-08,5.842352E-08,5.682592E-08,5.527201E-08,
                             5.376060E-08,5.229051E-08,5.086062E-08,4.946984E-08,4.811708E-08,4.680132E-08,
                             4.552153E-08,4.427674E-08,4.306599E-08,4.188835E-08,4.074291E-08,3.962880E-08,
                             3.854515E-08,3.749113E-08,3.646593E-08,3.546877E-08,3.449887E-08,3.355550E-08,
                             3.263792E-08,3.174544E-08,3.087735E-08,3.003301E-08,2.921176E-08,2.841296E-08,
                             2.763601E-08,2.688030E-08,2.614526E-08,2.543031E-08,2.473492E-08,2.405854E-08,
                             2.340066E-08,2.276077E-08,2.213837E-08,2.153300E-08,2.094418E-08,2.037146E-08,
                             1.981440E-08,1.927257E-08,1.874556E-08,1.823296E-08,1.773438E-08,1.724944E-08,
                             1.677775E-08,1.631896E-08,1.587272E-08,1.543868E-08,1.501651E-08,1.460588E-08,
                             1.420648E-08,1.381800E-08,1.344015E-08,1.307263E-08,1.271516E-08,1.236746E-08,
                             1.202927E-08,1.170033E-08,1.138038E-08,1.106919E-08,1.076650E-08,1.047209E-08,
                             1.018573E-08,9.907199E-09,9.636286E-09,9.372782E-09,9.116482E-09,8.867192E-09,
                             8.624718E-09,8.388874E-09,8.159480E-09,7.936359E-09,7.719339E-09,7.508253E-09,
                             7.302939E-09,7.103240E-09,6.909002E-09,6.720075E-09,6.536314E-09,6.357578E-09,
                             6.183730E-09,6.014635E-09,5.850165E-09,5.690192E-09,5.534593E-09,5.383249E-09],
                             [1.133578E-07,1.111350E-07,1.089557E-07,1.068191E-07,1.047245E-07,1.026709E-07,
                             1.006576E-07,9.868374E-08,9.674861E-08,9.485143E-08,9.299145E-08,9.116795E-08,
                             8.938020E-08,8.762751E-08,8.590918E-08,8.422456E-08,8.257297E-08,8.095376E-08,
                             7.936631E-08,7.780998E-08,7.628418E-08,7.478829E-08,7.332174E-08,7.188394E-08,
                             7.047434E-08,6.909238E-08,6.773752E-08,6.640923E-08,6.510699E-08,6.383028E-08,
                             6.257861E-08,6.135148E-08,6.014841E-08,5.896894E-08,5.781259E-08,5.667892E-08,
                             5.556749E-08,5.447784E-08,5.340956E-08,5.236223E-08,5.133544E-08,5.032879E-08,
                             4.934187E-08,4.837431E-08,4.742571E-08,4.649573E-08,4.558397E-08,4.469010E-08,
                             4.381375E-08,4.295459E-08,4.211228E-08,4.128648E-08,4.047688E-08,3.968315E-08,
                             3.890499E-08,3.814209E-08,3.739414E-08,3.666087E-08,3.594197E-08,3.523717E-08,
                             3.454619E-08,3.386876E-08,3.320462E-08,3.255349E-08,3.191514E-08,3.128930E-08,
                             3.067574E-08,3.007421E-08,2.948447E-08,2.890630E-08,2.833946E-08,2.778374E-08,
                             2.723892E-08,2.670478E-08,2.618112E-08,2.566772E-08,2.516439E-08,2.467093E-08,
                             2.418715E-08,2.371286E-08,2.324786E-08,2.279199E-08,2.234505E-08,2.190688E-08,
                             2.147730E-08,2.105614E-08,2.064324E-08,2.023844E-08,1.984158E-08,1.945250E-08,
                             1.907104E-08,1.869707E-08,1.833043E-08,1.797099E-08,1.761859E-08,1.727310E-08,
                             1.693438E-08,1.660231E-08,1.627675E-08,1.595757E-08,1.564465E-08,1.533787E-08,
                             1.503710E-08,1.474223E-08,1.445315E-08,1.416973E-08,1.389187E-08,1.361946E-08,
                             1.335239E-08,1.309056E-08,1.283386E-08,1.258220E-08,1.233547E-08,1.209358E-08,
                             1.185643E-08,1.162393E-08,1.139599E-08,1.117252E-08,1.095344E-08,1.073865E-08,
                             1.052807E-08,1.032162E-08,1.011922E-08,9.920788E-09,9.726248E-09,9.535522E-09,
                             9.348536E-09,9.165217E-09,8.985493E-09,8.809293E-09,8.636548E-09,8.467190E-09,
                             8.301154E-09,8.138373E-09,7.978785E-09,7.822326E-09,7.668935E-09,7.518552E-09,
                             7.371117E-09,7.226574E-09,7.084866E-09,6.945936E-09,6.809730E-09,6.676195E-09,
                             6.545279E-09,6.416930E-09,6.291098E-09,6.167734E-09,6.046788E-09,5.928214E-09,
                             5.811966E-09,5.697997E-09,5.586262E-09,5.476719E-09,5.369324E-09,5.264035E-09,
                             5.160810E-09,5.059610E-09,4.960394E-09,4.863124E-09,4.767761E-09,4.674268E-09,
                             4.582609E-09,4.492746E-09,4.404646E-09,4.318274E-09,4.233595E-09,4.150577E-09,
                             4.069187E-09,3.989392E-09,3.911163E-09,3.834467E-09,3.759276E-09,3.685559E-09,
                             3.613287E-09,3.542433E-09,3.472968E-09,3.404865E-09,3.338098E-09,3.272640E-09,
                             3.208465E-09,3.145549E-09,3.083867E-09,3.023394E-09,2.964107E-09,2.905983E-09,
                             2.848998E-09,2.793131E-09,2.738360E-09,2.684662E-09,2.632017E-09,2.580405E-09,
                             2.529805E-09,2.480197E-09,2.431562E-09,2.383880E-09,2.337134E-09,2.291304E-09,
                             2.246373E-09,2.202323E-09,2.159137E-09,2.116798E-09,2.075288E-09,2.034593E-09,
                             1.994696E-09,1.955581E-09,1.917234E-09,1.879638E-09,1.842779E-09,1.806644E-09,
                             1.771216E-09,1.736484E-09,1.702433E-09,1.669049E-09,1.636320E-09,1.604233E-09,
                             1.572775E-09,1.541933E-09,1.511697E-09,1.482054E-09,1.452991E-09,1.424499E-09,
                             1.396566E-09,1.369180E-09,1.342331E-09,1.316009E-09,1.290203E-09,1.264903E-09,
                             1.240099E-09,1.215781E-09,1.191940E-09,1.168567E-09,1.145652E-09,1.123187E-09,
                             1.101162E-09,1.079568E-09,1.058399E-09,1.037644E-09,1.017297E-09,9.973481E-10,
                             9.777907E-10,9.586168E-10,9.398189E-10,9.213897E-10,9.033218E-10,8.856082E-10,
                             8.682420E-10,8.512163E-10,8.345244E-10,8.181599E-10,8.021163E-10,7.863873E-10,
                             7.709667E-10,7.558485E-10,7.410268E-10,7.264957E-10,7.122496E-10,6.982828E-10,
                             6.845899E-10,6.711655E-10,6.580044E-10,6.451013E-10,6.324513E-10,6.200493E-10,
                             6.078905E-10,5.959701E-10,5.842835E-10,5.728261E-10,5.615933E-10,5.505808E-10,
                             5.397842E-10,5.291994E-10,5.188221E-10,5.086483E-10,4.986741E-10,4.888954E-10,
                             4.793084E-10,4.699095E-10,4.606948E-10,4.516609E-10,4.428041E-10,4.341210E-10,
                             4.256081E-10,4.172622E-10,4.090800E-10,4.010581E-10,3.931936E-10,3.854834E-10,
                             3.779243E-10,3.705134E-10,3.632479E-10,3.561248E-10,3.491414E-10,3.422949E-10,
                             3.355828E-10,3.290022E-10,3.225506E-10,3.162256E-10,3.100246E-10,3.039452E-10,
                             2.979851E-10,2.921418E-10,2.864130E-10,2.807966E-10,2.752904E-10,2.698921E-10,
                             2.645997E-10,2.594111E-10,2.543242E-10,2.493370E-10,2.444477E-10,2.396542E-10,
                             2.349547E-10,2.303474E-10,2.258304E-10,2.214020E-10,2.170605E-10,2.128041E-10,
                             2.086311E-10,2.045400E-10,2.005291E-10,1.965968E-10,1.927417E-10,1.889621E-10,
                             1.852567E-10,1.816239E-10,1.780624E-10,1.745707E-10,1.711475E-10,1.677914E-10,
                             1.645011E-10,1.612753E-10,1.581128E-10,1.550123E-10,1.519726E-10,1.489925E-10,
                             1.460709E-10,1.432065E-10,1.403983E-10,1.376452E-10,1.349461E-10,1.322999E-10,
                             1.297055E-10,1.271621E-10,1.246685E-10,1.222238E-10,1.198271E-10,1.174774E-10,
                             1.151737E-10,1.129152E-10,1.107010E-10,1.085302E-10,1.064020E-10,1.043156E-10,
                             1.022700E-10,1.002645E-10,9.829841E-11,9.637084E-11,9.448107E-11,9.262835E-11,
                             9.081196E-11,8.903120E-11,8.728535E-11,8.557374E-11,8.389569E-11,8.225054E-11]]

        try:
            # internal model constants
            ted_empty.num_simulation_days = 366

            ted_empty.hectare_to_acre = 2.47105
            ted_empty.gms_to_mg = 1000.
            ted_empty.lbs_to_gms = 453.592
            ted_empty.crop_hgt = 1. # m
            ted_empty.hectare_area = 10000.  # m2
            ted_empty.m3_to_liters = 1000.
            ted_empty.mass_plant = 25000. # kg/hectare
            ted_empty.density_plant = 0.77 # kg/L

            # internally calculated variable (hlc in atm-m3/mol are 2.0e-7, 1.0e-5, 3.5e-6)
            ted_empty.log_unitless_hlc = pd.Series([-5.087265, -3.388295, -3.844227], dtype='float')

            # input variables that change per simulation
            ted_empty.log_kow = pd.Series([2.75, 4., 6.], dtype='float')
            ted_empty.foliar_diss_hlife = pd.Series([15., 25., 35.])
            ted_empty.app_rate_min = pd.Series([0.18, 0.5, 1.25]) # lbs a.i./acre

            # application scenarios generated from 'daily_app_flag' tests and reused here
            daily_flag = pd.Series([[True, False, False, True, False, False, True, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                             [True, False, False, False, False, False, False, True, False, False,
                              False, False, False, False, True, False, False, False, False, False,
                              False, True, False, False, False, False, False, False, True, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False, False, False, False, False,
                              False, False, False, False, False, False],
                              [True, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False]], dtype='bool')

            for i in range(3):
                result[i] = ted_empty.daily_canopy_air_timeseries(i, ted_empty.app_rate_min[i], daily_flag[i])
                # tolerance set to 1e-3 instead of 1e-4 because precision in specifying constants between this code and the OPP TED spreadsheet
                npt.assert_allclose(result[i],expected_results[i],rtol=1e-3, atol=0, err_msg='', verbose=True)
        finally:
            for i in range(3):
                tab = [result[i], expected_results[i]]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
        return


    def test_set_max_drift_distance(self):
        """
        :description sets the maximum distance from applicaiton source area for which spray drift calculations are calculated
        :param app_method; application method (aerial/ground/airblast)
        :param max_spray_drift_dist: maximum distance from applicaiton source area for which spray drift calculations are calculated (feet)

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([2600., 1000., 1000.], dtype='float')
        result = pd.Series([], dtype='float')

        try:

            ted_empty.num_simulations = 3
            # input variable that change per simulation
            ted_empty.app_method_min = pd.Series(['aerial', 'ground', 'airblast'], dtype='object')

            for i in range(ted_empty.num_simulations):
                result[i] = ted_empty.set_max_drift_distance(ted_empty.app_method_min[i])
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_set_max_respire_frac(self):
        """
        :description provides parmaeter values to use when calculating distances from edge of application source area to
                     concentration of interest
        :param app_method; application method (aerial/ground/airblast)
        :param drop_size; droplet spectrum for application (see list below for aerial/ground - 'NA' if airblast)
        :param max_respire_frac; volumetric fraction of droplet spectrum not exceeding the upper size liit of respired particles for birds

        :NOTE this represents specification from OPP TED Excel 'inputs' worksheet columns H & I rows 14 - 16
              these values are used in the 'min/max rate doses' worksheet column S (while referenced here as the MAX of
              three values specified in the 'inputs' worksheet (one per application method) the MAX will always be the value associated
              with the application method specified for the simulation (i.e., the value specified below)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([0.28, 0.067, 0.028, 0.02, 0.28, 0.067, 0.28], dtype='float')
        result = pd.Series([], dtype='float')

        try:

            ted_empty.num_simulations = 7
            # input variable that change per simulation

            ted_empty.app_method_min = pd.Series(['aerial', 'aerial','aerial','aerial', 'ground', 'ground', 'airblast'], dtype='object')
            ted_empty.droplet_spec_min = pd.Series(['very_fine_to_fine', 'fine_to_medium','medium_to_coarse','coarse_to_very_coarse',
                                                    'very_fine_to_fine', 'fine_to_medium-coarse', ' '], dtype='object')

            for i in range(ted_empty.num_simulations):
                result[i] = ted_empty.set_max_respire_frac(ted_empty.app_method_min[i], ted_empty.droplet_spec_min[i])
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_plant_risk_distance(self):
        """
        :description calculates the distance from the source area that plant toxicity thresholds occur
        :NOTE         represents columns C & D rows 32 to 51 in OPP TED Excel spreadsheet 'Plants' worksheet
                      (only calculated if health risk value is present;
                      if ratio of health risk value to applicatoin rate is greater than 1.0 then distance is set to 0.0 (i.e. at source area edge)
                      if distance is greater than max spray drift distance then distance is set to max spray drift distance

                      values for risk distances are not stored across simulations

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series(['nan', 0.0, 0.229889], dtype='float')
        result = pd.Series([], dtype='float')

        try:

            ted_empty.num_simulations = 3

            # input variable that change per simulation
            health_to_app_ratio = pd.Series(['nan', 2.0, 0.5], dtype='float')

            param_a = pd.Series([0.0292, 0.1913, 5.5513], dtype='float')
            param_b = pd.Series([0.822, 1.2366, 0.8523], dtype='float')
            param_c = pd.Series([0.6539, 1.0552, 1.0079], dtype='float')

            ted_empty.max_distance_from_source = pd.Series([1000., 2600., 1000.], dtype='float')

            for i in range(ted_empty.num_simulations):
                result[i] = ted_empty.calc_plant_risk_distance(health_to_app_ratio[i], param_a[i], param_b[i], param_c[i], ted_empty.max_distance_from_source[i])
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sum_exceedances(self):
        """
        :description this method accumulates the number of time various toxicity measures are exceeded within daily time
                     series of food item concentrations
        :param num_ts number of time series included in the aggregate incoming 'time_series'
        :param num_tox number of toxicity measures to be precessed per time series
        :param eec_ts_upper_min_1 a panda series representing an aggregation of time series representing the daily concentrations in food items (e.g., short grass, arthropods etc.)
        :param tox_cbt_mamm a panda series representing the list of toxicity measures

        :NOTE this method is used to replicate the OPP TED Excel model worksheet 'Min/Max rate - dietary conc results' columns D - N lines 3 - 54
              (this method is a temporary solution for the need to populate a panda series with mixed data types;
              when a more elegant solution comes available this method can simply be replaced without other changes - or so I think)

              for example: the following line of code performs the same function when all series values are floats
              exceedances = [(self.time_sesries[0][i] > self.tox_series[0][j]).sum() for i in range(11) for j in range(13)]

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        self.num_simulation_days = 15

        eec_ts_1 = pd.Series([10.,9.,8.,7.,6.,5.,4.,3.,2.,1.,0.9,0.8,0.7,0.6,0.5])
        eec_ts_2 = pd.Series([10.,9.,8.,7.,6.,5.,4.,3.,2.,1.,0.9,0.8,0.7,0.6,0.5])
        eec_ts_3 = pd.Series([10.,9.,8.,7.,6.,5.,4.,3.,2.,1.,0.9,0.8,0.7,0.6,0.5])
        eec_ts_4 = pd.Series([10.,9.,8.,7.,6.,5.,4.,3.,2.,1.,0.9,0.8,0.7,0.6,0.5])

        na_series = pd.Series(self.num_simulation_days * ['NA'])

        expected_results = pd.Series([9, 8, 7, 8, 9, 8, 7, 9, 8, 7, 9, 8, 7, 8, 9, 8, 7, 9, 8, 7,
                                      9, 8, 7, 8, 9, 8, 7, 9, 8, 7, 9, 8, 7, 8, 9, 8, 7, 9, 8, 7,
                                      'NA','NA','NA','NA','NA','NA','NA','NA','NA','NA',], dtype='object')
        result = pd.Series([], dtype='object')

        try:
            num_ts = 5
            num_tox = 10
            tox_cbt_mamm = pd.Series([1., 2., 3., 2., 1., 2., 3., 1., 2., 3.])
            eec_ts_upper_min_1 = pd.Series([[eec_ts_1], [eec_ts_2], [eec_ts_3], [eec_ts_4], [na_series]])

            result = ted_empty.sum_exceedances(num_ts, num_tox, eec_ts_upper_min_1, tox_cbt_mamm)
            npt.assert_array_equal(result, expected_results, err_msg='', verbose=True)

        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_eec_tox_frac(self):
            """
            :description calculates the ratio of toxicity measure and maximum of daily food item concentrations
            :param num_eec_max number of food items included
            :param num_tox number of toxicity measures to be processed
            :param max_eec_series a panda series representing an aggregation of maximum concentrations in food items (e.g., short grass, arthropods etc.)
            :param tox_series a panda series representing the list of toxicity measures

            :return:
            """

            # create empty pandas dataframes to create empty object for this unittest
            ted_empty = self.create_ted_object()

            expected_results = pd.Series([0.2, 0.2, 0.2, 'NA', 8.0, 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', 'NA',
                                          1.0, 1.0, 1.0, 'NA', 40., 'NA', 0.02, 0.02, 0.02, 'NA', 0.8, 'NA'], dtype='object')
            result = pd.Series([], dtype='object')

            try:
                num_tox = 6
                num_eec_max = 4
                tox_series = pd.Series([1., 1., 1., np.nan, 40., np.nan]) # the toxicity numbers come from input as NaN
                max_eec_series = pd.Series([5.0, 'NA', 1.0, 50.0, ])

                result = ted_empty.calc_eec_tox_frac(num_eec_max, num_tox, max_eec_series, tox_series)
                npt.assert_array_equal(result, expected_results, err_msg='', verbose=True)

            finally:
                tab = [result, expected_results]
                print("\n")
                print(inspect.currentframe().f_code.co_name)
                print(tabulate(tab, headers='keys', tablefmt='rst'))
            return

    def test_calc_maxeec_distance(self):
        """
        :description calculates the distance from the source area that plant toxicity thresholds occur
        :param toxicity_to_app_ratio; ratio of toxicity measure to scenarios application rate
        :param param_a; spray drift parameter a
        :param param_b; spray drift parameter b
        :param param_c; spray drift parameter c
        :param max_drift_distance;

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        ted_empty = self.create_ted_object()

        expected_results = pd.Series([2600., 2348.357448005348, 110.46619534267889, 39.008907082694385, 0.0, 'NA'], dtype='object')
        result = pd.Series([], dtype='object')

        try:
            toxicity_to_apprate_ratio = pd.Series([0.002, 0.02, 0.2, 0.35, 3., 'NA'])
            param_a = 0.0292
            param_b = 0.822
            param_c = 0.6539
            max_drift_distance = 2600.

            result = ted_empty.calc_maxeec_distance(toxicity_to_apprate_ratio, param_a, param_b, param_c, max_drift_distance)
            npt.assert_array_equal(result, expected_results, err_msg='', verbose=True)

        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return


