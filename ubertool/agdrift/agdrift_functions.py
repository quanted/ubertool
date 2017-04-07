from __future__ import division  # brings in Python 3.0 mixed type calculation rules
from functools import wraps
import logging
import numpy as np
import os
import pandas as pd
from scipy.optimize import curve_fit
from sqlalchemy import Column, Table, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *
import sqlalchemy_utils as sqlu
import sqlite3
import time
import csv

metadata = MetaData()


class AgdriftFunctions(object):
    """
    Function class for agdrift.
    """

    def __init__(self):
        """Class representing the functions for agdrift"""
        super(AgdriftFunctions, self).__init__()

    def validate_sim_scenarios(self):
        """
        :description determines if user defined scenarios are valid for processing
        :param application_method: type of Tier I application method employed
        :param aquatic_body_def: type of endpoint of concern (e.g., pond, wetland); implies whether
        :                    endpoint of concern parameters (e.g.,, pond width) are set (i.e., by user or EPA standard)
        :param drop_size: qualitative description of spray droplet size
        :param boom_height: qualitative height above ground of spray boom
        :param airblast_type: type of orchard being sprayed
        :NOTE we perform an additional validation check related to distances later in the code just before integration
        :return
        """
        aquatic_body_type_list = ['EPA Defined Pond', 'User Defined Pond', 'EPA Defined Wetland', 'User Defined Wetland']
        aquatic_drop_size_list = ['Very Fine to Fine', 'Fine to Medium', 'Medium to Coarse', 'Coarse to Very Coarse']
        terrestrial_field_type_list = ['EPA Defined Terrestrial', 'User Defined Terrestrial']
        terrestrial_drop_size_list = ['Very Fine', 'Fine to Medium/Coarse']
        airblast_type_list = ['Orchard', 'Vineyard', 'Normal', 'Dense', 'Sparse']
        boom_height_list = ['High', 'Low']

        for i in range(self.num_simulations):
            print(self.ecosystem_type[i])
            if (self.ecosystem_type[i] == 'Aquatic Assessment'):
                if self.application_method[i] == 'Tier I Aerial':
                    if (self.aquatic_body_type[i] in aquatic_body_type_list and
                                self.drop_size[i] in aquatic_drop_size_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Aquatic Aerial Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Aerial Scenario'
                elif self.application_method[i] == 'Tier I Ground':
                    if (self.aquatic_body_type[i] in aquatic_body_type_list and
                                self.drop_size[i] in terrestrial_drop_size_list and
                                self.boom_height[i] in boom_height_list):
                         self.out_sim_scenario_chk[i] = 'Valid Tier I Aquatic Ground Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Ground Scenario'
                elif self.application_method[i] == 'Tier I Airblast':
                    if (self.aquatic_body_type[i] in aquatic_body_type_list and
                        self.airblast_type[i] in airblast_type_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Aquatic Airblast Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Airblast Scenario'
                else:
                    self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Assessment application_method'
            elif (self.ecosystem_type[i] == 'Terrestrial Assessment'):
                if self.application_method[i] == 'Tier I Aerial':
                    if (self.terrestrial_field_type[i] in terrestrial_field_type_list and
                                self.drop_size[i] in aquatic_drop_size_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Terrestrial Aerial Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Aerial Scenario'
                elif self.application_method[i] == 'Tier I Ground':
                    if (self.terrestrial_field_type[i] in terrestrial_field_type_list and
                         self.boom_height[i] in boom_height_list):
                         self.out_sim_scenario_chk[i] = 'Valid Tier I Terrestrial Ground Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Ground Scenario'
                elif self.application_method[i] == 'Tier I Airblast':
                    if (self.terrestrial_field_type[i] in terrestrial_field_type_list and
                                self.airblast_type[i] in airblast_type_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Terrestrial Airblast Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Airblast Scenario'
                else:
                    self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Assessment application_method'
            else:
                    self.out_sim_scenario_chk[i] = 'Invalid scenario ecosystem_type'
        return

    def assign_column_names(self):
        """
        :description assigns column names from sql database to internal scenario names
        :param column_name: short name for pesiticide application scenario for which distance vs deposition data is provided
        :param scenario_name: internal variable for holding scenario names
        :param scenario_number: index for scenario_name (this method assumes the distance values could occur in any column
        :param distance_name: internal name for the column holding distance data
        :return:
        """
        self.scenario_name = pd.Series([], dtype='object')
        self.scenario_number = 0
        for i in range(len(self.column_names)):
            if ('dist' in self.column_names[i]):
                self.distance_name = self.column_names[i]
            else:
                self.scenario_name[self.scenario_number] = self.column_names[i]
                self.scenario_number += 1
        return

    def set_sim_scenario_id(self):
        """
        :description provides scenario ids per simulation that match scenario names (i.e., column_names) from SQL database
        :return:
        """
        self.out_sim_scenario_id = pd.Series([], dtype='object')
        for i in range(self.num_simulations):
            if(not 'Invalid' in self.out_sim_scenario_chk[i]):
                if self.application_method[i] == 'Tier I Aerial':
                    if self.drop_size[i] == 'Very Fine to Fine':
                        self.out_sim_scenario_id[i] = 'aerial_vf2f'
                    elif self.drop_size[i] == 'Fine to Medium':
                        self.out_sim_scenario_id[i] = 'aerial_f2m'
                    elif self.drop_size[i] == 'Medium to Coarse':
                        self.out_sim_scenario_id[i] = 'aerial_m2c'
                    elif self.drop_size[i] == 'Coarse to Very Coarse':
                        self.out_sim_scenario_id[i] = 'aerial_c2vc'
                elif self.application_method[i] == 'Tier I Ground':
                    if self.boom_height[i] == 'Low':
                        if self.drop_size[i] == 'Very Fine':
                            self.out_sim_scenario_id[i] = 'ground_low_vf'
                        elif self.drop_size[i] == 'Fine to Medium/Coarse':
                            self.out_sim_scenario_id[i] = 'ground_low_fmc'
                    elif self.boom_height[i] == 'High':
                        if self.drop_size[i] == 'Very Fine':
                            self.out_sim_scenario_id[i] = 'ground_high_vf'
                        elif self.drop_size[i] == 'Fine to Medium/Coarse':
                            self.out_sim_scenario_id[i] = 'ground_high_fmc'
                elif self.application_method[i] == 'Tier I Airblast':
                    if self.airblast_type[i] == 'Normal':
                        self.out_sim_scenario_id[i] = 'airblast_normal'
                    elif self.airblast_type[i] == 'Dense':
                        self.out_sim_scenario_id[i] = 'airblast_dense'
                    elif self.airblast_type[i] == 'Sparse':
                        self.out_sim_scenario_id[i] = 'airblast_sparse'
                    elif self.airblast_type[i] == 'Vineyard':
                        self.out_sim_scenario_id[i] = 'airblast_vineyard'
                    elif self.airblast_type[i] == 'Orchard':
                        self.out_sim_scenario_id[i] = 'airblast_orchard'
            else:
                self.out_sim_scenario_id[i] = 'Invalid'
        return

    def list_sims_per_scenario(self):
        """
        :description scan simulations and count number and indices of simulations that apply to each scenario
        :parameter num_scenarios number of deposition scenarios included in SQL database
        :parameter num_simulations number of simulations included in this model execution
        :parameter scenario_name name of deposition scenario as recorded in SQL database
        :parameter out_sim_scenario_id identification of deposition scenario specified per model run simulation
        :return:
        """

        # initialize lists of simulation counts per scenario and simulation numbers (indices) per scenario
        num_sims = pd.Series(self.num_scenarios*[0], dtype='int')
        sim_indices = pd.Series([self.num_simulations*[0] for i in range (self.num_scenarios)], dtype='int')

        # process simulation deposition scenario names and 1) count number simulations that include scenario, and
        # 2) list the simulation index for which each scenario is identified
        for i in range(self.num_simulations):
            for j in range(self.num_scenarios):
                if (self.scenario_name[j] == self.out_sim_scenario_id[i]):
                    num_sims[j] += 1
                    sim_indices[j][num_sims[j] - 1] = i
        return num_sims, sim_indices

    def filter_arrays(self,x_in,y_in):
        """
        :description  eliminate blank data cells (i.e., distances for which no deposition value is provided)
                     (and thus reduce the number of x,y values to be used)
        :parameter x_in: array of distance values associated with values for a deposition scenario (e.g., Aerial/EPA Defined Pond)
        :parameter y_in: array of deposition values associated with a deposition scenario (e.g., Aerial/EPA Defined Pond)
        :parameter x_out: processed array of x_in values eliminating indices of blank distance/deposition values
        :parameter y_out: processed array of y_in values eliminating indices of blank distance/deposition values
        :NOTE arrays are assumed to be populated by values >= 0. except for the blanks as 'nan' entries
        :return:
        """

        x_out = pd.Series([], dtype='float')
        y_out = pd.Series([], dtype='float')
        j = 0
        for i in range(len(x_in)):
            if (y_in[i] >= 0.0):
                # fill temp arrays of x and y
                x_out[j] = x_in[i]
                y_out[j] = y_in[i]
                j += 1
        return x_out, y_out

    def determine_area_dimensions(self, i):
        """
        :description determine relevant area/length/depth of waterbody or terrestrial area
        :param i: simulation number
        :param ecosystem_type: type of assessment to be conducted
        :param aquatic_body_type: source of dimensional data for area (EPA or User defined)
        :param terrestrial_field_type: source of dimensional data for area (EPA or User defined)
        :param *_width: default or user specified width of waterbody or terrestrial field
        :param *_length: default or user specified length of waterbody or terrestrial field
        :param *_depth: default or user specified depth of waterbody or terrestrial field
        :NOTE  all areas, i.e., ponds, wetlands, and terrestrial fields are of 1 hectare size; the user can elect
               to specify a width other than the default width but it won't change the area size; thus for
               user specified areas the length is calculated and not specified by the user)
        :return:
        """

        if (self.ecosystem_type[i] == 'Aquatic Assessment'):
            if (self.aquatic_body_type[i] == 'EPA Defined Pond'):
                self.out_area_width[i] = self.default_width
                self.out_area_length[i] = self.default_length
                self.out_area_depth[i] = self.default_pond_depth
            elif (self.aquatic_body_type[i] == 'EPA Defined Wetland'):
                self.out_area_width[i] = self.default_width
                self.out_area_length[i] = self.default_length
                self.out_area_depth[i] = self.default_wetland_depth
            elif (self.aquatic_body_type[i] == 'User Defined Pond'):
                self.out_area_width[i] = self.user_pond_width[i]
                self.out_area_length[i] = self.sqft_per_hectare / self.out_area_width[i]
                self.out_area_depth[i] = self.user_pond_depth[i]
            elif (self.aquatic_body_type[i] == 'User Defined Wetland'):
                self.out_area_width[i] = self.user_wetland_width[i]
                self.out_area_length[i] = self.sqft_per_hectare / self.out_area_width[i]
                self.out_area_depth[i] = self.user_wetland_depth[i]
        elif (self.ecosystem_type[i] == 'Terrestrial Assessment'):
            if (self.terrestrial_field_type[i] == 'User Defined Terrestrial'):  # implies user to specify an area width
                self.out_area_width[i] = self.user_terrestrial_width[i]
                self.out_area_length[i] = self.sqft_per_hectare / self.out_area_width[i]
                self.out_area_depth[i] = 0.  # terrestrial areas have no depth
            else:  #this is the EPA Defined Terrestrial (i.e., a point as opposed to an area) for which we don't need dimensions
                self.out_area_width[i] = 0.
                self.out_area_length[i] = 0.
                self.out_area_depth[i] = 0.
        return self.out_area_width[i], self.out_area_length[i], self.out_area_depth[i]
    
    def extend_dist_dep_curve(self,i):
        """
        :description extends distance vs deposition (fraction of applied) curce to enable model calculations 
                     when area of interest (pond, wetland, terrestrial field) lie partially outside the orginal
                     curve (whose extent is 997 feet).  The extension is achieved by fitting a line of best fit
                     to the last 16 points of the original curve.  The x,y values representing the last 16 points
                     are natural log transforms of the distance and deposition values at the 16 points.  Two long
                     transforms are coded here, reflecting the fact that the AGDRIFT model (v2.1.1) uses each of them
                     under different circumstandes (which I believe is not the intention but is the way the model 
                     functions  --  my guess is that one of the transforms was used and then a second one was coded 
                     to increase the degree of conservativeness  -- but the code was changed in only one of the two 
                     places where the transformation occurs.  
                     Finally, the AGDRIFT model extends the curve only when necessary (i.e., when it determines that 
                     the area of intereest lies partially beyond the last point of the origanal curve (997 ft).  In 
                     this code all the curves are extended out to 1994 ft, which represents the furthest distance that 
                     the downwind edge of an area of concern can be specified.  All scenario curves are extended here 
                     because we are running multiple simulations (e.g., monte carlo) and instead of extending the 
                     curves each time a simulation requires it (which may be multiple time for the same scenario 
                     curve) we just do it for all curves up front.  There is a case to be made that the 
                     curves should be extended external to this code and simply provide the full curve in the SQLite
                     database containing the original curve.  
                    
        :param i: index representing distance vs deposition scenario curve to be extended
        :return:
        """

        #set first and last index of points to be used to fit line 
        npts_orig = len(self.scenario_distance_data[i])
        first_fit_pt = npts_orig - 16

        # set arrays for containing curve points to be used to fit/extend curve at tail
        x_array = np.zeros([16])  #distance
        y_array = np.zeros([16])  #deposition (fraction of applied)

        # select the last 16 data points and perform a natural log transform on the distance/deposition values
        # then fit these data to a line of best fit

        if (self.extend_ln_ln):  #straight ln ln transformation
            x_array = np.array([self.scenario_distance_data[i][j] for j in range(first_fit_pt, npts_orig)])
            x_array = np.log(x_array)
            y_array = np.array([self.scenario_deposition_data[i][j] for j in range(first_fit_pt, npts_orig)])
            y_array = np.log(y_array)
        else:  
            # this ln transformation is done with relative x,y values (this is the transformation
            # used in the AGDRIFT AGEXTD code
            x_zero = self.scenario_distance_data[i][first_fit_pt - 1]
            y_zero = self.scenario_deposition_data[i][first_fit_pt - 1]
            y_zero_log = np.log(y_zero)

            k = 0
            for j in range(first_fit_pt, npts_orig):
                x_array[k] = np.log(self.scenario_distance_data[i][j] - x_zero)
                y_array[k] = np.log(self.scenario_deposition_data[i][j] / y_zero)
                k += 1

        # establish scipy function to be fit to x_array, y_array data pts
        def func(x_array, a, b):
            return a * x_array + b

        # use scipy's curve fit and get the coefficients for the established function
        coefficients, pcov = curve_fit(func, x_array, y_array)
        coef_a = coefficients[0]
        coef_b = coefficients[1]

        # extend the distance array to 2 * 997 = 1994ft in increments of 6.56ft (and calculate related depositions)
        npts_ext = int(((((self.max_distance * 2.) - self.scenario_distance_data[i][npts_orig - 1]) / \
                         self.distance_inc) + 1) + npts_orig)
        dist = self.scenario_distance_data[i][npts_orig - 1]
        for j in range(npts_orig, npts_ext):
            dist = dist + self.distance_inc

            if (self.extend_ln_ln):
                self.scenario_deposition_data[i][j] = np.exp(coef_a * np.log(dist) + coef_b)
            else:
                y_temp = coef_a * np.log(dist - x_zero) + coef_b
                self.scenario_deposition_data[i][j] = np.exp(y_temp + y_zero_log)

            self.scenario_distance_data[i][j] = self.scenario_distance_data[i][j - 1] + self.distance_inc
        return

    def get_column_names(self):
        """
        :description retrieves column names from sql database (sqlite_agdrift_1994ft.db)
        :            (each column name refers to a specific deposition scenario;
        :             the scenario name is used later to retrieve the deposition data)
        :parameter output name of sql database table from which to retrieve requested data
        :return:
        """

        # connect to the sql database and get column names (1st column will be the distances
        # rather than a scenario name)
        if sqlu.database_exists(self.db_name):
            engine = create_engine(self.db_name)
            conn = engine.connect()
            result1 = conn.execute("SELECT * from " + self.db_table)
            col_names = result1.keys()
        else:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            logging.info('current directory path is:')
            logging.info(dir_path)
            print('cannot find agdrift database at ' + self.db_name)
        return col_names

    def get_distances(self, num_values):
        """
        :description retrieves distance values for deposition scenario datasets
        :            all scenarios use same distances
        :param num_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE any blank fields are filled with 'nan'
        :return:
        """
        engine = create_engine(self.db_name)
        conn = engine.connect()
        result = conn.execute("SELECT " + self.distance_name + " from " + self.db_table)

        data = pd.Series(np.zeros(num_values))
        for i, row in enumerate(result):
            try:
                temp = float(row[0])
                data[i] = temp.real
            except:
                data[i] = 'nan'  # fill in empty elements (should not be any empty elements for distance array)
        conn.close()
        return data

    def get_scenario_deposition_data(self, scenario, num_values):
        """
        :description retrieves deposition data for a scenario from sql database
        :            (for all elements that are blank a 'nan' value is inserted)
        :param scenario: name of scenario for which data is to be retrieved
        :param num_values: number of values included in scenario datasets
        :return:
        """

        # establish connection and target scenario data
        engine = create_engine(self.db_name)
        conn = engine.connect()
        #cursor = conn.cursor()

        #testing for column names
        string_query = 'SELECT * from ' + self.db_table
        logging.info(string_query)
        result1 = conn.execute(string_query)
        col_names = result1.keys()
        logging.info(col_names)

        result = conn.execute("SELECT " + scenario + " from " + self.db_table)

        data = pd.Series(np.zeros(num_values))
        for i, row in enumerate(result):
            try:
                temp = float(row[0])
                data[i] = temp.real
            except:
                data[i] = 'nan'  # fill in empty elements (for later filtering)
        conn.close()
        return data

    def calc_avg_dep_foa(self, integration_result, integration_distance):
        """
        :description calculation of average deposition over width of water body
        :param integration_result result of integration of deposition curve across the distance
        :                         beginning at the near distance and extending to the far distance of the water body
        :param integration_distance effectively the width of the water body
        :param avg_dep_foa  average deposition rate across the width of the water body
        :return:
        """

        avg_dep_foa = integration_result / integration_distance
        return avg_dep_foa

    def calc_avg_dep_lbac(self, avg_dep_foa, application_rate):
        """
        Deposition calculation.
        :param avg_dep_foa: average deposition over width of water body as fraction of applied
        :param application_rate: actual application rate
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :return:
        """

        avg_dep_lbac = avg_dep_foa * application_rate
        return avg_dep_lbac

    def calc_avg_dep_foa_from_lbac(self, avg_dep_lbac, application_rate):
        """
        Deposition calculation.
        :param avg_dep_foa: average deposition over width of water body as fraction of applied
        :param application_rate: actual application rate
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :return:
        """

        avg_dep_foa = avg_dep_lbac / application_rate
        return avg_dep_foa

    def calc_avg_dep_gha (self, avg_dep_lbac):
        """
        :description average deposition over width of water body in grams per acre
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param acres_per_hectare: conversion factor to convert acres to hectares
        :return:
        """

        avg_dep_gha = avg_dep_lbac * self.gms_per_lb * self.acres_per_hectare
        return avg_dep_gha

    def calc_avg_dep_lbac_from_gha(self, avg_dep_gha):
        """
        :description average deposition over width of water body in pounds per acre
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param acres_per_hectare: conversion factor to convert acres to hectares
        :return:
        """

        avg_dep_lbac = avg_dep_gha / (self.gms_per_lb * self.acres_per_hectare)
        return avg_dep_lbac

    def calc_avg_waterconc_ngl(self, avg_dep_lbac , area_width, area_length, area_depth):
        """
        :description calculate the average concentration of pesticide in the pond/wetland
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param area_width: average width of water body
        :parem area_length: average length of water body
        :param area_depth: average depth of water body
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param ng_per_gram conversion factor
        :param sqft_per_acre conversion factor
        :param liters_per_ft3 conversion factor
        :return:
        """

        #this expression could be shortened but is left in this form to allow easier interpretation
        avg_waterconc_ngl = ((avg_dep_lbac * self.gms_per_lb * self.ng_per_gram) * \
                            (area_width * area_length / self.sqft_per_acre)) / \
                            (area_width * area_length * area_depth * self.liters_per_ft3)
        return avg_waterconc_ngl

    def calc_avg_dep_lbac_from_waterconc_ngl(self, avg_waterconc_ngl, area_width, area_length, area_depth):
        """
        :description calculate the average deposition onto the pond/wetland/field
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param area_width: average width of water body
        :parem area_length: average length of water body
        :param area_depth: average depth of water body
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param ng_per_gram conversion factor
        :param sqft_per_acre conversion factor
        :param liters_per_ft3 conversion factor
        :return:
        """

        #this expression could be shortened but is left in this form to allow easier interpretation
        avg_dep_lbac =  (avg_waterconc_ngl * self.liters_per_ft3) * (area_width * area_length * area_depth) /  \
                        (area_width * area_length / self.sqft_per_acre) / (self.gms_per_lb * self.ng_per_gram)

        return avg_dep_lbac

    def calc_avg_fielddep_mgcm(self, avg_dep_lbac):
        """
        :description calculate the average deposition of pesticide over the terrestrial field
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param area_depth: average depth of water body
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param mg_per_gram conversion factor
        :param sqft_per_acre conversion factor
        :param cm2_per_ft2 conversion factor
        :return:
        """

        avg_fielddep_mgcm = ((avg_dep_lbac * self.gms_per_lb *
                          self.mg_per_gram) / (self.sqft_per_acre * self.cm2_per_ft2))
        return avg_fielddep_mgcm

    def calc_avg_dep_lbac_from_mgcm(self, avg_fielddep_mgcm):
        """
        :description calculate the average deposition of pesticide over the terrestrial field
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param area_depth: average depth of water body
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param mg_per_gram conversion factor
        :param sqft_per_acre conversion factor
        :param cm2_per_ft2 conversion factor
        :return:
        """

        avg_dep_lbac = (avg_fielddep_mgcm * (self.sqft_per_acre * self.cm2_per_ft2)) / (self.gms_per_lb * self.mg_per_gram)
        return avg_dep_lbac


    def generate_running_avg(self, npts_orig, x_array_in, y_array_in, x_dist):
        """
        :description this method takes an x/y array and creates a x_out/y_out array of running weighted averages;
                     the algorithm mimics the AGAVE.FOR routine created by OPP and found in the collection of
                     software delivered from OPP related to AGDRIFT; this routine is not used here  because it is
                     computationally inefficient; it was produced here simply to provide a check on the new
                     routine found in "create_integration_avg"
        :param npts_orig: number of points in orginal x vs y data points
        :param x_array_in: x values of original x vs y data points
        :param y_array_in: y values of original x vs y data points (assumed to apply from x(i) to x(i+1))
        :param x_dist: length (in x units) for which running weighted average is to be calculated
        :param x_array_out: x values of running weighted average output
        :param y_array_out: y values of running weighted average output
        :param npts_out: number of points in running weighted average output array
        :NOTE We assume we have a monotonically increasing/decreasing y_array; linearity between points;
              x(i) can be non-uniformly spaced; the unning averages are calculated for each x[i] (thus, large gaps in
              in x values (e.g, greater than x_dist) may skew results
        :return:
        """

        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        for i in range (npts_orig-1): #calculate running average for these points
            continuing = True
            if(x_array_in[i] < (x_array_in[npts_orig-1] - x_dist)):
                 j = i
                 #calculate area under curve for this increment of x (assuming linearity of y between x points)
                 cum_area =  (0.5 * (y_array_in[j] + y_array_in[j+1])) * (x_array_in[j+1] - x_array_in[j])

                    #if x_dist is completely within this x[i] to x[i+1] segment then interpolate the one needed value of cum_area
                 if (x_array_in[j+1] > (x_array_in[i] + x_dist)):
                     x_interp = x_array_in[i] + x_dist
                     y_interp = (y_array_in[j] * (x_array_in[j + 1] - x_interp) +
                                 y_array_in[j + 1] * (x_interp - x_array_in[j])) / (x_array_in[j + 1] - x_array_in[j])
                     cum_area = (0.5 * (y_interp + y_array_in[j])) * (x_interp - x_array_in[j])
                     continuing = False
 
                 #if x_dist extends beyond x[i+1], i.e., next x value; then calculate and accumulate all necessary cum_area
                 while continuing:
                    j += 1
                    if (x_array_in[j+1] < (x_array_in[i] + x_dist)):
                        cum_area = cum_area + (0.5 * (y_array_in[j] + y_array_in[j+1])) * (x_array_in[j+1] - x_array_in[j])
                    else:
                        x_interp = x_array_in[i] + x_dist
                        y_interp = (y_array_in[j] * (x_array_in[j+1] - x_interp) +
                                    y_array_in[j+1] * (x_interp - x_array_in[j])) / (x_array_in[j+1] - x_array_in[j])
                        cum_area = cum_area + (0.5 * (y_interp + y_array_in[j])) * (x_interp - x_array_in[j])

                        continuing = False
                 x_array_out[i] = x_array_in[i]
                 y_array_out[i] = cum_area / x_dist
                 npts_out = len(x_array_out)

        return x_array_out, y_array_out, npts_out

    def create_integration_avg(self, npts_orig, x_array_in, y_array_in, x_dist, integrated_avg):
        """
        :description this algorithm searches through a series of x/y values to locate a specified integrated average
        :            integrated averages are processed for each x[] from x[0] until the integrated average matches that
        :            specified in the input; for example, say you have a time series of daily water concentrations and you're
        :            interested in when the 7-day integrated average exceeds a user specified value; this algorithm
        :            would start at day 1, compute the 7-day integrated average (which would simpily be the 7-day average
        :            if the the x points are evenly spaced, i.e., every day), it would then check the 7-day average against
        :            the specified integrated average and if no match it would move to subsequent days and repeat the process
        :            until it finds the integrated average of interest
        :            integrated average (which represents a value of the running average of interest to the user
        :param npts_orig: number of points in orginal x vs y data points
        :param x_array_in: x values of original x vs y data points
        :param y_array_in: y values of original x vs y data points
        :param x_dist: length (in x units) for which running weighted average is to be calculated
        :param integrated_avg: weighted average of y_array_in over x_dist
        :param x_array_out: x values of running weighted average output
        :param y_array_out: y values of running weighted average output
        :param npts_out: number of points in running weighted average output array
        :param x_dist_of_interest: x location of trailing edge of x_dist for which the specified integrated_avg applies
        :NOTE We assume we have a monotonically decreasing y_array
        :NOTE This code could use better documentation; there are multiple indices in use and it is not
              easy to follow at this point
              segment: distance (in x-axis units) associated with length of running weighted average (e.g., 7-day averaging)
              increment: step (x-asix distance between x_array_in points) included in calculation of segment weighted average
        :return:
        """

        x_array_out = pd.Series([], dtype='float') #array of x pts associated with y_array_out
        y_array_out = pd.Series([], dtype='float') #array of running weighted averages
        range_chk = 'in range'  #for reporting when user specified integrated average is not found within the data series
        continuing = True
        x_tot = 0   #total x-axis distance from start point of current averaging
        j_init = 0 #initial x[] of current averaging
        for i in range (npts_orig-1): #calculate running weighted average for these points
            if(x_array_in[i] < (x_array_in[npts_orig-1] - x_dist)):
                if (i == 0):   #first time through process full extent of x_dist (i.e., all x_array_in pts included in x dist)
                    j = 0
                    integrated_tot = 0

                    while continuing:
                        x_tot = x_array_in[j+1]  #because this is the first segment we can simply use the x_array_in
                                                 #points to represent total distance along x-axis
                        integrated_inc = (0.5 * (y_array_in[j] + y_array_in[j+1])) * (x_array_in[j+1] - x_array_in[j])
                        if(j == 0): init_inc = integrated_inc  #save first segment integrated increment

                        if (x_tot <= x_dist):
                            integrated_tot = integrated_tot + integrated_inc
                            j += 1
                        else:  #last segment
                            x_dist_frac = ((x_dist - x_array_in[j]) / (x_array_in[j+1] - x_array_in[j]))
                            integrated_inc = integrated_inc * x_dist_frac
                            if (j == 0): #save last increment?
                                last_inc = 0.  #don't double count if last increment is same as 1st for this segment
                            else:
                                last_inc = integrated_inc
                            integrated_tot = integrated_tot + integrated_inc
                            continuing = False

                    #populate output array that holds values of running integrated averages
                    x_array_out[i] = x_array_in[i]
                    y_array_out[i] = integrated_tot / x_dist
                    npts_out = len(x_array_out)  # not really necessary; at this point it will always be equal to 1

                    #determine if the user specified integrated average has been located
                    if (y_array_in[1] < y_array_in[0]):
                        if (y_array_out[i] < integrated_avg):  #if true then we have achieved the integrated_avg before completing the first x_dist
                            # if we surpass the user supplied integrated_avg before reaching the edge of the first running average then
                            # output the message and set the x_dist_of_interest to zero (as is done in the original AGDRIFT model)
                            print "User-specified integrated average occurs before 1st x_dist extent is completed - x distance of interest set to first x_array_in value"
                            x_dist_of_interest = x_array_in[0]  #original AGDRIFT model sets this value to zero (i.e., first x point value)
                            return x_array_out, y_array_out, npts_out, x_dist_of_interest
                    else:
                        if (y_array_out[i] > integrated_avg):  #if true then we have achieved the integrated_avg before completing the first x_dist
                            # if we surpass the user supplied integrated_avg before reaching the edge of the first running average then
                            # output the message and set the x_dist_of_interest to zero (as is done in the original AGDRIFT model)
                            print "User-specified integrated average occurs before 1st x_dist extent is completed - x distance of interest set to first x_array_in value"
                            x_dist_of_interest = x_array_in[0]  #original AGDRIFT model sets this value to zero (i.e., first x point value)
                            return x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk

                else:  #need to process only edges of running weighted average segment (i.e., subtract 1st and last
                       #increments from previous segment; then start adding new segments)

                    #initialize next segment (i.e., beginning at x[i])
                    if (j == 0 or j == i or j == i-1):  #3 conditions for a new segment without overlap with previous one
                        #new segment has no overlap with previous segment
                        j = j_init = i
                        x_tot = 0.
                        integrated_tot = 0.
                    else:
                        #new segment includes portion of previous segment
                        j_init = j  #j_init is the lower bound of 1st 'new' segment to be processed for this new average
                        x_tot = x_tot - ((x_array_in[j+1] - x_array_in[j]) + (x_array_in[i] - x_array_in[i-1]))
                        integrated_tot = integrated_tot - init_inc - last_inc
                    continuing = True

                    while continuing:
                        x_tot_prev = x_tot
                        x_tot = x_tot + (x_array_in[j+1] - x_array_in[j])
                        integrated_inc = (0.5 * (y_array_in[j] + y_array_in[j+1])) * (x_array_in[j+1] - x_array_in[j])
                        if (j == j_init): init_inc = (0.5 * (y_array_in[i] + y_array_in[i+1])) * \
                                                     (x_array_in[i+1] - x_array_in[i])  #note 'i' index to denote 1st increment of current segment

                        if (x_tot <= x_dist):
                            integrated_tot = integrated_tot + integrated_inc
                            j += 1
                        else:
                            x_dist_frac = (x_dist - x_tot_prev) / (x_array_in[j+1] - x_array_in[j])
                            integrated_inc = integrated_inc * x_dist_frac
                            if (j == i): #save last increment?
                                last_inc = 0. #don't double count if last increment is same as 1st for this segment
                            else:
                                last_inc = integrated_inc
                            integrated_tot = integrated_tot + integrated_inc
                            continuing = False

                    #populate output arrays with latest running weighted average
                    x_array_out[i] = x_array_in[i]
                    y_array_out[i] = integrated_tot / x_dist
                    npts_out = len(x_array_out)

                    #determine if the user supplied integrated average has been surpassed; if so compute the interpolated distance to the point of interest
                    if (y_array_in[1] < y_array_in[0]):  #monotonically decreasing function
                        if (y_array_out[i] <= integrated_avg):
                            fraction = (y_array_out[i-1] - integrated_avg) / (y_array_out[i-1] - y_array_out[i])
                            if(self.find_nearest_x):  #if true then round to nearest half x unit
                                #above is precise x_dist_of_interest; below is OPP protocol for rounding the distance up to the nearest segment midpoint or segment boundary
                                if (fraction >= 0.5):
                                    x_dist_of_interest = x_array_out[i]
                                else:
                                    x_dist_of_interest = x_array_out[i-1] + 0.5 * (x_array_out[i] - x_array_out[i-1])
                            else:
                                x_dist_of_interest = x_array_out[i-1] + fraction * (x_array_out[i] - x_array_out[i-1])
                            #write output arrays to excel file  --  just for debugging
                            #self.write_arrays_to_csv(x_array_out, y_array_out, "output_array.csv")
                            return x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk

                    else:
                        #this increasing function does not naviagate to the nearest 1/2 x point as done above for decreasing function
                        if (y_array_out[i] > integrated_avg):
                            fraction = (integrated_avg - y_array_out[i-1]) / (y_array_out[i] - y_array_out[i-1])
                            x_dist_of_interest = x_array_out[i-1] + fraction * (x_array_out[i] - x_array_out[i-1])
                            return x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk

                        # #the following code (except the return statement) should be removed and placed in a separate methods
                    #
                    # #the following code represents OPP protocol to round up x_dist_of_interest to nearest x midpoint or boundary value
                    # #(except when x_dist_of_interest is in the range of the first 2 meters (i.e., 6.5616 ft)
                    # if (fraction <= 0.5 and x_dist_of_interest > 3.2808):
                    #     round_up_x_dist = 0.5 * (x_array_out[i] + x_array_out[i-1])
                    # elif (fraction > 0.5 and x_dist_of_interest > 3.2808):
                    #     round_up_x_dist = x_array_out[i]
                    # else:
                    #     round_up_x_dist = 3.2808
                    # if (x_dist_of_interest > 3.2808 and x_dist_of_interest < 6.5616):
                    #     round_up_x_dist = 6.5616
                    #return x_array_out, y_array_out, npts_out, round_up_x_dist

        #some extent of the area-of-interest (e.g., pond) lies outside the data range
        range_chk = 'out of range'
        return x_array_out, y_array_out, npts_out, 'NaN', range_chk

    def find_dep_pt_location(self, x_in, y_in, npts, foa):
        """
        :description this method locates the downwind distance associated with a specific deposition rate
        :param x_in: array of distance values
        :param y_in: array of deposition values
        :param npts: number of values in x/y arrays
        :param foa: value of deposition (y value) of interest
        :return:
        """
        range_chk = 'in range'
        continuing = True
        j = 0
        while continuing:
            if (j == 0 and y_in[j] < foa): #means we're in the spray area and not 'downwind'
                out_dist = 0.
            elif (j > npts): #means we are beyond the data range
                range_chk = 'out of range'
            else:
                if (y_in[j] < foa):
                    fraction = (y_in[j-1] - foa) / (y_in[j-1] - y_in[j])
                    out_dist = x_in[j-1] + fraction * (x_in[j] - x_in[j-1])

                    # the following code represents OPP protocol to round up x_dist_of_interest to nearest x midpoint or boundary value
                    # (except when x_dist_of_interest is in the range of the first 2 meters (i.e., 6.5616 ft)
                    if (fraction <= 0.5 and out_dist > 3.2808):
                        round_up_x_dist = 0.5 * (x_in[j] + x_in[j-1])
                    elif (fraction > 0.5 and out_dist > 3.2808):
                        round_up_x_dist = x_in[j]
                    else:
                        round_up_x_dist = 3.2808
                    if (out_dist > 3.2808 and out_dist < 6.5616):
                        round_up_x_dist = 6.5616
                    out_dist = round_up_x_dist  # i is simulation number
                    continuing = False
                j += 1
        return out_dist, range_chk

    def round_model_outputs(self, avg_dep_foa, avg_dep_lbac, avg_dep_gha, avg_waterconc_ngl,
                                     avg_field_dep_mgcm, i):
        """
        :description round output variable values (and place in output variable series) so that they can be directly
                     compared to expected results (which were limited in terms of their output format from the OPP AGDRIFT
                     model (V2.1.1) interface (we don't have the AGDRIFT code so we cannot change the output format to
                    agree with this model
        :param avg_dep_foa:
        :param avg_dep_lbac:
        :param avg_dep_gha:
        :param avg_waterconc_ngl:
        :param avg_field_dep_mgcm:
        :param i: simulation number
        :return:
        """

        if (np.isfinite(avg_dep_foa)):
            if (avg_dep_foa > 1e-4 and avg_dep_foa < 1.):
                self.out_avg_dep_foa[i] = round(avg_dep_foa, 4)
            elif (avg_dep_foa > 1.):
                self.out_avg_dep_foa[i] = round(avg_dep_foa, 2)
            else :
                self.out_avg_dep_foa[i] = float('{:0.2e}'.format(float(avg_dep_foa)))
        else:
            self.out_avg_dep_foa[i] = avg_dep_foa

        if (np.isfinite(avg_dep_lbac)):
            if (avg_dep_lbac > 1e-4 and avg_dep_lbac < 1.):
                self.out_avg_dep_lbac[i] = round(avg_dep_lbac, 4)
            elif (avg_dep_lbac > 1.):
                self.out_avg_dep_lbac[i] = round(avg_dep_lbac, 2)
            else :
                self.out_avg_dep_lbac[i] = float('{:0.2e}'.format(float(avg_dep_lbac)))
        else:
            self.out_avg_dep_lbac[i] = avg_dep_lbac

        if (np.isfinite(avg_dep_gha)):
            if (avg_dep_gha > 1e-4 and avg_dep_gha < 1.):
                self.out_avg_dep_gha[i] = round(avg_dep_gha, 4)
            elif (avg_dep_gha > 1.):
                self.out_avg_dep_gha[i] = round(avg_dep_gha, 2)
            else :
                self.out_avg_dep_gha[i] = float('{:0.2e}'.format(float(avg_dep_gha)))
        else:
            self.out_avg_dep_gha[i] = avg_dep_gha

        if (np.isfinite(avg_waterconc_ngl)):
            if (avg_waterconc_ngl > 1e-4 and avg_waterconc_ngl < 1.):
                self.out_avg_waterconc_ngl[i] = round(avg_waterconc_ngl, 4)
            elif (avg_waterconc_ngl > 1.):
                self.out_avg_waterconc_ngl[i] = round(avg_waterconc_ngl, 2)
            else :
                self.out_avg_waterconc_ngl[i] = float('{:0.2e}'.format(float(avg_waterconc_ngl)))
        else:
            self.out_avg_waterconc_ngl[i] = avg_waterconc_ngl

        if(np.isfinite(avg_field_dep_mgcm)):
            if (avg_field_dep_mgcm > 1e-4 and avg_field_dep_mgcm < 1.):
                self.out_avg_field_dep_mgcm[i] = round(avg_field_dep_mgcm, 4)
            elif (avg_field_dep_mgcm > 1.):
                self.out_avg_field_dep_mgcm[i] = round(avg_field_dep_mgcm, 2)
            else:
                self.out_avg_field_dep_mgcm[i] = float('{:0.2e}'.format(float(avg_field_dep_mgcm)))
        else:
            self.out_avg_field_dep_mgcm[i] = avg_field_dep_mgcm
        return

    def write_data_to_csv(self, scenario_index):

        #just a quick method to help debugging
        #write distance and deposition data to csv file
        x_in = pd.Series([], dtype='float')
        y_in = pd.Series([], dtype='float')

        x_in = self.scenario_distance_data[scenario_index]
        y_in = self.scenario_deposition_data[scenario_index]

        with open("dist_dep.csv", 'wb') as output_file:
            wr = csv.writer(output_file, dialect='excel')
            for k in range(len(x_in)):
                item1 = x_in[k]
                item2 = y_in[k]
                wr.writerow([item1,item2],)
        output_file.close()
        return

    def write_arrays_to_csv(self, x_in, y_in, db_name):

        # just a quick method to help debugging

        with open(db_name, 'wb') as output_file:
            wr = csv.writer(output_file, dialect='excel')
            for k in range(len(x_in)):
                item1 = x_in[k]
                item2 = y_in[k]
                wr.writerow([item1, item2], )
        output_file.close()
        return

                # def deposition_gha_to_ngl_f(self):
    #     """
    #     Deposition calculation.
    #     :param out_init_avg_dep_foa:
    #     :param application_rate:
    #     :return:
    #     """
    #     if (self.aquatic_type == '1'):
    #         self.out_deposition_gha_ngl_f = [self.out_avg_depo_gha * 0.05 * 1000.0]
    #     else:
    #         self.out_deposition_ngl_f = [self.out_avg_depo_gha * 0.05 * 1000.0 * (6.56 / 0.4921)]
    #     return self.out_deposition_gha_ngl_f
    #
    # def deposition_gha_to_mgcm_f(self):
    #     """
    #     Deposition calculation.
    #     :param out_init_avg_dep_foa:
    #     :param application_rate:
    #     :return:
    #     """
    #     self.out_deposition_mgcm = [self.out_avg_depo_gha * 0.00001]
    #     return self.out_deposition_mgcm

        # def deposition_lbac_to_foa_f(self):
        #     """
        #     Deposition calculation.
        #     :param out_init_avg_dep_foa:
        #     :param application_rate:
        #     :return:
        #     """
        #     # self.application_rate = float(self.application_rate)
        #     self.out_init_avg_dep_foa = [self.out_avg_depo_lbac[0] / self.application_rate[0]]
        #     return self.out_init_avg_dep_foa


        # def deposition_lbac_to_gha_f(self):
        #     """
        #     Deposition calculation.
        #     :param out_init_avg_dep_foa:
        #     :param application_rate:
        #     :return:
        #     """
        #     # self.out_avg_depo_lbac = float(self.out_avg_depo_lbac)
        #     self.out_avg_depo_gha = [(self.out_avg_depo_lbac[0] * 453.592) / 0.404686]
        #     # logging.info self.out_avg_depo_gha
        #     return self.out_avg_depo_gha

    # def tier_I_aerial(self, i):
    #     logging.info(
    #         '------------- Agdrift results' + self.aquatic_type[0] + self.application_method[0] + self.drop_size[0])
    # 
    #     # TIER I AERIAL
    #     # if self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Aerial' and self.drop_size[i] == 'Fine':
    #     if self.aquatic_type[i] == 'EPA Defined Pond' and self.application_method[i] == 'Tier I Aerial' and \
    #                     self.drop_size[i] == 'Very Fine to Fine':
    #         self.out_y.loc[i] = [self.pond_aerial_vf2f]
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae[i] = [0]
    #         self.out_express_y[i] = [self.pond_aerial_vf2f]
    #         self.out_x[i] = self.out_x
    #     # TIER I AERIAL
    #     # elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Aerial' and self.drop_size[i] == 'Medium'):
    #     elif (self.aquatic_type[i] == 'EPA Defined Pond' and self.application_method[i] == 'Tier I Aerial' and
    #                   self.drop_size[i] == 'Fine to Medium'):
    #         self.out_y.loc[i] = [self.pond_aerial_f2m]
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae.loc[i] = [1]
    #         self.out_express_y.loc[i] = [self.pond_aerial_f2m]
    #         self.out_x[i] = self.out_x
    #     # TIER I AERIAL
    #     # elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Aerial' and self.drop_size[i] == 'Coarse'):
    #     elif (self.aquatic_type[i] == 'EPA Defined Pond' and self.application_method[i] == 'Tier I Aerial' and
    #                   self.drop_size[i] == 'Medium to Coarse'):
    #         self.out_y.loc[i] = [self.pond_aerial_m2c]
    #         self.out_nasae.loc[i] = [2]
    #         self.out_express_y.loc[i] = [self.pond_aerial_m2c]
    #         self.out_x[i] = self.out_x
    #     # TIER I AERIAL
    #     # elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Tier I Aerial' and self.drop_size[i] == 'Very Coarse'):
    #     elif (self.aquatic_type[i] == 'EPA Defined Pond' and self.application_method[i] == 'Tier I Aerial' and
    #                   self.drop_size[i] == 'Coarse to Very Coarse'):
    #         self.out_y.loc[i] = [self.pond_aerial_c2vc]
    #         # python 3 = list(map(str,self.pond_aerial_c2vc))
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae.loc[i] = [3]
    #         self.out_express_y.loc[i] = [self.pond_aerial_c2vc]
    #         # self.out_x[i] = self.out_x
    #         self.out_x.loc[i] = self.out_x_temp
    #     else:
    #         self.out_y.loc[i] = [3]
    # 
    # def tier_I_ground(self, i):
    #     logging.info(
    #         '------------- Agdrift results' + self.ecosystem_type[0] + self.application_method[0] + self.drop_size[0] +
    #         self.boom_height[0])
    # 
    #     # TIER I GROUND
    #     if (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Ground' and self.drop_size[
    #         i] == 'Fine' and self.boom_height[i] == 'low'):
    #         self.out_y[i] = [self.pond_ground_low_vf2f]
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae[i] = [4]
    #         self.out_express_y[i] = [self.pond_ground_low_vf2f]
    #         self.out_x[i] = self.out_x
    #     # TIER I GROUND
    #     elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Ground' and self.drop_size[
    #         i] == 'Medium' and self.boom_height[i] == 'low'):
    #         self.out_y[i] = [self.pond_ground_low_f2m]
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae[i] = [6]
    #         self.out_express_y[i] = [self.pond_ground_low_f2m]
    #         self.out_x[i] = self.out_x
    #     # TIER I GROUND
    #     elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Ground' and
    #                   self.drop_size[i] == 'Fine' and self.boom_height[i] == 'High'):
    #         self.out_y[i] = [self.pond_ground_high_vf2f]  # ??
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae[i] = [5]
    #         self.out_express_y[i] = [self.pond_ground_high_vf2f]
    #         self.out_x[i] = self.out_x
    #     # TIER I GROUND
    #     elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Ground' and self.drop_size[
    #         i] == 'Medium' and self.boom_height[i] == 'High'):
    #         self.out_y[i] = [self.pond_ground_high_f2m]
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae[i] = [7]
    #         self.out_express_y[i] = [self.pond_ground_high_f2m]
    #         self.out_x[i] = self.out_x
    # 
    # # TIER I ORCHARD/AIRBLAST
    # def tier_I_airblast(self, i):
    #     logging.info(
    #         '------------- Agdrift results' + self.ecosystem_type[0] + self.application_method[0] + self.airblast_type[0])
    # 
    #     if (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Orchard/Airblast' and
    #                 self.airblast_type[i] == 'Orchard'):
    #         self.out_y[i] = [self.pond_airblast_orchard]
    #         # self.out_x[0] = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
    #         self.out_nasae[i] = [9]
    #         self.out_express_y[i] = [self.pond_airblast_orchard]
    #         self.out_x[i] = self.out_x
    # 
    #     # TIER I ORCHARD/AIRBLAST
    #     elif (self.ecosystem_type[i] == 'EPA Pond' and self.application_method[i] == 'Orchard/Airblast' and
    #                   self.airblast_type[i] == 'Vineyard'):
    #         self.out_y[i] = [self.pond_airblast_vineyard]
    #         self.out_express_y[i] = [self.pond_airblast_vineyard]
    #         self.out_x[i] = self.out_x
    #         self.out_nasae[i] = [8]
    #     else:
    #         self.out_y[i] = [3]

    # def express_extrapolate_f(self):
    #     """
    #     Extrapolate results from express implementation.
    #     :param out_y:
    #     :param out_nasae:
    #     :param distance:
    #     :return:
    #     """
    #     # XV = np.array([X0, X1, X2, X3, X4, X5, X6, X7, X8, X9])
    #
    #     # NASAE1=int(self.out_nasae[0])-1
    #     # N=max(0,min(9,(self.out_nasae[0]-1)))
    #     # I=max(0,min(99,int(0.5*int(self.distance[0]))+1))
    #     i_f = max(1, min(100, int(0.5 * int(self.distance)) + 1))
    #     ym = 2.0 * (i_f - 1)
    #     yp = 2.0 * i_f
    #     i = i_f - 1  # to account for python being zero based
    #
    #     self.out_init_avg_dep_foa = [(0.5 * (self.out_y[i] * (yp - int(self.distance)) + self.out_y[i + 1] *
    #                                          (int(self.distance) - ym))) / 100]
    #     return self.out_init_avg_dep_foa

    # def extrapolate_from_fig(self, bisect_left, out_x):
    #     """
    #     Extrapolating from nearest figure points.
    #     :param ecosystem_type:
    #     :param distance:
    #     :param bisect_left:
    #     :param out_x:
    #     :param out_y:
    #     :return:
    #     """
    #     #self.distance = int(self.distance)
    #     if self.distance[0] in self.out_x:
    #         y_index = out_x.index(self.distance[0])
    #         self.out_init_avg_dep_foa = [self.out_y[y_index]]
    #     else:
    #         i = bisect_left(self.out_x, self.distance[0])  # find largest distance closest to value
    #         low1 = self.out_x[0][i - 1]  # assign nearest lowest out_x value for interpolation
    #         high1 = self.out_x[0][i]  # assign nearest highest out_x value for interpolation
    #         low_i = i - 1  # assign index values to use to find nearest out_y values for interpolation
    #         high_i = i  # assign index values to use to find nearest out_y values for interpolation
    #         self.out_init_avg_dep_foa = [((self.distance[0] - low1) * (self.out_y[0][high_i] - self.out_y[0][low_i]) / (high1 - low1)) + \
    #                                 self.out_y[0][low_i]]
    #     return self.out_init_avg_dep_foa

    # def extrapolate_from_fig2(self, out_y):
    #     """
    #     Extrapolating from nearest figure points, alternative figure.
    #     :param ecosystem_type:
    #     :param out_init_avg_dep_foa:
    #     :param bisect_left:
    #     :param out_x:
    #     :param out_y:
    #     :return:
    #     """
    #     #self.out_init_avg_dep_foa = float(self.out_init_avg_dep_foa)
    #     if self.out_init_avg_dep_foa in self.out_y:
    #         x_index = out_y.index(self.out_init_avg_dep_foa[0])
    #         self.distance[0] = self.out_x[x_index]
    #     else:
    #         i = min(enumerate(self.out_y), key=lambda out_x: abs(
    #                 out_x[1] - self.out_init_avg_dep_foa))  # finds smallest closest value closest to input value
    #         i2 = i[0]
    #         low1 = self.out_y[i2]  # assign nearest lowest out_x value for interpolation
    #         high1 = self.out_y[i2 - 1]  # assign nearest highest out_x value for interpolation
    #         low_i = i2  # assign index values to use to find nearest out_y values for interpolation
    #         high_i = i2 - 1  # assign index values to use to find nearest out_y values for interpolation
    #         self.distance[0] = ((self.out_init_avg_dep_foa[0] - low1) * (self.out_x[high_i] - self.out_x[low_i]) / (high1 - low1)) + \
    #                         self.out_x[low_i]
    #     return self.distance

    # def deposition_foa_to_gha_f(self):
    #     """
    #     Deposition calculation.
    #     :param out_init_avg_dep_foa:
    #     :param application_rate:
    #     :return:
    #     """
    #     self.out_avg_depo_gha = [self.out_init_avg_dep_foa * 100.0 * self.application_rate * 10.0]
    #     return self.out_avg_depo_gha

    # def deposition_ngl_2_gha_f(self):
    #     """
    #     Deposition calculation.
    #     :param out_init_avg_dep_foa:
    #     :param application_rate:
    #     :return:
    #     """
    #     # self.out_deposition_ngl = float(self.out_deposition_ngl)
    #     if (self.aquatic_type == '1'):
    #         self.deposition_ngl_2_gha_f = [self.out_deposition_ngl[0] / (0.05 * 1000)]
    #     else:
    #         self.deposition_ngl_2_gha_f = [((self.out_deposition_ngl[0] / 6.56) * 0.4921) / (0.05 * 1000)]
    #     return self.deposition_ngl_2_gha_f

    # def deposition_ghac_to_lbac_f(self):
    #     """
    #     Deposition calculation.
    #     :param out_init_avg_dep_foa:
    #     :param application_rate:
    #     :return:
    #     """
    #     # self.out_avg_depo_gha = float(self.out_avg_depo_gha)
    #     self.out_avg_depo_lbac = [(self.out_avg_depo_gha[0] * 0.00220462 / 2.47105)]
    #     return self.out_avg_depo_lbac

    # def deposition_mgcm_to_gha_f(self):
    #     """
    #     Deposition calculation.
    #     :param out_init_avg_dep_foa:
    #     :param application_rate:
    #     :return:
    #     """
    #     # self.out_deposition_mgcm = float(self.out_deposition_mgcm)
    #     self.out_avg_depo_gha = [self.out_deposition_mgcm[0] / 0.00001]
    #     return self.out_avg_depo_gha


        # elif (self.calculation_input == 'Fraction'):
        #     self.extrapolate_from_fig2(self.out_y)
        #     self.deposition_foa_to_lbac_f()
        #     self.deposition_lbac_to_gha_f()
        #     self.deposition_gha_to_ngl_f()
        #     self.deposition_gha_to_mgcm_f()

        # elif (self.calculation_input == 'Initial Average Deposition (g/ha)'):
        #     self.deposition_ghac_to_lbac_f()
        #     self.deposition_lbac_to_foa_f()
        #     self.extrapolate_from_fig2(self.out_y)
        #     self.deposition_gha_to_ngl_f()
        #     self.deposition_gha_to_mgcm_f()

        # elif (self.  == 'Initial Average Deposition (lb/ac)'):
        #     logging.info self.out_avg_depo_lbac
        #     self.deposition_lbac_to_gha_f()
        #     self.deposition_gha_to_ngl_f()
        #     self.deposition_gha_to_mgcm_f()
        #     self.deposition_lbac_to_foa_f()
        #     self.extrapolate_from_fig2(self.out_y)

        # elif (self.calculation_input == 'Initial Average Concentration (ng/l)'):
        #     self.deposition_ngl_2_gha_f()
        #     self.deposition_ghac_to_lbac_f()
        #     self.deposition_lbac_to_foa_f()
        #     self.extrapolate_from_fig2(self.out_y)
        #     self.deposition_gha_to_mgcm_f()

        # else:
        #     self.deposition_mgcm_to_gha_f()
        #     self.deposition_ghac_to_lbac_f()
        #     self.deposition_lbac_to_foa_f()
        #     self.extrapolate_from_fig2(self.out_y)
        #     self.deposition_gha_to_ngl_f()

        # def results(self):
        #     self.pond_ground_high_vf2f = [0.0616,0.0572,0.0455,0.0376,0.0267,0.0194,0.013,0.0098,0.0078,0.0064,0.0053,0.0046,0.0039,0.0035,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014,0.0013,0.0012]
        #     self.pond_ground_high_f2m = [0.0165,0.0137,0.0104,0.009,0.0071,0.0056,0.0042,0.0034,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.00095,0.0009,0.0008,0.0008,0.0007,0.0007]
        #     self.pond_ground_low_vf2f = [0.0268,0.0231,0.0167,0.0136,0.01,0.0076,0.0054,0.0043,0.0036,0.0031,0.0027,0.0024,0.0021,0.0019,0.0017,0.0016,0.0015,0.0013,0.0012,0.0012,0.0011,0.001,0.001,0.0009,0.0009]
        #     self.pond_ground_low_f2m = [0.0109,0.0086,0.0065,0.0056,0.0045,0.0036,0.0028,0.0023,0.0019,0.0017,0.0015,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008,0.0007,0.0007,0.0006,0.0006,0.0006,0.0006]

        # #####one less value (begin)
        #     self.pond_aerial_vf2f = [0.2425,0.2409,0.2344,0.2271,0.2083,0.1829,0.1455,0.1204,0.103,0.0904,0.0809,0.0734,0.0674,0.0625,0.0584,0.055,0.0521,0.0497,0.0476,0.0458,0.0442,0.0428,0.0416,0.0405,0.0396]
        #     self.pond_aerial_f2m = [0.1266,0.1247,0.1172,0.1094,0.0926,0.0743,0.0511,0.0392,0.0321,0.0272,0.0238,0.0212,0.0193,0.0177,0.0165,0.0155,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117,0.0114,0.0111]
        #     self.pond_aerial_m2c = [0.0892,0.0900,0.0800,0.0700,0.0600,0.0400,0.0300,0.0200,0.0200,0.0130,0.0112,0.0099,0.0090,0.0083,0.0077,0.0073,0.0069,0.0066,0.0063,0.0060,0.0058,0.0056,0.0055,0.0053,0.0052]
        #     self.pond_aerial_c2vc = [0.0892,0.0900,0.0800,0.0700,0.0600,0.0400,0.0300,0.0200,0.0200,0.0130,0.0112,0.0099,0.0090,0.0083,0.0077,0.0073,0.0069,0.0066,0.0063,0.0060,0.0058,0.0056,0.0055,0.0053,0.0052]
        #     self.terr_aerial_vf2f = [0.5000,0.4913,0.4564,0.4220,0.3588,0.3039,0.2247,0.1741,0.1403,0.1171,0.1010,0.0893,0.0799,0.0729,0.0671,0.0626,0.0585,0.0550,0.0519,0.0494,0.0475,0.0458,0.0442,0.0428,0.0416]
        #     self.terr_aerial_f2m = [0.4999,0.4808,0.4046,0.3365,0.2231,0.1712,0.0979,0.0638,0.0469,0.0374,0.0312,0.0266,0.0234,0.021,0.0192,0.0177,0.0164,0.0154,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117]
        #     self.terr_aerial_m2c =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
        #     self.terr_aerial_c2vc =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
        #     self.terr_ground_vf2f = [1.06,0.8564,0.4475,0.2595,0.104,0.05,0.0248,0.0164,0.012,0.0093,0.0075,0.0062,0.0053,0.0045,0.0039,0.0034,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014]
        # #####one less value (end)

        #     self.terr_ground_f2m = [1.01,0.3731,0.0889,0.0459,0.0208,0.0119,0.007,0.0051,0.004,0.0033,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008]
        #     self.pond_airblast_normal = [0.0011,0.0011,0.001,0.0009,0.0007,0.0005,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000978,0.0000863,0.0000769,0.0000629,0.0000626,0.0000571,0.0000523,0.0000482,0.0000446,0.0000414,0.0000386,0.0000361,0.0000339]
        #     self.pond_airblast_dense = [0.0145,0.014,0.0122,0.0106,0.0074,0.005,0.003,0.0022,0.0017,0.0014,0.0012,0.0011,0.001,0.0009,0.0008,0.0007,0.0007,0.0006,0.0006,0.0005,0.0005,0.0005,0.0005,0.0004,0.0004]
        #     self.pond_airblast_sparse = [0.0416,0.0395,0.0323,0.0258,0.015,0.0077,0.0031,0.0017,0.001,0.0007,0.0005,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000898,0.0000771,0.0000668,0.0000583,0.0000513,0.0000453,0.0000405]
        #     self.pond_airblast_vineyard = [0.0024,0.0023,0.0018,0.0014,0.0009,0.0006,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.0000881,0.0000765,0.0000672,0.0000596,0.0000533,0.000048,0.0000435,0.0000397,0.0000363,0.0000334,0.0000309,0.0000286,0.0000267]
        #     self.pond_airblast_orchard = [0.0218,0.0208,0.0175,0.0145,0.0093,0.0056,0.0031,0.0021,0.0016,0.0013,0.0011,0.0009,0.0008,0.0007,0.0007,0.0006,0.0005,0.0005,0.0005,0.0004,0.0004,0.0004,0.0004,0.0003,0.0003]
        #     self.terr_airblast_normal = [0.0089,0.0081,0.0058,0.0042,0.0023,0.0012,0.0006,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000965,0.0000765,0.0000625,0.0000523,0.0000446,0.0000387]
        #     self.terr_airblast_dense = [0.1155,0.1078,0.0834,0.0631,0.033,0.0157,0.0065,0.0038,0.0026,0.002,0.0016,0.0014,0.0012,0.0011,0.0009,0.0008,0.0007,0.0006,0.0005,0.0005]
        #     self.terr_airblast_sparse = [0.4763,0.4385,0.3218,0.2285,0.1007,0.0373,0.0103,0.0044,0.0023,0.0014,0.0009,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001,0.0000889,0.0000665,0.0000514]
        #     self.terr_airblast_vineyard = [0.0376,0.0324,0.0195,0.012,0.0047,0.0019,0.0008,0.0004,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.000087,0.0000667,0.0000531,0.0000434,0.0000363,0.000031]
        #     self.terr_airblast_orchard = [0.2223,0.2046,0.1506,0.108,0.0503,0.021,0.0074,0.004,0.0026,0.0019,0.0015,0.0012,0.0011,0.0009,0.0008,0.0006,0.0005,0.0005,0.0004,0.0004]

        #     if (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
        #         self.out_y = self.pond_aerial_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
        #         self.out_y = self.pond_aerial_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
        #         self.out_y = self.pond_aerial_m2c
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
        #         self.out_y = self.pond_aerial_c2vc
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'low'):
        #         self.out_y = self.pond_ground_low_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'low'):
        #         self.out_y = self.pond_ground_low_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Fine' and self.boom_height == 'High'):
        #         self.out_y = self.pond_ground_high_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Ground' and self.drop_size == 'Medium' and self.boom_height == 'High'):
        #         self.out_y = self.pond_ground_high_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
        #         self.out_y = self.terr_aerial_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
        #         self.out_y = self.terr_aerial_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
        #         self.out_y = self.terr_aerial_m2c
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
        #         self.out_y = self.terr_aerial_c2vc
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Fine'):
        #         self.out_y = self.terr_ground_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Medium'):
        #         self.out_y = self.terr_ground_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Normal'):
        #         self.out_y = self.pond_airblast_normal
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Dense'):
        #         self.out_y = self.pond_airblast_dense
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Sparse'):
        #         self.out_y = self.pond_airblast_sparse
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Vineyard'):
        #         self.out_y = self.pond_airblast_vineyard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Orchard'):
        #         self.out_y = pond_airblast_orchard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Normal'):
        #         self.out_y = self.terr_airblast_normal
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Dense'):
        #         self.out_y = self.terr_airblast_dense
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Sparse'):
        #         self.out_y = self.terr_airblast_sparse
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Vineyard'):
        #         self.out_y = self.terr_airblast_vineyard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Orchard'):
        #         self.out_y = self.terr_airblast_orchard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #         self.z = 4
        #     else:
        #         #logging.info 2
        #         self.out_y = 3
        #     return self.out_x, self.out_y

        #     self.terr_aerial_vf2f = [0.5000,0.4913,0.4564,0.4220,0.3588,0.3039,0.2247,0.1741,0.1403,0.1171,0.1010,0.0893,0.0799,0.0729,0.0671,0.0626,0.0585,0.0550,0.0519,0.0494,0.0475,0.0458,0.0442,0.0428,0.0416]
        #     self.terr_aerial_f2m = [0.4999,0.4808,0.4046,0.3365,0.2231,0.1712,0.0979,0.0638,0.0469,0.0374,0.0312,0.0266,0.0234,0.021,0.0192,0.0177,0.0164,0.0154,0.0146,0.0139,0.0133,0.0128,0.0124,0.012,0.0117]
        #     self.terr_aerial_m2c =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
        #     self.terr_aerial_c2vc =[0.5,0.4776,0.3882,0.3034,0.1711,0.1114,0.0561,0.0346,0.0249,0.0188,0.015,0.0126,0.011,0.0098,0.0089,0.0082,0.0077,0.0072,0.0069,0.0065,0.0063,0.006,0.0058,0.0056,0.0055]
        #     self.terr_ground_vf2f = [1.06,0.8564,0.4475,0.2595,0.104,0.05,0.0248,0.0164,0.012,0.0093,0.0075,0.0062,0.0053,0.0045,0.0039,0.0034,0.003,0.0027,0.0024,0.0022,0.002,0.0018,0.0017,0.0015,0.0014]
        # #####one less value (end)

        #     self.terr_ground_f2m = [1.01,0.3731,0.0889,0.0459,0.0208,0.0119,0.007,0.0051,0.004,0.0033,0.0028,0.0024,0.0021,0.0019,0.0017,0.0015,0.0014,0.0013,0.0012,0.0011,0.001,0.0009,0.0009,0.0008,0.0008]
        #     self.pond_airblast_normal = [0.0011,0.0011,0.001,0.0009,0.0007,0.0005,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000978,0.0000863,0.0000769,0.0000629,0.0000626,0.0000571,0.0000523,0.0000482,0.0000446,0.0000414,0.0000386,0.0000361,0.0000339]
        #     self.pond_airblast_dense = [0.0145,0.014,0.0122,0.0106,0.0074,0.005,0.003,0.0022,0.0017,0.0014,0.0012,0.0011,0.001,0.0009,0.0008,0.0007,0.0007,0.0006,0.0006,0.0005,0.0005,0.0005,0.0005,0.0004,0.0004]

        #     self.pond_airblast_orchard = [0.0218,0.0208,0.0175,0.0145,0.0093,0.0056,0.0031,0.0021,0.0016,0.0013,0.0011,0.0009,0.0008,0.0007,0.0007,0.0006,0.0005,0.0005,0.0005,0.0004,0.0004,0.0004,0.0004,0.0003,0.0003]
        #     self.terr_airblast_normal = [0.0089,0.0081,0.0058,0.0042,0.0023,0.0012,0.0006,0.0004,0.0003,0.0002,0.0002,0.0002,0.0001,0.0001,0.0000965,0.0000765,0.0000625,0.0000523,0.0000446,0.0000387]
        #     self.terr_airblast_dense = [0.1155,0.1078,0.0834,0.0631,0.033,0.0157,0.0065,0.0038,0.0026,0.002,0.0016,0.0014,0.0012,0.0011,0.0009,0.0008,0.0007,0.0006,0.0005,0.0005]
        #     self.terr_airblast_sparse = [0.4763,0.4385,0.3218,0.2285,0.1007,0.0373,0.0103,0.0044,0.0023,0.0014,0.0009,0.0006,0.0005,0.0004,0.0003,0.0002,0.0001,0.0000889,0.0000665,0.0000514]
        #     self.terr_airblast_vineyard = [0.0376,0.0324,0.0195,0.012,0.0047,0.0019,0.0008,0.0004,0.0003,0.0002,0.0002,0.0001,0.0001,0.0001,0.000087,0.0000667,0.0000531,0.0000434,0.0000363,0.000031]
        #     self.terr_airblast_orchard = [0.2223,0.2046,0.1506,0.108,0.0503,0.021,0.0074,0.004,0.0026,0.0019,0.0015,0.0012,0.0011,0.0009,0.0008,0.0006,0.0005,0.0005,0.0004,0.0004]

        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Fine'):
        #         self.out_y = self.terr_aerial_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Medium'):
        #         self.out_y = self.terr_aerial_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Coarse'):
        #         self.out_y = self.terr_aerial_m2c
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Aerial' and self.drop_size == 'Very Coarse'):
        #         self.out_y = self.terr_aerial_c2vc
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Fine'):
        #         self.out_y = self.terr_ground_vf2f
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Ground' and self.drop_size == 'Medium'):
        #         self.out_y = self.terr_ground_f2m
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Normal'):
        #         self.out_y = self.pond_airblast_normal
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Dense'):
        #         self.out_y = self.pond_airblast_dense
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'EPA Pond' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Orchard'):
        #         self.out_y = pond_airblast_orchard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Normal'):
        #         self.out_y = self.terr_airblast_normal
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Dense'):
        #         self.out_y = self.terr_airblast_dense
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Sparse'):
        #         self.out_y = self.terr_airblast_sparse
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Vineyard'):
        #         self.out_y = self.terr_airblast_vineyard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #     elif (self.ecosystem_type == 'Terrestrial' and self.application_method == 'Orchard/Airblast' and self.airblast_type == 'Orchard'):
        #         self.out_y = self.terr_airblast_orchard
        #         self.out_x = [0,1,5,10,25,50,100,150,200,250,300,350,400,450,500,600,700,800,900,997]
        #         self.z = 4

    # def load_pond_ground_high_vf2f(self):
    #     conn = sqlite3.connect('agdrift.db')
    #     cur = conn.cursor()
    #     cur.execute("SELECT pond_ground_high_vf2f  from output")
    #     pond_ground_high_vf2fs = cur.fetchall()
    #     pond_ground_high_vf2fs = np.array(pond_ground_high_vf2fs).astype('float').flatten()
    #     cur.close()
    #     conn.close()
    #     return pond_ground_high_vf2fs


    # def get_distance(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT distance from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_ground_high_vf2f(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_ground_high_vf2f from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_ground_high_f2m(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_ground_high_f2m from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_ground_low_f2m(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_ground_low_f2m from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_ground_low_vf2f(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_ground_low_vf2f from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_aerial_vf2f(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_aerial_vf2f from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_aerial_f2m(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_aerial_f2m from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_aerial_m2c(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_aerial_m2c from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_aerial_c2vc(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_aerial_c2vc from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_airblast_orchard(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_airblast_orchard from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data
    #
    # def get_pond_airblast_vineyard(self):
    #     engine = create_engine('sqlite:///sqlite_agdrift.db')
    #     conn = engine.connect()
    #     result = conn.execute("SELECT pond_airblast_vineyard from output")
    #     data = pd.Series(np.zeros(300))
    #     for i, row in enumerate(result):
    #         temp = float(row[0])
    #         data[i] = temp.real
    #     conn.close()
    #     return data


#-------------------------

        # def get_pond_ground_high_vf2f(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_ground_high_vf from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_ground_high_f2m(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_ground_high_f2m from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_ground_low_f2m(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_ground_low_f2m from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_ground_low_vf2f(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_ground_low_vf2f from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_aerial_vf2f(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_aerial_vf2f from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         try:
        #             temp = float(row[0])
        #             data[i] = temp.real
        #         except:
        #             data[i] = 'nan'
        #     conn.close()
        #     return data
        #
        # def get_pond_aerial_f2m(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_aerial_f2m from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_aerial_m2c(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_aerial_m2c from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_aerial_c2vc(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_aerial_c2vc from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_airblast_orchard(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_airblast_orchard from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data
        #
        # def get_pond_airblast_vineyard(self):
        #     engine = create_engine('sqlite:///sqlite_agdrift_1994ft.db')
        #     conn = engine.connect()
        #     result = conn.execute("SELECT pond_airblast_vineyard from output")
        #     data = pd.Series(np.zeros(161))
        #     for i, row in enumerate(result):
        #         temp = float(row[0])
        #         data[i] = temp.real
        #     conn.close()
        #     return data