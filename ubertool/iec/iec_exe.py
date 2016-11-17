from __future__ import division
import numpy as np
import pandas as pd
from scipy.special import erfc
from base.uber_model import UberModel, ModelSharedInputs


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
        self.out_z_score_f = pd.Series(name="out_z_score_f")
        self.out_f8_f = pd.Series(name="out_f8_f")
        self.out_chance_f = pd.Series(name="out_chance_f")


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
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

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
        self.out_z_score_f = self.dose_response * (np.log10(self.lc50 * self.threshold) - np.log10(self.lc50))
        return self.out_z_score_f

    def f8_f(self):
        """
        Use error function to get probability based on z-score.
        :return:
        """
        self.out_f8_f = 0.5 * erfc(-self.out_z_score_f / np.sqrt(2))
        return self.out_f8_f

    def chance_f(self):
        """
        Chance calculation.
        :return:
        """
        self.out_chance_f = 1 / self.out_f8_f
        return self.out_chance_f
