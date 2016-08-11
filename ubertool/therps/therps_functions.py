from __future__ import division  #brings in Python 3.0 mixed type calculation rules
from functools import wraps
import logging
import numpy as np
import pandas as pd
import time


class THerpsFunctions(object):
    """
    Function class for THerps.
    """

    def __init__(self):
        """Class representing the functions for Trex"""
        super(THerpsFunctions, self).__init__()

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

        food_intake_herps = pd.Series([], 'float')
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

    # def at_bird(self, avian_ld50, bw_herp, tw_bird, mineau_scaling_factor):
    #     """
    #     acute adjusted toxicity value for birds.
    #     :param avian_ld50:
    #     :param bw_herp:
    #     :param tw_bird:
    #     :param mineau_scaling_factor:
    #     :return:
    #     """
    #     try:
    #         avian_ld50 = float(avian_ld50)
    #         bw_herp = float(bw_herp)
    #         tw_bird = float(tw_bird)
    #         mineau_scaling_factor = float(mineau_scaling_factor)
    #     except IndexError:
    #         raise IndexError \
    #             ('The lethal dose, body weight of assessed bird, body weight of tested' \
    #              ' bird, and/or Mineau scaling factor for birds must be supplied on' \
    #              ' the command line.')
    #     except ValueError:
    #         raise ValueError \
    #             ('The lethal dose must be a real number, not "%mg/kg"' % avian_ld50)
    #     except ValueError:
    #         raise ValueError \
    #             ('The body weight of assessed bird must be a real number, not "%g"' % bw_herp)
    #     except ValueError:
    #         raise ValueError \
    #             ('The body weight of tested bird must be a real number, not "%g"' % tw_bird)
    #     except ValueError:
    #         raise ValueError \
    #             ('The Mineau scaling factor for birds must be a real number' % mineau_scaling_factor)
    #     except ZeroDivisionError:
    #         raise ZeroDivisionError \
    #             ('The body weight of tested bird must be non-zero.')
    #     if avian_ld50 < 0:
    #         raise ValueError \
    #             ('ld50=%g is a non-physical value.' % avian_ld50)
    #     if bw_herp < 0:
    #         raise ValueError \
    #             ('bw_herp=%g is a non-physical value.' % bw_herp)
    #     if tw_bird < 0:
    #         raise ValueError \
    #             ('tw_bird=%g is a non-physical value.' % tw_bird)
    #     if mineau_scaling_factor < 0:
    #         raise ValueError \
    #             ('mineau_scaling_factor=%g is non-physical value.' % mineau_scaling_factor)
    #     return (avian_ld50) * ((bw_herp / tw_bird) ** (mineau_scaling_factor - 1))

    def at_bird(self, aw_herp):
        """
        # Acute adjusted toxicity value for birds
        # Note: bird toxicity data is used as surrogate for herptiles due to lack of herptile data
        """
        adjusted_toxicity = pd.Series([], dtype='float')
        adjusted_toxicity = self.ld50_bird * ((aw_herp / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1))
        return adjusted_toxicity

##?? following method is not called; contained in and not called in original THERPS.py either
    # def at_mamm(ld50_mamm, aw_mamm, tw_mamm):
    #     """
    #     acute adjusted toxicity value for mammals.
    #     :param aw_mamm:
    #     :param tw_mamm:
    #     :return:
    #     """
    #     try:
    #         ld50_mamm = float(ld50_mamm)
    #         aw_mamm = float(aw_mamm)
    #         tw_mamm = float(tw_mamm)
    #     except IndexError:
    #         raise IndexError \
    #             ('The lethal dose, body weight of assessed mammal, and body weight of tested' \
    #              ' mammal must be supplied on' \
    #              ' the command line.')
    #     except ValueError:
    #         raise ValueError \
    #             ('The lethal dose must be a real number, not "%mg/kg"' % ld50_mamm)
    #     except ValueError:
    #         raise ValueError \
    #             ('The body weight of assessed mammals must be a real number, not "%g"' % aw_mamm)
    #     except ValueError:
    #         raise ValueError \
    #             ('The body weight of tested mammals must be a real number, not "%g"' % tw_mamm)
    #     except ZeroDivisionError:
    #         raise ZeroDivisionError \
    #             ('The body weight of tested mammals must be non-zero.')
    #     if ld50_mamm < 0:
    #         raise ValueError \
    #             ('ld50_mamm=%g is a non-physical value.' % ld50_mamm)
    #     if aw_mamm < 0:
    #         raise ValueError \
    #             ('aw_mamm=%g is a non-physical value.' % aw_mamm)
    #     if tw_mamm < 0:
    #         raise ValueError \
    #             ('tw_mamm=%g is a non-physical value.' % tw_mamm)
    #     return (ld50_mamm) * ((tw_mamm / aw_mamm) ** (0.25))

##?? following method is not called; contained in and not called in original THERPS.py either
    # def anoael_mamm(noael_mamm, aw_mamm, tw_mamm):
    #     """
    #     adjusted chronic toxicity (noael) value for mammals
    #     :param aw_mamm:
    #     :param tw_mamm:
    #     :return:
    #     """
    #     try:
    #         noael_mamm = float(noael_mamm)
    #         aw_mamm = float(aw_mamm)
    #         tw_mamm = float(tw_mamm)
    #     except IndexError:
    #         raise IndexError \
    #             ('The noael, body weight of assessed mammal, and body weight of tested' \
    #              ' mammal must be supplied on' \
    #              ' the command line.')
    #     except ValueError:
    #         raise ValueError \
    #             ('The noael must be a real number, not "%mg/kg"' % noael_mamm)
    #     except ValueError:
    #         raise ValueError \
    #             ('The body weight of assessed mammals must be a real number, not "%g"' % aw_mamm)
    #     except ValueError:
    #         raise ValueError \
    #             ('The body weight of tested mammals must be a real number, not "%g"' % tw_mamm)
    #     except ZeroDivisionError:
    #         raise ZeroDivisionError \
    #             ('The body weight of tested mammals must be non-zero.')
    #     if noael_mamm < 0:
    #         raise ValueError \
    #             ('noael_mamm=%g is a non-physical value.' % noael_mamm)
    #     if aw_mamm < 0:
    #         raise ValueError \
    #             ('aw_mamm=%g is a non-physical value.' % aw_mamm)
    #     if tw_mamm < 0:
    #         raise ValueError \
    #             ('tw_mamm=%g is a non-physical value.' % tw_mamm)
    #     return (noael_mamm) * ((tw_mamm / aw_mamm) ** (0.25))

    # def c_0(self, a_r, a_i, para):
    #     """
    #     Initial concentration
    #     :param a_r:
    #     :param a_i:
    #     :param para:
    #     :return:
    #     """
    #     try:
    #         a_r = float(a_r)
    #         a_i = float(a_i)
    #     except IndexError:
    #         raise IndexError \
    #             ('The application rate, and/or the percentage of active ingredient ' \
    #              'must be supplied on the command line.')
    #     except ValueError:
    #         raise ValueError \
    #             ('The application rate must be a real number, not "%g"' % a_r)
    #     except ValueError:
    #         raise ValueError \
    #             ('The percentage of active ingredient must be a real number, not "%"' % a_i)
    #     if a_r < 0:
    #         raise ValueError \
    #             ('The application rate=%g is a non-physical value.' % a_r)
    #     if a_i < 0:
    #         raise ValueError \
    #             ('The percentage of active ingredient=%g is a non-physical value.' % a_i)
    #     return (a_r * a_i * para)

    # def c_t(self, C_ini, h_l):
    #     """
    #     Concentration over time
    #     :param C_ini:
    #     :param h_l:
    #     :return:
    #     """
    #     try:
    #         h_l = float(h_l)
    #     except IndexError:
    #         raise IndexError \
    #             ('The initial concentration, and/or the foliar dissipation half life, ' \
    #              'must be supplied on the command line.')
    #     except ValueError:
    #         raise ValueError \
    #             ('The foliar dissipation half life must be a real number, not "%g"' % h_l)
    #     if h_l < 0:
    #         raise ValueError \
    #             ('The foliar dissipation half life=%g is a non-physical value.' % h_l)
    #     return (C_ini * np.exp(-(np.log(2) / h_l) * 1))

    # def eec_diet(self, c_0, c_t, n_a, i_a, a_r, a_i, para, h_l):
    #     """
    #     Dietary based eecs
    #     :param c_0:
    #     :param c_t:
    #     :param n_a:
    #     :param i_a:
    #     :param a_r:
    #     :param a_i:
    #     :param para:
    #     :param h_l:
    #     :return:
    #     """
    #     c_0 = c_0(a_r, a_i, para)
    #     try:
    #         n_a = float(n_a)
    #         i_a = float(i_a)
    #     except IndexError:
    #         raise IndexError \
    #             ('The number of applications, and/or the interval between applications ' \
    #              'must be supplied on the command line.')
    #     except ValueError:
    #         raise ValueError \
    #             ('The number of applications must be a real number, not "%g"' % n_a)
    #     except ValueError:
    #         raise ValueError \
    #             ('The interval between applications must be a real number, not "%g"' % i_a)
    #     if n_a < 0:
    #         raise ValueError \
    #             ('The number of applications=%g is a non-physical value.' % n_a)
    #     if i_a < 0:
    #         raise ValueError \
    #             ('The interval between applications=%g is a non-physical value.' % i_a)
    #     if a_i * n_a > 365:
    #         raise ValueError \
    #             ('The schduled application=%g is over the modeling period (1 year).' % i_a * n_a)
    #
    #         # c_temp=[1.0]*365 #empty array to hold the concentrations over days
    #     c_temp = np.ones((365, 1))  # empty array to hold the concentrations over days
    #     a_p_temp = 0  # application period temp
    #     n_a_temp = 0  # number of existed applications
    #
    #     for i in range(0, 365):
    #         if i == 0:
    #             a_p_temp = 0
    #             n_a_temp = n_a_temp + 1
    #             c_temp[i] = c_0
    #         elif a_p_temp == (i_a - 1) and n_a_temp < n_a:
    #             a_p_temp = 0
    #             n_a_temp = n_a_temp + 1
    #             c_temp[i] = c_t(c_temp[i - 1], h_l) + c_0
    #         elif a_p_temp < (i_a - 1) and n_a_temp <= n_a:
    #             a_p_temp = a_p_temp + 1
    #             c_temp[i] = c_t(c_temp[i - 1], h_l)
    #         else:
    #             c_temp[i] = c_t(c_temp[i - 1], h_l)
    #     return (max(c_temp))

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
        # get maximum daily concentration that occurs during the year
        max_concs = [temp_ts[i].max() for i in range(temp_ts.__len__())]
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
        eec_dose_tp_temp = pd.Series([], 'float')
        at_bird_temp = pd.Series([], 'float')
        amphibian_acute_rq = pd.Series([], 'float')

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
        return (eec_diet_tp_temp / self.lc50_bird)

    def crq_diet_herp(self, food_multiplier):
        """
        amphibian chronic dietary-based risk quotients

        :return:
        """

        eec_diet_temp = pd.Series([], dtype = 'float')
        amphibain_chronic_rq = pd.Series([], dtype = 'float')

        eec_diet_temp = self.eec_diet_max(food_multiplier)
        ##??assert isinstance(eec_diet, object)
        amphibain_chronic_rq = eec_diet_temp / self.noaec_bird
        return

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
