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

    #######################################################
    # def gv_zoo_f(self):
    #     """
    #     Ventilation rate of zooplankton
    #     unit: L/d
    #     Eq. A5.2b
    #     :return:
    #     """
    #     self.gv_zoo = (1400 * (self.zoo_wb ** 0.65)) / self.conc_do
    #     return self.gv_zoo
    #
    # def gv_beninv_f(self):
    #     """
    #     Ventilation rate
    #     :return:
    #     """
    #     self.gv_beninv = (1400 * ((self.beninv_wb ** 0.65) / self.conc_do))
    #     return self.gv_beninv
    #
    # def gv_ff_f(self):
    #     """
    #     Ventilation rate
    #     :return:
    #     """
    #     self.gv_ff = (1400.0 * ((self.filterfeeders_wb ** 0.65) / self.conc_do))
    #     return self.gv_ff
    #
    # def gv_sf_f(self):
    #     """
    #     Ventilation rate
    #     :return:
    #     """
    #     self.gv_sf = (1400.0 * ((self.sfish_wb ** 0.65) / self.conc_do))
    #     return self.gv_sf
    #
    # def gv_mf_f(self):
    #     """
    #     Ventilation rate
    #     :return:
    #     """
    #     self.gv_mf = (1400.0 * ((self.mfish_wb ** 0.65) / self.conc_do))
    #     return self.gv_mf
    #
    # def gv_lf_f(self):
    #     """
    #     Ventilation rate
    #     :return:
    #     """
    #     self.gv_lf = (1400.0 * ((self.lfish_wb ** 0.65) / self.conc_do))
    #     return self.gv_lf
###########################################################
###########################################################

    def ventilation_rate(self, wet_wgt):
        """
        :description Ventilation rate of aquatic animal
        :unit L/d
        :expression Kabam Eq. A5.2b (Gv)
        :param wet_wgt: wet weight of animal (kg)
        :param conc_do: concentration of dissolved oxygen (mg O2/L)
        :return:
        """

        vent_rate = pd.Series([], dtype = 'float')

        vent_rate = (1400.0 * ((wet_wgt ** 0.65) / self.conc_do))
        return vent_rate

###############################################
    # def ew_zoo_f(self):
    #     """
    #     Pesticide uptake efficiency by gills
    #     unit: fraction
    #     Eq. A5.2a
    #     :return:
    #     """
    #     self.ew_zoo = (1 / (1.85 + (155 / self.log_kow)))
    #     return self.ew_zoo
    #
    # def ew_beninv_f(self):
    #     """
    #     Rate constant for elimination through the gills for benthic invertebrates
    #     :return:
    #     """
    #     self.ew_beninv = (1 / (1.85 + (155 / self.log_kow)))
    #     return self.ew_beninv
    #
    # def ew_ff_f(self):
    #     """
    #     Rate constant for elimination through the gills for filter feeders
    #     :return:
    #     """
    #     self.ew_ff = (1.0 / (1.85 + (155.0 / self.log_kow)))
    #     return self.ew_ff
    #
    # def ew_sf_f(self):
    #     """
    #     Rate constant for elimination through the gills for small fish
    #     :return:
    #     """
    #     self.ew_sf = (1.0 / (1.85 + (155.0 / self.log_kow)))
    #     return self.ew_sf
    #
    # def ew_mf_f(self):
    #     """
    #     Rate constant for elimination through the gills for medium fish
    #     :return:
    #     """
    #     self.ew_mf = (1.0 / (1.85 + (155.0 / self.log_kow)))
    #     return self.ew_mf
    #
    # def ew_lf_f(self):
    #     """
    #     Rate constant for elimination through the gills for large fish
    #     :return:
    #     """
    #     self.ew_lf = (1.0 / (1.85 + (155.0 / self.log_kow)))
    #     return self.ew_lf

######################################################
######################################################

    def pest_uptake_eff_bygills(self):
        """
        :description Pesticide uptake efficiency by gills
        :unit fraction
        :expression Kabam Eq. A5.2a (Ew)
        :param log kow: octanol-water partition coefficient ()
        :return:
        """

        pest_uptake_eff_bygills = pd.Series([], dtype = 'float')

        pest_uptake_eff_bygills = (1 / (1.85 + (155 / self.log_kow)))
        return pest_uptake_eff_bygills

################################################################
## bioaccumulation/concentration calculations: K1

    # calculation for phytoplankton is different than for other aquatic animals
    # def phytoplankton_k1_f(self):
    #     """
    #     Rate constant for uptake through respiratory area
    #     Eq. A5.1  (unique to phytoplankton)
    #     :return:
    #     """
    #     self.phytoplankton_k1 = 1 / (6.0e-5 + (5.5 / self.log_kow))
    #     return self.phytoplankton_k1
    #
    # def zoo_k1_f(self):
    #     """
    #     Uptake rate constant through respiratory area for zooplankton
    #     unit: L/kg*d
    #     Eq.A5.2
    #     :return:
    #     """
    #     self.zoo_k1 = self.ew_zoo * self.gv_zoo / self.zoo_wb
    #     return self.zoo_k1
    #
    # def beninv_k1_f(self):
    #     """
    #     Uptake rate constant through respiratory area for benthic invertebrates
    #     :return:
    #     """
    #     self.beninv_k1 = ((self.ew_beninv * self.gv_beninv) / self.beninv_wb)
    #     return self.beninv_k1
    #
    # def filterfeeders_k1_f(self):
    #     """
    #     Uptake rate constant through respiratory area for filter feeders
    #     :return:
    #     """
    #     self.filterfeeders_k1 = ((self.ew_filterfeeders * self.gv_filterfeeders) / self.filterfeeders_wb)
    #     return self.filterfeeders_k1
    #
    # def sfish_k1_f(self):
    #     """
    #     Uptake rate constant through respiratory area for small fish
    #     :return:
    #     """
    #     self.sfish_k1 = ((self.ew_sfish * self.gv_sfish) / self.sfish_wb)
    #     return self.sfish_k1
    #
    # def mfish_k1_f(self):
    #     """
    #     Uptake rate constant through respiratory area for medium fish
    #     :return:
    #     """
    #     self.mfish_k1 = ((self.ew_mfish * self.gv_mfish) / self.mfish_wb)
    #     return self.mfish_k1
    #
    # def lfish_k1_f(self):
    #     """
    #     Uptake rate constant through respiratory area for large fish
    #     :return:
    #     """
    #     self.lfish_k1 = ((self.ew_lfish * self.gv_lfish) / self.lfish_wb)
    #     return self.lfish_k1

######################################################
######################################################

    def phytoplankton_k1_calc(self):
        """
        :description Uptake rate constant through respiratory area for phytoplankton
        :unit L/kg*d
        :expression Kabam Eq. A5.1  (K1:unique to phytoplankton)
        :param 6.05e-5: Parameter 'A' in Eq. A5.1; constant related to resistance to pesticide
                        uptake through the aquaeous phase of plant (days)
        :param 5.5: Parameter 'B' in Eq. A5.1; contant related to the resistance to pesticide
                    uptake through the organice phase of plant (days)
        :param log kow: octanol-water partition coefficient ()

        :return:
        """

        phyto_k1 = pd.Series([], dtype = 'float')

        phyto_k1 = 1 / (6.0e-5 + (5.5 / self.log_kow))
        return phyto_k1

    def aq_animal_k1_calc(self, pest_uptake_eff_bygills, vent_rate, wet_wgt):
        """
        :description Uptake rate constant through respiratory area for aquatic animals
        :unit L/kg*d
        :expression Kabam Eq. A5.2 (K1)
        :param pest_uptake_eff_bygills: Pesticide uptake efficiency by gills of aquatic animals (fraction)
        :param vent_rate: Ventilation rate of aquatic animal (L/d)
        :param wet_wgt: wet weight of animal (kg)

        :return:
        """

        aq_animal_k1 = pd.Series([], dtype = 'float')

        aq_animal_k1 = ((pest_uptake_eff_bygills * vent_rate) / wet_wgt)
        return aq_animal_k1

########################################################

    # def k_bw_phytoplankton_f(self):
    #     """
    #     Phytoplankton water partition coefficient
    #     Eq. A6a
    #     :return:
    #     """
    #     self.k_bw_phytoplankton = (self.phytoplankton_lipid * self.log_kow) + (
    #                                self.phytoplankton_nlom * 0.35 * self.log_kow) + self.phytoplankton_water
    #     return self.k_bw_phytoplankton
    #
    # def k_bw_zoo_f(self):
    #     """
    #     Zooplankton-water partition coefficient (based on wet weight)
    #     unit: -
    #     Eq. A6a
    #     :return:
    #     """
    #     self.k_bw_zoo = (self.zoo_lipid * self.log_kow) + (self.zoo_nlom * 0.035 * self.log_kow) + self.zoo_water
    #     return self.k_bw_zoo
    #
    # def k_bw_beninv_f(self):
    #     """
    #     Benthic invertebrate water partition coefficient
    #     :return:
    #     """
    #     self.k_bw_beninv = (self.beninv_lipid * self.log_kow) + (self.beninv_nlom * 0.035 * self.log_kow) + self.beninv_water
    #     return self.k_bw_beninv
    #
    # def k_bw_ff_f(self):
    #     """
    #     Filter feeder water partition coefficient
    #     :return:
    #     """
    #     self.k_bw_ff = (self.filterfeeders_lipid * self.log_kow) + (self.filterfeeders_nlom * 0.035 * self.log_kow) + self.filterfeeders_water
    #     return self.k_bw_ff
    #
    # def k_bw_sf_f(self):
    #     """
    #     Small fish water partition coefficient
    #     :return:
    #     """
    #     self.k_bw_sf = (self.sfish_lipid * self.log_kow) + (self.sfish_nlom * 0.035 * self.log_kow) + self.sfish_water
    #     return self.k_bw_sf
    #
    # def k_bw_mf_f(self):
    #     """
    #     Medium fish water partition coefficient
    #     :return:
    #     """
    #     self.k_bw_mf = (self.mfish_lipid * self.log_kow) + (self.mfish_nlom * 0.035 * self.log_kow) + self.mfish_water
    #     return self.k_bw_mf
    #
    # def k_bw_lf_f(self):
    #     """
    #     Large fish water partition coefficient
    #     :return:
    #     """
    #     self.k_bw_lf = (self.lfish_lipid * self.log_kow) + (self.lfish_nlom * 0.035 * self.log_kow) + self.lfish_water
    #     return self.k_bw_lf

##########################################################
##########################################################

    def animal_water_part_coef(self, frac_lipid_cont, frac_nlom_cont, frac_water_cont, beta):
        """
        :description Organism-Water partition coefficient (based on organism wet weight)
        :unit ()
        :expression Kabam Eq. A6a (Kbw)
        :param frac_lipid_cont: lipid fraction of organism (kg lipid/kg organism wet weight)
        :param frac_nlom_cont: non-lipid organic matter (NLOM) fraction of organism (kg NLOM/kg organism wet weight)
        :param frac_water_cont water content of organism (kg water/kg organism wet weight)
        :param log kow: octanol-water partition coefficient ()
        :param beta: proportionality constant expressing the sorption capacity of NLOM or NLOC to
                     that of octanol (0.35 for phytoplankton; 0.035 for all other aquatic animals)
        :return:
        """
        part_coef = pd.Series([], dtype = 'float')

        part_coef = (frac_lipid_cont * self.kow) + (frac_nlom_cont * beta * self.kow) + frac_water_cont
        return part_coef


 #########################################################
    #  def phytoplankton_k2_f(self):
    #     """
    #     Rate constant for elimination through the gills for phytoplankton
    #     Eq. A6
    #     :return:
    #     """
    #     self.phytoplankton_k2 = self.phytoplankton_k1 / self.k_bw_phytoplankton
    #     return self.phytoplankton_k2
    #
    # def zoo_k2_f(self):
    #     """
    #     Elimination rate constant through the gills for zooplankton
    #     :return:
    #     """
    #     self.zoo_k2 = self.zoo_k1 / self.k_bw_zoo
    #     return self.zoo_k2
    #
    # def beninv_k2_f(self):
    #     """
    #     Elimination rate constant through the gills for zooplankton
    #     :return:
    #     """
    #     self.beninv_k2 = self.beninv_k1 / self.k_bw_beninv
    #     return self.beninv_k2
    #
    # def filterfeeders_k2_f(self):
    #     """
    #     Elimination rate constant through the gills for filter feeders
    #     :return:
    #     """
    #     self.filterfeeders_k2 = self.filterfeeders_k1 / self.k_bw_ff
    #     return self.filterfeeders_k2
    #
    # def sfish_k2_f(self):
    #     """
    #     Elimination rate constant through the gills for small fish
    #     :return:
    #     """
    #     self.sfish_k2 = self.sfish_k1 / self.k_bw_sf
    #     return self.sfish_k2
    #
    # def mfish_k2_f(self):
    #     """
    #     Elimination rate constant through the gills for medium fish
    #     :return:
    #     """
    #     self.mfish_k2 = self.mfish_k1 / self.k_bw_mf
    #     return self.mfish_k2
    #
    # def lfish_k2_f(self):
    #     """
    #     Elimination rate constant through the gills for large fish
    #     :return:
    #     """
    #     self.lfish_k2 = self.lfish_k1 / self.k_bw_lf
    #     return self.lfish_k2

##########################################################
##########################################################
    def aq_animal_k2_calc(self, aq_animal_k1, animal_water_part_coef):
        """
        :description Elimination rate constant through the respiratory area
        :unit (per day)
        :expression Kabam Eq. A6 (K2)
        :param aq_animal_k1: Uptake rate constant through respiratory area for aquatic animals, including phytoplankton (L/kg*d)
        :param animal_water_part_coef (Kbw): Organism-Water partition coefficient (based on organism wet weight ()

        :return:
        """
        aq_animal_k2 = pd.Series([], dtype = 'float')

        aq_animal_k2 = aq_animal_k1 / animal_water_part_coef
        return aq_animal_k2

##########################################################

    # def kg_zoo_f(self):
    #     """
    #     Zooplankton growth rate constant
    #     :return:
    #     """
    #     if self.water_temp < 17.5:
    #         self.kg_zoo = 0.0005 * self.zoo_wb ** -0.2
    #     else:
    #         self.kg_zoo = 0.00251 * self.zoo_wb ** -0.2
    #     return self.kg_zoo
    #
    # def kg_beninv_f(self):
    #     """
    #     Benthic invertebrate growth rate constant
    #     :return:
    #     """
    #     if self.water_temp < 17.5:
    #         self.kg_beninv = 0.0005 * self.beninv_wb ** -0.2
    #     else:
    #         self.kg_beninv = 0.00251 * self.beninv_wb ** -0.2
    #     return self.kg_beninv
    #
    # def kg_ff_f(self):
    #     """
    #     Filter feeder growth rate constant
    #     :return:
    #     """
    #     if self.water_temp < 17.5:
    #         self.kg_ff = 0.0005 * self.filterfeeders_wb ** -0.2
    #     else:
    #         self.kg_ff = 0.00251 * self.filterfeeders_wb ** -0.2
    #     return self.kg_ff
    #
    # def sfish_kg_f(self):
    #     """
    #     Small fish growth rate constant
    #     :return:
    #     """
    #     if self.water_temp < 17.5:
    #         self.sfish_kg = 0.0005 * self.sfish_wb ** -0.2
    #     else:
    #         self.sfish_kg = 0.00251 * self.sfish_wb ** -0.2
    #     return self.sfish_kg
    #
    # def mfish_kg_f(self):
    #     """
    #     Medium fish growth rate constant
    #     :return:
    #     """
    #     if self.water_temp < 17.5:
    #         self.mfish_kg = 0.0005 * self.mfish_wb ** -0.2
    #     else:
    #         self.mfish_kg = 0.00251 * self.mfish_wb ** -0.2
    #     return self.mfish_kg
    #
    # def lfish_kg_f(self):
    #     """
    #     Medium fish growth rate constant
    #     :return:
    #     """
    #     if self.water_temp < 17.5:
    #         self.lfish_kg = 0.0005 * self.lfish_wb ** -0.2
    #     else:
    #         self.lfish_kg = 0.00251 * self.lfish_wb ** -0.2
    #     return self.lfish_kg

#############################################################
#############################################################

    def animal_grow_rate_const(self, wet_wgt):
        """
        :description Aquatic animal/organism growth rate constant
        :unit (per day)
        :expression Kabam Eq. A7.1 & A7.2
        :param wet_wgt: wet weight of animal/organism (kg)
        :param water_temp: water temperature (degrees C)
        :return:
        """

        growth_rate = pd.Series([], dtype = 'float')

        if self.water_temp < 17.5:
            growth_rate = 0.0005 * (wet_wgt ** -0.2)
        else:
            growth_rate = 0.00251 * (wet_wgt ** -0.2)
        return growth_rate

##############################################################
    # def ed_zoo_f(self):
    #     """
    #     Zooplankton dietary pesticide transfer efficiency
    #     :return:
    #     """
    #     self.ed_zoo = 1 / ((.0000003) * self.log_kow + 2.0)
    #     return self.ed_zoo
    #
    # def ed_beninv_f(self):
    #     """
    #     Zoo plankton dietary pesticide transfer efficiency
    #     :return:
    #     """
    #     self.ed_beninv = 1 / (.0000003 * self.log_kow + 2.0)
    #     return self.ed_beninv
    #
    # def ed_ff_f(self):
    #     """
    #     Filter feeder dietary pesticide transfer efficiency
    #     :return:
    #     """
    #     self.ed_ff = 1 / (.0000003 * self.log_kow + 2.0)
    #     return self.ed_ff
    #
    # def ed_sf_f(self):
    #     """
    #     Small fish dietary pesticide transfer efficiency
    #     :return:
    #     """
    #     self.ed_sf = 1 / (.0000003 * self.log_kow + 2.0)
    #     return self.ed_sf
    #
    # def ed_mf_f(self):
    #     """
    #     Medium fish dietary pesticide transfer efficiency
    #     :return:
    #     """
    #     self.ed_mf = 1 / (.0000003 * self.log_kow + 2.0)
    #     return self.ed_mf
    #
    # def ed_lf_f(self):
    #     """
    #     Large fish dietary pesticide transfer efficiency
    #     :return:
    #     """
    #     self.ed_lf = 1 / (.0000003 * self.log_kow + 2.0)
    #     return self.ed_lf

###############################################################
###############################################################
    def dietary_trans_eff(self):
        """
        :description Aquatic animal/organizm dietary pesticide transfer efficiency
        :unit fraction
        :expression Kabam Eq. A8a (Ed)
        :param kow: octanol-water partition coefficient ()
        :return:
        """

        trans_eff = pd.Series([], dtype = 'float')

        trans_eff = 1 / (.0000003 * self.kow + 2.0)
        return trans_eff

##############################################################
    # def gd_zoo_f(self):
    #     """
    #     Zooplankton feeding rate
    #     :return:
    #     """
    #     self.gd_zoo = 0.022 * self.zoo_wb ** 0.85 * math.exp(0.06 * self.water_temp)
    #     return self.gd_zoo
    #
    # def gd_beninv_f(self):
    #     """
    #     Zooplankton feeding rate
    #     :return:
    #     """
    #     self.gd_beninv = 0.022 * self.beninv_wb ** 0.85 * math.exp(0.06 * self.water_temp)
    #     return self.gd_beninv
    #
    # def gd_sf_f(self):
    #     """
    #     Small fish feeding rate
    #     :return:
    #     """
    #     self.gd_sf = 0.022 * self.sfish_wb ** 0.85 * math.exp(0.06 * self.water_temp)
    #     return self.gd_sf
    #
    # def gd_mf_f(self):
    #     """
    #     Medium fish feeding rate
    #     :return:
    #     """
    #     self.gd_mf = 0.022 * self.mfish_wb ** 0.85 * math.exp(0.06 * self.water_temp)
    #     return self.gd_mf
    #
    # def gd_lf_f(self):
    #     """
    #     Large fish feeding rate
    #     :return:
    #     """
    #     self.gd_lf = 0.022 * self.lfish_wb ** 0.85 * math.exp(0.06 * self.water_temp)
    #     return self.gd_lf
    #
    #
    # ##filterfeeder calcs
    # def gd_ff_f(self):
    #     """
    #     Filter feeder feeding rate
    #     :return:
    #     """
    #     self.gd_ff = self.gv_filterfeeders * self.conc_ss * 1
    #     return self.gd_ff

################################################################
################################################################
    def aq_animal_feeding_rate(self, wet_wgt):
        """
        :description Aquatic animal feeding rate (except filterfeeders)
        :unit kg/d
        :expression Kabam Eq. A8b1 (Gd)
        :param wet_wgt: wet weight of animal/organism (kg)
        :return:
        """

        feeding_rate = pd.Series([], dtype = 'float')

        feeding_rate = 0.022 * wet_wgt ** 0.85 * math.exp(0.06 * self.water_temp)
        return feeding_rate

    def filterfeeders_feeding_rate(self):
        """
        :description Filter feeder feeding rate
        :unit kg/d
        :expression Kabam Eq. A8b2 (Gd)
        :param self.gv_filterfeeders: filterfeeder ventilation rate (L/d)
        :param self.conc_ss: Concentration of Suspended Solids (Css - kg/L)
        :param particle_scav_eff: efficiency of scavenging of particles absorbed from water (fraction)
        :return:
        """

        feeding_rate = pd.Series([], dtype = 'float')

        feeding_rate = self.gv_filterfeeders * self.conc_ss * self.particle_scav_eff
        return feeding_rate


#################################################################
    # def zoo_kd_f(self):
    #     """
    #     Zooplankton rate constant pesticide uptake by food ingestion
    #     :return:
    #     """
    #     self.zoo_kd = self.ed_zoo * (self.gd_zoo / self.zoo_wb)
    #     return self.zoo_kd
    #
    # def beninv_kd_f(self):
    #     """
    #     Zooplankton rate constant pesticide uptake by food ingestion
    #     :return:
    #     """
    #     self.beninv_kd = self.ed_beninv * (self.gd_beninv / self.beninv_wb)
    #     return self.beninv_kd
    #
    # def filterfeeders_kd_f(self):
    #     """
    #     Filter feeder rate constant pesticide uptake by food ingestion
    #     :return:
    #     """
    #     self.filterfeeders_kd = self.ed_ff * (self.gd_ff / self.filterfeeders_wb)
    #     return self.filterfeeders_kd
    #
    # def sfish_kd_f(self):
    #     """
    #     Small fish rate constant pesticide uptake by food ingestion
    #     :return:
    #     """
    #     self.sfish_kd = self.ed_sf * self.gd_sf / self.sfish_wb
    #     return self.sfish_kd
    #
    # def mfish_kd_f(self):
    #     """
    #     Medium fish rate constant pesticide uptake by food ingestion
    #     :return:
    #     """
    #     self.mfish_kd = self.ed_mf * self.gd_mf / self.mfish_wb
    #     return self.mfish_kd
    #
    # def lfish_kd_f(self):
    #     """
    #     Large fish rate constant pesticide uptake by food ingestion
    #     :return:
    #     """
    #     self.lfish_kd = self.ed_lf * self.gd_lf / self.lfish_wb
    #     return self.lfish_kd

##################################################################
##################################################################
    def diet_uptake_rate_const(self, dietary_trans_eff, feeding_rate, wet_wgt):
        """
        :description Pesticide uptake rate constant for uptake through ingestion of food rate
        :unit (kg food)/(kg organism - day)
        :expression Kabam Eq. A8 (kD)
        :param wet weight of aquatic animal/organism (kg)
        :param dietary_trans_eff: dietary pesticide transfer efficiency (fraction)
        :param feeding rate: animal/organism feeding rate (kg/d)
        :return:
        """
        dietary_uptake_constantt = pd.Series([], dtype = 'float')

        dietary_uptake_constant = dietary_trans_eff * feeding_rate / wet_wgt
        return dietary_uptake_constant

###################################################################
    # #methods for calculating overall content of lipids/NLOM/Water in aquatic animal/organism diet
    #
    # #zooplankton
    # def v_ld_zoo_f(self):
    #     """
    #     Overall lipid content of diet
    #     :return:
    #     """
    #     self.v_ld_zoo = self.zoo_diet_sediment * self.sediment_lipid + self.zoo_diet_phyto * self.phytoplankton_lipid
    #     return self.v_ld_zoo
    #
    # def v_nd_zoo_f(self):
    #     """
    #     Overall nonlipid content of diet
    #     :return:
    #     """
    #     self.v_nd_zoo = self.zoo_diet_sediment * self.sediment_nlom + self.zoo_diet_phyto * self.phytoplankton_nlom
    #     return self.v_nd_zoo
    #
    # def v_wd_zoo_f(self):
    #     """
    #     Overall water content of diet
    #     :return:
    #     """
    #     self.v_wd_zoo = self.zoo_diet_sediment * self.sediment_water + self.zoo_diet_phyto * self.phytoplankton_water
    #     return self.v_wd_zoo
    #
    # #####invertebrates
    # def v_ld_beninv_f(self):
    #     """
    #     Overall lipid content of diet
    #     :return:
    #     """
    #     self.v_ld_beninv = self.beninv_diet_sediment * self.sediment_lipid + self.beninv_diet_phytoplankton * self.phytoplankton_lipid + self.beninv_diet_zooplankton * self.zoo_lipid
    #     return self.v_ld_beninv
    #
    # def v_nd_beninv_f(self):
    #     """
    #     Overall nonlipid content of diet
    #     :return:
    #     """
    #     self.v_nd_beninv = self.beninv_diet_sediment * self.sediment_nlom + self.beninv_diet_phytoplankton * self.phytoplankton_nlom + self.beninv_diet_zooplankton * self.zoo_nlom
    #     return self.v_nd_beninv
    #
    # def v_wd_beninv_f(self):
    #     """
    #     Overall water content of diet
    #     :return:
    #     """
    #     self.v_wd_beninv = self.beninv_diet_sediment * self.sediment_water + self.beninv_diet_phytoplankton * self.phytoplankton_water + self.beninv_diet_zooplankton * self.zoo_water
    #     return self.v_wd_beninv
    #
    # #filterfeeders
    # def v_ld_ff_f(self):
    #     """
    #     Overall lipid content of diet
    #     :return:
    #     """
    #     self.v_ld_ff = self.filterfeeders_diet_sediment * self.sediment_lipid + self.filterfeeders_diet_phytoplankton * self.phytoplankton_lipid + self.filterfeeders_diet_zooplankton * self.zoo_lipid
    #     return self.v_ld_ff
    #
    # def v_nd_ff_f(self):
    #     """
    #     Overall nonlipid content of diet
    #     :return:
    #     """
    #     self.v_nd_ff = self.filterfeeders_diet_sediment * self.sediment_nlom + self.filterfeeders_diet_phytoplankton * self.phytoplankton_nlom + self.filterfeeders_diet_zooplankton * self.zoo_nlom
    #     return self.v_nd_ff
    #
    # def v_wd_ff_f(self):
    #     """
    #     Overall water content of diet
    #     :return:
    #     """
    #     self.v_wd_ff = self.filterfeeders_diet_sediment * self.sediment_water + self.filterfeeders_diet_phytoplankton * self.phytoplankton_water + self.filterfeeders_diet_zooplankton * self.zoo_water
    #     return self.v_wd_ff
    #
    # #small fish
    # def v_ld_sf_f(self):
    #     """
    #     Small fish lipid
    #     :return:
    #     """
    #     self.v_ld_sf = self.sfish_diet_sediment * self.sediment_lipid + self.sfish_diet_phytoplankton * self.phytoplankton_lipid + self.sfish_diet_benthic_invertebrates * self.beninv_lipid + self.sfish_diet_zooplankton * self.zoo_lipid + self.sfish_diet_filter_feeders * self.filterfeeders_lipid
    #     return self.v_ld_sf
    #
    # def v_nd_sf_f(self):
    #     """
    #     Overall nonlipid content of diet
    #     :return:
    #     """
    #     self.v_nd_sf = self.sfish_diet_sediment * self.sediment_nlom + self.sfish_diet_phytoplankton * self.phytoplankton_nlom + self.sfish_diet_benthic_invertebrates * self.beninv_nlom + self.sfish_diet_zooplankton * self.zoo_nlom + self.sfish_diet_filter_feeders * self.filterfeeders_nlom
    #     return self.v_nd_sf
    #
    # def v_wd_sf_f(self):
    #     """
    #     Overall water content of diet
    #     :return:
    #     """
    #     self.v_wd_sf = self.sfish_diet_sediment * self.sediment_water + self.sfish_diet_phytoplankton * self.phytoplankton_water + self.sfish_diet_benthic_invertebrates * self.beninv_water + self.sfish_diet_zooplankton * self.zoo_water + self.sfish_diet_filter_feeders * self.filterfeeders_water
    #     return self.v_wd_sf
    #
    # #medium fish
    # def v_ld_mf_f(self):
    #     """
    #     Overall lipid content of diet
    #     :return:
    #     """
    #     self.v_ld_mf = self.mfish_diet_sediment * self.sediment_lipid + self.mfish_diet_phytoplankton * self.phytoplankton_lipid + self.mfish_diet_benthic_invertebrates * self.beninv_lipid + self.mfish_diet_zooplankton * self.zoo_lipid + self.mfish_diet_filter_feeders * self.filterfeeders_lipid + self.mfish_diet_small_fish * self.sfish_lipid
    #     return self.v_ld_mf
    #
    # def v_nd_mf_f(self):
    #     """
    #     Overall nonlipid content of diet
    #     :return:
    #     """
    #     self.v_nd_mf = self.mfish_diet_sediment * self.sediment_nlom + self.mfish_diet_phytoplankton * self.phytoplankton_nlom + self.mfish_diet_benthic_invertebrates * self.beninv_nlom + self.mfish_diet_zooplankton * self.zoo_nlom + self.mfish_diet_filter_feeders * self.filterfeeders_nlom + self.mfish_diet_small_fish * self.sfish_nlom
    #     return self.v_nd_mf
    #
    # def v_wd_mf_f(self):
    #     """
    #     Overall water content of diet
    #     :return:
    #     """
    #     self.v_wd_mf = self.mfish_diet_sediment * self.sediment_water + self.mfish_diet_phytoplankton * self.phytoplankton_water + self.mfish_diet_benthic_invertebrates * self.beninv_water + self.mfish_diet_zooplankton * self.zoo_water + self.mfish_diet_filter_feeders * self.filterfeeders_water + self.mfish_diet_small_fish * self.sfish_water
    #     return self.v_wd_mf
    #
    # #large fish
    # def v_ld_lf_f(self):
    #     """
    #     Overall lipid content of diet
    #     :return:
    #     """
    #     self.v_ld_lf = self.lfish_diet_sediment * self.sediment_lipid + self.lfish_diet_phytoplankton * self.phytoplankton_lipid + self.lfish_diet_benthic_invertebrates * self.beninv_lipid + self.lfish_diet_zooplankton * self.zoo_lipid + self.lfish_diet_filter_feeders * self.filterfeeders_lipid + self.lfish_diet_small_fish * self.sfish_lipid + self.lfish_diet_medium_fish * self.mfish_lipid
    #     return self.v_ld_lf
    #
    # def v_nd_lf_f(self):
    #     """
    #     Overall nonlipid content of diet
    #     :return:
    #     """
    #     self.v_nd_lf = self.lfish_diet_sediment * self.sediment_nlom + self.lfish_diet_phytoplankton * self.phytoplankton_nlom + self.lfish_diet_benthic_invertebrates * self.beninv_nlom + self.lfish_diet_zooplankton * self.zoo_nlom + self.lfish_diet_filter_feeders * self.filterfeeders_nlom + self.lfish_diet_small_fish * self.sfish_nlom + self.lfish_diet_medium_fish * self.mfish_nlom
    #     return self.v_nd_lf
    #
    # def v_wd_lf_f(self):
    #     """
    #     Overall water content of diet
    #     :return:
    #     """
    #     self.v_wd_lf = self.lfish_diet_sediment * self.sediment_water + self.lfish_diet_phytoplankton * self.phytoplankton_water + self.lfish_diet_benthic_invertebrates * self.beninv_water + self.lfish_diet_zooplankton * self.zoo_water + self.lfish_diet_filter_feeders * self.filterfeeders_water + self.lfish_diet_small_fish * self.sfish_water + self.lfish_diet_medium_fish * self.mfish_water
    #     return self.v_wd_lf
###################################################################
###################################################################
    def overall_diet_content(self, diet_fraction, content_fraction):
        """
        :description Overall fraction of aquatic animal/organism diet attibuted to diet food component (i.e., lipids or NLOM or water)
        :unit kg/kg
        :expression not shown in Kabam documentation: it is associated with Kabam Eq. A9
                    overall_diet_content is equal to the sum over dietary elements
        :           of (fraction of diet) * (content in diet element); for example zooplankton ingest seidment and
        :           phytoplankton, thus the overall lipid content of the zooplankton diet equals
        :           (fraction of sediment in zooplankton diet) * (fraction of lipids in sediment) +
        :           (fraction of phytoplankton in zooplankton diet) * (fraction of lipids in phytoplankton)
        :param diet_fraction: list of values representing fractions of aquatic animal/organism diet attibuted
                              to each element of diet
        :param content_fraction: list of values representing fraction of diet element attributed to a specific
                                 component of that diet element (e.g., lipid, NLOM, or water)
        :return:
        """

        overall_diet_fraction = pd.Series([], dtype = 'float')
        overall_diet_fraction = 0.0

        for i in range(len(diet_fraction)):
            overall_diet_fraction = overall_diet_fraction + diet_fraction[i] * content_fraction[i]

        return overall_diet_fraction
###################################################################
    # def gf_zoo_f(self):
    #     """
    #     Egestion rate of fecal matter
    #     :return:
    #     """
    #     self.gf_zoo = (((1 - .72) * self.v_ld_zoo) + ((1 - .72) * self.v_nd_zoo) + (
    #         (1 - .25) * self.v_wd_zoo)) * self.gd_zoo
    #     # rr=self.zoo_diet_phyto
    #     # if rr==0:
    #     #   rr==0.00000001
    #     # return rr
    #     return self.gf_zoo
    #
    # def gf_beninv_f(self):
    #     """
    #     Egestion rate of fecal matter
    #     :return:
    #     """
    #     self.gf_beninv = ((1 - 0.75) * self.v_ld_beninv + (1 - 0.75) * self.v_nd_beninv + (
    #         1 - 0.25) * self.v_wd_beninv) * self.gd_beninv
    #     return self.gf_beninv
    #
    # def gf_ff_f(self):
    #     """
    #     Gf ff
    #     :return:
    #     """
    #     self.gf_ff = ((1 - 0.75) * self.v_ld_ff + (1 - 0.75) * self.v_nd_ff + (1 - 0.25) * self.v_wd_ff) * self.gd_ff
    #     return self.gf_ff
    #
    # def gf_sf_f(self):
    #     """
    #     Small fish
    #     :return:
    #     """
    #     self.gf_sf = ((1 - 0.92) * self.v_ld_sf + (1 - 0.6) * self.v_nd_sf + (1 - 0.25) * self.v_wd_sf) * self.gd_sf
    #     return self.gf_sf
    #
    # def gf_mf_f(self):
    #     """
    #     Medium fish
    #     :return:
    #     """
    #     self.gf_mf = ((1 - 0.92) * self.v_ld_mf + (1 - 0.6) * self.v_nd_mf + (1 - 0.25) * self.v_wd_mf) * self.gd_mf
    #     return self.gf_mf
    #
    # def gf_lf_f(self):
    #     """
    #     Large fiah
    #     :return:
    #     """
    #     self.gf_lf = ((1 - 0.92) * self.v_ld_lf + (1 - 0.6) * self.v_nd_lf + (1 - 0.25) * self.v_wd_lf) * self.gd_lf
    #     return self.gf_lf

#####################################################################
#####################################################################
    def fecal_egestion_rate_factor(self, epsilonL, epsilonN, epsilonW, diet_lipid, diet_nlom, diet_water):
        """
        :description Aquatic animal/organism egestion rate of fecal matter factor (to be multiplied by the
                     feeding rate to calculate egestion rate of fecal matter)
        :unit (kg lipid)/[(kg diet)
        :expression Kabam Eq. A9 (GF)
        :param epsilonL: dietary assimilation rate of lipids (fraction)
        :param epsilonN: dietary assimilation rate of NLOM (fraction)
        :param epsilonW: dietary assimilation rate of water (fraction)
        :param diet_lipid; lipid content of aquatic animal/organism diet (fraction)
        :param diet_nlom NLOM content of aquatic animal/organism diet (fraction)
        :param diet_water water content of aquatic animal/organism diet (fraction)
        :return:
        """

        rate_factor = pd.Series([], dtype = 'float')

        rate_factor = (((1 - epsilonL) * diet_lipid) + ((1 - epsilonN) * diet_nlom) + (
            (1 - epsilonW) * diet_water))
        return rate_factor

###################################################################

    # def vlg_zoo_f(self):
    #     """
    #     Lipid content in gut
    #     :return:
    #     """
    #     self.vlg_zoo = (1 - 0.72) * self.v_ld_zoo * self.gd_zoo / self.gf_zoo
    #     return self.vlg_zoo
    #
    # def vng_zoo_f(self):
    #     """
    #     Non lipid content in gut
    #     :return:
    #     """
    #     self.vng_zoo = (1 - 0.72) * self.v_nd_zoo * self.gd_zoo / self.gf_zoo
    #     return self.vng_zoo
    #
    # def vwg_zoo_f(self):
    #     """
    #     Water content in the gut
    #     :return:
    #     """
    #     self.vwg_zoo = (1 - 0.25) * self.v_wd_zoo * self.gd_zoo / self.gf_zoo
    #     return self.vwg_zoo
    #
    # def vlg_beninv_f(self):
    #     """
    #     Lipid content in gut
    #     :return:
    #     """
    #     self.vlg_beninv = (1 - 0.75) * self.v_ld_beninv * self.gd_beninv / self.gf_beninv
    #     return self.vlg_beninv
    #
    # def vng_beninv_f(self):
    #     """
    #     Non lipid content in gut
    #     :return:
    #     """
    #     self.vng_beninv = (1 - 0.75) * self.v_nd_beninv * self.gd_beninv / self.gf_beninv
    #     return self.vng_beninv
    #
    # def vwg_beninv_f(self):
    #     """
    #     Water content in the gut
    #     :return:
    #     """
    #     self.vwg_beninv = (1 - 0.25) * self.v_wd_beninv * self.gd_beninv / self.gf_beninv
    #     return self.vwg_beninv
    #
    # def vlg_ff_f(self):
    #     """
    #     Lipid content in gut
    #     :return:
    #     """
    #     self.vlg_ff = (1 - 0.75) * self.v_ld_ff * self.gd_ff / self.gf_ff
    #     return self.vlg_ff
    #
    # def vng_ff_f(self):
    #     """
    #     Non lipid content in gut
    #     :return:
    #     """
    #     self.vng_ff = (1 - 0.75) * self.v_nd_ff * self.gd_ff / self.gf_ff
    #     return self.vng_ff
    #
    # def vwg_ff_f(self):
    #     """
    #     Water content in the gut
    #     :return:
    #     """
    #     self.vwg_ff = (1 - 0.25) * self.v_wd_ff * self.gd_ff / self.gf_ff
    #     return self.vwg_ff
    #
    # def vlg_sf_f(self):
    #     """
    #     Lipid content in gut
    #     :return:
    #     """
    #     self.vlg_sf = (1 - 0.92) * self.v_ld_sf * self.gd_sf / self.gf_sf
    #     return self.vlg_sf
    #
    # def vng_sf_f(self):
    #     """
    #     Non lipid content in gut
    #     :return:
    #     """
    #     self.vng_sf = (1 - 0.6) * self.v_nd_sf * self.gd_sf / self.gf_sf
    #     return self.vng_sf
    #
    # def vwg_sf_f(self):
    #     """
    #     Water content in the gut
    #     :return:
    #     """
    #     self.vwg_sf = (1 - 0.25) * self.v_wd_sf * self.gd_sf / self.gf_sf
    #     return self.vwg_sf
    #
    # def vlg_mf_f(self):
    #     """
    # # lipid content in gut
    #     :return:
    #     """
    #     self.vlg_mf = (1 - 0.92) * self.v_ld_mf * self.gd_mf / self.gf_mf
    #     return self.vlg_mf
    #
    # def vng_mf_f(self):
    #     """
    #     Non lipid content in gut
    #     :return:
    #     """
    #     self.vng_mf = (1 - 0.6) * self.v_nd_mf * self.gd_mf / self.gf_mf
    #     return self.vng_mf
    #
    # def vwg_mf_f(self):
    #     """
    #     Water content in the gut
    #     :return:
    #     """
    #     self.vwg_mf = (1 - 0.25) * self.v_wd_mf * self.gd_mf / self.gf_mf
    #     return self.vwg_mf
    #
    # def vlg_lf_f(self):
    #     """
    #     Lipid content in gut
    #     :return:
    #     """
    #     self.vlg_lf = (1 - 0.92) * self.v_ld_lf * self.gd_lf / self.gf_lf
    #     return self.vlg_lf
    #
    # def vng_lf_f(self):
    #     """
    #     Non lipid content in gut
    #     :return:
    #     """
    #     self.vng_lf = (1 - 0.6) * self.v_nd_lf * self.gd_lf / self.gf_lf
    #     return self.vng_lf
    #
    # def vwg_lf_f(self):
    #     """
    #     Water content in the gut
    #     :return:
    #     """
    #     self.vwg_lf = (1 - 0.25) * self.v_wd_lf * self.gd_lf / self.gf_lf
    #     return self.vwg_lf

#####################################################################
#####################################################################
    def diet_elements_gut(self, epsilon, overall_diet_content, egestion_rate_factor):
        """
        :description Fraction of diet elements (i.e., lipid, NLOM, water) in the gut
        :unit (kg lipid) / (kg digested wet weight)
        :expression Kabam Eq. A9 (VLG, VNG, VWG)
        :param epsilon relevant dietary assimilation rate (fraction)
        :param overall_diet_content relevant overall diet content of diet element (kg/kg)
        :param egestion_rate_factor relevant: Aquatic animal/organism egestion rate of fecal matter factor
        :return:
        """

        gut_content = pd.Series([], dtype = 'float')

        gut_content = ((1. - epsilon) * overall_diet_content) / egestion_rate_factor
        return gut_content


####################################################################

    # def kgb_zoo_f(self):
    #     """
    #     Partition coefficient of the pesticide between the gastrointenstinal track and the organism
    #     :return:
    #     """
    #     self.kgb_zoo = (self.vlg_zoo * self.log_kow + self.vng_zoo * 0.035 * self.log_kow + self.vwg_zoo) / (
    #         self.zoo_lipid * self.log_kow + self.zoo_nlom * 0.035 * self.log_kow + self.zoo_water)
    #     return self.kgb_zoo
    #
    # def kgb_beninv_f(self):
    #     """
    #     Kgb ben inverts
    #     :return:
    #     """
    #     self.kgb_beninv = (self.vlg_beninv * self.log_kow + self.vng_beninv * 0.035 * self.log_kow + self.vwg_beninv) / (
    #         self.beninv_lipid * self.log_kow + self.beninv_nlom * 0.035 * self.log_kow + self.beninv_water)
    #     return self.kgb_beninv
    #
    # def kgb_ff_f(self):
    #     """
    #     Kgb ff
    #     :return:
    #     """
    #     self.kgb_ff = (self.vlg_ff * self.log_kow + self.vng_ff * 0.035 * self.log_kow + self.vwg_ff) / (
    #         self.filterfeeders_lipid * self.log_kow + self.filterfeeders_nlom * 0.035 * self.log_kow + self.filterfeeders_water)
    #     return self.kgb_ff
    #
    # def kgb_sf_f(self):
    #     """
    #     Small fish
    #     :return:
    #     """
    #     self.kgb_sf = (self.vlg_sf * self.log_kow + self.vng_sf * 0.035 * self.log_kow + self.vwg_sf) / (
    #         self.sfish_lipid * self.log_kow + self.sfish_nlom * 0.035 * self.log_kow + self.sfish_water)
    #     return self.kgb_sf
    #
    # def kgb_mf_f(self):
    #     """
    #     Medium fish
    #     :return:
    #     """
    #     self.kgb_mf = (self.vlg_mf * self.log_kow + self.vng_mf * 0.035 * self.log_kow + self.vwg_mf) / (
    #         self.mfish_lipid * self.log_kow + self.mfish_nlom * 0.035 * self.log_kow + self.mfish_water)
    #     return self.kgb_mf
    #
    # def kgb_lf_f(self):
    #     """
    #     Large fish
    #     :return:
    #     """
    #     self.kgb_lf = (self.vlg_lf * self.log_kow + self.vng_lf * 0.035 * self.log_kow + self.vwg_mf) / (
    #         self.lfish_lipid * self.log_kow + self.lfish_nlom * 0.035 * self.log_kow + self.mfish_water)
    #     return self.kgb_lf
#####################################################################
#####################################################################
    def gut_organism_partition_coef(self, gut_lipid, gut_nlom, gut_water, pest_kow, beta,
                                    organism_lipid, organism_nlom, organism_water):
        """
        :description Partition coefficient of the pesticide between the gastrointenstinal track and the organism
        :unit none
        :expression Kabam Eq. A9 (KGB)
        :param gut_lipid: lipid content in the gut
        :param gut_nlom: nlom content in the gut
        :param gut_water: water content in the gut
        :param pest_kow: pesticide Kow
        :param beta: proportionality constant expressing the sorption capacity of NLOM to that of octanol
        :param organism_lipid: lipid content in the whole organism
        :param organism_nlom: nlom content in the whole organism
        :param organism_water: water content in the whole organism
        :return:
        """

        partition_coef = pd.Series([], dtype = 'float')

        partition_coef = (pest_kow * (gut_lipid + beta * gut_nlom) + gut_water) /  \
                         (pest_kow * (organism_lipid + beta * organism_nlom) + organism_water)
        return partition_coef

#####################################################################

    # def zoo_ke_f(self):
    #     """
    #     Dietary elimination rate constant
    #     :return:
    #     """
    #     self.zoo_ke = self.gf_zoo * self.ed_zoo * self.kgb_zoo / self.zoo_wb
    #     #   self.zoo_ke = self.zoo_diet_phyto
    #     return self.zoo_ke
    #
    # def beninv_ke_f(self):
    #     """
    #     Dietary elimination rate constant
    #     :return:
    #     """
    #     self.beninv_ke = self.gf_beninv * self.ed_beninv * (self.kgb_beninv / self.beninv_wb)
    #     return self.beninv_ke
    #
    # def filterfeeders_ke_f(self):
    #     """
    #     Ke ff
    #     :return:
    #     """
    #     self.filterfeeders_ke = (self.gf_ff * self.ed_ff * self.kgb_ff) / self.filterfeeders_wb
    #     return self.filterfeeders_ke
    #
    # def sfish_ke_f(self):
    #     """
    #     Small fish
    #     :return:
    #     """
    #     self.sfish_ke = self.gf_sf * self.ed_sf * (self.kgb_sf / self.sfish_wb)
    #     return self.sfish_ke
    #
    # def mfish_ke_f(self):
    #     """
    #
    #     :return:
    #     """
    #     self.mfish_ke = self.gf_mf * self.ed_mf * (self.kgb_mf / self.mfish_wb)
    #     return self.mfish_ke
    #
    #
    # def lfish_ke_f(self):
    #     """
    #     Large fish
    #     :return:
    #     """
    #     self.lfish_ke = self.gf_lf * self.ed_lf * (self.kgb_lf / self.lfish_wb)
    #     return self.lfish_ke

######################################################################
######################################################################
    def fecal_elim_rate_const(self, fecal_egestion_rate, diet_trans_eff, part_coef, wet_wgt):
        """
        :description Rate constant for elimination of the pesticide through excretion of contaminated feces
        :unit per day
        :param fecal_egestion_rate: egestion rate of fecal matter (kg feces)/(kg organism-day)
        :param diet_trans_eff: dietary pesticide transfer efficiency (fraction)
        :param part_coef: gut - partition coefficient of the pesticide between the gastrointestinal tract
                          and the organism (-)
        :param wet_wgt: wet weight of organism (kg)
        :return:
        """

        elim_rate_const = pd.Series([], dtype = 'float')

        elim_rate_const = fecal_egestion_rate * diet_trans_eff * (part_coef / wet_wgt)
        return elim_rate_const

######################################################################
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

#############################################################
#############################################################
    def frac_pest_freely_diss(self):
        """
        :description Calculate Fraction of pesticide freely dissolved in water column (that can be
                     absorbed via membrane diffusion)
        :unit fraction
        :expression Kabam Eq. A2
        :param conc_poc: Concentration of Particulate Organic Carbon in water column (kg OC/L)
        :param kow: octonal-water partition coefficient (-)
        :param conc_doc: Concentration of Dissolved Organic Carbon in water column (kg OC/L)
        :return:
        """
        frac_pest_diss_ = pd.Series([], dtype = 'float')

        frac_pest_diss = 1 / (1 + (self.conc_poc * self.alpha_poc * self.kow) + (self.conc_doc * self.alpha_doc * self.kow))
        return frac_pest_diss

#######################################################################
    def water_d(self):
        """
        concentration of freely dissolved pesticide in overlying water column
        :return:
        """
        self.water_d = self.phi * self.water_column_eec * 1000000 ## THIS SHOULD BE / 1000000. (see cell C9 of 'Parameters & Calculations of OPP Model spreadsheet)
        return self.water_d

##########################################################
###########################################################
    def conc_freely_diss_watercol(self):
        """
        :description Concentration of freely dissolved pesticide in overlying water column
        :unit g/L
        :expression Kabam A1 (product of terms - [phi * water_column_eec], used in Eqs F2 & F4)
        :param phi: Fraction of pesticide freely dissolved in water column (that can be
                    absorbed via membrane diffusion) (fraction)
        :param water_column_eec: Water Column 1-in-10 year EECs (ug/L)
        :param 1000000: conversion factor from ug/L to g/L
        :return:
        """
        conc_diss_watercol = pd.Series([], dtype = 'float')

        conc_diss_watercol = self.phi * self.water_column_eec / 1000000.
        return conc_diss_watercol

#####################################################################
    def c_soc_f(self):
        """
        Normalized pesticide concentration in sediment
        Eq. A4a
        :return:
        """
        self.c_soc = self.k_oc * self.pore_water_eec #SHOULD BE /1000000.
        return self.c_soc

######################################################################
######################################################################
    def  conc_sed_norm_4oc(self):
        """
        :description Pesticide concentration in sediment normalized for organic carbon
        :unit g/(kg OC)
        :expression Kabam Eq. A4a
        :param pore_water_eec: freely dissolved pesticide concentration in sediment pore water
        :param k_oc: organic carbon partition coefficient (L/kg OC)
        :param 1000000: conversion factor from ug/L to g/L

        :return:
        """
        conc_diss_sed = pd.Series([], dtype = 'float')

        conc_diss_sed = self.k_oc * self.pore_water_eec / 1000000.
        return conc_diss_sed
################################################################

    def c_s_f(self):
        """
        Calculate concentration of chemical in solid portion of sediment
        Eq. A4
        :return:
        """
        self.c_s = self.c_soc * self.sediment_oc
        return self.c_s

#####################################################################
#####################################################################
    def conc_sed_dry_wgt(self):
        """
        :description Calculate concentration of chemical in solid portion of sediment
        :unit g/(kg dry)
        :expression Kabam Eq. A4
        :param c_soc: pesticide concentration in sediment normalized for organic carbon g/(kg OC)
        :param sediment_oc: fraction organic carbon in sediment (fraction)
        :return:
        """

        conc_sed = pd.Series([], dtype = 'float')

        conc_sed = self.c_soc * self.sediment_oc_frac
        return conc_sed

#######################################################################

                #THIS METHOD IS NOT NEEDED BECAUSE sed_om IS EQUAL TO c_soc
                #     def sed_om_f(self):
                #         """
                #         Calculate organic matter fraction in sediment
                # #?? don't see this calculation in model documentation; looks like it is same as c_soc_f
                #         :return:
                #         """
                #         self.sed_om = self.c_s / self.sediment_oc
                #         return self.sed_om

#########################################################################
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

    def cbd_zoo_f(self): #this method for zoo is inserted here because it is not applied for phytoplankton but needs to be included
        """
        Zooplankton pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_zoo = (0 * (1.0) * self.phi * self.water_column_eec + (0 * self.pore_water_eec) + (self.zoo_kd * (self.diet_zoo))) / (
            self.zoo_k2 + self.zoo_ke + self.kg_zoo + 0)
        # print "cbd_zoo =", self.cbd_zoo
        return self.cbd_zoo

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
#?? why no 1e6 factor here as in 'cbaf_phytoplankton_f' or vice versa
        self.cbsafl_phytoplankton = self.cb_phytoplankton / self.sed_om
        return self.cbsafl_phytoplankton

    def bmf_zoo_f(self): #zoo example is used here because phytoplankton does not have a bmf
        """
        Zooplankton biomagnification factor
        :return:
        """
        self.bmf_zoo = (self.cb_zoo / self.zoo_lipid) / (
            self.zoo_diet_phyto * self.cb_phytoplankton / self.phytoplankton_lipid)
        return self.bmf_zoo

    def diet_zoo_f(self):
        """
        Diet fraction
        :return:
        """
        self.diet_zoo = self.c_s * self.zoo_diet_sediment + self.cb_phytoplankton * self.zoo_diet_phyto
        return self.diet_zoo

    def diet_beninv_f(self):
        """
        Diet fraction benthic inverts
        :return:
        """
        self.diet_beninv = self.c_s * self.beninv_diet_sediment + self.cb_phytoplankton * self.beninv_diet_phytoplankton + self.cb_zoo * self.beninv_diet_zooplankton
        return self.diet_beninv

    def diet_ff_f(self):
        """
        Diet filter feeders
        :return:
        """
        self.diet_ff = self.c_s * self.filterfeeders_diet_sediment + self.cb_phytoplankton * self.filterfeeders_diet_phytoplankton + self.cb_zoo * self.filterfeeders_diet_zooplankton + self.cb_beninv * self.filterfeeders_diet_benthic_invertebrates
        return self.diet_ff

    def diet_sf_f(self):
        """
        Diet small fish
        :return:
        """
        self.diet_sf = self.c_s * self.sfish_diet_sediment + self.cb_phytoplankton * self.sfish_diet_phytoplankton + self.cb_zoo * self.sfish_diet_zooplankton + self.cb_beninv * self.sfish_diet_benthic_invertebrates + self.cb_ff * self.sfish_diet_filter_feeders
        return self.diet_sf

    def diet_mf_f(self):
        """
        Diet medium fish
        :return:
        """
        self.diet_mf = self.c_s * self.mfish_diet_sediment + self.cb_phytoplankton * self.mfish_diet_phytoplankton + self.cb_zoo * self.mfish_diet_zooplankton + self.cb_beninv * self.mfish_diet_benthic_invertebrates + self.cb_ff * self.mfish_diet_filter_feeders + self.cb_sf * self.mfish_diet_small_fish
        return self.diet_mf

    def diet_lf_f(self):
        """
        Large fish
        :return:
        """
        self.diet_lf = self.c_s * self.lfish_diet_sediment + self.cb_phytoplankton * self.lfish_diet_phytoplankton + self.cb_zoo * self.lfish_diet_zooplankton + self.cb_beninv * self.lfish_diet_benthic_invertebrates + self.cb_ff * self.lfish_diet_filter_feeders + self.cb_sf * self.lfish_diet_small_fish + self.cb_mf * self.lfish_diet_medium_fish
        return self.diet_lf
#################################################################################
    def diet_aq_animals(self):
        """
        Large fish
        :return:
        """

## Phytoplankton bioaccumulation/concentration calculations

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

        # partition coefficient of the pesticide between the gastrointenstinal track and the organism

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

    ###### filter feeders

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

    ############# small fish

        # overall lipid content of diet

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

########################################################################
########################################################################
    def pest_conc_organism(self, k1, k2, kD, kE, kG, kM, mP, mO, diet_conc):
        """
        :description Concentration of pesticide in aquatic animal/organism
        :unit g/(kg wet weight)
        :expression Kabam Eq. A1 (CB)
        :param k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param kD: pesticide uptake rate constant for uptake through ingestion of food (kg food/(kg organism - day)
        :param kE: rate constant for elimination of the pesticide through excretion of feces (/d)
        :param kG: animal/organism growth rate constant (/d)
        :param kM: rate constant for pesticide metabolic transformation (/d)
        :param mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :param diet_conc: concentration of pesticide in overall diet of aquatic animal/organism (g/kg wet weight)
        #because phytoplankton have no diet the (Kd * SUM(Pi * Cdi)) portion of Eq. A1 is not included here
        :return:
        """
        pest_conc_organism = pd.Series([], dtype = 'float')

        pest_conc_organism = (k1 * (mO * self.phi * self.water_column_eec + (mP * self.pore_water_eec)) + kD * diet_conc) / (k2 + kE + kG + kM)
        return pest_conc_organism

    def pest_conc_diet_uptake(self, kD,  k2, kE, kG, kM, diet_conc):
        """
        :description Pesticide concentration in animal/organism originating from uptake through diet
        :unit g/kg ww
        :expression Kabam A1 (with k1 = 0)
        :param kD: pesticide uptake rate constant for uptake through ingestion of food (kg food/kg organizm - day)
        :param diet_conc: overall concentration of pesticide in diet of animal/organism (g/kg-ww)
        :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param kE: rate constant for elimination of the pesticide through excretion of feces (/d)
        :param kG: animal/organism growth rate constant (/d)
        :param kM: rate constant for pesticide metabolic transformation (/d)
        :return:
        """
        pest_conc_from_diet = pd.Series([], dtype = 'float')

        pest_conc_from_diet = (kD * diet_conc) / (k2 + kE + kG + kM)
        return pest_conc_from_diet

    def pest_conc_respir_uptake(self, k1, k2, kE, kG, kM, mP, mO):
        """
        :description Pesticide concentration in animal/organism originating from uptake through respiration
        :unit g/kg ww
        :expression Kabam A1 (with kD = 0)
        :param k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param kE: rate constant for elimination of the pesticide through excretion of feces (/d)
        :param kG: animal/organism growth rate constant (/d)
        :param kM: rate constant for pesticide metabolic transformation (/d)
        :param mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :return:
        """
        pest_conc_from_respir = pd.Series([], dtype = 'float')

        pest_conc_from_respir = (k1 * (mO * self.phi * self.water_column_eec + (mP * self.pore_water_eec)) / k2 ) / (k2 + kE + kM + kG)
        return pest_conc_from_respir

    def lipid_norm_residue_conc(self, total_conc, lipid_content):
        """
        :description Lipid normalized pesticide residue in aquatic animal/organism
        :unit ug/kg-lipid
        :expresssion represents a factor (CB/VLB) used in Kabam Eqs. F4, F5, & F6
        :param total_conc: total pesticide concentration in animal/organism (g/kg-ww)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :return:
        """
        lipid_norm_conc = pd.Series([], dtype = 'float')

        lipid_norm_conc = (total_conc / lipid_content) * self.gms_to_microgms
        return lipid_norm_conc

    def tot_bioconc_fact(self, k1, k2, mP, mO):
        """
        :description Total bioconcentration factor
        :unit (ug pesticide/kg ww) / (ug pesticide/L water)
        :expression Kabam Eq. F1
        :param k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :return:
        """
        tot_bioconc_fact = pd.Series([], dtype = 'float')

        tot_bioconc_fact = (k1 * (mO * self.phi * self.water_column_eec + mP * self.pore_water_eec) / k2 ) / self.water_column_eec
        return tot_bioconc_fact

    def lipid_norm_bioconc_fact(self, k1, k2, mP, mO, lipid_content):
        """
        :description Lipid normalized bioconcentration factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F2
        :param k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :return:
        """

        lipid_norm_bcf = pd.Series([], dtype = 'float')

        lipid_norm_bcf = ((k1 * (mO * self.phi * self.water_column_eec + mP * self.pore_water_eec) / k2 ) / lipid_content) / \
                          (self.water_column_eec * self.phi)
        return lipid_norm_bcf

    def tot_bioacc_fact(self, pest_conc):
        """
        :description Total bioaccumulation factor
        :unit (ug pesticide/kg ww) / (ug pesticide/L water)
        :expression Kabam Eq. F3
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param water_column_eec:  total pesticide concentraiton in water column above sediment (g/L)
        :return:
        """

        total_bioacc_fact = pd.Series([], dtype = 'float')

        total_bioacc_fact = pest_conc / self.water_column_eec
        return total_bioacc_fact

    def lipid_norm_bioacc_fact(self, pest_conc, lipid_content):
        """
        :description Lipid normalized bioaccumulation factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F4
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
        :return:
        """

        lipid_norm_baf = pd.Series([], dtype = 'float')

        lipid_norm_baf = (pest_conc / lipid_content) / (self.water_column_eec * self.phi)
        return lipid_norm_baf

    def biota_sed_acc_fact(self, pest_conc, lipid_content):  #cdsafl
        """
        :description Biota-sediment accumulation factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F5
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :param c_soc Pesticide concentration in sediment normalized for organic carbon content (g/kg OC)
        :return:
        """

        sediment_acc_fact = pd.Series([], dtype = 'float')

        sediment_acc_fact = (pest_conc / lipid_content) / self.c_soc
        return sediment_acc_fact

    def biomag_fact(self, pest_conc, lipid_content, lipid_norm_diet_conc):
        """
        :description Biomagnification factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/kg lipid)
        :expression Kabam Eq. F6
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :param diet_conc: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight))
        :return:
        """

        biomag_fact = pd.Series([], dtype = 'float')

        biomag_fact = (pest_conc / lipid_content) / lipid_norm_diet_conc
        return biomag_fact
#############################################################################
#these methods are not created in final Kabam model; the mweight and awight arrays are created in 'set_global_constants'
#and the conversion of concentrations (self.cb_*) is performed in the main routine
        # Mammals EECs
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

    def aweight_f(self):
        """
        Avian
        :return:
        """
        self.aweight = np.array([[0.02, 6.7, 0.07, 2.9, 1.25, 7.5]])
        return self.aweight

##############################################################################

    def dfir_f(self):
        """
        dry food ingestion rate: Mammals
        :return:
        """
        self.dfir = (0.0687 * self.mweight ** 0.822) / self.mweight
        return self.dfir
###############################################################################
###############################################################################
    def dry_food_ingest_rate_mammals(self):
        """
        :description dry food ingestion rate: Mammals (kg dry food/kg-bw day)
        :unit (kg dry food / kg-bw day)
        :expresssion  Kabam Eq. G1
        :param mammal_weights: body weight of mammal (kg)
        :return:
        """

        ingestion_rate_mammals = np.array([], dtype = 'float')

        ingestion_rate_mammals = (0.0687 * self.mammal_weights ** 0.822) / self.mammal_weights
        return ingestion_rate_mammals
####################################################################################
    def dfir_a_f(self):
        """
        dry food ingestion rate: Avian
        :return:
        """
        self.dfir_a = (0.0582 * self.aweight ** 0.651) / self.aweight
        return self.dfir_a
##############################################################################
##############################################################################
    def dry_food_ingest_rate_birds(self):
        """
        :description dry food ingestion rate: Birds (kg dry food/kg-bw day)
        :unit (kg dry food / kg-bw day)
        :expresssion  Kabam Eq. G2
        :param bird_weights: body weight of bird (kg)
        :return:
        """

        ingestion_rate_birds = np.array([], dtype = 'float')

        ingestion_rate_birds = (0.0582 * self.bird_weights ** 0.651) / self.bird_weights
        return ingestion_rate_birds
######################################################################################
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
        self.denom3 = self.denom2[:, 6]  # selects out seventh row of array which is the cumulative sums of the products
        self.denom4 = 1 - self.denom3
        # wet food ingestion rate for mammals
        self.wet_food_ingestion_m = self.dfir / self.denom4
        return self.wet_food_ingestion_m

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

#################################################################################
################################################################################
    def wet_food_ingestion_rates(self, prey_water_contents, diet_fractions, dry_food_ingestion_rates):
        """
        :description wet food ingestion rate for mammals and birds
        :unit (kg food ww / kg-bw day)
        :expresssion Kabam Eq. G3
        :param prey_water_contents: fraction of prey body weights that are water
        :param diet_fractions: fraction of predator (mammal or bird) diet attributed to individual prey
        :param dry_food_ingestion_rates: predator (mammal or bird) dry food ingestion rate (kg food dw / kg-bw day)
        :return:
        """

        wet_food_ingest_rates = np.array([], dtype = 'float')

        factor_1 = np.array([], dtype = 'float')
        factor_2 = np.array([], dtype = 'float')
        factor_3 = np.array([], dtype = 'float')
        factor_4 = np.array([], dtype = 'float')

        # calculate elemental factors of Kabam Eq. G3

        factor_1 = diet_fractions * prey_water_contents
        factor_2 = np.cumsum(factor_1, axis=1)
        factor_3 = factor_2[:, 6]  # selects out seventh row of array which is the cumulative sums of the products
        factor_4 = 1. - self.factor_3

        # wet food ingestion rate
        wet_food_ingest_rates = dry_food_ingestion_rates / factor_4
        return wet_food_ingest_rates

 ##############################################################################
    def drinking_water_intake_m_f(self):
        """
        Array of drinking water intake rate for mammals
        :return:
        """
        self.drinking_water_intake_m = .099 * self.mweight ** 0.9
        return self.drinking_water_intake_m
###############################################################################
###############################################################################
    def drinking_water_intake_mammals(self):
        """
        :description drinking water ingestion rate: Mammals
        :unit (L / day)
        :expresssion  Kabam Eq. G4
        :param mammal_weights: body weight of mammal (kg)
        :return:
        """

        water_ingestion_rate_mammals = np.array([], dtype = 'float')

        water_ingestion_rate_mammals = (0.099 * self.mammal_weights ** 0.90)
        return water_ingestion_rate_mammals
####################################################################################
    def drinking_water_intake_a_f(self):
        """
        Avian drinking water intake
        :return:
        """
        self.drinking_water_intake_a = 0.059 * self.aweight ** 0.67
        return self.drinking_water_intake_a

##############################################################################
##############################################################################
    def drinking_water_intake_birds(self):
        """
        :description drinking water ingestion rate: Birds
        :unit (L / day)
        :expresssion  Kabam Eq. G5
        :param bird_weights: body weight of bird (kg)
        :return:
        """

        water_ingestion_rate_birds = np.array([], dtype = 'float')

        water_ingestion_rate_birds = (0.059 * self.bird_weights ** 0.67)
        return water_ingestion_rate_birds
######################################################################################
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

    def db4a_f(self):
        """
        Avian
        :return:
        """
        overall_diet_conc = self.cb_a2 * self.diet_avian
        sum_diet_fracs = np.cumsum(overall_diet_conc, axis=1)
        overall_diet_conc = sum_diet_fracs[:, 6]
        # dose based  EEC
        self.db4a = (overall_diet_conc / 1000) * self.wet_food_ingestion_a + (self.water_column_eec / 1000) * (
            self.drinking_water_intake_a / self.aweight)
        return self.db4a
#######################################################################
###########################################################################
    def dose_based_eec(self, wc_eec, pest_conc_diet, diet_fraction, wet_food_ingest_rate, water_ingest_rate, body_weight):
        """
        :description dose-based EECs
        :unit (mg pesticide / kg-bw day)
        :expression Kabam Eq. G6
        :param wc_eec: water column eec (ug/L)
        :param pest_conc_diet: overall concentration of pesticide in predator (mammal or bird) diet (ug pesticide/kg-bw)
        :param diet_fraction: fraction of aquatic animal/organism in diet of predator
        :param wet_food_ingest_rate: overall food ingestion rate (wet based) of predator (food ww/day)
        :param water_ingest_rate: drinking water ingestion rate (L/day)
        :param body_weight: body weight of predator (kg)
        :return:
        """
        frac_diet_conc = np.array([], dtype = 'float')
        sum_diet_fracs = np.array([], dtype = 'float')
        overall_diet_conc = np.array([], dtype = 'float')
        dose_based_eec = np.array([], dtype = 'float')

        #calculate relevant factors
        frac_diet_conc = pest_conc_diet * diet_fraction
        sum_diet_fracs = np.cumsum(frac_diet_conc, axis=1)
        overall_diet_conc = sum_diet_fracs[:, 6]

        # dose based  EEC  (the /1000 converts ug to mg)
        dose_based_eec = (overall_diet_conc / 1000) * wet_food_ingest_rate + \
                         (((wc_eec / 1000) * water_ingest_rate) / body_weight)
        return dose_based_eec

############################################################################
    def db5_f(self):
        """
        Mammals
        :return:
        """
        # dietary based EEC
        self.db5 = self.db3 / 1000
        return self.db5

    def db5a_f(self):
        """
        Avian
        :return:
        """
        # dietary based EEC
        self.db5a = (self.db3 / 1000)
        return self.db5a
############################################################################
############################################################################
    def dietary_based_eec(self, pest_conc_diet, diet_fraction):
        """
        :description dietary-based EECs
        :unit (mg pesticide / kg-bw day)
        :expression Kabam Eq. G7
        :param pest_conc_diet: overall concentration of pesticide in predator (mammal or bird) diet (ug pesticide/kg-bw)
        :param diet_fraction: fraction of aquatic animal/organism in diet of predator
        :return:
        """
        frac_diet_conc = np.array([], dtype = 'float')
        sum_diet_fracs = np.array([], dtype = 'float')
        overall_diet_conc = np.array([], dtype = 'float')
        dietary_based_eec = np.array([], dtype = 'float')

        #calculate relevant factors
        frac_diet_conc = pest_conc_diet * diet_fraction
        sum_diet_fracs = np.cumsum(frac_diet_conc, axis=1)
        overall_diet_conc = sum_diet_fracs[:, 6]

        # dietary-based  EEC  (the /1000 converts ug to mg)
        dietary_based_eec = (overall_diet_conc / 1000)
        return dietary_based_eec

##############################################################
    def acute_dose_based_m_f(self):
        """
        Dose-based acute toxicity for mammals
        :return:
        """
        self.acute_dose_based_m = self.mammalian_ld50 * ((float(self.bw_mamm) / 1000) / self.mweight) ** 0.25
        return self.acute_dose_based_m
###############################################################################
###############################################################################
    def acute_dose_based_tox_mammals(self, ld50_mammal, tested_mammal_bw):
        """
        :description Dose-based acute toxicity for mammals
        :unit (mg/kg-bw)
        :expression Kabam Eq. G8
        :param ld50_mammal: Mammalian acute oral LD50 (mg/kg-bw)
        :param tested_mammal_bw: body weight of tested mammal (gms)
        :param mammal_weights: body weight of assessed mammal (kg)
        :return:
        """
        acute_toxicity_mammal = pd.Series([], dtype = 'float')

        acute_toxicity_mammal = ld50_mammal * ((tested_mammal_bw / 1000) / self.mammal_weights) ** 0.25
        return acute_toxicity_mammal

###########################################################################
    def acute_dose_based_a_f(self):
        """
        Dose based acute toxicity for birds
        :return:
        """
        self.acute_dose_based_a = self.avian_ld50 * (self.aweight / (float(self.bw_bird) / 1000)) ** (
            self.mineau_scaling_factor - 1)
        return self.acute_dose_based_a
#############################################################################
################################################################################
    def acute_dose_based_tox_birds(self, ld50_bird, tested_bird_bw, scaling_factor):
        """
        :description Dose-based acute toxicity for birds
        :unit (mg/kg-bw)
        :expression Kabam Eq. G9
        :param ld50_bird: avian acute oral LD50 (mg/kg-bw)
        :param tested_bird_bw: body weight of tested bird (gms)
        :param bird_weights: body weight of assessed bird (kg)
        :param scaling_factor: Chemical Specific Mineau scaling factor ()
        :return:
        """
        acute_toxicity_bird = pd.Series([], dtype = 'float')

        acute_toxicity_bird = ld50_bird * (self.bird_weights / (tested_bird_bw / 1000)) ** (scaling_factor - 1.)
        return acute_toxicity_bird

############################################################################
    def chronic_dose_based_m_f(self):
        """
        Dose based chronic toxicity for mammals
        :return:
        """
        self.chronic_dose_based_m = (self.mammalian_chronic_endpoint / 20) * (
            ((float(self.bw_mamm) / 1000) / self.mweight) ** 0.25)
        return self.chronic_dose_based_m
###################################################################################
##############################################################################
    def chronic_dose_based_tox_mammals(self, mammalian_chronic_endpt, mammalian_chronic_endpt_unit, tested_mammal_bw):
        """
        :description Dose=based chronic toxicity for mammals
        :unit (mg/kg-bw)
        :expression (non known documentation; see EPA OPP Kabam spreadsheet
        :param mammalian_chronic_endpt:
        :param mammalian_chronic_endpt_unit: ppm or mg/kg-bw
        :param tested_mammal_bw: body weight of tested mammal (gms)
        :param mammal_weights: body weight of assessed mammal(kg)
        :return:
        """
        chronic_toxicity = pd.Series([], dtype = 'float')
        # the /1000 converts gms to kg; the /20 converts ppm to mg/kg-diet
        if (mammalian_chronic_endpt_unit == 'ppm'):
            chronic_toxicity = (mammalian_chronic_endpt / 20) * (((
                (tested_mammal_bw / 1000) / self.mammal_weights)) ** 0.25)
        else:
            chronic_toxicity = (mammalian_chronic_endpt) * (((
                (tested_mammal_bw / 1000) / self.mammal_weights)) ** 0.25)
        return chronic_toxicity


##################################### RQ Values
    def acute_rq_dose_m_f(self):
        """
        RQ dose based for mammals
        :return:
        """
        self.acute_rq_dose_m = self.db4 / self.acute_dose_based_m
        return self.acute_rq_dose_m
#######################################################################
#######################################################################
    def acute_rq_dose_mammals(self):
        """
        :description Dose-based risk quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
         :param dose_based_eec_mammals: self defined
         :param acute_dose_based_tox_mammals: self defined
        :return:
        """
        acute_rq_dose_mamm = np.array([], dtype = 'float')

        acute_rq_dose_mamm = self.dose_based_eec_mammals / self.acute_dose_based_tox_mammals
        return acute_rq_dose_mamm


#######################################################################
    def chronic_rq_dose_m_f(self):
        """
        Chronic RQ
        :return:
        """
        self.chronic_rq_dose_m = self.db4 / self.chronic_dose_based_m
        return self.chronic_rq_dose_m
########################################################################
#########################################################################
    def chronic_rq_dose_mammals(self):
        """
        :description Chronic dose-based risk quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param dose_based_eec_mammals: self defined
        :param chronic_dose_based_tox_mammals: self defined
        :return:
        """
        chronic_rq_dose_mamm = np.array([], dtype = 'float')

        chronic_rq_dose_mamm = self.dose_based_eec_mammals / self.chronic_dose_based_tox_mammals
        return chronic_rq_dose_mamm

##########################################################################
    def acute_rq_diet_m_f(self):
        """
        Acute RQ diet based for mammals
        :return:
        """
        self.acute_rq_diet_m = self.db5 / self.mammalian_lc50
        return self.acute_rq_diet_m
############################################################################
############################################################################
    def acute_rq_diet_mammals(self, diet_based_eec, mammal_lc50):
        """
        :description Acute diet-based for risk quotient mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param mammal_lc50; mammalian lc50 (mg/kg-diet)
        :param diet_based_eec: diet-based eec for mammal (mg pesticide / kg-bw day)
        :note in the OPP spreadsheet 'mammal_lc50' may be input as 'N/A' or have
              a value; in the case it is assigned 'N/A' this method should assign
              'acute_rq_diet_mamm' a value of 'N/A'  -- as implemented below it will
              either assign a 'nan' or issue a divide by zero error.
        :return:
        """
        acute_rq_diet_mamm = np.array([], dtype = 'float')

        acute_rq_diet_mamm = diet_based_eec/ mammal_lc50
        return acute_rq_diet_mamm

##########################################################################
    def chronic_rq_diet_m_f(self):
        """
        Chronic RQ diet based for mammals
        :return:
        """
        self.chronic_rq_diet_m = self.db5 / self.mammalian_chronic_endpoint
        return self.chronic_rq_diet_m
############################################################################
#############################################################################
    def chronic_rq_diet_mammals(self, diet_based_eec, mammalian_chronic_endpt, mammalian_chronic_endpt_unit):
        """
        :description chronic diet-based  rist quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param mammalian_chronic_endpt:  (ppm)
        :param diet_based_eec: diet-based eec for mammal (mg pesticide / kg
        :return:
        """
        chronic_rq_diet_mamm = np.array([], dtype = 'float')
        if (mammalian_chronic_endpt_unit == 'ppm'):
            chronic_rq_diet_mamm = diet_based_eec / mammalian_chronic_endpt
        else:
            chronic_rq_diet_mamm = diet_based_eec / (mammalian_chronic_endpt * 20.)
        return chronic_rq_diet_mamm

################################################################################
    def acute_rq_dose_a_f(self):
        """
        RQ dose based for birds
        :return:
        """
        self.acute_rq_dose_a = self.db4a / self.acute_dose_based_a
        return self.acute_rq_dose_a
##################################################################################
##############################################################################
    def acute_rq_dose_birds(self):
        """
        :description Dose-based risk quotient for birds
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
         :param dose_based_eec_birds: self defined
         :param acute_dose_based_tox_birds: self defined
        :return:
        """
        acute_rq_dose_bird = np.array([], dtype = 'float')

        acute_rq_dose_bird = self.dose_based_eec_birds / self.acute_dose_based_tox_birds
        return acute_rq_dose_bird

############################################################################
    def acute_rq_diet_a_f(self):
        """
        RQ diet based for birds
        :return:
        """
        self.acute_rq_diet_a = self.db5a / self.avian_lc50
        return self.acute_rq_diet_a
#################################################################################
##############################################################################
    def acute_rq_diet_birds(self, diet_based_eec, bird_lc50):
        """
        :description Acute diet-based for risk quotient birds
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param bird_lc50; avian lc50 (mg/kg-diet)
        :param diet_based_eec: diet-based eec for birds (mg pesticide / kg-bw day)
        :note in the OPP spreadsheet 'bird_lc50' may be input as 'N/A' or have
              a value; in the case it is assigned 'N/A' this method should assign
              'acute_rq_diet_bird' a value of 'N/A'  -- as implemented below it will
              either assign a 'nan' or issue a divide by zero error.
        :return:
        """
        acute_rq_diet_bird = np.array([], dtype = 'float')

        acute_rq_diet_bird = diet_based_eec/ bird_lc50
        return acute_rq_diet_bird

#############################################################################
    def chronic_rq_diet_a_f(self):
        """
        Chronic RQ diet for birds
        :return:
        """
        self.chronic_rq_diet_a = self.db5a / self.avian_noaec
        return self.chronic_rq_diet_a
#############################################################################
#############################################################################
    def chronic_rq_diet_birds(self, diet_based_eec, avian_chronic_endpt):
        """
        :description chronic diet-based  rist quotient for birds
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param avian_chronic_endpt:  avian noaec (mg/kg-diet)
        :param diet_based_eec: diet-based eec for mammal (mg pesticide / kg
        :return:
        """
        chronic_rq_diet_bird = np.array([], dtype = 'float')

        chronic_rq_diet_bird = diet_based_eec / avian_chronic_endpt
        return chronic_rq_diet_bird