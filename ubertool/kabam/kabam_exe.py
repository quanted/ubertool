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
        self.pore_water_eec = pd.Series([], dtype='float')
        self.water_column_eec = pd.Series([], dtype='float')
#        self.c_wto = pd.Series([], dtype='float')  # replaced by 'self.water_column_eec' above; chk this one more time
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
        self.lfish_diet_beninv = pd.Series([], dtype='float')
        self.lfish_diet_filter_feeders = pd.Series([], dtype='float')
        self.lfish_diet_small_fish = pd.Series([], dtype='float')
        self.lfish_diet_medium_fish = pd.Series([], dtype='float')
        self.mfish_diet_sediment = pd.Series([], dtype='float')
        self.mfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.mfish_diet_zooplankton = pd.Series([], dtype='float')
        self.mfish_diet_beninv = pd.Series([], dtype='float')
        self.mfish_diet_filter_feeders = pd.Series([], dtype='float')
        self.mfish_diet_small_fish = pd.Series([], dtype='float')
        self.sfish_diet_sediment = pd.Series([], dtype='float')
        self.sfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.sfish_diet_zooplankton = pd.Series([], dtype='float')
        self.sfish_diet_beninv = pd.Series([], dtype='float')
        self.sfish_diet_filter_feeders = pd.Series([], dtype='float')
        self.filterfeeders_diet_sediment = pd.Series([], dtype='float')
        self.filterfeeders_diet_phytoplankton = pd.Series([], dtype='float')
        self.filterfeeders_diet_zooplankton = pd.Series([], dtype='float')
        self.filterfeeders_diet_beninv = pd.Series([], dtype='float')
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
        self.zoo_wb = pd.Series([], dtype='float')
        self.zoo_lipid = pd.Series([], dtype='float')
        self.zoo_nlom = pd.Series([], dtype='float')
        self.zoo_water = pd.Series([], dtype='float')
        self.beninv_wb = pd.Series([], dtype='float')
        self.beninv_lipid = pd.Series([], dtype='float')
        self.beninv_nlom = pd.Series([], dtype='float')
        self.beninv_water = pd.Series([], dtype='float')
        self.filterfeeders_wb = pd.Series([], dtype='float')
        self.filterfeeders_lipid = pd.Series([], dtype='float')
        self.filterfeeders_nlom = pd.Series([], dtype='float')
        self.filterfeeders_water = pd.Series([], dtype='float')
        self.sfish_wb = pd.Series([], dtype='float')
        self.sfish_lipid = pd.Series([], dtype='float')
        self.sfish_nlom = pd.Series([], dtype='float')
        self.sfish_water = pd.Series([], dtype='float')
        self.mfish_wb = pd.Series([], dtype='float')
        self.mfish_lipid = pd.Series([], dtype='float')
        self.mfish_nlom = pd.Series([], dtype='float')
        self.mfish_water = pd.Series([], dtype='float')
        self.lfish_wb = pd.Series([], dtype='float')
        self.lfish_lipid = pd.Series([], dtype='float')
        self.lfish_nlom = pd.Series([], dtype='float')
        self.lfish_water = pd.Series([], dtype='float')
        self.phytoplankton_kg = pd.Series([], dtype='float')
        self.phytoplankton_kd = pd.Series([], dtype='float')
        self.phytoplankton_ke = pd.Series([], dtype='float')
        self.phytoplankton_mo = pd.Series([], dtype='float')
        self.phytoplankton_mp = pd.Series([], dtype='float')
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
        self.filterfeeders_k1 = pd.Series([], dtype='float')
        self.filterfeeders_k2 = pd.Series([], dtype='float')
        self.filterfeeders_kd = pd.Series([], dtype='float')
        self.filterfeeders_ke = pd.Series([], dtype='float')
        self.filterfeeders_km = pd.Series([], dtype='float')
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
        self.filterfeeders_respire = pd.Series([], dtype='float')
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

        self.out_cb_phytoplankton = pd.Series([], dtype = 'float', name="out_cb_phytoplankton")

# #??        if self.rate_constants == 'a':
#         self.k_bw_phytoplankton_f()
#         self.phytoplankton_k1_f()
#         self.phytoplankton_k2_f()
#         self.ew_zoo_f()
#         self.gv_zoo_f()
#         self.k_bw_zoo_f()
#         self.ed_zoo_f()
#         self.gd_zoo_f()
#         self.zoo_k1_f()
#         self.zoo_k2_f()
#         self.zoo_kd_f()
#         self.v_nd_zoo_f()
#         self.v_wd_zoo_f()
#         self.v_ld_zoo_f()
#         self.gf_zoo_f()
#         self.vlg_zoo_f()
#         self.vng_zoo_f()
#         self.vwg_zoo_f()
#         self.kgb_zoo_f()
#         self.zoo_ke_f()
#
#         self.k_bw_beninv_f()
#         self.ed_beninv_f()
#         self.gd_beninv_f()
#         self.kg_beninv_f()
#         self.v_ld_beninv_f()
#         self.v_nd_beninv_f()
#         self.v_wd_beninv_f()
#         self.gf_beninv_f()
#         self.vlg_beninv_f()
#         self.vng_beninv_f()
#         self.vwg_beninv_f()
#         self.kgb_beninv_f()
#         self.ew_beninv_f()
#         self.gv_beninv_f()
#         self.beninv_k1_f()
#         self.beninv_k2_f()
#         self.beninv_kd_f()
#         self.beninv_ke_f()
#
#         self.gv_ff_f()
#         self.ew_ff_f()
#         self.k_bw_ff_f()
#         self.ed_ff_f()
#         self.gd_ff_f()
#         self.kg_ff_f()
#         self.v_ld_ff_f()
#         self.v_nd_ff_f()
#         self.v_wd_ff_f()
#         self.gf_ff_f()
#         self.vlg_ff_f()
#         self.vng_ff_f()
#         self.vwg_ff_f()
#         self.kgb_ff_f()
#         self.filterfeeders_k1_f()
#         self.filterfeeders_k2_f()
#         self.filterfeeders_kd_f()
#         self.filterfeeders_ke_f()
#
#         self.gv_sf_f()
#         self.ew_sf_f()
#         self.k_bw_sf_f()
#         self.ed_sf_f()
#         self.gd_sf_f()
#         self.kg_sf_f()
#         self.v_ld_sf_f()
#         self.v_nd_sf_f()
#         self.v_wd_sf_f()
#         self.gf_sf_f()
#         self.vlg_sf_f()
#         self.vng_sf_f()
#         self.vwg_sf_f()
#         self.kgb_sf_f()
#         self.sfish_k1_f()
#         self.sfish_k2_f()
#         self.sfish_kd_f()
#         self.sfish_ke_f()
#
#         self.gv_mf_f()
#         self.ew_mf_f()
#         self.k_bw_mf_f()
#         self.ed_mf_f()
#         self.gd_mf_f()
#         self.kg_mf_f()
#         self.v_ld_mf_f()
#         self.v_nd_mf_f()
#         self.v_wd_mf_f()
#         self.gf_mf_f()
#         self.vlg_mf_f()
#         self.vng_mf_f()
#         self.vwg_mf_f()
#         self.kgb_mf_f()
#         self.mfish_k1_f()
#         self.mfish_k2_f()
#         self.mfish_kd_f()
#         self.mfish_ke_f()
#
#         self.gv_lf_f()
#         self.ew_lf_f()
#         self.k_bw_lf_f()
#         self.ed_lf_f()
#         self.gd_lf_f()
#         self.kg_lf_f()
#         self.v_ld_lf_f()
#         self.v_nd_lf_f()
#         self.v_wd_lf_f()
#         self.gf_lf_f()
#         self.vlg_lf_f()
#         self.vng_lf_f()
#         self.vwg_lf_f()
#         self.kgb_lf_f()
#         self.lfish_k1_f()
#         self.lfish_k2_f()
#         self.lfish_kd_f()
#         self.lfish_ke_f()
# #??    else:
#         # self.phytoplankton_k1 = phytoplankton_k1
#         # self.phytoplankton_k2 = phytoplankton_k2
#         # self.phytoplankton_kd = phytoplankton_kd
#         # self.phytoplankton_ke = phytoplankton_ke
#         # self.phytoplankton_km = phytoplankton_km
#         # self.zoo_k1 = zoo_k1
#         # self.zoo_k2 = zoo_k2
#         # self.zoo_kd = zoo_kd
#         # self.zoo_ke = zoo_ke
#         # self.zoo_km = zoo_km
#         # self.beninv_k1 = beninv_k1
#         # self.beninv_k2 = beninv_k2
#         # self.beninv_kd = beninv_kd
#         # self.beninv_ke = beninv_ke
#         # self.beninv_km = beninv_km
#         # self.filterfeeders_k1 = filterfeeders_k1
#         # self.filterfeeders_k2 = filterfeeders_k2
#         # self.filterfeeders_kd = filterfeeders_kd
#         # self.filterfeeders_ke = filterfeeders_ke
#         # self.filterfeeders_km = filterfeeders_km
#         # self.sfish_k1 = sfish_k1
#         # self.sfish_k2 = sfish_k2
#         # self.sfish_kd = sfish_kd
#         # self.sfish_ke = sfish_ke
#         # self.sfish_km = sfish_km
#         # self.mfish_k1 = mfish_k1
#         # self.mfish_k2 = mfish_k2
#         # self.mfish_kd = mfish_kd
#         # self.mfish_ke = mfish_ke
#         # self.mfish_km = mfish_km
#         # self.lfish_k1 = lfish_k1
#         # self.lfish_k2 = lfish_k2
#         # self.lfish_kd = lfish_kd
#         # self.lfish_ke = lfish_ke
#         # self.lfish_km = lfish_km


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

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()

        self.phytoplankton_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.phytoplankton_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.phytoplankton_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.phytoplankton_lipid_frac = self.percent_to_frac(self.phytoplankton_lipid)
        self.phytoplankton_nlom_frac = self.percent_to_frac(self.phytoplankton_nlom)
        self.phytoplankton_water_frac = self.percent_to_frac(self.phytoplankton_water)


        self.zoo_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.zoo_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.zoo_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.zoo_lipid_frac = self.percent_to_frac(self.zoo_lipid)
        self.zoo_nlom_frac = self.percent_to_frac(self.zoo_nlom)
        self.zoo_water_frac = self.percent_to_frac(self.zoo_water)


        self.beninv_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.beninv_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.beninv_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.beninv_lipid_frac = self.percent_to_frac(self.beninv_lipid)
        self.beninv_nlom_frac = self.percent_to_frac(self.beninv_nlom)
        self.beninv_water_frac = self.percent_to_frac(self.water_lipid)


        self.filterfeeders_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.filterfeeders_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.filterfeeders_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.filterfeeders_lipid_frac = self.percent_to_frac(self.filterfeeders_lipid)
        self.filterfeeders_nlom_frac = self.percent_to_frac(self.filterfeeders_nlom)
        self.filterfeeders_water_frac = self.percent_to_frac(self.water_lipid)


        self.sfish_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.sfish_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.sfish_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.sfish_lipid_frac = self.percent_to_frac(self.sfish_lipid)
        self.sfish_nlom_frac = self.percent_to_frac(self.sfish_nlom)
        self.sfish_water_frac = self.percent_to_frac(self.sfish_water)


        self.mfish_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.mfish_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.mfish_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.mfish_lipid_frac = self.percent_to_frac(self.mfish_lipid)
        self.mfish_nlom_frac = self.percent_to_frac(self.mfish_nlom)
        self.mfish_water_frac = self.percent_to_frac(self.mfish_water)


        self.lfish_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.lfish_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.lfish_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.lfish_lipid_frac = self.percent_to_frac(self.lfish_lipid)
        self.lfish_nlom_frac = self.percent_to_frac(self.lfish_nlom)
        self.lfish_water_frac = self.percent_to_frac(self.lfish_water)

        # aquatic animal ventilation rates (Kabam Eq. A5.2b)
        self.gv_zoo = self.ventilation_rate(self.zoo_wb)
        self.gv_beninv = self.ventilation_rate(self.beninv_wb)
        self.gv_filterfeeders = self.ventilation_rate(self.filterfedders_wb)
        self.gv_sfish = self.ventilation_rate(self.sfish_wb)
        self.gv_mfish = self.ventilation_rate(self.mfish_wb)
        self.gv_lfish = self.ventilation_rate(self.lfish_wb)

        # Pesticide uptake efficiency by gills of aquatic animals (Kabam Eq. A5.2a)
        self.ew_aq_animals = self.pest_uptake_eff_gills()
        self.ew_zoo = self.ew_beninv = self.ew_filterfeeders = self.ew_sfish = \
                      self.ew_mfish = self.ew_lfish = self.ew_zoo = self.ew_aq_animals

        # aquatic animal respitory area uptake rate constant (Kabam Ea. A5.1 & A5.2
        self.phytoplankton_k1 = self.phytoplankton_k1_calc()
        self.zoo_k1 = self.aq_animal_k1_calc(self.ew_zoo, self.gv_zoo, self.zoo_wb)
        self.beninv_k1 = self.aq_animal_k1_calc(self.ew_beninv, self.gv_beninv, self.beninv_wb)
        self.filterfedders_k1 = self.aq_animal_k1_calc(self.ew_filterfedders, self.gv_filterfedders, self.filterfedders_wb)
        self.sfish_k1 = self.aq_animal_k1_calc(self.ew_sfish, self.gv_sfish, self.sfish_wb)
        self.mfish_k1 = self.aq_animal_k1_calc(self.ew_mfish, self.gv_mfish, self.mfish_wb)
        self.lfish_k1 = self.aq_animal_k1_calc(self.ew_lfish, self.gv_lfish, self.lfish_wb)

        #Aquatic animal-Water partition coeficient (Kabam Eq. A6a)
        # beta_* represent the proportionality constant expressing the sorption capacity of NLOM to that of octanol
        self.k_bw_phytoplankton = self.animal_water_part_coef(self.phytoplankton_lipid_frac,
                                                              self.phytoplankton_nlom_frac,
                                                              self.phytoplankton_water_frac, self.beta_phyto)
        self.k_bw_zoo = self.animal_water_part_coef(self.zoo_lipid_frac, self.zoo_nlom_frac,
                                                    self.zoo_water_frac, self.beta_aq_animals)
        self.k_bw_beninv = self.animal_water_part_coef(self.beninv_lipid_frac, self.beninv_nlom_frac,
                                                       self.beninv_water_frac, self.beta_aq_animals)
        self.k_bw_filterfeeders = self.animal_water_part_coef(self.filterfeeders_lipid_frac, self.filterfeeders_nlom_frac,
                                                              self.filterfeeders_water_frac, self.beta_aq_animals)
        self.k_bw_sfish = self.animal_water_part_coef(self.sfish_lipid_frac, self.sfish_nlom_frac,
                                                      self.sfish_water_frac, self.beta_aq_animals)
        self.k_bw_mfish = self.animal_water_part_coef(self.mfish_lipid_frac, self.mfish_nlom_frac,
                                                      self.mfish_water_frac, self.beta_aq_animals)
        self.k_bw_lfish = self.animal_water_part_coef(self.lfish_lipid_frac, self.lfish_nlom_frac,
                                                      self.lfish_water_frac, self.beta_aq_animals)

        # Pesticide uptake rate constant for chemical uptake through respiratory area
        self.phytoplankton_k2 = self.aq_animal_k2_calc(self.phytoplankton_k1, self.k_bw_phytoplankton)
        self.zoo_k2 = self.aq_animal_k2_calc(self.zoo_k1, self.k_bw_zoo)
        self.beninv_k2 = self.aq_animal_k2_calc(self.beninv_k1, self.k_bw_beninv)
        self.filterfeeders_k2 = self.aq_animal_k2_calc(self.filterfeeders_k1, self.k_bw_filterfeeders)
        self.sfish_k2 = self.aq_animal_k2_calc(self.sfish_k1, self.k_bw_sfish)
        self.mfish_k2 = self.aq_animal_k2_calc(self.mfish_k1, self.k_bw_mfish)
        self.lfish_k2 = self.aq_animal_k2_calc(self.lfish_k1, self.k_bw_lfish)

        # aquatic animal/organism growth rate constants
        self.kg_phytoplankton = 0.1 # check this; 0.1 is assigned in OPP model spreadsheet
#??                                    # in worksheet 'Parameters & Calculations' cell C48
        self.kg_zoo = self.animal_grow_rate_const(self.zoo_wb)
        self.kg_beninv = self.animal_grow_rate_const(self.beninv_wb)
        self.kg_filterfeeders = self.animal_grow_rate_const(self.filterfeeders_wb)
        self.kg_sfish = self.animal_grow_rate_const(self.sfish_wb)
        self.kg_mfish = self.animal_grow_rate_const(self.mfish_wb)
        self.kg_lfish = self.animal_grow_rate_const(self.lfish_wb)

        # aquatic animal/organism dietary pesticide transfer efficiency
        # i think the following declarations should be moved to output class
        self.ed_zoo = pd.Series([], dtype = 'float')
        self.ed_beninv = pd.Series([], dtype = 'float')
        self.ed_filterfeeders = pd.Series([], dtype = 'float')
        self.ed_sfish = pd.Series([], dtype = 'float')
        self.ed_mfish = pd.Series([], dtype = 'float')
        self.ed_lfish = pd.Series([], dtype = 'float')

        self.ed_zoo = self.ed_beninv = self.ed_filterfeeders = self.ed_sfish = \
                      self.ed_mfish = self.ed_lfish = self.dietary_trans_eff()

        # aquatic animal/organism feeding rate
        self.gd_zoo = self.aq_animal_feeding_rate(self, self.zoo_wb)
        self.gd_beninv = self.aq_animal_feeding_rate(self, self.beninv_wb)
        self.gd_filterfeeders = self.filterfeeder_feeding_rate()
        self.gd_sfish = self.aq_animal_feeding_rate(self, self.sfish_wb)
        self.gd_mfish = self.aq_animal_feeding_rate(self, self.mfish_wb)
        self.gd_lfish = self.aq_animal_feeding_rate(self, self.lfish_wb)

        # dietary uptake rate constant
        self.zoo_kd = self.diet_uptake_rate_const(self.ed_zoo, self.gd_zoo, self.zoo_wb)
        self.beninv_kd = self.diet_uptake_rate_const(self.ed_beninv, self.gd_beninv, self.beninv_wb)
        self.filterfeeders_kd = self.diet_uptake_rate_const(self.ed_filterfeeders,
                                                            self.gd_filterfeeders, self.filterfeeders_wb)
        self.sfish_kd = self.diet_uptake_rate_const(self.ed_sfish, self.gd_sfish, self.sfish_wb)
        self.mfish_kd = self.diet_uptake_rate_const(self.ed_mfish, self.gd_mfish, self.mfish_wb)
        self.lfish_kd = self.diet_uptake_rate_const(self.ed_lfish, self.gd_lfish, self.lfish_wb)

        #overall lipid, NLOM, and Water content of aquatic animal/organism diet
            #loops reflect stepping through model simulation runs one at a time
            #notes: 1. there is some room here for reduction of code; the 'diet_content_*_*' variable
            #          could be reduced to a single set that is used for each trophic level
            #       2. for future consideration: this processing might be optimized with matrix based calculations
        #zooplankton lipid content of diet
        self.diet_frac_zoo = pd.Series([], dtype = 'float')
        self.diet_content_zoo_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.zoo_diet_sediment)):
            self.diet_frac_zoo = [self.kabam_empty.zoo_diet_sediment[i],
                             self.kabam_empty.zoo_diet_phytoplankton[i]]
            self.diet_content_zoo_lipid = [self.kabam_empty.sediment_lipid[i],
                             self.kabam_empty.phytoplankton_lipid[i]]
        self.v_ld_zoo = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_lipid)

        #zooplankton NLOM content of diet
        self.diet_content_zoo_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.zoo_diet_sediment)):
            self.diet_content_zoo_nlom = [self.kabam_empty.sediment_nlom[i],
                             self.kabam_empty.phytoplankton_nlom[i]]
        self.v_nd_zoo = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_nlom)

        #zooplankton water content of diet
        self.diet_content_beninv_water = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.zoo_diet_sediment)):
            self.diet_content_zoo_water = [self.kabam_empty.sediment_water[i],
                             self.kabam_empty.phytoplankton_water[i]]
        self.v_wd_zoo = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_water)

        #benthic invertebrates lipid content of diet
        self.diet_frac_beninv = pd.Series([], dtype = 'float')
        self.diet_content_beninv_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.beninv_diet_sediment)):
            self.diet_frac_beninv = [self.kabam_empty.beninv_diet_sediment[i],
                             self.kabam_empty.beninv_diet_phytoplankton[i],
                             self.kabam_empty.beninv_diet_zooplankton[i]]
            self.diet_content_beninv_lipid = [self.kabam_empty.sediment_lipid[i],
                             self.kabam_empty.phytoplankton_lipid[i],
                             self.kabam_empty.zooplankton_lipid[i]]
        self.v_ld_beninv = self.overall_diet_content(self.diet_frac_beninv, self.diet_content_beninv_lipid)

        #benthic invertebrates NLOM content of diet
        self.diet_content_beninv_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.beninv_diet_sediment)):
            self.diet_content_beninv_nlom = [self.kabam_empty.sediment_nlom[i],
                             self.kabam_empty.phytoplankton_nlom[i],
                             self.kabam_empty.zooplankton_nlom[i]]
        self.v_nd_beninv = self.overall_diet_content(self.diet_frac_beninv, self.diet_content_beninv_nlom)

        #benthic invertebrates water content of diet
        self.diet_content_beninv_water = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.beninv_diet_sediment)):
            self.diet_content_beninv_water = [self.kabam_empty.sediment_water[i],
                             self.kabam_empty.phytoplankton_water[i],
                             self.kabam_empty.zooplankton_water[i]]
        self.v_wd_beninv = self.overall_diet_content(self.diet_frac_beninv, self.diet_content_beninv_water)

        #filterfeeders lipid content of diet
        self.diet_frac_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_content_filterfeeders_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.filterfeeders_diet_sediment)):
           diet_frac_zoo = [self.kabam_empty.filterfeeders_diet_sediment[i],
                             self.kabam_empty.filterfeeders_diet_phytoplankton[i],
                             self.kabam_empty.filterfeeders_diet_zooplankton[i],
                             self.kabam_empty.filterfeeders_diet_beninv[i]]
        self.diet_content_filterfeeders_lipid = [self.kabam_empty.sediment_lipid[i],
                             self.kabam_empty.phytoplankton_lipid[i],
                             self.kabam_empty.zoo_lipid[i],
                             self.kabam_empty.beninv_lipid[i]]
        self.v_ld_filterfeeders = self.overall_diet_content(self.diet_frac_filterfeeders,
                                                            self.diet_content_filterfeeders_lipid)

        #filterfeeders NLOM content of diet
        self.diet_content_filterfeeders_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.filterfeeders_diet_sediment)):
            self.diet_content_filterfeeders_nlom = [self.kabam_empty.sediment_nlom[i],
                             self.kabam_empty.phytoplankton_nlom[i],
                             self.kabam_empty.zoo_nlom[i],
                             self.kabam_empty.beninv_nlom[i]]
        self.v_nd_filterfeeders = self.overall_diet_content(self.diet_frac_filterfeeders,
                                                            self.diet_content_filterfeeders_nlom)

        #filterfeeders water content of diet
        self.diet_content_filterfeeders_water = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.filterfeeders_diet_sediment)):
            self.diet_content_filterfeeders_water = [self.kabam_empty.sediment_water[i],
                             self.kabam_empty.phytoplankton_water[i],
                             self.kabam_empty.zoo_water[i],
                             self.kabam_empty.beninv_water[i]]
        self.v_wd_filterfeeders = self.overall_diet_content(self.diet_frac_filterfeeders,
                                                            self.diet_content_filterfeeders_water)

        #small fish lipid content of diet
        self.diet_frac_sfish = pd.Series([], dtype = 'float')
        self.diet_content_sfish_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.sfish_diet_sediment)):
            self.diet_frac_sfish = [self.kabam_empty.sfish_diet_sediment[i],
                             self.kabam_empty.sfish_diet_phytoplankton[i],
                             self.kabam_empty.sfish_diet_zooplankton[i],
                             self.kabam_empty.sfish_diet_beninv[i],
                             self.kabam_empty.sfish_diet_filterfeeders[i]]
            self.diet_content_sfish_lipid = [self.kabam_empty.sediment_lipid[i],
                             self.kabam_empty.phytoplankton_lipid[i],
                             self.kabam_empty.zoo_lipid[i],
                             self.kabam_empty.beninv_lipid[i],
                             self.kabam_empty.filterfeeders_lipid[i]]

        self.v_ld_sfish = self.overall_diet_content(self.diet_frac_sfish, self.diet_content_sfish_lipid)

        #small fish NLOM content of diet
        self.diet_content_sfish_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.sfish_diet_sediment)):
            self.diet_content_sfish_nlom = [self.kabam_empty.sediment_nlom[i],
                             self.kabam_empty.phytoplankton_nlom[i],
                             self.kabam_empty.zoo_nlom[i],
                             self.kabam_empty.beninv_nlom[i],
                             self.kabam_empty.filterfeeders_nlom[i]]
        self.v_nd_sfish = self.overall_diet_content(self.diet_frac_sfish, self.diet_content_sfish_nlom)

        #small fish water
        self.diet_content_sfish_water = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.sfish_diet_sediment)):
            self.diet_content_sfish_water = [self.kabam_empty.sediment_water[i],
                             self.kabam_empty.phytoplankton_water[i],
                             self.kabam_empty.zoo_water[i],
                             self.kabam_empty.beninv_water[i],
                             self.kabam_empty.filterfeeders_water[i]]
        self.v_wd_sfish = self.overall_diet_content(self.diet_frac_sfish, self.diet_content_sfish_water)

        #medium fish lipid content of diet
        self.diet_frac_mfish = pd.Series([], dtype = 'float')
        self.diet_content_mfish_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.mfish_diet_sediment)):
            self.diet_frac_mfish = [self.kabam_empty.mfish_diet_sediment[i],
                             self.kabam_empty.mfish_diet_phytoplankton[i],
                             self.kabam_empty.mfish_diet_zooplankton[i],
                             self.kabam_empty.mfish_diet_beninv[i],
                             self.kabam_empty.mfish_diet_filterfeeders[i],
                             self.kabam_empty.mfish_diet_sfish[i]]
            self.diet_content_mfish_lipid = [self.kabam_empty.sediment_lipid[i],
                             self.kabam_empty.phytoplankton_lipid[i],
                             self.kabam_empty.zoo_lipid[i],
                             self.kabam_empty.beninv_lipid[i],
                             self.kabam_empty.filterfeeders_lipid[i],
                             self.kabam_empty.sfish_lipid[i]]
        self.v_ld_mfish = self.overall_diet_content(self.diet_frac_mfish, self.diet_content_mfish_lipid)

        #medium fish NLOM content of diet
        self.diet_content_zoo_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.zoo_diet_sediment)):
            self.diet_content_mfish_nlom = [self.kabam_empty.sediment_nlom[i],
                             self.kabam_empty.phytoplankton_nlom[i],
                             self.kabam_empty.zoo_nlom[i],
                             self.kabam_empty.beninv_nlom[i],
                             self.kabam_empty.filterfeeders_nlom[i],
                             self.kabam_empty.sfish_nlom[i]]
        self.v_nd_mfish = self.overall_diet_content(self.diet_frac_mfish, self.diet_content_mfish_nlom)

        #medium fish water content of diet
        self.diet_content_mfish_water = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.zoo_diet_sediment)):
            self.diet_content_mfish_water = [self.kabam_empty.sediment_water[i],
                             self.kabam_empty.phytoplankton_water[i],
                             self.kabam_empty.zoo_water[i],
                             self.kabam_empty.beninv_water[i],
                             self.kabam_empty.filterfeeders_water[i],
                             self.kabam_empty.sfish_water[i]]
        self.v_wd_mfish = self.overall_diet_content(self.diet_frac_mfish, self.diet_content_mfish_water)

        #large fish lipid content of diet
        self.diet_frac_lfish = pd.Series([], dtype = 'float')
        self.diet_content_lfish_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.lfish_diet_sediment)):
            self.diet_frac_lfish = [self.kabam_empty.lfish_diet_sediment[i],
                             self.kabam_empty.lfish_diet_phytoplankton[i],
                             self.kabam_empty.lfish_diet_zooplankton[i],
                             self.kabam_empty.lfish_diet_beninv[i],
                             self.kabam_empty.lfish_diet_filterfeeders[i],
                             self.kabam_empty.lfish_diet_sfish[i],
                             self.kabam_empty.lfish_diet_mfish[i]]
            self.diet_content_lfish_lipid = [self.kabam_empty.sediment_lipid[i],
                             self.kabam_empty.phytoplankton_lipid[i],
                             self.kabam_empty.zoo_lipid[i],
                             self.kabam_empty.beninv_lipid[i],
                             self.kabam_empty.filterfeeders_lipid[i],
                             self.kabam_empty.sfish_lipid[i],
                             self.kabam_empty.mfish_lipid[i]]
        self.v_ld_lfish = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_lipid)

        #large fish NLOM content of diet
        self.diet_content_lfish_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.lfish_diet_sediment)):
            self.diet_content_lfish_nlom = [self.kabam_empty.sediment_nlom[i],
                             self.kabam_empty.phytoplankton_nlom[i],
                             self.kabam_empty.zoo_nlom[i],
                             self.kabam_empty.beninv_nlom[i],
                             self.kabam_empty.filterfeeders_nlom[i],
                             self.kabam_empty.sfish_nlom[i],
                             self.kabam_empty.mfish_nlom[i]]
        self.v_nd_lfish = self.overall_diet_content(self.diet_frac_lfish, self.diet_content_lfish_nlom)

        #large fish water content of diet
        self.diet_content_lfish_water = pd.Series([], dtype = 'float')
        for i in range(len(self.kabam_empty.lfish_diet_sediment)):
            self.diet_content_lfish_water = [self.kabam_empty.sediment_water[i],
                             self.kabam_empty.phytoplankton_water[i],
                             self.kabam_empty.zoo_water[i],
                             self.kabam_empty.beninv_water[i],
                             self.kabam_empty.filterfeeders_water[i],
                             self.kabam_empty.sfish_water[i],
                             self.kabam_empty.mfish_water[i]]
        self.v_wd_lfish = self.overall_diet_content(self.diet_frac_lfish, self.diet_content_lfish_water)

        # overall diet assimilation factor and egestion rate of fecal matter
        self.diet_assim_factor_zoo = pd.Series([], dtype = 'float')
        self.diet_assim_factor_beninv = pd.Series([], dtype = 'float')
        self.diet_assim_factor_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_assim_factor_sfish = pd.Series([], dtype = 'float')
        self.diet_assim_factor_mfish = pd.Series([], dtype = 'float')
        self.diet_assim_factor_lfish = pd.Series([], dtype = 'float')

        self.diet_assim_factor_zoo = self.fecal_egestion_rate_factor(self.epsilon_lipid_zoo, self.epsilon_nlom_zoo,
                                                    self.epsilon_water, self.v_ld_zoo, self.v_nd_zoo, self.v_wd_zoo)
        self.gf_zoo = self.diet_assim_factor_zoo * self.gd_zoo
        self.diet_assim_factor_beninv = self.fecal_egestion_rate_factor(self.epsilon_lipid_inv, self.epsilon_nlom_inv,
                                                self.epsilon_water, self.v_ld_beninv, self.v_nd_beninv, self.v_wd_beninv)
        self.gf_beninv = self.diet_assim_factor_beninv * self.gd_beninv
        self.diet_assim_factor_filterfeeders = self.fecal_egestion_rate_factor(self.epsilon_lipid_inv,
                                                self.epsilon_nlom_inv, self.epsilon_water, self.v_ld_filterfeeders,
                                                self.v_nd_filterfeeders, self.v_wd_filterfeeders)
        self.gf_filterfeeders = self.diet_assim_factor_filterfeeders * self.gd_filterfeeders
        self.diet_assim_factor_sfish = self.fecal_egestion_rate_factor(self.epsilon_lipid_fish, self.epsilon_nlom_fish,
                                                self.epsilon_water, self.v_ld_sfish, self.v_nd_sfish, self.v_wd_sfish)
        self.gf_sfish = self.diet_assim_factor_sfish * self.gd_sfish
        self.diet_assim_factor_mfish = self.fecal_egestion_rate_factor(self.epsilon_lipid_fish, self.epsilon_nlom_fish,
                                                self.epsilon_water, self.v_ld_mfish, self.v_nd_mfish, self.v_wd_mfish)
        self.gf_mfish = self.diet_assim_factor_mfish * self.gd_mfish
        self.diet_assim_factor_lfish = self.fecal_egestion_rate_factor(self.epsilon_lipid_fish, self.epsilon_nlom_fish,
                                                self.epsilon_water, self.v_ld_lfish, self.v_nd_lfish, self.v_wd_lfish)
        self.gf_lfish = self.diet_assim_factor_lfish * self.gd_lfish

        #fraction of diet elements (i.e., lipids, NLOM, water) in gut
        self.vlg_zoo = self.diet_elements_gut(self.epsilon_lipid_zoo, self.v_ld_zoo, self.diet_assim_factor_zoo)
        self.vng_zoo = self.diet_elements_gut(self.epsilon_nlom_zoo, self.v_nd_zoo, self.diet_assim_factor_zoo)
        self.vwg_zoo = self.diet_elements_gut(self.epsilon_water, self.v_wd_zoo, self.diet_assim_factor_zoo)

        self.vlg_beninv = self.diet_elements_gut(self.epsilon_lipid_inv, self.v_ld_beninv,
                                                         self.diet_assim_factor_beninv)
        self.vng_beninv = self.diet_elements_gut(self.epsilon_lipid_inv, self.v_nd_beninv,
                                                         self.diet_assim_factor_beninv)
        self.vwg_beninv = self.diet_elements_gut(self.epsilon_lipid_inv, self.v_wd_beninv,
                                                         self.diet_assim_factor_beninv)

        self.vlg_filterfeeders = self.diet_elements_gut(self.epsilon_lipid_inv, self.v_ld_filterfeeders,
                                                                self.diet_assim_factor_filterfeeders)
        self.vng_filterfeeders = self.diet_elements_gut(self.epsilon_nlom_inv, self.v_nd_filterfeeders,
                                                                self.diet_assim_factor_filterfeeders)
        self.vwg_filterfeeders = self.diet_elements_gut(self.epsilon_water, self.v_wd_filterfeeders,
                                                                self.diet_assim_factor_filterfeeders)

        self.vlg_sfish = self.diet_elements_gut(self.epsilon_lipid_fish, self.v_ld_sfish, self.diet_assim_factor_sfish)
        self.vng_sfish = self.diet_elements_gut(self.epsilon_nlom_fish, self.v_nd_sfish, self.diet_assim_factor_sfish)
        self.vwg_sfish = self.diet_elements_gut(self.epsilon_water, self.v_wd_sfish, self.diet_assim_factor_sfish)

        self.vlg_mfish = self.diet_elements_gut(self.epsilon_lipid_fish, self.v_ld_mfish, self.diet_assim_factor_mfish)
        self.vng_mfish = self.diet_elements_gut(self.epsilon_nlom_fish, self.v_nd_mfish, self.diet_assim_factor_mfish)
        self.vwg_mfish = self.diet_elements_gut(self.epsilon_water, self.v_wd_mfish, self.diet_assim_factor_mfish)

        self.vlg_lfish = self.diet_elements_gut(self.epsilon_lipid_fish, self.v_ld_lfish, self.diet_assim_factor_lfish)
        self.vng_lfish = self.diet_elements_gut(self.epsilon_nlom_fish, self.v_nd_lfish, self.diet_assim_factor_lfish)
        self.vwg_lfish = self.diet_elements_gut(self.epsilon_water, self.v_wd_lfish, self.diet_assim_factor_lfish)

        #partition coefficient of the pesticide between the gatro-intestinal tract and the organism
        self.kgb_zoo = self.gut_organism_partition_coef(self.vlg_zoo, self.vng_zoo, self.vwg_zoo, self.kow,
                                    self.beta_aq_animals, self.zoo_lipid_frac, self.zoo_nlom_frac, self.zoo_water_frac)
        self.kgb_beninv = self.gut_organism_partition_coef(self.vlg_beninv, self.vng_beninv, self.vwg_beninv, self.kow,
                                    self.beta_aq_animals, self.beninv_lipid_frac, self.beninv_nlom_frac,
                                    self.beninv_water_frac)
        self.kgb_filterfeeders = self.gut_organism_partition_coef(self.vlg_filterfeeders, self.vng_filterfeeders,
                                    self.vwg_filterfeeders, self.kow, self.beta_aq_animals,
                                    self.filterfeeders_lipid_frac, self.filterfeeders_nlom_frac,
                                    self.filterfeeders_water_frac)
        self.kgb_sfish = self.gut_organism_partition_coef(self.vlg_sfish, self.vng_sfish, self.vwg_sfish, self.kow,
                                    self.beta_aq_animals, self.sfish_lipid_frac, self.sfish_nlom_frac,
                                    self.sfish_water_frac)
        self.kgb_mfish = self.gut_organism_partition_coef(self.vlg_mfish, self.vng_mfish, self.vwg_mfish, self.kow,
                                    self.beta_aq_animals, self.mfish_lipid_frac, self.mfish_nlom_frac,
                                    self.mfish_water_frac)
        self.kgb_lfish = self.gut_organism_partition_coef(self.vlg_lfish, self.vng_lfish, self.vwg_lfish, self.kow,
                                    self.beta_aq_animals, self.lfish_lipid_frac, self.lfish_nlom_frac,
                                    self.lfish_water_frac)

        #rate constant for elimination of pesticide through excretion of contaminated feces
        self.zoo_ke = self.fecal_elim_rate_const(self.gf_zoo, self.ed_zoo, self.kgb_zoo, self.zoo_wb)
        self.beninv_ke = self.fecal_elim_rate_const(self.gf_beninv, self.ed_beninv, self.kgb_beninv, self.beninv_wb)
        self.filterfeeders_ke = self.fecal_elim_rate_const(self.gf_filterfeeders, self.ed_filterfeeders,
                                                           self.kgb_filterfeeders, self.filterfeeders_wb)
        self.sfish_ke = self.fecal_elim_rate_const(self.gf_sfish, self.ed_sfish, self.kgb_sfish, self.sfish_wb)
        self.mfish_ke = self.fecal_elim_rate_const(self.gf_mfish, self.ed_mfish, self.kgb_mfish, self.mfish_wb)
        self.lfish_ke = self.fecal_elim_rate_const(self.gf_lfish, self.ed_lfish, self.kgb_lfish, self.lfish_wb)

        # calculate fraction of overlying water concentration of pesticide that is freely dissolved and can be absorbed via membrane diffusion
        self.phi = self.frac_pest_freely_diss()

        #calculate concentration of freely dissolved pesticide in overlying water column
        self.water_d = self.conc_freely_diss_watercol()

        #calculate pesticide concentration in sediment normalized for organic carbon content
        self.c_soc = self.conc_sed_norm_4oc()

        #calculate pesticide concentrationin sediment (sediment dry weight basis)
        self.c_s = self.conc_sed_dry_wgt()


        # self.phi_f()
        # self.c_soc_f()
        # self.c_s_f()
        # self.sed_om_f()
        # self.water_d()
        # # self.k_bw_phytoplankton_f()
        # # self.phytoplankton_k1_f()
        # # self.phytoplankton_k2_f()
        # self.cb_phytoplankton_f()
        # self.cbl_phytoplankton_f()
        # self.cbf_phytoplankton_f()
        # self.cbr_phytoplankton_f()
        # self.cbfl_phytoplankton_f()
        # self.cbaf_phytoplankton_f()
        # self.cbafl_phytoplankton_f()
        # self.cbsafl_phytoplankton_f()
        # # self.gv_zoo_f()
        # # self.ew_zoo_f()
        # # self.zoo_k1_f()
        # # self.k_bw_zoo_f()
        # # self.zoo_k2_f()
        # # self.ed_zoo_f()
        # # self.gd_zoo_f()
        # # self.zoo_kd_f()
        # # self.kg_zoo_f()
        # # self.v_ld_zoo_f()
        # # self.v_nd_zoo_f()
        # # self.v_wd_zoo_f()
        # # self.gf_zoo_f()
        # # self.vlg_zoo_f()
        # # self.vng_zoo_f()
        # # self.vwg_zoo_f()
        # # self.kgb_zoo_f()
        # # self.zoo_ke_f()
        # self.diet_zoo_f()
        # self.cb_zoo_f()
        # self.cbl_zoo_f()
        # self.cbd_zoo_f()
        # self.cbr_zoo_f()
        # self.cbf_zoo_f()
        # self.cbfl_zoo_f()
        # self.cbaf_zoo_f()
        # self.cbafl_zoo_f()
        # self.cbsafl_zoo_f()
        # self.bmf_zoo_f()
        # # self.gv_beninv_f()
        # # self.ew_beninv_f()
        # # self.beninv_k1_f()
        # # self.k_bw_beninv_f()
        # # # self.beninv_k2_f()
        # # self.ed_beninv_f()
        # # self.gd_beninv_f()
        # # # self.beninv_kd_f()
        # self.kg_beninv_f()
        # # self.v_ld_beninv_f()
        # # self.v_nd_beninv_f()
        # # self.v_wd_beninv_f()
        # # self.gf_beninv_f()
        # # self.vlg_beninv_f()
        # # self.vng_beninv_f()
        # # self.vwg_beninv_f()
        # # self.kgb_beninv_f()
        # # self.beninv_ke_f()
        # self.diet_beninv_f()
        # self.cb_beninv_f()
        # self.cbl_beninv_f()
        # self.cbd_beninv_f()
        # self.cbr_beninv_f()
        # self.cbf_beninv_f()
        # self.cbfl_beninv_f()
        # self.cbaf_beninv_f()
        # self.cbafl_beninv_f()
        # self.cbsafl_beninv_f()
        # self.bmf_beninv_f()
        # # self.gv_ff_f()
        # # self.ew_ff_f()
        # # # self.filterfeeders_k1_f()
        # # self.k_bw_ff_f()
        # # # self.filterfeeders_k2_f()
        # # self.ed_ff_f()
        # # self.gd_ff_f()
        # # # self.filterfeeders_kd_f()
        # self.kg_ff_f()
        # # self.v_ld_ff_f()
        # # self.v_nd_ff_f()
        # # self.v_wd_ff_f()
        # # self.gf_ff_f()
        # # self.vlg_ff_f()
        # # self.vng_ff_f()
        # # self.vwg_ff_f()
        # # self.kgb_ff_f()
        # # self.filterfeeders_ke_f()
        # self.diet_ff_f()
        # self.cb_ff_f()
        # self.cbl_ff_f()
        # self.cbd_ff_f()
        # self.cbr_ff_f()
        # self.cbf_ff_f()
        # self.cbfl_ff_f()
        # self.cbaf_ff_f()
        # self.cbafl_ff_f()
        # self.cbsafl_ff_f()
        # self.bmf_ff_f()
        # # self.gv_sf_f()
        # # self.ew_sf_f()
        # # # self.sfish_k1_f()
        # # self.k_bw_sf_f()
        # # # self.sfish_k2_f()
        # # self.ed_sf_f()
        # # self.gd_sf_f()
        # # # self.sfish_kd_f()
        # self.kg_sf_f()
        # # self.v_ld_sf_f()
        # # self.v_nd_sf_f()
        # # self.v_wd_sf_f()
        # # self.gf_sf_f()
        # # self.vlg_sf_f()
        # # self.vng_sf_f()
        # # self.vwg_sf_f()
        # # self.kgb_sf_f()
        # # self.sfish_ke_f()
        # self.diet_sf_f()
        # self.cb_sf_f()
        # self.cbl_sf_f()
        # self.cbd_sf_f()
        # self.cbr_sf_f()
        # self.cbf_sf_f()
        # self.cbfl_sf_f()
        # self.cbaf_sf_f()
        # self.cbafl_sf_f()
        # self.cbsafl_sf_f()
        # self.bmf_sf_f()
        # # self.gv_mf_f()
        # # self.ew_mf_f()
        # # # self.mfish_k1_f()
        # # self.k_bw_mf_f()
        # # # self.mfish_k2_f()
        # # self.ed_mf_f()
        # # self.gd_mf_f()
        # # # self.mfish_kd_f()
        # self.kg_mf_f()
        # # self.v_ld_mf_f()
        # # self.v_nd_mf_f()
        # # self.v_wd_mf_f()
        # # self.gf_mf_f()
        # # self.vlg_mf_f()
        # # self.vng_mf_f()
        # # self.vwg_mf_f()
        # # self.kgb_mf_f()
        # # self.mfish_ke_f()
        # self.diet_mf_f()
        # self.cb_mf_f()
        # self.cbl_mf_f()
        # self.cbd_mf_f()
        # self.cbr_mf_f()
        # self.cbf_mf_f()
        # self.cbfl_mf_f()
        # self.cbaf_mf_f()
        # self.cbafl_mf_f()
        # self.cbsafl_mf_f()
        # self.cbmf_mf_f()
        # # self.gv_lf_f()
        # # self.ew_lf_f()
        # # # self.lfish_k1_f()
        # # self.k_bw_lf_f()
        # # # self.lfish_k2_f()
        # # self.ed_lf_f()
        # # self.gd_lf_f()
        # # # self.lfish_kd_f()
        # self.kg_lf_f()
        # # self.v_ld_lf_f()
        # # self.v_nd_lf_f()
        # # self.v_wd_lf_f()
        # # self.gf_lf_f()
        # # self.vlg_lf_f()
        # # self.vng_lf_f()
        # # self.vwg_lf_f()
        # # self.kgb_lf_f()
        # # self.lfish_ke_f()
        # self.diet_lf_f()
        # self.cb_lf_f()
        # self.cbl_lf_f()
        # self.cbd_lf_f()
        # self.cbr_lf_f()
        # self.cbf_lf_f()
        # self.cbfl_lf_f()
        # self.cbaf_lf_f()
        # self.cbafl_lf_f()
        # self.cbsafl_lf_f()
        # self.cbmf_lf_f()
        # self.mweight_f()
        # self.dfir_f()
        # self.wet_food_ingestion_m_f()
        # self.drinking_water_intake_m_f()
        # self.db4_f()
        # self.db5_f()
        # self.aweight_f()
        # self.dfir_a_f()
        # self.wet_food_ingestion_a_f()
        # self.drinking_water_intake_a_f()
        # self.db4a_f()
        # self.db5a_f()
        # self.acute_dose_based_m_f()
        # self.chronic_dose_based_m_f()
        # self.acute_dose_based_a_f()
        # self.acute_rq_dose_m_f()
        # self.chronic_rq_dose_m_f()
        # self.acute_rq_diet_m_f()
        # self.chronic_rq_diet_m_f()
        # self.acute_rq_dose_a_f()
        # self.acute_rq_diet_a_f()
        # self.chronic_rq_diet_a_f()

    def set_global_constants(self):

        # list of aquatic animals in the food chain from lowest to highest trophic level
        #(data in related arrays will reflect this order)
        self.aquatic_animals = np.array(['pytoplankton', 'zooplankton', 'benthic_invertebrates', 'filterfeeders',
                                          'small_fish', 'medium_fish', 'large_fish'], dtype = 'str')

        #list of mammals (data in related arrays will reflect this order)
        self.mammals = np.array(['fog/water shrew', 'rice rat/nosed mole', 'small mink', 'large mink',
                                 'small river otter', 'large river otter'])
        self.mammal_weights = np.array([0.018, 0.085, 0.45, 1.8, 5., 15.])
        self.diet_mammals = np.array([[0, 0, 1, 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1, 0],
                                      [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])

        #list of birds (data in related arrays will reflect this order)
        self.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons', 'small osprey', 'white pelican'])
        self.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5])
        self.diet_birds = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0],
                                    [0, 0, 0.5, 0, 0.5, 0, 0], [0, 0, 0.5, 0, 0, 0.5, 0],
                                    [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])

        # conversions

        self.kow = pd.Series([], dtype = 'float')
        self.sediment_oc_frac = pd.Series([], dtype = 'float')

        self.kow = 10.**(self.log_kow) # convert log kow to kow
        self.sediment_oc_frac = percent_to_frac(self.sediment_oc)

        # Assigned constants
        self.particle_scav_eff = 1.0  # filterfeeder efficiency of scavenging of particles absorbed from water (Kabam Eq. A8b2)

        # beta_* represent the proportionality constant expressing the sorption capacity of NLOM to that of octanol
        self.beta_aq_animals = 0.035
        self.beta_phyto = 0.35

        self.epsilon_lipid_fish = 0.92  # fish dietary assimilation rate of lipids (Kabam Eq. A9)
        self.epsilon_lipid_inv = 0.75  # aquatic invertabrates dietary assimilation rate of lipids (Kabam Eq. A9)
        self.epsilon_lipid_zoo = 0.72  # zooplankton dietary assimilation rate of lipids (Kabam Eq. A9)

        self.epsilon_nlom_fish  = 0.60 # fish dietary assimilation rate of NLOM (Kabam Eq. A9)
        self.epsilon_nlom_inv  = 0.60 # aquatic invertebrates dietary assimilation rate of NLOM (Kabam Eq. A9)
        self.epsilon_nlom_zoo  = 0.60 # zooplankton dietary assimilation rate of NLOM (Kabam Eq. A9)

        self.epsilon_water = 0.25  # freshwater organisms dietary assimilation rate of water

        self.alpha_poc = 0.35  #proportionality constant to describe the similarity of phase partitioning of POC in relation to octanol
        self.alpha_doc = 0.08  #proportionality constant to describe the similarity of phase partitioning of DOC in relation to octanol

