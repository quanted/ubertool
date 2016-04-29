#?? do we need the following import
from __future__ import division
import os.path
import sys
import pandas as pd
import trex_functions
#?? do we want time and logging to be in this code
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

# changed a_i to percent_act_ing and call function to convert from % to fraction
        # self.a_i /= 100  # change from percentage to proportion
        self.percent_act_ing = pd_obj['percent_act_ing']
        frac_act_ing = pd_obj['frac_act_ing']
        self.frac_act_ing = trex_functions.percent_to_fracttion

        self.application_type = pd_obj['application_type']
        self.seed_treatment_formulation_name = pd_obj['seed_treatment_formulation_name']
        self.seed_crop = pd_obj['seed_crop']
        self.seed_crop_v = pd_obj['seed_crop_v']
        self.r_s = pd_obj['r_s']
        self.b_w = pd_obj['b_w']
        self.b_w /= 12  # convert to ft
        self.p_i = pd_obj['p_i']
        self.p_i /= 100  # change from percentage to proportion
        self.den = pd_obj['den']
        self.h_l = pd_obj['h_l']  # half-life
        self.noa = pd_obj['noa']  # number of applications

        self.rate_list = []  # application rates for each application day (needs to be built)
        self.day_list = []  # day numbers of the applications (needs to be built as a dataframe)
        logging.info(range(self.noa.iloc[0]))
        napps = self.noa.iloc[0]
        for i in range(napps):
            logging.info(i)
            j = i + 1  # front end variables are one-based
            # rate_temp = request.POST.get('rate'+str(j))
            rate_temp = getattr(pd_obj, 'rate' + str(j))
            self.rate_list.append(float(rate_temp))
            logging.info("self.rate_list")
            logging.info(type(self.rate_list))
            logging.info(self.rate_list)
            # day_temp = float(request.POST.get('day'+str(j)))
            day_temp = getattr(pd_obj, 'day' + str(j))
            self.day_list.append(day_temp)
            logging.info("self.day_list")
            logging.info(type(self.day_list))
            logging.info(self.day_list)

        # needs to be dataframe for batch runs (convert lists to series)
        self.rate_out = pd.Series(name="rate_out")
        self.rate_out = self.rate_list
        logging.info("rate_out")
        logging.info(self.rate_out)
        self.day_out = pd.Series(name="day_out")
        self.day_out = self.day_list
        logging.info("day_out")
        logging.info(self.day_out)

        # self.ar_lb = self.rate_out[0] #?
        self.first_app_lb = pd.Series(name="first_app_lb")
        self.first_app_lb = self.rate_out[0]

#?? what does pd.obj do, why is it underlined in red
        self.ld50_bird = pd_obj['ld50_bird']
        self.lc50_bird = pd_obj['lc50_bird']
        self.NOAEC_bird = pd_obj['NOAEC_bird']
        self.NOAEL_bird = pd_obj['NOAEL_bird']
        self.aw_bird_sm = pd_obj['aw_bird_sm']
        self.aw_bird_md = pd_obj['aw_bird_md']
        self.aw_bird_lg = pd_obj['aw_bird_lg']

        self.Species_of_the_tested_bird_avian_ld50 = pd_obj['Species_of_the_tested_bird_avian_ld50']
        self.Species_of_the_tested_bird_avian_lc50 = pd_obj['Species_of_the_tested_bird_avian_lc50']
        self.Species_of_the_tested_bird_avian_NOAEC = pd_obj['Species_of_the_tested_bird_avian_NOAEC']
        self.Species_of_the_tested_bird_avian_NOAEL = pd_obj['Species_of_the_tested_bird_avian_NOAEL']

        self.tw_bird_ld50 = pd_obj['tw_bird_ld50']
        self.tw_bird_lc50 = pd_obj['tw_bird_lc50']
        self.tw_bird_NOAEC = pd_obj['tw_bird_NOAEC']
        self.tw_bird_NOAEL = pd_obj['tw_bird_NOAEL']
        self.x = pd_obj['x']                             # mineau scaling factor
        self.ld50_mamm = pd_obj['ld50_mamm']
        self.lc50_mamm = pd_obj['lc50_mamm']
        self.NOAEC_mamm = pd_obj['NOAEC_mamm']
        self.NOAEL_mamm = pd_obj['NOAEL_mamm']
        self.aw_mamm_sm = pd_obj['aw_mamm_sm']
        self.aw_mamm_md = pd_obj['aw_mamm_md']
        self.aw_mamm_lg = pd_obj['aw_mamm_lg']
        self.tw_mamm = pd_obj['tw_mamm']
        self.m_s_r_p = pd_obj['m_s_r_p']

class TrexOutputs(object):
    """
    Output class for Trex.
    """

    def __init__(self):
        """Class representing the outputs for Trex"""
        super(TrexOutputs, self).__init__()

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

#?? what to do with time series variables below----------------------------------
        # time series estimate based on first application rate - needs to be matrices for batch runs
        self.out_c_ts_sg = pd.Series(name="out_c_ts_sg")  # short grass
        self.out_c_ts_tg = pd.Series(name="out_c_ts_tg")  # tall grass
        self.out_c_ts_blp = pd.Series(name="out_c_ts_blp")  # broad-leafed plants
        self.out_c_ts_fp = pd.Series(name="out_c_ts_fp")  # fruits/pods
        self.out_c_ts_arthro = pd.Series(name="out_c_ts_arthro")  # arthropods
#?? what to do with time series variables above----------------------------------

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
        self.out_EEC_diet_SG = pd.Series(name="out_EEC_diet_SG")
        self.out_EEC_diet_TG = pd.Series(name="out_EEC_diet_TG")
        self.out_EEC_diet_BP = pd.Series(name="out_EEC_diet_BP")
        self.out_EEC_diet_FR = pd.Series(name="out_EEC_diet_FR")
        self.out_EEC_diet_AR = pd.Series(name="out_EEC_diet_AR")

        # Table 7
        self.out_EEC_dose_bird_SG_sm = pd.Series(name="out_EEC_dose_bird_SG_sm")
        self.out_EEC_dose_bird_SG_md = pd.Series(name="out_EEC_dose_bird_SG_md")
        self.out_EEC_dose_bird_SG_lg = pd.Series(name="out_EEC_dose_bird_SG_lg")
        self.out_EEC_dose_bird_TG_sm = pd.Series(name="out_EEC_dose_bird_TG_sm")
        self.out_EEC_dose_bird_TG_md = pd.Series(name="out_EEC_dose_bird_TG_md")
        self.out_EEC_dose_bird_TG_lg = pd.Series(name="out_EEC_dose_bird_TG_lg")
        self.out_EEC_dose_bird_BP_sm = pd.Series(name="out_EEC_dose_bird_BP_sm")
        self.out_EEC_dose_bird_BP_md = pd.Series(name="out_EEC_dose_bird_BP_md")
        self.out_EEC_dose_bird_BP_lg = pd.Series(name="out_EEC_dose_bird_BP_lg")
        self.out_EEC_dose_bird_FP_sm = pd.Series(name="out_EEC_dose_bird_FP_sm")
        self.out_EEC_dose_bird_FP_md = pd.Series(name="out_EEC_dose_bird_FP_md")
        self.out_EEC_dose_bird_FP_lg = pd.Series(name="out_EEC_dose_bird_FP_lg")
        self.out_EEC_dose_bird_AR_sm = pd.Series(name="out_EEC_dose_bird_AR_sm")
        self.out_EEC_dose_bird_AR_md = pd.Series(name="out_EEC_dose_bird_AR_md")
        self.out_EEC_dose_bird_AR_lg = pd.Series(name="out_EEC_dose_bird_AR_lg")
        self.out_EEC_dose_bird_SE_sm = pd.Series(name="out_EEC_dose_bird_SE_sm")
        self.out_EEC_dose_bird_SE_md = pd.Series(name="out_EEC_dose_bird_SE_md")
        self.out_EEC_dose_bird_SE_lg = pd.Series(name="out_EEC_dose_bird_SE_lg")

        # Table 7_add
        self.out_ARQ_bird_SG_sm = pd.Series(name="out_ARQ_bird_SG_sm")
        self.out_ARQ_bird_SG_md = pd.Series(name="out_ARQ_bird_SG_md")
        self.out_ARQ_bird_SG_lg = pd.Series(name="out_ARQ_bird_SG_lg")
        self.out_ARQ_bird_TG_sm = pd.Series(name="out_ARQ_bird_TG_sm")
        self.out_ARQ_bird_TG_md = pd.Series(name="out_ARQ_bird_TG_md")
        self.out_ARQ_bird_TG_lg = pd.Series(name="out_ARQ_bird_TG_lg")
        self.out_ARQ_bird_BP_sm = pd.Series(name="out_ARQ_bird_BP_sm")
        self.out_ARQ_bird_BP_md = pd.Series(name="out_ARQ_bird_BP_md")
        self.out_ARQ_bird_BP_lg = pd.Series(name="out_ARQ_bird_BP_lg")
        self.out_ARQ_bird_FP_sm = pd.Series(name="out_ARQ_bird_FP_sm")
        self.out_ARQ_bird_FP_md = pd.Series(name="out_ARQ_bird_FP_md")
        self.out_ARQ_bird_FP_lg = pd.Series(name="out_ARQ_bird_FP_lg")
        self.out_ARQ_bird_AR_sm = pd.Series(name="out_ARQ_bird_AR_sm")
        self.out_ARQ_bird_AR_md = pd.Series(name="out_ARQ_bird_AR_md")
        self.out_ARQ_bird_AR_lg = pd.Series(name="out_ARQ_bird_AR_lg")
        self.out_ARQ_bird_SE_sm = pd.Series(name="out_ARQ_bird_SE_sm")
        self.out_ARQ_bird_SE_md = pd.Series(name="out_ARQ_bird_SE_md")
        self.out_ARQ_bird_SE_lg = pd.Series(name="out_ARQ_bird_SE_lg")

        # Table 8
        self.out_ARQ_diet_bird_SG_A = pd.Series(name="out_ARQ_diet_bird_SG_A")
        self.out_ARQ_diet_bird_SG_C = pd.Series(name="out_ARQ_diet_bird_SG_C")
        self.out_ARQ_diet_bird_TG_A = pd.Series(name="out_ARQ_diet_bird_TG_A")
        self.out_ARQ_diet_bird_TG_C = pd.Series(name="out_ARQ_diet_bird_TG_C")
        self.out_ARQ_diet_bird_BP_A = pd.Series(name="out_ARQ_diet_bird_BP_A")
        self.out_ARQ_diet_bird_BP_C = pd.Series(name="out_ARQ_diet_bird_BP_C")
        self.out_ARQ_diet_bird_FP_A = pd.Series(name="out_ARQ_diet_bird_FP_A")
        self.out_ARQ_diet_bird_FP_C = pd.Series(name="out_ARQ_diet_bird_FP_C")
        self.out_ARQ_diet_bird_AR_A = pd.Series(name="out_ARQ_diet_bird_AR_A")
        self.out_ARQ_diet_bird_AR_C = pd.Series(name="out_ARQ_diet_bird_AR_C")

        # Table 9
        self.out_EEC_dose_mamm_SG_sm = pd.Series(name="out_EEC_dose_mamm_SG_sm")
        self.out_EEC_dose_mamm_SG_md = pd.Series(name="out_EEC_dose_mamm_SG_md")
        self.out_EEC_dose_mamm_SG_lg = pd.Series(name="out_EEC_dose_mamm_SG_lg")
        self.out_EEC_dose_mamm_TG_sm = pd.Series(name="out_EEC_dose_mamm_TG_sm")
        self.out_EEC_dose_mamm_TG_md = pd.Series(name="out_EEC_dose_mamm_TG_md")
        self.out_EEC_dose_mamm_TG_lg = pd.Series(name="out_EEC_dose_mamm_TG_lg")
        self.out_EEC_dose_mamm_BP_sm = pd.Series(name="out_EEC_dose_mamm_BP_sm")
        self.out_EEC_dose_mamm_BP_md = pd.Series(name="out_EEC_dose_mamm_BP_md")
        self.out_EEC_dose_mamm_BP_lg = pd.Series(name="out_EEC_dose_mamm_BP_lg")
        self.out_EEC_dose_mamm_FP_sm = pd.Series(name="out_EEC_dose_mamm_FP_sm")
        self.out_EEC_dose_mamm_FP_md = pd.Series(name="out_EEC_dose_mamm_FP_md")
        self.out_EEC_dose_mamm_FP_lg = pd.Series(name="out_EEC_dose_mamm_FP_lg")
        self.out_EEC_dose_mamm_AR_sm = pd.Series(name="out_EEC_dose_mamm_AR_sm")
        self.out_EEC_dose_mamm_AR_md = pd.Series(name="out_EEC_dose_mamm_AR_md")
        self.out_EEC_dose_mamm_AR_lg = pd.Series(name="out_EEC_dose_mamm_AR_lg")
        self.out_EEC_dose_mamm_SE_sm = pd.Series(name="out_EEC_dose_mamm_SE_sm")
        self.out_EEC_dose_mamm_SE_md = pd.Series(name="out_EEC_dose_mamm_SE_md")
        self.out_EEC_dose_mamm_SE_lg = pd.Series(name="out_EEC_dose_mamm_SE_lg")

        # Table 10out_
        self.out_ARQ_dose_mamm_SG_sm = pd.Series(name="out_ARQ_dose_mamm_SG_sm")
        self.out_CRQ_dose_mamm_SG_sm = pd.Series(name="out_CRQ_dose_mamm_SG_sm")
        self.out_ARQ_dose_mamm_SG_md = pd.Series(name="out_ARQ_dose_mamm_SG_md")
        self.out_CRQ_dose_mamm_SG_md = pd.Series(name="out_CRQ_dose_mamm_SG_md")
        self.out_ARQ_dose_mamm_SG_lg = pd.Series(name="out_ARQ_dose_mamm_SG_lg")
        self.out_CRQ_dose_mamm_SG_lg = pd.Series(name="out_CRQ_dose_mamm_SG_lg")

        self.out_ARQ_dose_mamm_TG_sm = pd.Series(name="out_ARQ_dose_mamm_TG_sm")
        self.out_CRQ_dose_mamm_TG_sm = pd.Series(name="out_CRQ_dose_mamm_TG_sm")
        self.out_ARQ_dose_mamm_TG_md = pd.Series(name="out_ARQ_dose_mamm_TG_md")
        self.out_CRQ_dose_mamm_TG_md = pd.Series(name="out_CRQ_dose_mamm_TG_md")
        self.out_ARQ_dose_mamm_TG_lg = pd.Series(name="out_ARQ_dose_mamm_TG_lg")
        self.out_CRQ_dose_mamm_TG_lg = pd.Series(name="out_CRQ_dose_mamm_TG_lg")

        self.out_ARQ_dose_mamm_BP_sm = pd.Series(name="out_ARQ_dose_mamm_BP_sm")
        self.out_CRQ_dose_mamm_BP_sm = pd.Series(name="out_CRQ_dose_mamm_BP_sm")
        self.out_ARQ_dose_mamm_BP_md = pd.Series(name="out_ARQ_dose_mamm_BP_md")
        self.out_CRQ_dose_mamm_BP_md = pd.Series(name="out_CRQ_dose_mamm_BP_md")
        self.out_ARQ_dose_mamm_BP_lg = pd.Series(name="out_ARQ_dose_mamm_BP_lg")
        self.out_CRQ_dose_mamm_BP_lg = pd.Series(name="out_CRQ_dose_mamm_BP_lg")

        self.out_ARQ_dose_mamm_FP_sm = pd.Series(name="out_ARQ_dose_mamm_FP_sm")
        self.out_CRQ_dose_mamm_FP_sm = pd.Series(name="out_CRQ_dose_mamm_FP_sm")
        self.out_ARQ_dose_mamm_FP_md = pd.Series(name="out_ARQ_dose_mamm_FP_md")
        self.out_CRQ_dose_mamm_FP_md = pd.Series(name="out_CRQ_dose_mamm_FP_md")
        self.out_ARQ_dose_mamm_FP_lg = pd.Series(name="out_ARQ_dose_mamm_FP_lg")
        self.out_CRQ_dose_mamm_FP_lg = pd.Series(name="out_CRQ_dose_mamm_FP_lg")

        self.out_ARQ_dose_mamm_AR_sm = pd.Series(name="out_ARQ_dose_mamm_AR_sm")
        self.out_CRQ_dose_mamm_AR_sm = pd.Series(name="out_CRQ_dose_mamm_AR_sm")
        self.out_ARQ_dose_mamm_AR_md = pd.Series(name="out_ARQ_dose_mamm_AR_md")
        self.out_CRQ_dose_mamm_AR_md = pd.Series(name="out_CRQ_dose_mamm_AR_md")
        self.out_ARQ_dose_mamm_AR_lg = pd.Series(name="out_ARQ_dose_mamm_AR_lg")
        self.out_CRQ_dose_mamm_AR_lg = pd.Series(name="out_CRQ_dose_mamm_AR_lg")

        self.out_ARQ_dose_mamm_SE_sm = pd.Series(name="out_ARQ_dose_mamm_SE_sm")
        self.out_CRQ_dose_mamm_SE_sm = pd.Series(name="out_CRQ_dose_mamm_SE_sm")
        self.out_ARQ_dose_mamm_SE_md = pd.Series(name="out_ARQ_dose_mamm_SE_md")
        self.out_CRQ_dose_mamm_SE_md = pd.Series(name="out_CRQ_dose_mamm_SE_md")
        self.out_ARQ_dose_mamm_SE_lg = pd.Series(name="out_ARQ_dose_mamm_SE_lg")
        self.out_CRQ_dose_mamm_SE_lg = pd.Series(name="out_CRQ_dose_mamm_SE_lg")

        # table 11
        self.out_ARQ_diet_mamm_SG = pd.Series(name="out_ARQ_diet_mamm_SG")
        self.out_ARQ_diet_mamm_TG = pd.Series(name="out_ARQ_diet_mamm_TG")
        self.out_ARQ_diet_mamm_BP = pd.Series(name="out_ARQ_diet_mamm_BP")
        self.out_ARQ_diet_mamm_FP = pd.Series(name="out_ARQ_diet_mamm_FP")
        self.out_ARQ_diet_mamm_AR = pd.Series(name="out_ARQ_diet_mamm_AR")

        self.out_CRQ_diet_mamm_SG = pd.Series(name="out_CRQ_diet_mamm_SG")
        self.out_CRQ_diet_mamm_TG = pd.Series(name="out_CRQ_diet_mamm_TG")
        self.out_CRQ_diet_mamm_BP = pd.Series(name="out_CRQ_diet_mamm_BP")
        self.out_CRQ_diet_mamm_FP = pd.Series(name="out_CRQ_diet_mamm_FP")
        self.out_CRQ_diet_mamm_AR = pd.Series(name="out_CRQ_diet_mamm_AR")

        # Table12
        self.out_LD50_rg_bird_sm = pd.Series(name="out_LD50_rg_bird_sm")
        self.out_LD50_rg_mamm_sm = pd.Series(name="out_LD50_rg_mamm_sm")
        self.out_LD50_rg_bird_md = pd.Series(name="out_LD50_rg_bird_md")
        self.out_LD50_rg_mamm_md = pd.Series(name="out_LD50_rg_mamm_md")
        self.out_LD50_rg_bird_lg = pd.Series(name="out_LD50_rg_bird_lg")
        self.out_LD50_rg_mamm_lg = pd.Series(name="out_LD50_rg_mamm_lg")

        # Table13
        self.out_LD50_rl_bird_sm = pd.Series(name="out_LD50_rl_bird_sm")
        self.out_LD50_rl_mamm_sm = pd.Series(name="out_LD50_rl_mamm_sm")
        self.out_LD50_rl_bird_md = pd.Series(name="out_LD50_rl_bird_md")
        self.out_LD50_rl_mamm_md = pd.Series(name="out_LD50_rl_mamm_md")
        self.out_LD50_rl_bird_lg = pd.Series(name="out_LD50_rl_bird_lg")
        self.out_LD50_rl_mamm_lg = pd.Series(name="out_LD50_rl_mamm_lg")

        # Table14
        self.out_LD50_bg_bird_sm = pd.Series(name="out_LD50_bg_bird_sm")
        self.out_LD50_bg_mamm_sm = pd.Series(name="out_LD50_bg_mamm_sm")
        self.out_LD50_bg_bird_md = pd.Series(name="out_LD50_bg_bird_md")
        self.out_LD50_bg_mamm_md = pd.Series(name="out_LD50_bg_mamm_md")
        self.out_LD50_bg_bird_lg = pd.Series(name="out_LD50_bg_bird_lg")
        self.out_LD50_bg_mamm_lg = pd.Series(name="out_LD50_bg_mamm_lg")

        # Table15
        self.out_LD50_bl_bird_sm = pd.Series(name="out_LD50_bl_bird_sm")
        self.out_LD50_bl_mamm_sm = pd.Series(name="out_LD50_bl_mamm_sm")
        self.out_LD50_bl_bird_md = pd.Series(name="out_LD50_bl_bird_md")
        self.out_LD50_bl_mamm_md = pd.Series(name="out_LD50_bl_mamm_md")
        self.out_LD50_bl_bird_lg = pd.Series(name="out_LD50_bl_bird_lg")
        self.out_LD50_bl_mamm_lg = pd.Series(name="out_LD50_bl_mamm_lg")

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
        logging.info("run_methods")

        # initial concentrations for different food types
        self.out_c_0_sg = trex_functions.c_0_sg
        self.out_c_0_tg = trex_functions.c_0_tg
        self.out_c_0_blp = trex_functions.c_0_blp
        self.out_c_0_fp = trex_functions.c_0_fp
        self.out_c_0_arthro = trex_functions.c_0_arthro

        # mean concentration estimate based on first application rate
        self.out_c_mean_sg = trex_functions.c_mean_sg
        self.out_c_mean_tg = trex_functions.c_mean_tg
        self.out_c_mean_blp = trex_functions.c_mean_blp
        self.out_c_mean_fp = trex_functions.c_mean_fp
        self.out_c_mean_arthro = trex_functions.c_mean_arthro

        # time series estimate based on first application rate - needs to be matrices for batch runs
        self.out_c_ts_sg = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.frac_act_ing, self.h_l, 240)  # short grass
        self.out_c_ts_tg = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.frac_act_ing, self.h_l, 110)  # tall grass
        self.out_c_ts_blp = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.frac_act_ing, self.h_l, 135)  # broad-leafed plants
        self.out_c_ts_fp = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.frac_act_ing, self.h_l, 15)  # fruits/pods
        self.out_c_ts_arthro = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.frac_act_ing, self.h_l, 94)  # arthropods

        # Table5
        logging.info("table 5")
        self.out_sa_bird_1_s = trex_functions.sa_bird_1(0.1, 0.02, self.aw_bird_sm, self.tw_bird_ld50)
        self.out_sa_bird_2_s = trex_functions.sa_bird_2(self.frac_act_ing, self.den, self.m_s_r_p, self.at_bird,
                                          self.ld50_bird, self.aw_bird_sm, self.tw_bird_ld50, self.x, 0.02)
        self.out_sc_bird_s = trex_functions.sc_bird(self.frac_act_ing, self.den, self.NOAEC_bird)
        self.out_sa_mamm_1_s = trex_functions.sa_mamm_1(self.frac_act_ing, self.den, self.at_mamm, self.fi_mamm, 0.1,
                                          self.ld50_mamm, self.aw_mamm_sm, self.tw_mamm, 0.015)
        self.out_sa_mamm_2_s = trex_functions.sa_mamm_2(self.frac_act_ing, self.den, self.m_s_r_p, self.at_mamm,
                                          self.ld50_mamm, self.aw_mamm_sm, self.tw_mamm, 0.015)
        self.out_sc_mamm_s = trex_functions.sc_mamm(self.frac_act_ing, self.den, self.NOAEL_mamm, self.aw_mamm_sm,
                                      self.fi_mamm, 0.1, self.tw_mamm, self.ANOAEL_mamm, 0.015)

        self.out_sa_bird_1_m = trex_functions.sa_bird_1(0.1, 0.1, self.aw_bird_md, self.tw_bird_ld50)
        self.out_sa_bird_2_m = trex_functions.sa_bird_2(self.frac_act_ing, self.den, self.m_s_r_p, self.at_bird,
                                          self.ld50_bird, self.aw_bird_md, self.tw_bird_ld50, self.x, 0.1)
        self.out_sc_bird_m = trex_functions.sc_bird(self.frac_act_ing, self.den, self.NOAEC_bird)
        self.out_sa_mamm_1_m = trex_functions.sa_mamm_1(self.frac_act_ing, self.den, self.at_mamm, self.fi_mamm, 0.1,
                                          self.ld50_mamm, self.aw_mamm_md, self.tw_mamm, 0.035)
        self.out_sa_mamm_2_m = trex_functions.sa_mamm_2(self.frac_act_ing, self.den, self.m_s_r_p, self.at_mamm,
                                          self.ld50_mamm, self.aw_mamm_md, self.tw_mamm, 0.035)
        self.out_sc_mamm_m = trex_functions.sc_mamm(self.frac_act_ing, self.den, self.NOAEL_mamm, self.aw_mamm_md,
                                      self.fi_mamm, 0.1, self.tw_mamm, self.ANOAEL_mamm, 0.035)

        self.out_sa_bird_1_l = trex_functions.sa_bird_1(0.1, 1.0, self.aw_bird_lg, self.tw_bird_ld50)
        self.out_sa_bird_2_l = trex_functions.sa_bird_2(self.frac_act_ing, self.den, self.m_s_r_p, self.at_bird,
                                          self.ld50_bird, self.aw_bird_lg, self.tw_bird_ld50, self.x, 1.0)
        self.out_sc_bird_l = trex_functions.sc_bird(self.frac_act_ing, self.den, self.NOAEC_bird)
        self.out_sa_mamm_1_l = trex_functions.sa_mamm_1(self.frac_act_ing, self.den, self.at_mamm, self.fi_mamm, 0.1,
                                          self.ld50_mamm, self.aw_mamm_lg, self.tw_mamm, 1)
        self.out_sa_mamm_2_l = trex_functions.sa_mamm_2(self.frac_act_ing, self.den, self.m_s_r_p, self.at_mamm,
                                          self.ld50_mamm, self.aw_mamm_lg, self.tw_mamm, 1)
        self.out_sc_mamm_l = trex_functions.sc_mamm(self.frac_act_ing, self.den, self.NOAEL_mamm, self.aw_mamm_lg,
                                      self.fi_mamm, 0.1, self.tw_mamm, self.ANOAEL_mamm, 1)

        # Table 6
        logging.info("table 6")
        self.out_EEC_diet_SG = trex_functions.EEC_diet(self.C_t_sg, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                         self.day_out)
        self.out_EEC_diet_TG = trex_functions.EEC_diet(self.C_t_tg, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                         self.day_out)
        self.out_EEC_diet_BP = trex_functions.EEC_diet(self.C_t_blp, self.noa, self.first_app_lb, self.frac_act_ing, 135,
                                         self.h_l, self.day_out)
        self.out_EEC_diet_FR = trex_functions.EEC_diet(self.C_t_f_p, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                         self.day_out)
        self.out_EEC_diet_AR = trex_functions.EEC_diet(self.C_t_arhtro, self.noa, self.first_app_lb, self.frac_act_ing, 94,
                                         self.h_l, self.day_out)

        # Table 7
        logging.info("table 7")
        self.out_EEC_dose_bird_SG_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_SG_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_SG_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_TG_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_TG_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_TG_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_BP_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_BP_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_BP_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_FP_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_FP_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_FP_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_AR_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_AR_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_AR_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_SE_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_SE_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_bird_SE_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)

        # Table 7_add
        self.out_ARQ_bird_SG_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_SG_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_SG_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_TG_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_TG_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_TG_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_BP_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_BP_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_BP_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_FP_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_FP_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_FP_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_AR_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_AR_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_AR_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_SE_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.1, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_SE_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.1, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                 self.day_out)
        self.out_ARQ_bird_SE_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.1, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                 self.day_out)

        # Table 8
        logging.info("table 8")
        self.out_ARQ_diet_bird_SG_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 240, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_SG_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 240, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_TG_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 110, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_TG_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 110, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_BP_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 135, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_BP_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 135, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_FP_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 15, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_FP_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 15, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_AR_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 94, self.h_l, self.day_out)
        self.out_ARQ_diet_bird_AR_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.frac_act_ing, 94, self.h_l, self.day_out)

        # Table 9
        logging.info("table 9")
        self.out_EEC_dose_mamm_SG_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_SG_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_SG_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_TG_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_TG_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_TG_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_BP_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_BP_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_BP_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_FP_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_FP_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_FP_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_AR_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_AR_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_AR_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_SE_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_SE_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_EEC_dose_mamm_SE_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)

        # Table 10
        logging.info("table 10")
        self.out_ARQ_dose_mamm_SG_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_SG_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_SG_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_SG_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_SG_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_SG_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 240,
                                                      self.h_l, self.day_out)

        self.out_ARQ_dose_mamm_TG_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_TG_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_TG_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_TG_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_TG_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_TG_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 110,
                                                      self.h_l, self.day_out)

        self.out_ARQ_dose_mamm_BP_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_BP_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_BP_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_BP_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_BP_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_BP_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 135,
                                                      self.h_l, self.day_out)

        self.out_ARQ_dose_mamm_FP_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_FP_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_FP_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_FP_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_FP_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_FP_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15,
                                                      self.h_l, self.day_out)

        self.out_ARQ_dose_mamm_AR_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_AR_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_AR_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_AR_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_AR_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_AR_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 94,
                                                      self.h_l, self.day_out)

        self.out_ARQ_dose_mamm_SE_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_SE_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.1,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_SE_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_SE_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.1,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15,
                                                      self.h_l, self.day_out)
        self.out_ARQ_dose_mamm_SE_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15, self.h_l,
                                                      self.day_out)
        self.out_CRQ_dose_mamm_SE_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.1,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.frac_act_ing, 15,
                                                      self.h_l, self.day_out)

        # table 11
        logging.info("table 11")
        if self.lc50_mamm != 'N/A':
            self.out_ARQ_diet_mamm_SG = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.frac_act_ing, 240, self.h_l, self.day_out)
            self.out_ARQ_diet_mamm_TG = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.frac_act_ing, 110, self.h_l, self.day_out)
            self.out_ARQ_diet_mamm_BP = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.frac_act_ing, 135, self.h_l, self.day_out)
            self.out_ARQ_diet_mamm_FP = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.frac_act_ing, 15, self.h_l, self.day_out)
            self.out_ARQ_diet_mamm_AR = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.frac_act_ing, 94, self.h_l, self.day_out)
        else:
            self.out_ARQ_diet_mamm_SG = 'N/A'
            self.out_ARQ_diet_mamm_TG = 'N/A'
            self.out_ARQ_diet_mamm_BP = 'N/A'
            self.out_ARQ_diet_mamm_FP = 'N/A'
            self.out_ARQ_diet_mamm_AR = 'N/A'

        self.out_CRQ_diet_mamm_SG = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.frac_act_ing, 240, self.h_l, self.day_out)
        self.out_CRQ_diet_mamm_TG = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.frac_act_ing, 110, self.h_l, self.day_out)
        self.out_CRQ_diet_mamm_BP = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.frac_act_ing, 135, self.h_l, self.day_out)
        self.out_CRQ_diet_mamm_FP = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.frac_act_ing, 15, self.h_l, self.day_out)
        self.out_CRQ_diet_mamm_AR = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.frac_act_ing, 94, self.h_l, self.day_out)

        # Table12
        logging.info("table 12")
        self.out_LD50_rg_bird_sm = trex_functions.LD50_rg_bird(self.first_app_lb, self.frac_act_ing, self.p_i, self.r_s,
                                                 self.b_w, self.aw_bird_sm, self.at_bird, self.ld50_bird,
                                                 self.tw_bird_ld50, self.x)
        self.out_LD50_rg_mamm_sm = trex_functions.LD50_rg_mamm(self.first_app_lb, self.frac_act_ing, self.p_i, self.r_s,
                                                 self.b_w, self.aw_mamm_sm, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_rg_bird_md = trex_functions.LD50_rg_bird(self.first_app_lb, self.frac_act_ing, self.p_i, self.r_s,
                                                 self.b_w, self.aw_bird_md, self.at_bird, self.ld50_bird,
                                                 self.tw_bird_ld50, self.x)
        self.out_LD50_rg_mamm_md = trex_functions.LD50_rg_mamm(self.first_app_lb, self.frac_act_ing, self.p_i, self.r_s,
                                                 self.b_w, self.aw_mamm_md, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_rg_bird_lg = trex_functions.LD50_rg_bird(self.first_app_lb, self.frac_act_ing, self.p_i, self.r_s,
                                                 self.b_w, self.aw_bird_lg, self.at_bird, self.ld50_bird,
                                                 self.tw_bird_ld50, self.x)
        self.out_LD50_rg_mamm_lg = trex_functions.LD50_rg_mamm(self.first_app_lb, self.frac_act_ing, self.p_i, self.r_s,
                                                 self.b_w, self.aw_mamm_lg, self.at_mamm, self.ld50_mamm, self.tw_mamm)

        # Table13
        logging.info("table 13")
        self.out_LD50_rl_bird_sm = trex_functions.LD50_rl_bird(self.first_app_lb, self.frac_act_ing, self.p_i, self.b_w,
                                                 self.aw_bird_sm, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.out_LD50_rl_mamm_sm = trex_functions.LD50_rl_mamm(self.first_app_lb, self.frac_act_ing, self.p_i, self.b_w,
                                                 self.aw_mamm_sm, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_rl_bird_md = trex_functions.LD50_rl_bird(self.first_app_lb, self.frac_act_ing, self.p_i, self.b_w,
                                                 self.aw_bird_md, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.out_LD50_rl_mamm_md = trex_functions.LD50_rl_mamm(self.first_app_lb, self.frac_act_ing, self.p_i, self.b_w,
                                                 self.aw_mamm_md, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_rl_bird_lg = trex_functions.LD50_rl_bird(self.first_app_lb, self.frac_act_ing, self.p_i, self.b_w,
                                                 self.aw_bird_lg, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.out_LD50_rl_mamm_lg = trex_functions.LD50_rl_mamm(self.first_app_lb, self.frac_act_ing, self.p_i, self.b_w,
                                                 self.aw_mamm_lg, self.at_mamm, self.ld50_mamm, self.tw_mamm)

        # Table14
        logging.info("table 14")
        self.out_LD50_bg_bird_sm = trex_functions.LD50_bg_bird(self.first_app_lb, self.frac_act_ing, self.p_i,
                                                 self.aw_bird_sm, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.out_LD50_bg_mamm_sm = trex_functions.LD50_bg_mamm(self.first_app_lb, self.frac_act_ing, self.p_i,
                                                 self.aw_mamm_sm, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_bg_bird_md = trex_functions.LD50_bg_bird(self.first_app_lb, self.frac_act_ing, self.p_i,
                                                 self.aw_bird_md, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.out_LD50_bg_mamm_md = trex_functions.LD50_bg_mamm(self.first_app_lb, self.frac_act_ing, self.p_i,
                                                 self.aw_mamm_md, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_bg_bird_lg = trex_functions.LD50_bg_bird(self.first_app_lb, self.frac_act_ing, self.p_i,
                                                 self.aw_bird_lg, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.out_LD50_bg_mamm_lg = trex_functions.LD50_bg_mamm(self.first_app_lb, self.frac_act_ing, self.p_i,
                                                 self.aw_mamm_lg, self.at_mamm, self.ld50_mamm, self.tw_mamm)

        # Table15
        logging.info("table 15")
        self.out_LD50_bl_bird_sm = trex_functions.LD50_bl_bird(self.first_app_lb, self.frac_act_ing, self.aw_bird_sm,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x)
        self.out_LD50_bl_mamm_sm = trex_functions.LD50_bl_mamm(self.first_app_lb, self.frac_act_ing, self.aw_mamm_sm,
                                                 self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_bl_bird_md = trex_functions.LD50_bl_bird(self.first_app_lb, self.frac_act_ing, self.aw_bird_md,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x)
        self.out_LD50_bl_mamm_md = trex_functions.LD50_bl_mamm(self.first_app_lb, self.frac_act_ing, self.aw_mamm_md,
                                                 self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.out_LD50_bl_bird_lg = trex_functions.LD50_bl_bird(self.first_app_lb, self.frac_act_ing, self.aw_bird_lg,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x)
        self.out_LD50_bl_mamm_lg = trex_functions.LD50_bl_mamm(self.first_app_lb, self.frac_act_ing, self.aw_mamm_lg,
                                                 self.at_mamm, self.ld50_mamm, self.tw_mamm)