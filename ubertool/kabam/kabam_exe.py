from __future__ import division
import numpy as np
import os.path
import pandas as pd
import sys

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from base.uber_model import UberModel, ModelSharedInputs
from kabam_functions import KabamFunctions

class KabamInputs(ModelSharedInputs):
    """
    Required inputs class for Kabam.
    """

    def __init__(self):
        """Class representing the inputs for Kabam"""
        super(KabamInputs, self).__init__()
        #Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.version = pd.Series([], dtype='object')
        self.chemical_name = pd.Series([], dtype='object')
        self.pc_code = pd.Series([], dtype='object')

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

        self.species_of_the_tested_bird = pd.Series([], dtype='object')
        self.bw_quail = pd.Series([], dtype='float')
        self.bw_duck = pd.Series([], dtype='float')
        self.bw_other_bird = pd.Series([], dtype='float')
            # not sure why this construct is here
            # if Species_of_the_tested_bird == '178':
            #     self.bw_bird = pd.Series([], dtype='float')
            # elif Species_of_the_tested_bird == '1580':
            #     self.bw_bird = pd.Series([], dtype='float')
            # else:
            #     self.bw_bird = pd.Series([], dtype='float')
        self.avian_ld50 = pd.Series([], dtype='float')
        self.avian_lc50 = pd.Series([], dtype='float')
        self.avian_noaec = pd.Series([], dtype='float')
        self.species_of_the_tested_mammal = pd.Series([], dtype='object')
        self.bw_rat = pd.Series([], dtype='float')
        self.bw_other_mammal = pd.Series([], dtype='float')
            # not sure why this construct is here
            # if m_species == '350':
            #     self.bw_mamm = pd.Series([], dtype='float')
            # else:
            #     self.bw_mamm = pd.Series([], dtype='float')
        self.mammalian_ld50 = pd.Series([], dtype='float')
        self.mammalian_lc50 = pd.Series([], dtype='float')
        self.mammalian_chronic_endpoint = pd.Series([], dtype='float')
        self.mammalian_chronic_endpoint_unit = pd.Series([], dtype='object') #added variable

        self.lfish_diet_sediment = pd.Series([], dtype='float')
        self.lfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.lfish_diet_zooplankton = pd.Series([], dtype='float')
        self.lfish_diet_beninv = pd.Series([], dtype='float')
        self.lfish_diet_filterfeeders = pd.Series([], dtype='float')
        self.lfish_diet_sfish = pd.Series([], dtype='float')
        self.lfish_diet_mfish = pd.Series([], dtype='float')
        self.mfish_diet_sediment = pd.Series([], dtype='float')
        self.mfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.mfish_diet_zooplankton = pd.Series([], dtype='float')
        self.mfish_diet_beninv = pd.Series([], dtype='float')
        self.mfish_diet_filterfeeders = pd.Series([], dtype='float')
        self.mfish_diet_sfish = pd.Series([], dtype='float')
        self.sfish_diet_sediment = pd.Series([], dtype='float')
        self.sfish_diet_phytoplankton = pd.Series([], dtype='float')
        self.sfish_diet_zooplankton = pd.Series([], dtype='float')
        self.sfish_diet_beninv = pd.Series([], dtype='float')
        self.sfish_diet_filterfeeders = pd.Series([], dtype='float')
        self.filterfeeders_diet_sediment = pd.Series([], dtype='float')
        self.filterfeeders_diet_phytoplankton = pd.Series([], dtype='float')
        self.filterfeeders_diet_zooplankton = pd.Series([], dtype='float')
        self.filterfeeders_diet_beninv = pd.Series([], dtype='float')
        self.beninv_diet_sediment = pd.Series([], dtype='float')
        self.beninv_diet_phytoplankton = pd.Series([], dtype='float')
        self.beninv_diet_zooplankton = pd.Series([], dtype='float')
        self.zoo_diet_sediment = pd.Series([], dtype='float')
        self.zoo_diet_phytoplankton = pd.Series([], dtype='float')

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

        #following rate constants may be input as numerical value or specified to be 'calculated'
        #these inputs are read in as string objects (with _temp extension) and converted as appropriate internally
        self.phytoplankton_k1_temp = pd.Series([], dtype='object')
        self.phytoplankton_k2_temp = pd.Series([], dtype='object')
        self.phytoplankton_kd_temp = pd.Series([], dtype='object')
        self.phytoplankton_ke_temp = pd.Series([], dtype='object')
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
        self.zoo_km = pd.Series([], dtype='float')
        self.beninv_km = pd.Series([], dtype='float')
        self.filterfeeders_km = pd.Series([], dtype='float')
        self.sfish_km = pd.Series([], dtype='float')
        self.mfish_km = pd.Series([], dtype='float')
        self.lfish_km = pd.Series([], dtype='float')

        self.rate_constants = pd.Series([], dtype='object')
        self.sediment_respire = pd.Series([], dtype='object')
        self.phyto_respire = pd.Series([], dtype='object')
        self.zoo_respire = pd.Series([], dtype='object')
        self.beninv_respire = pd.Series([], dtype='object')
        self.filterfeeders_respire = pd.Series([], dtype='object')
        self.sfish_respire = pd.Series([], dtype='object')
        self.mfish_respire = pd.Series([], dtype='object')
        self.lfish_respire = pd.Series([], dtype='object')

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
        self.out_cb_filterfeeders = pd.Series([], dtype = 'float', name="out_cb_filterfeeders")
        self.out_cb_sfish = pd.Series([], dtype = 'float', name="out_cb_sfish")
        self.out_cb_mfish = pd.Series([], dtype = 'float', name="out_cb_mfish")
        self.out_cb_lfish = pd.Series([], dtype = 'float', name="out_cb_lfish")
        self.out_cbl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbl_phytoplankton")
        self.out_cbl_zoo = pd.Series([], dtype = 'float', name="out_cbl_zoo")
        self.out_cbl_beninv = pd.Series([], dtype = 'float', name="out_cbl_beninv")
        self.out_cbl_filterfeeders = pd.Series([], dtype = 'float', name="out_cbl_filterfeeders")
        self.out_cbl_sfish = pd.Series([], dtype = 'float', name="out_cbl_sfish")
        self.out_cbl_mfish = pd.Series([], dtype = 'float', name="out_cbl_mfish")
        self.out_cbl_lfish = pd.Series([], dtype = 'float', name="out_cbl_lfish")
        self.out_cbd_zoo = pd.Series([], dtype = 'float', name="out_cbd_zoo")
        self.out_cbd_beninv = pd.Series([], dtype = 'float', name="out_cbd_beninv")
        self.out_cbd_filterfeeders = pd.Series([], dtype = 'float', name="out_cbd_filterfeeders")
        self.out_cbd_sfish = pd.Series([], dtype = 'float', name="out_cbd_sfish")
        self.out_cbd_mfish = pd.Series([], dtype = 'float', name="out_cbd_mfish")
        self.out_cbd_lfish = pd.Series([], dtype = 'float', name="out_cbd_lfish")
        self.out_cbr_phytoplankton = pd.Series([], dtype = 'float', name="out_cbr_phytoplankton")
        self.out_cbr_zoo = pd.Series([], dtype = 'float', name="out_cbr_zoo")
        self.out_cbr_beninv = pd.Series([], dtype = 'float', name="out_cbr_beninv")
        self.out_cbr_filterfeeders = pd.Series([], dtype = 'float', name="out_cbr_filterfeeders")
        self.out_cbr_sfish = pd.Series([], dtype = 'float', name="out_cbr_sfish")
        self.out_cbr_mfish = pd.Series([], dtype = 'float', name="out_cbr_mfish")
        self.out_cbr_lfish = pd.Series([], dtype = 'float', name="out_cbr_lfish")
        self.out_cbf_phytoplankton = pd.Series([], dtype = 'float', name="out_cbf_phytoplankton")
        self.out_cbf_zoo = pd.Series([], dtype = 'float', name="out_cbf_zoo")
        self.out_cbf_beninv = pd.Series([], dtype = 'float', name="out_cbf_beninv")
        self.out_cbf_filterfeeders = pd.Series([], dtype = 'float', name="out_cbf_filterfeeders")
        self.out_cbf_sfish = pd.Series([], dtype = 'float', name="out_cbf_sfish")
        self.out_cbf_mfish = pd.Series([], dtype = 'float', name="out_cbf_mfish")
        self.out_cbf_lfish = pd.Series([], dtype = 'float', name="out_cbf_lfish")
        self.out_cbaf_phytoplankton = pd.Series([], dtype = 'float', name="out_cbaf_phytoplankton")
        self.out_cbaf_zoo = pd.Series([], dtype = 'float', name="out_cbaf_zoo")
        self.out_cbaf_beninv = pd.Series([], dtype = 'float', name="out_cbaf_beninv")
        self.out_cbaf_filterfeeders = pd.Series([], dtype = 'float', name="out_cbaf_filterfeeders")
        self.out_cbaf_sfish = pd.Series([], dtype = 'float', name="out_cbaf_sfish")
        self.out_cbaf_mfish = pd.Series([], dtype = 'float', name="out_cbaf_mfish")
        self.out_cbaf_lfish = pd.Series([], dtype = 'float', name="out_cbaf_lfish")
        self.out_cbfl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbfl_phytoplankton")
        self.out_cbfl_zoo = pd.Series([], dtype = 'float', name="out_cbfl_zoo")
        self.out_cbfl_beninv = pd.Series([], dtype = 'float', name="out_cbfl_beninv")
        self.out_cbfl_filterfeeders = pd.Series([], dtype = 'float', name="out_cbfl_filterfeeders")
        self.out_cbfl_sfish = pd.Series([], dtype = 'float', name="out_cbfl_sfish")
        self.out_cbfl_mfish = pd.Series([], dtype = 'float', name="out_cbfl_mfish")
        self.out_cbfl_lfish = pd.Series([], dtype = 'float', name="out_cbfl_lfish")
        self.out_cbafl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbafl_phytoplankton")
        self.out_cbafl_zoo = pd.Series([], dtype = 'float', name="out_cbafl_zoo")
        self.out_cbafl_beninv = pd.Series([], dtype = 'float', name="out_cbafl_beninv")
        self.out_cbafl_filterfeeders = pd.Series([], dtype = 'float', name="out_cbafl_filterfeeders")
        self.out_cbafl_sfish = pd.Series([], dtype = 'float', name="out_cbafl_sfish")
        self.out_cbafl_mfish = pd.Series([], dtype = 'float', name="out_cbafl_mfish")
        self.out_cbafl_lfish = pd.Series([], dtype = 'float', name="out_cbafl_lfish")
        self.out_bmf_zoo = pd.Series([], dtype = 'float', name="out_bmf_zoo")
        self.out_bmf_beninv = pd.Series([], dtype = 'float', name="out_bmf_beninv")
        self.out_bmf_filterfeeders = pd.Series([], dtype = 'float', name="out_bmf_filterfeeders")
        self.out_bmf_sfish = pd.Series([], dtype = 'float', name="out_bmf_sfish")
        self.out_bmf_mfish = pd.Series([], dtype = 'float', name="out_bmf_mfish")
        self.out_bmf_lfish = pd.Series([], dtype = 'float', name="out_bmf_lfish")
        self.out_cbsafl_phytoplankton = pd.Series([], dtype = 'float', name="out_cbsafl_phytoplankton")
        self.out_cbsafl_zoo = pd.Series([], dtype = 'float', name="out_cbsafl_zoo")
        self.out_cbsafl_beninv = pd.Series([], dtype = 'float', name="out_cbsafl_beninv")
        self.out_cbsafl_filterfeeders = pd.Series([], dtype = 'float', name="out_cbsafl_filterfeeders")
        self.out_cbsafl_sfish = pd.Series([], dtype = 'float', name="out_cbsafl_sfish")
        self.out_cbsafl_mfish = pd.Series([], dtype = 'float', name="out_cbsafl_mfish")
        self.out_cbsafl_lfish = pd.Series([], dtype = 'float', name="out_cbsafl_lfish")
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

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Run the model's methods to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

    def run_methods(self):
        """
        Execute all subroutines in proper order.
        :return:
        """

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()

        # set fraction of respiratory ventilation that involves pore-water of sediment
        self.phytoplankton_mo = pd.Series([], dtype='float')
        self.phytoplankton_mp = pd.Series([], dtype='float')
        self.zoo_mo = pd.Series([], dtype='float')
        self.zoo_mp = pd.Series([], dtype='float')
        self.beninv_mo = pd.Series([], dtype='float')
        self.beninv_mp = pd.Series([], dtype='float')
        self.filterfeeders_mo = pd.Series([], dtype='float')
        self.filterfeeders_mp = pd.Series([], dtype='float')
        self.sfish_mo = pd.Series([], dtype='float')
        self.sfish_mp = pd.Series([], dtype='float')
        self.mfish_mo = pd.Series([], dtype='float')
        self.mfish_mp = pd.Series([], dtype='float')
        self.lfish_mo = pd.Series([], dtype='float')
        self.lfish_mp = pd.Series([], dtype='float')

        for i in range(self.num_simulations):
            self.phytoplankton_mp[i] = self.zoo_mp[i] = self.beninv_mp[i] = self.filterfeeders_mp[i] =  \
            self.sfish_mp[i] = self.mfish_mp[i] = self.lfish_mp[i] = 0.0

            if (self.phyto_respire[i] == 'yes'): self.phytoplankton_mp[i] = 0.05
            if (self.zoo_respire[i] == 'yes'): self.zoo_mp[i] = 0.05
            if (self.beninv_respire[i] == 'yes'): self.beninv_mp[i] = 0.05
            if (self.filterfeeders_respire[i] == 'yes'): self.filterfeeders_mp[i] = 0.05
            if (self.sfish_respire[i] == 'yes'): self.sfish_mp[i] = 0.05
            if (self.mfish_respire[i] == 'yes'): self.mfish_mp[i] = 0.05
            if (self.lfish_respire[i] == 'yes'): self.lfish_mp[i] = 0.05

            self.phytoplankton_mo[i] = 1. - self.phytoplankton_mp[i]
            self.zoo_mo[i] = 1. - self.zoo_mp[i]
            self.beninv_mo[i] = 1. - self.beninv_mp[i]
            self.filterfeeders_mo[i] = 1. - self.filterfeeders_mp[i]
            self.sfish_mo[i] = 1. - self.sfish_mp[i]
            self.mfish_mo[i] = 1. - self.mfish_mp[i]
            self.lfish_mo[i] = 1. - self.lfish_mp[i]


        # aquatic animal ventilation rates (Kabam Eq. A5.2b)
        self.gv_zoo = self.ventilation_rate(self.zoo_wb)
        self.gv_beninv = self.ventilation_rate(self.beninv_wb)
        self.gv_filterfeeders = self.ventilation_rate(self.filterfeeders_wb)
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
        self.zoo_k1 = pd.Series([], dtype = 'float')
        self.beninv_k1 = pd.Series([], dtype = 'float')
        self.filterfeeders_k1 = pd.Series([], dtype = 'float')
        self.sfish_k1 = pd.Series([], dtype = 'float')
        self.mfish_k1 = pd.Series([], dtype = 'float')
        self.lfish_k1 = pd.Series([], dtype = 'float')

        for i in range(self.num_simulations):
            if (self.phytoplankton_k1_temp[i] == 'calculated'):
                self.phytoplankton_k1[i] = self.phytoplankton_k1_calc(self.kow[i])
            else:
                self.phytoplankton_k1[i] = float(self.phytoplankton_k1_temp[i])

            if (self.zoo_k1_temp[i]  == 'calculated'):
                self.zoo_k1[i]  = self.aq_animal_k1_calc(self.ew_zoo[i] , self.gv_zoo[i] , self.zoo_wb[i] )
            else:
                self.zoo_k1[i]  = float(self.zoo_k1_temp[i] )

            if (self.beninv_k1_temp[i] == 'calculated'):
                self.beninv_k1[i] = self.aq_animal_k1_calc(self.ew_beninv[i], self.gv_beninv[i], self.beninv_wb[i])
            else:
                self.beninv_k1[i] = float(self.beninv_k1_temp[i])

            if (self.filterfeeders_k1_temp[i] == 'calculated'):
                self.filterfeeders_k1[i] = self.aq_animal_k1_calc(self.ew_filterfeeders[i], self.gv_filterfeeders[i],
                                                               self.filterfeeders_wb[i])
            else:
                self.filterfeeders_k1[i] = float(self.filterfeeders_k1_temp[i])

            if (self.sfish_k1_temp[i] == 'calculated'):
                self.sfish_k1[i] = self.aq_animal_k1_calc(self.ew_sfish[i], self.gv_sfish[i], self.sfish_wb[i])
            else:
                self.sfish_k1[i] = float(self.sfish_k1_temp[i])

            if (self.mfish_k1_temp[i] == 'calculated'):
                self.mfish_k1[i] = self.aq_animal_k1_calc(self.ew_mfish[i], self.gv_mfish[i], self.mfish_wb[i])
            else:
                self.mfish_k1[i] = float(self.mfish_k1_temp[i])

            if (self.lfish_k1_temp[i] == 'calculated'):
                self.lfish_k1[i] = self.aq_animal_k1_calc(self.ew_lfish[i], self.gv_lfish[i], self.lfish_wb[i])
            else:
                self.lfish_k1[i] = float(self.lfish_k1_temp[i])

        #Aquatic animal-Water partition coeficient (Kabam Eq. A6a)
        # beta_* represent the proportionality constant expressing the sorption capacity of NLOM to that of octanol
        self.k_bw_phytoplankton = pd.Series([], dtype='float')
        self.k_bw_zoo =pd.Series([], dtype='float')
        self.k_bw_beninv = pd.Series([], dtype='float')
        self.k_bw_filterfeeders = pd.Series([], dtype='float')
        self.k_bw_sfish = pd.Series([], dtype='float')
        self.k_bw_mfish = pd.Series([], dtype='float')
        self.k_bw_lfish = pd.Series([], dtype='float')

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
        self.zoo_k2 = pd.Series([], dtype = 'float')
        self.beninv_k2 = pd.Series([], dtype = 'float')
        self.filterfeeders_k2 = pd.Series([], dtype = 'float')
        self.sfish_k2 = pd.Series([], dtype = 'float')
        self.mfish_k2 = pd.Series([], dtype = 'float')
        self.lfish_k2 = pd.Series([], dtype = 'float')

        for i in range(self.num_simulations):
            if (self.phytoplankton_k2_temp[i] == 'calculated'):
                self.phytoplankton_k2[i] = self.aq_animal_k2_calc(self.phytoplankton_k1[i], self.k_bw_phytoplankton[i])
            else:
                self.phytoplankton_k2[i] = float(self.phytoplankton_k2_temp[i])

            if (self.zoo_k2_temp[i] == 'calculated'):
                self.zoo_k2[i] = self.aq_animal_k2_calc(self.zoo_k1[i], self.k_bw_zoo[i])
            else:
                self.zoo_k2[i] = float(self.zoo_k2_temp[i])

            if (self.beninv_k2_temp[i] == 'calculated'):
                self.beninv_k2[i] = self.aq_animal_k2_calc(self.beninv_k1[i], self.k_bw_beninv[i])
            else:
                self.beninv_k2[i] = float(self.beninv_k2_temp[i])

            if (self.filterfeeders_k2_temp[i] == 'calculated'):
                self.filterfeeders_k2[i] = self.aq_animal_k2_calc(self.filterfeeders_k1[i], self.k_bw_filterfeeders[i])
            else:
                self.filterfeeders_k2[i] = float(self.filterfeeders_k2_temp[i])

            if (self.sfish_k2_temp[i] == 'calculated'):
                self.sfish_k2[i] = self.aq_animal_k2_calc(self.sfish_k1[i], self.k_bw_sfish[i])
            else:
                self.sfish_k2[i] = float(self.sfish_k2_temp[i])

            if (self.mfish_k2_temp[i] == 'calculated'):
                self.mfish_k2[i] = self.aq_animal_k2_calc(self.mfish_k1[i], self.k_bw_mfish[i])
            else:
                self.mfish_k2[i] = float(self.mfish_k2_temp[i])

            if (self.lfish_k2_temp[i] == 'calculated'):
                self.lfish_k2[i] = self.aq_animal_k2_calc(self.lfish_k1[i], self.k_bw_lfish[i])
            else:
                self.lfish_k2[i] = float(self.lfish_k2_temp[i])

        # aquatic animal/organism growth rate constants (Kabam Eq. A7.1 & A7.2)
        self.phytoplankton_kg = pd.Series([], dtype = 'float')
        self.zoo_kg = pd.Series([], dtype = 'float')
        self.beninv_kg = pd.Series([], dtype = 'float')
        self.filterfeeders_kg = pd.Series([], dtype = 'float')
        self.sfish_kg = pd.Series([], dtype = 'float')
        self.mfish_kg = pd.Series([], dtype = 'float')
        self.lfish_kg = pd.Series([], dtype = 'float')

        self.phytoplankton_kg = 0.1 # 0.1 is assigned (not calculated) in OPP model spreadsheet
                                    # in worksheet 'Parameters & Calculations' cell C48
        self.zoo_kg = self.animal_grow_rate_const(self.zoo_wb)
        self.beninv_kg = self.animal_grow_rate_const(self.beninv_wb)
        self.filterfeeders_kg = self.animal_grow_rate_const(self.filterfeeders_wb)
        self.sfish_kg = self.animal_grow_rate_const(self.sfish_wb)
        self.mfish_kg = self.animal_grow_rate_const(self.mfish_wb)
        self.lfish_kg = self.animal_grow_rate_const(self.lfish_wb)

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
        self.gd_zoo = self.aq_animal_feeding_rate(self.zoo_wb)
        self.gd_beninv = self.aq_animal_feeding_rate(self.beninv_wb)
        self.gd_filterfeeders = self.filterfeeders_feeding_rate()
        self.gd_sfish = self.aq_animal_feeding_rate(self.sfish_wb)
        self.gd_mfish = self.aq_animal_feeding_rate(self.mfish_wb)
        self.gd_lfish = self.aq_animal_feeding_rate(self.lfish_wb)

        # dietary uptake rate constant Eq. A8 (kD)
        # set value depending on user option for input (either specific by user or calculated internally)
        self.phytoplankton_kd = pd.Series([], dtype = 'float')
        self.zoo_kd = pd.Series([], dtype = 'float')
        self.beninv_kd = pd.Series([], dtype = 'float')
        self.filterfeeders_kd = pd.Series([], dtype = 'float')
        self.sfish_kd = pd.Series([], dtype = 'float')
        self.mfish_kd = pd.Series([], dtype = 'float')
        self.lfish_kd = pd.Series([], dtype = 'float')

        for i in range(self.num_simulations):
            self.phytoplankton_kd[i] = self.phytoplankton_kd_temp[i]  #should be 0.0 as per Appendix A.5 of Kabam Documentation
            if (self.zoo_kd_temp[i] == 'calculated'):
                self.zoo_kd[i] = self.diet_uptake_rate_const(self.ed_zoo[i], self.gd_zoo[i], self.zoo_wb[i])
            else:
                self.zoo_kd[i] = float(self.zoo_kd_temp[i])

            if (self.beninv_kd_temp[i] == 'calculated'):
                self.beninv_kd[i] = self.diet_uptake_rate_const(self.ed_beninv[i], self.gd_beninv[i], self.beninv_wb[i])
            else:
                self.beninv_kd[i] = float(self.beninv_kd_temp[i])

            if (self.filterfeeders_kd_temp[i] == 'calculated'):
                self.filterfeeders_kd[i] = self.diet_uptake_rate_const(self.ed_filterfeeders[i],
                                                                    self.gd_filterfeeders[i], self.filterfeeders_wb[i])
            else:
                self.filterfeeders_kd[i] = float(self.filterfeeders_kd_temp[i])

            if (self.sfish_kd_temp[i] == 'calculated'):
                self.sfish_kd[i] = self.diet_uptake_rate_const(self.ed_sfish[i], self.gd_sfish[i], self.sfish_wb[i])
            else:
                self.sfish_kd[i] = float(self.sfish_kd_temp[i])

            if (self.mfish_kd_temp[i] == 'calculated'):
                self.mfish_kd[i] = self.diet_uptake_rate_const(self.ed_mfish[i], self.gd_mfish[i], self.mfish_wb[i])
            else:
                self.mfish_kd[i] = float(self.mfish_kd_temp[i])

            if (self.lfish_kd_temp[i] == 'calculated'):
                self.lfish_kd[i] = self.diet_uptake_rate_const(self.ed_lfish[i], self.gd_lfish[i], self.lfish_wb[i])
            else:
                self.lfish_kd[i] = float(self.lfish_kd_temp[i])

        #overall lipid, NLOM, and Water content of aquatic animal/organism diet (associated with Eq A9 VLD, VND, VWD
            #loops reflect stepping through model simulation runs one at a time
            #notes: 1. there is some room here for reduction of code; the 'diet_content_*_*' variable
            #          could be reduced to a single set that is used for each trophic level
            #       2. for future consideration: this processing might be optimized with matrix based calculations

        #zooplankton lipid content of diet
        self.diet_frac_zoo = pd.Series([], dtype = 'float')
        self.diet_content_zoo_lipid = pd.Series([], dtype = 'float')
        self.v_ld_zoo = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_frac_zoo[i] = [self.zoo_diet_sediment_frac[i],
                             self.zoo_diet_phytoplankton_frac[i]]
            self.diet_content_zoo_lipid[i] = [self.sediment_lipid_frac[i],
                             self.phytoplankton_lipid_frac[i]]
            self.v_ld_zoo[i] = self.overall_diet_content(self.diet_frac_zoo[i], self.diet_content_zoo_lipid[i])

        #zooplankton NLOM content of diet
        self.diet_content_zoo_nlom = pd.Series([], dtype = 'float')
        self.v_nd_zoo = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_zoo_nlom[i] = [self.sediment_nlom_frac[i],
                             self.phytoplankton_nlom_frac[i]]
            self.v_nd_zoo[i] = self.overall_diet_content(self.diet_frac_zoo[i], self.diet_content_zoo_nlom[i])

        #zooplankton water content of diet
        self.diet_content_zoo_water = pd.Series([], dtype = 'float')
        self.v_wd_zoo = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_zoo_water[i] = [self.sediment_water_frac[i],
                             self.phytoplankton_water_frac[i]]
            self.v_wd_zoo[i] = self.overall_diet_content(self.diet_frac_zoo[i], self.diet_content_zoo_water[i])

        #benthic invertebrates lipid content of diet
        self.diet_frac_beninv = pd.Series([], dtype = 'float')
        self.diet_content_beninv_lipid = pd.Series([], dtype = 'float')
        self.v_ld_beninv = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_frac_beninv[i] = [self.beninv_diet_sediment_frac[i],
                             self.beninv_diet_phytoplankton_frac[i],
                             self.beninv_diet_zooplankton_frac[i]]
            self.diet_content_beninv_lipid[i] = [self.sediment_lipid_frac[i],
                             self.phytoplankton_lipid_frac[i],
                             self.zoo_lipid_frac[i]]
            self.v_ld_beninv[i] = self.overall_diet_content(self.diet_frac_beninv[i], self.diet_content_beninv_lipid[i])

        #benthic invertebrates NLOM content of diet
        self.diet_content_beninv_nlom = pd.Series([], dtype = 'float')
        self.v_nd_beninv = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_beninv_nlom[i] = [self.sediment_nlom_frac[i],
                             self.phytoplankton_nlom_frac[i],
                             self.zoo_nlom_frac[i]]
            self.v_nd_beninv[i] = self.overall_diet_content(self.diet_frac_beninv[i], self.diet_content_beninv_nlom[i])

        #benthic invertebrates water content of diet
        self.diet_content_beninv_water = pd.Series([], dtype = 'float')
        self.v_wd_beninv = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_beninv_water[i] = [self.sediment_water_frac[i],
                             self.phytoplankton_water_frac[i],
                             self.zoo_water_frac[i]]
            self.v_wd_beninv[i] = self.overall_diet_content(self.diet_frac_beninv[i], self.diet_content_beninv_water[i])

        #filterfeeders lipid content of diet
        self.diet_frac_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_content_filterfeeders_lipid = pd.Series([], dtype = 'float')
        self.v_ld_filterfeeders = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
           self.diet_frac_filterfeeders[i] = [self.filterfeeders_diet_sediment_frac[i],
                             self.filterfeeders_diet_phytoplankton_frac[i],
                             self.filterfeeders_diet_zooplankton_frac[i],
                             self.filterfeeders_diet_beninv_frac[i]]
           self.diet_content_filterfeeders_lipid[i] = [self.sediment_lipid_frac[i],
                             self.phytoplankton_lipid_frac[i],
                             self.zoo_lipid_frac[i],
                             self.beninv_lipid_frac[i]]
           self.v_ld_filterfeeders[i] = self.overall_diet_content(self.diet_frac_filterfeeders[i],
                                                            self.diet_content_filterfeeders_lipid[i])

        #filterfeeders NLOM content of diet
        self.diet_content_filterfeeders_nlom = pd.Series([], dtype = 'float')
        self.v_nd_filterfeeders = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_filterfeeders_nlom[i] = [self.sediment_nlom_frac[i],
                             self.phytoplankton_nlom_frac[i],
                             self.zoo_nlom_frac[i],
                             self.beninv_nlom_frac[i]]
            self.v_nd_filterfeeders[i] = self.overall_diet_content(self.diet_frac_filterfeeders[i],
                                                            self.diet_content_filterfeeders_nlom[i])

        #filterfeeders water content of diet
        self.diet_content_filterfeeders_water = pd.Series([], dtype = 'float')
        self.v_wd_filterfeeders = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_filterfeeders_water[i] = [self.sediment_water_frac[i],
                             self.phytoplankton_water_frac[i],
                             self.zoo_water_frac[i],
                             self.beninv_water_frac[i]]
            self.v_wd_filterfeeders[i] = self.overall_diet_content(self.diet_frac_filterfeeders[i],
                                                            self.diet_content_filterfeeders_water[i])

        #small fish lipid content of diet
        self.diet_frac_sfish = pd.Series([], dtype = 'float')
        self.diet_content_sfish_lipid = pd.Series([], dtype = 'float')
        self.v_ld_sfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_frac_sfish[i] = [self.sfish_diet_sediment_frac[i],
                             self.sfish_diet_phytoplankton_frac[i],
                             self.sfish_diet_zooplankton_frac[i],
                             self.sfish_diet_beninv_frac[i],
                             self.sfish_diet_filterfeeders_frac[i]]
            self.diet_content_sfish_lipid[i] = [self.sediment_lipid_frac[i],
                             self.phytoplankton_lipid_frac[i],
                             self.zoo_lipid_frac[i],
                             self.beninv_lipid_frac[i],
                             self.filterfeeders_lipid_frac[i]]
            self.v_ld_sfish[i] = self.overall_diet_content(self.diet_frac_sfish[i], self.diet_content_sfish_lipid[i])

        #small fish NLOM content of diet
        self.diet_content_sfish_nlom = pd.Series([], dtype = 'float')
        self.v_nd_sfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_sfish_nlom[i] = [self.sediment_nlom_frac[i],
                             self.phytoplankton_nlom_frac[i],
                             self.zoo_nlom_frac[i],
                             self.beninv_nlom_frac[i],
                             self.filterfeeders_nlom_frac[i]]
            self.v_nd_sfish[i] = self.overall_diet_content(self.diet_frac_sfish[i], self.diet_content_sfish_nlom[i])

        #small fish water
        self.diet_content_sfish_water = pd.Series([], dtype = 'float')
        self.v_wd_sfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_sfish_water[i] = [self.sediment_water_frac[i],
                             self.phytoplankton_water_frac[i],
                             self.zoo_water_frac[i],
                             self.beninv_water_frac[i],
                             self.filterfeeders_water_frac[i]]
            self.v_wd_sfish[i] = self.overall_diet_content(self.diet_frac_sfish[i], self.diet_content_sfish_water[i])

        #medium fish lipid content of diet
        self.diet_frac_mfish = pd.Series([], dtype = 'float')
        self.diet_content_mfish_lipid = pd.Series([], dtype = 'float')
        self.v_ld_mfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_frac_mfish[i] = [self.mfish_diet_sediment_frac[i],
                             self.mfish_diet_phytoplankton_frac[i],
                             self.mfish_diet_zooplankton_frac[i],
                             self.mfish_diet_beninv_frac[i],
                             self.mfish_diet_filterfeeders_frac[i],
                             self.mfish_diet_sfish_frac[i]]
            self.diet_content_mfish_lipid[i] = [self.sediment_lipid_frac[i],
                             self.phytoplankton_lipid_frac[i],
                             self.zoo_lipid_frac[i],
                             self.beninv_lipid_frac[i],
                             self.filterfeeders_lipid_frac[i],
                             self.sfish_lipid_frac[i]]
            self.v_ld_mfish[i] = self.overall_diet_content(self.diet_frac_mfish[i], self.diet_content_mfish_lipid[i])

        #medium fish NLOM content of diet
        self.diet_content_mfish_nlom = pd.Series([], dtype = 'float')
        self.v_nd_mfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_mfish_nlom[i] = [self.sediment_nlom_frac[i],
                             self.phytoplankton_nlom_frac[i],
                             self.zoo_nlom_frac[i],
                             self.beninv_nlom_frac[i],
                             self.filterfeeders_nlom_frac[i],
                             self.sfish_nlom_frac[i]]
            self.v_nd_mfish[i] = self.overall_diet_content(self.diet_frac_mfish[i], self.diet_content_mfish_nlom[i])

        #medium fish water content of diet
        self.diet_content_mfish_water = pd.Series([], dtype = 'float')
        self.v_wd_mfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_mfish_water[i] = [self.sediment_water_frac[i],
                             self.phytoplankton_water_frac[i],
                             self.zoo_water_frac[i],
                             self.beninv_water_frac[i],
                             self.filterfeeders_water_frac[i],
                             self.sfish_water_frac[i]]
            self.v_wd_mfish[i] = self.overall_diet_content(self.diet_frac_mfish[i], self.diet_content_mfish_water[i])

        #large fish lipid content of diet
        self.diet_frac_lfish = pd.Series([], dtype = 'float')
        self.diet_content_lfish_lipid = pd.Series([], dtype = 'float')
        self.v_ld_lfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_frac_lfish[i] = [self.lfish_diet_sediment_frac[i],
                             self.lfish_diet_phytoplankton_frac[i],
                             self.lfish_diet_zooplankton_frac[i],
                             self.lfish_diet_beninv_frac[i],
                             self.lfish_diet_filterfeeders_frac[i],
                             self.lfish_diet_sfish_frac[i],
                             self.lfish_diet_mfish_frac[i]]
            self.diet_content_lfish_lipid[i] = [self.sediment_lipid_frac[i],
                             self.phytoplankton_lipid_frac[i],
                             self.zoo_lipid_frac[i],
                             self.beninv_lipid_frac[i],
                             self.filterfeeders_lipid_frac[i],
                             self.sfish_lipid_frac[i],
                             self.mfish_lipid_frac[i]]
            self.v_ld_lfish[i] = self.overall_diet_content(self.diet_frac_lfish[i], self.diet_content_lfish_lipid[i])

        #large fish NLOM content of diet
        self.diet_content_lfish_nlom = pd.Series([], dtype = 'float')
        self.v_nd_lfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_lfish_nlom[i] = [self.sediment_nlom_frac[i],
                             self.phytoplankton_nlom_frac[i],
                             self.zoo_nlom_frac[i],
                             self.beninv_nlom_frac[i],
                             self.filterfeeders_nlom_frac[i],
                             self.sfish_nlom_frac[i],
                             self.mfish_nlom_frac[i]]
            self.v_nd_lfish[i] = self.overall_diet_content(self.diet_frac_lfish[i], self.diet_content_lfish_nlom[i])

        #large fish water content of diet
        self.diet_content_lfish_water = pd.Series([], dtype = 'float')
        self.v_wd_lfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):
            self.diet_content_lfish_water[i] = [self.sediment_water_frac[i],
                             self.phytoplankton_water_frac[i],
                             self.zoo_water_frac[i],
                             self.beninv_water_frac[i],
                             self.filterfeeders_water_frac[i],
                             self.sfish_water_frac[i],
                             self.mfish_water_frac[i]]
            self.v_wd_lfish[i] = self.overall_diet_content(self.diet_frac_lfish[i], self.diet_content_lfish_water[i])

        # overall diet assimilation factor and egestion rate of fecal matter  Eq A9 GF
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
        self.vlg_zoo = pd.Series([], dtype = 'float')
        self.vng_zoo = pd.Series([], dtype = 'float')
        self.vwg_zoo = pd.Series([], dtype = 'float')
        self.vlg_beninv = pd.Series([], dtype = 'float')
        self.vng_beninv = pd.Series([], dtype = 'float')
        self.vwg_beninv = pd.Series([], dtype = 'float')
        self.vlg_filterfeeders = pd.Series([], dtype = 'float')
        self.vng_filterfeeders = pd.Series([], dtype = 'float')
        self.vwg_filterfeeders = pd.Series([], dtype = 'float')
        self.vlg_sfish = pd.Series([], dtype = 'float')
        self.vng_sfish = pd.Series([], dtype = 'float')
        self.vwg_sfish = pd.Series([], dtype = 'float')
        self.vlg_mfish = pd.Series([], dtype = 'float')
        self.vng_mfish = pd.Series([], dtype = 'float')
        self.vwg_mfish = pd.Series([], dtype = 'float')
        self.vlg_lfish = pd.Series([], dtype = 'float')
        self.vng_lfish = pd.Series([], dtype = 'float')
        self.vwg_lfish = pd.Series([], dtype = 'float')
        
        self.vlg_zoo = self.diet_elements_gut(self.epsilon_lipid_zoo, self.v_ld_zoo, self.diet_assim_factor_zoo)
        self.vng_zoo = self.diet_elements_gut(self.epsilon_nlom_zoo, self.v_nd_zoo, self.diet_assim_factor_zoo)
        self.vwg_zoo = self.diet_elements_gut(self.epsilon_water, self.v_wd_zoo, self.diet_assim_factor_zoo)

        self.vlg_beninv = self.diet_elements_gut(self.epsilon_lipid_inv, self.v_ld_beninv,
                                                         self.diet_assim_factor_beninv)
        self.vng_beninv = self.diet_elements_gut(self.epsilon_nlom_inv, self.v_nd_beninv,
                                                         self.diet_assim_factor_beninv)
        self.vwg_beninv = self.diet_elements_gut(self.epsilon_water, self.v_wd_beninv,
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
        self.phytoplankton_ke = pd.Series([], dtype = 'float')
        self.zoo_ke = pd.Series([], dtype = 'float')
        self.beninv_ke = pd.Series([], dtype = 'float')
        self.filterfeeders_ke = pd.Series([], dtype = 'float')
        self.sfish_ke = pd.Series([], dtype = 'float')
        self.mfish_ke = pd.Series([], dtype = 'float')
        self.lfish_ke = pd.Series([], dtype = 'float')

        for i in range(self.num_simulations):
            self.phytoplankton_ke[i] = self.phytoplankton_ke_temp[i]  #should be 0.0 as per Appendix A.5 of Kabam Documentation
            if (self.zoo_ke_temp[i] == 'calculated'):
                self.zoo_ke[i] = self.fecal_elim_rate_const(self.gf_zoo[i], self.ed_zoo[i], self.kgb_zoo[i],
                                                            self.zoo_wb[i])
            else:
                self.zoo_ke[i] = float(self.zoo_ke_temp[i])

            if (self.beninv_ke_temp[i] == 'calculated'):
                self.beninv_ke[i] = self.fecal_elim_rate_const(self.gf_beninv[i], self.ed_beninv[i],
                                                               self.kgb_beninv[i], self.beninv_wb[i])
            else:
                self.beninv_ke[i] = float(self.beninv_ke_temp[i])

            if (self.filterfeeders_ke_temp[i] == 'calculated'):
                self.filterfeeders_ke[i] = self.fecal_elim_rate_const(self.gf_filterfeeders[i], self.ed_filterfeeders[i],
                                                                   self.kgb_filterfeeders[i], self.filterfeeders_wb[i])
            else:
                self.filterfeeders_ke[i] = float(self.filterfeeders_ke_temp[i])

            if (self.sfish_ke_temp[i] == 'calculated'):
                self.sfish_ke[i] = self.fecal_elim_rate_const(self.gf_sfish[i], self.ed_sfish[i], self.kgb_sfish[i],
                                                              self.sfish_wb[i])
            else:
                self.sfish_ke[i] = float(self.sfish_ke_temp[i])

            if (self.mfish_ke_temp[i] == 'calculated'):
                self.mfish_ke[i] = self.fecal_elim_rate_const(self.gf_mfish[i], self.ed_mfish[i], self.kgb_mfish[i],
                                                              self.mfish_wb[i])
            else:
                self.mfish_ke[i] = float(self.mfish_ke_temp[i])

            if (self.lfish_ke_temp[i] == 'calculated'):
                self.lfish_ke[i] = self.fecal_elim_rate_const(self.gf_lfish[i], self.ed_lfish[i], self.kgb_lfish[i],
                                                              self.lfish_wb[i])
            else:
                self.lfish_ke[i] = float(self.lfish_ke_temp[i])

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
            # :unit ug/(kg wet weight)
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
            # :param water_column_eec: total pesticide concentraiton in water column above sediment (ug/L)
            # :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (ug/L)
            # :param diet_conc: concentration of pesticide in overall diet of aquatic animal/organism (ug/kg wet weight)

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
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.diet_frac_zoo[i] = [self.zoo_diet_sediment_frac[i], self.zoo_diet_phytoplankton_frac[i]]
            self.diet_conc_zoo[i] = [self.c_s[i], self.out_cb_phytoplankton[i]]
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
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.diet_frac_beninv[i] = [self.beninv_diet_sediment_frac[i], self.beninv_diet_phytoplankton_frac[i],
                                        self.beninv_diet_zooplankton_frac[i]]
            self.diet_conc_beninv[i] = [self.c_s[i], self.out_cb_phytoplankton[i], self.out_cb_zoo[i]]
            self.diet_lipid_content_beninv[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i]]
        self.total_diet_conc_beninv, self.lipid_norm_diet_conc_beninv = self.diet_pest_conc(self.diet_frac_beninv,
                                                                  self.diet_conc_beninv, self.diet_lipid_content_beninv)
        self.out_cb_beninv = self.pest_conc_organism(self.beninv_k1, self.beninv_k2, self.beninv_kd, self.beninv_ke,
                                                      self.beninv_kg, self.beninv_km, self.beninv_mp, self.beninv_mo,
                                                      self.total_diet_conc_beninv)
 
        #filterfeeders
        self.diet_frac_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_conc_filterfeeders = pd.Series([], dtype = 'float')
        self.total_diet_conc_filterfeeders = pd.Series([], dtype = 'float')
        self.diet_lipid_content_filterfeeders = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_filterfeeders = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.diet_frac_filterfeeders[i] = [self.filterfeeders_diet_sediment_frac[i],
                                               self.filterfeeders_diet_phytoplankton_frac[i],
                                               self.filterfeeders_diet_zooplankton_frac[i],
                                               self.filterfeeders_diet_beninv_frac[i]]
            self.diet_conc_filterfeeders[i] = [self.c_s[i], self.out_cb_phytoplankton[i], self.out_cb_zoo[i],
                                                self.out_cb_beninv[i]]
            self.diet_lipid_content_filterfeeders[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i], self.beninv_lipid_frac[i]]
        self.total_diet_conc_filterfeeders, self.lipid_norm_diet_conc_filterfeeders = \
            self.diet_pest_conc(self.diet_frac_filterfeeders, self.diet_conc_filterfeeders,
            self.diet_lipid_content_filterfeeders)
        self.out_cb_filterfeeders = self.pest_conc_organism(self.filterfeeders_k1, self.filterfeeders_k2,
                                                            self.filterfeeders_kd, self.filterfeeders_ke,
                                                            self.filterfeeders_kg, self.filterfeeders_km,
                                                            self.filterfeeders_mp, self.filterfeeders_mo,
                                                            self.total_diet_conc_filterfeeders)
 
        #small fish
        self.diet_frac_sfish = pd.Series([], dtype = 'float')
        self.diet_conc_sfish = pd.Series([], dtype = 'float')
        self.total_diet_conc_sfish = pd.Series([], dtype = 'float')
        self.diet_lipid_content_sfish = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_sfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.diet_frac_sfish[i] = [self.sfish_diet_sediment_frac[i], self.sfish_diet_phytoplankton_frac[i],
                                       self.sfish_diet_zooplankton_frac[i], self.sfish_diet_beninv_frac[i],
                                       self.sfish_diet_filterfeeders_frac[i]]
            self.diet_conc_sfish[i] = [self.c_s[i], self.out_cb_phytoplankton[i], self.out_cb_zoo[i],
                                       self.out_cb_beninv[i], self.out_cb_filterfeeders[i]]
            self.diet_lipid_content_sfish[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i], self.beninv_lipid_frac[i], self.filterfeeders_lipid_frac[i]]
        self.total_diet_conc_sfish, self.lipid_norm_diet_conc_sfish = self.diet_pest_conc(self.diet_frac_sfish,
                                                                  self.diet_conc_sfish, self.diet_lipid_content_sfish)
        self.out_cb_sfish = self.pest_conc_organism(self.sfish_k1, self.sfish_k2, self.sfish_kd, self.sfish_ke,
                                                      self.sfish_kg, self.sfish_km, self.sfish_mp, self.sfish_mo,
                                                      self.total_diet_conc_sfish)
 
        #medium fish
        self.diet_frac_mfish = pd.Series([], dtype = 'float')
        self.diet_conc_mfish = pd.Series([], dtype = 'float')
        self.total_diet_conc_mfish = pd.Series([], dtype = 'float')
        self.diet_lipid_content_mfish = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_mfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.diet_frac_mfish[i] = [self.mfish_diet_sediment_frac[i], self.mfish_diet_phytoplankton_frac[i],
                                       self.mfish_diet_zooplankton_frac[i], self.mfish_diet_beninv_frac[i],
                                       self.mfish_diet_filterfeeders_frac[i], self.mfish_diet_sfish_frac[i]]
            self.diet_conc_mfish[i] = [self.c_s[i], self.out_cb_phytoplankton[i], self.out_cb_zoo[i],
                                        self.out_cb_beninv[i], self.out_cb_filterfeeders[i], self.out_cb_sfish[i]]
            self.diet_lipid_content_mfish[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                              self.zoo_lipid_frac[i], self.beninv_lipid_frac[i],
                                                self.filterfeeders_lipid_frac[i], self.sfish_lipid_frac[i]]
        self.total_diet_conc_mfish, self.lipid_norm_diet_conc_mfish = self.diet_pest_conc(self.diet_frac_mfish,
                                                                  self.diet_conc_mfish, self.diet_lipid_content_mfish)
        self.out_cb_mfish = self.pest_conc_organism(self.mfish_k1, self.mfish_k2, self.mfish_kd, self.mfish_ke,
                                                      self.mfish_kg, self.mfish_km, self.mfish_mp, self.mfish_mo,
                                                      self.total_diet_conc_mfish)
        
        #large fish
        self.diet_frac_lfish = pd.Series([], dtype = 'float')
        self.diet_conc_lfish = pd.Series([], dtype = 'float')
        self.total_diet_conc_lfish = pd.Series([], dtype = 'float')
        self.diet_lipid_content_lfish = pd.Series([], dtype = 'float')
        self.lipid_norm_diet_conc_lfish = pd.Series([], dtype = 'float')
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.diet_frac_lfish[i] = [self.lfish_diet_sediment_frac[i], self.lfish_diet_phytoplankton_frac[i],
                                       self.lfish_diet_zooplankton_frac[i], self.lfish_diet_beninv_frac[i],
                                       self.lfish_diet_filterfeeders_frac[i], self.lfish_diet_sfish_frac[i],
                                       self.lfish_diet_mfish_frac[i]]
            self.diet_conc_lfish[i] = [self.c_s[i], self.out_cb_phytoplankton[i], self.out_cb_zoo[i],
                                        self.out_cb_beninv[i], self.out_cb_filterfeeders[i], self.out_cb_sfish[i],
                                        self.out_cb_mfish[i]]
            self.diet_lipid_content_lfish[i] = [self.sediment_lipid_frac[i], self.phytoplankton_lipid_frac[i],
                                                self.zoo_lipid_frac[i], self.beninv_lipid_frac[i],
                                                self.filterfeeders_lipid_frac[i], self.sfish_lipid_frac[i],
                                                self.mfish_lipid_frac[i]]
        self.total_diet_conc_lfish, self.lipid_norm_diet_conc_lfish = self.diet_pest_conc(self.diet_frac_lfish,
                                                                  self.diet_conc_lfish, self.diet_lipid_content_lfish)
        self.out_cb_lfish = self.pest_conc_organism(self.lfish_k1, self.lfish_k2, self.lfish_kd, self.lfish_ke,
                                                    self.lfish_kg, self.lfish_km, self.lfish_mp, self.lfish_mo,
                                                    self.total_diet_conc_lfish)
        
        #LIPID NORMALIZED PESTICIDE TISSUE RESIDUE

        self.out_cbl_phytoplankton = self.lipid_norm_residue_conc(self.out_cb_phytoplankton,self.phytoplankton_lipid_frac)
        self.out_cbl_zoo = self.lipid_norm_residue_conc(self.out_cb_zoo,self.zoo_lipid_frac)
        self.out_cbl_beninv = self.lipid_norm_residue_conc(self.out_cb_beninv,self.beninv_lipid_frac)
        self.out_cbl_filterfeeders = self.lipid_norm_residue_conc(self.out_cb_filterfeeders,self.filterfeeders_lipid_frac)
        self.out_cbl_sfish = self.lipid_norm_residue_conc(self.out_cb_sfish,self.sfish_lipid_frac)
        self.out_cbl_mfish = self.lipid_norm_residue_conc(self.out_cb_mfish,self.mfish_lipid_frac)
        self.out_cbl_lfish = self.lipid_norm_residue_conc(self.out_cb_lfish,self.lfish_lipid_frac)

        #PESTICIDE CONCENTRAITON ORGINATING FROM UPTAKE THROUGH DIET (K1 = 0; no phytoplankton due to lack of diet)
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
                                                                   self.phytoplankton_mp, self.phytoplankton_mo,
                                                                   self.phytoplankton_lipid_frac)
        self.out_cbfl_zoo = self.lipid_norm_bioconc_fact(self.zoo_k1, self.zoo_k2,
                                                self.zoo_mp, self.zoo_mo, self.zoo_lipid_frac)
        self.out_cbfl_beninv = self.lipid_norm_bioconc_fact(self.beninv_k1, self.beninv_k2,
                                                self.beninv_mp, self.beninv_mo, self.beninv_lipid_frac)
        self.out_cbfl_filterfeeders = self.lipid_norm_bioconc_fact(self.filterfeeders_k1, self.filterfeeders_k2,
                                                                   self.filterfeeders_mp, self.filterfeeders_mo,
                                                                   self.filterfeeders_lipid_frac)
        self.out_cbfl_sfish = self.lipid_norm_bioconc_fact(self.sfish_k1, self.sfish_k2,
                                                self.sfish_mp, self.sfish_mo, self.sfish_lipid_frac)
        self.out_cbfl_mfish = self.lipid_norm_bioconc_fact(self.mfish_k1, self.mfish_k2,
                                                self.mfish_mp, self.mfish_mo, self.mfish_lipid_frac)
        self.out_cbfl_lfish = self.lipid_norm_bioconc_fact(self.lfish_k1, self.lfish_k2,
                                                self.lfish_mp, self.lfish_mo, self.lfish_lipid_frac)

        #total bioaccumulation factor (Table 12)
        self.out_cbaf_phytoplankton = self.tot_bioacc_fact(self.out_cb_phytoplankton)
        self.out_cbaf_zoo = self.tot_bioacc_fact(self.out_cb_zoo)
        self.out_cbaf_beninv = self.tot_bioacc_fact(self.out_cb_beninv)
        self.out_cbaf_filterfeeders = self.tot_bioacc_fact(self.out_cb_filterfeeders)
        self.out_cbaf_sfish = self.tot_bioacc_fact(self.out_cb_sfish)
        self.out_cbaf_mfish = self.tot_bioacc_fact(self.out_cb_mfish)
        self.out_cbaf_lfish = self.tot_bioacc_fact(self.out_cb_lfish)
        
        #lipid normalized bioaccumulation factor (Table 13)
        self.out_cbafl_phytoplankton = self.lipid_norm_bioacc_fact(self.out_cb_phytoplankton,
                                                                   self.phytoplankton_lipid_frac)
        self.out_cbafl_zoo = self.lipid_norm_bioacc_fact(self.out_cb_zoo, self.zoo_lipid_frac)
        self.out_cbafl_beninv = self.lipid_norm_bioacc_fact(self.out_cb_beninv, self.beninv_lipid_frac)
        self.out_cbafl_filterfeeders = self.lipid_norm_bioacc_fact(self.out_cb_filterfeeders,
                                                                   self.filterfeeders_lipid_frac)
        self.out_cbafl_sfish = self.lipid_norm_bioacc_fact(self.out_cb_sfish, self.sfish_lipid_frac)
        self.out_cbafl_mfish = self.lipid_norm_bioacc_fact(self.out_cb_mfish, self.mfish_lipid_frac)
        self.out_cbafl_lfish = self.lipid_norm_bioacc_fact(self.out_cb_lfish, self.lfish_lipid_frac)

        #biota sediment accumulatoin factor (Table 13)
        self.out_cbsafl_phytoplankton = self.biota_sed_acc_fact(self.out_cb_phytoplankton, self.phytoplankton_lipid_frac)
        self.out_cbsafl_zoo = self.biota_sed_acc_fact(self.out_cb_zoo, self.zoo_lipid_frac)
        self.out_cbsafl_beninv = self.biota_sed_acc_fact(self.out_cb_beninv, self.beninv_lipid_frac)
        self.out_cbsafl_filterfeeders = self.biota_sed_acc_fact(self.out_cb_filterfeeders, self.filterfeeders_lipid_frac)
        self.out_cbsafl_sfish = self.biota_sed_acc_fact(self.out_cb_sfish, self.sfish_lipid_frac)
        self.out_cbsafl_mfish = self.biota_sed_acc_fact(self.out_cb_mfish, self.mfish_lipid_frac)
        self.out_cbsafl_lfish = self.biota_sed_acc_fact(self.out_cb_lfish, self.lfish_lipid_frac)

        #biomagnification factor (Table 13 - none for phytoplankton due to lack of diet)
        self.out_bmf_zoo = self.biomag_fact(self.out_cb_zoo, self.zoo_lipid_frac, self.lipid_norm_diet_conc_zoo)
        self.out_bmf_beninv = self.biomag_fact(self.out_cb_beninv, self.beninv_lipid_frac,
                                               self.lipid_norm_diet_conc_beninv)
        self.out_bmf_filterfeeders = self.biomag_fact(self.out_cb_filterfeeders, self.filterfeeders_lipid_frac,
                                                      self.lipid_norm_diet_conc_filterfeeders)
        self.out_bmf_sfish = self.biomag_fact(self.out_cb_sfish, self.sfish_lipid_frac, self.lipid_norm_diet_conc_sfish)
        self.out_bmf_mfish = self.biomag_fact(self.out_cb_mfish, self.mfish_lipid_frac, self.lipid_norm_diet_conc_mfish)
        self.out_bmf_lfish = self.biomag_fact(self.out_cb_lfish, self.lfish_lipid_frac, self.lipid_norm_diet_conc_lfish)

        #BEGIN CALCULATIONS FOR DIETARY-BASED AND DOSE-BASED EECs, TOXICITY VALUES, AND RQs


        #PLACE AQUATIC ORGANISM CONCENTRATIONS INTO ARRAY STRUCTURE
        self.cb_a = np.zeros((self.num_simulations,len(self.aquatic_animals)))
        for i in range (self.num_simulations):
            self.cb_a[i] = np.array([self.out_cb_phytoplankton[i], self.out_cb_zoo[i], self.out_cb_beninv[i],
                               self.out_cb_filterfeeders[i], self.out_cb_sfish[i], self.out_cb_mfish[i],
                               self.out_cb_lfish[i]])

        #DRY/WET FOOD INGESTION RATES & DRINKING WATER INTAKE FOR MAMMALS AND BIRDS (TABLE 14)

        #dry food ingestion rates: mammals (Table 14)
        self.dry_food_ingestion_rate_mammals = np.array([], dtype = 'float')
        self.dry_food_ingestion_rate_mammals = self.dry_food_ingest_rate_mammals()
        #trasfer to individual output variables (repeat for each model run simulation)
        for i in range (self.num_simulations):
            self.out_dfir0[i], self.out_dfir1[i], self.out_dfir2[i], self.out_dfir3[i], \
                self.out_dfir4[i], self.out_dfir5[i] =  self.dry_food_ingestion_rate_mammals

        #dry food ingestion rates: birds (Table 14)
        self.dry_food_ingestion_rate_birds = np.array([], dtype = 'float')
        self.dry_food_ingestion_rate_birds = self.dry_food_ingest_rate_birds()
        #trasfer to individual output variables (repeat for each model run simulation)
        for i in range (self.num_simulations):
            self.out_dfira0[i], self.out_dfira1[i], self.out_dfira2[i], self.out_dfira3[i], \
                self.out_dfira4[i], self.out_dfira5[i] =  self.dry_food_ingestion_rate_birds

        self.aq_animal_water_content = np.zeros((self.num_simulations,len(self.aquatic_animals)))
        self.wet_food_ingestion_rate_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        self.wet_food_ingestion_rate_birds = np.zeros((self.num_simulations,len(self.birds)))
        for i in range(self.num_simulations):     #loop through model simulation runs
            self.aq_animal_water_content[i] = [self.phytoplankton_water_frac[i], self.zoo_water_frac[i],
                                                        self.beninv_water_frac[i], self.filterfeeders_water_frac[i],
                                                        self.sfish_water_frac[i], self.mfish_water_frac[i],
                                                        self.lfish_water_frac[i]]

            #wet food ingestion rates: mammals (Table 14)
            self.wet_food_ingestion_rate_mammals[i] = self.wet_food_ingestion_rates(self.aq_animal_water_content[i],
                                                   self.diet_mammals, self.dry_food_ingestion_rate_mammals)
            #trasfer to individual output variables
            self.out_wet_food_ingestion_m0[i], self.out_wet_food_ingestion_m1[i], self.out_wet_food_ingestion_m2[i],  \
                    self.out_wet_food_ingestion_m3[i], self.out_wet_food_ingestion_m4[i],  \
                    self.out_wet_food_ingestion_m5[i] = self.wet_food_ingestion_rate_mammals[i]

            #wet food ingestion rates: birds (Table 14)
            self.wet_food_ingestion_rate_birds[i] = self.wet_food_ingestion_rates(self.aq_animal_water_content[i],
                                                 self.diet_birds, self.dry_food_ingestion_rate_birds)
            #trasfer to individual output variables
            self.out_wet_food_ingestion_a0[i], self.out_wet_food_ingestion_a1[i], self.out_wet_food_ingestion_a2[i],  \
                    self.out_wet_food_ingestion_a3[i], self.out_wet_food_ingestion_a4[i],  \
                    self.out_wet_food_ingestion_a5[i] = self.wet_food_ingestion_rate_birds[i]

        #drinking water intake rates:mammals (Table 14)
        self.water_ingestion_rate_mammals = np.zeros((len(self.aquatic_animals)))
        self.water_ingestion_rate_mammals = self.drinking_water_intake_mammals()
        #trasfer to individual output variables
        #these values are a function of body weights which are hardwired as constants
        #thus, they are calculated once and assigned across all model run simulations
        for i in range (self.num_simulations):
            self.out_drinking_water_intake_m0[i], self.out_drinking_water_intake_m1[i],       \
                self.out_drinking_water_intake_m2[i], self.out_drinking_water_intake_m3[i],   \
                self.out_drinking_water_intake_m4[i], self.out_drinking_water_intake_m5[i]    \
                = self.water_ingestion_rate_mammals[0:6]

        #drinking water intake rates:birds (Table 14)
        #these values are a function of body weights which are hardwired as constants
        #thus, they are calculated once and assigned across all model run simulations
        self.water_ingestion_rate_birds = np.array([], dtype = 'float')
        self.water_ingestion_rate_birds = self.drinking_water_intake_birds()
        #trasfer to individual output variables (need to
        for i in range (self.num_simulations):
            self.out_drinking_water_intake_a0[i], self.out_drinking_water_intake_a1[i], \
                self.out_drinking_water_intake_a2[i], self.out_drinking_water_intake_a3[i], \
                self.out_drinking_water_intake_a4[i], self.out_drinking_water_intake_a5[i]\
                = self.water_ingestion_rate_birds[0:6]

        # EEC CALCULATIONS FOR MAMMALS AND BIRDS (TABLE 14)

        #dose_based EECs: Mammals
        self.dose_based_eec_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range (self.num_simulations):
            self.dose_based_eec_mammals[i] = self.dose_based_eec(self.water_column_eec[i], self.cb_a[i],
                                                          self.diet_mammals, self.wet_food_ingestion_rate_mammals[i],
                                                          self.water_ingestion_rate_mammals, self.mammal_weights)
            #transfer to individual output variables
            self.out_db40[i],self.out_db41[i],self.out_db42[i],self.out_db43[i],self.out_db44[i],self.out_db45[i] = \
                    self.dose_based_eec_mammals[i]

        #dose-based EECs: Birds (TABLE 14)
        self.dose_based_eec_birds = np.zeros((self.num_simulations,len(self.birds)))
        for i in range (self.num_simulations):
            self.dose_based_eec_birds[i] = self.dose_based_eec(self.water_column_eec[i], self.cb_a[i], self.diet_birds,
                               self.wet_food_ingestion_rate_birds[i],
                               self.water_ingestion_rate_birds, self.bird_weights)
            #transfer to individual output variables
            self.out_db4a0[i],self.out_db4a1[i],self.out_db4a2[i],self.out_db4a3[i],self.out_db4a4[i],\
                self.out_db4a5[i] = self.dose_based_eec_birds[i]

        #dietary-based EECs: Mammals (TABLE 14)
        self.diet_based_eec_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range (self.num_simulations):
            self.diet_based_eec_mammals[i] = self.dietary_based_eec(self.cb_a[i], self.diet_mammals)
            #transfer to individual output variables
            self.out_db50[i],self.out_db51[i],self.out_db52[i],self.out_db53[i],self.out_db54[i],\
                self.out_db55[i] = self.diet_based_eec_mammals[i]

        #dietary-based EECs: Birds (TABLE 14)
        self.diet_based_eec_birds = np.zeros((self.num_simulations,len(self.birds)))
        for i in range (self.num_simulations):
            self.diet_based_eec_birds[i] = self.dietary_based_eec(self.cb_a[i], self.diet_birds)
            #transfer to individual output variables
            self.out_db5a0[i],self.out_db5a1[i],self.out_db5a2[i],self.out_db5a3[i],self.out_db5a4[i],\
                self.out_db5a5[i] = self.diet_based_eec_birds[i]
        
        #TOXICITY VALUES FOR MAMMALS AND BIRDS (TABLE 15)

        #adjusted/acute dose-based toxicity for mammals (TABLE 15)
        self.dose_based_tox_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range(self.num_simulations):   #loop through model simulation runs
            if (self.species_of_the_tested_mammal[i] == 'rat'):
                tested_bw = self.bw_rat[i]
            else:
                tested_bw = self.bw_other_mammal[i]
            self.dose_based_tox_mammals[i] = self.acute_dose_based_tox_mammals(self.mammalian_ld50[i], tested_bw)
            #transfer to individual output variables
            self.out_acute_dose_based_m0[i],self.out_acute_dose_based_m1[i],self.out_acute_dose_based_m2[i],\
                self.out_acute_dose_based_m3[i], self.out_acute_dose_based_m4[i],\
                self.out_acute_dose_based_m5[i] = self.dose_based_tox_mammals[i]

            #adjusted/acute diet-based toxicity for mammals - all are equal to the mammalian_lc50 value IF PROVIDED(Table 15)
            self.out_acute_diet_based_m0[i] = self.out_acute_diet_based_m1[i] = self.out_acute_diet_based_m2[i] =  \
                self.out_acute_diet_based_m3[i] = self.out_acute_diet_based_m4[i] =  \
                self.out_acute_diet_based_m5[i] = self.mammalian_lc50[i]

        #chronic dose-based toxicity for mammals (TABLE 15)
        self.chronic_dose_based_tox_mamm = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range(self.num_simulations):   #loop through model simulation runs
            if (self.species_of_the_tested_mammal[i] == 'rat'):
                tested_bw = self.bw_rat[i]
            else:
                tested_bw = self.bw_other_mammal[i]
            self.chronic_dose_based_tox_mamm[i] = self.chronic_dose_based_tox_mammals(
                                                                    self.mammalian_chronic_endpoint[i], 
                                                                    self.mammalian_chronic_endpoint_unit[i], tested_bw)
            #transfer to individual output variables
            self.out_chronic_dose_based_m0[i], self.out_chronic_dose_based_m1[i], self.out_chronic_dose_based_m2[i],\
                self.out_chronic_dose_based_m3[i], self.out_chronic_dose_based_m4[i],\
                self.out_chronic_dose_based_m5[i] = self.chronic_dose_based_tox_mamm[i]

        #Chronic diet-based toxicity for mammals (Table 15)
        self.chronic_diet_based_tox_mamm = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range(self.num_simulations):
            self.chronic_diet_based_tox_mamm[i] = self.chronic_diet_based_tox_mammals(
                                              self.mammalian_chronic_endpoint[i],
                                              self.mammalian_chronic_endpoint_unit[i])
            #transfer to individual output variables
            self.out_chronic_diet_based_m0[i], self.out_chronic_diet_based_m1[i], \
                self.out_chronic_diet_based_m2[i], self.out_chronic_diet_based_m3[i], \
                self.out_chronic_diet_based_m4[i], self.out_chronic_diet_based_m5[i] \
                = self.chronic_diet_based_tox_mamm[i]

        #adjusted/acute dose-based toxicity for birds (TABLE 15)
        self.dose_based_tox_birds = np.zeros((self.num_simulations,len(self.birds)))
        for i in range(self.num_simulations):   #loop through model simulation runs
            if (self.species_of_the_tested_bird[i] == 'quail'):
                tested_bw = self.bw_quail
            elif (self.species_of_the_tested_bird[i] == 'duck'):
                tested_bw = self.bw_duck
            else:
                tested_bw = self.bw_other_bird
            self.dose_based_tox_birds[i] = self.acute_dose_based_tox_birds(self.avian_ld50[i], tested_bw[i],
                                                                           self.mineau_scaling_factor[i])
            self.out_acute_dose_based_a0[i], self.out_acute_dose_based_a1[i], self.out_acute_dose_based_a2[i], \
                self.out_acute_dose_based_a3[i], self.out_acute_dose_based_a4[i], \
                self.out_acute_dose_based_a5[i] = self.dose_based_tox_birds[i]

            #adjusted/acute diet-based toxicity for birds - all are equal to the avian_lc50 value(Table 15)
            self.out_acute_diet_based_a0[i] = self.out_acute_diet_based_a1[i] = self.out_acute_diet_based_a2[i] =  \
                self.out_acute_diet_based_a3[i] = self.out_acute_diet_based_a4[i] =  \
                self.out_acute_diet_based_a5[i] = self.avian_lc50[i]

            #Note: There is no chronic dosed-based toxicity for birds

            #chronic diet-based toxicity for birds - all are equal to the avian_noaec value(Table 15)
            self.out_chronic_diet_based_a0[i] = self.out_chronic_diet_based_a1[i] = self.out_chronic_diet_based_a2[i] =\
            self.out_chronic_diet_based_a3[i] = self.out_chronic_diet_based_a4[i] =\
            self.out_chronic_diet_based_a5[i] = self.avian_noaec[i]


        #CALCULATE RISK QUOTIENTS FOR MAMMALS AND BIRDS (TABLE 16)

        #Acute dose-based risk quotient for mammals (Table 16)
        self.acute_dose_based_rq_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        self.acute_dose_based_rq_mammals = self.acute_rq_dose_mammals()
        for i in range(self.num_simulations):   #loop through model simulation runs
            self.out_acute_rq_dose_m0[i], self.out_acute_rq_dose_m1[i], self.out_acute_rq_dose_m2[i], \
                self.out_acute_rq_dose_m3[i], self.out_acute_rq_dose_m4[i], self.out_acute_rq_dose_m5[i] \
                = self.acute_dose_based_rq_mammals[i]

        #Chronic dose-based risk quotient for mammals (Table 16)
        self.chronic_dose_based_rq_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        self.chronic_dose_based_rq_mammals = self.chronic_rq_dose_mammals()
        for i in range(self.num_simulations):   #loop through model simulation runs
            self.out_chronic_rq_dose_m0[i], self.out_chronic_rq_dose_m1[i], self.out_chronic_rq_dose_m2[i], \
                self.out_chronic_rq_dose_m3[i], self.out_chronic_rq_dose_m4[i], self.out_chronic_rq_dose_m5[i] \
                = self.chronic_dose_based_rq_mammals[i]

        #Acute diet-based risk quotient for mammals (Table 16)
                    #Note: when a value for mammalian_lc50 is not availble the OPP spreadsheet enters 'N/A'
                    #this doesn't work well in the python code because numpy arrays need to be homogeneous in datatype
                    #so, for now anyway I recommend that the appropriate cell in the ubertool input spreadsheet be blank
                    # rather than inserting a 'N/A'; the blank will be processed as 'nan' rather than 'N/A'
        self.acute_diet_based_rq_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range(self.num_simulations):
            self.acute_diet_based_rq_mammals[i] = self.acute_rq_diet_mammals(self.diet_based_eec_mammals[i],
                                                                             self.mammalian_lc50[i])
            self.out_acute_rq_diet_m0[i], self.out_acute_rq_diet_m1[i], self.out_acute_rq_diet_m2[i], \
                self.out_acute_rq_diet_m3[i], self.out_acute_rq_diet_m4[i], self.out_acute_rq_diet_m5[i] \
                = self.acute_diet_based_rq_mammals[i]

        #Chronic diet-based risk quotient for mammals (Table 16)
        self.chronic_diet_based_rq_mammals = np.zeros((self.num_simulations,len(self.mammals)))
        for i in range(self.num_simulations):
            self.chronic_diet_based_rq_mammals[i] = self.chronic_rq_diet_mammals(self.diet_based_eec_mammals[i],
                                                 self.mammalian_chronic_endpoint[i],
                                                 self.mammalian_chronic_endpoint_unit[i])
            self.out_chronic_rq_diet_m0[i], self.out_chronic_rq_diet_m1[i], self.out_chronic_rq_diet_m2[i], \
                self.out_chronic_rq_diet_m3[i], self.out_chronic_rq_diet_m4[i], \
                self.out_chronic_rq_diet_m5[i]  = self.chronic_diet_based_rq_mammals[i]

        #Acute dose-based risk quotient for birds (Table 16)
        self.acute_dose_based_rq_birds = np.zeros((self.num_simulations,len(self.birds)))
        self.acute_dose_based_rq_birds = self.acute_rq_dose_birds()
        for i in range(self.num_simulations):   #loop through model simulation runs
            self.out_acute_rq_dose_a0[i], self.out_acute_rq_dose_a1[i], self.out_acute_rq_dose_a2[i], \
                self.out_acute_rq_dose_a3[i], self.out_acute_rq_dose_a4[i], self.out_acute_rq_dose_a5[i] \
                    = self.acute_dose_based_rq_birds[i]

        #Acute diet-based for risk quotient birds (Table 16)
        self.acute_diet_based_rq_birds = np.zeros((self.num_simulations,len(self.birds)))
        for i in range(self.num_simulations):  #loop through model simulation runs
            self.acute_diet_based_rq_birds[i] = self.acute_rq_diet_birds(self.diet_based_eec_birds[i],
                                                 self.avian_lc50[i])
            self.out_acute_rq_diet_a0[i], self.out_acute_rq_diet_a1[i], self.out_acute_rq_diet_a2[i], \
                self.out_acute_rq_diet_a3[i], self.out_acute_rq_diet_a4[i], \
                self.out_acute_rq_diet_a5[i] = self.acute_diet_based_rq_birds[i]

        #Note: There is no chronic dosed-based risk quotient for birds

        #Chronic diet-based for risk quotient birds (Table 16)
        self.chronic_diet_based_rq_birds = np.zeros((self.num_simulations,len(self.birds)))
        for i in range(self.num_simulations):  #loop through model simulation runs
            self.chronic_diet_based_rq_birds[i] = self.chronic_rq_diet_birds(self.diet_based_eec_birds[i],
                                                 self.avian_noaec[i])
            self.out_chronic_rq_diet_a0[i], self.out_chronic_rq_diet_a1[i], self.out_chronic_rq_diet_a2[i], \
                self.out_chronic_rq_diet_a3[i], self.out_chronic_rq_diet_a4[i], \
                self.out_chronic_rq_diet_a5[i] = self.chronic_diet_based_rq_birds[i]

    def set_global_constants(self):

        #set number of model run simulations to be performed (equal to the number of entries in any one of the input variables)
        #used throughout code to specify number of times a piece of code should be executed (e.g., for loops)
        self.num_simulations = len(self.log_kow)

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
        #transfer mammal weights to output variable (replicate for each model simulation run)
        for i in range(self.num_simulations):
            self.out_mweight0[i], self.out_mweight1[i], self.out_mweight2[i], self.out_mweight3[i], \
                self.out_mweight4[i], self.out_mweight5[i] = self.mammal_weights

        #list of birds (data in related arrays will reflect this order)
        self.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons', 'small osprey', 'white pelican'], dtype = 'str')
        self.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5], dtype = 'float')
        self.diet_birds = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0],
                                    [0, 0, 0.5, 0, 0.5, 0, 0], [0, 0, 0.5, 0, 0, 0.5, 0],
                                    [0, 0, 0, 0, 0, 1., 0], [0, 0, 0, 0, 0, 0, 1.]], dtype = 'float')
        #transfer bird weights to output variable (replicate for each model simulation run)
        for i in range(self.num_simulations):
            self.out_aweight0[i], self.out_aweight1[i], self.out_aweight2[i], self.out_aweight3[i], \
                self.out_aweight4[i], self.out_aweight5[i] = self.bird_weights

        # conversions

        self.kow = pd.Series([], dtype = 'float')
        self.sediment_oc_frac = pd.Series([], dtype = 'float')

        self.kow = 10.**(self.log_kow) # convert log kow to kow
        self.sediment_oc_frac = self.percent_to_frac(self.sediment_oc)

        #set conversion factor
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
        self.epsilon_nlom_inv  = 0.75 # aquatic invertebrates dietary assimilation rate of NLOM (Kabam Eq. A9)
        self.epsilon_nlom_zoo  = 0.72 # zooplankton dietary assimilation rate of NLOM (Kabam Eq. A9)

        self.epsilon_water = 0.25  # freshwater organisms dietary assimilation rate of water

        self.alpha_poc = 0.35  #proportionality constant to describe the similarity of phase partitioning of POC in relation to octanol
        self.alpha_doc = 0.08  #proportionality constant to describe the similarity of phase partitioning of DOC in relation to octanol

        #convert all percentage-based inputs to fractions
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
        self.beninv_water_frac = self.percent_to_frac(self.beninv_water)

        self.filterfeeders_lipid_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.filterfeeders_nlom_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion
        self.filterfeeders_water_frac = pd.Series([], dtype="float")  #not direct input; result of units conversion

        self.filterfeeders_lipid_frac = self.percent_to_frac(self.filterfeeders_lipid)
        self.filterfeeders_nlom_frac = self.percent_to_frac(self.filterfeeders_nlom)
        self.filterfeeders_water_frac = self.percent_to_frac(self.filterfeeders_water)

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

        #convert diet data from percentages to fractions

        self.zoo_diet_sediment_frac = pd.Series([], dtype='float')
        self.zoo_diet_phytoplankton_frac = pd.Series([], dtype='float')

        self.zoo_diet_sediment_frac = self.percent_to_frac(self.zoo_diet_sediment)
        self.zoo_diet_phytoplankton_frac = self.percent_to_frac(self.zoo_diet_phytoplankton)

        self.beninv_diet_sediment_frac = pd.Series([], dtype='float')
        self.beninv_diet_phytoplankton_frac = pd.Series([], dtype='float')
        self.beninv_diet_zooplankton_frac = pd.Series([], dtype='float')

        self.beninv_diet_sediment_frac = self.percent_to_frac(self.beninv_diet_sediment)
        self.beninv_diet_phytoplankton_frac = self.percent_to_frac(self.beninv_diet_phytoplankton)
        self.beninv_diet_zooplankton_frac = self.percent_to_frac(self.beninv_diet_zooplankton)

        self.filterfeeders_diet_sediment_frac = pd.Series([], dtype='float')
        self.filterfeeders_diet_phytoplankton_frac = pd.Series([], dtype='float')
        self.filterfeeders_diet_zooplankton_frac = pd.Series([], dtype='float')
        self.filterfeeders_diet_beninv_frac = pd.Series([], dtype='float')

        self.filterfeeders_diet_sediment_frac = self.percent_to_frac(self.filterfeeders_diet_sediment)
        self.filterfeeders_diet_phytoplankton_frac = self.percent_to_frac(self.filterfeeders_diet_phytoplankton)
        self.filterfeeders_diet_zooplankton_frac = self.percent_to_frac(self.filterfeeders_diet_zooplankton)
        self.filterfeeders_diet_beninv_frac = self.percent_to_frac(self.filterfeeders_diet_beninv)

        self.sfish_diet_sediment_frac = pd.Series([], dtype='float')
        self.sfish_diet_phytoplankton_frac = pd.Series([], dtype='float')
        self.sfish_diet_zooplankton_frac = pd.Series([], dtype='float')
        self.sfish_diet_beninv_frac = pd.Series([], dtype='float')
        self.sfish_diet_filterfeeders_frac = pd.Series([], dtype='float')

        self.sfish_diet_sediment_frac = self.percent_to_frac(self.sfish_diet_sediment)
        self.sfish_diet_phytoplankton_frac = self.percent_to_frac(self.sfish_diet_phytoplankton)
        self.sfish_diet_zooplankton_frac = self.percent_to_frac(self.sfish_diet_zooplankton)
        self.sfish_diet_beninv_frac = self.percent_to_frac(self.sfish_diet_beninv)
        self.sfish_diet_filterfeeders_frac = self.percent_to_frac(self.sfish_diet_filterfeeders)

        self.mfish_diet_sediment_frac = pd.Series([], dtype='float')
        self.mfish_diet_phytoplankton_frac = pd.Series([], dtype='float')
        self.mfish_diet_zooplankton_frac = pd.Series([], dtype='float')
        self.mfish_diet_beninv_frac = pd.Series([], dtype='float')
        self.mfish_diet_filterfeeders_frac = pd.Series([], dtype='float')
        self.mfish_diet_sfish_frac = pd.Series([], dtype='float')

        self.mfish_diet_sediment_frac = self.percent_to_frac(self.mfish_diet_sediment)
        self.mfish_diet_phytoplankton_frac = self.percent_to_frac(self.mfish_diet_phytoplankton)
        self.mfish_diet_zooplankton_frac = self.percent_to_frac(self.mfish_diet_zooplankton)
        self.mfish_diet_beninv_frac = self.percent_to_frac(self.mfish_diet_beninv)
        self.mfish_diet_filterfeeders_frac = self.percent_to_frac(self.mfish_diet_filterfeeders)
        self.mfish_diet_sfish_frac = self.percent_to_frac(self.mfish_diet_sfish)

        self.lfish_diet_sediment_frac = pd.Series([], dtype='float')
        self.lfish_diet_phytoplankton_frac = pd.Series([], dtype='float')
        self.lfish_diet_zooplankton_frac = pd.Series([], dtype='float')
        self.lfish_diet_beninv_frac = pd.Series([], dtype='float')
        self.lfish_diet_filterfeeders_frac = pd.Series([], dtype='float')
        self.lfish_diet_sfish_frac = pd.Series([], dtype='float')
        self.lfish_diet_mfish_frac = pd.Series([], dtype='float')

        self.lfish_diet_sediment_frac = self.percent_to_frac(self.lfish_diet_sediment)
        self.lfish_diet_phytoplankton_frac = self.percent_to_frac(self.lfish_diet_phytoplankton)
        self.lfish_diet_zooplankton_frac = self.percent_to_frac(self.lfish_diet_zooplankton)
        self.lfish_diet_beninv_frac = self.percent_to_frac(self.lfish_diet_beninv)
        self.lfish_diet_filterfeeders_frac = self.percent_to_frac(self.lfish_diet_filterfeeders)
        self.lfish_diet_sfish_frac = self.percent_to_frac(self.lfish_diet_sfish)
        self.lfish_diet_mfish_frac = self.percent_to_frac(self.lfish_diet_mfish)










