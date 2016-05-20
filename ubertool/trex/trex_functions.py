from functools import wraps
import logging
import numpy as np
import pandas as pd
import time


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("trex2_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result

    return measure_time


class TrexFunctions(object):
    """
    Function class for Trex.
    """

    def __init__(self):
        """Class representing the functions for Trex"""
        super(TrexFunctions, self).__init__()


    @timefn
    def app_rate_parsing(self):
        # extract first day and maximum application rates from each model simulation run
        # these variables are needed in various methods
        for i in range(len(self.app_rates)):
            self.first_app_rate[i] = self.app_rates[i][0]
            self.max_app_rate[i] = max(self.app_rates[i])
        return

    @timefn
    def conc_initial(self, food_multiplier):
    # Initial concentration from new application
        conc_0 = (self.first_app_rate * self.frac_act_ing * food_multiplier)
        return conc_0

    # Concentration over time
    @timefn
    #??what is the purpose of the '* 1', just a timestep value to be complete
    def conc_timestep(self,conc_ini):
        conc = conc_ini * np.exp(-(np.log(2) / self.foliar_diss_hlife) * 1)
        return conc

    @timefn
    def percent_to_frac(self, percent):
        fraction = percent / 100
        return fraction

    def inches_to_feet(self, inches):
        feet = inches / 12
        return feet

    @timefn
    def conc_food_timeseries(self, food_multiplier):
        # Concentration time series for a selected food item
        """
        :type

        """
        conc_food = np.zeros((371, 1))  # empty array to hold the concentrations over days
        existing_conc = 0.  # start concentration
                # add_conc = 0.  # intermediate concentration calculation
                # app_check = False  # checks to see if there are more applications left in the year
        app_counter = 0  # tracks number of applications
                # app_day = 0  # app_day tracks day number of the next application
                # app_rate = 0.  # application rate of next application
                # app_total = 0  # total number of applications
        app_total = len(self.day_out)

        for i in range(0, 371):  # i is day number in the year
            app_check = bool(app_counter <= app_total)
            if app_check:  # check for next application day
                        # logging.info("day_out")
                        # logging.info(self.day_out)
                        # logging.info("rate_out")
                        # logging.info(self.rate_out)
                app_day = int(self.day_out[0][app_counter])  # day number of the next application
                        # logging.info(app_day)
                app_rates = float(self.rate_out[0])  # application rate of next application
                        # logging.info(app_rates)
                if i == app_day:  # application day
                    if i > 0:  # decay yesterdays concentration
                        existing_conc = conc_timestep(conc_food[i - 1], self.foliar_diss_hlife)
                    add_conc = conc_initial(app_rates, food_multiplier)  # new application conc
                    conc_food[i] = existing_conc + add_conc  # calculate today's total concentration
                    app_counter += 1  # increment number of applications so far
                elif i > 0:
                    # decay yesterdays concentration if no application
                    conc_food[i] = conc_timestep(conc_food[i - 1], self.foliar_diss_hlife)
                else:
                    conc_food[i] = 0  # handle first day if no application
        return conc_food

    @timefn
    def sa_bird_1(self, size):
    # Seed treatment acute RQ for birds method 1

        # setup panda series
        at_bird_temp = pd.Series(name="at_bird_temp")
        fi_bird_temp = pd.Series(name="fi_bird_temp")
        m_s_a_r_temp = pd.Series(name="m_s_a_r_temp")
        nagy_bird_temp = pd.Series(name="nagy_bird_temp")
        sa_bird_1_return = pd.Series(name="sa_bird_1_return")

        if size == "small":
            mf_w_bird = self.mf_w_bird_1
            nagy_bird_coef = self.nagy_bird_coef_sm
            aw_bird = self.aw_bird_sm
        elif size == "medium":
            mf_w_bird = self.mf_w_bird_1
            nagy_bird_coef = self.nagy_bird_coef_md
            aw_bird = self.aw_bird_md
        elif size == "large":
            mf_w_bird = self.mf_w_bird_1
            nagy_bird_coef = self.nagy_bird_coef_lg
            aw_bird = self.aw_bird_lg

        # run calculations
        at_bird_temp = at_bird(aw_bird)
        fi_bird_temp = fi_bird(aw_bird, mf_w_bird)
        # maximum seed application rate=application rate*10000
    #??should assign these constants to variables in TrexInputs class or explain conversions
        m_s_a_r_temp = ((self.app_rates * self.frac_act_ing) / 128.) * self.density * 10000
        nagy_bird_temp = fi_bird_temp * 0.001 * m_s_a_r_temp / nagy_bird_coef
        sa_bird_1_return = nagy_bird_temp / at_bird_temp
        return sa_bird_1_return


    @timefn
    def sa_bird_2(self, size):
        # Seed treatment acute RQ for birds method 2

        if size == "small":
            nagy_bird_coef = self.nagy_bird_coef_sm
            aw_bird = self.aw_bird_sm
        elif size == "medium":
            nagy_bird_coef = self.nagy_bird_coef_md
            aw_bird = self.aw_bird_md
        elif size == "large":
            nagy_bird_coef = self.nagy_bird_coef_lg
            aw_bird = self.aw_bird_lg

        at_bird_temp = at_bird(self.ld50_bird, aw_bird, self.tw_bird_ld50, self.mineau_sca_fact)
        m_a_r = (self.max_seed_rate * ((self.frac_act_ing * self.app_rates[0]) / 128) * self.density) / 100  # maximum application rate
        av_ai = m_a_r * 1e6 / (43560 * 2.2)
        sa_bird_2_return = av_ai / (at_bird_temp * nagy_bird_coef)
        return sa_bird_2_return

    @timefn
    def sc_bird(self, app_rates):
        # Seed treatment chronic RQ for birds
        m_s_a_r = ((app_rates * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        risk_quotient = m_s_a_r / self.noaec_bird
        return risk_quotient

    @timefn
    def sa_mamm_1(self, size):
        # Seed treatment acute RQ for mammals method 1

        if size == "small":
            mf_w_bird = self.mf_w_bird_1
            nagy_mamm_coef = self.nagy_mamm_coef_sm
            aw_mamm = self.aw_mamm_sm
        elif size == "medium":
            mf_w_bird = self.mf_w_bird_1
            nagy_mamm_coef = self.nagy_mamm_coef_md
            aw_mamm = self.aw_mamm_md
        elif size == "large":
            mf_w_bird = self.mf_w_bird_1
            nagy_mamm_coef = self.nagy_mamm_coef_lg
            aw_mamm = self.aw_mamm_lg

        at_mamm_temp = at_mamm(aw_mamm)
        fi_mamm_temp = fi_mamm(aw_mamm, mf_w_bird)
        m_s_a_r = ((self.app_rates * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        nagy_mamm = fi_mamm_temp * 0.001 * m_s_a_r / nagy_mamm_coef
        quotient = nagy_mamm / at_mamm_temp
        return quotient

    @timefn
    def sa_mamm_2(self, size):
        # Seed treatment acute RQ for mammals method 2

        if size == "small":
            nagy_mamm_coef = self.nagy_mamm_coef_sm
            aw_mamm = self.aw_mamm_sm
        elif size == "medium":
            nagy_mamm_coef = self.nagy_mamm_coef_md
            aw_mamm = self.aw_mamm_md
        elif size == "large":
            nagy_mamm_coef = self.nagy_mamm_coef_lg
            aw_mamm = self.aw_mamm_lg

        at_mamm_temp = at_mamm(aw_mamm)
        m_a_r = (self.max_seed_rate * ((self.app_rates * self.frac_act_ing) / 128) * self.density) / 100  # maximum application rate
        av_ai = m_a_r * 1000000 / (43560 * 2.2)
        quotient = av_ai / (at_mamm_temp * nagy_mamm_coef)
        return quotient

    @timefn
    def sc_mamm(self, size):
        # Seed treatment chronic RQ for mammals

        if size == "small":
            mf_w_bird = self.mf_w_bird_1
            nagy_mamm_coef = self.nagy_mamm_coef_sm
            aw_mamm = self.aw_mamm_sm
        elif size == "medium":
            mf_w_bird = self.mf_w_bird_1
            nagy_mamm_coef = self.nagy_mamm_coef_md
            aw_mamm = self.aw_mamm_md
        elif size == "large":
            mf_w_bird = self.mf_w_bird_1
            nagy_mamm_coef = self.nagy_mamm_coef_lg
            aw_mamm = self.aw_mamm_lg

        anoael_mamm_temp = anoael_mamm(aw_mamm)
        fi_mamm_temp = fi_mamm(aw_mamm, mf_w_bird)
        m_s_a_r = ((self.app_rates * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        nagy_mamm = fi_mamm_temp * 0.001 * m_s_a_r / nagy_mamm_coef
        quotient = nagy_mamm / anoael_mamm_temp
        return quotient


    @timefn
    def fi_bird(self, aw_bird, mf_w_bird):
        # food intake for birds
        food_intake = (0.648 * (aw_bird ** 0.651)) / (1 - mf_w_bird)
        return food_intake


    @timefn
    def fi_mamm(self, aw_mamm, mf_w_mamm):
        # food intake for mammals
        food_intake = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        return food_intake


    @timefn
    def at_bird(self, aw_bird):
        # Acute adjusted toxicity value for birds
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        return adjusted_toxicity



    @timefn
    def at_mamm(self, aw_mamm):
        # Acute adjusted toxicity value for mammals
        adjusted_toxicity = self.ld50_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
        return adjusted_toxicity



    @timefn
    def anoael_mamm(self, aw_mamm):
    # Adjusted chronic toxicity (NOAEL) value for mammals
        adjusted_toxicity = self.noael_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
        return adjusted_toxicity



    @timefn
    def eec_diet(self, food_multiplier):
    # concentration over time if application rate or time interval is variable
    # returns max daily concentration, can be multiple applications
    # Dietary based EECs

        # new in trex1.5.1
        if self.num_apps.any() == 1:
            # get initial concentration
            C_temp = conc_initial(self, self.app_rates[0], food_multiplier)
            return np.array([C_temp])
        else:
            C_temp = np.ones((371, 1))  # empty array to hold the concentrations over daysp
            num_apps_temp = 0  # number of existing applications
            dayt = 0
            day_out_l = len(self.day_out)
            for i in range(0, 371):
                if i == 0:  # first day of application
                    C_temp[i] = conc_initial(self.app_rates[0], food_multiplier)
                    num_apps_temp += 1
                    dayt += 1
                elif dayt <= self.day_out_l - 1 and num_apps_temp <= self.num_apps:  # next application day
                    if i == self.day_out[dayt]:
                        C_temp[i] = conc_timestep(C_temp[i - 1]) + conc_initial(self.app_rates[dayt], food_multiplier)
                        num_apps_temp += 1
                        dayt += 1
                    else:
                        C_temp[i] = conc_timestep(C_temp[i - 1])
            max_c_return = max(C_temp)
            return max_c_return



    @timefn
    def eec_dose_bird(self, aw_bird, mf_w_bird, food_multiplier):
    # Dose based EECs for birds
        fi_bird_calc = fi_bird(aw_bird, mf_w_bird)
        eec_diet_temp = eec_diet(food_multiplier)
        eec_out = eec_diet_temp * fi_bird_calc / aw_bird
        return eec_out


    # Dose based EECs for granivores birds

    # def EEC_dose_bird_g(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, noa, a_r, self.frac_act_ing, para, foliar_diss_hlife):
    # if para==15:
    # noa = float(noa)
    # #  i_a = float(i_a)
    # aw_bird = float(aw_bird)
    # mf_w_bird = float(mf_w_bird)
    # a_r = float(a_r)
    # frac_act_ing = float(frac_act_ing)
    # para = float(para)
    # foliar_diss_hlife = float(foliar_diss_hlife)
    # fi_bird = fi_bird(aw_bird, mf_w_bird)
    # EEC_diet=EEC_diet(C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife, day)
    # return (EEC_diet*fi_bird/aw_bird)
    # else:
    # return(0)


    @timefn
    def eec_dose_mamm(self, aw_mamm, mf_w_mamm, food_multiplier):
    # Dose based EECs for mammals
        eec_diet_temp = eec_diet(food_multiplier)
        fi_mamm_temp = fi_mamm(aw_mamm, mf_w_mamm)
        dose_eec = eec_diet_temp * fi_mamm_temp / aw_mamm
        return dose_eec


    # Dose based EECs for granivores mammals

    # def EEC_dose_mamm_g(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife):
    # if para==15:
    # aw_mamm = float(aw_mamm)
    # EEC_diet=EEC_diet(C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife, day)
    # fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
    # return (EEC_diet*fi_mamm/aw_mamm)
    # else:
    # return(0)


    @timefn
    def arq_dose_bird(self, aw_bird, mf_w_bird, food_multiplier):
    # Acute dose-based risk quotients for birds
        eec_dose_bird_temp = eec_dose_bird(aw_bird, mf_w_bird, food_multiplier)
        at_bird_temp = at_bird(aw_bird)
        risk_quotient = eec_dose_bird_temp / at_bird_temp
        return risk_quotient


    # Acute dose-based risk quotients for granivores birds

    # def ARQ_dose_bird_g(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, mineau_sca_fact, mf_w_bird, C_0,
    # noa, a_r, frac_act_ing, para, foliar_diss_hlife):
    # if para==15:
    # EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife)
    # at_bird = at_bird(ld50_bird,aw_bird,tw_bird,mineau_sca_fact)
    # return (EEC_dose_bird/at_bird)
    # else:
    # return (0)


    @timefn
    def arq_dose_mamm(self, aw_mamm, mf_w_mamm, food_multiplier):
    # Acute dose-based risk quotients for mammals
        eec_dose_mamm_temp = eec_dose_mamm(aw_mamm, mf_w_mamm, food_multiplier)
        at_mamm_temp = at_mamm(aw_mamm)
        risk_quotient = eec_dose_mamm_temp / at_mamm_temp
        return risk_quotient


    # Acute dose-based risk quotients for granivores mammals
    # def ARQ_dose_mamm_g(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife):
    # if para==15:
    # EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife)
    # at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
    # return (EEC_dose_mamm/at_mamm)
    # else:
    # return(0)


    @timefn
    def arq_diet_bird(self, food_multiplier):
    # Acute dietary-based risk quotients for birds
        eec_diet_temp = eec_diet(food_multiplier)
        risk_quotient = eec_diet_temp / self.lc50_bird
        return risk_quotient

    @timefn
    def arq_diet_mamm(self, food_multiplier):
    # Acute dietary-based risk quotients for mammals
        eec_diet_temp = eec_diet(food_multiplier)
        risk_quotient = eec_diet_temp / self.lc50_mamm
        return risk_quotient



    @timefn
    def crq_diet_bird(self, food_multiplier):
    # Chronic dietary-based risk quotients for birds
        eec_diet_temp = eec_diet(food_multiplier)
        risk_quotient = eec_diet_temp / self.noaec_bird
        return risk_quotient



    @timefn
    def crq_diet_mamm(self, food_multiplier):
    # Chronic dietary-based risk quotients for mammals
        eec_diet_temp = eec_diet(food_multiplier)
        crq_diet_mamm_temp = eec_diet_temp / self.noaec_mamm
        return crq_diet_mamm_temp



    @timefn
    def crq_dose_mamm(self, aw_mamm, mf_w_mamm, food_multiplier):
    # Chronic dose-based risk quotients for mammals
        anoael_mamm_temp = anoael_mamm(aw_mamm)
        eec_dose_mamm_temp = eec_dose_mamm(aw_mamm, mf_w_mamm, food_multiplier)
        risk_quotient = eec_dose_mamm_temp / anoael_mamm_temp
        return risk_quotient

    # Chronic dose-based risk quotients for granviores mammals
    # def CRQ_dose_mamm_g(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, noa, a_r,
    # frac_act_ing, para, foliar_diss_hlife):
    # if para==15:
    # ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
    # EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, foliar_diss_hlife)
    # return (EEC_dose_mamm/ANOAEL_mamm)
    # else:
    # return (0)


    @timefn
    def ld50_rg_bird(self, aw_bird):
    # LD50ft-2 for row/band/in-furrow granular birds
        if self.application_type == 'Row/Band/In-furrow-Granular':
            at_bird_temp = at_bird(aw_bird)
            n_r = (43560 ** 0.5) / self.row_spacing
            expo_rg_bird = (max(self.app_rates) * self.frac_act_ing * 453590.0) / \
                           (n_r * (43560.0 ** 0.5) * self.bandwidth) * (1 - self.frac_incorp)
            ld50_rg_bird_temp = expo_rg_bird / (at_bird_temp * (aw_bird / 1000.0))
            return ld50_rg_bird_temp
        else:
            return 0



    @timefn
    def ld50_rl_bird(self, aw_bird):
    # LD50ft-2 for row/band/in-furrow liquid birds
        if self.application_type == 'Row/Band/In-furrow-Liquid':
            at_bird_temp = at_bird(aw_bird)
            expo_rl_bird = ((max(self.app_rates) * 28349 * self.frac_act_ing) / (1000 * self.bandwidth)) * \
                           (1 - self.frac_incorp)
            ld50_rl_bird_temp = expo_rl_bird / (at_bird_temp * (aw_bird / 1000.0))
            return ld50_rl_bird_temp
        else:
            return 0



    @timefn
    def ld50_rg_mamm(self, aw_mamm):
    # LD50ft-2 for row/band/in-furrow granular mammals
        if self.application_type == 'Row/Band/In-furrow-Granular':
            # a_r = max(app_rates)
            at_mamm_temp = at_mamm(aw_mamm)
            n_r = (43560 ** 0.5) / self.row_spacing
            expo_rg_mamm = (max(self.app_rates) * self.frac_act_ing * 453590) / (n_r * (43560 ** 0.5) * bandwidth) * (1 - frac_incorp)
            ld50_rg_mamm_temp = expo_rg_mamm / (at_mamm_temp * (aw_mamm / 1000.0))
            return ld50_rg_mamm_temp
        else:
            return 0


    # LD50ft-2 for row/band/in-furrow liquid mammals
    @timefn
    def ld50_rl_mamm(self, aw_mamm):
    # LD50ft-2 for row/band/in-furrow liquid mammals
        if self.application_type == 'Row/Band/In-furrow-Liquid':
            at_mamm_temp = at_mamm(aw_mamm)
            expo_rl_bird = ((max(self.app_rates) * 28349 * self.frac_act_ing) / (1000 * self.bandwidth)) * \
                           (1 - self.frac_incorp)
            ld50_rl_mamm_temp = expo_rl_bird / (at_mamm_temp * (aw_mamm / 1000.0))
            return ld50_rl_mamm_temp
        else:
            return 0


    # LD50ft-2 for broadcast granular birds
    @timefn
    def ld50_bg_bird(self, aw_bird):
    # LD50ft-2 for broadcast granular birds
        if self.application_type == 'Broadcast-Granular':
            at_bird_temp = at_bird(aw_bird)
            expo_bg_bird = ((max(self.app_rates) * self.frac_act_ing * 453590) / 43560)
            ld50_bg_bird_temp = expo_bg_bird / (at_bird_temp * (aw_bird / 1000.0))
            return ld50_bg_bird_temp
        else:
            return 0



    @timefn
    def ld50_bl_bird(self, aw_bird):
    # LD50ft-2 for broadcast liquid birds
        if self.application_type == 'Broadcast-Liquid':
            at_bird_temp = at_bird(self.ld50_bird, aw_bird, self.tw_bird, self.mineau_sca_fact)
            # expo_bl_bird=((max(self.app_rates)*28349*frac_act_ing)/43560)*(1-frac_incorp)
            expo_bl_bird = ((max(self.app_rates) * 453590 * self.frac_act_ing) / 43560)
            ld50_bl_bird_temp = expo_bl_bird / (at_bird_temp * (aw_bird / 1000.0))
            return ld50_bl_bird_temp
        else:
            return 0



    @timefn
    def ld50_bg_mamm(self, aw_mamm):
    # LD50ft-2 for broadcast granular mammals
        if self.application_type == 'Broadcast-Granular':
            at_mamm_temp = at_mamm(aw_mamm)
            expo_bg_mamm = ((max(self.app_rates) * self.frac_act_ing * 453590) / 43560)
            ld50_bg_mamm_temp = expo_bg_mamm / (at_mamm_temp * (aw_mamm / 1000.0))
            return ld50_bg_mamm_temp
        else:
            return 0



    @timefn
    def ld50_bl_mamm(self, aw_mamm):
    # LD50ft-2 for broadcast liquid mammals
        if self.application_type == 'Broadcast-Liquid':
            at_mamm_temp = at_mamm(aw_mamm)
            # expo_bl_mamm=((max(self.app_rates)*28349*self.frac_act_ing)/43560)*(1-frac_incorp)
            expo_bl_mamm = ((max(self.app_rates) * self.frac_act_ing * 453590) / 43560)  #453590 mg/lb; 43560ft2/acre
            ld50_bl_mamm_temp = expo_bl_mamm / (at_mamm_temp * (aw_mamm / 1000.0))
            return ld50_bl_mamm_temp
        else:
            return 0