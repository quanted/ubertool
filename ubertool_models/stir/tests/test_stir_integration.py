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
from stir_exe import Stir

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'stir_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./stir_qaqc_in_transpose.csv"
        print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./stir_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    print('stir inputs')
    #print('stir input dimensions ' + str(pd_obj_inputs.shape))
    #print('stir input keys ' + str(pd_obj_inputs.columns.values.tolist()))
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
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'stir_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
        print("stir expected outputs")
        print('stir expected output dimensions ' + str(pd_obj_exp.shape))
        print('stir expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    else:
        csv_transpose_path_exp = "./stir_qaqc_exp_transpose.csv"
        print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    print('stir expected')

# create an instance of stir object with qaqc data
stir_calc = Stir(pd_obj_inputs, pd_obj_exp)
stir_calc.execute_model
inputs_json, outputs_json, exp_out_json = sip_calc.get_dict_rep(sip_calc)
print("stir output")
print(inputs_json)

#print input tables
print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,6:11], headers='keys', tablefmt='fancy_grid'))
print(tabulate(pd_obj_inputs.iloc[:,12:17], headers='keys', tablefmt='fancy_grid'))

#print expected output tables
print(tabulate(pd_obj_exp.iloc[:,0:1], headers='keys', tablefmt='fancy_grid'))

test = {}


class TestStir(unittest.TestCase):
    """
    Integration tests for Stir.
    """

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

    def test_sat_air_conc(self):
        """
        Integration test for stir.out_sat_air_conc
        """
        try:
            self.blackbox_method_int('out_sat_air_conc')
        finally:
            pass
        return

    def test_inh_rate_avian(self):
        """
        integration test for stir.out_inh_rate_avian
        """
        try:
            self.blackbox_method_int('out_inh_rate_avian')
        finally:
            pass
        return

    def test_vid_avian(self):
        """
        integration test for stir.out_vid_avian
        """
        try:
            self.blackbox_method_int('out_vid_avian')
        finally:
            pass
        return

    def test_inh_rate_mammal(self):
        """
        integration test for stir.out_inh_rate_mammal
        """
        try:
            self.blackbox_method_int('out_inh_rate_mammal')
        finally:
            pass
        return

    def test_vid_mammal(self):
        """
        integration test for stir.out_vid_mammal
        """
        try:
            self.blackbox_method_int('out_vid_mammal')
        finally:
            pass
        return

    def test_air_conc(self):
        """
        integration test for stir.out_air_conc
        """
        try:
            self.blackbox_method_int('out_air_conc')
        finally:
            pass
        return

    def test_sid_avian(self):
        """
        integration test for stir.out_sid_avian
        """
        try:
            self.blackbox_method_int('out_sid_avian')
        finally:
            pass
        return

    def test_sid_mammal(self):
        """
        integration test for stir.out_sid_mammal
        """
        try:
            self.blackbox_method_int('out_sid_mammal')
        finally:
            pass
        return

    def test_mammal_inhalation_ld50(self):
        """
        integration test for stir.out_mammal_inhalation_ld50
        """
        try:
            self.blackbox_method_int('out_mammal_inhalation_ld50')
        finally:
            pass
        return

    def test_adjusted_mammal_inhalation_ld50(self):
        """
        integration test for stir.out_adjusted_mammal_inhalation_ld50
        """
        try:
            self.blackbox_method_int('out_adjusted_mammal_inhalation_ld50')
        finally:
            pass
        return

    def test_estimated_avian_inhalation_ld50(self):
        """
        integration test for stir.out_estimated_avian_inhalation_ld50
        """
        try:
            self.blackbox_method_int('out_estimated_avian_inhalation_ld50')
        finally:
            pass
        return

    def test_adjusted_avian_inhalation_ld50(self):
        """
        integration test for stir.out_adjusted_avian_inhalation_ld50
        """
        try:
            self.blackbox_method_int('out_adjusted_avian_inhalation_ld50')
        finally:
            pass
        return

    def test_ratio_vid_avian(self):
        """
        integration test for stir.out_ratio_vid_avian
        """
        try:
            self.blackbox_method_int('out_ratio_vid_avian')
        finally:
            pass
        return

    def test_loc_vid_avian(self):
        """
        integration test for stir.out_loc_vid_avian
        """
        try:
            self.blackbox_method_str('out_loc_vid_avian')
        finally:
            pass
        return

    def test_ratio_sid_avian(self):
        """
        integration test for stir.out_ratio_sid_avian
        """
        try:
            self.blackbox_method_int('out_ratio_sid_avian')
        finally:
            pass
        return

    def test_loc_sid_avian(self):
        """
        integration test for stir.out_loc_sid_avian
        """
        try:
            self.blackbox_method_str('out_loc_sid_avian')
        finally:
            pass
        return

    def test_ratio_vid_mammal(self):
        """
        integration test for stir.out_ratio_vid_mammal
        """
        try:
            self.blackbox_method_int('out_ratio_vid_mammal')
        finally:
            pass
        return

    def test_loc_vid_mammal(self):
        """
        integration test for stir.out_loc_vid_mammal
        """
        try:
            self.blackbox_method_str('out_loc_vid_mammal')
        finally:
            pass
        return

    def test_ratio_sid_mammal(self):
        """
        integration test for stir.out_ratio_sid_mammal
        """
        try:
            self.blackbox_method_int('out_ratio_sid_mammal')
        finally:
            pass
        return

    def test_loc_sid_mammal(self):
        """
        integration test for stir.out_loc_sid_mammal
        """
        try:
            self.blackbox_method_str('out_loc_sid_mammal')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from STIR model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format', '{:.4E}'.format)  # display model output in scientific notation
        result = stir_calc.pd_obj_out[output]
        expected = stir_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, '', True)

    def blackbox_method_str(self, output):
        """
        Helper method
        :param output:
        :return:
        """
        result = stir_calc.pd_obj_out[output]
        expected = stir_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result, expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        npt.assert_array_equal(result, expected)


# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
