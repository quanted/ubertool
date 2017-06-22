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

class FellerarleyInputs(ModelSharedInputs):
    """
    Input class for Fellerarley.
    #(N_o,K,rho,q,E,T)
    """

    def __init__(self):
        """Class representing the inputs for Fellerarley"""
        super(FellerarleyInputs, self).__init__()
        self.init_pop_size = pd.Series([], dtype="float")
        self.growth_rate = pd.Series([], dtype="float")
        self.time_steps = pd.Series([], dtype="float")
        self.death_rate = pd.Series([], dtype="float")
        self.iteration = pd.Series([], dtype="float")


class FellerarleyOutputs(object):
    """
    Output class for Fellerarley.
    """

    def __init__(self):
        """Class representing the outputs for Fellerarley"""
        super(FellerarleyOutputs, self).__init__()
        #dictionary of time, outputs
        self.out_pop_time_series = []


class Fellerarley(UberModel, FellerarleyInputs, FellerarleyOutputs):
    """
    Fellerarley model for population growth.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Fellerarley model and containing all its methods"""
        super(Fellerarley, self).__init__()
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
            self.batch_fellerarley()
        except Exception as e:
            print(str(e))

    def fellerarley_growth(self, idx):
        #T=self.time_steps
        #index_set = range(T+1)
        index_set = range(self.time_steps[idx] + 1)
        Ite=self.iteration
        x = np.zeros((Ite,len(index_set)))
        x_mu = np.zeros(len(index_set))
        x_mu[0]=self.init_pop_size[idx]
        rho=self.growth_rate[idx]/100
        beta=self.death_rate[idx]/100


        for i in range(0,Ite):
            x[i][0]=self.init_pop_size[idx]
            n=0
            while n<index_set:
                x_mu[n+1]=(1+rho-beta)*x_mu[n]

                if x[i][n]<10000:
                    m=np.random.random(x[i][n])
                    m1=np.random.random(x[i][n])
                    n_birth=np.sum(m<rho)
                    n_death=np.sum(m1<beta)
                    x[i][n+1]=x[i][n]+n_birth-n_death

                    if x[i][n+1]<0:
                        x[i][n+1]=0
                else:
                    x[i][n+1]=(1+rho-beta)*x[i][n]
                n=n+1
        t = range(0, self.time_steps[idx])
        d = dict(zip(t, x))
        self.out_pop_time_series[idx].append(d)
        return
        # x=x.tolist()
        # x_mu=x_mu.tolist()
        # return x, x_mu

    def batch_fellerarley(self):
        for idx in enumerate(self.init_pop_size):
            self.fellerarley_growth(idx)
        return