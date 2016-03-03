import logging
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
import unittest
#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from stir_exe import Stir

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
stir_empty = Stir(df_empty, df_empty)

test = {}


class TestStir(unittest.TestCase):
    """
    Unit tests for Stir.
    """

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

    def test_calc_sat_air_conc(self):
        """
        unittest for function stir.CalcSatAirConc
        eq. 1 saturated air concentration in mg/m^3
        :return:
        """
        # self.out_sat_air_conc = (self.vapor_pressure * self.molecular_weight * conv)/(pressure * air_vol)
        try:
            stir_empty.vapor_pressure = pd.Series([0.000008])
            stir_empty.molecular_weight = pd.Series([200.])
            result = stir_empty.calc_sat_air_conc()
            npt.assert_array_almost_equal(result, 0.086105, 4, '', True)
        finally:
            pass
        return

    def test_calc_inh_rate_avian(self):
        """
        unittest for function stir.CalcInhRateAvian
        eq. 2 Avian inhalation rate
        :return:
        """
        # self.out_inh_rate_avian = magic1 * (self.body_weight_assessed_bird**magic2) * conversion * activity_factor
        try:
            stir_empty.body_weight_assessed_bird = pd.Series([0.05])
            result = stir_empty.calc_inh_rate_avian()
            npt.assert_array_almost_equal(result, 5090.9373, 4, '', True)
        finally:
            pass
        return

    def test_calc_vid_avian(self):
        """
        unittest for function stir.CalcVidAvian
        eq. 3  Maximum avian vapor inhalation dose
        :return:
        """
        # self.out_vid_avian = (self.out_sat_air_conc * self.out_inh_rate_avian * duration_hours)/(conversion_factor * self.body_weight_assessed_bird)
        try:
            stir_empty.sat_air_conc = pd.Series([200.])
            stir_empty.inh_rate_avian = pd.Series([10.])
            stir_empty.body_weight_assessed_bird = pd.Series([0.05])
            result = stir_empty.calc_vid_avian()
            npt.assert_array_almost_equal(result, 0.04, 4, '', True)
        finally:
            pass
        return

    def test_calc_inh_rate_mammal(self):
        """
        unittest for function stir.CalcInhRateMammal
        eq. 4 Mammalian inhalation rate
        :return:
        """
        # self.out_inh_rate_mammal = magic1 * (self.body_weight_assessed_mammal**magic2) * minutes_conversion * activity_factor
        try:
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08])
            result = stir_empty.calc_inh_rate_mammal()
            npt.assert_array_almost_equal(result, 9044.4821, 4, '', True)
        finally:
            pass
        return

    def test_calc_vid_mammal(self):
        """
        unittest for function stir.CalcVidMammal
        eq. 5 Maximum mammalian vapor inhalation dose
        :return:
        """
        # self.out_vid_mammal = (self.out_sat_air_conc * self.out_inh_rate_mammal * duration_hours)/(conversion_factor * self.body_weight_assessed_mammal)
        try:
            stir_empty.sat_air_conc = pd.Series([100.])
            stir_empty.inh_rate_mammal = pd.Series([50.])
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08])
            result = stir_empty.calc_vid_mammal()
            npt.assert_array_almost_equal(result, 0.0625, 4, '', True)
        finally:
            pass
        return

    def test_calc_conc_air(self):
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
        try:
            stir_empty.application_rate = pd.Series([2.])
            stir_empty.column_height = pd.Series([2.])
            result = stir_empty.calc_conc_air()
            npt.assert_array_almost_equal(result, 0.0001121, 4, '', True)
        finally:
            pass
        return

    def test_calc_sid_avian(self):
        """
        unittest for function stir.CalcSidAvian
        eq. 7 Avian spray droplet inhalation dose
        :return:
        """
        # self.out_sid_avian = (self.out_air_conc * self.out_inh_rate_avian * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_bird)
        try:
            stir_empty.air_conc = pd.Series([150.])
            stir_empty.inh_rate_avian = pd.Series([10.])
            stir_empty.direct_spray_duration = pd.Series([0.5])
            stir_empty.spray_drift_fraction = pd.Series([0.75])
            stir_empty.body_weight_assessed_bird = pd.Series([0.02])
            result = stir_empty.calc_sid_avian()
            npt.assert_array_almost_equal(result, 468.75, 4, '', True)
        finally:
            pass
        return

    def test_calc_sid_mammal(self):
        """
        unittest for function stir.CalcSidMammal
        eq. 8 Mammalian spray droplet inhalation dose
        :return:
        """
        # self.out_sid_mammal = (self.out_air_conc * self.out_inh_rate_mammal * self.direct_spray_duration * self.spray_drift_fraction)/(60.0 * self.body_weight_assessed_mammal)
        try:
            stir_empty.air_conc = pd.Series([150.])
            stir_empty.inh_rate_mammal = pd.Series([50.])
            stir_empty.direct_spray_duration = pd.Series([0.5])
            stir_empty.spray_drift_fraction = pd.Series([0.75])
            stir_empty.body_weight_assessed_mammal = pd.Series([0.08])
            result = stir_empty.calc_sid_mammal()
            npt.assert_array_almost_equal(result, 585.9375, 4, '', True)
        finally:
            pass
        return

    def test_calc_convert_mammal_inh_lc50_to_ld50(self):
        """
        unittest for function stir.CalcConvertMammalInhalationLC50toLD50
        eq. 9 Conversion of mammalian LC50 to LD50
        :return:
        """
        # activity_factor = 1.
        # absorption = 1.
        # self.out_mammal_inhalation_ld50 = self.mammal_inhalation_lc50 * absorption * ((self.out_inh_rate_mammal * 0.001)/self.body_weight_tested_mammal) * self.duration_mammal_inhalation_study * activity_factor
        try:
            stir_empty.mammal_inhalation_lc50 = pd.Series([0.5])
            stir_empty.inh_rate_mammal = pd.Series([50.])
            stir_empty.body_weight_tested_mammal = pd.Series([0.35])
            stir_empty.duration_mammal_inhalation_study = pd.Series([2.])
            result = stir_empty.calc_convert_mammal_inhalation_lc50_to_ld50()
            npt.assert_array_almost_equal(result, 0.14286, 4, '', True)
        finally:
            pass
        return

    def test_calc_adjusted_mammal_inhalation_ld50(self):
        """
        unittest for function stir.CalcAdjustedMammalInhalationLD50
        eq. 10 Adjusted mammalian inhalation LD50
        :return:
        """
        # self.out_adjusted_mammal_inhalation_ld50 = self.out_mammal_inhalation_ld50 * (self.body_weight_tested_mammal/self.body_weight_assessed_mammal)**magicpower
        try:
            stir_empty.mammal_inhalation_ld50 = pd.Series([2.])
            stir_empty.body_weight_tested_mammal = pd.Series([0.35])
            stir_empty.body_weight_assessed_mammal = pd.Series([0.2])
            result = stir_empty.calc_adjusted_mammal_inhalation_ld50()
            npt.assert_array_almost_equal(result, 2.3003, 4, '', True)
        finally:
            pass
        return

    def test_calc_estimated_avian_inhalation_ld50(self):
        """
        unittest for function stir.CalcEstimatedAvianInhalationLD50
        eq. 11 Estimated avian inhalation LD50
        :return:
        """
        # three_five = 3.5
        # self.out_estimated_avian_inhalation_ld50 = (self.avian_oral_ld50 * self.out_mammal_inhalation_ld50)/(three_five * self.mammal_oral_ld50)
        try:
            stir_empty.avian_oral_ld50 = pd.Series([500.])
            stir_empty.mammal_inhalation_ld50 = pd.Series([2.])
            stir_empty.mammal_oral_ld50 = pd.Series([20.])
            result = stir_empty.calc_estimated_avian_inhalation_ld50()
            npt.assert_array_almost_equal(result, 14.2857, 4, '', True)
        finally:
            pass
        return

    def test_calc_adjusted_avian_inhalation_ld50(self):
        """
        unittest for function stir.CalcAdjustedAvianInhalationLD50
        eq. 12 Adjusted avian inhalation LD50
        :return:
        """
        # self.out_adjusted_avian_inhalation_ld50 = self.out_estimated_avian_inhalation_ld50 * (self.body_weight_assessed_bird/self.body_weight_tested_bird)**(self.mineau_scaling_factor - 1)
        try:
            stir_empty.estimated_avian_inhalation_ld50 = pd.Series([0.5])
            stir_empty.body_weight_assessed_bird = pd.Series([0.02])
            stir_empty.body_weight_tested_bird = pd.Series([0.1])
            stir_empty.mineau_scaling_factor = pd.Series([2.])
            result = stir_empty.calc_adjusted_avian_inhalation_ld50()
            npt.assert_array_almost_equal(result, 0.1, 4, '', True)
        finally:
            pass
        return

    def test_return_ratio_vid_avian(self):
        """
        unittest for function stir.ReturnRatioVidAvian
        results #1: Ratio of avian vapor dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_vid_avian = self.out_vid_avian/self.out_adjusted_avian_inhalation_ld50
        try:
            stir_empty.vid_avian = pd.Series([0.04])
            stir_empty.adjusted_avian_inhalation_ld50 = pd.Series([5.])
            result = stir_empty.return_ratio_vid_avian()
            npt.assert_array_almost_equal(result, 0.008, 4, '', True)
        finally:
            pass
        return

    def test_return_loc_vid_avian(self):
        """
        unittest for function stir.ReturnLocVidAvian
        results #2: Level of Concern for avian vapor phase risk
        :return:
        """
        # if self.out_ratio_vid_avian < 0.1:
        #    self.out_loc_vid_avian = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_vid_avian = 'Proceed to Refinements'
        try:
            stir_empty.ratio_vid_avian = pd.Series([0.2])
            result = stir_empty.return_loc_vid_avian()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_return_ratio_sid_avian(self):
        """
        unittest for function stir.ReturnRatioSidAvian
        results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_sid_avian = self.out_sid_avian/self.out_adjusted_avian_inhalation_ld50
        try:
            stir_empty.sid_avian = pd.Series([4.])
            stir_empty.adjusted_avian_inhalation_ld50 = pd.Series([10.])
            result = stir_empty.return_ratio_sid_avian()
            npt.assert_array_almost_equal(result, 0.4, 4, '', True)
        finally:
            pass
        return

    def test_return_loc_sid_avian(self):
        """
        unittest for function stir.ReturnLocSidAvian
        results #4: Level of Concern for avian droplet inhalation risk
        :return:
        """
        # if self.out_ratio_sid_avian < 0.1:
        #    self.out_loc_sid_avian = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_sid_avian = 'Proceed to Refinements'
        try:
            stir_empty.ratio_sid_avian = pd.Series([0.2])
            result = stir_empty.return_loc_sid_avian()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_return_ratio_vid_mammal(self):
        """
        unittest for function stir.ReturnRatioVidMammal
        results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_vid_mammal = self.out_vid_mammal/self.out_adjusted_mammal_inhalation_ld50
        try:
            stir_empty.vid_mammal = pd.Series([4.])
            stir_empty.adjusted_mammal_inhalation_ld50 = pd.Series([2.])
            result = stir_empty.return_ratio_vid_mammal()
            print(result)
            npt.assert_array_almost_equal(result, 2., 4, '', True)
        finally:
            pass
        return

    def test_return_loc_vid_mammal(self):
        """
        unittest for function stir.ReturnLocVidMammal
        results #6: Level of Concern for mammalian vapor phase risk
        :return:
        """
        # if self.out_ratio_vid_mammal < 0.1:
        #    self.out_loc_vid_mammal = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_vid_mammal = 'Proceed to Refinements'
        try:
            stir_empty.ratio_vid_mammal = pd.Series([0.3])
            result = stir_empty.return_loc_vid_mammal()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_return_ratio_sid_mammal(self):
        """
        unittest for function stir.ReturnRatioSidMammal
        results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
        :return:
        """
        # self.out_ratio_sid_mammal = self.out_sid_mammal/self.out_adjusted_mammal_inhalation_ld50
        try:
            stir_empty.sid_mammal = pd.Series([0.5])
            stir_empty.adjusted_mammal_inhalation_ld50 = pd.Series([2.])
            result = stir_empty.return_ratio_sid_mammal()
            npt.assert_array_almost_equal(result, 0.25, 4, '', True)
        finally:
            pass
        return

    def test_return_loc_sid_mammal(self):
        """
        unittest for function stir.ReturnLocSidMammal
        results #8: Level of Concern for mammaliam droplet inhalation risk
        :return:
        """
        # if self.out_ratio_sid_mammal < 0.1:
        #    self.out_loc_sid_mammal = 'Exposure not Likely Significant'
        # else:
        #    self.out_loc_sid_mammal = 'Proceed to Refinements'
        try:
            stir_empty.ratio_sid_mammal = pd.Series([0.6])
            result = stir_empty.return_loc_sid_mammal()
            exp = pd.Series("Proceed to Refinements")
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return


# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
