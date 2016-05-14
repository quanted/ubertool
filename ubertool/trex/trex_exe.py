from __future__ import division
import os.path
import sys
import pandas as pd
import trex_functions
import time
from functools import wraps
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
        print("trex2_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result

    return measure_time


class TrexInputs(ModelSharedInputs):
    """
    Input class for Trex.
    """

    def __init__(self):
        """Class representing the inputs for Trex"""
        super(TrexInputs, self).__init__()
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.chem_name = pd_obj['chem_name']
        self.use = pd_obj['use']
        self.formu_name = pd_obj['formu_name']
        self.percent_act_ing = pd_obj['percent_act_ing']
        self.application_type = pd_obj['application_type']
        self.seed_treatment_formulation_name = pd_obj['seed_treatment_formulation_name']
        self.seed_crop = pd_obj['seed_crop']
# ??what is the seed_crop_v, not listed in the crosswalk table, not referenced in code
        self.seed_crop_v = pd_obj['seed_crop_v']
        self.row_spacing = pd_obj['row_spacing']
        self.bandwidth = pd_obj['bandwidth']
        self.percent_incorp = pd_obj['percent_incorp']
        self.density = pd_obj['density']
        self.foliar_diss_hlife = pd_obj['floiar_diss_hlife']  # half-life
        self.num_apps = pd_obj['num_apps']  # number of applications
        self.rate_list = []  # application rates for each application day (needs to be built)
        self.day_list = []  # day numbers of the applications (needs to be built as a dataframe)
        napps = self.num_apps.iloc[0]
        for i in range(napps):
            j = i + 1  # front end variables are one-based
            # rate_temp = request.POST.get('rate'+str(j))
            rate_temp = getattr(pd_obj, 'rate' + str(j))
            self.rate_list.append(float(rate_temp))
            # day_temp = float(request.POST.get('day'+str(j)))
            day_temp = getattr(pd_obj, 'day' + str(j))
            self.day_list.append(day_temp)

        # needs to be dataframe for batch runs (convert lists to series)
        self.rate_out = pd.Series(name="rate_out")
        self.rate_out = self.rate_list
        self.day_out = pd.Series(name="day_out")
        self.day_out = self.day_list

        # self.first_app_rate = self.rate_out[0] #?
        self.first_app_rate = pd.Series(name="first_app_rate")
        self.first_app_rate = self.rate_out[0]
        self.ld50_bird = pd_obj['ld50_bird']
        self.lc50_bird = pd_obj['lc50_bird']
        self.num_appsec_bird = pd_obj['noaec_bird']
        self.noael_bird = pd_obj['noael_bird']
        self.aw_bird_sm = pd_obj['aw_bird_sm']
        self.aw_bird_md = pd_obj['aw_bird_md']
        self.aw_bird_lg = pd_obj['aw_bird_lg']

        self.species_of_the_tested_bird_avian_ld50 = pd_obj['species_of_the_tested_bird_avian_ld50']
        self.species_of_the_tested_bird_avian_lc50 = pd_obj['species_of_the_tested_bird_avian_lc50']
        self.species_of_the_tested_bird_avian_noaec = pd_obj['species_of_the_tested_bird_avian_noaec']
        self.species_of_the_tested_bird_avian_noael = pd_obj['species_of_the_tested_bird_avian_noael']

        self.tw_bird_ld50 = pd_obj['tw_bird_ld50']
        self.tw_bird_lc50 = pd_obj['tw_bird_lc50']
        self.tw_bird_noaec = pd_obj['tw_bird_noaec']
        self.tw_bird_noael = pd_obj['tw_bird_noael']
        self.mineau_sca_fact = pd_obj['mineau_sca_fact']  # mineau scaling factor
        self.ld50_mamm = pd_obj['ld50_mamm']
        self.lc50_mamm = pd_obj['lc50_mamm']
        self.noaec_mamm = pd_obj['noaec_mamm']
        self.noael_mamm = pd_obj['noael_mamm']
        self.aw_mamm_sm = pd_obj['aw_mamm_sm']
        self.aw_mamm_md = pd_obj['aw_mamm_md']
        self.aw_mamm_lg = pd_obj['aw_mamm_lg']
        self.tw_mamm = pd_obj['tw_mamm']
        self.max_seed_rate = pd_obj['max_seed_rate']

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

        self.nagy_bird_coef_sm = 0.02
        self.nagy_bird_coef_md = 0.1
        self.nagy_bird_coef_lg = 1.0
        self.nagy_mamm_coef_sm = 0.015
        self.nagy_mamm_coef_md = 0.035
        self.nagy_mamm_coef_lg = 1.0


class TrexOutputs(object):
    """
    Output class for Trex.
    """

    def __init__(self):
        """Class representing the outputs for Trex"""
        super(TrexOutputs, self).__init__()

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

        # Tabout_le 6
        self.out_eec_diet_sg = pd.series(name="out_eec_diet_sg")
        self.out_eec_diet_tg = pd.series(name="out_eec_diet_tg")
        self.out_eec_diet_bp = pd.series(name="out_eec_diet_bp")
        self.out_eec_diet_fr = pd.series(name="out_eec_diet_fr")
        self.out_eec_diet_ar = pd.series(name="out_eec_diet_ar")

        # Table 7
        self.out_eec_dose_bird_sg_sm = pd.series(name="out_eec_dose_bird_sg_sm")
        self.out_eec_dose_bird_sg_md = pd.series(name="out_eec_dose_bird_sg_md")
        self.out_eec_dose_bird_sg_lg = pd.series(name="out_eec_dose_bird_sg_lg")
        self.out_eec_dose_bird_tg_sm = pd.series(name="out_eec_dose_bird_tg_sm")
        self.out_eec_dose_bird_tg_md = pd.series(name="out_eec_dose_bird_tg_md")
        self.out_eec_dose_bird_tg_lg = pd.series(name="out_eec_dose_bird_tg_lg")
        self.out_eec_dose_bird_bp_sm = pd.series(name="out_eec_dose_bird_bp_sm")
        self.out_eec_dose_bird_bp_md = pd.series(name="out_eec_dose_bird_bp_md")
        self.out_eec_dose_bird_bp_lg = pd.series(name="out_eec_dose_bird_bp_lg")
        self.out_eec_dose_bird_fp_sm = pd.series(name="out_eec_dose_bird_fp_sm")
        self.out_eec_dose_bird_fp_md = pd.series(name="out_eec_dose_bird_fp_md")
        self.out_eec_dose_bird_fp_lg = pd.series(name="out_eec_dose_bird_fp_lg")
        self.out_eec_dose_bird_ar_sm = pd.series(name="out_eec_dose_bird_ar_sm")
        self.out_eec_dose_bird_ar_md = pd.series(name="out_eec_dose_bird_ar_md")
        self.out_eec_dose_bird_ar_lg = pd.series(name="out_eec_dose_bird_ar_lg")
        self.out_eec_dose_bird_se_sm = pd.series(name="out_eec_dose_bird_se_sm")
        self.out_eec_dose_bird_se_md = pd.series(name="out_eec_dose_bird_se_md")
        self.out_eec_dose_bird_se_lg = pd.series(name="out_eec_dose_bird_se_lg")

        # Table 7_add
        self.out_arq_bird_sg_sm = pd.series(name="out_arq_bird_sg_sm")
        self.out_arq_bird_sg_md = pd.series(name="out_arq_bird_sg_md")
        self.out_arq_bird_sg_lg = pd.series(name="out_arq_bird_sg_lg")
        self.out_arq_bird_tg_sm = pd.series(name="out_arq_bird_tg_sm")
        self.out_arq_bird_tg_md = pd.series(name="out_arq_bird_tg_md")
        self.out_arq_bird_tg_lg = pd.series(name="out_arq_bird_tg_lg")
        self.out_arq_bird_bp_sm = pd.series(name="out_arq_bird_bp_sm")
        self.out_arq_bird_bp_md = pd.series(name="out_arq_bird_bp_md")
        self.out_arq_bird_bp_lg = pd.series(name="out_arq_bird_bp_lg")
        self.out_arq_bird_fp_sm = pd.series(name="out_arq_bird_fp_sm")
        self.out_arq_bird_fp_md = pd.series(name="out_arq_bird_fp_md")
        self.out_arq_bird_fp_lg = pd.series(name="out_arq_bird_fp_lg")
        self.out_arq_bird_ar_sm = pd.series(name="out_arq_bird_ar_sm")
        self.out_arq_bird_ar_md = pd.series(name="out_arq_bird_ar_md")
        self.out_arq_bird_ar_lg = pd.series(name="out_arq_bird_ar_lg")
        self.out_arq_bird_se_sm = pd.series(name="out_arq_bird_se_sm")
        self.out_arq_bird_se_md = pd.series(name="out_arq_bird_se_md")
        self.out_arq_bird_se_lg = pd.series(name="out_arq_bird_se_lg")

        # Table 8
        self.out_arq_diet_bird_sg_a = pd.series(name="out_arq_diet_bird_sg_a")
        self.out_arq_diet_bird_sg_c = pd.series(name="out_arq_diet_bird_sg_c")
        self.out_arq_diet_bird_tg_a = pd.series(name="out_arq_diet_bird_tg_a")
        self.out_arq_diet_bird_tg_c = pd.series(name="out_arq_diet_bird_tg_c")
        self.out_arq_diet_bird_bp_a = pd.series(name="out_arq_diet_bird_bp_a")
        self.out_arq_diet_bird_bp_c = pd.series(name="out_arq_diet_bird_bp_c")
        self.out_arq_diet_bird_fp_a = pd.series(name="out_arq_diet_bird_fp_a")
        self.out_arq_diet_bird_fp_c = pd.series(name="out_arq_diet_bird_fp_c")
        self.out_arq_diet_bird_ar_a = pd.series(name="out_arq_diet_bird_ar_a")
        self.out_arq_diet_bird_ar_c = pd.series(name="out_arq_diet_bird_ar_c")

        # Table 9
        self.out_eec_dose_mamm_sg_sm = pd.series(name="out_eec_dose_mamm_sg_sm")
        self.out_eec_dose_mamm_sg_md = pd.series(name="out_eec_dose_mamm_sg_md")
        self.out_eec_dose_mamm_sg_lg = pd.series(name="out_eec_dose_mamm_sg_lg")
        self.out_eec_dose_mamm_tg_sm = pd.series(name="out_eec_dose_mamm_tg_sm")
        self.out_eec_dose_mamm_tg_md = pd.series(name="out_eec_dose_mamm_tg_md")
        self.out_eec_dose_mamm_tg_lg = pd.series(name="out_eec_dose_mamm_tg_lg")
        self.out_eec_dose_mamm_bp_sm = pd.series(name="out_eec_dose_mamm_bp_sm")
        self.out_eec_dose_mamm_bp_md = pd.series(name="out_eec_dose_mamm_bp_md")
        self.out_eec_dose_mamm_bp_lg = pd.series(name="out_eec_dose_mamm_bp_lg")
        self.out_eec_dose_mamm_fp_sm = pd.series(name="out_eec_dose_mamm_fp_sm")
        self.out_eec_dose_mamm_fp_md = pd.series(name="out_eec_dose_mamm_fp_md")
        self.out_eec_dose_mamm_fp_lg = pd.series(name="out_eec_dose_mamm_fp_lg")
        self.out_eec_dose_mamm_ar_sm = pd.series(name="out_eec_dose_mamm_ar_sm")
        self.out_eec_dose_mamm_ar_md = pd.series(name="out_eec_dose_mamm_ar_md")
        self.out_eec_dose_mamm_ar_lg = pd.series(name="out_eec_dose_mamm_ar_lg")
        self.out_eec_dose_mamm_se_sm = pd.series(name="out_eec_dose_mamm_se_sm")
        self.out_eec_dose_mamm_se_md = pd.series(name="out_eec_dose_mamm_se_md")
        self.out_eec_dose_mamm_se_lg = pd.series(name="out_eec_dose_mamm_se_lg")

        # Table 10out_
        self.out_arq_dose_mamm_sg_sm = pd.series(name="out_arq_dose_mamm_sg_sm")
        self.out_crq_dose_mamm_sg_sm = pd.series(name="out_crq_dose_mamm_sg_sm")
        self.out_arq_dose_mamm_sg_md = pd.series(name="out_arq_dose_mamm_sg_md")
        self.out_crq_dose_mamm_sg_md = pd.series(name="out_crq_dose_mamm_sg_md")
        self.out_arq_dose_mamm_sg_lg = pd.series(name="out_arq_dose_mamm_sg_lg")
        self.out_crq_dose_mamm_sg_lg = pd.series(name="out_crq_dose_mamm_sg_lg")

        self.out_arq_dose_mamm_tg_sm = pd.series(name="out_arq_dose_mamm_tg_sm")
        self.out_crq_dose_mamm_tg_sm = pd.series(name="out_crq_dose_mamm_tg_sm")
        self.out_arq_dose_mamm_tg_md = pd.series(name="out_arq_dose_mamm_tg_md")
        self.out_crq_dose_mamm_tg_md = pd.series(name="out_crq_dose_mamm_tg_md")
        self.out_arq_dose_mamm_tg_lg = pd.series(name="out_arq_dose_mamm_tg_lg")
        self.out_crq_dose_mamm_tg_lg = pd.series(name="out_crq_dose_mamm_tg_lg")

        self.out_arq_dose_mamm_bp_sm = pd.series(name="out_arq_dose_mamm_bp_sm")
        self.out_crq_dose_mamm_bp_sm = pd.series(name="out_crq_dose_mamm_bp_sm")
        self.out_arq_dose_mamm_bp_md = pd.series(name="out_arq_dose_mamm_bp_md")
        self.out_crq_dose_mamm_bp_md = pd.series(name="out_crq_dose_mamm_bp_md")
        self.out_arq_dose_mamm_bp_lg = pd.series(name="out_arq_dose_mamm_bp_lg")
        self.out_crq_dose_mamm_bp_lg = pd.series(name="out_crq_dose_mamm_bp_lg")

        self.out_arq_dose_mamm_fp_sm = pd.series(name="out_arq_dose_mamm_fp_sm")
        self.out_crq_dose_mamm_fp_sm = pd.series(name="out_crq_dose_mamm_fp_sm")
        self.out_arq_dose_mamm_fp_md = pd.series(name="out_arq_dose_mamm_fp_md")
        self.out_crq_dose_mamm_fp_md = pd.series(name="out_crq_dose_mamm_fp_md")
        self.out_arq_dose_mamm_fp_lg = pd.series(name="out_arq_dose_mamm_fp_lg")
        self.out_crq_dose_mamm_fp_lg = pd.series(name="out_crq_dose_mamm_fp_lg")

        self.out_arq_dose_mamm_ar_sm = pd.series(name="out_arq_dose_mamm_ar_sm")
        self.out_crq_dose_mamm_ar_sm = pd.series(name="out_crq_dose_mamm_ar_sm")
        self.out_arq_dose_mamm_ar_md = pd.series(name="out_arq_dose_mamm_ar_md")
        self.out_crq_dose_mamm_ar_md = pd.series(name="out_crq_dose_mamm_ar_md")
        self.out_arq_dose_mamm_ar_lg = pd.series(name="out_arq_dose_mamm_ar_lg")
        self.out_crq_dose_mamm_ar_lg = pd.series(name="out_crq_dose_mamm_ar_lg")

        self.out_arq_dose_mamm_se_sm = pd.series(name="out_arq_dose_mamm_se_sm")
        self.out_crq_dose_mamm_se_sm = pd.series(name="out_crq_dose_mamm_se_sm")
        self.out_arq_dose_mamm_se_md = pd.series(name="out_arq_dose_mamm_se_md")
        self.out_crq_dose_mamm_se_md = pd.series(name="out_crq_dose_mamm_se_md")
        self.out_arq_dose_mamm_se_lg = pd.series(name="out_arq_dose_mamm_se_lg")
        self.out_crq_dose_mamm_se_lg = pd.series(name="out_crq_dose_mamm_se_lg")

        # Table 11
        self.out_arq_diet_mamm_sg = pd.series(name="out_arq_diet_mamm_sg")
        self.out_arq_diet_mamm_tg = pd.series(name="out_arq_diet_mamm_tg")
        self.out_arq_diet_mamm_bp = pd.series(name="out_arq_diet_mamm_bp")
        self.out_arq_diet_mamm_fp = pd.series(name="out_arq_diet_mamm_fp")
        self.out_arq_diet_mamm_ar = pd.series(name="out_arq_diet_mamm_ar")

        self.out_crq_diet_mamm_sg = pd.series(name="out_crq_diet_mamm_sg")
        self.out_crq_diet_mamm_tg = pd.series(name="out_crq_diet_mamm_tg")
        self.out_crq_diet_mamm_bp = pd.series(name="out_crq_diet_mamm_bp")
        self.out_crq_diet_mamm_fp = pd.series(name="out_crq_diet_mamm_fp")
        self.out_crq_diet_mamm_ar = pd.series(name="out_crq_diet_mamm_ar")

        # Table12
        self.out_ld50_rg_bird_sm = pd.series(name="out_ld50_rg_bird_sm")
        self.out_ld50_rg_mamm_sm = pd.series(name="out_ld50_rg_mamm_sm")
        self.out_ld50_rg_bird_md = pd.series(name="out_ld50_rg_bird_md")
        self.out_ld50_rg_mamm_md = pd.series(name="out_ld50_rg_mamm_md")
        self.out_ld50_rg_bird_lg = pd.series(name="out_ld50_rg_bird_lg")
        self.out_ld50_rg_mamm_lg = pd.series(name="out_ld50_rg_mamm_lg")

        # Table13
        self.out_ld50_rl_bird_sm = pd.series(name="out_ld50_rl_bird_sm")
        self.out_ld50_rl_mamm_sm = pd.series(name="out_ld50_rl_mamm_sm")
        self.out_ld50_rl_bird_md = pd.series(name="out_ld50_rl_bird_md")
        self.out_ld50_rl_mamm_md = pd.series(name="out_ld50_rl_mamm_md")
        self.out_ld50_rl_bird_lg = pd.series(name="out_ld50_rl_bird_lg")
        self.out_ld50_rl_mamm_lg = pd.series(name="out_ld50_rl_mamm_lg")

        # Table14
        self.out_ld50_bg_bird_sm = pd.series(name="out_ld50_bg_bird_sm")
        self.out_ld50_bg_mamm_sm = pd.series(name="out_ld50_bg_mamm_sm")
        self.out_ld50_bg_bird_md = pd.series(name="out_ld50_bg_bird_md")
        self.out_ld50_bg_mamm_md = pd.series(name="out_ld50_bg_mamm_md")
        self.out_ld50_bg_bird_lg = pd.series(name="out_ld50_bg_bird_lg")
        self.out_ld50_bg_mamm_lg = pd.series(name="out_ld50_bg_mamm_lg")

        # Table15
        self.out_ld50_bl_bird_sm = pd.series(name="out_ld50_bl_bird_sm")
        self.out_ld50_bl_mamm_sm = pd.series(name="out_ld50_bl_mamm_sm")
        self.out_ld50_bl_bird_md = pd.series(name="out_ld50_bl_bird_md")
        self.out_ld50_bl_mamm_md = pd.series(name="out_ld50_bl_mamm_md")
        self.out_ld50_bl_bird_lg = pd.series(name="out_ld50_bl_bird_lg")
        self.out_ld50_bl_mamm_lg = pd.series(name="out_ld50_bl_mamm_lg")


class TRex(UberModel, TrexInputs, TrexOutputs):
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
        # Perform units conversions on necessary raw inputs
        self.frac_act_ing = pd_obj['frac_act_ing']
        self.frac_act_ing = trex_functions.percent_to_frac(self.percent_act_ing)

        self.bandwidth = trex_functions.inches_to_feet(self.bandwidth)

        self.frac_incorp = pd_obj['frac_incorp']
        self.frac_incorp = trex_functions.percent_to_frac(self.percent_incorp)

        # initial concentrations for different food types
        # need to pass in first_app_rate because other functions calculate c_initial per timestep application rate
        self.out_c_0_sg = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_init_sg)
        self.out_c_0_tg = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_init_tg)
        self.out_c_0_blp = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_init_blp)
        self.out_c_0_fp = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_init_fp)
        self.out_c_0_arthro = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_init_arthro)
        # mean concentration estimate based on first application rate
        self.out_c_mean_sg = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_mean_sg)
        self.out_c_mean_tg = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_mean_tg)
        self.out_c_mean_blp = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_mean_blp)
        self.out_c_mean_fp = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_mean_fp)
        self.out_c_mean_arthro = trex_functions.conc_initial(self.first_app_rate[0], self.food_multiplier_mean_arthro)

        # ?? need to process these time series
        # time series estimate based on first application rate - needs to be matrices for batch runs
        self.out_c_ts_sg = trex_functions.conc_food_timeseries(self.food_multiplier_init_sg)  # short grass
        self.out_c_ts_tg = trex_functions.conc_food_timeseries(self.food_mulitplier_init_tg)  # tall grass
        self.out_c_ts_blp = trex_functions.conc_food_timeseries(self.food_multiplier_init_blp)  # broad-leafed plants
        self.out_c_ts_fp = trex_functions.conc_food_timeseries(self.food_multiplier_init_fp)  # fruits/pods
        self.out_c_ts_arthro = trex_functions.conc_food_timeseries(self.food_multiplier_init_arthro)  # arthropods

        # Table5
        self.out_sa_bird_1_s = trex_functions.sa_bird_1("small")
        self.out_sa_bird_2_s = trex_functions.sa_bird_2("small")
        self.out_sc_bird_s = trex_functions.sc_bird()
        self.out_sa_mamm_1_s = trex_functions.sa_mamm_1("small")
        self.out_sa_mamm_2_s = trex_functions.sa_mamm_2("small" )
        self.out_sc_mamm_s = trex_functions.sc_mamm("small")

        self.out_sa_bird_1_m = trex_functions.sa_bird_1("medium")
        self.out_sa_bird_2_m = trex_functions.sa_bird_2("medium")
        self.out_sc_bird_m = trex_functions.sc_bird(self)
        self.out_sa_mamm_1_m = trex_functions.sa_mamm_1("medium")
        self.out_sa_mamm_2_m = trex_functions.sa_mamm_2("medium")
        self.out_sc_mamm_m = trex_functions.sc_mamm("medium")

        self.out_sa_bird_1_l = trex_functions.sa_bird_1("large")
        self.out_sa_bird_2_l = trex_functions.sa_bird_2("large")
        self.out_sc_bird_l = trex_functions.sc_bird(self)
        self.out_sa_mamm_1_l = trex_functions.sa_mamm_1("large")
        self.out_sa_mamm_2_l = trex_functions.sa_mamm_2("large")
        self.out_sc_mamm_l = trex_functions.sc_mamm("large")

        # Table 6
#??the use of 'first_app_rate' here should be checked to ensure list is available in functions
        self.out_eec_diet_sg = trex_functions.eec_diet(self.first_app_rate, self.food_multiplier_init_sg)
        self.out_eec_diet_tg = trex_functions.eec_diet(self.first_app_rate, self.food_multiplier_init_tg)
        self.out_eec_diet_bp = trex_functions.eec_diet(self.first_app_rate, self.food_multiplier_init_blp)
        self.out_eec_diet_fr = trex_functions.eec_diet(self.first_app_rate, self.food_multiplier_init_fp)
        self.out_eec_diet_ar = trex_functions.eec_diet(self.first_app_rate, self.food_multiplier_init_arthro)

        # Table 7
        self.out_eec_dose_bird_sg_sm = trex_functions.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_sg_md = trex_functions.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_sg_lg = trex_functions.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_sg)
        self.out_eec_dose_bird_tg_sm = trex_functions.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_tg_md = trex_functions.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_tg_lg = trex_functions.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_tg)
        self.out_eec_dose_bird_bp_sm = trex_functions.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_bp_md = trex_functions.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_bp_lg = trex_functions.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_blp)
        self.out_eec_dose_bird_fp_sm = trex_functions.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_fp_md = trex_functions.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_fp_lg = trex_functions.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_ar_sm = trex_functions.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_3, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_ar_md = trex_functions.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_3, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_ar_lg = trex_functions.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_3, self.food_multiplier_init_arthro)
        self.out_eec_dose_bird_se_sm = trex_functions.eec_dose_bird(self.aw_bird_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_se_md = trex_functions.eec_dose_bird(self.aw_bird_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_bird_se_lg = trex_functions.eec_dose_bird(self.aw_bird_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 7_add
        self.out_arq_bird_sg_sm = trex_functions.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_sg_md = trex_functions.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_sg_lg = trex_functions.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_arq_bird_tg_sm = trex_functions.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_tg_md = trex_functions.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_tg_lg = trex_functions.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_arq_bird_bp_sm = trex_functions.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_bp_md = trex_functions.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_bp_lg = trex_functions.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_arq_bird_fp_sm = trex_functions.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_fp_md = trex_functions.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_fp_lg = trex_functions.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_arq_bird_ar_sm = trex_functions.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_ar_md = trex_functions.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_ar_lg = trex_functions.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_arq_bird_se_sm = trex_functions.arq_dose_bird(self.aw_bird_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_arq_bird_se_md = trex_functions.arq_dose_bird(self.aw_bird_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_arq_bird_se_lg = trex_functions.arq_dose_bird(self.aw_bird_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 8
        self.out_arq_diet_bird_sg_a = trex_functions.arq_diet_bird(self.food_multiplier_init_sg)
        self.out_arq_diet_bird_sg_c = trex_functions.crq_diet_bird(self.food_multiplier_init_sg)
        self.out_arq_diet_bird_tg_a = trex_functions.arq_diet_bird(self.food_multiplier_init_tg)
        self.out_arq_diet_bird_tg_c = trex_functions.crq_diet_bird(self.food_multiplier_init_tg)
        self.out_arq_diet_bird_bp_a = trex_functions.arq_diet_bird(self.food_multiplier_init_blp)
        self.out_arq_diet_bird_bp_c = trex_functions.crq_diet_bird(self.food_multiplier_init_blp)
        self.out_arq_diet_bird_fp_a = trex_functions.arq_diet_bird(self.food_multiplier_init_fp)
        self.out_arq_diet_bird_fp_c = trex_functions.crq_diet_bird(self.food_multiplier_init_fp)
        self.out_arq_diet_bird_ar_a = trex_functions.arq_diet_bird(self.food_multiplier_init_arthro)
        self.out_arq_diet_bird_ar_c = trex_functions.crq_diet_bird(self.food_multiplier_init_arthro)

        # Table 9
        self.out_eec_dose_mamm_sg_sm = trex_functions.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_sg_md = trex_functions.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_sg_lg = trex_functions.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_sg)
        self.out_eec_dose_mamm_tg_sm = trex_functions.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_tg_md = trex_functions.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_tg_lg = trex_functions.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_tg)
        self.out_eec_dose_mamm_bp_sm = trex_functions.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_bp_md = trex_functions.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_bp_lg = trex_functions.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_blp)
        self.out_eec_dose_mamm_fp_sm = trex_functions.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_fp_md = trex_functions.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_fp_lg = trex_functions.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_ar_sm = trex_functions.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_ar_md = trex_functions.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_ar_lg = trex_functions.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2, self.food_multiplier_init_arthro)
        self.out_eec_dose_mamm_se_sm = trex_functions.eec_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_se_md = trex_functions.eec_dose_mamm(self.aw_mamm_md, self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_eec_dose_mamm_se_lg = trex_functions.eec_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # Table 10
        self.out_arq_dose_mamm_sg_sm = trex_functions.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_sm = trex_functions.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_arq_dose_mamm_sg_md = trex_functions.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_md = trex_functions.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_arq_dose_mamm_sg_lg = trex_functions.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_sg)
        self.out_crq_dose_mamm_sg_lg = trex_functions.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_sg)

        self.out_arq_dose_mamm_tg_sm = trex_functions.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_sm = trex_functions.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_arq_dose_mamm_tg_md = trex_functions.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_md = trex_functions.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_arq_dose_mamm_tg_lg = trex_functions.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_tg)
        self.out_crq_dose_mamm_tg_lg = trex_functions.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_tg)

        self.out_arq_dose_mamm_bp_sm = trex_functions.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_sm = trex_functions.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_arq_dose_mamm_bp_md = trex_functions.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_md = trex_functions.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_arq_dose_mamm_bp_lg = trex_functions.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_blp)
        self.out_crq_dose_mamm_bp_lg = trex_functions.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_blp)

        self.out_arq_dose_mamm_fp_sm = trex_functions.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_sm = trex_functions.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_fp_md = trex_functions.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_md = trex_functions.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_fp_lg = trex_functions.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_fp_lg = trex_functions.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_fp)

        self.out_arq_dose_mamm_ar_sm = trex_functions.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_sm = trex_functions.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_arq_dose_mamm_ar_md = trex_functions.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_md = trex_functions.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_arq_dose_mamm_ar_lg = trex_functions.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_2,self.food_multiplier_init_arthro)
        self.out_crq_dose_mamm_ar_lg = trex_functions.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_2,self.food_multiplier_init_arthro)

        self.out_arq_dose_mamm_se_sm = trex_functions.arq_dose_mamm(self.aw_mamm_sm,self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_sm = trex_functions.crq_dose_mamm(self.aw_mamm_sm, self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_se_md = trex_functions.arq_dose_mamm(self.aw_mamm_md,self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_md = trex_functions.crq_dose_mamm(self.aw_mamm_md, self.mf_w_bird_1,self.food_multiplier_init_fp)
        self.out_arq_dose_mamm_se_lg = trex_functions.arq_dose_mamm(self.aw_mamm_lg,self.mf_w_bird_1, self.food_multiplier_init_fp)
        self.out_crq_dose_mamm_se_lg = trex_functions.crq_dose_mamm(self.aw_mamm_lg, self.mf_w_bird_1, self.food_multiplier_init_fp)

        # table 11
        if self.lc50_mamm != 'N/A':
            self.out_arq_diet_mamm_sg = trex_functions.arq_diet_mamm(self.food_multiplier_inti_sg)
            self.out_arq_diet_mamm_tg = trex_functions.arq_diet_mamm(self.food_multiplier_inti_tg)
            self.out_arq_diet_mamm_bp = trex_functions.arq_diet_mamm(self.food_multiplier_inti_blp)
            self.out_arq_diet_mamm_fp = trex_functions.arq_diet_mamm(self.food_multiplier_inti_fp)
            self.out_arq_diet_mamm_ar = trex_functions.arq_diet_mamm(self.food_multiplier_inti_arthro)
        else:
            self.out_arq_diet_mamm_sg = 'n/a'
            self.out_arq_diet_mamm_tg = 'n/a'
            self.out_arq_diet_mamm_bp = 'n/a'
            self.out_arq_diet_mamm_fp = 'n/a'
            self.out_arq_diet_mamm_ar = 'n/a'

        self.out_crq_diet_mamm_sg = trex_functions.crq_diet_mamm(self.food_multiplier_inti_sg)
        self.out_crq_diet_mamm_tg = trex_functions.crq_diet_mamm(self.food_multiplier_inti_tg)
        self.out_crq_diet_mamm_bp = trex_functions.crq_diet_mamm(self.food_multiplier_inti_blp)
        self.out_crq_diet_mamm_fp = trex_functions.crq_diet_mamm(self.food_multiplier_inti_fp)
        self.out_crq_diet_mamm_ar = trex_functions.crq_diet_mamm(self.food_multiplier_inti_arthro)

        # Table12
        self.out_ld50_rg_bird_sm = trex_functions.ld50_rg_bird(self.aw_bird_sm)
        self.out_ld50_rg_mamm_sm = trex_functions.ld50_rg_mamm(self.aw_mamm_sm)
        self.out_ld50_rg_bird_md = trex_functions.ld50_rg_bird(self.aw_bird_md)
        self.out_ld50_rg_mamm_md = trex_functions.ld50_rg_mamm(self.aw_mamm_md)
        self.out_ld50_rg_bird_lg = trex_functions.ld50_rg_bird(self.aw_bird_lg)
        self.out_ld50_rg_mamm_lg = trex_functions.ld50_rg_mamm(self.aw_mamm_lg)

        # Table13
        self.out_ld50_rl_bird_sm = trex_functions.ld50_rl_bird(self.aw_bird_sm)
        self.out_ld50_rl_mamm_sm = trex_functions.ld50_rl_mamm(self.aw_mamm_sm)
        self.out_ld50_rl_bird_md = trex_functions.ld50_rl_bird(self.aw_bird_md)
        self.out_ld50_rl_mamm_md = trex_functions.ld50_rl_mamm(self.aw_mamm_md)
        self.out_ld50_rl_bird_lg = trex_functions.ld50_rl_bird(self.aw_bird_lg)
        self.out_ld50_rl_mamm_lg = trex_functions.ld50_rl_mamm(self.aw_mamm_lg)

        # Table14
        self.out_ld50_bg_bird_sm = trex_functions.ld50_bg_bird(self.aw_bird_sm)
        self.out_ld50_bg_mamm_sm = trex_functions.ld50_bg_mamm(self.aw_mamm_sm)
        self.out_ld50_bg_bird_md = trex_functions.ld50_bg_bird(self.aw_bird_md)
        self.out_ld50_bg_mamm_md = trex_functions.ld50_bg_mamm(self.aw_mamm_md)
        self.out_ld50_bg_bird_lg = trex_functions.ld50_bg_bird(self.aw_bird_lg)
        self.out_ld50_bg_mamm_lg = trex_functions.ld50_bg_mamm(self.aw_mamm_lg)

        # Table15
        self.out_ld50_bl_bird_sm = trex_functions.ld50_bl_bird(self.aw_bird_sm)
        self.out_ld50_bl_mamm_sm = trex_functions.ld50_bl_mamm(self.aw_mamm_sm)
        self.out_ld50_bl_bird_md = trex_functions.ld50_bl_bird(self.aw_bird_md)
        self.out_ld50_bl_mamm_md = trex_functions.ld50_bl_mamm(self.aw_mamm_md)
        self.out_ld50_bl_bird_lg = trex_functions.ld50_bl_bird(self.aw_bird_lg)
        self.out_ld50_bl_mamm_lg = trex_functions.ld50_bl_mamm(self.aw_mamm_lg)
