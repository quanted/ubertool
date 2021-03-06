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
from ..rice_exe import Rice, RiceOutputs

#print(sys.path)
#print(os.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'rice_qaqc_in_transpose.csv')
        data_inputs = BytesIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = os.path.join(os.path.dirname(__file__), 'rice_qaqc_in_transpose.csv')
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        pd_obj_inputs['csrfmiddlewaretoken'] = 'test'
        #with open('./rice_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print('rice inputs')
    #print('rice input dimensions ' + str(pd_obj_inputs.shape))
    #print('rice input keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(pd_obj_inputs)

# load transposed qaqc data for expected outputs
# works for local nosetests from parent directory
# but not for travis container that calls nosetests:
# csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
# pd_obj_exp_out = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
# print(pd_obj_exp_out)
# this works for both local nosetests and travis deploy
#expected output details
try:
    if __package__ is not None:
        data_exp_outputs = BytesIO(pkgutil.get_data(__package__, 'rice_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        #print("rice expected outputs")
        #print('rice expected output dimensions ' + str(pd_obj_exp.shape))
        #print('rice expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        #csv_transpose_path_exp = "./rice_qaqc_exp_transpose.csv"
        csv_transpose_path_exp = os.path.join(os.path.dirname(__file__), 'rice_qaqc_exp_transpose.csv')
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print('rice expected')

#generate output
rice_output_empty = RiceOutputs()
rice_calc = Rice(pd_obj_inputs, pd_obj_exp)
rice_calc.execute_model()
inputs_json, outputs_json, exp_out_json = rice_calc.get_dict_rep()
#print("rice output")
#print(inputs_json)

#
#print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#
#print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

test = {}


class TestRice(unittest.TestCase):
    """
    Integration tests for Rice.
    """
    print("rice integration tests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routing for rice tests
        :return:
        """
        pass
        # rice2 = rice_model.rice(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open rice qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routing for rice tests
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(rice_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = rice_calc.pd_obj_out.columns[i]
                output = getattr(rice_calc, column_name)
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
            num_variables = len(rice_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = rice_calc.pd_obj_out.columns[i]
                output_result = getattr(rice_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(rice_output_empty, column_name)
                output_expected2 = getattr(rice_calc.pd_obj_out, column_name)
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

    def test_rice_msed_integration(self):
        """
        Test for calcmsed
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('msed', func_name)
        finally:
            pass
        return

    def test_rice_vw_integration(self):
        """
        Test for calcvw
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('vw', func_name)
        finally:
            pass
        return

    def test_rice_mass_area_integration(self):
        """
        Test for calcmass
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('mass_area', func_name)
        finally:
            pass
        return

    def test_rice_cw_integration(self):
        """
        Test for calccw
        :param self:
        :return:
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('cw', func_name)
        finally:
            pass
        return

    def blackbox_method_float(self, output, func_name):
        """
        Helper method to reuse code for testing numpy array outputs from rice model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        try:
            pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
            result = rice_calc.pd_obj_out["out_" + output]
            expected = rice_calc.pd_obj_exp["exp_" + output]
            # npt.assert_array_almost_equal(result, expected, 4, '', True)
            rtol = 1e-5
            npt.assert_allclose(result, expected, rtol, 0, '', True)
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
    pass