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
from sip_exe import Sip

#print(sys.path)
#print(os.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'sip_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./sip_qaqc_in_transpose.csv"
        print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./sip_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    print('sip inputs')
    #print('sip input dimensions ' + str(pd_obj_inputs.shape))
    #print('sip input keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(pd_obj_inputs)

#expected output details
try:
    if __package__ is not None:
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'sip_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        print("sip expected outputs")
        print('sip expected output dimensions ' + str(pd_obj_exp.shape))
        print('sip expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        csv_transpose_path_exp = "./sip_qaqc_exp_transpose.csv"
        print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    print('sip expected')

#generate output
sip_calc = Sip(pd_obj_inputs, pd_obj_exp)
sip_calc.execute_model()
inputs_json, outputs_json, exp_out_json = sip_calc.get_dict_rep(sip_calc)
print("sip output")
print(inputs_json)

#print input tables
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#print expected output tables
print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

test = {}


class TestSip(unittest.TestCase):
    """
    Integration tests for Sip.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor for sip integration tests
        :param args:
        :param kwargs:
        :return:
        """
        #adding to TestCase constructor so super
        super(TestSip, self).__init__(*args, **kwargs)
        self.ncases = len(pd_obj_inputs)

    def setUp(self):
        """
        Setup routine for sip integration tests
        :return:
        """
        pass
        # sip2 = sip_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for sip integration tests
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_integration_dose_bird(self):
        """
        Integration test for output sip.dose_bird
        :return:
        """
        try:
            self.blackbox_method_int('dose_bird')
        finally:
            pass
        return

    def test_integration_dose_mamm(self):
        """
        Integration test for output sip.dose_mamm
        :return:
        """
        try:
            self.blackbox_method_int('dose_mamm')
        finally:
            pass
        return

    def test_integration_at_bird(self):
        """
        Integration test for output sip.at_bird
        :return:
        """
        try:
            self.blackbox_method_int('at_bird')
        finally:
            pass
        return

    def test_integration_at_mamm(self):
        """
        Integration test for output sip.at_mamm
        :return:
        """
        try:
            self.blackbox_method_int('at_mamm')
        finally:
            pass
        return

    def test_integration_fi_bird(self):
        """
        Integration test for output sip.fi_bird
        :return:
        """
        try:
            #self.blackbox_method('fi_bird')
            pass
        finally:
            pass
        return

    def test_integration_det(self):
        """
        Integration test for output sip.det
        :return:
        """
        try:
            self.blackbox_method_int('det')
        finally:
            pass
        return

    def test_integration_act(self):
        """
        Integration test for output sip.act
        :return:
        """
        try:
            self.blackbox_method_int('act')
        finally:
            pass
        return

    def test_integration_acute_bird(self):
        """
        Integration test for output sip.acute_bird
        :return:
        """
        try:
            self.blackbox_method_int('acute_bird')
        finally:
            pass
        return

    def test_integration_acuconb(self):
        """
        Integration test for output sip.acuconb
        :return:
        """
        try:
            self.blackbox_method_str('acuconb')
        finally:
            pass
        return

    def test_integration_acute_mamm(self):
        """
        Integration test for output sip.acute_mamm
        :return:
        """
        try:
            self.blackbox_method_int('acute_mamm')
        finally:
            pass
        return

    def test_integration_acuconm(self):
        """
        Integration test for output sip.acuconm
        :return:
        """
        try:
            self.blackbox_method_str('acuconm')
        finally:
            pass
        return

    def test_integration_chron_bird(self):
        """
        Integration test for output sip.chron_bird
        :return:
        """
        try:
            self.blackbox_method_int('chron_bird')
        finally:
            pass
        return

    def test_integration_chronconb(self):
        """
        Integration test for output sip.chronconb
        :return:
        """
        try:
            self.blackbox_method_str('chronconb')
        finally:
            pass
        return

    def test_integration_chron_mamm(self):
        """
        integration test for output sip.chron_mamm
        :return:
        """
        try:
            self.blackbox_method_int('chron_mamm')
        finally:
            pass
        return

    def test_integration_chronconm(self):
        """
        integration test for output sip.chronconm
        :return:
        """
        try:
            self.blackbox_method_str('chronconm')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from SIP model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = sip_calc.pd_obj_out["out_" + output]
        expected = sip_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

    def blackbox_method_str(self, output):
        """
        Helper method that needs to be moved
        :param output:
        :return:
        """
        result = sip_calc.pd_obj_out["out_" + output]
        expected = sip_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print("sip integration test for " + output + "\n")
        print(tab)
        npt.assert_array_equal(result, expected)

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    #unittest.main()
    pass
