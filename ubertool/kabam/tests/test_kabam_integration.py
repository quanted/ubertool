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
sys.path.append(parent_dir)

from kabam_exe import Kabam, KabamOutputs

print("sys.path")
print(sys.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'kabam_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./kabam_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./kabam_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print("kabam inputs")
    #print(pd_obj_inputs.shape)
    #print('kabam expected output keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='plain'))

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'kabam_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        csv_transpose_path_exp = "./kabam_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print("kabam expected outputs")
    #print('kabam expected output dimensions ' + str(pd_obj_exp.shape))
    #print('kabam expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    #print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='plain'))

# create an instance of kabam object with qaqc data
kabam_calc = Kabam(pd_obj_inputs, pd_obj_exp)
kabam_calc.execute_model()
kabam_output_empty = KabamOutputs()
inputs_json, outputs_json, exp_out_json = kabam_calc.get_dict_rep()
    #print("kabam output")
    #print(inputs_json)
    #print("####")
    #######print(kabam_calc)
test = {}
######kabam_calc.execute_model()

class TestKabam(unittest.TestCase):
    """
    Integration tests for kabam.
    """
    def setUp(self):
        """
        Setup routine for kabam.
        :return:
        """
        pass

    def tearDown(self):
        """
        Teardown routine for kabam.
        :return:
        """
        pass

    def test_assert_output_series(self):
        """ Verify that each output variable is a pd.Series """

        try:
            num_variables = len(kabam_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                column_name = kabam_calc.pd_obj_out.columns[i]
                output = getattr(kabam_calc, column_name)
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
        """ Verify that each output variable is the correct dtype,
            essentially checking that initial declaration of dtype has not
            changed due to computation-based coercion of dtype"""

        try:
            num_variables = len(kabam_calc.pd_obj_out.columns)
            result = pd.Series(False, index=list(range(num_variables)), dtype='bool')
            expected = pd.Series(True, index=list(range(num_variables)), dtype='bool')

            for i in range(num_variables):
                #get the string of the dtype that is expected and the type that has resulted
                output_name = kabam_calc.pd_obj_out.columns[i]
                output_result = getattr(kabam_calc, output_name)
                output_dtype_result = output_result.dtype.name
                #kabam_output_empty is a copy of the original ModelOutputs declarations (unchanged by computations
                output_expected_attr = getattr(kabam_output_empty, output_name)
                output_dtype_expected = output_expected_attr.dtype.name
                if output_dtype_result == output_dtype_expected:
                    result[i] = True

                #tab = pd.concat([result,expected], axis=1)
                if(result[i] != expected[i]):
                    print(str(i) + ":" + output_name)
                    print("output assertaion state (result/expected) : " + str(result[i]) + "/" + str(expected[i]))
                    print("output dtype (result/expected) :            " + output_dtype_result + "/" + output_dtype_expected)
            npt.assert_array_equal(result, expected)
        finally:
            pass
        return

    def test_cb_phytoplankton(self):
        """
        Integration test for kabam.cb_phytoplankton
        """
        try:
            self.blackbox_method_int('cb_phytoplankton')
        finally:
            pass
        return

    def test_cb_zoo(self):
        """
        Integration test for kabam.cb_zoo
        """
        try:
            self.blackbox_method_int('cb_zoo')
        finally:
            pass
        return

    def test_cb_beninv(self):
        """
        Integration test for kabam.cb_beninv
        """
        try:
            self.blackbox_method_int('cb_beninv')
        finally:
            pass
        return

    def test_cb_filterfeeders(self):
        """
        Integration test for kabam.cb_filterfeeders
        """
        try:
            self.blackbox_method_int('cb_filterfeeders')
        finally:
            pass
        return

    def test_cb_sfish(self):
        """
        Integration test for kabam.cb_sfish
        """
        try:
            self.blackbox_method_int('cb_sfish')
        finally:
            pass
        return

    def test_cb_mfish(self):
        """
        Integration test for kabam.cb_mfish
        """
        try:
            self.blackbox_method_int('cb_mfish')
        finally:
            pass
        return

    def test_cb_lfish(self):
        """
        Integration test for kabam.cb_lfish
        """
        try:
            self.blackbox_method_int('cb_lfish')
        finally:
            pass
        return

    def test_cbl_phytoplankton(self):
        """
        Integration test for kabam.cbl_phytoplankton
        """
        try:
            self.blackbox_method_int('cbl_phytoplankton')
        finally:
            pass
        return

    def test_cbl_zoo(self):
        """
        Integration test for kabam.cbl_zoo
        """
        try:
            self.blackbox_method_int('cbl_zoo')
        finally:
            pass
        return

    def test_cbl_beninv(self):
        """
        Integration test for kabam.cbl_beninv
        """
        try:
            self.blackbox_method_int('cbl_beninv')
        finally:
            pass
        return


    def test_cbl_filterfeeders(self):
        """
        Integration test for kabam.cbl_filterfeeders
        """
        try:
            self.blackbox_method_int('cbl_filterfeeders')
        finally:
            pass
        return

    def test_cbl_sfish(self):
        """
        Integration test for kabam.cbl_sfish
        """
        try:
            self.blackbox_method_int('cbl_sfish')
        finally:
            pass
        return

    def test_cbl_mfish(self):
        """
        Integration test for kabam.cbl_mfish
        """
        try:
            self.blackbox_method_int('cbl_mfish')
        finally:
            pass
        return

    def test_cbl_lfish(self):
        """
        Integration test for kabam.cbl_lfish
        """
        try:
            self.blackbox_method_int('cbl_lfish')
        finally:
            pass
        return

    def test_cbd_zoo(self):
        """
        Integration test for kabam.cbd_zoo
        """
        try:
            self.blackbox_method_int('cbd_zoo')
        finally:
            pass
        return

    def test_cbd_beninv(self):
        """
        Integration test for kabam.cbd_beninv
        """
        try:
            self.blackbox_method_int('cbd_beninv')
        finally:
            pass
        return

    def test_cbd_filterfeeders(self):
        """
        Integration test for kabam.cbd_filterfeeders
        """
        try:
            self.blackbox_method_int('cbd_filterfeeders')
        finally:
            pass
        return

    def test_cbd_sfish(self):
        """
        Integration test for kabam.cbd_sfish
        """
        try:
            self.blackbox_method_int('cbd_sfish')
        finally:
            pass
        return

    def test_cbd_mfish(self):
        """
        Integration test for kabam.cbd_mfish
        """
        try:
            self.blackbox_method_int('cbd_mfish')
        finally:
            pass
        return

    def test_cbd_lfish(self):
        """
        Integration test for kabam.cbd_lfish
        """
        try:
            self.blackbox_method_int('cbd_lfish')
        finally:
            pass
        return

    def test_cbr_phytoplankton(self):
        """
        Integration test for kabam.cbr_phytoplankton
        """
        try:
            self.blackbox_method_int('cbr_phytoplankton')
        finally:
            pass
        return

    def test_cbr_zoo(self):
        """
        Integration test for kabam.cbr_zoo
        """
        try:
            self.blackbox_method_int('cbr_zoo')
        finally:
            pass
        return

    def test_cbr_beninv(self):
        """
        Integration test for kabam.cbr_beninv
        """
        try:
            self.blackbox_method_int('cbr_beninv')
        finally:
            pass
        return

    def test_cbr_filterfeeders(self):
        """
        Integration test for kabam.cbr_filterfeeders
        """
        try:
            self.blackbox_method_int('cbr_filterfeeders')
        finally:
            pass
        return

    def test_cbr_sfish(self):
        """
        Integration test for kabam.cbr_sfish
        """
        try:
            self.blackbox_method_int('cbr_sfish')
        finally:
            pass
        return

    def test_cbr_mfish(self):
        """
        Integration test for kabam.cbr_mfish
        """
        try:
            self.blackbox_method_int('cbr_mfish')
        finally:
            pass
        return

    def test_cbr_lfish(self):
        """
        Integration test for kabam.cbr_lfish
        """
        try:
            self.blackbox_method_int('cbr_lfish')
        finally:
            pass
        return

    def test_cbf_phytoplankton(self):
        """
        Integration test for kabam.cbf_phytoplankton
        """
        try:
            self.blackbox_method_int('cbf_phytoplankton')
        finally:
            pass
        return

    def test_cbf_zoo(self):
        """
        Integration test for kabam.cbf_zoo
        """
        try:
            self.blackbox_method_int('cbf_zoo')
        finally:
            pass
        return

    def test_cbf_beninv(self):
        """
        Integration test for kabam.cbf_beninv
        """
        try:
            self.blackbox_method_int('cbf_beninv')
        finally:
            pass
        return

    def test_cbf_filterfeeders(self):
        """
        Integration test for kabam.cbf_filterfeeders
        """
        try:
            self.blackbox_method_int('cbf_filterfeeders')
        finally:
            pass
        return

    def test_cbf_sfish(self):
        """
        Integration test for kabam.cbf_sfish
        """
        try:
            self.blackbox_method_int('cbf_sfish')
        finally:
            pass
        return

    def test_cbf_mfish(self):
        """
        Integration test for kabam.cbf_mfish
        """
        try:
            self.blackbox_method_int('cbf_mfish')
        finally:
            pass
        return

    def test_cbf_lfish(self):
        """
        Integration test for kabam.cbf_lfish
        """
        try:
            self.blackbox_method_int('cbf_lfish')
        finally:
            pass
        return

    def test_cbaf_phytoplankton(self):
        """
        Integration test for kabam.cbaf_phytoplankton
        """
        try:
            self.blackbox_method_int('cbaf_phytoplankton')
        finally:
            pass
        return

    def test_cbaf_zoo(self):
        """
        Integration test for kabam.cbaf_zoo
        """
        try:
            self.blackbox_method_int('cbaf_zoo')
        finally:
            pass
        return

    def test_cbaf_beninv(self):
        """
        Integration test for kabam.cbaf_beninv
        """
        try:
            self.blackbox_method_int('cbaf_beninv')
        finally:
            pass
        return

    def test_cbaf_filterfeeders(self):
        """
        Integration test for kabam.cbaf_filterfeeders
        """
        try:
            self.blackbox_method_int('cbaf_filterfeeders')
        finally:
            pass
        return

    def test_cbaf_sfish(self):
        """
        Integration test for kabam.cbaf_sfish
        """
        try:
            self.blackbox_method_int('cbaf_sfish')
        finally:
            pass
        return

    def test_cbaf_mfish(self):
        """
        Integration test for kabam.cbaf_mfish
        """
        try:
            self.blackbox_method_int('cbaf_mfish')
        finally:
            pass
        return

    def test_cbaf_lfish(self):
        """
        Integration test for kabam.cbaf_lfish
        """
        try:
            self.blackbox_method_int('cbaf_lfish')
        finally:
            pass
        return

    def test_cbfl_phytoplankton(self):
        """
        Integration test for kabam.cbfl_phytoplankton
        """
        try:
            self.blackbox_method_int('cbfl_phytoplankton')
        finally:
            pass
        return

    def test_cbfl_zoo(self):
        """
        Integration test for kabam.cbfl_zoo
        """
        try:
            self.blackbox_method_int('cbfl_zoo')
        finally:
            pass
        return

    def test_cbfl_beninv(self):
        """
        Integration test for kabam.cbfl_beninv
        """
        try:
            self.blackbox_method_int('cbfl_beninv')
        finally:
            pass
        return

    def test_cbfl_filterfeeders(self):
        """
        Integration test for kabam.cbfl_filterfeeders
        """
        try:
            self.blackbox_method_int('cbfl_filterfeeders')
        finally:
            pass
        return

    def test_cbfl_sfish(self):
        """
        Integration test for kabam.cbfl_sfish
        """
        try:
            self.blackbox_method_int('cbfl_sfish')
        finally:
            pass
        return

    def test_cbfl_mfish(self):
        """
        Integration test for kabam.cbfl_mfish
        """
        try:
            self.blackbox_method_int('cbfl_mfish')
        finally:
            pass
        return

    def test_cbfl_lfish(self):
        """
        Integration test for kabam.cbfl_lfish
        """
        try:
            self.blackbox_method_int('cbfl_lfish')
        finally:
            pass
        return

    def test_cbafl_phytoplankton(self):
        """
        Integration test for kabam.cbafl_phytoplankton
        """
        try:
            self.blackbox_method_int('cbafl_phytoplankton')
        finally:
            pass
        return

    def test_cbafl_zoo(self):
        """
        Integration test for kabam.cbafl_zoo
        """
        try:
            self.blackbox_method_int('cbafl_zoo')
        finally:
            pass
        return

    def test_cbafl_beninv(self):
        """
        Integration test for kabam.cbafl_beninv
        """
        try:
            self.blackbox_method_int('cbafl_beninv')
        finally:
            pass
        return

    def test_cbafl_filterfeeders(self):
        """
        Integration test for kabam.cbafl_filterfeeders
        """
        try:
            self.blackbox_method_int('cbafl_filterfeeders')
        finally:
            pass
        return

    def test_cbafl_sfish(self):
        """
        Integration test for kabam.cbafl_sfish
        """
        try:
            self.blackbox_method_int('cbafl_sfish')
        finally:
            pass
        return

    def test_cbafl_mfish(self):
        """
        Integration test for kabam.cbafl_mfish
        """
        try:
            self.blackbox_method_int('cbafl_mfish')
        finally:
            pass
        return

    def test_cbafl_lfish(self):
        """
        Integration test for kabam.cbafl_lfish
        """
        try:
            self.blackbox_method_int('cbafl_lfish')
        finally:
            pass
        return

    def test_bmf_zoo(self):
        """
        Integration test for kabam.bmf_zoo
        """
        try:
            self.blackbox_method_int('bmf_zoo')
        finally:
            pass
        return

    def test_bmf_beninv(self):
        """
        Integration test for kabam.bmf_beninv
        """
        try:
            self.blackbox_method_int('bmf_beninv')
        finally:
            pass
        return

    def test_bmf_filterfeeders(self):
        """
        Integration test for kabam.bmf_filterfeeders
        """
        try:
            self.blackbox_method_int('bmf_filterfeeders')
        finally:
            pass
        return

    def test_bmf_sfish(self):
        """
        Integration test for kabam.bmf_sfish
        """
        try:
            self.blackbox_method_int('bmf_sfish')
        finally:
            pass
        return

    def test_bmf_mfish(self):
        """
        Integration test for kabam.bmf_mfish
        """
        try:
            self.blackbox_method_int('bmf_mfish')
        finally:
            pass
        return

    def test_bmf_lfish(self):
        """
        Integration test for kabam.bmf_lfish
        """
        try:
            self.blackbox_method_int('bmf_lfish')
        finally:
            pass
        return

    def test_cbsafl_phytoplankton(self):
        """
        Integration test for kabam.cbsafl_phytoplankton
        """
        try:
            self.blackbox_method_int('cbsafl_phytoplankton')
        finally:
            pass
        return

    def test_cbsafl_zoo(self):
        """
        Integration test for kabam.cbsafl_zoo
        """
        try:
            self.blackbox_method_int('cbsafl_zoo')
        finally:
            pass
        return

    def test_cbsafl_beninv(self):
        """
        Integration test for kabam.cbsafl_beninv
        """
        try:
            self.blackbox_method_int('cbsafl_beninv')
        finally:
            pass
        return

    def test_cbsafl_filterfeeders(self):
        """
        Integration test for kabam.cbsafl_filterfeeders
        """
        try:
            self.blackbox_method_int('cbsafl_filterfeeders')
        finally:
            pass
        return

    def test_cbsafl_sfish(self):
        """
        Integration test for kabam.cbsafl_sfish
        """
        try:
            self.blackbox_method_int('cbsafl_sfish')
        finally:
            pass
        return

    def test_cbsafl_mfish(self):
        """
        Integration test for kabam.cbsafl_mfish
        """
        try:
            self.blackbox_method_int('cbsafl_mfish')
        finally:
            pass
        return

    def test_cbsafl_lfish(self):
        """
        Integration test for kabam.cbsafl_lfish
        """
        try:
            self.blackbox_method_int('cbsafl_lfish')
        finally:
            pass
        return

    def test_mweight0(self):
        """
        Integration test for kabam.mweight0
        """
        try:
            self.blackbox_method_int('mweight0')
        finally:
            pass
        return

    def test_mweight1(self):
        """
        Integration test for kabam.mweight1
        """
        try:
            self.blackbox_method_int('mweight1')
        finally:
            pass
        return

    def test_mweight2(self):
        """
        Integration test for kabam.mweight2
        """
        try:
            self.blackbox_method_int('mweight2')
        finally:
            pass
        return

    def test_mweight3(self):
        """
        Integration test for kabam.mweight3
        """
        try:
            self.blackbox_method_int('mweight3')
        finally:
            pass
        return

    def test_mweight4(self):
        """
        Integration test for kabam.mweight4
        """
        try:
            self.blackbox_method_int('mweight4')
        finally:
            pass
        return

    def test_mweight5(self):
        """
        Integration test for kabam.mweight5
        """
        try:
            self.blackbox_method_int('mweight5')
        finally:
            pass
        return

    def test_aweight0(self):
        """
        Integration test for kabam.aweight0
        """
        try:
            self.blackbox_method_int('aweight0')
        finally:
            pass
        return

    def test_aweight1(self):
        """
        Integration test for kabam.aweight1
        """
        try:
            self.blackbox_method_int('aweight1')
        finally:
            pass
        return

    def test_cb_beninv(self):
        """
        Integration test for kabam.aweight2
        """
        try:
            self.blackbox_method_int('aweight2')
        finally:
            pass
        return

    def test_aweight3(self):
        """
        Integration test for kabam.aweight3
        """
        try:
            self.blackbox_method_int('aweight3')
        finally:
            pass
        return

    def test_aweight4(self):
        """
        Integration test for kabam.aweight4
        """
        try:
            self.blackbox_method_int('aweight4')
        finally:
            pass
        return

    def test_aweight5(self):
        """
        Integration test for kabam.aweight5
        """
        try:
            self.blackbox_method_int('aweight5')
        finally:
            pass
        return

    def test_dfir0(self):
        """
        Integration test for kabam.dfir0
        """
        try:
            self.blackbox_method_int('dfir0')
        finally:
            pass
        return

    def test_dfir1(self):
        """
        Integration test for kabam.dfir1
        """
        try:
            self.blackbox_method_int('dfir1')
        finally:
            pass
        return

    def test_dfir2(self):
        """
        Integration test for kabam.dfir2
        """
        try:
            self.blackbox_method_int('dfir2')
        finally:
            pass
        return

    def test_dfir3(self):
        """
        Integration test for kabam.dfir3
        """
        try:
            self.blackbox_method_int('dfir3')
        finally:
            pass
        return

    def test_dfir4(self):
        """
        Integration test for kabam.dfir4
        """
        try:
            self.blackbox_method_int('dfir4')
        finally:
            pass
        return

    def test_dfir5(self):
        """
        Integration test for kabam.dfir5
        """
        try:
            self.blackbox_method_int('dfir5')
        finally:
            pass
        return

    def test_dfira0(self):
        """
        Integration test for kabam.dfira0
        """
        try:
            self.blackbox_method_int('dfira0')
        finally:
            pass
        return

    def test_dfira1(self):
        """
        Integration test for kabam.dfira1
        """
        try:
            self.blackbox_method_int('dfira1')
        finally:
            pass
        return

    def test_dfira2(self):
        """
        Integration test for kabam.dfira2
        """
        try:
            self.blackbox_method_int('dfira2')
        finally:
            pass
        return

    def test_dfira3(self):
        """
        Integration test for kabam.dfira3
        """
        try:
            self.blackbox_method_int('dfira3')
        finally:
            pass
        return

    def test_dfira4(self):
        """
        Integration test for kabam.dfira4
        """
        try:
            self.blackbox_method_int('dfira4')
        finally:
            pass
        return

    def test_dfira5(self):
        """
        Integration test for kabam.dfira5
        """
        try:
            self.blackbox_method_int('dfira5')
        finally:
            pass
        return

    def test_wet_food_ingestion_m0(self):
        """
        Integration test for kabam.wet_food_ingestion_m0
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_m0')
        finally:
            pass
        return

    def test_wet_food_ingestion_m1(self):
        """
        Integration test for kabam.wet_food_ingestion_m1
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_m1')
        finally:
            pass
        return

    def test_wet_food_ingestion_m2(self):
        """
        Integration test for kabam.wet_food_ingestion_m2
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_m2')
        finally:
            pass
        return

    def test_wet_food_ingestion_m3(self):
        """
        Integration test for kabam.wet_food_ingestion_m3
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_m3')
        finally:
            pass
        return

    def test_wet_food_ingestion_m4(self):
        """
        Integration test for kabam.wet_food_ingestion_m4
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_m4')
        finally:
            pass
        return

    def test_wet_food_ingestion_m5(self):
        """
        Integration test for kabam.wet_food_ingestion_m5
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_m5')
        finally:
            pass
        return

    def test_wet_food_ingestion_a0(self):
        """
        Integration test for kabam.wet_food_ingestion_a0
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_a0')
        finally:
            pass
        return

    def test_wet_food_ingestion_a1(self):
        """
        Integration test for kabam.wet_food_ingestion_a1
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_a1')
        finally:
            pass
        return

    def test_wet_food_ingestion_a2(self):
        """
        Integration test for kabam.wet_food_ingestion_a2
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_a2')
        finally:
            pass
        return

    def test_wet_food_ingestion_a3(self):
        """
        Integration test for kabam.wet_food_ingestion_a3
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_a3')
        finally:
            pass
        return

    def test_wet_food_ingestion_a4(self):
        """
        Integration test for kabam.wet_food_ingestion_a4
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_a4')
        finally:
            pass
        return

    def test_wet_food_ingestion_a5(self):
        """
        Integration test for kabam.wet_food_ingestion_a5
        """
        try:
            self.blackbox_method_int('wet_food_ingestion_a5')
        finally:
            pass
        return

    def test_drinking_water_intake_m0(self):
        """
        Integration test for kabam.drinking_water_intake_m0
        """
        try:
            self.blackbox_method_int('drinking_water_intake_m0')
        finally:
            pass
        return

    def test_drinking_water_intake_m1(self):
        """
        Integration test for kabam.drinking_water_intake_m1
        """
        try:
            self.blackbox_method_int('drinking_water_intake_m1')
        finally:
            pass
        return

    def test_drinking_water_intake_m2(self):
        """
        Integration test for kabam.drinking_water_intake_m2
        """
        try:
            self.blackbox_method_int('drinking_water_intake_m2')
        finally:
            pass
        return

    def test_drinking_water_intake_m3(self):
        """
        Integration test for kabam.drinking_water_intake_m3
        """
        try:
            self.blackbox_method_int('drinking_water_intake_m3')
        finally:
            pass
        return

    def test_drinking_water_intake_m4(self):
        """
        Integration test for kabam.drinking_water_intake_m4
        """
        try:
            self.blackbox_method_int('drinking_water_intake_m4')
        finally:
            pass
        return

    def test_drinking_water_intake_m5(self):
        """
        Integration test for kabam.drinking_water_intake_m5
        """
        try:
            self.blackbox_method_int('drinking_water_intake_m5')
        finally:
            pass
        return

    def test_drinking_water_intake_a0(self):
        """
        Integration test for kabam.drinking_water_intake_a0
        """
        try:
            self.blackbox_method_int('drinking_water_intake_a0')
        finally:
            pass
        return

    def test_drinking_water_intake_a1(self):
        """
        Integration test for kabam.drinking_water_intake_a1
        """
        try:
            self.blackbox_method_int('drinking_water_intake_a1')
        finally:
            pass
        return

    def test_drinking_water_intake_a2(self):
        """
        Integration test for kabam.drinking_water_intake_a2
        """
        try:
            self.blackbox_method_int('drinking_water_intake_a2')
        finally:
            pass
        return

    def test_drinking_water_intake_a3(self):
        """
        Integration test for kabam.drinking_water_intake_a3
        """
        try:
            self.blackbox_method_int('drinking_water_intake_a3')
        finally:
            pass
        return

    def test_drinking_water_intake_a4(self):
        """
        Integration test for kabam.drinking_water_intake_a4
        """
        try:
            self.blackbox_method_int('drinking_water_intake_a4')
        finally:
            pass
        return

    def test_drinking_water_intake_a5(self):
        """
        Integration test for kabam.drinking_water_intake_a5
        """
        try:
            self.blackbox_method_int('drinking_water_intake_a5')
        finally:
            pass
        return

    def test_db40(self):
        """
        Integration test for kabam.db40
        """
        try:
            self.blackbox_method_int('db40')
        finally:
            pass
        return

    def test_db41(self):
        """
        Integration test for kabam.db41
        """
        try:
            self.blackbox_method_int('db41')
        finally:
            pass
        return

    def test_db42(self):
        """
        Integration test for kabam.db42
        """
        try:
            self.blackbox_method_int('db42')
        finally:
            pass
        return

    def test_db43(self):
        """
        Integration test for kabam.db43
        """
        try:
            self.blackbox_method_int('db43')
        finally:
            pass
        return

    def test_db44(self):
        """
        Integration test for kabam.db44
        """
        try:
            self.blackbox_method_int('db44')
        finally:
            pass
        return

    def test_db45(self):
        """
        Integration test for kabam.db45
        """
        try:
            self.blackbox_method_int('db45')
        finally:
            pass
        return

    def test_db4a0(self):
        """
        Integration test for kabam.db4a0
        """
        try:
            self.blackbox_method_int('db4a0')
        finally:
            pass
        return

    def test_db4a1(self):
        """
        Integration test for kabam.db4a1
        """
        try:
            self.blackbox_method_int('db4a1')
        finally:
            pass
        return

    def test_db4a2(self):
        """
        Integration test for kabam.db4a2
        """
        try:
            self.blackbox_method_int('db4a2')
        finally:
            pass
        return

    def test_db4a3(self):
        """
        Integration test for kabam.db4a3
        """
        try:
            self.blackbox_method_int('db4a3')
        finally:
            pass
        return

    def test_db4a4(self):
        """
        Integration test for kabam.db4a4
        """
        try:
            self.blackbox_method_int('db4a4')
        finally:
            pass
        return

    def test_db4a5(self):
        """
        Integration test for kabam.db4a5
        """
        try:
            self.blackbox_method_int('db4a5')
        finally:
            pass
        return

    def test_db50(self):
        """
        Integration test for kabam.db50
        """
        try:
            self.blackbox_method_int('db50')
        finally:
            pass
        return

    def test_db51(self):
        """
        Integration test for kabam.db51
        """
        try:
            self.blackbox_method_int('db51')
        finally:
            pass
        return

    def test_db52(self):
        """
        Integration test for kabam.db52
        """
        try:
            self.blackbox_method_int('db52')
        finally:
            pass
        return

    def test_db53(self):
        """
        Integration test for kabam.db53
        """
        try:
            self.blackbox_method_int('db53')
        finally:
            pass
        return

    def test_db54(self):
        """
        Integration test for kabam.db54
        """
        try:
            self.blackbox_method_int('db54')
        finally:
            pass
        return

    def test_db55(self):
        """
        Integration test for kabam.db55
        """
        try:
            self.blackbox_method_int('db55')
        finally:
            pass
        return

    def test_db5a0(self):
        """
        Integration test for kabam.db5a0
        """
        try:
            self.blackbox_method_int('db5a0')
        finally:
            pass
        return

    def test_db5a1(self):
        """
        Integration test for kabam.db5a1
        """
        try:
            self.blackbox_method_int('db5a1')
        finally:
            pass
        return

    def test_db5a2(self):
        """
        Integration test for kabam.db5a2
        """
        try:
            self.blackbox_method_int('db5a2')
        finally:
            pass
        return

    def test_db5a3(self):
        """
        Integration test for kabam.db5a3
        """
        try:
            self.blackbox_method_int('db5a3')
        finally:
            pass
        return

    def test_db5a4(self):
        """
        Integration test for kabam.db5a4
        """
        try:
            self.blackbox_method_int('db5a4')
        finally:
            pass
        return

    def test_db5a5(self):
        """
        Integration test for kabam.db5a5
        """
        try:
            self.blackbox_method_int('db5a5')
        finally:
            pass
        return

    def test_acute_dose_based_m0(self):
        """
        Integration test for kabam.acute_dose_based_m0
        """
        try:
            self.blackbox_method_int('acute_dose_based_m0')
        finally:
            pass
        return

    def test_acute_dose_based_m1(self):
        """
        Integration test for kabam.acute_dose_based_m1
        """
        try:
            self.blackbox_method_int('acute_dose_based_m1')
        finally:
            pass
        return

    def test_acute_dose_based_m2(self):
        """
        Integration test for kabam.acute_dose_based_m2
        """
        try:
            self.blackbox_method_int('acute_dose_based_m2')
        finally:
            pass
        return

    def test_acute_dose_based_m3(self):
        """
        Integration test for kabam.acute_dose_based_m3
        """
        try:
            self.blackbox_method_int('acute_dose_based_m3')
        finally:
            pass
        return

    def test_acute_dose_based_m4(self):
        """
        Integration test for kabam.acute_dose_based_m4
        """
        try:
            self.blackbox_method_int('acute_dose_based_m4')
        finally:
            pass
        return

    def test_acute_dose_based_m5(self):
        """
        Integration test for kabam.acute_dose_based_m5
        """
        try:
            self.blackbox_method_int('acute_dose_based_m5')
        finally:
            pass
        return

    def test_acute_dose_based_a0(self):
        """
        Integration test for kabam.acute_dose_based_a0
        """
        try:
            self.blackbox_method_int('acute_dose_based_a0')
        finally:
            pass
        return

    def test_acute_dose_based_a1(self):
        """
        Integration test for kabam.acute_dose_based_a1
        """
        try:
            self.blackbox_method_int('acute_dose_based_a1')
        finally:
            pass
        return

    def test_acute_dose_based_a2(self):
        """
        Integration test for kabam.acute_dose_based_a2
        """
        try:
            self.blackbox_method_int('acute_dose_based_a2')
        finally:
            pass
        return

    def test_acute_dose_based_a3(self):
        """
        Integration test for kabam.acute_dose_based_a3
        """
        try:
            self.blackbox_method_int('acute_dose_based_a3')
        finally:
            pass
        return

    def test_acute_dose_based_a4(self):
        """
        Integration test for kabam.acute_dose_based_a4
        """
        try:
            self.blackbox_method_int('acute_dose_based_a4')
        finally:
            pass
        return

    def test_acute_dose_based_a5(self):
        """
        Integration test for kabam.acute_dose_based_a5
        """
        try:
            self.blackbox_method_int('acute_dose_based_a5')
        finally:
            pass
        return

    def test_acute_diet_based_m0(self):
        """
        Integration test for kabam.acute_diet_based_m0
        """
        try:
            self.blackbox_method_int('acute_diet_based_m0')
        finally:
            pass
        return

    def test_acute_diet_based_m1(self):
        """
        Integration test for kabam.acute_diet_based_m1
        """
        try:
            self.blackbox_method_int('acute_diet_based_m1')
        finally:
            pass
        return

    def test_acute_diet_based_m2(self):
        """
        Integration test for kabam.acute_diet_based_m2
        """
        try:
            self.blackbox_method_int('acute_diet_based_m2')
        finally:
            pass
        return

    def test_acute_diet_based_m3(self):
        """
        Integration test for kabam.acute_diet_based_m3
        """
        try:
            self.blackbox_method_int('acute_diet_based_m3')
        finally:
            pass
        return

    def test_acute_diet_based_m4(self):
        """
        Integration test for kabam.acute_diet_based_m4
        """
        try:
            self.blackbox_method_int('acute_diet_based_m4')
        finally:
            pass
        return

    def test_acute_diet_based_m5(self):
        """
        Integration test for kabam.acute_diet_based_m5
        """
        try:
            self.blackbox_method_int('acute_diet_based_m5')
        finally:
            pass
        return

    def test_acute_diet_based_a0(self):
        """
        Integration test for kabam.acute_diet_based_a0
        """
        try:
            self.blackbox_method_int('acute_diet_based_a0')
        finally:
            pass
        return

    def test_acute_diet_based_a1(self):
        """
        Integration test for kabam.acute_diet_based_a1
        """
        try:
            self.blackbox_method_int('acute_diet_based_a1')
        finally:
            pass
        return

    def test_acute_diet_based_a2(self):
        """
        Integration test for kabam.acute_diet_based_a2
        """
        try:
            self.blackbox_method_int('acute_diet_based_a2')
        finally:
            pass
        return

    def test_acute_diet_based_a3(self):
        """
        Integration test for kabam.acute_diet_based_a3
        """
        try:
            self.blackbox_method_int('acute_diet_based_a3')
        finally:
            pass
        return

    def test_acute_diet_based_a4(self):
        """
        Integration test for kabam.acute_diet_based_a4
        """
        try:
            self.blackbox_method_int('acute_diet_based_a4')
        finally:
            pass
        return

    def test_acute_diet_based_a5(self):
        """
        Integration test for kabam.acute_diet_based_a5
        """
        try:
            self.blackbox_method_int('acute_diet_based_a5')
        finally:
            pass
        return

    def test_chronic_dose_based_m0(self):
        """
        Integration test for kabam.chronic_dose_based_m0
        """
        try:
            self.blackbox_method_int('chronic_dose_based_m0')
        finally:
            pass
        return

    def test_chronic_dose_based_m1(self):
        """
        Integration test for kabam.chronic_dose_based_m1
        """
        try:
            self.blackbox_method_int('chronic_dose_based_m1')
        finally:
            pass
        return

    def test_chronic_dose_based_m2(self):
        """
        Integration test for kabam.chronic_dose_based_m2
        """
        try:
            self.blackbox_method_int('chronic_dose_based_m2')
        finally:
            pass
        return

    def test_chronic_dose_based_m3(self):
        """
        Integration test for kabam.chronic_dose_based_m3
        """
        try:
            self.blackbox_method_int('chronic_dose_based_m3')
        finally:
            pass
        return

    def test_chronic_dose_based_m4(self):
        """
        Integration test for kabam.chronic_dose_based_m4
        """
        try:
            self.blackbox_method_int('chronic_dose_based_m4')
        finally:
            pass
        return

    def test_chronic_dose_based_m5(self):
        """
        Integration test for kabam.chronic_dose_based_m5
        """
        try:
            self.blackbox_method_int('chronic_dose_based_m5')
        finally:
            pass
        return

    def test_chronic_diet_based_m0(self):
        """
        Integration test for kabam.chronic_diet_based_m0
        """
        try:
            self.blackbox_method_int('chronic_diet_based_m0')
        finally:
            pass
        return

    def test_chronic_diet_based_m1(self):
        """
        Integration test for kabam.chronic_diet_based_m1
        """
        try:
            self.blackbox_method_int('chronic_diet_based_m1')
        finally:
            pass
        return

    def test_chronic_diet_based_m2(self):
        """
        Integration test for kabam.chronic_diet_based_m2
        """
        try:
            self.blackbox_method_int('chronic_diet_based_m2')
        finally:
            pass
        return

    def test_chronic_diet_based_m3(self):
        """
        Integration test for kabam.chronic_diet_based_m3
        """
        try:
            self.blackbox_method_int('chronic_diet_based_m3')
        finally:
            pass
        return

    def test_chronic_diet_based_m4(self):
        """
        Integration test for kabam.chronic_diet_based_m4
        """
        try:
            self.blackbox_method_int('chronic_diet_based_m4')
        finally:
            pass
        return

    def test_chronic_diet_based_m5(self):
        """
        Integration test for kabam.chronic_diet_based_m5
        """
        try:
            self.blackbox_method_int('chronic_diet_based_m5')
        finally:
            pass
        return

    def test_chronic_diet_based_a0(self):
        """
        Integration test for kabam.chronic_diet_based_a0
        """
        try:
            self.blackbox_method_int('chronic_diet_based_a0')
        finally:
            pass
        return

    def test_chronic_diet_based_a1(self):
        """
        Integration test for kabam.chronic_diet_based_a1
        """
        try:
            self.blackbox_method_int('chronic_diet_based_a1')
        finally:
            pass
        return

    def test_chronic_diet_based_a2(self):
        """
        Integration test for kabam.chronic_diet_based_a2
        """
        try:
            self.blackbox_method_int('chronic_diet_based_a2')
        finally:
            pass
        return

    def test_chronic_diet_based_a3(self):
        """
        Integration test for kabam.chronic_diet_based_a3
        """
        try:
            self.blackbox_method_int('chronic_diet_based_a3')
        finally:
            pass
        return

    def test_chronic_diet_based_a4(self):
        """
        Integration test for kabam.chronic_diet_based_a4
        """
        try:
            self.blackbox_method_int('chronic_diet_based_a4')
        finally:
            pass
        return

    def test_chronic_diet_based_a5(self):
        """
        Integration test for kabam.chronic_diet_based_a5
        """
        try:
            self.blackbox_method_int('chronic_diet_based_a5')
        finally:
            pass
        return

    def test_acute_rq_dose_m0(self):
        """
        Integration test for kabam.acute_rq_dose_m0
        """
        try:
            self.blackbox_method_int('acute_rq_dose_m0')
        finally:
            pass
        return

    def test_acute_rq_dose_m1(self):
        """
        Integration test for kabam.acute_rq_dose_m1
        """
        try:
            self.blackbox_method_int('acute_rq_dose_m1')
        finally:
            pass
        return

    def test_acute_rq_dose_m2(self):
        """
        Integration test for kabam.acute_rq_dose_m2
        """
        try:
            self.blackbox_method_int('acute_rq_dose_m2')
        finally:
            pass
        return

    def test_acute_rq_dose_m3(self):
        """
        Integration test for kabam.acute_rq_dose_m3
        """
        try:
            self.blackbox_method_int('acute_rq_dose_m3')
        finally:
            pass
        return

    def test_acute_rq_dose_m4(self):
        """
        Integration test for kabam.acute_rq_dose_m4
        """
        try:
            self.blackbox_method_int('acute_rq_dose_m4')
        finally:
            pass
        return

    def test_acute_rq_dose_m5(self):
        """
        Integration test for kabam.acute_rq_dose_m5
        """
        try:
            self.blackbox_method_int('acute_rq_dose_m5')
        finally:
            pass
        return

    def test_acute_rq_dose_a0(self):
        """
        Integration test for kabam.acute_rq_dose_a0
        """
        try:
            self.blackbox_method_int('acute_rq_dose_a0')
        finally:
            pass
        return

    def test_acute_rq_dose_a1(self):
        """
        Integration test for kabam.acute_rq_dose_a1
        """
        try:
            self.blackbox_method_int('acute_rq_dose_a1')
        finally:
            pass
        return

    def test_acute_rq_dose_a2(self):
        """
        Integration test for kabam.acute_rq_dose_a2
        """
        try:
            self.blackbox_method_int('acute_rq_dose_a2')
        finally:
            pass
        return

    def test_acute_rq_dose_a3(self):
        """
        Integration test for kabam.acute_rq_dose_a3
        """
        try:
            self.blackbox_method_int('acute_rq_dose_a3')
        finally:
            pass
        return

    def test_acute_rq_dose_a4(self):
        """
        Integration test for kabam.acute_rq_dose_a4
        """
        try:
            self.blackbox_method_int('acute_rq_dose_a4')
        finally:
            pass
        return

    def test_acute_rq_dose_a5(self):
        """
        Integration test for kabam.acute_rq_dose_a5
        """
        try:
            self.blackbox_method_int('acute_rq_dose_a5')
        finally:
            pass
        return

    def test_acute_rq_diet_m0(self):
        """
        Integration test for kabam.acute_rq_diet_m0
        """
        try:
            self.blackbox_method_int('acute_rq_diet_m0')
        finally:
            pass
        return

    def test_acute_rq_diet_m1(self):
        """
        Integration test for kabam.acute_rq_diet_m1
        """
        try:
            self.blackbox_method_int('acute_rq_diet_m1')
        finally:
            pass
        return

    def test_acute_rq_diet_m2(self):
        """
        Integration test for kabam.acute_rq_diet_m2
        """
        try:
            self.blackbox_method_int('acute_rq_diet_m2')
        finally:
            pass
        return

    def test_acute_rq_diet_m3(self):
        """
        Integration test for kabam.acute_rq_diet_m3
        """
        try:
            self.blackbox_method_int('acute_rq_diet_m3')
        finally:
            pass
        return

    def test_acute_rq_diet_m4(self):
        """
        Integration test for kabam.acute_rq_diet_m4
        """
        try:
            self.blackbox_method_int('acute_rq_diet_m4')
        finally:
            pass
        return

    def test_acute_rq_diet_m5(self):
        """
        Integration test for kabam.acute_rq_diet_m5
        """
        try:
            self.blackbox_method_int('acute_rq_diet_m5')
        finally:
            pass
        return

    def test_acute_rq_diet_a0(self):
        """
        Integration test for kabam.acute_rq_diet_a0
        """
        try:
            self.blackbox_method_int('acute_rq_diet_a0')
        finally:
            pass
        return

    def test_acute_rq_diet_a1(self):
        """
        Integration test for kabam.acute_rq_diet_a1
        """
        try:
            self.blackbox_method_int('acute_rq_diet_a1')
        finally:
            pass
        return

    def test_acute_rq_diet_a2(self):
        """
        Integration test for kabam.acute_rq_diet_a2
        """
        try:
            self.blackbox_method_int('acute_rq_diet_a2')
        finally:
            pass
        return

    def test_acute_rq_diet_a3(self):
        """
        Integration test for kabam.acute_rq_diet_a3
        """
        try:
            self.blackbox_method_int('acute_rq_diet_a3')
        finally:
            pass
        return

    def test_acute_rq_diet_a4(self):
        """
        Integration test for kabam.acute_rq_diet_a4
        """
        try:
            self.blackbox_method_int('acute_rq_diet_a4')
        finally:
            pass
        return

    def test_acute_rq_diet_a5(self):
        """
        Integration test for kabam.acute_rq_diet_a5
        """
        try:
            self.blackbox_method_int('acute_rq_diet_a5')
        finally:
            pass
        return

    def test_chronic_rq_dose_m0(self):
        """
        Integration test for kabam.chronic_rq_dose_m0
        """
        try:
            self.blackbox_method_int('chronic_rq_dose_m0')
        finally:
            pass
        return

    def test_chronic_rq_dose_m1(self):
        """
        Integration test for kabam.chronic_rq_dose_m1
        """
        try:
            self.blackbox_method_int('chronic_rq_dose_m1')
        finally:
            pass
        return

    def test_chronic_rq_dose_m2(self):
        """
        Integration test for kabam.chronic_rq_dose_m2
        """
        try:
            self.blackbox_method_int('chronic_rq_dose_m2')
        finally:
            pass
        return

    def test_chronic_rq_dose_m3(self):
        """
        Integration test for kabam.chronic_rq_dose_m3
        """
        try:
            self.blackbox_method_int('chronic_rq_dose_m3')
        finally:
            pass
        return

    def test_chronic_rq_dose_m4(self):
        """
        Integration test for kabam.chronic_rq_dose_m4
        """
        try:
            self.blackbox_method_int('chronic_rq_dose_m4')
        finally:
            pass
        return

    def test_chronic_rq_dose_m5(self):
        """
        Integration test for kabam.chronic_rq_dose_m5
        """
        try:
            self.blackbox_method_int('chronic_rq_dose_m5')
        finally:
            pass
        return

    def test_chronic_rq_diet_m0(self):
        """
        Integration test for kabam.chronic_rq_diet_m0
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_m0')
        finally:
            pass
        return

    def test_chronic_rq_diet_m1(self):
        """
        Integration test for kabam.chronic_rq_diet_m1
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_m1')
        finally:
            pass
        return

    def test_chronic_rq_diet_m2(self):
        """
        Integration test for kabam.chronic_rq_diet_m2
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_m2')
        finally:
            pass
        return

    def test_chronic_rq_diet_m3(self):
        """
        Integration test for kabam.chronic_rq_diet_m3
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_m3')
        finally:
            pass
        return

    def test_chronic_rq_diet_m4(self):
        """
        Integration test for kabam.chronic_rq_diet_m4
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_m4')
        finally:
            pass
        return

    def test_chronic_rq_diet_m5(self):
        """
        Integration test for kabam.chronic_rq_diet_m5
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_m5')
        finally:
            pass
        return

    def test_chronic_rq_diet_a0(self):
        """
        Integration test for kabam.chronic_rq_diet_a0
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_a0')
        finally:
            pass
        return

    def test_chronic_rq_diet_a1(self):
        """
        Integration test for kabam.chronic_rq_diet_a1
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_a1')
        finally:
            pass
        return

    def test_chronic_rq_diet_a2(self):
        """
        Integration test for kabam.chronic_rq_diet_a2
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_a2')
        finally:
            pass
        return

    def test_chronic_rq_diet_a3(self):
        """
        Integration test for kabam.chronic_rq_diet_a3
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_a3')
        finally:
            pass
        return

    def test_chronic_rq_diet_a4(self):
        """
        Integration test for kabam.chronic_rq_diet_a4
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_a4')
        finally:
            pass
        return

    def test_chronic_rq_diet_a5(self):
        """
        Integration test for kabam.chronic_rq_diet_a5
        """
        try:
            self.blackbox_method_int('chronic_rq_diet_a5')
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
        result = kabam_calc.pd_obj_out["out_" + output]
        expected = kabam_calc.pd_obj_exp["exp_" + output]
        tab = pd.concat([result,expected], axis=1)
        print(" ")
        print(tabulate(tab, headers='keys', tablefmt='fancy_grid'))
        err_msg = str(result) + '\n' + str(expected)
        # npt.assert_array_almost_equal(result, expected, 4, '', True)
        rtol = 1e-5
        npt.assert_allclose(result,expected,rtol,0,True,err_msg,True)

    def blackbox_method_str(self, output):
        """
        Helper method.
        :param output:
        :return:
        """
        result = kabam_calc.pd_obj_out["out_" + output]
        expected = kabam_calc.pd_obj_exp["exp_" + output]
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