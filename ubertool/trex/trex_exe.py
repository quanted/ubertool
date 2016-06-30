from __future__ import division
import os.path
import sys
import pandas as pd
from trex_functions import TRexFunctions
import time
from functools import wraps
#import logging

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs

#tf = TrexFunctions

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("trex_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result
    return measure_time


class TRexInputs(ModelSharedInputs):
    """
    Required inputs class for Trex.
    """

    def __init__(self):
        """Class representing the inputs for Trex"""
        super(TRexInputs, self).__init__()
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.use = pd.Series([], dtype="object")
        self.formu_name = pd.Series([], dtype="object")
        self.percent_act_ing = pd.Series([], dtype="float")
        self.application_type = pd.Series([], dtype="object")
        self.seed_treatment_formulation_name = pd.Series([], dtype="object")
        self.seed_crop = pd.Series([], dtype="object")
        # ??what is the seed_crop_v,
        # not listed in the crosswalk table, not referenced in code
        #self.seed_crop_v = pd.Series([], dtype="float")
        self.row_spacing = pd.Series([], dtype="float")
        self.bandwidth = pd.Series([], dtype="float")
        self.percent_incorp = pd.Series([], dtype="float")
        self.density = pd.Series([], dtype="float")
        self.foliar_diss_hlife = pd.Series([], dtype="float")
        self.app_rates = pd.Series([], dtype="object") #Series of lists, each list contains app_rates of a model simulation run
        self.day_out = pd.Series([], dtype="object") #Series of lists, each list contains day #'s of applications
        self.num_apps = pd.Series([], dtype="float") # number of applications per model simulation run
        # could calculate self.num_apps = len(self.app_rates) # should at least check if user supplied value is consistent
#=======================================================================

        self.ld50_bird = pd.Series([], dtype="float")
        self.lc50_bird = pd.Series([], dtype="float")
        self.noaec_bird = pd.Series([], dtype="float")
        self.noael_bird = pd.Series([], dtype="float")
        self.aw_bird_sm = pd.Series([], dtype="float")
        self.aw_bird_md = pd.Series([], dtype="float")
        self.aw_bird_lg = pd.Series([], dtype="float")

        self.species_of_the_tested_bird_avian_ld50 = pd.Series([], dtype="float")
        self.species_of_the_tested_bird_avian_lc50 = pd.Series([], dtype="float")
        self.species_of_the_tested_bird_avian_noaec = pd.Series([], dtype="float")
        self.species_of_the_tested_bird_avian_noael = pd.Series([], dtype="float")

        self.tw_bird_ld50 = pd.Series([], dtype="float")
        self.tw_bird_lc50 = pd.Series([], dtype="float")
        self.tw_bird_noaec = pd.Series([], dtype="float")
        self.tw_bird_noael = pd.Series([], dtype="float")
        self.mineau_sca_fact = pd.Series([], dtype="float")
        self.ld50_mamm = pd.Series([], dtype="float")
        self.lc50_mamm = pd.Series([], dtype="float")
        self.noaec_mamm = pd.Series([], dtype="float")
        self.noael_mamm = pd.Series([], dtype="float")
        self.aw_mamm_sm = pd.Series([], dtype="float")
        self.aw_mamm_md = pd.Series([], dtype="float")
        self.aw_mamm_lg = pd.Series([], dtype="float")
        self.tw_mamm = pd.Series([], dtype="float")
        self.max_seed_rate = pd.Series([], dtype="float")


class TRexOutputs(object):
    """
    Output class for Trex.
    """

    def __init__(self):
        """Class representing the outputs for Trex"""
        super(TRexOutputs, self).__init__()

        # ??do the following 15 variables need to be included in the crosswalk table
        # initial concentrations for different food types
        self.out_c_0_sg = pd.Series(name="out_c_0_sg")  # short grass
        self.out_c_0_tg = pd.Series(name="out_c_0_tg")  # tall grass
        self.out_c_0_blp = pd.Series(name="out_c_0_blp")  # broad-leafed plants
        self.out_c_0_fp = pd.Series(name="out_c_0_fp")  # fruits/pods
        self.out_c_0_arthro = pd.Series(name="out_c_0_arthro")  # arthropods

        # mean concentration estimate based on first application rate
        self.out_c_mean_sg = pd.Series(name="out_c_mean_sg")  # short grass
        self.out_c_mean_tg = pd.Series(name="out_c_mean_tg")  # tall grass
        self.out_c_mean_blp = pd.Series(name="out_c_mean_blp")  # broad-leafed plants
        self.out_c_mean_fp = pd.Series(name="out_c_mean_fp")  # fruits/pods
        self.out_c_mean_arthro = pd.Series(name="out_c_mean_arthro")  # arthropods

        # ?? what to do with time series variables below----------------------------------
        # time series estimate based on first application rate - needs to be matrices for batch runs
        self.out_c_ts_sg = pd.Series(name="out_c_ts_sg")  # short grass
        self.out_c_ts_tg = pd.Series(name="out_c_ts_tg")  # tall grass
        self.out_c_ts_blp = pd.Series(name="out_c_ts_blp")  # broad-leafed plants
        self.out_c_ts_fp = pd.Series(name="out_c_ts_fp")  # fruits/pods
        self.out_c_ts_arthro = pd.Series(name="out_c_ts_arthro")  # arthropods
        # ?? what to do with time series variables above----------------------------------

        # Table5
        self.out_sa_bird_1_s = pd.Series(name="out_sa_bird_1_s")
        self.out_sa_bird_2_s = pd.Series(name="out_sa_bird_2_s")
        self.out_sc_bird_s = pd.Series(name="out_sc_bird_s")
        self.out_sa_mamm_1_s = pd.Series(name="out_sa_mamm_1_s")
        self.out_sa_mamm_2_s = pd.Series(name="out_sa_mamm_2_s")
        self.out_sc_mamm_s = pd.Series(name="out_sc_mamm_s")

        self.out_sa_bird_1_m = pd.Series(name="out_sa_bird_1_m")
        self.out_sa_bird_2_m = pd.Series(name="out_sa_bird_2_m")
        self.out_sc_bird_m = pd.Series(name="out_sc_bird_m")
        self.out_sa_mamm_1_m = pd.Series(name="out_sa_mamm_1_m")
        self.out_sa_mamm_2_m = pd.Series(name="out_sa_mamm_2_m")
        self.out_sc_mamm_m = pd.Series(name="out_sc_mamm_m")

        self.out_sa_bird_1_l = pd.Series(name="out_sa_bird_1_l")
        self.out_sa_bird_2_l = pd.Series(name="out_sa_bird_2_l")
        self.out_sc_bird_l = pd.Series(name="out_sc_bird_l")
        self.out_sa_mamm_1_l = pd.Series(name="out_sa_mamm_1_l")
        self.out_sa_mamm_2_l = pd.Series(name="out_sa_mamm_2_l")
        self.out_sc_mamm_l = pd.Series(name="out_sc_mamm_l")

        # Table 6
        self.out_eec_diet_sg = pd.Series(name="out_eec_diet_sg")
        self.out_eec_diet_tg = pd.Series(name="out_eec_diet_tg")
        self.out_eec_diet_bp = pd.Series(name="out_eec_diet_bp")
        self.out_eec_diet_fr = pd.Series(name="out_eec_diet_fr")
        self.out_eec_diet_ar = pd.Series(name="out_eec_diet_ar")

        # Table 7
        self.out_eec_dose_bird_sg_sm = pd.Series(name="out_eec_dose_bird_sg_sm")
        self.out_eec_dose_bird_sg_md = pd.Series(name="out_eec_dose_bird_sg_md")
        self.out_eec_dose_bird_sg_lg = pd.Series(name="out_eec_dose_bird_sg_lg")
        self.out_eec_dose_bird_tg_sm = pd.Series(name="out_eec_dose_bird_tg_sm")
        self.out_eec_dose_bird_tg_md = pd.Series(name="out_eec_dose_bird_tg_md")
        self.out_eec_dose_bird_tg_lg = pd.Series(name="out_eec_dose_bird_tg_lg")
        self.out_eec_dose_bird_bp_sm = pd.Series(name="out_eec_dose_bird_bp_sm")
        self.out_eec_dose_bird_bp_md = pd.Series(name="out_eec_dose_bird_bp_md")
        self.out_eec_dose_bird_bp_lg = pd.Series(name="out_eec_dose_bird_bp_lg")
        self.out_eec_dose_bird_fp_sm = pd.Series(name="out_eec_dose_bird_fp_sm")
        self.out_eec_dose_bird_fp_md = pd.Series(name="out_eec_dose_bird_fp_md")
        self.out_eec_dose_bird_fp_lg = pd.Series(name="out_eec_dose_bird_fp_lg")
        self.out_eec_dose_bird_ar_sm = pd.Series(name="out_eec_dose_bird_ar_sm")
        self.out_eec_dose_bird_ar_md = pd.Series(name="out_eec_dose_bird_ar_md")
        self.out_eec_dose_bird_ar_lg = pd.Series(name="out_eec_dose_bird_ar_lg")
        self.out_eec_dose_bird_se_sm = pd.Series(name="out_eec_dose_bird_se_sm")
        self.out_eec_dose_bird_se_md = pd.Series(name="out_eec_dose_bird_se_md")
        self.out_eec_dose_bird_se_lg = pd.Series(name="out_eec_dose_bird_se_lg")

        # Table 7_add
        self.out_arq_bird_sg_sm = pd.Series(name="out_arq_bird_sg_sm")
        self.out_arq_bird_sg_md = pd.Series(name="out_arq_bird_sg_md")
        self.out_arq_bird_sg_lg = pd.Series(name="out_arq_bird_sg_lg")
        self.out_arq_bird_tg_sm = pd.Series(name="out_arq_bird_tg_sm")
        self.out_arq_bird_tg_md = pd.Series(name="out_arq_bird_tg_md")
        self.out_arq_bird_tg_lg = pd.Series(name="out_arq_bird_tg_lg")
        self.out_arq_bird_bp_sm = pd.Series(name="out_arq_bird_bp_sm")
        self.out_arq_bird_bp_md = pd.Series(name="out_arq_bird_bp_md")
        self.out_arq_bird_bp_lg = pd.Series(name="out_arq_bird_bp_lg")
        self.out_arq_bird_fp_sm = pd.Series(name="out_arq_bird_fp_sm")
        self.out_arq_bird_fp_md = pd.Series(name="out_arq_bird_fp_md")
        self.out_arq_bird_fp_lg = pd.Series(name="out_arq_bird_fp_lg")
        self.out_arq_bird_ar_sm = pd.Series(name="out_arq_bird_ar_sm")
        self.out_arq_bird_ar_md = pd.Series(name="out_arq_bird_ar_md")
        self.out_arq_bird_ar_lg = pd.Series(name="out_arq_bird_ar_lg")
        self.out_arq_bird_se_sm = pd.Series(name="out_arq_bird_se_sm")
        self.out_arq_bird_se_md = pd.Series(name="out_arq_bird_se_md")
        self.out_arq_bird_se_lg = pd.Series(name="out_arq_bird_se_lg")

        # Table 8
        self.out_arq_diet_bird_sg_a = pd.Series(name="out_arq_diet_bird_sg_a")
        self.out_arq_diet_bird_sg_c = pd.Series(name="out_arq_diet_bird_sg_c")
        self.out_arq_diet_bird_tg_a = pd.Series(name="out_arq_diet_bird_tg_a")
        self.out_arq_diet_bird_tg_c = pd.Series(name="out_arq_diet_bird_tg_c")
        self.out_arq_diet_bird_bp_a = pd.Series(name="out_arq_diet_bird_bp_a")
        self.out_arq_diet_bird_bp_c = pd.Series(name="out_arq_diet_bird_bp_c")
        self.out_arq_diet_bird_fp_a = pd.Series(name="out_arq_diet_bird_fp_a")
        self.out_arq_diet_bird_fp_c = pd.Series(name="out_arq_diet_bird_fp_c")
        self.out_arq_diet_bird_ar_a = pd.Series(name="out_arq_diet_bird_ar_a")
        self.out_arq_diet_bird_ar_c = pd.Series(name="out_arq_diet_bird_ar_c")

        # Table 9
        self.out_eec_dose_mamm_sg_sm = pd.Series(name="out_eec_dose_mamm_sg_sm")
        self.out_eec_dose_mamm_sg_md = pd.Series(name="out_eec_dose_mamm_sg_md")
        self.out_eec_dose_mamm_sg_lg = pd.Series(name="out_eec_dose_mamm_sg_lg")
        self.out_eec_dose_mamm_tg_sm = pd.Series(name="out_eec_dose_mamm_tg_sm")
        self.out_eec_dose_mamm_tg_md = pd.Series(name="out_eec_dose_mamm_tg_md")
        self.out_eec_dose_mamm_tg_lg = pd.Series(name="out_eec_dose_mamm_tg_lg")
        self.out_eec_dose_mamm_bp_sm = pd.Series(name="out_eec_dose_mamm_bp_sm")
        self.out_eec_dose_mamm_bp_md = pd.Series(name="out_eec_dose_mamm_bp_md")
        self.out_eec_dose_mamm_bp_lg = pd.Series(name="out_eec_dose_mamm_bp_lg")
        self.out_eec_dose_mamm_fp_sm = pd.Series(name="out_eec_dose_mamm_fp_sm")
        self.out_eec_dose_mamm_fp_md = pd.Series(name="out_eec_dose_mamm_fp_md")
        self.out_eec_dose_mamm_fp_lg = pd.Series(name="out_eec_dose_mamm_fp_lg")
        self.out_eec_dose_mamm_ar_sm = pd.Series(name="out_eec_dose_mamm_ar_sm")
        self.out_eec_dose_mamm_ar_md = pd.Series(name="out_eec_dose_mamm_ar_md")
        self.out_eec_dose_mamm_ar_lg = pd.Series(name="out_eec_dose_mamm_ar_lg")
        self.out_eec_dose_mamm_se_sm = pd.Series(name="out_eec_dose_mamm_se_sm")
        self.out_eec_dose_mamm_se_md = pd.Series(name="out_eec_dose_mamm_se_md")
        self.out_eec_dose_mamm_se_lg = pd.Series(name="out_eec_dose_mamm_se_lg")

        # Table 10out_
        self.out_arq_dose_mamm_sg_sm = pd.Series(name="out_arq_dose_mamm_sg_sm")
        self.out_crq_dose_mamm_sg_sm = pd.Series(name="out_crq_dose_mamm_sg_sm")
        self.out_arq_dose_mamm_sg_md = pd.Series(name="out_arq_dose_mamm_sg_md")
        self.out_crq_dose_mamm_sg_md = pd.Series(name="out_crq_dose_mamm_sg_md")
        self.out_arq_dose_mamm_sg_lg = pd.Series(name="out_arq_dose_mamm_sg_lg")
        self.out_crq_dose_mamm_sg_lg = pd.Series(name="out_crq_dose_mamm_sg_lg")

        self.out_arq_dose_mamm_tg_sm = pd.Series(name="out_arq_dose_mamm_tg_sm")
        self.out_crq_dose_mamm_tg_sm = pd.Series(name="out_crq_dose_mamm_tg_sm")
        self.out_arq_dose_mamm_tg_md = pd.Series(name="out_arq_dose_mamm_tg_md")
        self.out_crq_dose_mamm_tg_md = pd.Series(name="out_crq_dose_mamm_tg_md")
        self.out_arq_dose_mamm_tg_lg = pd.Series(name="out_arq_dose_mamm_tg_lg")
        self.out_crq_dose_mamm_tg_lg = pd.Series(name="out_crq_dose_mamm_tg_lg")
        self.out_arq_dose_mamm_bp_sm = pd.Series(name="out_arq_dose_mamm_bp_sm")
        self.out_crq_dose_mamm_bp_sm = pd.Series(name="out_crq_dose_mamm_bp_sm")
        self.out_arq_dose_mamm_bp_md = pd.Series(name="out_arq_dose_mamm_bp_md")
        self.out_crq_dose_mamm_bp_md = pd.Series(name="out_crq_dose_mamm_bp_md")
        self.out_arq_dose_mamm_bp_lg = pd.Series(name="out_arq_dose_mamm_bp_lg")
        self.out_crq_dose_mamm_bp_lg = pd.Series(name="out_crq_dose_mamm_bp_lg")

        self.out_arq_dose_mamm_fp_sm = pd.Series(name="out_arq_dose_mamm_fp_sm")
        self.out_crq_dose_mamm_fp_sm = pd.Series(name="out_crq_dose_mamm_fp_sm")
        self.out_arq_dose_mamm_fp_md = pd.Series(name="out_arq_dose_mamm_fp_md")
        self.out_crq_dose_mamm_fp_md = pd.Series(name="out_crq_dose_mamm_fp_md")
        self.out_arq_dose_mamm_fp_lg = pd.Series(name="out_arq_dose_mamm_fp_lg")
        self.out_crq_dose_mamm_fp_lg = pd.Series(name="out_crq_dose_mamm_fp_lg")

        self.out_arq_dose_mamm_ar_sm = pd.Series(name="out_arq_dose_mamm_ar_sm")
        self.out_crq_dose_mamm_ar_sm = pd.Series(name="out_crq_dose_mamm_ar_sm")
        self.out_arq_dose_mamm_ar_md = pd.Series(name="out_arq_dose_mamm_ar_md")
        self.out_crq_dose_mamm_ar_md = pd.Series(name="out_crq_dose_mamm_ar_md")
        self.out_arq_dose_mamm_ar_lg = pd.Series(name="out_arq_dose_mamm_ar_lg")
        self.out_crq_dose_mamm_ar_lg = pd.Series(name="out_crq_dose_mamm_ar_lg")

        self.out_arq_dose_mamm_se_sm = pd.Series(name="out_arq_dose_mamm_se_sm")
        self.out_crq_dose_mamm_se_sm = pd.Series(name="out_crq_dose_mamm_se_sm")
        self.out_arq_dose_mamm_se_md = pd.Series(name="out_arq_dose_mamm_se_md")
        self.out_crq_dose_mamm_se_md = pd.Series(name="out_crq_dose_mamm_se_md")
        self.out_arq_dose_mamm_se_lg = pd.Series(name="out_arq_dose_mamm_se_lg")
        self.out_crq_dose_mamm_se_lg = pd.Series(name="out_crq_dose_mamm_se_lg")

        # Table 11
        self.out_arq_diet_mamm_sg = pd.Series(name="out_arq_diet_mamm_sg")
        self.out_arq_diet_mamm_tg = pd.Series(name="out_arq_diet_mamm_tg")
        self.out_arq_diet_mamm_bp = pd.Series(name="out_arq_diet_mamm_bp")
        self.out_arq_diet_mamm_fp = pd.Series(name="out_arq_diet_mamm_fp")
        self.out_arq_diet_mamm_ar = pd.Series(name="out_arq_diet_mamm_ar")

        self.out_crq_diet_mamm_sg = pd.Series(name="out_crq_diet_mamm_sg")
        self.out_crq_diet_mamm_tg = pd.Series(name="out_crq_diet_mamm_tg")
        self.out_crq_diet_mamm_bp = pd.Series(name="out_crq_diet_mamm_bp")
        self.out_crq_diet_mamm_fp = pd.Series(name="out_crq_diet_mamm_fp")
        self.out_crq_diet_mamm_ar = pd.Series(name="out_crq_diet_mamm_ar")

        # Table12
        self.out_ld50_rg_bird_sm = pd.Series(name="out_ld50_rg_bird_sm")
        self.out_ld50_rg_mamm_sm = pd.Series(name="out_ld50_rg_mamm_sm")
        self.out_ld50_rg_bird_md = pd.Series(name="out_ld50_rg_bird_md")
        self.out_ld50_rg_mamm_md = pd.Series(name="out_ld50_rg_mamm_md")
        self.out_ld50_rg_bird_lg = pd.Series(name="out_ld50_rg_bird_lg")
        self.out_ld50_rg_mamm_lg = pd.Series(name="out_ld50_rg_mamm_lg")

        # Table13
        self.out_ld50_rl_bird_sm = pd.Series(name="out_ld50_rl_bird_sm")
        self.out_ld50_rl_mamm_sm = pd.Series(name="out_ld50_rl_mamm_sm")
        self.out_ld50_rl_bird_md = pd.Series(name="out_ld50_rl_bird_md")
        self.out_ld50_rl_mamm_md = pd.Series(name="out_ld50_rl_mamm_md")
        self.out_ld50_rl_bird_lg = pd.Series(name="out_ld50_rl_bird_lg")
        self.out_ld50_rl_mamm_lg = pd.Series(name="out_ld50_rl_mamm_lg")

        # Table14
        self.out_ld50_bg_bird_sm = pd.Series(name="out_ld50_bg_bird_sm")
        self.out_ld50_bg_mamm_sm = pd.Series(name="out_ld50_bg_mamm_sm")
        self.out_ld50_bg_bird_md = pd.Series(name="out_ld50_bg_bird_md")
        self.out_ld50_bg_mamm_md = pd.Series(name="out_ld50_bg_mamm_md")
        self.out_ld50_bg_bird_lg = pd.Series(name="out_ld50_bg_bird_lg")
        self.out_ld50_bg_mamm_lg = pd.Series(name="out_ld50_bg_mamm_lg")

        # Table15
        self.out_ld50_bl_bird_sm = pd.Series(name="out_ld50_bl_bird_sm")
        self.out_ld50_bl_mamm_sm = pd.Series(name="out_ld50_bl_mamm_sm")
        self.out_ld50_bl_bird_md = pd.Series(name="out_ld50_bl_bird_md")
        self.out_ld50_bl_mamm_md = pd.Series(name="out_ld50_bl_mamm_md")
        self.out_ld50_bl_bird_lg = pd.Series(name="out_ld50_bl_bird_lg")
        self.out_ld50_bl_mamm_lg = pd.Series(name="out_ld50_bl_mamm_lg")


class TRex(UberModel, TRexInputs, TRexOutputs, TRexFunctions):
    """
    Estimate exposure concentrations and risk quotients for birds and mammals.
    """

    @timefn
    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Trex model and containing all its methods"""
        super(TRex, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    @timefn
    def json(self, pd_obj, pd_obj_out, pd_obj_exp):
        """
            Convert DataFrames to JSON, returning a tuple
            of JSON strings (inputs, outputs, exp_out)
        """

        pd_obj_json = pd_obj.to_json()
        pd_obj_out_json = pd_obj_out.to_json()
        try:
            pd_obj_exp_json = pd_obj_exp.to_json()
        except:
            pd_obj_exp_json = "{}"

        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json

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

    # Begin model methods
    @timefn
    def run_methods(self):

        # convert user supplied app_rates/day_out from series of lists as
        # strings to series of lists as floats/integers
        self.app_rates = self.convert_strlist_float(self.app_rates)
        print(self.app_rates)
        self.day_out = self.convert_strlist_int(self.day_out)
        print(self.day_out)

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()
        self.frac_incorp = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.frac_act_ing = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.frac_act_ing = self.percent_to_frac(self.percent_act_ing)
        self.frac_incorp = self.percent_to_frac(self.percent_incorp)
        self.bandwidth = self.inches_to_feet(self.bandwidth)

        # extract first day and maximum application rates from each model simulation run
        self.app_rate_parsing()

        # # initial concentrations for different food types
        # # need to pass in app_rates because other functions calculate c_initial per timestep application rate
        # self.out_c_0_sg = self.conc_initial(self.food_multiplier_init_sg)
        # self.out_c_0_tg = self.conc_initial(self.food_multiplier_init_tg)
        # self.out_c_0_blp = self.conc_initial(self.food_multiplier_init_blp)
        # self.out_c_0_fp = self.conc_initial(self.food_multiplier_init_fp)
        # self.out_c_0_arthro = self.conc_initial(self.food_multiplier_init_arthro)
        #
        # # mean concentration estimate based on first application rate
        # self.out_c_mean_sg = self.conc_initial(self.food_multiplier_mean_sg)
        # self.out_c_mean_tg = self.conc_initial(self.food_multiplier_mean_tg)
        # self.out_c_mean_blp = self.conc_initial(self.food_multiplier_mean_blp)
        # self.out_c_mean_fp = self.conc_initial(self.food_multiplier_mean_fp)
        # self.out_c_mean_arthro = self.conc_initial(self.food_multiplier_mean_arthro)

        # ?? need to process these time series
        # time series estimate based on first test case - needs to be matrices for batch runs
        self.out_c_ts_sg = self.eec_diet_timeseries(self.food_multiplier_init_sg)  # short grass
        self.out_c_ts_tg = self.eec_diet_timeseries(self.food_multiplier_init_tg)  # tall grass
        self.out_c_ts_blp = self.eec_diet_timeseries(self.food_multiplier_init_blp)  # broad-leafed plants
        self.out_c_ts_fp = self.eec_diet_timeseries(self.food_multiplier_init_fp)  # fruits/pods
        self.out_c_ts_arthro = self.eec_diet_timeseries(self.food_multiplier_init_arthro)  # arthropods

        # Table5
        self.out_sa_bird_1_s = self.sa_bird_1("small")
        self.out_sa_bird_2_s = self.sa_bird_2("small")
        self.out_sc_bird_s = self.sc_bird()
        self.out_sa_mamm_1_s = self.sa_mamm_1("small")
        self.out_sa_mamm_2_s = self.sa_mamm_2("small")
        self.out_sc_mamm_s = self.sc_mamm("small")

        self.out_sa_bird_1_m = self.sa_bird_1("medium")
        self.out_sa_bird_2_m = self.sa_bird_2("medium")
        self.out_sc_bird_m = self.sc_bird()
        self.out_sa_mamm_1_m = self.sa_mamm_1("medium")
        self.out_sa_mamm_2_m = self.sa_mamm_2("medium")
        self.out_sc_mamm_m = self.sc_mamm("medium")

        self.out_sa_bird_1_l = self.sa_bird_1("large")
        self.out_sa_bird_2_l = self.sa_bird_2("large")
        self.out_sc_bird_l = self.sc_bird()
        self.out_sa_mamm_1_l = self.sa_mamm_1("large")
        self.out_sa_mamm_2_l = self.sa_mamm_2("large")
        self.out_sc_mamm_l = self.sc_mamm("large")

        # Table 6
        self.out_eec_diet_sg = self.eec_diet_max(self.food_multiplier_init_sg)
        self.out_eec_diet_tg = self.eec_diet_max(self.food_multiplier_init_tg)
        self.out_eec_diet_bp = self.eec_diet_max(self.food_multiplier_init_blp)
        self.out_eec_diet_fr = self.eec_diet_max(self.food_multiplier_init_fp)
        self.out_eec_diet_ar = self.eec_diet_max(self.food_multiplier_init_arthro)

        # Table 7
        self.out_eec_dose_bird_sg_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_sg_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_sg_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_tg_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_tg_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_tg_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_bp_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_bp_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_bp_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_fp_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_fp_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_fp_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_ar_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_ar_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_ar_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_se_sm = self.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_se_md = self.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_se_lg = self.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 7_add
        self.out_arq_bird_sg_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_sg_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_sg_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_tg_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_tg_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_tg_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_bp_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_bp_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_bp_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_fp_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_fp_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_fp_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_ar_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_ar_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_ar_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_se_sm = self.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_arq_bird_se_md = self.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_arq_bird_se_lg = self.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 8
        self.out_arq_diet_bird_sg_a = self.arq_diet_bird(self.food_multiplier_init_sg)
        self.out_arq_diet_bird_sg_c = self.crq_diet_bird(self.food_multiplier_init_sg)
        self.out_arq_diet_bird_tg_a = self.arq_diet_bird(self.food_multiplier_init_tg)
        self.out_arq_diet_bird_tg_c = self.crq_diet_bird(self.food_multiplier_init_tg)
        self.out_arq_diet_bird_bp_a = self.arq_diet_bird(self.food_multiplier_init_blp)
        self.out_arq_diet_bird_bp_c = self.crq_diet_bird(self.food_multiplier_init_blp)
        self.out_arq_diet_bird_fp_a = self.arq_diet_bird(self.food_multiplier_init_fp)
        self.out_arq_diet_bird_fp_c = self.crq_diet_bird(self.food_multiplier_init_fp)
        self.out_arq_diet_bird_ar_a = self.arq_diet_bird(self.food_multiplier_init_arthro)
        self.out_arq_diet_bird_ar_c = self.crq_diet_bird(self.food_multiplier_init_arthro)

        # Table 9
        self.out_eec_dose_mamm_sg_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_sg_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_sg_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_tg_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_tg_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_tg_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_bp_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_bp_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_bp_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_fp_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_fp_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_fp_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_ar_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_ar_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_ar_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_se_sm = self.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_se_md = self.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_se_lg = self.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 10
        self.out_arq_dose_mamm_sg_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_arq_dose_mamm_sg_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_arq_dose_mamm_sg_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_sg)

        self.out_arq_dose_mamm_tg_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_arq_dose_mamm_tg_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_arq_dose_mamm_tg_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_tg)

        self.out_arq_dose_mamm_bp_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_arq_dose_mamm_bp_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_arq_dose_mamm_bp_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_blp)

        self.out_arq_dose_mamm_fp_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_fp_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_fp_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_fp)

        self.out_arq_dose_mamm_ar_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_arq_dose_mamm_ar_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_arq_dose_mamm_ar_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_arthro)

        self.out_arq_dose_mamm_se_sm = self.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_sm = self.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_se_md = self.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_md = self.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_se_lg = self.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_lg = self.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # table 11
        self.out_arq_diet_mamm_sg = self.arq_diet_mamm(self.food_multiplier_init_sg)
        self.out_arq_diet_mamm_tg = self.arq_diet_mamm(self.food_multiplier_init_tg)
        self.out_arq_diet_mamm_bp = self.arq_diet_mamm(self.food_multiplier_init_blp)
        self.out_arq_diet_mamm_fp = self.arq_diet_mamm(self.food_multiplier_init_fp)
        self.out_arq_diet_mamm_ar = self.arq_diet_mamm(self.food_multiplier_init_arthro)

        self.out_crq_diet_mamm_sg = self.crq_diet_mamm(self.food_multiplier_init_sg)
        self.out_crq_diet_mamm_tg = self.crq_diet_mamm(self.food_multiplier_init_tg)
        self.out_crq_diet_mamm_bp = self.crq_diet_mamm(self.food_multiplier_init_blp)
        self.out_crq_diet_mamm_fp = self.crq_diet_mamm(self.food_multiplier_init_fp)
        self.out_crq_diet_mamm_ar = self.crq_diet_mamm(self.food_multiplier_init_arthro)

        # Table12
        self.out_ld50_rg_bird_sm = self.ld50_rg_bird(self.aw_bird_sm)
        self.out_ld50_rg_mamm_sm = self.ld50_rg_mamm(self.aw_mamm_sm)
        self.out_ld50_rg_bird_md = self.ld50_rg_bird(self.aw_bird_md)
        self.out_ld50_rg_mamm_md = self.ld50_rg_mamm(self.aw_mamm_md)
        self.out_ld50_rg_bird_lg = self.ld50_rg_bird(self.aw_bird_lg)
        self.out_ld50_rg_mamm_lg = self.ld50_rg_mamm(self.aw_mamm_lg)

        # Table13
        self.out_ld50_rl_bird_sm = self.ld50_rl_bird(self.aw_bird_sm)
        self.out_ld50_rl_mamm_sm = self.ld50_rl_mamm(self.aw_mamm_sm)
        self.out_ld50_rl_bird_md = self.ld50_rl_bird(self.aw_bird_md)
        self.out_ld50_rl_mamm_md = self.ld50_rl_mamm(self.aw_mamm_md)
        self.out_ld50_rl_bird_lg = self.ld50_rl_bird(self.aw_bird_lg)
        self.out_ld50_rl_mamm_lg = self.ld50_rl_mamm(self.aw_mamm_lg)

        # Table14
        self.out_ld50_bg_bird_sm = self.ld50_bg_bird(self.aw_bird_sm)
        self.out_ld50_bg_mamm_sm = self.ld50_bg_mamm(self.aw_mamm_sm)
        self.out_ld50_bg_bird_md = self.ld50_bg_bird(self.aw_bird_md)
        self.out_ld50_bg_mamm_md = self.ld50_bg_mamm(self.aw_mamm_md)
        self.out_ld50_bg_bird_lg = self.ld50_bg_bird(self.aw_bird_lg)
        self.out_ld50_bg_mamm_lg = self.ld50_bg_mamm(self.aw_mamm_lg)

        # Table15
        self.out_ld50_bl_bird_sm = self.ld50_bl_bird(self.aw_bird_sm)
        self.out_ld50_bl_mamm_sm = self.ld50_bl_mamm(self.aw_mamm_sm)
        self.out_ld50_bl_bird_md = self.ld50_bl_bird(self.aw_bird_md)
        self.out_ld50_bl_mamm_md = self.ld50_bl_mamm(self.aw_mamm_md)
        self.out_ld50_bl_bird_lg = self.ld50_bl_bird(self.aw_bird_lg)
        self.out_ld50_bl_mamm_lg = self.ld50_bl_mamm(self.aw_mamm_lg)

    def set_global_constants(self):
        # Assigned constants

        #initial residue concentration multiplier
        self.food_multiplier_init_sg = 240.  # short grass
        self.food_multiplier_init_tg = 110.  # tall grass
        self.food_multiplier_init_blp = 135.  # broad-leafed plants
        self.food_multiplier_init_fp = 15.  # fruits/pods
        self.food_multiplier_init_arthro = 94.  # arthropods

        #mean residue concentration multiplier
        self.food_multiplier_mean_sg = 85.  # short grass
        self.food_multiplier_mean_tg = 36.  # tall grass
        self.food_multiplier_mean_blp = 45.  # broad-leafed plants
        self.food_multiplier_mean_fp = 7.  # fruits/pods
        self.food_multiplier_mean_arthro = 65.  # arthropods

        # mass fraction of water in food source (higher values for herbivores and lower for granivores)

        self.mf_w_bird_1 = 0.1
        self.mf_w_bird_2 = 0.8
        self.mf_w_bird_3 = 0.9
        self.mf_w_mamm_1 = 0.1
        self.mf_w_mamm_2 = 0.8
        self.mf_w_mamm_3 = 0.9

        self.nagy_bird_coef_sm = 0.02
        self.nagy_bird_coef_md = 0.1
        self.nagy_bird_coef_lg = 1.0
        self.nagy_mamm_coef_sm = 0.015
        self.nagy_mamm_coef_md = 0.035
        self.nagy_mamm_coef_lg = 1.0
