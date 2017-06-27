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
# import sqlalchemy_utils as sqlu
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
        #list of valid options per scenario variable
        aquatic_body_type_list = ['epa_defined_pond', 'user_defined_pond', 'epa_defined_wetland', 'user_defined_wetland']
        aerial_drop_size_list = ['very_fine_to_fine', 'fine_to_medium', 'medium_to_coarse', 'coarse_to_very_coarse']
        terrestrial_field_type_list = ['epa_defined_terrestrial', 'user_defined_terrestrial']
        ground_drop_size_list = ['very_fine', 'fine_to_medium-coarse']
        airblast_type_list = ['orchard', 'vineyard', 'normal', 'dense', 'sparse']
        boom_height_list = ['high', 'low']

        for i in range(self.num_simulations):
            #print(self.ecosystem_type[i])
            if (self.ecosystem_type[i] == 'aquatic_assessment'):
                if self.application_method[i] == 'tier_1_aerial':
                    if (self.aquatic_body_type[i] in aquatic_body_type_list and
                                self.drop_size_aerial[i] in aerial_drop_size_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Aquatic Aerial Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Aerial Scenario'
                elif self.application_method[i] == 'tier_1_ground':
                    if (self.aquatic_body_type[i] in aquatic_body_type_list and
                                self.drop_size_ground[i] in ground_drop_size_list and
                                self.boom_height[i] in boom_height_list):
                         self.out_sim_scenario_chk[i] = 'Valid Tier I Aquatic Ground Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Ground Scenario'
                elif self.application_method[i] == 'tier_1_airblast':
                    if (self.aquatic_body_type[i] in aquatic_body_type_list and
                        self.airblast_type[i] in airblast_type_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Aquatic Airblast Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Airblast Scenario'
                else:
                    self.out_sim_scenario_chk[i] = 'Invalid Tier I Aquatic Assessment application method'
            elif (self.ecosystem_type[i] == 'terrestrial_assessment'):
                if self.application_method[i] == 'tier_1_aerial':
                    if (self.terrestrial_field_type[i] in terrestrial_field_type_list and
                                self.drop_size_aerial[i] in aerial_drop_size_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Terrestrial Aerial Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Aerial Scenario'
                elif self.application_method[i] == 'tier_1_ground':
                    if (self.terrestrial_field_type[i] in terrestrial_field_type_list and
                            self.drop_size_ground[i] in ground_drop_size_list and
                            self.boom_height[i] in boom_height_list):
                         self.out_sim_scenario_chk[i] = 'Valid Tier I Terrestrial Ground Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Ground Scenario'
                elif self.application_method[i] == 'tier_1_airblast':
                    if (self.terrestrial_field_type[i] in terrestrial_field_type_list and
                                self.airblast_type[i] in airblast_type_list):
                        self.out_sim_scenario_chk[i] = 'Valid Tier I Terrestrial Airblast Scenario'
                    else:
                        self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Airblast Scenario'
                else:
                    self.out_sim_scenario_chk[i] = 'Invalid Tier I Terrestrial Assessment application method'
            else:
                    self.out_sim_scenario_chk[i] = 'Invalid scenario ecosystem_type'
        return

    def check_numerical_inputs(self):
        """
        :description determines if all numerical inputs for valid scenarios are present and in appropriate range
        :return
        """
        #list of valid options for calculation input
        calculation_input_list = ['distance_to_point_or_area_ft', 'fraction_of_applied', 'initial_deposition_gha',
                                  'initial_deposition_lbac', 'initial_deposition_mgcm2', 'initial_concentration_ngL']

        #initialize validation variables to default values
        self.user_pond_width_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_pond_depth_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_wetland_width_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_wetland_depth_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_terrestrial_width_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.calculation_input_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.downwind_distance_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_frac_applied_type_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_avg_dep_gha_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_avg_dep_mgcm2_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_avg_conc_ngl_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.user_avg_dep_lbac_chk = pd.Series(self.num_simulations * ['na'], dtype='object')
        self.scenario_description_sum_chk = pd.Series(self.num_simulations * ['Valid'], dtype='object')
        self.scenario_area_dim_sum_chk = pd.Series(self.num_simulations * ['Valid'], dtype='object')
        self.scenario_calc_type_sum_chk = pd.Series(self.num_simulations * ['Valid'], dtype='object')


        for i in range(self.num_simulations):
            #check pond/wetland/terrestrial area dimensions
            if ('Valid Tier I Aquatic' in self.out_sim_scenario_chk[i]):
                if ('user_defined_pond' in self.aquatic_body_type[i]):
                    if (self.user_pond_width[i] >= self.min_area_width and
                            self.user_pond_width[i] <= self.max_distance):
                        self.user_pond_width_chk[i] = 'Ok'
                    else:
                        self.user_pond_width_chk[i] = 'Must be >= ' + str(self.min_area_width) +  \
                                                       ' and <= ' + str(self.max_distance) + 'feet'
                        self.scenario_area_dim_sum_chk[i] = 'Invalid'

                    if (self.user_pond_depth[i] >= self.min_waterbody_depth and
                        self.user_pond_depth[i] <= self.max_waterbody_depth):
                        self.user_pond_depth_chk[i] = 'Ok'
                    else:
                        self.user_pond_depth_chk[i] = 'Must be >= ' + str(self.min_waterbody_depth) + \
                                                       ' and  <= ' + str(self.max_waterbody_depth)
                        self.scenario_area_dim_sum_chk[i] = 'Invalid'

                elif ('user_defined_wetland' in self.aquatic_body_type[i]):
                    if (self.user_wetland_width[i] >= self.min_area_width and
                            self.user_wetland_width[i] <= self.max_distance):
                        self.user_wetland_width_chk[i] = 'Ok'
                    else:
                        self.user_wetland_width_chk[i] = 'Must be >= 0'
                        self.scenario_area_dim_sum_chk[i] = 'Invalid'
                    if (self.user_wetland_depth[i] > self.min_waterbody_depth and
                        self.user_wetland_depth[i] <= self.max_waterbody_depth):
                        self.user_wetland_depth_chk[i] = 'Ok'
                    else:
                        self.user_wetland_depth_chk[i] = 'Must be >= ' + str(self.min_waterbody_depth) + \
                                                       ' and  <= ' + str(self.max_waterbody_depth)
                        self.scenario_area_dim_sum_chk[i] = 'Invalid'

            elif ('Valid Tier I Terrestrial' in self.out_sim_scenario_chk[i]):
                if ('user_defined_terrestrial' in self.terrestrial_field_type[i]):
                    if (self.user_terrestrial_width[i] > 0.0):
                        self.user_terrestrial_width_chk[i] = 'Ok'
                    else:
                        self.user_terrestrial_width_chk[i] = 'Must be > 0'
                        self.scenario_area_dim_sum_chk[i] = 'Invalid'

            else:
                self.scenario_description_sum_chk[i] = 'Invalid'

            #check calculation input type and values
            if (self.calculation_input[i] in calculation_input_list):
                self.calculation_input_chk[i] = 'Ok'
                if (self.calculation_input[i] == 'distance_to_point_or_area_ft'):
                    if (self.downwind_distance[i] >= 0 and  \
                            self.downwind_distance[i] <= self.max_distance):
                        self.downwind_distance_chk[i] = 'Ok'
                    else:
                        self.downwind_distance_chk[i] = 'Must be >= 0 and <= ' + str(self.max_distance)
                        self.scenario_calc_type_sum_chk[i] = 'Invalid'
                elif (self.calculation_input[i] == 'fraction_of_applied'):
                    if (self.user_frac_applied[i] > 0):
                        self.user_frac_applied_type_chk[i] = 'Ok'
                    else:
                        self.user_frac_applied_type_chk[i] = 'Must be > 0'
                        self.scenario_calc_type_sum_chk[i] = 'Invalid'
                elif (self.calculation_input[i] == 'initial_deposition_gha'):
                    if (self.user_avg_dep_gha[i] > 0):
                        self.user_avg_dep_gha_chk[i] = 'Ok'
                    else:
                        self.user_avg_dep_gha_chk[i] = 'Must be > 0'
                        self.scenario_calc_type_sum_chk[i] = 'Invalid'
                elif (self.calculation_input[i] == 'initial_deposition_lbac'):
                    if (self.user_avg_dep_lbac[i] > 0):
                        self.user_avg_dep_lbac_chk[i] = 'Ok'
                    else:
                        self.user_avg_dep_lbac_chk[i] = 'Must be > 0'
                        self.scenario_calc_type_sum_chk[i] = 'Invalid'
                elif (self.calculation_input[i] == 'initial_deposition_mgcm2'):
                    if (self.user_avg_dep_mgcm2[i] > 0):
                        self.user_avg_dep_mgcm2_chk[i] = 'Ok'
                    else:
                        self.user_avg_dep_mgcm2_chk[i] = 'Must be > 0'
                        self.scenario_calc_type_sum_chk[i] = 'Invalid'
                elif (self.calculation_input[i] == 'initial_concentration_ngL'):
                    if (self.user_avg_conc_ngl[i] > 0):
                        self.user_avg_conc_ngl_chk[i] = 'Ok'
                    else:
                        self.user_avg_conc_ngl_chk[i] = 'Must be > 0'
                        self.scenario_calc_type_sum_chk[i] = 'Invalid'
            else:
                self.calculation_input_chk[i] = 'Invalid calculation_input string'
                self.scenario_calc_type_sum_chk[i] = 'Invalid'


        #write results to summary excel file
        csv_path = "./agdrift_input_validation.xlsx"
        sim_num = pd.Series(['Simulation ' + str(i) for i in range (self.num_simulations)], dtype='object')

        #populate general scenario validation summary dataframe
        inputs_summary_df = pd.concat([sim_num, self.scenario_description_sum_chk, self.scenario_area_dim_sum_chk,
                                self.scenario_calc_type_sum_chk], axis=1 )
        inputs_summary_df.columns = ['Simulation #', 'Scenario Description', 'Area Dimensions', 'Calculation Type & Intial Values']

        #populate scenario validation details dataframe
        inputs_details_df = pd.concat([sim_num, self.out_sim_scenario_chk, self.user_pond_width_chk, self.user_pond_depth_chk, \
                     self.user_wetland_width_chk, self.user_wetland_depth_chk, self.user_terrestrial_width_chk, \
                     self.calculation_input_chk, self.downwind_distance_chk, self.user_frac_applied_type_chk, \
                     self.user_avg_dep_gha_chk, self.user_avg_dep_lbac_chk, self.user_avg_dep_mgcm2_chk, \
                     self.user_avg_conc_ngl_chk], axis=1)
        inputs_details_df.columns = ['Simulation #', 'Scenario Description Check','User Pond Width', 'User Pond Depth',
                              'Users Wetland Width','User Wetland Depth','Terrestrial Width', 'Calculation Type',
                              'Downwind Distance','Fraction Applied','Avg Deposition(gha)', 'Avg Deposition(lbac)',
                              'Avg Deposition(mgcm2)','Avg Concentration(ngl)']

        #write worksheets within excel file; one for summary validation data and one for detailed validation data
        writer = pd.ExcelWriter(csv_path, engine='xlsxwriter')
        inputs_summary_df.to_excel(writer, sheet_name='input_validation_summary')
        inputs_details_df.to_excel(writer, sheet_name='input_validation_matrix')
        writer.save()

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
                if self.application_method[i] == 'tier_1_aerial':
                    if self.drop_size_aerial[i] == 'very_fine_to_fine':
                        self.out_sim_scenario_id[i] = 'aerial_vf2f'
                    elif self.drop_size_aerial[i] == 'fine_to_medium':
                        self.out_sim_scenario_id[i] = 'aerial_f2m'
                    elif self.drop_size_aerial[i] == 'medium_to_coarse':
                        self.out_sim_scenario_id[i] = 'aerial_m2c'
                    elif self.drop_size_aerial[i] == 'coarse_to_very_coarse':
                        self.out_sim_scenario_id[i] = 'aerial_c2vc'
                elif self.application_method[i] == 'tier_1_ground':
                    if self.boom_height[i] == 'low':
                        if self.drop_size_ground[i] == 'very_fine':
                            self.out_sim_scenario_id[i] = 'ground_low_vf'
                        elif self.drop_size_ground[i] == 'fine_to_medium-coarse':
                            self.out_sim_scenario_id[i] = 'ground_low_fmc'
                    elif self.boom_height[i] == 'high':
                        if self.drop_size_ground[i] == 'very_fine':
                            self.out_sim_scenario_id[i] = 'ground_high_vf'
                        elif self.drop_size_ground[i] == 'fine_to_medium-coarse':
                            self.out_sim_scenario_id[i] = 'ground_high_fmc'
                elif self.application_method[i] == 'tier_1_airblast':
                    if self.airblast_type[i] == 'normal':
                        self.out_sim_scenario_id[i] = 'airblast_normal'
                    elif self.airblast_type[i] == 'dense':
                        self.out_sim_scenario_id[i] = 'airblast_dense'
                    elif self.airblast_type[i] == 'sparse':
                        self.out_sim_scenario_id[i] = 'airblast_sparse'
                    elif self.airblast_type[i] == 'vineyard':
                        self.out_sim_scenario_id[i] = 'airblast_vineyard'
                    elif self.airblast_type[i] == 'orchard':
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

        if (self.ecosystem_type[i] == 'aquatic_assessment'):
            if (self.aquatic_body_type[i] == 'epa_defined_pond'):
                self.out_area_width[i] = self.default_width
                self.out_area_length[i] = self.default_length
                self.out_area_depth[i] = self.default_pond_depth
            elif (self.aquatic_body_type[i] == 'epa_defined_wetland'):
                self.out_area_width[i] = self.default_width
                self.out_area_length[i] = self.default_length
                self.out_area_depth[i] = self.default_wetland_depth
            elif (self.aquatic_body_type[i] == 'user_defined_pond'):
                self.out_area_width[i] = self.user_pond_width[i]
                self.out_area_length[i] = self.sqft_per_hectare / self.out_area_width[i]
                self.out_area_depth[i] = self.user_pond_depth[i]
            elif (self.aquatic_body_type[i] == 'user_defined_wetland'):
                self.out_area_width[i] = self.user_wetland_width[i]
                self.out_area_length[i] = self.sqft_per_hectare / self.out_area_width[i]
                self.out_area_depth[i] = self.user_wetland_depth[i]
        elif (self.ecosystem_type[i] == 'terrestrial_assessment'):
            if (self.terrestrial_field_type[i] == 'user_defined_terrestrial'):  # implies user to specify an area width
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
        THIS METHOD WAS REWRITTEN (SEE 'EXTEND_CURVE') TO MAKE MORE GENERIC BY PASSING IN THE DATA ARRAYS TO BE EXTENDED
        :description extends distance vs deposition (fraction of applied) curve to enable model calculations 
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

    def extend_curve(self, x_array, y_array, max_dist, dist_inc, num_pts_ext, ln_ln_trans):
        """
        :description extends/extrapolates an x,y array of data points that reflect a ln ln relationship by selecting
                     a number of points near the end of the x,y arrays and fitting a line to the points
                     ln ln transforms (two ln ln transforms can by applied; on using the straight natural log of
                     each selected x,y point and one using a 'relative' value of each of the selected points  --
                     the relative values are calculated by establishing a zero point closest to the selected
                     points

                     For AGDRIFT: extends distance vs deposition (fraction of applied) curve to enable model calculations
                     when area of interest (pond, wetland, terrestrial field) lie partially outside the original
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

        :param x_array: array of x values to be extended (must be at least 17 data points in original array)
        :param y_array: array of y values to be extended
        :param max_dist: maximum distance (ft) associated with unextended x values
        :param dist_inc: increment (ft) for each extended data point
        :param num_pts_ext: number of points at end of original x,y arrays to be used for extending the curve
        :param ln_ln_trans: form of transformation to perform (True: straight ln ln, False: relative ln ln)
        :return:
        """

        # set first and last index of points to be used to fit line 
        npts_orig = len(x_array)
        first_fitting_pt = npts_orig - num_pts_ext

        # set arrays for containing curve points to be used to fit/extend curve at tail
        x_fitting_pts = np.zeros([num_pts_ext])  # distance
        y_fitting_pts = np.zeros([num_pts_ext])  # deposition (fraction of applied)

        # select the last num_pts_ext data points and perform a natural log transform on the distance/deposition values
        # then fit these data to a line of best fit

        if (ln_ln_trans):  # straight ln ln transformation
            x_fitting_pts = np.array([x_array[j] for j in range(first_fitting_pt, npts_orig)])
            x_fitting_pts = np.log(x_fitting_pts)
            y_fitting_pts = np.array([y_array[j] for j in range(first_fitting_pt, npts_orig)])
            y_fitting_pts = np.log(y_fitting_pts)
        else:
            # this ln transformation is done with relative x,y values (this is the transformation
            # used in the AGDRIFT AGEXTD code
            x_zero = x_array[first_fitting_pt - 1]
            y_zero = y_array[first_fitting_pt - 1]
            y_zero_log = np.log(y_zero)

            k = 0
            for j in range(first_fitting_pt, npts_orig):
                x_fitting_pts[k] = np.log(x_array[j] - x_zero)
                y_fitting_pts[k] = np.log(y_array[j] / y_zero)
                k += 1

        # establish scipy function to be fit to x_fitting_pts, y_fitting_pts data 
        def func(x_fitting_pts, a, b):
            return a * x_fitting_pts + b

        # use scipy's curve fit and get the coefficients for the established function
        coefficients, pcov = curve_fit(func, x_fitting_pts, y_fitting_pts)
        coef_a = coefficients[0]
        coef_b = coefficients[1]

        # extend the distance array to 2 * 997 = 1994ft in increments of 6.56ft (and calculate related depositions)
        npts_ext = int(((((max_dist * 2.) - x_array[npts_orig - 1]) / \
                         dist_inc)) + npts_orig)
        dist = x_array[npts_orig - 1]
        for j in range(npts_orig, npts_ext):
            dist = dist + dist_inc

            if (ln_ln_trans):
                y_array[j] = np.exp(coef_a * np.log(dist) + coef_b)
            else:
                y_temp = coef_a * np.log(dist - x_zero) + coef_b
                y_array[j] = np.exp(y_temp + y_zero_log)

            x_array[j] = x_array[j-1] + dist_inc
        return x_array, y_array

    def extend_curve_opp(self, x_array, y_array, max_dist, dist_inc, num_pts_ext, ln_ln_trans):
        """
        :description extends/extrapolates an x,y array of data points that reflect a ln ln relationship by selecting
                     a number of points near the end of the x,y arrays and fitting a line to the points
                     ln ln transforms (two ln ln transforms can by applied; on using the straight natural log of
                     each selected x,y point and one using a 'relative' value of each of the selected points  --
                     the relative values are calculated by establishing a zero point closest to the selected
                     points

                     For AGDRIFT: extends distance vs deposition (fraction of applied) curve to enable model calculations
                     when area of interest (pond, wetland, terrestrial field) lie partially outside the original
                     curve (whose extent is 997 feet).  The extension is achieved by fitting a line of best fit
                     to the last 16 points of the original curve.  The x,y values representing the last 16 points
                     are natural log transforms of the distance and deposition values at the 16 points.  Two long
                     transforms are coded here, reflecting the fact that the AGDRIFT model (v2.1.1) uses each of them
                     under different circumstandes (which I believe is not the intention but is the way the model
                     functions  --  my guess is that one of the transforms was used and then a second one was coded
                     to increase the degree of conservativeness  -- but the code was changed in only one of the two
                     places where the transformation occurs.
                     Finally, the AGDRIFT model extends the curve only when necessary (i.e., when it determines that
                     the area of interest lies partially beyond the last point of the original curve (997 ft).  In
                     this code all the curves are extended out to 1994 ft, which represents the furthest distance that
                     the downwind edge of an area of concern can be specified.  All scenario curves are extended here
                     because we are running multiple simulations (e.g., monte carlo) and instead of extending the
                     curves each time a simulation requires it (which may be multiple time for the same scenario
                     curve) we just do it for all curves up front.  There is a case to be made that the
                     curves should be extended external to this code and simply provide the full curve in the SQLite
                     database containing the original curve.

        :param x_array: array of x values to be extended (must be at least 17 data points in original array)
        :param y_array: array of y values to be extended
        :param max_dist: maximum distance (ft) associated with unextended x values
        :param dist_inc: increment (ft) for each extended data point
        :param num_pts_ext: number of points at end of original x,y arrays to be used for extending the curve
        :param ln_ln_trans: form of transformation to perform (True: straight ln ln, False: relative ln ln)
        :return:
        """

        # set first and last index of points to be used to fit line
        npts_orig = len(x_array)
        first_fitting_pt = npts_orig - num_pts_ext

        # set arrays for containing curve points to be used to fit/extend curve at tail
        x_fitting_pts = np.zeros([num_pts_ext])  # distance
        y_fitting_pts = np.zeros([num_pts_ext])  # deposition (fraction of applied)

        # select the last num_pts_ext data points and perform a natural log transform on the distance/deposition values
        # then fit these data to a line of best fit

        #convert x_array from feet to meters
        x_array = x_array * self.meters_per_ft
        inc_dist = dist_inc * self.meters_per_ft

        #perform data transformations per Agdrift AGEXTD.FOR routine
        if (ln_ln_trans):  # straight ln ln transformation
            x_fitting_pts = np.array([x_array[j] for j in range(first_fitting_pt, npts_orig)])
            x_fitting_pts = np.log(x_fitting_pts)
            y_fitting_pts = np.array([y_array[j] for j in range(first_fitting_pt, npts_orig)])
            y_fitting_pts = np.log(y_fitting_pts)
        else:
            # this ln transformation is done with relative x,y values (this is the transformation
            x_zero = x_array[first_fitting_pt - 1]
            y_zero = y_array[first_fitting_pt - 1]
            y_zero_log = np.log(y_zero)

            k = 0
            for j in range(first_fitting_pt, npts_orig):
                x_fitting_pts[k] = np.log(x_array[j] - x_zero)
                y_fitting_pts[k] = np.log(y_array[j] / y_zero)
                k += 1

        #calculate coefficients as per the Agdrift AGEXTD.FOR routine
        sum_x = 0.
        sum_y = 0.
        sum_x2 = 0.
        sum_y2 = 0.
        for i in range(num_pts_ext):
            sum_x = sum_x + x_fitting_pts[i]
            sum_y = sum_y + y_fitting_pts[i]
            sum_x2 = sum_x2 + (x_fitting_pts[i])**2.
            sum_y2 = sum_y2 + (x_fitting_pts[i] * y_fitting_pts[i])
        coef_b = (sum_y2 - (sum_x * sum_y/num_pts_ext)) / (sum_x2 - (sum_x*sum_x/num_pts_ext))
        coef_a = np.exp((sum_y - coef_b*sum_x) / num_pts_ext)

        npts_ext = int((((((max_dist*self.meters_per_ft * 2.) - x_array[npts_orig - 1]) / \
                         2.0)) + npts_orig) + 1)
        dist = x_array[npts_orig - 1]
        for j in range(npts_orig, npts_ext):
            dist = dist + inc_dist

            if (ln_ln_trans):
                y_array[j] = coef_a * dist**coef_b
            else:
                y_array[j] = y_zero * coef_a * (dist - x_zero)**coef_b

            x_array[j] = x_array[j-1] + inc_dist

        #convert x_array back to feet
        x_array = x_array * (1./self.meters_per_ft)
        return x_array, y_array

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
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        get_table = cursor.execute("SELECT * from " + self.db_table)
        conn.close()
        col_names = [description[0] for description in get_table.description]
        # col_names = get_table.keys() sql_alchemy
        print(col_names)
        if len(col_names) > 0:
            # if os.path.isfile(self.db_name):
            logging.info('found agdrift database')
        else:
            logging.info('cannot find agdrift database')
            dir_path = os.path.dirname(os.path.abspath(__file__))
            logging.info('current directory path is:')
            logging.info(dir_path)
        # if sqlu.database_exists(self.db_name):
        #     engine = create_engine(self.db_name)
        #     conn = engine.connect()
        #     result1 = conn.execute("SELECT * from " + self.db_table)
        #     col_names = result1.keys()
        # else:
        #     dir_path = os.path.dirname(os.path.abspath(__file__))
        #     logging.info('current directory path is:')
        #     logging.info(dir_path)
        #     print('cannot find agdrift database at ' + self.db_name)
        #     dir_path = os.path.dirname(os.path.abspath(__file__))
        #     print('current directory path is:')
        #     print(dir_path)
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
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        result = cursor.execute("SELECT " + self.distance_name + " from " + self.db_table)

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
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        #testing for column names
        string_query = 'SELECT * from ' + self.db_table
        logging.info(string_query)
        result1 = cursor.execute(string_query)
                             #col_names = result1.keys()
                             #logging.info(col_names)

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

    def calc_avg_dep_gha(self, avg_dep_lbac):
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

    def calc_avg_fielddep_mgcm2(self, avg_dep_lbac):
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

        avg_fielddep_mgcm2 = ((avg_dep_lbac * self.gms_per_lb *
                          self.mg_per_gram) / (self.sqft_per_acre * self.cm2_per_ft2))
        return avg_fielddep_mgcm2

    def calc_avg_dep_lbac_from_mgcm2(self, avg_fielddep_mgcm2):
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

        avg_dep_lbac = (avg_fielddep_mgcm2 * (self.sqft_per_acre * self.cm2_per_ft2)) / (self.gms_per_lb * self.mg_per_gram)
        return avg_dep_lbac


    def generate_running_avg(self, npts_orig, x_array_in, y_array, x_dist):
        """
        :description this method takes an x/y array and creates a x_out/y_out array of running weighted averages;
                     the algorithm mimics the AGAVE.FOR routine created by OPP and found in the collection of
                     software delivered from OPP related to AGDRIFT; this routine is not used here  because it is
                     computationally inefficient; it was produced here simply to provide a check on the new
                     routine found in "locate_integrated_avg"

                     The method generates the running average for each x value (as opposed to establishing
                     redefining the x values to reflect a value for each x_dist increment; thus if the specified
                     x_dist is shorter than the distance between any 2 x values then the running average will not be
                     'continuous', i.e., there will be portions of the original curve not included in the overall
                     running average
        :param npts_orig: number of points in orginal x vs y data points
        :param x_array_in: x values of original x vs y data points
        :param y_array: y values of original x vs y data points (assumed to apply from x(i) to x(i+1))
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
                 cum_area =  (0.5 * (y_array[j] + y_array[j+1])) * (x_array_in[j+1] - x_array_in[j])

                    #if x_dist is completely within this x[i] to x[i+1] segment then interpolate the one needed value of cum_area
                 if (x_array_in[j+1] > (x_array_in[i] + x_dist)):
                     x_interp = x_array_in[i] + x_dist
                     y_interp = (y_array[j] * (x_array_in[j+1] - x_interp) +
                                 y_array[j+1] * (x_interp - x_array_in[j])) / (x_array_in[j + 1] - x_array_in[j])
                     cum_area = (0.5 * (y_interp + y_array[j])) * (x_interp - x_array_in[j])
                     continuing = False
 
                 #if x_dist extends beyond x[i+1], i.e., next x value; then calculate and accumulate all necessary cum_area
                 while continuing:
                    j += 1
                    if (x_array_in[j+1] < (x_array_in[i] + x_dist)):
                        cum_area = cum_area + (0.5 * (y_array[j] + y_array[j+1])) * (x_array_in[j+1] - x_array_in[j])
                    else:
                        x_interp = x_array_in[i] + x_dist
                        y_interp = (y_array[j] * (x_array_in[j+1] - x_interp) +
                                    y_array[j+1] * (x_interp - x_array_in[j])) / (x_array_in[j+1] - x_array_in[j])
                        cum_area = cum_area + (0.5 * (y_interp + y_array[j])) * (x_interp - x_array_in[j])

                        continuing = False
                 x_array_out[i] = x_array_in[i]
                 y_array_out[i] = cum_area / x_dist
                 npts_out = len(x_array_out)

        return x_array_out, y_array_out, npts_out

    def locate_integrated_avg(self, npts_orig, x_array_in, y_array, x_dist, integrated_avg):
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
        :param y_array: y values of original x vs y data points
        :param x_dist: length (in x units) for which running weighted average is to be calculated
        :param integrated_avg: weighted average of y_array over x_dist
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
        j_init = 0 #index of initial x[] of current averaging
        for i in range (npts_orig-1): #calculate running weighted average for these points
            if(x_array_in[i] < (x_array_in[npts_orig-1] - x_dist)):
                if (i == 0):   #first time through process full extent of x_dist (i.e., all x_array_in pts included in x dist)
                    j = 0
                    integrated_tot = 0

                    while continuing:
                        x_tot = x_tot + (x_array_in[j+1] - x_array_in[j])
                        integrated_inc = (0.5 * (y_array[j] + y_array[j+1])) * (x_array_in[j+1] - x_array_in[j])
                        if(j == 0): init_inc = integrated_inc  #save first increment of running average integration

                        if (x_tot <= x_dist):
                            integrated_tot = integrated_tot + integrated_inc
                            j += 1
                        else:  #last segment
                            x_interp = x_array_in[i] + x_dist
                            y_interp = (y_array[j] * (x_array_in[j+1] - x_interp) +
                                        y_array[j+1] * (x_interp - x_array_in[j])) / (
                                       x_array_in[j+1] - x_array_in[j])
                            integrated_inc = (0.5 * (y_interp + y_array[j])) * (x_interp - x_array_in[j])
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
                    if (y_array[1] < y_array[0]):     #y is decreasing function of x
                        if (y_array_out[i] < integrated_avg):  #if true then we have achieved the integrated_avg before completing the first x_dist
                            # if we surpass the user supplied integrated_avg before reaching the edge of the first running average then
                            # output the message and set the x_dist_of_interest to zero (as is done in the original AGDRIFT model)

                            x_dist_of_interest = x_array_in[0]  #original AGDRIFT model sets this value to zero (i.e., first x point value)
                            return x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk
                    else:
                        if (y_array_out[i] > integrated_avg):  #if true then we have achieved the integrated_avg before completing the first x_dist
                            # if we surpass the user supplied integrated_avg before reaching the edge of the first running average then
                            # output the message and set the x_dist_of_interest to zero (as is done in the original AGDRIFT model)

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
                        x_tot = x_tot + (x_array_in[j+1] - x_array_in[j])
                        integrated_inc = (0.5 * (y_array[j] + y_array[j+1])) * (x_array_in[j+1] - x_array_in[j])
                        if (j == j_init): init_inc = (0.5 * (y_array[i] + y_array[i+1])) * \
                                                     (x_array_in[i+1] - x_array_in[i])  #note 'i' index to denote 1st increment of current averaging

                        if (x_tot <= x_dist):
                            integrated_tot = integrated_tot + integrated_inc
                            j += 1
                        else:
                            x_interp = x_array_in[i] + x_dist
                            y_interp = (y_array[j] * (x_array_in[j+1] - x_interp) +
                                        y_array[j+1] * (x_interp - x_array_in[j])) / (
                                       x_array_in[j+1] - x_array_in[j])
                            integrated_inc = (0.5 * (y_interp + y_array[j])) * (x_interp - x_array_in[j])
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
                    if (y_array[1] < y_array[0]):  #y is decreasing function of x
                        if (y_array_out[i] <= integrated_avg):
                            fraction = (y_array_out[i-1] - integrated_avg) / (y_array_out[i-1] - y_array_out[i])
                            if(self.find_nearest_x):  #if true then round to nearest half x unit
                                #above is precise x_dist_of_interest; below is OPP protocol for rounding the distance up to the nearest segment midpoint or segment boundary
                                if (fraction >= 0.5):
                                    x_dist_of_interest = x_array_out[i]
                                else:
                                    x_dist_of_interest = x_array_out[i-1] + 0.5 * (x_array_out[i] - x_array_out[i-1])
                                #this is crazy but it is what the OPP Agdrift appears to do
                                if(x_dist_of_interest <= 3.2808): x_dist_of_interest = 3.2808
                                if(x_dist_of_interest > 3.2808 and x_dist_of_interest <= 6.5616): x_dist_of_interest = 6.5616
                                if(x_dist_of_interest > 6.5616 and x_dist_of_interest <= 9.8424): x_dist_of_interest = 9.8424
                                if(x_dist_of_interest > 9.8424 and x_dist_of_interest <= 13.1232): x_dist_of_interest = 13.1232
                            else:
                                x_dist_of_interest = x_array_out[i-1] + fraction * (x_array_out[i] - x_array_out[i-1])
                            #write output arrays to excel file  --  just for debugging
                            #self.write_arrays_to_csv(x_array_out, y_array_out, "output_array.csv")

                            return x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk

                    else:
                        #this increasing function does not navigate to the nearest 1/2 x point as done above for decreasing function
                        if (y_array_out[i] > integrated_avg):
                            fraction = (integrated_avg - y_array_out[i-1]) / (y_array_out[i] - y_array_out[i-1])
                            x_dist_of_interest = x_array_out[i-1] + fraction * (x_array_out[i] - x_array_out[i-1])
                            return x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk

        #some extent of the area-of-interest (e.g., pond) lies outside the data range
        range_chk = 'out of range'
        return x_array_out, y_array_out, npts_out, np.nan, range_chk

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
                continuing = False
            elif (j > npts-1): #means we are beyond the data range
                out_dist = np.nan
                range_chk = 'out of range'
                continuing = False
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
                                     avg_field_dep_mgcm2, i):
        """
        :description round output variable values (and place in output variable series) so that they can be directly
                     compared to expected results (which were limited in terms of their output format from the OPP AGDRIFT
                     model (V2.1.1) interface (we don't have the AGDRIFT code so we cannot change the output format to
                    agree with this model
        :param avg_dep_foa:
        :param avg_dep_lbac:
        :param avg_dep_gha:
        :param avg_waterconc_ngl:
        :param avg_field_dep_mgcm2:
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

        if(np.isfinite(avg_field_dep_mgcm2)):
            if (avg_field_dep_mgcm2 > 1e-4 and avg_field_dep_mgcm2 < 1.):
                self.out_avg_field_dep_mgcm2[i] = round(avg_field_dep_mgcm2, 4)
            elif (avg_field_dep_mgcm2 > 1.):
                self.out_avg_field_dep_mgcm2[i] = round(avg_field_dep_mgcm2, 2)
            else:
                self.out_avg_field_dep_mgcm2[i] = float('{:0.2e}'.format(float(avg_field_dep_mgcm2)))
        else:
            self.out_avg_field_dep_mgcm2[i] = avg_field_dep_mgcm2
        return

    def write_arrays_to_csv(self, x_in, y_in, db_name):

        # just a quick method to help debugging

        with open(db_name, 'wb') as output_file:
            wr = csv.writer(output_file, dialect='excel')
            for k in range(len(x_in)):
                item1 = x_in[k]
                item2 = y_in[k]
                wr.writerow([item1, item2])
        output_file.close()
        return