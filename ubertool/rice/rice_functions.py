from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
import pandas as pd

class RiceFunctions(object):
    """
    Function class for Stir.
    """

    def __init__(self):
        """Class representing the functions for Sip"""
        super(RiceFunctions, self).__init__()

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