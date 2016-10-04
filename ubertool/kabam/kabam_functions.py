from __future__ import division  #brings in Python 3.0 mixed type calculation rules
from functools import wraps
import logging
import numpy as np
import pandas as pd
import time

from math import exp

class KabamFunctions(object):
    """
    Function class for Kabam.
    """

    def __init__(self):
        """Class representing the functions for Kabam"""
        super(KabamFunctions, self).__init__()


    def percent_to_frac(self, percent):
        fraction = percent / 100.
        return fraction

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

    def pest_uptake_eff_bygills(self):
        """
        :description Pesticide uptake efficiency by gills
        :unit fraction
        :expression Kabam Eq. A5.2a (Ew)
        :param log kow: octanol-water partition coefficient ()
        :return:
        """

        pest_uptake_eff_bygills = pd.Series([], dtype = 'float')

        pest_uptake_eff_bygills = (1 / (1.85 + (155 / self.kow)))
        return pest_uptake_eff_bygills

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

        phyto_k1 = 1 / (6.0e-5 + (5.5 / self.kow))
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
        aqueous_animal_k1 = pd.Series([], dtype = 'float')

        aqueous_animal_k1 = ((pest_uptake_eff_bygills * vent_rate) / wet_wgt)
        return aqueous_animal_k1

    def animal_water_part_coef(self, frac_lipid_cont, frac_nlom_cont, frac_water_cont, beta):
        """
        :description Organism-Water partition coefficient (based on organism wet weight)
        :unit ()
        :expression Kabam Eq. A6a (Kbw)
        :param frac_lipid_cont: lipid fraction of organism (kg lipid/kg organism wet weight)
        :param frac_nlom_cont: non-lipid organic matter (NLOM) fraction of organism (kg NLOM/kg organism wet weight)
        :param frac_water_cont water content of organism (kg water/kg organism wet weight)
        :param kow: octanol-water partition coefficient ()
        :param beta: proportionality constant expressing the sorption capacity of NLOM or NLOC to
                     that of octanol (0.35 for phytoplankton; 0.035 for all other aquatic animals)
        :return:
        """

        part_coef = pd.Series([], dtype = 'float')

        part_coef = (frac_lipid_cont * self.kow) + (frac_nlom_cont * beta * self.kow) + frac_water_cont
        return part_coef

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

        for i in range(len(self.water_temp)):
            if self.water_temp[i] < 17.5:
                growth_rate[i] = 0.0005 * (wet_wgt[i] ** -0.2)
            else:
                growth_rate[i] = 0.00251 * (wet_wgt[i] ** -0.2)
        return growth_rate

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

    def aq_animal_feeding_rate(self, wet_wgt):
        """
        :description Aquatic animal feeding rate (except filterfeeders)
        :unit kg/d
        :expression Kabam Eq. A8b1 (Gd)
        :param wet_wgt: wet weight of animal/organism (kg)
        :return:
        """

        feeding_rate = pd.Series([], dtype = 'float')

        for i in range(len(self.water_temp)):
            feeding_rate[i] = 0.022 * wet_wgt[i] ** 0.85 * exp(0.06 * self.water_temp[i])

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

    def diet_uptake_rate_const(self, dietary_trans_eff, feeding_rate, wet_wgt):
        """
        :description Pesticide uptake rate constant for uptake through ingestion of food rate
        :unit kg food/kg organism - day
        :expression Kabam Eq. A8 (kD)
        :param wet weight of aquatic animal/organism (kg)
        :param dietary_trans_eff: dietary pesticide transfer efficiency (fraction)
        :param feeding rate: animal/organism feeding rate (kg/d)
        :return:
        """
        dietary_uptake_constantt = pd.Series([], dtype = 'float')

        dietary_uptake_constant = dietary_trans_eff * feeding_rate / wet_wgt
        return dietary_uptake_constant

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
        :param diet_fraction: list of values representing fractions of aquatic animal/organism diet attributed
                              to each element (prey) of diet
        :param content_fraction: list of values representing fraction of diet element (prey) attributed to a specific
                                 component of that diet element (e.g., lipid, NLOM, or water)
        :return:
        """

        overall_diet_fraction = pd.Series([], dtype = 'float')
        overall_diet_fraction = 0.0

        for i in range(len(diet_fraction)):
            overall_diet_fraction = overall_diet_fraction + diet_fraction[i] * content_fraction[i]

        return overall_diet_fraction

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

        part_coef = pd.Series([], dtype = 'float')

        part_coef = (pest_kow * (gut_lipid + beta * gut_nlom) + gut_water) /  \
                         (pest_kow * (organism_lipid + beta * organism_nlom) + organism_water)
        return part_coef

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
        frac_diss = pd.Series([], dtype = 'float')

        frac_diss = 1 / (1 + (self.conc_poc * self.alpha_poc * self.kow) + (self.conc_doc * self.alpha_doc * self.kow))
        return frac_diss

    def conc_freely_diss_watercol(self):
        """
        :description Concentration of freely dissolved pesticide in overlying water column
        :unit g/L
        :expression Kabam A1 (product of terms - [phi * Cwto], used in Eqs F2 & F4)
        :param phi: Fraction of pesticide freely dissolved in water column (that can be
                    absorbed via membrane diffusion) (fraction)
        :param water_column_eec: Water Column 1-in-10 year EECs (ug/L)
        :param 1000000: conversion factor from ug/L to g/L
        :return:
        """
        conc_pest_diss = pd.Series([], dtype = 'float')

        conc_pest_diss = self.phi * self.water_column_eec / 1000000.
        return conc_pest_diss

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

    def diet_pest_conc(self, prey_frac, prey_pest_conc):
        """
        :description Overall concentration of pesticide in aquatic animal/organism diet
        :unit g/(kg wet weight)
        :expression Kabam Eq. A1 (SUM(Pi * CDi);
        :param: prey_frac: fraction of diet containing prey i (Pi in Eq. A1))
        :param: prey_pest_conc: concentraiton of pesticide in prey i (CDi in Eq. A1)
        :return:
        """

        overall_diet_conc = pd.Series([], dtype = 'float')
        overall_diet_conc = len(prey_frac) * [0.0]

        for j in range(len(prey_frac)):
            for i in range(len(prey_frac[j])):
                overall_diet_conc[j] = overall_diet_conc[j] + prey_frac[j][i] * prey_pest_conc[j][i]

        return overall_diet_conc

    def pest_conc_organism(self, k1, k2, kD, kE, kG, kM, mP, mO, pest_diet_conc):
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
        :param cwto: total pesticide concentraiton in water column above sediment (g/L)
        :param cwdp: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :param pest_diet_conc: concentration of pesticide in overall diet of aquatic animal/organism (g/kg wet weight)
        #because phytoplankton have no diet the (Kd * SUM(Pi * Cdi)) portion of Eq. A1 is not included here
        :return:
        """


        pest_conc_organism = pd.Series([], dtype = 'float')

        pest_conc_organism = (k1 * (mO * self.phi * self.cwto * mP * self.cwdp) + (kD * pest_diet_conc)) / (k2 + kE + kG + kM)
        return pest_conc_organism

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
        :param cwto: total pesticide concentraiton in water column above sediment (g/L)
        :param cwdp: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :return:
        """

        bioconc_fact = pd.Series([], dtype = 'float')

        bioconc_fact = (k1 * (mO * self.phi * self.cwto * mP * self.cwdp) / k2 ) / self.cwto
        return bioconc_fact