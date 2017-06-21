import numpy as np
import os.path
import pandas as pd
import sys
#find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs

#print(sys.path)
#print(os.path)

class GompertzInputs(ModelSharedInputs):
    """
    Input class for Gompertz.
    """

    def __init__(self):
        """Class representing the inputs for Gompertz"""
        super(GompertzInputs, self).__init__()
        self.init_pop_size = pd.Series([], dtype="float")
        self.growth_rate = pd.Series([], dtype="float")
        self.time_steps = pd.Series([], dtype="float")
        self.K = pd.Series([], dtype="float")


class GompertzOutputs(object):
    """
    Output class for Gompertz.
    """

    def __init__(self):
        """Class representing the outputs for Gompertz"""
        super(GompertzOutputs, self).__init__()
        #dictionary of time, outputs
        self.out_pop_time_series = []


class Gompertz(UberModel, GompertzInputs, GompertzOutputs):
    """
    Gompertz model for population growth.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Gompertz model and containing all its methods"""
        super(Gompertz, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Run the model's methods to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj, self)
        self.pd_obj_out = self.populate_outputs(self)
        self.run_methods()
        self.fill_output_dataframe(self)

    # Begin model methods
    def run_methods(self):
        """ Execute all algorithm methods for model logic """
        try:
            # dictionaries of population time series
            self.batch_gompertz()
        except Exception as e:
            print(str(e))

    def gompertz_grow(self, idx):
        index_set = range(self.time_steps[idx] + 1)
        x = np.zeros(len(index_set))
        x[0] = self.init_pop_size[idx]
        for n in index_set[1:]:
            x[n] = self.K[idx] * np.exp((-np.log(self.K[idx]/self.init_pop_size[idx]) * np.exp(-self.growth_rate[idx]/100*n)))
        t = range(0, self.time_steps[idx])
        d = dict(zip(t, x))
        self.out_pop_time_series[idx].append(d)
        return

    def batch_gompertz(self):
        for idx in enumerate(self.init_pop_size):
            self.gompertz_grow(idx)
        return