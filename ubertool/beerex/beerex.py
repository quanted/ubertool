from __future__ import division
# from ..base.ubertool import UberModel
from ubertool.base.ubertool import UberModel
import pandas as pd


class BeerexInputs(object):
    """
    Input class for Beerex
    """
    def __init__(self):
        """Class representing the inputs for Beerex"""
        super(BeerexInputs, self).__init__()
        self.application_rate = pd.Series([], dtype="float")
        self.application_method = pd.Series([], dtype="object")
        self.application_units = pd.Series([], dtype="object")
        self.empirical_residue = pd.Series([], dtype="object")
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
        self.out_eec_method = pd.Series(name="out_eec_method").astype("object")
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
        self.out_awcell_total_dose = pd.Series(name="out_awcell_total_dose").astype("float")
        self.out_awbrood_total_dose = pd.Series(name="out_awbrood_total_dose").astype("float")
        self.out_awcomb_total_dose = pd.Series(name="out_awcomb_total_dose").astype("float")
        self.out_awpollen_total_dose = pd.Series(name="out_awpollen_total_dose").astype("float")
        self.out_awnectar_total_dose = pd.Series(name="out_awnectar_total_dose").astype("float")
        self.out_awwinter_total_dose = pd.Series(name="out_awwinter_total_dose").astype("float")
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
        self.out_awcell_acute_rq = pd.Series(name="out_awcell_acute_rq").astype("float")
        self.out_awbrood_acute_rq = pd.Series(name="out_awbrood_acute_rq").astype("float")
        self.out_awcomb_acute_rq = pd.Series(name="out_awcomb_acute_rq").astype("float")
        self.out_awpollen_acute_rq = pd.Series(name="out_awpollen_acute_rq").astype("float")
        self.out_awnectar_acute_rq = pd.Series(name="out_awnectar_acute_rq").astype("float")
        self.out_awwinter_acute_rq = pd.Series(name="out_awwinter_acute_rq").astype("float")
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
        self.out_awcell_chronic_rq = pd.Series(name="out_awcell_chronic_rq").astype("float")
        self.out_awbrood_chronic_rq = pd.Series(name="out_awbrood_chronic_rq").astype("float")
        self.out_awcomb_chronic_rq = pd.Series(name="out_awcomb_chronic_rq").astype("float")
        self.out_awpollen_chronic_rq = pd.Series(name="out_awpollen_chronic_rq").astype("float")
        self.out_awnectar_chronic_rq = pd.Series(name="out_awnectar_chronic_rq").astype("float")
        self.out_awwinter_chronic_rq = pd.Series(name="out_awwinter_chronic_rq").astype("float")
        self.out_ad_chronic_rq = pd.Series(name="out_ad_chronic_rq").astype("float")
        self.out_aq_chronic_rq = pd.Series(name="out_aq_chronic_rq").astype("float")
        self.out_adult_acute_contact = pd.Series(name="out_adult_acute_contact").astype("float")
        self.out_adult_acute_dietary = pd.Series(name="out_adult_acute_dietary").astype("float")
        self.out_adult_chronic_dietary = pd.Series(name="out_adult_chronic_dietary").astype("float")
        self.out_larvae_acute_dietary = pd.Series(name="out_larvae_acute_dietary").astype("float")
        self.out_larvae_chronic_dietary = pd.Series(name="out_larvae_chronic_dietary").astype("float")


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
        self.populate_inputs(self.pd_obj, self)
        self.pd_obj_out = self.populate_outputs(self)
        self.run_methods()
        self.fill_output_dataframe(self)

    def run_methods(self):
        """Execute the model's methods to generate the model output"""
        try:
            self.eec_spray()
            self.eec_soil()
            self.eec_seed()
            self.eec_tree()
            self.eec_method()
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
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    def eec_spray(self):
        """
        EEC for foliar spray
        """
        self.out_eec_spray = (110 * self.application_rate) / 1000
        return self.out_eec_spray

    def eec_soil(self):
        """
        EEC for soil application
        """
        self.out_eec_soil = ((10**(0.95*self.log_kow-2.05)+0.82) *
                             (-0.0648*(self.log_kow**2)+0.2431*self.log_kow+0.5822) *
                             (1.5/(0.2+1.5*self.koc*0.01)) * (0.5 * self.application_rate)) / 1000
        return self.out_eec_soil

    def eec_seed(self):
        """
        EEC for seed treatment
        """
        self.out_eec_seed = 1 * (self.lw4_pollen + self.lw4_nectar)/1000
        return self.out_eec_seed

    def eec_tree(self):
        """
        EEC for tree trunk
        """
        self.out_eec_tree = (self.application_rate/self.mass_tree_vegetation) / 1000
        return self.out_eec_tree

    def eec_method(self):
        """
        determine which application method is used for subsequent EEC and RQ calculations
        """
        if self.application_method == "foliar spray":
            self.out_eec_method = self.out_eec_spray
        elif self.application_method == "soil application":
            self.out_eec_method = self.out_eec_soil
        elif self.application_method == "seed treatment":
            self.out_eec_method = self.out_eec_seed
        elif self.application_method == "tree trunk":
            self.out_eec_method = self.out_eec_tree
        return self.out_eec_method

    def lw1_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 1
        """
        self.out_lw1_total_dose = (self.out_eec_method/100) * self.lw1_jelly
        return self.out_lw1_total_dose

    def lw2_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 2
        """
        self.out_lw2_total_dose = (self.out_eec_method/100) * self.lw2_jelly
        return self.out_lw2_total_dose

    def lw3_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 3
        """
        self.out_lw3_total_dose = (self.out_eec_method/100) * self.lw3_jelly
        return self.out_lw3_total_dose

    def lw4_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 4
        """
        self.out_lw4_total_dose = (self.out_eec_method * self.lw4_pollen) + (self.out_eec_method * self.lw4_nectar)
        return self.out_lw4_total_dose

    def lw5_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval worker day 5
        """
        self.out_lw5_total_dose = (self.out_eec_method * self.lw5_pollen) + (self.out_eec_method * self.lw5_nectar)
        return self.out_lw5_total_dose

    def ld6_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval drone aged 6+ days
        """
        self.out_ld6_total_dose = (self.out_eec_method * self.ld6_pollen) + (self.out_eec_method * self.ld6_nectar)
        return self.out_ld6_total_dose

    def lq1_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen day 1
        """
        self.out_lq1_total_dose = (self.out_eec_method/100) * self.lq1_jelly
        return self.out_lq1_total_dose

    def lq2_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen day 2
        """
        self.out_lq2_total_dose = (self.out_eec_method/100) * self.lq2_jelly
        return self.out_lq2_total_dose

    def lq3_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen day 3
        """
        self.out_lq3_total_dose = (self.out_eec_method/100) * self.lq3_jelly
        return self.out_lq3_total_dose

    def lq4_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for larval queen aged 4+ days
        """
        self.out_lq4_total_dose = (self.out_eec_method/100) * self.lq4_jelly
        return self.out_lq4_total_dose

    def aw_cell_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (cell cleaning and capping)
        """
        self.out_awcell_total_dose = (self.out_eec_method * self.aw_cell_nectar) + (self.out_eec_method * self.aw_cell_pollen)
        return self.out_awcell_total_dose

    def aw_brood_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (brood and queen tending, nurse bees)
        """
        self.out_awbrood_total_dose = (self.out_eec_method * self.aw_brood_nectar) + (self.out_eec_method * self.aw_brood_pollen)
        return self.out_awbrood_total_dose

    def aw_comb_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (comb building, cleaning, and food handling)
        """
        self.out_awcomb_total_dose = (self.out_eec_method * self.aw_comb_nectar) + (self.out_eec_method * self.aw_comb_pollen)
        return self.out_awcomb_total_dose

    def aw_pollen_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (foraging for pollen)
        """
        self.out_awpollen_total_dose = (self.out_eec_method * self.aw_fpollen_nectar) + (self.out_eec_method * self.aw_fpollen_pollen)
        return self.out_awpollen_total_dose

    def aw_nectar_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (foraging for nectar)
        """
        self.out_awnectar_total_dose = (self.out_eec_method * self.aw_fnectar_nectar) + (self.out_eec_method * self.aw_fnectar_pollen)
        return self.out_awnectar_total_dose

    def aw_winter_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult worker (maintenance of hive in winter)
        """
        self.out_awwinter_total_dose = (self.out_eec_method * self.aw_winter_nectar) + (self.out_eec_method * self.aw_winter_pollen)
        return self.out_awwinter_total_dose

    def ad_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult drone
        """
        self.out_ad_total_dose = (self.out_eec_method * self.ad_nectar) + (self.out_eec_method * self.ad_pollen)
        return self.out_ad_total_dose

    def aq_total_dose(self):
        """
        Pesticide dose in ug a.i./bee for adult queen (laying 1500 eggs/day)
        """
        self.out_aq_total_dose = (self.out_eec_method/100) * self.aq_jelly
        return self.out_aq_total_dose

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
        self.out_awcell_acute_rq = self.out_awcell_total_dose/self.adult_oral_ld50
        return self.out_awcell_acute_rq

    def aw_brood_acute_rq(self):
        """
        Acute risk quotient for adult worker (brood and queen tending, nurse bees)
        """
        self.out_awbrood_acute_rq = self.out_awbrood_total_dose/self.adult_oral_ld50
        return self.out_awbrood_acute_rq

    def aw_comb_acute_rq(self):
        """
        Acute risk quotient for adult worker (comb building, cleaning, and food handling)
        """
        self.out_awcomb_acute_rq = self.out_awcomb_total_dose/self.adult_oral_ld50
        return self.out_awcomb_acute_rq

    def aw_pollen_acute_rq(self):
        """
        Acute risk quotient for adult worker (foraging for pollen)
        """
        self.out_awpollen_acute_rq = self.out_awpollen_total_dose/self.adult_oral_ld50
        return self.out_awpollen_acute_rq

    def aw_nectar_acute_rq(self):
        """
        Acute risk quotient for adult worker (foraging for nectar)
        """
        self.out_awnectar_acute_rq = self.out_awnectar_total_dose/self.adult_oral_ld50
        return self.out_awnectar_acute_rq

    def aw_winter_acute_rq(self):
        """
        Acute risk quotient for adult worker (maintenance of hive in winter)
        """
        self.out_awwinter_acute_rq = self.out_awwinter_total_dose/self.adult_oral_ld50
        return self.out_awwinter_acute_rq

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
        self.out_lw3_chronic_rq = self.out_lw2_total_dose/self.larval_noael
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
        self.out_awcell_chronic_rq = self.out_awcell_total_dose/self.adult_oral_noael
        return self.out_awcell_chronic_rq

    def aw_brood_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (brood and queen tending, nurse bees)
        """
        self.out_awbrood_chronic_rq = self.out_awbrood_total_dose/self.adult_oral_noael
        return self.out_awbrood_chronic_rq

    def aw_comb_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (comb building, cleaning, and food handling)
        """
        self.out_awcomb_chronic_rq = self.out_awcomb_total_dose/self.adult_oral_noael
        return self.out_awcomb_chronic_rq

    def aw_pollen_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (foraging for pollen)
        """
        self.out_awpollen_chronic_rq = self.out_awpollen_total_dose/self.adult_oral_noael
        return self.out_awpollen_chronic_rq

    def aw_nectar_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (foraging for nectar)
        """
        self.out_awnectar_chronic_rq = self.out_awnectar_total_dose/self.adult_oral_noael
        return self.out_awnectar_chronic_rq

    def aw_winter_chronic_rq(self):
        """
        Chronic risk quotient for adult worker (maintenance of hive in winter)
        """
        self.out_awwinter_chronic_rq = self.out_awwinter_total_dose/self.adult_oral_noael
        return self.out_awwinter_chronic_rq

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


if __name__ == '__main__':
    pd_in = pd.DataFrame({
        "application_rate": [1.2],
        "application_method": ['foliar spray'],
        "application_units": [],
        "empirical_residue": [],
        "adult_contact_ld50": [],
        "adult_oral_ld50": [],
        "adult_oral_noael": [],
        "larval_ld50": [],
        "larval_noael": [],
        "log_kow": [],
        "koc": [],
        "mass_tree_vegetation": [],
        "lw1_jelly": [],
        "lw2_jelly": [],
        "lw3_jelly": [],
        "lw4_nectar": [],
        "lw4_pollen": [],
        "lw5_nectar": [],
        "lw5_pollen": [],
        "ld6_nectar": [],
        "ld6_pollen": [],
        "lq1_jelly": [],
        "lq2_jelly": [],
        "lq3_jelly": [],
        "lq4_jelly": [],
        "aw_cell_nectar": [],
        "aw_cell_pollen": [],
        "aw_brood_nectar": [],
        "aw_brood_pollen": [],
        "aw_comb_nectar": [],
        "aw_comb_pollen": [],
        "aw_fpollen_nectar": [],
        "aw_fpollen_pollen": [],
        "aw_fnectar_nectar": [],
        "aw_fnectar_pollen": [],
        "aw_winter_nectar": [],
        "aw_winter_pollen": [],
        "ad_nectar": [],
        "ad_pollen": [],
        "aq_jelly": [],
    })
    output = Beerex(pd_in, None)
    output.execute_model()
    print "Nothing"