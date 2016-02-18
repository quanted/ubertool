from __future__ import division
#from ..base.uber_model import UberModel, ModelSharedInputs
import sys
sys.path.append('/Users/puruckertom/git/qed/ubertool_ecorest/ubertool/ubertool_models/base')
from uber_model import UberModel, ModelSharedInputs
#from ubertool.ubertool.base import uber_model #UberModel, ModelSharedInputs
import pandas as pd


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


class Earthworm(UberModel, EarthwormInputs, EarthwormOutputs):
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
        self.populate_inputs(self.pd_obj, self)
        self.pd_obj_out = self.populate_outputs(self)
        self.run_methods()
        self.fill_output_dataframe(self)

    # Begin model methods
    def run_methods(self):
        """ Execute all algorithm methods for model logic """
        try:
            self.earthworm_fugacity()
        except Exception, e:
            print str(e)

    def earthworm_fugacity(self):
        """
        most recent version of EFED equation circa 3-26-2013 is implemented in the formula below
        model runs documented in ubertool crosswalk use the EFED model in "earthworm models 3-26-13b.xlsx"
        """
        self.out_earthworm_fugacity = self.k_ow * self.l_f_e * (self.c_s / (self.k_d * self.p_s))
        return self.out_earthworm_fugacity
