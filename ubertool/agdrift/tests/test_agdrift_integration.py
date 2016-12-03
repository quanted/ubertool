from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import pkgutil
from StringIO import StringIO
import sys
from tabulate import tabulate
import unittest

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
print(parentddir)
sys.path.append(parentddir)
from agdrift_exe import Agdrift

print(sys.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'agdrift_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./agdrift_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./agdrift_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print('agdrift inputs')
    #print('agdrift input dimensions ' + str(pd_obj_inputs.shape))
    #print('agdrift input keys ' + str(pd_obj_inputs.columns.values.tolist()))
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
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'agdrift_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        #print("agdrift expected outputs")
        #print('agdrift expected output dimensions ' + str(pd_obj_exp.shape))
        #print('agdrift expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        csv_transpose_path_exp = "./agdrift_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print('agdrift expected')

#generate output
agdrift_calc = Agdrift(pd_obj_inputs, pd_obj_exp)
agdrift_calc.execute_model()
inputs_json, outputs_json, exp_out_json = agdrift_calc.get_dict_rep()
#print("agdrift output")
#print(inputs_json)

#print input tables
#print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
#print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#print expected output tables
#print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

test = {}


class TestAgdrift(unittest.TestCase):
    """
    Integration tests for agdrift model.
    """
    print("agdrift integration tests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Test setup method.
        :return:
        """
        pass

    def tearDown(self):
        """
        Test teardown method.
        :return:
        """
        pass

    def test_agdrift_init_avg_dep_foa_integration(self):
        """
        Integration test for agdrift.agdrift_fugacity
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('init_avg_dep_foa', func_name)
        finally:
            pass
        return

    def test_agdrift_init_avg_dep_foa_integration(self):
        """
        Integration test for agdrift.agdrift_fugacity
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('avg_dep_lbac', func_name)
        finally:
            pass
        return

    def test_agdrift_init_avg_dep_foa_integration(self):
        """
        Integration test for agdrift.agdrift_fugacity
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('avg_dep_gha', func_name)
        finally:
            pass
        return

    def test_agdrift_init_avg_dep_foa_integration(self):
        """
        Integration test for agdrift.agdrift_fugacity
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('deposition_ngL', func_name)
        finally:
            pass
        return

    def test_agdrift_init_avg_dep_foa_integration(self):
        """
        Integration test for agdrift.agdrift_fugacity
        """
        func_name = inspect.currentframe().f_code.co_name
        try:
            self.blackbox_method_float('deposition_mgcm', func_name)
        finally:
            pass
        return

    def blackbox_method_float(self, output, func_name):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        try:
            pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
            result = agdrift_calc.pd_obj_out["out_" + output]
            expected = agdrift_calc.pd_obj_exp["exp_" + output]
            #npt.assert_array_almost_equal(result, expected, 4, '', True)
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