from functools import wraps
import logging
import numpy as np
import pandas as pd
import time

#?? is the following correct
from trex_exe import TrexOutputs
from trex_exe import TrexInputs



def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        t1 = time.time()
        result = fn(*args, **kwargs)
        t2 = time.time()
        print("trex2_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result

    return measure_time


# Dietary based EECs
# Initial concentration from new application
@timefn
def conc_initial(a_r, fract_act_ing, food_multiplier):
    conc_new = (a_r * fract_act_ing * food_multiplier)
    return conc_new


# Concentration over time
@timefn
def conc_timestep(C_ini, h_l):
    return C_ini * np.exp(-(np.log(2) / h_l) * 1)

@timefn
def percent_to_frac(self):
    frac_act_ing = percent_act_ing / 100
    return frac_act_ing

# Concentration time series for a selected food item
@timefn
#?? so these arguments need to be consistent with trex_exe.model_inputs, correct; e.g. half_life --> h_1
def conc_food_timeseries(self):
    """
    :type
    day_out, rate_out, active_ing, half_life, food_multiplier
    """
    conc_food = np.zeros((371, 1))  # empty array to hold the concentrations over days
    existing_conc = 0.  # start concentration
    # add_conc = 0.  # intermediate concentration calculation
    # app_check = False  # checks to see if there are more applications left in the year
    app_counter = 0  # tracks number of applications
    # app_day = 0  # app_day tracks day number of the next application
    # app_rate = 0.  # application rate of next application
    # app_total = 0  # total number of applications
    app_total = len(day_out)

    for i in range(0, 371):  # i is day number in the year
        app_check = bool(app_counter <= app_total)
        if app_check:  # check for next application day
            logging.info("day_out")
            logging.info(day_out)
            logging.info("rate_out")
            logging.info(rate_out)
            app_day = int(day_out[0][app_counter])  # day number of the next application
            logging.info(app_day)
            app_rate = float(rate_out[0])  # application rate of next application
            logging.info(app_rate)
            if i == app_day:  # application day
                if i > 0:  # decay yesterdays concentration
                    existing_conc = conc_timestep(conc_food[i - 1], half_life)
                add_conc = conc_initial(app_rate, active_ing, food_multiplier)  # new application conc
                conc_food[i] = existing_conc + add_conc  # calculate today's total concentration
                app_counter += 1  # increment number of applications so far
            elif i > 0:
                # decay yesterdays concentration if no application
                conc_food[i] = conc_timestep(conc_food[i - 1], half_life)
            else:
                conc_food[i] = 0  # handle first day if no application
    return conc_food


# Seed treatment acute RQ for birds method 1
# @timefn
def sa_bird_1(self, mf_w_bird, nagy_bird_coef, aw_bird, tw_bird):
    #  logging
    logging.info("sa_bird_1")
    logging.info(self.ld50_bird)
    logging.info(aw_bird)
    logging.info(tw_bird)
    logging.info(self.x)

    # setup panda series
    at_bird_temp = pd.Series(name="at_bird_temp")
    fi_bird_temp = pd.Series(name="fi_bird_temp")
    m_s_a_r_temp = pd.Series(name="m_s_a_r_temp")
    nagy_bird_temp = pd.Series(name="nagy_bird_temp")
    sa_bird_1_return = pd.Series(name="sa_bird_1_return")

    # run calculations
    at_bird_temp = self.at_bird(self.ld50_bird, aw_bird, tw_bird, self.x)
    fi_bird_temp = self.fi_bird(aw_bird, mf_w_bird)
    # maximum seed application rate=application rate*10000
    m_s_a_r_temp = ((self.first_app_lb * self.frac_act_ing) / 128.) * self.den * 10000
    nagy_bird_temp = fi_bird_temp * 0.001 * m_s_a_r_temp / nagy_bird_coef
    sa_bird_1_return = nagy_bird_temp / at_bird_temp
    return sa_bird_1_return

    # Seed treatment acute RQ for birds method 2


#  self.sa_bird_2_s = self.sa_bird_2(self.first_app_lb, self.frac_act_ing, self.den, self.m_s_r_p, self.at_bird,
# self.ld50_bird, self.aw_bird_sm, self.tw_bird_ld50, self.x, 0.02)
@timefn
def sa_bird_2(a_r_p, frac_act_ing, den, m_s_r_p, at_bird, ld50_bird, aw_bird, tw_bird, x, nagy_bird_coef):
    at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
    m_a_r = (m_s_r_p * ((frac_act_ing * a_r_p) / 128) * den) / 100  # maximum application rate
    av_ai = m_a_r * 1e6 / (43560 * 2.2)
    return av_ai / (at_bird * nagy_bird_coef)

    # Seed treatment chronic RQ for birds


@timefn
def sc_bird(a_r_p, frac_act_ing, den, NOAEC_bird):
    m_s_a_r = ((a_r_p * frac_act_ing) / 128) * den * 10000  # maximum seed application rate=application rate*10000
    return m_s_a_r / NOAEC_bird

    # Seed treatment acute RQ for mammals method 1


@timefn
def sa_mamm_1(a_r_p, frac_act_ing, den, at_mamm, fi_mamm, mf_w_bird, ld50_mamm, aw_mamm, tw_mamm, nagy_mamm_coef):
    at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
    fi_mamm = fi_mamm(aw_mamm, mf_w_bird)
    m_s_a_r = ((a_r_p * frac_act_ing) / 128) * den * 10000  # maximum seed application rate=application rate*10000
    nagy_mamm = fi_mamm * 0.001 * m_s_a_r / nagy_mamm_coef
    return nagy_mamm / at_mamm

    # Seed treatment acute RQ for mammals method 2


@timefn
def sa_mamm_2(a_r_p, frac_act_ing, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm, tw_mamm, nagy_mamm_coef):
    at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
    m_a_r = (m_s_r_p * ((a_r_p * frac_act_ing) / 128) * den) / 100  # maximum application rate
    av_ai = m_a_r * 1000000 / (43560 * 2.2)
    return av_ai / (at_mamm * nagy_mamm_coef)

    # Seed treatment chronic RQ for mammals


@timefn
def sc_mamm(a_r_p, frac_act_ing, den, NOAEL_mamm, aw_mamm, fi_mamm, mf_w_bird, tw_mamm, ANOAEL_mamm, nagy_mamm_coef):
    ANOAEL_mamm = ANOAEL_mamm(NOAEL_mamm, aw_mamm, tw_mamm)
    fi_mamm = fi_mamm(aw_mamm, mf_w_bird)
    m_s_a_r = ((a_r_p * frac_act_ing) / 128) * den * 10000  # maximum seed application rate=application rate*10000
    nagy_mamm = fi_mamm * 0.001 * m_s_a_r / nagy_mamm_coef
    return nagy_mamm / ANOAEL_mamm


# food intake for birds
@timefn
def fi_bird(aw_bird, mf_w_bird):
    return (0.648 * (aw_bird ** 0.651)) / (1 - mf_w_bird)


# food intake for mammals
@timefn
def fi_mamm(aw_mamm, mf_w_mamm):
    return (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)


# Acute adjusted toxicity value for birds
@timefn
def at_bird(ld50_bird, aw_bird, tw_bird, x):
    logging.info("at_bird")
    logging.info(ld50_bird)
    logging.info(aw_bird)
    logging.info(tw_bird)
    logging.info(x)
    at_bird_return = ld50_bird * (aw_bird / tw_bird) ** (x - 1)
    return at_bird_return


# Acute adjusted toxicity value for mammals
@timefn
def at_mamm(ld50_mamm, aw_mamm, tw_mamm):
    return ld50_mamm * ((tw_mamm / aw_mamm) ** 0.25)


# Adjusted chronic toxicity (NOAEL) value for mammals
@timefn
def ANOAEL_mamm(NOAEL_mamm, aw_mamm, tw_mamm):
    return NOAEL_mamm * ((tw_mamm / aw_mamm) ** 0.25)


# concentration over time if application rate or time interval is variable
# returns max daily concentration, can be multiple applications
# Dietary based EECs
@timefn
def EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    # new in trex1.5.1
    logging.info("EEC_diet")
    logging.info("noa")
    logging.info(noa.dtype)
    logging.info(noa)
    logging.info(noa.any())
    logging.info("a_r")
    logging.info(a_r)
    if noa.any() == 1:
        # get initial concentration
        C_temp = C_0(a_r, frac_act_ing, para)
        logging.info("C_temp")
        logging.info(C_temp)
        return np.array([C_temp])
    else:
        C_temp = np.ones((371, 1))  # empty array to hold the concentrations over daysp
        noa_temp = 0  # number of existing applications
        dayt = 0
        day_out_l = len(day_out)
        for i in range(0, 371):
            if i == 0:  # first day of application
                C_temp[i] = C_0(a_r[0], frac_act_ing, para)
                noa_temp += 1
                dayt += 1
            elif dayt <= day_out_l - 1 and noa_temp <= noa:  # next application day
                if i == day_out[dayt]:
                    C_temp[i] = C_t(C_temp[i - 1], h_l) + C_0(a_r[dayt], frac_act_ing, para)
                    noa_temp += 1
                    dayt += 1
                else:
                    C_temp[i] = C_t(C_temp[i - 1], h_l)
        logging.info("C_temp")
        logging.info(C_temp)
        max_c_return = max(C_temp)
        logging.info("max_c_return")
        logging.info(max_c_return)
        return max_c_return


# Dose based EECs for birds
@timefn
def EEC_dose_bird(EEC_diet, aw_bird, mf_w_bird, C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    logging.info("EEC_dose_bird")
    fi_bird_calc = fi_bird(mf_w_bird)
    EEC_diet = EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out)
    logging.info(EEC_diet)
    logging.info(fi_bird_calc)
    logging.info(aw_bird)
    EEC_out = EEC_diet * fi_bird_calc / aw_bird
    logging.info("EEC_out")
    logging.info(EEC_out)
    return EEC_out


# Dose based EECs for granivores birds

# def EEC_dose_bird_g(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, noa, a_r, self.frac_act_ing, para, h_l):
# if para==15:
# noa = float(noa)
# #  i_a = float(i_a)
# aw_bird = float(aw_bird)
# mf_w_bird = float(mf_w_bird)
# a_r = float(a_r)
# frac_act_ing = float(frac_act_ing)
# para = float(para)
# h_l = float(h_l)
# fi_bird = fi_bird(aw_bird, mf_w_bird)
# EEC_diet=EEC_diet(C_0, noa, a_r, frac_act_ing, para, h_l, day)
# return (EEC_diet*fi_bird/aw_bird)
# else:
# return(0)

# Dose based EECs for mammals
@timefn
def EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_diet = EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out)
    fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
    return EEC_diet * fi_mamm / aw_mamm


# Dose based EECs for granivores mammals

# def EEC_dose_mamm_g(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, h_l):
# if para==15:
# aw_mamm = float(aw_mamm)
# EEC_diet=EEC_diet(C_0, noa, a_r, frac_act_ing, para, h_l, day)
# fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
# return (EEC_diet*fi_mamm/aw_mamm)
# else:
# return(0)

# Acute dose-based risk quotients for birds
@timefn
def ARQ_dose_bird(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0,
                  C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, C_t, noa, a_r, frac_act_ing, para, h_l,
                                  day_out)
    at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
    return EEC_dose_bird / at_bird


# Acute dose-based risk quotients for granivores birds

# def ARQ_dose_bird_g(EEC_dose_bird, EEC_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, C_0,
# noa, a_r, frac_act_ing, para, h_l):
# if para==15:
# EEC_dose_bird = EEC_dose_bird(EEC_diet, aw_bird, fi_bird, mf_w_bird, C_0, noa, a_r, frac_act_ing, para, h_l)
# at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
# return (EEC_dose_bird/at_bird)
# else:
# return (0)

# Acute dose-based risk quotients for mammals
@timefn
def ARQ_dose_mamm(EEC_dose_mamm, EEC_diet, at_mamm, aw_mamm, fi_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, C_t,
                  noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, C_t, noa, a_r, frac_act_ing, para, h_l,
                                  day_out)
    at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
    return EEC_dose_mamm / at_mamm


# Acute dose-based risk quotients for granivores mammals
# def ARQ_dose_mamm_g(EEC_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, h_l):
# if para==15:
# EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, h_l)
# at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
# return (EEC_dose_mamm/at_mamm)
# else:
# return(0)

# Acute dietary-based risk quotients for birds
@timefn
def ARQ_diet_bird(EEC_diet, lc50_bird, C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_diet = EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out)
    return EEC_diet / lc50_bird


# Acute dietary-based risk quotients for mammals
@timefn
def ARQ_diet_mamm(EEC_diet, lc50_mamm, C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_diet = EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out)
    return EEC_diet / lc50_mamm


# Chronic dietary-based risk quotients for birds
@timefn
def CRQ_diet_bird(EEC_diet, NOAEC_bird, C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_diet = EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out)
    return EEC_diet / NOAEC_bird


# Chronic dietary-based risk quotients for mammals
@timefn
def CRQ_diet_mamm(EEC_diet, NOAEC_mamm, C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    EEC_diet = EEC_diet(C_0, C_t, noa, a_r, frac_act_ing, para, h_l, day_out)
    return EEC_diet / NOAEC_mamm


# Chronic dose-based risk quotients for mammals
@timefn
def CRQ_dose_mamm(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, fi_mamm, tw_mamm, mf_w_mamm, C_0,
                  C_t, noa, a_r, frac_act_ing, para, h_l, day_out):
    ANOAEL_mamm = ANOAEL_mamm(NOAEL_mamm, aw_mamm, tw_mamm)
    EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, C_t, noa, a_r, frac_act_ing, para, h_l,
                                  day_out)
    return EEC_dose_mamm / ANOAEL_mamm

# initial concentration for different food types (short grass)
@timefn
def c_0_sg(self):
    self.out_c_0_sg = self.first_app_lb * self.frac_act_ing * 240.
    return self.out_c_0_sg

# initial concentration for different food types (tall grass)
@timefn
def c_0_tg(self):
    self.out_c_0_tg = self.first_app_lb * self.frac_act_ing * 110.
    return self.out_c_0_tg

# initial concentration for different food types (broad-leafed plants)
@timefn
def c_0_blp(self):
    self.out_c_0_blp = self.first_app_lb * self.frac_act_ing * 135.
    return self.out_c_0_blp

# initial concentration for different food types (fruits/pods)
@timefn
def c_0_fp(self):
    self.out_c_0_fp = self.first_app_lb * self.frac_act_ing * 15.
    return self.out_c_0_fp

# initial concentration for different food types (arthropods)
@timefn
def c_0_arthro(self):
    self.out_c_0_arthro = self.first_app_lb * self.frac_act_ing * 94.
    return self.out_c_0_arthro

# mean concentration estimate based on first application rate (short grass)
@timefn
def c_mean_sg(self):
    self.out_c_mean_sg = self.first_app_lb * self.frac_act_ing * 85.
    return self.out_c_mean_sg

# mean concentration estimate based on first application rate (tall grass)
@timefn
def c_mean_tg(self):
    self.out_c_mean_tg = self.first_app_lb * self.frac_act_ing * 36.
    return self.out_c_mean_tg

# mean concentration estimate based on first application rate (broad-leafed plants)
@timefn
def c_mean_blp(self):
    self.out_c_mean_blp = self.first_app_lb * self.frac_act_ing * 45.
    return self.out_c_mean_blp

# mean concentration estimate based on first application rate (fruits/pods)
@timefn
def c_mean_fp(self):
    self.out_c_mean_fp = self.first_app_lb * self.frac_act_ing * 7.
    return self.out_c_mean_fp

# mean concentration estimate based on first application rate (arthropods)
@timefn
def c_mean_arthro(self):
    self.out_c_mean_arthro = self.first_app_lb * self.frac_act_ing * 65.
    return self.out_c_mean_arthro

# Chronic dose-based risk quotients for granviores mammals
# def CRQ_dose_mamm_g(EEC_diet, EEC_dose_mamm, ANOAEL_mamm, NOAEL_mamm, aw_mamm, tw_mamm, mf_w_mamm, noa, a_r,
# frac_act_ing, para, h_l):
# if para==15:
# ANOAEL_mamm=ANOAEL_mamm(NOAEL_mamm,aw_mamm,tw_mamm)
# EEC_dose_mamm = EEC_dose_mamm(EEC_diet, aw_mamm, fi_mamm, mf_w_mamm, C_0, noa, a_r, frac_act_ing, para, h_l)
# return (EEC_dose_mamm/ANOAEL_mamm)
# else:
# return (0)

# LD50ft-2 for row/band/in-furrow granular birds
@timefn
def LD50_rg_bird(application_type, a_r, frac_act_ing, p_i, r_s, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
    if application_type == 'Row/Band/In-furrow-Granular':
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        # print 'r_s', r_s
        n_r = (43560 ** 0.5) / r_s
        # print 'n_r=', n_r
        # print 'a_r=', a_r
        # print 'b_w=', b_w
        # print 'p_i=', p_i
        # print 'frac_act_ing', frac_act_ing
        # print 'class a_r', type(a_r)
        expo_rg_bird = (max(a_r) * frac_act_ing * 453590.0) / (n_r * (43560.0 ** 0.5) * b_w) * (1 - p_i)
        return expo_rg_bird / (at_bird * (aw_bird / 1000.0))
    else:
        return 0


# LD50ft-2 for row/band/in-furrow liquid birds
@timefn
def LD50_rl_bird(application_type, a_r, frac_act_ing, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
    if application_type == 'Row/Band/In-furrow-Liquid':
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        expo_rl_bird = ((max(a_r) * 28349 * frac_act_ing) / (1000 * b_w)) * (1 - p_i)
        return expo_rl_bird / (at_bird * (aw_bird / 1000.0))
    else:
        return 0


# LD50ft-2 for row/band/in-furrow granular mammals
@timefn
def LD50_rg_mamm(application_type, a_r, frac_act_ing, p_i, r_s, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if application_type == 'Row/Band/In-furrow-Granular':
        # a_r = max(first_app_lb)
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        n_r = (43560 ** 0.5) / r_s
        expo_rg_mamm = (max(a_r) * frac_act_ing * 453590) / (n_r * (43560 ** 0.5) * b_w) * (1 - p_i)
        return expo_rg_mamm / (at_mamm * (aw_mamm / 1000.0))
    else:
        return 0


# LD50ft-2 for row/band/in-furrow liquid mammals
@timefn
def LD50_rl_mamm(application_type, a_r, frac_act_ing, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if application_type == 'Row/Band/In-furrow-Liquid':
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        expo_rl_bird = ((max(a_r) * 28349 * frac_act_ing) / (1000 * b_w)) * (1 - p_i)
        return expo_rl_bird / (at_mamm * (aw_mamm / 1000.0))
    else:
        return 0


# LD50ft-2 for broadcast granular birds
@timefn
def LD50_bg_bird(application_type, a_r, frac_act_ing, aw_bird, at_bird, ld50_bird, tw_bird, x):
    if application_type == 'Broadcast-Granular':
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        expo_bg_bird = ((max(a_r) * frac_act_ing * 453590) / 43560)
        return expo_bg_bird / (at_bird * (aw_bird / 1000.0))
    else:
        return 0


# LD50ft-2 for broadcast liquid birds
@timefn
def LD50_bl_bird(application_type, a_r, frac_act_ing, aw_bird, at_bird, ld50_bird, tw_bird, x):
    if application_type == 'Broadcast-Liquid':
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        # expo_bl_bird=((max(a_r)*28349*frac_act_ing)/43560)*(1-p_i)
        expo_bl_bird = ((max(a_r) * 453590 * frac_act_ing) / 43560)
        return expo_bl_bird / (at_bird * (aw_bird / 1000.0))
    else:
        return 0


# LD50ft-2 for broadcast granular mammals
@timefn
def LD50_bg_mamm(application_type, a_r, frac_act_ing, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if application_type == 'Broadcast-Granular':
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        expo_bg_mamm = ((max(a_r) * frac_act_ing * 453590) / 43560)
        return expo_bg_mamm / (at_mamm * (aw_mamm / 1000.0))
    else:
        return 0


# LD50ft-2 for broadcast liquid mammals
@timefn
def LD50_bl_mamm(application_type, a_r, frac_act_ing, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
    if application_type == 'Broadcast-Liquid':
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        # expo_bl_mamm=((max(a_r)*28349*frac_act_ing)/43560)*(1-p_i)
        expo_bl_mamm = ((max(a_r) * frac_act_ing * 453590) / 43560)
        return expo_bl_mamm / (at_mamm * (aw_mamm / 1000.0))
    else:
        return 0