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
from therps_exe import THerps, THerpsOutputs

print("sys.path")
print(sys.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'therps_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./therps_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./therps_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print("therps inputs")
    #print(pd_obj_inputs.shape)
    #print('therps expected output keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='plain'))

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'therps_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        csv_transpose_path_exp = "./therps_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print("therps expected outputs")
    #print('therps expected output dimensions ' + str(pd_obj_exp.shape))
    #print('therps expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    #print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='plain'))

# create an instance of therps object with qaqc data
therps_output_empty = THerpsOutputs()
therps_calc = THerps(pd_obj_inputs, pd_obj_exp)
therps_calc.execute_model()
inputs_json, outputs_json, exp_out_json = therps_calc.get_dict_rep()

#inputs_json, outputs_json, exp_out_json = therps_calc.get_dict_rep(therps_calc)
    #print("therps output")
    #print(inputs_json)
    #print("####")
    #######print(therps_calc)
test = {}
######therps_calc.execute_model()

class TestTherps(unittest.TestCase):
    """
    Integration tests for therps.
    """
    def setUp(self):
        """
        Setup routine for therps.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for therps.
        :return:
        """
        pass

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(therps_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = therps_calc.pd_obj_out.columns[i]
                output = getattr(therps_calc, column_name)
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
            num_variables = len(therps_calc.pd_obj_out.columns)
            #get the string of the type that is expected and the type that has resulted
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = therps_calc.pd_obj_out.columns[i]
                output_result = getattr(therps_calc, column_name)
                column_dtype_result = output_result.dtype.name
                output_expected = getattr(therps_output_empty, column_name)
                output_expected2 = getattr(therps_calc.pd_obj_out, column_name)
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

    def test_ld50_ad_sm(self):
        """
        Integration test for therps.ld50_ad_sm
        """
        try:
            self.blackbox_method_int('ld50_ad_sm')
        finally:
            pass
        return

    def test_ld50_ad_md(self):
        """
        Integration test for therps.ld50_ad_md
        """
        try:
            self.blackbox_method_int('ld50_ad_md')
        finally:
            pass
        return

    def test_ld50_ad_lg(self):
        """
        Integration test for therps.ld50_ad_lg
        """
        try:
            self.blackbox_method_int('ld50_ad_lg')
        finally:
            pass
        return

    def test_eec_dose_bp_sm(self):
        """
        Integration test for therps.eec_dose_bp_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bp_sm')
        finally:
            pass
        return

    def test_eec_dose_bp_md(self):
        """
        Integration test for therps.eec_dose_bp_md
        """
        try:
            self.blackbox_method_int('eec_dose_bp_md')
        finally:
            pass
        return

    def test_eec_dose_bp_lg(self):
        """
        Integration test for therps.eec_dose_bp_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bp_lg')
        finally:
            pass
        return

    def test_arq_dose_bp_sm(self):
        """
        Integration test for therps.arq_dose_bp_sm
        """
        try:
            self.blackbox_method_int('arq_dose_bp_sm')
        finally:
            pass
        return

    def test_arq_dose_bp_md(self):
        """
        Integration test for therps.arq_dose_bp_md
        """
        try:
            self.blackbox_method_int('arq_dose_bp_md')
        finally:
            pass
        return

    def test_arq_dose_bp_lg(self):
        """
        Integration test for therps.arq_dose_bp_lg
        """
        try:
            self.blackbox_method_int('arq_dose_bp_lg')
        finally:
            pass
        return

    def test_eec_dose_fr_sm(self):
        """
        Integration test for therps.eec_dose_fr_sm
        """
        try:
            self.blackbox_method_int('eec_dose_fr_sm')
        finally:
            pass
        return

    def test_eec_dose_fr_md(self):
        """
        Integration test for therps.eec_dose_fr_md
        """
        try:
            self.blackbox_method_int('eec_dose_fr_md')
        finally:
            pass
        return

    def test_eec_dose_fr_lg(self):
        """
        Integration test for therps.eec_dose_fr_lg
        """
        try:
            self.blackbox_method_int('eec_dose_fr_lg')
        finally:
            pass
        return

    def test_arq_dose_fr_sm(self):
        """
        Integration test for therps.arq_dose_fr_sm
        """
        try:
            self.blackbox_method_int('arq_dose_fr_sm')
        finally:
            pass
        return

    def test_arq_dose_fr_md(self):
        """
        Integration test for therps.arq_dose_fr_md
        """
        try:
            self.blackbox_method_int('arq_dose_fr_md')
        finally:
            pass
        return

    def test_arq_dose_fr_lg(self):
        """
        Integration test for therps.arq_dose_fr_lg
        """
        try:
            self.blackbox_method_int('arq_dose_fr_lg')
        finally:
            pass
        return

    def test_eec_dose_hm_md(self):
        """
        Integration test for therps.eec_dose_hm_md
        """
        try:
            self.blackbox_method_int('eec_dose_hm_md')
        finally:
            pass
        return

    def test_eec_dose_hm_lg(self):
        """
        Integration test for therps.eec_dose_hm_lg
        """
        try:
            self.blackbox_method_int('eec_dose_hm_lg')
        finally:
            pass
        return

    def test_arq_dose_hm_md(self):
        """
        Integration test for therps.arq_dose_hm_md
        """
        try:
            self.blackbox_method_int('arq_dose_hm_md')
        finally:
            pass
        return

    def test_arq_dose_hm_lg(self):
        """
        Integration test for therps.arq_dose_hm_lg
        """
        try:
            self.blackbox_method_int('arq_dose_hm_lg')
        finally:
            pass
        return

    def test_eec_dose_im_md(self):
        """
        Integration test for therps.eec_dose_im_md
        """
        try:
            self.blackbox_method_int('eec_dose_im_md')
        finally:
            pass
        return

    def test_eec_dose_im_lg(self):
        """
        Integration test for therps.eec_dose_im_lg
        """
        try:
            self.blackbox_method_int('eec_dose_im_lg')
        finally:
            pass
        return

    def test_arq_dose_im_md(self):
        """
        Integration test for therps.arq_dose_im_md
        """
        try:
            self.blackbox_method_int('arq_dose_im_md')
        finally:
            pass
        return

    def test_arq_dose_im_lg(self):
        """
        Integration test for therps.arq_dose_im_lg
        """
        try:
            self.blackbox_method_int('arq_dose_im_lg')
        finally:
            pass
        return

    def test_eec_dose_tp_md(self):
        """
        Integration test for therps.eec_dose_tp_md
        """
        try:
            self.blackbox_method_int('eec_dose_tp_md')
        finally:
            pass
        return

    def test_eec_dose_tp_lg(self):
        """
        Integration test for therps.eec_dose_tp_lg
        """
        try:
            self.blackbox_method_int('eec_dose_tp_lg')
        finally:
            pass
        return

    def test_arq_dose_tp_md(self):
        """
        Integration test for therps.arq_dose_tp_md
        """
        try:
            self.blackbox_method_int('arq_dose_tp_md')
        finally:
            pass
        return

    def test_arq_dose_tp_lg(self):
        """
        Integration test for therps.arq_dose_tp_lg
        """
        try:
            self.blackbox_method_int('arq_dose_tp_lg')
        finally:
            pass
        return

    def test_eec_diet_herp_bl(self):
        """
        Integration test for therps.eec_diet_herp_bl
        """
        try:
            self.blackbox_method_int('eec_diet_herp_bl')
        finally:
            pass
        return

    def test_eec_arq_herp_bl(self):
        """
        Integration test for therps.eec_arq_herp_bl
        """
        try:
            self.blackbox_method_int('eec_arq_herp_bl')
        finally:
            pass
        return

    def test_eec_diet_herp_fr(self):
        """
        Integration test for therps.eec_diet_herp_fr
        """
        try:
            self.blackbox_method_int('eec_diet_herp_fr')
        finally:
            pass
        return

    def test_eec_arq_herp_fr(self):
        """
        Integration test for therps.eec_arq_herp_fr
        """
        try:
            self.blackbox_method_int('eec_arq_herp_fr')
        finally:
            pass
        return


    def test_eec_diet_herp_hm(self):
        """
        Integration test for therps.eec_diet_herp_hm
        """
        try:
            self.blackbox_method_int('eec_diet_herp_hm')
        finally:
            pass
        return

    def test_eec_arq_herp_hm(self):
        """
        Integration test for therps.eec_arq_herp_hm
        """
        try:
            self.blackbox_method_int('eec_arq_herp_hm')
        finally:
            pass

    def test_eec_diet_herp_im(self):
        """
        Integration test for therps.eec_diet_herp_im
        """
        try:
            self.blackbox_method_int('eec_diet_herp_im')
        finally:
            pass

    def test_eec_arq_herp_im(self):
        """
        Integration test for therps.eec_arq_herp_im
        """
        try:
            self.blackbox_method_int('eec_arq_herp_im')
        finally:
            pass

    def test_eec_diet_herp_tp(self):
        """
        Integration test for therps.eec_diet_herp_tp
        """
        try:
            self.blackbox_method_int('eec_diet_herp_tp')
        finally:
            pass

    def test_eec_arq_herp_tp(self):
        """
        Integration test for therps.eec_arq_herp_tp
        """
        try:
            self.blackbox_method_int('eec_arq_herp_tp')
        finally:
            pass

    def test_eec_crq_herp_bl(self):
        """
        Integration test for therps.eec_crq_herp_bl
        """
        try:
            self.blackbox_method_int('eec_crq_herp_bl')
        finally:
            pass

    def test_eec_crq_herp_fr(self):
        """
        Integration test for therps.eec_crq_herp_fr
        """
        try:
            self.blackbox_method_int('eec_crq_herp_fr')
        finally:
            pass

    def test_eec_crq_herp_hm(self):
        """
        Integration test for therps.eec_crq_herp_hm
        """
        try:
            self.blackbox_method_int('eec_crq_herp_hm')
        finally:
            pass

    def test_eec_crq_herp_im(self):
        """
        Integration test for therps.eec_crq_herp_im
        """
        try:
            self.blackbox_method_int('eec_crq_herp_im')
        finally:
            pass
        return

    def test_eec_crq_herp_tp(self):
        """
        Integration test for therps.eec_crq_herp_tp
        """
        try:
            self.blackbox_method_int('eec_crq_herp_tp')
        finally:
            pass
        return

    def test_eec_dose_bp_sm_mean(self):
        """
        Integration test for therps.eec_dose_bp_sm_mean
        """
        try:
            self.blackbox_method_int('eec_dose_bp_sm_mean')
        finally:
            pass
        return

    def test_eec_dose_bp_md_mean(self):
        """
        Integration test for therps.eec_dose_bp_md_mean
        """
        try:
            self.blackbox_method_int('eec_dose_bp_md_mean')
        finally:
            pass
        return

    def test_eec_dose_bp_lg_mean(self):
        """
        Integration test for therps.eec_dose_bp_lg_mean
        """
        try:
            self.blackbox_method_int('eec_dose_bp_lg_mean')
        finally:
            pass
        return

    def test_arq_dose_bp_sm_mean(self):
        """
        Integration test for therps.arq_dose_bp_sm_mean
        """
        try:
            self.blackbox_method_int('arq_dose_bp_sm_mean')
        finally:
            pass
        return

    def test_arq_dose_bp_md_mean(self):
        """
        Integration test for therps.arq_dose_bp_md_mean
        """
        try:
            self.blackbox_method_int('arq_dose_bp_md_mean')
        finally:
            pass
        return

    def test_arq_dose_bp_lg_mean(self):
        """
        Integration test for therps.arq_dose_bp_lg_mean
        """
        try:
            self.blackbox_method_int('arq_dose_bp_lg_mean')
        finally:
            pass
        return

    def test_eec_dose_fr_sm_mean(self):
        """
        Integration test for therps.eec_dose_fr_sm_mean
        """
        try:
            self.blackbox_method_int('eec_dose_fr_sm_mean')
        finally:
            pass
        return

    def test_eec_dose_fr_md_mean(self):
        """
        Integration test for therps.eec_dose_fr_md_mean
        """
        try:
            self.blackbox_method_int('eec_dose_fr_md_mean')
        finally:
            pass
        return

    def test_eec_dose_fr_lg_mean(self):
        """
        Integration test for therps.eec_dose_fr_lg_mean
        """
        try:
            self.blackbox_method_int('eec_dose_fr_lg_mean')
        finally:
            pass
        return

    def test_arq_dose_fr_sm_mean(self):
        """
        Integration test for therps.arq_dose_fr_sm_mean
        """
        try:
            self.blackbox_method_int('arq_dose_fr_sm_mean')
        finally:
            pass
        return

    def test_arq_dose_fr_md_mean(self):
        """
        Integration test for therps.arq_dose_fr_md_mean
        """
        try:
            self.blackbox_method_int('arq_dose_fr_md_mean')
        finally:
            pass
        return

    def test_arq_dose_fr_lg_mean(self):
        """
        Integration test for therps.arq_dose_fr_lg_mean
        """
        try:
            self.blackbox_method_int('arq_dose_fr_lg_mean')
        finally:
            pass
        return

    def test_eec_dose_hm_md_mean(self):
        """
        Integration test for therps.eec_dose_hm_md_mean
        """
        try:
            self.blackbox_method_int('eec_dose_hm_md_mean')
        finally:
            pass
        return

    def test_eec_dose_hm_lg_mean(self):
        """
        Integration test for therps.eec_dose_hm_lg_mean
        """
        try:
            self.blackbox_method_int('eec_dose_hm_lg_mean')
        finally:
            pass
        return

    def test_arq_dose_hm_md_mean(self):
        """
        Integration test for therps.arq_dose_hm_md_mean
        """
        try:
            self.blackbox_method_int('arq_dose_hm_md_mean')
        finally:
            pass
        return

    def test_arq_dose_hm_lg_mean(self):
        """
        Integration test for therps.arq_dose_hm_lg_mean
        """
        try:
            self.blackbox_method_int('arq_dose_hm_lg_mean')
        finally:
            pass
        return

    def test_eec_dose_im_md_mean(self):
        """
        Integration test for therps.eec_dose_im_md_mean
        """
        try:
            self.blackbox_method_int('eec_dose_im_md_mean')
        finally:
            pass
        return

    def test_eec_dose_im_lg_mean(self):
        """
        Integration test for therps.eec_dose_im_lg_mean
        """
        try:
            self.blackbox_method_int('eec_dose_im_lg_mean')
        finally:
            pass
        return

    def test_arq_dose_im_md_mean(self):
        """
        Integration test for therps.arq_dose_im_md_mean
        """
        try:
            self.blackbox_method_int('arq_dose_im_md_mean')
        finally:
            pass
        return

    def test_arq_dose_im_lg_mean(self):
        """
        Integration test for therps.arq_dose_im_lg_mean
        """
        try:
            self.blackbox_method_int('arq_dose_im_lg_mean')
        finally:
            pass
        return

    def test_eec_dose_tp_md_mean(self):
        """
        Integration test for therps.eec_dose_tp_md_mean
        """
        try:
            self.blackbox_method_int('eec_dose_tp_md_mean')
        finally:
            pass
        return

    def test_eec_dose_tp_lg_mean(self):
        """
        Integration test for therps.eec_dose_tp_lg_mean
        """
        try:
            self.blackbox_method_int('eec_dose_tp_lg_mean')
        finally:
            pass
        return

    def test_arq_dose_tp_md_mean(self):
        """
        Integration test for therps.arq_dose_tp_md_mean
        """
        try:
            self.blackbox_method_int('arq_dose_tp_md_mean')
        finally:
            pass
        return

    def test_arq_dose_tp_lg_mean(self):
        """
        Integration test for therps.arq_dose_tp_lg_mean
        """
        try:
            self.blackbox_method_int('arq_dose_tp_lg_mean')
        finally:
            pass
        return

    def test_eec_diet_herp_bl_mean(self):
        """
        Integration test for therps.eec_diet_herp_bl_mean
        """
        try:
            self.blackbox_method_int('eec_diet_herp_bl_mean')
        finally:
            pass
        return

    def test_eec_arq_herp_bl_mean(self):
        """
        Integration test for therps.eec_arq_herp_bl_mean
        """
        try:
            self.blackbox_method_int('eec_arq_herp_bl_mean')
        finally:
            pass
        return

    def test_eec_diet_herp_fr_mean(self):
        """
        Integration test for therps.eec_diet_herp_fr_mean
        """
        try:
            self.blackbox_method_int('eec_diet_herp_fr_mean')
        finally:
            pass
        return

    def test_eec_arq_herp_fr_mean(self):
        """
        Integration test for therps.eec_arq_herp_fr_mean
        """
        try:
            self.blackbox_method_int('eec_arq_herp_fr_mean')
        finally:
            pass
        return

    def test_eec_diet_herp_hm_mean(self):
        """
        Integration test for therps.eec_diet_herp_hm_mean
        """
        try:
            self.blackbox_method_int('eec_diet_herp_hm_mean')
        finally:
            pass
        return

    def test_eec_arq_herp_hm_mean(self):
        """
        Integration test for therps.eec_arq_herp_hm_mean
        """
        try:
            self.blackbox_method_int('eec_arq_herp_hm_mean')
        finally:
            pass
        return

    def test_eec_diet_herp_im_mean(self):
        """
        Integration test for therps.eec_diet_herp_im_mean
        """
        try:
            self.blackbox_method_int('eec_diet_herp_im_mean')
        finally:
            pass
        return

    def test_eec_arq_herp_im_mean(self):
        """
        Integration test for therps.eec_arq_herp_im_mean
        """
        try:
            self.blackbox_method_int('eec_arq_herp_im_mean')
        finally:
            pass
        return

    def test_eec_diet_herp_tp_mean(self):
        """
        Integration test for therps.eec_diet_herp_tp_mean
        """
        try:
            self.blackbox_method_int('eec_diet_herp_tp_mean')
        finally:
            pass
        return

    def test_eec_arq_herp_tp_mean(self):
        """
        Integration test for therps.eec_arq_herp_tp_mean
        """
        try:
            self.blackbox_method_int('eec_arq_herp_tp_mean')
        finally:
            pass
        return

    def test_eec_crq_herp_bl_mean(self):
        """
        Integration test for therps.eec_crq_herp_bl_mean
        """
        try:
            self.blackbox_method_int('eec_crq_herp_bl_mean')
        finally:
            pass
        return

    def test_eec_crq_herp_fr_mean(self):
        """
        Integration test for therps.eec_crq_herp_fr_mean
        """
        try:
            self.blackbox_method_int('eec_crq_herp_fr_mean')
        finally:
            pass
        return

    def test_eec_crq_herp_hm_mean(self):
        """
        Integration test for therps.eec_crq_herp_hm_mean
        """
        try:
            self.blackbox_method_int('eec_crq_herp_hm_mean')
        finally:
            pass
        return

    def test_eec_crq_herp_im_mean(self):
        """
        Integration test for therps.eec_crq_herp_im_mean
        """
        try:
            self.blackbox_method_int('eec_crq_herp_im_mean')
        finally:
            pass
        return

    def test_eec_crq_herp_tp_mean(self):
        """
        Integration test for therps.eec_crq_herp_tp_mean
        """
        try:
            self.blackbox_method_int('eec_crq_herp_tp_mean')
        finally:
            pass
        return

    def blackbox_method_int(self, output):
        """
        Helper method to reuse code for testing numpy array outputs from TerrPlant model
        :param output: String; Pandas Series name (e.g. column name) without '_out'
        :return:
        """
        pd.set_option('display.float_format', lambda x: '%.10e' % x)
        result = therps_calc.pd_obj_out["out_" + output]
        expected = therps_calc.pd_obj_exp["exp_" + output]
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
        result = therps_calc.pd_obj_out["out_" + output]
        expected = therps_calc.pd_obj_exp["exp_" + output]
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