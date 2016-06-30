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
sys.path.append(parentddir)
from trex_exe import TRex

#print(sys.path)
#print(os.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'trex_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./trex_qaqc_in_transpose.csv"
        print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./sip_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    print("trex inputs")
    print(pd_obj_inputs.shape)
    print('trex expected output keys ' + str(pd_obj_inputs.columns.values.tolist()))
    print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='plain'))
    print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='plain'))
    print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='plain'))
    print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='plain'))

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'trex_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        csv_transpose_path_exp = "./trex_qaqc_exp_transpose.csv"
        print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    print("trex expected outputs")
    print('trex expected output dimensions ' + str(pd_obj_exp.shape))
    print('trex expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='plain'))
    print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='plain'))
    print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='plain'))
    print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='plain'))

# create an instance of trex object with qaqc data
trex_calc = TRex(pd_obj_inputs, pd_obj_exp)
trex_calc.execute_model()
inputs_json, outputs_json, exp_out_json = trex_calc.get_dict_rep(trex_calc)
print("trex output")
print(inputs_json)
print("####")
print(trex_calc)
test = {}
trex_calc.execute_model()

class TestTRex(unittest.TestCase):
    """
    Integration tests for trex.
    """
    def setUp(self):
        """
        Setup routine for trex.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for trex.
        :return:
        """
        pass

    def test_eec_diet_sg(self):
        """
        Integration test for trex.rundry
        """
        try:
            self.blackbox_method_int('eec_diet_sg')
        finally:
            pass
        return

    def test_eec_diet_tg(self):
        """
        Integration test for trex.runsemi
        """
        try:
            self.blackbox_method_int('eec_diet_tg')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = trex_calc.pd_obj_out["out_" + output]
        expected = trex_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

    def blackbox_method_str(self, output):
        """
        Helper method.
        :param output:
        :return:
        """
        result = trex_calc.pd_obj_out["out_" + output]
        expected = trex_calc.pd_obj_exp["exp_" + output]
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