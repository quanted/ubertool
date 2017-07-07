from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import pkgutil
import sys
from tabulate import tabulate
import unittest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

#find parent directory and import model methods
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
currentdir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.curdir))
inputdir = currentdir + '\\tests\\'
print(parentddir)
sys.path.append(parentddir)
sys.path.append(currentdir)
sys.path.append(inputdir)

#from base.uber_model import UberModel, ModelSharedInputs
#from .agdrift_functions import AgdriftFunctions
from agdrift_exe import Agdrift, AgdriftInputs, AgdriftOutputs

print(sys.path)

# load transposed qaqc data for inputs and expected outputs
# this works for both local nosetests and travis deploy
#input details
try:
    if __package__ is not None:
        csv_data = pkgutil.get_data(__package__, 'agdrift_qaqc_in_transpose.csv')
        data_inputs = StringIO(csv_data)
        pd_obj_inputs = pd.read_csv(data_inputs, index_col=0, engine='python')
    else:
        csv_transpose_path_in = "./tests/agdrift_qaqc_in_transpose.csv"
        #print(csv_transpose_path_in)
        pd_obj_inputs = pd.read_csv(csv_transpose_path_in, index_col=0, engine='python')

    pd_obj_exp = pd.DataFrame()

    agdrift_calc = Agdrift(pd_obj_inputs, pd_obj_exp)
    agdrift_calc.populate_inputs(pd_obj_inputs)

    #set initial parameter values and constants
    agdrift_calc.set_global_constants()

    # determine if scenario description data combine to form a valid scenario (i.e., one for which deposition data exists)
    agdrift_calc.out_sim_scenario_chk = pd.Series([], dtype='object')
    agdrift_calc.validate_sim_scenarios()

    #check if scenario numerical inputs are present and in appropriate range
    agdrift_calc.check_numerical_inputs()

finally:
    pass