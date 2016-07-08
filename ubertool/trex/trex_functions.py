from __future__ import division  #brings in Python 3.0 mixed type calculation rules
from functools import wraps
import logging
import numpy as np
import pandas as pd
import time


class TRexFunctions(object):
    """
    Function class for Trex.
    """

    def __init__(self):
        """Class representing the functions for Trex"""
        super(TRexFunctions, self).__init__()

    def app_rate_parsing(self):
        # extract first day and maximum application rates from each model simulation run
        # these variables are needed in various methods
        self.first_app_rate = pd.Series([], dtype='float') #series of first_day app rates across model simulations
        self.max_app_rate = pd.Series([], dtype='float') #series of maximum app_rates across model simulations
        for i in range(len(self.app_rates)):
            self.first_app_rate[i] = self.app_rates[i][0]
            self.max_app_rate[i] = max(self.app_rates[i])
        return

    def convert_strlist_float(self, pd_series_strings):
        #method converts a panda series of lists whose elements are strings
        #to a series of lists of either floats
        #create list of strings
        pd_series_floats = pd.Series([], dtype="object")
        temp1 = pd.Series([], dtype="object")
        temp = pd_series_strings.tolist()
        for j, item in enumerate(temp):
            temp1[j] = item.strip('[')
            temp1[j] = temp1[j].strip(']')
        #create list of vectors of strings
        temp2 = [str(i).split(',') for i in temp1]
        #convert to floats and assign back to series
        for j, item in enumerate(temp2):
            temp_item = map(float, item)
            pd_series_floats.loc[j] = temp_item
        return pd_series_floats

    def convert_strlist_int(self, pd_series_strings):
        # #method converts a panda series of lists whose elements are strings
        # #to a series of lists of either floats
        # #create list of strings
        # pd_series_ints = pd.Series([], dtype="object")
        # temp = pd_series_strings.tolist()
        # #create list of vectors of strings
        # temp2 = [str(i).split(',') for i in temp]
        # #convert to floats and assign back to series
        # for j, item in enumerate(temp2):
        #     temp_item = map(int, item)
        #     pd_series_ints.loc[j] = temp_item
        # return pd_series_ints
            #method converts a panda series of lists whose elements are strings
        #to a series of lists of either floats
        #create list of strings
        pd_series_ints = pd.Series([], dtype="object")
        temp1 = pd.Series([], dtype="object")
        temp = pd_series_strings.tolist()
        for j, item in enumerate(temp):
            temp1[j] = item.strip('[')
            temp1[j] = temp1[j].strip(']')
        #create list of vectors of strings
        temp2 = [str(i).split(',') for i in temp1]
        #convert to floats and assign back to series
        for j, item in enumerate(temp2):
            temp_item = map(int, item)
            pd_series_ints.loc[j] = temp_item
        return pd_series_ints

    def conc_initial(self, i, application_rate, food_multiplier):
    # Initial concentration from new application
        conc_0 = (application_rate * self.frac_act_ing[i] * food_multiplier)
        return conc_0

    def conc_timestep(self, i, conc_ini):
        # calculate concentration resulting from degradation for a daily timestep
        #??what is the purpose of the '* 1', just a timestep value to be complete
        conc = conc_ini * np.exp(-(np.log(2) / self.foliar_diss_hlife[i]) * 1)
        return conc

    def percent_to_frac(self, percent):
        fraction = percent / 100.
        return fraction

    def inches_to_feet(self, inches):
        feet = inches / 12
        return feet

    def sa_bird_1(self, size):
    # Seed treatment acute RQ for birds method 1

        # setup panda series
        at_bird_temp = pd.Series([], dtype='float', name="at_bird_temp")
        fi_bird_temp = pd.Series([], dtype='float',name="fi_bird_temp")
        #maximum seed application rate (m_s_r_p)
        m_s_a_r_temp = pd.Series([], dtype='float',name="m_s_a_r_temp")
        nagy_bird_temp = pd.Series([], dtype='float',name="nagy_bird_temp")
        aw_bird = pd.Series([], dtype = 'float', name="aw_bird")

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

        #fi_bird_temp = self.fi_bird(aw_bird, mf_w_bird)
        for i in range(len(aw_bird)):
            at_bird_temp[i] = self.at_bird(i, aw_bird[i])
        fi_bird_temp = self.fi_bird(aw_bird, mf_w_bird)
        m_s_a_r_temp = ((self.first_app_rate  * self.frac_act_ing) / 128.) * self.density * 10000
        nagy_bird_temp = fi_bird_temp * 0.001 * m_s_a_r_temp / nagy_bird_coef
        sa_bird_1_return = nagy_bird_temp / at_bird_temp
        return sa_bird_1_return

    def sa_bird_2(self, size): 
        # Seed treatment acute RQ for birds method 2

        at_bird_temp = pd.Series([], dtype='float', name="at_bird_temp")
        m_a_r = pd.Series([], dtype='float', name="m_a_r")
        av_ai = pd.Series([], dtype='float', name="av_ai")
        sa_bird_2_return = pd.Series([], dtype='float', name="sa_bird_2_return")

        if size == "small":
            nagy_bird_coef = self.nagy_bird_coef_sm
            aw_bird = self.aw_bird_sm
        elif size == "medium":
            nagy_bird_coef = self.nagy_bird_coef_md
            aw_bird = self.aw_bird_md
        elif size == "large":
            nagy_bird_coef = self.nagy_bird_coef_lg
            aw_bird = self.aw_bird_lg

        for i in range(len(aw_bird)):
            at_bird_temp[i] = self.at_bird(i, aw_bird[i])
        m_a_r = (self.max_seed_rate * ((self.frac_act_ing * self.first_app_rate) / 128) * self.density) / 100  # maximum application rate
        av_ai = m_a_r * 1e6 / (43560 * 2.2)
        sa_bird_2_return = av_ai / (at_bird_temp * nagy_bird_coef)
        return sa_bird_2_return

    def sc_bird(self):
        # Seed treatment chronic RQ for birds
        m_s_a_r = ((self.first_app_rate * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        risk_quotient = m_s_a_r / self.noaec_bird
        return risk_quotient

    def sa_mamm_1(self, size):
        # Seed treatment acute RQ for mammals method 1

        at_mamm_temp = pd.Series([], dtype='float', name="at_mamm_temp")

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

        for i in range(len(aw_mamm)):
            at_mamm_temp[i] = self.at_mamm(i, aw_mamm[i])
        fi_mamm_temp = self.fi_mamm(aw_mamm, mf_w_bird)
        m_s_a_r = ((self.first_app_rate * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        nagy_mamm = fi_mamm_temp * 0.001 * m_s_a_r / nagy_mamm_coef
        quotient = nagy_mamm / at_mamm_temp
        return quotient

    def sa_mamm_2(self, size):
        # Seed treatment acute RQ for mammals method 2

        at_mamm_temp = pd.Series([], dtype='float', name="at_mamm_temp")

        if size == "small":
            nagy_mamm_coef = self.nagy_mamm_coef_sm
            aw_mamm = self.aw_mamm_sm
        elif size == "medium":
            nagy_mamm_coef = self.nagy_mamm_coef_md
            aw_mamm = self.aw_mamm_md
        elif size == "large":
            nagy_mamm_coef = self.nagy_mamm_coef_lg
            aw_mamm = self.aw_mamm_lg

        for i in range(len(aw_mamm)):
            at_mamm_temp[i] = self.at_mamm(i, aw_mamm[i])
        m_a_r = (self.max_seed_rate * ((self.first_app_rate * self.frac_act_ing) / 128) * self.density) / 100  # maximum application rate
        av_ai = m_a_r * 1000000 / (43560 * 2.2)
        quotient = av_ai / (at_mamm_temp * nagy_mamm_coef)
        return quotient

    def sc_mamm(self, size):
        # Seed treatment chronic RQ for mammals

        if size == "small":
            mf_w_mamm = self.mf_w_mamm_1
            nagy_mamm_coef = self.nagy_mamm_coef_sm
            aw_mamm = self.aw_mamm_sm
        elif size == "medium":
            mf_w_mamm = self.mf_w_mamm_1
            nagy_mamm_coef = self.nagy_mamm_coef_md
            aw_mamm = self.aw_mamm_md
        elif size == "large":
            mf_w_mamm = self.mf_w_mamm_1
            nagy_mamm_coef = self.nagy_mamm_coef_lg
            aw_mamm = self.aw_mamm_lg

        anoael_mamm_temp = self.anoael_mamm(aw_mamm)
        fi_mamm_temp = self.fi_mamm(aw_mamm, mf_w_mamm)
        m_s_a_r = ((self.first_app_rate * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        nagy_mamm = fi_mamm_temp * 0.001 * m_s_a_r / nagy_mamm_coef
        quotient = nagy_mamm / anoael_mamm_temp
        return quotient

    def fi_bird(self, aw_bird, mf_w_bird):
        # food intake for birds
        food_intake = (0.648 * (aw_bird ** 0.651)) / (1 - mf_w_bird)
        return food_intake

    def fi_mamm(self, aw_mamm, mf_w_mamm):
        # food intake for mammals
        food_intake = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        return food_intake

    def at_bird(self, i, aw_bird):
        # Acute adjusted toxicity value for birds
        adjusted_toxicity = self.ld50_bird[i] * (aw_bird / self.tw_bird_ld50[i]) ** (self.mineau_sca_fact[i] - 1)
        return adjusted_toxicity

    def at_bird1(self, aw_bird):
        # Acute adjusted toxicity value for birds
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        return adjusted_toxicity

    def at_mamm(self, i, aw_mamm):
        # Acute adjusted toxicity value for mammals
        adjusted_toxicity = self.ld50_mamm[i] * ((self.tw_mamm[i] / aw_mamm) ** 0.25)
        return adjusted_toxicity

    def anoael_mamm(self, aw_mamm):
    # Adjusted chronic toxicity (NOAEL) value for mammals
        adjusted_toxicity = self.noael_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
        return adjusted_toxicity

    def eec_diet_max(self, food_multiplier):
        """
        method produces a concentration timeseries (daily for 1 yr + a week) and extracts the maximum concentration value
        """
        max_concs = pd.Series([], dtype = 'float')
        temp_ts = pd.Series([], dtype = 'float')

        #get timeseries
        temp_ts = self.eec_diet_timeseries(food_multiplier)
        max_concs = [temp_ts[i].max() for i in range(temp_ts.__len__())]
        return max_concs

    def eec_diet_timeseries(self, food_multiplier):
        # Dietary based EECs
        # returns maximum daily concentration that occurs during year as result of one or more applications
        # calculations are performed daily from day of first application through the last day of the year
        # note: day numbers are synchronized with 0-based array indexing; thus January 1 is the 0th array index
        #max_conc = pd.Series([], dtype = 'float')
        c_temp_1 = pd.Series([], dtype='object')

        for i in range(len(self.num_apps)):  #i denotes model simulation (e.g., within monte carlo simulation)

            c_temp = np.zeros((371, 1))  # empty array to hold the concentrations over days of year (index 0 = Jan 1)
            app_counter = 0  #iniitalize application number counter for this iteration
            temp_num_apps = self.num_apps[i]
            temp_app_indices = np.asarray(self.day_out[i]) - 1
            temp_app_rates = np.asarray(self.app_rates[i])
            #temp_food_multiplier = np.float(food_multiplier[i])

            for day_index in range(temp_app_indices[0], 371):     # day number of first application
                if day_index == temp_app_indices[0]:  # first day of application (single or multiple application model simulation run)
                    c_temp[day_index] = self.conc_initial(i, temp_app_rates[0], food_multiplier)
                    app_counter += 1
                elif app_counter <= temp_num_apps - 1:  # next application day
                    if day_index == temp_app_indices[app_counter]:
                        c_temp[day_index] = (self.conc_timestep(i, c_temp[day_index - 1]) +
                                             self.conc_initial(i, temp_app_rates[app_counter], food_multiplier))
                        app_counter += 1
                    else:
                        c_temp[day_index] = self.conc_timestep(i, c_temp[day_index - 1])
                else:
                    #following line allows for all days after last application to be computed
                    c_temp[day_index] = self.conc_timestep(i, c_temp[day_index - 1])
            #max_conc[i] = float(max(c_temp))
            c_temp_1[i] = c_temp #complete set of time series (e.g., for plotting)
        return c_temp_1

    def eec_dose_bird(self, aw_bird, mf_w_bird, food_multiplier):
    # Dose based EECs for birds
        fi_bird_calc = self.fi_bird(aw_bird, mf_w_bird)
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        eec_out = eec_diet_temp * fi_bird_calc / aw_bird
        return eec_out

    def eec_dose_mamm(self, aw_mamm, mf_w_mamm, food_multiplier):
    # Dose based EECs for mammals
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        fi_mamm_temp = self.fi_mamm(aw_mamm, mf_w_mamm)
        dose_eec = eec_diet_temp * fi_mamm_temp / aw_mamm
        return dose_eec

    def arq_dose_bird(self, aw_bird, mf_w_bird, food_multiplier):
    # Acute dose-based risk quotients for birds
        at_bird_temp = pd.Series([], dtype = 'float')
        eec_dose_bird_temp = self.eec_dose_bird(aw_bird, mf_w_bird, food_multiplier)
        for i in range(len(aw_bird)):
            at_bird_temp[i] = self.at_bird(i, aw_bird[i])
        risk_quotient = eec_dose_bird_temp / at_bird_temp
        return risk_quotient

    def arq_dose_mamm(self, aw_mamm, mf_w_mamm, food_multiplier):
    # Acute dose-based risk quotients for mammals
        at_mamm_temp = pd.Series([], dtype = 'float')
        eec_dose_mamm_temp = self.eec_dose_mamm(aw_mamm, mf_w_mamm, food_multiplier)
        for i in range(len(aw_mamm)):
            at_mamm_temp[i] = self.at_mamm(i, aw_mamm[i])
        risk_quotient = eec_dose_mamm_temp / at_mamm_temp
        return risk_quotient

    def arq_diet_bird(self, food_multiplier):
    # Acute dietary-based risk quotients for birds
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        risk_quotient = eec_diet_temp / self.lc50_bird
        return risk_quotient

    def arq_diet_mamm(self, food_multiplier):
    # Acute dietary-based risk quotients for mammals
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        risk_quotient = eec_diet_temp / self.lc50_mamm
        return risk_quotient

    def crq_diet_bird(self, food_multiplier):
    # Chronic dietary-based risk quotients for birds
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        risk_quotient = eec_diet_temp / self.noaec_bird
        return risk_quotient

    def crq_diet_mamm(self, food_multiplier):
    # Chronic dietary-based risk quotients for mammals
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        crq_diet_mamm_temp = eec_diet_temp / self.noaec_mamm
        return crq_diet_mamm_temp

    def crq_dose_mamm(self, aw_mamm, mf_w_mamm, food_multiplier):
    # Chronic dose-based risk quotients for mammals
        anoael_mamm_temp = self.anoael_mamm(aw_mamm)
        eec_dose_mamm_temp = self.eec_dose_mamm(aw_mamm, mf_w_mamm, food_multiplier)
        risk_quotient = eec_dose_mamm_temp / anoael_mamm_temp
        return risk_quotient

    def ld50_rg_bird(self, aw_bird):
        # LD50ft-2 for row/band/in-furrow granular birds
        ld50_rg_bird_temp = pd.Series([], dtype='float')
        at_bird_temp = pd.Series([], dtype = 'float')
        num_rows_peracre = pd.Series([], dtype = 'float')
        expo_rg_bird = pd.Series([], dtype = 'float')
        for i in range(len(aw_bird)):
            if self.application_type[i] == 'Row/Band/In-furrow-Granular':
                at_bird_temp = self.at_bird(i, aw_bird[i])
                num_rows_peracre = (43560 ** 0.5) / self.row_spacing[i]
                expo_rg_bird = ((max(self.app_rates[i]) * self.frac_act_ing[i] * 453590.0) /
                               (num_rows_peracre * (43560.0 ** 0.5) * self.bandwidth[i])) * (1 - self.frac_incorp[i])
                ld50_rg_bird_temp[i] = expo_rg_bird / (at_bird_temp * (aw_bird[i] / 1000.0))
            else:
                ld50_rg_bird_temp[i] = np.nan
        return ld50_rg_bird_temp

    def ld50_rg_bird1(self, aw_bird):
        """
        # LD50ft-2 for row/band/in-furrow granular birds
        """

        ld50_rg_bird_temp = pd.Series([], dtype='float')
        at_bird_temp = pd.Series([], dtype = 'float')
        num_rows_peracre = pd.Series([], dtype = 'float')
        expo_rg_bird = pd.Series([], dtype = 'float')

        # calculate all values of 'ld50_rg_bird_temp' regardless of application_type (to facilitate vectorization)
        at_bird_temp = self.at_bird1(aw_bird)
        num_rows_peracre = (43560 ** 0.5) / self.row_spacing
        expo_rg_bird = ((self.max_app_rate * self.frac_act_ing * 453590.0) /
                       (num_rows_peracre * (43560.0 ** 0.5) * self.bandwidth)) * (1 - self.frac_incorp)
        ld50_rg_bird_temp = expo_rg_bird / (at_bird_temp * (aw_bird / 1000.0))
        #go back and replace all non 'Row/Band/In-furrow-Granular' app types with value of zero
        for i in range(len(aw_bird)):
            if self.application_type[i] != 'Row/Band/In-furrow-Granular':
                ld50_rg_bird_temp[i] = np.nan
        return ld50_rg_bird_temp

    def ld50_rl_bird(self, aw_bird):
        # LD50ft-2 for row/band/in-furrow liquid birds
        ld50_rl_bird_temp = pd.Series([], dtype = 'float')
        for i in range(len(aw_bird)):
            if self.application_type[i] == 'Row/Band/In-furrow-Liquid':
                at_bird_temp = self.at_bird(i, aw_bird[i])
                expo_rl_bird = ((max(self.app_rates[i]) * 28349 * self.frac_act_ing[i]) /
                                (1000 * self.bandwidth[i])) * (1 - self.frac_incorp[i])
                ld50_rl_bird_temp[i] = expo_rl_bird / (at_bird_temp * (aw_bird[i] / 1000.0))
            else:
                ld50_rl_bird_temp[i] = np.nan
        return ld50_rl_bird_temp

    def ld50_bg_bird(self, aw_bird):
        # LD50ft-2 for broadcast granular birds
        ld50_bg_bird_temp = pd.Series([], dtype = 'float')
        for i in range(len(aw_bird)):
            if self.application_type[i] == 'Broadcast-Granular':
                at_bird_temp = self.at_bird(i, aw_bird[i])
                expo_bg_bird = ((max(self.app_rates[i]) * self.frac_act_ing[i] * 453590) / 43560)
                ld50_bg_bird_temp[i] = expo_bg_bird / (at_bird_temp * (aw_bird[i] / 1000.0))
            else:
                ld50_bg_bird_temp[i] = np.nan
        return ld50_bg_bird_temp

    def ld50_bl_bird(self, aw_bird):
        # LD50ft-2 for broadcast liquid birds
        ld50_bl_bird_temp = pd.Series([], dtype = 'float')
        for i in range(len(aw_bird)):
            if self.application_type[i] == 'Broadcast-Liquid':
                at_bird_temp = self.at_bird(i, aw_bird[i])
                # this would be used for fl oz but front end requires lb/a
                # expo_bl_bird=((max(self.app_rates)*28349*frac_act_ing)/43560)*(1-frac_incorp)
                # for lb based liquid application rates
                expo_bl_bird = ((max(self.app_rates[i]) * 453590 * self.frac_act_ing[i]) / 43560)
                ld50_bl_bird_temp[i] = expo_bl_bird / (at_bird_temp * (aw_bird[i] / 1000.0))
            else:
                ld50_bl_bird_temp[i] = np.nan
        return ld50_bl_bird_temp

    def ld50_rg_mamm(self, aw_mamm):
        # LD50ft-2 for row/band/in-furrow granular mammals
        ld50_rg_mamm_temp = pd.Series([], dtype = 'float')
        for i in range(len(aw_mamm)):
            if self.application_type[i] == 'Row/Band/In-furrow-Granular':
                # a_r = max(app_rates)
                at_mamm_temp = self.at_mamm(i, aw_mamm[i])
                num_rows_peracre = (43560 ** 0.5) / self.row_spacing[i]
                expo_rg_mamm = ((max(self.app_rates[i]) * self.frac_act_ing[i] * 453590) /
                               (num_rows_peracre * (43560 ** 0.5) * self.bandwidth[i]) * (1 - self.frac_incorp[i]))
                ld50_rg_mamm_temp[i] = expo_rg_mamm / (at_mamm_temp * (aw_mamm[i] / 1000.0))
            else:
                ld50_rg_mamm_temp[i] = np.nan
        return ld50_rg_mamm_temp

    def ld50_rl_mamm(self, aw_mamm):
        # LD50ft-2 for row/band/in-furrow liquid mammals
        ld50_rl_mamm_temp = pd.Series([], dtype = 'float')
        for i in range(len(aw_mamm)):
            if self.application_type[i] == 'Row/Band/In-furrow-Liquid':
                at_mamm_temp = self.at_mamm(i, aw_mamm[i])
                expo_rl_mamm = ((max(self.app_rates[i]) * 28349 * self.frac_act_ing[i]) /
                                (1000 * self.bandwidth[i])) * (1 - self.frac_incorp[i])
                ld50_rl_mamm_temp[i] = expo_rl_mamm / (at_mamm_temp * (aw_mamm[i] / 1000.0))
            else:
                ld50_rl_mamm_temp[i] = np.nan
        return ld50_rl_mamm_temp

    def ld50_bg_mamm(self, aw_mamm):
    # LD50ft-2 for broadcast granular mammals
        ld50_bg_mamm_temp = pd.Series([], dtype="float")
        for i in range(len(aw_mamm)):
            if self.application_type[i] == 'Broadcast-Granular':
                at_mamm_temp = self.at_mamm(i, aw_mamm[i])
                expo_bg_mamm = ((max(self.app_rates[i]) * self.frac_act_ing[i] * 453590) / 43560)
                ld50_bg_mamm_temp[i] = expo_bg_mamm / (at_mamm_temp * (aw_mamm[i] / 1000.0))
            else:
                ld50_bg_mamm_temp[i] = np.nan
        return ld50_bg_mamm_temp

    def ld50_bl_mamm(self, aw_mamm):
    # LD50ft-2 for broadcast liquid mammals
        ld50_bl_mamm_temp = pd.Series([], dtype="float")
        for i in range(len(aw_mamm)):
            if self.application_type[i] == 'Broadcast-Liquid':
                at_mamm_temp = self.at_mamm(i, aw_mamm[i])
                # expo_bl_mamm=((max(self.app_rates)*28349*self.frac_act_ing)/43560)*(1-frac_incorp)
                expo_bl_mamm = ((max(self.app_rates[i]) * self.frac_act_ing[i] * 453590.) / 43560.)  #453590 mg/lb; 43560ft2/acre
                ld50_bl_mamm_temp[i] = expo_bl_mamm / (at_mamm_temp * (aw_mamm[i] / 1000.0))
            else:
                ld50_bl_mamm_temp[i] = np.nan
        return ld50_bl_mamm_temp