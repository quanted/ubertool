from __future__ import division  # brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
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

    def drift_distance_calc(self, app_rate_frac, param_a, param_b, param_c):
        """
        :description calculates distance from edge of application source area to where the fraction of the application rate
                     results in a concentration that would result in the health threshold (which is in terms of a dose resulting
                     from exposure to the concentration) ; TED calculates the fraction by dividing the health threshold of interest
                     by the maximum dose from among all dietary items and ingestion/inhalation/contact of/with water/air/soil
        :param app_rate_frac; fraction of active ingredient application rate equivalent to the health threshold of concern
        :param param_a; parameter a for spray drift distance calculation
        :param param_b; parameter b for spray drift distance calculation
        :param param_c; parameter c for spray drift distance calculation

        # this represents Eq 1 of Attachment 1-7 of 'Biological Evaluation Chapters for Diazinon ESA Assessment'

        :return:
        """
        distance = (((param_c / app_rate_frac) ** (1. / param_b)) - 1.) / param_a

        # reset distance if outside bounds
        if (distance < 0.0): distance = 0.0
        if (distance > self.max_distance_from_source): distance = self.max_distance_from_source

        return distance

    # -----------------------------------------------------------------------
    # THE FOLLOWING METHODS MAY BE ORGAINIZED BETTER IN A PARAMETERS CLASS; or called from the constants method
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