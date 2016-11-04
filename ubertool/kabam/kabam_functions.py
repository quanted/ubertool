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

    def phytoplankton_k1_calc(self, k_ow):
        """
        :description Uptake rate constant through respiratory area for phytoplankton
        :unit L/kg*d
        :expression Kabam Eq. A5.1  (K1:unique to phytoplankton)
        :param 6.05e-5: Parameter 'A' in Eq. A5.1; constant related to resistance to pesticide
                        uptake through the aquaeous phase of plant (days)
        :param 5.5: Parameter 'B' in Eq. A5.1; contant related to the resistance to pesticide
                    uptake through the organice phase of plant (days)
        :param k_ow: octanol-water partition coefficient ()

        :return:
        """

        phyto_k1 = pd.Series([], dtype = 'float')

        phyto_k1 = 1 / (6.0e-5 + (5.5 / k_ow))
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
        :note the loop here could be moved to the main routine with the
        coefficient *i.e., 0.0005, 0.00251) provided through a calling argument
        :return:
        """
        growth_rate = pd.Series([], dtype = 'float')

        for i in range(len(self.water_temp)):  #loop through model simulation runs
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
        :unit kg diet / kg organism
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

        rate_factor = (((1. - epsilonL) * diet_lipid) + ((1. - epsilonN) * diet_nlom) + (
                    (1. - epsilonW) * diet_water))
        return rate_factor

    def diet_elements_gut(self, epsilon, overall_diet_content, egestion_rate_factor):
        """
        :description Fraction of diet elements (i.e., lipid, NLOM, water) in the gut
        :unit (kg lipid) / (kg digested wet weight)
        :expression Kabam Eq. A9 (VLG, VNG, VWG)
        :param epsilon relevant dietary assimilation rate (fraction)
        :param overall_diet_content relevant overall diet content of diet element, e.g., lipid/nlom/water (kg/kg)
        :param egestion_rate_factor relevant: Aquatic animal/organism egestion rate of fecal matter factor
        :return:
        """

        gut_content = pd.Series([], dtype = 'float')

        try:
            gut_content = ((1. - epsilon) * overall_diet_content) / egestion_rate_factor
        except:
            print('Likely divide by zero in routine diet_elements_gut')
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
        :expression Kabam Eq. A9
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
        :expression Kabam A1 (product of terms - [phi * water_column_eec], used in Eqs F2 & F4)
        :param phi: Fraction of pesticide freely dissolved in water column (that can be
                    absorbed via membrane diffusion) (fraction)
        :param water_column_eec: Water Column 1-in-10 year EECs (ug/L)
        :param 1000000: conversion factor from ug/L to g/L
        :return:
        """
        conc_pest_diss = pd.Series([], dtype = 'float')

        conc_pest_diss = self.phi * self.water_column_eec / 1000000.
        return conc_pest_diss

    def conc_sed_norm_4oc(self):
        """
        :description Pesticide concentration in sediment normalized for organic carbon
        :unit ug/(kg OC)
        :expression Kabam Eq. A4a
        :param pore_water_eec: freely dissolved pesticide concentration in sediment pore water (ug/L)
        :param k_oc: organic carbon partition coefficient (L/kg OC)
        :Note units here are in ug/kg as opposed to g/kg as in OPP spreadsheet; this is just to be consistent with
              other units used throughout
        :return:
        """
        conc_diss_sed = pd.Series([], dtype = 'float')

        conc_diss_sed = self.k_oc * self.pore_water_eec
        return conc_diss_sed

    def conc_sed_dry_wgt(self):
        """
        :description Calculate concentration of pesticide in solid portion of sediment
        :unit ug/(kg dry sediment)
        :expression Kabam Eq. A4
        :param c_soc: pesticide concentration in sediment normalized for organic carbon ug/(kg OC)
        :param sediment_oc: fraction organic carbon in sediment (fraction)
        :Note units here are in ug/kg as opposed to g/kg as in OPP spreadsheet; this is just to be consistent with
              other units used throughout
        :return:
        """

        conc_sed = pd.Series([], dtype = 'float')

        conc_sed = self.c_soc * self.sediment_oc_frac
        return conc_sed

    def diet_pest_conc(self, prey_frac, prey_pest_conc, diet_lipid_frac):
        """
        :description Overall concentration of pesticide in aquatic animal/organism diet and
                     lipid normalized overall concentration of pesticide in aquatic animal/organism diet
        :unit g/(kg wet weight)
        :expression Kabam Eq. A1 (SUM(Pi * CDi);
        :param prey_frac: fraction of diet containing prey i (Pi in Eq. A1))
        :param prey_pest_conc: concentraiton of pesticide in prey i (CDi in Eq. A1)
        :param diet_lipid_frac: fraction of animal/organism that is lipid
        :return:
        """

        overall_diet_conc = pd.Series([], dtype = 'float')
        overall_lipid_norm_conc = pd.Series([], dtype = 'float')
        overall_diet_conc = len(prey_frac) * [0.0]
        overall_lipid_norm_conc = len(prey_frac) * [0.0]

        for j in range(len(prey_frac)):  # process model simulation runs
            for i in range(len(prey_frac[j])):  # process individual prey items
                prey_conc = prey_frac[j][i] * prey_pest_conc[j][i]
                if (diet_lipid_frac[j][i] > 0.0):
                    lipid_norm_prey_conc = prey_conc / diet_lipid_frac[j][i]
                else:
                    lipid_norm_prey_conc = 0.0

                overall_diet_conc[j] = overall_diet_conc[j] + prey_conc
                overall_lipid_norm_conc[j] = overall_lipid_norm_conc[j] + lipid_norm_prey_conc

        return overall_diet_conc, overall_lipid_norm_conc

    def pest_conc_organism(self, k1, k2, kD, kE, kG, kM, mP, mO, pest_diet_conc):
        """
        :description Concentration of pesticide in aquatic animal/organism
        :unit ug/(kg wet weight)
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
        :param water_column_eec: total pesticide concentraiton in water column above sediment (ug/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (ug/L)
        :param pest_diet_conc: concentration of pesticide in overall diet of aquatic animal/organism (ug/kg wet weight)
        #because phytoplankton have no diet the (Kd * SUM(Pi * Cdi)) portion of Eq. A1 is not included here
        :return:
        """

        pest_conc_organism = pd.Series([], dtype = 'float')

        pest_conc_organism = (k1 * ((mO * self.phi * self.water_column_eec) +
                             (mP * self.pore_water_eec)) + (kD * pest_diet_conc)) / (k2 + kE + kG + kM)
        return pest_conc_organism

    def lipid_norm_residue_conc(self, total_conc, lipid_content):
        """
        :description Lipid normalized pesticide residue in aquatic animal/organism
        :unit ug/kg-lipid
        :expresssion represents a factor (CB/VLB) used in Kabam Eqs. F4, F5, & F6
        :param total_conc: total pesticide concentration in animal/organism (ug/kg-ww)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :return:
        """
        lipid_norm_conc = pd.Series([], dtype = 'float')

        lipid_norm_conc = total_conc / lipid_content
        return lipid_norm_conc

    def pest_conc_diet_uptake(self, kD,  k2, kE, kG, kM, diet_conc):
        """
        :description Pesticide concentration in aquatic animal/organism originating from uptake through diet
        :unit ug/kg ww
        :expression Kabam A1 (with k1 = 0)
        :param kD: pesticide uptake rate constant for uptake through ingestion of food (kg food/kg organizm - day)
        :param diet_conc: overall concentration of pesticide in diet of animal/organism (ug/kg-ww)
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
        :unit ug/kg ww
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
        :param water_column_eec: total pesticide concentraiton in water column above sediment (ug/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (ug/L)
        :return:
        """
        pest_conc_from_respir = pd.Series([], dtype = 'float')

        pest_conc_from_respir = (k1 * (mO * self.phi * self.water_column_eec + (mP * self.pore_water_eec))
                                 / (k2 + kE + kM + kG))
        return pest_conc_from_respir

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
        :param water_column_eec: total pesticide concentraiton in water column above sediment (ug/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (ug/L)
        :return:
        """
        bioconc_fact = pd.Series([], dtype = 'float')

        bioconc_fact = (k1 * (mO * self.phi * self.water_column_eec + (mP * self.pore_water_eec)) / k2 )\
                       / self.water_column_eec
        return bioconc_fact

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
        :param water_column_eec: total pesticide concentraiton in water column above sediment (ug/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (ug/L)
        :return:
        """

        lipid_norm_bcf = pd.Series([], dtype = 'float')

        lipid_norm_bcf = ((k1 * (mO * self.phi * self.water_column_eec + mP * self.pore_water_eec) / k2 )
                          / lipid_content) /  (self.water_column_eec * self.phi)
        return lipid_norm_bcf

    def tot_bioacc_fact(self, pest_conc):
        """
        :description Total bioaccumulation factor
        :unit (ug pesticide/kg ww) / (ug pesticide/L water)
        :expression Kabam Eq. F3
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (ug/(kg wet weight)
        :param water_column_eec:  total pesticide concentraiton in water column above sediment (ug/L)
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
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (ug/(kg wet weight)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (ug/L)
        :return:
        """
        lipid_norm_baf = pd.Series([], dtype = 'float')

        lipid_norm_baf = (pest_conc/ lipid_content) / (self.water_column_eec * self.phi)
        return lipid_norm_baf

    def biota_sed_acc_fact(self, pest_conc, lipid_content):  #cdsafl
        """
        :description Biota-sediment accumulation factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F5
        :param pest_conc: Concentration of pesticide in aquatic animal/organism (ug/(kg wet weight)
        :param lipid_content: fraction of animal/organism that is lipid (fraction)
        :param c_soc Pesticide concentration in sediment normalized for organic carbon content (ug/kg OC)
        :return:
        """

        sediment_acc_fact = pd.Series([], dtype = 'float')
        #conversions not necessary, included for consistency of units use
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

        #biomag_fact = pd.Series([], dtype = 'float')

        biomag_fact = pd.Series((pest_conc / lipid_content) / lipid_norm_diet_conc, dtype = 'float')

        return biomag_fact

#############################################################################
#############################################################################
#this method is not created in final Kabam model; the mweight array is created in 'set_global_constants' method
#and the conversion of concentrations (self.cb_*) is performed in the main routine
    #     # Mammals EECs
    # def mweight_f(self):
    #     """
    #     Mammals
    #     :return:
    #     """
    #     self.cb_a = np.array(
    #         [[self.cb_phytoplankton, self.cb_zoo, self.cb_beninv, self.cb_ff, self.cb_sf, self.cb_mf, self.cb_lf]])
    #     self.cb_a2 = self.cb_a * 1000000
    #     # array of mammal weights
    #     #[fog/water shrew,rice rat/star-nosed mole,small mink,large mink,small river otter	,large river otter]
    #     self.mweight = np.array([[0.018, 0.085, 0.45, 1.8, 5, 15]])
    #     return self.mweight
##############################################################################

    def dry_food_ingest_rate_mammals(self):
        """
        :description dry food ingestion rate: Mammals (kg dry food/kg-bw day)
        :unit (kg dry food / kg-bw day)
        :expresssion  Kabam Eq. G1
        :param mammal_weights: body weight of mammal (kg)
        :notes because mammal.weights are represented as constants (hardwired in the code) this
               method is not designed for matrix/parallel processing; if the weights are
               changed to inputs this method would be modified by removing the array structure and
               inserting a simulation-based loop in the main model routine
        :return:
        """

        ingestion_rate = np.array([], dtype = 'float')

        ingestion_rate = (0.0687 * self.mammal_weights ** 0.822) / self.mammal_weights
        return ingestion_rate

    def dry_food_ingest_rate_birds(self):
        """
        :description dry food ingestion rate: Birds (kg dry food/kg-bw day)
        :unit (kg dry food / kg-bw day)
        :expresssion  Kabam Eq. G2
        :param bird_weights: body weight of bird (kg)
        :notes because bird.weights are represented as constants (hardwired in the code) this
               method is not designed for matrix/parallel processing; if the weights are
               changed to inputs this method would be modified by removing the array structure and
               inserting a simulation-based loop in the main model routine
        :return:
        """

        ingestion_rate_birds = np.array([], dtype = 'float')

        ingestion_rate_birds = (0.0582 * self.bird_weights ** 0.651) / self.bird_weights
        return ingestion_rate_birds

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
        factor_4 = 1. - factor_3

        # wet food ingestion rate
        wet_food_ingest_rates = dry_food_ingestion_rates / factor_4
        return wet_food_ingest_rates

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
        dose_based_eec = (overall_diet_conc / 1000.) * wet_food_ingest_rate + \
                         (((wc_eec / 1000.) * water_ingest_rate) / body_weight)
        return dose_based_eec

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
        dietary_eec = np.array([], dtype = 'float')

        #calculate relevant factors
        frac_diet_conc = pest_conc_diet * diet_fraction
        sum_diet_fracs = np.cumsum(frac_diet_conc, axis=1)
        overall_diet_conc = sum_diet_fracs[:, 6]

        # dietary-based  EEC  (the /1000 converts ug to mg)
        dietary_eec = (overall_diet_conc / 1000)
        return dietary_eec

    def acute_dose_based_tox_mammals(self, ld50_mammal, tested_animal_bw):
        """
        :description Dose-based acute toxicity for mammals
        :unit (mg/kg-bw)
        :expression Kabam Eq. G8
        :param ld50_mammal: Mammalian acute oral LD50 (mg/kg-bw)
        :param tested_animal_bw: body weight of tested animal (gms)
        :param mammal_weights: body weight of assessed animal (kg)
        :return:
        """

        acute_toxicity_mammal = ld50_mammal * ((tested_animal_bw / 1000.) / self.mammal_weights) ** 0.25
        return acute_toxicity_mammal

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

        acute_toxicity_bird = ld50_bird * ((self.bird_weights / (tested_bird_bw / 1000.)) ** (scaling_factor - 1.))
        return acute_toxicity_bird

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

    def chronic_diet_based_tox_mammals(self, mammalian_chronic_endpt, mammalian_chronic_endpt_unit):
        """
        :description chronic diet-based toxicity for mammals
        :unit (mg/kg-diet)
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param mammalian_chronic_endpt:  (ppm or mg/kg-diet)
        :return:
        """
        chronic_toxicity = np.array([], dtype = 'float')
        if (mammalian_chronic_endpt_unit == 'ppm'):
            chronic_toxicity = mammalian_chronic_endpt
        else:
            chronic_toxicity = mammalian_chronic_endpt * 20.
        return chronic_toxicity

    def acute_rq_dose_mammals(self):
        """
        :description Dose-based risk quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet)
         :param dose_based_eec_mammals
         :param acute_dose_based_tox_mammals
        :return:
        """

        acute_rq_dose_mamm = self.dose_based_eec_mammals / self.dose_based_tox_mammals
        return acute_rq_dose_mamm

    def chronic_rq_dose_mammals(self):
        """
        :description Chronic dose-based risk quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet)
        :param dose_based_eec_mammals: self defined
        :param chronic_dose_based_tox_mammals: self defined
        :return:
        """

        chronic_rq_dose_mamm = self.dose_based_eec_mammals / self.chronic_dose_based_tox_mamm
        return chronic_rq_dose_mamm

    def acute_rq_diet_mammals(self, diet_based_eec, mammal_lc50):
        """
        :description Acute diet-based for risk quotient mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param mammal_lc50; mammalian lc50 (mg/kg-diet)
        :param diet_based_eec: diet-based eec for mammal (mg pesticide / kg-bw day)
        :return:
        """
        acute_rq_diet_mamm = np.array([], dtype = 'float')

        acute_rq_diet_mamm = diet_based_eec/ mammal_lc50
        return acute_rq_diet_mamm

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

    def acute_rq_dose_birds(self):
        """
        :description Dose-based risk quotient for birds
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
         :param dose_based_eec_birds: self defined
         :param acute_dose_based_tox_birds: self defined
        :return:
        """

        acute_rq_dose_bird = self.dose_based_eec_birds / self.dose_based_tox_birds
        return acute_rq_dose_bird

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

        acute_rq_diet_bird = diet_based_eec/ bird_lc50
        return acute_rq_diet_bird

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