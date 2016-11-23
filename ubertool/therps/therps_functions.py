from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import numpy as np
import pandas as pd


class TherpsFunctions(object):
    """
    Function class for THerps.
    """

    def percent_to_frac(self, percent):
        fraction = percent / 100.
        return fraction

    def convert_app_intervals(self):
        """
        method converts number of applications and application interval into application rates and day of year number
        this is so that the same concentration timeseries method from trex_functions can be reused here
        :return:
        """
        day_out_temp = pd.Series([], dtype = 'object')
        app_rates_temp = pd.Series([], dtype = 'object')
        app_rate_temp = pd.Series([], dtype = 'float')
        app_days_temp = pd.Series([], dtype = 'int')

        for i in range(len(self.num_apps)):  # iterate over number of simulations to process
            app_days_temp = range(self.num_apps[i]) #reset list lengths for current iteration/simulation
            app_rate_temp = range(self.num_apps[i])
            for k in range (0, self.num_apps[i]):  # assign rates and app days per simulation
                app_rate_temp[k] = self.application_rate[i]
                if k == 0:
                    app_days_temp[k] = 1  #changed to 1 to reflect day number rather than list index                       #elif k == 1:
                        #    app_days_temp[k] = (self.app_interval[i] + app_days_temp[k-1]) - 1
                else:
                    app_days_temp[k] = self.app_interval[i] + app_days_temp[k-1]
            day_out_temp[i] = app_days_temp  #move simulation specific data lists into model objects
            app_rates_temp[i] = app_rate_temp
        return day_out_temp, app_rates_temp

    def convert_app_intervals_original(self):
        """
        method converts number of applications and application interval into application rates and day of year number
        this is so that the same concentration timeseries method from trex_functions can be reused here
        :return:
        """
        day_out_temp = pd.Series([], dtype = 'object')
        app_rates_temp = pd.Series([], dtype = 'object')
        app_rate_temp = pd.Series([], dtype = 'float')
        app_days_temp = pd.Series([], dtype = 'int')

        for i in range(len(self.num_apps)):  # iterate over number of simulations to process
            app_days_temp = range(self.num_apps[i]) #reset list lengths for current iteration/simulation
            app_rate_temp = range(self.num_apps[i])
            for k in range (0, self.num_apps[i]):  # assign rates and app days per simulation
                app_rate_temp[k] = self.application_rate[i]
                if k == 0:
                    app_days_temp[k] = 0
                elif k == 1:
                    app_days_temp[k] = (self.app_interval[i] + app_days_temp[k-1]) - 1
                else:
                    app_days_temp[k] = self.app_interval[i] + app_days_temp[k-1]
            day_out_temp[i] = app_days_temp  #move simulation specific data lists into model objects
            app_rates_temp[i] = app_rate_temp
        return day_out_temp, app_rates_temp

    def fi_herp(self, aw_herp, mf_w_herp):
        """
        Food intake for herps.
        :param aw_herp:
        :param mf_w_herp:
        :return:
        """

        food_intake_herps = pd.Series([], dtype = 'float')
        food_intake_herps = (0.013 * (aw_herp ** 0.773)) / (1 - mf_w_herp)
        return food_intake_herps

    def fi_mamm(self, aw_mamm, mf_w_mamm):
        """
        Food intake for mammals.
        :param aw_mamm:
        :param mf_w_mamm:
        :return:
        """

        food_intake_mamm = pd.Series([], dtype = 'float')
        food_intake_mamm = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        return food_intake_mamm

    def at_bird(self, aw_herp):
        """
        # Acute adjusted toxicity value for birds
        # Note: bird toxicity data is used as surrogate for herptiles due to lack of herptile data
        """
        adjusted_toxicity = pd.Series([], dtype='float')
        adjusted_toxicity = self.ld50_bird * ((aw_herp / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1))
        return adjusted_toxicity

    def conc_initial(self, i, application_rate, food_multiplier):
    # Initial concentration from new application
        conc_0 = (application_rate * self.frac_act_ing[i] * food_multiplier)
        return conc_0

    def conc_timestep(self, i, conc_ini):
        # calculate concentration resulting from degradation for a daily timestep
        #??what is the purpose of the '* 1', just a timestep value to be complete
        conc = conc_ini * np.exp(-(np.log(2) / self.foliar_diss_hlife[i]) * 1)
        return conc

    def eec_diet_max(self, food_multiplier):
        """
        method ported from trex_functions
        method calls method to produce a concentration timeseries (daily for 1 yr + a week) and extracts the maximum concentration value
        then scans the time series and extracts the maximum daily concentration for the year
        """
        max_concs = pd.Series([], dtype = 'float')
        temp_ts = pd.Series([], dtype = 'float')

        #get timeseries of daily concentrations for the year (+ a week)
        temp_ts = self.eec_diet_timeseries(food_multiplier)
        # get maximum daily concentration that occurs during the year for each simulation
        max_concs = pd.Series([temp_ts[i].max() for i in range(temp_ts.__len__())])
        return max_concs

    def eec_diet_timeseries(self, food_multiplier):
        """
        method ported from trex_functions
        method produces a concentration timeseries (daily for 1 yr + a week) and extracts the maximum concentration value
        """
        # Dietary based EECs
        # calculations are performed daily from day of first application through the last day of the year
        # note: day numbers are synchronized with 0-based array indexing; thus January 1 is the 0th array index
        c_temp_1 = pd.Series([], dtype='object')
        c_temp = pd.Series([], dtype='float')
        temp_app_indices = pd.Series([], dtype='float')
        temp_app_rates = pd.Series([], dtype='float')
        temp_num_apps = pd.Series([], dtype='float')

        for i in range(len(self.num_apps)):  #i denotes model simulation run (e.g., within a monte carlo simulation)

            c_temp = np.zeros((371, 1))  # empty array to hold the concentrations over days of year (index 0 = Jan 1)
            app_counter = 0  #iniitalize application number counter for this model simulation run (i)
            temp_num_apps = self.num_apps[i]
            #day_out is input as the day number, i.e., 1 - 365, the array indices start at 0, thus the '- 1'
            #should note that the user input for 'day_out' should be actual day number (i.e., 1 <- day_out <-365)
            temp_app_indices = np.asarray(self.day_out[i]) - 1
            temp_app_rates = np.asarray(self.app_rates[i])

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
            c_temp_1[i] = c_temp #complete set of time series (e.g., for plotting)
        return c_temp_1


    def eec_diet_mamm(self, food_multiplier, bw_frog_prey, mf_w_mamm):
        """
        Dietary_mammal based eecs

        :return:
        """
        eec_diet_temp = pd.Series([], dtype = 'float')
        fi_mamm_temp = pd.Series([], dtype = 'float')
        mammal_dietary_eec = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        fi_mamm_temp = self.fi_mamm(bw_frog_prey, mf_w_mamm)
        mammal_dietary_eec = eec_diet_temp * fi_mamm_temp / bw_frog_prey
        return mammal_dietary_eec

    def eec_diet_tp(self, food_multiplier, bw_frog_prey, awc_herp):
        """
        Dietary terrestrial phase based eecs

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        tp_dietary_eec = pd.Series([], dtype = 'float')
        fi_herp_temp = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        fi_herp_temp = self.fi_herp(bw_frog_prey, awc_herp)
        tp_dietary_eec = (eec_diet_temp * fi_herp_temp / (bw_frog_prey))
        return tp_dietary_eec

    def eec_dose_herp(self, aw_herp, awc_herp, food_multiplier):
        """
        amphibian Dose based eecs

        :return:
        """
        fi_herp_temp = pd.Series([], dtype = 'float')
        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibian_dose = pd.Series([], dtype = 'float')

        fi_herp_temp = self.fi_herp(aw_herp, awc_herp)
        eec_diet_temp = self.eec_diet_max(food_multiplier)
        amphibian_dose = (eec_diet_temp * fi_herp_temp / aw_herp)
        return amphibian_dose

    def eec_dose_mamm(self, food_multiplier, aw_herp, bw_frog_prey, mf_w_mamm):
        """
        amphibian Dose based eecs for mammals

        :return:
        """

        eec_diet_mamm_temp = pd.Series([], dtype = 'float')
        amphibian_dose_eec = pd.Series([], dtype = 'float')

        eec_diet_mamm_temp = self.eec_diet_mamm(food_multiplier, bw_frog_prey, mf_w_mamm)
        amphibian_dose_eec = eec_diet_mamm_temp * bw_frog_prey / aw_herp
        return amphibian_dose_eec

    def eec_dose_tp(self, food_multiplier, aw_herp, bw_frog_prey, awc_herp_sm, awc_herp_md):
        """
        amphibian Dose based eecs for terrestrial

        :return:
        """

        eec_diet_tp_temp = pd.Series([], dtype = 'float')
        fi_herp_temp = pd.Series([], dtype = 'float')
        amphibian_dose_eec = pd.Series([], dtype = 'float')

        eec_diet_tp_temp = self.eec_diet_tp(food_multiplier, bw_frog_prey, awc_herp_sm)
        fi_herp_temp = self.fi_herp(aw_herp, awc_herp_md)
        amphibian_dose_eec = eec_diet_tp_temp * fi_herp_temp / aw_herp
        return amphibian_dose_eec

    def arq_dose_herp(self, aw_herp, awc_herp, food_multiplier):
        """
        amphibian acute dose-based risk quotients

        :return:
        """
        at_bird_temp = pd.Series([], dtype = 'float')
        eec_dose_herp_temp = pd.Series([], dtype = 'float')
        amphibian_arq = pd.Series([], dtype = 'float')

        eec_dose_herp_temp = self.eec_dose_herp(aw_herp, awc_herp, food_multiplier)
        at_bird_temp = self.at_bird(aw_herp)
        amphibian_arq = (eec_dose_herp_temp / at_bird_temp)
        return amphibian_arq

    def arq_dose_mamm(self, food_multiplier, aw_herp, bw_frog_prey, mf_w_mamm):
        """
        amphibian acute dose-based risk quotients for mammals


        :return:
        """

        at_bird_temp = pd.Series([], dtype = 'float')
        eec_dose_mamm_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_dose_mamm_temp = self.eec_dose_mamm(food_multiplier, aw_herp, bw_frog_prey, mf_w_mamm)
        at_bird_temp = self.at_bird(aw_herp)
        amphibian_acute_rq = eec_dose_mamm_temp / at_bird_temp
        return amphibian_acute_rq

    def arq_dose_tp(self, food_multiplier, aw_herp, bw_frog_prey, awc_herp_sm, awc_herp_md):
        """
        amphibian acute dose-based risk quotients for tp

        :return:
        """
        eec_dose_tp_temp = pd.Series([], dtype = 'float')
        at_bird_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_dose_tp_temp = self.eec_dose_tp(food_multiplier, aw_herp, bw_frog_prey, awc_herp_sm, awc_herp_md)
        at_bird_temp = self.at_bird(aw_herp)
        amphibian_acute_rq = eec_dose_tp_temp / at_bird_temp
        return amphibian_acute_rq

    def arq_diet_herp(self, food_multiplier):
        """
        amphibian acute dietary-based risk quotients

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        amphibian_acute_rq = eec_diet_temp / self.lc50_bird
        return amphibian_acute_rq

    def arq_diet_mamm(self, food_multiplier, bw_frog_prey, mf_w_mamm):
        """
        amphibian acute dietary-based risk quotients for mammals

        :return:
        """

        eec_diet_mamm_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_diet_mamm_temp = self.eec_diet_mamm(food_multiplier, bw_frog_prey, mf_w_mamm)
        amphibian_acute_rq = eec_diet_mamm_temp / self.lc50_bird
        return amphibian_acute_rq

    def arq_diet_tp(self, food_multiplier, bw_frog_prey, awc_herp):
        """
        # amphibian acute dietary-based risk quotients for tp

        :return:
        """
        eec_diet_tp_temp = pd.Series([], dtype = 'float')
        amphibian_acute_rq = pd.Series([], dtype = 'float')

        eec_diet_tp_temp = self.eec_diet_tp(food_multiplier, bw_frog_prey, awc_herp)
        amphibian_acute_rq = eec_diet_tp_temp / self.lc50_bird
        return amphibian_acute_rq

    def crq_diet_herp(self, food_multiplier):
        """
        amphibian chronic dietary-based risk quotients

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibain_chronic_rq = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        amphibain_chronic_rq = eec_diet_temp / self.noaec_bird
        return amphibain_chronic_rq

    def crq_diet_mamm(self, food_multiplier, bw_frog_prey, mf_w_mamm):
        """
        amphibian chronic dietary-based risk quotients for mammal

        :return:
        """
        eec_diet_mamm_temp = pd.Series([], dtype = 'float')
        amphibian_chronic_rq = pd.Series([], dtype = 'float')

        eec_diet_mamm_temp = self.eec_diet_mamm(food_multiplier, bw_frog_prey, mf_w_mamm)
        amphibian_chronic_rq = eec_diet_mamm_temp / self.noaec_bird
        return amphibian_chronic_rq

    def crq_diet_tp(self, food_multiplier, bw_frog_prey, awc_herp):
        """
        amphibian chronic dietary-based risk quotients for tp

        :return:
        """
        eec_diet_tp_temp = pd.Series([], dtype = 'float')
        amphibian_chronic_rq = pd.Series([], dtype = 'float')

        eec_diet_tp_temp = self.eec_diet_tp(food_multiplier, bw_frog_prey, awc_herp)
        amphibian_chronic_rq = eec_diet_tp_temp / self.noaec_bird
        return amphibian_chronic_rq
