import datetime
import inspect
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
from ..screenip_exe import Screenip, ScreenipOutputs

#print(sys.path)
#print(os.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'screenip_qaqc_in_transpose.csv')
        data_inputs = BytesIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./screenip_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./screenip_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print('screenip inputs')
    #print('screenip input dimensions ' + str(pd_obj_inputs.shape))
    #print('screenip input keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(pd_obj_inputs)

#expected output details
try:
    if __package__ is not None:
        data_exp_outputs = BytesIO(pkgutil.get_data(__package__, 'screenip_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        #print("screenip expected outputs")
        #print('screenip expected output dimensions ' + str(pd_obj_exp.shape))
        #print('screenip expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        csv_transpose_path_exp = "./screenip_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print('screenip expected')

#generate output
screenip_output_empty = ScreenipOutputs()
screenip_calc = Screenip(pd_obj_inputs, pd_obj_exp)
screenip_calc.execute_model()
inputs_json, outputs_json, exp_out_json = screenip_calc.get_dict_rep()
#print("screenip output")
#print(inputs_json)

#
#print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#
#print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

test = {}


class TestScreenip(unittest.TestCase):
    """
    Integration tests for screenip.
    """
    print("screenip integration tests conducted at " + str(datetime.datetime.today()))

    def __init__(self, *args, **kwargs):
        """
        Constructor for screenip integration tests
        :param args:
        :param kwargs:
        :return:
        """
        #adding to TestCase constructor so super
        super(TestScreenip, self).__init__(*args, **kwargs)
        self.ncases = len(pd_obj_inputs)

    def setUp(self):
        """
        Setup routine for screenip integration tests
        :return:
        """
        pass
        # screenip2 = screenip_model.screenip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open screenip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for screenip integration tests
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(screenip_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = screenip_calc.pd_obj_out.columns[i]
                output = getattr(screenip_calc, column_name)
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
            num_variables = len(screenip_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = screenip_calc.pd_obj_out.columns[i]
                output_result = getattr(screenip_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(screenip_output_empty, column_name)
                output_expected2 = getattr(screenip_calc.pd_obj_out, column_name)
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

    def test_screenip_integration_dose_bird(self):
        """
        Integration test for output screenip.dose_bird
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('dose_bird', func_name)
        finally:
            pass
        return

    def test_screenip_integration_dose_mamm(self):
        """
        Integration test for output screenip.dose_mamm
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('dose_mamm', func_name)
        finally:
            pass
        return

    def test_screenip_integration_at_bird(self):
        """
        Integration test for output screenip.at_bird
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('at_bird', func_name)
        finally:
            pass
        return

    def test_screenip_integration_at_mamm(self):
        """
        Integration test for output screenip.at_mamm
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('at_mamm', func_name)
        finally:
            pass
        return

    # def test_screenip_integration_fi_bird(self):
    #     """
    #     Integration test for output screenip.fi_bird
    #     :return:
    #     """
    #     func_name = inspect.currentframe().f_code.co_name
    #     try:
    #         self.blackbox_method_int('fi_bird', func_name)
    #         pass
    #     finally:
    #         pass
    #     return

    def test_screenip_integration_det(self):
        """
        Integration test for output screenip.det
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('det', func_name)
        finally:
            pass
        return

    def test_screenip_integration_act(self):
        """
        Integration test for output screenip.act
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('act', func_name)
        finally:
            pass
        return

    def test_screenip_integration_acute_bird(self):
        """
        Integration test for output screenip.acute_bird
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('acute_bird', func_name)
        finally:
            pass
        return

    def test_screenip_integration_acuconb(self):
        """
        Integration test for output screenip.acuconb
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_str('acuconb', func_name)
        finally:
            pass
        return

    def test_screenip_integration_acute_mamm(self):
        """
        Integration test for output screenip.acute_mamm
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('acute_mamm', func_name)
        finally:
            pass
        return

    def test_screenip_integration_acuconm(self):
        """
        Integration test for output screenip.acuconm
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_str('acuconm', func_name)
        finally:
            pass
        return

    def test_screenip_integration_chron_bird(self):
        """
        Integration test for output screenip.chron_bird
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('chron_bird', func_name)
        finally:
            pass
        return

    def test_screenip_integration_chronconb(self):
        """
        Integration test for output screenip.chronconb
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_str('chronconb', func_name)
        finally:
            pass
        return

    def test_screenip_integration_chron_mamm(self):
        """
        integration test for output screenip.chron_mamm
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_int('chron_mamm', func_name)
        finally:
            pass
        return

    def test_screenip_integration_chronconm(self):
        """
        integration test for output screenip.chronconm
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_str('chronconm', func_name)
        finally:
            pass
        return

    def blackbox_method_int(self, output, func_name):
        """
        Helper method to reuse code for testing numpy array outputs from screenip model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        try:
            pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
            result = screenip_calc.pd_obj_out["out_" + output]
            expected = screenip_calc.pd_obj_exp["exp_" + output]
            tab = pd.concat([result, expected], axis=1)
            #print(" ")
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
        Helper method that needs to be moved
        :param output:
        :return:
        """
        try:
            result = screenip_calc.pd_obj_out["out_" + output]
            expected = screenip_calc.pd_obj_exp["exp_" + output]
            tab = pd.concat([result, expected], axis=1)
            print("screenip integration test for " + output + "\n")
            print(tab)
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
    #unittest.main()
    pass
