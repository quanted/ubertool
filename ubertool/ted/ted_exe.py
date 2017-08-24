from __future__ import division
from functools import wraps
import pandas as pd
import numpy as np
import time
import csv, sys
import os.path


from .ted_functions import TedFunctions
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

    def ReadSpeciesProperties(self):
        # this is a temporary method to initiate the species/diet food items lists (this will be replaced with
        # a method to access a SQL database containing the properties
        filename = 'TEDSpeciesProperties.csv'
        try:
            with open(filename,'rt') as csvfile:
                # csv.DictReader uses first line in file for column headings by default
                dr = pd.read_csv(csvfile) # comma is default delimiter
        except csv.Error as e:
            sys.exit('file: %s, %s' (filename, e))

        print(dr)
        sci_name = dr.ix[:,'Scientific Name']
        com_name = dr.ix[:,'Common Name']
        taxa = dr.ix[:,'Taxa']
        order = dr.ix[:,'Order']
        usfws_id = dr.ix[:,'USFWS Species ID (ENTITY_ID)']
        body_wgt= dr.ix[:,'BW (g)']
        diet_item = dr.ix[:,'Food item']
        h2o_cont = dr.ix[:,'Water content of diet']

class TedInputs(ModelSharedInputs):
    """
    Required inputs class for Ted.
    """

    def __init__(self):
        """Class representing the inputs for Ted"""
        super(TedInputs, self).__init__()

        # Inputs: Assign object attribute variables from the input Pandas DataFrame

        self.chem_name = pd.Series([], dtype="object", name="chem_name")

        # application parameters for min/max application scenarios
        self.crop_min = pd.Series([], dtype="object", name="crop")
        self.app_method_min = pd.Series([], dtype="object", name="app_method_min")
        self.app_rate_min = pd.Series([], dtype="float", name="app_rate_min")
        self.num_apps_min = pd.Series([], dtype="int", name="num_apps_min")
        self.app_interval_min = pd.Series([], dtype="int", name="app_interval_min")

        self.droplet_spec_min = pd.Series([], dtype="object", name="droplet_spec_min")
        self.boom_hgt_min = pd.Series([], dtype="float", name="droplet_spec_min")

        self.crop_max = pd.Series([], dtype="object", name="crop")
        self.app_method_max = pd.Series([], dtype="object", name="app_method_max")
        self.app_rate_max = pd.Series([], dtype="float", name="app_rate_max")
        self.num_apps_max = pd.Series([], dtype="int", name="num_app_maxs")
        self.app_interval_max = pd.Series([], dtype="int", name="app_interval_max")

        self.droplet_spec_max = pd.Series([], dtype="object", name="droplet_spec_max")
        self.boom_hgt_max = pd.Series([], dtype="float", name="droplet_spec_max")

        # physical, chemical, and fate properties of pesticide
        self.foliar_diss_hlife = pd.Series([], dtype="float", name="foliar_diss_hlife")
        self.aerobic_soil_meta_hlife = pd.Series([], dtype="float", name="aerobic_soil_meta_hlife")
        self.frac_retained_mammals = pd.Series([], dtype="float", name="frac_retained_mammals")
        self.frac_retained_birds = pd.Series([], dtype="float", name="frac_retained_birds")
        self.log_kow = pd.Series([], dtype="float", name="log_kow")
        self.koc = pd.Series([], dtype="float", name="koc")
        self.solubility = pd.Series([], dtype="float", name="solubility")
        self.henry_law_const = pd.Series([], dtype="float", name="henry_law_const")

        # self.mineau_sca_fact = pd.Series([], dtype="float", name="mineau_sca_fact")
        #
        # self.ld50_bird = pd.Series([], dtype="float")
        # self.lc50_bird = pd.Series([], dtype="float")
        # self.noaec_bird = pd.Series([], dtype="float")
        # self.noael_bird = pd.Series([], dtype="float")
        # self.aw_bird_sm = pd.Series([], dtype="float")  # body weight of assessed bird (small)
        # self.aw_bird_md = pd.Series([], dtype="float")  # body weight of assessed bird (medium)
        # self.aw_bird_lg = pd.Series([], dtype="float")  # body weight of assessed bird (large)
        # self.tw_bird_ld50 = pd.Series([], dtype="float")
        # self.tw_bird_lc50 = pd.Series([], dtype="float")
        # self.tw_bird_noaec = pd.Series([], dtype="float")
        # self.tw_bird_noael = pd.Series([], dtype="float")
        #
        # self.species_of_the_tested_bird_avian_ld50 = pd.Series([], dtype="object")
        # self.species_of_the_tested_bird_avian_lc50 = pd.Series([], dtype="object")
        # self.species_of_the_tested_bird_avian_noaec = pd.Series([], dtype="object")
        # self.species_of_the_tested_bird_avian_noael = pd.Series([], dtype="object")
        #
        # self.ld50_mamm = pd.Series([], dtype="float")
        # self.lc50_mamm = pd.Series([], dtype="float")
        # self.noaec_mamm = pd.Series([], dtype="float")
        # self.noael_mamm = pd.Series([], dtype="float")
        # self.aw_mamm_sm = pd.Series([], dtype="float")  # body weight of assessed mammal (small)
        # self.aw_mamm_md = pd.Series([], dtype="float")  # body weight of assessed mammal (medium)
        # self.aw_mamm_lg = pd.Series([], dtype="float")  # body weight of assessed mammal (large)
        # self.tw_mamm = pd.Series([], dtype="float")  # body weight of tested mammal


class TedOutputs(object):
    """
    Output class for Ted.
    """

    def __init__(self):
        """Class representing the outputs for Ted"""
        super(TedOutputs, self).__init__()

        self.out_diet_eec_upper_min_sg_maxdaily = pd.Series([], dtype='float', name="out_diet_eec_upper_min_sg_maxdaily")


class Ted(UberModel, TedInputs, TedOutputs, TedFunctions, TedSpeciesProperties):  # others? ...e.g. TrexFunctions, TherpsFunctions):
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

        # read species properties from database
        self.ReadSpeciesProperties()

        # Define constants and perform units conversions on necessary raw inputs
        self.set_global_constants()

        # process simulations--------------------------------------------------------------------

        for sim_num in range(self.num_simulations):

            # TODO: need to decide which of the following variables are to be outputs; currently they are (I guess we could populate
            # TODO: an EXCEL spreadsheet to match that of OPP)

            # set/reset arrays for holding single simulation results
            self.intialize_eec_arrays()


            # set spray drift parameters for estimating distances from source related to downgradient pesticide concentrations (for min/max application scenarios)
            drift_param_a_min, drift_param_b_min, drift_param_c_min = self.set_drift_parameters(self.app_method_min[sim_num], self.boom_hgt_min[sim_num], self.droplet_spec_min[sim_num])
            drift_param_a_max, drift_param_b_max, drift_param_c_max = self.set_drift_parameters(self.app_method_max[sim_num], self.boom_hgt_max[sim_num], self.droplet_spec_max[sim_num])

            # calculate daily time series of conentration based EECs (TED Worksheets : 'Min rate concentrations' & 'Max rate concentration)

            # generate daily flag to identify application day number within year for min/max application scenarios
            app_flags_min_scenario = self.daily_app_flag(self.num_apps_min[sim_num], self.app_interval_min[sim_num])
            app_flags_max_scenario = self.daily_app_flag(self.num_apps_max[sim_num], self.app_interval_max[sim_num])

            # calculate upper bound and mean concentration based EECs for food items (daily values for a year) - min application scenario
            self.out_diet_eec_upper_min_sg = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_upper_sg, app_flags_min_scenario)  # short grass
            self.out_diet_eec_upper_min_tg = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_upper_tg,  app_flags_min_scenario)  # tall grass
            self.out_diet_eec_upper_min_blp = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_upper_blp, app_flags_min_scenario)  # broad-leafed plants
            self.out_diet_eec_upper_min_fp = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_upper_fp, app_flags_min_scenario)  # seeds/fruits/pods
            self.out_diet_eec_upper_min_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_upper_arthro, app_flags_min_scenario)  # arthropods

            self.out_diet_eec_mean_min_sg = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_mean_sg, app_flags_min_scenario)  # short grass
            self.out_diet_eec_mean_min_tg = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_mean_tg, app_flags_min_scenario)  # tall grass
            self.out_diet_eec_mean_min_blp = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_mean_blp, app_flags_min_scenario)  # broad-leafed plants
            self.out_diet_eec_mean_min_fp = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_mean_fp, app_flags_min_scenario)  # seeds/fruits/pods
            self.out_diet_eec_mean_min_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_min, self.food_multiplier_mean_arthro, app_flags_min_scenario)  # arthropods

            # calculate upper bound and mean concentration based EECs for food items (daily values for a year) - max application scenario
            self.out_diet_eec_upper_max_sg = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_upper_sg, app_flags_max_scenario)  # short grass
            self.out_diet_eec_upper_max_tg = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_upper_tg, app_flags_max_scenario)  # tall grass
            self.out_diet_eec_upper_max_blp = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_upper_blp, app_flags_max_scenario)  # broad-leafed plants
            self.out_diet_eec_upper_max_fp = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_upper_fp, app_flags_max_scenario)  # seeds/fruits/pods
            self.out_diet_eec_upper_max_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_upper_arthro, app_flags_max_scenario)  # arthropods

            self.out_diet_eec_mean_max_sg = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_mean_sg, app_flags_max_scenario)  # short grass
            self.out_diet_eec_mean_max_tg = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_mean_tg, app_flags_max_scenario)  # tall grass
            self.out_diet_eec_mean_max_blp = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_mean_blp, app_flags_max_scenario)  # broad-leafed plants
            self.out_diet_eec_mean_max_fp = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_mean_fp, app_flags_max_scenario)  # seeds/fruits/pods
            self.out_diet_eec_mean_max_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_max, self.food_multiplier_mean_arthro, app_flags_max_scenario)  # arthropods

            # calculate daily soil pore water, soil, puddles, and dew concentrations (min/max application scenarios)
            self.out_conc_pore_h2o_min = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_min, app_flags_min_scenario, "pore_water")
            self.out_conc_pore_h2o_max = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_max, app_flags_max_scenario, "pore_water")

            self.out_conc_puddles_min = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_min, app_flags_min_scenario, "puddles")
            self.out_conc_puddles_max = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_max, app_flags_max_scenario, "puddles")

            self.out_dew_conc_min = self.daily_plant_dew_timeseries(sim_num, self.out_diet_eec_upper_min_blp)
            self.out_dew_conc_max = self.daily_plant_dew_timeseries(sim_num, self.out_diet_eec_upper_max_blp)

            self.out_soil_conc_min = self.daily_soil_timeseries(sim_num, self.out_conc_pore_h20_min)
            self.out_soil_conc_max = self.daily_soil_timeseries(sim_num, self.out_conc_pore_h20_max)

            # calculate daily air (under canopy) concentrations (min/max application scenarios)
            self.out_air_conc_min = self.daily_canopy_air_timeseries(sim_num, self.app_rate_min, app_flags_min_scenario)
            self.out_air_conc_max = self.daily_canopy_air_timeseries(sim_num, self.app_rate_max, app_flags_max_scenario)

            # calculate daily concentrations for soil-dwelling invertebrates, small mammals, large mammals, and small birds
            # (min/max application scenarios & upper/mean food multipliers)
            self.out_diet_eec_min_soil_inv = self.daily_soil_inv_timeseries(sim_num, self.out_conc_pore_h20_min)
            self.out_diet_eec_max_soil_inv = self.daily_soil_inv_timeseries(sim_num, self.out_conc_pore_h20_max)

            # calculate daily whole body concentrations for prey items (small mammals, large mammals, small birds, small terrestrial phase amphibians/reptiles
            # (min/max application scenarios & upper/mean food multipliers)
            self.out_diet_dose_upper_min_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_min_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_upper_min_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_min_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_upper_min_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_min_arthro, self.frac_retained_birds[sim_num])
            self.out_diet_dose_upper_min_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_min_arthro, self.frac_retained_birds[sim_num])

            self.out_diet_dose_mean_min_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_min_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_mean_min_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_min_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_mean_min_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_min_arthro, self.frac_retained_birds[sim_num])
            self.out_diet_dose_mean_min_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_min_arthro, self.frac_retained_birds[sim_num])

            self.out_diet_dose_upper_max_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_max_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_upper_max_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_max_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_upper_max_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_max_arthro, self.frac_retained_birds[sim_num])
            self.out_diet_dose_upper_max_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_max_arthro, self.frac_retained_birds[sim_num])

            self.out_diet_dose_mean_max_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_max_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_mean_max_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_max_sg, self.frac_retained_mamm[sim_num])
            self.out_diet_dose_mean_max_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_max_arthro, self.frac_retained_birds[sim_num])
            self.out_diet_dose_mean_max_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_max_arthro, self.frac_retained_birds[sim_num])

    def set_global_constants(self):
        # Assigned constants

        self.num_simulations = len(self.chem_name)

        self.num_simulation_days = 366.
        self.day_num = np.arange(366)  # create array of day numbers from 0 - 365

        # constants and conversions
        self.density_h2o = 1.  # kg/L
        self.stan_temp_kelvin = 298.  # temperature in Kelvin for 25degC
        self.gas_const = 8.205e-5  # universal gas constant (atm-m3/mol-K)
        self_hectare_area = 10000.  # area of hectare (m2)
        self.lbs_to_gms = 453.592
        self.hectare_to_acre = 2.47105
        self.gms_to_mg = 1000.
        self.m3_to_liters = 1000.

        self.unitless_henry_law = self.henry_law_const / (self.gas_const * self.stan_temp_kelvin)
        self.log_unitless_hlc = np.log10(self.unitless_henry_law)

        # initial residue concentration multiplier (upper bound)
        self.food_multiplier_upper_sg = 240.  # short grass
        self.food_multiplier_upper_tg = 110.  # tall grass
        self.food_multiplier_upper_blp = 135.  # broad-leafed plants
        self.food_multiplier_upper_fp = 15.  # fruits/pods
        self.food_multiplier_upper_arthro = 94.  # arthropods

        # mean residue concentration multiplier (mean)
        self.food_multiplier_mean_sg = 85.  # short grass
        self.food_multiplier_mean_tg = 36.  # tall grass
        self.food_multiplier_mean_blp = 45.  # broad-leafed plants
        self.food_multiplier_mean_fp = 7.  # fruits/pods
        self.food_multiplier_mean_arthro = 65.  # arthropods

        # soil properties
        self.soil_depth = 2.6  # cm
        self.soil_foc = 0.015
        self.app_rate_conv = 11.2  # conversion factor used to convert units of application rate (lbs a.i./acre) to (ug a.i./mL); assuming 1 inch depth of soil
        self.soil_particle_density = 2.65  # kg/L
        self.soil_bulk_density = 1.5  # kg/L
        self.soil_porosity = (1. - (self.soil_bulk_density / self.soil_particle_density))
        self_h2o_depth_puddles = 1.3  # centimeters; for water depth in Eq.3
        self_h2o_depth_soil = 0.0  # centimeters; for water depth in Eq.3

        # earthworm properties
        self.lipid_earthworm = 0.01  # lipid content of earthworm
        self.density_earthworm = 1.0  # assumed equivalent to water

        # broad leaf plant properties (for determining pesticide concentration in dew)
        self.frac_pest_on_surface = 0.62  # from Eq 11; accounts for the amount of pesticide that is present on leaf surface and thus may partition between waxy layer and dew
        self.mass_wax = 0.012  # central tendency of mass of wax on broadleaf plants kg/m2

        self.crop_hgt = 1.  # default crop height (m) for use in Eq.26
        self.mass_plant = 25000.  # mass of plant (crop) per hectare (kg)
        self.density_plant = 0.77  # the density of the crop tissue assumed as fresh leaf (kg/L)

        # fraction of water in fresh food items (Table A 1-7.4 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
        self.frac_h2o_amphi = 0.85
        self.frac_h2o_arthro = 0.69
        self.frac_h2o_aq_plant = 0.8
        self.frac_h2o_ben_invert = 0.78
        self.frac_h2o_bird_mamm = 0.68
        self.frac_h2o_broadleaves = 0.85
        self.frac_h2o_fruit = 0.77
        self.frac_h2o_fish = 0.75
        self.frac_h2o_grass = 0.79
        self.frac_h2o_filt_feeder = 0.82
        self.frac_h2o_nectar = 0.70
        self.frac_h2o_pollen = 0.063
        self.frac_h2o_soil_inv = 0.84
        self.frac_h2o_reptile = 0.66
        self.frac_h2o_seeds = 0.093
        self.frac_h2o_zooplanton = 0.83

        # parameters used to calculate food intake rate for vertebrates (Table A 1-7.5 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
        self.intake_param_a1_birds_gen = 0.648  # these ..._gen parameter values are used in calculation of concentration based EECs (see OPP TED worksheet 'Min rate concentrations' column J)
        self.intake_param_b1_birds_gen = 0.651
        self.intake_param_a1_birds_pass = 0.398
        self.intake_param_b1_birds_pass = 0.850
        self.intake_param_a1_birds_nonpass = 0.301
        self.intake_param_b1_birds_nonpass = 0.751
        self.intake_param_a1_mamm_rodent = 0.621
        self.intake_param_b1_mamm_rodent = 0.564
        self.intake_param_a1_mamm_nonrodent = 0.235
        self.intake_param_b1_mamm_nonrodent = 0.822
        self.intake_param_a1_rep_amphi = 0.013
        self.intake_param_b1_rep_amphi = 0.773

        # generic animal bodyweights (for use in daily allometric dietary consumption rate calculations)
        self.mamm_sm_bodywgt = 15.  # gms
        self.mamm_lg_bodywgt = 1000.  # gms
        self.bird_sm_bodywgt = 20.  # gms
        self.rep_amphi_bodywgt = 2. # gms

    def initialize_eec_arrays(self):

        app_flags_min_scenario = np.zeros(self.num_simulation_days)
        app_flags_max_scenario = np.zeros(self.num_simulation_days)

        self.out_diet_eec_upper_min_sg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_tg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_blp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_fp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_arthro = np.zeros(self.num_simulation_days)

        self.out_diet_eec_mean_min_sg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_tg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_blp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_fp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_arthro = np.zeros(self.num_simulation_days)

        self.out_diet_eec_upper_max_sg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_tg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_blp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_fp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_arthro = np.zeros(self.num_simulation_days)

        self.out_diet_eec_mean_max_sg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_tg = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_blp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_fp = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_arthro = np.zeros(self.num_simulation_days)

        self.out_conc_pore_h2o_min = np.zeros(self.num_simulation_days)
        self.out_conc_pore_h2o_max = np.zeros(self.num_simulation_days)

        self.out_conc_puddles_min = np.zeros(self.num_simulation_days)
        self.out_conc_puddles_max = np.zeros(self.num_simulation_days)

        self.out_dew_conc_min = np.zeros(self.num_simulation_days)
        self.out_dew_conc_max = np.zeros(self.num_simulation_days)

        self.out_soil_conc_min = np.zeros(self.num_simulation_days)
        self.out_soil_conc_max = np.zeros(self.num_simulation_days)

        self.out_air_conc_min = np.zeros(self.num_simulation_days)
        self.out_air_conc_max = np.zeros(self.num_simulation_days)

        self.out_diet_eec_min_soil_inv = np.zeros(self.num_simulation_days)
        self.out_diet_eec_max_soil_inv = np.zeros(self.num_simulation_days)

        self.out_diet_dose_upper_min_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_upper_min_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_upper_min_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_dose_upper_min_sm_amphi = np.zeros(self.num_simulation_days)

        self.out_diet_dose_mean_min_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_mean_min_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_mean_min_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_dose_mean_min_sm_amphi = np.zeros(self.num_simulation_days)

        self.out_diet_dose_upper_max_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_upper_max_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_upper_max_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_dose_upper_max_sm_amphi = np.zeros(self.num_simulation_days)

        self.out_diet_dose_mean_max_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_mean_max_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_dose_mean_max_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_dose_mean_max_sm_amphi = np.zeros(self.num_simulation_days)

