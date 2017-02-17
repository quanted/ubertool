from __future__ import division  # brings in Python 3.0 mixed type calculation rules
from functools import wraps
import logging
import numpy as np
import pandas as pd
import time

import sqlite3
from sqlalchemy import Column, Table, Integer, Float, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import *

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
                area_width = self.out_default_width
                area_length = self.out_default_length
                area_depth = self.out_default_pond_depth
            elif (self.aquatic_body_type[i] == 'EPA Defined Wetland'):
                area_width = self.out_default_width
                area_length = self.out_default_length
                area_depth = self.out_default_wetland_depth
            elif (self.aquatic_body_type[i] == 'User Defined Pond'):
                area_width = self.user_pond_width[i]
                area_length = self.sqft_per_hectare / area_width
                area_depth = self.user_pond_depth[i]
            elif (self.aquatic_body_type[i] == 'User Defined Wetland'):
                area_width = self.user_wetland_width[i]
                area_length = self.sqft_per_hectare / area_width
                area_depth = self.user_wetland_depth[i]
        elif (self.ecosystem_type[i] == 'Terrestrial Assessment'):
            if (self.terrestrial_field_type[i] == 'User Defined Terrestrial'):  # implies user to specify an area width
                area_width = self.user_terrestrial_width[i]
                area_length = self.sqft_per_hectare / area_width
                area_depth = 0.  # terrestrial areas have no depth
            else:  #this is the EPA Defined Terrestrial (i.e., a point as opposed to an area) for which we don't need dimensions
                area_width = 0.
                area_length = 0.
                area_depth = 0.
        return area_width, area_length, area_depth

    # def load_scenario_raw_data(self):
    #     """
    #     :description retrieve deposition data from SQL database for all scenarios (e.g., aerial/EPA Defined Pond
    #     :parameter num_scenarios number of deposition scenarios included in SQL database
    #     :parameter scenario_name name of scenario as included in SQL database
    #     :parameter num_db_values number of values included in deposition scenarios (same for all scenarios)
    #     :parameter scenario_raw_data array of depostion values retrieved from SQL database
    #     :NOTE This method is not currently utilized (instead we use 'get_scenario_deposition_data' to retrieve them as needed)
    #     :return:
    #     """
    #     self.scenario_raw_data = pd.Series([], dtype='float')
    #     for i in range(self.num_scenarios):
    #         self.scenario_raw_data[i] = self.get_scenario_deposition_data(self.scenario_name[i], self.num_db_values)
    #     return

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

        engine = create_engine(self.db_name)
        conn = engine.connect()
        result1 = conn.execute("SELECT * from " + self.db_table)
        col_names = result1.keys()
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

    def calc_avg_waterconc_ngl(self, avg_dep_lbac ,area_width, area_length, area_depth):
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
                            (area_width * area_length / self.sqft_per_acre) / \
                            (area_width * area_length * area_depth)) / self.liters_per_ft3
        return avg_waterconc_ngl

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
        #     # print self.out_avg_depo_gha
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
        #     print self.out_avg_depo_lbac
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
        #         #print 2
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