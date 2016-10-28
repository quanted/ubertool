from __future__ import division
import pandas as pd
from base.uber_model import UberModel, ModelSharedInputs


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


class Rice(UberModel, RiceInputs, RiceOutputs):
    """
    Estimate surface water exposure from the use of pesticide in rice paddies
    """
#?? does the following __init__ override the __init__ located in the inherited classes
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
            print "Type Error: Your variables are not set correctly."

    def calc_msed(self):
        """
        The mass of the sediment at equilibrium with the water column
        Sediment depth (dsed) * Area of rice paddy (area) * Bulk density of sediment(mass/volume) pb
        """
        self.out_msed = self.dsed * self.area * self.pb
        return self.out_msed

    def calc_vw(self):
        """
        The volume of the water column plus pore water
        """
        self.out_vw = (self.dw * self.area) + (self.dsed * self.osed * self.area)
        return self.out_vw

    def calc_mass_area(self):
        """
        The pesticide mass per unit area
        """
        self.out_mass_area = (self.mai / self.area) * 10000
        return self.out_mass_area

    def calc_cw(self):
        """
        Water Concentration
        """
        self.out_cw = (self.out_mass_area / (self.dw + (self.dsed * (self.osed + (self.pb * self.kd * 1e-5))))) * 100
        return self.out_cw
