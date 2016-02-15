from __future__ import division
from ..base.uber_model import UberModel, ModelSharedInputs
import pandas as pd
import numpy as np
from scipy.special import erfc


class IecInputs(ModelSharedInputs):
    """
    Input class for IEC.
    """

    def __init__(self):
        """Class representing the inputs for IEC"""
        super(IecInputs, self).__init__()
        self.dose_response = pd.Series([], dtype="float")
        self.lc50 = pd.Series([], dtype="float")
        self.threshold = pd.Series([], dtype="float")


class IecOutputs(object):
    """
    Output class for IEC.
    """

    def __init__(self):
        """Class representing the outputs for IEC"""
        super(IecOutputs, self).__init__()
        self.z_score_f_out = pd.Series(name="z_score_f_out")
        self.f8_f_out = pd.Series(name="f8_f_out")
        self.chance_f_out = pd.Series(name="chance_f_out")


class Iec(UberModel, IecInputs, IecOutputs):
    """
    IEC model for proportional population effect based on normal distribution.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the IEC model and containing all its methods"""
        super(Iec, self).__init__()
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

    def run_methods(self):
        """
        Execute all algorithm methods for model logic.
        :return:
        """
        try:
            self.z_score_f()
            self.f8_f()
            self.chance_f()
        except Exception, e:
            print str(e)

    def z_score_f(self):
        """
        Calculate z score.
        :return:
        """
        self.z_score_f_out = self.dose_response * (np.log10(self.lc50 * self.threshold) - np.log10(self.lc50))
        return self.z_score_f_out

    def f8_f(self):
        """
        Use error function to get probability based on z-score.
        :return:
        """
        self.f8_f_out = 0.5 * erfc(-self.z_score_f_out / np.sqrt(2))
        return self.f8_f_out

    def chance_f(self):
        """
        Chance calculation.
        :return:
        """
        self.chance_f_out = 1 / self.f8_f_out
        return self.chance_f_out
