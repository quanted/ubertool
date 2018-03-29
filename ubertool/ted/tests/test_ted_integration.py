from __future__ import division  # brings in Python 3.0 mixed type calculation rules
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

from ..ted_exe import Ted, TedOutputs

# #find parent directory and import model
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# print("parent_dir")
# print(parent_dir)
# sys.path.append(parent_dir)


print("sys.path")
print(sys.path)

# load transposed qaqc data for inputs and expected outputs
# input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'ted_qaqc_in_transpose.csv')
        data_inputs = BytesIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        #csv_transpose_path_in = "./ted_qaqc_in_transpose.csv"
        csv_transpose_path_in = os.path.join(os.path.dirname(__file__), "ted_qaqc_in_transpose.csv")
        # print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        # with open('./ted_qaqc_in_transpose.csv') as f:
        # csv_data = csv.reader(f)
finally:
    pass

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = BytesIO(pkgutil.get_data(__package__, 'ted_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        #csv_transpose_path_exp = "./ted_qaqc_exp_transpose.csv"
        csv_transpose_path_exp = os.path.join(os.path.dirname(__file__), "ted_qaqc_exp_transpose.csv")
        # print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass

# create an instance of ted object with qaqc data
ted_output_empty = TedOutputs()
ted_calc = Ted(pd_obj_inputs, pd_obj_exp)
ted_calc.execute_model()
inputs_json, outputs_json, exp_out_json = ted_calc.get_dict_rep()

test = {}

class Testted(unittest.TestCase):
    """
    Integration tests for ted.
    """
    def setUp(self):
        """
        Setup routine for ted.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for ted.
        :return:
        """
        pass

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(ted_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = ted_calc.pd_obj_out.columns[i]
                output = getattr(ted_calc, column_name)
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
            num_variables = len(ted_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = ted_calc.pd_obj_out.columns[i]
                output_result = getattr(ted_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(ted_output_empty, column_name)
                output_expected2 = getattr(ted_calc.pd_obj_out, column_name)
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
                # print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
            npt.assert_array_equal(result, expected)
        finally:
            pass
        return

    def test_diet_eec_upper_min_sg_maxdaily(self):
        """
        Integration test for ted.eec_diet_sg
        """
        try:
            self.blackbox_method_int('diet_eec_upper_min_sg_maxdaily')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format', lambda x: '{0:.10e}'.format(x))
        result = ted_calc.pd_obj_out["out_" + output]
        expected = ted_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        err_msg = str(result) + '\n' + str(expected)
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, True, err_msg)

    def blackbox_method_str(self, output):
        """
        Helper method.
        :param output:
        :return:
        """
        result = ted_calc.pd_obj_out["out_" + output]
        expected = ted_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()