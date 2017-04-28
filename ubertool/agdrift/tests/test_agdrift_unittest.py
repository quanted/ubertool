from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy as np
import numpy.testing as npt
import os.path
import pandas as pd
import sys
from tabulate import tabulate
import unittest

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from agdrift_exe import Agdrift

test = {}

class TestAgdrift(unittest.TestCase):
    """
    IEC unit tests.
    """
    def setUp(self):
        """
        setup the test as needed
        e.g. pandas to open agdrift qaqc csv
        Read qaqc csv and create pandas DataFrames for inputs and expected outputs
        :return:
        """
        pass

    def tearDown(self):
        """
        teardown called after each test
        e.g. maybe write test results to some text file
        :return:
        """
        pass

    def create_agdrift_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty agdrift object
        agdrift_empty = Agdrift(df_empty, df_empty)
        return agdrift_empty


    def test_validate_sim_scenarios(self):
        """
        :description determines if user defined scenarios are valid for processing
        :param application_method: type of Tier I application method employed
        :param aquatic_body_def: type of endpoint of concern (e.g., pond, wetland); implies whether
        :                    endpoint of concern parameters (e.g.,, pond width) are set (i.e., by user or EPA standard)
        :param drop_size_*: qualitative description of spray droplet size for aerial & ground applications
        :param boom_height: qualitative height above ground of spray boom
        :param airblast_type: type of orchard being sprayed
        :NOTE we perform an additional validation check related to distances later in the code just before integration
        :return
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.out_sim_scenario_chk = pd.Series([], dtype='object')
        expected_result = pd.Series([
            'Valid Tier I Aquatic Aerial Scenario',
            'Valid Tier I Terrestrial Aerial Scenario',
            'Valid Tier I Aquatic Aerial Scenario',
            'Valid Tier I Terrestrial Aerial Scenario',
            'Valid Tier I Aquatic Aerial Scenario',
            'Valid Tier I Terrestrial Ground Scenario',
            'Valid Tier I Aquatic Ground Scenario',
            'Valid Tier I Terrestrial Ground Scenario',
            'Valid Tier I Aquatic Ground Scenario',
            'Valid Tier I Terrestrial Airblast Scenario',
            'Valid Tier I Aquatic Airblast Scenario',
            'Valid Tier I Terrestrial Airblast Scenario',
            'Valid Tier I Aquatic Airblast Scenario',
            'Valid Tier I Terrestrial Airblast Scenario',
            'Invalid Tier I Aquatic Aerial Scenario',
            'Invalid Tier I Aquatic Ground Scenario',
            'Invalid Tier I Aquatic Airblast Scenario',
            'Invalid Tier I Terrestrial Aerial Scenario',
            'Valid Tier I Terrestrial Ground Scenario',
            'Valid Tier I Terrestrial Airblast Scenario',
            'Invalid scenario ecosystem_type',
            'Invalid Tier I Aquatic Assessment application_method',
            'Invalid Tier I Terrestrial Assessment application_method'],dtype='object')

        try:
            #set test data
            agdrift_empty.num_simulations = len(expected_result)
            agdrift_empty.application_method = pd.Series(
                ['Tier I Aerial',
                 'Tier I Aerial',
                 'Tier I Aerial',
                 'Tier I Aerial',
                 'Tier I Aerial',
                 'Tier I Ground',
                 'Tier I Ground',
                 'Tier I Ground',
                 'Tier I Ground',
                 'Tier I Airblast',
                 'Tier I Airblast',
                 'Tier I Airblast',
                 'Tier I Airblast',
                 'Tier I Airblast',
                 'Tier I Aerial',
                 'Tier I Ground',
                 'Tier I Airblast',
                 'Tier I Aerial',
                 'Tier I Ground',
                 'Tier I Airblast',
                 'Tier I Aerial',
                 'Tier II Aerial',
                 'Tier III Aerial'], dtype='object')
            agdrift_empty.ecosystem_type = pd.Series(
                ['Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Aquatic Assessment',
                 'Aquatic Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment',
                 'Terrestrial Assessment',
                 'Terrestrial Assessment',
                 'Field Assessment',
                 'Aquatic Assessment',
                 'Terrestrial Assessment'], dtype='object')
            agdrift_empty.aquatic_body_type = pd.Series(
                ['EPA Defined Pond',
                 'NaN',
                 'EPA Defined Wetland',
                 'NaN',
                 'User Defined Pond',
                 'NaN',
                 'User Defined Wetland',
                 'NaN',
                 'EPA Defined Wetland',
                 'NaN',
                 'User Defined Pond',
                 'NaN',
                 'User Defined Wetland',
                 'NaN',
                 'Defined Pond',
                 'User Defined Pond',
                 'EPA Defined Pond',
                 'NaN',
                 'NaN',
                 'NaN',
                 'EPA Defined Pond',
                 'User Defined Wetland',
                 'User Defined Pond'], dtype='object')
            agdrift_empty.terrestrial_field_type = pd.Series(
                 ['NaN',
                 'User Defined Terrestrial',
                 'NaN',
                 'EPA Defined Terrestrial',
                 'NaN',
                 'User Defined Terrestrial',
                 'NaN',
                 'User Defined Terrestrial',
                 'NaN',
                 'EPA Defined Terrestrial',
                 'NaN',
                 'User Defined Terrestrial',
                 'NaN',
                 'User Defined Terrestrial',
                 'NaN',
                 'NaN',
                 'NaN',
                 'User Defined Terrestrial',
                 'User Defined Terrestrial',
                 'User Defined Terrestrial',
                 'NaN',
                 'NaN',
                 'User Defined Terrestrial'], dtype='object')
            agdrift_empty.drop_size_aerial = pd.Series(
                ['Very Fine to Fine',
                'Fine to Medium',
                'Medium to Coarse',
                'Coarse to Very Coarse',
                'Fine to Medium',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'Medium to Coarse',
                'NaN',
                'Very Fine to Medium',
                'NaN',
                'Very Fine Indeed',
                'NaN',
                'Very Fine to Medium',
                'Medium to Coarse',
                'NaN'], dtype='object')
            agdrift_empty.drop_size_ground = pd.Series(
                ['NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'Very Fine',
                'Fine to Medium/Coarse',
                'Very Fine',
                'Fine to Medium/Coarse',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'Very Fine',
                'NaN',
                'Fine to Medium/Coarse',
                'Very Fine',
                'NaN',
                'Very Fine to Medium',
                'NaN',
                'Very Fine'], dtype='object')
            agdrift_empty.boom_height = pd.Series(
               ['NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'High',
                'Low',
                'High',
                'Low',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'High',
                'NaN',
                'NaN',
                'NaN',
                'NaN'],dtype='object')
            agdrift_empty.airblast_type = pd.Series(
                ['NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'Normal',
                 'Dense',
                 'Sparse',
                 'Orchard',
                 'Vineyard',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'NaN',
                 'Vineyard',
                 'NaN',
                 'NaN',
                 'NaN'], dtype='object')

            agdrift_empty.validate_sim_scenarios()
            result = agdrift_empty.out_sim_scenario_chk
            npt.assert_array_equal(result, expected_result, err_msg="", verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_set_sim_scenario_id(self):
        """
        :description provides scenario ids per simulation that match scenario names (i.e., column_names) from SQL database
        :param out_sim_scenario_id: scenario name as assigned to individual simulations
        :param num_simulations: number of simulations to assign scenario names
        :param out_sim_scenario_chk: from previous method where scenarios were checked for validity
        :param application_method: application method of scenario
        :param drop_size_*: qualitative description of spray droplet size for aerial and ground applications
        :param boom_height: qualitative height above ground of spray boom
        :param airblast_type: type of airblast application (e.g., vineyard, orchard)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series(['aerial_vf2f',
                                     'aerial_f2m',
                                     'aerial_m2c',
                                     'aerial_c2vc',
                                     'ground_low_vf',
                                     'ground_low_fmc',
                                     'ground_high_vf',
                                     'ground_high_fmc',
                                     'airblast_normal',
                                     'airblast_dense',
                                     'airblast_sparse',
                                     'airblast_vineyard',
                                     'airblast_orchard',
                                     'Invalid'], dtype='object')
        try:
            agdrift_empty.num_simulations = len(expected_result)
            agdrift_empty.out_sim_scenario_chk = pd.Series(['Valid Tier I Aerial',
                                                          'Valid Tier I Aerial',
                                                          'Valid Tier I Aerial',
                                                          'Valid Tier I Aerial',
                                                          'Valid Tier I Ground',
                                                          'Valid Tier I Ground',
                                                          'Valid Tier I Ground',
                                                          'Valid Tier I Ground',
                                                          'Valid Tier I Airblast',
                                                          'Valid Tier I Airblast',
                                                          'Valid Tier I Airblast',
                                                          'Valid Tier I Airblast',
                                                          'Valid Tier I Airblast',
                                                          'Invalid Scenario'], dtype='object')

            agdrift_empty.application_method = pd.Series(['Tier I Aerial',
                                                          'Tier I Aerial',
                                                          'Tier I Aerial',
                                                          'Tier I Aerial',
                                                          'Tier I Ground',
                                                          'Tier I Ground',
                                                          'Tier I Ground',
                                                          'Tier I Ground',
                                                          'Tier I Airblast',
                                                          'Tier I Airblast',
                                                          'Tier I Airblast',
                                                          'Tier I Airblast',
                                                          'Tier I Airblast',
                                                          'Tier I Aerial'], dtype='object')
            agdrift_empty.drop_size_aerial = pd.Series(['Very Fine to Fine',
                                                 'Fine to Medium',
                                                 'Medium to Coarse',
                                                 'Coarse to Very Coarse',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN'], dtype='object')
            agdrift_empty.drop_size_ground = pd.Series(['NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'Very Fine',
                                                 'Fine to Medium/Coarse',
                                                 'Very Fine',
                                                 'Fine to Medium/Coarse',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN',
                                                 'NaN'], dtype='object')
            agdrift_empty.boom_height = pd.Series(['NaN',
                                                   'NaN',
                                                   'NaN',
                                                   'NaN',
                                                   'Low',
                                                   'Low',
                                                   'High',
                                                   'High',
                                                   'NaN',
                                                   'NaN',
                                                   'NaN',
                                                   'NaN',
                                                   'NaN',
                                                   'NaN'], dtype='object')
            agdrift_empty.airblast_type = pd.Series(['NaN',
                                                     'NaN',
                                                     'NaN',
                                                     'NaN',
                                                     'NaN',
                                                     'NaN',
                                                     'NaN',
                                                     'NaN',
                                                     'Normal',
                                                     'Dense',
                                                     'Sparse',
                                                     'Vineyard',
                                                     'Orchard',
                                                     'NaN'], dtype='object')

            agdrift_empty.set_sim_scenario_id()
            result = agdrift_empty.out_sim_scenario_id
            npt.assert_array_equal(result, expected_result, err_msg="", verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_assign_column_names(self):
        """
        :description assigns column names (except distaqnce column) from sql database to internal scenario names
        :param column_name: short name for pesiticide application scenario for which distance vs deposition data is provided
        :param scenario_name: internal variable for holding scenario names
        :param scenario_number: index for scenario_name (this method assumes the distance values could occur in any column
        :param distance_name: internal name for the column holding distance data
        :NOTE to test both outputs of this method I simply appended them together
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.scenario_name = pd.Series([], dtype='object')
        expected_result = pd.Series(['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                     'ground_low_vf', 'ground_low_fmc',
                                     'ground_high_vf', 'ground_high_fmc',
                                     'airblast_normal', 'airblast_dense', 'airblast_sparse',
                                     'airblast_vineyard', 'airblast_orchard'], dtype='object')

        try:
            agdrift_empty.column_names = pd.Series(['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                     'ground_low_vf', 'ground_low_fmc',
                                     'ground_high_vf', 'ground_high_fmc',
                                     'airblast_normal', 'airblast_dense', 'airblast_sparse',
                                     'airblast_vineyard', 'airblast_orchard', 'distance_ft'])

            #call method to assign scenario names
            agdrift_empty.assign_column_names()
            result = agdrift_empty.scenario_name
            npt.assert_array_equal(result, expected_result, err_msg="", verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_get_distances(self):
        """
        :description retrieves distance values for deposition scenario datasets
        :            all scenarios use same distances
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE any blank fields are filled with 'nan'
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.db_name = 'sqlite:///../sqlite_agdrift_distance.db'
        agdrift_empty.db_table = 'output'

        expected_result = pd.Series([], dtype='float')

        try:

            expected_result = [0.,0.102525,0.20505,0.4101,0.8202,1.6404,3.2808,4.9212,6.5616,9.8424,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632]

            agdrift_empty.distance_name = 'distance_ft'
            agdrift_empty.num_db_values = len(expected_result)
            result = agdrift_empty.get_distances(agdrift_empty.num_db_values)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_get_scenario_deposition_data(self):
        """
        :description retrieves deposition data for all scenarios from sql database
        :            and checks that for each the first, last, and total number of values
        :            are correct
        :param scenario: name of scenario for which data is to be retrieved
        :param num_values: number of values included in scenario datasets
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()
        #scenario_data = pd.Series([[]], dtype='float')
        result = pd.Series([], dtype='float')

        #changing expected values to the 161st
        expected_result = [0.50013,0.041273,161.0, #aerial_vf2f
                           0.49997,0.011741,161.0, #aerial_f2m
                           0.4999,0.0053241,161.0, #aerial_m2c
                           0.49988,0.0031189,161.0, #aerial_c2vc
                           1.019339,9.66E-04,161.0, #ground_low_vf
                           1.007885,6.13E-04,161.0, #ground_low_fmc
                           1.055205,1.41E-03,161.0, #ground_high_vf
                           1.012828,7.72E-04,161.0, #ground_high_fmc
                           8.91E-03,3.87E-05,161.0, #airblast_normal
                           0.1155276,4.66E-04,161.0, #airblast_dense
                           0.4762651,5.14E-05,161.0, #airblast_sparse
                           3.76E-02,3.10E-05,161.0, #airblast_vineyard
                           0.2223051,3.58E-04,161.0] #airblast_orchard

        try:
            agdrift_empty.num_db_values = 161  #set number of data values in sql db
            agdrift_empty.db_name = 'sqlite:///../sqlite_agdrift_distance.db'
            agdrift_empty.db_table = 'output'
            #agdrift_empty.db_name = 'sqlite_agdrift_distance.db'
            #this is the list of scenario names (column names) in sql db (the order here is important because
            #the expected values are ordered in this manner
            agdrift_empty.scenario_name = ['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                           'ground_low_vf', 'ground_low_fmc', 'ground_high_vf', 'ground_high_fmc',
                                           'airblast_normal', 'airblast_dense', 'airblast_sparse', 'airblast_vineyard',
                                           'airblast_orchard']

            #cycle through reading scenarios and building result list
            for i in range(len(agdrift_empty.scenario_name)):
                #get scenario data
                scenario_data = agdrift_empty.get_scenario_deposition_data(agdrift_empty.scenario_name[i],
                                                                              agdrift_empty.num_db_values)
                print(scenario_data)
                #extract 1st and last values of scenario data and build result list (including how many values are
                #retrieved for each scenario
                if i == 0:
                    #fix this
                    result = [scenario_data[0], scenario_data[agdrift_empty.num_db_values - 1],
                              float(len(scenario_data))]
                else:
                    result.extend([scenario_data[0], scenario_data[agdrift_empty.num_db_values - 1],
                              float(len(scenario_data))])
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_get_column_names(self):
        """
        :description retrieves column names from sql database (sqlite_agdrift_distance.db)
        :            (each column name refers to a specific deposition scenario;
        :             the scenario name is used later to retrieve the deposition data)
        :parameter output name of sql database table from which to retrieve requested data
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.db_name = 'sqlite:///../sqlite_agdrift_distance.db'
        agdrift_empty.db_table = 'output'

        result = pd.Series([], dtype='object')
        expected_result = ['distance_ft','aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                           'ground_low_vf', 'ground_low_fmc', 'ground_high_vf', 'ground_high_fmc',
                                           'airblast_normal', 'airblast_dense', 'airblast_sparse', 'airblast_vineyard',
                                           'airblast_orchard']

        try:
            result = agdrift_empty.get_column_names()
            npt.assert_array_equal(result, expected_result, err_msg="", verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_filter_arrays(self):
        """
        :description  eliminate blank data cells (i.e., distances for which no deposition value is provided)
                     (and thus reduce the number of x,y values to be used)
        :parameter x_in: array of distance values associated with values for a deposition scenario (e.g., Aerial/EPA Defined Pond)
        :parameter y_in: array of deposition values associated with a deposition scenario (e.g., Aerial/EPA Defined Pond)
        :parameter x_out: processed array of x_in values eliminating indices of blank distance/deposition values
        :parameter y_out: processed array of y_in values eliminating indices of blank distance/deposition values
        :NOTE y_in array is assumed to be populated by values >= 0. except for the blanks as 'nan' entries
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([0.,1.,4.,5.,6.,7.], dtype='float')
        expected_result_y = pd.Series([10.,11.,14.,15.,16.,17.], dtype='float')

        try:
            x_in = pd.Series([0.,1.,2.,3.,4.,5.,6.,7.], dtype='float')
            y_in = pd.Series([10.,11.,'nan','nan',14.,15.,16.,17.], dtype='float')
            x_out, y_out = agdrift_empty.filter_arrays(x_in, y_in)
            result_x = x_out
            result_y = y_out
            npt.assert_allclose(result_x, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(result_y, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result_x, expected_result_x]
            tab = [result_y, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_list_sims_per_scenario(self):
        """
        :description scan simulations and count number and indices of simulations that apply to each scenario
        :parameter num_scenarios number of deposition scenarios included in SQL database
        :parameter num_simulations number of simulations included in this model execution
        :parameter scenario_name name of deposition scenario as recorded in SQL database
        :parameter out_sim_scenario_id identification of deposition scenario specified per model run simulation
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_num_sims = pd.Series([2,2,2,2,2,2,2,2,2,2,2,2,2], dtype='int')
        expected_sim_indices = pd.Series([[0,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [1,14,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [2,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [3,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [4,17,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [5,18,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [6,19,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [7,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [8,21,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [9,22,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [10,23,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [11,24,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                                          [12,25,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], dtype='int')

        try:

            agdrift_empty.scenario_name = pd.Series(['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                           'ground_low_vf', 'ground_low_fmc', 'ground_high_vf', 'ground_high_fmc',
                                           'airblast_normal', 'airblast_dense', 'airblast_sparse', 'airblast_vineyard',
                                           'airblast_orchard'], dtype='object')
            agdrift_empty.out_sim_scenario_id = pd.Series(['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                           'ground_low_vf', 'ground_low_fmc', 'ground_high_vf', 'ground_high_fmc',
                                           'airblast_normal', 'airblast_dense', 'airblast_sparse', 'airblast_vineyard',
                                           'airblast_orchard','aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                           'ground_low_vf', 'ground_low_fmc', 'ground_high_vf', 'ground_high_fmc',
                                           'airblast_normal', 'airblast_dense', 'airblast_sparse', 'airblast_vineyard',
                                           'airblast_orchard'], dtype='object')

            agdrift_empty.num_simulations = len(agdrift_empty.out_sim_scenario_id)
            agdrift_empty.num_scenarios = len(agdrift_empty.scenario_name)

            result_num_sims, result_sim_indices = agdrift_empty.list_sims_per_scenario()
            npt.assert_array_equal(result_num_sims, expected_num_sims, err_msg='', verbose=True)
            npt.assert_array_equal(result_sim_indices, expected_sim_indices, err_msg='', verbose=True)
        finally:
            tab = [result_num_sims, expected_num_sims, result_sim_indices, expected_sim_indices]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_determine_area_dimensions(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_width = pd.Series([208.7, 208.7, 100., 400., 150., 0.], dtype='float')
        expected_length = pd.Series([515.8, 515.8, 1076.39, 269.098, 717.593, 0.], dtype='float')
        expected_depth = pd.Series([6.56, 0.4921, 7., 23., 0., 0.], dtype='float')

        try:
            agdrift_empty.ecosystem_type = pd.Series(['Aquatic Assessment',
                                                      'Aquatic Assessment',
                                                      'Aquatic Assessment',
                                                      'Aquatic Assessment',
                                                      'Terrestrial Assessment',
                                                      'Terrestrial Assessment'], dtype='object')
            agdrift_empty.aquatic_body_type = pd.Series(['EPA Defined Pond',
                                                         'EPA Defined Wetland',
                                                         'User Defined Pond',
                                                         'User Defined Wetland',
                                                         'NaN',
                                                         'NaN'], dtype='object')
            agdrift_empty.terrestrial_field_type = pd.Series(['NaN',
                                                              'NaN',
                                                              'NaN',
                                                              'NaN',
                                                              'User Defined Terrestrial',
                                                              'EPA Defined Terrestrial'], dtype='object')
            num_simulations = len(agdrift_empty.ecosystem_type)

            agdrift_empty.default_width = 208.7
            agdrift_empty.default_length = 515.8
            agdrift_empty.default_pond_depth = 6.56
            agdrift_empty.default_wetland_depth = 0.4921

            agdrift_empty.user_pond_width = pd.Series(['NaN', 'NaN', 100., 'NaN', 'NaN', 'NaN'], dtype='float')
            agdrift_empty.user_pond_depth = pd.Series(['NaN', 'NaN', 7., 'NaN', 'NaN', 'NaN'], dtype='float')
            agdrift_empty.user_wetland_width = pd.Series(['NaN', 'NaN', 'NaN', 400., 'NaN', 'NaN'], dtype='float')
            agdrift_empty.user_wetland_depth = pd.Series(['NaN','NaN', 'NaN', 23., 'NaN', 'NaN'], dtype='float')
            agdrift_empty.user_terrestrial_width = pd.Series(['NaN', 'NaN', 'NaN', 'NaN', 150., 'NaN'], dtype='float')

            width_result = pd.Series(num_simulations * ['NaN'], dtype='float')
            length_result = pd.Series(num_simulations * ['NaN'], dtype='float')
            depth_result = pd.Series(num_simulations * ['NaN'], dtype='float')
            agdrift_empty.out_area_width = pd.Series(num_simulations * ['nan'], dtype='float')
            agdrift_empty.out_area_length = pd.Series(num_simulations * ['nan'], dtype='float')
            agdrift_empty.out_area_depth = pd.Series(num_simulations * ['nan'], dtype='float')

            agdrift_empty.sqft_per_hectare = 107639

            for i in range(num_simulations):
                width_result[i], length_result[i], depth_result[i] = agdrift_empty.determine_area_dimensions(i)

            npt.assert_allclose(width_result, expected_width, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(length_result, expected_length, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(depth_result, expected_depth, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [width_result, expected_width, length_result, expected_length, depth_result, expected_depth]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_foa(self):
        """
        :description calculation of average deposition over width of water body
        :param integration_result result of integration of deposition curve across the distance
        :                         beginning at the near distance and extending to the far distance of the water body
        :param integration_distance effectively the width of the water body
        :param avg_dep_foa  average deposition rate across the width of the water body
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([0.1538462, 0.5, 240.])

        try:
            integration_result = pd.Series([1.,125.,3e5], dtype='float')
            integration_distance = pd.Series([6.5,250.,1250.], dtype='float')

            result = agdrift_empty.calc_avg_dep_foa(integration_result, integration_distance)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_lbac(self):
        """
        Deposition calculation.
        :param avg_dep_foa: average deposition over width of water body as fraction of applied
        :param application_rate: actual application rate
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([6.5, 3.125e4, 3.75e8])

        try:
            avg_dep_foa = pd.Series([1.,125.,3e5], dtype='float')
            application_rate = pd.Series([6.5,250.,1250.], dtype='float')

            result = agdrift_empty.calc_avg_dep_lbac(avg_dep_foa, application_rate)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_foa_from_lbac(self):
        """
        Deposition calculation.
        :param avg_dep_foa: average deposition over width of water body as fraction of applied
        :param application_rate: actual application rate
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([1.553846e-01, 8.8e-06, 4.e-08])

        try:
            avg_dep_lbac = pd.Series([1.01, 0.0022, 0.00005], dtype='float')
            application_rate = pd.Series([6.5,250.,1250.], dtype='float')

            result = agdrift_empty.calc_avg_dep_foa_from_lbac(avg_dep_lbac, application_rate)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_lbac_from_gha(self):
        """
        Deposition calculation.
        :param avg_dep_gha: average deposition over width of water body in units of grams/hectare
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param acres_per_hectare: conversion factor to convert hectares to acres
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([0.01516739, 0.111524, 0.267659])

        try:
            avg_dep_gha = pd.Series([17., 125., 3e2], dtype='float')
            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.acres_per_hectare = 2.471
            result = agdrift_empty.calc_avg_dep_lbac_from_gha(avg_dep_gha)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_lbac_from_waterconc_ngl(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([2.311455e-05, 2.209479e-03, 2.447423e-03])

        try:
            avg_waterconc_ngl = pd.Series([17., 125., 3e2], dtype='float')
            area_width = pd.Series([50., 200., 500.], dtype='float')
            area_length = pd.Series([6331., 538., 215.], dtype='float')
            area_depth = pd.Series([0.5, 6.5, 3.], dtype='float')
            agdrift_empty.liters_per_ft3 = 28.3168
            agdrift_empty.sqft_per_acre = 43560.
            agdrift_empty.ng_per_gram = 1.e9
            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.acres_per_hectare = 2.471
            result = agdrift_empty.calc_avg_dep_lbac_from_waterconc_ngl(avg_waterconc_ngl, area_width,
                                                                        area_length, area_depth)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_lbac_from_mgcm2(self):
        """
        :description calculate the average deposition of pesticide over the terrestrial field in lbs/acre
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param area_depth: average depth of water body
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param mg_per_gram conversion factor
        :param sqft_per_acre conversion factor
        :param cm2_per_ft2 conversion factor
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([2.676538e-02, 2.2304486, 44.608973])

        try:

            avg_fielddep_mgcm2 = pd.Series([3.e-4, 2.5e-2, 5.e-01])
            agdrift_empty.sqft_per_acre = 43560.
            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.cm2_per_ft2 = 929.03
            agdrift_empty.mg_per_gram = 1.e3
            result = agdrift_empty.calc_avg_dep_lbac_from_mgcm2(avg_fielddep_mgcm2)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_dep_gha(self):
        """
        :description average deposition over width of water body in grams per acre
        :param avg_dep_lbac: average deposition over width of water body in lbs per acre
        :param gms_per_lb: conversion factor to convert lbs to grams
        :param acres_per_hectare: conversion factor to convert acres to hectares
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([1.401061, 0.3648362, 0.03362546])

        try:
            avg_dep_lbac = pd.Series([1.25e-3,3.255e-4,3e-5], dtype='float')
            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.acres_per_hectare = 2.47105

            result = agdrift_empty.calc_avg_dep_gha(avg_dep_lbac)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_waterconc_ngl(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([70.07119, 18.24654, 22.41823])

        try:
            avg_dep_lbac = pd.Series([1.25e-3,3.255e-4,3e-5], dtype='float')
            area_width = pd.Series([6.56, 208.7, 997.], dtype='float')
            area_length = pd.Series([1.640838e4, 515.7595, 107.9629], dtype='float')
            area_depth = pd.Series([6.56, 6.56, 0.4921], dtype='float')

            agdrift_empty.ng_per_gram = 1.e9
            agdrift_empty.liters_per_ft3 = 28.3168
            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.sqft_per_acre = 43560.


            result = agdrift_empty.calc_avg_waterconc_ngl(avg_dep_lbac ,area_width, area_length, area_depth)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_fielddep_mgcm2(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result = pd.Series([1.401063e-5, 3.648369e-6, 3.362552e-7])

        try:
            avg_dep_lbac = pd.Series([1.25e-3,3.255e-4,3e-5], dtype='float')

            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.sqft_per_acre = 43560.
            agdrift_empty.mg_per_gram = 1.e3
            agdrift_empty.cm2_per_ft2 = 929.03

            result = agdrift_empty.calc_avg_fielddep_mgcm2(avg_dep_lbac)
            npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_generate_running_avg(self):
        """
        :description retrieves values for distance and the first deposition scenario from the sql database
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE any blank fields are filled with 'nan'
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.db_name = 'sqlite:///../sqlite_agdrift_distance.db'
        agdrift_empty.db_table = 'output'

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')
        expected_result_npts = pd.Series([], dtype='object')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,0.102525,0.20505,0.4101,0.8202,1.6404,3.2808,4.9212,6.5616,9.8424,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016]


            expected_result_y = [0.364712246,0.351507467,0.339214283,0.316974687,0.279954504,0.225948786,0.159949625,
                                 0.123048839,0.099781801,0.071666234,0.056352938,0.03860139,0.029600805,0.024150524,
                                 0.020550354,0.01795028,0.015967703,0.014467663,0.013200146,0.01215011,0.011300098,
                                 0.010550085,0.009905072,0.009345065,0.008845057,0.008400051,0.008000046,0.007635043,
                                 0.007300039,0.007000034,0.006725033,0.00646503,0.006230027,0.006010027,0.005805023,
                                 0.005615023,0.005435021,0.00527002,0.00511002,0.004960017,0.004820017,0.004685016,
                                 0.004560015,0.004440015,0.004325013,0.004220012,0.004120012,0.004020012,0.003925011,
                                 0.003835011,0.00375001,0.00367001,0.00359001,0.00351001,0.003435009,0.003365009,
                                 0.003300007,0.003235009,0.003170007,0.003110007,0.003055006,0.003000007,0.002945006,
                                 0.002895006,0.002845006,0.002795006,0.002745006,0.002695006,0.002650005,0.002610005,
                                 0.002570005,0.002525006,0.002485004,0.002450005,0.002410005,0.002370005,0.002335004,
                                 0.002300005,0.002265004,0.002235004,0.002205004,0.002175004,0.002145004,0.002115004,
                                 0.002085004,0.002055004,0.002025004,0.002000002,0.001975004,0.001945004,0.001920002,
                                 0.001900002,0.001875004,0.001850002,0.001830002,0.001805004,0.001780002,0.001760002,
                                 0.001740002,0.001720002,0.001700002,0.001680002,0.001660002,0.001640002,0.001620002,
                                 0.001605001,0.001590002,0.001570002,0.001550002,0.001535001,0.001520002,0.001500002,
                                 0.001485001,0.001470002,0.001455001,0.001440002,0.001425001,0.001410002,0.001395001,
                                 0.001385001,0.001370002,0.001355001,0.001340002,0.001325001,0.001315001,0.001305001,
                                 0.001290002,0.001275001,0.001265001,0.001255001,0.001245001,0.001230002,0.001215001,
                                 0.001205001,0.001195001,0.001185001,0.001175001,0.001165001,0.001155001,0.001145001,
                                 0.001135001,0.001125001,0.001115001,0.001105001,0.001095001,0.001085001,0.001075001,
                                 0.001065001,0.00106,0.001055001,0.001045001,0.001035001,0.001025001,0.001015001,
                                 0.001005001,0.0009985,0.000993001,0.000985001,0.000977001,0.000969501]

            expected_result_npts = 160

            x_dist = 6.56
            agdrift_empty.distance_name = 'distance_ft'
            agdrift_empty.scenario_name = 'ground_low_vf'
            agdrift_empty.num_db_values = 161

            x_array_in = agdrift_empty.get_distances(agdrift_empty.num_db_values)
            y_array_in = agdrift_empty.get_scenario_deposition_data(agdrift_empty.scenario_name, agdrift_empty.num_db_values)

            x_array_out, y_array_out, npts_out = agdrift_empty.generate_running_avg(agdrift_empty.num_db_values,
                                                                                    x_array_in, y_array_in, x_dist)
            # write output arrays to excel file  --  just for debugging
            agdrift_empty.write_arrays_to_csv(x_array_out, y_array_out, "output_array_generate.csv")
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_generate_running_avg1(self):
        """
        :description creates a running average for a specified x axis width (e.g., 7-day average values of an array)
        :param x_array_in: array of x-axis values
        :param y_array_in: array of y-axis values
        :param num_db_values: number of points in the input arrays
        :param x_array_out: array of x-zxis values in output array
        :param y_array_out: array of y-axis values in output array
        :param npts_out: number of points in the output array
        :param x_dist: width in x_axis units of running weighted average
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE This test uses a uniformly spaced x_array and monotonically increasing y_array
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')
        expected_result_npts = pd.Series([], dtype='object')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                                 11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                                 21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                                 31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                                 41.,42.,43.,44.]
            expected_result_y = [2.5,3.5,4.5,5.5,6.5,7.5,8.5,9.5,10.5,11.5,
                                 12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,
                                 22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,
                                 32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5,40.5,41.5,
                                 42.5,43.5,44.5,45.5, 46.5]
            expected_result_npts = 45

            x_dist = 5.
            num_db_values = 51
            x_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                               11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                               21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                               31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                               41.,42.,43.,44.,45.,46.,47.,48.,49.,50.]
            y_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                               11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                               21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                               31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                               41.,42.,43.,44.,45.,46.,47.,48.,49.,50.]

            x_array_out, y_array_out, npts_out = agdrift_empty.generate_running_avg(num_db_values, x_array_in,
                                                                                    y_array_in, x_dist)
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_generate_running_avg2(self):
        """
        :description creates a running average for a specified x axis width (e.g., 7-day average values of an array)
        :param x_array_in: array of x-axis values
        :param y_array_in: array of y-axis values
        :param num_db_values: number of points in the input arrays
        :param x_array_out: array of x-zxis values in output array
        :param y_array_out: array of y-axis values in output array
        :param npts_out: number of points in the output array
        :param x_dist: width in x_axis units of running weighted average
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE This test uses a non-uniformly spaced x_array and monotonically increasing y_array
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')
        expected_result_npts = pd.Series([], dtype='object')
        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')


        try:

            expected_result_x = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                                 11.5,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                                 21.5,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                                 31.5,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                                 41.5,42.,43.,44.]
            expected_result_y = [2.5,3.5,4.5,5.5,6.5,7.5,8.4666667,9.4,10.4,11.4,
                                 12.4,13.975,14.5,15.5,16.5,17.5,18.466666667,19.4,20.4,21.4,
                                 22.4,23.975,24.5,25.5,26.5,27.5,28.46666667,29.4,30.4,31.4,
                                 32.4,33.975,34.5,35.5,36.5,37.5,38.466666667,39.4,40.4,41.4,
                                 42.4,43.975,44.5,45.5, 46.5]
            expected_result_npts = 45

            x_dist = 5.
            agdrift_empty.num_db_values = 51
            x_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                               11.5,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                               21.5,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                               31.5,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                               41.5,42.,43.,44.,45.,46.,47.,48.,49.,50.]
            y_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                               11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                               21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                               31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                               41.,42.,43.,44.,45.,46.,47.,48.,49.,50.]

            x_array_out, y_array_out, npts_out = agdrift_empty.generate_running_avg(agdrift_empty.num_db_values,
                                                                                    x_array_in, y_array_in, x_dist)
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_generate_running_avg3(self):
        """
        :description creates a running average for a specified x axis width (e.g., 7-day average values of an array);
                     averages reflect weighted average assuming linearity between x points;
                     average is calculated as the area under the y-curve beginning at each x point and extending out x_dist
                     divided by x_dist (which yields the weighted average y between the relevant x points)
        :param x_array_in: array of x-axis values
        :param y_array_in: array of y-axis values
        :param num_db_values: number of points in the input arrays
        :param x_array_out: array of x-zxis values in output array
        :param y_array_out: array of y-axis values in output array
        :param npts_out: number of points in the output array
        :param x_dist: width in x_axis units of running weighted average
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE This test uses a monotonically increasing y_array and inserts a gap in the x values
              that is greater than x_dist
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')
        expected_result_npts = pd.Series([], dtype='object')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,1.,2.,3.,4.,5.,6.,7.,16.,17.,18.,19.,20.,
                                 21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                                 31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                                 41.,42.,43.,44.,45.,46.,47.,48.,49.,50.,51.,52.]
            expected_result_y = [2.5,3.5,4.5,5.4111111,6.14444444,6.7,7.07777777,7.277777777,10.5,11.5,
                                 12.5,13.5,14.5,15.5,16.5,17.5,18.5,19.5,20.5,21.5,
                                 22.5,23.5,24.5,25.5,26.5,27.5,28.5,29.5,30.5,31.5,
                                 32.5,33.5,34.5,35.5,36.5,37.5,38.5,39.5,40.5,41.5,
                                 42.5,43.5,44.5,45.5, 46.5]
            expected_result_npts = 45

            x_dist = 5.
            num_db_values = 51
            x_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,16.,17.,18.,19.,20.,
                               21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                               31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                               41.,42.,43.,44.,45.,46.,47.,48.,49.,50.,
                               51.,52.,53.,54.,55.,56.,57.,58.]
            y_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                               11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                               21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                               31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                               41.,42.,43.,44.,45.,46.,47.,48.,49.,50.]

            x_array_out, y_array_out, npts_out = agdrift_empty.generate_running_avg(num_db_values, x_array_in,
                                                                                    y_array_in, x_dist)
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print(tabulate(tab2, headers='keys', tablefmt='rst'))

        return

    def test_locate_integrated_avg(self):
        """
        :description retrieves values for distance and the first deposition scenario from the sql database
                     and generates running weighted averages from the first x,y value until it locates the user
                     specified integrated average of interest
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE any blank fields are filled with 'nan'
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.db_name = 'sqlite:///../sqlite_agdrift_distance.db'
        agdrift_empty.db_table = 'output'

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')
        expected_result_npts = pd.Series([], dtype='object')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,0.102525,0.20505,0.4101,0.8202,1.6404,3.2808,4.9212,6.5616,9.8424,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016]


            expected_result_y = [0.364712246,0.351507467,0.339214283,0.316974687,0.279954504,0.225948786,0.159949625,
                                 0.123048839,0.099781801,0.071666234,0.056352938,0.03860139,0.029600805,0.024150524,
                                 0.020550354,0.01795028,0.015967703,0.014467663,0.013200146,0.01215011,0.011300098,
                                 0.010550085,0.009905072,0.009345065,0.008845057,0.008400051,0.008000046,0.007635043,
                                 0.007300039,0.007000034,0.006725033,0.00646503,0.006230027,0.006010027,0.005805023,
                                 0.005615023,0.005435021,0.00527002,0.00511002,0.004960017,0.004820017,0.004685016,
                                 0.004560015,0.004440015,0.004325013,0.004220012,0.004120012,0.004020012,0.003925011,
                                 0.003835011,0.00375001,0.00367001,0.00359001,0.00351001,0.003435009,0.003365009,
                                 0.003300007,0.003235009,0.003170007,0.003110007,0.003055006,0.003000007,0.002945006,
                                 0.002895006,0.002845006,0.002795006,0.002745006,0.002695006,0.002650005,0.002610005,
                                 0.002570005,0.002525006,0.002485004,0.002450005,0.002410005,0.002370005,0.002335004,
                                 0.002300005,0.002265004,0.002235004,0.002205004,0.002175004,0.002145004,0.002115004,
                                 0.002085004,0.002055004,0.002025004,0.002000002,0.001975004,0.001945004,0.001920002,
                                 0.001900002,0.001875004,0.001850002,0.001830002,0.001805004,0.001780002,0.001760002,
                                 0.001740002,0.001720002,0.001700002,0.001680002,0.001660002,0.001640002,0.001620002,
                                 0.001605001,0.001590002,0.001570002,0.001550002,0.001535001,0.001520002,0.001500002,
                                 0.001485001,0.001470002,0.001455001,0.001440002,0.001425001,0.001410002,0.001395001,
                                 0.001385001,0.001370002,0.001355001,0.001340002,0.001325001,0.001315001,0.001305001,
                                 0.001290002,0.001275001,0.001265001,0.001255001,0.001245001,0.001230002,0.001215001,
                                 0.001205001,0.001195001,0.001185001,0.001175001,0.001165001,0.001155001,0.001145001,
                                 0.001135001,0.001125001,0.001115001,0.001105001,0.001095001,0.001085001,0.001075001,
                                 0.001065001,0.00106,0.001055001,0.001045001,0.001035001,0.001025001,0.001015001,
                                 0.001005001,0.0009985,0.000993001,0.000985001,0.000977001,0.000969501]

            expected_result_npts = 160
            expected_x_dist_of_interest = 990.8016


            x_dist = 6.56
            weighted_avg = 0.0009697  #this is the running average value we're looking for
            agdrift_empty.distance_name = 'distance_ft'
            agdrift_empty.scenario_name = 'ground_low_vf'
            agdrift_empty.num_db_values = 161
            agdrift_empty.find_nearest_x = True
            x_array_in = agdrift_empty.get_distances(agdrift_empty.num_db_values)
            y_array_in = agdrift_empty.get_scenario_deposition_data(agdrift_empty.scenario_name, agdrift_empty.num_db_values)

            x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk = \
                agdrift_empty.locate_integrated_avg(agdrift_empty.num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

            npt.assert_array_equal(expected_x_dist_of_interest, x_dist_of_interest, verbose=True)
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} x-units to area and got {1} '.format(expected_x_dist_of_interest, x_dist_of_interest))
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_locate_integrated_avg1(self):
        """
        :description retrieves values for distance and the first deposition scenario from the sql database
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE this test is for a monotonically increasing function with some irregularity in x-axis points
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()


        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,7.0,16.0,17.0,18.0,19.0,20.0,28.0,29.0,30.0,31.]
            expected_result_y = [0.357143,1.27778,4.4125,5.15,5.7125,6.1,6.3125,9.5,10.5,11.5,12.5]
            expected_result_npts = 11
            expected_x_dist_of_interest = 30.5

            x_dist = 5.
            weighted_avg = 12.
            num_db_values = 51
            x_array_in = [0.,7.,16.,17.,18.,19.,20.,28.,29.,30.,
                          31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                          41.,42.,43.,44.,45.,46.,47.,48.,49.,50.,
                          51.,52.,53.,54.,55.,56.,57.,58.,59.,60.,
                          61.,62.,63.,64.,65.,66.,67.,68.,69.,70.,
                          71.]
            y_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,
                          11.,12.,13.,14.,15.,16.,17.,18.,19.,20.,
                          21.,22.,23.,24.,25.,26.,27.,28.,29.,30.,
                          31.,32.,33.,34.,35.,36.,37.,38.,39.,40.,
                          41.,42.,43.,44.,45.,46.,47.,48.,49.,50.]
            agdrift_empty.find_nearest_x = True

            x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk = \
                agdrift_empty.locate_integrated_avg(num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

            npt.assert_array_equal(expected_x_dist_of_interest, x_dist_of_interest, verbose=True)
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} x-units to area and got {1} '.format(expected_x_dist_of_interest, x_dist_of_interest))
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))

        return

    def test_locate_integrated_avg2(self):
        """
        :description retrieves values for distance and the first deposition scenario from the sql database
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE This test is for a monotonically decreasing function with irregular x-axis spacing
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,7.,16.,17.,18.,19.,20.,28.,29.,30.,
                                34.,35.,36.,37.,38.,39.,40.,
                                41.,42.,43.,44.,45.,46.,47.,48.,49.,50.,
                                51.,52.,53.,54.,55.,56.,57.,58.,59.,60.]
            expected_result_y = [49.6429,48.7222,45.5875,44.85,44.2875,43.9,43.6875,41.175,40.7,40.3,
                                 37.5,36.5,35.5,34.5,33.5,32.5,31.5,30.5,29.5,28.5,
                                 27.5,26.5,25.5,24.5,23.5,22.5,21.5,20.5,19.5,18.5,
                                 17.5,16.5,15.5,14.5,13.5,12.5,11.5]
            expected_result_npts = 37
            expected_x_dist_of_interest = 60.

            x_dist = 5.
            weighted_avg = 12.
            num_db_values = 51
            agdrift_empty.find_nearest_x = True

            x_array_in = [0.,7.,16.,17.,18.,19.,20.,28.,29.,30.,
                          34.,35.,36.,37.,38.,39.,40.,
                          41.,42.,43.,44.,45.,46.,47.,48.,49.,50.,
                          51.,52.,53.,54.,55.,56.,57.,58.,59.,60.,
                          61.,62.,63.,64.,65.,66.,67.,68.,69.,70.,
                          71.,72.,73.,74. ]
            y_array_in = [50.,49.,48.,47.,46.,45.,44.,43.,42.,41.,
                          40.,39.,38.,37.,36.,35.,34.,33.,32.,31.,
                          30.,29.,28.,27.,26.,25.,24.,23.,22.,21.,
                          20.,19.,18.,17.,16.,15.,14.,13.,12.,11.,
                          10.,9.,8.,7.,6.,5.,4.,3.,2.,1.,0.]

            x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk = \
                agdrift_empty.locate_integrated_avg(num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

            npt.assert_array_equal(expected_x_dist_of_interest, x_dist_of_interest, verbose=True)
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} x-units to area and got {1} '.format(expected_x_dist_of_interest, x_dist_of_interest))
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_locate_integrated_avg3(self):
        """
        :description retrieves values for distance and the first deposition scenario from the sql database
        :param num_db_values: number of distance values to be retrieved
        :param distance_name: name of column in sql database that contains the distance values
        :NOTE this test is for a monotonically decreasing function with regular x-axis spacing
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()


        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')
        expected_result_x_dist = pd.Series([], dtype='float')

        try:

            expected_result_x = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,
                          10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,
                          20.,21.,22.,23.,24.,25.,26.,27.,28.,29.,
                          30.,31.,32.,33.,34.,35.,36.]
            expected_result_y = [47.5,46.5,45.5,44.5,43.5,42.5,41.5,40.5,39.5,38.5,
                                 37.5,36.5,35.5,34.5,33.5,32.5,31.5,30.5,29.5,28.5,
                                 27.5,26.5,25.5,24.5,23.5,22.5,21.5,20.5,19.5,18.5,
                                 17.5,16.5,15.5,14.5,13.5,12.5,11.5]
            expected_result_npts = 37
            expected_x_dist_of_interest = 36.

            x_dist = 5.
            weighted_avg = 12.
            num_db_values = 51
            agdrift_empty.find_nearest_x = True
            x_array_in = [0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,
                          10.,11.,12.,13.,14.,15.,16.,17.,18.,19.,
                          20.,21.,22.,23.,24.,25.,26.,27.,28.,29.,
                          30.,31.,32.,33.,34.,35.,36.,37.,38.,39.,
                          40.,41.,42.,43.,44.,45.,46.,47.,48.,49.,
                          50.]
            y_array_in = [50.,49.,48.,47.,46.,45.,44.,43.,42.,41.,
                          40.,39.,38.,37.,36.,35.,34.,33.,32.,31.,
                          30.,29.,28.,27.,26.,25.,24.,23.,22.,21.,
                          20.,19.,18.,17.,16.,15.,14.,13.,12.,11.,
                          10.,9.,8.,7.,6.,5.,4.,3.,2.,1.,0.]

            x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk = \
                agdrift_empty.locate_integrated_avg(num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

            npt.assert_array_equal(expected_x_dist_of_interest, x_dist_of_interest, verbose=True )
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True )
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} x-units to area and got {1} '.format(expected_x_dist_of_interest, x_dist_of_interest))
            print('expected {0} number of points and got {1} points'.format(expected_result_npts, npts_out))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_round_model_outputs(self):
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
        :param num_sims: number of simulations
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        num_sims = 3
        num_args = 5
        agdrift_empty.out_avg_dep_foa = pd.Series(num_sims * [np.nan], dtype='float')
        agdrift_empty.out_avg_dep_lbac = pd.Series(num_sims * [np.nan], dtype='float')
        agdrift_empty.out_avg_dep_gha = pd.Series(num_sims * [np.nan], dtype='float')
        agdrift_empty.out_avg_waterconc_ngl = pd.Series(num_sims * [np.nan], dtype='float')
        agdrift_empty.out_avg_field_dep_mgcm2 = pd.Series(num_sims * [np.nan], dtype='float')

        result = pd.Series(num_sims * [num_args*[np.nan]], dtype='float')
        expected_result = pd.Series(num_sims * [num_args*[np.nan]], dtype='float')

        expected_result[0] = [1.26,1.26,1.26,1.26,1.26]
        expected_result[1] = [0.0004,0.0004,0.0004,0.0004,0.0004]
        expected_result[2] = [3.45e-05,3.45e-05,3.45e-05,3.45e-05,3.45e-05]

        try:
            #setting each variable to same values, each value tests a separate pathway through rounding method
            avg_dep_lbac = pd.Series([1.2567,3.55e-4,3.454e-5], dtype='float')
            avg_dep_foa = pd.Series([1.2567,3.55e-4,3.454e-5], dtype='float')
            avg_dep_gha = pd.Series([1.2567,3.55e-4,3.454e-5], dtype='float')
            avg_waterconc_ngl = pd.Series([1.2567,3.55e-4,3.454e-5], dtype='float')
            avg_field_dep_mgcm2 = pd.Series([1.2567,3.55e-4,3.454e-5], dtype='float')

            for i in range(num_sims):
                lbac = avg_dep_lbac[i]
                foa = avg_dep_foa[i]
                gha = avg_dep_gha[i]
                ngl = avg_waterconc_ngl[i]
                mgcm2 = avg_field_dep_mgcm2[i]

                agdrift_empty.round_model_outputs(foa, lbac, gha, ngl, mgcm2, i)

                result[i] = [agdrift_empty.out_avg_dep_foa[i], agdrift_empty.out_avg_dep_lbac[i],
                            agdrift_empty.out_avg_dep_gha[i], agdrift_empty.out_avg_waterconc_ngl[i],
                            agdrift_empty.out_avg_field_dep_mgcm2[i]]
            npt.assert_allclose(result[0], expected_result[0], rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(result[1], expected_result[1], rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(result[2], expected_result[2], rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_find_dep_pt_location(self):
        """
        :description this method locates the downwind distance associated with a specific deposition rate
        :param x_array: array of distance values
        :param y_array: array of deposition values
        :param npts: number of values in x/y arrays
        :param foa: value of deposition (y value) of interest
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        result = [[],[],[],[]]
        expected_result = [(0.0, 'in range'), (259.1832, 'in range'), (997.3632, 'in range'), (np.nan, 'out of range')]

        try:

            x_array = [0.,0.102525,0.20505,0.4101,0.8202,1.6404,3.2808,4.9212,6.5616,9.8424,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016, 997.3632]


            y_array = [0.364706389,0.351133211,0.338484161,0.315606383,0.277604029,0.222810736,0.159943507,
                                 0.121479708,0.099778741,0.068653,0.05635,0.0386,0.0296,0.02415,0.02055,0.01795,
                                 0.0159675,0.0144675,0.0132,0.01215,0.0113,0.01055,0.009905,0.009345,0.008845,0.0084,
                                 0.008,0.007635,0.0073,0.007,0.006725,0.006465,0.00623,0.00601,0.005805,0.005615,
                                 0.005435,0.00527,0.00511,0.00496,0.00482,0.004685,0.00456,0.00444,0.004325,0.00422,
                                 0.00412,0.00402,0.003925,0.003835,0.00375,0.00367,0.00359,0.00351,0.003435,0.003365,
                                 0.0033,0.003235,0.00317,0.00311,0.003055,0.003,0.002945,0.002895,0.002845,0.002795,
                                 0.002745,0.002695,0.00265,0.00261,0.00257,0.002525,0.002485,0.00245,0.00241,0.00237,
                                 0.002335,0.0023,0.002265,0.002235,0.002205,0.002175,0.002145,0.002115,0.002085,
                                 0.002055,0.002025,0.002,0.001975,0.001945,0.00192,0.0019,0.001875,0.00185,0.00183,
                                 0.001805,0.00178,0.00176,0.00174,0.00172,0.0017,0.00168,0.00166,0.00164,0.00162,
                                 0.001605,0.00159,0.00157,0.00155,0.001535,0.00152,0.0015,0.001485,0.00147,0.001455,
                                 0.00144,0.001425,0.00141,0.001395,0.001385,0.00137,0.001355,0.00134,0.001325,0.001315,
                                 0.001305,0.00129,0.001275,0.001265,0.001255,0.001245,0.00123,0.001215,0.001205,
                                 0.001195,0.001185,0.001175,0.001165,0.001155,0.001145,0.001135,0.001125,0.001115,
                                 0.001105,0.001095,0.001085,0.001075,0.001065,0.00106,0.001055,0.001045,0.001035,
                                 0.001025,0.001015,0.001005,0.0009985,0.000993,0.000985,0.000977,0.0009695,0.0009612]
            npts = len(x_array)
            num_sims = 4
            foa = [0.37, 0.004, 0.0009613, 0.0008]

            for i in range(num_sims):
                result[i] = agdrift_empty.find_dep_pt_location(x_array, y_array, npts, foa[i])

            npt.assert_equal(expected_result, result, verbose=True)
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_extend_curve_opp(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        # x_array_in = pd.Series([], dtype='float')
        # y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')


        try:

            expected_result_x = [0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632,
                        1003.9232,1010.4832,1017.0432,1023.6032,1030.1632,1036.7232,1043.2832,1049.8432,1056.4032,
                        1062.9632,1069.5232,1076.0832,1082.6432,1089.2032,1095.7632,1102.3232,1108.8832,1115.4432,
                        1122.0032,1128.5632,1135.1232,1141.6832,1148.2432,1154.8032,1161.3632,1167.9232,1174.4832,
                        1181.0432,1187.6032,1194.1632,1200.7232,1207.2832,1213.8432,1220.4032,1226.9632,1233.5232,
                        1240.0832,1246.6432,1253.2032,1259.7632,1266.3232,1272.8832,1279.4432,1286.0032,1292.5632,
                        1299.1232,1305.6832,1312.2432,1318.8032,1325.3632,1331.9232,1338.4832,1345.0432,1351.6032,
                        1358.1632,1364.7232,1371.2832,1377.8432,1384.4032,1390.9632,1397.5232,1404.0832,1410.6432,
                        1417.2032,1423.7632,1430.3232,1436.8832,1443.4432,1450.0032,1456.5632,1463.1232,1469.6832,
                        1476.2432,1482.8032,1489.3632,1495.9232,1502.4832,1509.0432,1515.6032,1522.1632,1528.7232,
                        1535.2832,1541.8432,1548.4032,1554.9632,1561.5232,1568.0832,1574.6432,1581.2032,1587.7632,
                        1594.3232,1600.8832,1607.4432,1614.0032,1620.5632,1627.1232,1633.6832,1640.2432,1646.8032,
                        1653.3632,1659.9232,1666.4832,1673.0432,1679.6032,1686.1632,1692.7232,1699.2832,1705.8432,
                        1712.4032,1718.9632,1725.5232,1732.0832,1738.6432,1745.2032,1751.7632,1758.3232,1764.8832,
                        1771.4432,1778.0032,1784.5632,1791.1232,1797.6832,1804.2432,1810.8032,1817.3632,1823.9232,
                        1830.4832,1837.0432,1843.6032,1850.1632,1856.7232,1863.2832,1869.8432,1876.4032,1882.9632,
                        1889.5232,1896.0832,1902.6432,1909.2032,1915.7632,1922.3232,1928.8832,1935.4432,1942.0032,
                        1948.5632,1955.1232,1961.6832,1968.2432,1974.8032,1981.3632,1987.9232,1994.4832]
            expected_result_y = [0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741,1.1826345E-02,1.1812256E-02,
                                1.1798945E-02,1.1786331E-02,1.1774344E-02,1.1762927E-02,1.1752028E-02,1.1741602E-02,
                                1.1731610E-02,1.1722019E-02,1.1712796E-02,1.1703917E-02,1.1695355E-02,1.1687089E-02,
                                1.1679100E-02,1.1671370E-02,1.1663883E-02,1.1656623E-02,1.1649579E-02,1.1642737E-02,
                                1.1636087E-02,1.1629617E-02,1.1623319E-02,1.1617184E-02,1.1611203E-02,1.1605369E-02,
                                1.1599676E-02,1.1594116E-02,1.1588684E-02,1.1583373E-02,1.1578179E-02,1.1573097E-02,
                                1.1568122E-02,1.1563249E-02,1.1558475E-02,1.1553795E-02,1.1549206E-02,1.1544705E-02,
                                1.1540288E-02,1.1535953E-02,1.1531695E-02,1.1527514E-02,1.1523405E-02,1.1519367E-02,
                                1.1515397E-02,1.1511493E-02,1.1507652E-02,1.1503873E-02,1.1500154E-02,1.1496493E-02,
                                1.1492889E-02,1.1489338E-02,1.1485841E-02,1.1482395E-02,1.1478999E-02,1.1475651E-02,
                                1.1472351E-02,1.1469096E-02,1.1465886E-02,1.1462720E-02,1.1459595E-02,1.1456512E-02,
                                1.1453469E-02,1.1450465E-02,1.1447499E-02,1.1444570E-02,1.1441677E-02,1.1438820E-02,
                                1.1435997E-02,1.1433208E-02,1.1430452E-02,1.1427728E-02,1.1425036E-02,1.1422374E-02,
                                1.1419742E-02,1.1417139E-02,1.1414566E-02,1.1412020E-02,1.1409502E-02,1.1407011E-02,
                                1.1404546E-02,1.1402107E-02,1.1399693E-02,1.1397304E-02,1.1394939E-02,1.1392598E-02,
                                1.1390281E-02,1.1387986E-02,1.1385713E-02,1.1383463E-02,1.1381234E-02,1.1379026E-02,
                                1.1376840E-02,1.1374673E-02,1.1372527E-02,1.1370400E-02,1.1368292E-02,1.1366204E-02,
                                1.1364134E-02,1.1362082E-02,1.1360048E-02,1.1358032E-02,1.1356033E-02,1.1354052E-02,
                                1.1352087E-02,1.1350139E-02,1.1348207E-02,1.1346291E-02,1.1344390E-02,1.1342505E-02,
                                1.1340635E-02,1.1338781E-02,1.1336941E-02,1.1335115E-02,1.1333304E-02,1.1331507E-02,
                                1.1329723E-02,1.1327954E-02,1.1326197E-02,1.1324454E-02,1.1322724E-02,1.1321007E-02,
                                1.1319303E-02,1.1317611E-02,1.1315931E-02,1.1314263E-02,1.1312608E-02,1.1310964E-02,
                                1.1309332E-02,1.1307711E-02,1.1306101E-02,1.1304503E-02,1.1302915E-02,1.1301339E-02,
                                1.1299773E-02,1.1298218E-02,1.1296673E-02,1.1295138E-02,1.1293614E-02,1.1292099E-02,
                                1.1290594E-02,1.1289100E-02,1.1287614E-02,1.1286139E-02,1.1284672E-02,1.1283215E-02,
                                1.1281767E-02,1.1280328E-02,1.1278898E-02,1.1277477E-02,1.1276065E-02,1.1274661E-02]

            expected_result_npts = [305]
            max_dist = 997.3632
            dist_inc = 6.56
            num_pts_ext = 16
            ln_ln_trans = False  #using the relative ln ln transformation in this test
            agdrift_empty.meters_per_ft = 0.3048

            x_array_in = pd.Series([0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632])
            y_array_in = pd.Series([0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457 ,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741])

            x_array_out, y_array_out = agdrift_empty.extend_curve_opp(x_array_in, y_array_in, max_dist, dist_inc, num_pts_ext,
                                                                  ln_ln_trans)
            npts_out = [len(y_array_out)]
            #print out output arrays for debugging
            agdrift_empty.write_arrays_to_csv(x_array_out, y_array_out, "extend_data.csv")
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts[0], npts_out[0]))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_extend_curve_opp1(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        # x_array_in = pd.Series([], dtype='float')
        # y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')


        try:

            expected_result_x = [0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632,
                        1003.9232,1010.4832,1017.0432,1023.6032,1030.1632,1036.7232,1043.2832,1049.8432,1056.4032,
                        1062.9632,1069.5232,1076.0832,1082.6432,1089.2032,1095.7632,1102.3232,1108.8832,1115.4432,
                        1122.0032,1128.5632,1135.1232,1141.6832,1148.2432,1154.8032,1161.3632,1167.9232,1174.4832,
                        1181.0432,1187.6032,1194.1632,1200.7232,1207.2832,1213.8432,1220.4032,1226.9632,1233.5232,
                        1240.0832,1246.6432,1253.2032,1259.7632,1266.3232,1272.8832,1279.4432,1286.0032,1292.5632,
                        1299.1232,1305.6832,1312.2432,1318.8032,1325.3632,1331.9232,1338.4832,1345.0432,1351.6032,
                        1358.1632,1364.7232,1371.2832,1377.8432,1384.4032,1390.9632,1397.5232,1404.0832,1410.6432,
                        1417.2032,1423.7632,1430.3232,1436.8832,1443.4432,1450.0032,1456.5632,1463.1232,1469.6832,
                        1476.2432,1482.8032,1489.3632,1495.9232,1502.4832,1509.0432,1515.6032,1522.1632,1528.7232,
                        1535.2832,1541.8432,1548.4032,1554.9632,1561.5232,1568.0832,1574.6432,1581.2032,1587.7632,
                        1594.3232,1600.8832,1607.4432,1614.0032,1620.5632,1627.1232,1633.6832,1640.2432,1646.8032,
                        1653.3632,1659.9232,1666.4832,1673.0432,1679.6032,1686.1632,1692.7232,1699.2832,1705.8432,
                        1712.4032,1718.9632,1725.5232,1732.0832,1738.6432,1745.2032,1751.7632,1758.3232,1764.8832,
                        1771.4432,1778.0032,1784.5632,1791.1232,1797.6832,1804.2432,1810.8032,1817.3632,1823.9232,
                        1830.4832,1837.0432,1843.6032,1850.1632,1856.7232,1863.2832,1869.8432,1876.4032,1882.9632,
                        1889.5232,1896.0832,1902.6432,1909.2032,1915.7632,1922.3232,1928.8832,1935.4432,1942.0032,
                        1948.5632,1955.1232,1961.6832,1968.2432,1974.8032,1981.3632,1987.9232,1994.4832]
            expected_result_y = [0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741,1.16941E-02,1.16540E-02,
                                1.16144E-02,1.15752E-02,1.15363E-02,1.14978E-02,1.14597E-02,1.14219E-02,1.13845E-02,
                                1.13475E-02,1.13108E-02,1.12744E-02,1.12384E-02,1.12027E-02,1.11674E-02,1.11323E-02,
                                1.10976E-02,1.10632E-02,1.10291E-02,1.09953E-02,1.09618E-02,1.09286E-02,1.08957E-02,
                                1.08630E-02,1.08307E-02,1.07986E-02,1.07668E-02,1.07353E-02,1.07040E-02,1.06730E-02,
                                1.06423E-02,1.06118E-02,1.05816E-02,1.05516E-02,1.05218E-02,1.04923E-02,1.04631E-02,
                                1.04341E-02,1.04053E-02,1.03767E-02,1.03484E-02,1.03203E-02,1.02924E-02,1.02647E-02,
                                1.02372E-02,1.02100E-02,1.01829E-02,1.01561E-02,1.01295E-02,1.01031E-02,1.00768E-02,
                                1.00508E-02,1.00250E-02,9.99932E-03,9.97386E-03,9.94860E-03,9.92351E-03,9.89861E-03,
                                9.87389E-03,9.84934E-03,9.82498E-03,9.80078E-03,9.77676E-03,9.75291E-03,9.72923E-03,
                                9.70571E-03,9.68236E-03,9.65916E-03,9.63613E-03,9.61326E-03,9.59055E-03,9.56799E-03,
                                9.54558E-03,9.52332E-03,9.50122E-03,9.47926E-03,9.45745E-03,9.43578E-03,9.41426E-03,
                                9.39287E-03,9.37163E-03,9.35053E-03,9.32957E-03,9.30874E-03,9.28804E-03,9.26748E-03,
                                9.24705E-03,9.22675E-03,9.20657E-03,9.18653E-03,9.16661E-03,9.14682E-03,9.12714E-03,
                                9.10760E-03,9.08817E-03,9.06886E-03,9.04967E-03,9.03060E-03,9.01164E-03,8.99280E-03,
                                8.97407E-03,8.95546E-03,8.93696E-03,8.91856E-03,8.90028E-03,8.88210E-03,8.86404E-03,
                                8.84608E-03,8.82822E-03,8.81047E-03,8.79282E-03,8.77527E-03,8.75782E-03,8.74048E-03,
                                8.72323E-03,8.70608E-03,8.68903E-03,8.67208E-03,8.65522E-03,8.63845E-03,8.62178E-03,
                                8.60521E-03,8.58872E-03,8.57233E-03,8.55602E-03,8.53981E-03,8.52368E-03,8.50765E-03,
                                8.49170E-03,8.47583E-03,8.46005E-03,8.44436E-03,8.42875E-03,8.41323E-03,8.39778E-03,
                                8.38242E-03,8.36714E-03,8.35194E-03,8.33682E-03,8.32178E-03,8.30682E-03,8.29193E-03,
                                8.27713E-03,8.26240E-03,8.24774E-03,8.23316E-03,8.21866E-03,8.20422E-03,8.18987E-03,
                                8.17558E-03,8.16137E-03,8.14722E-03]

            expected_result_npts = [305]
            max_dist = 997.3632
            dist_inc = 6.56
            num_pts_ext = 16
            ln_ln_trans = True  #using the absolute ln ln transformation in this test
            agdrift_empty.meters_per_ft = 0.3048

            x_array_in = pd.Series([0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632])
            y_array_in = pd.Series([0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741])

            x_array_out, y_array_out = agdrift_empty.extend_curve_opp(x_array_in, y_array_in, max_dist, dist_inc, num_pts_ext,
                                                                  ln_ln_trans)
            npts_out = [len(y_array_out)]
            #print out output arrays for debugging
            agdrift_empty.write_arrays_to_csv(x_array_out, y_array_out, "extend_data.csv")
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts[0], npts_out[0]))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_extend_curve(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        # x_array_in = pd.Series([], dtype='float')
        # y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')


        try:

            expected_result_x = [0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632,
                        1003.9232,1010.4832,1017.0432,1023.6032,1030.1632,1036.7232,1043.2832,1049.8432,1056.4032,
                        1062.9632,1069.5232,1076.0832,1082.6432,1089.2032,1095.7632,1102.3232,1108.8832,1115.4432,
                        1122.0032,1128.5632,1135.1232,1141.6832,1148.2432,1154.8032,1161.3632,1167.9232,1174.4832,
                        1181.0432,1187.6032,1194.1632,1200.7232,1207.2832,1213.8432,1220.4032,1226.9632,1233.5232,
                        1240.0832,1246.6432,1253.2032,1259.7632,1266.3232,1272.8832,1279.4432,1286.0032,1292.5632,
                        1299.1232,1305.6832,1312.2432,1318.8032,1325.3632,1331.9232,1338.4832,1345.0432,1351.6032,
                        1358.1632,1364.7232,1371.2832,1377.8432,1384.4032,1390.9632,1397.5232,1404.0832,1410.6432,
                        1417.2032,1423.7632,1430.3232,1436.8832,1443.4432,1450.0032,1456.5632,1463.1232,1469.6832,
                        1476.2432,1482.8032,1489.3632,1495.9232,1502.4832,1509.0432,1515.6032,1522.1632,1528.7232,
                        1535.2832,1541.8432,1548.4032,1554.9632,1561.5232,1568.0832,1574.6432,1581.2032,1587.7632,
                        1594.3232,1600.8832,1607.4432,1614.0032,1620.5632,1627.1232,1633.6832,1640.2432,1646.8032,
                        1653.3632,1659.9232,1666.4832,1673.0432,1679.6032,1686.1632,1692.7232,1699.2832,1705.8432,
                        1712.4032,1718.9632,1725.5232,1732.0832,1738.6432,1745.2032,1751.7632,1758.3232,1764.8832,
                        1771.4432,1778.0032,1784.5632,1791.1232,1797.6832,1804.2432,1810.8032,1817.3632,1823.9232,
                        1830.4832,1837.0432,1843.6032,1850.1632,1856.7232,1863.2832,1869.8432,1876.4032,1882.9632,
                        1889.5232,1896.0832,1902.6432,1909.2032,1915.7632,1922.3232,1928.8832,1935.4432,1942.0032,
                        1948.5632,1955.1232,1961.6832,1968.2432,1974.8032,1981.3632,1987.9232,1994.4832]
            expected_result_y = [0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741,0.011695283,0.01165546,
                                0.011616029,0.011576983,0.011538317,0.011500024,0.011462099,0.011424535,0.011387327,
                                0.01135047,0.011313958,0.011277785,0.011241946,0.011206437,0.011171253,0.011136388,
                                0.011101837,0.011067597,0.011033662,0.011000028,0.010966691,0.010933646,0.010900889,
                                0.010868416,0.010836222,0.010804305,0.01077266,0.010741283,0.01071017,0.010679318,
                                0.010648723,0.010618382,0.010588291,0.010558447,0.010528846,0.010499485,0.010470361,
                                0.010441471,0.010412812,0.010384381,0.010356174,0.010328189,0.010300423,0.010272873,
                                0.010245536,0.01021841,0.010191491,0.010164778,0.010138268,0.010111958,0.010085846,
                                0.010059928,0.010034204,0.01000867,0.009983324,0.009958164,0.009933188,0.009908393,
                                0.009883777,0.009859339,0.009835075,0.009810984,0.009787064,0.009763313,0.009739729,
                                0.00971631,0.009693054,0.00966996,0.009647024,0.009624247,0.009601625,0.009579157,
                                0.009556841,0.009534676,0.009512659,0.009490791,0.009469067,0.009447488,0.009426051,
                                0.009404755,0.009383599,0.00936258,0.009341698,0.00932095,0.009300337,0.009279855,
                                0.009259504,0.009239282,0.009219188,0.009199221,0.009179379,0.009159662,0.009140066,
                                0.009120593,0.009101239,0.009082005,0.009062888,0.009043888,0.009025004,0.009006234,
                                0.008987576,0.008969031,0.008950597,0.008932272,0.008914057,0.008895949,0.008877947,
                                0.008860051,0.00884226,0.008824572,0.008806987,0.008789503,0.00877212,0.008754837,
                                0.008737652,0.008720565,0.008703575,0.008686681,0.008669882,0.008653177,0.008636566,
                                0.008620047,0.008603619,0.008587282,0.008571035,0.008554878,0.008538808,0.008522826,
                                0.008506931,0.008491122,0.008475398,0.008459758,0.008444202,0.008428729,0.008413338,
                                0.008398029,0.0083828,0.008367652,0.008352583,0.008337592,0.00832268,0.008307845,
                                0.008293086,0.008278404,0.008263797,0.008249265,0.008234806,0.008220422,0.00820611,
                                0.00819187,0.008177702,0.008163606]

            expected_result_npts = [305]
            max_dist = 997.3632
            dist_inc = 6.56
            num_pts_ext = 15
            ln_ln_trans = True

            x_array_in = pd.Series([0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632])
            y_array_in = pd.Series([0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741])

            x_array_out, y_array_out = agdrift_empty.extend_curve(x_array_in, y_array_in, max_dist, dist_inc, num_pts_ext,
                                                                  ln_ln_trans)
            npts_out = [len(y_array_out)]
            #print out output arrays for debugging
            agdrift_empty.write_arrays_to_csv(x_array_out, y_array_out, "extend_data.csv")
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts[0], npts_out[0]))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

    def test_extend_curve1(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        expected_result_x = pd.Series([], dtype='float')
        expected_result_y = pd.Series([], dtype='float')

        # x_array_in = pd.Series([], dtype='float')
        # y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')


        try:

            expected_result_x = [0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632,
                        1003.9232,1010.4832,1017.0432,1023.6032,1030.1632,1036.7232,1043.2832,1049.8432,1056.4032,
                        1062.9632,1069.5232,1076.0832,1082.6432,1089.2032,1095.7632,1102.3232,1108.8832,1115.4432,
                        1122.0032,1128.5632,1135.1232,1141.6832,1148.2432,1154.8032,1161.3632,1167.9232,1174.4832,
                        1181.0432,1187.6032,1194.1632,1200.7232,1207.2832,1213.8432,1220.4032,1226.9632,1233.5232,
                        1240.0832,1246.6432,1253.2032,1259.7632,1266.3232,1272.8832,1279.4432,1286.0032,1292.5632,
                        1299.1232,1305.6832,1312.2432,1318.8032,1325.3632,1331.9232,1338.4832,1345.0432,1351.6032,
                        1358.1632,1364.7232,1371.2832,1377.8432,1384.4032,1390.9632,1397.5232,1404.0832,1410.6432,
                        1417.2032,1423.7632,1430.3232,1436.8832,1443.4432,1450.0032,1456.5632,1463.1232,1469.6832,
                        1476.2432,1482.8032,1489.3632,1495.9232,1502.4832,1509.0432,1515.6032,1522.1632,1528.7232,
                        1535.2832,1541.8432,1548.4032,1554.9632,1561.5232,1568.0832,1574.6432,1581.2032,1587.7632,
                        1594.3232,1600.8832,1607.4432,1614.0032,1620.5632,1627.1232,1633.6832,1640.2432,1646.8032,
                        1653.3632,1659.9232,1666.4832,1673.0432,1679.6032,1686.1632,1692.7232,1699.2832,1705.8432,
                        1712.4032,1718.9632,1725.5232,1732.0832,1738.6432,1745.2032,1751.7632,1758.3232,1764.8832,
                        1771.4432,1778.0032,1784.5632,1791.1232,1797.6832,1804.2432,1810.8032,1817.3632,1823.9232,
                        1830.4832,1837.0432,1843.6032,1850.1632,1856.7232,1863.2832,1869.8432,1876.4032,1882.9632,
                        1889.5232,1896.0832,1902.6432,1909.2032,1915.7632,1922.3232,1928.8832,1935.4432,1942.0032,
                        1948.5632,1955.1232,1961.6832,1968.2432,1974.8032,1981.3632,1987.9232,1994.4832]
            expected_result_y = [0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741,0.011826349,0.011812263,
                                0.011798955,0.011786343,0.011774359,0.011762944,0.011752047,0.011741623,0.011731633,
                                0.011722043,0.011712822,0.011703943,0.011695383,0.011687118,0.01167913,0.011671401,
                                0.011663915,0.011656656,0.011649613,0.011642772,0.011636122,0.011629653,0.011623356,
                                0.011617221,0.011611241,0.011605408,0.011599715,0.011594155,0.011588724,0.011583413,
                                0.01157822,0.011573138,0.011568163,0.011563291,0.011558517,0.011553838,0.011549249,
                                0.011544748,0.011540332,0.011535997,0.01153174,0.011527558,0.01152345,0.011519412,
                                0.011515442,0.011511538,0.011507698,0.011503919,0.011500201,0.01149654,0.011492935,
                                0.011489385,0.011485888,0.011482442,0.011479046,0.011475699,0.011472399,0.011469144,
                                0.011465934,0.011462768,0.011459644,0.011456561,0.011453518,0.011450514,0.011447548,
                                0.011444619,0.011441727,0.011438869,0.011436047,0.011433258,0.011430502,0.011427778,
                                0.011425086,0.011422424,0.011419792,0.01141719,0.011414616,0.011412071,0.011409553,
                                0.011407062,0.011404597,0.011402158,0.011399744,0.011397355,0.01139499,0.01139265,
                                0.011390332,0.011388037,0.011385765,0.011383515,0.011381286,0.011379078,0.011376891,
                                0.011374725,0.011372579,0.011370452,0.011368344,0.011366256,0.011364186,0.011362134,
                                0.011360101,0.011358085,0.011356086,0.011354104,0.01135214,0.011350191,0.011348259,
                                0.011346343,0.011344443,0.011342558,0.011340688,0.011338834,0.011336994,0.011335168,
                                0.011333357,0.01133156,0.011329777,0.011328007,0.011326251,0.011324508,0.011322778,
                                0.011321061,0.011319356,0.011317664,0.011315985,0.011314317,0.011312661,0.011311018,
                                0.011309385,0.011307764,0.011306155,0.011304557,0.011302969,0.011301393,0.011299827,
                                0.011298272,0.011296727,0.011295192,0.011293668,0.011292153,0.011290649,0.011289154,
                                0.011287669,0.011286193,0.011284727,0.011283269,0.011281822,0.011280383,0.011278953,
                                0.011277532,0.011276119,0.011274716]

            expected_result_npts = [305]
            max_dist = 997.3632
            dist_inc = 6.56
            num_pts_ext = 16
            ln_ln_trans = False

            x_array_in = pd.Series([0.,6.5616,13.1232,19.6848,26.2464,
                        32.808,39.3696,45.9312,52.4928,59.0544,65.616,72.1776,78.7392,85.3008,91.8624,98.424,104.9856,
                        111.5472,118.1088,124.6704,131.232,137.7936,144.3552,150.9168,157.4784,164.04,170.6016,177.1632,
                        183.7248,190.2864,196.848,203.4096,209.9712,216.5328,223.0944,229.656,236.2176,242.7792,249.3408,
                        255.9024,262.464,269.0256,275.5872,282.1488,288.7104,295.272,301.8336,308.3952,314.9568,321.5184,
                        328.08,334.6416,341.2032,347.7648,354.3264,360.888,367.4496,374.0112,380.5728,387.1344,393.696,
                        400.2576,406.8192,413.3808,419.9424,426.504,433.0656,439.6272,446.1888,452.7504,459.312,465.8736,
                        472.4352,478.9968,485.5584,492.12,498.6816,505.2432,511.8048,518.3664,524.928,531.4896,538.0512,
                        544.6128,551.1744,557.736,564.2976,570.8592,577.4208,583.9824,590.544,597.1056,603.6672,610.2288,
                        616.7904,623.352,629.9136,636.4752,643.0368,649.5984,656.16,662.7216,669.2832,675.8448,682.4064,
                        688.968,695.5296,702.0912,708.6528,715.2144,721.776,728.3376,734.8992,741.4608,748.0224,754.584,
                        761.1456,767.7072,774.2688,780.8304,787.392,793.9536,800.5152,807.0768,813.6384,820.2,826.7616,
                        833.3232,839.8848,846.4464,853.008,859.5696,866.1312,872.6928,879.2544,885.816,892.3776,898.9392,
                        905.5008,912.0624,918.624,925.1856,931.7472,938.3088,944.8704,951.432,957.9936,964.5552,971.1168,
                        977.6784,984.24,990.8016,997.3632])
            y_array_in = pd.Series([0.49997,0.37451,0.29849,0.25004,0.2138,0.19455,0.18448,0.17591,0.1678,0.15421,0.1401,
                                0.12693,0.11785,0.11144,0.10675,0.099496,0.092323,0.085695,0.079234,0.074253,0.070316,
                                0.067191,0.064594,0.062337,0.060348,0.058192,0.055224,0.051972,0.049283,0.04757,
                                0.046226,0.044969,0.043922,0.043027,0.041934,0.040528,0.039018,0.037744,0.036762,
                                0.035923,0.035071,0.034267,0.033456,0.032629,0.03184,0.031078,0.030363,0.02968,0.029028,
                                0.028399,0.027788,0.027199,0.026642,0.026124,0.025635,0.02517,0.024719,0.024287,0.023867,
                                0.023457,0.023061,0.022685,0.022334,0.021998,0.021675,0.02136,0.021055,0.020758,0.020467,
                                0.020186,0.019919,0.019665,0.019421,0.019184,0.018951,0.018727,0.018514,0.018311,
                                0.018118,0.017929,0.017745,0.017564,0.017387,0.017214,0.017046,0.016886,0.016732,
                                0.016587,0.016446,0.016309,0.016174,0.016039,0.015906,0.015777,0.015653,0.015532,
                                0.015418,0.015308,0.015202,0.015097,0.014991,0.014885,0.014782,0.014683,0.014588,0.0145,
                                0.014415,0.014334,0.014254,0.014172,0.01409,0.014007,0.013926,0.013846,0.01377,0.013697,
                                0.013628,0.013559,0.013491,0.013423,0.013354,0.013288,0.013223,0.01316,0.013099,0.01304,
                                0.012983,0.012926,0.01287,0.012814,0.012758,0.012703,0.012649,0.012597,0.012547,0.012499,
                                0.01245,0.012402,0.012352,0.012302,0.012254,0.012205,0.012158,0.012113,0.012068,0.012025,
                                0.011982,0.01194,0.011899,0.011859,0.011819,0.01178,0.011741])

            x_array_out, y_array_out = agdrift_empty.extend_curve(x_array_in, y_array_in, max_dist, dist_inc, num_pts_ext,
                                                                  ln_ln_trans)
            npts_out = [len(y_array_out)]
            #print out output arrays for debugging
            agdrift_empty.write_arrays_to_csv(x_array_out, y_array_out, "extend_data.csv")
            npt.assert_array_equal(expected_result_npts, npts_out, verbose=True)
            npt.assert_allclose(x_array_out, expected_result_x, rtol=1e-5, atol=0, err_msg='', verbose=True)
            npt.assert_allclose(y_array_out, expected_result_y, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
            tab1 = [x_array_out, expected_result_x]
            tab2 = [y_array_out, expected_result_y]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print('expected {0} number of points and got {1} points'.format(expected_result_npts[0], npts_out[0]))
            print("x_array result/x_array_expected")
            print(tabulate(tab1, headers='keys', tablefmt='rst'))
            print("y_array result/y_array_expected")
            print(tabulate(tab2, headers='keys', tablefmt='rst'))
        return

# unittest will
# 1) call the setup method
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
