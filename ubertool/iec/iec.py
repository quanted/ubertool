from __future__ import division
import logging
import pandas as pd
import numpy as np
from scipy.special import erfc


class Iec(object):
    """
    IEC model for proportional population effect based on normal distribution.
    """
    def __init__(self, run_type, pd_obj, pd_obj_exp):
        """
        Constructor for iec
        :param run_type:
        :param pd_obj:
        :param pd_obj_exp:
        :return:
        """
        # run_type can be single, batch or qaqc
        # 0 to run calculation, else it wont
        self.run_type = run_type
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        # Execute model methods if requested
        if self.run_type != "empty":
            self.execute_model()

    def execute_model(self):
        """
        Called by constructor to populate class and run methods.
        :return:
        """
        self.populate_input_properties()
        self.create_output_properties()
        self.run_methods()
        self.create_output_dataframe()
        # Callable from Bottle that returns JSON
        self.json = self.json(self.pd_obj, self.pd_obj_out, self.pd_obj_exp)

    def populate_input_properties(self):
        """
        Set all input properties for class
        Inputs: Assign object attribute variables from the input Pandas DataFrame
        :return:
        """
        self.dose_response = self.pd_obj['dose_response']
        self.lc50 = self.pd_obj['LC50']
        self.threshold = self.pd_obj['threshold']

    def create_output_properties(self):
        """
        Set all output properties for class
        Outputs: Assign object attribute variables to Pandas Series
        """
        self.z_score_f_out = pd.Series(name="z_score_f_out")
        self.f8_f_out = pd.Series(name="F8_f_out")
        self.chance_f_out = pd.Series(name="chance_f_out")

    def run_methods(self):
        """
        Execute all algorithm methods for model logic.
        :return:
        """
        try:
            self.z_score_f()
            self.f8_f()
            self.chance_f()
        finally:
            pass

    def create_output_dataframe(self):
        """
        Combine all output properties into numpy pandas dataframe
        Create DataFrame containing output value Series
        :return:
        """
        pd_obj_out = pd.DataFrame({
            "z_score_f_out": self.z_score_f_out,
            "F8_f_out": self.f8_f_out,
            "chance_f_out": self.chance_f_out
        })
        # create pandas properties for acceptance testing
        self.pd_obj_out = pd_obj_out

    def json(self, pd_obj, pd_obj_out, pd_obj_exp):
        """
        Convert DataFrames to JSON, returning a tuplehere
        of JSON strings (inputs, outputs, exp_out)
        """
        pd_obj_json = pd_obj.to_json()
        pd_obj_out_json = pd_obj_out.to_json()
        try:
            pd_obj_exp_json = pd_obj_exp.to_json()
        except Exception as e:
            # handle exception
            print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)
            pd_obj_exp_json = "{}"
        # Callable from Bottle that returns JSON
        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json

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
