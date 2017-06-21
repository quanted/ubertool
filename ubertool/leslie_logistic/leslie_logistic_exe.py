import numpy as np
import os.path
import pandas as pd
import sys

# find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs


# print(sys.path)
# print(os.path)


class LeslieLogisticInputs(ModelSharedInputs):
    """
    Input class for LeslieLogistic.
    """

    def __init__(self):
        """Class representing the inputs for LeslieLogistic"""
        super(LeslieLogisticInputs, self).__init__()
        self.init_pop_size = pd.Series([], dtype="float")
        self.stages = pd.Series([], dtype="float")
        self.l_m = pd.Series([], dtype="float")
        self.time_steps = pd.Series([], dtype="float")
        self.init_conc = pd.Series([], dtype="float")
        self.half_life = pd.Series([], dtype="float")
        self.logistic_a = pd.Series([], dtype="float")
        self.logistic_b = pd.Series([], dtype="float")
        self.logistic_gamma = pd.Series([], dtype="float")


class LeslieLogisticOutputs(object):
    """
    Output class for LeslieLogistic.
    """

    def __init__(self):
        """Class representing the outputs for LeslieLogistic"""
        super(LeslieLogisticOutputs, self).__init__()
        self.out_pop_matrix = pd.Series(name="out_pop_matrix")


class LeslieLogistic(UberModel, LeslieLogisticInputs, LeslieLogisticOutputs):
    """
    LeslieLogistic model for population growth.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the LeslieLogistic model and containing all its methods"""
        super(LeslieLogistic, self).__init__()
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
            self.leslie_logistic_growth()
        except Exception as e:
            print(str(e))

    def leslie_growth(self):
        self.out_pop_matrix = np.zeros(shape=(self.stages, self.time_steps))
        self.out_pop_matrix[:, 0] = self.init_pop_size
        for i in range(1, self.time_steps):
            n = np.dot(self.l_m, self.out_pop_matrix[:, i - 1])
            self.out_pop_matrix[:, i] = n.squeeze()
        return self.out_pop_matrix.tolist()

    def leslie_logistic_growth(self):
        # S, l_m, n_o, T, HL, Con, a, b, c
        # stages, l_m, init_pop_size, time_steps, init_conc, half_life, logistic_a, logistic_b, logistic_gamma
        self.out_pop_matrix = np.zeros(shape=(self.stages, self.time_steps + 1), dtype=float)
        l_m_temp = np.zeros(shape=(self.stages, self.stages), dtype=float)
        total_pop = np.sum(self.init_pop_size)
        self.out_pop_matrix[:, 0] = self.init_pop_size
        for i in range(1, self.time_steps + 1):
            for j in range(0, self.stages):
                l_m_temp[0, j] = self.l_m[0, j] * np.exp(-self.logistic_gamma * total_pop)
                if j - 1 >= 0:
                    denom = 1 + np.exp(-self.logistic_a * np.log(self.init_conc * 0.5 ** (i/self.half_life)) - self.logistic_b)
                    m48 = 1/denom
                    l_m_temp[j, j - 1] = self.l_m[j, j - 1] * (1 - m48)
            n = np.dot(l_m_temp, self.out_pop_matrix[:, i - 1])
            #this total_pop might be too big
            total_pop = np.sum(n)
            self.out_pop_matrix[:, i] = n.squeeze()
        return
