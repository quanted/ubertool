from __future__ import division  #brings in Python 3.0 mixed type calculations
from functools import wraps
import math
import numpy as np
import os.path
import sys
import pandas as pd
import time
from trex_functions import TRexFunctions
#import logging

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs


class KabamInputs(ModelSharedInputs):
    """
    Required inputs class for Kabam.
    """

    def __init__(self):
        """Class representing the inputs for Kabam"""
        super(KabamInputs, self).__init__()
        #Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.l_kow = pd.Series([], dtype='float')
        self.k_oc = pd.Series([], dtype='float')
        self.c_wdp = pd.Series([], dtype='float')
        self.water_column_EEC = pd.Series([], dtype='float')
        self.c_wto = pd.Series([], dtype='float')
        self.mineau_scaling_factor = pd.Series([], dtype='float')
        self.x_poc = pd.Series([], dtype='float')
        self.x_doc = pd.Series([], dtype='float')
        self.c_ox = pd.Series([], dtype='float')
        self.w_t = pd.Series([], dtype='float')
        self.c_ss = pd.Series([], dtype='float')
        self.oc = pd.Series([], dtype='float')
        self.k_ow = pd.Series([], dtype='float')
        self.Species_of_the_tested_bird = pd.Series([], dtype='object')
        self.bw_quail = pd.Series([], dtype='float')
        self.bw_duck = pd.Series([], dtype='float')
        self.bwb_other = pd.Series([], dtype='float')
        if Species_of_the_tested_bird == '178':
            self.bw_bird = pd.Series([], dtype='float')
        elif Species_of_the_tested_bird == '1580':
            self.bw_bird = pd.Series([], dtype='float')
        else:
            self.bw_bird = pd.Series([], dtype='float')
        self.avian_ld50 = pd.Series([], dtype='float')
        self.avian_lc50 = pd.Series([], dtype='float')
        self.avian_noaec = pd.Series([], dtype='float')
        self.m_species = pd.Series([], dtype='float')
        self.bw_rat = pd.Series([], dtype='float')
        self.bwm_other = pd.Series([], dtype='float')
        if m_species == '350':
            self.bw_mamm = pd.Series([], dtype='float')
        else:
            self.bw_mamm = pd.Series([], dtype='float')
        self.mammalian_ld50 = pd.Series([], dtype='float')
        self.mammalian_lc50 = pd.Series([], dtype='float')
        self.mammalian_chronic_endpoint = pd.Series([], dtype='float')
        self.lf_p_sediment = pd.Series([], dtype='float')
        self.lf_p_phytoplankton = pd.Series([], dtype='float')
        self.lf_p_zooplankton = pd.Series([], dtype='float')
        self.lf_p_benthic_invertebrates = pd.Series([], dtype='float')
        self.lf_p_filter_feeders = pd.Series([], dtype='float')
        self.lf_p_small_fish = pd.Series([], dtype='float')
        self.lf_p_medium_fish = pd.Series([], dtype='float')
        self.mf_p_sediment = pd.Series([], dtype='float')
        self.mf_p_phytoplankton = pd.Series([], dtype='float')
        self.mf_p_zooplankton = pd.Series([], dtype='float')
        self.mf_p_benthic_invertebrates = pd.Series([], dtype='float')
        self.mf_p_filter_feeders = pd.Series([], dtype='float')
        self.mf_p_small_fish = pd.Series([], dtype='float')
        self.sf_p_sediment = pd.Series([], dtype='float')
        self.sf_p_phytoplankton = pd.Series([], dtype='float')
        self.sf_p_zooplankton = pd.Series([], dtype='float')
        self.sf_p_benthic_invertebrates = pd.Series([], dtype='float')
        self.sf_p_filter_feeders = pd.Series([], dtype='float')
        self.ff_p_sediment = pd.Series([], dtype='float')
        self.ff_p_phytoplankton = pd.Series([], dtype='float')
        self.ff_p_zooplankton = pd.Series([], dtype='float')
        self.ff_p_benthic_invertebrates = pd.Series([], dtype='float')
        self.beninv_p_sediment = pd.Series([], dtype='float')
        self.beninv_p_phytoplankton = pd.Series([], dtype='float')
        self.beninv_p_zooplankton = pd.Series([], dtype='float')
        self.zoo_p_sediment = pd.Series([], dtype='float')
        self.zoo_p_phyto = pd.Series([], dtype='float')
        self.s_lipid = pd.Series([], dtype='float')
        self.s_NLOM = pd.Series([], dtype='float')
        self.s_water = pd.Series([], dtype='float')
        self.v_lb_phytoplankton = pd.Series([], dtype='float')
        self.v_nb_phytoplankton = pd.Series([], dtype='float')
        self.v_wb_phytoplankton = pd.Series([], dtype='float')
        self.wb_zoo = pd.Series([], dtype='float')
        self.v_lb_zoo = pd.Series([], dtype='float')
        self.v_nb_zoo = pd.Series([], dtype='float')
        self.v_wb_zoo = pd.Series([], dtype='float')
        self.wb_beninv = pd.Series([], dtype='float')
        self.v_lb_beninv = pd.Series([], dtype='float')
        self.v_nb_beninv = pd.Series([], dtype='float')
        self.v_wb_beninv = pd.Series([], dtype='float')
        self.wb_ff = pd.Series([], dtype='float')
        self.v_lb_ff = pd.Series([], dtype='float')
        self.v_nb_ff = pd.Series([], dtype='float')
        self.v_wb_ff = pd.Series([], dtype='float')
        self.wb_sf = pd.Series([], dtype='float')
        self.v_lb_sf = pd.Series([], dtype='float')
        self.v_nb_sf = pd.Series([], dtype='float')
        self.v_wb_sf = pd.Series([], dtype='float')
        self.wb_mf = pd.Series([], dtype='float')
        self.v_lb_mf = pd.Series([], dtype='float')
        self.v_nb_mf = pd.Series([], dtype='float')
        self.v_wb_mf = pd.Series([], dtype='float')
        self.wb_lf = pd.Series([], dtype='float')
        self.v_lb_lf = pd.Series([], dtype='float')
        self.v_nb_lf = pd.Series([], dtype='float')
        self.v_wb_lf = pd.Series([], dtype='float')
        self.kg_phytoplankton = pd.Series([], dtype='float')
        self.kd_phytoplankton = pd.Series([], dtype='float')
        self.ke_phytoplankton = pd.Series([], dtype='float')
        self.mo_phytoplankton = pd.Series([], dtype='float')
        self.mp_phytoplankton = pd.Series([], dtype='float')
        self.km_phytoplankton = pd.Series([], dtype='float')
        self.km_zoo = pd.Series([], dtype='float')
        self.k1_phytoplankton = pd.Series([], dtype='float')
        self.k2_phytoplankton = pd.Series([], dtype='float')
        self.k1_zoo = pd.Series([], dtype='float')
        self.k2_zoo = pd.Series([], dtype='float')
        self.kd_zoo = pd.Series([], dtype='float')
        self.ke_zoo = pd.Series([], dtype='float')
        self.k1_beninv = pd.Series([], dtype='float')
        self.k2_beninv = pd.Series([], dtype='float')
        self.kd_beninv = pd.Series([], dtype='float')
        self.ke_beninv = pd.Series([], dtype='float')
        self.km_beninv = pd.Series([], dtype='float')
        self.k1_ff = pd.Series([], dtype='float')
        self.k2_ff = pd.Series([], dtype='float')
        self.kd_ff = pd.Series([], dtype='float')
        self.ke_ff = pd.Series([], dtype='float')
        self.km_ff = pd.Series([], dtype='float')
        self.k1_sf = pd.Series([], dtype='float')
        self.k2_sf = pd.Series([], dtype='float')
        self.kd_sf = pd.Series([], dtype='float')
        self.ke_sf = pd.Series([], dtype='float')
        self.km_sf = pd.Series([], dtype='float')
        self.k1_mf = pd.Series([], dtype='float')
        self.k2_mf = pd.Series([], dtype='float')
        self.kd_mf = pd.Series([], dtype='float')
        self.ke_mf = pd.Series([], dtype='float')
        self.km_mf = pd.Series([], dtype='float')
        self.k1_lf = pd.Series([], dtype='float')
        self.k2_lf = pd.Series([], dtype='float')
        self.kd_lf = pd.Series([], dtype='float')
        self.ke_lf = pd.Series([], dtype='float')
        self.km_lf = pd.Series([], dtype='float')
        # self.k_bw_phytoplankton=k_bw_phytoplankton
        # self.k_bw_zoo=k_bw_zoo
        # self.k_bw_beninv=k_bw_beninv
        # self.k_bw_ff=k_bw_ff
        # self.k_bw_sf=k_bw_sf
        # self.k_bw_mf=k_bw_mf
        # self.k_bw_lf=k_bw_lf
        self.rate_constants = pd.Series([], dtype='float')
        self.s_respire = pd.Series([], dtype='float')
        self.phyto_respire = pd.Series([], dtype='float')
        self.zoo_respire = pd.Series([], dtype='float')
        self.beninv_respire = pd.Series([], dtype='float')
        self.ff_respire = pd.Series([], dtype='float')
        self.sfish_respire = pd.Series([], dtype='float')
        self.mfish_respire = pd.Series([], dtype='float')
        self.lfish_respire = pd.Series([], dtype='float')

class KabamOutputs(object):
    """
    Output class for Kabam.
    """

    def __init__(self):
        """Class representing the outputs for Kabam"""
        super(KabamOutputs, self).__init__()
        # outputs
        if self.rate_constants == 'a':
            self.k_bw_phytoplankton_f()
            self.k1_phytoplankton_f()
            self.k2_phytoplankton_f()
            self.ew_zoo_f()
            self.gv_zoo_f()
            self.k_bw_zoo_f()
            self.ed_zoo_f()
            self.gd_zoo_f()
            self.k1_zoo_f()
            self.k2_zoo_f()
            self.kd_zoo_f()
            self.v_nd_zoo_f()
            self.v_wd_zoo_f()
            self.v_ld_zoo_f()
            self.gf_zoo_f()
            self.vlg_zoo_f()
            self.vng_zoo_f()
            self.vwg_zoo_f()
            self.kgb_zoo_f()
            self.ke_zoo_f()

            self.k_bw_beninv_f()
            self.ed_beninv_f()
            self.gd_beninv_f()
            self.kg_beninv_f()
            self.v_ld_beninv_f()
            self.v_nd_beninv_f()
            self.v_wd_beninv_f()
            self.gf_beninv_f()
            self.vlg_beninv_f()
            self.vng_beninv_f()
            self.vwg_beninv_f()
            self.kgb_beninv_f()
            self.ew_beninv_f()
            self.gv_beninv_f()
            self.k1_beninv_f()
            self.k2_beninv_f()
            self.kd_beninv_f()
            self.ke_beninv_f()

            self.gv_ff_f()
            self.ew_ff_f()
            self.k_bw_ff_f()
            self.ed_ff_f()
            self.gd_ff_f()
            self.kg_ff_f()
            self.v_ld_ff_f()
            self.v_nd_ff_f()
            self.v_wd_ff_f()
            self.gf_ff_f()
            self.vlg_ff_f()
            self.vng_ff_f()
            self.vwg_ff_f()
            self.kgb_ff_f()
            self.k1_ff_f()
            self.k2_ff_f()
            self.kd_ff_f()
            self.ke_ff_f()

            self.gv_sf_f()
            self.ew_sf_f()
            self.k_bw_sf_f()
            self.ed_sf_f()
            self.gd_sf_f()
            self.kg_sf_f()
            self.v_ld_sf_f()
            self.v_nd_sf_f()
            self.v_wd_sf_f()
            self.gf_sf_f()
            self.vlg_sf_f()
            self.vng_sf_f()
            self.vwg_sf_f()
            self.kgb_sf_f()
            self.k1_sf_f()
            self.k2_sf_f()
            self.kd_sf_f()
            self.ke_sf_f()

            self.gv_mf_f()
            self.ew_mf_f()
            self.k_bw_mf_f()
            self.ed_mf_f()
            self.gd_mf_f()
            self.kg_mf_f()
            self.v_ld_mf_f()
            self.v_nd_mf_f()
            self.v_wd_mf_f()
            self.gf_mf_f()
            self.vlg_mf_f()
            self.vng_mf_f()
            self.vwg_mf_f()
            self.kgb_mf_f()
            self.k1_mf_f()
            self.k2_mf_f()
            self.kd_mf_f()
            self.ke_mf_f()

            self.gv_lf_f()
            self.ew_lf_f()
            self.k_bw_lf_f()
            self.ed_lf_f()
            self.gd_lf_f()
            self.kg_lf_f()
            self.v_ld_lf_f()
            self.v_nd_lf_f()
            self.v_wd_lf_f()
            self.gf_lf_f()
            self.vlg_lf_f()
            self.vng_lf_f()
            self.vwg_lf_f()
            self.kgb_lf_f()
            self.k1_lf_f()
            self.k2_lf_f()
            self.kd_lf_f()
            self.ke_lf_f()
        else:
            self.k1_phytoplankton = k1_phytoplankton
            self.k2_phytoplankton = k2_phytoplankton
            self.kd_phytoplankton = kd_phytoplankton
            self.ke_phytoplankton = ke_phytoplankton
            self.km_phytoplankton = km_phytoplankton
            self.k1_zoo = k1_zoo
            self.k2_zoo = k2_zoo
            self.kd_zoo = kd_zoo
            self.ke_zoo = ke_zoo
            self.km_zoo = km_zoo
            self.k1_beninv = k1_beninv
            self.k2_beninv = k2_beninv
            self.kd_beninv = kd_beninv
            self.ke_beninv = ke_beninv
            self.km_beninv = km_beninv
            self.k1_ff = k1_ff
            self.k2_ff = k2_ff
            self.kd_ff = kd_ff
            self.ke_ff = ke_ff
            self.km_ff = km_ff
            self.k1_sf = k1_sf
            self.k2_sf = k2_sf
            self.kd_sf = kd_sf
            self.ke_sf = ke_sf
            self.km_sf = km_sf
            self.k1_mf = k1_mf
            self.k2_mf = k2_mf
            self.kd_mf = kd_mf
            self.ke_mf = ke_mf
            self.km_mf = km_mf
            self.k1_lf = k1_lf
            self.k2_lf = k2_lf
            self.kd_lf = kd_lf
            self.ke_lf = ke_lf
            self.km_lf = km_lf


class Kabam(UberModel, KabamInputs, KabamOutputs, KabamFunctions):
    """
    Hydrophobic organic pesticide bioaccumulation in aquatic components of a food web to terrestrial
    exposure in birds and mammals
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Kabam model and containing all its methods"""
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
        """
        Execute all subroutines in proper order.
        :return:
        """
        self.phi_f()
        self.c_soc_f()
        self.c_s_f()
        self.sed_om_f()
        self.water_d()
        # self.k_bw_phytoplankton_f()
        # self.k1_phytoplankton_f()
        # self.k2_phytoplankton_f()
        self.cb_phytoplankton_f()
        self.cbl_phytoplankton_f()
        self.cbf_phytoplankton_f()
        self.cbr_phytoplankton_f()
        self.cbfl_phytoplankton_f()
        self.cbaf_phytoplankton_f()
        self.cbafl_phytoplankton_f()
        self.cbsafl_phytoplankton_f()
        # self.gv_zoo_f()
        # self.ew_zoo_f()
        # self.k1_zoo_f()
        # self.k_bw_zoo_f()
        # self.k2_zoo_f()
        # self.ed_zoo_f()
        # self.gd_zoo_f()
        # self.kd_zoo_f()
        self.kg_zoo_f()
        # self.v_ld_zoo_f()
        # self.v_nd_zoo_f()
        # self.v_wd_zoo_f()
        # self.gf_zoo_f()
        # self.vlg_zoo_f()
        # self.vng_zoo_f()
        # self.vwg_zoo_f()
        # self.kgb_zoo_f()
        # self.ke_zoo_f()
        self.diet_zoo_f()
        self.cb_zoo_f()
        self.cbl_zoo_f()
        self.cbd_zoo_f()
        self.cbr_zoo_f()
        self.cbf_zoo_f()
        self.cbfl_zoo_f()
        self.cbaf_zoo_f()
        self.cbafl_zoo_f()
        self.cbsafl_zoo_f()
        self.bmf_zoo_f()
        # self.gv_beninv_f()
        # self.ew_beninv_f()
        # self.k1_beninv_f()
        # self.k_bw_beninv_f()
        # # self.k2_beninv_f()
        # self.ed_beninv_f()
        # self.gd_beninv_f()
        # # self.kd_beninv_f()
        self.kg_beninv_f()
        # self.v_ld_beninv_f()
        # self.v_nd_beninv_f()
        # self.v_wd_beninv_f()
        # self.gf_beninv_f()
        # self.vlg_beninv_f()
        # self.vng_beninv_f()
        # self.vwg_beninv_f()
        # self.kgb_beninv_f()
        # self.ke_beninv_f()
        self.diet_beninv_f()
        self.cb_beninv_f()
        self.cbl_beninv_f()
        self.cbd_beninv_f()
        self.cbr_beninv_f()
        self.cbf_beninv_f()
        self.cbfl_beninv_f()
        self.cbaf_beninv_f()
        self.cbafl_beninv_f()
        self.cbsafl_beninv_f()
        self.bmf_beninv_f()
        # self.gv_ff_f()
        # self.ew_ff_f()
        # # self.k1_ff_f()
        # self.k_bw_ff_f()
        # # self.k2_ff_f()
        # self.ed_ff_f()
        # self.gd_ff_f()
        # # self.kd_ff_f()
        self.kg_ff_f()
        # self.v_ld_ff_f()
        # self.v_nd_ff_f()
        # self.v_wd_ff_f()
        # self.gf_ff_f()
        # self.vlg_ff_f()
        # self.vng_ff_f()
        # self.vwg_ff_f()
        # self.kgb_ff_f()
        # self.ke_ff_f()
        self.diet_ff_f()
        self.cb_ff_f()
        self.cbl_ff_f()
        self.cbd_ff_f()
        self.cbr_ff_f()
        self.cbf_ff_f()
        self.cbfl_ff_f()
        self.cbaf_ff_f()
        self.cbafl_ff_f()
        self.cbsafl_ff_f()
        self.bmf_ff_f()
        # self.gv_sf_f()
        # self.ew_sf_f()
        # # self.k1_sf_f()
        # self.k_bw_sf_f()
        # # self.k2_sf_f()
        # self.ed_sf_f()
        # self.gd_sf_f()
        # # self.kd_sf_f()
        self.kg_sf_f()
        # self.v_ld_sf_f()
        # self.v_nd_sf_f()
        # self.v_wd_sf_f()
        # self.gf_sf_f()
        # self.vlg_sf_f()
        # self.vng_sf_f()
        # self.vwg_sf_f()
        # self.kgb_sf_f()
        # self.ke_sf_f()
        self.diet_sf_f()
        self.cb_sf_f()
        self.cbl_sf_f()
        self.cbd_sf_f()
        self.cbr_sf_f()
        self.cbf_sf_f()
        self.cbfl_sf_f()
        self.cbaf_sf_f()
        self.cbafl_sf_f()
        self.cbsafl_sf_f()
        self.bmf_sf_f()
        # self.gv_mf_f()
        # self.ew_mf_f()
        # # self.k1_mf_f()
        # self.k_bw_mf_f()
        # # self.k2_mf_f()
        # self.ed_mf_f()
        # self.gd_mf_f()
        # # self.kd_mf_f()
        self.kg_mf_f()
        # self.v_ld_mf_f()
        # self.v_nd_mf_f()
        # self.v_wd_mf_f()
        # self.gf_mf_f()
        # self.vlg_mf_f()
        # self.vng_mf_f()
        # self.vwg_mf_f()
        # self.kgb_mf_f()
        # self.ke_mf_f()
        self.diet_mf_f()
        self.cb_mf_f()
        self.cbl_mf_f()
        self.cbd_mf_f()
        self.cbr_mf_f()
        self.cbf_mf_f()
        self.cbfl_mf_f()
        self.cbaf_mf_f()
        self.cbafl_mf_f()
        self.cbsafl_mf_f()
        self.cbmf_mf_f()
        # self.gv_lf_f()
        # self.ew_lf_f()
        # # self.k1_lf_f()
        # self.k_bw_lf_f()
        # # self.k2_lf_f()
        # self.ed_lf_f()
        # self.gd_lf_f()
        # # self.kd_lf_f()
        self.kg_lf_f()
        # self.v_ld_lf_f()
        # self.v_nd_lf_f()
        # self.v_wd_lf_f()
        # self.gf_lf_f()
        # self.vlg_lf_f()
        # self.vng_lf_f()
        # self.vwg_lf_f()
        # self.kgb_lf_f()
        # self.ke_lf_f()
        self.diet_lf_f()
        self.cb_lf_f()
        self.cbl_lf_f()
        self.cbd_lf_f()
        self.cbr_lf_f()
        self.cbf_lf_f()
        self.cbfl_lf_f()
        self.cbaf_lf_f()
        self.cbafl_lf_f()
        self.cbsafl_lf_f()
        self.cbmf_lf_f()
        self.mweight_f()
        self.dfir_f()
        self.wet_food_ingestion_m_f()
        self.drinking_water_intake_m_f()
        self.db4_f()
        self.db5_f()
        self.aweight_f()
        self.dfir_a_f()
        self.wet_food_ingestion_a_f()
        self.drinking_water_intake_a_f()
        self.db4a_f()
        self.db5a_f()
        self.acute_dose_based_m_f()
        self.chronic_dose_based_m_f()
        self.acute_dose_based_a_f()
        self.acute_rq_dose_m_f()
        self.chronic_rq_dose_m_f()
        self.acute_rq_diet_m_f()
        self.chronic_rq_diet_m_f()
        self.acute_rq_dose_a_f()
        self.acute_rq_diet_a_f()
        self.chronic_rq_diet_a_f()