from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import os

# needs to be run whenever the qaqc csv is updated
csv_path = os.path.join(os.path.dirname(__file__),"therps_qaqc.csv")
csv_in = os.path.join(os.path.dirname(__file__),"therps_qaqc_in_transpose.csv")
csv_exp = os.path.join(os.path.dirname(__file__),"therps_qaqc_exp_transpose.csv")
import pandas as pd

#skiprows 0-indexed (supposedly, but does not seem to be the case)
#skipfooter- number of rows at bottom to skip
try:
    pd_obj_inputs = pd.read_csv(csv_path, index_col=0, header=None, skiprows=1, skipfooter=162, engine='python')
    pd_obj_inputs = pd_obj_inputs.drop(labels=pd_obj_inputs.columns[range(5)], axis=1)
    pd_obj_inputs.index.name = None
    pd_obj_inputs.columns -= 6
    pd_obj_inputs_transposed = pd_obj_inputs.transpose()
    print(pd_obj_inputs_transposed)
    pd_obj_inputs_transposed.to_csv(csv_in)

    pd_obj_exp_out = pd.read_csv(csv_path, index_col=0, header=None, skiprows=111, engine='python', na_values='')
    pd_obj_exp_out = pd_obj_exp_out.drop(labels=pd_obj_exp_out.columns[range(5)], axis=1)
    pd_obj_exp_out.index.name = None
    pd_obj_exp_out.columns -= 6
    pd_obj_exp_out_transposed = pd_obj_exp_out.transpose()
    print(pd_obj_exp_out_transposed)
    pd_obj_exp_out_transposed.to_csv(csv_exp)
except Exception as e:
    print (e.message)