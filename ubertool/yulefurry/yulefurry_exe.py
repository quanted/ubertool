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

class YuleFurryInputs(ModelSharedInputs):
    """
    Input class for YuleFurry.
    """

    def __init__(self):
        """Class representing the inputs for YuleFurry"""
        super(YuleFurryInputs, self).__init__()
        self.init_pop_size = pd.Series([], dtype="float")
        self.birth_probability = pd.Series([], dtype="float")
        self.time_steps = pd.Series([], dtype="float")
        self.n_iterations = pd.Series([], dtype="float")


class YuleFurryOutputs(object):
    """
    Output class for YuleFurry.
    """

    def __init__(self):
        """Class representing the outputs for YuleFurry"""
        super(YuleFurryOutputs, self).__init__()
        # self.out_x = pd.Series(name="out_x")
        # self.out_x_mu = pd.Series(name="out_x_mu")
        #dictionary of time, outputs
        self.out_pop_time_series = []  #x
        self.out_x_mu = []


class YuleFurry(UberModel, YuleFurryInputs, YuleFurryOutputs):
    """
    YuleFurry model for population growth.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the YuleFurry model and containing all its methods"""
        super(YuleFurry, self).__init__()
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
            self.batch_yulefurry()
        except Exception as e:
            print(str(e))

    def exponential_growth(self):
        index_set = range(self.time_steps + 1)
        x = np.zeros(len(index_set))
        x[0] = self.init_pop_size
        for n in index_set[1:]:
            x[n] = self.init_pop_size * np.exp(self.growth_rate / 100 * n)
        self.out_pop_time_series = x.tolist()
        return self.out_pop_time_series

    def yule_furry_growth(self):
        #N_o, T, rho, Ite
        #init_pop_size, time_steps, birth_probability, n_iterations
        index_set = range(self.time_steps[idx] + 1)
        x = np.zeros((self.n_iterations[idx], len(index_set)))
        x_mu = np.zeros(len(index_set))
        x_mu[0] = self.init_pop_size[idx]
        self.birth_probability[idx] /= 100

        for i in range(0, n_iterations):
            #rho=1-np.exp(-rho)
            x[i][0] = self.init_pop_size[idx]
            n = 0
            while n < self.time_steps[idx]:
                x_mu[n+1] = (1 + self.birth_probability[idx]) * x_mu[n]
                if x[i][n] < 10000:
                    m = np.random.random(x[i][n])
                    n_birth = np.sum(m < self.birth_probability[idx])
                    x[i][n+1] = x[i][n] + n_birth
                else:
                    x[i][n+1] = (1 + self.birth_probability[idx]) * x[i][n]
                n += 1

        # self.out_x = x.tolist()
        # self.out_x_mu = x_mu.tolist()
        # return
        t = range(0, self.time_steps[idx])
        xmu = range(0, self.birth_probability[idx])
        d_t = dict(zip(t, x))
        d_xmu = dict(zip(xmu,x))
        self.out_pop_time_series[idx].append(d_t)  #x
        self.out_x_mu[idx].apend(d_xmu)
        return

    def batch_yulefurry(self):
        for idx in enumerate(self.init_pop_size):
            self.yule_furry_growth(idx)
        return