from functools import wraps
import logging
# import numpy as np
import pandas as pd
import time
import trex_functions

def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("trex2_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result

    return measure_time


class trex2(object):
    @timefn
    def __init__(self, run_type, pd_obj, pd_obj_exp):
        logging.info("************** trex back end **********************")
        # run_type can be single, batch or qaqc
        self.run_type = run_type

        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.chem_name = pd_obj['chem_name']
        self.use = pd_obj['use']
        self.formu_name = pd_obj['formu_name']
        self.a_i = pd_obj['a_i']
        self.a_i /= 100  # change from percentage to proportion
        self.Application_type = pd_obj['Application_type']
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

        # needs to be dataframe for batch runs
        #convert lists to series
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
        self.x = pd_obj['x']  # mineau scaling factor
        self.ld50_mamm = pd_obj['ld50_mamm']
        self.lc50_mamm = pd_obj['lc50_mamm']
        self.NOAEC_mamm = pd_obj['NOAEC_mamm']
        self.NOAEL_mamm = pd_obj['NOAEL_mamm']
        self.aw_mamm_sm = pd_obj['aw_mamm_sm']
        self.aw_mamm_md = pd_obj['aw_mamm_md']
        self.aw_mamm_lg = pd_obj['aw_mamm_lg']
        self.tw_mamm = pd_obj['tw_mamm']
        self.m_s_r_p = pd_obj['m_s_r_p']

        # Outputs: Assign object attribute variables to Pandas Series
        # initial concentrations for different food types
        self.C_0_sg = pd.Series(name="C_0_sg")  # short grass
        self.C_0_tg = pd.Series(name="C_0_tg")  # tall grass
        self.C_0_blp = pd.Series(name="C_0_blp")  # broad-leafed plants
        self.C_0_fp = pd.Series(name="C_0_fp")  # fruits/pods
        self.C_0_arthro = pd.Series(name="C_0_arthro")  # arthropods

        # mean concentration estimate based on first application rate
        self.C_mean_sg = pd.Series(name="C_mean_sg")  # short grass
        self.C_mean_tg = pd.Series(name="C_mean_tg")  # tall grass
        self.C_mean_blp = pd.Series(name="C_mean_blp")  # broad-leafed plants
        self.C_mean_fp = pd.Series(name="C_mean_fp")  # fruits/pods
        self.C_mean_arthro = pd.Series(name="C_mean_arthro")  # arthropods

        # time series estimate based on first application rate - needs to be matrices for batch runs
        self.C_ts_sg = pd.Series(name="C_ts_sg")  # short grass
        self.C_ts_tg = pd.Series(name="C_ts_tg")  # tall grass
        self.C_ts_blp = pd.Series(name="C_ts_blp")  # broad-leafed plants
        self.C_ts_fp = pd.Series(name="C_ts_fp")  # fruits/pods
        self.C_ts_arthro = pd.Series(name="C_ts_arthro")  # arthropods

        # Table5
        self.sa_bird_1_s = pd.Series(name="sa_bird_1_s")
        self.sa_bird_2_s = pd.Series(name="sa_bird_2_s")
        self.sc_bird_s = pd.Series(name="sc_bird_s")
        self.sa_mamm_1_s = pd.Series(name="sa_mamm_1_s")
        self.sa_mamm_2_s = pd.Series(name="sa_mamm_2_s")
        self.sc_mamm_s = pd.Series(name="sc_mamm_s")

        self.sa_bird_1_m = pd.Series(name="sa_bird_1_m")
        self.sa_bird_2_m = pd.Series(name="sa_bird_2_m")
        self.sc_bird_m = pd.Series(name="sc_bird_m")
        self.sa_mamm_1_m = pd.Series(name="sa_mamm_1_m")
        self.sa_mamm_2_m = pd.Series(name="sa_mamm_2_m")
        self.sc_mamm_m = pd.Series(name="sc_mamm_m")

        self.sa_bird_1_l = pd.Series(name="sa_bird_1_l")
        self.sa_bird_2_l = pd.Series(name="sa_bird_2_l")
        self.sc_bird_l = pd.Series(name="sc_bird_l")
        self.sa_mamm_1_l = pd.Series(name="sa_mamm_1_l")
        self.sa_mamm_2_l = pd.Series(name="sa_mamm_2_l")
        self.sc_mamm_l = pd.Series(name="sc_mamm_l")

        # Table 6
        self.EEC_diet_SG = pd.Series(name="EEC_diet_SG")
        self.EEC_diet_TG = pd.Series(name="EEC_diet_TG")
        self.EEC_diet_BP = pd.Series(name="EEC_diet_BP")
        self.EEC_diet_FR = pd.Series(name="EEC_diet_FR")
        self.EEC_diet_AR = pd.Series(name="EEC_diet_AR")

        # Table 7
        self.EEC_dose_bird_SG_sm = pd.Series(name="EEC_dose_bird_SG_sm")
        self.EEC_dose_bird_SG_md = pd.Series(name="EEC_dose_bird_SG_md")
        self.EEC_dose_bird_SG_lg = pd.Series(name="EEC_dose_bird_SG_lg")
        self.EEC_dose_bird_TG_sm = pd.Series(name="EEC_dose_bird_TG_sm")
        self.EEC_dose_bird_TG_md = pd.Series(name="EEC_dose_bird_TG_md")
        self.EEC_dose_bird_TG_lg = pd.Series(name="EEC_dose_bird_TG_lg")
        self.EEC_dose_bird_BP_sm = pd.Series(name="EEC_dose_bird_BP_sm")
        self.EEC_dose_bird_BP_md = pd.Series(name="EEC_dose_bird_BP_md")
        self.EEC_dose_bird_BP_lg = pd.Series(name="EEC_dose_bird_BP_lg")
        self.EEC_dose_bird_FP_sm = pd.Series(name="EEC_dose_bird_FP_sm")
        self.EEC_dose_bird_FP_md = pd.Series(name="EEC_dose_bird_FP_md")
        self.EEC_dose_bird_FP_lg = pd.Series(name="EEC_dose_bird_FP_lg")
        self.EEC_dose_bird_AR_sm = pd.Series(name="EEC_dose_bird_AR_sm")
        self.EEC_dose_bird_AR_md = pd.Series(name="EEC_dose_bird_AR_md")
        self.EEC_dose_bird_AR_lg = pd.Series(name="EEC_dose_bird_AR_lg")
        self.EEC_dose_bird_SE_sm = pd.Series(name="EEC_dose_bird_SE_sm")
        self.EEC_dose_bird_SE_md = pd.Series(name="EEC_dose_bird_SE_md")
        self.EEC_dose_bird_SE_lg = pd.Series(name="EEC_dose_bird_SE_lg")

        # Table 7_add
        self.ARQ_bird_SG_sm = pd.Series(name="ARQ_bird_SG_sm")
        self.ARQ_bird_SG_md = pd.Series(name="ARQ_bird_SG_md")
        self.ARQ_bird_SG_lg = pd.Series(name="ARQ_bird_SG_lg")
        self.ARQ_bird_TG_sm = pd.Series(name="ARQ_bird_TG_sm")
        self.ARQ_bird_TG_md = pd.Series(name="ARQ_bird_TG_md")
        self.ARQ_bird_TG_lg = pd.Series(name="ARQ_bird_TG_lg")
        self.ARQ_bird_BP_sm = pd.Series(name="ARQ_bird_BP_sm")
        self.ARQ_bird_BP_md = pd.Series(name="ARQ_bird_BP_md")
        self.ARQ_bird_BP_lg = pd.Series(name="ARQ_bird_BP_lg")
        self.ARQ_bird_FP_sm = pd.Series(name="ARQ_bird_FP_sm")
        self.ARQ_bird_FP_md = pd.Series(name="ARQ_bird_FP_md")
        self.ARQ_bird_FP_lg = pd.Series(name="ARQ_bird_FP_lg")
        self.ARQ_bird_AR_sm = pd.Series(name="ARQ_bird_AR_sm")
        self.ARQ_bird_AR_md = pd.Series(name="ARQ_bird_AR_md")
        self.ARQ_bird_AR_lg = pd.Series(name="ARQ_bird_AR_lg")
        self.ARQ_bird_SE_sm = pd.Series(name="ARQ_bird_SE_sm")
        self.ARQ_bird_SE_md = pd.Series(name="ARQ_bird_SE_md")
        self.ARQ_bird_SE_lg = pd.Series(name="ARQ_bird_SE_lg")

        # Table 8
        self.ARQ_diet_bird_SG_A = pd.Series(name="ARQ_diet_bird_SG_A")
        self.ARQ_diet_bird_SG_C = pd.Series(name="ARQ_diet_bird_SG_C")
        self.ARQ_diet_bird_TG_A = pd.Series(name="ARQ_diet_bird_TG_A")
        self.ARQ_diet_bird_TG_C = pd.Series(name="ARQ_diet_bird_TG_C")
        self.ARQ_diet_bird_BP_A = pd.Series(name="ARQ_diet_bird_BP_A")
        self.ARQ_diet_bird_BP_C = pd.Series(name="ARQ_diet_bird_BP_C")
        self.ARQ_diet_bird_FP_A = pd.Series(name="ARQ_diet_bird_FP_A")
        self.ARQ_diet_bird_FP_C = pd.Series(name="ARQ_diet_bird_FP_C")
        self.ARQ_diet_bird_AR_A = pd.Series(name="ARQ_diet_bird_AR_A")
        self.ARQ_diet_bird_AR_C = pd.Series(name="ARQ_diet_bird_AR_C")

        # Table 9
        self.EEC_dose_mamm_SG_sm = pd.Series(name="EEC_dose_mamm_SG_sm")
        self.EEC_dose_mamm_SG_md = pd.Series(name="EEC_dose_mamm_SG_md")
        self.EEC_dose_mamm_SG_lg = pd.Series(name="EEC_dose_mamm_SG_lg")
        self.EEC_dose_mamm_TG_sm = pd.Series(name="EEC_dose_mamm_TG_sm")
        self.EEC_dose_mamm_TG_md = pd.Series(name="EEC_dose_mamm_TG_md")
        self.EEC_dose_mamm_TG_lg = pd.Series(name="EEC_dose_mamm_TG_lg")
        self.EEC_dose_mamm_BP_sm = pd.Series(name="EEC_dose_mamm_BP_sm")
        self.EEC_dose_mamm_BP_md = pd.Series(name="EEC_dose_mamm_BP_md")
        self.EEC_dose_mamm_BP_lg = pd.Series(name="EEC_dose_mamm_BP_lg")
        self.EEC_dose_mamm_FP_sm = pd.Series(name="EEC_dose_mamm_FP_sm")
        self.EEC_dose_mamm_FP_md = pd.Series(name="EEC_dose_mamm_FP_md")
        self.EEC_dose_mamm_FP_lg = pd.Series(name="EEC_dose_mamm_FP_lg")
        self.EEC_dose_mamm_AR_sm = pd.Series(name="EEC_dose_mamm_AR_sm")
        self.EEC_dose_mamm_AR_md = pd.Series(name="EEC_dose_mamm_AR_md")
        self.EEC_dose_mamm_AR_lg = pd.Series(name="EEC_dose_mamm_AR_lg")
        self.EEC_dose_mamm_SE_sm = pd.Series(name="EEC_dose_mamm_SE_sm")
        self.EEC_dose_mamm_SE_md = pd.Series(name="EEC_dose_mamm_SE_md")
        self.EEC_dose_mamm_SE_lg = pd.Series(name="EEC_dose_mamm_SE_lg")

        # Table 10
        self.ARQ_dose_mamm_SG_sm = pd.Series(name="ARQ_dose_mamm_SG_sm")
        self.CRQ_dose_mamm_SG_sm = pd.Series(name="CRQ_dose_mamm_SG_sm")
        self.ARQ_dose_mamm_SG_md = pd.Series(name="ARQ_dose_mamm_SG_md")
        self.CRQ_dose_mamm_SG_md = pd.Series(name="CRQ_dose_mamm_SG_md")
        self.ARQ_dose_mamm_SG_lg = pd.Series(name="ARQ_dose_mamm_SG_lg")
        self.CRQ_dose_mamm_SG_lg = pd.Series(name="CRQ_dose_mamm_SG_lg")

        self.ARQ_dose_mamm_TG_sm = pd.Series(name="ARQ_dose_mamm_TG_sm")
        self.CRQ_dose_mamm_TG_sm = pd.Series(name="CRQ_dose_mamm_TG_sm")
        self.ARQ_dose_mamm_TG_md = pd.Series(name="ARQ_dose_mamm_TG_md")
        self.CRQ_dose_mamm_TG_md = pd.Series(name="CRQ_dose_mamm_TG_md")
        self.ARQ_dose_mamm_TG_lg = pd.Series(name="ARQ_dose_mamm_TG_lg")
        self.CRQ_dose_mamm_TG_lg = pd.Series(name="CRQ_dose_mamm_TG_lg")

        self.ARQ_dose_mamm_BP_sm = pd.Series(name="ARQ_dose_mamm_BP_sm")
        self.CRQ_dose_mamm_BP_sm = pd.Series(name="CRQ_dose_mamm_BP_sm")
        self.ARQ_dose_mamm_BP_md = pd.Series(name="ARQ_dose_mamm_BP_md")
        self.CRQ_dose_mamm_BP_md = pd.Series(name="CRQ_dose_mamm_BP_md")
        self.ARQ_dose_mamm_BP_lg = pd.Series(name="ARQ_dose_mamm_BP_lg")
        self.CRQ_dose_mamm_BP_lg = pd.Series(name="CRQ_dose_mamm_BP_lg")

        self.ARQ_dose_mamm_FP_sm = pd.Series(name="ARQ_dose_mamm_FP_sm")
        self.CRQ_dose_mamm_FP_sm = pd.Series(name="CRQ_dose_mamm_FP_sm")
        self.ARQ_dose_mamm_FP_md = pd.Series(name="ARQ_dose_mamm_FP_md")
        self.CRQ_dose_mamm_FP_md = pd.Series(name="CRQ_dose_mamm_FP_md")
        self.ARQ_dose_mamm_FP_lg = pd.Series(name="ARQ_dose_mamm_FP_lg")
        self.CRQ_dose_mamm_FP_lg = pd.Series(name="CRQ_dose_mamm_FP_lg")

        self.ARQ_dose_mamm_AR_sm = pd.Series(name="ARQ_dose_mamm_AR_sm")
        self.CRQ_dose_mamm_AR_sm = pd.Series(name="CRQ_dose_mamm_AR_sm")
        self.ARQ_dose_mamm_AR_md = pd.Series(name="ARQ_dose_mamm_AR_md")
        self.CRQ_dose_mamm_AR_md = pd.Series(name="CRQ_dose_mamm_AR_md")
        self.ARQ_dose_mamm_AR_lg = pd.Series(name="ARQ_dose_mamm_AR_lg")
        self.CRQ_dose_mamm_AR_lg = pd.Series(name="CRQ_dose_mamm_AR_lg")

        self.ARQ_dose_mamm_SE_sm = pd.Series(name="ARQ_dose_mamm_SE_sm")
        self.CRQ_dose_mamm_SE_sm = pd.Series(name="CRQ_dose_mamm_SE_sm")
        self.ARQ_dose_mamm_SE_md = pd.Series(name="ARQ_dose_mamm_SE_md")
        self.CRQ_dose_mamm_SE_md = pd.Series(name="CRQ_dose_mamm_SE_md")
        self.ARQ_dose_mamm_SE_lg = pd.Series(name="ARQ_dose_mamm_SE_lg")
        self.CRQ_dose_mamm_SE_lg = pd.Series(name="CRQ_dose_mamm_SE_lg")

        # table 11
        self.ARQ_diet_mamm_SG = pd.Series(name="ARQ_diet_mamm_SG")
        self.ARQ_diet_mamm_TG = pd.Series(name="ARQ_diet_mamm_TG")
        self.ARQ_diet_mamm_BP = pd.Series(name="ARQ_diet_mamm_BP")
        self.ARQ_diet_mamm_FP = pd.Series(name="ARQ_diet_mamm_FP")
        self.ARQ_diet_mamm_AR = pd.Series(name="ARQ_diet_mamm_AR")

        self.CRQ_diet_mamm_SG = pd.Series(name="CRQ_diet_mamm_SG")
        self.CRQ_diet_mamm_TG = pd.Series(name="CRQ_diet_mamm_TG")
        self.CRQ_diet_mamm_BP = pd.Series(name="CRQ_diet_mamm_BP")
        self.CRQ_diet_mamm_FP = pd.Series(name="CRQ_diet_mamm_FP")
        self.CRQ_diet_mamm_AR = pd.Series(name="CRQ_diet_mamm_AR")

        # Table12
        self.LD50_rg_bird_sm = pd.Series(name="LD50_rg_bird_sm")
        self.LD50_rg_mamm_sm = pd.Series(name="LD50_rg_mamm_sm")
        self.LD50_rg_bird_md = pd.Series(name="LD50_rg_bird_md")
        self.LD50_rg_mamm_md = pd.Series(name="LD50_rg_mamm_md")
        self.LD50_rg_bird_lg = pd.Series(name="LD50_rg_bird_lg")
        self.LD50_rg_mamm_lg = pd.Series(name="LD50_rg_mamm_lg")

        # Table13
        self.LD50_rl_bird_sm = pd.Series(name="LD50_rl_bird_sm")
        self.LD50_rl_mamm_sm = pd.Series(name="LD50_rl_mamm_sm")
        self.LD50_rl_bird_md = pd.Series(name="LD50_rl_bird_md")
        self.LD50_rl_mamm_md = pd.Series(name="LD50_rl_mamm_md")
        self.LD50_rl_bird_lg = pd.Series(name="LD50_rl_bird_lg")
        self.LD50_rl_mamm_lg = pd.Series(name="LD50_rl_mamm_lg")

        # Table14
        self.LD50_bg_bird_sm = pd.Series(name="LD50_bg_bird_sm")
        self.LD50_bg_mamm_sm = pd.Series(name="LD50_bg_mamm_sm")
        self.LD50_bg_bird_md = pd.Series(name="LD50_bg_bird_md")
        self.LD50_bg_mamm_md = pd.Series(name="LD50_bg_mamm_md")
        self.LD50_bg_bird_lg = pd.Series(name="LD50_bg_bird_lg")
        self.LD50_bg_mamm_lg = pd.Series(name="LD50_bg_mamm_lg")

        # Table15
        self.LD50_bl_bird_sm = pd.Series(name="LD50_bl_bird_sm")
        self.LD50_bl_mamm_sm = pd.Series(name="LD50_bl_mamm_sm")
        self.LD50_bl_bird_md = pd.Series(name="LD50_bl_bird_md")
        self.LD50_bl_mamm_md = pd.Series(name="LD50_bl_mamm_md")
        self.LD50_bl_bird_lg = pd.Series(name="LD50_bl_bird_lg")
        self.LD50_bl_mamm_lg = pd.Series(name="LD50_bl_mamm_lg")

        # Execute model methods
        self.run_methods()

        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame({
            # Table5
            'sa_bird_1_s': self.sa_bird_1_s,
            'sa_bird_2_s': self.sa_bird_2_s,
            'sc_bird_s': self.sc_bird_s,
            'sa_mamm_1_s': self.sa_mamm_1_s,
            'sa_mamm_2_s': self.sa_mamm_2_s,
            'sc_mamm_s': self.sc_mamm_s,

            'sa_bird_1_m': self.sa_bird_1_m,
            'sa_bird_2_m': self.sa_bird_2_m,
            'sc_bird_m': self.sc_bird_m,
            'sa_mamm_1_m': self.sa_mamm_1_m,
            'sa_mamm_2_m': self.sa_mamm_2_m,
            'sc_mamm_m': self.sc_mamm_m,

            'sa_bird_1_l': self.sa_bird_1_l,
            'sa_bird_2_l': self.sa_bird_2_l,
            'sc_bird_l': self.sc_bird_l,
            'sa_mamm_1_l': self.sa_mamm_1_l,
            'sa_mamm_2_l': self.sa_mamm_2_l,
            'sc_mamm_l': self.sc_mamm_l,

            # Table 6
            'EEC_diet_SG': self.EEC_diet_SG,
            'EEC_diet_TG': self.EEC_diet_TG,
            'EEC_diet_BP': self.EEC_diet_BP,
            'EEC_diet_FR': self.EEC_diet_FR,
            'EEC_diet_AR': self.EEC_diet_AR,

            # Table 7
            'EEC_dose_bird_SG_sm': self.EEC_dose_bird_SG_sm,
            'EEC_dose_bird_SG_md': self.EEC_dose_bird_SG_md,
            'EEC_dose_bird_SG_lg': self.EEC_dose_bird_SG_lg,
            'EEC_dose_bird_TG_sm': self.EEC_dose_bird_TG_sm,
            'EEC_dose_bird_TG_md': self.EEC_dose_bird_TG_md,
            'EEC_dose_bird_TG_lg': self.EEC_dose_bird_TG_lg,
            'EEC_dose_bird_BP_sm': self.EEC_dose_bird_BP_sm,
            'EEC_dose_bird_BP_md': self.EEC_dose_bird_BP_md,
            'EEC_dose_bird_BP_lg': self.EEC_dose_bird_BP_lg,
            'EEC_dose_bird_FP_sm': self.EEC_dose_bird_FP_sm,
            'EEC_dose_bird_FP_md': self.EEC_dose_bird_FP_md,
            'EEC_dose_bird_FP_lg': self.EEC_dose_bird_FP_lg,
            'EEC_dose_bird_AR_sm': self.EEC_dose_bird_AR_sm,
            'EEC_dose_bird_AR_md': self.EEC_dose_bird_AR_md,
            'EEC_dose_bird_AR_lg': self.EEC_dose_bird_AR_lg,
            'EEC_dose_bird_SE_sm': self.EEC_dose_bird_SE_sm,
            'EEC_dose_bird_SE_md': self.EEC_dose_bird_SE_md,
            'EEC_dose_bird_SE_lg': self.EEC_dose_bird_SE_lg,

            # Table 7_add
            'ARQ_bird_SG_sm': self.ARQ_bird_SG_sm,
            'ARQ_bird_SG_md': self.ARQ_bird_SG_md,
            'ARQ_bird_SG_lg': self.ARQ_bird_SG_lg,
            'ARQ_bird_TG_sm': self.ARQ_bird_TG_sm,
            'ARQ_bird_TG_md': self.ARQ_bird_TG_md,
            'ARQ_bird_TG_lg': self.ARQ_bird_TG_lg,
            'ARQ_bird_BP_sm': self.ARQ_bird_BP_sm,
            'ARQ_bird_BP_md': self.ARQ_bird_BP_md,
            'ARQ_bird_BP_lg': self.ARQ_bird_BP_lg,
            'ARQ_bird_FP_sm': self.ARQ_bird_FP_sm,
            'ARQ_bird_FP_md': self.ARQ_bird_FP_md,
            'ARQ_bird_FP_lg': self.ARQ_bird_FP_lg,
            'ARQ_bird_AR_sm': self.ARQ_bird_AR_sm,
            'ARQ_bird_AR_md': self.ARQ_bird_AR_md,
            'ARQ_bird_AR_lg': self.ARQ_bird_AR_lg,
            'ARQ_bird_SE_sm': self.ARQ_bird_SE_sm,
            'ARQ_bird_SE_md': self.ARQ_bird_SE_md,
            'ARQ_bird_SE_lg': self.ARQ_bird_SE_lg,

            # Table 8
            'ARQ_diet_bird_SG_A': self.ARQ_diet_bird_SG_A,
            'ARQ_diet_bird_SG_C': self.ARQ_diet_bird_SG_C,
            'ARQ_diet_bird_TG_A': self.ARQ_diet_bird_TG_A,
            'ARQ_diet_bird_TG_C': self.ARQ_diet_bird_TG_C,
            'ARQ_diet_bird_BP_A': self.ARQ_diet_bird_BP_A,
            'ARQ_diet_bird_BP_C': self.ARQ_diet_bird_BP_C,
            'ARQ_diet_bird_FP_A': self.ARQ_diet_bird_FP_A,
            'ARQ_diet_bird_FP_C': self.ARQ_diet_bird_FP_C,
            'ARQ_diet_bird_AR_A': self.ARQ_diet_bird_AR_A,
            'ARQ_diet_bird_AR_C': self.ARQ_diet_bird_AR_C,

            # Table 9
            'EEC_dose_mamm_SG_sm': self.EEC_dose_mamm_SG_sm,
            'EEC_dose_mamm_SG_md': self.EEC_dose_mamm_SG_md,
            'EEC_dose_mamm_SG_lg': self.EEC_dose_mamm_SG_lg,
            'EEC_dose_mamm_TG_sm': self.EEC_dose_mamm_TG_sm,
            'EEC_dose_mamm_TG_md': self.EEC_dose_mamm_TG_md,
            'EEC_dose_mamm_TG_lg': self.EEC_dose_mamm_TG_lg,
            'EEC_dose_mamm_BP_sm': self.EEC_dose_mamm_BP_sm,
            'EEC_dose_mamm_BP_md': self.EEC_dose_mamm_BP_md,
            'EEC_dose_mamm_BP_lg': self.EEC_dose_mamm_BP_lg,
            'EEC_dose_mamm_FP_sm': self.EEC_dose_mamm_FP_sm,
            'EEC_dose_mamm_FP_md': self.EEC_dose_mamm_FP_md,
            'EEC_dose_mamm_FP_lg': self.EEC_dose_mamm_FP_lg,
            'EEC_dose_mamm_AR_sm': self.EEC_dose_mamm_AR_sm,
            'EEC_dose_mamm_AR_md': self.EEC_dose_mamm_AR_md,
            'EEC_dose_mamm_AR_lg': self.EEC_dose_mamm_AR_lg,
            'EEC_dose_mamm_SE_sm': self.EEC_dose_mamm_SE_sm,
            'EEC_dose_mamm_SE_md': self.EEC_dose_mamm_SE_md,
            'EEC_dose_mamm_SE_lg': self.EEC_dose_mamm_SE_lg,

            # Table 10
            'ARQ_dose_mamm_SG_sm': self.ARQ_dose_mamm_SG_sm,
            'CRQ_dose_mamm_SG_sm': self.CRQ_dose_mamm_SG_sm,
            'ARQ_dose_mamm_SG_md': self.ARQ_dose_mamm_SG_md,
            'CRQ_dose_mamm_SG_md': self.CRQ_dose_mamm_SG_md,
            'ARQ_dose_mamm_SG_lg': self.ARQ_dose_mamm_SG_lg,
            'CRQ_dose_mamm_SG_lg': self.CRQ_dose_mamm_SG_lg,

            'ARQ_dose_mamm_TG_sm': self.ARQ_dose_mamm_TG_sm,
            'CRQ_dose_mamm_TG_sm': self.CRQ_dose_mamm_TG_sm,
            'ARQ_dose_mamm_TG_md': self.ARQ_dose_mamm_TG_md,
            'CRQ_dose_mamm_TG_md': self.CRQ_dose_mamm_TG_md,
            'ARQ_dose_mamm_TG_lg': self.ARQ_dose_mamm_TG_lg,
            'CRQ_dose_mamm_TG_lg': self.CRQ_dose_mamm_TG_lg,

            'ARQ_dose_mamm_BP_sm': self.ARQ_dose_mamm_BP_sm,
            'CRQ_dose_mamm_BP_sm': self.CRQ_dose_mamm_BP_sm,
            'ARQ_dose_mamm_BP_md': self.ARQ_dose_mamm_BP_md,
            'CRQ_dose_mamm_BP_md': self.CRQ_dose_mamm_BP_md,
            'ARQ_dose_mamm_BP_lg': self.ARQ_dose_mamm_BP_lg,
            'CRQ_dose_mamm_BP_lg': self.CRQ_dose_mamm_BP_lg,

            'ARQ_dose_mamm_FP_sm': self.ARQ_dose_mamm_FP_sm,
            'CRQ_dose_mamm_FP_sm': self.CRQ_dose_mamm_FP_sm,
            'ARQ_dose_mamm_FP_md': self.ARQ_dose_mamm_FP_md,
            'CRQ_dose_mamm_FP_md': self.CRQ_dose_mamm_FP_md,
            'ARQ_dose_mamm_FP_lg': self.ARQ_dose_mamm_FP_lg,
            'CRQ_dose_mamm_FP_lg': self.CRQ_dose_mamm_FP_lg,

            'ARQ_dose_mamm_AR_sm': self.ARQ_dose_mamm_AR_sm,
            'CRQ_dose_mamm_AR_sm': self.CRQ_dose_mamm_AR_sm,
            'ARQ_dose_mamm_AR_md': self.ARQ_dose_mamm_AR_md,
            'CRQ_dose_mamm_AR_md': self.CRQ_dose_mamm_AR_md,
            'ARQ_dose_mamm_AR_lg': self.ARQ_dose_mamm_AR_lg,
            'CRQ_dose_mamm_AR_lg': self.CRQ_dose_mamm_AR_lg,

            'ARQ_dose_mamm_SE_sm': self.ARQ_dose_mamm_SE_sm,
            'CRQ_dose_mamm_SE_sm': self.CRQ_dose_mamm_SE_sm,
            'ARQ_dose_mamm_SE_md': self.ARQ_dose_mamm_SE_md,
            'CRQ_dose_mamm_SE_md': self.CRQ_dose_mamm_SE_md,
            'ARQ_dose_mamm_SE_lg': self.ARQ_dose_mamm_SE_lg,
            'CRQ_dose_mamm_SE_lg': self.CRQ_dose_mamm_SE_lg,

            # table 11
            'ARQ_diet_mamm_SG': self.ARQ_diet_mamm_SG,
            'ARQ_diet_mamm_TG': self.ARQ_diet_mamm_TG,
            'ARQ_diet_mamm_BP': self.ARQ_diet_mamm_BP,
            'ARQ_diet_mamm_FP': self.ARQ_diet_mamm_FP,
            'ARQ_diet_mamm_AR': self.ARQ_diet_mamm_AR,

            'CRQ_diet_mamm_SG': self.CRQ_diet_mamm_SG,
            'CRQ_diet_mamm_TG': self.CRQ_diet_mamm_TG,
            'CRQ_diet_mamm_BP': self.CRQ_diet_mamm_BP,
            'CRQ_diet_mamm_FP': self.CRQ_diet_mamm_FP,
            'CRQ_diet_mamm_AR': self.CRQ_diet_mamm_AR,

            # Table12
            'LD50_rg_bird_sm': self.LD50_rg_bird_sm,
            'LD50_rg_mamm_sm': self.LD50_rg_mamm_sm,
            'LD50_rg_bird_md': self.LD50_rg_bird_md,
            'LD50_rg_mamm_md': self.LD50_rg_mamm_md,
            'LD50_rg_bird_lg': self.LD50_rg_bird_lg,
            'LD50_rg_mamm_lg': self.LD50_rg_mamm_lg,

            # Table13
            'LD50_rl_bird_sm': self.LD50_rl_bird_sm,
            'LD50_rl_mamm_sm': self.LD50_rl_mamm_sm,
            'LD50_rl_bird_md': self.LD50_rl_bird_md,
            'LD50_rl_mamm_md': self.LD50_rl_mamm_md,
            'LD50_rl_bird_lg': self.LD50_rl_bird_lg,
            'LD50_rl_mamm_lg': self.LD50_rl_mamm_lg,

            # Table14
            'LD50_bg_bird_sm': self.LD50_bg_bird_sm,
            'LD50_bg_mamm_sm': self.LD50_bg_mamm_sm,
            'LD50_bg_bird_md': self.LD50_bg_bird_md,
            'LD50_bg_mamm_md': self.LD50_bg_mamm_md,
            'LD50_bg_bird_lg': self.LD50_bg_bird_lg,
            'LD50_bg_mamm_lg': self.LD50_bg_mamm_lg,

            # Table15
            'LD50_bl_bird_sm': self.LD50_bl_bird_sm,
            'LD50_bl_mamm_sm': self.LD50_bl_mamm_sm,
            'LD50_bl_bird_md': self.LD50_bl_bird_md,
            'LD50_bl_mamm_md': self.LD50_bl_mamm_md,
            'LD50_bl_bird_lg': self.LD50_bl_bird_lg,
            'LD50_bl_mamm_lg': self.LD50_bl_mamm_lg
        })

        # Callable from Bottle that returns JSON
        self.json = self.json(pd_obj, pd_obj_out, pd_obj_exp)

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

    # Begin model methods
    @timefn
    def run_methods(self):
        logging.info("run_methods")
        # build time series for each type

        # initial concentrations for different food types
        self.C_0_sg = self.first_app_lb * self.a_i * 240.  # short grass
        self.C_0_tg = self.first_app_lb * self.a_i * 110.  # tall grass
        self.C_0_blp = self.first_app_lb * self.a_i * 135.  # broad-leafed plants
        self.C_0_fp = self.first_app_lb * self.a_i * 15.  # fruits/pods
        self.C_0_arthro = self.first_app_lb * self.a_i * 94.  # arthropods

        # mean concentration estimate based on first application rate
        self.C_mean_sg = self.first_app_lb * self.a_i * 85.  # short grass
        self.C_mean_tg = self.first_app_lb * self.a_i * 36.  # tall grass
        self.C_mean_blp = self.first_app_lb * self.a_i * 45.  # broad-leafed plants
        self.C_mean_fp = self.first_app_lb * self.a_i * 7.  # fruits/pods
        self.C_mean_arthro = self.first_app_lb * self.a_i * 65.  # arthropods

        # time series estimate based on first application rate - needs to be matrices for batch runs
        self.C_ts_sg = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.a_i, self.h_l, 240)  # short grass
        self.C_ts_tg = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.a_i, self.h_l, 110)  # tall grass
        self.C_ts_blp = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.a_i, self.h_l, 135)  # broad-leafed plants
        self.C_ts_fp = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.a_i, self.h_l, 15)  # fruits/pods
        self.C_ts_arthro = trex_functions.conc_food_timeseries(self.day_out, self.rate_out, self.a_i, self.h_l, 94)  # arthropods

        # Table5
        logging.info("table 5")
        self.sa_bird_1_s = trex_functions.sa_bird_1(0.1, 0.02, self.aw_bird_sm, self.tw_bird_ld50)
        self.sa_bird_2_s = trex_functions.sa_bird_2(self.a_i, self.den, self.m_s_r_p, self.at_bird,
                                          self.ld50_bird, self.aw_bird_sm, self.tw_bird_ld50, self.x, 0.02)
        self.sc_bird_s = trex_functions.sc_bird(self.a_i, self.den, self.NOAEC_bird)
        self.sa_mamm_1_s = trex_functions.sa_mamm_1(self.a_i, self.den, self.at_mamm, self.fi_mamm, 0.1,
                                          self.ld50_mamm, self.aw_mamm_sm, self.tw_mamm, 0.015)
        self.sa_mamm_2_s = trex_functions.sa_mamm_2(self.a_i, self.den, self.m_s_r_p, self.at_mamm,
                                          self.ld50_mamm, self.aw_mamm_sm, self.tw_mamm, 0.015)
        self.sc_mamm_s = trex_functions.sc_mamm(self.a_i, self.den, self.NOAEL_mamm, self.aw_mamm_sm,
                                      self.fi_mamm, 0.1, self.tw_mamm, self.ANOAEL_mamm, 0.015)

        self.sa_bird_1_m = trex_functions.sa_bird_1(0.1, 0.1, self.aw_bird_md, self.tw_bird_ld50)
        self.sa_bird_2_m = trex_functions.sa_bird_2(self.a_i, self.den, self.m_s_r_p, self.at_bird,
                                          self.ld50_bird, self.aw_bird_md, self.tw_bird_ld50, self.x, 0.1)
        self.sc_bird_m = trex_functions.sc_bird(self.a_i, self.den, self.NOAEC_bird)
        self.sa_mamm_1_m = trex_functions.sa_mamm_1(self.a_i, self.den, self.at_mamm, self.fi_mamm, 0.1,
                                          self.ld50_mamm, self.aw_mamm_md, self.tw_mamm, 0.035)
        self.sa_mamm_2_m = trex_functions.sa_mamm_2(self.a_i, self.den, self.m_s_r_p, self.at_mamm,
                                          self.ld50_mamm, self.aw_mamm_md, self.tw_mamm, 0.035)
        self.sc_mamm_m = trex_functions.sc_mamm(self.a_i, self.den, self.NOAEL_mamm, self.aw_mamm_md,
                                      self.fi_mamm, 0.1, self.tw_mamm, self.ANOAEL_mamm, 0.035)

        self.sa_bird_1_l = trex_functions.sa_bird_1(0.1, 1.0, self.aw_bird_lg, self.tw_bird_ld50)
        self.sa_bird_2_l = trex_functions.sa_bird_2(self.a_i, self.den, self.m_s_r_p, self.at_bird,
                                          self.ld50_bird, self.aw_bird_lg, self.tw_bird_ld50, self.x, 1.0)
        self.sc_bird_l = trex_functions.sc_bird(self.a_i, self.den, self.NOAEC_bird)
        self.sa_mamm_1_l = trex_functions.sa_mamm_1(self.a_i, self.den, self.at_mamm, self.fi_mamm, 0.1,
                                          self.ld50_mamm, self.aw_mamm_lg, self.tw_mamm, 1)
        self.sa_mamm_2_l = trex_functions.sa_mamm_2(self.a_i, self.den, self.m_s_r_p, self.at_mamm,
                                          self.ld50_mamm, self.aw_mamm_lg, self.tw_mamm, 1)
        self.sc_mamm_l = trex_functions.sc_mamm(self.a_i, self.den, self.NOAEL_mamm, self.aw_mamm_lg,
                                      self.fi_mamm, 0.1, self.tw_mamm, self.ANOAEL_mamm, 1)

        # Table 6
        logging.info("table 6")
        self.EEC_diet_SG = trex_functions.EEC_diet(self.C_t_sg, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                         self.day_out)
        self.EEC_diet_TG = trex_functions.EEC_diet(self.C_t_tg, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                         self.day_out)
        self.EEC_diet_BP = trex_functions.EEC_diet(self.C_t_blp, self.noa, self.first_app_lb, self.a_i, 135,
                                         self.h_l, self.day_out)
        self.EEC_diet_FR = trex_functions.EEC_diet(self.C_t_f_p, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                         self.day_out)
        self.EEC_diet_AR = trex_functions.EEC_diet(self.C_t_arhtro, self.noa, self.first_app_lb, self.a_i, 94,
                                         self.h_l, self.day_out)

        # Table 7
        logging.info("table 7")
        self.EEC_dose_bird_SG_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_SG_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_SG_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_TG_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_TG_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_TG_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_BP_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_BP_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_BP_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_FP_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_FP_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_FP_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_AR_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_AR_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_AR_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.9, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_SE_sm = trex_functions.EEC_dose_bird(self.aw_bird_sm, self.fi_bird, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_SE_md = trex_functions.EEC_dose_bird(self.aw_bird_md, self.fi_bird, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_bird_SE_lg = trex_functions.EEC_dose_bird(self.aw_bird_lg, self.fi_bird, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)

        # Table 7_add
        self.ARQ_bird_SG_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_SG_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_SG_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_TG_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_TG_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_TG_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_BP_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_BP_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_BP_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_FP_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_FP_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_FP_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_AR_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_AR_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_AR_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.8, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_SE_sm = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_sm, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.1, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_SE_md = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_md, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.1, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                 self.day_out)
        self.ARQ_bird_SE_lg = trex_functions.ARQ_dose_bird(self.EEC_diet, self.aw_bird_lg, self.fi_bird,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x, 0.1, self.C_0,
                                                 self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                 self.day_out)

        # Table 8
        logging.info("table 8")
        self.ARQ_diet_bird_SG_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 240, self.h_l, self.day_out)
        self.ARQ_diet_bird_SG_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 240, self.h_l, self.day_out)
        self.ARQ_diet_bird_TG_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 110, self.h_l, self.day_out)
        self.ARQ_diet_bird_TG_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 110, self.h_l, self.day_out)
        self.ARQ_diet_bird_BP_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 135, self.h_l, self.day_out)
        self.ARQ_diet_bird_BP_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 135, self.h_l, self.day_out)
        self.ARQ_diet_bird_FP_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 15, self.h_l, self.day_out)
        self.ARQ_diet_bird_FP_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 15, self.h_l, self.day_out)
        self.ARQ_diet_bird_AR_A = trex_functions.ARQ_diet_bird(self.lc50_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 94, self.h_l, self.day_out)
        self.ARQ_diet_bird_AR_C = trex_functions.CRQ_diet_bird(self.NOAEC_bird, self.C_0, self.C_t, self.noa,
                                                     self.first_app_lb, self.a_i, 94, self.h_l, self.day_out)

        # Table 9
        logging.info("table 9")
        self.EEC_dose_mamm_SG_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_SG_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_SG_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_TG_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_TG_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_TG_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_BP_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_BP_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_BP_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_FP_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_FP_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_FP_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_AR_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_AR_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_AR_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_SE_sm = trex_functions.EEC_dose_mamm(self.aw_mamm_sm, self.fi_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_SE_md = trex_functions.EEC_dose_mamm(self.aw_mamm_md, self.fi_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.EEC_dose_mamm_SE_lg = trex_functions.EEC_dose_mamm(self.aw_mamm_lg, self.fi_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)

        # Table 10
        logging.info("table 10")
        self.ARQ_dose_mamm_SG_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_SG_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 240,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_SG_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_SG_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 240,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_SG_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 240, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_SG_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 240,
                                                      self.h_l, self.day_out)

        self.ARQ_dose_mamm_TG_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_TG_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 110,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_TG_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_TG_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 110,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_TG_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 110, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_TG_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 110,
                                                      self.h_l, self.day_out)

        self.ARQ_dose_mamm_BP_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_BP_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 135,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_BP_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_BP_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 135,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_BP_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 135, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_BP_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 135,
                                                      self.h_l, self.day_out)

        self.ARQ_dose_mamm_FP_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_FP_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 15,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_FP_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_FP_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 15,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_FP_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_FP_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 15,
                                                      self.h_l, self.day_out)

        self.ARQ_dose_mamm_AR_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_AR_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 94,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_AR_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_AR_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 94,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_AR_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.8, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 94, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_AR_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.8,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 94,
                                                      self.h_l, self.day_out)

        self.ARQ_dose_mamm_SE_sm = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_sm,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_SE_sm = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_sm, self.fi_mamm, self.tw_mamm, 0.1,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 15,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_SE_md = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_md,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_SE_md = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_md, self.fi_mamm, self.tw_mamm, 0.1,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 15,
                                                      self.h_l, self.day_out)
        self.ARQ_dose_mamm_SE_lg = trex_functions.ARQ_dose_mamm(self.EEC_diet, self.at_mamm, self.aw_mamm_lg,
                                                      self.fi_mamm, self.ld50_mamm, self.tw_mamm, 0.1, self.C_0,
                                                      self.C_t, self.noa, self.first_app_lb, self.a_i, 15, self.h_l,
                                                      self.day_out)
        self.CRQ_dose_mamm_SE_lg = trex_functions.CRQ_dose_mamm(self.EEC_dose_mamm, self.ANOAEL_mamm,
                                                      self.NOAEL_mamm, self.aw_mamm_lg, self.fi_mamm, self.tw_mamm, 0.1,
                                                      self.C_0, self.C_t, self.noa, self.first_app_lb, self.a_i, 15,
                                                      self.h_l, self.day_out)

        # table 11
        logging.info("table 11")
        if self.lc50_mamm != 'N/A':
            self.ARQ_diet_mamm_SG = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.a_i, 240, self.h_l, self.day_out)
            self.ARQ_diet_mamm_TG = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.a_i, 110, self.h_l, self.day_out)
            self.ARQ_diet_mamm_BP = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.a_i, 135, self.h_l, self.day_out)
            self.ARQ_diet_mamm_FP = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.a_i, 15, self.h_l, self.day_out)
            self.ARQ_diet_mamm_AR = trex_functions.ARQ_diet_mamm(self.lc50_mamm, self.C_0, self.C_t, self.noa,
                                                       self.first_app_lb, self.a_i, 94, self.h_l, self.day_out)
        else:
            self.ARQ_diet_mamm_SG = 'N/A'
            self.ARQ_diet_mamm_TG = 'N/A'
            self.ARQ_diet_mamm_BP = 'N/A'
            self.ARQ_diet_mamm_FP = 'N/A'
            self.ARQ_diet_mamm_AR = 'N/A'

        self.CRQ_diet_mamm_SG = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.a_i, 240, self.h_l, self.day_out)
        self.CRQ_diet_mamm_TG = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.a_i, 110, self.h_l, self.day_out)
        self.CRQ_diet_mamm_BP = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.a_i, 135, self.h_l, self.day_out)
        self.CRQ_diet_mamm_FP = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.a_i, 15, self.h_l, self.day_out)
        self.CRQ_diet_mamm_AR = trex_functions.CRQ_diet_mamm(self.NOAEC_mamm, self.C_0, self.C_t, self.noa,
                                                   self.first_app_lb, self.a_i, 94, self.h_l, self.day_out)

        # Table12
        logging.info("table 12")
        self.LD50_rg_bird_sm = trex_functions.LD50_rg_bird(self.first_app_lb, self.a_i, self.p_i, self.r_s,
                                                 self.b_w, self.aw_bird_sm, self.at_bird, self.ld50_bird,
                                                 self.tw_bird_ld50, self.x)
        self.LD50_rg_mamm_sm = trex_functions.LD50_rg_mamm(self.first_app_lb, self.a_i, self.p_i, self.r_s,
                                                 self.b_w, self.aw_mamm_sm, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_rg_bird_md = trex_functions.LD50_rg_bird(self.first_app_lb, self.a_i, self.p_i, self.r_s,
                                                 self.b_w, self.aw_bird_md, self.at_bird, self.ld50_bird,
                                                 self.tw_bird_ld50, self.x)
        self.LD50_rg_mamm_md = trex_functions.LD50_rg_mamm(self.first_app_lb, self.a_i, self.p_i, self.r_s,
                                                 self.b_w, self.aw_mamm_md, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_rg_bird_lg = trex_functions.LD50_rg_bird(self.first_app_lb, self.a_i, self.p_i, self.r_s,
                                                 self.b_w, self.aw_bird_lg, self.at_bird, self.ld50_bird,
                                                 self.tw_bird_ld50, self.x)
        self.LD50_rg_mamm_lg = trex_functions.LD50_rg_mamm(self.first_app_lb, self.a_i, self.p_i, self.r_s,
                                                 self.b_w, self.aw_mamm_lg, self.at_mamm, self.ld50_mamm, self.tw_mamm)

        # Table13
        logging.info("table 13")
        self.LD50_rl_bird_sm = trex_functions.LD50_rl_bird(self.first_app_lb, self.a_i, self.p_i, self.b_w,
                                                 self.aw_bird_sm, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.LD50_rl_mamm_sm = trex_functions.LD50_rl_mamm(self.first_app_lb, self.a_i, self.p_i, self.b_w,
                                                 self.aw_mamm_sm, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_rl_bird_md = trex_functions.LD50_rl_bird(self.first_app_lb, self.a_i, self.p_i, self.b_w,
                                                 self.aw_bird_md, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.LD50_rl_mamm_md = trex_functions.LD50_rl_mamm(self.first_app_lb, self.a_i, self.p_i, self.b_w,
                                                 self.aw_mamm_md, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_rl_bird_lg = trex_functions.LD50_rl_bird(self.first_app_lb, self.a_i, self.p_i, self.b_w,
                                                 self.aw_bird_lg, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.LD50_rl_mamm_lg = trex_functions.LD50_rl_mamm(self.first_app_lb, self.a_i, self.p_i, self.b_w,
                                                 self.aw_mamm_lg, self.at_mamm, self.ld50_mamm, self.tw_mamm)

        # Table14
        logging.info("table 14")
        self.LD50_bg_bird_sm = trex_functions.LD50_bg_bird(self.first_app_lb, self.a_i, self.p_i,
                                                 self.aw_bird_sm, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.LD50_bg_mamm_sm = trex_functions.LD50_bg_mamm(self.first_app_lb, self.a_i, self.p_i,
                                                 self.aw_mamm_sm, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_bg_bird_md = trex_functions.LD50_bg_bird(self.first_app_lb, self.a_i, self.p_i,
                                                 self.aw_bird_md, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.LD50_bg_mamm_md = trex_functions.LD50_bg_mamm(self.first_app_lb, self.a_i, self.p_i,
                                                 self.aw_mamm_md, self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_bg_bird_lg = trex_functions.LD50_bg_bird(self.first_app_lb, self.a_i, self.p_i,
                                                 self.aw_bird_lg, self.at_bird, self.ld50_bird, self.tw_bird_ld50,
                                                 self.x)
        self.LD50_bg_mamm_lg = trex_functions.LD50_bg_mamm(self.first_app_lb, self.a_i, self.p_i,
                                                 self.aw_mamm_lg, self.at_mamm, self.ld50_mamm, self.tw_mamm)

        # Table15
        logging.info("table 15")
        self.LD50_bl_bird_sm = trex_functions.LD50_bl_bird(self.first_app_lb, self.a_i, self.aw_bird_sm,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x)
        self.LD50_bl_mamm_sm = trex_functions.LD50_bl_mamm(self.first_app_lb, self.a_i, self.aw_mamm_sm,
                                                 self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_bl_bird_md = trex_functions.LD50_bl_bird(self.first_app_lb, self.a_i, self.aw_bird_md,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x)
        self.LD50_bl_mamm_md = trex_functions.LD50_bl_mamm(self.first_app_lb, self.a_i, self.aw_mamm_md,
                                                 self.at_mamm, self.ld50_mamm, self.tw_mamm)
        self.LD50_bl_bird_lg = trex_functions.LD50_bl_bird(self.first_app_lb, self.a_i, self.aw_bird_lg,
                                                 self.at_bird, self.ld50_bird, self.tw_bird_ld50, self.x)
        self.LD50_bl_mamm_lg = trex_functions.LD50_bl_mamm(self.first_app_lb, self.a_i, self.aw_mamm_lg,
                                                 self.at_mamm, self.ld50_mamm, self.tw_mamm)