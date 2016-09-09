from __future__ import division  #brings in Python 3.0 mixed type calculation rules
from functools import wraps
import logging
import numpy as np
import pandas as pd
import time

class KabamFunctions(object):
    """
    Function class for Kabam.
    """

    def __init__(self):
        """Class representing the functions for Kabam"""
        super(KabamFunctions, self).__init__()


# # ###Parameters & Calculations
#
# ## Chemical specific; dependent on concentrations of pesticide/organic carbon/particulate oc etc
# ## in water column/sediment pore-water
#
#     def phi_f(self):
#         """
#         Calculate Fraction of pesticide freely dissolved in water column (can be
#         absorbed via membrane diffusion)
#         Eq. A2
#         :return:
#         """
#         frac_diss = pd.Series([], dtype = 'float')
#
#         frac_diss = 1 / (1 + (self.conc_poc * 0.35 * self.log_kow) + (self.conc_doc * 0.08 * self.log_kow))
#         return frac_diss
#
#     def water_d(self):
#         """
#         concentration of freely dissolved pesticide in overlying water column
#         :return:
#         """
#         self.water_d = self.phi * self.water_column_eec * 1000000
#         return self.water_d
#
#     def c_soc_f(self):
#         """
#         Normalized pesticide concentration in sediment
#         Eq. A4a
#         :return:
#         """
#         self.c_soc = self.k_oc * self.pore_water_eec
#         return self.c_soc
#
#     def c_s_f(self):
#         """
#         Calculate concentration of chemical in solid portion of sediment
#         Eq. A4
#         :return:
#         """
#         self.c_s = self.c_soc * self.sediment_oc
#         return self.c_s
#
#     def sed_om_f(self):
#         """
#         Calculate organic matter fraction in sediment
# #?? don't see this calculation in model documentation; looks like it is same as c_soc_f
#         :return:
#         """
#         self.sed_om = self.c_s / self.sediment_oc
#         return self.sed_om
#
# ## Phytoplankton bioaccumulation/concentration calculations
#
#     def phytoplankton_k1_f(self):
#         """
#         Rate constant for uptake through respiratory area
#         Eq. A5.1  (unique to phytoplankton)
#         :return:
#         """
#         self.phytoplankton_k1 = 1 / (6.0e-5 + (5.5 / self.log_kow))
#         return self.phytoplankton_k1
#
#     def phytoplankton_k2_f(self):
#         """
#         Rate constant for elimination through the gills for phytoplankton
#         Eq. A6
#         :return:
#         """
#         self.phytoplankton_k2 = self.phytoplankton_k1 / self.k_bw_phytoplankton
#         return self.phytoplankton_k2
#
#     def k_bw_phytoplankton_f(self):
#         """
#         Phytoplankton water partition coefficient
#         Eq. A6a
#         :return:
#         """
#         self.k_bw_phytoplankton = (self.phytoplankton_lipid * self.log_kow) + (
#                                    self.phytoplankton_nlom * 0.35 * self.log_kow) + self.phytoplankton_water
#         return self.k_bw_phytoplankton
#
#     def cb_phytoplankton_f(self):
#         """
#         Phytoplankton pesticide tissue residue
#         Eq. A1
#         #because phytoplankton have no diet the (Kd * SUM(Pi * Cdi)) portion of Eq. A1 is not included here
#         :return:
#         """
#         self.cb_phytoplankton = (self.phytoplankton_k1 * (self.phytoplankton_mo * self.water_column_eec *
#                                  self.phi + self.phytoplankton_mp * self.pore_water_eec)) / (self.phytoplankton_k2 +
#                                  self.phytoplankton_ke + self.phytoplankton_kg + self.phytoplankton_km)
#         return self.cb_phytoplankton
#
#     def cbl_phytoplankton_f(self):
#         """
#         Lipid normalized pesticide residue in phytoplankton
#         used in Eqs. F4 (cbafl_phytoplankton_f) & F5 (cbsafl_phytoplankton_f)
#         :return:
#         """
#         self.cbl_phytoplankton = (1e6 * self.cb_phytoplankton) / self.phytoplankton_lipid
#         return self.cbl_phytoplankton
#
#     def cbr_phytoplankton_f(self):
#         """
#         Phytoplankton pesticide residue concentration originating from uptake through respiration
#         Cbr in Table A1  (this simply equals 'cb_phytoplankton_f' for phytoplankton because
#         phytoplankton_kd = 0)
#         """
#
#         self.cbr_phytoplankton = ((self.phytoplankton_k1 * (self.phytoplankton_mo * self.water_column_eec *
#                                    self.phi + self.phytoplankton_mp * self.pore_water_eec)) / (
#                                    self.phytoplankton_k2 + self.phytoplankton_ke + self.phytoplankton_kg +
#                                    self.phytoplankton_km))
#         return self.cbr_phytoplankton
#
#     def cbf_phytoplankton_f(self):
#         """
#         Phytoplankton total bioconcentration factor;
#         Eq. F1 with phytoplankton_ke, phytoplankton_kg, phytoplankton_kd, and phytoplankton_km = 0
#         :return:
#         """
#         # phytoplankton_kd = 0 #phytoplankton_kd is uptake rate constant for uptake
#         # through ingestion of food; phytoplanton has no diet thus _kd is always = 0
#
#         self.cbf_phytoplankton = ((self.phytoplankton_k1 * (self.phytoplankton_mo * self.water_column_eec *
#                                    self.phi + self.phytoplankton_mp * self.pore_water_eec)) / (
#                                    self.phytoplankton_k2 )) / self.water_column_eec
#         return self.cbf_phytoplankton
#
#     def cbfl_phytoplankton_f(self):
#         """
#         Phytoplankton lipid normalized total bioconcentration factor
#         Eq. F2
#         :return:
#         """
#
#         self.cbfl_phytoplankton = (self.cbf_phytoplankton / self.phytoplankton_lipid) / self.water_d
#
#         return self.cbfl_phytoplankton
#
#     def cbaf_phytoplankton_f(self):
#         """
#         Phytoplankton bioaccumulation factor
#         Eq. F3
#         :return:
#         """
#         self.cbaf_phytoplankton = (1e6 * self.cb_phytoplankton) / self.water_column_eec
#         return self.cbaf_phytoplankton
#
#     def cbafl_phytoplankton_f(self):
#         """
#         Phytoplankton lipid normalized bioaccumulation factor
#         Eq. F4
#         :return:
#         """
#         self.cbafl_phytoplankton = self.cbl_phytoplankton / self.water_d
#         return self.cbafl_phytoplankton
#
#     def cbsafl_phytoplankton_f(self):
#         """
#         Phytoplankton biota-sediment accumulation factor
#         Eq. F5
#         :return:
#         """
# #?? why no 1e6 factor here as in 'cbaf_phytoplankton_f' or vice versa
#         self.cbsafl_phytoplankton = self.cb_phytoplankton / self.sed_om
#         return self.cbsafl_phytoplankton

    def ventilation_rate(self, wet_wgt, do_conc):
        """
        Ventilation rate of aquatic animal
        unit: L/d
        Eq. A5.2b
        :param wet_wgt: wet weight of animal (kg)
        :param do_conc: concentration of dissolved oxygen (mg O2/L)
        :return:
        """

        vent_rate = pd.Series([], dtype = 'float')
        vent_rate = (1400.0 * ((wet_wgt ** 0.65) / do_conc))
        return vent_rate

    def pest_uptake_eff_gills(self, kow):
        """
        Pesticide uptake efficiency by gills
        unit: fraction
        Eq. A5.2a
        :param log kow: octanol-water partition coefficient ()
        :return:
        """

        pest_uptake_eff = pd.Series([], dtype = 'float')

        pest_uptake_eff = (1 / (1.85 + (155 / kow)))
        return self.ew_zoo
