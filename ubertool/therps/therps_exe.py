from __future__ import division
import numpy as np
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
        print("therps_model_rest.py@timefn: " + fn.func_name + " took " + "{:.6f}".format(t2 - t1) + " seconds")
        return result

    return measure_time

class TherpsInputs(ModelSharedInputs):
    """
    Input class for Therps.
    """

    def __init__(self):
        """Class representing the inputs for Therps"""
        super(TherpsInputs, self).__init__()
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        """
        THerps constructor.
        :param chem_name:
        :param use:
        :param formu_name:
        :param a_i:
        :param h_l:
        :param n_a:
        :param i_a:
        :param a_r:
        :param avian_ld50:
        :param avian_lc50:
        :param avian_noaec:
        :param avian_noael:
        :param species_of_the_tested_bird_avian_ld50:
        :param species_of_the_tested_bird_avian_lc50:
        :param species_of_the_tested_bird_avian_noaec:
        :param species_of_the_tested_bird_avian_noael:
        :param bw_avian_ld50:
        :param bw_avian_lc50:
        :param bw_avian_noaec:
        :param bw_avian_noael:
        :param mineau_scaling_factor:
        :param bw_herp_a_sm:
        :param bw_herp_a_md:
        :param bw_herp_a_lg:
        :param wp_herp_a_sm:
        :param wp_herp_a_md:
        :param wp_herp_a_lg:
        :param c_mamm_a:
        :param c_herp_a:
        :return:
        """
        self.use = pd_obj['use']
        self.formu_name = pd_obj['formu_name']
        self.a_i = pd_obj['a_i']
        self.a_i_disp = pd_obj['100 * a_i']
        self.h_l = pd_obj['h_l']
        self.n_a = pd_obj['n_a']
        self.i_a = pd_obj['i_a']
        self.a_r = pd_obj['a_r']
        self.avian_ld50 = pd_obj['avian_ld50']
        self.avian_lc50 = pd_obj['avian_lc50']
        self.avian_noaec = pd_obj['avian_noaec']
        self.avian_noael = pd_obj['avian_noael']
        self.species_of_the_tested_bird_avian_ld50 = pd_obj['species_of_the_tested_bird_avian_ld50']
        self.species_of_the_tested_bird_avian_lc50 = pd_obj['species_of_the_tested_bird_avian_lc50']
        self.species_of_the_tested_bird_avian_noaec = pd_obj['species_of_the_tested_bird_avian_noaec']
        self.species_of_the_tested_bird_avian_noael = pd_obj['species_of_the_tested_bird_avian_noael']
        self.bw_avian_ld50 = pd_obj['bw_avian_ld50']
        self.bw_avian_lc50 = pd_obj['bw_avian_lc50']
        self.bw_avian_noaec = pd_obj['bw_avian_noaec']
        self.bw_avian_noael = pd_obj['bw_avian_noael']
        self.mineau_scaling_factor = pd_obj['mineau_scaling_factor']
        self.bw_herp_a_sm = pd_obj['bw_herp_a_sm']
        self.bw_herp_a_md = pd_obj['bw_herp_a_md']
        self.bw_herp_a_lg = pd_obj['bw_herp_a_lg']
        self.wp_herp_a_sm = pd_obj['wp_herp_a_sm']
        self.wp_herp_a_md = pd_obj['wp_herp_a_md']
        self.wp_herp_a_lg = pd_obj['wp_herp_a_lg']
        self.c_mamm_a = pd_obj['c_mamm_a']
        self.c_herp_a = pd_obj['c_herp_a']

class TherpsOutputs(object):
    """
    Output class for Therps.
    """

    def __init__(self):
        """Class representing the outputs for Therps"""
        super(TherpsOutputs, self).__init__()

        # Table 5
        self.ld50_ad_sm = self.at_bird(avian_ld50, bw_herp_a_sm, bw_avian_ld50, mineau_scaling_factor)
        self.ld50_ad_md = self.at_bird(avian_ld50, bw_herp_a_md, bw_avian_ld50, mineau_scaling_factor)
        self.ld50_ad_lg = self.at_bird(avian_ld50, bw_herp_a_lg, bw_avian_ld50, mineau_scaling_factor)

        self.eec_dose_bp_sm = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_dose_bp_md = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_dose_bp_lg = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_sm = self.arq_dose_herp(self.eec_dose_herp_sm, self.eec_diet, bw_herp_a_sm,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_md = self.arq_dose_herp(self.eec_dose_herp_md, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_lg = self.arq_dose_herp(self.eec_dose_herp_lg, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)

        self.eec_dose_fr_sm = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_dose_fr_md = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_dose_fr_lg = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_sm = self.arq_dose_herp(self.eec_dose_herp_sm, self.eec_diet, bw_herp_a_sm,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_md = self.arq_dose_herp(self.eec_dose_herp_md, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_lg = self.arq_dose_herp(self.eec_dose_herp_lg, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)

        self.eec_dose_hm_md = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 240, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_hm_lg = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 240, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_hm_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 240, h_l, self.fi_mamm)
        self.arq_dose_hm_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 240, h_l, self.fi_mamm)

        self.eec_dose_im_md = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 15, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_im_lg = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 15, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_im_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 15, h_l, self.fi_mamm)
        self.arq_dose_im_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 15, h_l, self.fi_mamm)

        self.eec_dose_tp_md = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                               135, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md)
        self.eec_dose_tp_lg = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                               135, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md)
        self.arq_dose_tp_md = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t,
                                               n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md, bw_avian_ld50,
                                               mineau_scaling_factor)
        self.arq_dose_tp_lg = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t,
                                               n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg, bw_avian_ld50,
                                               mineau_scaling_factor)

        # Table 6
        self.eec_diet_herp_bl = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_arq_herp_bl = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  135, h_l)
        self.eec_diet_herp_fr = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_arq_herp_fr = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15,
                                                  h_l)
        self.eec_diet_herp_hm = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 240, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_hm = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_im = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_im = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_tp = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l,
                                                 self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_arq_herp_tp = self.arq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a,
                                                i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 7
        self.eec_diet_herp_bl = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_crq_herp_bl = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  135, h_l)
        self.eec_diet_herp_fr = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_crq_herp_fr = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  15, h_l)
        self.eec_diet_herp_hm = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 240, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_hm = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_im = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_im = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_tp = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l,
                                                 self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_crq_herp_tp = self.crq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a,
                                                i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 8
        self.eec_dose_bp_sm_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_dose_bp_md_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_dose_bp_lg_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_sm_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_sm,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_md_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_md,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_lg_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_lg,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)

        self.eec_dose_fr_sm_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_dose_fr_md_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_dose_fr_lg_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_sm_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_sm,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_md_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_md,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_lg_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_lg,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)

        self.eec_dose_hm_md_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_hm_lg_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_hm_md_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_md, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)
        self.arq_dose_hm_lg_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_lg, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)

        self.eec_dose_im_md_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_im_lg_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_im_md_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_md, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)
        self.arq_dose_im_lg_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_lg, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)

        self.eec_dose_tp_md_mean = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                    a_i, 45, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm,
                                                    wp_herp_a_md)
        self.eec_dose_tp_lg_mean = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                    a_i, 45, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm,
                                                    wp_herp_a_md)
        self.arq_dose_tp_md_mean = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0,
                                                    self.c_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a,
                                                    wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md,
                                                    bw_avian_ld50, mineau_scaling_factor)
        self.arq_dose_tp_lg_mean = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0,
                                                    self.c_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a,
                                                    wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg,
                                                    bw_avian_ld50, mineau_scaling_factor)

        # Table 9
        self.eec_diet_herp_bl_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_arq_herp_bl_mean = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 45, h_l)
        self.eec_diet_herp_fr_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_arq_herp_fr_mean = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 7, h_l)
        self.eec_diet_herp_hm_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 85, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_hm_mean = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_im_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_im_mean = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_tp_mean = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l,
                                                      self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_arq_herp_tp_mean = self.arq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                     n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 10
        self.eec_diet_herp_bl_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_crq_herp_bl_mean = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 45, h_l)
        self.eec_diet_herp_fr_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_crq_herp_fr_mean = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 7, h_l)
        self.eec_diet_herp_hm_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 85, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_hm_mean = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_im_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_im_mean = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_tp_mean = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l,
                                                      self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_crq_herp_tp_mean = self.crq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                     n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)


class Therps(UberModel, TrexInputs, TrexOutputs):
    """
    Estimate dietary exposure and risk to terrestrial-phase amphibians and reptiles from pesticide use.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Trex model and containing all its methods"""
        super(TRex, self).__init__()
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

    def __init__(self, chem_name, use, formu_name, a_i, h_l, n_a, i_a, a_r, avian_ld50, avian_lc50, avian_noaec,
                 avian_noael,
                 species_of_the_tested_bird_avian_ld50, species_of_the_tested_bird_avian_lc50,
                 species_of_the_tested_bird_avian_noaec, species_of_the_tested_bird_avian_noael,
                 bw_avian_ld50, bw_avian_lc50, bw_avian_noaec, bw_avian_noael,
                 mineau_scaling_factor, bw_herp_a_sm, bw_herp_a_md, bw_herp_a_lg, wp_herp_a_sm, wp_herp_a_md,
                 wp_herp_a_lg, c_mamm_a, c_herp_a):


        # Result variables

        # Table 5
        self.ld50_ad_sm = self.at_bird(avian_ld50, bw_herp_a_sm, bw_avian_ld50, mineau_scaling_factor)
        self.ld50_ad_md = self.at_bird(avian_ld50, bw_herp_a_md, bw_avian_ld50, mineau_scaling_factor)
        self.ld50_ad_lg = self.at_bird(avian_ld50, bw_herp_a_lg, bw_avian_ld50, mineau_scaling_factor)

        self.eec_dose_bp_sm = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_dose_bp_md = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_dose_bp_lg = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_sm = self.arq_dose_herp(self.eec_dose_herp_sm, self.eec_diet, bw_herp_a_sm,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_md = self.arq_dose_herp(self.eec_dose_herp_md, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.arq_dose_bp_lg = self.arq_dose_herp(self.eec_dose_herp_lg, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)

        self.eec_dose_fr_sm = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_dose_fr_md = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_dose_fr_lg = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                 self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_sm = self.arq_dose_herp(self.eec_dose_herp_sm, self.eec_diet, bw_herp_a_sm,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_md = self.arq_dose_herp(self.eec_dose_herp_md, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.arq_dose_fr_lg = self.arq_dose_herp(self.eec_dose_herp_lg, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                 wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)

        self.eec_dose_hm_md = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 240, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_hm_lg = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 240, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_hm_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 240, h_l, self.fi_mamm)
        self.arq_dose_hm_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 240, h_l, self.fi_mamm)

        self.eec_dose_im_md = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 15, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_im_lg = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                 a_i, 15, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_im_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_md,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 15, h_l, self.fi_mamm)
        self.arq_dose_im_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet, bw_herp_a_lg,
                                                 self.at_bird, avian_ld50, bw_avian_ld50,
                                                 mineau_scaling_factor, c_mamm_a, 0.8, self.c_0, self.c_t, n_a, i_a,
                                                 a_r, a_i, 15, h_l, self.fi_mamm)

        self.eec_dose_tp_md = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                               135, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md)
        self.eec_dose_tp_lg = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                               135, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md)
        self.arq_dose_tp_md = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t,
                                               n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md, bw_avian_ld50,
                                               mineau_scaling_factor)
        self.arq_dose_tp_lg = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t,
                                               n_a, i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm,
                                               wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg, bw_avian_ld50,
                                               mineau_scaling_factor)

        # Table 6
        self.eec_diet_herp_bl = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_arq_herp_bl = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  135, h_l)
        self.eec_diet_herp_fr = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_arq_herp_fr = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15,
                                                  h_l)
        self.eec_diet_herp_hm = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 240, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_hm = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_im = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_im = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_tp = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l,
                                                 self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_arq_herp_tp = self.arq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a,
                                                i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 7
        self.eec_diet_herp_bl = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l)
        self.eec_crq_herp_bl = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  135, h_l)
        self.eec_diet_herp_fr = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l)
        self.eec_crq_herp_fr = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r, a_i,
                                                  15, h_l)
        self.eec_diet_herp_hm = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 240, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_hm = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 240, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_im = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 15, h_l,
                                                   self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_im = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                  n_a, i_a, a_r, a_i, 15, h_l, self.fi_mamm, c_mamm_a, 0.8)
        self.eec_diet_herp_tp = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 135, h_l,
                                                 self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_crq_herp_tp = self.crq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a,
                                                i_a, a_r, a_i, 135, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 8
        self.eec_dose_bp_sm_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_dose_bp_md_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_dose_bp_lg_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_sm_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_sm,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_md_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_md,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.arq_dose_bp_lg_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_lg,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)

        self.eec_dose_fr_sm_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_sm, wp_herp_a_sm, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_dose_fr_md_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_md, wp_herp_a_md, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_dose_fr_lg_mean = self.eec_dose_herp(self.eec_diet, bw_herp_a_lg, wp_herp_a_lg, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_sm_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_sm,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_sm, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_md_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_md,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_md, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.arq_dose_fr_lg_mean = self.arq_dose_herp(self.eec_dose_herp, self.eec_diet, bw_herp_a_lg,
                                                      self.at_bird, avian_ld50, bw_avian_ld50, mineau_scaling_factor,
                                                      wp_herp_a_lg, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)

        self.eec_dose_hm_md_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_hm_lg_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 85, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_hm_md_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_md, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)
        self.arq_dose_hm_lg_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_lg, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm)

        self.eec_dose_im_md_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_md, c_mamm_a, 0.8)
        self.eec_dose_im_lg_mean = self.eec_dose_mamm(self.eec_diet_mamm, self.eec_diet, self.c_0, self.c_t, n_a, i_a,
                                                      a_r, a_i, 7, h_l, self.fi_mamm, bw_herp_a_lg, c_mamm_a, 0.8)
        self.arq_dose_im_md_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_md, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)
        self.arq_dose_im_lg_mean = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet_mamm, self.eec_diet,
                                                      bw_herp_a_lg, self.at_bird, avian_ld50,
                                                      bw_avian_ld50, mineau_scaling_factor, c_mamm_a, 0.8, self.c_0,
                                                      self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm)

        self.eec_dose_tp_md_mean = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                    a_i, 45, h_l, self.fi_herp, bw_herp_a_md, c_herp_a, wp_herp_a_sm,
                                                    wp_herp_a_md)
        self.eec_dose_tp_lg_mean = self.eec_dose_tp(self.eec_diet_tp, self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r,
                                                    a_i, 45, h_l, self.fi_herp, bw_herp_a_lg, c_herp_a, wp_herp_a_sm,
                                                    wp_herp_a_md)
        self.arq_dose_tp_md_mean = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0,
                                                    self.c_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a,
                                                    wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_md,
                                                    bw_avian_ld50, mineau_scaling_factor)
        self.arq_dose_tp_lg_mean = self.arq_dose_tp(self.eec_dose_tp, self.eec_diet_tp, self.eec_diet, self.c_0,
                                                    self.c_t, n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a,
                                                    wp_herp_a_sm, wp_herp_a_md, self.at_bird, avian_ld50, bw_herp_a_lg,
                                                    bw_avian_ld50, mineau_scaling_factor)

        # Table 9
        self.eec_diet_herp_bl_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_arq_herp_bl_mean = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 45, h_l)
        self.eec_diet_herp_fr_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_arq_herp_fr_mean = self.arq_diet_herp(self.eec_diet, avian_lc50, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 7, h_l)
        self.eec_diet_herp_hm_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 85, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_hm_mean = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_im_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_arq_herp_im_mean = self.arq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_lc50, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_tp_mean = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l,
                                                      self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_arq_herp_tp_mean = self.arq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_lc50, self.c_0, self.c_t,
                                                     n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

        # Table 10
        self.eec_diet_herp_bl_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l)
        self.eec_crq_herp_bl_mean = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 45, h_l)
        self.eec_diet_herp_fr_mean = self.eec_diet(self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l)
        self.eec_crq_herp_fr_mean = self.crq_diet_herp(self.eec_diet, avian_noaec, self.c_0, self.c_t, n_a, i_a, a_r,
                                                       a_i, 7, h_l)
        self.eec_diet_herp_hm_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 85, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_hm_mean = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 85, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_im_mean = self.eec_diet_mamm(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 7, h_l,
                                                        self.fi_mamm, c_mamm_a, 0.8)
        self.eec_crq_herp_im_mean = self.crq_diet_mamm(self.eec_diet_mamm, self.eec_diet, avian_noaec, self.c_0,
                                                       self.c_t, n_a, i_a, a_r, a_i, 7, h_l, self.fi_mamm, c_mamm_a,
                                                       0.8)
        self.eec_diet_herp_tp_mean = self.eec_diet_tp(self.eec_diet, self.c_0, self.c_t, n_a, i_a, a_r, a_i, 45, h_l,
                                                      self.fi_herp, c_herp_a, wp_herp_a_sm)
        self.eec_crq_herp_tp_mean = self.crq_diet_tp(self.eec_diet_tp, self.eec_diet, avian_noaec, self.c_0, self.c_t,
                                                     n_a, i_a, a_r, a_i, 45, h_l, self.fi_herp, c_herp_a, wp_herp_a_sm)

