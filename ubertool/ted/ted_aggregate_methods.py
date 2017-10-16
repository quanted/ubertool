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

        self.num_ts = 11   # number of food item daily time series to be processed to determine number of exceedances of EECs
        self.num_tox = 13  # number of toxicity measures to be processed to determine number of exceedances of EECs

        # constants and conversions
        self.density_h2o = 1.  # kg/L
        self.stan_temp_kelvin = 298.  # temperature in Kelvin for 25degC
        self.gas_const = 8.205e-5  # universal gas constant (atm-m3/mol-K)
        self.hectare_area = 10000.  # area of hectare (m2)
        self.lbs_to_gms = 453.592
        self.hectare_to_acre = 2.47105
        self.gms_to_mg = 1000.
        self.m3_to_liters = 1000.
        self.mg_to_ug = 1000.

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

        # concentration levels in water (ug/L) used in calculating aquatic invertebrate and fish tissue concentrations
        self.aq_conc_level1 = 0.01
        self.aq_conc_level2 = 0.1
        self.aq_conc_level3 = 1.0
        self.aq_conc_level4 = 10.
        self.aq_conc_level5 = 100.

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
        self.intake_param_a1_birds_gen = 0.648  # these ..._gen parameter values are used in calculation of concentration based EECs (see OPP TED worksheet 'Min/Max rate concentrations' column L)
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
        self.initialize_eec_timeseries()

        # generate daily flag to identify application day numbers within year for min/max application scenarios
        self.app_flags_min_scenario = self.daily_app_flag(self.num_apps_min[sim_num], self.app_interval_min[sim_num])
        self.app_flags_max_scenario = self.daily_app_flag(self.num_apps_max[sim_num], self.app_interval_max[sim_num])

        # calculate upper bound and mean concentration based EECs for food items (daily values for a year) - min application scenario
        self.out_diet_eec_upper_min_sg = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_sg, self.app_flags_min_scenario)  # short grass
        self.out_diet_eec_upper_min_tg = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_tg, self.app_flags_min_scenario)  # tall grass
        self.out_diet_eec_upper_min_blp = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_blp, self.app_flags_min_scenario)  # broad-leafed plants
        self.out_diet_eec_upper_min_fp = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_fp, self.app_flags_min_scenario)  # seeds/fruits/pods
        self.out_diet_eec_upper_min_arthro  = self.daily_plant_timeseries(sim_num, self.app_rate_min[sim_num], self.food_multiplier_upper_arthro, self.app_flags_min_scenario)  # arthropods

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
        self.out_diet_eec_upper_min_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_min_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_eec_upper_min_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_min_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_eec_upper_min_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_min_arthro,
                                                                                 self.frac_retained_birds[sim_num])
        self.out_diet_eec_upper_min_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_min_arthro,
                                                                                  self.frac_retained_birds[sim_num])

        self.out_diet_eec_mean_min_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_min_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_eec_mean_min_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_min_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_eec_mean_min_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_min_arthro,
                                                                                self.frac_retained_birds[sim_num])
        self.out_diet_eec_mean_min_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_min_arthro,
                                                                                 self.frac_retained_birds[sim_num])

        self.out_diet_eec_upper_max_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_max_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_eec_upper_max_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_upper_max_sg,
                                                                                 self.frac_retained_mamm[sim_num])
        self.out_diet_eec_upper_max_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_max_arthro,
                                                                                 self.frac_retained_birds[sim_num])
        self.out_diet_eec_upper_max_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_upper_max_arthro,
                                                                                  self.frac_retained_birds[sim_num])

        self.out_diet_eec_mean_max_sm_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_sm_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_max_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_eec_mean_max_lg_mamm = self.daily_animal_dose_timeseries(self.intake_param_a1_mamm_rodent, self.intake_param_b1_mamm_rodent, self.mamm_lg_bodywgt, self.frac_h2o_aq_plant, self.out_diet_eec_mean_max_sg,
                                                                                self.frac_retained_mamm[sim_num])
        self.out_diet_eec_mean_max_sm_bird = self.daily_animal_dose_timeseries(self.intake_param_a1_birds_gen, self.intake_param_b1_birds_gen, self.bird_sm_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_max_arthro,
                                                                                self.frac_retained_birds[sim_num])
        self.out_diet_eec_mean_max_sm_amphi = self.daily_animal_dose_timeseries(self.intake_param_a1_rep_amphi, self.intake_param_b1_rep_amphi, self.rep_amphi_bodywgt, self.frac_h2o_arthro, self.out_diet_eec_mean_max_arthro,
                                                                                 self.frac_retained_birds[sim_num])

    def eec_exceedances(self, sim_num):
        """
        :description calculates the number of times a food item concentration (a time series of days for a year)
                     exceeds the various toxicity thresholds
        :param sim_num number of simulation
        :NOTE this represents OPP TED Excel model worksheet 'Min/Max rate - dietary conc results' columns D - N lines 3 - 54 and 58 - 109
              (the objective is to replicate the rows and columns of the worksheets)
        :return:
        """

        na_series = pd.Series(366*['NA']) # dummy daily time series containing 'NA' to be used when food item is not relevant to a speicies specific toxicity measure

        # collect concentration based toxicity data into a single series for each taxa
        self.tox_cbt_mamm = pd.Series([self.cbt_mamm_1inmill_mort[sim_num], self.cbt_mamm_1inten_mort[sim_num], self.cbt_mamm_low_lc50[sim_num], self.cbt_mamm_sub_direct[sim_num],
                          self.cbt_mamm_grow_noec[sim_num], self.cbt_mamm_grow_loec[sim_num], self.cbt_mamm_repro_noec[sim_num], self.cbt_mamm_repro_loec[sim_num], self.cbt_mamm_behav_noec[sim_num],
                          self.cbt_mamm_behav_loec[sim_num], self.cbt_mamm_sensory_noec[sim_num], self.cbt_mamm_sensory_loec[sim_num], self.cbt_mamm_sub_indirect[sim_num]])


        self.tox_cbt_bird = pd.Series([self.cbt_bird_1inmill_mort[sim_num],self.cbt_bird_1inten_mort[sim_num],self.cbt_bird_low_lc50[sim_num],self.cbt_bird_sub_direct[sim_num],
                            self.cbt_bird_grow_noec[sim_num],self.cbt_bird_grow_loec[sim_num],self.cbt_bird_repro_noec[sim_num],self.cbt_bird_repro_loec[sim_num],self.cbt_bird_behav_noec[sim_num],
                            self.cbt_bird_behav_loec[sim_num],self.cbt_bird_sensory_noec[sim_num],self.cbt_bird_sensory_loec[sim_num],self.cbt_bird_sub_indirect[sim_num]])

        self.tox_cbt_reptile = pd.Series([self.cbt_reptile_1inmill_mort[sim_num],self.cbt_reptile_1inten_mort[sim_num],self.cbt_reptile_low_lc50[sim_num],self.cbt_reptile_sub_direct[sim_num],
                               self.cbt_reptile_grow_noec[sim_num],self.cbt_reptile_grow_loec[sim_num],self.cbt_reptile_repro_noec[sim_num],self.cbt_reptile_repro_loec[sim_num],self.cbt_reptile_behav_noec[sim_num],
                               self.cbt_reptile_behav_loec[sim_num],self.cbt_reptile_sensory_noec[sim_num],self.cbt_reptile_sensory_loec[sim_num],self.cbt_reptile_sub_indirect[sim_num]])

        self.tox_cbt_inv  = pd.Series([self.cbt_inv_food_1inmill_mort[sim_num],self.cbt_inv_food_1inten_mort[sim_num],self.cbt_inv_food_low_lc50[sim_num],self.cbt_inv_food_sub_direct[sim_num],
                            self.cbt_inv_food_grow_noec[sim_num],self.cbt_inv_food_grow_loec[sim_num],self.cbt_inv_food_repro_noec[sim_num],self.cbt_inv_food_repro_loec[sim_num],self.cbt_inv_food_behav_noec[sim_num],
                            self.cbt_inv_food_behav_loec[sim_num],self.cbt_inv_food_sensory_noec[sim_num],self.cbt_inv_food_sensory_loec[sim_num],self.cbt_inv_food_sub_indirect[sim_num]])

        #         collect/aggregate timeseries of food item concentrations into a single series (upper bound/mean and min/max application scenario)
        #         notice that the time series have an _1 an _2 associated with them; the difference is associated with the list of food items
        #         that are relevant to the taxa; the _1 aggregates food item time series are relevant to mammals/birds/reptiles while the
        #         _2 aggregates time series relevant to terrestrial invertebrates  --
        #         for all non-relevant food items per taxa a dummy time series filled with 'NA' is used in the aggregation; this allows the
        #         OPP TED spreadsheet to be replicated

        # process minimum application scenario time series with upper bound & mean residue concentration multipliers for food items

        self.eec_ts_upper_min_1 = pd.Series([[self.out_diet_eec_upper_min_sg], [self.out_diet_eec_upper_min_tg], [self.out_diet_eec_upper_min_blp], \
                                  [self.out_diet_eec_upper_min_fp], [self.out_diet_eec_upper_min_arthro], [self.out_diet_eec_min_soil_inv],
                                  [self.out_diet_eec_upper_min_sm_mamm], [self.out_diet_eec_upper_min_lg_mamm], [self.out_diet_eec_upper_min_sm_bird],
                                  [self.out_diet_eec_upper_min_sm_amphi], [na_series]])

        self.eec_ts_upper_min_2 = pd.Series([[self.out_diet_eec_upper_min_sg], [self.out_diet_eec_upper_min_tg], [self.out_diet_eec_upper_min_blp], \
                                                [self.out_diet_eec_upper_min_fp], [self.out_diet_eec_upper_min_arthro], [self.out_diet_eec_min_soil_inv],
                                                [na_series], [na_series], [na_series], [na_series], [self.out_soil_conc_min]])

        self.eec_exc_upper_min_mamm = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_mamm)
        self.eec_exc_upper_min_bird = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_bird)
        self.eec_exc_upper_min_reptile = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_reptile)
        self.eec_exc_upper_min_inv = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_min_2, self.tox_cbt_inv)

        self.eec_ts_mean_min_1 = pd.Series([[self.out_diet_eec_mean_min_sg], [self.out_diet_eec_mean_min_tg], [self.out_diet_eec_mean_min_blp], \
                                  [self.out_diet_eec_mean_min_fp], [self.out_diet_eec_mean_min_arthro], [na_series],
                                  [self.out_diet_eec_mean_min_sm_mamm], [self.out_diet_eec_mean_min_lg_mamm], [self.out_diet_eec_mean_min_sm_bird],
                                  [self.out_diet_eec_mean_min_sm_amphi], [na_series]])

        self.eec_ts_mean_min_2 = pd.Series([[self.out_diet_eec_mean_min_sg], [self.out_diet_eec_mean_min_tg], [self.out_diet_eec_mean_min_blp], \
                                               [self.out_diet_eec_mean_min_fp], [self.out_diet_eec_mean_min_arthro], [na_series],
                                               [na_series], [na_series], [na_series], [na_series], [na_series]])  # soil concentration timeseries same as upper bound case

        self.eec_exc_mean_min_mamm = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_min_1, self.tox_cbt_mamm)
        self.eec_exc_mean_min_bird = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_min_1, self.tox_cbt_bird)
        self.eec_exc_mean_min_reptile = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_min_1, self.tox_cbt_reptile)
        self.eec_exc_mean_min_inv = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_min_2, self.tox_cbt_inv)

        # process maximum application scenario time series with upper bound & mean residue concentration multipliers for food items

        self.eec_ts_upper_max_1 = pd.Series([[self.out_diet_eec_upper_max_sg], [self.out_diet_eec_upper_max_tg], [self.out_diet_eec_upper_max_blp], \
                                  [self.out_diet_eec_upper_max_fp], [self.out_diet_eec_upper_max_arthro], [self.out_diet_eec_max_soil_inv],
                                  [self.out_diet_eec_upper_max_sm_mamm], [self.out_diet_eec_upper_max_lg_mamm], [self.out_diet_eec_upper_max_sm_bird],
                                  [self.out_diet_eec_upper_max_sm_amphi], [na_series]])

        self.eec_ts_upper_max_2 = pd.Series([[self.out_diet_eec_upper_max_sg], [self.out_diet_eec_upper_max_tg], [self.out_diet_eec_upper_max_blp],
                                                [self.out_diet_eec_upper_max_fp], [self.out_diet_eec_upper_max_arthro], [self.out_diet_eec_max_soil_inv],
                                                [na_series], [na_series], [na_series], [na_series], [self.out_soil_conc_max]])

        self.eec_exc_upper_max_mamm = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_mamm)
        self.eec_exc_upper_max_bird = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_bird)
        self.eec_exc_upper_max_reptile = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_reptile)
        self.eec_exc_upper_max_inv = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_upper_max_2, self.tox_cbt_inv)

        self.eec_ts_mean_max_1 = pd.Series([[self.out_diet_eec_mean_max_sg], [self.out_diet_eec_mean_max_tg], [self.out_diet_eec_mean_max_blp], \
                                  [self.out_diet_eec_mean_max_fp], [self.out_diet_eec_mean_max_arthro], [na_series],
                                  [self.out_diet_eec_mean_max_sm_mamm], [self.out_diet_eec_mean_max_lg_mamm], [self.out_diet_eec_mean_max_sm_bird],
                                  [self.out_diet_eec_mean_max_sm_amphi], [na_series]])

        self.eec_ts_mean_max_2 = pd.Series([[self.out_diet_eec_mean_max_sg], [self.out_diet_eec_mean_max_tg], [self.out_diet_eec_mean_max_blp], \
                                 [self.out_diet_eec_mean_max_fp], [self.out_diet_eec_mean_max_arthro], [na_series],
                                 [na_series], [na_series], [na_series], [na_series], [na_series]]) # soil concentration timeseries same as upper bound case

        self.eec_exc_mean_max_mamm = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_max_1, self.tox_cbt_mamm)
        self.eec_exc_mean_max_bird = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_max_1, self.tox_cbt_bird)
        self.eec_exc_mean_max_reptile = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_max_1, self.tox_cbt_reptile)
        self.eec_exc_mean_max_inv = self.sum_exceedances(self.num_ts, self.num_tox, self.eec_ts_mean_max_2, self.tox_cbt_inv)

    def eec_drift_distances(self, sim_num):
        """
        :description calculates the distance from the pesticide spray source area to where the maximum daily food item concentration
                     occurs (only computed for upper bound residue concentrations and min/max application scenarios)
        :param sim_num number of simulation
        :NOTE this represents OPP TED Excel model worksheet 'Min/Max rate - dietary conc results' columns D - N lines 113 - 164
              (the objective is to replicate the rows and columns of the worksheets)
        :return:
        """

        # we will reference 'self.tox_cbt_mamm', 'self.tox_cbt_bird', 'self.tox_cbt_reptile', & 'self.tox_cbt_inv' which
        # represent aggregations of the toxicity measures per taxa into panda series for processing (the series were constructed
        # in method 'eec_exceedances'

        na_series = pd.Series(366*['NA']) # dummy daily time series containing 'NA' to be used when food item is not relevant to a speicies specific toxicity measure

        #         collect/aggregate maximum concentrations from timeseries of food item concentrations into a single series (upper bound/mean and min/max application scenario)
        #         notice that the time series have an _1 an _2 associated with them; the difference is associated with the list of food items
        #         that are relevant to the taxa; the _1 aggregates food item time series are relevant to mammals/birds/reptiles while the
        #         _2 aggregates time series relevant to terrestrial invertebrates  --
        #         for all non-relevant food items per taxa a dummy time series filled with 'NA' is used in the aggregation; this allows the
        #         OPP TED spreadsheet to be replicated

        # process minimum application scenario time series with upper bound residue concentration multipliers for food items

        self.eec_ts_upper_min_1 = pd.Series([self.out_diet_eec_upper_min_sg.max(), self.out_diet_eec_upper_min_tg.max(), self.out_diet_eec_upper_min_blp.max(), \
                                  self.out_diet_eec_upper_min_fp.max(), self.out_diet_eec_upper_min_arthro.max(), self.out_diet_eec_min_soil_inv.max(),
                                  self.out_diet_eec_upper_min_sm_mamm.max(), self.out_diet_eec_upper_min_lg_mamm.max(), self.out_diet_eec_upper_min_sm_bird.max(),
                                  self.out_diet_eec_upper_min_sm_amphi.max(), na_series.max()])

        self.eec_ts_upper_min_2 = pd.Series([self.out_diet_eec_upper_min_sg.max(), self.out_diet_eec_upper_min_tg.max(), self.out_diet_eec_upper_min_blp.max(), \
                                                self.out_diet_eec_upper_min_fp.max(), self.out_diet_eec_upper_min_arthro.max(), self.out_diet_eec_min_soil_inv.max(),
                                                na_series.max(), na_series.max(), na_series.max(), na_series.max(), self.out_soil_conc_min.max()])

        self.eec_tox_frac_mamm_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_mamm)
        self.eec_tox_frac_bird_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_bird)
        self.eec_tox_frac_reptile_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_reptile)
        self.eec_tox_frac_inv_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_min_1, self.tox_cbt_inv)

        # calculate distances from source area related to max daily concentration
        self.eec_dist_upper_min_mamm = self.calc_maxeec_distance(self.eec_tox_frac_mamm_1, self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)
        self.eec_dist_upper_min_bird = self.calc_maxeec_distance(self.eec_tox_frac_bird_1, self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)
        self.eec_dist_upper_min_reptile = self.calc_maxeec_distance(self.eec_tox_frac_reptile_1, self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)
        self.eec_dist_upper_min_inv = self.calc_maxeec_distance(self.eec_tox_frac_inv_1, self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        # process maximum application scenario time series with upper bound residue concentration multipliers for food items
        self.eec_ts_upper_max_1 = pd.Series([self.out_diet_eec_upper_max_sg.max(), self.out_diet_eec_upper_max_tg.max(), self.out_diet_eec_upper_max_blp.max(), \
                                  self.out_diet_eec_upper_max_fp.max(), self.out_diet_eec_upper_max_arthro.max(), self.out_diet_eec_max_soil_inv.max(),
                                  self.out_diet_eec_upper_max_sm_mamm.max(), self.out_diet_eec_upper_max_lg_mamm.max(), self.out_diet_eec_upper_max_sm_bird.max(),
                                  self.out_diet_eec_upper_max_sm_amphi.max(), na_series.max()])

        self.eec_ts_upper_max_2 = pd.Series([self.out_diet_eec_upper_max_sg.max(), self.out_diet_eec_upper_max_tg.max(), self.out_diet_eec_upper_max_blp.max(), \
                                                self.out_diet_eec_upper_max_fp.max(), self.out_diet_eec_upper_max_arthro.max(), self.out_diet_eec_max_soil_inv.max(),
                                                na_series.max(), na_series.max(), na_series.max(), na_series.max(), self.out_soil_conc_max.max()])

        self.eec_tox_frac_mamm_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_mamm)
        self.eec_tox_frac_bird_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_bird)
        self.eec_tox_frac_reptile_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_reptile)
        self.eec_tox_frac_inv_1 = self.calc_eec_tox_frac(self.num_ts, self.num_tox, self.eec_ts_upper_max_1, self.tox_cbt_inv)

        # calculate distances from source area related to max daily concentration (not calculated for minimum application scenario)
        self.eec_dist_upper_max_mamm = self.calc_maxeec_distance(self.eec_tox_frac_mamm_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)
        self.eec_dist_upper_max_bird = self.calc_maxeec_distance(self.eec_tox_frac_bird_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)
        self.eec_dist_upper_max_reptile = self.calc_maxeec_distance(self.eec_tox_frac_reptile_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)
        self.eec_dist_upper_max_inv = self.calc_maxeec_distance(self.eec_tox_frac_inv_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

    def initialize_eec_timeseries(self):

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

        self.out_diet_eec_upper_min_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_min_sm_amphi = np.zeros(self.num_simulation_days)

        self.out_diet_eec_mean_min_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_min_sm_amphi = np.zeros(self.num_simulation_days)

        self.out_diet_eec_upper_max_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_eec_upper_max_sm_amphi = np.zeros(self.num_simulation_days)

        self.out_diet_eec_mean_max_sm_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_lg_mamm = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_sm_bird = np.zeros(self.num_simulation_days)
        self.out_diet_eec_mean_max_sm_amphi = np.zeros(self.num_simulation_days)

    def species_doses(self, sim_num):
        """
        :description executes collection of functions/methods associated with the 'min/max rate doses' worksheet in the OPP TED Excel model
            # calculate species/food item specific doses and health measure ratios
        :param sim_num model simulation number

        :return:
        """

        # read species properties from database
        self.ReadSpeciesProperties()

        # set value for volumetric fraction of droplet spectrum related to bird respiration limits
        self.max_respire_frac_minapp = self.set_max_respire_frac(self.app_method_min[sim_num], self.droplet_spec_min[sim_num])
        self.max_respire_frac_maxapp = self.set_max_respire_frac(self.app_method_max[sim_num], self.droplet_spec_max[sim_num])

        # calculate upper bound and mean concentrations in diet per species/diet item combination (for min/max application scenarios)
        self.calc_species_diet_concs_minapp(sim_num)
        self.calc_species_diet_concs_maxapp(sim_num)

        # calculate upper bound and mean dietary doses per species/dieatary item (for min/max application scenarios)
        self.calc_species_diet_dose_minapp(sim_num)
        self.calc_species_diet_dose_maxapp(sim_num)

        return

    def calc_species_diet_concs_minapp(self, sim_num):
        """
        :description calculates upper bound and mean concentrations of dietary items per species (for minimum application scenario)
        :param sim_num model simulation number

        NOTE: this method addresses columns I & J of worksheet 'Min rate doses' of OPP TED spreadsheet model
        :return:
        """

        # initialize panda series to contain upper bound and mean results
        self.out_diet_conc_upper_min = pd.Series(len(self.com_name) * ['NA'], dtype='object')
        self.out_diet_conc_mean_min = pd.Series(len(self.com_name) * ['NA'], dtype='object')

        # collect the maximum concentrations from time series of upper bound and mean diet concentrations unique to each diet/food item (to minimize determination of time series maximums (tsmax))
        upper_arthro_tsmax = self.out_diet_eec_upper_min_arthro.max()
        mean_arthro_tsmax = self.out_diet_eec_mean_min_arthro.max()
        upper_soil_inv_tsmax = self.out_diet_eec_min_soil_inv.max()
        upper_sm_amphi_tsmax = self.out_diet_eec_upper_min_sm_amphi.max()
        mean_sm_amphi_tsmax = self.out_diet_eec_mean_min_sm_amphi.max()
        upper_sm_mamm_tsmax = self.out_diet_eec_upper_min_sm_mamm.max()
        mean_sm_mamm_tsmax = self.out_diet_eec_mean_min_sm_mamm.max()
        upper_inverts_tsmax = self.water_conc_1[sim_num] * (self.inv_bcf_upper[sim_num] / 1000.)
        mean_inverts_tsmax = self.water_conc_1[sim_num] * (self.inv_bcf_mean[sim_num] / 1000.)
        upper_sm_bird_tsmax = self.out_diet_eec_upper_min_sm_bird.max()
        mean_sm_bird_tsmax = self.out_diet_eec_mean_min_sm_bird.max()
        upper_fish_tsmax = self.water_conc_1[sim_num] * (self.fish_bcf_upper[sim_num] / 1000.)
        mean_fish_tsmax = self.water_conc_1[sim_num] * (self.fish_bcf_mean[sim_num] / 1000.)
        upper_plant_algae_tsmax = self.water_conc_1[sim_num] * (self.aq_plant_algae_bcf_upper[sim_num] / 1000.)
        mean_plant_algae_tsmax = self.water_conc_1[sim_num] * (self.aq_plant_algae_bcf_mean[sim_num] / 1000.)
        upper_sg_tsmax = self.out_diet_eec_upper_min_sg.max()
        mean_sg_tsmax = self.out_diet_eec_mean_min_sg.max()
        upper_blp_tsmax = self.out_diet_eec_upper_min_blp.max()
        mean_blp_tsmax = self.out_diet_eec_mean_min_blp.max()
        upper_fp_tsmax = self.out_diet_eec_upper_min_fp.max()
        mean_fp_tsmax = self.out_diet_eec_mean_min_fp.max()
        upper_lg_mamm_tsmax = self.out_diet_eec_upper_min_lg_mamm.max()
        mean_lg_mamm_tsmax = self.out_diet_eec_mean_min_lg_mamm.max()
        upper_tg_tsmax = self.out_diet_eec_upper_min_tg.max()
        mean_tg_tsmax = self.out_diet_eec_mean_min_tg.max()

        for i in range(len(self.com_name)):
            if (self.diet_item[i] == 'arthropods'):
                self.out_diet_conc_upper_min[i] = upper_arthro_tsmax
                self.out_diet_conc_mean_min[i] = mean_arthro_tsmax
            elif (self.diet_item[i] == 'soil inverts'):
                self.out_diet_conc_upper_min[i] = upper_soil_inv_tsmax
                self.out_diet_conc_mean_min[i] = 'NA'
            elif (self.diet_item[i] == 'amphibians'):
                self.out_diet_conc_upper_min[i] = upper_sm_amphi_tsmax
                self.out_diet_conc_mean_min[i] = mean_sm_amphi_tsmax
            elif (self.diet_item[i] == 'mammals (small)'):
                self.out_diet_conc_upper_min[i] = upper_sm_mamm_tsmax
                self.out_diet_conc_mean_min[i] = mean_sm_mamm_tsmax
            elif (self.diet_item[i] == 'benthic inverts'):
                self.out_diet_conc_upper_min[i] = upper_inverts_tsmax
                self.out_diet_conc_mean_min[i] = mean_inverts_tsmax
            elif (self.diet_item[i] == 'birds'):
                self.out_diet_conc_upper_min[i] = upper_sm_bird_tsmax
                self.out_diet_conc_mean_min[i] = mean_sm_bird_tsmax
            elif (self.diet_item[i] == 'fish, aq amphibians'):
                self.out_diet_conc_upper_min[i] = upper_fish_tsmax
                self.out_diet_conc_mean_min[i] = mean_fish_tsmax
            elif (self.diet_item[i] == 'fish and aq amphibians'):
                self.out_diet_conc_upper_min[i] = upper_fish_tsmax
                self.out_diet_conc_mean_min[i] = mean_fish_tsmax
            elif (self.diet_item[i] == 'fish'):
                self.out_diet_conc_upper_min[i] = upper_fish_tsmax
                self.out_diet_conc_mean_min[i] = mean_fish_tsmax
            elif (self.diet_item[i] == 'filter feeders'):
                self.out_diet_conc_upper_min[i] = upper_inverts_tsmax
                self.out_diet_conc_mean_min[i] = mean_inverts_tsmax
            elif (self.diet_item[i] == 'reptiles'):
                self.out_diet_conc_upper_min[i] = upper_sm_amphi_tsmax
                self.out_diet_conc_mean_min[i] = mean_sm_amphi_tsmax
            elif (self.diet_item[i] == 'algae'):
                self.out_diet_conc_upper_min[i] = upper_plant_algae_tsmax
                self.out_diet_conc_mean_min[i] = mean_plant_algae_tsmax
            elif (self.diet_item[i] == 'grass'):
                self.out_diet_conc_upper_min[i] = upper_sg_tsmax
                self.out_diet_conc_mean_min[i] = mean_sg_tsmax
            elif (self.diet_item[i] == 'leaves'):
                self.out_diet_conc_upper_min[i] = upper_blp_tsmax
                self.out_diet_conc_mean_min[i] = mean_blp_tsmax
            elif (self.diet_item[i] == 'seeds'):
                self.out_diet_conc_upper_min[i] = upper_fp_tsmax
                self.out_diet_conc_mean_min[i] = mean_fp_tsmax
            elif (self.diet_item[i] == 'fruit'):
                self.out_diet_conc_upper_min[i] = upper_fp_tsmax
                self.out_diet_conc_mean_min[i] = mean_fp_tsmax
            elif (self.diet_item[i] == 'leaves, flowers'):
                self.out_diet_conc_upper_min[i] = upper_blp_tsmax
                self.out_diet_conc_mean_min[i] = mean_blp_tsmax
            elif (self.diet_item[i] == 'zooplankton'):
                self.out_diet_conc_upper_min[i] = upper_inverts_tsmax
                self.out_diet_conc_mean_min[i] = mean_inverts_tsmax
            elif (self.diet_item[i] == 'aquatic plants'):
                self.out_diet_conc_upper_min[i] = upper_plant_algae_tsmax
                self.out_diet_conc_mean_min[i] = mean_plant_algae_tsmax
            elif (self.diet_item[i] == 'carrion'):
                self.out_diet_conc_upper_min[i] = upper_lg_mamm_tsmax
                self.out_diet_conc_mean_min[i] = mean_lg_mamm_tsmax
            elif (self.diet_item[i] == 'nectar'):
                self.out_diet_conc_upper_min[i] = upper_tg_tsmax
                self.out_diet_conc_mean_min[i] = mean_tg_tsmax
            elif (self.diet_item[i] == 'leaves (surrogate for fungi)'):
                self.out_diet_conc_upper_min[i] = upper_blp_tsmax
                self.out_diet_conc_mean_min[i] = mean_blp_tsmax
            elif (self.diet_item[i] == 'mammals (large)'):
                self.out_diet_conc_upper_min[i] = upper_lg_mamm_tsmax
                self.out_diet_conc_mean_min[i] = mean_lg_mamm_tsmax
            elif (self.diet_item[i] == 'nectar, pollen'):
                self.out_diet_conc_upper_min[i] = upper_tg_tsmax
                self.out_diet_conc_mean_min[i] = mean_tg_tsmax
            elif (self.diet_item[i] == 'pollen'):
                self.out_diet_conc_upper_min[i] = upper_tg_tsmax
                self.out_diet_conc_mean_min[i] = mean_tg_tsmax
            elif (self.diet_item[i] == 'bark (twigs), pine  needles (grass as surrogate'):
                self.out_diet_conc_upper_min[i] = upper_sg_tsmax
                self.out_diet_conc_mean_min[i] = mean_sg_tsmax
            elif (self.diet_item[i] == 'aquatic plants, algae'):
                self.out_diet_conc_upper_min[i] = upper_plant_algae_tsmax
                self.out_diet_conc_mean_min[i] = mean_plant_algae_tsmax
        return

    def calc_species_diet_concs_maxapp(self, sim_num):
        """
        :description calculates upper bound and mean concentrations of dietary items per species (for mmaximum application scenario)
        :param sim_num model simulation number

        NOTE: this method addresses columns I & J of worksheet 'Max rate doses' of OPP TED spreadsheet model
        :return:
        """

        # initialize panda series to contain upper bound and mean results
        self.out_diet_conc_upper_max = pd.Series(len(self.com_name) * ['NA'], dtype='object')
        self.out_diet_conc_mean_max = pd.Series(len(self.com_name) * ['NA'], dtype='object')

        # collect the maximum concentrations from time series of upper bound and mean diet concentrations unique to each diet/food item (to minimize determination of time series maximums (tsmax))
        upper_arthro_tsmax = self.out_diet_eec_upper_max_arthro.max()
        mean_arthro_tsmax = self.out_diet_eec_mean_max_arthro.max()
        upper_soil_inv_tsmax = self.out_diet_eec_max_soil_inv.max()
        upper_sm_amphi_tsmax = self.out_diet_eec_upper_max_sm_amphi.max()
        mean_sm_amphi_tsmax = self.out_diet_eec_mean_max_sm_amphi.max()
        upper_sm_mamm_tsmax = self.out_diet_eec_upper_max_sm_mamm.max()
        mean_sm_mamm_tsmax = self.out_diet_eec_mean_max_sm_mamm.max()
        upper_inverts_tsmax = self.water_conc_1[sim_num] * (self.inv_bcf_upper[sim_num] / 1000.)
        mean_inverts_tsmax = self.water_conc_1[sim_num] * (self.inv_bcf_mean[sim_num] / 1000.)
        upper_sm_bird_tsmax = self.out_diet_eec_upper_max_sm_bird.max()
        mean_sm_bird_tsmax = self.out_diet_eec_mean_max_sm_bird.max()
        upper_fish_tsmax = self.water_conc_1[sim_num] * (self.fish_bcf_upper[sim_num] / 1000.)
        mean_fish_tsmax = self.water_conc_1[sim_num] * (self.fish_bcf_mean[sim_num] / 1000.)
        upper_plant_algae_tsmax = self.water_conc_1[sim_num] * (self.aq_plant_algae_bcf_upper[sim_num] / 1000.)
        mean_plant_algae_tsmax = self.water_conc_1[sim_num] * (self.aq_plant_algae_bcf_mean[sim_num] / 1000.)
        upper_sg_tsmax = self.out_diet_eec_upper_max_sg.max()
        mean_sg_tsmax = self.out_diet_eec_mean_max_sg.max()
        upper_blp_tsmax = self.out_diet_eec_upper_max_blp.max()
        mean_blp_tsmax = self.out_diet_eec_mean_max_blp.max()
        upper_fp_tsmax = self.out_diet_eec_upper_max_fp.max()
        mean_fp_tsmax = self.out_diet_eec_mean_max_fp.max()
        upper_lg_mamm_tsmax = self.out_diet_eec_upper_max_lg_mamm.max()
        mean_lg_mamm_tsmax = self.out_diet_eec_mean_max_lg_mamm.max()
        upper_tg_tsmax = self.out_diet_eec_upper_max_tg.max()
        mean_tg_tsmax = self.out_diet_eec_mean_max_tg.max()

        for i in range(len(self.com_name)):
            if (self.diet_item[i] == 'arthropods'):
                self.out_diet_conc_upper_max[i] = upper_arthro_tsmax
                self.out_diet_conc_mean_max[i] = mean_arthro_tsmax
            elif (self.diet_item[i] == 'soil inverts'):
                self.out_diet_conc_upper_max[i] = upper_soil_inv_tsmax
                self.out_diet_conc_mean_max[i] = 'NA'
            elif (self.diet_item[i] == 'amphibians'):
                self.out_diet_conc_upper_max[i] = upper_sm_amphi_tsmax
                self.out_diet_conc_mean_max[i] = mean_sm_amphi_tsmax
            elif (self.diet_item[i] == 'mammals (small)'):
                self.out_diet_conc_upper_max[i] = upper_sm_mamm_tsmax
                self.out_diet_conc_mean_max[i] = mean_sm_mamm_tsmax
            elif (self.diet_item[i] == 'benthic inverts'):
                self.out_diet_conc_upper_max[i] = upper_inverts_tsmax
                self.out_diet_conc_mean_max[i] = mean_inverts_tsmax
            elif (self.diet_item[i] == 'birds'):
                self.out_diet_conc_upper_max[i] = upper_sm_bird_tsmax
                self.out_diet_conc_mean_max[i] = mean_sm_bird_tsmax
            elif (self.diet_item[i] == 'fish, aq amphibians'):
                self.out_diet_conc_upper_max[i] = upper_fish_tsmax
                self.out_diet_conc_mean_max[i] = mean_fish_tsmax
            elif (self.diet_item[i] == 'fish and aq amphibians'):
                self.out_diet_conc_upper_min[i] = upper_fish_tsmax
                self.out_diet_conc_mean_min[i] = mean_fish_tsmax
            elif (self.diet_item[i] == 'fish'):
                self.out_diet_conc_upper_max[i] = upper_fish_tsmax
                self.out_diet_conc_mean_max[i] = mean_fish_tsmax
            elif (self.diet_item[i] == 'filter feeders'):
                self.out_diet_conc_upper_max[i] = upper_inverts_tsmax
                self.out_diet_conc_mean_max[i] = mean_inverts_tsmax
            elif (self.diet_item[i] == 'reptiles'):
                self.out_diet_conc_upper_max[i] = upper_sm_amphi_tsmax
                self.out_diet_conc_mean_max[i] = mean_sm_amphi_tsmax
            elif (self.diet_item[i] == 'algae'):
                self.out_diet_conc_upper_max[i] = upper_plant_algae_tsmax
                self.out_diet_conc_mean_max[i] = mean_plant_algae_tsmax
            elif (self.diet_item[i] == 'grass'):
                self.out_diet_conc_upper_max[i] = upper_sg_tsmax
                self.out_diet_conc_mean_max[i] = mean_sg_tsmax
            elif (self.diet_item[i] == 'leaves'):
                self.out_diet_conc_upper_max[i] = upper_blp_tsmax
                self.out_diet_conc_mean_max[i] = mean_blp_tsmax
            elif (self.diet_item[i] == 'seeds'):
                self.out_diet_conc_upper_max[i] = upper_fp_tsmax
                self.out_diet_conc_mean_max[i] = mean_fp_tsmax
            elif (self.diet_item[i] == 'fruit'):
                self.out_diet_conc_upper_max[i] = upper_fp_tsmax
                self.out_diet_conc_mean_max[i] = mean_fp_tsmax
            elif (self.diet_item[i] == 'leaves, flowers'):
                self.out_diet_conc_upper_max[i] = upper_blp_tsmax
                self.out_diet_conc_mean_max[i] = mean_blp_tsmax
            elif (self.diet_item[i] == 'zooplankton'):
                self.out_diet_conc_upper_max[i] = upper_inverts_tsmax
                self.out_diet_conc_mean_max[i] = mean_inverts_tsmax
            elif (self.diet_item[i] == 'aquatic plants'):
                self.out_diet_conc_upper_max[i] = upper_plant_algae_tsmax
                self.out_diet_conc_mean_max[i] = mean_plant_algae_tsmax
            elif (self.diet_item[i] == 'carrion'):
                self.out_diet_conc_upper_max[i] = upper_lg_mamm_tsmax
                self.out_diet_conc_mean_max[i] = mean_lg_mamm_tsmax
            elif (self.diet_item[i] == 'nectar'):
                self.out_diet_conc_upper_max[i] = upper_tg_tsmax
                self.out_diet_conc_mean_max[i] = mean_tg_tsmax
            elif (self.diet_item[i] == 'leaves (surrogate for fungi)'):
                self.out_diet_conc_upper_max[i] = upper_blp_tsmax
                self.out_diet_conc_mean_max[i] = mean_blp_tsmax
            elif (self.diet_item[i] == 'mammals (large)'):
                self.out_diet_conc_upper_max[i] = upper_lg_mamm_tsmax
                self.out_diet_conc_mean_max[i] = mean_lg_mamm_tsmax
            elif (self.diet_item[i] == 'nectar, pollen'):
                self.out_diet_conc_upper_max[i] = upper_tg_tsmax
                self.out_diet_conc_mean_max[i] = mean_tg_tsmax
            elif (self.diet_item[i] == 'pollen'):
                self.out_diet_conc_upper_max[i] = upper_tg_tsmax
                self.out_diet_conc_mean_max[i] = mean_tg_tsmax
            elif (self.diet_item[i] == 'bark (twigs), pine  needles (grass as surrogate'):
                self.out_diet_conc_upper_max[i] = upper_sg_tsmax
                self.out_diet_conc_mean_max[i] = mean_sg_tsmax
            elif (self.diet_item[i] == 'aquatic plants, algae'):
                self.out_diet_conc_upper_max[i] = upper_plant_algae_tsmax
                self.out_diet_conc_mean_max[i] = mean_plant_algae_tsmax
        return

    def calc_species_diet_dose_minapp(self, sim_num):
        """
        :description calculates upper bound and mean dose of dietary items per species (for minimum application scenario)
        :param sim_num model simulation number

        NOTE: this method addresses columns K & L of worksheet 'Min rate doses' of OPP TED spreadsheet model
        :return:
        """

        # initialize panda series to contain upper bound and mean results
        self.out_diet_dose_upper_min = pd.Series(len(self.com_name) * ['NA'], dtype='object')
        self.out_diet_dose_mean_min = pd.Series(len(self.com_name) * ['NA'], dtype='object')

        for i in range(len(self.com_name)):
            if (self.taxa[i] == 'Birds'):
                if (self.order[i] == 'Passeriformes'):
                    param_a = self.intake_param_a1_birds_pass
                    param_b = self.intake_param_b1_birds_pass
                else: # must be non-Passeriformes
                    param_a = self.intake_param_a1_birds_nonpass
                    param_b = self.intake_param_b1_birds_nonpass
            elif (self.taxa[i] == 'Amphibians' or self.taxa[i] == 'Reptiles'):
                param_a = self.intake_param_a1_rep_amphi
                param_b = self.intake_param_b1_rep_amphi
            elif (self.taxa[i] == 'Mammals'):
                if (self.order[i] == 'Rodentia'):
                    param_a = self.intake_param_a1_mamm_rodent
                    param_b = self.intake_param_b1_mamm_rodent
                else: # must be non-Rodentia
                    param_a = self.intake_param_a1_mamm_nonrodent
                    param_b = self.intake_param_b1_mamm_nonrodent

            # calculate intake and then dose
            intake_rate = self.animal_dietary_intake(param_a, param_b, self.body_wgt[i], self.h2o_cont[i])
            if (self.out_diet_conc_upper_min[i] == 'NA'):
                self.out_diet_dose_upper_min[i] = 'NA'
            else:
                self.out_diet_dose_upper_min[i] = self.animal_dietary_dose(self.body_wgt[i], intake_rate, self.out_diet_conc_upper_min[i])
            if (self.out_diet_conc_mean_min[i] == 'NA'):
                self.out_diet_dose_mean_min[i] = 'NA'
            else:
                self.out_diet_dose_mean_min[i] = self.animal_dietary_dose(self.body_wgt[i], intake_rate, self.out_diet_conc_mean_min[i])
        return
    
    def calc_species_diet_dose_maxapp(self, sim_num):
        """
        :description calculates upper bound and mean dose of dietary items per species (for maximum application scenario)
        :param sim_num model simulation number

        NOTE: this method addresses columns K & L of worksheet 'Max rate doses' of OPP TED spreadsheet model
        :return:
        """

        # initialize panda series to contain upper bound and mean results
        self.out_diet_dose_upper_max = pd.Series(len(self.com_name) * ['NA'], dtype='object')
        self.out_diet_dose_mean_max = pd.Series(len(self.com_name) * ['NA'], dtype='object')

        for i in range(len(self.com_name)):
            if (self.taxa[i] == 'Birds'):
                if (self.order[i] == 'Passeriformes'):
                    param_a = self.intake_param_a1_birds_pass
                    param_b = self.intake_param_b1_birds_pass
                else: # must be non-Passeriformes
                    param_a = self.intake_param_a1_birds_nonpass
                    param_b = self.intake_param_b1_birds_nonpass
            elif (self.taxa[i] == 'Amphibians' or self.taxa[i] == 'Reptiles'):
                param_a = self.intake_param_a1_rep_amphi
                param_b = self.intake_param_b1_rep_amphi
            elif (self.taxa[i] == 'Mammals'):
                if (self.order[i] == 'Rodentia'):
                    param_a = self.intake_param_a1_mamm_rodent
                    param_b = self.intake_param_b1_mamm_rodent
                else: # must be non-Rodentia
                    param_a = self.intake_param_a1_mamm_nonrodent
                    param_b = self.intake_param_b1_mamm_nonrodent

            # calculate intake and then dose
            intake_rate = self.animal_dietary_intake(param_a, param_b, self.body_wgt[i], self.h2o_cont[i])
            if (self.out_diet_conc_upper_max[i] == 'NA'):
                self.out_diet_dose_upper_max[i] = 'NA'
            else:
                self.out_diet_dose_upper_max[i] = self.animal_dietary_dose(self.body_wgt[i], intake_rate, self.out_diet_conc_upper_max[i])
            if (self.out_diet_conc_mean_max[i] == 'NA'):
                self.out_diet_dose_mean_max[i] = 'NA'
            else:
                self.out_diet_dose_mean_max[i] = self.animal_dietary_dose(self.body_wgt[i], intake_rate, self.out_diet_conc_mean_max[i])
        return