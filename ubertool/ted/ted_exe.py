from __future__ import division
from functools import wraps
import pandas as pd
import numpy as np
import time
import csv, sys
import os.path
import logging


from .ted_functions import TedFunctions
from .ted_aggregate_methods import TedAggregateMethods
from base.uber_model import UberModel, ModelSharedInputs

class TedSpeciesProperties(object):
    """
    Listing of species properties that will eventually be read in from a SQL db
    """

    def __init__(self):
        """Class representing Species properties"""
        super(TedSpeciesProperties, self).__init__()

        self.sci_name = pd.Series([], dtype='object')
        self.com_name = pd.Series([], dtype='object')
        self.taxa = pd.Series([], dtype='object')
        self.order = pd.Series([], dtype='object')
        self.usfws_id = pd.Series([], dtype='object')
        self.body_wgt = pd.Series([], dtype='object')
        self.diet_item = pd.Series([], dtype='object')
        self.h2o_cont = pd.Series([], dtype='float')

    def read_species_properties(self):
        # this is a temporary method to initiate the species/diet food items lists (this will be replaced with
        # a method to access a SQL database containing the properties
        filename = './ted/tests/TEDSpeciesProperties.csv'
        try:
            with open(filename,'rt') as csvfile:
                # csv.DictReader uses first line in file for column headings by default
                dr = pd.read_csv(csvfile) # comma is default delimiter
        except csv.Error as e:
            sys.exit('file: %s, %s' (filename, e))

        print(dr)
        self.sci_name = dr.ix[:,'Scientific Name']
        self.com_name = dr.ix[:,'Common Name']
        self.taxa = dr.ix[:,'Taxa']
        self.order = dr.ix[:,'Order']
        self.usfws_id = dr.ix[:,'USFWS Species ID (ENTITY_ID)']
        self.body_wgt= dr.ix[:,'BW (g)']
        self.diet_item = dr.ix[:,'Food item']
        self.h2o_cont = dr.ix[:,'Water content of diet']

class TedInputs(ModelSharedInputs):
    """
    Required inputs class for Ted.
    """

    def __init__(self):
        """Class representing the inputs for Ted"""
        super(TedInputs, self).__init__()

        # Inputs: Assign object attribute variables from the input Pandas DataFrame

        self.chemical_name = pd.Series([], dtype="object", name="chemical_name")

        # application parameters for min/max application scenarios
        self.crop_min = pd.Series([], dtype="object", name="crop")
        self.app_method_min = pd.Series([], dtype="object", name="app_method_min")
        self.app_rate_min = pd.Series([], dtype="float", name="app_rate_min")
        self.num_apps_min = pd.Series([], dtype="int", name="num_apps_min")
        self.app_interval_min = pd.Series([], dtype="int", name="app_interval_min")

        self.droplet_spec_min = pd.Series([], dtype="object", name="droplet_spec_min")
        self.boom_hgt_min = pd.Series([], dtype="object", name="droplet_spec_min")

        self.pest_incorp_depth_min = pd.Series([], dtype="object", name="pest_incorp_depth")

        self.crop_max = pd.Series([], dtype="object", name="crop")
        self.app_method_max = pd.Series([], dtype="object", name="app_method_max")
        self.app_rate_max = pd.Series([], dtype="float", name="app_rate_max")
        self.num_apps_max = pd.Series([], dtype="int", name="num_app_maxs")
        self.app_interval_max = pd.Series([], dtype="int", name="app_interval_max")

        self.droplet_spec_max = pd.Series([], dtype="object", name="droplet_spec_max")
        self.boom_hgt_max = pd.Series([], dtype="object", name="droplet_spec_max")

        self.pest_incorp_depth_max = pd.Series([], dtype="object", name="pest_incorp_depth")

        # physical, chemical, and fate properties of pesticide
        self.foliar_diss_hlife = pd.Series([], dtype="float", name="foliar_diss_hlife")
        self.aerobic_soil_meta_hlife = pd.Series([], dtype="float", name="aerobic_soil_meta_hlife")
        self.frac_retained_mamm = pd.Series([], dtype="float", name="frac_retained_mamm")
        self.frac_retained_birds = pd.Series([], dtype="float", name="frac_retained_birds")
        self.log_kow = pd.Series([], dtype="float", name="log_kow")
        self.koc = pd.Series([], dtype="float", name="koc")
        self.solubility = pd.Series([], dtype="float", name="solubility")
        self.henry_law_const = pd.Series([], dtype="float", name="henry_law_const")
        
        # bio concentration factors  (ug active ing/kg-ww) / (ug active ing/liter)
        self.aq_plant_algae_bcf_mean = pd.Series([], dtype="float", name="aq_plant_algae_bcf_mean")
        self.aq_plant_algae_bcf_upper = pd.Series([], dtype="float", name="aq_plant_algae_bcf_upper")
        self.inv_bcf_mean = pd.Series([], dtype="float", name="inv_bcf_mean")
        self.inv_bcf_upper = pd.Series([], dtype="float", name="inv_bcf_upper")
        self.fish_bcf_mean = pd.Series([], dtype="float", name="fish_bcf_mean")
        self.fish_bcf_upper = pd.Series([], dtype="float", name="fish_bcf_upper")

        # bounding water concentrations (ug active ing/liter)
        self.water_conc_1 = pd.Series([], dtype="float", name="water_conc_1")  # lower bound
        self.water_conc_2 = pd.Series([], dtype="float", name="water_conc_2")  # upper bound

        # health value inputs

        # naming convention (based on listing from OPP TED Excel spreadsheet 'inputs' worksheet):

        # dbt: dose based toxicity
        # cbt: concentration-based toxicity
        # arbt: application rate-based toxicity
        # 1inmill_mort: 1/million mortality (note initial character is numeral 1, not letter l)
        # 1inten_mort: 10% mortality  (note initial character is numeral 1, not letter l)
        # others are self explanatory

        # dose based toxicity(dbt): mammals  (mg-pest/kg-bw) & weight of test animal (grams)
        self.dbt_mamm_1inmill_mort = pd.Series([], dtype="float", name="dbt_mamm_1inmill_mort")
        self.dbt_mamm_1inten_mort = pd.Series([], dtype="float", name="dbt_mamm_1inten_mort")
        self.dbt_mamm_low_ld50 = pd.Series([], dtype="float", name="dbt_mamm_low_ld50")
        self.dbt_mamm_rat_oral_ld50 = pd.Series([], dtype="float", name="dbt_mamm_1inten_mort")
        self.dbt_mamm_rat_derm_ld50 = pd.Series([], dtype="float", name="dbt_mamm_rat_derm_ld50")
        self.dbt_mamm_rat_inhal_ld50 = pd.Series([], dtype="float", name="dbt_mamm_rat_inhal_ld50")
        self.dbt_mamm_sub_direct = pd.Series([], dtype="float", name="dbt_mamm_sub_direct")
        self.dbt_mamm_sub_indirect = pd.Series([], dtype="float", name="dbt_mamm_sub_indirect")

        self.dbt_mamm_1inmill_mort_wgt = pd.Series([], dtype="float", name="dbt_mamm_1inmill_mort_wgt")
        self.dbt_mamm_1inten_mort_wgt = pd.Series([], dtype="float", name="dbt_mamm_1inten_mort_wgt")
        self.dbt_mamm_low_ld50_wgt = pd.Series([], dtype="float", name="dbt_mamm_low_ld50_wgt")
        self.dbt_mamm_rat_oral_ld50_wgt = pd.Series([], dtype="float", name="dbt_mamm_1inten_mort_wgt")
        self.dbt_mamm_rat_derm_ld50_wgt = pd.Series([], dtype="float", name="dbt_mamm_rat_derm_ld50_wgt")
        self.dbt_mamm_rat_inhal_ld50_wgt = pd.Series([], dtype="float", name="dbt_mamm_rat_inhal_ld50_wgt")
        self.dbt_mamm_sub_direct_wgt = pd.Series([], dtype="float", name="dbt_mamm_sub_direct_wgt")
        self.dbt_mamm_sub_indirect_wgt = pd.Series([], dtype="float", name="dbt_mamm_sub_indirect_wgt")

        # dose based toxicity(dbt): birds  (mg-pest/kg-bw) & weight of test animal (grams)
        self.dbt_bird_1inmill_mort = pd.Series([], dtype="float", name="dbt_bird_1inmill_mort")
        self.dbt_bird_1inten_mort = pd.Series([], dtype="float", name="dbt_bird_1inten_mort")
        self.dbt_bird_low_ld50 = pd.Series([], dtype="float", name="dbt_bird_low_ld50")
        self.dbt_bird_hc05 = pd.Series([], dtype="float", name="dbt_bird_hc05")
        self.dbt_bird_hc50 = pd.Series([], dtype="float", name="dbt_bird_hc50")
        self.dbt_bird_hc95 = pd.Series([], dtype="float", name="dbt_bird_hc95")
        self.dbt_bird_sub_direct = pd.Series([], dtype="float", name="dbt_bird_sub_direct")
        self.dbt_bird_sub_indirect = pd.Series([], dtype="float", name="dbt_bird_sub_indirect")

        self.mineau_sca_fact = pd.Series([], dtype="float", name="mineau_sca_fact")
        
        self.dbt_bird_1inmill_mort_wgt = pd.Series([], dtype="float", name="dbt_bird_1inmill_mort_wgt")
        self.dbt_bird_1inten_mort_wgt = pd.Series([], dtype="float", name="dbt_bird_1inten_mort_wgt")
        self.dbt_bird_low_ld50_wgt = pd.Series([], dtype="float", name="dbt_bird_low_ld50_wgt")
        self.dbt_bird_hc05_wgt = pd.Series([], dtype="float", name="dbt_bird_hc05_wgt")
        self.dbt_bird_hc50_wgt = pd.Series([], dtype="float", name="dbt_bird_hc50_wgt")
        self.dbt_bird_hc95_wgt = pd.Series([], dtype="float", name="dbt_bird_hc95_wgt")
        self.dbt_bird_sub_direct_wgt = pd.Series([], dtype="float", name="dbt_bird_sub_direct_wgt")
        self.dbt_bird_sub_indirect_wgt = pd.Series([], dtype="float", name="dbt_bird_sub_indirect_wgt")

        self.mineau_sca_fact_wgt = pd.Series([], dtype="float", name="mineau_sca_fact_wgt")
        
        # dose based toxicity(dbt): reptiles, terrestrial-phase amphibians  (mg-pest/kg-bw) & weight of test animal (grams)
        self.dbt_reptile_1inmill_mort = pd.Series([], dtype="float", name="dbt_reptile_1inmill_mort")
        self.dbt_reptile_1inten_mort = pd.Series([], dtype="float", name="dbt_reptile_1inten_mort")
        self.dbt_reptile_low_ld50 = pd.Series([], dtype="float", name="dbt_reptile_low_ld50")
        self.dbt_reptile_sub_direct = pd.Series([], dtype="float", name="dbt_reptile_sub_direct")
        self.dbt_reptile_sub_indirect = pd.Series([], dtype="float", name="dbt_reptile_sub_indirect")

        self.dbt_reptile_1inmill_mort_wgt = pd.Series([], dtype="float", name="dbt_reptile_1inmill_mort_wgt")
        self.dbt_reptile_1inten_mort_wgt = pd.Series([], dtype="float", name="dbt_reptile_1inten_mort_wgt")
        self.dbt_reptile_low_ld50_wgt = pd.Series([], dtype="float", name="dbt_reptile_low_ld50_wgt")
        self.dbt_reptile_sub_direct_wgt = pd.Series([], dtype="float", name="dbt_reptile_sub_direct_wgt")
        self.dbt_reptile_sub_indirect_wgt = pd.Series([], dtype="float", name="dbt_reptile_sub_indirect_wgt")

        # concentration-based toxicity (cbt) : mammals (mg-pest/kg-diet food)
        self.cbt_mamm_1inmill_mort = pd.Series([], dtype="float", name="cbt_mamm_1inmill_mort")
        self.cbt_mamm_1inten_mort = pd.Series([], dtype="float", name="cbt_mamm_1inten_mort")
        self.cbt_mamm_low_lc50 = pd.Series([], dtype="float", name="cbt_mamm_low_lc50")
        self.cbt_mamm_sub_direct = pd.Series([], dtype="float", name="cbt_mamm_sub_direct")
        self.cbt_mamm_grow_noec = pd.Series([], dtype="float", name="cbt_mamm_grow_noec")
        self.cbt_mamm_grow_loec = pd.Series([], dtype="float", name="cbt_mamm_grow_loec")
        self.cbt_mamm_repro_noec = pd.Series([], dtype="float", name="cbt_mamm_repro_noec")
        self.cbt_mamm_repro_loec = pd.Series([], dtype="float", name="cbt_mamm_repro_loec")
        self.cbt_mamm_behav_noec = pd.Series([], dtype="float", name="cbt_mamm_behav_noec")
        self.cbt_mamm_behav_loec = pd.Series([], dtype="float", name="cbt_mamm_behav_loec")
        self.cbt_mamm_sensory_noec = pd.Series([], dtype="float", name="cbt_mamm_sensory_noec")
        self.cbt_mamm_sensory_loec = pd.Series([], dtype="float", name="cbt_mamm_sensory_loec")
        self.cbt_mamm_sub_indirect = pd.Series([], dtype="float", name="cbt_mamm_sub_indirect")
        
        # concentration-based toxicity (cbt) : birds (mg-pest/kg-diet food)
        self.cbt_bird_1inmill_mort = pd.Series([], dtype="float", name="cbt_bird_1inmill_mort")
        self.cbt_bird_1inten_mort = pd.Series([], dtype="float", name="cbt_bird_1inten_mort")
        self.cbt_bird_low_lc50 = pd.Series([], dtype="float", name="cbt_bird_low_lc50")
        self.cbt_bird_sub_direct = pd.Series([], dtype="float", name="cbt_bird_sub_direct")
        self.cbt_bird_grow_noec = pd.Series([], dtype="float", name="cbt_bird_grow_noec")
        self.cbt_bird_grow_loec = pd.Series([], dtype="float", name="cbt_bird_grow_loec")
        self.cbt_bird_repro_noec = pd.Series([], dtype="float", name="cbt_bird_repro_noec")
        self.cbt_bird_repro_loec = pd.Series([], dtype="float", name="cbt_bird_repro_loec")
        self.cbt_bird_behav_noec = pd.Series([], dtype="float", name="cbt_bird_behav_noec")
        self.cbt_bird_behav_loec = pd.Series([], dtype="float", name="cbt_bird_behav_loec")
        self.cbt_bird_sensory_noec = pd.Series([], dtype="float", name="cbt_bird_sensory_noec")
        self.cbt_bird_sensory_loec = pd.Series([], dtype="float", name="cbt_bird_sensory_loec")
        self.cbt_bird_sub_indirect = pd.Series([], dtype="float", name="cbt_bird_sub_indirect")
        
        # concentration-based toxicity (cbt) : reptiles, terrestrial-phase amphibians (mg-pest/kg-diet food)
        self.cbt_reptile_1inmill_mort = pd.Series([], dtype="float", name="cbt_reptile_1inmill_mort")
        self.cbt_reptile_1inten_mort = pd.Series([], dtype="float", name="cbt_reptile_1inten_mort")
        self.cbt_reptile_low_lc50 = pd.Series([], dtype="float", name="cbt_reptile_low_lc50")
        self.cbt_reptile_sub_direct = pd.Series([], dtype="float", name="cbt_reptile_sub_direct")
        self.cbt_reptile_grow_noec = pd.Series([], dtype="float", name="cbt_reptile_grow_noec")
        self.cbt_reptile_grow_loec = pd.Series([], dtype="float", name="cbt_reptile_grow_loec")
        self.cbt_reptile_repro_noec = pd.Series([], dtype="float", name="cbt_reptile_repro_noec")
        self.cbt_reptile_repro_loec = pd.Series([], dtype="float", name="cbt_reptile_repro_loec")
        self.cbt_reptile_behav_noec = pd.Series([], dtype="float", name="cbt_reptile_behav_noec")
        self.cbt_reptile_behav_loec = pd.Series([], dtype="float", name="cbt_reptile_behav_loec")
        self.cbt_reptile_sensory_noec = pd.Series([], dtype="float", name="cbt_reptile_sensory_noec")
        self.cbt_reptile_sensory_loec = pd.Series([], dtype="float", name="cbt_reptile_sensory_loec")
        self.cbt_reptile_sub_indirect = pd.Series([], dtype="float", name="cbt_reptile_sub_indirect")

        # concentration-based toxicity (cbt) : invertebrates body weight (mg-pest/kg-bw(ww))
        self.cbt_inv_bw_1inmill_mort = pd.Series([], dtype="float", name="cbt_inv_bw_1inmill_mort")
        self.cbt_inv_bw_1inten_mort = pd.Series([], dtype="float", name="cbt_inv_bw_1inten_mort")
        self.cbt_inv_bw_low_lc50 = pd.Series([], dtype="float", name="cbt_inv_bw_low_lc50")
        self.cbt_inv_bw_sub_direct = pd.Series([], dtype="float", name="cbt_inv_bw_sub_direct")
        self.cbt_inv_bw_grow_noec = pd.Series([], dtype="float", name="cbt_inv_bw_grow_noec")
        self.cbt_inv_bw_grow_loec = pd.Series([], dtype="float", name="cbt_inv_bw_grow_loec")
        self.cbt_inv_bw_repro_noec = pd.Series([], dtype="float", name="cbt_inv_bw_repro_noec")
        self.cbt_inv_bw_repro_loec = pd.Series([], dtype="float", name="cbt_inv_bw_repro_loec")
        self.cbt_inv_bw_behav_noec = pd.Series([], dtype="float", name="cbt_inv_bw_behav_noec")
        self.cbt_inv_bw_behav_loec = pd.Series([], dtype="float", name="cbt_inv_bw_behav_loec")
        self.cbt_inv_bw_sensory_noec = pd.Series([], dtype="float", name="cbt_inv_bw_sensory_noec")
        self.cbt_inv_bw_sensory_loec = pd.Series([], dtype="float", name="cbt_inv_bw_sensory_loec")
        self.cbt_inv_bw_sub_indirect = pd.Series([], dtype="float", name="cbt_inv_bw_sub_indirect")
        
        # concentration-based toxicity (cbt) : invertebrates body diet (mg-pest/kg-food(ww))
        self.cbt_inv_food_1inmill_mort = pd.Series([], dtype="float", name="cbt_inv_food_1inmill_mort")
        self.cbt_inv_food_1inten_mort = pd.Series([], dtype="float", name="cbt_inv_food_1inten_mort")
        self.cbt_inv_food_low_lc50 = pd.Series([], dtype="float", name="cbt_inv_food_low_lc50")
        self.cbt_inv_food_sub_direct = pd.Series([], dtype="float", name="cbt_inv_food_sub_direct")
        self.cbt_inv_food_grow_noec = pd.Series([], dtype="float", name="cbt_inv_food_grow_noec")
        self.cbt_inv_food_grow_loec = pd.Series([], dtype="float", name="cbt_inv_food_grow_loec")
        self.cbt_inv_food_repro_noec = pd.Series([], dtype="float", name="cbt_inv_food_repro_noec")
        self.cbt_inv_food_repro_loec = pd.Series([], dtype="float", name="cbt_inv_food_repro_loec")
        self.cbt_inv_food_behav_noec = pd.Series([], dtype="float", name="cbt_inv_food_behav_noec")
        self.cbt_inv_food_behav_loec = pd.Series([], dtype="float", name="cbt_inv_food_behav_loec")
        self.cbt_inv_food_sensory_noec = pd.Series([], dtype="float", name="cbt_inv_food_sensory_noec")
        self.cbt_inv_food_sensory_loec = pd.Series([], dtype="float", name="cbt_inv_food_sensory_loec")
        self.cbt_inv_food_sub_indirect = pd.Series([], dtype="float", name="cbt_inv_food_sub_indirect")
  
        # concentration-based toxicity (cbt) : invertebrates soil (mg-pest/kg-soil(dw))
        self.cbt_inv_soil_1inmill_mort = pd.Series([], dtype="float", name="cbt_inv_soil_1inmill_mort")
        self.cbt_inv_soil_1inten_mort = pd.Series([], dtype="float", name="cbt_inv_soil_1inten_mort")
        self.cbt_inv_soil_low_lc50 = pd.Series([], dtype="float", name="cbt_inv_soil_low_lc50")
        self.cbt_inv_soil_sub_direct = pd.Series([], dtype="float", name="cbt_inv_soil_sub_direct")
        self.cbt_inv_soil_grow_noec = pd.Series([], dtype="float", name="cbt_inv_soil_grow_noec")
        self.cbt_inv_soil_grow_loec = pd.Series([], dtype="float", name="cbt_inv_soil_grow_loec")
        self.cbt_inv_soil_repro_noec = pd.Series([], dtype="float", name="cbt_inv_soil_repro_noec")
        self.cbt_inv_soil_repro_loec = pd.Series([], dtype="float", name="cbt_inv_soil_repro_loec")
        self.cbt_inv_soil_behav_noec = pd.Series([], dtype="float", name="cbt_inv_soil_behav_noec")
        self.cbt_inv_soil_behav_loec = pd.Series([], dtype="float", name="cbt_inv_soil_behav_loec")
        self.cbt_inv_soil_sensory_noec = pd.Series([], dtype="float", name="cbt_inv_soil_sensory_noec")
        self.cbt_inv_soil_sensory_loec = pd.Series([], dtype="float", name="cbt_inv_soil_sensory_loec")
        self.cbt_inv_soil_sub_indirect = pd.Series([], dtype="float", name="cbt_inv_soil_sub_indirect")

        # application rate-based toxicity (arbt) : mammals  (lbs active ingredient/Acre)
        self.arbt_mamm_mort = pd.Series([], dtype="float", name="arbt_mamm_mort")
        self.arbt_mamm_growth = pd.Series([], dtype="float", name="arbt_mamm_growth")
        self.arbt_mamm_repro = pd.Series([], dtype="float", name="arbt_mamm_repro")
        self.arbt_mamm_behav = pd.Series([], dtype="float", name="arbt_mamm_behav")
        self.arbt_mamm_sensory = pd.Series([], dtype="float", name="arbt_mamm_sensory")

        # application rate-based toxicity (arbt) : birds  (lbs active ingredient/Acre)
        self.arbt_bird_mort = pd.Series([], dtype="float", name="arbt_bird_mort")
        self.arbt_bird_growth = pd.Series([], dtype="float", name="arbt_bird_growth")
        self.arbt_bird_repro = pd.Series([], dtype="float", name="arbt_bird_repro")
        self.arbt_bird_behav = pd.Series([], dtype="float", name="arbt_bird_behav")
        self.arbt_bird_sensory = pd.Series([], dtype="float", name="arbt_bird_sensory")
        
        # application rate-based toxicity (arbt) : reptiles  (lbs active ingredient/Acre)
        self.arbt_reptile_mort = pd.Series([], dtype="float", name="arbt_reptile_mort")
        self.arbt_reptile_growth = pd.Series([], dtype="float", name="arbt_reptile_growth")
        self.arbt_reptile_repro = pd.Series([], dtype="float", name="arbt_reptile_repro")
        self.arbt_reptile_behav = pd.Series([], dtype="float", name="arbt_reptile_behav")
        self.arbt_reptile_sensory = pd.Series([], dtype="float", name="arbt_reptile_sensory")
        
        # application rate-based toxicity (arbt) : invertebrates  (lbs active ingredient/Acre)
        self.arbt_inv_1inmill_mort = pd.Series([], dtype="float", name="arbt_inv_1inmill_mort")
        self.arbt_inv_1inten_mort = pd.Series([], dtype="float", name="arbt_inv_1inten_mort")
        self.arbt_inv_sub_direct = pd.Series([], dtype="float", name="arbt_inv_sub_direct")
        self.arbt_inv_sub_indirect = pd.Series([], dtype="float", name="arbt_inv_sub_indirect")
        self.arbt_inv_growth = pd.Series([], dtype="float", name="arbt_inv_growth")
        self.arbt_inv_repro = pd.Series([], dtype="float", name="arbt_inv_repro")
        self.arbt_inv_behav = pd.Series([], dtype="float", name="arbt_inv_behav")
        self.arbt_inv_sensory = pd.Series([], dtype="float", name="arbt_inv_sensory")
        
        # plant toxicity (pt) : monocots (lbs active ingredient/Acre)
        self.pt_mono_pre_noec = pd.Series([], dtype="float", name="pt_mono_pre_noec")
        self.pt_mono_pre_loec = pd.Series([], dtype="float", name="pt_mono_pre_loec")
        self.pt_mono_pre_ec25 = pd.Series([], dtype="float", name="pt_mono_pre_ec25")
        self.pt_mono_post_noec = pd.Series([], dtype="float", name="pt_mono_post_noec")
        self.pt_mono_post_loec = pd.Series([], dtype="float", name="pt_mono_post_loec")
        self.pt_mono_post_ec25 = pd.Series([], dtype="float", name="pt_mono_post_ec25")
        self.pt_mono_dir_mort = pd.Series([], dtype="float", name="pt_mono_dir_mort")
        self.pt_mono_indir_mort = pd.Series([], dtype="float", name="pt_mono_indir_mort")
        self.pt_mono_dir_repro = pd.Series([], dtype="float", name="pt_mono_dir_repro")
        self.pt_mono_indir_repro = pd.Series([], dtype="float", name="pt_mono_indir_repro")
        
        # plant toxicity (pt) : dicots (lbs active ingredient/Acre)
        self.pt_dicot_pre_noec = pd.Series([], dtype="float", name="pt_dicot_pre_noec")
        self.pt_dicot_pre_loec = pd.Series([], dtype="float", name="pt_dicot_pre_loec")
        self.pt_dicot_pre_ec25 = pd.Series([], dtype="float", name="pt_dicot_pre_ec25")
        self.pt_dicot_post_noec = pd.Series([], dtype="float", name="pt_dicot_post_noec")
        self.pt_dicot_post_loec = pd.Series([], dtype="float", name="pt_dicot_post_loec")
        self.pt_dicot_post_ec25 = pd.Series([], dtype="float", name="pt_dicot_post_ec25")
        self.pt_dicot_dir_mort = pd.Series([], dtype="float", name="pt_dicot_dir_mort")
        self.pt_dicot_indir_mort = pd.Series([], dtype="float", name="pt_dicot_indir_mort")
        self.pt_dicot_dir_repro = pd.Series([], dtype="float", name="pt_dicot_dir_repro")
        self.pt_dicot_indir_repro = pd.Series([], dtype="float", name="pt_dicot_indir_repro")

class TedOutputs(object):
    """
    Output class for Ted.
    """

    def __init__(self):
        """Class representing the outputs for Ted"""
        super(TedOutputs, self).__init__()

        self.out_diet_eec_upper_min_sg_maxdaily = pd.Series([], dtype='float', name="out_diet_eec_upper_min_sg_maxdaily")


class Ted(UberModel, TedInputs, TedOutputs, TedFunctions, TedAggregateMethods, TedSpeciesProperties):  # others? ...e.g. TrexFunctions, TherpsFunctions):
    """
    Estimate relevant dietary and environmental exposure concentrations (EECs) of pesticides applied to crops
    and resulting doses/risks for birds, mammals, amphibians, and reptiles
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Ted model and containing all its methods"""
        super(Ted, self).__init__()
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

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()

        # calculate aquatic dependent dietary concentration thresholds for mammals, birds, and reptiles/amphibians
        self.calc_plant_tox_ratios()              # for all simulations

        # calculate aquatic dependent species concentration thresholds for dietary items (i.e., algae, invertebraters, and reptiles/amphibians)
        self.calc_aquatic_vert_conc_thresholds()  # for all simulations (worksheet 'Aquatic dependent sp thresholds')

        # calculate estimated tissue concentrations in aquatic invertebrates and fish using BCFs (worksheet 'aquatic organism tissue concs')
        self.calc_aq_invert_fish_concs()          # for all simulations

        # read species properties from database
        self.read_species_properties()

        # calculate species body surface areas
        self.calc_species_surface_area()

        # calculate species specific volume of air respired
        self.calc_species_inhalation_vol()

        # process simulations--------------------------------------------------------------------
        for sim_num in range(self.num_simulations):

            # TODO: need to decide which of the following variables are to be outputs; currently they are (I guess we could populate
            # TODO: an EXCEL spreadsheet to match that of OPP)

            # set spray drift parameters
            self.spray_drift_params(sim_num)

            # calculate runoff parameters for min/max application scenarios
            self.runoff_params(sim_num)

            # execute plant related methods and functions ;  worksheet 'plants' in OPP TED Excel model
            self.plants(sim_num)

            # calculate daily time series of concentration based EECs (worksheets 'min/max rate concentrations' in OPP TED Excel model
            self.conc_based_eec_timeseries(sim_num)

            # count number of exceedances of various risk thresholds within eec timeseries (worksheets 'Min/Max rate - dietary conc results')
            self.eec_exceedances(sim_num)

            # calculate spray drfit distances from source area to max daily food item concentration (worksheets 'Min/Max rate - dietary conc results')
            self.eec_drift_distances(sim_num)

            # calculate species/food item specific doses via intake pathways and related health measure ratios ; worksheets 'min/max rate doses' in OPP TED Excel model
            self.species_doses(sim_num)