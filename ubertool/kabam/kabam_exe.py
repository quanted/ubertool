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
        self.mammalian_chronic_endpoint_unit = pd.Series([], dtype='float') #added variable
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
        self.phytoplankton_mo = pd.Series([], dtype='float')
        self.phytoplankton_mp = pd.Series([], dtype='float')

        #following rate constants may be input as numerical value or specified to be 'calculated'
        #these inputs are read in as string objects (with _temp extension) and converted as appropriate internally
        self.phytoplankton_k1_temp = pd.Series([], dtype='object')
        self.phytoplankton_k2_temp = pd.Series([], dtype='object')
        self.phytoplankton_kd_temp = pd.Series([], dtype='object')
        self.phytoplankton_ke_temp = pd.Series([], dtype='object')
        self.zoo_km = pd.Series([], dtype='float')
        self.zoo_k1_temp = pd.Series([], dtype='object')
        self.zoo_k2_temp = pd.Series([], dtype='object')
        self.zoo_kd_temp = pd.Series([], dtype='object')
        self.zoo_ke_temp = pd.Series([], dtype='object')
        self.beninv_k1_temp = pd.Series([], dtype='object')
        self.beninv_k2_temp = pd.Series([], dtype='object')
        self.beninv_kd_temp = pd.Series([], dtype='object')
        self.beninv_ke_temp = pd.Series([], dtype='object')
        self.filterfeeders_k1_temp = pd.Series([], dtype='object')
        self.filterfeeders_k2_temp = pd.Series([], dtype='object')
        self.filterfeeders_kd_temp = pd.Series([], dtype='object')
        self.filterfeeders_ke_temp = pd.Series([], dtype='object')
        self.sfish_k1_temp = pd.Series([], dtype='object')
        self.sfish_k2_temp = pd.Series([], dtype='object')
        self.sfish_kd_temp = pd.Series([], dtype='object')
        self.sfish_ke_temp = pd.Series([], dtype='object')
        self.mfish_k1_temp = pd.Series([], dtype='object')
        self.mfish_k2_temp = pd.Series([], dtype='object')
        self.mfish_kd_temp = pd.Series([], dtype='object')
        self.mfish_ke_temp = pd.Series([], dtype='object')
        self.lfish_k1_temp = pd.Series([], dtype='object')
        self.lfish_k2_temp = pd.Series([], dtype='object')
        self.lfish_kd_temp = pd.Series([], dtype='object')
        self.lfish_ke_temp = pd.Series([], dtype='object')

        #following rate constant 'km' is input as float; with a default value of 0.0 typically provided
        self.phytoplankton_km = pd.Series([], dtype='float')
        self.beninv_km = pd.Series([], dtype='float')
        self.filterfeeders_km = pd.Series([], dtype='float')
        self.sfish_km = pd.Series([], dtype='float')
        self.mfish_km = pd.Series([], dtype='float')
        self.lfish_km = pd.Series([], dtype='float')

        self.k_bw_phytoplankton = pd.Series([], dtype='float')
        self.k_bw_zoo =pd.Series([], dtype='float')
        self.k_bw_beninv = pd.Series([], dtype='float')
        self.k_bw_ff = pd.Series([], dtype='float')
        self.k_bw_sf = pd.Series([], dtype='float')
        self.k_bw_mf = pd.Series([], dtype='float')
        self.k_bw_lf = pd.Series([], dtype='float')
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
        self.out_cb_zoo = pd.Series([], dtype = 'float', name="out_cb_zoo")
        self.out_cb_beninv = pd.Series([], dtype = 'float', name="out_cb_beninv")
        self.out_cb_ff = pd.Series([], dtype = 'float', name="out_cb_ff")
        self.out_cb_sf = pd.Series([], dtype = 'float', name="out_cb_sf")
        self.out_cb_mf = pd.Series([], dtype = 'float', name="out_cb_lf")
        self.out_cb_lf = pd.Series([], dtype = 'float', name="out_cb_lf")
        self.out_cbl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbl_phytoplankton")
        self.out_cbl_zoo = pd.Series([], dtype = 'float', name="out_cbl_zoo")
        self.out_cbl_beninv = pd.Series([], dtype = 'float', name="out_cbl_beninv")
        self.out_cbl_ff = pd.Series([], dtype = 'float', name="out_cbl_ff")
        self.out_cbl_sf = pd.Series([], dtype = 'float', name="out_cbl_sf")
        self.out_cbl_mf = pd.Series([], dtype = 'float', name="out_cbl_mf")
        self.out_cbl_lf = pd.Series([], dtype = 'float', name="out_cbl_lf")
        self.out_cbd_zoo = pd.Series([], dtype = 'float', name="out_cbd_zoo")
        self.out_cbd_beninv = pd.Series([], dtype = 'float', name="out_cbd_beninv")
        self.out_cbd_ff = pd.Series([], dtype = 'float', name="out_cbd_ff")
        self.out_cbd_sf = pd.Series([], dtype = 'float', name="out_cbd_sf")
        self.out_cbd_mf = pd.Series([], dtype = 'float', name="out_cbd_mf")
        self.out_cbd_lf = pd.Series([], dtype = 'float', name="out_cbd_lf")
        self.out_cbr_phytoprankton = pd.Series([], dtype = 'float', name="out_cbr_phytoplankton")
        self.out_cbr_zoo = pd.Series([], dtype = 'float', name="out_cbr_zoo")
        self.out_cbr_beninv = pd.Series([], dtype = 'float', name="out_cbr_beninv")
        self.out_cbr_ff = pd.Series([], dtype = 'float', name="out_cbr_ff")
        self.out_cbr_sf = pd.Series([], dtype = 'float', name="out_cbr_sf")
        self.out_cbr_mf = pd.Series([], dtype = 'float', name="out_cbr_mf")
        self.out_cbr_lf = pd.Series([], dtype = 'float', name="out_cbr_lf")
        self.out_cbf_phytoplankton = pd.Series([], dtype = 'float', name="out_cbf_phytoplankton")
        self.out_cbf_zoo = pd.Series([], dtype = 'float', name="out_cbf_zoo")
        self.out_cbf_beninv = pd.Series([], dtype = 'float', name="out_cbf_beninv")
        self.out_cbf_ff = pd.Series([], dtype = 'float', name="out_cbf_ff")
        self.out_cbf_sf = pd.Series([], dtype = 'float', name="out_cbf_sf")
        self.out_cbf_mf = pd.Series([], dtype = 'float', name="out_cbf_mf")
        self.out_cbf_lf = pd.Series([], dtype = 'float', name="out_cbf_lf")
        self.out_cbaf_phytoplankton = pd.Series([], dtype = 'float', name="out_cbaf_phytoplankton")
        self.out_cbaf_zoo = pd.Series([], dtype = 'float', name="out_cbaf_zoo")
        self.out_cbaf_beninv = pd.Series([], dtype = 'float', name="out_cbaf_beninv")
        self.out_cbaf_ff = pd.Series([], dtype = 'float', name="out_cbaf_ff")
        self.out_cbaf_sf = pd.Series([], dtype = 'float', name="out_cbaf_sf")
        self.out_cbaf_mf = pd.Series([], dtype = 'float', name="out_cbaf_mf")
        self.out_cbaf_lf = pd.Series([], dtype = 'float', name="out_cbaf_lf")
        self.out_cbfl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbfl_phytoplankton")
        self.out_cbfl_zoo = pd.Series([], dtype = 'float', name="out_cbfl_zoo")
        self.out_cbfl_beninv = pd.Series([], dtype = 'float', name="out_cbfl_beninv")
        self.out_cbfl_ff = pd.Series([], dtype = 'float', name="out_cbfl_ff")
        self.out_cbfl_sf = pd.Series([], dtype = 'float', name="out_cbfl_sf")
        self.out_cbfl_mf = pd.Series([], dtype = 'float', name="out_cbfl_mf")
        self.out_cbfl_lf = pd.Series([], dtype = 'float', name="out_cbfl_lf")
        self.out_cbafl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbafl_phytoplankton")
        self.out_cbafl_zoo = pd.Series([], dtype = 'float', name="out_cbafl_zoo")
        self.out_cbafl_beninv = pd.Series([], dtype = 'float', name="out_cbafl_beninv")
        self.out_cbafl_ff = pd.Series([], dtype = 'float', name="out_cbafl_ff")
        self.out_cbafl_sf = pd.Series([], dtype = 'float', name="out_cbafl_sf")
        self.out_cbafl_mf = pd.Series([], dtype = 'float', name="out_cbafl_mf")
        self.out_cbafl_lf = pd.Series([], dtype = 'float', name="out_cbafl_lf")
        self.out_bmf_zoo = pd.Series([], dtype = 'float', name="out_bmf_zoo")
        self.out_bmf_beninv = pd.Series([], dtype = 'float', name="out_bmf_beninv")
        self.out_bmf_ff = pd.Series([], dtype = 'float', name="out_bmf_ff")
        self.out_bmf_sf = pd.Series([], dtype = 'float', name="out_bmf_sf")
        self.out_bmf_mf = pd.Series([], dtype = 'float', name="out_bmf_mf")
        self.out_bmf_lf = pd.Series([], dtype = 'float', name="out_bmf_lf")
        self.out_cbsafl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbsafl_phytoplankton")
        self.out_cbsafl_zoo = pd.Series([], dtype = 'float', name="out_cbsafl_zoo")
        self.out_cbsafl_beninv = pd.Series([], dtype = 'float', name="out_cbsafl_beninv")
        self.out_cbsafl_ff = pd.Series([], dtype = 'float', name="out_cbsafl_ff")
        self.out_cbsafl_sf = pd.Series([], dtype = 'float', name="out_cbsafl_sf")
        self.out_cbsafl_mf = pd.Series([], dtype = 'float', name="out_cbsafl_mf")
        self.out_cbsafl_lf = pd.Series([], dtype = 'float', name="out_cbsafl_lf")
        self.out_mweight0 = pd.Series([], dtype = 'float', name="mweight0")
        self.out_mweight1 = pd.Series([], dtype = 'float', name="mweight1")
        self.out_mweight2 = pd.Series([], dtype = 'float', name="mweight2")
        self.out_mweight3 = pd.Series([], dtype = 'float', name="mweight3")
        self.out_mweight4 = pd.Series([], dtype = 'float', name="mweight4")
        self.out_mweight5 = pd.Series([], dtype = 'float', name="mweight5")
        self.out_aweight0 = pd.Series([], dtype = 'float', name="aweight0")
        self.out_aweight1 = pd.Series([], dtype = 'float', name="aweight1")
        self.out_aweight2 = pd.Series([], dtype = 'float', name="aweight2")
        self.out_aweight3 = pd.Series([], dtype = 'float', name="aweight3")
        self.out_aweight4 = pd.Series([], dtype = 'float', name="aweight4")
        self.out_aweight5 = pd.Series([], dtype = 'float', name="aweight5")
        self.out_dfir0 = pd.Series([], dtype = 'float', name="dfir0")
        self.out_dfir1 = pd.Series([], dtype = 'float', name="dfir1")
        self.out_dfir2 = pd.Series([], dtype = 'float', name="dfir2")
        self.out_dfir3 = pd.Series([], dtype = 'float', name="dfir3")
        self.out_dfir4 = pd.Series([], dtype = 'float', name="dfir4")
        self.out_dfir5 = pd.Series([], dtype = 'float', name="dfir5")
        self.out_dfira0 = pd.Series([], dtype = 'float', name="dfira0")
        self.out_dfira1 = pd.Series([], dtype = 'float', name="dfira1")
        self.out_dfira2 = pd.Series([], dtype = 'float', name="dfira2")
        self.out_dfira3 = pd.Series([], dtype = 'float', name="dfira3")
        self.out_dfira4 = pd.Series([], dtype = 'float', name="dfira4")
        self.out_dfira5 = pd.Series([], dtype = 'float', name="dfira5")
        self.out_wet_food_ingestion_m0 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_m0")
        self.out_wet_food_ingestion_m1 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_m1")
        self.out_wet_food_ingestion_m2 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_m2")
        self.out_wet_food_ingestion_m3 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_m3")
        self.out_wet_food_ingestion_m4 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_m4")
        self.out_wet_food_ingestion_m5 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_m5")
        self.out_wet_food_ingestion_a0 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_a0")
        self.out_wet_food_ingestion_a1 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_a1")
        self.out_wet_food_ingestion_a2 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_a2")
        self.out_wet_food_ingestion_a3 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_a3")
        self.out_wet_food_ingestion_a4 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_a4")
        self.out_wet_food_ingestion_a5 = pd.Series([], dtype = 'float', name="out_wet_food_ingestion_a5")
        self.out_drinking_water_intake_m0 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_m0")
        self.out_drinking_water_intake_m1 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_m1")
        self.out_drinking_water_intake_m2 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_m2")
        self.out_drinking_water_intake_m3 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_m3")
        self.out_drinking_water_intake_m4 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_m4")
        self.out_drinking_water_intake_m5 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_m5")
        self.out_drinking_water_intake_a0 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_a0")
        self.out_drinking_water_intake_a1 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_a1")
        self.out_drinking_water_intake_a2 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_a2")
        self.out_drinking_water_intake_a3 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_a3")
        self.out_drinking_water_intake_a4 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_a4")
        self.out_drinking_water_intake_a5 = pd.Series([], dtype = 'float', name="out_drinking_water_intake_a5")
        self.out_db40 = pd.Series([], dtype = 'float', name="out_db40")
        self.out_db41 = pd.Series([], dtype = 'float', name="out_db41")
        self.out_db42 = pd.Series([], dtype = 'float', name="out_db42")
        self.out_db43 = pd.Series([], dtype = 'float', name="out_db43")
        self.out_db44 = pd.Series([], dtype = 'float', name="out_db44")
        self.out_db45 = pd.Series([], dtype = 'float', name="out_db45")
        self.out_db4a0 = pd.Series([], dtype = 'float', name="out_db4a0")
        self.out_db4a1 = pd.Series([], dtype = 'float', name="out_db4a1")
        self.out_db4a2 = pd.Series([], dtype = 'float', name="out_db4a2")
        self.out_db4a3 = pd.Series([], dtype = 'float', name="out_db4a3")
        self.out_db4a4 = pd.Series([], dtype = 'float', name="out_db4a4")
        self.out_db4a5 = pd.Series([], dtype = 'float', name="out_db4a5")
        self.out_db50 = pd.Series([], dtype = 'float', name="out_out_db50")
        self.out_db51 = pd.Series([], dtype = 'float', name="out_out_db51")
        self.out_db52 = pd.Series([], dtype = 'float', name="out_out_db52")
        self.out_db53 = pd.Series([], dtype = 'float', name="out_out_db53")
        self.out_db54 = pd.Series([], dtype = 'float', name="out_out_db54")
        self.out_db55 = pd.Series([], dtype = 'float', name="out_out_db55")
        self.out_db5a0 = pd.Series([], dtype = 'float', name="out_out_db5a0")
        self.out_db5a1 = pd.Series([], dtype = 'float', name="out_out_db5a1")
        self.out_db5a2 = pd.Series([], dtype = 'float', name="out_out_db5a2")
        self.out_db5a3 = pd.Series([], dtype = 'float', name="out_out_db5a3")
        self.out_db5a4 = pd.Series([], dtype = 'float', name="out_out_db5a4")
        self.out_db5a5 = pd.Series([], dtype = 'float', name="out_out_db5a5")
        self.out_acute_dose_based_m0 = pd.Series([], dtype = 'float', name="out_acute_dose_based_m0")
        self.out_acute_dose_based_m1 = pd.Series([], dtype = 'float', name="out_acute_dose_based_m1")
        self.out_acute_dose_based_m2 = pd.Series([], dtype = 'float', name="out_acute_dose_based_m2")
        self.out_acute_dose_based_m3 = pd.Series([], dtype = 'float', name="out_acute_dose_based_m3")
        self.out_acute_dose_based_m4 = pd.Series([], dtype = 'float', name="out_acute_dose_based_m4")
        self.out_acute_dose_based_m5 = pd.Series([], dtype = 'float', name="out_acute_dose_based_m5")
        self.out_acute_dose_based_a0 = pd.Series([], dtype = 'float', name="out_acute_dose_based_a0")
        self.out_acute_dose_based_a1 = pd.Series([], dtype = 'float', name="out_acute_dose_based_a1")
        self.out_acute_dose_based_a2 = pd.Series([], dtype = 'float', name="out_acute_dose_based_a2")
        self.out_acute_dose_based_a3 = pd.Series([], dtype = 'float', name="out_acute_dose_based_a3")
        self.out_acute_dose_based_a4 = pd.Series([], dtype = 'float', name="out_acute_dose_based_a4")
        self.out_acute_dose_based_a5 = pd.Series([], dtype = 'float', name="out_acute_dose_based_a5")
        self.out_acute_diet_based_m0 = pd.Series([], dtype = 'float', name="out_acute_diet_based_m0")
        self.out_acute_diet_based_m1 = pd.Series([], dtype = 'float', name="out_acute_diet_based_m1")
        self.out_acute_diet_based_m2 = pd.Series([], dtype = 'float', name="out_acute_diet_based_m2")
        self.out_acute_diet_based_m3 = pd.Series([], dtype = 'float', name="out_acute_diet_based_m3")
        self.out_acute_diet_based_m4 = pd.Series([], dtype = 'float', name="out_acute_diet_based_m4")
        self.out_acute_diet_based_m5 = pd.Series([], dtype = 'float', name="out_acute_diet_based_m5")
        self.out_acute_diet_based_a0 = pd.Series([], dtype = 'float', name="out_acute_diet_based_a0")
        self.out_acute_diet_based_a1 = pd.Series([], dtype = 'float', name="out_acute_diet_based_a1")
        self.out_acute_diet_based_a2 = pd.Series([], dtype = 'float', name="out_acute_diet_based_a2")
        self.out_acute_diet_based_a3 = pd.Series([], dtype = 'float', name="out_acute_diet_based_a3")
        self.out_acute_diet_based_a4 = pd.Series([], dtype = 'float', name="out_acute_diet_based_a4")
        self.out_acute_diet_based_a5 = pd.Series([], dtype = 'float', name="out_acute_diet_based_a5")
        self.out_chronic_dose_based_m0 = pd.Series([], dtype = 'float', name="out_chronic_dose_based_m0")
        self.out_chronic_dose_based_m1 = pd.Series([], dtype = 'float', name="out_chronic_dose_based_m1")
        self.out_chronic_dose_based_m2 = pd.Series([], dtype = 'float', name="out_chronic_dose_based_m2")
        self.out_chronic_dose_based_m3 = pd.Series([], dtype = 'float', name="out_chronic_dose_based_m3")
        self.out_chronic_dose_based_m4 = pd.Series([], dtype = 'float', name="out_chronic_dose_based_m4")
        self.out_chronic_dose_based_m5 = pd.Series([], dtype = 'float', name="out_chronic_dose_based_m5")
        self.out_chronic_diet_based_m0 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_m0")
        self.out_chronic_diet_based_m1 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_m1")
        self.out_chronic_diet_based_m2 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_m2")
        self.out_chronic_diet_based_m3 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_m3")
        self.out_chronic_diet_based_m4 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_m4")
        self.out_chronic_diet_based_m5 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_m5")
        self.out_chronic_diet_based_a0 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_a0")
        self.out_chronic_diet_based_a1 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_a1")
        self.out_chronic_diet_based_a2 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_a2")
        self.out_chronic_diet_based_a3 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_a3")
        self.out_chronic_diet_based_a4 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_a4")
        self.out_chronic_diet_based_a5 = pd.Series([], dtype = 'float', name="out_chronic_diet_based_a5")
        self.out_acute_rq_dose_m0 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_m0")
        self.out_acute_rq_dose_m1 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_m1")
        self.out_acute_rq_dose_m2 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_m2")
        self.out_acute_rq_dose_m3 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_m3")
        self.out_acute_rq_dose_m4 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_m4")
        self.out_acute_rq_dose_m5 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_m5")
        self.out_acute_rq_dose_a0 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_a0")
        self.out_acute_rq_dose_a1 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_a1")
        self.out_acute_rq_dose_a2 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_a2")
        self.out_acute_rq_dose_a3 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_a3")
        self.out_acute_rq_dose_a4 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_a4")
        self.out_acute_rq_dose_a5 = pd.Series([], dtype = 'float', name="out_acute_rq_dose_a5")
        self.out_acute_rq_diet_m0 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_m0")
        self.out_acute_rq_diet_m1 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_m1")
        self.out_acute_rq_diet_m2 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_m2")
        self.out_acute_rq_diet_m3 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_m3")
        self.out_acute_rq_diet_m4 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_m4")
        self.out_acute_rq_diet_m5 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_m5")
        self.out_acute_rq_diet_a0 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_a0")
        self.out_acute_rq_diet_a1 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_a1")
        self.out_acute_rq_diet_a2 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_a2")
        self.out_acute_rq_diet_a3 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_a3")
        self.out_acute_rq_diet_a4 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_a4")
        self.out_acute_rq_diet_a5 = pd.Series([], dtype = 'float', name="out_acute_rq_diet_a5")
        self.out_chronic_rq_dose_m0 = pd.Series([], dtype = 'float', name="out_chronic_rq_dose_m0")
        self.out_chronic_rq_dose_m1 = pd.Series([], dtype = 'float', name="out_chronic_rq_dose_m1")
        self.out_chronic_rq_dose_m2 = pd.Series([], dtype = 'float', name="out_chronic_rq_dose_m2")
        self.out_chronic_rq_dose_m3 = pd.Series([], dtype = 'float', name="out_chronic_rq_dose_m3")
        self.out_chronic_rq_dose_m4 = pd.Series([], dtype = 'float', name="out_chronic_rq_dose_m4")
        self.out_chronic_rq_dose_m5 = pd.Series([], dtype = 'float', name="out_chronic_rq_dose_m5")
        self.out_chronic_rq_diet_m0 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_m0")
        self.out_chronic_rq_diet_m1 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_m1")
        self.out_chronic_rq_diet_m2 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_m2")
        self.out_chronic_rq_diet_m3 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_m3")
        self.out_chronic_rq_diet_m4 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_m4")
        self.out_chronic_rq_diet_m5 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_m5")
        self.out_chronic_rq_diet_a0 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_a0")
        self.out_chronic_rq_diet_a1 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_a1")
        self.out_chronic_rq_diet_a2 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_a2")
        self.out_chronic_rq_diet_a3 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_a3")
        self.out_chronic_rq_diet_a4 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_a4")
        self.out_chronic_rq_diet_a5 = pd.Series([], dtype = 'float', name="out_chronic_rq_diet_a5")

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

        self.out_dfir0 = pd.Series([], dtype = 'float')
        self.out_dfir1 = pd.Series([], dtype = 'float')
        self.out_dfir2 = pd.Series([], dtype = 'float')
        self.out_dfir3 = pd.Series([], dtype = 'float')
        self.out_dfir4 = pd.Series([], dtype = 'float')
        self.out_dfir5 = pd.Series([], dtype = 'float')

        self.out_dfira0 = pd.Series([], dtype = 'float')
        self.out_dfira1 = pd.Series([], dtype = 'float')
        self.out_dfira2 = pd.Series([], dtype = 'float')
        self.out_dfira3 = pd.Series([], dtype = 'float')
        self.out_dfira4 = pd.Series([], dtype = 'float')
        self.out_dfira5 = pd.Series([], dtype = 'float')

        self.out_wet_food_ingestion_m0 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_m1 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_m2 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_m3 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_m4 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_m5 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_a0 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_a1 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_a2 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_a3 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_a4 = pd.Series([], dtype = 'float')
        self.out_wet_food_ingestion_a5 = pd.Series([], dtype = 'float')

        self.out_acute_dose_based_m0 = pd.Series([], dtype = 'float')
        self.out_acute_dose_based_m1 = pd.Series([], dtype = 'float')
        self.out_acute_dose_based_m2 = pd.Series([], dtype = 'float')
        self.out_acute_dose_based_m3 = pd.Series([], dtype = 'float')
        self.out_acute_dose_based_m4 = pd.Series([], dtype = 'float')
        self.out_acute_dose_based_m5 = pd.Series([], dtype = 'float')


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

        self.sediment_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.sediment_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.sediment_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.sediment_lipid_frac = self.percent_to_frac(self.sediment_lipid)
        self.sediment_nlom_frac = self.percent_to_frac(self.sediment_nlom)
        self.sediment_water_frac = self.percent_to_frac(self.sediment_water)

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
        self.ew_aq_animals = self.pest_uptake_eff_bygills()
        self.ew_zoo = self.ew_beninv = self.ew_filterfeeders = self.ew_sfish = \
                      self.ew_mfish = self.ew_lfish = self.ew_aq_animals

        # aquatic animal respitory area uptake rate constant (Kabam Eqs. A5.1 & A5.2
        # set value depending on user option for input (either specific by user or calculated internally)
        self.phytoplankton_k1 = pd.Series([], dtype = 'float')
        if (self.phytoplankton_k1_temp == 'calculated'):
            self.phytoplankton_k1 = self.phytoplankton_k1_calc()
        else:
            self.phytoplankton_k1 = float(self.phytoplankton_k1_temp)

        self.zoo_k1 = pd.Series([], dtype = 'float')
        if (self.zoo_k1_temp == 'calculated'):
            self.zoo_k1 = self.aq_animal_k1_calc(self.ew_zoo, self.gv_zoo, self.zoo_wb)
        else:
            self.zoo_k1 = float(self.zoo_k1_temp)

        self.beninv_k1 = pd.Series([], dtype = 'float')
        if (self.beninv_k1_temp == 'calculated'):
            self.beninv_k1 = self.aq_animal_k1_calc(self.ew_beninv, self.gv_beninv, self.beninv_wb)
        else:
            self.beninv_k1 = float(self.beninv_k1_temp)

        self.filterfeeders_k1 = pd.Series([], dtype = 'float')
        if (self.filterfeeders_k1_temp == 'calculated'):
            self.filterfeeders_k1 = self.aq_animal_k1_calc(self.ew_filterfeeders, self.gv_filterfeeders,
                                                           self.filterfeeders_wb)
        else:
            self.filterfeeders_k1 = float(self.filterfeeders_k1_temp)

        self.sfish_k1 = pd.Series([], dtype = 'float')
        if (self.sfish_k1_temp == 'calculated'):
            self.sfish_k1 = self.aq_animal_k1_calc(self.ew_sfish, self.gv_sfish, self.sfish_wb)
        else:
            self.sfish_k1 = float(self.sfish_k1_temp)

        self.mfish_k1 = pd.Series([], dtype = 'float')
        if (self.mfish_k1_temp == 'calculated'):
            self.mfish_k1 = self.aq_animal_k1_calc(self.ew_mfish, self.gv_mfish, self.mfish_wb)
        else:
            self.mfish_k1 = float(self.mfish_k1_temp)
            
        self.lfish_k1 = pd.Series([], dtype = 'float')
        if (self.lfish_k1_temp == 'calculated'):
            self.lfish_k1 = self.aq_animal_k1_calc(self.ew_lfish, self.gv_lfish, self.lfish_wb)
        else:
            self.lfish_k1 = float(self.lfish_k1_temp)

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

        # Pesticide uptake rate constant for chemical uptake through respiratory area (Kabam Eq. A6)
        # set value depending on user option for input (either specific by user or calculated internally)
        self.phytoplankton_k2 = pd.Series([], dtype = 'float')
        if (self.phytoplankton_k2_temp == 'calculated'):
            self.phytoplankton_k2 = self.aq_animal_k2_calc(self.phytoplankton_k1, self.k_bw_phytoplankton)
        else:
            self.phytoplankton_k2 = float(self.phytoplankton_k2_temp)

        self.zoo_k2 = pd.Series([], dtype = 'float')
        if (self.zoo_k2_temp == 'calculated'):
            self.zoo_k2 = self.aq_animal_k2_calc(self.zoo_k1, self.k_bw_zoo)
        else:
            self.zoo_k2 = float(self.zoo_k2_temp)
            
        self.beninv_k2 = pd.Series([], dtype = 'float')
        if (self.beninv_k2_temp == 'calculated'):
            self.beninv_k2 = self.aq_animal_k2_calc(self.beninv_k1, self.k_bw_beninv)
        else:
            self.beninv_k2 = float(self.beninv_k2_temp)

        self.filterfeeders_k2 = pd.Series([], dtype = 'float')
        if (self.filterfeeders_k2_temp == 'calculated'):
            self.filterfeeders_k2 = self.aq_animal_k2_calc(self.filterfeeders_k1, self.k_bw_filterfeeders)
        else:
            self.filterfeeders_k2 = float(self.filterfeeders_k2_temp)
            
        self.sfish_k2 = pd.Series([], dtype = 'float')
        if (self.sfish_k2_temp == 'calculated'):
            self.sfish_k2 = self.aq_animal_k2_calc(self.sfish_k1, self.k_bw_sfish)
        else:
            self.sfish_k2 = float(self.sfish_k2_temp)
            
        self.mfish_k2 = pd.Series([], dtype = 'float')
        if (self.mfish_k2_temp == 'calculated'):
            self.mfish_k2 = self.aq_animal_k2_calc(self.mfish_k1, self.k_bw_mfish)
        else:
            self.mfish_k2 = float(self.mfish_k2_temp)
            
        self.lfish_k2 = pd.Series([], dtype = 'float')
        if (self.lfish_k2_temp == 'calculated'):
            self.lfish_k2 = self.aq_animal_k2_calc(self.lfish_k1, self.k_bw_lfish)
        else:
            self.lfish_k2 = float(self.lfish_k2_temp)

        # aquatic animal/organism growth rate constants (Kabam Eq. A7.1 & A7.2)
        self.kg_phytoplankton = 0.1 # check this; 0.1 is assigned (not calculated) in OPP model spreadsheet
#??                                 # in worksheet 'Parameters & Calculations' cell C48
        self.kg_zoo = self.animal_grow_rate_const(self.zoo_wb)
        self.kg_beninv = self.animal_grow_rate_const(self.beninv_wb)
        self.kg_filterfeeders = self.animal_grow_rate_const(self.filterfeeders_wb)
        self.kg_sfish = self.animal_grow_rate_const(self.sfish_wb)
        self.kg_mfish = self.animal_grow_rate_const(self.mfish_wb)
        self.kg_lfish = self.animal_grow_rate_const(self.lfish_wb)

        # aquatic animal/organism dietary pesticide transfer efficiency Eq. A8 (kD)
        # i think the following declarations should be moved to output class
        self.ed_zoo = pd.Series([], dtype = 'float')
        self.ed_beninv = pd.Series([], dtype = 'float')
        self.ed_filterfeeders = pd.Series([], dtype = 'float')
        self.ed_sfish = pd.Series([], dtype = 'float')
        self.ed_mfish = pd.Series([], dtype = 'float')
        self.ed_lfish = pd.Series([], dtype = 'float')

        self.ed_zoo = self.ed_beninv = self.ed_filterfeeders = self.ed_sfish = \
                      self.ed_mfish = self.ed_lfish = self.dietary_trans_eff()

        # aquatic animal/organism feeding rate Eq. A8b1 (Gd)
        self.gd_zoo = self.aq_animal_feeding_rate(self, self.zoo_wb)
        self.gd_beninv = self.aq_animal_feeding_rate(self, self.beninv_wb)
        self.gd_filterfeeders = self.filterfeeder_feeding_rate()
        self.gd_sfish = self.aq_animal_feeding_rate(self, self.sfish_wb)
        self.gd_mfish = self.aq_animal_feeding_rate(self, self.mfish_wb)
        self.gd_lfish = self.aq_animal_feeding_rate(self, self.lfish_wb)

        # dietary uptake rate constant Eq. A8 (kD)
        # set value depending on user option for input (either specific by user or calculated internally)
        self.zoo_kd = pd.Series([], dtype = 'float')
        if (self.zoo_kd_temp == 'calculated'):
            self.zoo_kd = self.diet_uptake_rate_const(self.ed_zoo, self.gd_zoo, self.zoo_wb)
        else:
            self.zoo_kd = float(self.zoo_kd_temp)

        self.beninv_kd = pd.Series([], dtype = 'float')
        if (self.beninv_kd_temp == 'calculated'):
            self.beninv_kd = self.diet_uptake_rate_const(self.ed_beninv, self.gd_beninv, self.beninv_wb)
        else:
            self.beninv_kd = float(self.beninv_kd_temp)
            
        self.filterfeeders_kd = pd.Series([], dtype = 'float')
        if (self.filterfeeders_kd_temp == 'calculated'):
            self.filterfeeders_kd = self.diet_uptake_rate_const(self.ed_filterfeeders, self.gd_filterfeeders,
                                                                self.filterfeeders_wb)
        else:
            self.filterfeeders_kd = float(self.filterfeeders_kd_temp)
            
        self.sfish_kd = pd.Series([], dtype = 'float')
        if (self.sfish_kd_temp == 'calculated'):
            self.sfish_kd = self.diet_uptake_rate_const(self.ed_sfish, self.gd_sfish, self.sfish_wb)
        else:
            self.sfish_kd = float(self.sfish_kd_temp)
            
        self.mfish_kd = pd.Series([], dtype = 'float')
        if (self.mfish_kd_temp == 'calculated'):
            self.mfish_kd = self.diet_uptake_rate_const(self.ed_mfish, self.gd_mfish, self.mfish_wb)
        else:
            self.mfish_kd = float(self.mfish_kd_temp)
            
        self.lfish_kd = pd.Series([], dtype = 'float')
        if (self.lfish_kd_temp == 'calculated'):
            self.lfish_kd = self.diet_uptake_rate_const(self.ed_lfish, self.gd_lfish, self.lfish_wb)
        else:
            self.lfish_kd = float(self.lfish_kd_temp)

        #overall lipid, NLOM, and Water content of aquatic animal/organism diet (associated with Eq A9 VLD, VND, VWD
            #loops reflect stepping through model simulation runs one at a time
            #notes: 1. there is some room here for reduction of code; the 'diet_content_*_*' variable
            #          could be reduced to a single set that is used for each trophic level
            #       2. for future consideration: this processing might be optimized with matrix based calculations

        #zooplankton lipid content of diet
        self.diet_frac_zoo = pd.Series([], dtype = 'float')
        self.diet_content_zoo_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.zoo_diet_sediment)):
            self.diet_frac_zoo[i] = [self.zoo_diet_sediment[i],
                             self.zoo_diet_phytoplankton[i]]
            self.diet_content_zoo_lipid[i] = [self.sediment_lipid[i],
                             self.phytoplankton_lipid[i]]
        self.v_ld_zoo = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_lipid)

        #zooplankton NLOM content of diet
        self.diet_content_zoo_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.zoo_diet_sediment)):
            self.diet_content_zoo_nlom[i] = [self.sediment_nlom[i],
                             self.phytoplankton_nlom[i]]
        self.v_nd_zoo = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_nlom)

        #zooplankton water content of diet
        self.diet_content_beninv_water = pd.Series([], dtype = 'float')
        for i in range(len(self.zoo_diet_sediment)):
            self.diet_content_zoo_water[i] = [self.sediment_water[i],
                             self.phytoplankton_water[i]]
        self.v_wd_zoo = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_water)

        #benthic invertebrates lipid content of diet
        self.diet_frac_beninv = pd.Series([], dtype = 'float')
        self.diet_content_beninv_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.beninv_diet_sediment)):
            self.diet_frac_beninv[i] = [self.beninv_diet_sediment[i],
                             self.beninv_diet_phytoplankton[i],
                             self.beninv_diet_zooplankton[i]]
            self.diet_content_beninv_lipid[i] = [self.sediment_lipid[i],
                             self.phytoplankton_lipid[i],
                             self.zooplankton_lipid[i]]
        self.v_ld_beninv = self.overall_diet_content(self.diet_frac_beninv, self.diet_content_beninv_lipid)

        #benthic invertebrates NLOM content of diet
        self.diet_content_beninv_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.beninv_diet_sediment)):
            self.diet_content_beninv_nlom[i] = [self.sediment_nlom[i],
                             self.phytoplankton_nlom[i],
                             self.zooplankton_nlom[i]]
        self.v_nd_beninv = self.overall_diet_content(self.diet_frac_beninv, self.diet_content_beninv_nlom)

        #benthic invertebrates water content of diet
        self.diet_content_beninv_water = pd.Series([], dtype = 'float')
        for i in range(len(self.beninv_diet_sediment)):
            self.diet_content_beninv_water[i] = [self.sediment_water[i],
                             self.phytoplankton_water[i],
                             self.zooplankton_water[i]]
        self.v_wd_beninv = self.overall_diet_content(self.diet_frac_beninv, self.diet_content_beninv_water)

        #filterfeeders lipid content of diet
        self.diet_frac_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_content_filterfeeders_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.filterfeeders_diet_sediment)):
           self.diet_frac_zoo[i] = [self.filterfeeders_diet_sediment[i],
                             self.filterfeeders_diet_phytoplankton[i],
                             self.filterfeeders_diet_zooplankton[i],
                             self.filterfeeders_diet_beninv[i]]
           self.diet_content_filterfeeders_lipid[i] = [self.sediment_lipid[i],
                             self.phytoplankton_lipid[i],
                             self.zoo_lipid[i],
                             self.beninv_lipid[i]]
        self.v_ld_filterfeeders = self.overall_diet_content(self.diet_frac_filterfeeders,
                                                            self.diet_content_filterfeeders_lipid)

        #filterfeeders NLOM content of diet
        self.diet_content_filterfeeders_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.filterfeeders_diet_sediment)):
            self.diet_content_filterfeeders_nlom[i] = [self.sediment_nlom[i],
                             self.phytoplankton_nlom[i],
                             self.zoo_nlom[i],
                             self.beninv_nlom[i]]
        self.v_nd_filterfeeders = self.overall_diet_content(self.diet_frac_filterfeeders,
                                                            self.diet_content_filterfeeders_nlom)

        #filterfeeders water content of diet
        self.diet_content_filterfeeders_water = pd.Series([], dtype = 'float')
        for i in range(len(self.filterfeeders_diet_sediment)):
            self.diet_content_filterfeeders_water[i] = [self.sediment_water[i],
                             self.phytoplankton_water[i],
                             self.zoo_water[i],
                             self.beninv_water[i]]
        self.v_wd_filterfeeders = self.overall_diet_content(self.diet_frac_filterfeeders,
                                                            self.diet_content_filterfeeders_water)

        #small fish lipid content of diet
        self.diet_frac_sfish = pd.Series([], dtype = 'float')
        self.diet_content_sfish_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.sfish_diet_sediment)):
            self.diet_frac_sfish[i] = [self.sfish_diet_sediment[i],
                             self.sfish_diet_phytoplankton[i],
                             self.sfish_diet_zooplankton[i],
                             self.sfish_diet_beninv[i],
                             self.sfish_diet_filterfeeders[i]]
            self.diet_content_sfish_lipid[i] = [self.sediment_lipid[i],
                             self.phytoplankton_lipid[i],
                             self.zoo_lipid[i],
                             self.beninv_lipid[i],
                             self.filterfeeders_lipid[i]]

        self.v_ld_sfish = self.overall_diet_content(self.diet_frac_sfish, self.diet_content_sfish_lipid)

        #small fish NLOM content of diet
        self.diet_content_sfish_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.sfish_diet_sediment)):
            self.diet_content_sfish_nlom[i] = [self.sediment_nlom[i],
                             self.phytoplankton_nlom[i],
                             self.zoo_nlom[i],
                             self.beninv_nlom[i],
                             self.filterfeeders_nlom[i]]
        self.v_nd_sfish = self.overall_diet_content(self.diet_frac_sfish, self.diet_content_sfish_nlom)

        #small fish water
        self.diet_content_sfish_water = pd.Series([], dtype = 'float')
        for i in range(len(self.sfish_diet_sediment)):
            self.diet_content_sfish_water[i] = [self.sediment_water[i],
                             self.phytoplankton_water[i],
                             self.zoo_water[i],
                             self.beninv_water[i],
                             self.filterfeeders_water[i]]
        self.v_wd_sfish = self.overall_diet_content(self.diet_frac_sfish, self.diet_content_sfish_water)

        #medium fish lipid content of diet
        self.diet_frac_mfish = pd.Series([], dtype = 'float')
        self.diet_content_mfish_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.mfish_diet_sediment)):
            self.diet_frac_mfish[i] = [self.mfish_diet_sediment[i],
                             self.mfish_diet_phytoplankton[i],
                             self.mfish_diet_zooplankton[i],
                             self.mfish_diet_beninv[i],
                             self.mfish_diet_filterfeeders[i],
                             self.mfish_diet_sfish[i]]
            self.diet_content_mfish_lipid[i] = [self.sediment_lipid[i],
                             self.phytoplankton_lipid[i],
                             self.zoo_lipid[i],
                             self.beninv_lipid[i],
                             self.filterfeeders_lipid[i],
                             self.sfish_lipid[i]]
        self.v_ld_mfish = self.overall_diet_content(self.diet_frac_mfish, self.diet_content_mfish_lipid)

        #medium fish NLOM content of diet
        self.diet_content_zoo_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.zoo_diet_sediment)):
            self.diet_content_mfish_nlom[i] = [self.sediment_nlom[i],
                             self.phytoplankton_nlom[i],
                             self.zoo_nlom[i],
                             self.beninv_nlom[i],
                             self.filterfeeders_nlom[i],
                             self.sfish_nlom[i]]
        self.v_nd_mfish = self.overall_diet_content(self.diet_frac_mfish, self.diet_content_mfish_nlom)

        #medium fish water content of diet
        self.diet_content_mfish_water = pd.Series([], dtype = 'float')
        for i in range(len(self.zoo_diet_sediment)):
            self.diet_content_mfish_water[i] = [self.sediment_water[i],
                             self.phytoplankton_water[i],
                             self.zoo_water[i],
                             self.beninv_water[i],
                             self.filterfeeders_water[i],
                             self.sfish_water[i]]
        self.v_wd_mfish = self.overall_diet_content(self.diet_frac_mfish, self.diet_content_mfish_water)

        #large fish lipid content of diet
        self.diet_frac_lfish = pd.Series([], dtype = 'float')
        self.diet_content_lfish_lipid = pd.Series([], dtype = 'float')
        for i in range(len(self.lfish_diet_sediment)):
            self.diet_frac_lfish[i] = [self.lfish_diet_sediment[i],
                             self.lfish_diet_phytoplankton[i],
                             self.lfish_diet_zooplankton[i],
                             self.lfish_diet_beninv[i],
                             self.lfish_diet_filterfeeders[i],
                             self.lfish_diet_sfish[i],
                             self.lfish_diet_mfish[i]]
            self.diet_content_lfish_lipid[i] = [self.sediment_lipid[i],
                             self.phytoplankton_lipid[i],
                             self.zoo_lipid[i],
                             self.beninv_lipid[i],
                             self.filterfeeders_lipid[i],
                             self.sfish_lipid[i],
                             self.mfish_lipid[i]]
        self.v_ld_lfish = self.overall_diet_content(self.diet_frac_zoo, self.diet_content_zoo_lipid)

        #large fish NLOM content of diet
        self.diet_content_lfish_nlom = pd.Series([], dtype = 'float')
        for i in range(len(self.lfish_diet_sediment)):
            self.diet_content_lfish_nlom[i] = [self.sediment_nlom[i],
                             self.phytoplankton_nlom[i],
                             self.zoo_nlom[i],
                             self.beninv_nlom[i],
                             self.filterfeeders_nlom[i],
                             self.sfish_nlom[i],
                             self.mfish_nlom[i]]
        self.v_nd_lfish = self.overall_diet_content(self.diet_frac_lfish, self.diet_content_lfish_nlom)

        #large fish water content of diet
        self.diet_content_lfish_water = pd.Series([], dtype = 'float')
        for i in range(len(self.lfish_diet_sediment)):
            self.diet_content_lfish_water[i] = [self.sediment_water[i],
                             self.phytoplankton_water[i],
                             self.zoo_water[i],
                             self.beninv_water[i],
                             self.filterfeeders_water[i],
                             self.sfish_water[i],
                             self.mfish_water[i]]
        self.v_wd_lfish = self.overall_diet_content(self.diet_frac_lfish, self.diet_content_lfish_water)

        # overall diet assimilation factor and egestion rate of fecal matter  Eq a9 GF
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

        #fraction of diet elements (i.e., lipids, NLOM, water) in gut  Eq A9 VLG, VNG, VWG
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

        #partition coefficient of the pesticide between the gatro-intestinal tract and the organism  Eq. A9 (KGB)
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

        #rate constant for elimination of pesticide through excretion of contaminated feces  Eq. A9
        # set value depending on user option for input (either specific by user or calculated internally)
        self.zoo_ke = pd.Series([], dtype = 'float')
        if (self.zoo_ke_temp == 'calculated'):
            self.zoo_ke = self.fecal_elim_rate_const(self.gf_zoo, self.ed_zoo, self.kgb_zoo, self.zoo_wb)
        else:
            self.zoo_ke = float(self.zoo_ke_temp)

        self.beninv_ke = pd.Series([], dtype = 'float')
        if (self.beninv_ke_temp == 'calculated'):
            self.beninv_ke = self.fecal_elim_rate_const(self.gf_beninv, self.ed_beninv, self.kgb_beninv, self.beninv_wb)
        else:
            self.beninv_ke = float(self.beninv_ke_temp)

        self.filterfeeders_ke = pd.Series([], dtype = 'float')
        if (self.filterfeeders_ke_temp == 'calculated'):
            self.filterfeeders_ke = self.fecal_elim_rate_const(self.gf_filterfeeders, self.ed_filterfeeders,
                                                               self.kgb_filterfeeders, self.filterfeeders_wb)
        else:
            self.filterfeeders_ke = float(self.filterfeeders_ke_temp)

        self.sfish_ke = pd.Series([], dtype = 'float')
        if (self.sfish_ke_temp == 'calculated'):
            self.sfish_ke = self.fecal_elim_rate_const(self.gf_sfish, self.ed_sfish, self.kgb_sfish, self.sfish_wb)
        else:
            self.sfish_ke = float(self.sfish_ke_temp)

        self.mfish_ke = pd.Series([], dtype = 'float')
        if (self.mfish_ke_temp == 'calculated'):
            self.mfish_ke = self.fecal_elim_rate_const(self.gf_mfish, self.ed_mfish, self.kgb_mfish, self.mfish_wb)
        else:
            self.mfish_ke = float(self.mfish_ke_temp)

        self.lfish_ke = pd.Series([], dtype = 'float')
        if (self.lfish_ke_temp == 'calculated'):
            self.lfish_ke = self.fecal_elim_rate_const(self.gf_lfish, self.ed_lfish, self.kgb_lfish, self.lfish_wb)
        else:
            self.lfish_ke = float(self.lfish_ke_temp)

        # calculate fraction of overlying water concentration of pesticide that is freely dissolved and can
        # be absorbed via membrane diffusion  Eq A2
        self.phi = pd.Series([], dtype='float')
        self.phi = self.frac_pest_freely_diss()

        #calculate concentration of freely dissolved pesticide in overlying water column  used in Eqs F2 & F4
        self.water_d = pd.Series([], dtype='float')
        self.water_d = self.conc_freely_diss_watercol()

        #calculate pesticide concentration in sediment normalized for organic carbon content  Eq A4a
        self.c_soc = pd.Series([], dtype='float')
        self.c_soc = self.conc_sed_norm_4oc()

        #calculate pesticide concentration in sediment (sediment dry weight basis -- Eq A4)
        self.c_s = pd.Series([], dtype='float')
        self.c_s = self.conc_sed_dry_wgt()

        #calculate diet-based concentrations of aquatic animals/organisms and resulting concentrations in the animal/organism
        #(these need to be done in the order presented here bacuse the diet concentrations accumulate up the food chain
        #the following argument list is used for all aquatic animal/organism concentration calculations
        #calculations are performed with various arguments set to 0.0

            #  pest_conc_organism(self, k1, k2, kD, kE, kG, kM, mP, mO, diet_conc):
            # concentration of pesticide in aquatic animal/organism; this method
            # :unit g/(kg wet weight)
            # :expression Kabam Eq. A1 (CB)
            # :param k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
            # :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
            # :param kD: pesticide uptake rate constant for uptake through ingestion of food (kg food/(kg organism - day)
            # :param kE: rate constant for elimination of the pesticide through excretion of feces (/d)
            # :param kG: animal/organism growth rate constant (/d)
            # :param kM: rate constant for pesticide metabolic transformation (/d)
            # :param mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
            # :param mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
            # :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
            #             via membrane diffusion (fraction)
            # :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
            # :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
            # :param diet_conc: concentration of pesticide in overall diet of aquatic animal/organism (g/kg wet weight)

        #PESTICIDE CONCENTRATION IN ORGANISM AND LIPID NORMALIZED PESTICIDE CONCENTRATION IN ORGANISM

        #phytoplanton
            #because phytoplankton have no diet the (SUM(Pi * Cdi), i.e., diet_conc) portion of Eq. A1 is set to 0.0
        self.out_cb_phytoplankton = self.pest_conc_organism(self.phytoplankton_k1, self.phytoplankton_k2,
                                                self.phytoplankton_kd, self.phytoplankton_ke, self.phytoplankton_kg,
                                                self.phytoplankton_km, self.phytoplankton_mp, self.phytoplankton_mo, 0.0)
        #zooplankton
        self.diet_frac_zoo = pd.Series([], dtype = 'float')
        self.diet_conc_zoo = pd.Series([], dtype = 'float')
        self.total_diet_conc_zoo = pd.Series([], dtype = 'float')
        self.diet_lipid_content_zoo = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_zoo = pd.Series([], dtype = 'float')
        for i in range(len(self.zoo_diet_sediment)):     #loop through model simulation runs
            self.diet_frac_zoo[i] = [self.zoo_diet_sediment[i], self.zoo_diet_phytoplankton[i]]
            self.diet_conc_zoo_[i] = [self.c_s[i], self.cb_phytoplankton[i]]
            self.diet_lipid_content_zoo[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i]]
        self.total_diet_conc_zoo, self.lipid_norm_diet_conc_zoo = self.diet_pest_conc(self.diet_frac_zoo,
                                                                  self.diet_conc_zoo, self.diet_lipid_content_zoo)
        self.out_cb_zoo = self.pest_conc_organism(self.zoo_k1, self.zoo_k2, self.zoo_kd, self.zoo_ke, self.zoo_kg,
                                                  self.zoo_km, self.zoo_mp, self.zoo_mo, self.total_diet_conc_zoo)
 
        #benthic invertebrates
        self.diet_frac_beninv = pd.Series([], dtype = 'float')
        self.diet_conc_beninv = pd.Series([], dtype = 'float')
        self.total_diet_conc_beninv = pd.Series([], dtype = 'float')
        self.diet_lipid_content_beninv = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_beninv = pd.Series([], dtype = 'float')
        for i in range(len(self._beninv_diet_sediment)):     #loop through model simulation runs
            self.diet_frac_beninv[i] = [self._beninv_diet_sediment[i], self._beninv_diet_phytoplankton[i], 
                                        self.beninv_diet_zoo[i]]
            self.diet_conc_beninv_[i] = [self.c_s[i], self.cb_phytoplankton[i], self.cb_zoo[i]]
            self.diet_lipid_content_beninv[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i]]
        self.total_diet_conc_beninv, self.lipid_norm_diet_conc_beninv = self.diet_pest_conc(self.diet_frac__beninv,
                                                                  self.diet_conc__beninv, self.diet_lipid_content__beninv)
        self.out_cb_beninv = self.pest_conc_organism(self._beninv_k1, self._beninv_k2, self._beninv_kd, self._beninv_ke,
                                                      self._beninv_kg, self._beninv_km, self._beninv_mp, self._beninv_mo, 
                                                      self.total_diet_conc__beninv)
 
        #filterfeeders
        self.diet_frac_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_conc_filterfeeders = pd.Series([], dtype = 'float')
        self.total_diet_conc_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_lipid_content_filterfeeders = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_filterfeeders = pd.Series([], dtype = 'float')
        for i in range(len(self._filterfeeders_diet_sediment)):     #loop through model simulation runs
            self.diet_frac_filterfeeders[i] = [self._filterfeeders_diet_sediment[i], self._filterfeeders_diet_phytoplankton[i], 
                                        self.filterfeeders_diet_zoo[i], self.filterfeeders_diet_beninv[i]]
            self.diet_conc_filterfeeders_[i] = [self.c_s[i], self.cb_phytoplankton[i], self.cb_zoo[i], self.cb_beninv[i]]
            self.diet_lipid_content_filterfeeders[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i], self.beninv_lipid_frac[i]]
        self.total_diet_conc_filterfeeders, self.lipid_norm_diet_conc_filterfeeders = self.diet_pest_conc(self.diet_frac__filterfeeders,
                                                                  self.diet_conc__filterfeeders, self.diet_lipid_content__filterfeeders)
        self.out_cb_filterfeeders = self.pest_conc_organism(self._filterfeeders_k1, self._filterfeeders_k2, self._filterfeeders_kd, self._filterfeeders_ke,
                                                      self._filterfeeders_kg, self._filterfeeders_km, self._filterfeeders_mp, self._filterfeeders_mo, 
                                                      self.total_diet_conc__filterfeeders)
 
        #small fish
        self.diet_frac_sfish = pd.Series([], dtype = 'float')
        self.diet_conc_sfish = pd.Series([], dtype = 'float')
        self.total_diet_conc_sfish = pd.Series([], dtype = 'float')
        self.diet_lipid_content_sfish = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_sfish = pd.Series([], dtype = 'float')
        for i in range(len(self._sfish_diet_sediment)):     #loop through model simulation runs
            self.diet_frac_sfish[i] = [self._sfish_diet_sediment[i], self._sfish_diet_phytoplankton[i], 
                                        self.sfish_diet_zoo[i], self.sfish_diet_beninv[i], self.sfish_diet_filterfeeders[i]]
            self.diet_conc_sfish_[i] = [self.c_s[i], self.cb_phytoplankton[i], self.cb_zoo[i], self.cb_beninv[i], self.cb_filterfeeders[i]]
            self.diet_lipid_content_sfish[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i], self.beninv_lipid_frac[i], self.filterfeeders_lipid_frac[i]]
        self.total_diet_conc_sfish, self.lipid_norm_diet_conc_sfish = self.diet_pest_conc(self.diet_frac__sfish,
                                                                  self.diet_conc__sfish, self.diet_lipid_content__sfish)
        self.out_cb_sfish = self.pest_conc_organism(self._sfish_k1, self._sfish_k2, self._sfish_kd, self._sfish_ke,
                                                      self._sfish_kg, self._sfish_km, self._sfish_mp, self._sfish_mo, 
                                                      self.total_diet_conc__sfish)
 
        #medium fish
        self.diet_frac_mfish = pd.Series([], dtype = 'float')
        self.diet_conc_mfish = pd.Series([], dtype = 'float')
        self.total_diet_conc_mfish = pd.Series([], dtype = 'float')
        self.diet_lipid_content_mfish = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_mfish = pd.Series([], dtype = 'float')
        for i in range(len(self._mfish_diet_sediment)):     #loop through model simulation runs
            self.diet_frac_mfish[i] = [self._mfish_diet_sediment[i], self._mfish_diet_phytoplankton[i], 
                                        self.mfish_diet_zoo[i], self.mfish_diet_beninv[i], self.mfish_diet_filterfeeders[i], self.mfish_diet_sfish[i]]
            self.diet_conc_mfish_[i] = [self.c_s[i], self.cb_phytoplankton[i], self.cb_zoo[i], self.cb_beninv[i], self.cb_filterfeeders[i], self.cb_sfish[i]]
            self.diet_lipid_content_mfish[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i], self.beninv_lipid_frac[i], self.filterfeeders_lipid_frac[i], self.sfish_lipid_frac[i]]
        self.total_diet_conc_mfish, self.lipid_norm_diet_conc_mfish = self.diet_pest_conc(self.diet_frac__mfish,
                                                                  self.diet_conc__mfish, self.diet_lipid_content__mfish)
        self.out_cb_mfish = self.pest_conc_organism(self._mfish_k1, self._mfish_k2, self._mfish_kd, self._mfish_ke,
                                                      self._mfish_kg, self._mfish_km, self._mfish_mp, self._mfish_mo, 
                                                      self.total_diet_conc__mfish)
        
        #large fish
        self.diet_frac_lfish = pd.Series([], dtype = 'float')
        self.diet_conc_lfish = pd.Series([], dtype = 'float')
        self.total_diet_conc_lfish = pd.Series([], dtype = 'float')
        self.diet_lipid_content_lfish = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_lfish = pd.Series([], dtype = 'float')
        for i in range(len(self._lfish_diet_sediment)):     #loop through model simulation runs
            self.diet_frac_lfish[i] = [self._lfish_diet_sediment[i], self._lfish_diet_phytoplankton[i], 
                                       self.lfish_diet_zoo[i], self.lfish_diet_beninv[i],
                                       self.lfish_diet_filterfeeders[i], self.lfish_diet_sfish[i],
                                       self.lfish_diet_mfish[i]]
            self.diet_conc_lfish_[i] = [self.c_s[i], self.cb_phytoplankton[i], self.cb_zoo[i], self.cb_beninv[i],
                                        self.cb_filterfeeders[i], self.cb_sfish[i], self.cb_mfish[i]]
            self.diet_lipid_content_lfish[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                                self.zoo_lipid_frac[i], self.beninv_lipid_frac[i],
                                                self.filterfeeders_lipid_frac[i], self.sfish_lipid_frac[i],
                                                self.mfish_lipid_frac[i]]
        self.total_diet_conc_lfish, self.lipid_norm_diet_conc_lfish = self.diet_pest_conc(self.diet_frac__lfish,
                                                                  self.diet_conc__lfish, self.diet_lipid_content__lfish)
        self.out_cb_lfish = self.pest_conc_organism(self._lfish_k1, self._lfish_k2, self._lfish_kd, self._lfish_ke,
                                                    self._lfish_kg, self._lfish_km, self._lfish_mp, self._lfish_mo,
                                                    self.total_diet_conc__lfish)
        
        #LIPID NORMALIZED PESTICIDE TISSUE RESIDUE

        self.out_cbl_phytoplankton = self.lipid_norm_residue_conc(self.out_cb_phytoplankton,self.phytoplankton_lipid)
        self.out_cbl_zoo = self.lipid_norm_residue_conc(self.out_cb_zoo,self.zoo_lipid)
        self.out_cbl_beninv = self.lipid_norm_residue_conc(self.out_cb_beninv,self.beninv_lipid)
        self.out_cbl_filterfeeders = self.lipid_norm_residue_conc(self.out_cb_filterfeeders,self.filterfeeders_lipid)
        self.out_cbl_sfish = self.lipid_norm_residue_conc(self.out_cb_sfish,self.sfish_lipid)
        self.out_cbl_mfish = self.lipid_norm_residue_conc(self.out_cb_mfish,self.mfish_lipid)
        self.out_cbl_lfish = self.lipid_norm_residue_conc(self.out_cb_lfish,self.lfish_lipid)

        #PESTICIDE CONCENTRAITON ORGINATING FROM UPTAKE THROUGH DIET (K1 = 0; non phytoplankton due to lack of diet)
        self.out_cbd_zoo = self.pest_conc_diet_uptake(self.zoo_kd, self.zoo_k2, self.zoo_ke,  self.zoo_kg,
                                                      self.zoo_km, self.total_diet_conc_zoo)
        self.out_cbd_beninv = self.pest_conc_diet_uptake(self.beninv_kd, self.beninv_k2, self.beninv_ke,
                                                      self.beninv_kg, self.beninv_km, self.total_diet_conc_beninv)
        self.out_cbd_filterfeeders = self.pest_conc_diet_uptake(self.filterfeeders_kd, self.filterfeeders_k2, 
                                                      self.filterfeeders_ke,  self.filterfeeders_kg,
                                                      self.filterfeeders_km, self.total_diet_conc_filterfeeders)
        self.out_cbd_sfish = self.pest_conc_diet_uptake(self.sfish_kd, self.sfish_k2, self.sfish_ke,  self.sfish_kg,
                                                      self.sfish_km, self.total_diet_conc_sfish)
        self.out_cbd_mfish = self.pest_conc_diet_uptake(self.mfish_kd, self.mfish_k2, self.mfish_ke,  self.mfish_kg,
                                                      self.mfish_km, self.total_diet_conc_mfish)
        self.out_cbd_lfish = self.pest_conc_diet_uptake(self.lfish_kd, self.lfish_k2, self.lfish_ke,  self.lfish_kg,
                                                      self.lfish_km, self.total_diet_conc_lfish)

        #PESTICIDE CONCENTRATION ORIGINATING FROM UPTAKE THROUGH RESPIRATION (kD = 0)
        self.out_cbr_phytoplankton = self.pest_conc_respir_uptake(self.phytoplankton_k1, self.phytoplankton_k2,
                                                self.phytoplankton_ke, self.phytoplankton_kg,
                                                self.phytoplankton_km, self.phytoplankton_mp, self.phytoplankton_mo)
        self.out_cbr_zoo = self.pest_conc_respir_uptake(self.zoo_k1, self.zoo_k2, self.zoo_ke, self.zoo_kg,
                                                self.zoo_km, self.zoo_mp, self.zoo_mo)
        self.out_cbr_beninv = self.pest_conc_respir_uptake(self.beninv_k1, self.beninv_k2, self.beninv_ke, 
                                                self.beninv_kg,  self.beninv_km, self.beninv_mp, self.beninv_mo)
        self.out_cbr_filterfeeders = self.pest_conc_respir_uptake(self.filterfeeders_k1, self.filterfeeders_k2, 
                                                self.filterfeeders_ke, self.filterfeeders_kg, self.filterfeeders_km,
                                                self.filterfeeders_mp, self.filterfeeders_mo)
        self.out_cbr_sfish = self.pest_conc_respir_uptake(self.sfish_k1, self.sfish_k2, self.sfish_ke, self.sfish_kg,
                                                self.sfish_km, self.sfish_mp, self.sfish_mo)
        self.out_cbr_mfish = self.pest_conc_respir_uptake(self.mfish_k1, self.mfish_k2, self.mfish_ke, self.mfish_kg,
                                                self.mfish_km, self.mfish_mp, self.mfish_mo)
        self.out_cbr_lfish = self.pest_conc_respir_uptake(self.lfish_k1, self.lfish_k2, self.lfish_ke, self.lfish_kg,
                                                self.lfish_km, self.lfish_mp, self.lfish_mo)

        #BIOCONCENTRATION AND BIOMAGNIFICATION FACTORS FOR AQUATIC ANIMALS/ORGANISMS

        #total bioconcentration factor (Table 12)
        self.out_cbf_phytoplankton = self.tot_bioconc_fact(self.phytoplankton_k1, self.phytoplankton_k2,
                                                           self.phytoplankton_mp, self.phytoplankton_mo)
        self.out_cbf_zoo = self.tot_bioconc_fact(self.zoo_k1, self.zoo_k2, self.zoo_mp, self.zoo_mo)
        self.out_cbf_beninv = self.tot_bioconc_fact(self.beninv_k1, self.beninv_k2, self.beninv_mp, self.beninv_mo)
        self.out_cbf_filterfeeders = self.tot_bioconc_fact(self.filterfeeders_k1, self.filterfeeders_k2,
                                                           self.filterfeeders_mp, self.filterfeeders_mo)
        self.out_cbf_sfish = self.tot_bioconc_fact(self.sfish_k1, self.sfish_k2, self.sfish_mp, self.sfish_mo)
        self.out_cbf_mfish = self.tot_bioconc_fact(self.mfish_k1, self.mfish_k2, self.mfish_mp, self.mfish_mo)
        self.out_cbf_lfish = self.tot_bioconc_fact(self.lfish_k1, self.lfish_k2, self.lfish_mp, self.lfish_mo)


        #lipid normalized bionconcentration factor (Table 13)
        self.out_cbfl_phytoplankton = self.lipid_norm_bioconc_fact(self.phytoplankton_k1, self.phytoplankton_k2,
                                                self.phytoplankton_mp, self.phytoplankton_mo, self.phytoplankton_lipid)
        self.out_cbfl_zoo = self.lipid_norm_bioconc_fact(self.zoo_k1, self.zoo_k2,
                                                self.zoo_mp, self.zoo_mo, self.zoo_lipid)
        self.out_cbfl_beninv = self.lipid_norm_bioconc_fact(self.beninv_k1, self.beninv_k2,
                                                self.beninv_mp, self.beninv_mo, self.beninv_lipid)
        self.out_cbfl_filterfeeders = self.lipid_norm_bioconc_fact(self.filterfeeders_k1, self.filterfeeders_k2,
                                                self.filterfeeders_mp, self.filterfeeders_mo, self.filterfeeders_lipid)
        self.out_cbfl_sfish = self.lipid_norm_bioconc_fact(self.sfish_k1, self.sfish_k2,
                                                self.sfish_mp, self.sfish_mo, self.sfish_lipid)
        self.out_cbfl_mfish = self.lipid_norm_bioconc_fact(self.mfish_k1, self.mfish_k2,
                                                self.mfish_mp, self.mfish_mo, self.mfish_lipid)
        self.out_cbfl_lfish = self.lipid_norm_bioconc_fact(self.lfish_k1, self.lfish_k2,
                                                self.lfish_mp, self.lfish_mo, self.lfish_lipid)

        #total bioaccumulation factor (Table 12)
        self.out_cbaf_phytoplankton = self.bioacc_fact(self.out_cb_phytoplankton)
        self.out_cbaf_zoo = self.bioacc_fact(self.out_cb_zoo)
        self.out_cbaf_beninv = self.bioacc_fact(self.out_cb_beninv)
        self.out_cbaf_filterfeeders = self.bioacc_fact(self.out_cb_filterfeeders)
        self.out_cbaf_sfish = self.bioacc_fact(self.out_cb_sfish)
        self.out_cbaf_mfish = self.bioacc_fact(self.out_cb_mfish)
        self.out_cbaf_lfish = self.bioacc_fact(self.out_cb_lfish)
        
        #lipid normalized bioaccumulation factor (Table 13)
        self.out_cbafl_phytoplankton = self.lipid_norm_bioacc_fact(self.out_cb_phytoplankton, self.out_phytoplankton_lipid)
        self.out_cbafl_zoo = self.lipid_norm_bioacc_fact(self.out_cb_zoo, self.out_zoo_lipid)
        self.out_cbafl_beninv = self.lipid_norm_bioacc_fact(self.out_cb_beninv, self.out_beninv_lipid)
        self.out_cbafl_filterfeeders = self.lipid_norm_bioacc_fact(self.out_cb_filterfeeders, self.out_filterfeeders_lipid)
        self.out_cbafl_sfish = self.lipid_norm_bioacc_fact(self.out_cb_sfish, self.out_sfish_lipid)
        self.out_cbafl_mfish = self.lipid_norm_bioacc_fact(self.out_cb_mfish, self.out_mfish_lipid)
        self.out_cbafl_lfish = self.lipid_norm_bioacc_fact(self.out_cb_lfish, self.out_lfish_lipid)

        #biota sediment accumulatoin factor (Table 13)
        self.out_cbsafl_phytoplankton = self.biota_sed_acc_fact(self.out_cb_phytoplankton, self.out_phytoplankton_lipid)
        self.out_cbsafl_zoo = self.biota_sed_acc_fact(self.out_cb_zoo, self.out_zoo_lipid)
        self.out_cbsafl_beninv = self.biota_sed_acc_fact(self.out_cb_beninv, self.out_beninv_lipid)
        self.out_cbsafl_filterfeeders = self.biota_sed_acc_fact(self.out_cb_filterfeeders, self.out_filterfeeders_lipid)
        self.out_cbsafl_sfish = self.biota_sed_acc_fact(self.out_cb_sfish, self.out_sfish_lipid)
        self.out_cbsafl_mfish = self.biota_sed_acc_fact(self.out_cb_mfish, self.out_mfish_lipid)
        self.out_cbsafl_lfish = self.biota_sed_acc_fact(self.out_cb_lfish, self.out_lfish_lipid)

        #biomagnification factor (Table 13 - none for phytoplankton due to lack of diet)
        self.out_bmf_zoo = self.biomag_fact(self.out_cb_zoo, self.out_zoo_lipid, self.lipid_norm_diet_conc_zoo)
        self.out_bmf_beninv = self.biomag_fact(self.out_cb_beninv, self.out_beninv_lipid, self.lipid_norm_diet_conc_beninv)
        self.out_bmf_filterfeeders = self.biomag_fact(self.out_cb_filterfeeders, self.out_filterfeeders_lipid,
                                                      self.lipid_norm_diet_conc_filterfeeders)
        self.out_bmf_sfish = self.biomag_fact(self.out_cb_sfish, self.out_sfish_lipid, self.lipid_norm_diet_conc_sfish)
        self.out_bmf_mfish = self.biomag_fact(self.out_cb_mfish, self.out_mfish_lipid, self.lipid_norm_diet_conc_mfish)
        self.out_bmf_lfish = self.biomag_fact(self.out_cb_lfish, self.out_lfish_lipid, self.lipid_norm_diet_conc_lfish)

        #BEGIN CALCULATIONS FOR DIETARY-BASED AND DOSE-BASED EECs, TOXICITY VALUES, AND RQs

        #CONVERT AQUATIC ORGANISM/ANIMAL PESTICIDE CONCENTRATIONS FROM G/KG WW TO UG/KG WW (AND PLACE IN ARRAY STRUCTURE)
        self.cb_a = np.array([[self.out_cb_phytoplankton, self.out_cb_zoo, self.out_cb_beninv,
                               self.out_cb_filterfeeders, self.out_cb_sfish, self.out_cb_mfish,
                               self.out_cb_lfish]], dtype = 'float')
        self.cb_a2 = self.cb_a * self.gms_to_microgms

        #DRY/WET FOOD INGESTION RATES & DRINKING WATER INTAKE FOR MAMMALS AND BIRDS (TABLE 14)

        #dry food ingestion rates: mammals (Table 14)
        self.dry_food_ingestion_rate_mammals = np.array([], dtype = 'float')
        self.dry_food_ingestion_rate_mammals = self.dry_food_ingest_rate_mammals()
        #trasfer to individual output variables
        self.out_dfir0, self.out_dfir1, self.out_dfir2, self.out_dfir3, \
            self.out_dfir4, self.out_dfir5 =  self.dry_food_ingestion_rate_mammals

        #dry food ingestion rates: birds (Table 14)
        self.dry_food_ingestion_rate_birds = np.array([], dtype = 'float')
        self.dry_food_ingestion_rate_birds = self.dry_food_ingest_rate_birds()
        #trasfer to individual output variables
        self.out_dfira0, self.out_dfira1, self.out_dfira2, self.out_dfira3, \
            self.out_dfira4, self.out_dfira5 =  self.dry_food_ingestion_rate_birds

        self.aq_animal_water_content = np.array([], dtype = 'float')
        self.wet_food_ingestion_rate_mammals = np.array([], dtype = 'float')
        self.wet_food_ingestion_rate_birds = np.array([], dtype = 'float')

        for i in range(len(self.phytoplankton_water)):     #loop through model simulation runs
            self.aq_animal_water_content[i] = [self.phytoplankton_water[i], self.zoo_water[i], self.beninv_water[i],
                             self.filterfeeders_water[i], self.sfish_water[i], self.mfish_water[i], self.lfish_water[i]]

            #wet food ingestion rates: mammals (Table 14)
            self.wet_food_ingestion_rate_mammals[i] = self.wet_food_ingestion_rates(self.self.aq_animal_water_content[i],
                                                   self.diet_mammals, self.dry_food_ingestion_rate_mammals)
            #trasfer to individual output variables
            self.out_wet_food_ingestion_m0[i], self.out_wet_food_ingestion_m1[i], self.out_wet_food_ingestion_m2[i],  \
                    self.out_wet_food_ingestion_m3[i], self.out_wet_food_ingestion_m4[i],  \
                    self.out_wet_food_ingestion_m5[i] = self.wet_food_ingestion_rate_mammals[i]

            #wet food ingestion rates: birds (Table 14)
            self.wet_food_ingestion_rate_birds[i] = self.wet_food_ingestion_rates( self.self.aq_animal_water_content[i],
                                                 self.diet_birds, self.dry_food_ingestion_rate_birds)
            #trasfer to individual output variables
            self.out_wet_food_ingestion_a0[i], self.out_wet_food_ingestion_a1[i], self.out_wet_food_ingestion_a2[i],  \
                    self.out_wet_food_ingestion_a3[i], self.out_wet_food_ingestion_a4[i],  \
                    self.out_wet_food_ingestion_a5[i] = self.wet_food_ingestion_rate_birds[i]

        #drinking water intake rates:mammals (Table 14)
        self.water_ingestion_rate_mammals = np.array([], dtype = 'float')
        self.water_ingestion_rate_mammals = self.drinking_water_intake_mammals()
        #trasfer to individual output variables
        self.out_drinking_water_intake_m0, self.out_drinking_water_intake_m1, self.out_drinking_water_intake_m2, \
            self.out_drinking_water_intake_m3, self.out_drinking_water_intake_m4,   \
            self.out_drinking_water_intake_m5 = self.water_ingestion_rate_mammals

        #drinking water intake rates:birds (Table 14)
        self.water_ingestion_rate_birds = np.array([], dtype = 'float')
        self.water_ingestion_rate_birds = self.drinking_water_intake_birds()
        #trasfer to individual output variables
        self.out_drinking_water_intake_a0, self.out_drinking_water_intake_a1, self.out_drinking_water_intake_a2, \
            self.out_drinking_water_intake_a3, self.out_drinking_water_intake_a4,   \
            self.out_drinking_water_intake_a5 = self.water_ingestion_rate_birds

        # EEC CALCULATIONS FOR MAMMALS AND BIRDS (TABLE 14)

        #dose_based EECs: Mammals
        self.dose_based_eec_mammals = np.array([], dtype = 'float')
        self.dose_based_eec_mammals = self.dose_based_eec(self.cb_a2, self.diet_mammals, self.wet_food_ingestion_rate_mammals,
                                self.water_ingestion_rate_mammals, self.mammal_weights)
        #transfer to individual output variables
        self.out_db40,self.out_db41,self.out_db42,self.out_db43,self.out_db44,self.out_db45 = self.dose_based_eec_mammals

        #dose-based EECs: Birds (TABLE 14)
        dose_based_eec_birds = np.array([], dtype = 'float')
        dose_based_eec_birds = self.dose_based_eec(self.cb_a2, self.diet_birds, self.wet_food_ingestion_rate_birds,
                                self.water_ingestion_rate_birds, self.bird_weights)
        #transfer to individual output variables
        self.out_db4a0,self.out_db4a1,self.out_db4a2,self.out_db4a3,self.out_db4a4,self.out_db4a5 = dose_based_eec_birds

        #dietary-based EECs: Mammals (TABLE 14)
        self.diet_based_eec_mammals = np.array([], dtype = 'float')
        self.diet_based_eec_mammals = self.dietary_based_eec(self.cb_a2, self.diet_mammals)
        #transfer to individual output variables
        self.out_db50,self.out_db51,self.out_db52,self.out_db53,self.out_db54,self.out_db55 = self.diet_based_eec_mammals

        #dietary-based EECs: Birds (TABLE 14)
        self.diet_based_eec_birds = np.array([], dtype = 'float')
        self.diet_based_eec_birds = self.dietary_based_eec(self.cb_a2, self.diet_birds)
        #transfer to individual output variables
        self.out_db5a0,self.out_db5a1,self.out_db5a2,self.out_db5a3,self.out_db5a4,self.out_db5a5 = self.diet_based_eec_birds
        
        #TOXICITY VALUES FOR MAMMALS AND BIRDS (TABLE 15)

        #adjusted/acute dose-based toxicity for mammals (TABLE 15)
        self.dose_based_tox_mammals = np.array([], dtype = 'float')
        for i in range(len(self.species_of_the_tested_mammal)):   #loop through model simulation runs
            if (self.species_of_the_tested_mammal[i] == 'rat'):
                tested_bw = self.bw_rat
            else:
                tested_bw = self.bw_other_mammal
            self.dose_based_tox_mammals[i] = self.acute_dose_based_tox_mammals(self.mammalian_ld50[i], tested_bw)
        self.out_acute_dose_based_m0,self.out_acute_dose_based_m1,self.out_acute_dose_based_m2,\
            self.out_acute_dose_based_m3, self.out_acute_dose_based_m4,\
            self.out_acute_dose_based_m5 = self.acute_dose_based_tox_mammals

        #adjusted/acute diet-based toxicity for mammals - all are equal to the mammalian_lc50 value IF PROVIDED(Table 15)
        self.out_acute_diet_based_m0 = self.out_acute_diet_based_m1 = self.out_acute_diet_based_m2 =  \
            self.out_acute_diet_based_m3 = self.out_acute_diet_based_m4 =\
            self.out_acute_diet_based_m5 = self.mammalian_lc50

        #chronic dose-based toxicity for mammals (TABLE 15)
        self.chronic_dose_based_tox_mamm = np.array([], dtype = 'float')
        for i in range(len(self.species_of_the_tested_mammal)):   #loop through model simulation runs
            if (self.species_of_the_tested_mammal[i] == 'rat'):
                tested_bw = self.bw_rat[i]
            else:
                tested_bw = self.bw_other_mammal[i]
            self.chronic_dose_based_tox_mamm[i] = self.chronic_dose_based_tox_mammals(
                                                                    self.mammalian_chronic_endpoint[i], 
                                                                    self.mammalian_chronic_endpoint_unit[i], tested_bw)
        self.out_chronic_dose_based_m0,self.out_chronic_dose_based_m1,self.out_chronic_dose_based_m2,\
            self.out_chronic_dose_based_m3, self.out_chronic_dose_based_m4,\
            self.out_chronic_dose_based_m5 = self.chronic_dose_based_tox_mammals

        #Chronic diet-based toxicity for mammals (Table 15)
        self.chronic_diet_based_tox_mamm = np.array([], dtype = 'float')
        for i in range(len(self.mammalian_chronic_endpoint)):
            self.chronic_diet_based_tox_mamm = self.chronic_diet_based_tox_mammals(
                                              self.mammalian_chronic_endpoint[i],
                                              self.mammalian_chronic_endpoint_unit[i])
        self.out_chronic_diet_based_tox_m0, self.out_chronic_diet_based_tox_m1, self.out_chronic_diet_based_tox_m2, \
            self.out_chronic_diet_based_tox_m3, self.out_chronic_diet_based_tox_m4, \
            self.out_chronic_diet_based_tox_m5 = self.chronic_diet_based_tox_mamm

        #adjusted/acute dose-based toxicity for birds (TABLE 15)
        self.dose_based_tox_birds = np.array([], dtype = 'float')
        for i in range(len(self.species_of_the_tested_bird)):   #loop through model simulation runs
            if (self.species_of_the_tested_bird[i] == 'quail'):
                tested_bw = self.bw_quail
            elif (self.species_of_the_tested_bird == 'duck'):
                tested_bw = self.bw_duck
            else:
                tested_bw = self.bw_other_bird
            self.dose_based_tox_birds[i] = self.acute_dose_based_tox_birds(self.avian_ld50, tested_bw,
                                                                           self.mineau_scaling_factor[i])
        self.out_acute_dose_based_a0,self.out_acute_dose_based_a1,self.out_acute_dose_based_a2,\
            self.out_acute_dose_based_a3, self.out_acute_dose_based_a4,\
            self.out_acute_dose_based_a5 = self.acute_dose_based_tox_birds

        #adjusted/acute diet-based toxicity for birds - all are equal to the avian_lc50 value(Table 15)
        self.out_acute_diet_based_a0 = self.out_acute_diet_based_a1 = self.out_acute_diet_based_a2 =  \
            self.out_acute_diet_based_a3 = self.out_acute_diet_based_a4 =\
            self.out_acute_diet_based_a5 = self.avian_lc50

        #Note: There is no chronic dosed-based toxicity for birds

        #chronic diet-based toxicity for birds - all are equal to the avian_noaec value(Table 15)
        self.out_chronic_diet_based_a0 = self.out_chronic_diet_based_a1 = self.out_chronic_diet_based_a2 =\
            self.out_chronic_diet_based_a3 = self.out_chronic_diet_based_a4 =\
            self.out_chronic_diet_based_a5 = self.avian_noaec


        #CALCULATE RISK QUOTIENTS FOR MAMMALS AND BIRDS (TABLE 16)

        #Acute dose-based risk quotient for mammals (Table 16)
        self.acute_dose_based_rq_mammals = np.array([], dtype = 'float')
        self.acute_dose_based_rq_mammals = self.acute_rq_dose_mammals()
        self.out_acute_rq_dose_m0, self.out_acute_rq_dose_m1, self.out_acute_rq_dose_m2, self.out_acute_rq_dose_m3, \
            self.out_acute_rq_dose_m4, self.out_acute_rq_dose_m5 = self.acute_dose_based_rq_mammals

        #Chronic dose-based risk quotient for mammals (Table 16)
        self.chronic_dose_based_rq_mammals = np.array([], dtype = 'float')
        self.chronic_dose_based_rq_mammals = self.chronic_rq_dose_mammals()
        self.out_chronic_rq_dose_m0, self.out_chronic_rq_dose_m1, self.out_chronic_rq_dose_m2, self.out_chronic_rq_dose_m3, \
            self.out_chronic_rq_dose_m4, self.out_chronic_rq_dose_m5 = self.chronic_dose_based_rq_mammals

        #Acute diet-based risk quotient for mammals (Table 16)
                    #Note: when a value for mammalian_lc50 is not availble the OPP spreadsheet enters 'N/A'
                    #this doesn't work well in the python code because numpy arrays need to be homogeneous in datatype
                    #so, for now anyway I recommend that the appropriate cell in the ubertool input spreadsheet be blank
                    # rather than inserting a 'N/A'; the blank will be processed as 'nan' rather than 'N/A'
        self.acute_diet_based_rq_mammals = np.array([], dtype = 'float')
        for i in range(len(self.mammalian_lc50)):
            self.acute_diet_based_rq_mammals[i] = self.acute_rq_diet_mammals(self.diet_based_eec_mammals[i],
                                                                             self.mammalian_lc50[i])
        self.out_acute_rq_diet_m0, self.out_acute_rq_diet_m1, self.out_acute_rq_diet_m2, self.out_acute_rq_diet_m3, \
            self.out_acute_rq_diet_m4, self.out_acute_rq_diet_m5 = self.acute_diet_based_rq_mammals

        #Chronic diet-based risk quotient for mammals (Table 16)
        self.chronic_diet_based_rq_mammals = np.array([], dtype = 'float')
        for i in range(len(self.mammalian_chronic_endpoint)):
            self.chronic_diet_based_rq_mammals = self.chronic_rq_diet_mammals(self.diet_based_eec_mammals[i],
                                                 self.mammalian_chronic_endpoint[i],
                                                 self.mammalian_chronic_endpoint_unit[i])
        self.out_chronic_rq_diet_m0, self.out_chronic_rq_diet_m1, self.out_chronic_rq_diet_m2, \
            self.out_chronic_rq_diet_m3, self.out_chronic_rq_diet_m4, \
            self.out_chronic_rq_diet_m5 = self.chronic_diet_based_rq_mammals

        #Acute dose-based risk quotient for birds (Table 16)
        self.acute_dose_based_rq_birds = np.array([], dtype = 'float')
        self.acute_dose_based_rq_birds = self.acute_rq_dose_birds()
        self.out_acute_rq_dose_a0, self.out_acute_rq_dose_a1, self.out_acute_rq_dose_a2, self.out_acute_rq_dose_a3, \
            self.out_acute_rq_dose_a4, self.out_acute_rq_dose_a5 = self.acute_dose_based_rq_birds

        #Acute diet-based for risk quotient birds (Table 16)
        self.acute_diet_based_rq_birds = np.array([], dtype = 'float')
        for i in range(len(self.avian_lc50)):  #loop through model simulation runs
            self.chronic_diet_based_rq_birds = self.acute_rq_diet_birds(self.diet_based_eec_birds[i],
                                                 self.avian_lc50[i])
        self.out_acute_rq_diet_m0, self.out_acute_rq_diet_a1, self.out_acute_rq_diet_a2, \
            self.out_acute_rq_diet_a3, self.out_acute_rq_diet_a4, \
            self.out_acute_rq_diet_a5 = self.acute_diet_based_rq_birds

        #Note: There is no chronic dosed-based risk quotient for birds

        #Chronic diet-based for risk quotient birds (Table 16)
        self.chronic_diet_based_rq_birds = np.array([], dtype = 'float')
        for i in range(len(self.avian_noaec)):  #loop through model simulation runs
            self.chronic_diet_based_rq_birds = self.chronic_rq_diet_birds(self.diet_based_eec_birds[i],
                                                 self.avian_noaec[i])
        self.out_chronic_rq_diet_m0, self.out_chronic_rq_diet_a1, self.out_chronic_rq_diet_a2, \
            self.out_chronic_rq_diet_a3, self.out_chronic_rq_diet_a4, \
            self.out_chronic_rq_diet_a5 = self.chronic_diet_based_rq_birds

    def set_global_constants(self):

        # list of aquatic animals in the food chain from lowest to highest trophic level
        #(data in related arrays will reflect this order)
        self.aquatic_animals = np.array(['pytoplankton', 'zooplankton', 'benthic_invertebrates', 'filterfeeders',
                                          'small_fish', 'medium_fish', 'large_fish'], dtype = 'str')

        #list of mammals (data in related arrays will reflect this order)
        self.mammals = np.array(['fog/water shrew', 'rice rat/nosed mole', 'small mink', 'large mink',
                                 'small river otter', 'large river otter'], dtype = 'str')
        self.mammal_weights = np.array([0.018, 0.085, 0.45, 1.8, 5., 15.], dtype = 'float')
        self.diet_mammals = np.array([[0, 0, 1., 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1., 0],
                                      [0, 0, 0, 0, 0, 1., 0], [0, 0, 0, 0, 0, 1., 0], [0, 0, 0, 0, 0, 0, 1.]], dtype = 'float')
        #transfer mammal weights to output variable
        self.out_mweight0, self.out_mweight1, self.out_mweight2, self.out_mweight3, \
        self.out_mweight4, self.out_mweight5 = self.mammal_weights

        #list of birds (data in related arrays will reflect this order)
        self.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons', 'small osprey', 'white pelican'], dtype = 'str')
        self.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5], dtype = 'float')
        self.diet_birds = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0],
                                    [0, 0, 0.5, 0, 0.5, 0, 0], [0, 0, 0.5, 0, 0, 0.5, 0],
                                    [0, 0, 0, 0, 0, 1., 0], [0, 0, 0, 0, 0, 0, 1.]], dtype = 'float')
        #transfer bird weights to output variable
        self.out_aweight0, self.out_aweight1, self.out_aweight2, self.out_aweight3, \
        self.out_aweight4, self.out_aweight5 = self.bird_weights

        # conversions

        self.kow = pd.Series([], dtype = 'float')
        self.sediment_oc_frac = pd.Series([], dtype = 'float')

        self.kow = 10.**(self.log_kow) # convert log kow to kow
        self.sediment_oc_frac = self.percent_to_frac(self.sediment_oc)

        self.gms_to_microgms = 1.e6

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
