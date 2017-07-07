from __future__ import division
import pandas as pd
from ..base.uber_model import UberModel, ModelSharedInputs
from .sip_functions import SipFunctions


class SipInputs(ModelSharedInputs):
    """
    Input class for SIP.
    """

    def __init__(self):
        """Class representing the inputs for SIP"""
        super(SipInputs, self).__init__()
        self.solubility = pd.Series([], dtype="float")
        self.ld50_mammal_water = pd.Series([], dtype="float")
        self.ld50_species_tested_mammal = pd.Series([], dtype="object")
        self.ld50_bodyweight_tested_mammal_other = pd.Series([], dtype="float")
        self.noael_mammal_water = pd.Series([], dtype="float")
        self.noael_species_tested_mammal = pd.Series([], dtype="object")
        self.noael_bodyweight_tested_mammal_other = pd.Series([], dtype="float")
        self.ld50_avian_water = pd.Series([], dtype="float")
        self.ld50_species_tested_bird = pd.Series([], dtype="object")
        self.ld50_bodyweight_tested_bird_other = pd.Series([], dtype="float")
        self.mineau_scaling_factor = pd.Series([], dtype="float")
        self.noaec_duck = pd.Series([], dtype="float")
        self.noaec_quail = pd.Series([], dtype="float")
        self.noaec_bird_other_1 = pd.Series([], dtype="float")
        self.noaec_bodyweight_bird_other_1 = pd.Series([], dtype="float")
        self.noaec_bird_other_2 = pd.Series([], dtype="float")
        self.noaec_bodyweight_bird_other_2 = pd.Series([], dtype="float")


class SipOutputs(object):
    """
    Output class for SIP.
    """

    def __init__(self):
        """Class representing the outputs for SIP"""
        super(SipOutputs, self).__init__()
        self.out_fw_bird = pd.Series([], dtype="float", name="out_fw_bird")
        self.out_fw_mamm = pd.Series([], dtype="float", name="out_fw_mamm")
        self.out_dose_bird = pd.Series([], dtype="float", name="out_dose_bird")
        self.out_dose_mamm = pd.Series([], dtype="float", name="out_dose_mamm")
        self.out_at_bird = pd.Series([], dtype="float", name="out_at_bird")
        self.out_at_mamm = pd.Series([], dtype="float", name="out_at_mamm")
        # self.out_fi_bird = pd.Series([], dtype="float", name="out_fi_bird")  # Removed bc this is used multiple times, therefore only the last calculated value would be reported...
        self.out_det = pd.Series([], dtype="float", name="out_det")
        self.out_act = pd.Series([], dtype="float", name="out_act")
        self.out_acute_bird = pd.Series([], dtype="float", name="out_acute_bird")
        self.out_acuconb = pd.Series([], dtype="object", name="out_acuconb")
        self.out_acute_mamm = pd.Series([], dtype="float", name="out_acute_mamm")
        self.out_acuconm = pd.Series([], dtype="object", name="out_acuconm")
        self.out_chron_bird = pd.Series([], dtype="float", name="out_chron_bird")
        self.out_chronconb = pd.Series([], dtype="object", name="out_chronconb")
        self.out_chron_mamm = pd.Series([], dtype="float", name="out_chron_mamm")
        self.out_chronconm = pd.Series([], dtype="object", name="out_chronconm")
#        self.out_det_quail = pd.Series([], dtype="float", name="out_det_quail")
#        self.out_det_duck = pd.Series([], dtype="float", name="out_det_duck")
#        self.out_det_other_1 = pd.Series([], dtype="float", name="out_det_other_1")
#        self.out_det_other_2 = pd.Series([], dtype="float", name="out_det_other_2")


class Sip(UberModel, SipInputs, SipOutputs, SipFunctions):
    """
    Estimate chemical exposure from drinking water alone in birds and mammals.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Terrplant model and containing all its methods"""
        super(Sip, self).__init__()
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
            self.set_global_constants()
            self.fw_bird()
            self.fw_mamm()
            self.dose_bird()
            self.dose_mamm()
            self.at_bird()
            self.at_mamm()
            self.det()
            self.act()
            self.acute_bird()
            self.acuconb()
            self.acute_mamm()
            self.acuconm()
            self.chron_bird()
            self.chronconb()
            self.chron_mamm()
            self.chronconm()
        except TypeError:
            pass

    def set_global_constants(self):
        """

        :return:
        """

        self.no_of_runs = len(self.pd_obj)  # Number of model runs (e.g. rows in input/output DF)

        self.bodyweight_assessed_bird = 20.
        self.bodyweight_assessed_mammal = 1000.

        self.bodyweight_mallard_duck = 1580.
        self.bodyweight_bobwhite_quail = 178.
        self.bodyweight_laboratory_rat = 350.

        #set bodyweight of tested bird and mammal to be used in ld50-based model calculations (for each model simulation run)
        self.ld50_bodyweight_tested_mammal = pd.Series([], dtype='float')
        self.ld50_bodyweight_tested_bird = pd.Series([], dtype='float')
        for i in range(self.no_of_runs):
            #for ld50 related calculations
            if (self.ld50_species_tested_mammal[i] == 'laboratory rat'):
                self.ld50_bodyweight_tested_mammal[i] = self.bodyweight_laboratory_rat
            else:
                self.ld50_bodyweight_tested_mammal[i] = self.ld50_bodyweight_tested_mammal_other[i]
            if (self.ld50_species_tested_bird[i] == 'mallard duck'):
                self.ld50_bodyweight_tested_bird[i] = self.bodyweight_mallard_duck
            elif (self.ld50_species_tested_bird[i] == 'bobwhite quail'):
                self.ld50_bodyweight_tested_bird[i] = self.bodyweight_bobwhite_quail
            else:
                self.ld50_bodyweight_tested_bird[i] = self.ld50_bodyweight_tested_bird_other[i]

        #set bodyweight of tested mammal to be used in NOAEL-based model calculations (for each model simulation run)
        self.noael_bodyweight_tested_mammal = pd.Series([], dtype='float')
        for i in range(self.no_of_runs):
            #for noael related calculations
            if (self.noael_species_tested_mammal[i] == 'laboratory rat'):
                self.noael_bodyweight_tested_mammal[i] = self.bodyweight_laboratory_rat
            else:
                self.noael_bodyweight_tested_mammal[i] = self.noael_bodyweight_tested_mammal_other[i]
