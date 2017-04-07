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
        :param drop_size: qualitative description of spray droplet size
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
            agdrift_empty.drop_size = pd.Series(
                ['Very Fine to Fine',
                'Fine to Medium',
                'Medium to Coarse',
                'Coarse to Very Coarse',
                'Fine to Medium',
                'Very Fine',
                'Fine to Medium/Coarse',
                'Very Fine',
                'Fine to Medium/Coarse',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'NaN',
                'Medium to Coarse',
                'Very Fine',
                'Very Fine to Medium',
                'Fine to Medium/Coarse',
                'Very Fine Indeed',
                'NaN',
                'Very Fine to Medium',
                'Medium to Coarse',
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
        :param drop_size: qualitative description of spray droplet size
        :param boom_height: qualitative height above ground of spray boom
        :param airblast_type: type of airblast application (e.g., vineyard, orchard)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        agdrift_empty = self.create_agdrift_object()

        agdrift_empty.out_sim_scenario_id = pd.Series([], dtype='object')
        expected_result = pd.Series(['aerial_vf2f',
                                     'aerial_f2m',
                                     'aerial_m2c'
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
            agdrift_empty.drop_size = pd.Series(['Very Fine to Fine',
                                                 'Fine to Medium',
                                                 'Medium to Coarse',
                                                 'Coarse to Very Coarse',
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
                                                     'Orchard'
                                                     'NaN'], dtype='object')

            agdrift_empty.set_sim_scenario_id()
            result = agdrift_empty.out_sim_scenario_id
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
                                     'airblast_vineyard', 'airblast_orchard', 13])

        try:
            agdrift_empty.column_names = pd.Series(['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                     'ground_low_vf', 'ground_low_fmc',
                                     'ground_high_vf', 'ground_high_fmc',
                                     'airblast_normal', 'airblast_dense', 'airblast_sparse',
                                     'airblast_vineyard', 'airblast_orchard', 'distance_ft'])

            #call method to assign scenario names
            agdrift_empty.assign_column_names()
            result = agdrift_empty.scenario_name
            #ready scenario count for appending to scneario list for test purposes
            #couldn't find more appropriate way to do this appending
            scenario_num = pd.Series([agdrift_empty.scenario_number], dtype='object')
            result.append(scenario_num)
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


        #sqlite_agdrift_distance is only 161 long
        # expected_result = [0.50013,0.0389962,163.0, #aerial_vf2f
        #                    0.49997,0.0111688,163.0, #aerial_f2m
        #                    0.4999,.0050397964,163.0, #aerial_m2c
        #                    0.49988,0.0029500385,163.0, #aerial_c2vc
        #                    1.019339,8.6596354e-4,163.0, #ground_low_vf
        #                    1.007885,5.5617929e-4,163.0, #ground_low_fmc
        #                    1.055205,1.2169296e-3,163.0, #ground_high_vf
        #                    1.012828,6.8997011e-4,163.0, #ground_high_fmc
        #                    8.91E-03,3.4298396e-5,163.0, #airblast_normal
        #                    0.1155276,4.5799708e-4,163.0, #airblast_dense
        #                    0.4762651,4.0496026e-5,163.0, #airblast_sparse
        #                    3.76E-02,2.6858491e-5,163.0, #airblast_vineyard
        #                    0.2223051,3.2098651e-4,163.0] #airblast_orchard

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
                #was scenario_data[i] =
                vector_query = agdrift_empty.get_scenario_deposition_data(agdrift_empty.scenario_name[i],
                                                                              agdrift_empty.num_db_values)
                print(vector_query)
                #extract 1st and last values of scenario data and build result list (including how many values are
                #retrieved for each scenario
                if i == 0:
                    #fix this
                    result = [vector_query[0], vector_query[agdrift_empty.num_db_values - 1],
                              float(len(vector_query))]
                else:
                    result.extend([vector_query[0], vector_query[agdrift_empty.num_db_values - 1],
                              float(len(vector_query))])
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
        expected_result = ['aerial_vf2f', 'aerial_f2m', 'aerial_m2c', 'aerial_c2vc',
                                           'ground_low_vf', 'ground_low_fmc', 'ground_high_vf', 'ground_high_fmc',
                                           'airblast_normal', 'airblast_dense', 'airblast_sparse', 'airblast_vineyard',
                                           'airblast_orchard']

        try:
            result = agdrift_empty.get_column_names()
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

        expected_result = pd.Series([1.401061, 0.3648362, 0.003362546])

        try:
            avg_dep_lbac = pd.Series([1.25e-3,3.255e-4,3e-5], dtype='float')
            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.acres_per_hectare = 2.47105

            result = agdrift_empty.calc_avg_dep_gha(avg_dep_lbac)
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
        finally:
            tab = [result, expected_result]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_calc_avg_fielddep_mgcm(self):
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

        expected_result = pd.Series([1.401063e-5, 3.648369e-6, 3.362552e3])

        try:
            avg_dep_lbac = pd.Series([1.25e-3,3.255e-4,3e-5], dtype='float')

            agdrift_empty.gms_per_lb = 453.592
            agdrift_empty.sqft_per_acre = 43560.
            agdrift_empty.mg_per_gram = 1.e3
            agdrift_empty.cm2_per_ft2 = 929.03

            result = agdrift_empty.calc_avg_fielddep_mgcm(avg_dep_lbac)
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

        expected_result = pd.Series([], dtype='float')
        x_array_in = pd.Series([], dtype='float')
        y_array_in = pd.Series([], dtype='float')
        x_array_out = pd.Series([], dtype='float')
        y_array_out = pd.Series([], dtype='float')

        try:

            expected_result = [0.,0.1025,0.2051,0.4101,0.8202,1.6404,3.2808,4.9212,6.5616,9.8424,13.1232,19.6848,26.2464,
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
                        977.6784,984.24,990.8016,997.3632,1495.5,1994.0]

            x_dist = 10.
            agdrift_empty.distance_name = 'distance_ft'
            agdrift_empty.scenario_name = 'ground_low_vf'
            agdrift_empty.num_db_values = 161
            x_array_in = agdrift_empty.get_distances(agdrift_empty.num_db_values)
            y_array_in = agdrift_empty.get_scenario_deposition_data(agdrift_empty.scenario_name, agdrift_empty.num_db_values)

            x_array_out, y_array_out, npts_out = agdrift_empty.generate_running_avg(agdrift_empty.num_db_values,
                                                                        x_array_in, y_array_in, x_dist)

            #npt.assert_allclose(y_array_out, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
        finally:
            pass
        #     tab = [y_array_out, expected_result]
        #     print("\n")
        #     print(inspect.currentframe().f_code.co_name)
        #     print(tabulate(tab, headers='keys', tablefmt='rst'))
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

    def test_create_integration_avg(self):
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


            expected_result_y = [0.364706389,0.351133211,0.338484161,0.315606383,0.277604029,0.222810736,0.159943507,
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
                                 0.001025,0.001015,0.001005,0.0009985,0.000993,0.000985,0.000977,0.0009695]

            expected_result_npts = 160
            expected_x_dist_of_interest = 990.8016


            x_dist = 6.56
            weighted_avg = 0.0009695
            agdrift_empty.distance_name = 'distance_ft'
            agdrift_empty.scenario_name = 'ground_low_vf'
            agdrift_empty.num_db_values = 161
            agdrift_empty.find_nearest_x = True
            x_array_in = agdrift_empty.get_distances(agdrift_empty.num_db_values)
            y_array_in = agdrift_empty.get_scenario_deposition_data(agdrift_empty.scenario_name, agdrift_empty.num_db_values)

            x_array_out, y_array_out, npts_out, x_dist_of_interest, range_chk = \
                agdrift_empty.create_integration_avg(agdrift_empty.num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

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

    def test_create_integration_avg1(self):
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
            expected_result_y = [0.5,1.5,4.5,5.3,5.9,6.3,6.5,9.5,10.5,11.5,12.5]
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
                agdrift_empty.create_integration_avg(num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

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

    def test_create_integration_avg2(self):
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
            expected_result_y = [49.5,48.5,45.5,44.7,44.1,43.7,43.5,41.1,40.7,40.3,
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
                agdrift_empty.create_integration_avg(num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

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

    def test_create_integration_avg3(self):
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
                agdrift_empty.create_integration_avg(num_db_values, x_array_in, y_array_in, x_dist, weighted_avg)

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

#     def test_get_pond_ground_high_vf2f(self):
#
#        # create empty pandas dataframes to create empty object for this unittest
#        agdrift_empty = self.create_agdrift_object()
#
#        try:
#             agdrift_empty.pond_ground_high_vf2f = agdrift_empty.get_pond_ground_high_vf2f()
#             result = agdrift_empty.pond_ground_high_vf2f[0:3]
#             expected_result = pd.Series([0.06164, 0.052075, 0.04251])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#        finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#        return
#
#     def test_get_pond_ground_high_f2m(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_ground_high_f2m = agdrift_empty.get_pond_ground_high_f2m()
#             result = agdrift_empty.pond_ground_high_f2m[0:3]
#             expected_result = pd.Series([0.0165, 0.013171, 0.009842])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_ground_low_vf2f(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_ground_low_vf2f = agdrift_empty.get_pond_ground_low_vf2f()
#             result = agdrift_empty.pond_ground_low_vf2f[0:3]
#             expected_result = pd.Series([0.02681, 0.02115, 0.01549])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_ground_low_f2m(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_ground_low_f2m = agdrift_empty.get_pond_ground_low_f2m()
#             result = agdrift_empty.pond_ground_low_f2m[0:3]
#             expected_result = pd.Series([0.0109,0.008512, 0.006124])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_aerial_vf2f(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_aerial_vf2f = agdrift_empty.get_pond_aerial_vf2f()
#             result = agdrift_empty.pond_aerial_vf2f[0:3]
#             expected_result = pd.Series([0.2425, 0.2372, 0.2319])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_aerial_f2m(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_aerial_f2m = agdrift_empty.get_pond_aerial_f2m()
#             result = agdrift_empty.pond_aerial_f2m[0:3]
#             expected_result = pd.Series([0.1266, 0.1204, 0.1142])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_aerial_m2c(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_aerial_m2c = agdrift_empty.get_pond_aerial_m2c()
#             result = agdrift_empty.pond_aerial_m2c[0:3]
#             expected_result = pd.Series([0.08918, 0.082835, 0.07649])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_aerial_c2vc(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#         result = pd.Series([], dtype='float')
#         try:
#             agdrift_empty.pond_aerial_c2vc = agdrift_empty.get_pond_aerial_c2vc()
#             result = agdrift_empty.pond_aerial_c2vc[0:3]
#             expected_result = pd.Series([0.06879, 0.062505, 0.05622])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_airblast_orchard(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_airblast_orchard = agdrift_empty.get_pond_airblast_orchard()
#             result = agdrift_empty.pond_airblast_orchard[0:3]
#             expected_result = pd.Series([0.0218, 0.01911, 0.01642])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_get_pond_airblast_vineyard(self):
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.pond_airblast_vineyard = agdrift_empty.get_pond_airblast_vineyard()
#             result = agdrift_empty.pond_airblast_vineyard[0:3]
#             expected_result = pd.Series([2.433e-3, 2.0455e-3, 1.658e-3])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#
#     def test_tier_I_aerial_c2vc(self):
#         """
#         unittest for function agdrift.tier_I_aerial
#         :return:
#         """
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         result = pd.Series([], dtype='object')
#         try:
#             expected_result = pd.Series([0.06878999999999999, 0.06250499999999999, 0.05622])
#             #n_tests = len(expected_result) # has to match with the number of arrays in the expected_result above
#             agdrift_empty.load_data()
#             result = agdrift_empty.pond_aerial_c2vc[0:3]
#             #agdrift_empty.aquatic_type = pd.Series(['EPA Defined Pond'],index=range(n_tests))
#             #agdrift_empty.application_method = pd.Series(['Tier I Aerial'],index=range(n_tests))
#             #agdrift_empty.drop_size = pd.Series(['Coarse to Very Coarse'],index=range(n_tests))
#             #agdrift_empty.out_y = pd.Series(np.nan,index=range(n_tests))
# #??             #agdrift_empty.out_y = [[[np.nan]]*n_tests]
#             #agdrift_empty.out_nasae = pd.Series(np.nan, index=range(n_tests))
# #??             #agdrift_empty.out_nasae = [[[np.nan]] * n_tests]
#             #agdrift_empty.out_express_y = pd.Series(np.nan, index=range(n_tests))
#             # agdrift_empty.out_express_y = [[[np.nan]] * n_tests]
# #??             #agdrift_empty.out_x = pd.Series(np.nan, index=range(n_tests))
#             #for i in range(n_tests):
#             #    agdrift_empty.tier_I_aerial(i)
#             #    #result[i] = agdrift_empty.out_nasae[i]
#             #    #result[i] = [agdrift_empty.out_y[i][0][0:3]]
#             #    result.loc[i] = agdrift_empty.out_y[i][0:3]
#
#             #result.tolist()
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#             # [[agdrift_empty.pond_aerial_c2vc], [3],
#             #         [[0.06878999999999999, 0.06250499999999999, 0.05622, 0.052035, 0.047850000000000004,
#             #               0.044875000000000005, 0.04190000000000001, 0.039685, 0.037469999999999996, 0.03574,
#             #               0.03401, 0.03262, 0.03123, 0.03008, 0.028929999999999997, 0.027925, 0.026920000000000003,
#             #               0.025985, 0.02505, 0.02418, 0.02331, 0.02253, 0.02175, 0.02109, 0.02043, 0.019865,
#             #               0.019299999999999998, 0.018799999999999997, 0.0183, 0.01784, 0.01738, 0.016955, 0.01653,
#             #               0.016135, 0.01574, 0.015375000000000002, 0.015009999999999999, 0.014674999999999999,
#             #               0.014339999999999999, 0.014034999999999999, 0.01373, 0.013455, 0.01318,
#             #               0.012930000000000002, 0.01268, 0.012445, 0.01221, 0.011995, 0.011779999999999999,
#             #               0.011575, 0.01137, 0.011179999999999999, 0.01099, 0.010815000000000002, 0.01064,
#             #               0.010474999999999998, 0.01031, 0.010154999999999999, 0.01, 0.00986, 0.00972, 0.009588,
#             #               0.009455999999999999, 0.009332, 0.009208, 0.0090925, 0.008977, 0.008869, 0.008761,
#             #               0.00866, 0.008559, 0.008464000000000001, 0.008369, 0.0082795, 0.00819, 0.008105,
#             #               0.008020000000000001, 0.007939, 0.007858, 0.0077815, 0.007705, 0.007632, 0.007559,
#             #               0.0074895, 0.0074199999999999995, 0.0073535, 0.007287, 0.0072239999999999995, 0.007161,
#             #               0.0070999999999999995, 0.007039, 0.006980999999999999, 0.006923, 0.006867000000000001,
#             #               0.006811, 0.006757, 0.006703, 0.006651000000000001, 0.006599000000000001,
#             #               0.006548000000000001, 0.006497, 0.006448000000000001, 0.006399, 0.0063514999999999995,
#             #               0.006304, 0.0062575, 0.0062109999999999995, 0.0061660000000000005, 0.006121,
#             #               0.0060775000000000004, 0.006034, 0.005991, 0.005948, 0.0059065, 0.005865, 0.005824,
#             #               0.005783, 0.005743000000000001, 0.005703000000000001, 0.0056645, 0.005626,
#             #               0.005587999999999999, 0.00555, 0.0055130000000000005, 0.005476, 0.005439499999999999,
#             #               0.005403, 0.005367500000000001, 0.005332, 0.005297499999999999, 0.005263,
#             #               0.0052285000000000005, 0.005194, 0.0051605, 0.0051270000000000005, 0.005094499999999999,
#             #               0.005062, 0.00503, 0.004998, 0.0049665, 0.004935, 0.0049045, 0.004874, 0.0048445,
#             #               0.004815, 0.004785500000000001, 0.004756, 0.0047275, 0.004699, 0.004671,
#             #               0.0046429999999999996, 0.004616, 0.004588999999999999, 0.0045625, 0.004536, 0.00451,
#             #               0.004484, 0.004459, 0.0044340000000000004, 0.004409, 0.004384, 0.00436, 0.004336,
#             #               0.004313, 0.0042899999999999995, 0.004267, 0.004244, 0.004222, 0.0042, 0.0041785,
#             #               0.004157, 0.004136, 0.004115, 0.004095, 0.004075, 0.004055, 0.004035,
#             #               0.0040160000000000005, 0.003997, 0.0039785, 0.00396, 0.003942, 0.003924, 0.0039065,
#             #               0.003889, 0.003872, 0.003855, 0.0038385000000000003, 0.003822, 0.003806, 0.00379,
#             #               0.0037745, 0.003759, 0.003744, 0.003729, 0.0037145, 0.0037, 0.0036855, 0.003671,
#             #               0.0036575, 0.003644, 0.0036305, 0.0036170000000000004, 0.003603500000000001, 0.00359,
#             #               0.0035765000000000016, 0.0035630000000000006, 0.003549499999999999, 0.0035360000000000014,
#             #               0.0035225000000000018, 0.003509, 0.003495499999999998, 0.003482000000000003,
#             #               0.0034685000000000033, 0.0034549999999999993, 0.0034414999999999997, 0.003428,
#             #               0.0034145000000000048, 0.003401000000000005, 0.003387500000000001, 0.0033740000000000016,
#             #               0.003360500000000002, 0.0033469999999999975, 0.0033335000000000027, 0.0033199999999999983,
#             #               0.0033065000000000034, 0.003293000000000008, 0.003279500000000004, 0.003266,
#             #               0.003252500000000005, 0.0032390000000000006, 0.0032255000000000057, 0.0032120000000000013,
#             #               0.0031984999999999974, 0.003185000000000002, 0.003171499999999998, 0.003158000000000012,
#             #               0.003144500000000008, 0.0031310000000000036, 0.0031175000000000087, 0.0031040000000000043,
#             #               0.0030905000000000004, 0.003077000000000005, 0.003063500000000001, 0.003049999999999997,
#             #               0.003036499999999993, 0.0030230000000000066, 0.0030095000000000026, 0.0029959999999999987,
#             #               0.0029824999999999947, 0.0029689999999999907, 0.002955500000000004, 0.002942000000000018,
#             #               0.002928500000000014, 0.0029150000000000096, 0.0029015000000000056, 0.0028880000000000017,
#             #               0.0028745000000000155, 0.002861000000000011, 0.002847500000000007, 0.002834000000000003,
#             #               0.0028204999999999992, 0.0028070000000000126, 0.0027935000000000086,
#             #               0.0027800000000000047, 0.0027665000000000007, 0.0027529999999999968, 0.00273950000000001,
#             #               0.002726000000000006, 0.0027125000000000022, 0.0026989999999999983, 0.002685499999999994,
#             #               0.0026720000000000077, 0.0026585000000000215, 0.002645000000000017, 0.002631500000000013,
#             #               0.002618000000000009, 0.0026045000000000052, 0.0025910000000000186, 0.0025775000000000147,
#             #               0.0025640000000000107, 0.0025505000000000068, 0.002537000000000003, 0.002523500000000016,
#             #               0.0025100000000000122, 0.0024965000000000083, 0.0024830000000000043,
#             #               0.0024695000000000177, 0.002455999999999996, 0.0024425000000000098, 0.002428999999999988,
#             #               0.002415500000000037, 0.0024020000000000152, 0.002388500000000029, 0.0023750000000000073,
#             #               0.0023615000000000207, 0.002347999999999999, 0.0023345000000000128, 0.002320999999999991,
#             #               0.0023075000000000044]]]
#             #self.assertItemsEqual(result, expected)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#         # finally:
#         #     tab = [result, expected_result]
#         #     print("\n")
#         #     print(inspect.currentframe().f_code.co_name)
#         #     print(tabulate(tab, headers='keys', tablefmt='rst'))
#         # return
#
#     def test_tier_I_ground(self):
#         """
#         unittest for function agdrift.tier_I_ground
#         :return:
#         """
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.load_data() #unittest needs agdrift_empty.pond_ground_high_vf2f
#             agdrift_empty.ecosystem_type = pd.Series(['EPA Pond'])
#             agdrift_empty.application_method = pd.Series(['Ground'])
#             agdrift_empty.drop_size = pd.Series(['Fine'])
#             agdrift_empty.boom_height = pd.Series(['High'])
#             result = agdrift_empty.out_express_y[0:3]
#             expected_result = pd.Series([0.06164, 0.052074999999999996, 0.042510000000000006])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#         # finally:
#         #     tab = [result, expected_result]
#         #     print("\n")
#         #     print(inspect.currentframe().f_code.co_name)
#         #     print(tabulate(tab, headers='keys', tablefmt='rst'))
#         # return
#
#
#     # def test_tier_I_aerial(self):
#     #     """
#     #     unittest for function agdrift.tier_I_aerial
#     #     :return:
#     #     """
#     #     try:
#     #         agdrift_empty.load_data()
#     #         agdrift_empty.ecosystem_type = pd.Series(['EPA Pond'])
#     #         agdrift_empty.application_method = pd.Series(['Aerial'])
#     #         agdrift_empty.drop_size = pd.Series(['Very Coarse'])
#     #         agdrift_empty.tier_I_aerial()
#     #         result = agdrift_empty.out_nasae
#     #         expected = [3]
#                 # [[agdrift_empty.pond_aerial_c2vc], [3],
#                 #         [[0.06878999999999999, 0.06250499999999999, 0.05622, 0.052035, 0.047850000000000004,
#                 #               0.044875000000000005, 0.04190000000000001, 0.039685, 0.037469999999999996, 0.03574,
#                 #               0.03401, 0.03262, 0.03123, 0.03008, 0.028929999999999997, 0.027925, 0.026920000000000003,
#                 #               0.025985, 0.02505, 0.02418, 0.02331, 0.02253, 0.02175, 0.02109, 0.02043, 0.019865,
#                 #               0.019299999999999998, 0.018799999999999997, 0.0183, 0.01784, 0.01738, 0.016955, 0.01653,
#                 #               0.016135, 0.01574, 0.015375000000000002, 0.015009999999999999, 0.014674999999999999,
#                 #               0.014339999999999999, 0.014034999999999999, 0.01373, 0.013455, 0.01318,
#                 #               0.012930000000000002, 0.01268, 0.012445, 0.01221, 0.011995, 0.011779999999999999,
#                 #               0.011575, 0.01137, 0.011179999999999999, 0.01099, 0.010815000000000002, 0.01064,
#                 #               0.010474999999999998, 0.01031, 0.010154999999999999, 0.01, 0.00986, 0.00972, 0.009588,
#                 #               0.009455999999999999, 0.009332, 0.009208, 0.0090925, 0.008977, 0.008869, 0.008761,
#                 #               0.00866, 0.008559, 0.008464000000000001, 0.008369, 0.0082795, 0.00819, 0.008105,
#                 #               0.008020000000000001, 0.007939, 0.007858, 0.0077815, 0.007705, 0.007632, 0.007559,
#                 #               0.0074895, 0.0074199999999999995, 0.0073535, 0.007287, 0.0072239999999999995, 0.007161,
#                 #               0.0070999999999999995, 0.007039, 0.006980999999999999, 0.006923, 0.006867000000000001,
#                 #               0.006811, 0.006757, 0.006703, 0.006651000000000001, 0.006599000000000001,
#                 #               0.006548000000000001, 0.006497, 0.006448000000000001, 0.006399, 0.0063514999999999995,
#                 #               0.006304, 0.0062575, 0.0062109999999999995, 0.0061660000000000005, 0.006121,
#                 #               0.0060775000000000004, 0.006034, 0.005991, 0.005948, 0.0059065, 0.005865, 0.005824,
#                 #               0.005783, 0.005743000000000001, 0.005703000000000001, 0.0056645, 0.005626,
#                 #               0.005587999999999999, 0.00555, 0.0055130000000000005, 0.005476, 0.005439499999999999,
#                 #               0.005403, 0.005367500000000001, 0.005332, 0.005297499999999999, 0.005263,
#                 #               0.0052285000000000005, 0.005194, 0.0051605, 0.0051270000000000005, 0.005094499999999999,
#                 #               0.005062, 0.00503, 0.004998, 0.0049665, 0.004935, 0.0049045, 0.004874, 0.0048445,
#                 #               0.004815, 0.004785500000000001, 0.004756, 0.0047275, 0.004699, 0.004671,
#                 #               0.0046429999999999996, 0.004616, 0.004588999999999999, 0.0045625, 0.004536, 0.00451,
#                 #               0.004484, 0.004459, 0.0044340000000000004, 0.004409, 0.004384, 0.00436, 0.004336,
#                 #               0.004313, 0.0042899999999999995, 0.004267, 0.004244, 0.004222, 0.0042, 0.0041785,
#                 #               0.004157, 0.004136, 0.004115, 0.004095, 0.004075, 0.004055, 0.004035,
#                 #               0.0040160000000000005, 0.003997, 0.0039785, 0.00396, 0.003942, 0.003924, 0.0039065,
#                 #               0.003889, 0.003872, 0.003855, 0.0038385000000000003, 0.003822, 0.003806, 0.00379,
#                 #               0.0037745, 0.003759, 0.003744, 0.003729, 0.0037145, 0.0037, 0.0036855, 0.003671,
#                 #               0.0036575, 0.003644, 0.0036305, 0.0036170000000000004, 0.003603500000000001, 0.00359,
#                 #               0.0035765000000000016, 0.0035630000000000006, 0.003549499999999999, 0.0035360000000000014,
#                 #               0.0035225000000000018, 0.003509, 0.003495499999999998, 0.003482000000000003,
#                 #               0.0034685000000000033, 0.0034549999999999993, 0.0034414999999999997, 0.003428,
#                 #               0.0034145000000000048, 0.003401000000000005, 0.003387500000000001, 0.0033740000000000016,
#                 #               0.003360500000000002, 0.0033469999999999975, 0.0033335000000000027, 0.0033199999999999983,
#                 #               0.0033065000000000034, 0.003293000000000008, 0.003279500000000004, 0.003266,
#                 #               0.003252500000000005, 0.0032390000000000006, 0.0032255000000000057, 0.0032120000000000013,
#                 #               0.0031984999999999974, 0.003185000000000002, 0.003171499999999998, 0.003158000000000012,
#                 #               0.003144500000000008, 0.0031310000000000036, 0.0031175000000000087, 0.0031040000000000043,
#                 #               0.0030905000000000004, 0.003077000000000005, 0.003063500000000001, 0.003049999999999997,
#                 #               0.003036499999999993, 0.0030230000000000066, 0.0030095000000000026, 0.0029959999999999987,
#                 #               0.0029824999999999947, 0.0029689999999999907, 0.002955500000000004, 0.002942000000000018,
#                 #               0.002928500000000014, 0.0029150000000000096, 0.0029015000000000056, 0.0028880000000000017,
#                 #               0.0028745000000000155, 0.002861000000000011, 0.002847500000000007, 0.002834000000000003,
#                 #               0.0028204999999999992, 0.0028070000000000126, 0.0027935000000000086,
#                 #               0.0027800000000000047, 0.0027665000000000007, 0.0027529999999999968, 0.00273950000000001,
#                 #               0.002726000000000006, 0.0027125000000000022, 0.0026989999999999983, 0.002685499999999994,
#                 #               0.0026720000000000077, 0.0026585000000000215, 0.002645000000000017, 0.002631500000000013,
#                 #               0.002618000000000009, 0.0026045000000000052, 0.0025910000000000186, 0.0025775000000000147,
#                 #               0.0025640000000000107, 0.0025505000000000068, 0.002537000000000003, 0.002523500000000016,
#                 #               0.0025100000000000122, 0.0024965000000000083, 0.0024830000000000043,
#                 #               0.0024695000000000177, 0.002455999999999996, 0.0024425000000000098, 0.002428999999999988,
#                 #               0.002415500000000037, 0.0024020000000000152, 0.002388500000000029, 0.0023750000000000073,
#                 #               0.0023615000000000207, 0.002347999999999999, 0.0023345000000000128, 0.002320999999999991,
#                 #               0.0023075000000000044]]]
#         #     self.assertItemsEqual(result, expected)
#         # finally:
#         #     pass
#         # return
#
#     # def test_tier_I_ground(self):
#     #     """
#     #     unittest for function agdrift.tier_I_ground
#     #     :return:
#     #     """
#     #     try:
#     #         agdrift_empty.ecosystem_type = pd.Series(['EPA Pond'])
#     #         agdrift_empty.application_method = pd.Series(['Ground'])
#     #         agdrift_empty.drop_size = pd.Series(['Fine'])
#     #         agdrift_empty.boom_height = pd.Series(['High'])
#     #         result = agdrift_empty.tier_I_ground()
#     #         expected = [[agdrift_empty.pond_ground_high_vf2f], [5],
#     #                     [[0.06164, 0.052074999999999996, 0.042510000000000006, 0.03838, 0.034249999999999996,
#     #                           0.031805, 0.02936, 0.027715, 0.026070000000000003, 0.024855000000000002,
#     #                           0.023639999999999998, 0.022685, 0.02173, 0.020949999999999996, 0.02017,
#     #                           0.019514999999999998, 0.01886, 0.018295, 0.01773, 0.017235, 0.016739999999999998, 0.0163,
#     #                           0.01586, 0.015470000000000001, 0.01508, 0.014725000000000002, 0.01437, 0.014045,
#     #                           0.013720000000000001, 0.01343, 0.01314, 0.01287, 0.0126, 0.012349999999999998, 0.0121,
#     #                           0.011865, 0.01163, 0.011415000000000002, 0.011200000000000002, 0.011000000000000001,
#     #                           0.0108, 0.01061, 0.01042, 0.010244999999999999, 0.010069999999999999,
#     #                           0.009904999999999999, 0.00974, 0.0095835, 0.009427, 0.009279500000000001, 0.009132,
#     #                           0.0089925, 0.008853, 0.008720499999999999, 0.008588, 0.0084625, 0.008337, 0.008218,
#     #                           0.008099, 0.007984999999999999, 0.007871, 0.007763, 0.0076549999999999995, 0.007552,
#     #                           0.007449, 0.00735, 0.007251, 0.007157, 0.007063000000000001, 0.0069725, 0.006882,
#     #                           0.006795500000000001, 0.0067090000000000006, 0.0066265, 0.0065439999999999995, 0.0064645,
#     #                           0.006384999999999999, 0.006308499999999999, 0.006232, 0.0061585, 0.006085,
#     #                           0.006014500000000001, 0.0059440000000000005, 0.005876, 0.005808, 0.005742499999999999,
#     #                           0.005677, 0.005614, 0.005551, 0.00549, 0.005429000000000001, 0.0053705, 0.005312,
#     #                           0.005255000000000001, 0.005198, 0.0051435000000000005, 0.005089, 0.0050360000000000005,
#     #                           0.0049830000000000004, 0.0049315, 0.00488, 0.0048305, 0.0047810000000000005, 0.004733,
#     #                           0.004685, 0.0046385, 0.004592, 0.004547, 0.004502, 0.0044585, 0.004415, 0.004373,
#     #                           0.004331, 0.0042899999999999995, 0.004249, 0.004209, 0.004169, 0.0041305000000000005,
#     #                           0.004092, 0.0040545, 0.004017, 0.0039805000000000005, 0.003944, 0.0039085,
#     #                           0.0038729999999999997, 0.0038385000000000003, 0.003804, 0.0037705, 0.003737, 0.0037045,
#     #                           0.0036720000000000004, 0.0036404999999999996, 0.003609, 0.003578, 0.0035470000000000002,
#     #                           0.003517, 0.003487, 0.0034575, 0.003428, 0.0033994999999999997, 0.0033710000000000003,
#     #                           0.0033435000000000006, 0.003316, 0.003289, 0.0032619999999999997, 0.0032355, 0.003209,
#     #                           0.003183, 0.0031569999999999997, 0.003132, 0.003107, 0.0030825, 0.003058,
#     #                           0.0030340000000000002, 0.00301, 0.0029869999999999996, 0.002964, 0.0029410000000000005,
#     #                           0.002918, 0.0028959999999999997, 0.002874, 0.002852, 0.0028299999999999996, 0.002809,
#     #                           0.002788, 0.002767, 0.002746, 0.002726, 0.002706, 0.002686, 0.002666, 0.002647,
#     #                           0.0026279999999999997, 0.002609, 0.0025900000000000003, 0.0025715, 0.002553,
#     #                           0.0025345000000000003, 0.002516, 0.0024985, 0.0024809999999999997, 0.0024635,
#     #                           0.0024460000000000003, 0.002429, 0.002412, 0.0023955, 0.002379, 0.002363, 0.002347,
#     #                           0.002331, 0.0023150000000000002, 0.0022995, 0.002284, 0.0022685, 0.002253, 0.002238,
#     #                           0.002223, 0.0022085, 0.002194, 0.0021795, 0.002165, 0.0021504999999999996, 0.002136,
#     #                           0.0021215, 0.0021069999999999995, 0.0020925000000000006, 0.002078, 0.0020634999999999994,
#     #                           0.0020489999999999996, 0.002034499999999999, 0.0020199999999999997, 0.0020054999999999977,
#     #                           0.0019910000000000006, 0.0019764999999999987, 0.0019619999999999993,
#     #                           0.0019474999999999976, 0.001932999999999998, 0.0019185000000000007, 0.001903999999999999,
#     #                           0.0018894999999999973, 0.001875, 0.0018604999999999982, 0.0018459999999999965,
#     #                           0.0018314999999999948, 0.0018169999999999974, 0.0018025000000000003,
#     #                           0.0017879999999999986, 0.0017735000000000012, 0.0017589999999999995,
#     #                           0.0017444999999999978, 0.001729999999999996, 0.0017154999999999987, 0.001700999999999997,
#     #                           0.0016864999999999953, 0.001671999999999998, 0.0016575000000000006, 0.0016429999999999988,
#     #                           0.0016284999999999971, 0.0016139999999999954, 0.0015994999999999937, 0.001585000000000001,
#     #                           0.0015704999999999992, 0.0015559999999999975, 0.0015414999999999956,
#     #                           0.0015269999999999939, 0.0015124999999999921, 0.0014979999999999904,
#     #                           0.0014834999999999976, 0.001468999999999996, 0.0014544999999999942, 0.0014399999999999925,
#     #                           0.0014254999999999906, 0.0014109999999999978, 0.001396499999999996, 0.0013820000000000032,
#     #                           0.0013675000000000015, 0.0013529999999999998, 0.0013384999999999981,
#     #                           0.0013239999999999962, 0.0013094999999999945, 0.0012949999999999928, 0.0012805,
#     #                           0.0012659999999999982, 0.0012514999999999965, 0.0012369999999999948,
#     #                           0.0012224999999999931, 0.0012079999999999912, 0.0011934999999999895,
#     #                           0.0011789999999999967, 0.001164499999999995, 0.0011499999999999933, 0.0011354999999999916,
#     #                           0.0011209999999999987, 0.001106499999999997, 0.001091999999999995, 0.0010774999999999934,
#     #                           0.0010629999999999917, 0.00104849999999999, 0.0010339999999999883, 0.0010195000000000043,
#     #                           0.0010050000000000026, 0.000990500000000001, 0.0009759999999999991, 0.0009614999999999974,
#     #                           0.0009469999999999956, 0.0009324999999999939, 0.0009179999999999922,
#     #                           0.0009034999999999905, 0.0008889999999999886, 0.0008744999999999869,
#     #                           0.0008599999999999852, 0.0008454999999999835, 0.0008309999999999817,
#     #                           0.0008164999999999978, 0.0008019999999999961, 0.0007874999999999944,
#     #                           0.0007729999999999926, 0.0007584999999999908, 0.0007439999999999891,
#     #                           0.0007294999999999874]]]
#     #         self.assertListEqual(result, expected)
#     #     finally:
#     #         pass
#     #     return
#
#     def test_tier_I_airblast(self):
#         """
#         unittest for function agdrift.tier_I_airblast
#         :return:
#         """
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.load_data()
#             agdrift_empty.ecosystem_type = pd.Series(['EPA Pond'])
#             agdrift_empty.application_method = pd.Series(['Orchard/Airblast'])
#             agdrift_empty.airblast_type = pd.Series(['Vineyard'])
#             result = agdrift_empty.out_express_y[0:3]
#             expected_result = pd.Series([0.002433, 0.0020455, 0.001658])
#             npt.assert_allclose(result, expected_result, rtol=1e-5, atol=0, err_msg='', verbose=True)
#             #     [[agdrift_empty.pond_airblast_vineyard], [8],
#             #             [[0.002433, 0.0020455, 0.001658, 0.001466, 0.0012740000000000002, 0.0011565, 0.001039,
#             #                   0.00096125, 0.0008835, 0.00082735, 0.0007712, 0.0007285999999999999, 0.000686,
#             #                   0.0006523999999999999, 0.0006188, 0.0005914999999999999, 0.0005641999999999999, 0.0005415,
#             #                   0.0005188, 0.0004996, 0.00048039999999999997, 0.0004639, 0.00044740000000000003,
#             #                   0.00043300000000000006, 0.00041860000000000004, 0.00040595, 0.00039329999999999996,
#             #                   0.00038209999999999996, 0.00037089999999999996, 0.00036085, 0.0003508, 0.00034175,
#             #                   0.0003327, 0.0003245, 0.0003163, 0.00030885, 0.0003014, 0.00029455000000000003, 0.0002877,
#             #                   0.00028145, 0.00027519999999999997, 0.0002694, 0.0002636, 0.00025825, 0.0002529,
#             #                   0.0002479, 0.0002429, 0.00023825, 0.00023359999999999999, 0.0002293, 0.000225, 0.00022095,
#             #                   0.00021690000000000001, 0.00021310000000000003, 0.00020930000000000002,
#             #                   0.00020569999999999999, 0.00020209999999999998, 0.00019874999999999998,
#             #                   0.00019539999999999998, 0.00019224999999999998, 0.0001891, 0.00018610000000000002,
#             #                   0.0001831, 0.00018025, 0.00017739999999999998, 0.0001747, 0.000172,
#             #                   0.00016945000000000003, 0.0001669, 0.0001645, 0.00016209999999999998, 0.0001598,
#             #                   0.0001575, 0.0001553, 0.0001531, 0.000151, 0.00014890000000000001, 0.0001469, 0.0001449,
#             #                   0.000143, 0.0001411, 0.0001393, 0.0001375, 0.00013575, 0.000134, 0.00013230000000000002,
#             #                   0.0001306, 0.000129, 0.0001274, 0.00012585, 0.0001243, 0.00012285, 0.0001214,
#             #                   0.00011994999999999999, 0.0001185, 0.00011715, 0.0001158, 0.0001145, 0.0001132,
#             #                   0.00011190000000000001, 0.0001106, 0.0001094, 0.0001082, 0.00010704999999999999,
#             #                   0.0001059, 0.00010475, 0.0001036, 0.00010249999999999998, 0.0001014,
#             #                   0.00010033999999999999, 9.928e-05, 9.826e-05, 9.724e-05, 9.6255e-05, 9.527e-05,
#             #                   9.431500000000001e-05, 9.336e-05, 9.244e-05, 9.152e-05, 9.062500000000001e-05, 8.973e-05,
#             #                   8.8865e-05, 8.800000000000001e-05, 8.716000000000001e-05, 8.632000000000001e-05,
#             #                   8.551e-05, 8.47e-05, 8.390999999999999e-05, 8.312e-05, 8.236e-05, 8.16e-05,
#             #                   8.085500000000001e-05, 8.011e-05, 7.939500000000001e-05, 7.868e-05, 7.798e-05,
#             #                   7.727999999999999e-05, 7.66e-05, 7.591999999999999e-05, 7.526e-05, 7.46e-05, 7.396e-05,
#             #                   7.332e-05, 7.2695e-05, 7.206999999999999e-05, 7.1465e-05, 7.086000000000001e-05,
#             #                   7.027e-05, 6.968e-05, 6.9105e-05, 6.853e-05, 6.7975e-05, 6.742e-05, 6.6875e-05, 6.633e-05,
#             #                   6.58e-05, 6.527e-05, 6.475e-05, 6.423e-05, 6.373e-05, 6.323e-05, 6.2735e-05, 6.224e-05,
#             #                   6.1765e-05, 6.129e-05, 6.0820000000000004e-05, 6.035e-05, 5.9895e-05,
#             #                   5.943999999999999e-05, 5.8995e-05, 5.855e-05, 5.811999999999999e-05, 5.769e-05,
#             #                   5.7265e-05, 5.684e-05, 5.6425e-05, 5.601e-05, 5.561e-05, 5.521e-05, 5.4815e-05, 5.442e-05,
#             #                   5.4035e-05, 5.365e-05, 5.327e-05, 5.2890000000000004e-05, 5.252e-05, 5.215e-05, 5.179e-05,
#             #                   5.143e-05, 5.108e-05, 5.0730000000000004e-05, 5.038499999999999e-05,
#             #                   5.0039999999999995e-05, 4.9705e-05, 4.937e-05, 4.9040000000000005e-05,
#             #                   4.8710000000000006e-05, 4.8385000000000005e-05, 4.8060000000000004e-05, 4.7745e-05,
#             #                   4.743e-05, 4.7114999999999985e-05, 4.679999999999999e-05, 4.6485e-05,
#             #                   4.616999999999998e-05, 4.5854999999999994e-05, 4.553999999999999e-05,
#             #                   4.5224999999999954e-05, 4.490999999999998e-05, 4.459499999999998e-05,
#             #                   4.427999999999994e-05, 4.3964999999999976e-05, 4.365000000000001e-05,
#             #                   4.333499999999997e-05, 4.301999999999993e-05, 4.2704999999999965e-05,
#             #                   4.2389999999999924e-05, 4.207499999999996e-05, 4.175999999999999e-05,
#             #                   4.144499999999995e-05, 4.112999999999992e-05, 4.081499999999995e-05,
#             #                   4.0499999999999914e-05, 4.018499999999994e-05, 3.9869999999999976e-05,
#             #                   3.955500000000001e-05, 3.923999999999997e-05, 3.892499999999993e-05,
#             #                   3.8609999999999896e-05, 3.8295e-05, 3.797999999999996e-05, 3.766499999999992e-05,
#             #                   3.7349999999999885e-05, 3.7034999999999844e-05, 3.671999999999981e-05,
#             #                   3.640499999999977e-05, 3.609000000000001e-05, 3.5774999999999975e-05,
#             #                   3.5459999999999935e-05, 3.51449999999999e-05, 3.482999999999986e-05,
#             #                   3.451499999999982e-05, 3.419999999999992e-05, 3.388499999999989e-05,
#             #                   3.356999999999985e-05, 3.325499999999981e-05, 3.2939999999999776e-05,
#             #                   3.262499999999988e-05, 3.230999999999998e-05, 3.199499999999994e-05, 3.16799999999999e-05,
#             #                   3.1364999999999724e-05, 3.104999999999997e-05, 3.073500000000007e-05,
#             #                   3.0419999999999892e-05, 3.0104999999999994e-05, 2.9789999999999818e-05,
#             #                   2.9474999999999917e-05, 2.916000000000002e-05, 2.8844999999999843e-05,
#             #                   2.8529999999999945e-05, 2.821499999999977e-05, 2.789999999999987e-05,
#             #                   2.7584999999999693e-05, 2.7269999999999795e-05, 2.6954999999999897e-05,
#             #                   2.6639999999999718e-05, 2.632499999999982e-05, 2.6009999999999644e-05,
#             #                   2.5694999999999746e-05, 2.537999999999957e-05, 2.506499999999967e-05,
#             #                   2.474999999999977e-05, 2.4434999999999874e-05, 2.4119999999999976e-05,
#             #                   2.38049999999998e-05, 2.34899999999999e-05, 2.3175e-05, 2.2859999999999825e-05,
#             #                   2.2544999999999927e-05, 2.222999999999975e-05, 2.191499999999985e-05,
#             #                   2.1599999999999675e-05, 2.1284999999999777e-05, 2.096999999999988e-05,
#             #                   2.06549999999997e-05, 2.0339999999999802e-05, 2.0024999999999626e-05,
#             #                   1.9709999999999728e-05, 1.9394999999999553e-05, 1.907999999999965e-05,
#             #                   1.8764999999999753e-05, 1.8449999999999578e-05, 1.813499999999968e-05,
#             #                   1.7819999999999504e-05, 1.750499999999988e-05, 1.7189999999999983e-05,
#             #                   1.6874999999999807e-05, 1.655999999999991e-05, 1.6244999999999734e-05]]]
#             # self.assertListEqual(result, expected)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#         # finally:
#         #     tab = [result, expected_result]
#         #     print("\n")
#         #     print(inspect.currentframe().f_code.co_name)
#         #     print(tabulate(tab, headers='keys', tablefmt='rst'))
#         # return
#
#     def test_express_extrapolate_f(self):
#         """
#         unittest for function agdrift.express_extrapolate_f:
#         :return:
#         """
#
#         # create empty pandas dataframes to create empty object for this unittest
#         agdrift_empty = self.create_agdrift_object()
#
#         try:
#             agdrift_empty.load_data()
#             agdrift_empty.distance = pd.Series([6.])
#             agdrift_empty.out_y = agdrift_empty.pond_ground_low_f2m
#             expected_result = agdrift_empty.express_extrapolate_f()
#             npt.assert_allclose(expected_result, 0.004774, rtol=1e-5,atol=0, err_msg='', verbose=True)
#         finally:
#             tab = [result, expected_result]
#             print("\n")
#             print(inspect.currentframe().f_code.co_name)
#             print(tabulate(tab, headers='keys', tablefmt='rst'))
#         return
#         # finally:
#         #     tab = [expected_result]
#         #     print("\n")
#         #     print(inspect.currentframe().f_code.co_name)
#         #     print(tabulate(tab, headers='keys', tablefmt='rst'))
#         # return


    # def test_deposition_foa_to_lbac_f(self):
    #     """
    #     unittest for function agdrift.deposition_foa_to_lbac_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         agdrift_empty.distance = pd.Series([75.])
    #         agdrift_empty.out_y = agdrift_empty.pond_aerial_vf2f
    #         agdrift_empty.application_rate = pd.Series([1.7])
    #         agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         expected_result = agdrift_empty.deposition_foa_to_lbac_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result, 0.155193, rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_lbac_to_gha_f(self):
    #     """
    #     unittest for function agdrift.deposition_lbac_to_gha_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         agdrift_empty.distance = pd.Series([12.])
    #         agdrift_empty.out_y = agdrift_empty.pond_ground_high_f2m
    #         agdrift_empty.application_rate = pd.Series([2.5])
    #         #agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
    #         excepted_result = agdrift_empty.deposition_lbac_to_gha_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(excepted_result, 17.19102539, rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [excepted_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_foa_to_gha_f(self):
    #     """
    #     unittest for function agdrift.deposition_foa_to_gha_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         #agdrift_empty.load_data()
    #         #agdrift_empty.distance = pd.Series([130.])
    #         #agdrift_empty.out_y = agdrift_empty.pond_airblast_orchard
    #         agdrift_empty.application_rate = pd.Series([2.2], dtype='float')
    #         agdrift_empty.out_init_avg_dep_foa = pd.Series([0.2], dtype='float')
    #         expected_result = agdrift_empty.deposition_foa_to_gha_f()
    #         npt.assert_allclose(expected_result,0.032824,rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_gha_to_ngl_f(self):
    #     """
    #     unittest for function agdrift.deposition_gha_to_ngl_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         #agdrift_empty.distance = pd.Series([128.])
    #         #agdrift_empty.out_y = agdrift_empty.pond_ground_high_f2m
    #         #agdrift_empty.application_rate = pd.Series([5.2])
    #         #agdrift_empty.out_init_avg_dep_foa = pd.Series([0.2], dtype='float')
    #         #agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
    #         agdrift_empty.out_avg_depo_gha = pd.Series([0.2], dtype='float')
    #         agdrift_empty.aquatic_type = pd.Series([1], dtype='float')
    #         expected_result = agdrift_empty.deposition_gha_to_ngl_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result,10,rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # except:
    #     #     pass
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_ngl_2_gha_f(self):
    #     """
    #     unittest for function agdrift.deposition_ngl_2_gha_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         # agdrift_empty.distance = pd.Series([223.])
    #         # agdrift_empty.out_y = agdrift_empty.pond_aerial_f2m
    #         # agdrift_empty.application_rate = pd.Series([5.8])
    #         # agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         # agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
    #         # agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
    #         agdrift_empty.out_deposition_ngl = pd.Series([0.2], dtype='float')
    #         agdrift_empty.aquatic_type = pd.Series([1])
    #         expected_result = agdrift_empty.deposition_ngl_2_gha_f()
    #         # npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result, 0.004, rtol=1e-5, atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # except:
    #     #     pass
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_gha_to_mgcm_f(self):
    #     """
    #     unittest for function agdrift.deposition_gha_to_mgcm_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         #agdrift_empty.distance = pd.Series([190.])
    #         #agdrift_empty.out_y = agdrift_empty.pond_ground_low_f2m
    #         #agdrift_empty.application_rate = pd.Series([2.1])
    #         #agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         #agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
    #         #agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
    #         agdrift_empty.out_avg_depo_gha = pd.Series([0.2], dtype='float')
    #         expected_result = agdrift_empty.deposition_gha_to_mgcm_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result,0.554622,rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    #
    # def test_deposition_ghac_to_lbac_f(self):
    #     """
    #     unittest for function agdrift.deposition_ghac_to_lbac_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         #agdrift_empty.distance = pd.Series([270.])
    #         #agdrift_empty.out_y = agdrift_empty.pond_airblast_vineyard
    #         #agdrift_empty.application_rate = pd.Series([6.5])
    #         #agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         #agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
    #         agdrift_empty.out_avg_depo_gha = pd.Series([0.2], dtype='float')
    #         expected_result = agdrift_empty.deposition_ghac_to_lbac_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result,0.000178,rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_lbac_to_foa_f(self):
    #     """
    #     unittest for function agdrift.deposition_lbac_to_foa_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         #agdrift_empty.distance = pd.Series([200.])
    #         #agdrift_empty.out_y = agdrift_empty.pond_ground_low_f2m
    #         agdrift_empty.application_rate = pd.Series([3.5])
    #         #agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         agdrift_empty.out_avg_depo_lbac = pd.Series([0.2], dtype='float')
    #         expected_result = agdrift_empty.deposition_lbac_to_foa_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result,0.057143,rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    #
    # def test_deposition_mgcm_to_gha_f(self):
    #     """
    #     unittest for function agdrift.deposition_mgcm_to_gha_f:
    #     :return:
    #     """
    #
    #     # create empty pandas dataframes to create empty object for this unittest
    #     agdrift_empty = self.create_agdrift_object()
    #
    #     try:
    #         agdrift_empty.load_data()
    #         #agdrift_empty.distance = pd.Series([76.])
    #         #agdrift_empty.out_y = agdrift_empty.pond_airblast_vineyard
    #         #agdrift_empty.application_rate = pd.Series([0.23])
    #         #agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
    #         #agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
    #         #agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
    #         agdrift_empty.out_deposition_mgcm = pd.Series([0.002], dtype='float')
    #         expected_result = agdrift_empty.deposition_mgcm_to_gha_f()
    #         #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
    #         npt.assert_allclose(expected_result,200,rtol=1e-5,atol=0, err_msg='', verbose=True)
    #     finally:
    #         tab = [result, expected_result]
    #         print("\n")
    #         print(inspect.currentframe().f_code.co_name)
    #         print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     return
    #     # finally:
    #     #     tab = [expected_result]
    #     #     print("\n")
    #     #     print(inspect.currentframe().f_code.co_name)
    #     #     print(tabulate(tab, headers='keys', tablefmt='rst'))
    #     # return
    
# unittest will
# 1) call the setup method
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
