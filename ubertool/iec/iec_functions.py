from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
import pandas as pd
from scipy.special import erfc

class IecFunctions(object):
    """
    Function class for Stir.
    """

    def __init__(self):
        """Class representing the functions for Sip"""
        super(IecFunctions, self).__init__()

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