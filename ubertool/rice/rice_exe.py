from __future__ import division
import pandas as pd
from base.uber_model import UberModel, ModelSharedInputs
from rice_functions import RiceFunctions

class RiceInputs(ModelSharedInputs):
    """
    Input class for Rice.
    """

    def __init__(self):
        """Class representing the inputs for Rice"""
        super(RiceInputs, self).__init__()
        self.mai = pd.Series([], dtype="float")
        self.dsed = pd.Series([], dtype="float")
        self.area = pd.Series([], dtype="float")
        self.pb = pd.Series([], dtype="float")
        self.dw = pd.Series([], dtype="float")
        self.osed = pd.Series([], dtype="float")
        self.kd = pd.Series([], dtype="float")


class RiceOutputs(object):
    """
    Output class for Rice.
    """

    def __init__(self):
        """Class representing the outputs for Rice"""
        super(RiceOutputs, self).__init__()
        self.out_msed = pd.Series(name="out_msed")
        self.out_vw = pd.Series(name="out_vw")
        self.out_mass_area = pd.Series(name="out_mass_area")
        self.out_cw = pd.Series(name="out_cw")


class Rice(UberModel, RiceInputs, RiceOutputs, RiceFunctions):
    """
    Estimate surface water exposure from the use of pesticide in rice paddies
    """
    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Terrplant model and containing all its methods"""
        super(Rice, self).__init__()
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

    def run_methods(self):
        try:
            """ Execute all algorithm methods for model logic """
            self.calc_msed()
            self.calc_vw()
            self.calc_mass_area()
            self.calc_cw()
        except TypeError:


