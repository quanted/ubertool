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
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')
        #with open('./sip_qaqc_in_transpose.csv') as f:
            #csv_data = csv.reader(f)
finally:
    pass
    #print("trex inputs")
    #print(pd_obj_inputs.shape)
    #print('trex expected output keys ' + str(pd_obj_inputs.columns.values.tolist()))
    #print(tabulate(pd_obj_inputs.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,11:13], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_inputs.iloc[:,14:17], headers='keys', tablefmt='plain'))

# load transposed qaqc data for expected outputs
try:
    if __package__ is not None:
        data_exp_outputs = StringIO(pkgutil.get_data(__package__, 'trex_qaqc_exp_transpose.csv'))
        pd_obj_exp = pd.read_csv(data_exp_outputs, index_col=0, engine= 'python')
    else:
        csv_transpose_path_exp = "./trex_qaqc_exp_transpose.csv"
        #print(csv_transpose_path_exp)
        pd_obj_exp = pd.read_csv(csv_transpose_path_exp, index_col=0, engine='python')
finally:
    pass
    #print("trex expected outputs")
    #print('trex expected output dimensions ' + str(pd_obj_exp.shape))
    #print('trex expected output keys ' + str(pd_obj_exp.columns.values.tolist()))
    #print(tabulate(pd_obj_exp.iloc[:,0:5], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,6:10], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,11:14], headers='keys', tablefmt='plain'))
    #print(tabulate(pd_obj_exp.iloc[:,15:16], headers='keys', tablefmt='plain'))

# create an instance of trex object with qaqc data
trex_calc = TRex(pd_obj_inputs, pd_obj_exp)
trex_calc.execute_model()
inputs_json, outputs_json, exp_out_json = trex_calc.get_dict_rep(trex_calc)
#print("trex output")
#print(inputs_json)
#print("####")
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
        Integration test for trex.eec_diet_sg
        """
        try:
            self.blackbox_method_int('eec_diet_sg')
        finally:
            pass
        return

    def test_eec_diet_tg(self):
        """
        Integration test for trex.eec_diet_tg
        """
        try:
            self.blackbox_method_int('eec_diet_tg')
        finally:
            pass
        return

    def test_eec_diet_bp(self):
        """
        Integration test for trex.eec_diet_bp
        """
        try:
            self.blackbox_method_int('eec_diet_bp')
        finally:
            pass
        return

    def test_eec_diet_fr(self):
        """
        Integration test for trex.eec_diet_fr
        """
        try:
            self.blackbox_method_int('eec_diet_fr')
        finally:
            pass
        return

    def test_eec_diet_ar(self):
        """
        Integration test for trex.eec_diet_ar
        """
        try:
            self.blackbox_method_int('eec_diet_ar')
        finally:
            pass
        return

    def test_eec_dose_bird_sg_sm(self):
        """
        Integration test for trex.eec_dose_bird_sg_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bird_sg_sm')
        finally:
            pass
        return

    def test_eec_dose_bird_sg_md(self):
        """
        Integration test for trex.eec_dose_bird_sg_md
        """
        try:
            self.blackbox_method_int('eec_dose_bird_sg_md')
        finally:
            pass
        return

    def test_eec_dose_bird_sg_lg(self):
        """
        Integration test for trex.eec_dose_bird_sg_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bird_sg_lg')
        finally:
            pass
        return

    def test_eec_dose_bird_tg_sm(self):
        """
        Integration test for trex.eec_dose_bird_tg_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bird_tg_sm')
        finally:
            pass
        return

    def test_eec_dose_bird_tg_md(self):
        """
        Integration test for trex.eec_dose_bird_tg_m
        """
        try:
            self.blackbox_method_int('eec_dose_bird_tg_md')
        finally:
            pass
        return

    def test_eec_dose_bird_tg_lg(self):
        """
        Integration test for trex.eec_dose_bird_tg_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bird_tg_lg')
        finally:
            pass
        return

    def test_eec_dose_bird_bp_sm(self):
        """
        Integration test for trex.eec_dose_bird_bp_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bird_bp_sm')
        finally:
            pass
        return

    def test_eec_dose_bird_bp_md(self):
        """
        Integration test for trex.eec_dose_bird_bp_md
        """
        try:
            self.blackbox_method_int('eec_dose_bird_bp_md')
        finally:
            pass
        return

    def test_eec_dose_bird_bp_lg(self):
        """
        Integration test for trex.eec_dose_bird_bp_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bird_bp_lg')
        finally:
            pass
        return

    def test_eec_dose_bird_fp_sm(self):
        """
        Integration test for trex.eec_dose_bird_fp_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bird_fp_sm')
        finally:
            pass
        return

    def test_eec_dose_bird_fp_md(self):
        """
        Integration test for trex.eec_dose_bird_fp_md
        """
        try:
            self.blackbox_method_int('eec_dose_bird_fp_md')
        finally:
            pass
        return

    def test_eec_dose_bird_fp_lg(self):
        """
        Integration test for trex.eec_dose_bird_fp_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bird_fp_lg')
        finally:
            pass
        return

    def test_eec_dose_bird_ar_sm(self):
        """
        Integration test for trex.eec_dose_bird_ar_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bird_ar_sm')
        finally:
            pass
        return

    def test_eec_dose_bird_ar_md(self):
        """
        Integration test for trex.eec_dose_bird_ar_md
        """
        try:
            self.blackbox_method_int('eec_dose_bird_ar_md')
        finally:
            pass
        return

    def test_eec_dose_bird_ar_lg(self):
        """
        Integration test for trex.eec_dose_bird_ar_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bird_ar_lg')
        finally:
            pass
        return

    def test_eec_dose_bird_se_sm(self):
        """
        Integration test for trex.eec_dose_bird_se_sm
        """
        try:
            self.blackbox_method_int('eec_dose_bird_se_sm')
        finally:
            pass
        return

    def test_eec_dose_bird_se_md(self):
        """
        Integration test for trex.eec_dose_bird_se_md
        """
        try:
            self.blackbox_method_int('eec_dose_bird_se_md')
        finally:
            pass
        return

    def test_eec_dose_bird_se_lg(self):
        """
        Integration test for trex.eec_dose_bird_se_lg
        """
        try:
            self.blackbox_method_int('eec_dose_bird_se_lg')
        finally:
            pass
        return

    def test_arq_bird_sg_sm(self):
        """
        Integration test for trex.arq_bird_sg_sm
        """
        try:
            self.blackbox_method_int('arq_bird_sg_sm')
        finally:
            pass
        return

    def test_arq_bird_sg_md(self):
        """
        Integration test for trex.arq_bird_sg_md
        """
        try:
            self.blackbox_method_int('arq_bird_sg_md')
        finally:
            pass
        return

    def test_arq_bird_sg_lg(self):
        """
        Integration test for trex.arq_bird_sg_lg
        """
        try:
            self.blackbox_method_int('arq_bird_sg_lg')
        finally:
            pass
        return

    def test_arq_bird_tg_sm(self):
        """
        Integration test for trex.arq_bird_tg_sm
        """
        try:
            self.blackbox_method_int('arq_bird_tg_sm')
        finally:
            pass
        return

    def test_arq_bird_tg_md(self):
        """
        Integration test for trex.arq_bird_tg_md
        """
        try:
            self.blackbox_method_int('arq_bird_tg_md')
        finally:
            pass
        return

    def test_arq_bird_tg_lg(self):
        """
        Integration test for trex.arq_bird_tg_lg
        """
        try:
            self.blackbox_method_int('arq_bird_tg_lg')
        finally:
            pass
        return

    def test_arq_bird_bp_sm(self):
        """
        Integration test for trex.arq_bird_bp_sm
        """
        try:
            self.blackbox_method_int('arq_bird_bp_sm')
        finally:
            pass
        return

    def test_arq_bird_bp_md(self):
        """
        Integration test for trex.arq_bird_bp_md
        """
        try:
            self.blackbox_method_int('arq_bird_bp_md')
        finally:
            pass
        return


    def test_arq_bird_bp_lg(self):
        """
        Integration test for trex.arq_bird_bp_lg
        """
        try:
            self.blackbox_method_int('arq_bird_bp_lg')
        finally:
            pass
        return

    def test_arq_bird_fp_sm(self):
        """
        Integration test for trex.arq_bird_fp_sm
        """
        try:
            self.blackbox_method_int('arq_bird_fp_sm')
        finally:
            pass

    def test_arq_bird_fp_mdg(self):
        """
        Integration test for trex.arq_bird_fp_md
        """
        try:
            self.blackbox_method_int('arq_bird_fp_md')
        finally:
            pass

    def test_arq_bird_fp_lg(self):
        """
        Integration test for trex.aarq_bird_fp_lg
        """
        try:
            self.blackbox_method_int('arq_bird_fp_lg')
        finally:
            pass

    def test_arq_bird_ar_sm(self):
        """
        Integration test for trex.arq_bird_ar_sm
        """
        try:
            self.blackbox_method_int('arq_bird_ar_sm')
        finally:
            pass

    def test_arq_bird_ar_md(self):
        """
        Integration test for trex.arq_bird_ar_md
        """
        try:
            self.blackbox_method_int('arq_bird_ar_md')
        finally:
            pass

    def test_arq_bird_ar_lg(self):
        """
        Integration test for trex.arq_bird_ar_lg
        """
        try:
            self.blackbox_method_int('arq_bird_ar_lg')
        finally:
            pass

    def test_arq_bird_se_sm(self):
        """
        Integration test for trex.arq_bird_se_sm
        """
        try:
            self.blackbox_method_int('arq_bird_se_sm')
        finally:
            pass

    def test_arq_bird_se_md(self):
        """
        Integration test for trex.arq_bird_se_md
        """
        try:
            self.blackbox_method_int('arq_bird_se_md')
        finally:
            pass

    def test_arq_bird_se_lg(self):
        """
        Integration test for trex.arq_bird_se_lg
        """
        try:
            self.blackbox_method_int('arq_bird_se_lg')
        finally:
            pass
        return

    def test_arq_diet_bird_sg_a(self):
        """
        Integration test for trex.arq_diet_bird_sg_a
        """
        try:
            self.blackbox_method_int('arq_diet_bird_sg_a')
        finally:
            pass
        return

    def test_arq_diet_bird_sg_c(self):
        """
        Integration test for trex.arq_diet_bird_sg_c
        """
        try:
            self.blackbox_method_int('arq_diet_bird_sg_c')
        finally:
            pass
        return

    def test_arq_diet_bird_tg_a(self):
        """
        Integration test for trex.arq_diet_bird_tg_a
        """
        try:
            self.blackbox_method_int('arq_diet_bird_tg_a')
        finally:
            pass
        return

    def test_arq_diet_bird_tg_c(self):
        """
        Integration test for trex.arq_diet_bird_tg_c
        """
        try:
            self.blackbox_method_int('arq_diet_bird_tg_c')
        finally:
            pass
        return

    def test_arq_diet_bird_bp_a(self):
        """
        Integration test for trex.arq_diet_bird_bp_a
        """
        try:
            self.blackbox_method_int('arq_diet_bird_bp_a')
        finally:
            pass
        return

    def test_arq_diet_bird_bp_c(self):
        """
        Integration test for trex.arq_diet_bird_bp_c
        """
        try:
            self.blackbox_method_int('arq_diet_bird_bp_c')
        finally:
            pass
        return

    def test_arq_diet_bird_fp_a(self):
        """
        Integration test for trex.arq_diet_bird_fp_a
        """
        try:
            self.blackbox_method_int('arq_diet_bird_fp_a')
        finally:
            pass
        return

    def test_arq_diet_bird_fp_c(self):
        """
        Integration test for trex.arq_diet_bird_fp_c
        """
        try:
            self.blackbox_method_int('arq_diet_bird_fp_c')
        finally:
            pass
        return

    def test_arq_diet_bird_ar_a(self):
        """
        Integration test for trex.arq_diet_bird_ar_a
        """
        try:
            self.blackbox_method_int('arq_diet_bird_ar_a')
        finally:
            pass
        return

    def test_arq_diet_bird_ar_c(self):
        """
        Integration test for trex.arq_diet_bird_ar_c
        """
        try:
            self.blackbox_method_int('arq_diet_bird_ar_c')
        finally:
            pass
        return

    def test_eec_dose_mamm_sg_sm(self):
        """
        Integration test for trex.eec_dose_mamm_sg_sm
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_sg_sm')
        finally:
            pass
        return

    def test_eec_dose_mamm_sg_md(self):
        """
        Integration test for trex.eec_dose_mamm_sg_md
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_sg_md')
        finally:
            pass
        return

    def test_eec_dose_mamm_sg_lg(self):
        """
        Integration test for trex.eec_dose_mamm_sg_lg
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_sg_lg')
        finally:
            pass
        return

    def test_eec_dose_mamm_tg_sm(self):
        """
        Integration test for trex.eec_dose_mamm_tg_sm
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_tg_sm')
        finally:
            pass
        return

    def test_eec_dose_mamm_tg_md(self):
        """
        Integration test for trex.eec_dose_mamm_tg_md
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_tg_md')
        finally:
            pass
        return

    def test_eec_dose_mamm_tg_lg(self):
        """
        Integration test for trex.eec_dose_mamm_tg_lg
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_tg_lg')
        finally:
            pass
        return

    def test_eec_dose_mamm_bp_sm(self):
        """
        Integration test for trex.eec_dose_mamm_bp_sm
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_bp_sm')
        finally:
            pass
        return

    def test_eec_dose_mamm_bp_md(self):
        """
        Integration test for trex.eec_dose_mamm_bp_md
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_bp_md')
        finally:
            pass
        return

    def test_eec_dose_mamm_bp_lg(self):
        """
        Integration test for trex.eec_dose_mamm_bp_lg
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_bp_lg')
        finally:
            pass
        return

    def test_eec_dose_mamm_fp_sm(self):
        """
        Integration test for trex.eec_dose_mamm_fp_sm
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_fp_sm')
        finally:
            pass
        return

    def test_eec_dose_mamm_fp_md(self):
        """
        Integration test for trex.eec_dose_mamm_fp_md
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_fp_md')
        finally:
            pass
        return

    def test_eec_dose_mamm_fp_lg(self):
        """
        Integration test for trex.eec_dose_mamm_fp_lg
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_fp_lg')
        finally:
            pass
        return

    def test_eec_dose_mamm_ar_sm(self):
        """
        Integration test for trex.eec_dose_mamm_ar_sm
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_ar_sm')
        finally:
            pass
        return

    def test_eec_dose_mamm_ar_md(self):
        """
        Integration test for trex.eec_dose_mamm_ar_md
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_ar_md')
        finally:
            pass
        return

    def test_eec_dose_mamm_ar_lg(self):
        """
        Integration test for trex.eec_dose_mamm_ar_lg
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_ar_lg')
        finally:
            pass
        return

    def test_eec_dose_mamm_se_sm(self):
        """
        Integration test for trex.eec_dose_mamm_se_sm
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_se_sm')
        finally:
            pass
        return

    def test_eec_dose_mamm_se_md(self):
        """
        Integration test for trex.eec_dose_mamm_se_md
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_se_md')
        finally:
            pass
        return

    def test_eec_dose_mamm_se_lg(self):
        """
        Integration test for trex.eec_dose_mamm_se_lg
        """
        try:
            self.blackbox_method_int('eec_dose_mamm_se_lg')
        finally:
            pass
        return

    def test_arq_dose_mamm_sg_sm(self):
        """
        Integration test for trex.arq_dose_mamm_sg_sm
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_sg_sm')
        finally:
            pass
        return

    def test_crq_dose_mamm_sg_sm(self):
        """
        Integration test for trex.crq_dose_mamm_sg_sm
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_sg_sm')
        finally:
            pass
        return

    def test_arq_dose_mamm_sg_md(self):
        """
        Integration test for trex.arq_dose_mamm_sg_md
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_sg_md')
        finally:
            pass
        return

    def test_crq_dose_mamm_sg_md(self):
        """
        Integration test for trex.crq_dose_mamm_sg_md
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_sg_md')
        finally:
            pass
        return

    def test_arq_dose_mamm_sg_lg(self):
        """
        Integration test for trex.arq_dose_mamm_sg_lg
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_sg_lg')
        finally:
            pass
        return

    def test_crq_dose_mamm_sg_lg(self):
        """
        Integration test for trex.crq_dose_mamm_sg_lg
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_sg_lg')
        finally:
            pass
        return

    def test_arq_dose_mamm_tg_sm(self):
        """
        Integration test for trex.arq_dose_mamm_tg_sm
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_tg_sm')
        finally:
            pass
        return

    def test_crq_dose_mamm_tg_sm(self):
        """
        Integration test for trex.crq_dose_mamm_tg_sm
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_tg_sm')
        finally:
            pass
        return

    def test_arq_dose_mamm_tg_md(self):
        """
        Integration test for trex.arq_dose_mamm_tg_md
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_tg_md')
        finally:
            pass
        return

    def test_crq_dose_mamm_tg_md(self):
        """
        Integration test for trex.crq_dose_mamm_tg_md
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_tg_md')
        finally:
            pass
        return

    def test_arq_dose_mamm_tg_lg(self):
        """
        Integration test for trex.arq_dose_mamm_tg_lg
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_tg_lg')
        finally:
            pass
        return

    def test_crq_dose_mamm_tg_lg(self):
        """
        Integration test for trex.crq_dose_mamm_tg_lg
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_tg_lg')
        finally:
            pass
        return

    def test_arq_dose_mamm_bp_sm(self):
        """
        Integration test for trex.arq_dose_mamm_bp_sm
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_bp_sm')
        finally:
            pass
        return

    def test_crq_dose_mamm_bp_sm(self):
        """
        Integration test for trex.crq_dose_mamm_bp_sm
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_bp_sm')
        finally:
            pass
        return

    def test_arq_dose_mamm_bp_md(self):
        """
        Integration test for trex.arq_dose_mamm_bp_md
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_bp_md')
        finally:
            pass
        return

    def test_crq_dose_mamm_bp_md(self):
        """
        Integration test for trex.crq_dose_mamm_bp_md
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_bp_md')
        finally:
            pass
        return

    def test_arq_dose_mamm_bp_lg(self):
        """
        Integration test for trex.arq_dose_mamm_bp_lg
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_bp_lg')
        finally:
            pass
        return

    def test_crq_dose_mamm_bp_lg(self):
        """
        Integration test for trex.crq_dose_mamm_bp_lg
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_bp_lg')
        finally:
            pass
        return

    def test_arq_dose_mamm_fp_sm(self):
        """
        Integration test for trex.arq_dose_mamm_fp_sm
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_fp_sm')
        finally:
            pass
        return

    def test_crq_dose_mamm_fp_sm(self):
        """
        Integration test for trex.crq_dose_mamm_fp_sm
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_fp_sm')
        finally:
            pass
        return

    def test_arq_dose_mamm_fp_md(self):
        """
        Integration test for trex.arq_dose_mamm_fp_md
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_fp_md')
        finally:
            pass
        return

    def test_crq_dose_mamm_fp_md(self):
        """
        Integration test for trex.crq_dose_mamm_fp_md
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_fp_md')
        finally:
            pass
        return

    def test_arq_dose_mamm_fp_lg(self):
        """
        Integration test for trex.arq_dose_mamm_fp_lg
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_fp_lg')
        finally:
            pass
        return

    def test_crq_dose_mamm_fp_lg(self):
        """
        Integration test for trex.crq_dose_mamm_fp_lg
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_fp_lg')
        finally:
            pass
        return

    def test_arq_dose_mamm_ar_sm(self):
        """
        Integration test for trex.arq_dose_mamm_ar_sm
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_ar_sm')
        finally:
            pass
        return

    def test_crq_dose_mamm_ar_sm(self):
        """
        Integration test for trex.crq_dose_mamm_ar_sm
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_ar_sm')
        finally:
            pass
        return

    def test_arq_dose_mamm_ar_md(self):
        """
        Integration test for trex.arq_dose_mamm_ar_md
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_ar_md')
        finally:
            pass
        return

    def test_crq_dose_mamm_ar_md(self):
        """
        Integration test for trex.crq_dose_mamm_ar_md
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_ar_md')
        finally:
            pass
        return

    def test_arq_dose_mamm_ar_lg(self):
        """
        Integration test for trex.arq_dose_mamm_ar_lg
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_ar_lg')
        finally:
            pass
        return

    def test_crq_dose_mamm_ar_lg(self):
        """
        Integration test for trex.crq_dose_mamm_ar_lg
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_ar_lg')
        finally:
            pass
        return

    def test_arq_dose_mamm_se_sm(self):
        """
        Integration test for trex.arq_dose_mamm_se_sm
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_se_sm')
        finally:
            pass
        return

    def test_crq_dose_mamm_se_sm(self):
        """
        Integration test for trex.crq_dose_mamm_se_sm
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_se_sm')
        finally:
            pass
        return

    def test_arq_dose_mamm_se_md(self):
        """
        Integration test for trex.arq_dose_mamm_se_md
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_se_md')
        finally:
            pass
        return

    def test_crq_dose_mamm_se_md(self):
        """
        Integration test for trex.crq_dose_mamm_se_md
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_se_md')
        finally:
            pass
        return

    def test_arq_dose_mamm_se_lg(self):
        """
        Integration test for trex.arq_dose_mamm_se_lg
        """
        try:
            self.blackbox_method_int('arq_dose_mamm_se_lg')
        finally:
            pass
        return

    def test_crq_dose_mamm_se_lg(self):
        """
        Integration test for trex.crq_dose_mamm_se_lg
        """
        try:
            self.blackbox_method_int('crq_dose_mamm_se_lg')
        finally:
            pass
        return

    def test_arq_diet_mamm_sg(self):
        """
        Integration test for trex.arq_diet_mamm_sg
        """
        try:
            self.blackbox_method_int('arq_diet_mamm_sg')
        finally:
            pass
        return

    def test_crq_diet_mamm_sg(self):
        """
        Integration test for trex.crq_diet_mamm_sg
        """
        try:
            self.blackbox_method_int('crq_diet_mamm_sg')
        finally:
            pass
        return

    def test_arq_diet_mamm_tg(self):
        """
        Integration test for trex.arq_diet_mamm_tg
        """
        try:
            self.blackbox_method_int('arq_diet_mamm_tg')
        finally:
            pass
        return

    def test_crq_diet_mamm_tg(self):
        """
        Integration test for trex.crq_diet_mamm_tg
        """
        try:
            self.blackbox_method_int('crq_diet_mamm_tg')
        finally:
            pass
        return

    def test_arq_diet_mamm_bp(self):
        """
        Integration test for trex.arq_diet_mamm_bp
        """
        try:
            self.blackbox_method_int('arq_diet_mamm_bp')
        finally:
            pass
        return

    def test_crq_diet_mamm_bp(self):
        """
        Integration test for trex.crq_diet_mamm_bp
        """
        try:
            self.blackbox_method_int('crq_diet_mamm_bp')
        finally:
            pass
        return

    def test_arq_diet_mamm_fp(self):
        """
        Integration test for trex.arq_diet_mamm_fp
        """
        try:
            self.blackbox_method_int('arq_diet_mamm_fp')
        finally:
            pass
        return

    def test_crq_diet_mamm_fp(self):
        """
        Integration test for trex.crq_diet_mamm_fp
        """
        try:
            self.blackbox_method_int('crq_diet_mamm_fp')
        finally:
            pass
        return

    def test_arq_diet_mamm_ar(self):
        """
        Integration test for trex.arq_diet_mamm_ar
        """
        try:
            self.blackbox_method_int('arq_diet_mamm_ar')
        finally:
            pass
        return

    def test_crq_diet_mamm_ar(self):
        """
        Integration test for trex.crq_diet_mamm_ar
        """
        try:
            self.blackbox_method_int('crq_diet_mamm_ar')
        finally:
            pass
        return

    def test_ld50_rg_bird_sm(self):
        """
        Integration test for trex.ld50_rg_bird_sm
        """
        try:
            self.blackbox_method_int('ld50_rg_bird_sm')
        finally:
            pass
        return

    def test_ld50_rl_bird_sm(self):
        """
        Integration test for trex.ld50_rl_bird_sm
        """
        try:
            self.blackbox_method_int('ld50_rl_bird_sm')
        finally:
            pass
        return

    def test_ld50_bg_bird_sm(self):
        """
        Integration test for trex.ld50_bg_bird_sm
        """
        try:
            self.blackbox_method_int('ld50_bg_bird_sm')
        finally:
            pass
        return

    def test_ld50_bl_bird_sm(self):
        """
        Integration test for trex.ld50_bl_bird_sm
        """
        try:
            self.blackbox_method_int('ld50_bl_bird_sm')
        finally:
            pass
        return

    def test_ld50_rg_mamm_sm(self):
        """
        Integration test for trex.ld50_rg_mamm_sm
        """
        try:
            self.blackbox_method_int('ld50_rg_mamm_sm')
        finally:
            pass
        return

    def test_ld50_rl_mamm_sm(self):
        """
        Integration test for trex.ld50_rl_mamm_sm
        """
        try:
            self.blackbox_method_int('ld50_rl_mamm_sm')
        finally:
            pass
        return

    def test_ld50_bg_mamm_sm(self):
        """
        Integration test for trex.ld50_bg_mamm_sm
        """
        try:
            self.blackbox_method_int('ld50_bg_mamm_sm')
        finally:
            pass
        return

    def test_ld50_bl_mamm_sm(self):
        """
        Integration test for trex.ld50_bl_mamm_sm
        """
        try:
            self.blackbox_method_int('ld50_bl_mamm_sm')
        finally:
            pass
        return

    def test_ld50_rg_bird_md(self):
        """
        Integration test for trex.ld50_rg_bird_md
        """
        try:
            self.blackbox_method_int('ld50_rg_bird_md')
        finally:
            pass
        return

    def test_ld50_rl_bird_md(self):
        """
        Integration test for trex.ld50_rl_bird_md
        """
        try:
            self.blackbox_method_int('ld50_rl_bird_md')
        finally:
            pass
        return

    def test_ld50_bg_bird_md(self):
        """
        Integration test for trex.ld50_bg_bird_md
        """
        try:
            self.blackbox_method_int('ld50_bg_bird_md')
        finally:
            pass
        return

    def test_ld50_bl_bird_md(self):
        """
        Integration test for trex.ld50_bl_bird_md
        """
        try:
            self.blackbox_method_int('ld50_bl_bird_md')
        finally:
            pass
        return

    def test_ld50_rg_mamm_md(self):
        """
        Integration test for trex.ld50_rg_mamm_md
        """
        try:
            self.blackbox_method_int('ld50_rg_mamm_md')
        finally:
            pass
        return

    def test_ld50_rl_mamm_md(self):
        """
        Integration test for trex.ld50_rl_mamm_md
        """
        try:
            self.blackbox_method_int('ld50_rl_mamm_md')
        finally:
            pass
        return

    def test_ld50_bg_mamm_md(self):
        """
        Integration test for trex.ld50_bg_mamm_md
        """
        try:
            self.blackbox_method_int('ld50_bg_mamm_md')
        finally:
            pass
        return

    def test_ld50_bl_mamm_md(self):
        """
        Integration test for trex.ld50_bl_mamm_md
        """
        try:
            self.blackbox_method_int('ld50_bl_mamm_md')
        finally:
            pass
        return

    def test_ld50_rg_bird_lg(self):
        """
        Integration test for trex.ld50_rg_bird_lg
        """
        try:
            self.blackbox_method_int('ld50_rg_bird_lg')
        finally:
            pass
        return

    def test_ld50_rl_bird_lg(self):
        """
        Integration test for trex.ld50_rl_bird_lg
        """
        try:
            self.blackbox_method_int('ld50_rl_bird_lg')
        finally:
            pass
        return

    def test_ld50_bg_bird_lg(self):
        """
        Integration test for trex.ld50_bg_bird_lg
        """
        try:
            self.blackbox_method_int('ld50_bg_bird_lg')
        finally:
            pass
        return

    def test_ld50_bl_bird_lg(self):
        """
        Integration test for trex.ld50_bl_bird_lg
        """
        try:
            self.blackbox_method_int('ld50_bl_bird_lg')
        finally:
            pass
        return

    def test_ld50_rg_mamm_lg(self):
        """
        Integration test for trex.ld50_rg_mamm_lg
        """
        try:
            self.blackbox_method_int('ld50_rg_mamm_lg')
        finally:
            pass
        return

    def test_ld50_rl_mamm_lg(self):
        """
        Integration test for trex.ld50_rl_mamm_lg
        """
        try:
            self.blackbox_method_int('ld50_rl_mamm_lg')
        finally:
            pass
        return

    def test_ld50_bg_mamm_lg(self):
        """
        Integration test for trex.ld50_bg_mamm_lg
        """
        try:
            self.blackbox_method_int('ld50_bg_mamm_lg')
        finally:
            pass
        return

    def test_ld50_bl_mamm_lg(self):
        """
        Integration test for trex.ld50_bl_mamm_lg
        """
        try:
            self.blackbox_method_int('ld50_bl_mamm_lg')
        finally:
            pass
        return

    def test_sc_bird_s(self):
        """
        Integration test for trex.sc_bird_s
        """
        try:
            self.blackbox_method_int('sc_bird_s')
        finally:
            pass
        return

    def test_sc_bird_m(self):
        """
        Integration test for trex.runsemi
        """
        try:
            self.blackbox_method_int('sc_bird_m')
        finally:
            pass
        return

    def test_sa_bird_1_s(self):
        """
        Integration test for trex.sa_bird_1_s
        """
        try:
            self.blackbox_method_int('sa_bird_1_s')
        finally:
            pass
        return

    def test_sa_bird_2_s(self):
        """
        Integration test for trex.sa_bird_2_s
        """
        try:
            self.blackbox_method_int('sa_bird_2_s')
        finally:
            pass
        return

    def test_sc_bird_s(self):
        """
        Integration test for trex.sc_bird_s
        """
        try:
            self.blackbox_method_int('sc_bird_s')
        finally:
            pass
        return

    def test_sa_mamm_1_s(self):
        """
        Integration test for trex.sa_mamm_1_s
        """
        try:
            self.blackbox_method_int('sa_mamm_1_s')
        finally:
            pass
        return

    def test_sa_mamm_2_s(self):
        """
        Integration test for trex.sa_mamm_2_s
        """
        try:
            self.blackbox_method_int('sa_mamm_2_s')
        finally:
            pass
        return

    def test_sc_mamm_s(self):
        """
        Integration test for trex.sc_mamm_s
        """
        try:
            self.blackbox_method_int('sc_mamm_s')
        finally:
            pass
        return

    def test_sa_bird_1_m(self):
        """
        Integration test for trex.sa_bird_1_m
        """
        try:
            self.blackbox_method_int('sa_bird_1_m')
        finally:
            pass
        return

    def test_sa_bird_2_m(self):
        """
        Integration test for trex.sa_bird_2_m
        """
        try:
            self.blackbox_method_int('sa_bird_2_m')
        finally:
            pass
        return

    def test_sc_bird_m(self):
        """
        Integration test for trex.sc_bird_m
        """
        try:
            self.blackbox_method_int('sc_bird_m')
        finally:
            pass
        return

    def test_sa_mamm_1_m(self):
        """
        Integration test for trex.sa_mamm_1_m
        """
        try:
            self.blackbox_method_int('sa_mamm_1_m')
        finally:
            pass
        return

    def test_sa_mamm_2_m(self):
        """
        Integration test for trex.sa_mamm_2_m
        """
        try:
            self.blackbox_method_int('sa_mamm_2_m')
        finally:
            pass
        return

    def test_sc_mamm_m(self):
        """
        Integration test for trex.sc_mamm_m
        """
        try:
            self.blackbox_method_int('sc_mamm_m')
        finally:
            pass
        return

    def test_sa_bird_1_l(self):
        """
        Integration test for trex.sa_bird_1_l
        """
        try:
            self.blackbox_method_int('sa_bird_1_l')
        finally:
            pass
        return

    def test_sa_bird_2_l(self):
        """
        Integration test for trex.sa_bird_2_l
        """
        try:
            self.blackbox_method_int('sa_bird_2_l')
        finally:
            pass
        return

    def test_sc_bird_l(self):
        """
        Integration test for trex.sc_bird_l
        """
        try:
            self.blackbox_method_int('sc_bird_l')
        finally:
            pass
        return

    def test_sa_mamm_1_l(self):
        """
        Integration test for trex.sa_mamm_1_l
        """
        try:
            self.blackbox_method_int('sa_mamm_1_l')
        finally:
            pass
        return

    def test_sa_mamm_2_l(self):
        """
        Integration test for trex.sa_mamm_2_l
        """
        try:
            self.blackbox_method_int('sa_mamm_2_l')
        finally:
            pass
        return

    def test_sc_mamm_l(self):
        """
        Integration test for trex.sc_mamm_l
        """
        try:
            self.blackbox_method_int('sc_mamm_l')
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
        npt.assert_allclose(result, expected, rtol, 0, True)

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