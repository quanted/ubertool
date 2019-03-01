from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import pkgutil
from io import StringIO
import sys
from tabulate import tabulate
import unittest

#find parent directory and import model
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
print("parent_dir")
print(parent_dir)
sys.path.append(parent_dir)
from beerex_exe import Beerex, BeerexOutputs
from ..beerex_exe import Beerex, BeerexOutputs

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
        csv_transpose_path_in = os.path.join(os.path.dirname(__file__), "beerex_qaqc_in_transpose.csv")
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        pd_obj_inputs['csrfmiddlewaretoken'] = 'test'
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
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine='python')
    else:
        #csv_transpose_path_exp = "./beerex_qaqc_exp_transpose.csv"
        csv_transpose_path_exp = os.path.join(os.path.dirname(__file__), "beerex_qaqc_exp_transpose.csv")
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
beerex_output_empty = BeerexOutputs()
beerex_calc = Beerex(pd_obj_inputs, pd_obj_exp)
beerex_calc.execute_model()
inputs_json, outputs_json, exp_out_json = beerex_calc.get_dict_rep()
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

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(beerex_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = beerex_calc.pd_obj_out.columns[i]
                output = getattr(beerex_calc, column_name)
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
            num_variables = len(beerex_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = beerex_calc.pd_obj_out.columns[i]
                output_result = getattr(beerex_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(beerex_output_empty, column_name)
                output_expected2 = getattr(beerex_calc.pd_obj_out, column_name)
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
            self.blackbox_method_int('eec')
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

    def test_aw_cell_total_dose(self):
        """
        Integration test for beerex.aw_cell_total_dose
        """
        try:
            self.blackbox_method_int('aw_cell_total_dose')
        finally:
            pass
        return

    def test_aw_brood_total_dose(self):
        """
        Integration test for beerex.aw_brood_total_dose
        """
        try:
            self.blackbox_method_int('aw_brood_total_dose')
        finally:
            pass
        return

    def test_aw_comb_total_dose(self):
        """
        Integration test for beerex.aw_comb_total_dose
        """
        try:
            self.blackbox_method_int('aw_comb_total_dose')
        finally:
            pass
        return

    def test_aw_pollen_total_dose(self):
        """
        Integration test for beerex.aw_pollen_total_dose
        """
        try:
            self.blackbox_method_int('aw_pollen_total_dose')
        finally:
            pass
        return

    def test_aw_nectar_total_dose(self):
        """
        Integration test for beerex.aw_nectar_total_dose
        """
        try:
            self.blackbox_method_int('aw_nectar_total_dose')
        finally:
            pass
        return

    def test_aw_winter_total_dose(self):
        """
        Integration test for beerex.aw_winter_total_dose
        """
        try:
            self.blackbox_method_int('aw_winter_total_dose')
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

    def test_aw_cell_acute_rq(self):
        """
        Integration test for beerex.aw_cell_acute_rq
        """
        try:
            self.blackbox_method_int('aw_cell_acute_rq')
        finally:
            pass

    def test_aw_brood_acute_rq(self):
        """
        Integration test for beerex.aw_brood_acute_rq
        """
        try:
            self.blackbox_method_int('aw_brood_acute_rq')
        finally:
            pass

    def test_aw_comb_acute_rq(self):
        """
        Integration test for beerex.aw_comb_acute_rq
        """
        try:
            self.blackbox_method_int('aw_comb_acute_rq')
        finally:
            pass

    def test_aw_pollen_acute_rq(self):
        """
        Integration test for beerex.aw_pollen_acute_rq
        """
        try:
            self.blackbox_method_int('aw_pollen_acute_rq')
        finally:
            pass

    def test_aw_nectar_acute_rq(self):
        """
        Integration test for beerex.aw_nectar_acute_rq
        """
        try:
            self.blackbox_method_int('aw_nectar_acute_rq')
        finally:
            pass

    def test_aw_winter_acute_rq(self):
        """
        Integration test for beerex.aw_winter_acute_rq
        """
        try:
            self.blackbox_method_int('aw_winter_acute_rq')
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

    def test_aw_cell_chronic_rq(self):
        """
        Integration test for beerex.aw_cell_chronic_rq
        """
        try:
            self.blackbox_method_int('aw_cell_chronic_rq')
        finally:
            pass

    def test_aw_brood_chronic_rq(self):
        """
        Integration test for beerex.aw_brood_chronic_rq
        """
        try:
            self.blackbox_method_int('aw_brood_chronic_rq')
        finally:
            pass

    def test_aw_comb_chronic_rq(self):
        """
        Integration test for beerex.aw_comb_chronic_rq
        """
        try:
            self.blackbox_method_int('aw_comb_chronic_rq')
        finally:
            pass

    def test_aw_pollen_chronic_rq(self):
        """
        Integration test for beerex.aw_pollen_chronic_rq
        """
        try:
            self.blackbox_method_int('aw_pollen_chronic_rq')
        finally:
            pass

    def test_aw_nectar_chronic_rq(self):
        """
        Integration test for beerex.aw_nectar_chronic_rq
        """
        try:
            self.blackbox_method_int('aw_nectar_chronic_rq')
        finally:
            pass

    def test_aw_winter_chronic_rq(self):
        """
        Integration test for beerex.aw_winter_chronic_rq
        """
        try:
            self.blackbox_method_int('aw_winter_chronic_rq')
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
        tab = pd.concat([result, expected], axis=1)
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