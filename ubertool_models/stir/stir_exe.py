from __future__ import division
import logging
import os.path
import pandas as pd
import sys
#find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs

#print(sys.path)
#print(os.path)


class StirInputs(ModelSharedInputs):
    """
    Input class for STIR.
    """

    def __init__(self):
        """Class representing the inputs for STIR"""
        super(StirInputs, self).__init__()
        self.application_rate = pd.Series([], dtype="float")
        self.column_height = pd.Series([], dtype="float")
        self.spray_drift_fraction = pd.Series([], dtype="float")
        self.direct_spray_duration = pd.Series([], dtype="float")
        self.molecular_weight = pd.Series([], dtype="float")
        self.vapor_pressure = pd.Series([], dtype="float")
        self.avian_oral_ld50 = pd.Series([], dtype="float")
        self.body_weight_assessed_bird = pd.Series([], dtype="float")
        self.body_weight_tested_bird = pd.Series([], dtype="float")
        self.mineau_scaling_factor = pd.Series([], dtype="float")
        self.mammal_inhalation_lc50 = pd.Series([], dtype="float")
        self.duration_mammal_inhalation_study = pd.Series([], dtype="float")
        self.body_weight_assessed_mammal = pd.Series([], dtype="float")
        self.body_weight_tested_mammal = pd.Series([], dtype="float")
        self.mammal_oral_ld50 = pd.Series([], dtype="float")


class StirOutputs(object):
    """
    Output class for STIR.
    """

    def __init__(self):
        """Class representing the outputs for STIR"""
        super(StirOutputs, self).__init__()
        self.out_sat_air_conc = pd.Series(name="out_sat_air_conc")
        self.out_inh_rate_avian = pd.Series(name="out_inh_rate_avian")
        self.out_vid_avian = pd.Series(name="out_vid_avian")
        self.out_inh_rate_mammal = pd.Series(name="out_inh_rate_mammal")
        self.out_vid_mammal = pd.Series(name="out_vid_mammal")
        self.out_ar2 = pd.Series(name="out_ar2")
        self.out_air_conc = pd.Series(name="out_air_conc")
        self.out_sid_avian = pd.Series(name="out_sid_avian")
        self.out_sid_mammal = pd.Series(name="out_sid_mammal")
        self.out_cf = pd.Series(name="out_cf")
        self.out_mammal_inhalation_ld50 = pd.Series(name="out_mammal_inhalation_ld50")
        self.out_adjusted_mammal_inhalation_ld50 = pd.Series(name="out_adjusted_mammal_inhalation_ld50")
        self.out_estimated_avian_inhalation_ld50 = pd.Series(name="out_estimated_avian_inhalation_ld50")
        self.out_adjusted_avian_inhalation_ld50 = pd.Series(name="out_adjusted_avian_inhalation_ld50")
        self.out_ratio_vid_avian = pd.Series(name="out_ratio_vid_avian")
        self.out_ratio_sid_avian = pd.Series(name="out_ratio_sid_avian")
        self.out_ratio_vid_mammal = pd.Series(name="out_ratio_vid_mammal")
        self.out_ratio_sid_mammal = pd.Series(name="out_ratio_sid_mammal")
        self.out_loc_vid_avian = pd.Series(name="out_loc_vid_avian")
        self.out_loc_sid_avian = pd.Series(name="out_loc_sid_avian")
        self.out_loc_vid_mammal = pd.Series(name="out_loc_vid_mammal")
        self.out_loc_sid_mammal = pd.Series(name="out_loc_sid_mammal")


class Stir(UberModel, StirInputs, StirOutputs):
    """
    Estimate inhalation risk of chemicals to birds and mammals.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Terrplant model and containing all its methods"""
        super(Stir, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Run the model's methods to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj, self)
        self.pd_obj_out = self.populate_outputs(self)
        self.run_methods()
        self.fill_output_dataframe(self)

    def run_methods(self):
        """ Execute all algorithm methods for model logic """
        try:
            self.calc_sat_air_conc()  # eq. 1
            self.calc_inh_rate_avian()  # eq. 2
            self.calc_vid_avian()  # eq. 3
            self.calc_inh_rate_mammal()  # eq. 4
            self.calc_vid_mammal()  # eq. 5
            self.calc_conc_air()  # eq. 6
            self.calc_sid_avian()  # eq. 7
            self.calc_sid_mammal()  # eq. 8
            self.calc_convert_mammal_inhalation_lc50_to_ld50()  # eq. 9
            self.calc_adjusted_mammal_inhalation_ld50()  # eq. 10
            self.calc_estimated_avian_inhalation_ld50()  # eq. 11
            self.calc_adjusted_avian_inhalation_ld50()  # eq. 12
            self.return_ratio_vid_avian()  # results #1
            self.return_loc_vid_avian()  # results #2
            self.return_ratio_sid_avian()  # results #3
            self.return_loc_sid_avian()  # results #4
            self.return_ratio_vid_mammal()  # results #5
            self.return_loc_vid_mammal()  # results #6
            self.return_ratio_sid_mammal()  # results #7
            self.return_loc_sid_mammal()  # results #8
        except:
            pass

    # Begin model methods
    def calc_sat_air_conc(self):
        """
        # eq. 1 saturated air concentration in mg/m^3
        """
        air_vol = 24.45
        pressure = 760.0
        conv = 1000000.0
        self.out_sat_air_conc = (self.vapor_pressure * self.molecular_weight * conv) / (pressure * air_vol)
        return self.out_sat_air_conc

    def calc_inh_rate_avian(self):
        """
        eq. 2 Avian inhalation rate
        """
        magic1 = 284.
        magic2 = 0.77
        conversion = 60.
        activity_factor = 3.
        self.out_inh_rate_avian = magic1 * (self.body_weight_assessed_bird ** magic2) * conversion * activity_factor
        return self.out_inh_rate_avian

    def calc_vid_avian(self):
        """
        eq. 3  Maximum avian vapor inhalation dose
        """
        duration_hours = 1.
        conversion_factor = 1000000.  # cm3/m3
        # 1 (hr) is duration of exposure
        self.out_vid_avian = (self.out_sat_air_conc * self.out_inh_rate_avian * duration_hours) / (
            conversion_factor * self.body_weight_assessed_bird)
        return self.out_vid_avian

    def calc_inh_rate_mammal(self):
        """
        eq. 4 Mammalian inhalation rate
        """
        magic1 = 379.0
        magic2 = 0.8
        minutes_conversion = 60.
        activity_factor = 3.
        self.out_inh_rate_mammal = magic1 * (
            self.body_weight_assessed_mammal ** magic2) * minutes_conversion * activity_factor
        return self.out_inh_rate_mammal

    def calc_vid_mammal(self):
        """
        eq. 5 Maximum mammalian vapor inhalation dose
        """
        duration_hours = 1.
        conversion_factor = 1000000.
        # 1 hr = duration of exposure
        self.out_vid_mammal = (self.out_sat_air_conc * self.out_inh_rate_mammal * duration_hours) / (
            conversion_factor * self.body_weight_assessed_mammal)
        return self.out_vid_mammal

    def calc_conc_air(self):
        """
        eq. 6 Air column concentration after spray
        """
        conversion_factor = 100.  # cm/m
        # conversion of application rate from lbs/acre to mg/cm2
        cf_g_lbs = 453.59237
        cf_mg_g = 1000.
        cf_cm2_acre = 40468564.2
        self.out_ar2 = (self.application_rate * cf_g_lbs * cf_mg_g) / cf_cm2_acre
        self.out_air_conc = self.out_ar2 / (self.column_height * conversion_factor)
        return self.out_air_conc

    def calc_sid_avian(self):
        """
        eq. 7 Avian spray droplet inhalation dose
        """
        self.out_sid_avian = (self.out_air_conc * self.out_inh_rate_avian * (
            self.direct_spray_duration / 60.0) * self.spray_drift_fraction) / (self.body_weight_assessed_bird)
        return self.out_sid_avian

    def calc_sid_mammal(self):
        """
        eq. 8 Mammalian spray droplet inhalation dose
        """
        self.out_sid_mammal = (self.out_air_conc * self.out_inh_rate_mammal * (
            self.direct_spray_duration / 60.0) * self.spray_drift_fraction) / (self.body_weight_assessed_mammal)
        return self.out_sid_mammal

    def calc_convert_mammal_inhalation_lc50_to_ld50(self):
        """
        eq. 9 Conversion of mammalian LC50 to LD50
        """
        self.out_cf = ((self.out_inh_rate_mammal * 0.001) / self.body_weight_tested_mammal)
        activity_factor = 1.
        absorption = 1.
        self.out_mammal_inhalation_ld50 = self.mammal_inhalation_lc50 * absorption * self.out_cf * \
                                          self.duration_mammal_inhalation_study * activity_factor
        return self.out_mammal_inhalation_ld50

    def calc_adjusted_mammal_inhalation_ld50(self):
        """
        eq. 10 Adjusted mammalian inhalation LD50
        """
        magic_power = 0.25
        self.out_adjusted_mammal_inhalation_ld50 = self.out_mammal_inhalation_ld50 * \
                                                (self.body_weight_tested_mammal / self.body_weight_assessed_mammal) ** \
                                                magic_power
        return self.out_adjusted_mammal_inhalation_ld50

    def calc_estimated_avian_inhalation_ld50(self):
        """
        eq. 11 Estimated avian inhalation LD50
        """
        three_five = 3.5
        self.out_estimated_avian_inhalation_ld50 = (self.avian_oral_ld50 * self.out_mammal_inhalation_ld50) / (
            three_five * self.mammal_oral_ld50)
        return self.out_estimated_avian_inhalation_ld50

    def calc_adjusted_avian_inhalation_ld50(self):
        """
        eq. 12 Adjusted avian inhalation LD50
        """
        self.out_adjusted_avian_inhalation_ld50 = self.out_estimated_avian_inhalation_ld50 * \
                                              (self.body_weight_assessed_bird / self.body_weight_tested_bird) ** \
                                              (self.mineau_scaling_factor - 1)
        return self.out_adjusted_avian_inhalation_ld50

    def return_ratio_vid_avian(self):
        """
        results #1: Ratio of avian vapor dose to adjusted inhalation LD50
        """
        self.out_ratio_vid_avian = self.out_vid_avian / self.out_adjusted_avian_inhalation_ld50
        return self.out_ratio_vid_avian

    def return_loc_vid_avian(self):
        """
        results #2: Level of Concern for avian vapor phase risk
        """
        exceed_boolean = self.out_ratio_vid_avian < 0.1
        self.out_loc_vid_avian = exceed_boolean.map(lambda x:
                                                'Exposure not Likely Significant' if x is True
                                                else 'Proceed to Refinements')
        return self.out_loc_vid_avian

    def return_ratio_sid_avian(self):
        """
        results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
        """
        self.out_ratio_sid_avian = self.out_sid_avian / self.out_adjusted_avian_inhalation_ld50
        return self.out_ratio_sid_avian

    def return_loc_sid_avian(self):
        """
        results #4: Level of Concern for avian droplet inhalation risk
        """
        exceed_boolean = self.out_ratio_sid_avian < 0.1
        self.out_loc_sid_avian = exceed_boolean.map(lambda x:
                                                'Exposure not Likely Significant' if x is True
                                                else 'Proceed to Refinements')
        return self.out_loc_sid_avian

    def return_ratio_vid_mammal(self):
        """
        results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
        """
        self.out_ratio_vid_mammal = self.out_vid_mammal / self.out_adjusted_mammal_inhalation_ld50
        return self.out_ratio_vid_mammal

    def return_loc_vid_mammal(self):
        """
        results #6: Level of Concern for mammalian vapor phase risk
        """
        exceed_boolean = self.out_ratio_vid_mammal < 0.1
        self.out_loc_vid_mammal = exceed_boolean.map(lambda x:
                                                 'Exposure not Likely Significant' if x is True
                                                 else 'Proceed to Refinements')
        return self.out_loc_vid_mammal

    def return_ratio_sid_mammal(self):
        """
        results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
        """
        self.out_ratio_sid_mammal = self.out_sid_mammal / self.out_adjusted_mammal_inhalation_ld50
        return self.out_ratio_sid_mammal

    def return_loc_sid_mammal(self):
        """
        results #8: Level of Concern for mammaliam droplet inhalation risk
        """
        exceed_boolean = self.out_ratio_sid_mammal < 0.1
        self.out_loc_sid_mammal = exceed_boolean.map(lambda x:
                                                 'Exposure not Likely Significant' if x is True
                                                 else 'Proceed to Refinements')
        return self.out_loc_sid_mammal


# def main():
#     """
#     main callable
#     :return:
#     """
#     test_stir = stir(True, True, 1, 1, 1, 1, 1, 1, 1, 1)
#     print vars(test_stir)
#     stir_json = toJSON(test_stir)
#     new_stir = fromJSON(stir_json)
#     print vars(new_stir)
#
#
# if __name__ == '__main__':
#     main()
