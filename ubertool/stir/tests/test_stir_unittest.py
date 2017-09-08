import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
from tabulate import tabulate
import unittest

# #find parent directory and import model
# parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(parentddir)
from ..stir_exe import Stir

test = {}

class TestStir(unittest.TestCase):
    """
    Unit tests for Stir.
    """
    print("stir unittests conducted at " + str(datetime.datetime.today()))

    def setup(self):
        """
        setup routine for stir unittests
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open stir qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        """
        teardown routine for stir unittest
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file


    def create_stir_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty stir object
        stir_empty = Stir(df_empty, df_empty)
        return stir_empty

    def test_stir_calc_sat_air_conc(self):
        """
        unittest for function stir.CalcSatAirConc
        eq. 1 saturated air concentration in mg/m^3
        :return:
        """
        # self.out_sat_air_conc = (self.vapor_pressure * self.molecular_weight * conv)/(pressure * air_vol)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.086105, 0.4238209,0.048933]
        try:
            stir_empty.vapor_pressure = pd.Series([0.000008, .00008, .0000048], dtype='float')
            stir_empty.molecular_weight = pd.Series([200., 98.443, 189.433], dtype='float')
            result = stir_empty.calc_sat_air_conc()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_inh_rate_avian(self):
        """
        unittest for function stir.CalcInhRateAvian
        eq. 2 Avian inhalation rate
        :return:
        """
        # self.out_inh_rate_avian = magic1 * (self.body_weight_assessed_bird**magic2) * conversion * activity_factor

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [5090.9373, 29977.66, 52038.63]
        try:
            stir_empty.body_weight_assessed_bird = pd.Series([0.05, 0.5, 1.0234], dtype='float')
            result = stir_empty.calc_inh_rate_avian()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_vid_avian(self):
        """
        unittest for function stir.CalcVidAvian
        eq. 3  Maximum avian vapor inhalation dose
        :return:
        """
        # self.out_vid_avian = (self.out_sat_air_conc * self.out_inh_rate_avian * duration_hours)/(conversion_factor * self.body_weight_assessed_bird)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.04, 0.0008686, 0.000532904]
        try:
            stir_empty.out_sat_air_conc = pd.Series([200., 100., 397.994], dtype='float')
            stir_empty.out_inh_rate_avian = pd.Series([10., 4.343, 1.3845], dtype='float')
            stir_empty.body_weight_assessed_bird = pd.Series([0.05, 0.5, 1.034], dtype='float')
            result = stir_empty.calc_vid_avian()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_inh_rate_mammal(self):
        """
        unittest for function stir.CalcInhRateMammal
        eq. 4 Mammalian inhalation rate
        :return:
        """
        # self.out_inh_rate_mammal = magic1 * (self.body_weight_assessed_mammal**magic2) * minutes_conversion * activity_factor

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [9044.4821, 63984.25, 127862.3]
        try:
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08, 0.923, 2.193], dtype='float')
            result = stir_empty.calc_inh_rate_mammal()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_vid_mammal(self):
        """
        unittest for function stir.CalcVidMammal
        eq. 5 Maximum mammalian vapor inhalation dose
        :return:
        """
        # self.out_vid_mammal = (self.out_sat_air_conc * self.out_inh_rate_mammal * duration_hours)/(conversion_factor * self.body_weight_assessed_mammal)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.0625, 0.0343144, 0.000163607]
        try:
            stir_empty.out_sat_air_conc = pd.Series([100., 329.432, 45.777], dtype='float')
            stir_empty.out_inh_rate_mammal = pd.Series([50., 83.33, 12.291], dtype='float')
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08, 0.8, 3.439], dtype='float')
            result = stir_empty.calc_vid_mammal()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_conc_air(self):
        """
        unittest for function stir.CalcConcAir
        eq. 6 Air column concentration after spray
        :return:
        """
        # conversion_factor = 100. #cm/m
        # cf_g_lbs = 453.59237
        # cf_mg_g = 1000.
        # cf_cm2_acre = 40468564.2
        # self.out_air_conc = ((self.application_rate*cf_g_lbs*cf_mg_g)/cf_cm2_acre)/(self.column_height * conversion_factor)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.000112085, 0.0000587687, 0.001816198]
        try:
            stir_empty.application_rate = pd.Series([2., 12.2293, 4.7639], dtype='float')
            stir_empty.column_height = pd.Series([2., 23.324, 0.294 ], dtype='float')
            result = stir_empty.calc_conc_air()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_sid_avian(self):
        """
        unittest for function stir.CalcSidAvian
        eq. 7 Avian spray droplet inhalation dose
        :return:
        """
        # self.out_sid_avian = (self.out_air_conc * self.out_inh_rate_avian * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_bird)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [468.75, 4.872462, 2341.357]
        try:
            stir_empty.out_air_conc = pd.Series([150., 82.343, 3832.342], dtype='float')
            stir_empty.out_inh_rate_avian = pd.Series([10., 2.023, 21.8392], dtype='float')
            stir_empty.direct_spray_duration = pd.Series([0.5, 1.5, 4.34], dtype='float')
            stir_empty.spray_drift_fraction = pd.Series([0.75, 0.234, 0.823], dtype='float')
            stir_empty.body_weight_assessed_bird = pd.Series([0.02, 0.2, 2.128], dtype='float')
            result = stir_empty.calc_sid_avian()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_sid_mammal(self):
        """
        unittest for function stir.CalcSidMammal
        eq. 8 Mammalian spray droplet inhalation dose
        :return:
        """
        # self.out_sid_mammal = (self.out_air_conc * self.out_inh_rate_mammal * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_mammal)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [585.9375, 26.88064, 52.017548]
        try:
            stir_empty.out_air_conc = pd.Series([150., 84.234, 394.223], dtype='float')
            stir_empty.out_inh_rate_mammal = pd.Series([50., 34.734, 10.293], dtype='float')
            stir_empty.direct_spray_duration = pd.Series([0.5, 1.5, 3.423], dtype='float')
            stir_empty.spray_drift_fraction = pd.Series([0.75, 0.294, 0.493], dtype='float')
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08, 0.8, 2.194], dtype='float')
            result = stir_empty.calc_sid_mammal()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_convert_mammal_inh_lc50_to_ld50(self):
        """
        unittest for function stir.CalcConvertMammalInhalationLC50toLD50
        eq. 9 Conversion of mammalian LC50 to LD50
        :return:
        """
        # activity_factor = 1.
        # absorption = 1.
        # self.out_mammal_inhalation_ld50 = self.mammal_inhalation_lc50 * absorption * ((self.out_inh_rate_mammal * 0.001)/self.body_weight_tested_mammal) * self.duration_mammal_inhalation_study * activity_factor

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.14286, 0.04316245, 0.1722205]
        try:
            stir_empty.mammal_inhalation_lc50 = pd.Series([0.5, 0.83, 2.834], dtype='float')
            stir_empty.out_inh_rate_mammal = pd.Series([50., 5.543, 73.334], dtype='float')
            stir_empty.body_weight_tested_mammal = pd.Series([0.35, 1.292, 4.221], dtype='float')
            stir_empty.duration_mammal_inhalation_study = pd.Series([2., 12.1212, 3.4978], dtype='float')
            result = stir_empty.calc_convert_mammal_inhalation_lc50_to_ld50()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_adjusted_mammal_inhalation_ld50(self):
        """
        unittest for function stir.CalcAdjustedMammalInhalationLD50
        eq. 10 Adjusted mammalian inhalation LD50
        :return:
        """
        # self.out_adjusted_mammal_inhalation_ld50 = self.out_mammal_inhalation_ld50 * (self.body_weight_tested_mammal/self.body_weight_assessed_mammal)**magicpower

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [2.3003, 14.62509, 3.941703]
        try:
            stir_empty.out_mammal_inhalation_ld50 = pd.Series([2., 13.834, 3.840], dtype='float')
            stir_empty.body_weight_tested_mammal = pd.Series([0.35, 3.54, 8.209], dtype='float')
            stir_empty.body_weight_assessed_mammal = pd.Series([0.2, 2.834, 7.394], dtype='float')
            result = stir_empty.calc_adjusted_mammal_inhalation_ld50()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_estimated_avian_inhalation_ld50(self):
        """
        unittest for function stir.CalcEstimatedAvianInhalationLD50
        eq. 11 Estimated avian inhalation LD50
        :return:
        """
        # three_five = 3.5
        # self.out_estimated_avian_inhalation_ld50 = (self.avian_oral_ld50 * self.out_mammal_inhalation_ld50)/(three_five * self.mammal_oral_ld50)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [14.2857, 27.83401, 38.32042]
        try:
            stir_empty.avian_oral_ld50 = pd.Series([500., 175., 750.], dtype='float')
            stir_empty.out_mammal_inhalation_ld50 = pd.Series([2., 5.5, 10.43], dtype='float')
            stir_empty.mammal_oral_ld50 = pd.Series([20., 9.88, 58.324], dtype='float')
            result = stir_empty.calc_estimated_avian_inhalation_ld50()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_calc_adjusted_avian_inhalation_ld50(self):
        """
        unittest for function stir.CalcAdjustedAvianInhalationLD50
        eq. 12 Adjusted avian inhalation LD50
        :return:
        """
        # self.out_adjusted_avian_inhalation_ld50 = self.out_estimated_avian_inhalation_ld50 * (self.body_weight_assessed_bird/self.body_weight_tested_bird)**(self.mineau_scaling_factor - 1)

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.1, 0.3510674, 9.585158]
        try:
            stir_empty.out_estimated_avian_inhalation_ld50 = pd.Series([0.5, 1.194, 8.339], dtype='float')
            stir_empty.body_weight_assessed_bird = pd.Series([0.02, 0.25, 2.334], dtype='float')
            stir_empty.body_weight_tested_bird = pd.Series([0.1, 0.435, 1.992], dtype='float')
            stir_empty.mineau_scaling_factor = pd.Series([2., 3.21, 1.879], dtype='float')
            result = stir_empty.calc_adjusted_avian_inhalation_ld50()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_ratio_vid_avian(self):
        """
        unittest for function stir.ReturnRatioVidAvian
        results #1: Ratio of avian vapor dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_vid_avian = self.out_vid_avian/self.out_adjusted_avian_inhalation_ld50

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.008, 0.0352941, 0.1453338]
        try:
            stir_empty.out_vid_avian = pd.Series([0.04, 0.456, 1.291], dtype='float')
            stir_empty.out_adjusted_avian_inhalation_ld50 = pd.Series([5., 12.92, 8.883], dtype='float')
            result = stir_empty.return_ratio_vid_avian()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_loc_vid_avian(self):
        """
        unittest for function stir.ReturnLocVidAvian
        results #2: Level of Concern for avian vapor phase risk
        :return:
        """
        # if self.out_ratio_vid_avian < 0.1:
        #    self.out_loc_vid_avian = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_vid_avian = 'Proceed to Refinements'

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = pd.Series(["Exposure not Likely Significant", "Proceed "
                            "to Refinements", "Exposure not Likely Significant"])
        try:
            stir_empty.out_ratio_vid_avian = pd.Series([0.09, 0.2, 0.002], dtype='float')
            result = stir_empty.return_loc_vid_avian()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_ratio_sid_avian(self):
        """
        unittest for function stir.ReturnRatioSidAvian
        results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_sid_avian = self.out_sid_avian/self.out_adjusted_avian_inhalation_ld50

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.4, 1.989259, 0.09725747]
        try:
            stir_empty.out_sid_avian = pd.Series([4., 9.445, 1.993], dtype='float')
            stir_empty.out_adjusted_avian_inhalation_ld50 = pd.Series([10., 4.748, 20.492], dtype='float')
            result = stir_empty.return_ratio_sid_avian()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_loc_sid_avian(self):
        """
        unittest for function stir.ReturnLocSidAvian
        results #4: Level of Concern for avian droplet inhalation risk
        :return:
        """
        # if self.out_ratio_sid_avian < 0.1:
        #    self.out_loc_sid_avian = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_sid_avian = 'Proceed to Refinements'

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = pd.Series(["Exposure not Likely Significant", "Proceed "
                           "to Refinements", "Exposure not Likely Significant"])
        try:
            stir_empty.out_ratio_sid_avian = pd.Series([0.099, 0.2, 0.0099], dtype='float')
            result = stir_empty.return_loc_sid_avian()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_ratio_vid_mammal(self):
        """
        unittest for function stir.ReturnRatioVidMammal
        results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_vid_mammal = self.out_vid_mammal/self.out_adjusted_mammal_inhalation_ld50

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [2.0, 0.0211981, 1.127584]
        try:
            stir_empty.out_vid_mammal = pd.Series([4., 0.092, 12.329], dtype='float')
            stir_empty.out_adjusted_mammal_inhalation_ld50 = pd.Series([2., 4.34, 10.934], dtype='float')
            result = stir_empty.return_ratio_vid_mammal()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_loc_vid_mammal(self):
        """
        unittest for function stir.ReturnLocVidMammal
        results #6: Level of Concern for mammalian vapor phase risk
        :return:
        """
        # if self.out_ratio_vid_mammal < 0.1:
        #    self.out_loc_vid_mammal = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_vid_mammal = 'Proceed to Refinements'

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = pd.Series(["Exposure not Likely Significant", "Proceed "
                           "to Refinements", "Exposure not Likely Significant"])
        try:
            stir_empty.out_ratio_vid_mammal = pd.Series([0.084, 0.3, 0.01], dtype='float')
            result = stir_empty.return_loc_vid_mammal()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_ratio_sid_mammal(self):
        """
        unittest for function stir.ReturnRatioSidMammal
        results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_sid_mammal = self.out_sid_mammal/self.out_adjusted_mammal_inhalation_ld50

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = [0.25, 2.327008, 0.284566]
        try:
            stir_empty.out_sid_mammal = pd.Series([0.5, 2.3298, 1.233], dtype='float')
            stir_empty.out_adjusted_mammal_inhalation_ld50 = pd.Series([2., 1.0012, 4.3329], dtype='float')
            result = stir_empty.return_ratio_sid_mammal()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_stir_return_loc_sid_mammal(self):
        """
        unittest for function stir.ReturnLocSidMammal
        results #8: Level of Concern for mammaliam droplet inhalation risk
        :return:
        """
        # if self.out_ratio_sid_mammal < 0.1:
        #    self.out_loc_sid_mammal = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_sid_mammal = 'Proceed to Refinements'

        # create empty pandas dataframes to create empty object for this unittest
        stir_empty = self.create_stir_object()

        expected_results = pd.Series(["Exposure not Likely Significant", "Proceed "
                           "to Refinements", "Exposure not Likely Significant"])
        try:
            stir_empty.out_ratio_sid_mammal = pd.Series([0.056, 0.6, 0.01001], dtype='float')
            result = stir_empty.return_loc_sid_mammal()
            pdt.assert_series_equal(result, expected_results, test)
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
