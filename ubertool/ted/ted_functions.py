from __future__ import division  # brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
from numpy import math
import pandas as pd


class TedFunctions(object):
    """
    Function class for TED model.
    """

    def __init__(self):
        """Class representing the functions for Trex"""
        super(TedFunctions, self).__init__()

    def daily_app_flag(self, num_apps, app_interval):
        """
        :description generates a daily flag to denote whether a pesticide is applied that day or not (1 - applied, 0 - anot applied)
        :param num_apps; number of applications
        :param app_interval; number of days between applications

        :NOTE in TED model there are two application scenarios per simulation (one for a min/max exposure scenario)
              (this is why the parameters are passed in)
        :return:
        """

        daily_flag = np.full(self.num_simulation_days, False, dtype=bool)  # set daily flag to default of 0

        # set daily_flag to 1 for all application days
        for i in range(num_apps):  # assume at least 1 application and it is on day 0
            # calculate day index of each application and update the daily application array flag
            if (i == 0):
                daily_flag[0] = 1
            index = i * app_interval
            daily_flag[index] = 1
        return daily_flag

    def conc_initial_plant(self, application_rate, food_multiplier): # similar but different from method used in TREX
        """
        :description calculates initial (1st application day) dietary based EEC (residue concentration) from pesticide application
                    (mg/kg-diet for food items including short/tall grass, broadleaf plants, seeds/fruit/pods, and above ground arthropods)
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs

        :return:
        """
        return application_rate * food_multiplier

    def conc_initial_soil_h2o(self, i, application_rate, water_type):
        """
        :description calculates initial (1st application day) concentration in soil pore water or surface puddles(ug/L)
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param soil_depth
        :param soil_bulk_density; kg/L
        :param porosity; soil porosity
        :param frac_org_cont_soil; fraction organic carbon in soil
        :param app_rate_conv;  conversion factor used to convert units of application rate (lbs a.i./acre) to (ug a.i./mL)

        :NOTE this represents Eq 3 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
              (the depth of water in this equation is assumed to be 0.0 and therefore not included here)

        :return:
        """

        if(water_type=="puddles"):
            return (application_rate*self.app_rate_conv) / (self.h2o_depth_puddles + (self.soil_depth*(self.soil_porosity + (self.soil_bulk_density*self.koc[i]*self.soil_foc))))
        elif(water_type=="pore_water"):
            return (application_rate*self.app_rate_conv) / (self.h2o_depth_soil + (self.soil_depth*(self.soil_porosity + (self.soil_bulk_density*self.koc[i]*self.soil_foc))))

        return

    def conc_initial_canopy_air(self, i, application_rate):
        """
        :description calculates initial (1st application day) air concentration of pesticide within plant canopy (ug/mL)
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param mass_pest; mass of pesticide on treated field (mg)
        :param volume_air; volume of air in 1 hectare to a height equal to the height of the crop canopy
        :param biotransfer_factor; the volume_based biotransfer factor; function of Henry's las constant and Log Kow

        NOTE: this represents Eq 24 (and supporting eqs 25,26,27) of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        mass_pest = application_rate * self.lbs_to_gms * self.hectare_to_acre * self.gms_to_mg  #converting lbs/acre to mg Eq 25
        volume_air = self.crop_hgt * self.hectare_area * self.m3_to_liters   #crop_hgt(m), hectare_area(m2), 1000 (L/m3) #Eq 26
        log_biotransfer_factor = 1.065 * self.log_kow[i] - self.log_unitless_hlc[i] - 1.654  #Eq 27

        conc_air = mass_pest / (volume_air + (self.mass_plant * 10.**(log_biotransfer_factor) / self.density_plant))

        return conc_air

    def conc_timestep(self, conc_ini, half_life):  # similar but different from method used in TREX
        """
        :description calculates pesiticide concentration on plant surfaces and soils for timestep (day) due to pesticide dissipation/degradation
                     (mg/kg-diet for food items)
        :param conc_ini; initial concentration for day (actually previous day concentration)
        :param half_life; halflife of pesiticde representing either foliar dissipation halflife or aerobic soil metabolism halflife (days)
        :return:
        """
        # calculate concentration resulting from degradation for a daily timestep
        return conc_ini * np.exp(-(np.log(2) / half_life))

    def daily_plant_timeseries(self, i, application_rate, food_multiplier, daily_flag): # similar but different from 'eec_diet_timeseries' method used in TREX
        """
        :description generates annual timeseries of daily pesticide residue concentration (EECs) for a food item
        :param i; simulation number/index
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs
        :param daily_flag; daily flag denoting if pesticide is applied (0 - not applied, 1 - applied)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        conc = np.zeros(self.num_simulation_days)

        for day_index in range(self.num_simulation_days):
            if(day_index==0):
                conc[day_index] = self.conc_initial_plant(application_rate, food_multiplier)
            else:
                conc[day_index] = self.conc_timestep(conc[day_index-1], self.foliar_diss_hlife[i])
                if(daily_flag[day_index]==1): conc[day_index] = conc[day_index] + conc[0]
        return conc

    def daily_soil_h2o_timeseries(self, i, application_rate, daily_flag, water_type):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil pore water and surface puddles
        :param i; simulation number/index
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs
        :param daily_flag; daily flag denoting if pesticide is applied (0 - not applied, 1 - applied)
        :param water_type; type of water (pore water or surface puddles)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        conc = np.zeros(self.num_simulation_days)

        for day_index in range(self.num_simulation_days):
            if(day_index==0):
                conc[day_index] = self.conc_initial_soil_h2o(i, application_rate, water_type)
            else:
                conc[day_index] = self.conc_timestep(conc[day_index-1], self.aerobic_soil_meta_hlife[i])
                if(daily_flag[day_index]==1): conc[day_index] = conc[day_index] + conc[0]
        return conc

    def daily_plant_dew_timeseries(self, i, blp_conc):
        """
        :description generates annual timeseries of daily pesticide concentrations in dew that resides on broad leaf plants
        :param i; simulation number/index
        :param blp_conc; daily values of pesticide concentration in broad leaf plant dew

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               #this represents Eq 11 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'
        :return:
        """

        conc = np.zeros(self.num_simulation_days)

        for day_index in range(self.num_simulation_days):
            conc[day_index] = (blp_conc[day_index] * self.frac_pest_on_surface * self.density_h2o) / (self.mass_wax * (10.**(self.log_kow[i])))
            if (conc[day_index] > self.solubility[i]): conc[day_index] = self.solubility[i]
        return conc

    def daily_soil_timeseries(self, i, pore_h2o_conc):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil
        :param i; simulation number/index
        :param pore_h2o_conc; daily values of pesticide concentration in soil pore water

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        conc = np.zeros(self.num_simulation_days)

        for day_index in range(self.num_simulation_days):
            conc[day_index] = pore_h2o_conc[day_index] * self.soil_foc * self.koc[i]
        return conc

    def daily_soil_inv_timeseries(self, i, pore_h2o_conc):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil invertebrates (earthworms)
        :param i; simulation number/index
        :param pore_h2o_conc; daily values of pesticide concentration in soil pore water

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               # this represents Eq 2 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        conc = np.zeros(self.num_simulation_days)

        for day_index in range(self.num_simulation_days):
            conc[day_index] = (pore_h2o_conc[day_index] * (10.** self.log_kow[i]) * self.lipid_earthworm) / self.density_earthworm
        return conc

    def daily_animal_dose_timeseries(self, a1, b1, body_wgt, frac_h2o, intake_food_conc, frac_retained):
        """
        :description generates annual timeseries of daily pesticide concentrations in animals (mammals, birds, amphibians, reptiles)
        :param a1; coefficient of allometric expression
        :param b1; exponent of allometrice expression
        :param body_wgt; body weight of species (g)
        :param frac_h2o; fraction of water in food item
        :param intake_food_conc; pesticide concentration in food item (daily mg a.i./kg)
        :param frac_retained; fraction of ingested food retained by animal (mammals, birds, reptiles/amphibians)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application

               # this represents Eqs 5&6 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """
        dose = np.zeros(self.num_simulation_days)

        # calculate daily consumption rate
        food_intake_rate = self.animal_dietary_intake(a1, b1, body_wgt, frac_h2o)  # (g/day-ww) Eq 6

        # calculate daily doses for the year
        for day_index in range(self.num_simulation_days):
            dose[day_index] = self.animal_dietary_dose(body_wgt, food_intake_rate, intake_food_conc[day_index])  #Eq 5
            if(day_index != 0):
                dose[day_index] = dose[day_index] + (dose[day_index-1] * frac_retained)  # 2nd part of this is the carry over from previous day
        return dose

    def animal_dietary_intake(self, a1, b1, body_wgt, frac_h2o):
        """
        :description generates pesticide intake via consumption of diet containing pesticide for animals (mammals, birds, amphibians, reptiles)
        :param a1; coefficient of allometric expression
        :param b1; exponent of allometric expression
        :param body_wgt; body weight of species (g)
        :param frac_h2o; fraction of water in food item

               # this represents Eqs 6 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # calculate daily dietary consumption rate # (g/day-ww)
        food_intake_rate = (a1 * body_wgt**b1) / (1. - frac_h2o)

        return food_intake_rate

    def animal_dietary_dose(self, body_wgt, food_intake_rate, food_pest_conc):
        """
        :description generates pesticide dietary-based dose for animals (mammals, birds, amphibians, reptiles)
        :param body_wgt; body weight of species (g)
        :param frac_h2o; fraction of water in food item
        :param food_intake_rate; ingestion rate of food item (g/day-ww)
        :param food_pest_conc; pesticide concentration in food item (mg a.i./kg)

               # this represents Eqs 5 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """

        # calculate dietary dose #Eq 5
        dose = (food_intake_rate * food_pest_conc) / body_wgt

        return dose

    def daily_canopy_air_timeseries(self, i, application_rate, daily_flag):
        """
        :description generates annual timeseries of daily pesticide concentrations in soil pore water and surface puddles
        :param i; simulation number/index
        :param application rate; active ingredient application rate (lbs a.i./acre)
        :param food_multiplier; factor by which application rate of active ingredient is multiplied to estimate dietary based EECs
        :param daily_flag; daily flag denoting if pesticide is applied (0 - not applied, 1 - applied)
        :param water_type; type of water (pore water or surface puddles)

        :Notes # calculations are performed daily from day of first application (assumed day 0) through the last day of a year
               # note: day numbers are synchronized with 0-based array indexing; thus the year does not have a calendar specific
               # assoication, rather it is one year from the day of 1st pesticide application
        :return:
        """

        conc = np.zeros(self.num_simulation_days)

        for day_index in range(self.num_simulation_days):
            if(day_index==0):
                conc[day_index] = self.conc_initial_canopy_air(i, application_rate)
            else:
                conc[day_index] = self.conc_timestep(conc[day_index-1], self.foliar_diss_hlife[i])
                if(daily_flag[day_index]==1): conc[day_index] = conc[day_index] + conc[0]
        return conc

    def drift_distance_calc(self, app_rate_frac, param_a, param_b, param_c, max_distance):
        """
        :description calculates distance from edge of application source area to where the fraction of the application rate
                     results in a concentration that would result in the health threshold (which is in terms of a dose resulting
                     from exposure to the concentration) ; TED calculates the fraction by dividing the health threshold of interest
                     by the maximum dose from among all dietary items and ingestion/inhalation/contact of/with water/air/soil
        :param app_rate_frac; fraction of active ingredient application rate equivalent to the health threshold of concern
        :param param_a; parameter a for spray drift distance calculation
        :param param_b; parameter b for spray drift distance calculation
        :param param_c; parameter c for spray drift distance calculation
        :param max_distance; maximum distance from source area for which drift calculations are executed (feet)

        # this represents Eq 1 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """
        distance = (((param_c / app_rate_frac) ** (1. / param_b)) - 1.) / param_a

        # reset distance if outside bounds
        if (distance < 0.0): distance = 0.0
        if (distance > max_distance): distance = max_distance

        return distance
    
    def calc_plant_tox_ratios(self):
        """
        :description calculates ratio of plant toxicity measures to application rate (min or max)
                     (this method is executed outside of simulation loop because it can be executed in vector mode)
        :NOTE         represents columns G & H of OPP TED Excel spreadsheet 'inputs' worksheet rows 205 - 224
                      (this method is 'vectorized', that is calculations are performed here for all simulations)

        :return:
        """

        # plant toxicity (pt) : monocots ; minimum application rate
        self.pt_mono_pre_noec_appratio_min = self.pt_mono_pre_noec / self.app_rate_min
        self.pt_mono_pre_loec_appratio_min = self.pt_mono_pre_loec / self.app_rate_min
        self.pt_mono_pre_ec25_appratio_min = self.pt_mono_pre_ec25 / self.app_rate_min
        self.pt_mono_post_noec_appratio_min = self.pt_mono_post_noec / self.app_rate_min
        self.pt_mono_post_loec_appratio_min = self.pt_mono_post_loec / self.app_rate_min
        self.pt_mono_post_ec25_appratio_min = self.pt_mono_post_ec25 / self.app_rate_min
        self.pt_mono_dir_mort_appratio_min = self.pt_mono_dir_mort / self.app_rate_min
        self.pt_mono_indir_mort_appratio_min = self.pt_mono_indir_mort / self.app_rate_min
        self.pt_mono_dir_repro_appratio_min = self.pt_mono_dir_repro / self.app_rate_min
        self.pt_mono_indir_repro_appratio_min = self.pt_mono_indir_repro / self.app_rate_min

        # plant toxicity (pt) : dicots ; minimum application rate
        self.pt_dicot_pre_noec_appratio_min = self.pt_dicot_pre_noec / self.app_rate_min
        self.pt_dicot_pre_loec_appratio_min = self.pt_dicot_pre_loec / self.app_rate_min
        self.pt_dicot_pre_ec25_appratio_min = self.pt_dicot_pre_ec25 / self.app_rate_min
        self.pt_dicot_post_noec_appratio_min = self.pt_dicot_post_noec / self.app_rate_min
        self.pt_dicot_post_loec_appratio_min = self.pt_dicot_post_loec / self.app_rate_min
        self.pt_dicot_post_ec25_appratio_min = self.pt_dicot_post_ec25 / self.app_rate_min
        self.pt_dicot_dir_mort_appratio_min = self.pt_dicot_dir_mort / self.app_rate_min
        self.pt_dicot_indir_mort_appratio_min = self.pt_dicot_indir_mort / self.app_rate_min
        self.pt_dicot_dir_repro_appratio_min = self.pt_dicot_dir_repro / self.app_rate_min
        self.pt_dicot_indir_repro_appratio_min = self.pt_dicot_indir_repro / self.app_rate_min
        
        # plant toxicity (pt) : monocots ; maximum application rate
        self.pt_mono_pre_noec_appratio_max = self.pt_mono_pre_noec / self.app_rate_max
        self.pt_mono_pre_loec_appratio_max = self.pt_mono_pre_loec / self.app_rate_max
        self.pt_mono_pre_ec25_appratio_max = self.pt_mono_pre_ec25 / self.app_rate_max
        self.pt_mono_post_noec_appratio_max = self.pt_mono_post_noec / self.app_rate_max
        self.pt_mono_post_loec_appratio_max = self.pt_mono_post_loec / self.app_rate_max
        self.pt_mono_post_ec25_appratio_max = self.pt_mono_post_ec25 / self.app_rate_max
        self.pt_mono_dir_mort_appratio_max = self.pt_mono_dir_mort / self.app_rate_max
        self.pt_mono_indir_mort_appratio_max = self.pt_mono_indir_mort / self.app_rate_max
        self.pt_mono_dir_repro_appratio_max = self.pt_mono_dir_repro / self.app_rate_max
        self.pt_mono_indir_repro_appratio_max = self.pt_mono_indir_repro / self.app_rate_max

        # plant toxicity (pt) : dicots ; maximum application rate
        self.pt_dicot_pre_noec_appratio_max = self.pt_dicot_pre_noec / self.app_rate_max
        self.pt_dicot_pre_loec_appratio_max = self.pt_dicot_pre_loec / self.app_rate_max
        self.pt_dicot_pre_ec25_appratio_max = self.pt_dicot_pre_ec25 / self.app_rate_max
        self.pt_dicot_post_noec_appratio_max = self.pt_dicot_post_noec / self.app_rate_max
        self.pt_dicot_post_loec_appratio_max = self.pt_dicot_post_loec / self.app_rate_max
        self.pt_dicot_post_ec25_appratio_max = self.pt_dicot_post_ec25 / self.app_rate_max
        self.pt_dicot_dir_mort_appratio_max = self.pt_dicot_dir_mort / self.app_rate_max
        self.pt_dicot_indir_mort_appratio_max = self.pt_dicot_indir_mort / self.app_rate_max
        self.pt_dicot_dir_repro_appratio_max = self.pt_dicot_dir_repro / self.app_rate_max
        self.pt_dicot_indir_repro_appratio_max = self.pt_dicot_indir_repro / self.app_rate_max

    def plant_risk_threshold_distances(self, i):
        """
        :description processes all the plant risk measures to determine the distance from the source area that plant toxicity thresholds occur
        :param i simulation number
        :NOTE         represents columns C & D rows 32 to 51 in OPP TED Excel spreadsheet 'Plants' worksheet
                      (only calculated if health risk value is present;
                      if ratio of health risk value to applicatoin rate is greater than 1.0 then distance is set to 0.0 (i.e. at source area edge)
                      if distance is greater than max spray drift distance then distance is set to max spray drift distance

                      values for risk distances are not stored across simulations

        :return:
        """

        # plant toxicity (pt) : monocots ; minimum application rate; threshold distance
        self.pt_mono_pre_noec_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_pre_noec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_pre_loec_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_pre_loec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_pre_ec25_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_pre_ec25_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_post_noec_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_post_noec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_post_loec_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_post_loec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_post_ec25_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_post_ec25_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_dir_mort_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_dir_mort_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_indir_mort_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_indir_mort_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_dir_repro_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_dir_repro_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_mono_indir_repro_thres_dist_min = self.calc_plant_risk_distance(self.pt_mono_indir_repro_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        # plant toxicity (pt) : dicots ; minimum application rate; threshold distance
        self.pt_dicot_pre_noec_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_pre_noec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_pre_loec_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_pre_loec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_pre_ec25_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_pre_ec25_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_post_noec_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_post_noec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_post_loec_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_post_loec_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_post_ec25_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_post_ec25_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_dir_mort_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_dir_mort_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_indir_mort_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_indir_mort_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_dir_repro_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_dir_repro_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        self.pt_dicot_indir_repro_thres_dist_min = self.calc_plant_risk_distance(self.pt_dicot_indir_repro_appratio_min[i],
                                        self.drift_param_a_min, self.drift_param_b_min, self.drift_param_c_min, self.max_drift_distance_minapp)

        # plant toxicity (pt) : monocots ; maximum application rate; threshold distance
        self.pt_mono_pre_noec_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_pre_noec_appratio_max[i],
                                               self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_pre_loec_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_pre_loec_appratio_max[i],
                                               self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_pre_ec25_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_pre_ec25_appratio_max[i],
                                               self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_post_noec_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_post_noec_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_post_loec_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_post_loec_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_post_ec25_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_post_ec25_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_dir_mort_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_dir_mort_appratio_max[i],
                                               self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_indir_mort_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_indir_mort_appratio_max[i],
                                                 self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_dir_repro_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_dir_repro_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_mono_indir_repro_thres_dist_max = self.calc_plant_risk_distance(self.pt_mono_indir_repro_appratio_max[i],
                                                  self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        # plant toxicity (pt) : dicots ; maximum application rate; threshold distance
        self.pt_dicot_pre_noec_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_pre_noec_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_pre_loec_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_pre_loec_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_pre_ec25_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_pre_ec25_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_post_noec_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_post_noec_appratio_max[i],
                                                 self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_post_loec_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_post_loec_appratio_max[i],
                                                 self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_post_ec25_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_post_ec25_appratio_max[i],
                                                 self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_dir_mort_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_dir_mort_appratio_max[i],
                                                self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_indir_mort_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_indir_mort_appratio_max[i],
                                                  self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_dir_repro_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_dir_repro_appratio_max[i],
                                                 self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        self.pt_dicot_indir_repro_thres_dist_max = self.calc_plant_risk_distance(self.pt_dicot_indir_repro_appratio_max[i],
                                                   self.drift_param_a_max, self.drift_param_b_max, self.drift_param_c_max, self.max_drift_distance_maxapp)

        return

    def calc_plant_risk_distance(self, health_to_apprate_ratio, param_a, param_b, param_c, max_drift_distance):
        """
        :description calculates the distance from the source area that plant toxicity thresholds occur
        :param health_to_app_ratio;
        :param plant_thres_dist;
        :param param_a; spray drift parameter a
        :param param_b; spray drift parameter b
        :param param_c; spray drift parameter c
        :param max_drift_distance;
        :NOTE         represents columns C & D rows 32 to 51 in OPP TED Excel spreadsheet 'Plants' worksheet
                      (only calculated if health risk value is present;
                      if ratio of health risk value to applicatoin rate is greater than 1.0 then distance is set to 0.0 (i.e. at source area edge)
                      if distance is greater than max spray drift distance then distance is set to max spray drift distance

                      values for risk distances are not stored across simulations

        :return:
        """

        if (math.isnan(health_to_apprate_ratio)):
            threshold_dist = np.nan
        elif (health_to_apprate_ratio > 1.0):
            threshold_dist = 0.0
        else:
            threshold_dist = self.drift_distance_calc(health_to_apprate_ratio, param_a, param_b, param_c, max_drift_distance)
        return threshold_dist

    def calc_aquatic_vert_conc_thresholds(self):
        """
        :description calculates threshold dietary concentrations in water (ug/l) for aquatic dependent vertebrate species
        :NOTE         represents columns D, E & F of worksheet 'Aquatic dependent sp thresholds' of OPP TED Excel spreadsheet model
                      (this method is 'vectorized', that is calculations are performed here for all simulations)
        :return:
        """

        # mammals
        self.aq_conc_thres_1inmill_mamm_algae = self.cbt_mamm_1inmill_mort * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_1inmill_mamm_invert = self.cbt_mamm_1inmill_mort * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_1inmill_mamm_fish = self.cbt_mamm_1inmill_mort * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_1inten_mamm_algae = self.cbt_mamm_1inten_mort * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_1inten_mamm_invert = self.cbt_mamm_1inten_mort * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_1inten_mamm_fish = self.cbt_mamm_1inten_mort * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_low_lc50_mamm_algae = self.cbt_mamm_low_lc50 * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_low_lc50_mamm_invert = self.cbt_mamm_low_lc50 * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_low_lc50_mamm_fish = self.cbt_mamm_low_lc50 * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sub_direct_mamm_algae = self.cbt_mamm_sub_direct * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sub_direct_mamm_invert = self.cbt_mamm_sub_direct * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sub_direct_mamm_fish = self.cbt_mamm_sub_direct * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_grow_noec_mamm_algae = self.cbt_mamm_grow_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_grow_noec_mamm_invert = self.cbt_mamm_grow_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_grow_noec_mamm_fish = self.cbt_mamm_grow_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_grow_loec_mamm_algae = self.cbt_mamm_grow_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_grow_loec_mamm_invert = self.cbt_mamm_grow_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_grow_loec_mamm_fish = self.cbt_mamm_grow_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_repro_noec_mamm_algae = self.cbt_mamm_repro_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_repro_noec_mamm_invert = self.cbt_mamm_repro_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_repro_noec_mamm_fish = self.cbt_mamm_repro_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_repro_loec_mamm_algae = self.cbt_mamm_repro_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_repro_loec_mamm_invert = self.cbt_mamm_repro_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_repro_loec_mamm_fish = self.cbt_mamm_repro_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_behav_noec_mamm_algae = self.cbt_mamm_behav_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_behav_noec_mamm_invert = self.cbt_mamm_behav_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_behav_noec_mamm_fish = self.cbt_mamm_behav_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_behav_loec_mamm_algae = self.cbt_mamm_behav_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_behav_loec_mamm_invert = self.cbt_mamm_behav_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_behav_loec_mamm_fish = self.cbt_mamm_behav_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sensory_noec_mamm_algae = self.cbt_mamm_sensory_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sensory_noec_mamm_invert = self.cbt_mamm_sensory_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sensory_noec_mamm_fish = self.cbt_mamm_sensory_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sensory_loec_mamm_algae = self.cbt_mamm_sensory_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sensory_loec_mamm_invert = self.cbt_mamm_sensory_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sensory_loec_mamm_fish = self.cbt_mamm_sensory_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sub_indirect_mamm_algae = self.cbt_mamm_sub_indirect * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sub_indirect_mamm_invert = self.cbt_mamm_sub_indirect * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sub_indirect_mamm_fish = self.cbt_mamm_sub_indirect * self.mg_to_ug / self.fish_bcf_upper

        # birds
        self.aq_conc_thres_1inmill_mort_bird_algae = self.cbt_bird_1inmill_mort * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_1inmill_mort_bird_invert = self.cbt_bird_1inmill_mort * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_1inmill_mort_bird_fish = self.cbt_bird_1inmill_mort * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_1inten_bird_algae = self.cbt_bird_1inten_mort * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_1inten_bird_invert = self.cbt_bird_1inten_mort * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_1inten_bird_fish = self.cbt_bird_1inten_mort * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_low_lc50_bird_algae = self.cbt_bird_low_lc50 * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_low_lc50_bird_invert = self.cbt_bird_low_lc50 * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_low_lc50_bird_fish = self.cbt_bird_low_lc50 * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sub_direct_bird_algae = self.cbt_bird_sub_direct * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sub_direct_bird_invert = self.cbt_bird_sub_direct * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sub_direct_bird_fish = self.cbt_bird_sub_direct * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_grow_noec_bird_algae = self.cbt_bird_grow_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_grow_noec_bird_invert = self.cbt_bird_grow_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_grow_noec_bird_fish = self.cbt_bird_grow_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_grow_loec_bird_algae = self.cbt_bird_grow_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_grow_loec_bird_invert = self.cbt_bird_grow_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_grow_loec_bird_fish = self.cbt_bird_grow_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_repro_noec_bird_algae = self.cbt_bird_repro_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_repro_noec_bird_invert = self.cbt_bird_repro_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_repro_noec_bird_fish = self.cbt_bird_repro_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_repro_loec_bird_algae = self.cbt_bird_repro_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_repro_loec_bird_invert = self.cbt_bird_repro_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_repro_loec_bird_fish = self.cbt_bird_repro_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_behav_noec_bird_algae = self.cbt_bird_behav_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_behav_noec_bird_invert = self.cbt_bird_behav_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_behav_noec_bird_fish = self.cbt_bird_behav_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_behav_loec_bird_algae = self.cbt_bird_behav_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_behav_loec_bird_invert = self.cbt_bird_behav_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_behav_loec_bird_fish = self.cbt_bird_behav_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sensory_noec_bird_algae = self.cbt_bird_sensory_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sensory_noec_bird_invert = self.cbt_bird_sensory_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sensory_noec_bird_fish = self.cbt_bird_sensory_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sensory_loec_bird_algae = self.cbt_bird_sensory_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sensory_loec_bird_invert = self.cbt_bird_sensory_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sensory_loec_bird_fish = self.cbt_bird_sensory_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sub_indirect_bird_algae = self.cbt_bird_sub_indirect * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sub_indirect_bird_invert = self.cbt_bird_sub_indirect * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sub_indirect_bird_fish = self.cbt_bird_sub_indirect * self.mg_to_ug / self.fish_bcf_upper

        # reptiles & terrestrial-phase amphibians
        self.aq_conc_thres_1inmill_mort_reptile_algae = self.cbt_reptile_1inmill_mort * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_1inmill_mort_reptile_invert = self.cbt_reptile_1inmill_mort * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_1inmill_mort_reptile_fish = self.cbt_reptile_1inmill_mort * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_1inten_reptile_algae = self.cbt_reptile_1inten_mort * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_1inten_reptile_invert = self.cbt_reptile_1inten_mort * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_1inten_reptile_fish = self.cbt_reptile_1inten_mort * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_low_lc50_reptile_algae = self.cbt_reptile_low_lc50 * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_low_lc50_reptile_invert = self.cbt_reptile_low_lc50 * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_low_lc50_reptile_fish = self.cbt_reptile_low_lc50 * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sub_direct_reptile_algae = self.cbt_reptile_sub_direct * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sub_direct_reptile_invert = self.cbt_reptile_sub_direct * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sub_direct_reptile_fish = self.cbt_reptile_sub_direct * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_grow_noec_reptile_algae = self.cbt_reptile_grow_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_grow_noec_reptile_invert = self.cbt_reptile_grow_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_grow_noec_reptile_fish = self.cbt_reptile_grow_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_grow_loec_reptile_algae = self.cbt_reptile_grow_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_grow_loec_reptile_invert = self.cbt_reptile_grow_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_grow_loec_reptile_fish = self.cbt_reptile_grow_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_repro_noec_reptile_algae = self.cbt_reptile_repro_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_repro_noec_reptile_invert = self.cbt_reptile_repro_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_repro_noec_reptile_fish = self.cbt_reptile_repro_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_repro_loec_reptile_algae = self.cbt_reptile_repro_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_repro_loec_reptile_invert = self.cbt_reptile_repro_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_repro_loec_reptile_fish = self.cbt_reptile_repro_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_behav_noec_reptile_algae = self.cbt_reptile_behav_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_behav_noec_reptile_invert = self.cbt_reptile_behav_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_behav_noec_reptile_fish = self.cbt_reptile_behav_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_behav_loec_reptile_algae = self.cbt_reptile_behav_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_behav_loec_reptile_invert = self.cbt_reptile_behav_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_behav_loec_reptile_fish = self.cbt_reptile_behav_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sensory_noec_reptile_algae = self.cbt_reptile_sensory_noec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sensory_noec_reptile_invert = self.cbt_reptile_sensory_noec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sensory_noec_reptile_fish = self.cbt_reptile_sensory_noec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sensory_loec_reptile_algae = self.cbt_reptile_sensory_loec * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sensory_loec_reptile_invert = self.cbt_reptile_sensory_loec * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sensory_loec_reptile_fish = self.cbt_reptile_sensory_loec * self.mg_to_ug / self.fish_bcf_upper
        self.aq_conc_thres_sub_indirect_reptile_algae = self.cbt_reptile_sub_indirect * self.mg_to_ug / self.aq_plant_algae_bcf_upper
        self.aq_conc_thres_sub_indirect_reptile_invert = self.cbt_reptile_sub_indirect * self.mg_to_ug / self.inv_bcf_upper
        self.aq_conc_thres_sub_indirect_reptile_fish = self.cbt_reptile_sub_indirect * self.mg_to_ug / self.fish_bcf_upper

    def calc_aq_invert_fish_concs(self):
        """
        :description calculates estimated tissue concentrations in aquatic invertebrates and fish using BCFs
        :NOTE         represents columns B, C, D, and F of worksheet 'aquatic organism tissue concs' of OPP TED Excel spreadsheet model
                      (this method is 'vectorized', that is calculations are performed here for all simulations)
        :return:
        """

        # invertebrates tissue concentrations (using mean BCF values)
        self.tissue_conc_aq_invert_mean_1 = self.aq_conc_level1 * self.inv_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_invert_mean_2 = self.aq_conc_level1 * self.inv_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_invert_mean_3 = self.aq_conc_level1 * self.inv_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_invert_mean_4 = self.aq_conc_level1 * self.inv_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_invert_mean_5 = self.aq_conc_level1 * self.inv_bcf_mean / self.mg_to_ug

        # invertebrate tissue concentrations (using upper bound BCF values)
        self.tissue_conc_aq_invert_upper_1 = self.aq_conc_level1 * self.inv_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_invert_upper_2 = self.aq_conc_level1 * self.inv_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_invert_upper_3 = self.aq_conc_level1 * self.inv_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_invert_upper_4 = self.aq_conc_level1 * self.inv_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_invert_upper_5 = self.aq_conc_level1 * self.inv_bcf_upper / self.mg_to_ug

        # fish tissue concentrations (using mean BCF values)
        self.tissue_conc_aq_fish_mean_1 = self.aq_conc_level1 * self.fish_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_fish_mean_2 = self.aq_conc_level1 * self.fish_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_fish_mean_3 = self.aq_conc_level1 * self.fish_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_fish_mean_4 = self.aq_conc_level1 * self.fish_bcf_mean / self.mg_to_ug
        self.tissue_conc_aq_fish_mean_5 = self.aq_conc_level1 * self.fish_bcf_mean / self.mg_to_ug

        # fish tissue concentrations (using upper bound BCF values)
        self.tissue_conc_aq_fish_upper_1 = self.aq_conc_level1 * self.fish_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_fish_upper_2 = self.aq_conc_level1 * self.fish_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_fish_upper_3 = self.aq_conc_level1 * self.fish_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_fish_upper_4 = self.aq_conc_level1 * self.fish_bcf_upper / self.mg_to_ug
        self.tissue_conc_aq_fish_upper_5 = self.aq_conc_level1 * self.fish_bcf_upper / self.mg_to_ug


    def calc_runoff_params(self, i, app_method, app_rate, pest_incorp_depth):
        """
        :description calculates runoff parameters used to calculate plant EECs for wet and dry areas

        :param i; simulation number
        :param app_method; application method (aerial/ground/airblast)
        :param app_rate; application rate (lbs a.i./Acre)
        :param pest_incorp_depth; pesticide incorporation depth in soil

        :NOTE  represents calculations found in columns C & D rows 3 - 5 in OPP TED Excel spreadsheet 'Plants' worksheet
        :return:
        """

        # set pesticide incorporation factor (default of 1 for aerial & airblast)
        if (app_method == 'aerial' or 'airblast'):
            pest_incorp_factor = 1.0
        else:  # ground application
            if (pest_incorp_depth < 1.0):
                pest_incorp_factor = 1.0
            elif (pest_incorp_depth > 1.0 and pest_incorp_depth < 6.0):
                pest_incorp_factor = pest_incorp_depth
            else: # greater than 6.0
                pest_incorp_factor = 6.0

        # set runoff fraction (based on pesticide solubilty)
        if (self.solubility[i] < 10.0):
            runoff_frac = 0.01
        elif (self.solubility[i] > 100.0):
            runoff_frac = 0.05
        else:
            runoff_frac = 0.02

        return pest_incorp_factor, runoff_frac

    def calc_runoff_based_eec(self, app_rate, pest_incorp_factor, runoff_frac):
        """
        :description calculates runoff based plant EECs for wet and dry areas

        :param app_rate; application rate (lbs a.i./Acre)
        :param pest_incorp_factor; pesticide incorporation factor (depth) in soil

        :NOTE  represents calculations found in columns C & D rows 9 - 10 in OPP TED Excel spreadsheet 'Plants' worksheet
        :return:
        """

        runoff_eec_dry_area = (app_rate / pest_incorp_factor) * runoff_frac

        runoff_eec_semiaq_area = runoff_eec_dry_area * 10.

        return runoff_eec_dry_area, runoff_eec_semiaq_area

    def plant_risk_conclusions(self, i):
        """
         :description calls method to determines if plant health thresholds are exceeded in terrestrial (dry) and wetland habitats

         :param i; simulation number

         :NOTE  represents determinations found in columns C & D rows 14 - 28 in OPP TED Excel spreadsheet 'Plants' worksheet
         :return:
         """

        # monocots; terrestrial habitats; minimum application scenario
        self.pt_mono_pre_noec_eec_exceed = self.plant_eec_exceedance(self.pt_mono_pre_noec[i], self.runoff_eec_dry_area_min)
        self.pt_mono_pre_loec_eec_exceed = self.plant_eec_exceedance(self.pt_mono_pre_loec[i], self.runoff_eec_dry_area_min)
        self.pt_mono_pre_ec25_eec_exceed = self.plant_eec_exceedance(self.pt_mono_pre_ec25[i], self.runoff_eec_dry_area_min)

        # dicots; terrestrial habitats; maximum application scenario
        self.pt_dicot_pre_noec_eec_exceed = self.plant_eec_exceedance(self.pt_dicot_pre_noec[i], self.runoff_eec_dry_area_max)
        self.pt_dicot_pre_loec_eec_exceed = self.plant_eec_exceedance(self.pt_dicot_pre_loec[i], self.runoff_eec_dry_area_max)
        self.pt_dicot_pre_ec25_eec_exceed = self.plant_eec_exceedance(self.pt_dicot_pre_ec25[i], self.runoff_eec_dry_area_max)

        # monocots; wetland habitats; minimum application scenario
        self.pt_mono_pre_noec_eec_exceed = self.plant_eec_exceedance(self.pt_mono_pre_noec[i], self.runoff_eec_semiaq_area_min)
        self.pt_mono_pre_loec_eec_exceed = self.plant_eec_exceedance(self.pt_mono_pre_loec[i], self.runoff_eec_semiaq_area_min)
        self.pt_mono_pre_ec25_eec_exceed = self.plant_eec_exceedance(self.pt_mono_pre_ec25[i], self.runoff_eec_semiaq_area_min)

        # dicots; wetland habitats; maximum application scenario
        self.pt_dicot_pre_noec_eec_exceed = self.plant_eec_exceedance(self.pt_dicot_pre_noec[i], self.runoff_eec_semiaq_area_max)
        self.pt_dicot_pre_loec_eec_exceed = self.plant_eec_exceedance(self.pt_dicot_pre_loec[i], self.runoff_eec_semiaq_area_max)
        self.pt_dicot_pre_ec25_eec_exceed = self.plant_eec_exceedance(self.pt_dicot_pre_ec25[i], self.runoff_eec_semiaq_area_max)

    def plant_eec_exceedance(self, health_measure, runoff_eec):

        """
         :description checks to determines if plant health threshold EEC is exceeded (in terrestrial (dry) and wetland habitats)

         :param health_measure; plant health measure (e.g., pre-emergence NOEC for growth for monocots and dicots)
         :param runoff_eec;  eec for plants resulting from pesticide in runoff

         :NOTE  represents determinations found in columns C & D rows 14 - 28 in OPP TED Excel spreadsheet 'Plants' worksheet
         :return:
         """

        if (math.isnan(health_measure)):
            exceedance_chk = 'NA'                     # no health measure given
        elif (self.runoff_eec_dry_area_min > health_measure):
            exceedance_chk = 'yes'
        else:
            exceedance_chk = 'no'
        return exceedance_chk

    # -----------------------------------------------------------------------
    # THE FOLLOWING METHODS MAY BE ORGAINIZED BETTER IN A PARAMETERS CLASS
    # -----------------------------------------------------------------------

    def set_drift_parameters(self, app_method, boom_hgt, drop_size):
        """
        :description provides parmaeter values to use when calculating distances from edge of application source area to
                     concentration of interest
        :param app_method; application method (aerial/ground/airblast)
        :param boom_hgt; height of boom (low/high) - 'NA' if not ground application
        :param drop_size; droplet spectrum for application (see list below for aerial/ground - 'NA' if airblast)
        :param param_a; parameter a for spray drift distance calculation
        :param param_b; parameter b for spray drift distance calculation
        :param param_c; parameter c for spray drift distance calculation

        :return:
        """

        if app_method == 'aerial':
            if drop_size == 'very_fine_to_fine':
                param_a = 0.0292
                param_b = 0.822
                param_c = 0.6539
            elif drop_size == 'fine_to_medium':
                param_a = 0.043
                param_b = 1.03
                param_c = 0.5
            elif drop_size == 'medium_to_coarse':
                param_a = 0.0721
                param_b = 1.0977
                param_c = 0.4999
            elif drop_size == 'coarse_to_very_coarse':
                param_a = 0.1014
                param_b = 1.1344
                param_c = 0.4999
        elif app_method == 'ground':
            if boom_hgt == 'low':
                if drop_size == 'very_fine_to_fine':
                    param_a = 1.0063
                    param_b = 0.9998
                    param_c = 1.0193
                elif drop_size == 'fine_to_medium-coarse':
                    param_a = 5.5513
                    param_b = 0.8523
                    param_c = 1.0079
            elif boom_hgt == 'high':
                if drop_size == 'very_fine_to_fine':
                    param_a = 0.1913
                    param_b = 1.2366
                    param_c = 1.0552
                elif drop_size == 'fine_to_medium-coarse':
                    param_a = 2.4154
                    param_b = 0.9077
                    param_c = 1.0128
        elif app_method == 'airblast':
            param_a = 0.0351
            param_b = 2.4586
            param_c = 0.4763

        else:
            pass

        return param_a, param_b, param_c

    def set_max_drift_distance(self, app_method):
        """
        :description sets the maximum distance from applicaiton source area for which spray drift calculations are calculated
        :param app_method; application method (aerial/ground/airblast)
        :param max_spray_drift_dist: maximum distance from applicaiton source area for which spray drift calculations are calculated (feet)

        :return:
        """

        max_spray_drift_dist = 1000.  # default value; used for ground and airblast application methods

        if app_method == 'aerial':
            max_spray_drift_dist = 2600.

        return max_spray_drift_dist

    def set_max_respire_frac(self, app_method, drop_size):
        """
        :description provides parmaeter values to use when calculating distances from edge of application source area to
                     concentration of interest
        :param app_method; application method (aerial/ground/airblast)
        :param drop_size; droplet spectrum for application (see list below for aerial/ground - 'NA' if airblast)
        :param max_respire_frac; volumetric fraction of droplet spectrum not exceeding the upper size liit of respired particles for birds

        :NOTE this represents specification from OPP TED Excel 'inputs' worksheet columns H & I rows 14 - 16
              these values are used in the 'min/max rate doses' worksheet column S (while referenced here as the MAX of
              three values specified in the 'inputs' worksheet (one per application method) the MAX will always be the value associated
              with the application method specified for the simulation (i.e., the value specified below)
        :return:
        """

        if app_method == 'aerial':
            if drop_size == 'very_fine_to_fine':
                max_respire_frac = 0.28
            elif drop_size == 'fine_to_medium':
                max_respire_frac = 0.067
            elif drop_size == 'medium_to_coarse':
                max_respire_frac = 0.028
            elif drop_size == 'coarse_to_very_coarse':
                max_respire_frac = 0.02
        elif app_method == 'ground':
            if drop_size == 'very_fine_to_fine':
                max_respire_frac = 0.28
            elif drop_size == 'fine_to_medium-coarse':
                max_respire_frac = 0.067
        elif app_method == 'airblast':
            max_respire_frac = 0.28
        else:
            pass
        return max_respire_frac

    def sum_exceedances(self, sim_num, num_ts, num_tox, time_series, tox_series):
        """
        :description this method accumulates the number of time various toxicity measures are exceeded within daily time
                     series of food item concentrations
        :param sim_num current simulation number; used to reference tox_series index
        :param num_ts number of time series included in the aggregate incoming 'time_series'
        :param num_tox number of toxicity measures to be precessed per time series
        :param a panda series representing an aggregation of time series representing the daily concentrations in food items (e.g., short grass, arthropods etc.)
        :param tox_series a panda series representing the list of toxicity measures

        :NOTE this method is used to replicate the OPP TED Excel model worksheet 'Min/Max rate - dietary conc results' columns D - N lines 3 - 54
              (this method is a temporary solution for the need to populate a panda series with mixed data types;
              when a more elegant solution comes available this method can simply be replaced without other changes - or so I think)

              for example: the following line of code performs the same function when all series values are floats
              exceedances = [(self.time_sesries[0][i] > self.tox_series[0][j]).sum() for i in range(11) for j in range(13)]

        :return:
        """

        k = -1
        exceedances = pd.Series([])
        for i in range(num_ts):       # process individual food item time series
            for j in range(num_tox):  # process individual toxicity measures
                k=k+1
                if (time_series[i][0][0] != 'NA'):
                    exceedances[k] = (time_series[i][0] > tox_series[j][sim_num]).sum() # place sums into series for subsequent slicing/shaping
                                                                                  # each num_tox values represents a food item
                else:
                   exceedances[k] = 'NA'
        return exceedances