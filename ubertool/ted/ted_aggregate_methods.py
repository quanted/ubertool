from __future__ import division  # brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
from numpy import math
import pandas as pd


class TedAggregateMethods(object):
    """
    Aggregate Method class for TED model(logical organizations of functions for a collective purpose).
    """

    def __init__(self):
        """Class representing the functions for Trex"""
        super(TedAggregateMethods, self).__init__()

    def set_global_constants(self):
        # Assigned constants

        self.num_simulations = len(self.chemical_name)

        self.num_simulation_days = 366
        self.day_num = np.arange(366)  # create array of day numbers from 0 - 365

        self.max_distance_from_source = 1000.  # max distance (m) from source for distance calculations

        # constants and conversions
        self.density_h2o = 1.  # kg/L
        self.stan_temp_kelvin = 298.  # temperature in Kelvin for 25degC
        self.gas_const = 8.205e-5  # universal gas constant (atm-m3/mol-K)
        self.hectare_area = 10000.  # area of hectare (m2)
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
        self.h2o_depth_puddles = 1.3  # centimeters; for water depth in Eq.3
        self.h2o_depth_soil = 0.0  # centimeters; for water depth in Eq.3

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

    def spray_drift_params(self, sim_num):
        """
        :description sets spray drift parameters for calculations of distance from source area associated with pesticide concentrations

        :return:
        """

        # set spray drift parameters for estimating distances from source related to downgradient pesticide concentrations (for min/max application scenarios)
        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min = \
        self.set_drift_parameters(self.app_method_min[sim_num], self.boom_hgt_min[sim_num],
                                  self.droplet_spec_min[sim_num])
        self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max = \
        self.set_drift_parameters(self.app_method_max[sim_num], self.boom_hgt_max[sim_num],
                                  self.droplet_spec_max[sim_num])

        # set maximum distances for spray drift calculations for min/max application scenarios
        self.max_drift_distance_minapp = self.set_max_drift_distance(self.app_method_min[sim_num])
        self.max_drift_distance_maxapp = self.set_max_drift_distance(self.app_method_max[sim_num])

    def runoff_params(self, sim_num):
        """
        :description  calculate runoff parameters for min/max application scenarios

        :return:
        """

        # runoff parameters (represents OPP TED Excel model worksheet 'plants' columns C & D rows 3 - 5
        self.pest_incorp_min, self.runoff_frac_min = self.calc_runoff_params(sim_num, self.app_method_min[sim_num], self.app_rate_min[sim_num], self.pest_incorp_depth_min[sim_num])
        self.pest_incorp_max, self.runoff_frac_max = self.calc_runoff_params(sim_num, self.app_method_max[sim_num], self.app_rate_max[sim_num], self.pest_incorp_depth_max[sim_num])

    def plants(self, sim_num):
        """
        :description executes collection of functions/methods associated with the 'plants' worksheet in the OPP TED Excel model

        :return:
        """

        # calculate plant toxicity to application rate (min/max) ratios across all simulations
        # (represents columns G & H rows 205 - 224 of OPP TED Excel spreadsheet 'inputs' worksheet)
        self.calc_plant_tox_ratios()

        # calculate plant runoff-based EECs for min/max application scenarios
        self.runoff_eec_dry_area_min, self.runoff_eec_semiaq_area_min = self.calc_runoff_based_eec(self.app_rate_min[sim_num], self.pest_incorp_min, self.runoff_frac_min)
        self.runoff_eec_dry_area_max, self.runoff_eec_semiaq_area_max = self.calc_runoff_based_eec(self.app_rate_max[sim_num], self.pest_incorp_max, self.runoff_frac_max)

        # determine if plant EEC due to runoff exceeds various thresholds for pre-emergence of monocots and dicots
        self.plant_risk_conclusions(sim_num)

        # calculate plant risk threshold distances
        self.plant_risk_threshold_distances(sim_num)

    def conc_based_eec_timeseries(self, sim_num):
        """
        :description executes collection of functions/methods associated with the 'min/max rate concentrations' worksheet in the OPP TED Excel model
            # calculate upper bound and mean concentration based EECs for food items (daily values for a year) - min application scenario

        :return:
        """
        # set/reset arrays for holding single simulation results
        self.initialize_eec_arrays()

        # generate daily flag to identify application day numbers within year for min/max application scenarios
        self.app_flags_min_scenario = self.daily_app_flag(self.num_apps_min[sim_num], self.app_interval_min[sim_num])
        self.app_flags_max_scenario = self.daily_app_flag(self.num_apps_max[sim_num], self.app_interval_max[sim_num])

        self.out_diet_eec_upper_min_sg = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_sg, self.app_flags_min_scenario)  # short grass
        self.out_diet_eec_upper_min_tg = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_tg, self.app_flags_min_scenario)  # tall grass
        self.out_diet_eec_upper_min_blp = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_blp, self.app_flags_min_scenario)  # broad-leafed plants
        self.out_diet_eec_upper_min_fp = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_fp, self.app_flags_min_scenario)  # seeds/fruits/pods
        self.out_diet_eec_upper_min_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_arthro, self.app_flags_min_scenario)  # arthropods

        self.out_diet_eec_mean_min_sg = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_mean_sg, self.app_flags_min_scenario)  # short grass
        self.out_diet_eec_mean_min_tg = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_mean_tg, self.app_flags_min_scenario)  # tall grass
        self.out_diet_eec_mean_min_blp = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_mean_blp, self.app_flags_min_scenario)  # broad-leafed plants
        self.out_diet_eec_mean_min_fp = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_mean_fp, self.app_flags_min_scenario)  # seeds/fruits/pods
        self.out_diet_eec_mean_min_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_mean_arthro, self.app_flags_min_scenario)  # arthropods

        # calculate upper bound and mean concentration based EECs for food items (daily values for a year) - max application scenario
        self.out_diet_eec_upper_max_sg = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_upper_sg, self.app_flags_max_scenario)  # short grass
        self.out_diet_eec_upper_max_tg = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_upper_tg, self.app_flags_max_scenario)  # tall grass
        self.out_diet_eec_upper_max_blp = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_upper_blp, self.app_flags_max_scenario)  # broad-leafed plants
        self.out_diet_eec_upper_max_fp = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_upper_fp, self.app_flags_max_scenario)  # seeds/fruits/pods
        self.out_diet_eec_upper_max_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_upper_arthro, self.app_flags_max_scenario)  # arthropods

        self.out_diet_eec_mean_max_sg = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_mean_sg, self.app_flags_max_scenario)  # short grass
        self.out_diet_eec_mean_max_tg = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_mean_tg, self.app_flags_max_scenario)  # tall grass
        self.out_diet_eec_mean_max_blp = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_mean_blp, self.app_flags_max_scenario)  # broad-leafed plants
        self.out_diet_eec_mean_max_fp = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_mean_fp, self.app_flags_max_scenario)  # seeds/fruits/pods
        self.out_diet_eec_mean_max_arthro = self.daily_plant_timeseries(sim_num, self.app_rate_max[sim_num], self.food_multiplier_mean_arthro, self.app_flags_max_scenario)  # arthropods

        # calculate daily soil pore water, soil, puddles, and dew concentrations (min/max application scenarios)
        self.out_conc_pore_h2o_min = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_min[sim_num], self.app_flags_min_scenario, "pore_water")
        self.out_conc_pore_h2o_max = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_max[sim_num], self.app_flags_max_scenario, "pore_water")

        self.out_conc_puddles_min = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_min[sim_num], self.app_flags_min_scenario, "puddles")
        self.out_conc_puddles_max = self.daily_soil_h2o_timeseries(sim_num, self.app_rate_max[sim_num], self.app_flags_max_scenario, "puddles")

        self.out_dew_conc_min = self.daily_plant_dew_timeseries(sim_num, self.out_diet_eec_upper_min_blp)
        self.out_dew_conc_max = self.daily_plant_dew_timeseries(sim_num, self.out_diet_eec_upper_max_blp)

        self.out_soil_conc_min = self.daily_soil_timeseries(sim_num, self.out_conc_pore_h2o_min)
        self.out_soil_conc_max = self.daily_soil_timeseries(sim_num, self.out_conc_pore_h2o_max)

        # calculate daily air (under canopy) concentrations (min/max application scenarios)
        self.out_air_conc_min = self.daily_canopy_air_timeseries(sim_num, self.app_rate_min[sim_num], self.app_flags_min_scenario)
        self.out_air_conc_max = self.daily_canopy_air_timeseries(sim_num, self.app_rate_max[sim_num], self.app_flags_max_scenario)

        # calculate daily concentrations for soil-dwelling invertebrates, small mammals, large mammals, and small birds
        # (min/max application scenarios & upper/mean food multipliers)
        self.out_diet_eec_min_soil_inv = self.daily_soil_inv_timeseries(sim_num, self.out_conc_pore_h2o_min)
        self.out_diet_eec_max_soil_inv = self.daily_soil_inv_timeseries(sim_num, self.out_conc_pore_h2o_max)

        # calculate daily whole body concentrations for prey items (small mammals, large mammals, small birds, small terrestrial phase amphibians/reptiles
        # (min/max application scenarios & upper/mean food multipliers)
        self.out_diet_dose_upper_min_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_min_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_dose_upper_min_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_min_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_dose_upper_min_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_min_arthro,
                                                                                 self.frac_retained_birds[sim_num])
        self.out_diet_dose_upper_min_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_min_arthro,
                                                                                  self.frac_retained_birds[sim_num])

        self.out_diet_dose_mean_min_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_min_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_dose_mean_min_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_min_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_dose_mean_min_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_min_arthro,
                                                                                self.frac_retained_birds[sim_num])
        self.out_diet_dose_mean_min_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_min_arthro,
                                                                                 self.frac_retained_birds[sim_num])

        self.out_diet_dose_upper_max_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_max_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_dose_upper_max_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_max_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_dose_upper_max_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_max_arthro,
                                                                                 self.frac_retained_birds[sim_num])
        self.out_diet_dose_upper_max_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_max_arthro,
                                                                                  self.frac_retained_birds[sim_num])

        self.out_diet_dose_mean_max_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_max_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_dose_mean_max_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_max_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_dose_mean_max_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_max_arthro,
                                                                                self.frac_retained_birds[sim_num])
        self.out_diet_dose_mean_max_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_max_arthro,
                                                                                 self.frac_retained_birds[sim_num])

    def initialize_eec_arrays(self):

        app_flags_min_scenario = np.full(self.num_simulation_days, True, dtype=bool)
        app_flags_max_scenario = np.full(self.num_simulation_days, True, dtype=bool)

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

    def species_doses(self, sim_num):
        """
        :description executes collection of functions/methods associated with the 'min/max rate doses' worksheet in the OPP TED Excel model
            # calculate species/food item specific doses and health measure ratios

        :return:
        """

        # read species properties from database
        self.ReadSpeciesProperties()

        # set value for volumetric fraction of droplet spectrum related to bird respiration limits
        self.max_respire_frac_minapp = self.set_max_respire_frac(self.app_method_min[sim_num], self.droplet_spec_min[sim_num])
        self.max_respire_frac_maxapp = self.set_max_respire_frac(self.app_method_max[sim_num], self.droplet_spec_max[sim_num])