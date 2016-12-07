from __future__ import division  #brings in Python 3.0 mixed type calculation rules

class EarthwormFunctions(object):
    """
    Function class for Stir.
    """

    def __init__(self):
        """Class representing the functions for Sip"""
        super(EarthwormFunctions, self).__init__()

    def earthworm_fugacity(self):
        """
        most recent version of EFED equation circa 3-26-2013 is implemented in the formula below
        model runs documented in ubertool crosswalk use the EFED model in "earthworm models 3-26-13b.xlsx"
        in this calculatoin Cw (concentration of pesticide in pore water) is assumed to be 0.0 mol/m3
        """
        self.out_earthworm_fugacity = self.k_ow * self.l_f_e * (self.c_s / (self.k_d * self.p_s))
        return self.out_earthworm_fugacity