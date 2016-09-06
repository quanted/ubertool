from __future__ import division  #brings in Python 3.0 mixed type calculations
from functools import wraps
import math
import numpy as np
import os.path
import sys
import pandas as pd
import time
from kabam_functions import KabamFunctions
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
        self.log_kow = pd.Series([], dtype='float')
        self.k_oc = pd.Series([], dtype='float')
        self.c_wdp = pd.Series([], dtype='float')
        self.water_column_eec = pd.Series([], dtype='float')
        self.c_wto = pd.Series([], dtype='float')
        self.mineau_scaling_factor = pd.Series([], dtype='float')
        self.conc_poc = pd.Series([], dtype='float')
        self.conc_doc = pd.Series([], dtype='float')
        self.conc_do = pd.Series([], dtype='float')
        self.water_temp = pd.Series([], dtype='float')
        self.conc_ss = pd.Series([], dtype='float')
        self.sediment_oc = pd.Series([], dtype='float')
        self.k_ow = pd.Series([], dtype='float')
        self.Species_of_the_tested_bird = pd.Series([], dtype='object')
        self.bw_quail = pd.Series([], dtype='float')
        self.bw_duck = pd.Series([], dtype='float')
        self.bwb_other = pd.Series([], dtype='float')
            # not sure why this construct is here
            # if Species_of_the_tested_bird == '178':
            #     self.bw_bird = pd.Series([], dtype='float')
            # elif Species_of_the_tested_bird == '1580':
            #     self.bw_bird = pd.Series([], dtype='float')
            # else:
            #     self.bw_bird = pd.Series([], dtype='float')
        self.bw_bird = pd.Series([], dtype='float')
        self.avian_ld50 = pd.Series([], dtype='float')
        self.avian_lc50 = pd.Series([], dtype='float')
        self.avian_noaec = pd.Series([], dtype='float')
        self.m_species = pd.Series([], dtype='float')
        self.bw_rat = pd.Series([], dtype='float')
        self.bw_other_mammal = pd.Series([], dtype='float')
            # not sure why this construct is here
            # if m_species == '350':
            #     self.bw_mamm = pd.Series([], dtype='float')
            # else:
            #     self.bw_mamm = pd.Series([], dtype='float')
        self.bw_mamm = pd.Series([], dtype='float')
        self.mammalian_ld50 = pd.Series([], dtype='float')
        self.mammalian_lc50 = pd.Series([], dtype='float')
        self.mammalian_chronic_endpoint = pd.Series([], dtype='float')
        self.lfish_diet_sediment = pd.Series([], dtype='float')
        self.lfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.lfish_diet_zooplankton = pd.Series([], dtype='float')
        self.lfish_diet_benthic_invertebrates = pd.Series([], dtype='float')
        self.lfish_diet_filter_feeders = pd.Series([], dtype='float')
        self.lfish_diet_small_fish = pd.Series([], dtype='float')
        self.lfish_diet_medium_fish = pd.Series([], dtype='float')
        self.mfish_diet_sediment = pd.Series([], dtype='float')
        self.mfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.mfish_diet_zooplankton = pd.Series([], dtype='float')
        self.mfish_diet_benthic_invertebrates = pd.Series([], dtype='float')
        self.mfish_diet_filter_feeders = pd.Series([], dtype='float')
        self.mfish_diet_small_fish = pd.Series([], dtype='float')
        self.sfish_diet_sediment = pd.Series([], dtype='float')
        self.sfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.sfish_diet_zooplankton = pd.Series([], dtype='float')
        self.sfish_diet_benthic_invertebrates = pd.Series([], dtype='float')
        self.sfish_diet_filter_feeders = pd.Series([], dtype='float')
        self.filterfish_diet_sediment = pd.Series([], dtype='float')
        self.filterfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.filterfish_diet_zooplankton = pd.Series([], dtype='float')
        self.filterfish_diet_benthic_invertebrates = pd.Series([], dtype='float')
        self.beninv_diet_sediment = pd.Series([], dtype='float')
        self.beninv_diet_phytoplankton = pd.Series([], dtype='float')
        self.beninv_diet_zooplankton = pd.Series([], dtype='float')
        self.zoo_diet_sediment = pd.Series([], dtype='float')
        self.zoo_diet_phyto = pd.Series([], dtype='float')
        self.sediment_lipid = pd.Series([], dtype='float')
        self.sediment_nlom = pd.Series([], dtype='float')
        self.sediment_water = pd.Series([], dtype='float')
        self.phytoplankton_lipid = pd.Series([], dtype='float')
        self.phytoplankton_nlom = pd.Series([], dtype='float')
        self.phytoplankton_water = pd.Series([], dtype='float')
        self.zoo_kg = pd.Series([], dtype='float')
        self.zoo_lipid = pd.Series([], dtype='float')
        self.zoo_nlom = pd.Series([], dtype='float')
        self.zoo_water = pd.Series([], dtype='float')
        self.beninv_kg = pd.Series([], dtype='float')
        self.beninv_lipid = pd.Series([], dtype='float')
        self.beninv_nlom = pd.Series([], dtype='float')
        self.beninv_water = pd.Series([], dtype='float')
        self.filterfish_kg = pd.Series([], dtype='float')
        self.filterfish_lipid = pd.Series([], dtype='float')
        self.filterfish_nlom = pd.Series([], dtype='float')
        self.filterfish_water = pd.Series([], dtype='float')
        self.sfish_kg = pd.Series([], dtype='float')
        self.sfish_lipid = pd.Series([], dtype='float')
        self.sfish_nlom = pd.Series([], dtype='float')
        self.sfish_water = pd.Series([], dtype='float')
        self.mfish_kg = pd.Series([], dtype='float')
        self.mfish_lipid = pd.Series([], dtype='float')
        self.mfish_nlom = pd.Series([], dtype='float')
        self.mfish_water = pd.Series([], dtype='float')
        self.lfish_kg = pd.Series([], dtype='float')
        self.lfish_lipid = pd.Series([], dtype='float')
        self.lfish_nlom = pd.Series([], dtype='float')
        self.lfish_water = pd.Series([], dtype='float')
        self.phytoplankton_kg = pd.Series([], dtype='float')
        self.phytoplankton_kd = pd.Series([], dtype='float')
        self.phytoplankton_ke = pd.Series([], dtype='float')
        self.mo_phytoplankton = pd.Series([], dtype='float')
        self.mp_phytoplankton = pd.Series([], dtype='float')
        self.phytoplankton_km = pd.Series([], dtype='float')
        self.zoo_km = pd.Series([], dtype='float')
        self.phytoplankton_k1 = pd.Series([], dtype='float')
        self.phytoplankton_k2 = pd.Series([], dtype='float')
        self.zoo_k1 = pd.Series([], dtype='float')
        self.zoo_k2 = pd.Series([], dtype='float')
        self.zoo_kd = pd.Series([], dtype='float')
        self.zoo_ke = pd.Series([], dtype='float')
        self.beninv_k1 = pd.Series([], dtype='float')
        self.beninv_k2 = pd.Series([], dtype='float')
        self.beninv_kd = pd.Series([], dtype='float')
        self.beninv_ke = pd.Series([], dtype='float')
        self.beninv_km = pd.Series([], dtype='float')
        self.filterfish_k1 = pd.Series([], dtype='float')
        self.filterfish_k2 = pd.Series([], dtype='float')
        self.filterfish_kd = pd.Series([], dtype='float')
        self.filterfish_ke = pd.Series([], dtype='float')
        self.filterfish_km = pd.Series([], dtype='float')
        self.sfish_k1 = pd.Series([], dtype='float')
        self.sfish_k2 = pd.Series([], dtype='float')
        self.sfish_kd = pd.Series([], dtype='float')
        self.sfish_ke = pd.Series([], dtype='float')
        self.sfish_km = pd.Series([], dtype='float')
        self.mfish_k1 = pd.Series([], dtype='float')
        self.mfish_k2 = pd.Series([], dtype='float')
        self.mfish_kd = pd.Series([], dtype='float')
        self.mfish_ke = pd.Series([], dtype='float')
        self.mfish_km = pd.Series([], dtype='float')
        self.lfish_k1 = pd.Series([], dtype='float')
        self.lfish_k2 = pd.Series([], dtype='float')
        self.lfish_kd = pd.Series([], dtype='float')
        self.lfish_ke = pd.Series([], dtype='float')
        self.lfish_km = pd.Series([], dtype='float')
        # self.k_bw_phytoplankton=k_bw_phytoplankton
        # self.k_bw_zoo=k_bw_zoo
        # self.k_bw_beninv=k_bw_beninv
        # self.k_bw_ff=k_bw_ff
        # self.k_bw_sf=k_bw_sf
        # self.k_bw_mf=k_bw_mf
        # self.k_bw_lf=k_bw_lf
        self.rate_constants = pd.Series([], dtype='str')
        self.sediment_repsire = pd.Series([], dtype='float')
        self.phyto_respire = pd.Series([], dtype='float')
        self.zoo_respire = pd.Series([], dtype='float')
        self.beninv_respire = pd.Series([], dtype='float')
        self.filterfish_respire = pd.Series([], dtype='float')
        self.sfish_respire = pd.Series([], dtype='float')
        self.mfish_respire = pd.Series([], dtype='float')
        self.lfish_respire = pd.Series([], dtype='float')

#?? is this the way to reference KabamInputs -- to get access to self.rate_constants
#class KabamOutputs(object, KabamInputs):
class KabamOutputs(object):

    """
    Output class for Kabam.
    """

    def __init__(self):
        """Class representing the outputs for Kabam"""
        super(KabamOutputs, self).__init__()
        # outputs
#??        if self.rate_constants == 'a':
        self.k_bw_phytoplankton_f()
        self.phytoplankton_k1_f()
        self.phytoplankton_k2_f()
        self.ew_zoo_f()
        self.gv_zoo_f()
        self.k_bw_zoo_f()
        self.ed_zoo_f()
        self.gd_zoo_f()
        self.zoo_k1_f()
        self.zoo_k2_f()
        self.zoo_kd_f()
        self.v_nd_zoo_f()
        self.v_wd_zoo_f()
        self.v_ld_zoo_f()
        self.gf_zoo_f()
        self.vlg_zoo_f()
        self.vng_zoo_f()
        self.vwg_zoo_f()
        self.kgb_zoo_f()
        self.zoo_ke_f()

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
        self.beninv_k1_f()
        self.beninv_k2_f()
        self.beninv_kd_f()
        self.beninv_ke_f()

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
        self.filterfish_k1_f()
        self.filterfish_k2_f()
        self.filterfish_kd_f()
        self.filterfish_ke_f()

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
        self.sfish_k1_f()
        self.sfish_k2_f()
        self.sfish_kd_f()
        self.sfish_ke_f()

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
        self.mfish_k1_f()
        self.mfish_k2_f()
        self.mfish_kd_f()
        self.mfish_ke_f()

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
        self.lfish_k1_f()
        self.lfish_k2_f()
        self.lfish_kd_f()
        self.lfish_ke_f()
#??    else:
        self.phytoplankton_k1 = phytoplankton_k1
        self.phytoplankton_k2 = phytoplankton_k2
        self.phytoplankton_kd = phytoplankton_kd
        self.phytoplankton_ke = phytoplankton_ke
        self.phytoplankton_km = phytoplankton_km
        self.zoo_k1 = zoo_k1
        self.zoo_k2 = zoo_k2
        self.zoo_kd = zoo_kd
        self.zoo_ke = zoo_ke
        self.zoo_km = zoo_km
        self.beninv_k1 = beninv_k1
        self.beninv_k2 = beninv_k2
        self.beninv_kd = beninv_kd
        self.beninv_ke = beninv_ke
        self.beninv_km = beninv_km
        self.filterfish_k1 = filterfish_k1
        self.filterfish_k2 = filterfish_k2
        self.filterfish_kd = filterfish_kd
        self.filterfish_ke = filterfish_ke
        self.filterfish_km = filterfish_km
        self.sfish_k1 = sfish_k1
        self.sfish_k2 = sfish_k2
        self.sfish_kd = sfish_kd
        self.sfish_ke = sfish_ke
        self.sfish_km = sfish_km
        self.mfish_k1 = mfish_k1
        self.mfish_k2 = mfish_k2
        self.mfish_kd = mfish_kd
        self.mfish_ke = mfish_ke
        self.mfish_km = mfish_km
        self.lfish_k1 = lfish_k1
        self.lfish_k2 = lfish_k2
        self.lfish_kd = lfish_kd
        self.lfish_ke = lfish_ke
        self.lfish_km = lfish_km


class Kabam(UberModel, KabamInputs, KabamOutputs, KabamFunctions):
    """
    Hydrophobic organic pesticide bioaccumulation in aquatic components of a food web to terrestrial
    exposure in birds and mammals
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Kabam model and containing all its methods"""
        super(Kabam, self).__init__()
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
        # self.phytoplankton_k1_f()
        # self.phytoplankton_k2_f()
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
        # self.zoo_k1_f()
        # self.k_bw_zoo_f()
        # self.zoo_k2_f()
        # self.ed_zoo_f()
        # self.gd_zoo_f()
        # self.zoo_kd_f()
        self.kg_zoo_f()
        # self.v_ld_zoo_f()
        # self.v_nd_zoo_f()
        # self.v_wd_zoo_f()
        # self.gf_zoo_f()
        # self.vlg_zoo_f()
        # self.vng_zoo_f()
        # self.vwg_zoo_f()
        # self.kgb_zoo_f()
        # self.zoo_ke_f()
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
        # self.beninv_k1_f()
        # self.k_bw_beninv_f()
        # # self.beninv_k2_f()
        # self.ed_beninv_f()
        # self.gd_beninv_f()
        # # self.beninv_kd_f()
        self.kg_beninv_f()
        # self.v_ld_beninv_f()
        # self.v_nd_beninv_f()
        # self.v_wd_beninv_f()
        # self.gf_beninv_f()
        # self.vlg_beninv_f()
        # self.vng_beninv_f()
        # self.vwg_beninv_f()
        # self.kgb_beninv_f()
        # self.beninv_ke_f()
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
        # # self.filterfish_k1_f()
        # self.k_bw_ff_f()
        # # self.filterfish_k2_f()
        # self.ed_ff_f()
        # self.gd_ff_f()
        # # self.filterfish_kd_f()
        self.kg_ff_f()
        # self.v_ld_ff_f()
        # self.v_nd_ff_f()
        # self.v_wd_ff_f()
        # self.gf_ff_f()
        # self.vlg_ff_f()
        # self.vng_ff_f()
        # self.vwg_ff_f()
        # self.kgb_ff_f()
        # self.filterfish_ke_f()
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
        # # self.sfish_k1_f()
        # self.k_bw_sf_f()
        # # self.sfish_k2_f()
        # self.ed_sf_f()
        # self.gd_sf_f()
        # # self.sfish_kd_f()
        self.kg_sf_f()
        # self.v_ld_sf_f()
        # self.v_nd_sf_f()
        # self.v_wd_sf_f()
        # self.gf_sf_f()
        # self.vlg_sf_f()
        # self.vng_sf_f()
        # self.vwg_sf_f()
        # self.kgb_sf_f()
        # self.sfish_ke_f()
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
        # # self.mfish_k1_f()
        # self.k_bw_mf_f()
        # # self.mfish_k2_f()
        # self.ed_mf_f()
        # self.gd_mf_f()
        # # self.mfish_kd_f()
        self.kg_mf_f()
        # self.v_ld_mf_f()
        # self.v_nd_mf_f()
        # self.v_wd_mf_f()
        # self.gf_mf_f()
        # self.vlg_mf_f()
        # self.vng_mf_f()
        # self.vwg_mf_f()
        # self.kgb_mf_f()
        # self.mfish_ke_f()
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
        # # self.lfish_k1_f()
        # self.k_bw_lf_f()
        # # self.lfish_k2_f()
        # self.ed_lf_f()
        # self.gd_lf_f()
        # # self.lfish_kd_f()
        self.kg_lf_f()
        # self.v_ld_lf_f()
        # self.v_nd_lf_f()
        # self.v_wd_lf_f()
        # self.gf_lf_f()
        # self.vlg_lf_f()
        # self.vng_lf_f()
        # self.vwg_lf_f()
        # self.kgb_lf_f()
        # self.lfish_ke_f()
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