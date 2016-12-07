from __future__ import division
import logging
import os.path
import pandas as pd
import sys

#find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from base.uber_model import UberModel, ModelSharedInputs
from stir_functions import StirFunctions

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
        self.out_sat_air_conc = pd.Series([], dtype="float", name="out_sat_air_conc")
        self.out_inh_rate_avian = pd.Series([], dtype="float", name="out_inh_rate_avian")
        self.out_vid_avian = pd.Series([], dtype="float", name="out_vid_avian")
        self.out_inh_rate_mammal = pd.Series([], dtype="float", name="out_inh_rate_mammal")
        self.out_vid_mammal = pd.Series([], dtype="float", name="out_vid_mammal")
        self.out_ar2 = pd.Series([], dtype="float", name="out_ar2")
        self.out_air_conc = pd.Series([], dtype="float", name="out_air_conc")
        self.out_sid_avian = pd.Series([], dtype="float", name="out_sid_avian")
        self.out_sid_mammal = pd.Series([], dtype="float", name="out_sid_mammal")
        self.out_cf = pd.Series([], dtype="float", name="out_cf")
        self.out_mammal_inhalation_ld50 = pd.Series([], dtype="float", name="out_mammal_inhalation_ld50")
        self.out_adjusted_mammal_inhalation_ld50 = pd.Series([], dtype="float", name="out_adjusted_mammal_inhalation_ld50")
        self.out_estimated_avian_inhalation_ld50 = pd.Series([], dtype="float", name="out_estimated_avian_inhalation_ld50")
        self.out_adjusted_avian_inhalation_ld50 = pd.Series([], dtype="float", name="out_adjusted_avian_inhalation_ld50")
        self.out_ratio_vid_avian = pd.Series([], dtype="float", name="out_ratio_vid_avian")
        self.out_ratio_sid_avian = pd.Series([], dtype="float", name="out_ratio_sid_avian")
        self.out_ratio_vid_mammal = pd.Series([], dtype="float", name="out_ratio_vid_mammal")
        self.out_ratio_sid_mammal = pd.Series([], dtype="float", name="out_ratio_sid_mammal")
        self.out_loc_vid_avian = pd.Series([], dtype="object", name="out_loc_vid_avian")
        self.out_loc_sid_avian = pd.Series([], dtype="object", name="out_loc_sid_avian")
        self.out_loc_vid_mammal = pd.Series([], dtype="object", name="out_loc_vid_mammal")
        self.out_loc_sid_mammal = pd.Series([], dtype="object", name="out_loc_sid_mammal")


class Stir(UberModel, StirInputs, StirOutputs, StirFunctions):
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
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

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
