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
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
print("parent_dir")
print(parent_dir)
sys.path.append(parent_dir)
from beerex_exe import Beerex

print("sys.path")
print(sys.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'beerex_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./beerex_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./beerex_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print("beerex inputs")
    #print(pd_obj_inputs.shape)
    #print('beerex expected output keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='plain'))

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, './beerex_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        csv_transpose_path_exp = "./beerex_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print("beerex expected outputs")
    #print('beerex expected output dimensions ' + str(pd_obj_exp.shape))
    #print('beerex expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    #print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='plain'))

# create an instance of trex object with qaqc data
beerex_calc = Beerex(pd_obj_inputs, pd_obj_exp)
beerex_calc.execute_model()
inputs_json, outputs_json, exp_out_json = beerex_calc.get_dict_rep(beerex_calc)
    #print("beerex output")
    #print(inputs_json)
    #print("####")
    #######print(beerex_calc)
test = {}
######beerex_calc.execute_model()

class TestBeerex(unittest.TestCase):
    """
    Integration tests for beerex.
    """
    def setUp(self):
        """
        Setup routine for beerex.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for beerex.
        :return:
        """
        pass

    def test_eec_spray(self):
        """
        Integration test for beerex.eec_spray
        """
        try:
            self.blackbox_method_int('eec_spray')
        finally:
            pass
        return

    def test_eec_soil(self):
        """
        Integration test for beerex.eec_soil
        """
        try:
            self.blackbox_method_int('eec_soil')
        finally:
            pass
        return

    def test_eec_seed(self):
        """
        Integration test for beerex.eec_seed
        """
        try:
            self.blackbox_method_int('eec_seed')
        finally:
            pass
        return

    def test_eec_tree(self):
        """
        Integration test for beerex.eec_tree
        """
        try:
            self.blackbox_method_int('eec_tree')
        finally:
            pass
        return

    def test_eec_method(self):
        """
        Integration test for beerex.eec_method
        """
        try:
            self.blackbox_method_int('eec_method')
        finally:
            pass
        return

    def test_lw1_total_dose(self):
        """
        Integration test for beerex.lw1_total_dose
        """
        try:
            self.blackbox_method_int('lw1_total_dose')
        finally:
            pass
        return

    def test_lw2_total_dose(self):
        """
        Integration test for beerex.lw2_total_dose
        """
        try:
            self.blackbox_method_int('lw2_total_dose')
        finally:
            pass
        return

    def test_lw3_total_dose(self):
        """
        Integration test for beerex.lw3_total_dose
        """
        try:
            self.blackbox_method_int('lw3_total_dose')
        finally:
            pass
        return

    def test_lw4_total_dose(self):
        """
        Integration test for beerex.lw4_total_dose
        """
        try:
            self.blackbox_method_int('lw4_total_dose')
        finally:
            pass
        return

    def test_lw5_total_dose(self):
        """
        Integration test for beerex.lw5_total_dose
        """
        try:
            self.blackbox_method_int('lw5_total_dose')
        finally:
            pass
        return

    def test_ld6_total_dose(self):
        """
        Integration test for beerex.ld6_total_dose
        """
        try:
            self.blackbox_method_int('ld6_total_dose')
        finally:
            pass
        return

    def test_lq1_total_dose(self):
        """
        Integration test for beerex.lq1_total_dose
        """
        try:
            self.blackbox_method_int('lq1_total_dose')
        finally:
            pass
        return

    def test_lq2_total_dose(self):
        """
        Integration test for beerex.lq2_total_dose
        """
        try:
            self.blackbox_method_int('lq2_total_dose')
        finally:
            pass
        return

    def test_lq3_total_dose(self):
        """
        Integration test for beerex.lq3_total_dose
        """
        try:
            self.blackbox_method_int('lq3_total_dose')
        finally:
            pass
        return

    def test_lq4_total_dose(self):
        """
        Integration test for beerex.lq4_total_dose
        """
        try:
            self.blackbox_method_int('lq4_total_dose')
        finally:
            pass
        return

    def test_awcell_total_dose(self):
        """
        Integration test for beerex.awcell_total_dose
        """
        try:
            self.blackbox_method_int('awcell_total_dose')
        finally:
            pass
        return

    def test_awbrood_total_dose(self):
        """
        Integration test for beerex.awbrood_total_dose
        """
        try:
            self.blackbox_method_int('awbrood_total_dose')
        finally:
            pass
        return

    def test_awcomb_total_dose(self):
        """
        Integration test for beerex.awcomb_total_dose
        """
        try:
            self.blackbox_method_int('awcomb_total_dose')
        finally:
            pass
        return

    def test_awpollen_total_dose(self):
        """
        Integration test for beerex.awpollen_total_dose
        """
        try:
            self.blackbox_method_int('awpollen_total_dose')
        finally:
            pass
        return

    def test_awnectar_total_dose(self):
        """
        Integration test for beerex.awnectar_total_dose
        """
        try:
            self.blackbox_method_int('awnectar_total_dose')
        finally:
            pass
        return

    def test_awwinter_total_dose(self):
        """
        Integration test for beerex.awwinter_total_dose
        """
        try:
            self.blackbox_method_int('awwinter_total_dose')
        finally:
            pass
        return

    def test_ad_total_dose(self):
        """
        Integration test for beerex.ad_total_dose
        """
        try:
            self.blackbox_method_int('ad_total_dose')
        finally:
            pass
        return

    def test_aq_total_dose(self):
        """
        Integration test for beerex.aq_total_dose
        """
        try:
            self.blackbox_method_int('aq_total_dose')
        finally:
            pass
        return

    def test_lw1_acute_rq(self):
        """
        Integration test for beerex.lw1_acute_rq
        """
        try:
            self.blackbox_method_int('lw1_acute_rq')
        finally:
            pass
        return

    def test_lw2_acute_rq(self):
        """
        Integration test for beerex.lw2_acute_rq
        """
        try:
            self.blackbox_method_int('lw2_acute_rq')
        finally:
            pass
        return

    def test_lw3_acute_rq(self):
        """
        Integration test for beerex.lw3_acute_rq
        """
        try:
            self.blackbox_method_int('lw3_acute_rq')
        finally:
            pass
        return

    def test_lw4_acute_rq(self):
        """
        Integration test for beerex.lw4_acute_rq
        """
        try:
            self.blackbox_method_int('lw4_acute_rq')
        finally:
            pass
        return

    def test_lw5_acute_rq(self):
        """
        Integration test for beerex.lw5_acute_rq
        """
        try:
            self.blackbox_method_int('lw5_acute_rq')
        finally:
            pass
        return

    def test_ld6_acute_rq(self):
        """
        Integration test for beerex.ld6_acute_rq
        """
        try:
            self.blackbox_method_int('ld6_acute_rq')
        finally:
            pass
        return

    def test_lq1_acute_rq(self):
        """
        Integration test for beerex.lq1_acute_rq
        """
        try:
            self.blackbox_method_int('lq1_acute_rq')
        finally:
            pass
        return

    def test_lq2_acute_rq(self):
        """
        Integration test for beerex.lq2_acute_rq
        """
        try:
            self.blackbox_method_int('lq2_acute_rq')
        finally:
            pass
        return


    def test_lq3_acute_rq(self):
        """
        Integration test for beerex.lq3_acute_rq
        """
        try:
            self.blackbox_method_int('lq3_acute_rq')
        finally:
            pass
        return

    def test_lq4_acute_rq(self):
        """
        Integration test for beerex.lq4_acute_rq
        """
        try:
            self.blackbox_method_int('lq4_acute_rq')
        finally:
            pass

    def test_awcell_acute_rq(self):
        """
        Integration test for beerex.awcell_acute_rq
        """
        try:
            self.blackbox_method_int('awcell_acute_rq')
        finally:
            pass

    def test_awbrood_acute_rq(self):
        """
        Integration test for beerex.awbrood_acute_rq
        """
        try:
            self.blackbox_method_int('awbrood_acute_rq')
        finally:
            pass

    def test_awcomb_acute_rq(self):
        """
        Integration test for beerex.awcomb_acute_rq
        """
        try:
            self.blackbox_method_int('awcomb_acute_rq')
        finally:
            pass

    def test_awpollen_acute_rq(self):
        """
        Integration test for beerex.awpollen_acute_rq
        """
        try:
            self.blackbox_method_int('awpollen_acute_rq')
        finally:
            pass

    def test_awnectar_acute_rq(self):
        """
        Integration test for beerex.awnectar_acute_rq
        """
        try:
            self.blackbox_method_int('awnectar_acute_rq')
        finally:
            pass

    def test_awwinter_acute_rq(self):
        """
        Integration test for beerex.awwinter_acute_rq
        """
        try:
            self.blackbox_method_int('awwinter_acute_rq')
        finally:
            pass

    def test_ad_acute_rq(self):
        """
        Integration test for beerex.ad_acute_rq
        """
        try:
            self.blackbox_method_int('ad_acute_rq')
        finally:
            pass

    def test_aq_acute_rq(self):
        """
        Integration test for beerex.aq_acute_rq
        """
        try:
            self.blackbox_method_int('aq_acute_rq')
        finally:
            pass
        return

    def test_lw1_chronic_rq(self):
        """
        Integration test for beerex.lw1_chronic_rq
        """
        try:
            self.blackbox_method_int('lw1_chronic_rq')
        finally:
            pass
        return

    def test_lw2_chronic_rq(self):
        """
        Integration test for beerex.lw2_chronic_rq
        """
        try:
            self.blackbox_method_int('lw2_chronic_rq')
        finally:
            pass
        return

    def test_lw3_chronic_rq(self):
        """
        Integration test for beerex.lw3_chronic_rq
        """
        try:
            self.blackbox_method_int('lw3_chronic_rq')
        finally:
            pass
        return

    def test_lw4_chronic_rq(self):
        """
        Integration test for beerex.lw4_chronic_rq
        """
        try:
            self.blackbox_method_int('lw4_chronic_rq')
        finally:
            pass
        return

    def test_lw5_chronic_rq(self):
        """
        Integration test for beerex.lw5_chronic_rq
        """
        try:
            self.blackbox_method_int('lw5_chronic_rq')
        finally:
            pass
        return

    def test_ld6_chronic_rq(self):
        """
        Integration test for beerex.ld6_chronic_rq
        """
        try:
            self.blackbox_method_int('ld6_chronic_rq')
        finally:
            pass
        return

    def test_lq1_chronic_rq(self):
        """
        Integration test for beerex.lq1_chronic_rq
        """
        try:
            self.blackbox_method_int('lq1_chronic_rq')
        finally:
            pass
        return

    def test_lq2_chronic_rq(self):
        """
        Integration test for beerex.lq2_chronic_rq
        """
        try:
            self.blackbox_method_int('lq2_chronic_rq')
        finally:
            pass
        return

    def test_lq3_chronic_rq(self):
        """
        Integration test for beerex.lq3_chronic_rq
        """
        try:
            self.blackbox_method_int('lq3_chronic_rq')
        finally:
            pass
        return

    def test_lq4_chronic_rq(self):
        """
        Integration test for beerex.lq4_chronic_rq
        """
        try:
            self.blackbox_method_int('lq4_chronic_rq')
        finally:
            pass

    def test_awcell_chronic_rq(self):
        """
        Integration test for beerex.awcell_chronic_rq
        """
        try:
            self.blackbox_method_int('awcell_chronic_rq')
        finally:
            pass

    def test_awbrood_chronic_rq(self):
        """
        Integration test for beerex.awbrood_chronic_rq
        """
        try:
            self.blackbox_method_int('awbrood_chronic_rq')
        finally:
            pass

    def test_awcomb_chronic_rq(self):
        """
        Integration test for beerex.awcomb_chronic_rq
        """
        try:
            self.blackbox_method_int('awcomb_chronic_rq')
        finally:
            pass

    def test_awpollen_chronic_rq(self):
        """
        Integration test for beerex.awpollen_chronic_rq
        """
        try:
            self.blackbox_method_int('awpollen_chronic_rq')
        finally:
            pass

    def test_awnectar_chronic_rq(self):
        """
        Integration test for beerex.awnectar_chronic_rq
        """
        try:
            self.blackbox_method_int('awnectar_chronic_rq')
        finally:
            pass

    def test_awwinter_chronic_rq(self):
        """
        Integration test for beerex.awwinter_chronic_rq
        """
        try:
            self.blackbox_method_int('awwinter_chronic_rq')
        finally:
            pass

    def test_ad_chronic_rq(self):
        """
        Integration test for beerex.ad_chronic_rq
        """
        try:
            self.blackbox_method_int('ad_chronic_rq')
        finally:
            pass

    def test_aq_chronic_rq(self):
        """
        Integration test for beerex.aq_chronic_rq
        """
        try:
            self.blackbox_method_int('aq_chronic_rq')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from Beerex model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format','{:.4E}'.format) # display model output in scientific notation
        result = beerex_calc.pd_obj_out["out_" + output]
        expected = beerex_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result, expected, rtol, 0, True)

    def blackbox_method_str(self, output):
        """
        Helper method.
        :param output:
        :return:
        """
        result = beerex_calc.pd_obj_out["out_" + output]
        expected = beerex_calc.pd_obj_exp["exp_" + output]
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