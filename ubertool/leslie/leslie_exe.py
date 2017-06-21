import numpy as np
import os.path
import pandas as pd
import sys
#find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs

# print(sys.path)
# print(os.path)


class LeslieInputs(ModelSharedInputs):
    """
    Input class for Leslie.
    """

    def __init__(self):
        """Class representing the inputs for Leslie"""
        super(LeslieInputs, self).__init__()
        self.init_pop_size = pd.Series([], dtype="float")
        self.stages = pd.Series([], dtype="float")
        self.l_m = pd.Series([], dtype="float")
        self.time_steps = pd.Series([], dtype="float")


class LeslieOutputs(object):
    """
    Output class for Leslie.
    """

    def __init__(self):
        """Class representing the outputs for Leslie"""
        super(LeslieOutputs, self).__init__()
        self.out_pop_matrix = pd.Series(name="out_pop_matrix")
        self.out_fecundity = pd.Series(name="out_fecundity")
        self.out_growth = pd.Series(name="out_growth")
        self.out_survival = pd.Series(name="out_survival")
        self.out_eigdom = pd.Series(name="out_eigdom")
        self.out_eigleft = pd.Series(name="out_eigleft")
        self.out_eigright = pd.Series(name="out_eigright")
        self.out_sensitivity = pd.Series(name="out_sensitivity")
        self.out_elasticity = pd.Series(name="out_elasticity")


class Leslie(UberModel, LeslieInputs, LeslieOutputs):
    """
    Leslie model for population growth.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Leslie model and containing all its methods"""
        super(Leslie, self).__init__()
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
            self.extract_fec()
            self.extract_growth()
            self.extract_survival()
            self.eigen()
            self.sensitivity()
            self.elasticity()
            self.leslie_grow()
        except Exception as e:
            print(str(e))

    def extract_fec(self):
        """ Method to subset fecundity values from first row of Leslie/Lefkovitch matrix """
        self.out_fecundity = self.l_m[0, :]
        return self.out_fecundity

    def extract_growth(self):
        """ Method to extract growth probability from Leslie/Lefkovitch matrix"""
        self.out_growth = np.zeros(shape=(np.ndim(self.stages)-1, 0))
        for k in [0, np.ndim(self.stages)-1]:
            g = self.l_m[k+1, k]
            self.out_growth[k] = g
        return self.out_growth

    def extract_survival(self):
        """Method to extract survival probability from Leslie/Lefkovitch model"""
        self.out_survival = np.zeros(shape=(self.stages, 0))
        for k in [0, self.stages]:
            s = self.l_m[k, k]
            self.out_survival[k] = s
        return self.out_survival

    def eigen(self):
        """ Calc dominant eigvalue (expected pop growth @ SSD), right eigvec (Stable Stage Distribution), and
         left eigvec (reproductive value)"""
        eig_val, eig_vec = np.linalg.eig(self.l_m)
        self.out_eigdom = np.max(abs(eig_val))
        self.out_eigleft = eig_vec[0, :]
        self.out_eigright = eig_vec[1, :]
        return

    def sensitivity(self):
        """ Calculate sensitivity by taking partial derivatives of Leslie matrix"""
        for k in [0, np.ndim(self.stages)-1]:
            prod = np.zeros(self.stages)
            prod[k-1] = self.out_eigleft[k] * self.out_eigright[k]
            temp = np.sum(prod)
        self.out_sensitivity = (self.out_eigleft * self.out_eigright) / temp
        return self.out_sensitivity

    def elasticity(self):
        """ Calculate elasticity of Leslie matrix"""
        self.out_elasticity = self.out_sensitivity * (self.l_m/self.out_eigdom)
        return self.out_elasticity

    def leslie_grow(self):
        self.out_pop_matrix = np.zeros(shape=(self.stages, self.time_steps))
        self.out_pop_matrix[:, 0] = self.init_pop_size
        for i in range(1, self.time_steps):
            n = np.dot(self.l_m, self.out_pop_matrix[:, i-1])
            self.out_pop_matrix[:, i] = n.squeeze()
        return self.out_pop_matrix.tolist()
