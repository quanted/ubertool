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


###Parameters & Calculations

## Chemical specific; dependent on concentrations of pesticide/organic carbon/particulate oc etc
## in water column/sediment pore-water

    def phi_f(self):
        """
        Calculate Fraction of pesticide freely dissolved in water column (can be
        absorbed via membrane diffusion)
        Eq. A2
        :return:
        """
        frac_diss = pd.Series([], dtype = 'float')

        frac_diss = 1 / (1 + (self.conc_poc * 0.35 * self.log_kow) + (self.conc_doc * 0.08 * self.log_kow))
        return frac_diss

    def water_d(self):
        """
        concentration of freely dissolved pesticide in overlying water column
        :return:
        """
        self.water_d = self.phi * self.water_column_eec * 1000000
        return self.water_d

    def c_soc_f(self):
        """
        Normalized pesticide concentration in sediment
        Eq. A4a
        :return:
        """
        self.c_soc = self.k_oc * self.pore_water_eec
        return self.c_soc

    def c_s_f(self):
        """
        Calculate concentration of chemical in solid portion of sediment
        Eq. A4
        :return:
        """
        self.c_s = self.c_soc * self.sediment_oc
        return self.c_s

    def sed_om_f(self):
        """
        Calculate organic matter fraction in sediment
#?? don't see this calculation in model documentation; looks like it is same as c_soc_f
        :return:
        """
        self.sed_om = self.c_s / self.sediment_oc
        return self.sed_om

## Phytoplankton bioaccumulation/concentration calculations

    def phytoplankton_k1_f(self):
        """
        Rate constant for uptake through respiratory area
        Eq. A5.1  (unique to phytoplankton)
        :return:
        """
        self.phytoplankton_k1 = 1 / (6.0e-5 + (5.5 / self.log_kow))
        return self.phytoplankton_k1

    def phytoplankton_k2_f(self):
        """
        Rate constant for elimination through the gills for phytoplankton
        Eq. A6
        :return:
        """
        self.phytoplankton_k2 = self.phytoplankton_k1 / self.k_bw_phytoplankton
        return self.phytoplankton_k2

    def k_bw_phytoplankton_f(self):
        """
        Phytoplankton water partition coefficient
        Eq. A6a
        :return:
        """
        self.k_bw_phytoplankton = (self.phytoplankton_lipid * self.log_kow) + (
                                   self.phytoplankton_nlom * 0.35 * self.log_kow) + self.phytoplankton_water
        return self.k_bw_phytoplankton

    def cb_phytoplankton_f(self):
        """
        Phytoplankton pesticide tissue residue
        Eq. A1
        #because phytoplankton have no diet the (Kd * SUM(Pi * Cdi)) portion of Eq. A1 is not included here
        :return:
        """
        self.cb_phytoplankton = (self.phytoplankton_k1 * (self.phytoplankton_mo * self.water_column_eec *
                                 self.phi + self.phytoplankton_mp * self.pore_water_eec)) / (self.phytoplankton_k2 +
                                 self.phytoplankton_ke + self.phytoplankton_kg + self.phytoplankton_km)
        return self.cb_phytoplankton

    def cbl_phytoplankton_f(self):
        """
        Lipid normalized pesticide residue in phytoplankton
        used in Eqs. F4 (cbafl_phytoplankton_f) & F5 (cbsafl_phytoplankton_f)
        :return:
        """
        self.cbl_phytoplankton = (1e6 * self.cb_phytoplankton) / self.phytoplankton_lipid
        return self.cbl_phytoplankton

    def cbr_phytoplankton_f(self):
        """
        Phytoplankton pesticide residue concentration originating from uptake through respiration
        Cbr in Table A1  (this simply equals 'cb_phytoplankton_f' for phytoplankton because
        phytoplankton_kd = 0)
        """

        self.cbr_phytoplankton = ((self.phytoplankton_k1 * (self.phytoplankton_mo * self.water_column_eec *
                                   self.phi + self.phytoplankton_mp * self.pore_water_eec)) / (
                                   self.phytoplankton_k2 + self.phytoplankton_ke + self.phytoplankton_kg +
                                   self.phytoplankton_km))
        return self.cbr_phytoplankton

    def cbf_phytoplankton_f(self):
        """
        Phytoplankton total bioconcentration factor;
        Eq. F1 with phytoplankton_ke, phytoplankton_kg, phytoplankton_kd, and phytoplankton_km = 0
        :return:
        """
        # phytoplankton_kd = 0 #phytoplankton_kd is uptake rate constant for uptake
        # through ingestion of food; phytoplanton has no diet thus _kd is always = 0

        self.cbf_phytoplankton = ((self.phytoplankton_k1 * (self.phytoplankton_mo * self.water_column_eec *
                                   self.phi + self.phytoplankton_mp * self.pore_water_eec)) / (
                                   self.phytoplankton_k2 )) / self.water_column_eec
        return self.cbf_phytoplankton

    def cbfl_phytoplankton_f(self):
        """
        Phytoplankton lipid normalized total bioconcentration factor
        Eq. F2
        :return:
        """

        self.cbfl_phytoplankton = (self.cbf_phytoplankton / self.phytoplankton_lipid) / self.water_d

        return self.cbfl_phytoplankton

    def cbaf_phytoplankton_f(self):
        """
        Phytoplankton bioaccumulation factor
        Eq. F3
        :return:
        """
        self.cbaf_phytoplankton = (1e6 * self.cb_phytoplankton) / self.water_column_eec
        return self.cbaf_phytoplankton

    def cbafl_phytoplankton_f(self):
        """
        Phytoplankton lipid normalized bioaccumulation factor
        Eq. F4
        :return:
        """
        self.cbafl_phytoplankton = self.cbl_phytoplankton / self.water_d
        return self.cbafl_phytoplankton

    def cbsafl_phytoplankton_f(self):
        """
        Phytoplankton biota-sediment accumulation factor
        Eq. F5
        :return:
        """
        self.cbsafl_phytoplankton = self.cbl_phytoplankton / self.sed_om
        return self.cbsafl_phytoplankton

    ##################zooplankton
    def gv_zoo_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_zoo = (1400 * (self.zoo_wb ** 0.65)) / self.conc_do
        return self.gv_zoo

    def ew_zoo_f(self):
        """
        Rate constant for elimination through the gills for zooplankton
        :return:
        """
        self.ew_zoo = (1 / (1.85 + (155 / self.log_kow)))
        return self.ew_zoo

    def zoo_k1_f(self):
        """
        Uptake rate constant through respiratory area for phytoplankton
        :return:
        """
        self.zoo_k1 = self.ew_zoo * self.gv_zoo / self.zoo_wb
        return self.zoo_k1

    def k_bw_zoo_f(self):
        """
        Zooplankton water partition coefficient
        :return:
        """
        self.k_bw_zoo = (self.zoo_lipid * self.log_kow) + (self.zoo_nlom * 0.035 * self.log_kow) + self.zoo_water
        return self.k_bw_zoo

    def zoo_k2_f(self):
        """
        Elimination rate constant through the gills for zooplankton
        :return:
        """
        self.zoo_k2 = self.zoo_k1 / self.k_bw_zoo
        return self.zoo_k2

    def ed_zoo_f(self):
        """
        Zooplankton dietary pesticide transfer efficiency
        :return:
        """
        self.ed_zoo = 1 / ((.0000003) * self.log_kow + 2.0)
        return self.ed_zoo

    def gd_zoo_f(self):
        """
        Zooplankton feeding rate
        :return:
        """
        self.gd_zoo = 0.022 * self.zoo_wb ** 0.85 * math.exp(0.06 * self.water_temp)
        return self.gd_zoo

    def zoo_kd_f(self):
        """
        Zooplankton rate constant pesticide uptake by food ingestion
        :return:
        """
        self.zoo_kd = self.ed_zoo * (self.gd_zoo / self.zoo_wb)
        return self.zoo_kd

    def kg_zoo_f(self):
        """
        Zooplankton growth rate constant
        :return:
        """
        if self.water_temp < 17.5:
            self.kg_zoo = 0.0005 * self.zoo_wb ** -0.2
        else:
            self.kg_zoo = 0.00251 * self.zoo_wb ** -0.2
        return self.kg_zoo

    def v_ld_zoo_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_zoo = self.zoo_diet_sediment * self.sediment_lipid + self.zoo_diet_phyto * self.phytoplankton_lipid
        return self.v_ld_zoo

    def v_nd_zoo_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_zoo = self.zoo_diet_sediment * self.sediment_nlom + self.zoo_diet_phyto * self.phytoplankton_nlom
        return self.v_nd_zoo

    def v_wd_zoo_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_zoo = self.zoo_diet_sediment * self.sediment_water + self.zoo_diet_phyto * self.phytoplankton_water
        return self.v_wd_zoo

    def gf_zoo_f(self):
        """
        Egestion rate of fecal matter
        :return:
        """
        self.gf_zoo = (((1 - .72) * self.v_ld_zoo) + ((1 - .72) * self.v_nd_zoo) + (
            (1 - .25) * self.v_wd_zoo)) * self.gd_zoo
        # rr=self.zoo_diet_phyto
        # if rr==0:
        #   rr==0.00000001
        # return rr
        return self.gf_zoo

    def vlg_zoo_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_zoo = (1 - 0.72) * self.v_ld_zoo * self.gd_zoo / self.gf_zoo
        return self.vlg_zoo

    def vng_zoo_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_zoo = (1 - 0.72) * self.v_nd_zoo * self.gd_zoo / self.gf_zoo
        return self.vng_zoo

    def vwg_zoo_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_zoo = (1 - 0.25) * self.v_wd_zoo * self.gd_zoo / self.gf_zoo
        return self.vwg_zoo

    def kgb_zoo_f(self):
        """
        Partition coefficient of the pesticide between the gastrointenstinal track and the organism
        :return:
        """
        self.kgb_zoo = (self.vlg_zoo * self.log_kow + self.vng_zoo * 0.035 * self.log_kow + self.vwg_zoo) / (
            self.zoo_lipid * self.log_kow + self.zoo_nlom * 0.035 * self.log_kow + self.zoo_water)
        return self.kgb_zoo

    def zoo_ke_f(self):
        """
        Dietary elimination rate constant
        :return:
        """
        self.zoo_ke = self.gf_zoo * self.ed_zoo * self.kgb_zoo / self.zoo_wb
        #   self.zoo_ke = self.zoo_diet_phyto
        return self.zoo_ke

    def diet_zoo_f(self):
        """
        Diet fraction
        :return:
        """
        self.diet_zoo = self.c_s * self.zoo_diet_sediment + self.cb_phytoplankton * self.zoo_diet_phyto
        return self.diet_zoo

    def cb_zoo_f(self):
        """
        Zooplankton pesticide tissue residue
        :return:
        """
        self.cb_zoo = (self.zoo_k1 * (1.0 * self.phi * self.water_column_eec + 0 * self.pore_water_eec) + self.zoo_kd * self.diet_zoo) / (
            self.zoo_k2 + self.zoo_ke + self.kg_zoo + 0)
        # print "cb_zoo =", self.cb_zoo
        return self.cb_zoo

    def cbl_zoo_f(self):
        """
        Zooplankton pesticide tissue residue lipid normalized
        :return:
        """
        self.cbl_zoo = (1e6 * self.cb_zoo) / self.zoo_lipid
        return self.cbl_zoo

    def cbd_zoo_f(self):
        """
        Zooplankton pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_zoo = (0 * (1.0) * self.phi * self.water_column_eec + (0 * self.pore_water_eec) + (self.zoo_kd * (self.diet_zoo))) / (
            self.zoo_k2 + self.zoo_ke + self.kg_zoo + 0)
        # print "cbd_zoo =", self.cbd_zoo
        return self.cbd_zoo

    def cbr_zoo_f(self):
        """
        Zooplankton pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_zoo = (self.zoo_k1 * (1. * self.phi * self.water_column_eec + 0 * self.pore_water_eec) + (0 * self.diet_zoo)) / (
            self.zoo_k2 + self.zoo_ke + self.kg_zoo + 0)
        return self.cbr_zoo

    def cbf_zoo_f(self):
        """
        Zooplankton total bioconcentration factor
        :return:
        """
        self.zoo_kd = 0
        self.zoo_ke = 0
        #    zoo_km = 0 zoo_km is always = 0
        self.kg_zoo = 0
        self.cbf_zoo = ((self.zoo_k1 * (1. * self.phi * self.water_column_eec + 0 * self.pore_water_eec) + self.zoo_kd * self.diet_zoo) / (
            self.zoo_k2 + self.zoo_ke + self.kg_zoo + 0)) / self.water_column_eec
        return self.cbf_zoo

    def cbfl_zoo_f(self):
        """
        Zooplankton lipid normalized total bioconcentration factor
        :return:
        """
        self.zoo_kd = 0
        self.zoo_ke = 0
        #    zoo_km = 0 zoo_km is always = 0
        self.kg_zoo = 0
        self.cbfl_zoo = (
                            (self.zoo_k1 * (
                                1.0 * self.phi * self.water_column_eec + 0 * self.pore_water_eec) + self.zoo_kd * self.diet_zoo) / (
                                self.zoo_k2 + self.zoo_ke + self.kg_zoo + 0)) / self.zoo_lipid / (self.water_column_eec * self.phi)
        return self.cbfl_zoo

    def cbaf_zoo_f(self):
        """
        Zooplankton bioaccumulation factor
        :return:
        """
        self.cbaf_zoo = (1e6 * self.cb_zoo) / self.water_column_eec
        return self.cbaf_zoo

    def cbafl_zoo_f(self):
        """
        Zooplankton lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_zoo = self.cbl_zoo / self.water_d
        return self.cbafl_zoo

    def cbsafl_zoo_f(self):
        """
        Zooplankton bioaccumulation
        :return:
        """
        self.cbsafl_zoo = (self.cb_zoo / self.zoo_lipid) / self.sed_om
        return self.cbsafl_zoo

    def bmf_zoo_f(self):
        """
        Zooplankton biomagnification factor
        :return:
        """
        self.bmf_zoo = (self.cb_zoo / self.zoo_lipid) / (
            self.zoo_diet_phyto * self.cb_phytoplankton / self.phytoplankton_lipid)
        return self.bmf_zoo

    ################################ benthic invertebrates
    ############################################################
    def gv_beninv_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_beninv = (1400 * ((self.beninv_wb ** 0.65) / self.conc_do))
        return self.gv_beninv

    def ew_beninv_f(self):
        """
        Rate constant for elimination through the gills for benthic invertebrates
        :return:
        """
        self.ew_beninv = (1 / (1.85 + (155 / self.log_kow)))
        return self.ew_beninv

    def beninv_k1_f(self):
        """
        Uptake rate constant through respiratory area for benthic invertebrates
        :return:
        """
        self.beninv_k1 = ((self.ew_beninv * self.gv_beninv) / self.beninv_wb)
        return self.beninv_k1

    def k_bw_beninv_f(self):
        """
        Benthic invertebrate water partition coefficient
        :return:
        """
        self.k_bw_beninv = (self.beninv_lipid * self.log_kow) + (self.beninv_nlom * 0.035 * self.log_kow) + self.beninv_water
        return self.k_bw_beninv

    def beninv_k2_f(self):
        """
        Elimination rate constant through the gills for zooplankton
        :return:
        """
        self.beninv_k2 = self.beninv_k1 / self.k_bw_beninv
        return self.beninv_k2

    def ed_beninv_f(self):
        """
        Zoo plankton dietary pesticide transfer efficiency
        :return:
        """
        self.ed_beninv = 1 / (.0000003 * self.log_kow + 2.0)
        return self.ed_beninv

    def gd_beninv_f(self):
        """
        Zooplankton feeding rate
        :return:
        """
        self.gd_beninv = 0.022 * self.beninv_wb ** 0.85 * math.exp(0.06 * self.water_temp)
        return self.gd_beninv

    def beninv_kd_f(self):
        """
        Zooplankton rate constant pesticide uptake by food ingestion
        :return:
        """
        self.beninv_kd = self.ed_beninv * (self.gd_beninv / self.beninv_wb)
        return self.beninv_kd

    def kg_beninv_f(self):
        """
        Benthic invertebrate growth rate constant
        :return:
        """
        if self.water_temp < 17.5:
            self.kg_beninv = 0.0005 * self.beninv_wb ** -0.2
        else:
            self.kg_beninv = 0.00251 * self.beninv_wb ** -0.2
        return self.kg_beninv

    def v_ld_beninv_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_beninv = self.beninv_diet_sediment * self.sediment_lipid + self.beninv_diet_phytoplankton * self.phytoplankton_lipid + self.beninv_diet_zooplankton * self.zoo_lipid
        return self.v_ld_beninv

    def v_nd_beninv_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_beninv = self.beninv_diet_sediment * self.sediment_nlom + self.beninv_diet_phytoplankton * self.phytoplankton_nlom + self.beninv_diet_zooplankton * self.zoo_nlom
        return self.v_nd_beninv

    def v_wd_beninv_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_beninv = self.beninv_diet_sediment * self.sediment_water + self.beninv_diet_phytoplankton * self.phytoplankton_water + self.beninv_diet_zooplankton * self.zoo_water
        return self.v_wd_beninv

    def gf_beninv_f(self):
        """
        Egestion rate of fecal matter
        :return:
        """
        self.gf_beninv = ((1 - 0.75) * self.v_ld_beninv + (1 - 0.75) * self.v_nd_beninv + (
            1 - 0.25) * self.v_wd_beninv) * self.gd_beninv
        return self.gf_beninv

    def vlg_beninv_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_beninv = (1 - 0.75) * self.v_ld_beninv * self.gd_beninv / self.gf_beninv
        return self.vlg_beninv

    def vng_beninv_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_beninv = (1 - 0.75) * self.v_nd_beninv * self.gd_beninv / self.gf_beninv
        return self.vng_beninv

    def vwg_beninv_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_beninv = (1 - 0.25) * self.v_wd_beninv * self.gd_beninv / self.gf_beninv
        return self.vwg_beninv
        # partition coefficient of the pesticide between the gastrointenstinal track and the organism

    def kgb_beninv_f(self):
        """
        Kgb ben inverts
        :return:
        """
        self.kgb_beninv = (self.vlg_beninv * self.log_kow + self.vng_beninv * 0.035 * self.log_kow + self.vwg_beninv) / (
            self.beninv_lipid * self.log_kow + self.beninv_nlom * 0.035 * self.log_kow + self.beninv_water)
        return self.kgb_beninv

    def beninv_ke_f(self):
        """
        Dietary elimination rate constant
        :return:
        """
        self.beninv_ke = self.gf_beninv * self.ed_beninv * (self.kgb_beninv / self.beninv_wb)
        return self.beninv_ke

    def diet_beninv_f(self):
        """
        Diet fraction benthic inverts
        :return:
        """
        self.diet_beninv = self.c_s * self.beninv_diet_sediment + self.cb_phytoplankton * self.beninv_diet_phytoplankton + self.cb_zoo * self.beninv_diet_zooplankton
        return self.diet_beninv

    def cb_beninv_f(self):
        """
        Benthic invertebrates pesticide tissue residue
        :return:
        """
        self.cb_beninv = (self.beninv_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.beninv_kd * self.diet_beninv) / (
                             self.beninv_k2 + self.beninv_ke + self.kg_beninv + 0)
        return self.cb_beninv

    def cbl_beninv_f(self):
        """
        Benthic invertebrates
        :return:
        """
        self.cbl_beninv = (1e6 * self.cb_beninv) / self.beninv_lipid
        return self.cbl_beninv

    def cbd_beninv_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_beninv = (0 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.beninv_kd * self.diet_beninv) / (
                              self.beninv_k2 + self.beninv_ke + self.kg_beninv + 0)
        return self.cbd_beninv

    def cbr_beninv_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_beninv = (self.beninv_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + 0 * self.diet_beninv) / (
                              self.beninv_k2 + self.beninv_ke + self.kg_beninv + 0)
        return self.cbr_beninv

    def cbf_beninv_f(self):
        """
        Benthic invertebrate total bioconcentration factor
        :return:
        """
        self.beninv_kd = 0
        self.beninv_ke = 0
        # beninv_km = 0    is always 0
        self.kg_beninv = 0
        self.cbf_beninv = ((self.beninv_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.beninv_kd * self.diet_beninv) / (
                               self.beninv_k2 + self.beninv_ke + self.kg_beninv + 0)) / self.water_column_eec
        return self.cbf_beninv

    def cbfl_beninv_f(self):
        """
        Benthic invertebrate lipid normalized total bioconcentration factor
        :return:
        """
        self.beninv_kd = 0
        self.beninv_ke = 0
        # beninv_km = 0    is always 0
        self.kg_beninv = 0
        self.cbfl_beninv = (((self.beninv_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.beninv_kd * self.diet_beninv)) / self.beninv_lipid / (
                                self.beninv_k2 + self.beninv_ke + self.kg_beninv + 0)) / (self.water_column_eec * self.phi)
        return self.cbfl_beninv

    def cbaf_beninv_f(self):
        """
        Benthic invertebrates bioaccumulation factor
        :return:
        """
        self.cbaf_beninv = (1e6 * self.cb_beninv) / self.water_column_eec
        return self.cbaf_beninv

    def cbafl_beninv_f(self):
        """
        Benthic invertebrate lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_beninv = self.cbl_beninv / self.water_d
        return self.cbafl_beninv

    def cbsafl_beninv_f(self):
        """
        Benthic inverts
        :return:
        """
        self.cbsafl_beninv = (self.cb_beninv / self.beninv_lipid) / self.sed_om
        return self.cbsafl_beninv

    def bmf_beninv_f(self):
        """
        Benthic invertebrates biomagnification factor
        :return:
        """
        self.bmf_beninv = (self.cb_beninv / self.beninv_lipid) / (
            (self.beninv_diet_zooplankton * self.cb_zoo / self.zoo_lipid) + (
                self.beninv_diet_phytoplankton * self.cb_phytoplankton / self.phytoplankton_lipid))
        return self.bmf_beninv

    #####################################################
    ###### filter feeders
    ################################################
    def gv_ff_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_ff = (1400.0 * ((self.filterfeeders_wb ** 0.65) / self.conc_do))
        return self.gv_ff

    def ew_ff_f(self):
        """
        Rate constant for elimination through the gills for filter feeders
        :return:
        """
        self.ew_ff = (1.0 / (1.85 + (155.0 / self.log_kow)))
        return self.ew_ff

    def filterfeeders_k1_f(self):
        """
        Uptake rate constant through respiratory area for filter feeders
        :return:
        """
        self.filterfeeders_k1 = ((self.ew_ff * self.gv_ff) / self.filterfeeders_wb)
        return self.filterfeeders_k1

    def k_bw_ff_f(self):
        """
        Filter feeder water partition coefficient
        :return:
        """
        self.k_bw_ff = (self.filterfeeders_lipid * self.log_kow) + (self.filterfeeders_nlom * 0.035 * self.log_kow) + self.filterfeeders_water
        return self.k_bw_ff

    def filterfeeders_k2_f(self):
        """
        Elimination rate constant through the gills for filter feeders
        :return:
        """
        self.filterfeeders_k2 = self.filterfeeders_k1 / self.k_bw_ff
        return self.filterfeeders_k2

    def ed_ff_f(self):
        """
        Filter feeder dietary pesticide transfer efficiency
        :return:
        """
        self.ed_ff = 1 / (.0000003 * self.log_kow + 2.0)
        return self.ed_ff

    def gd_ff_f(self):
        """
        Filter feeder feeding rate
        :return:
        """
        self.gd_ff = self.gv_ff * self.conc_ss * 1
        return self.gd_ff

    def filterfeeders_kd_f(self):
        """
        Filter feeder rate constant pesticide uptake by food ingestion
        :return:
        """
        self.filterfeeders_kd = self.ed_ff * (self.gd_ff / self.filterfeeders_wb)
        return self.filterfeeders_kd

    def kg_ff_f(self):
        """
        Filter feeder growth rate constant
        :return:
        """
        if self.water_temp < 17.5:
            self.kg_ff = 0.0005 * self.filterfeeders_wb ** -0.2
        else:
            self.kg_ff = 0.00251 * self.filterfeeders_wb ** -0.2
        return self.kg_ff

    def v_ld_ff_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_ff = self.filterfeeders_diet_sediment * self.sediment_lipid + self.filterfeeders_diet_phytoplankton * self.phytoplankton_lipid + self.filterfeeders_diet_zooplankton * self.zoo_lipid
        return self.v_ld_ff

    def v_nd_ff_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_ff = self.filterfeeders_diet_sediment * self.sediment_nlom + self.filterfeeders_diet_phytoplankton * self.phytoplankton_nlom + self.filterfeeders_diet_zooplankton * self.zoo_nlom
        return self.v_nd_ff

    def v_wd_ff_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_ff = self.filterfeeders_diet_sediment * self.sediment_water + self.filterfeeders_diet_phytoplankton * self.phytoplankton_water + self.filterfeeders_diet_zooplankton * self.zoo_water
        return self.v_wd_ff

    def gf_ff_f(self):
        """
        Gf ff
        :return:
        """
        self.gf_ff = ((1 - 0.75) * self.v_ld_ff + (1 - 0.75) * self.v_nd_ff + (1 - 0.25) * self.v_wd_ff) * self.gd_ff
        return self.gf_ff

    def vlg_ff_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_ff = (1 - 0.75) * self.v_ld_ff * self.gd_ff / self.gf_ff
        return self.vlg_ff

    def vng_ff_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_ff = (1 - 0.75) * self.v_nd_ff * self.gd_ff / self.gf_ff
        return self.vng_ff

    def vwg_ff_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_ff = (1 - 0.25) * self.v_wd_ff * self.gd_ff / self.gf_ff
        return self.vwg_ff

    def kgb_ff_f(self):
        """
        Kgb ff
        :return:
        """
        self.kgb_ff = (self.vlg_ff * self.log_kow + self.vng_ff * 0.035 * self.log_kow + self.vwg_ff) / (
            self.filterfeeders_lipid * self.log_kow + self.filterfeeders_nlom * 0.035 * self.log_kow + self.filterfeeders_water)
        return self.kgb_ff

    def filterfeeders_ke_f(self):
        """
        Ke ff
        :return:
        """
        self.filterfeeders_ke = (self.gf_ff * self.ed_ff * self.kgb_ff) / self.filterfeeders_wb
        return self.filterfeeders_ke

    def diet_ff_f(self):
        """
        Diet filter feeders
        :return:
        """
        self.diet_ff = self.c_s * self.filterfeeders_diet_sediment + self.cb_phytoplankton * self.filterfeeders_diet_phytoplankton + self.cb_zoo * self.filterfeeders_diet_zooplankton + self.cb_beninv * self.filterfeeders_diet_benthic_invertebrates
        return self.diet_ff

    def cb_ff_f(self):
        """
        Benthic invertebrates pesticide tissue residue
        :return:
        """
        self.cb_ff = (self.filterfeeders_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.filterfeeders_kd * self.diet_ff) / (
            self.filterfeeders_k2 + self.filterfeeders_ke + self.kg_ff + 0)
        return self.cb_ff

    def cbl_ff_f(self):
        """
        Filter feeders
        :return:
        """
        self.cbl_ff = (1e6 * self.cb_ff) / self.filterfeeders_lipid
        return self.cbl_ff

    def cbd_ff_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_ff = (0 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.filterfeeders_kd * self.diet_ff) / (
            self.filterfeeders_k2 + self.filterfeeders_ke + self.kg_ff + 0)
        return self.cbd_ff

    def cbr_ff_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.filterfeeders_kd = 0
        self.cbr_ff = (self.filterfeeders_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + 0 * self.diet_ff) / (
            self.filterfeeders_k2 + self.filterfeeders_ke + self.kg_ff + 0)
        return self.cbr_ff

    def cbf_ff_f(self):
        """
        Filter feeder total bioconcentration factor
        :return:
        """
        self.filterfeeders_kd = 0
        self.filterfeeders_ke = 0
        #  filterfeeders_km = 0  is always = 0
        self.kg_ff = 0
        self.cbf_ff = ((self.filterfeeders_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.filterfeeders_kd * self.diet_ff) / (
            self.filterfeeders_k2 + self.filterfeeders_ke + self.kg_ff + 0)) / self.water_column_eec
        return self.cbf_ff

    def cbfl_ff_f(self):
        """
        Filter feeder lipid normalized bioconcentration factor
        :return:
        """
        self.filterfeeders_kd = 0
        self.filterfeeders_ke = 0
        #  filterfeeders_km = 0  is always = 0
        self.kg_ff = 0
        self.cbfl_ff = (((self.filterfeeders_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.filterfeeders_kd * self.diet_ff) / (
                             self.filterfeeders_k2 + self.filterfeeders_ke + self.kg_ff + 0))) / self.filterfeeders_lipid / (self.water_column_eec * self.phi)
        return self.cbfl_ff

    def cbaf_ff_f(self):
        """
        Filter feeder bioaccumulation factor
        :return:
        """
        self.cbaf_ff = (1e6 * self.cb_ff) / self.water_column_eec
        return self.cbaf_ff

    def cbafl_ff_f(self):
        """
        Filter feeder lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_ff = self.cbl_ff / self.water_d
        return self.cbafl_ff

    def cbsafl_ff_f(self):
        """
        Filter feeder biota-sediment bioaccumulation factor
        :return:
        """
        self.cbsafl_ff = (self.cb_ff / self.filterfeeders_lipid) / self.sed_om
        return self.cbsafl_ff

    def bmf_ff_f(self):
        """
        Filter feeder biomagnification factor
        :return:
        """
        self.bmf_ff = (self.cb_ff / self.filterfeeders_lipid) / (
            (self.filterfeeders_diet_benthic_invertebrates * self.cb_beninv / self.beninv_lipid) + (
                self.filterfeeders_diet_zooplankton * self.cb_zoo / self.zoo_lipid) + (
                self.filterfeeders_diet_phytoplankton * self.cb_phytoplankton / self.phytoplankton_lipid))
        return self.bmf_ff

    #########################################################################
    ############# small fish
    def gv_sf_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_sf = (1400.0 * ((self.sfish_wb ** 0.65) / self.conc_do))
        return self.gv_sf

    def ew_sf_f(self):
        """
        Rate constant for elimination through the gills for small fish
        :return:
        """
        self.ew_sf = (1.0 / (1.85 + (155.0 / self.log_kow)))
        return self.ew_sf

    def sfish_k1_f(self):
        """
        Uptake rate constant through respiratory area for small fish
        :return:
        """
        self.sfish_k1 = ((self.ew_sf * self.gv_sf) / self.sfish_wb)
        return self.sfish_k1

    def k_bw_sf_f(self):
        """
        Small fish water partition coefficient
        :return:
        """
        self.k_bw_sf = (self.sfish_lipid * self.log_kow) + (self.sfish_nlom * 0.035 * self.log_kow) + self.sfish_water
        return self.k_bw_sf

    def sfish_k2_f(self):
        """
        Elimination rate constant through the gills for small fish
        :return:
        """
        self.sfish_k2 = self.sfish_k1 / self.k_bw_sf
        return self.sfish_k2

    def ed_sf_f(self):
        """
        Small fish dietary pesticide transfer efficiency
        :return:
        """
        self.ed_sf = 1 / (.0000003 * self.log_kow + 2.0)
        return self.ed_sf

    def gd_sf_f(self):
        """
        Small fish feeding rate
        :return:
        """
        self.gd_sf = 0.022 * self.sfish_wb ** 0.85 * math.exp(0.06 * self.water_temp)
        return self.gd_sf

    def sfish_kd_f(self):
        """
        Small fish rate constant pesticide uptake by food ingestion
        :return:
        """
        self.sfish_kd = self.ed_sf * self.gd_sf / self.sfish_wb
        return self.sfish_kd

    def sfish_kg_f(self):
        """
        Small fish growth rate constant
        :return:
        """
        if self.water_temp < 17.5:
            self.sfish_kg = 0.0005 * self.sfish_wb ** -0.2
        else:
            self.sfish_kg = 0.00251 * self.sfish_wb ** -0.2
        return self.sfish_kg

        # overall lipid content of diet

    def v_ld_sf_f(self):
        """
        Small fish lipid
        :return:
        """
        self.v_ld_sf = self.sfish_diet_sediment * self.sediment_lipid + self.sfish_diet_phytoplankton * self.phytoplankton_lipid + self.sfish_diet_benthic_invertebrates * self.beninv_lipid + self.sfish_diet_zooplankton * self.zoo_lipid + self.sfish_diet_filter_feeders * self.filterfeeders_lipid
        return self.v_ld_sf

    def v_nd_sf_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_sf = self.sfish_diet_sediment * self.sediment_nlom + self.sfish_diet_phytoplankton * self.phytoplankton_nlom + self.sfish_diet_benthic_invertebrates * self.beninv_nlom + self.sfish_diet_zooplankton * self.zoo_nlom + self.sfish_diet_filter_feeders * self.filterfeeders_nlom
        return self.v_nd_sf

    def v_wd_sf_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_sf = self.sfish_diet_sediment * self.sediment_water + self.sfish_diet_phytoplankton * self.phytoplankton_water + self.sfish_diet_benthic_invertebrates * self.beninv_water + self.sfish_diet_zooplankton * self.zoo_water + self.sfish_diet_filter_feeders * self.filterfeeders_water
        return self.v_wd_sf

    def gf_sf_f(self):
        """
        Small fish
        :return:
        """
        self.gf_sf = ((1 - 0.92) * self.v_ld_sf + (1 - 0.6) * self.v_nd_sf + (1 - 0.25) * self.v_wd_sf) * self.gd_sf
        return self.gf_sf

    def vlg_sf_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_sf = (1 - 0.92) * self.v_ld_sf * self.gd_sf / self.gf_sf
        return self.vlg_sf

    def vng_sf_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_sf = (1 - 0.6) * self.v_nd_sf * self.gd_sf / self.gf_sf
        return self.vng_sf

    def vwg_sf_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_sf = (1 - 0.25) * self.v_wd_sf * self.gd_sf / self.gf_sf
        return self.vwg_sf

    def kgb_sf_f(self):
        """
        Small fish
        :return:
        """
        self.kgb_sf = (self.vlg_sf * self.log_kow + self.vng_sf * 0.035 * self.log_kow + self.vwg_sf) / (
            self.sfish_lipid * self.log_kow + self.sfish_nlom * 0.035 * self.log_kow + self.sfish_water)
        return self.kgb_sf

    def sfish_ke_f(self):
        """
        Small fish
        :return:
        """
        self.sfish_ke = self.gf_sf * self.ed_sf * (self.kgb_sf / self.sfish_wb)
        return self.sfish_ke

    def diet_sf_f(self):
        """
        Diet small fish
        :return:
        """
        self.diet_sf = self.c_s * self.sfish_diet_sediment + self.cb_phytoplankton * self.sfish_diet_phytoplankton + self.cb_zoo * self.sfish_diet_zooplankton + self.cb_beninv * self.sfish_diet_benthic_invertebrates + self.cb_ff * self.sfish_diet_filter_feeders
        return self.diet_sf

    def cb_sf_f(self):
        """
        Small fish pesticide tissue residue
        :return:
        """
        self.cb_sf = (self.sfish_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.sfish_kd * self.diet_sf) / (
            self.sfish_k2 + self.sfish_ke + self.sfish_kg + 0)
        return self.cb_sf

    def cbl_sf_f(self):
        """
        Small fish lipid normalized pesticide tissue residue
        :return:
        """
        self.cbl_sf = (1e6 * self.cb_sf) / self.sfish_lipid
        return self.cbl_sf

    def cbd_sf_f(self):
        """
        Small fish pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_sf = (0 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.sfish_kd * self.diet_sf) / (
            self.sfish_k2 + self.sfish_ke + self.sfish_kg + 0)
        return self.cbd_sf

    def cbr_sf_f(self):
        """
        Small fish pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_sf = (self.sfish_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + 0 * self.diet_sf) / (
            self.sfish_k2 + self.sfish_ke + self.sfish_kg + 0)
        return self.cbr_sf

    def cbf_sf_f(self):
        """
        Small fish total bioconcentration factor
        :return:
        """
        self.sfish_kd = 0
        self.sfish_ke = 0
        #    sfish_km = 0 always = 0
        self.sfish_kg = 0
        self.cbf_sf = ((self.sfish_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.sfish_kd * self.diet_sf) / (
            self.sfish_k2 + self.sfish_ke + self.sfish_kg + 0)) / self.water_column_eec
        return self.cbf_sf

    def cbfl_sf_f(self):
        """
        Small fish lipid normalized bioconcentration factor
        :return:
        """
        self.sfish_kd = 0
        self.sfish_ke = 0
        #    sfish_km = 0 always = 0
        self.sfish_kg = 0
        self.cbfl_sf = (((self.sfish_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.sfish_kd * self.diet_sf) / (
                             self.sfish_k2 + self.sfish_ke + self.sfish_kg + 0)) / self.sfish_lipid) / (self.water_column_eec * self.phi)
        return self.cbfl_sf

    def cbaf_sf_f(self):
        """
        Small fish bioaccumulation factor
        :return:
        """
        self.cbaf_sf = (1e6 * self.cb_sf) / self.water_column_eec
        return self.cbaf_sf

    def cbafl_sf_f(self):
        """
        Small fish lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_sf = self.cbl_sf / self.water_d
        return self.cbafl_sf

    def cbsafl_sf_f(self):
        """
        Small fish
        :return:
        """
        self.cbsafl_sf = (self.cb_sf / self.sfish_lipid) / self.sed_om
        return self.cbsafl_sf

    def bmf_sf_f(self):
        """
        Small fish biomagnification factor
        :return:
        """
        self.bmf_sf = (self.cb_sf / self.sfish_lipid) / ((self.sfish_diet_filter_feeders * self.cb_ff / self.filterfeeders_lipid) + (
            self.sfish_diet_benthic_invertebrates * self.cb_beninv / self.beninv_lipid) + (
                                                         self.sfish_diet_zooplankton * self.cb_zoo / self.zoo_lipid) + (
                                                         self.sfish_diet_phytoplankton * self.cb_phytoplankton / self.phytoplankton_lipid))
        return self.bmf_sf

    ############ medium fish
    def gv_mf_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_mf = (1400.0 * ((self.mfish_wb ** 0.65) / self.conc_do))
        return self.gv_mf

    def ew_mf_f(self):
        """
        Rate constant for elimination through the gills for medium fish
        :return:
        """
        self.ew_mf = (1.0 / (1.85 + (155.0 / self.log_kow)))
        return self.ew_mf

    def mfish_k1_f(self):
        """
        Uptake rate constant through respiratory area for medium fish
        :return:
        """
        self.mfish_k1 = ((self.ew_mf * self.gv_mf) / self.mfish_wb)
        return self.mfish_k1

    def k_bw_mf_f(self):
        """
        Medium fish water partition coefficient
        :return:
        """
        self.k_bw_mf = (self.mfish_lipid * self.log_kow) + (self.mfish_nlom * 0.035 * self.log_kow) + self.mfish_water
        return self.k_bw_mf

    def mfish_k2_f(self):
        """
        Elimination rate constant through the gills for medium fish
        :return:
        """
        self.mfish_k2 = self.mfish_k1 / self.k_bw_mf
        return self.mfish_k2

    def ed_mf_f(self):
        """
        Medium fish dietary pesticide transfer efficiency
        :return:
        """
        self.ed_mf = 1 / (.0000003 * self.log_kow + 2.0)
        return self.ed_mf

    def gd_mf_f(self):
        """
        Medium fish feeding rate
        :return:
        """
        self.gd_mf = 0.022 * self.mfish_wb ** 0.85 * math.exp(0.06 * self.water_temp)
        return self.gd_mf

    def mfish_kd_f(self):
        """
        Medium fish rate constant pesticide uptake by food ingestion
        :return:
        """
        self.mfish_kd = self.ed_mf * self.gd_mf / self.mfish_wb
        return self.mfish_kd

    def mfish_kg_f(self):
        """
        Medium fish growth rate constant
        :return:
        """
        if self.water_temp < 17.5:
            self.mfish_kg = 0.0005 * self.mfish_wb ** -0.2
        else:
            self.mfish_kg = 0.00251 * self.mfish_wb ** -0.2
        return self.mfish_kg

    def v_ld_mf_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_mf = self.mfish_diet_sediment * self.sediment_lipid + self.mfish_diet_phytoplankton * self.phytoplankton_lipid + self.mfish_diet_benthic_invertebrates * self.beninv_lipid + self.mfish_diet_zooplankton * self.zoo_lipid + self.mfish_diet_filter_feeders * self.filterfeeders_lipid + self.mfish_diet_small_fish * self.sfish_lipid
        return self.v_ld_mf

    def v_nd_mf_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_mf = self.mfish_diet_sediment * self.sediment_nlom + self.mfish_diet_phytoplankton * self.phytoplankton_nlom + self.mfish_diet_benthic_invertebrates * self.beninv_nlom + self.mfish_diet_zooplankton * self.zoo_nlom + self.mfish_diet_filter_feeders * self.filterfeeders_nlom + self.mfish_diet_small_fish * self.sfish_nlom
        return self.v_nd_mf

    def v_wd_mf_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_mf = self.mfish_diet_sediment * self.sediment_water + self.mfish_diet_phytoplankton * self.phytoplankton_water + self.mfish_diet_benthic_invertebrates * self.beninv_water + self.mfish_diet_zooplankton * self.zoo_water + self.mfish_diet_filter_feeders * self.filterfeeders_water + self.mfish_diet_small_fish * self.sfish_water
        return self.v_wd_mf

    def gf_mf_f(self):
        """
        Medium fish
        :return:
        """
        self.gf_mf = ((1 - 0.92) * self.v_ld_mf + (1 - 0.6) * self.v_nd_mf + (1 - 0.25) * self.v_wd_mf) * self.gd_mf
        return self.gf_mf

    def vlg_mf_f(self):
        """
    # lipid content in gut
        :return:
        """
        self.vlg_mf = (1 - 0.92) * self.v_ld_mf * self.gd_mf / self.gf_mf
        return self.vlg_mf

    def vng_mf_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_mf = (1 - 0.6) * self.v_nd_mf * self.gd_mf / self.gf_mf
        return self.vng_mf

    def vwg_mf_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_mf = (1 - 0.25) * self.v_wd_mf * self.gd_mf / self.gf_mf
        return self.vwg_mf

    def kgb_mf_f(self):
        """
        Medium fish
        :return:
        """
        self.kgb_mf = (self.vlg_mf * self.log_kow + self.vng_mf * 0.035 * self.log_kow + self.vwg_mf) / (
            self.mfish_lipid * self.log_kow + self.mfish_nlom * 0.035 * self.log_kow + self.mfish_water)
        return self.kgb_mf

    def mfish_ke_f(self):
        """

        :return:
        """
        self.mfish_ke = self.gf_mf * self.ed_mf * (self.kgb_mf / self.mfish_wb)
        return self.mfish_ke

    def diet_mf_f(self):
        """
        Diet medium fish
        :return:
        """
        self.diet_mf = self.c_s * self.mfish_diet_sediment + self.cb_phytoplankton * self.mfish_diet_phytoplankton + self.cb_zoo * self.mfish_diet_zooplankton + self.cb_beninv * self.mfish_diet_benthic_invertebrates + self.cb_ff * self.mfish_diet_filter_feeders + self.cb_sf * self.mfish_diet_small_fish
        return self.diet_mf

    def cb_mf_f(self):
        """
        Medium fish pesticide tissue residue
        :return:
        """
        self.cb_mf = (self.mfish_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.mfish_kd * self.diet_mf) / (
            self.mfish_k2 + self.mfish_ke + self.mfish_kg + 0)
        return self.cb_mf

    def cbl_mf_f(self):
        """
        Medium fish lipid normalized pesticide tissue residue
        :return:
        """
        self.cbl_mf = (1e6 * self.cb_mf) / self.mfish_lipid
        return self.cbl_mf

    def cbd_mf_f(self):
        """
        Medium fish pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_mf = (0 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.mfish_kd * self.diet_mf) / (
            self.mfish_k2 + self.mfish_ke + self.mfish_kg + 0)
        return self.cbd_mf

    def cbr_mf_f(self):
        """
        Medium fish pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_mf = (self.mfish_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + 0 * self.diet_mf) / (
            self.mfish_k2 + self.mfish_ke + self.mfish_kg + 0)
        return self.cbr_mf

    def cbf_mf_f(self):
        """
        Medium fish total bioconcentration factor
        :return:
        """
        self.mfish_kd = 0
        self.mfish_ke = 0
        # mfish_km = 0
        self.mfish_kg = 0
        self.cbf_mf = ((self.mfish_k1 * (0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.mfish_kd * self.diet_mf) / (
            self.mfish_k2 + self.mfish_ke + self.mfish_kg + 0)) / self.water_column_eec
        return self.cbf_mf

    def cbfl_mf_f(self):
        """
        Medium fish lipid normalized bioconcentration factor
        :return:
        """
        self.mfish_kd = 0
        self.mfish_ke = 0
        # mfish_km = 0
        self.mfish_kg = 0
        self.cbfl_mf = ((((self.mfish_k1 * (
            0.95 * self.phi * self.water_column_eec + 0.05 * self.pore_water_eec) + self.mfish_kd * self.diet_mf) / (
                              self.mfish_k2 + self.mfish_ke + self.mfish_kg + 0))) / self.mfish_lipid) / (self.water_column_eec * self.phi)
        return self.cbfl_mf

    def cbaf_mf_f(self):
        """
        Medium fish bioaccumulation factor
        :return:
        """
        self.cbaf_mf = (1e6 * self.cb_mf) / self.water_column_eec
        return self.cbaf_mf

    def cbafl_mf_f(self):
        """
        Medium fish lipid normalized factor
        :return:
        """
        self.cbafl_mf = self.cbl_mf / self.water_d
        return self.cbafl_mf

    def cbsafl_mf_f(self):
        """
        Medium fish
        :return:
        """
        self.cbsafl_mf = (self.cb_mf / self.mfish_lipid) / self.sed_om
        return self.cbsafl_mf

    def cbmf_mf_f(self):
        """
        Medium fish biomagnification factor
        :return:
        """
        self.cbmf_mf = (self.cb_mf / self.mfish_lipid) / (
            (self.mfish_diet_small_fish * self.cb_sf / self.sfish_lipid) + (
                self.mfish_diet_filter_feeders * self.cb_ff / self.filterfeeders_lipid) + (
                self.mfish_diet_benthic_invertebrates * self.cb_beninv / self.beninv_lipid) + (
                self.mfish_diet_zooplankton * self.cb_zoo / self.zoo_lipid) + (
                self.mfish_diet_phytoplankton * self.cb_phytoplankton / self.phytoplankton_lipid))
        return self.cbmf_mf

    ############ large fish
    def gv_lf_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_lf = (1400.0 * ((self.lfish_wb ** 0.65) / self.conc_do))
        return self.gv_lf

    def ew_lf_f(self):
        """
        Rate constant for elimination through the gills for large fish
        :return:
        """
        self.ew_lf = (1.0 / (1.85 + (155.0 / self.log_kow)))
        return self.ew_lf

    def lfish_k1_f(self):
        """
        Uptake rate constant through respiratory area for large fish
        :return:
        """
        self.lfish_k1 = ((self.ew_lf * self.gv_lf) / self.lfish_wb)
        return self.lfish_k1

    def k_bw_lf_f(self):
        """
        Large fish water partition coefficient
        :return:
        """
        self.k_bw_lf = (self.lfish_lipid * self.log_kow) + (self.lfish_nlom * 0.035 * self.log_kow) + self.lfish_water
        return self.k_bw_lf

    def lfish_k2_f(self):
        """
        Elimination rate constant through the gills for large fish
        :return:
        """
        self.lfish_k2 = self.lfish_k1 / self.k_bw_lf
        return self.lfish_k2

    def ed_lf_f(self):
        """
        Large fish dietary pesticide transfer efficiency
        :return:
        """
        self.ed_lf = 1 / (.0000003 * self.log_kow + 2.0)
        return self.ed_lf

    def gd_lf_f(self):
        """
        Large fish feeding rate
        :return:
        """
        self.gd_lf = 0.022 * self.lfish_wb ** 0.85 * math.exp(0.06 * self.water_temp)
        return self.gd_lf

    def lfish_kd_f(self):
        """
        Large fish rate constant pesticide uptake by food ingestion
        :return:
        """
        self.lfish_kd = self.ed_lf * self.gd_lf / self.lfish_wb
        return self.lfish_kd

    def lfish_kg_f(self):
        """
        Medium fish growth rate constant
        :return:
        """
        if self.water_temp < 17.5:
            self.lfish_kg = 0.0005 * self.lfish_wb ** -0.2
        else:
            self.lfish_kg = 0.00251 * self.lfish_wb ** -0.2
        return self.lfish_kg

    def v_ld_lf_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_lf = self.lfish_diet_sediment * self.sediment_lipid + self.lfish_diet_phytoplankton * self.phytoplankton_lipid + self.lfish_diet_benthic_invertebrates * self.beninv_lipid + self.lfish_diet_zooplankton * self.zoo_lipid + self.lfish_diet_filter_feeders * self.filterfeeders_lipid + self.lfish_diet_small_fish * self.sfish_lipid + self.lfish_diet_medium_fish * self.mfish_lipid
        return self.v_ld_lf

    def v_nd_lf_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_lf = self.lfish_diet_sediment * self.sediment_nlom + self.lfish_diet_phytoplankton * self.phytoplankton_nlom + self.lfish_diet_benthic_invertebrates * self.beninv_nlom + self.lfish_diet_zooplankton * self.zoo_nlom + self.lfish_diet_filter_feeders * self.filterfeeders_nlom + self.lfish_diet_small_fish * self.sfish_nlom + self.lfish_diet_medium_fish * self.mfish_nlom
        return self.v_nd_lf

    def v_wd_lf_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_lf = self.lfish_diet_sediment * self.sediment_water + self.lfish_diet_phytoplankton * self.phytoplankton_water + self.lfish_diet_benthic_invertebrates * self.beninv_water + self.lfish_diet_zooplankton * self.zoo_water + self.lfish_diet_filter_feeders * self.filterfeeders_water + self.lfish_diet_small_fish * self.sfish_water + self.lfish_diet_medium_fish * self.mfish_water
        return self.v_wd_lf

    def gf_lf_f(self):
        """
        Large fiah
        :return:
        """
        self.gf_lf = ((1 - 0.92) * self.v_ld_lf + (1 - 0.6) * self.v_nd_lf + (1 - 0.25) * self.v_wd_lf) * self.gd_lf
        return self.gf_lf

    def vlg_lf_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_lf = (1 - 0.92) * self.v_ld_lf * self.gd_lf / self.gf_lf
        return self.vlg_lf

    def vng_lf_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_lf = (1 - 0.6) * self.v_nd_lf * self.gd_lf / self.gf_lf
        return self.vng_lf

    def vwg_lf_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_lf = (1 - 0.25) * self.v_wd_lf * self.gd_lf / self.gf_lf
        return self.vwg_lf

    def kgb_lf_f(self):
        """
        Large fish
        :return:
        """
        self.kgb_lf = (self.vlg_lf * self.log_kow + self.vng_lf * 0.035 * self.log_kow + self.vwg_lf) / (
            self.lfish_lipid * self.log_kow + self.lfish_nlom * 0.035 * self.log_kow + self.lfish_water)
        return self.kgb_lf

    def lfish_ke_f(self):
        """
        Large fish
        :return:
        """
        self.lfish_ke = self.gf_lf * self.ed_lf * (self.kgb_lf / self.lfish_wb)
        return self.lfish_ke

    def diet_lf_f(self):
        """
        Large fish
        :return:
        """
        self.diet_lf = self.c_s * self.lfish_diet_sediment + self.cb_phytoplankton * self.lfish_diet_phytoplankton + self.cb_zoo * self.lfish_diet_zooplankton + self.cb_beninv * self.lfish_diet_benthic_invertebrates + self.cb_ff * self.lfish_diet_filter_feeders + self.cb_sf * self.lfish_diet_small_fish + self.cb_mf * self.lfish_diet_medium_fish
        return self.diet_lf

    def cb_lf_f(self):
        """
        Large fish pesticide tissue residue
        :return:
        """
        self.cb_lf = (self.lfish_k1 * (1.0 * self.phi * self.water_column_eec + 0.00 * self.pore_water_eec) + self.lfish_kd * self.diet_lf) / (
            self.lfish_k2 + self.lfish_ke + self.lfish_kg + 0)
        return self.cb_lf

    def cbl_lf_f(self):
        """
        Large fish lipid normalized pesticide tissue residue
        :return:
        """
        self.cbl_lf = (1e6 * self.cb_lf) / self.lfish_lipid
        return self.cbl_lf

    def cbd_lf_f(self):
        """
        Large fish pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_lf = (0 * (1.0 * self.phi * self.water_column_eec + 0.0 * self.pore_water_eec) + self.lfish_kd * self.diet_lf) / (
            self.lfish_k2 + self.lfish_ke + self.lfish_kg + 0)
        return self.cbd_lf

    def cbr_lf_f(self):
        """
        Large fish pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_lf = (self.lfish_k1 * (1.0 * self.phi * self.water_column_eec + 0.0 * self.pore_water_eec) + 0 * self.diet_lf) / (
            self.lfish_k2 + self.lfish_ke + self.lfish_kg + 0)
        return self.cbr_lf

    def cbf_lf_f(self):
        """
        Large fish total bioconcentration factor
        :return:
        """
        self.lfish_kd = 0
        self.lfish_ke = 0
        # lfish_km = 0
        self.lfish_kg = 0
        self.cbf_lf = ((self.lfish_k1 * (1.0 * self.phi * self.water_column_eec + 0.00 * self.pore_water_eec) + self.lfish_kd * self.diet_lf) / (
            self.lfish_k2 + self.lfish_ke + self.lfish_kg + 0)) / self.water_column_eec
        return self.cbf_lf

    def cbfl_lf_f(self):
        """
        Large fish lipid normalized total bioconcentration factor
        :return:
        """
        self.lfish_kd = 0
        self.lfish_ke = 0
        # lfish_km = 0
        self.lfish_kg = 0
        self.cbfl_lf = ((
                            (self.lfish_k1 * (
                                1.0 * self.phi * self.water_column_eec + 0.00 * self.pore_water_eec) + self.lfish_kd * self.diet_lf) / (
                                self.lfish_k2 + self.lfish_ke + self.lfish_kg + 0)) / self.lfish_lipid) / (self.water_column_eec * self.phi)
        return self.cbfl_lf

    def cbaf_lf_f(self):
        """
        Large fish bioaccumulation factor
        :return:
        """
        self.cbaf_lf = (1e6 * self.cb_lf) / self.water_column_eec
        return self.cbaf_lf

    def cbafl_lf_f(self):
        """
        Large fish lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_lf = self.cbl_lf / self.water_d
        return self.cbafl_lf

    def cbsafl_lf_f(self):
        """
        Large fish biota-sediment accumulation factors
        :return:
        """
        self.cbsafl_lf = (self.cb_lf / self.lfish_lipid) / self.sed_om
        return self.cbsafl_lf

    def cbmf_lf_f(self):
        """
        Large fish biomagnification factor
        :return:
        """
        self.cbmf_lf = (self.cb_lf / self.lfish_lipid) / (
            (self.lfish_diet_medium_fish * self.cb_mf / self.mfish_lipid) + (self.lfish_diet_small_fish * self.cb_sf / self.sfish_lipid) + (
                self.lfish_diet_filter_feeders * self.cb_ff / self.filterfeeders_lipid) + (
                self.lfish_diet_benthic_invertebrates * self.cb_beninv / self.beninv_lipid) + (
                self.lfish_diet_zooplankton * self.cb_zoo / self.zoo_lipid) + (
                self.lfish_diet_phytoplankton * self.cb_phytoplankton / self.phytoplankton_lipid))
        return self.cbmf_lf

    ################################## Mammals EECs
    def mweight_f(self):
        """
        Mammals
        :return:
        """
        self.cb_a = np.array(
            [[self.cb_phytoplankton, self.cb_zoo, self.cb_beninv, self.cb_ff, self.cb_sf, self.cb_mf, self.cb_lf]])
        self.cb_a2 = self.cb_a * 1000000
        # array of mammal weights
        #[fog/water shrew,rice rat/star-nosed mole,small mink,large mink,small river otter	,large river otter]
        self.mweight = np.array([[0.018, 0.085, 0.45, 1.8, 5, 15]])
        return self.mweight

    def dfir_f(self):
        """
        Mammals
        :return:
        """
        self.dfir = (0.0687 * self.mweight ** 0.822) / self.mweight
        return self.dfir

    def wet_food_ingestion_m_f(self):
        """
        Mammals
        :return:
        """
        # creation of array for mammals of dry food ingestion rate
        # array of percent water in biota
        self.v_wb_a = np.array([[self.phytoplankton_water, self.zoo_water, self.beninv_water, self.filterfeeders_water, self.sfish_water,
                                 self.mfish_water, self.lfish_water]])
        # array of % diet of food web for each mammal
        self.diet_mammal = np.array(
            [[0, 0, 1, 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])
        self.denom1 = self.diet_mammal * self.v_wb_a
        self.denom1 = (
            [[0., 0., 0.76, 0., 0., 0., 0.], [0., 0., 0.2584, 0.2805, 0.2409, 0., 0.], [0., 0., 0., 0., 0., 0.73, 0.],
             [0., 0., 0., 0., 0., 0.73, 0.], [0., 0., 0., 0., 0., 0.73, 0.], [0., 0., 0., 0., 0., 0., 0.73]])
        self.denom2 = np.cumsum(self.denom1, axis=1)
        self.denom3 = self.denom2[:,
                      6]  # selects out seventh row of array which is the cumulative sums of the products
        self.denom4 = 1 - self.denom3
        # wet food ingestion rate for mammals
        self.wet_food_ingestion_m = self.dfir / self.denom4
        return self.wet_food_ingestion_m

    def drinking_water_intake_m_f(self):
        """
        Array of drinking water intake rate for mammals
        :return:
        """
        self.drinking_water_intake_m = .099 * self.mweight ** 0.9
        return self.drinking_water_intake_m

    def db4_f(self):
        """
        Mammals
        :return:
        """
        self.db1 = self.cb_a2 * self.diet_mammal
        self.db2 = np.cumsum(self.db1, axis=1)
        self.db3 = self.db2[:, 6]
        # dose based  EEC
        self.db4 = (self.db3 / 1000) * self.wet_food_ingestion_m + (self.water_column_eec / 1000) * (
            self.drinking_water_intake_m / self.mweight)
        return self.db4

    def db5_f(self):
        """
        Mammals
        :return:
        """
        # dietary based EEC
        self.db5 = self.db3 / 1000
        return self.db5

    ################################## Avian EECs
    def aweight_f(self):
        """
        Avian
        :return:
        """
        self.aweight = np.array([[0.02, 6.7, 0.07, 2.9, 1.25, 7.5]])
        return self.aweight

    def dfir_a_f(self):
        """
        Avian
        :return:
        """
        self.dfir_a = (0.0582 * self.aweight ** 0.651) / self.aweight
        return self.dfir_a

    def wet_food_ingestion_a_f(self):
        """
        Avian
        :return:
        """
        self.v_wb_a = np.array([[self.phytoplankton_water, self.zoo_water, self.beninv_water, self.filterfeeders_water, self.sfish_water,
                                 self.mfish_water, self.lfish_water]])
        # the following avian diet data reflects the diet of sandpipers, cranes, rails, herons, small osprey
        # and white pelicans; each avian species diet is provided as a percent of the diet elements
        # listed above (in that order)
        self.diet_avian = np.array(
            [[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0], [0, 0, 0.5, 0, 0.5, 0, 0],
             [0, 0, 0.5, 0, 0, 0.5, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])
        self.denom1a = self.diet_avian * self.v_wb_a
        self.denom2a = np.cumsum(self.denom1a, axis=1)
        self.denom3a = self.denom2a[:,
                       6]  # selects out seventh row of array which is the cumulative sums of the products
        self.denom4a = 1 - self.denom3a
        self.wet_food_ingestion_a = self.dfir_a / self.denom4a
        return self.wet_food_ingestion_a

    def drinking_water_intake_a_f(self):
        """
        Avian drinking water intake
        :return:
        """
        self.drinking_water_intake_a = 0.059 * self.aweight ** 0.67
        return self.drinking_water_intake_a

    def db4a_f(self):
        """
        Avian
        :return:
        """
        self.db1a = self.cb_a2 * self.diet_avian
        self.db2a = np.cumsum(self.db1a, axis=1)
        self.db3a = self.db2a[:, 6]
        # dose based  EEC
        self.db4a = (self.db3a / 1000) * self.wet_food_ingestion_a + (self.water_column_eec / 1000) * (
            self.drinking_water_intake_a / self.aweight)
        return self.db4a

    def db5a_f(self):
        """
        Avian
        :return:
        """
        # dietary based EEC
        self.db5a = (self.db3a / 1000)
        return self.db5a

        ##################################### toxicity values
        #################################### mammal

    def acute_dose_based_m_f(self):
        """
        Dose based acute toxicity for mammals
        :return:
        """
        self.acute_dose_based_m = self.mammalian_ld50 * ((float(self.bw_mamm) / 1000) / self.mweight) ** 0.25
        return self.acute_dose_based_m

    def chronic_dose_based_m_f(self):
        """
        Dose based chronic toxicity for mammals
        :return:
        """
        self.chronic_dose_based_m = (self.mammalian_chronic_endpoint / 20) * (
            ((float(self.bw_mamm) / 1000) / self.mweight) ** 0.25)
        return self.chronic_dose_based_m

    def acute_dose_based_a_f(self):
        """
        Dose based acute toxicity for birds
        :return:
        """
        self.acute_dose_based_a = self.avian_ld50 * (self.aweight / (float(self.bw_bird) / 1000)) ** (
            self.mineau_scaling_factor - 1)
        return self.acute_dose_based_a

    ##################################### RQ Values
    def acute_rq_dose_m_f(self):
        """
        RQ dose based for mammals
        :return:
        """
        self.acute_rq_dose_m = self.db4 / self.acute_dose_based_m
        return self.acute_rq_dose_m

    def chronic_rq_dose_m_f(self):
        """
        Chronic RQ
        :return:
        """
        self.chronic_rq_dose_m = self.db4 / self.chronic_dose_based_m
        return self.chronic_rq_dose_m

    def acute_rq_diet_m_f(self):
        """
        Acute RQ diet based for mammals
        :return:
        """
        self.acute_rq_diet_m = self.db5 / self.mammalian_lc50
        return self.acute_rq_diet_m

    def chronic_rq_diet_m_f(self):
        """
        Chronic RQ diet based for mammals
        :return:
        """
        self.chronic_rq_diet_m = self.db5 / self.mammalian_chronic_endpoint
        return self.chronic_rq_diet_m

    def acute_rq_dose_a_f(self):
        """
        RQ dose based for birds
        :return:
        """
        self.acute_rq_dose_a = self.db4a / self.acute_dose_based_a
        return self.acute_rq_dose_a

    def acute_rq_diet_a_f(self):
        """
        RQ diet based for birds
        :return:
        """
        self.acute_rq_diet_a = self.db5a / self.avian_lc50
        return self.acute_rq_diet_a

    def chronic_rq_diet_a_f(self):
        """
        Chronic RQ diet for birds
        :return:
        """
        self.chronic_rq_diet_a = self.db5a / self.avian_noaec
        return self.chronic_rq_diet_a
