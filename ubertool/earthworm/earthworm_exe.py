from __future__ import division
import pandas as pd
import os.path
import sys

parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from base.uber_model import UberModel, ModelSharedInputs
from .earthworm_functions import EarthwormFunctions

class EarthwormInputs(ModelSharedInputs):
    """
    Input class for Earthworm.
    """

    def __init__(self):
        """Class representing the inputs for Earthworm"""
        super(EarthwormInputs, self).__init__()
        self.k_ow = pd.Series([], dtype="float")
        self.l_f_e = pd.Series([], dtype="float")
        self.c_s = pd.Series([], dtype="float")
        self.k_d = pd.Series([], dtype="float")
        self.p_s = pd.Series([], dtype="float")


class EarthwormOutputs(object):
    """
    Output class for Earthworm.
    """

    def __init__(self):
        """Class representing the outputs for Earthworm"""
        super(EarthwormOutputs, self).__init__()
        self.out_earthworm_fugacity = pd.Series(name="out_earthworm_fugacity")


class Earthworm(UberModel, EarthwormInputs, EarthwormOutputs, EarthwormFunctions):
    """
    Earthworm model for annelid soil ingestion.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Earthworm model and containing all its methods"""
        super(Earthworm, self).__init__()
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
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

    # Begin model methods
    def run_methods(self):
        """ Execute all algorithm methods for model logic """
        try:
            self.earthworm_fugacity()
        except Exception as e:
            pass

