from __future__ import division
import numpy as np
import os.path
import sys
import pandas as pd
import therps_functions
import time
from functools import wraps
from therps_functions import THerpsFunctions
import logging

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("therps_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result

    return measure_time

class THerpsInputs(ModelSharedInputs):
    """
    Input class for Therps.
    """

    def __init__(self):
        """Class representing the inputs for Therps"""
        super(THerpsInputs, self).__init__()
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        """
        THerps constructor.
        :param chem_name:
        :param use:
        :param formu_name:
        :param percent_act_ing:
        :param foliar_diss_hlife:
        :param num_apps:
        :param app_interval:
        :param application_rate:
        :param ld50_bird:
        :param lc50_bird:
        :param noaec_bird:
        :param noael_bird:
        :param species_of_the_tested_bird_avian_ld50:
        :param species_of_the_tested_bird_avian_lc50:
        :param species_of_the_tested_bird_avian_noaec:
        :param species_of_the_tested_bird_avian_noael:
        :param tw_bird_ld50:
        :param tw_bird_lc50:
        :param tw_bird_noaec:
        :param tw_bird_noael:
        :param mineau_sca_fact:
        :param aw_herp_sm:
        :param aw_herp_md:
        :param aw_herp_slg:
        :param awc_herp_sm:
        :param awc_herp_md:
        :param awc_herp_lg:
        :param bw_frog_prey_mamm:
        :param bw_frog_prey_herp:
        :return:
        """
        self.use = pd.Series([], dtype = "object", name="use")
        self.formu_name = pd.Series([], dtype = "object", name="formu_name")
        self.percent_act_ing = pd.Series([], dtype = "float", name="percent_act_ing")
        self.foliar_diss_hlife = pd.Series([], dtype = "float", name="foliar_diss_hlife")
        self.num_apps = pd.Series([], dtype = "int", name="num_apps")
        self.app_interval = pd.Series([], dtype = "int", name="app_interval")

        self.application_rate = pd.Series([], dtype = "float", name="application_rate")

        self.ld50_bird = pd.Series([], dtype = "float", name="ld50_bird")
        self.lc50_bird = pd.Series([], dtype = "float", name="lc50_bird")
        self.noaec_bird = pd.Series([], dtype = "float", name="noaec_bird")
        self.noael_bird = pd.Series([], dtype = "float", name="noael_bird")
        
        self.species_of_the_tested_bird_avian_ld50 = pd.Series([], dtype = "float", name="species_of_the_tested_bird_avian_ld50")
        self.species_of_the_tested_bird_avian_lc50 = pd.Series([], dtype = "float", name="species_of_the_tested_bird_avian_lc50")
        self.species_of_the_tested_bird_avian_noaec = pd.Series([], dtype = "float", name="species_of_the_tested_bird_avian_noaec")
        self.species_of_the_tested_bird_avian_noael = pd.Series([], dtype = "float", name="species_of_the_tested_bird_avian_noael")

        self.tw_bird_ld50 = pd.Series([], dtype = "float", name="tw_bird_ld50")
        self.tw_bird_lc50 = pd.Series([], dtype = "float", name="tw_bird_lc50")
        self.tw_bird_noaec = pd.Series([], dtype = "float", name="tw_bird_noaec")
        self.tw_bird_noael = pd.Series([], dtype = "float", name="tw_bird_noael")

        self.mineau_sca_fact  = pd.Series([], dtype = "float", name="mineau_sca_fact")
        self.aw_herp_sm = pd.Series([], dtype = "float", name="aw_herp_sm")
        self.aw_herp_md = pd.Series([], dtype = "float", name="aw_herp_md")
        self.aw_herp_lg = pd.Series([], dtype = "float", name="aw_herp_lg")
        self.awc_herp_sm = pd.Series([], dtype = "float", name="awc_herp_sm")
        self.awc_herp_md = pd.Series([], dtype = "float", name="awc_herp_md")
        self.awc_herp_lg = pd.Series([], dtype = "float", name="awc_herp_lg")
        self.bw_frog_prey_mamm = pd.Series([], dtype = "float", name="bw_frog_prey_mamm")
        self.bw_frog_prey_herp = pd.Series([], dtype = "float", name="bw_frog_prey_herp")

class THerpsOutputs(object):
    """
    Output class for Therps.
    """

    def __init__(self):
        """Class representing the outputs for Therps"""
        super(THerpsOutputs, self).__init__()

        #application rates and days of applications
        self.day_out = pd.Series([], dtype = 'object', name = 'day_out')
        self.app_rates = pd.Series([], dtype = 'object', name = 'app_rates')

        #timeseries of concentrations related to herbiferous food sources
        self.out_c_ts_sg = pd.Series([], dtype = 'float')  # short grass
        self.out_c_ts_blp = pd.Series([], dtype = 'float')  # broad-leafed plants
        self.out_c_ts_fp = pd.Series([], dtype = 'float')  # fruits/pods

        self.out_c_ts_mean_sg = pd.Series([], dtype = 'float')  # short grass
        self.out_c_ts_mean_blp = pd.Series([], dtype = 'float')  # broad-leafed plants
        self.out_c_ts_mean_fp = pd.Series([], dtype = 'float')  # fruits/pods


        # Table 5
        self.out_ld50_ad_sm = pd.Series([], dtype = 'float', name="out_ld50_ad_sm")
        self.out_ld50_ad_md = pd.Series([], dtype = 'float', name="out_ld50_ad_md")
        self.out_ld50_ad_lg = pd.Series([], dtype = 'float', name="out_ld50_ad_lg")

        self.out_eec_dose_bp_sm = pd.Series([], dtype = 'float', name="out_eec_dose_bp_sm")
        self.out_eec_dose_bp_md = pd.Series([], dtype = 'float', name="out_eec_dose_bp_md")
        self.out_eec_dose_bp_lg = pd.Series([], dtype = 'float', name="out_eec_dose_bp_lg")
        self.out_arq_dose_bp_sm = pd.Series([], dtype = 'float', name="out_arq_dose_bp_sm")
        self.out_arq_dose_bp_md = pd.Series([], dtype = 'float', name="out_arq_dose_bp_md")
        self.out_arq_dose_bp_lg = pd.Series([], dtype = 'float', name="out_arq_dose_bp_lg")

        self.out_eec_dose_fr_sm = pd.Series([], dtype = 'float', name="out_eec_dose_fr_sm")
        self.out_eec_dose_fr_md = pd.Series([], dtype = 'float', name="out_eec_dose_fr_md")
        self.out_eec_dose_fr_lg = pd.Series([], dtype = 'float', name="out_eec_dose_fr_lg")
        self.out_arq_dose_fr_sm = pd.Series([], dtype = 'float', name="out_arq_dose_fr_sm")
        self.out_arq_dose_fr_md = pd.Series([], dtype = 'float', name="out_arq_dose_fr_md")
        self.out_arq_dose_fr_lg = pd.Series([], dtype = 'float', name="out_arq_dose_fr_lg")

        self.out_eec_dose_hm_md = pd.Series([], dtype = 'float', name="out_eec_dose_hm_md")
        self.out_eec_dose_hm_lg = pd.Series([], dtype = 'float', name="out_eec_dose_hm_lg")
        self.out_arq_dose_hm_md = pd.Series([], dtype = 'float', name="out_arq_dose_hm_md")
        self.out_arq_dose_hm_lg = pd.Series([], dtype = 'float', name="out_arq_dose_hm_lg")

        self.out_eec_dose_im_md = pd.Series([], dtype = 'float', name="out_eec_dose_im_md")
        self.out_eec_dose_im_lg = pd.Series([], dtype = 'float', name="out_eec_dose_im_lg")
        self.out_arq_dose_im_md = pd.Series([], dtype = 'float', name="out_arq_dose_im_md")
        self.out_arq_dose_im_lg = pd.Series([], dtype = 'float', name="out_arq_dose_im_lg")

        self.out_eec_dose_tp_md = pd.Series([], dtype = 'float', name="out_eec_dose_tp_md")
        self.out_eec_dose_tp_lg = pd.Series([], dtype = 'float', name="out_eec_dose_tp_lg")
        self.out_arq_dose_tp_md = pd.Series([], dtype = 'float', name="out_arq_dose_tp_md")
        self.out_arq_dose_tp_lg = pd.Series([], dtype = 'float', name="out_arq_dose_tp_lg")

        # Table 6
        self.out_eec_diet_herp_bl = pd.Series([], dtype = 'float', name="out_eec_diet_herp_bl")
        self.out_eec_arq_herp_bl = pd.Series([], dtype = 'float', name="out_eec_arq_herp_bl")
        self.out_eec_diet_herp_fr = pd.Series([], dtype = 'float', name="out_eec_diet_herp_fr")
        self.out_eec_arq_herp_fr = pd.Series([], dtype = 'float', name="out_eec_arq_herp_fr")
        self.out_eec_diet_herp_hm = pd.Series([], dtype = 'float', name="out_eec_diet_herp_hm")
        self.out_eec_arq_herp_hm = pd.Series([], dtype = 'float', name="out_eec_arq_herp_hm")
        self.out_eec_diet_herp_im = pd.Series([], dtype = 'float', name="out_eec_diet_herp_im")
        self.out_eec_arq_herp_im = pd.Series([], dtype = 'float', name="out_eec_arq_herp_im")
        self.out_eec_diet_herp_tp = pd.Series([], dtype = 'float', name="out_eec_diet_herp_tp")
        self.out_eec_arq_herp_tp = pd.Series([], dtype = 'float', name="out_eec_arq_herp_tp")

        # Table 7
        self.out_eec_diet_herp_bl = pd.Series([], dtype = 'float', name="out_eec_diet_herp_bl")
        self.out_eec_crq_herp_bl = pd.Series([], dtype = 'float', name="out_eec_crq_herp_bl")
        self.out_eec_diet_herp_fr = pd.Series([], dtype = 'float', name="out_eec_diet_herp_fr")
        self.out_eec_crq_herp_fr = pd.Series([], dtype = 'float', name="out_eec_crq_herp_fr")
        self.out_eec_diet_herp_hm = pd.Series([], dtype = 'float', name="out_eec_diet_herp_hm")
        self.out_eec_crq_herp_hm = pd.Series([], dtype = 'float', name="out_eec_crq_herp_hm")
        self.out_eec_diet_herp_im = pd.Series([], dtype = 'float', name="out_eec_diet_herp_im")
        self.out_eec_crq_herp_im = pd.Series([], dtype = 'float', name="out_eec_crq_herp_im")
        self.out_eec_diet_herp_tp = pd.Series([], dtype = 'float', name="out_eec_diet_herp_tp")
        self.out_eec_crq_herp_tp = pd.Series([], dtype = 'float', name="out_eec_crq_herp_tp")
        
        # Table 8
        self.out_eec_dose_bp_sm_mean = pd.Series([], dtype = 'float', name="out_eec_dose_bp_sm_mean")
        self.out_eec_dose_bp_md_mean = pd.Series([], dtype = 'float', name="out_eec_dose_bp_md_mean")
        self.out_eec_dose_bp_lg_mean = pd.Series([], dtype = 'float', name="out_eec_dose_bp_lg_mean")
        self.out_arq_dose_bp_sm_mean = pd.Series([], dtype = 'float', name="out_arq_dose_bp_sm_mean")
        self.out_arq_dose_bp_md_mean = pd.Series([], dtype = 'float', name="out_arq_dose_bp_md_mean")
        self.out_arq_dose_bp_lg_mean = pd.Series([], dtype = 'float', name="out_arq_dose_bp_lg_mean")

        self.out_eec_dose_fr_sm_mean = pd.Series([], dtype = 'float', name="out_eec_dose_fr_sm_mean")
        self.out_eec_dose_fr_md_mean = pd.Series([], dtype = 'float', name="out_eec_dose_fr_md_mean")
        self.out_eec_dose_fr_lg_mean = pd.Series([], dtype = 'float', name="out_eec_dose_fr_lg_mean")
        self.out_arq_dose_fr_sm_mean = pd.Series([], dtype = 'float', name="out_arq_dose_fr_sm_mean")
        self.out_arq_dose_fr_md_mean = pd.Series([], dtype = 'float', name="out_arq_dose_fr_md_mean")
        self.out_arq_dose_fr_lg_mean = pd.Series([], dtype = 'float', name="out_arq_dose_fr_lg_mean")

        self.out_eec_dose_hm_md_mean = pd.Series([], dtype = 'float', name="out_eec_dose_hm_md_mean")
        self.out_eec_dose_hm_lg_mean = pd.Series([], dtype = 'float', name="out_eec_dose_hm_lg_mean")
        self.out_arq_dose_hm_md_mean = pd.Series([], dtype = 'float', name="out_arq_dose_hm_md_mean")
        self.out_arq_dose_hm_lg_mean = pd.Series([], dtype = 'float', name="out_arq_dose_hm_lg_mean")

        self.out_eec_dose_im_md_mean = pd.Series([], dtype = 'float', name="out_eec_dose_im_md_mean")
        self.out_eec_dose_im_lg_mean = pd.Series([], dtype = 'float', name="out_eec_dose_im_lg_mean")
        self.out_arq_dose_im_md_mean = pd.Series([], dtype = 'float', name="out_arq_dose_im_md_mean")
        self.out_arq_dose_im_lg_mean = pd.Series([], dtype = 'float', name="out_arq_dose_im_lg_mean")

        self.out_eec_dose_tp_md_mean = pd.Series([], dtype = 'float', name="out_eec_dose_tp_md_mean")
        self.out_eec_dose_tp_lg_mean = pd.Series([], dtype = 'float', name="out_eec_dose_tp_lg_mean")
        self.out_arq_dose_tp_md_mean = pd.Series([], dtype = 'float', name="out_arq_dose_tp_md_mean")
        self.out_arq_dose_tp_lg_mean = pd.Series([], dtype = 'float', name="out_arq_dose_tp_lg_mean")

        # Table 9
        self.out_eec_diet_herp_bl_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_bl_mean")
        self.out_eec_arq_herp_bl_mean = pd.Series([], dtype = 'float', name="out_eec_arq_herp_bl_mean")
        self.out_eec_diet_herp_fr_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_fr_mean")
        self.out_eec_arq_herp_fr_mean = pd.Series([], dtype = 'float', name="out_eec_arq_herp_fr_mean")
        self.out_eec_diet_herp_hm_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_hm_mean")
        self.out_eec_arq_herp_hm_mean = pd.Series([], dtype = 'float', name="out_eec_arq_herp_hm_mean")
        self.out_eec_diet_herp_im_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_im_mean")
        self.out_eec_arq_herp_im_mean = pd.Series([], dtype = 'float', name="out_eec_arq_herp_im_mean")
        self.out_eec_diet_herp_tp_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_tp_mean")
        self.out_eec_arq_herp_tp_mean = pd.Series([], dtype = 'float', name="out_eec_arq_herp_tp_mean")

        # Table 10
        self.out_eec_diet_herp_bl_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_bl_mean")
        self.out_eec_crq_herp_bl_mean = pd.Series([], dtype = 'float', name="out_eec_crq_herp_bl_mean")
        self.out_eec_diet_herp_fr_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_fr_mean")
        self.out_eec_crq_herp_fr_mean = pd.Series([], dtype = 'float', name="out_eec_crq_herp_fr_mean")
        self.out_eec_diet_herp_hm_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_hm_mean")
        self.out_eec_crq_herp_hm_mean = pd.Series([], dtype = 'float', name="out_eec_crq_herp_hm_mean")
        self.out_eec_diet_herp_im_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_im_mean")
        self.out_eec_crq_herp_im_mean = pd.Series([], dtype = 'float', name="out_eec_crq_herp_im_mean")
        self.out_eec_diet_herp_tp_mean = pd.Series([], dtype = 'float', name="out_eec_diet_herp_tp_mean")
        self.out_eec_crq_herp_tp_mean = pd.Series([], dtype = 'float', name="out_eec_crq_herp_tp_mean")


class THerps(UberModel, THerpsInputs, THerpsOutputs, THerpsFunctions):
    """
    Estimate dietary exposure and risk to terrestrial-phase amphibians and reptiles from pesticide use.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the THerps model and containing all its methods"""
        super(THerps, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

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

    def run_methods(self):

        # Result variables

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()
        self.frac_act_ing = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.frac_act_ing = self.percent_to_frac(self.percent_act_ing)

#?? to be sure -- these values are coming in as percents and need to be converted to mass fractions
        # convert percent water content for herptivores to fraction water content
        self.awc_herp_sm = self.percent_to_frac(self.awc_herp_sm)
        self.awc_herp_md = self.percent_to_frac(self.awc_herp_md)
        self.awc_herp_lg = self.percent_to_frac(self.awc_herp_lg)

        # convert application rate and application interval to actual application rate and day of year object series/lists
        self.day_out, self.app_rates = self.convert_app_intervals()

        # time series of daily concentrations (one year + one week) related to each food source
        self.out_c_ts_sg = self.eec_diet_timeseries(self.food_multiplier_init_sg)  # short grass
        self.out_c_ts_blp = self.eec_diet_timeseries(self.food_multiplier_init_blp)  # broad-leafed plants
        self.out_c_ts_fp = self.eec_diet_timeseries(self.food_multiplier_init_fp)  # fruits/pods

        self.out_c_ts_mean_sg = self.eec_diet_timeseries(self.food_multiplier_mean_sg)  # short grass
        self.out_c_ts_mean_blp = self.eec_diet_timeseries(self.food_multiplier_mean_blp)  # broad-leafed plants
        self.out_c_ts_mean_fp = self.eec_diet_timeseries(self.food_multiplier_mean_fp)  # fruits/pods

        # Table 5
        self.out_ld50_ad_sm = self.at_bird(self.aw_herp_sm)
        self.out_ld50_ad_md = self.at_bird(self.aw_herp_md)
        self.out_ld50_ad_lg = self.at_bird(self.aw_herp_lg)

        self.out_eec_dose_bp_sm = self.eec_dose_herp(self.aw_herp_sm, self.awc_herp_sm, self.food_multiplier_init_blp)
        self.out_eec_dose_bp_md = self.eec_dose_herp(self.aw_herp_md, self.awc_herp_md, self.food_multiplier_init_blp)
        self.out_eec_dose_bp_lg = self.eec_dose_herp(self.aw_herp_lg, self.awc_herp_lg, self.food_multiplier_init_blp)
        self.out_arq_dose_bp_sm = self.arq_dose_herp(self.aw_herp_sm, self.awc_herp_sm, self.food_multiplier_init_blp)
        self.out_arq_dose_bp_md = self.arq_dose_herp(self.aw_herp_md, self.awc_herp_md, self.food_multiplier_init_blp)
        self.out_arq_dose_bp_lg = self.arq_dose_herp(self.aw_herp_lg, self.awc_herp_lg, self.food_multiplier_init_blp)

        self.out_eec_dose_fr_sm = self.eec_dose_herp(self.aw_herp_sm, self.awc_herp_sm, self.food_multiplier_init_fp)
        self.out_eec_dose_fr_md = self.eec_dose_herp(self.aw_herp_md, self.awc_herp_md, self.food_multiplier_init_fp)
        self.out_eec_dose_fr_lg = self.eec_dose_herp(self.aw_herp_lg, self.awc_herp_lg, self.food_multiplier_init_fp)
        self.out_arq_dose_fr_sm = self.arq_dose_herp(self.aw_herp_sm, self.awc_herp_sm, self.food_multiplier_init_fp)
        self.out_arq_dose_fr_md = self.arq_dose_herp(self.aw_herp_md, self.awc_herp_md, self.food_multiplier_init_fp)
        self.out_arq_dose_fr_lg = self.arq_dose_herp(self.aw_herp_lg, self.awc_herp_lg, self.food_multiplier_init_fp)

        self.out_eec_dose_hm_md = self.eec_dose_mamm(self.food_multiplier_init_sg, self.aw_herp_md,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_dose_hm_lg = self.eec_dose_mamm(self.food_multiplier_init_sg, self.aw_herp_lg,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_hm_md = self.arq_dose_mamm(self.food_multiplier_init_sg, self.aw_herp_md,
                                                     self.bw_frog_prey_mamm,self.mf_w_mamm_2)
        self.out_arq_dose_hm_lg = self.arq_dose_mamm(self.food_multiplier_init_sg, self.aw_herp_lg,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)

        self.out_eec_dose_im_md = self.eec_dose_mamm(self.food_multiplier_init_fp, self.aw_herp_md,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_dose_im_lg = self.eec_dose_mamm(self.food_multiplier_init_fp, self.aw_herp_lg,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_im_md = self.arq_dose_mamm(self.food_multiplier_init_fp, self.aw_herp_md,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_im_lg = self.arq_dose_mamm(self.food_multiplier_init_fp, self.aw_herp_lg,
                                                     self.bw_frog_prey_mamm, self.mf_w_mamm_2)

        self.out_eec_dose_tp_md = self.eec_dose_tp(self.food_multiplier_init_blp, self.aw_herp_md,
                                                   self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)
        self.out_eec_dose_tp_lg = self.eec_dose_tp(self.food_multiplier_init_blp, self.aw_herp_lg,
                                                   self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)
        self.out_arq_dose_tp_md = self.arq_dose_tp(self.food_multiplier_init_blp, self.aw_herp_md,
                                                   self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)
        self.out_arq_dose_tp_lg = self.arq_dose_tp(self.food_multiplier_init_blp, self.aw_herp_lg,
                                                   self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)

        # Table 6
        self.out_eec_diet_herp_bl = self.eec_diet_max(self.food_multiplier_init_blp)
        self.out_eec_arq_herp_bl = self.arq_diet_herp(self.food_multiplier_init_blp)
        self.out_eec_diet_herp_fr = self.eec_diet_max(self.food_multiplier_init_fp)
        self.out_eec_arq_herp_fr = self.arq_diet_herp(self.food_multiplier_init_fp)
        self.out_eec_diet_herp_hm = self.eec_diet_mamm(self.food_multiplier_init_sg,
                                                       self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_arq_herp_hm = self.arq_diet_mamm(self.food_multiplier_init_sg,
                                                      self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_im = self.eec_diet_mamm(self.food_multiplier_init_fp,
                                                       self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_arq_herp_im = self.arq_diet_mamm(self.food_multiplier_init_fp,
                                                      self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_tp = self.eec_diet_tp(self.food_multiplier_init_blp,
                                                     self.bw_frog_prey_herp, self.awc_herp_sm)
        self.out_eec_arq_herp_tp = self.arq_diet_tp(self.food_multiplier_init_blp,
                                                    self.bw_frog_prey_herp, self.awc_herp_sm)

        # Table 7
        self.out_eec_diet_herp_bl = self.eec_diet_max(self.food_multiplier_init_blp)
        self.out_eec_crq_herp_bl = self.crq_diet_herp(self.food_multiplier_init_blp)
        self.out_eec_diet_herp_fr = self.eec_diet_max(self.food_multiplier_init_fp)
        self.out_eec_crq_herp_fr = self.crq_diet_herp(self.food_multiplier_init_fp)
        self.out_eec_diet_herp_hm = self.eec_diet_mamm(self.food_multiplier_init_sg,
                                                       self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_crq_herp_hm = self.crq_diet_mamm(self.food_multiplier_init_sg,
                                                      self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_im = self.eec_diet_mamm(self.food_multiplier_init_fp,
                                                       self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_crq_herp_im = self.crq_diet_mamm(self.food_multiplier_init_fp,
                                                      self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_tp = self.eec_diet_tp(self.food_multiplier_init_blp,
                                                     self.bw_frog_prey_herp, self.awc_herp_sm)
        self.out_eec_crq_herp_tp = self.crq_diet_tp(self.food_multiplier_init_blp,
                                                    self.bw_frog_prey_herp, self.awc_herp_sm)

        # Table 8
        self.out_eec_dose_bp_sm_mean = self.eec_dose_herp(self.aw_herp_sm, self.awc_herp_sm,
                                                          self.food_multiplier_mean_blp)
        self.out_eec_dose_bp_md_mean = self.eec_dose_herp(self.aw_herp_md, self.awc_herp_md,
                                                          self.food_multiplier_mean_blp)
        self.out_eec_dose_bp_lg_mean = self.eec_dose_herp(self.aw_herp_lg, self.awc_herp_lg,
                                                          self.food_multiplier_mean_blp)
        self.out_arq_dose_bp_sm_mean = self.arq_dose_herp(self.aw_herp_sm, self.awc_herp_sm,
                                                          self.food_multiplier_mean_blp)
        self.out_arq_dose_bp_md_mean = self.arq_dose_herp(self.aw_herp_md, self.awc_herp_md,
                                                          self.food_multiplier_mean_blp)
        self.out_arq_dose_bp_lg_mean = self.arq_dose_herp(self.aw_herp_lg, self.awc_herp_lg,
                                                          self.food_multiplier_mean_blp)

        self.out_eec_dose_fr_sm_mean = self.eec_dose_herp(self.aw_herp_sm, self.awc_herp_sm,
                                                          self.food_multiplier_mean_fp)
        self.out_eec_dose_fr_md_mean = self.eec_dose_herp(self.aw_herp_md, self.awc_herp_md,
                                                          self.food_multiplier_mean_fp)
        self.out_eec_dose_fr_lg_mean = self.eec_dose_herp(self.aw_herp_lg, self.awc_herp_lg,
                                                          self.food_multiplier_mean_fp)
        self.out_arq_dose_fr_sm_mean = self.arq_dose_herp(self.aw_herp_sm, self.awc_herp_sm,
                                                          self.food_multiplier_mean_fp)
        self.out_arq_dose_fr_md_mean = self.arq_dose_herp(self.aw_herp_md, self.awc_herp_md,
                                                          self.food_multiplier_mean_fp)
        self.out_arq_dose_fr_lg_mean = self.arq_dose_herp(self.aw_herp_lg, self.awc_herp_lg,
                                                          self.food_multiplier_mean_fp)

        self.out_eec_dose_hm_md_mean = self.eec_dose_mamm(self.food_multiplier_mean_sg, self.aw_herp_md,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_dose_hm_lg_mean = self.eec_dose_mamm(self.food_multiplier_mean_sg, self.aw_herp_lg,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_hm_md_mean = self.arq_dose_mamm(self.food_multiplier_mean_sg, self.aw_herp_md,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_hm_lg_mean = self.arq_dose_mamm(self.food_multiplier_mean_sg, self.aw_herp_lg,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)

        self.out_eec_dose_im_md_mean = self.eec_dose_mamm(self.food_multiplier_mean_fp, self.aw_herp_md,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_dose_im_lg_mean = self.eec_dose_mamm(self.food_multiplier_mean_fp, self.aw_herp_lg,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_im_md_mean = self.arq_dose_mamm(self.food_multiplier_mean_fp, self.aw_herp_md,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_arq_dose_im_lg_mean = self.arq_dose_mamm(self.food_multiplier_mean_fp, self.aw_herp_lg,
                                                          self.bw_frog_prey_mamm, self.mf_w_mamm_2)

        self.out_eec_dose_tp_md_mean = self.eec_dose_tp(self.food_multiplier_mean_blp, self.aw_herp_md,
                                                        self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)
        self.out_eec_dose_tp_lg_mean = self.eec_dose_tp(self.food_multiplier_mean_blp,self.aw_herp_lg,
                                                        self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)
        self.out_arq_dose_tp_md_mean = self.arq_dose_tp(self.food_multiplier_mean_blp, self.aw_herp_md,
                                                        self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)
        self.out_arq_dose_tp_lg_mean = self.arq_dose_tp(self.food_multiplier_mean_blp, self.aw_herp_lg,
                                                        self.bw_frog_prey_herp, self.awc_herp_sm, self.awc_herp_md)

        # Table 9
        self.out_eec_diet_herp_bl_mean = self.eec_diet_max(self.food_multiplier_mean_blp)
        self.out_eec_arq_herp_bl_mean = self.arq_diet_herp(self.food_multiplier_mean_blp)
        self.out_eec_diet_herp_fr_mean = self.eec_diet_max(self.food_multiplier_mean_fp)
        self.out_eec_arq_herp_fr_mean = self.arq_diet_herp(self.food_multiplier_mean_fp)
        self.out_eec_diet_herp_hm_mean = self.eec_diet_mamm(self.food_multiplier_mean_sg,
                                                            self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_arq_herp_hm_mean = self.arq_diet_mamm(self.food_multiplier_mean_sg,
                                                           self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_im_mean = self.eec_diet_mamm(self.food_multiplier_mean_fp,
                                                            self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_arq_herp_im_mean = self.arq_diet_mamm(self.food_multiplier_mean_fp,
                                                           self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_tp_mean = self.eec_diet_tp(self.food_multiplier_mean_blp,
                                                          self.bw_frog_prey_herp, self.awc_herp_sm)
        self.out_eec_arq_herp_tp_mean = self.arq_diet_tp(self.food_multiplier_mean_blp,
                                                         self.bw_frog_prey_herp, self.awc_herp_sm)

        # Table 10
        self.out_eec_diet_herp_bl_mean = self.eec_diet_max(self.food_multiplier_mean_blp)
        self.out_eec_crq_herp_bl_mean = self.crq_diet_herp(self.food_multiplier_mean_blp)
        self.out_eec_diet_herp_fr_mean = self.eec_diet_max(self.food_multiplier_mean_fp)
        self.out_eec_crq_herp_fr_mean = self.crq_diet_herp(self.food_multiplier_mean_fp)
        self.out_eec_diet_herp_hm_mean = self.eec_diet_mamm(self.food_multiplier_mean_sg,
                                                            self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_crq_herp_hm_mean = self.crq_diet_mamm(self.food_multiplier_mean_sg,
                                                           self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_im_mean = self.eec_diet_mamm(self.food_multiplier_mean_fp,
                                                            self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_crq_herp_im_mean = self.crq_diet_mamm(self.food_multiplier_mean_fp,
                                                           self.bw_frog_prey_mamm, self.mf_w_mamm_2)
        self.out_eec_diet_herp_tp_mean = self.eec_diet_tp(self.food_multiplier_mean_blp,
                                                          self.bw_frog_prey_herp, self.awc_herp_sm)
        self.out_eec_crq_herp_tp_mean = self.crq_diet_tp(self.food_multiplier_mean_blp,
                                                         self.bw_frog_prey_herp, self.awc_herp_sm)

    def set_global_constants(self):
        # Assigned constants

        #initial residue concentration multiplier
        self.food_multiplier_init_sg = 240.  # short grass
        self.food_multiplier_init_blp = 135.  # broad-leafed plants
        self.food_multiplier_init_fp = 15.  # fruits/pods

        #mean residue concentration multiplier
        self.food_multiplier_mean_sg = 85.  # short grass
        self.food_multiplier_mean_blp = 45.  # broad-leafed plants
        self.food_multiplier_mean_fp = 7.  # fruits/pods

        # mass fraction of water in food source (higher values for herbivores and lower for granivores)
        # (EFED value = 0.8 for herbivores and insectivores)
        self.mf_w_mamm_2 = 0.8
