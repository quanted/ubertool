import logging
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
from iec_exe import Iec

#print(sys.path)
#print(os.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'iec_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./iec_qaqc_in_transpose.csv"
        print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./iec_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    print('iec inputs')
    #print('iec input dimensions ' + str(pd_obj_inputs.shape))
    #print('iec input keys ' + str(pd_obj_inputs.columns.values.tolist()))
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
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'iec_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        print("iec expected outputs")
        print('iec expected output dimensions ' + str(pd_obj_exp.shape))
        print('iec expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        csv_transpose_path_exp = "./iec_qaqc_exp_transpose.csv"
        print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    print('iec expected')


# create an instance of iec object with qaqc data
#print("####")
#print("dead here")
iec_calc = Iec(pd_obj_inputs, pd_obj_exp)
iec_calc.execute_model()
inputs_json, outputs_json, exp_out_json = iec_calc.get_dict_rep(iec_calc)
print("iec output")
print(inputs_json)

#print input tables
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#print expected output tables
print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

logging.info("###iec_calc.pd_obj_exp")
logging.info(iec_calc.pd_obj_exp)
test = {}


class TestIec(unittest.TestCase):
    """
    Integration tests for SIP model.
    """
    def __init__(self, *args, **kwargs):
        """
        adding to TestCase constructor so super
        :param args:
        :param kwargs:
        :return:
        """
        super(TestIec, self).__init__(*args, **kwargs)
        self.ncases = len(pd_obj_inputs)

    def setUp(self):
        """
        Test setup method.
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

    def test_integration_z_score_f(self):
        """
        integration test for output iec.z_score_f
        """
        try:
            self.blackbox_method_int('z_score_f')
        finally:
            pass
        return

    def test_integration_f8_f(self):
        """
        integration test for output iec.f8_f
        """
        try:
            self.blackbox_method_int('f8_f')
        finally:
            pass
        return

    def test_integration_chance_f(self):
        """
        integration test for output iec.chance_f
        """
        try:
            self.blackbox_method_int('chance_f')
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
        logging.info('### blackbox out_' + output)
        logging.info(iec_calc.pd_obj_out)
        result = iec_calc.pd_obj_out["out_" + output]
        expected = iec_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        #npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result,expected,rtol,0,'',True)


# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    #unittest.main()
    pass
