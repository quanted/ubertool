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
        self.minutes_per_hr = 60.

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
        self.app_rate_conv1 = 11.2  # conversion factor used to convert units of application rate (lbs a.i./acre) to metric units to derive concentration in units of (ug a.i./mL); assuming depth/height in units of centimeters
        self.app_rate_conv2 = 0.112 # conversion factor used to convert units of application rate (lbs a.i./acre) to metric units to derive concentration in units of (ug a.i./mL); assuming depth/height in units of meters
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

        # parameters used to calculate water intake rate for vertebrates (Table A 1-7.7 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
        self.h2ointake_param_a2_birds_pass = 1.18
        self.h2ointake_param_b2_birds_pass = 0.874
        self.h2ointake_param_c2_birds_pass = 1.0
        self.h2ointake_param_a2_birds_nonpass = 1.18
        self.h2ointake_param_b2_birds_nonpass = 0.874
        self.h2ointake_param_c2_birds_nonpass = 3.7
        self.h2ointake_param_a2_mamm = 0.326
        self.h2ointake_param_b2_mamm = 0.818
        self.h2ointake_param_c2_mamm = 1.0
        self.h2ointake_param_a2_rep_amphi = 0.065
        self.h2ointake_param_b2_rep_amphi = 0.726
        self.h2ointake_param_c2_rep_amphi = 1.0 # this number is in question; in OPP sreadsheet it is 3.7; in table A 1-7.7 it is 1.0

        # set constants for dermal dose calculations (from Table A 1-7.9 and Eq 16)
        self.foliar_residue_factor = 0.62
        self.foliar_contact_rate = 6.01
        self.derm_contact_hours = 8.0
        self.frac_animal_foliage_contact = 0.079
        self.derm_contact_factor = 0.1
        self.derm_absorp_factor = 1.0
        self.frac_body_exposed = 0.5

        # set species surface area parameters (from Eq 12)
        self.surface_area_birds_a3 = 10.0
        self.surface_area_birds_b3 = 0.667
        self.surface_area_mamm_a3 = 12.3
        self.surface_area_mamm_b3 = 0.65
        self.surface_area_amphi_frogs_toads_a3 = 1.131
        self.surface_area_amphi_frogs_toads_b3 = 0.579
        self.surface_area_amphi_sal_a3 = 8.42
        self.surface_area_amphi_sal_b3 = 0.694
        self.surface_area_reptile_turtle_a3 = 16.61
        self.surface_area_reptile_turtle_b3 = 0.61
        self.surface_area_reptile_snake_a3 = 25.05
        self.surface_area_reptile_snake_b3 = 0.63

        # set parameters used to calculate inhalation rate for vertebrates (Table A 1-7.12)
        self.inhal_rate_birds_a4 = 284.
        self.inhal_rate_birds_b4 = 0.77
        self.inhal_rate_mamm_a4 = 379.
        self.inhal_rate_mamm_b4 = 0.80
        self.inhal_rate_rep_amphi_a4 = 76.9
        self.inhal_rate_rep_amphi_b4 = 0.76

        self.app_frac_timestep_aerial = 0.025 # fraction of 1 hour time step (i.e., 90 seconds)
        self.app_frac_timestep_gnd_blast = 0.0083 # fraction of 1 hour time step (i.e., 30 seconds)
        self.spray_release_hgt_aerial = 3.3 # meters
        self.spray_release_hgt_gnd_blast = 1.0 # meters

        self.lab_to_field_factor = 3.0 # as included in Eq 19
        self.bird_to_mamm_pulmonary_diff_rate = 3.4 # as included in Eq 22

        self.inhal_dose_period = 24.0

        # generic animal bodyweights (for use in daily allometric dietary consumption rate calculations)
        self.mamm_sm_bodywgt = 15.   # gms
        self.mamm_lg_bodywgt = 1000. # gms
        self.bird_sm_bodywgt = 20.   # gms
        self.rep_amphi_bodywgt = 2.  # gms

    def spray_drift_params(self, sim_num):
        """
        :description sets spray drift parameters for calculations of distance from source area associated with pesticide concentrations
        :param sim_num number of simulation

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
        :param sim_num number of simulation

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
        # (represents calculations found in columns C & D rows 9 - 10 in OPP TED Excel spreadsheet 'Plants' worksheet)
        self.runoff_eec_dry_area_min, self.runoff_eec_semiaq_area_min = self.calc_runoff_based_eec(self.app_rate_min[sim_num], self.pest_incorp_min, self.runoff_frac_min)
        self.runoff_eec_dry_area_max, self.runoff_eec_semiaq_area_max = self.calc_runoff_based_eec(self.app_rate_max[sim_num], self.pest_incorp_max, self.runoff_frac_max)

        # determine if plant EEC due to runoff exceeds various thresholds for pre-emergence of monocots and dicots
        # (represents determinations found in columns C & D rows 14 - 28 in OPP TED Excel spreadsheet 'Plants' worksheet)
        self.plant_risk_conclusions(sim_num)

        # calculate plant risk threshold distances
        # (represents columns C & D rows 32 to 51 in OPP TED Excel spreadsheet 'Plants' worksheet)
        self.plant_risk_threshold_distances(sim_num)

    def conc_based_eec_timeseries(self, sim_num):
        """
        :description executes collection of functions/methods associated with the 'min/max rate concentrations' worksheet in the OPP TED Excel model
            # calculate upper bound and mean concentration based EECs for food items (daily values for a year) - min application scenario
        :param sim_num number of simulation

        :return:
        """
        # set/reset arrays for holding single simulation results
        self.initialize_simlation_panda_series()

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

        self.out_conc_dew_min = self.daily_plant_dew_timeseries(sim_num, self.out_diet_eec_upper_min_blp)
        self.out_conc_dew_max = self.daily_plant_dew_timeseries(sim_num, self.out_diet_eec_upper_max_blp)

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

        # calculate distances from source area related to max daily concentration (minimum application scenario)
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

        # calculate distances from source area related to max daily concentration (maximum application scenario)
        self.eec_dist_upper_max_mamm = self.calc_maxeec_distance(self.eec_tox_frac_mamm_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)
        self.eec_dist_upper_max_bird = self.calc_maxeec_distance(self.eec_tox_frac_bird_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)
        self.eec_dist_upper_max_reptile = self.calc_maxeec_distance(self.eec_tox_frac_reptile_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)
        self.eec_dist_upper_max_inv = self.calc_maxeec_distance(self.eec_tox_frac_inv_1, self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

    def species_doses(self, sim_num):
        """
        :description executes collection of functions/methods associated with the 'min/max rate doses' worksheet in the OPP TED Excel model
            # calculate species/food item specific doses and health measure ratios
        :param sim_num model simulation number

        :return:
        """

        # calculate upper bound and mean concentrations in diet per species/diet item combination (for min/max application scenarios)
        # (represents columns I & J of worksheet 'Min/Max rate doses' of OPP TED spreadsheet model)
        self.calc_species_diet_concs_minapp(sim_num)
        self.calc_species_diet_concs_maxapp(sim_num)

        # calculate upper bound and mean dietary doses per species/dieatary item (for min/max application scenarios)
        # (represents columns K & L of worksheet 'Min/Max rate doses' of OPP TED spreadsheet model)
        self.calc_species_diet_dose_minapp(sim_num)
        self.calc_species_diet_dose_maxapp(sim_num)

        # calculate water doses from puddle and dew water consumption
        # represents columns M & N of worksheet 'Min/Max rate doses' of OPP TED spreadsheet model)
        self.calc_h2o_doses_minapp(sim_num)
        self.calc_h2o_doses_maxapp(sim_num)

        # calculate dermal to oral toxicity equivalency factors
        # (this method implements Eqs 14 and 15 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment')
        self.calc_derm_route_equiv_factor(sim_num)

        # calculate dermal contact doses (upper bound and mean for minimum/maximum application scenarios)
        # (method addresses columns O & P of worksheet 'Min/Max rate doses' of OPP TED spreadsheet model)
        self.calc_species_derm_contact_dose_minapp(sim_num)
        self.calc_species_derm_contact_dose_maxapp(sim_num)

        # calculate dermal spray doses (for minimum/maximum application scenarios)
        # (represents column Q of worksheet 'Min rate doses' of OPP TED spreadsheet model)
        self.calc_species_derm_spray_dose_minmaxapp(sim_num)

        # calculate air concentration immediately after application (for use in calculating inhalation vapor/spray doses)
        self.calc_air_conc_drops_minmaxapp(sim_num)

        # set value for volumetric fraction of droplet spectrum related to bird respiration limits (for use in calculating inhalation vapor/spray doses)
        self.max_respire_frac_minapp = self.set_max_respire_frac(self.app_method_min[sim_num], self.droplet_spec_min[sim_num])
        self.max_respire_frac_maxapp = self.set_max_respire_frac(self.app_method_max[sim_num], self.droplet_spec_max[sim_num])

        # calculate inhalation to oral toxicity equivalency factors (for use in calculating inhalation vapor/spray doses)
        self.calc_inhal_route_equiv_factor(sim_num)

        # calculate inhalation vapor/spray doses
        self.calc_species_inhal_dose_vapor()
        self.calc_species_inhal_dose_spray(sim_num)

        # scan species specific doses (from diet based to inhalation) and determine maximum
        self.determine_max_dose_minmaxapp()

        # calculate Mortality threshold
        self.calc_species_mortality_thres(sim_num)

        # calculate sublethal threshold
        self.calc_species_sublethal_thres(sim_num)

        # calculate lowest LD50 threshold
        self.calc_species_lowld50_thres(sim_num)

        # calculate HC50 threshold
        self.calc_species_hc50_thres(sim_num)

        # calculate distances from source area to where toxicity thresholds occur
        self.calc_distance_to_risk_thres(sim_num)

        # calculate ratio of maximum dose to toxicity thresholds: mortality and sublethal
        self.calc_maxdose_toxthres_ratios(sim_num)

        return
