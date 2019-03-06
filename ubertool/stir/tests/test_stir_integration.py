import datetime
import inspect
import logging
import numpy.testing as npt
import os.path
import pandas as pd
import pkgutil
import sys
from tabulate import tabulate
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO, BytesIO

# #find parent directory and import model
# parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(parentddir)
from ..stir_exe import Stir, StirOutputs

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'stir_qaqc_in_transpose.csv')
        data_inputs = BytesIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        #csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
        csv_transpose_path_in = os.path.join(os.path.dirname(__file__),"stir_qaqc_in_transpose.csv")
        logging.info(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        pd_obj_inputs['csrfmiddlewaretoken'] = 'test'
        #with open('./stir_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #logging.info('stir inputs')
    #logging.info('stir input dimensions ' + str(pd_obj_inputs.shape))
    #logging.info('stir input keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #logging.info(pd_obj_inputs)

# load transposed qaqc data for expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# logging.info(pd_obj_exp_out)
# this works for both local nosetests and travis deploy
#expected output details
try:
    if __package__ is not None:
        data_exp_outputs = BytesIO(pkgutil.get_data(__package__, 'stir_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        #logging.info("stir expected outputs")
        #logging.info('stir expected output dimensions ' + str(pd_obj_exp.shape))
        #logging.info('stir expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        #csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
        csv_transpose_path_exp = os.path.join(os.path.dirname(__file__),"stir_qaqc_exp_transpose.csv")
        #logging.info(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #logging.info('stir expected')
    #logging.info('stir expected dimensions ' + str(pd_obj_exp.shape))
    #logging.info('stir expected keys ' + str(pd_obj_exp.columns.values.tolist()))
    #logging.info(pd_obj_exp)


# create an instance of stir object with qaqc data
stir_output_empty = StirOutputs()
stir_calc = Stir(pd_obj_inputs, pd_obj_exp)
stir_calc.execute_model()
inputs_json, outputs_json, exp_out_json = stir_calc.get_dict_rep()
#logging.info("stir output")
#logging.info(inputs_json)

#logging.info input tables
#logging.info(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
#logging.info(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
#logging.info(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#logging.info expected output tables
#logging.info(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

test = {}


class TestStir(unittest.TestCase):
    """
    Integration tests for Stir.
    """
    print("stir integration tests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for stir integration test
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open stir qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for stir integration test
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(stir_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = stir_calc.pd_obj_out.columns[i]
                output = getattr(stir_calc, column_name)
                if isinstance(output, pd.Series):
                    result[i] = True

            tab = pd.concat([result,expected], axis=1)
            print('model output properties as pandas series')
            print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
            npt.assert_array_equal(result, expected)
        finally:
            pass
        return

    def test_assert_output_series_dtypes(self):
        """ Verify that each output variable is the correct dtype """

        try:
            num_variables = len(stir_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = stir_calc.pd_obj_out.columns[i]
                output_result = getattr(stir_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(stir_output_empty, column_name)
                output_expected2 = getattr(stir_calc.pd_obj_out, column_name)
                column_dtype_expected = output_expected.dtype.name
                if column_dtype_result == column_dtype_expected:
                    result[i] = True

                #tab = pd.concat([result,expected], axis=1)
                if(result[i] != expected[i]):
                    print(i)
                    print(column_name)
                    print(str(result[i]) + "/" + str(expected[i]))
                    print(column_dtype_result + "/" + column_dtype_expected)
                    print('result')
                    print(output_result)
                    print('expected')
                    print(output_expected2)
                #print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
            npt.assert_array_equal(result, expected)
        finally:
            pass
        return

    def test_stir_sat_air_conc(self):
        """
        Integration test for stir.out_sat_air_conc
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('sat_air_conc', func_name)
        finally:
            pass
        return

    def test_stir_inh_rate_avian(self):
        """
        integration test for stir.out_inh_rate_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('inh_rate_avian', func_name)
        finally:
            pass
        return

    def test_stir_vid_avian(self):
        """
        integration test for stir.out_vid_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('vid_avian', func_name)
        finally:
            pass
        return

    def test_stir_inh_rate_mammal(self):
        """
        integration test for stir.out_inh_rate_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('inh_rate_mammal', func_name)
        finally:
            pass
        return

    def test_stir_vid_mammal(self):
        """
        integration test for stir.out_vid_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('vid_mammal', func_name)
        finally:
            pass
        return

    def test_stir_air_conc(self):
        """
        integration test for stir.out_air_conc
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('air_conc', func_name)
        finally:
            pass
        return

    def test_stir_sid_avian(self):
        """
        integration test for stir.out_sid_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('sid_avian', func_name)
        finally:
            pass
        return

    def test_stir_sid_mammal(self):
        """
        integration test for stir.out_sid_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('sid_mammal', func_name)
        finally:
            pass
        return

    def test_stir_mammal_inhalation_ld50(self):
        """
        integration test for stir.out_mammal_inhalation_ld50
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('mammal_inhalation_ld50', func_name)
        finally:
            pass
        return

    def test_stir_adjusted_mammal_inhalation_ld50(self):
        """
        integration test for stir.out_adjusted_mammal_inhalation_ld50
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('adjusted_mammal_inhalation_ld50', func_name)
        finally:
            pass
        return

    def test_stir_estimated_avian_inhalation_ld50(self):
        """
        integration test for stir.out_estimated_avian_inhalation_ld50
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('estimated_avian_inhalation_ld50', func_name)
        finally:
            pass
        return

    def test_stir_adjusted_avian_inhalation_ld50(self):
        """
        integration test for stir.out_adjusted_avian_inhalation_ld50
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('adjusted_avian_inhalation_ld50', func_name)
        finally:
            pass
        return

    def test_stir_ratio_vid_avian(self):
        """
        integration test for stir.out_ratio_vid_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('ratio_vid_avian', func_name)
        finally:
            pass
        return

    def test_stir_loc_vid_avian(self):
        """
        integration test for stir.out_loc_vid_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('loc_vid_avian', func_name)
        finally:
            pass
        return

    def test_stir_ratio_sid_avian(self):
        """
        integration test for stir.out_ratio_sid_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('ratio_sid_avian', func_name)
        finally:
            pass
        return

    def test_stir_loc_sid_avian(self):
        """
        integration test for stir.out_loc_sid_avian
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('loc_sid_avian', func_name)
        finally:
            pass
        return

    def test_stir_ratio_vid_mammal(self):
        """
        integration test for stir.out_ratio_vid_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('ratio_vid_mammal', func_name)
        finally:
            pass
        return

    def test_stir_loc_vid_mammal(self):
        """
        integration test for stir.out_loc_vid_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('loc_vid_mammal', func_name)
        finally:
            pass
        return

    def test_stir_ratio_sid_mammal(self):
        """
        integration test for stir.out_ratio_sid_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('ratio_sid_mammal', func_name)
        finally:
            pass
        return

    def test_stir_loc_sid_mammal(self):
        """
        integration test for stir.out_loc_sid_mammal
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('loc_sid_mammal', func_name)
        finally:
            pass
        return

    def blackbox_method_int(self, output, func_name):
        """
        Helper method to reuse code for testing numpy array outputs from STIR model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        try:
            pd.set_option('display.float_format', '{:.4E}'.format)  # display model output in scientific notation
            result = stir_calc.pd_obj_out["out_" + output]
            expected = stir_calc.pd_obj_exp["exp_" + output]
            tab = pd.concat([result, expected], axis=1)
            #logging.info(" ")
            #print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
            # npt.assert_array_almost_equal(result, expected, 4, '', True)
            rtol = 1e-5
            npt.assert_allclose(result, expected, rtol, 0, '', True)
        finally:
            tab = pd.concat([result, expected], axis=1)
            print("\n")
            print(func_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def blackbox_method_str(self, output, func_name):
        """
        Helper method
        :param output:
        :return:
        """
        try:
            result = stir_calc.pd_obj_out["out_" + output]
            expected = stir_calc.pd_obj_exp["exp_" + output]
            tab = pd.concat([result, expected], axis=1)
            #print(" ")
            #print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
            npt.assert_array_equal(result, expected)
        finally:
            tab = pd.concat([result, expected], axis=1)
            print("\n")
            print(func_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return


# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
