from __future__ import division  #brings in Python 3.0 mixed type calculations
import numpy as np
import os
import pandas as pd
import sys

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from base.uber_model import UberModel, ModelSharedInputs

class BeerexInputs(ModelSharedInputs):
    """
    Input class for Beerex
    """
    def __init__(self):
        """Class representing the inputs for Beerex"""
        super(BeerexInputs, self).__init__()
        #self.incorporation_depth = pd.Series([], dtype="float")
        self.application_rate = pd.Series([], dtype="float")
        self.application_method = pd.Series([], dtype="object")
        self.crop_type = pd.Series([], dtype="object")
        # self.application_units = pd.Series([], dtype="object")
        self.empirical_residue = pd.Series([], dtype="object")
        self.empirical_pollen = pd.Series([], dtype="float")
        self.empirical_nectar = pd.Series([], dtype="float")
        self.empirical_jelly = pd.Series([], dtype="float")
        self.adult_contact_ld50 = pd.Series([], dtype="float")
        self.adult_oral_ld50 = pd.Series([], dtype="float")
        self.adult_oral_noael = pd.Series([], dtype="float")
        self.larval_ld50 = pd.Series([], dtype="float")
        self.larval_noael = pd.Series([], dtype="float")
        self.log_kow = pd.Series([], dtype="float")
        self.koc = pd.Series([], dtype="float")
        self.mass_tree_vegetation = pd.Series([], dtype="float")
        self.lw1_jelly = pd.Series([], dtype="float")
        self.lw2_jelly = pd.Series([], dtype="float")
        self.lw3_jelly = pd.Series([], dtype="float")
        self.lw4_nectar = pd.Series([], dtype="float")
        self.lw4_pollen = pd.Series([], dtype="float")
        self.lw5_nectar = pd.Series([], dtype="float")
        self.lw5_pollen = pd.Series([], dtype="float")
        self.ld6_nectar = pd.Series([], dtype="float")
        self.ld6_pollen = pd.Series([], dtype="float")
        self.lq1_jelly = pd.Series([], dtype="float")
        self.lq2_jelly = pd.Series([], dtype="float")
        self.lq3_jelly = pd.Series([], dtype="float")
        self.lq4_jelly = pd.Series([], dtype="float")
        self.aw_cell_nectar = pd.Series([], dtype="float")
        self.aw_cell_pollen = pd.Series([], dtype="float")
        self.aw_brood_nectar = pd.Series([], dtype="float")
        self.aw_brood_pollen = pd.Series([], dtype="float")
        self.aw_comb_nectar = pd.Series([], dtype="float")
        self.aw_comb_pollen = pd.Series([], dtype="float")
        self.aw_fpollen_nectar = pd.Series([], dtype="float")
        self.aw_fpollen_pollen = pd.Series([], dtype="float")
        self.aw_fnectar_nectar = pd.Series([], dtype="float")
        self.aw_fnectar_pollen = pd.Series([], dtype="float")
        self.aw_winter_nectar = pd.Series([], dtype="float")
        self.aw_winter_pollen = pd.Series([], dtype="float")
        self.ad_nectar = pd.Series([], dtype="float")
        self.ad_pollen = pd.Series([], dtype="float")
        self.aq_jelly = pd.Series([], dtype="float")


class BeerexOutputs(object):
    """
    Output class for Beerex
    """
    def __init__(self):
        """Class representing the outputs for Beerex"""
        super(BeerexOutputs, self).__init__()
        self.out_eec_spray = pd.Series(name="out_eec_spray").astype("float")
        self.out_eec_soil = pd.Series(name="out_eec_soil").astype("float")
        self.out_eec_seed = pd.Series(name="out_eec_seed").astype("float")
        self.out_eec_tree = pd.Series(name="out_eec_tree").astype("float")
        self.out_eec = pd.Series(name="out_eec").astype("float")
        self.out_lw1_total_dose = pd.Series(name="out_lw1_total_dose").astype("float")
        self.out_lw2_total_dose = pd.Series(name="out_lw2_total_dose").astype("float")
        self.out_lw3_total_dose = pd.Series(name="out_lw3_total_dose").astype("float")
        self.out_lw4_total_dose = pd.Series(name="out_lw4_total_dose").astype("float")
        self.out_lw5_total_dose = pd.Series(name="out_lw5_total_dose").astype("float")
        self.out_ld6_total_dose = pd.Series(name="out_ld6_total_dose").astype("float")
        self.out_lq1_total_dose = pd.Series(name="out_lq1_total_dose").astype("float")
        self.out_lq2_total_dose = pd.Series(name="out_lq2_total_dose").astype("float")
        self.out_lq3_total_dose = pd.Series(name="out_lq3_total_dose").astype("float")
        self.out_lq4_total_dose = pd.Series(name="out_lq4_total_dose").astype("float")
        self.out_aw_cell_total_dose = pd.Series(name="out_aw_cell_total_dose").astype("float")
        self.out_aw_brood_total_dose = pd.Series(name="out_aw_brood_total_dose").astype("float")
        self.out_aw_comb_total_dose = pd.Series(name="out_aw_comb_total_dose").astype("float")
        self.out_aw_pollen_total_dose = pd.Series(name="out_aw_pollen_total_dose").astype("float")
        self.out_aw_nectar_total_dose = pd.Series(name="out_aw_nectar_total_dose").astype("float")
        self.out_aw_winter_total_dose = pd.Series(name="out_aw_winter_total_dose").astype("float")
        self.out_ad_total_dose = pd.Series(name="out_ad_total_dose").astype("float")
        self.out_aq_total_dose = pd.Series(name="out_aq_total_dose").astype("float")
        self.out_lw1_acute_rq = pd.Series(name="out_lw1_acute_rq").astype("float")
        self.out_lw2_acute_rq = pd.Series(name="out_lw2_acute_rq").astype("float")
        self.out_lw3_acute_rq = pd.Series(name="out_lw3_acute_rq").astype("float")
        self.out_lw4_acute_rq = pd.Series(name="out_lw4_acute_rq").astype("float")
        self.out_lw5_acute_rq = pd.Series(name="out_lw5_acute_rq").astype("float")
        self.out_ld6_acute_rq = pd.Series(name="out_ld6_acute_rq").astype("float")
        self.out_lq1_acute_rq = pd.Series(name="out_lq1_acute_rq").astype("float")
        self.out_lq2_acute_rq = pd.Series(name="out_lq2_acute_rq").astype("float")
        self.out_lq3_acute_rq = pd.Series(name="out_lq3_acute_rq").astype("float")
        self.out_lq4_acute_rq = pd.Series(name="out_lq4_acute_rq").astype("float")
        self.out_aw_cell_acute_rq = pd.Series(name="out_aw_cell_acute_rq").astype("float")
        self.out_aw_brood_acute_rq = pd.Series(name="out_aw_brood_acute_rq").astype("float")
        self.out_aw_comb_acute_rq = pd.Series(name="out_aw_comb_acute_rq").astype("float")
        self.out_aw_pollen_acute_rq = pd.Series(name="out_aw_pollen_acute_rq").astype("float")
        self.out_aw_nectar_acute_rq = pd.Series(name="out_aw_nectar_acute_rq").astype("float")
        self.out_aw_winter_acute_rq = pd.Series(name="out_aw_winter_acute_rq").astype("float")
        self.out_ad_acute_rq = pd.Series(name="out_ad_acute_rq").astype("float")
        self.out_aq_acute_rq = pd.Series(name="out_aq_acute_rq").astype("float")
        self.out_lw1_chronic_rq = pd.Series(name="out_lw1_chronic_rq").astype("float")
        self.out_lw2_chronic_rq = pd.Series(name="out_lw2_chronic_rq").astype("float")
        self.out_lw3_chronic_rq = pd.Series(name="out_lw3_chronic_rq").astype("float")
        self.out_lw4_chronic_rq = pd.Series(name="out_lw4_chronic_rq").astype("float")
        self.out_lw5_chronic_rq = pd.Series(name="out_lw5_chronic_rq").astype("float")
        self.out_ld6_chronic_rq = pd.Series(name="out_ld6_chronic_rq").astype("float")
        self.out_lq1_chronic_rq = pd.Series(name="out_lq1_chronic_rq").astype("float")
        self.out_lq2_chronic_rq = pd.Series(name="out_lq2_chronic_rq").astype("float")
        self.out_lq3_chronic_rq = pd.Series(name="out_lq3_chronic_rq").astype("float")
        self.out_lq4_chronic_rq = pd.Series(name="out_lq4_chronic_rq").astype("float")
        self.out_aw_cell_chronic_rq = pd.Series(name="out_aw_cell_chronic_rq").astype("float")
        self.out_aw_brood_chronic_rq = pd.Series(name="out_aw_brood_chronic_rq").astype("float")
        self.out_aw_comb_chronic_rq = pd.Series(name="out_aw_comb_chronic_rq").astype("float")
        self.out_aw_pollen_chronic_rq = pd.Series(name="out_aw_pollen_chronic_rq").astype("float")
        self.out_aw_nectar_chronic_rq = pd.Series(name="out_aw_nectar_chronic_rq").astype("float")
        self.out_aw_winter_chronic_rq = pd.Series(name="out_aw_winter_chronic_rq").astype("float")
        self.out_ad_chronic_rq = pd.Series(name="out_ad_chronic_rq").astype("float")
        self.out_aq_chronic_rq = pd.Series(name="out_aq_chronic_rq").astype("float")
        # self.out_adult_acute_contact = pd.Series(name="out_adult_acute_contact").astype("float")
        # self.out_adult_acute_dietary = pd.Series(name="out_adult_acute_dietary").astype("float")
        # self.out_adult_chronic_dietary = pd.Series(name="out_adult_chronic_dietary").astype("float")
        # self.out_larvae_acute_dietary = pd.Series(name="out_larvae_acute_dietary").astype("float")
        # self.out_larvae_chronic_dietary = pd.Series(name="out_larvae_chronic_dietary").astype("float")


class Beerex(UberModel, BeerexInputs, BeerexOutputs):
    """
    Individual-based model estimates exposures of bees to pesticides
    """
    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Beerex model and containing all its methods"""
        super(Beerex, self).__init__()
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
        boolog = True
        if boolog:
            print('execute_model start ============================')
            print('populate inputs')
        self.populate_inputs(self.pd_obj)
        if boolog:
            print('populate outputs')
        self.pd_obj_out = self.populate_outputs()
        if boolog:
            print('run methods')
        self.run_methods()
        if boolog:
            print('fill output dataframe')
        self.fill_output_dataframe()

    def run_methods(self):
        """Execute the model's methods to generate the model output"""
        self.set_global_constants()
        self.eec()
        self.lw1_total_dose()
        self.lw2_total_dose()
        self.lw3_total_dose()
        self.lw4_total_dose()
        self.lw5_total_dose()
        self.ld6_total_dose()
        self.lq1_total_dose()
        self.lq2_total_dose()
        self.lq3_total_dose()
        self.lq4_total_dose()
        self.aw_cell_total_dose()
        self.aw_brood_total_dose()
        self.aw_comb_total_dose()
        self.aw_pollen_total_dose()
        self.aw_nectar_total_dose()
        self.aw_winter_total_dose()
        self.ad_total_dose()
        self.aq_total_dose()
        self.lw1_acute_rq()
        self.lw2_acute_rq()
        self.lw3_acute_rq()
        self.lw4_acute_rq()
        self.lw5_acute_rq()
        self.ld6_acute_rq()
        self.lq1_acute_rq()
        self.lq2_acute_rq()
        self.lq3_acute_rq()
        self.lq4_acute_rq()
        self.aw_cell_acute_rq()
        self.aw_brood_acute_rq()
        self.aw_comb_acute_rq()
        self.aw_pollen_acute_rq()
        self.aw_nectar_acute_rq()
        self.aw_winter_acute_rq()
        self.ad_acute_rq()
        self.aq_acute_rq()
        self.lw1_chronic_rq()
        self.lw2_chronic_rq()
        self.lw3_chronic_rq()
        self.lw4_chronic_rq()
        self.lw5_chronic_rq()
        self.ld6_chronic_rq()
        self.lq1_chronic_rq()
        self.lq2_chronic_rq()
        self.lq3_chronic_rq()
        self.lq4_chronic_rq()
        self.aw_cell_chronic_rq()
        self.aw_brood_chronic_rq()
        self.aw_comb_chronic_rq()
        self.aw_pollen_chronic_rq()
        self.aw_nectar_chronic_rq()
        self.aw_winter_chronic_rq()
        self.ad_chronic_rq()
        self.aq_chronic_rq()
    #   except TypeError:
    #

    def eec_spray(self, i):
        """
        EEC for foliar spray
        """
        self.out_eec_spray[i] = (110. * self.application_rate[i]) / 1000
        self.out_eec_soil[i] = np.nan
        self.out_eec_seed[i] = np.nan
        self.out_eec_tree[i] = np.nan
        return # self.out_eec_spray[i]

    def eec_soil(self, i):
        """
        EEC for soil application
        """
        self.out_eec_soil[i] = ((10.**(0.95*self.log_kow[i]-2.05)+0.82) *
                             (-0.0648*(self.log_kow[i]**2)+0.2431*self.log_kow[i]+0.5822) *
                             (1.5/(0.2+1.5*self.koc[i]*0.01)) * (0.5 * self.application_rate[i])) / 1000.
        self.out_eec_spray[i] = np.nan
        self.out_eec_seed[i] = np.nan
        self.out_eec_tree[i] = np.nan
        return # self.out_eec_soil[i]

    def eec_seed(self, i):
        """
        EEC for seed treatment
        """
        self.out_eec_seed[i] = 1./1000.
        self.out_eec_soil[i] = np.nan
        self.out_eec_spray[i] = np.nan
        self.out_eec_tree[i] = np.nan
        return # self.out_eec_seed[i]

    def eec_tree(self, i):
        """
        EEC for tree trunk
        """
        self.out_eec_tree[i] = (self.application_rate[i]/self.mass_tree_vegetation[i]) / 1000.
        self.out_eec_soil[i] = np.nan
        self.out_eec_seed[i] = np.nan
        self.out_eec_spray[i] = np.nan
        return # self.out_eec_tree[i]

    def eec(self):
        """
        determine which application method is used for subsequent EEC and RQ calculations
        """
        print('eec method')
        print(self.n_runs)
        for i in range(self.n_runs):
            if self.application_method[i] == 'foliar spray':
                self.out_eec_spray[i] = self.eec_spray(i)
                self.out_eec[i] = self.out_eec_spray[i]
            elif self.application_method[i] == 'soil application':
                print('running beerex soil application')
                self.out_eec_soil[i] = self.eec_soil(i)
                self.out_eec[i] = self.out_eec_soil[i]
            elif self.application_method[i] == 'seed treatment':
                self.out_eec_seed[i] = self.eec_seed(i)
                self.out_eec[i] = self.out_eec_seed[i]
            elif self.application_method[i] == 'tree trunk':
                self.out_eec_tree[i] = self.eec_tree(i)
                self.out_eec[i] = self.out_eec_tree[i]
        #print(self.out_eec)
        return self.out_eec

    def lw1_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 1
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lw1_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lw1_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lw1_total_dose[i] = (self.out_eec[i]/100.) * self.lw1_jelly[i]
        return # self.out_lw1_total_dose[i]

    def lw2_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 2
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lw2_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lw2_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lw2_total_dose[i] = (self.out_eec[i]/100.) * self.lw2_jelly[i]
        return # self.out_lw2_total_dose[i]

    def lw3_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 3
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lw3_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lw3_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lw3_total_dose[i] = (self.out_eec[i]/100.) * self.lw3_jelly[i]
        return # self.out_lw3_total_dose[i]

    def lw4_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 4
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lw4_total_dose[i] = ((self.empirical_pollen[i]/1000.) * self.lw4_pollen[i]) + ((self.empirical_nectar[i]/1000.) * self.lw4_nectar[i])
            elif self.empirical_residue[i] == "no":
                self.out_lw4_total_dose[i] = (self.out_eec[i] * self.lw4_pollen[i]) + (self.out_eec[i] * self.lw4_nectar[i])
        return # self.out_lw4_total_dose[i]

    def lw5_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 5
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lw5_total_dose[i] = ((self.empirical_pollen[i]/1000.) * self.lw5_pollen[i]) + ((self.empirical_nectar[i]/1000.) * self.lw5_nectar[i])
            elif self.empirical_residue[i] == "no":
                self.out_lw5_total_dose[i] = (self.out_eec[i] * self.lw5_pollen[i]) + (self.out_eec[i] * self.lw5_nectar[i])
        return # self.out_lw5_total_dose[i]

    def ld6_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval drone aged 6+ days
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_ld6_total_dose[i] = ((self.empirical_pollen[i]/1000.) * self.ld6_pollen[i]) + ((self.empirical_nectar[i]/1000.) * self.ld6_nectar[i])
            elif self.empirical_residue[i] == "no":
                self.out_ld6_total_dose[i] = (self.out_eec[i] * self.ld6_pollen[i]) + (self.out_eec[i] * self.ld6_nectar[i])
        return # self.out_ld6_total_dose[i]

    def lq1_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen day 1
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lq1_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lq1_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lq1_total_dose[i] = (self.out_eec[i]/100.) * self.lq1_jelly[i]
        return # self.out_lq1_total_dose[i]

    def lq2_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen day 2
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lq2_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lq2_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lq2_total_dose[i] = (self.out_eec[i]/100.) * self.lq2_jelly[i]
        return # self.out_lq2_total_dose[i]

    def lq3_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen day 3
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lq3_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lq3_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lq3_total_dose[i] = (self.out_eec[i]/100.) * self.lq3_jelly[i]
        return # self.out_lq3_total_dose[i]

    def lq4_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen aged 4+ days
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_lq4_total_dose[i] = (self.empirical_jelly[i]/1000.) * self.lq4_jelly[i]
            elif self.empirical_residue[i] == "no":
                self.out_lq4_total_dose[i] = (self.out_eec[i]/100.) * self.lq4_jelly[i]
        return # self.out_lq4_total_dose[i]

    def aw_cell_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (cell cleaning and capping)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aw_cell_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.aw_cell_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.aw_cell_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_aw_cell_total_dose[i] = (self.out_eec[i] * self.aw_cell_nectar[i]) + (self.out_eec[i] * self.aw_cell_pollen[i])
        return # self.out_aw_cell_total_dose[i]

    def aw_brood_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (brood and queen tending, nurse bees)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aw_brood_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.aw_brood_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.aw_brood_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_aw_brood_total_dose[i] = (self.out_eec[i] * self.aw_brood_nectar[i]) + (self.out_eec[i] * self.aw_brood_pollen[i])
        return # self.out_aw_brood_total_dose[i]

    def aw_comb_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (comb building, cleaning, and food handling)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aw_comb_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.aw_comb_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.aw_comb_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_aw_comb_total_dose[i] = (self.out_eec[i] * self.aw_comb_nectar[i]) + (self.out_eec[i] * self.aw_comb_pollen[i])
        return # self.out_aw_comb_total_dose[i]

    def aw_pollen_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (foraging for pollen)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aw_pollen_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.aw_fpollen_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.aw_fpollen_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_aw_pollen_total_dose[i] = (self.out_eec[i] * self.aw_fpollen_nectar[i]) + (self.out_eec[i] * self.aw_fpollen_pollen[i])
        return # self.out_aw_pollen_total_dose[i]

    def aw_nectar_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (foraging for nectar)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aw_nectar_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.aw_fnectar_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.aw_fnectar_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_aw_nectar_total_dose[i] = (self.out_eec[i] * self.aw_fnectar_nectar[i]) + (self.out_eec[i] * self.aw_fnectar_pollen[i])
        return # self.out_aw_nectar_total_dose[i]

    def aw_winter_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (maintenance of hive in winter)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aw_winter_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.aw_winter_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.aw_winter_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_aw_winter_total_dose[i] = (self.out_eec[i] * self.aw_winter_nectar[i]) + (self.out_eec[i] * self.aw_winter_pollen[i])
        return # self.out_aw_winter_total_dose[i]

    def ad_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult drone
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_ad_total_dose[i] = ((self.empirical_nectar[i]/1000.) * self.ad_nectar[i]) + ((self.empirical_pollen[i]/1000.) * self.ad_pollen[i])
            elif self.empirical_residue[i] == "no":
                self.out_ad_total_dose[i] = (self.out_eec[i] * self.ad_nectar[i]) + (self.out_eec[i] * self.ad_pollen[i])
        return # self.out_ad_total_dose[i]

    def aq_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult queen (laying 1500 eggs/day)
        """
        for i in range(self.n_runs):
            if self.empirical_residue[i] == "yes":
                self.out_aq_total_dose[i] = ((self.empirical_jelly[i]/1000.) * self.aq_jelly[i])
            elif self.empirical_residue[i] == "no":
                self.out_aq_total_dose[i] = (self.out_eec[i]/100.) * self.aq_jelly[i]
        return # self.out_aq_total_dose[i]

    def lw1_acute_rq(self):
        """
        Acute risk quotient for larval worker day 1
        """
        self.out_lw1_acute_rq = self.out_lw1_total_dose/self.larval_ld50
        return self.out_lw1_acute_rq

    def lw2_acute_rq(self):
        """
        Acute risk quotient for larval worker day 2
        """
        self.out_lw2_acute_rq = self.out_lw2_total_dose/self.larval_ld50
        return self.out_lw2_acute_rq

    def lw3_acute_rq(self):
        """
        Acute risk quotient for larval worker day 3
        """
        self.out_lw3_acute_rq = self.out_lw3_total_dose/self.larval_ld50
        return self.out_lw3_acute_rq

    def lw4_acute_rq(self):
        """
        Acute risk quotient for larval worker day 4
        """
        self.out_lw4_acute_rq = self.out_lw4_total_dose/self.larval_ld50
        return self.out_lw4_acute_rq

    def lw5_acute_rq(self):
        """
        Acute risk quotient for larval worker day 5
        """
        self.out_lw5_acute_rq = self.out_lw5_total_dose/self.larval_ld50
        return self.out_lw5_acute_rq

    def ld6_acute_rq(self):
        """
        Acute risk quotient for larval drone aged day 6+
        """
        self.out_ld6_acute_rq = self.out_ld6_total_dose/self.larval_ld50
        return self.out_ld6_acute_rq

    def lq1_acute_rq(self):
        """
        Acute risk quotient for larval queen day 1
        """
        self.out_lq1_acute_rq = self.out_lq1_total_dose/self.larval_ld50
        return self.out_lq1_acute_rq

    def lq2_acute_rq(self):
        """
        Acute risk quotient for larval queen day 2
        """
        self.out_lq2_acute_rq = self.out_lq2_total_dose/self.larval_ld50
        return self.out_lq2_acute_rq

    def lq3_acute_rq(self):
        """
        Acute risk quotient for larval queen day 3
        """
        self.out_lq3_acute_rq = self.out_lq3_total_dose/self.larval_ld50
        return self.out_lq3_acute_rq

    def lq4_acute_rq(self):
        """
        Acute risk quotient for larval queen day 4
        """
        self.out_lq4_acute_rq = self.out_lq4_total_dose/self.larval_ld50
        return self.out_lq4_acute_rq

    def aw_cell_acute_rq(self):
        """
        Acute risk quotient for adult worker (cell cleaning and capping)
        """
        self.out_aw_cell_acute_rq = self.out_aw_cell_total_dose/self.adult_oral_ld50
        return self.out_aw_cell_acute_rq

    def aw_brood_acute_rq(self):
        """
        Acute risk quotient for adult worker (brood and queen tending, nurse bees)
        """
        self.out_aw_brood_acute_rq = self.out_aw_brood_total_dose/self.adult_oral_ld50
        return self.out_aw_brood_acute_rq

    def aw_comb_acute_rq(self):
        """
        Acute risk quotient for adult worker (comb building, cleaning, and food handling)
        """
        self.out_aw_comb_acute_rq = self.out_aw_comb_total_dose/self.adult_oral_ld50
        return self.out_aw_comb_acute_rq

    def aw_pollen_acute_rq(self):
        """
        Acute risk quotient for adult worker (foraging for pollen)
        """
        self.out_aw_pollen_acute_rq = self.out_aw_pollen_total_dose/self.adult_oral_ld50
        return self.out_aw_pollen_acute_rq

    def aw_nectar_acute_rq(self):
        """
        Acute risk quotient for adult worker (foraging for nectar)
        """
        self.out_aw_nectar_acute_rq = self.out_aw_nectar_total_dose/self.adult_oral_ld50
        return self.out_aw_nectar_acute_rq

    def aw_winter_acute_rq(self):
        """
        Acute risk quotient for adult worker (maintenance of hive in winter)
        """
        self.out_aw_winter_acute_rq = self.out_aw_winter_total_dose/self.adult_oral_ld50
        return self.out_aw_winter_acute_rq

    def ad_acute_rq(self):
        """
        Acute risk quotient for adult drone
        """
        self.out_ad_acute_rq = self.out_ad_total_dose/self.adult_oral_ld50
        return self.out_ad_acute_rq

    def aq_acute_rq(self):
        """
        Acute risk quotient for adult queen
        """
        self.out_aq_acute_rq = self.out_aq_total_dose/self.adult_oral_ld50
        return self.out_aq_acute_rq

    def lw1_chronic_rq(self):
        """
        Chronic risk quotient for larval worker day 1
        """
        self.out_lw1_chronic_rq = self.out_lw1_total_dose/self.larval_noael
        return self.out_lw1_chronic_rq

    def lw2_chronic_rq(self):
        """
        Chronic risk quotient for larval worker day 2
        """
        self.out_lw2_chronic_rq = self.out_lw2_total_dose/self.larval_noael
        return self.out_lw2_chronic_rq

    def lw3_chronic_rq(self):
        """
        Chronic risk quotient for larval worker day 3
        """
        self.out_lw3_chronic_rq = self.out_lw3_total_dose/self.larval_noael
        return self.out_lw3_chronic_rq

    def lw4_chronic_rq(self):
        """
        Chronic risk quotient for larval worker day 4
        """
        self.out_lw4_chronic_rq = self.out_lw4_total_dose/self.larval_noael
        return self.out_lw4_chronic_rq

    def lw5_chronic_rq(self):
        """
        Chronic risk quotient for larval worker day 5
        """
        self.out_lw5_chronic_rq = self.out_lw5_total_dose/self.larval_noael
        return self.out_lw5_chronic_rq

    def ld6_chronic_rq(self):
        """
        Chronic risk quotient for larval drone aged 6+ days
        """
        self.out_ld6_chronic_rq = self.out_ld6_total_dose/self.larval_noael
        return self.out_ld6_chronic_rq

    def lq1_chronic_rq(self):
        """
        Chronic risk quotient for larval queen day 1
        """
        self.out_lq1_chronic_rq = self.out_lq1_total_dose/self.larval_noael
        return self.out_lq1_chronic_rq

    def lq2_chronic_rq(self):
        """
        Chronic risk quotient for larval queen day 2
        """
        self.out_lq2_chronic_rq = self.out_lq2_total_dose/self.larval_noael
        return self.out_lq2_chronic_rq

    def lq3_chronic_rq(self):
        """
        Chronic risk quotient for larval queen day 3
        """
        self.out_lq3_chronic_rq = self.out_lq3_total_dose/self.larval_noael
        return self.out_lq3_chronic_rq

    def lq4_chronic_rq(self):
        """
        Chronic risk quotient for larval queen aged 4+ days
        """
        self.out_lq4_chronic_rq = self.out_lq4_total_dose/self.larval_noael
        return self.out_lq4_chronic_rq

    def aw_cell_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (cell cleaning and capping)
        """
        self.out_aw_cell_chronic_rq = self.out_aw_cell_total_dose/self.adult_oral_noael
        return self.out_aw_cell_chronic_rq

    def aw_brood_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (brood and queen tending, nurse bees)
        """
        self.out_aw_brood_chronic_rq = self.out_aw_brood_total_dose/self.adult_oral_noael
        return self.out_aw_brood_chronic_rq

    def aw_comb_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (comb building, cleaning, and food handling)
        """
        self.out_aw_comb_chronic_rq = self.out_aw_comb_total_dose/self.adult_oral_noael
        return self.out_aw_comb_chronic_rq

    def aw_pollen_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (foraging for pollen)
        """
        self.out_aw_pollen_chronic_rq = self.out_aw_pollen_total_dose/self.adult_oral_noael
        return self.out_aw_pollen_chronic_rq

    def aw_nectar_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (foraging for nectar)
        """
        self.out_aw_nectar_chronic_rq = self.out_aw_nectar_total_dose/self.adult_oral_noael
        return self.out_aw_nectar_chronic_rq

    def aw_winter_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (maintenance of hive in winter)
        """
        self.out_aw_winter_chronic_rq = self.out_aw_winter_total_dose/self.adult_oral_noael
        return self.out_aw_winter_chronic_rq

    def ad_chronic_rq(self):
        """
        Chronic risk quotient for adult drone
        """
        self.out_ad_chronic_rq = self.out_ad_total_dose/self.adult_oral_noael
        return self.out_ad_chronic_rq

    def aq_chronic_rq(self):
        """
        Chronic risk quotient for adult queen (laying 1500 eggs/day)
        """
        self.out_aq_chronic_rq = self.out_aq_total_dose/self.adult_oral_noael
        return self.out_aq_chronic_rq

    def set_global_constants(self):
        self.n_runs = len(self.application_method)
        if self.n_runs == 0:
            print('no runs to do')
        boolog = True
        if boolog:
            print('application method')
            print(self.application_method)
            print('number of runs')
            print(self.n_runs)
        self.out_eec_spray = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_eec_spray", dtype="float")
        self.out_eec_soil = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_eec_soil", dtype="float")
        self.out_eec_seed = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_eec_seed", dtype="float")
        self.out_eec_tree = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_eec_tree", dtype="float")
        self.out_eec = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_eec", dtype="float")
        self.out_lw1_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lw1_total_dose", dtype="float")
        self.out_lw2_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lw2_total_dose", dtype="float")
        self.out_lw3_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lw3_total_dose", dtype="float")
        self.out_ld6_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_ld6_total_dose", dtype="float")
        self.out_lq1_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lq1_total_dose", dtype="float")
        self.out_lq2_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lq2_total_dose", dtype="float")
        self.out_lq3_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lq3_total_dose", dtype="float")
        self.out_lq4_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lq4_total_dose", dtype="float")
        self.out_lw4_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lw4_total_dose", dtype="float")
        self.out_lw5_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_lw5_total_dose", dtype="float")
        self.out_aw_cell_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aw_cell_total_dose", dtype="float")
        self.out_aw_brood_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aw_brood_total_dose", dtype="float")
        self.out_aw_comb_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aw_comb_total_dose", dtype="float")
        self.out_aw_pollen_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aw_pollen_total_dose", dtype="float")
        self.out_aw_nectar_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aw_nectar_total_dose", dtype="float")
        self.out_aw_winter_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aw_winter_total_dose", dtype="float")
        self.out_ad_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_ad_total_dose", dtype="float")
        self.out_aq_total_dose = pd.Series(np.nan, index=list(range(self.n_runs)), name="out_aq_total_dose", dtype="float")

# if __name__ == '__main__':
#     pd_in = pd.DataFrame({
#         "application_rate": [1.2],
#         "application_method": ['foliar spray'],
#         "empirical_residue": ['FALSE'],
#         "empirical_pollen": [1.],
#         "empirical_nectar": [0.4],
#         "empirical_jelly": [0.5],
#         "adult_contact_ld50": [2.2],
#         "adult_oral_ld50": [3.5],
#         "adult_oral_noael": [1.7],
#         "larval_ld50": [0.8],
#         "larval_noael": [0.5],
#         "log_kow": [0.24],
#         "koc": [12.3],
#         "mass_tree_vegetation": [69.3],
#         "lw1_jelly": [1.9],
#         "lw2_jelly": [9.4],
#         "lw3_jelly": [19.],
#         "lw4_nectar": [60.],
#         "lw4_pollen": [1.8],
#         "lw5_nectar": [120.],
#         "lw5_pollen": [3.6],
#         "ld6_nectar": [130.],
#         "ld6_pollen": [3.6],
#         "lq1_jelly": [1.9],
#         "lq2_jelly": [9.4],
#         "lq3_jelly": [23.],
#         "lq4_jelly": [141.],
#         "aw_cell_nectar": [60.],
#         "aw_cell_pollen": [6.65],
#         "aw_brood_nectar": [140.],
#         "aw_brood_pollen": [9.6],
#         "aw_comb_nectar": [60.],
#         "aw_comb_pollen": [1.7],
#         "aw_fpollen_nectar": [43.5],
#         "aw_fpollen_pollen": [0.041],
#         "aw_fnectar_nectar": [292.],
#         "aw_fnectar_pollen": [0.041],
#         "aw_winter_nectar": [29.],
#         "aw_winter_pollen": [2.],
#         "ad_nectar": [235.],
#         "ad_pollen": [0.0002],
#         "aq_jelly": [525.],
#     })
#     output = Beerex(pd_in, None)
#     output.execute_model()
#     print("Model has been run")