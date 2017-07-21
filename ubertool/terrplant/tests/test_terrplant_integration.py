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
from ..terrplant_exe import Terrplant, TerrplantOutputs

#print(sys.path)
#print(os.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'terrplant_qaqc_in_transpose.csv')
        data_inputs = BytesIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./terrplant_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./terrplant_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print("terrplant inputs")
    #print(pd_obj_inputs.shape)
    #print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='plain'))

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = BytesIO(pkgutil.get_data(__package__, 'terrplant_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        csv_transpose_path_exp = "./terrplant_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print("terrplant expected outputs")
    #print('terrplant expected output dimensions ' + str(pd_obj_exp.shape))
    #print('terrplant expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    #print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='plain'))

# create an instance of terrplant object with qaqc data
terrplant_output_empty = TerrplantOutputs()
terrplant_calc = Terrplant(pd_obj_inputs, pd_obj_exp)
terrplant_calc.execute_model()
inputs_json, outputs_json, exp_out_json = terrplant_calc.get_dict_rep()
#print("terrplant output")
#print(inputs_json)
#print("####")
#print(terrplant_calc)
test = {}


class TestTerrplant(unittest.TestCase):
    """
    Integration tests for terrplant.
    """
    print("terrplant integration tests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for terrplant.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for terrplant.
        :return:
        """
        pass

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(terrplant_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = terrplant_calc.pd_obj_out.columns[i]
                output = getattr(terrplant_calc, column_name)
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
            num_variables = len(terrplant_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = terrplant_calc.pd_obj_out.columns[i]
                output_result = getattr(terrplant_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(terrplant_output_empty, column_name)
                output_expected2 = getattr(terrplant_calc.pd_obj_out, column_name)
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

    def test_terrplant_rundry(self):
        """
        Integration test for terrplant.rundry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('run_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_runsemi(self):
        """
        Integration test for terrplant.runsemi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('run_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_spray(self):
        """
        Integration test for terrplant.spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('spray', func_name)
        finally:
            pass
        return

    def test_terrplant_totaldry(self):
        """
        Integration test for terrplant.totaldry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('total_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_totalsemi(self):
        """
        Integration test for terrplant.totalsemi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('total_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_nms_rq_dry(self):
        """
        Integration test for terrplant.nms_rq_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('nms_rq_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_nms_loc_dry(self):
        """
        Integration test for terrplant.nms_loc_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('nms_loc_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_nms_rq_semi(self):
        """
        Integration test for terrplant.nms_rq_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('nms_rq_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_nms_loc_semi(self):
        """
        Integration test for terrplant.nms_loc_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('nms_loc_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_nms_rq_spray(self):
        """
        Integration test for terrplant.nms_rq_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('nms_rq_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_nms_loc_spray(self):
        """
        Integration test for terrplant.nms_loc_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('nms_loc_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_lms_rq_dry(self):
        """
        Integration test for terrplant.lms_rq_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('lms_rq_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_lms_loc_dry(self):
        """
        Integration test for terrplant.lms_loc_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('lms_loc_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_lms_rq_semi(self):
        """
        Integration test for terrplant.lms_rq_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('lms_rq_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_lms_loc_semi(self):
        """
        Integration test for terrplant.lms_loc_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('lms_loc_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_lms_rq_spray(self):
        """
        Integration test for terrplant.lms_rq_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('lms_rq_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_lms_loc_spray(self):
        """
        Integration test for terrplant.lms_loc_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('lms_loc_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_nds_rq_dry(self):
        """
        Integration test for terrplant.nds_rq_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('nds_rq_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_nds_loc_dry(self):
        """
        Integration test for terrplant.nds_loc_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('nds_loc_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_nds_rq_semi(self):
        """
        Integration test for terrplant.nds_rq_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('nds_rq_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_nds_loc_semi(self):
        """
        Integration test for terrplant.nds_loc_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('nds_loc_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_nds_rq_spray(self):
        """
        Integration test for terrplant.nds_rq_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('nds_rq_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_nds_loc_spray(self):
        """
        Integration test for terrplant.nds_loc_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('nds_loc_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_lds_rq_dry(self):
        """
        Integration test for terrplant.lds_rq_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('lds_rq_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_lds_loc_dry(self):
        """
        Integration test for terrplant.lds_loc_dry
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('lds_loc_dry', func_name)
        finally:
            pass
        return

    def test_terrplant_lds_rq_semi(self):
        """
        Integration test for terrplant.lds_rq_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('lds_rq_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_lds_loc_semi(self):
        """
        Integration test for terrplant.lds_loc_semi
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('lds_loc_semi', func_name)
        finally:
            pass
        return

    def test_terrplant_lds_rq_spray(self):
        """
        Integration test for terrplant.lds_rq_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('lds_rq_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_lds_loc_spray(self):
        """
        Integration test for terrplant.lds_loc_spray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_str('lds_loc_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_min_nms_spray(self):
        """
        Integration test for terrplant.minnmsspray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('min_nms_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_min_lms_spray(self):
        """
        Integration test for terrplant.minlmsspray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('min_lms_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_min_nds_spray(self):
        """
        Integration test for terrplant.minndsspray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('min_nds_spray', func_name)
        finally:
            pass
        return

    def test_terrplant_min_lds_spray(self):
        """
        Integration test for terrplant.minldsspray
        """
        try:
            func_name = inspect.currentframe().f_code.co_name
            self.blackbox_method_int('min_lds_spray', func_name)
        finally:
            pass
        return

    def blackbox_method_int(self, output, func_name):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        try:
            pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
            result = terrplant_calc.pd_obj_out["out_" + output]
            expected = terrplant_calc.pd_obj_exp["exp_" + output]
            #tab = pd.concat([result,expected], axis=1)
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
        Helper method.
        :param output:
        :return:
        """
        try:
            result = terrplant_calc.pd_obj_out["out_" + output]
            expected = terrplant_calc.pd_obj_exp["exp_" + output]
            tab = pd.concat([result,expected], axis=1)
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