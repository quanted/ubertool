from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import datetime
import inspect
import numpy as np
import numpy.testing as npt
import os.path
import pandas as pd
import sys
from tabulate import tabulate
import unittest

print("Python version: " + sys.version)
print("Numpy version: " + np.__version__)

#find parent directory and import model
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parent_dir)

from kabam_exe import Kabam

test = {}

class TestKabam(unittest.TestCase):
    """
    Unit tests for Kabam model.
    : unittest will
    : 1) call the setup method,
    : 2) then call every method starting with "test",
    : 3) then the teardown method
    """
    print("kabam unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for Kabam unit tests.
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open Kabam qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for Kabam unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def create_kabam_object(self):
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty kabam object
        kabam_empty = Kabam(df_empty, df_empty)
        return kabam_empty

    def test_ventilation_rate(self):
        """
        :description Ventilation rate of aquatic animal
        :unit L/d
        :expression Kabam Eq. A5.2b (Gv)
        :param zoo_wb: wet weight of animal (kg)
        :param conc_do: concentration of dissolved oxygen (mg O2/L)
        :return:
        """
        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 0.00394574, 0.468885], dtype = 'float')

        try:
            #use the zooplankton variables/values for the test
            kabam_empty.zoo_wb = pd.Series(['nan', 1.e-07, 1.e-4], dtype = 'float')
            kabam_empty.conc_do = pd.Series([5.0, 10.0, 7.5], dtype='float')

            result = kabam_empty.ventilation_rate(kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_pest_uptake_eff_gills(self):
        """
        :description Pesticide uptake efficiency by gills
        :unit fraction
        "expresssion Kabam Eq. A5.2a (Ew)
        :param log kow: octanol-water partition coefficient ()
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 0.540088, 0.540495], dtype = 'float')

        try:
            kabam_empty.log_kow = pd.Series(['nan', 5., 6.], dtype = 'float')
            kabam_empty.kow = 10.**(kabam_empty.log_kow)

            result = kabam_empty.pest_uptake_eff_bygills()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_phytoplankton_k1_calc(self):
        """
        :description Uptake rate constant through respiratory area for phytoplankton
        :unit: L/kg*d
        :expression Kabam Eq. A5.1  (K1:unique to phytoplankton)
        :param log kow: octanol-water partition coefficient ()
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([1639.34426, 8695.6521, 15267.1755], dtype = 'float')

        try:

            kabam_empty.log_kow = pd.Series([4., 5., 6.], dtype = 'float')
            kabam_empty.kow = 10.**(kabam_empty.log_kow)
            result = kabam_empty.phytoplankton_k1_calc(kabam_empty.kow)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_aq_animal_k1_calc(self):
        """
        U:description ptake rate constant through respiratory area for aquatic animals
        :unit: L/kg*d
        :expression Kabam Eq. A5.2 (K1)
        :param pest_uptake_eff_bygills: Pesticide uptake efficiency by gills of aquatic animals (fraction)
        :param vent_rate: Ventilation rate of aquatic animal (L/d)
        :param wet_wgt: wet weight of animal (kg)

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 1201.13849, 169.37439], dtype = 'float')

        try:
            pest_uptake_eff_bygills = pd.Series(['nan', 0.0304414, 0.0361228], dtype = 'float')
            vent_rate = pd.Series(['nan', 0.00394574, 0.468885], dtype = 'float')
            wet_wgt = pd.Series(['nan', 1.e-07, 1.e-4], dtype = 'float')

            result = kabam_empty.aq_animal_k1_calc(pest_uptake_eff_bygills, vent_rate, wet_wgt)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_animal_water_part_coef(self):
        """
        :description Organism-Water partition coefficient (based on organism wet weight)
        :unit ()
        :expression Kabam Eq. A6a (Kbw)
        :param zoo_lipid: lipid fraction of organism (kg lipid/kg organism wet weight)
        :param zoo_nlom: non-lipid organic matter (NLOM) fraction of organism (kg NLOM/kg organism wet weight)
        :param zoo_water: water content of organism (kg water/kg organism wet weight)
        :param kow: octanol-water partition coefficient ()
        :param beta: proportionality constant expressing the sorption capacity of NLOM or NLOC to
                     that of octanol
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([650.87, 11000.76, 165000.64], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            kabam_empty.zoo_lipid_frac = pd.Series([0.03, 0.04, 0.06], dtype = 'float')
            kabam_empty.zoo_nlom_frac = pd.Series([0.10, 0.20, 0.30,], dtype = 'float')
            kabam_empty.zoo_water_frac = pd.Series([0.87, 0.76, 0.64], dtype = 'float')
            kabam_empty.kow = pd.Series([1.e4, 1.e5, 1.e6], dtype = 'float')
            beta = 0.35

            result = kabam_empty.animal_water_part_coef(kabam_empty.zoo_lipid_frac,
                                            kabam_empty.zoo_nlom_frac,
                                            kabam_empty.zoo_water_frac, beta)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return


    def test_aq_animal_k2_calc(self):
        """
        :description Elimination rate constant through the respiratory area
        :unit (per day)
        :expression Kabam Eq. A6 (K2)
        :param zoo_k1: Uptake rate constant through respiratory area for aquatic animals
        :param k_bw_zoo (Kbw): Organism-Water partition coefficient (based on organism wet weight ()
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([2.5186969, 0.79045921, 0.09252798], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            kabam_empty.zoo_k1 = pd.Series([1639.34426, 8695.6521, 15267.1755], dtype = 'float')
            kabam_empty.k_bw_zoo = pd.Series([650.87, 11000.76, 165000.64], dtype = 'float')

            result = kabam_empty.aq_animal_k2_calc(kabam_empty.zoo_k1, kabam_empty.k_bw_zoo)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_animal_grow_rate_const(self):
        """
        :description Aquatic animal/organism growth rate constant
        :unit (per day)
        :expression Kabam Eq. A7.1 & A7.2
        :param zoo_wb: wet weight of animal/organism (kg)
        :param water_temp: water temperature (degrees C)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.01255943, 0.00125594, 0.00251], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            kabam_empty.zoo_wb = pd.Series([1.e-7, 1.e-2, 1.0], dtype = 'float')
            kabam_empty.water_temp = pd.Series([10., 15., 20.], dtype = 'float')

            result = kabam_empty.animal_grow_rate_const(kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_dietary_trans_eff(self):
        """
        :description Aquatic animal/organizm dietary pesticide transfer efficiency
        :unit fraction
        :expression Kabam Eq. A8a (Ed)
        :param kow: octanol-water partition coefficient ()
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.499251, 0.492611, 0.434783], dtype = 'float')

        try:
            kabam_empty.kow = pd.Series([1.e4, 1.e5, 1.e6], dtype = 'float')

            result = kabam_empty.dietary_trans_eff()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_aq_animal_feeding_rate(self):
        """
        :description Aquatic animal feeding rate (except filterfeeders)
        :unit kg/d
        :expression Kabam Eq. A8b1 (Gd)
        :param wet_wgt: wet weight of animal/organism (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([4.497792e-08, 1.0796617e-3, 0.073042572], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            kabam_empty.zoo_wb = pd.Series([1.e-7, 1.e-2, 1.], dtype = 'float')
            kabam_empty.water_temp = pd.Series([10., 15., 20.])

            result = kabam_empty.aq_animal_feeding_rate(kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_filterfeeder_feeding_rate(self):
        """
        :description Filter feeder feeding rate
        :unit kg/d
        :expression Kabam Eq. A8b2 (Gd)
        :param self.gv_filterfeeders: filterfeeder ventilation rate (L/d)
        :param self.conc_ss: Concentration of Suspended Solids (Css - kg/L)
        :param particle_scav_eff: efficiency of scavenging of particles absorbed from water (fraction)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 1.97287e-7, 0.03282195], dtype = 'float')

        try:
            kabam_empty.gv_filterfeeders = pd.Series(['nan', 0.00394574, 0.468885], dtype = 'float')
            kabam_empty.conc_ss = pd.Series([0.00005, 0.00005, 0.07], dtype = 'float')
            kabam_empty.particle_scav_eff = 1.0

            result = kabam_empty.filterfeeders_feeding_rate()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_diet_uptake_rate_const(self):
        """
        :description pesticide uptake rate constant for uptake through ingestion of food rate
        :unit kg food/kg organism - day
        :expression Kabam Eq. A8 (kD)
        :param dietary_trans_eff: dietary pesticide transfer efficiency (fraction)
        :param feeding rate: animal/organism feeding rate (kg/d)
        :param wet weight of aquatic animal/organism (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.22455272, 0.05318532, 0.031755767 ], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            kabam_empty.ed_zoo = pd.Series([0.499251, 0.492611, 0.434783], dtype = 'float')
            kabam_empty.gd_zoo = pd.Series([4.497792e-08, 1.0796617e-3, 0.073042572], dtype = 'float')
            kabam_empty.zoo_wb = pd.Series([1.e-7, 1.e-2, 1.0])

            result = kabam_empty.diet_uptake_rate_const(kabam_empty.ed_zoo,    \
                     kabam_empty.gd_zoo, kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_overall_diet_content(self):
        """
        :description Overall fraction of aquatic animal/organism diet attributed to diet food component
                    (i.e., lipids or NLOM or water)
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

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.025, 0.03355, 0.0465], dtype = 'float')

        try:
            #For test purposes we'll use the small fish diet variables/values
            kabam_empty.sfish_diet_sediment = pd.Series([0.0, 0.01, 0.05], dtype = 'float')
            kabam_empty.sfish_diet_phytoplankton = pd.Series([0.0, 0.01, 0.05], dtype = 'float')
            kabam_empty.sfish_diet_zooplankton = pd.Series([0.5, 0.4, 0.5], dtype = 'float')
            kabam_empty.sfish_diet_benthic_invertebrates = pd.Series([0.5, 0.57, 0.35], dtype = 'float')
            kabam_empty.sfish_diet_filterfeeders = pd.Series([0.0, 0.01, 0.05], dtype = 'float')

            kabam_empty.sediment_lipid = pd.Series([0.0, 0.01, 0.0], dtype = 'float')
            kabam_empty.phytoplankton_lipid = pd.Series([0.02, 0.015, 0.03], dtype = 'float')
            kabam_empty.zoo_lipid = pd.Series([0.03, 0.04, 0.05], dtype = 'float')
            kabam_empty.beninv_lipid = pd.Series([0.02, 0.03, 0.05], dtype = 'float')
            kabam_empty.filterfeeders_lipid = pd.Series([0.01, 0.02, 0.05], dtype = 'float')

            diet_elements = pd.Series([], dtype = 'float')
            content_fracs = pd.Series([], dtype = 'float')

            for i in range(len(kabam_empty.sfish_diet_sediment)):
                diet_elements = [kabam_empty.sfish_diet_sediment[i],
                                 kabam_empty.sfish_diet_phytoplankton[i],
                                 kabam_empty.sfish_diet_zooplankton[i],
                                 kabam_empty.sfish_diet_benthic_invertebrates[i],
                                 kabam_empty.sfish_diet_filterfeeders[i]]

                content_fracs = [kabam_empty.sediment_lipid[i],
                                 kabam_empty.phytoplankton_lipid[i],
                                 kabam_empty.zoo_lipid[i],
                                 kabam_empty.beninv_lipid[i],
                                 kabam_empty.filterfeeders_lipid[i]]

                result[i] = kabam_empty.overall_diet_content(diet_elements, content_fracs)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_fecal_egestion_rate_factor(self):
        """
        Aquatic animal/organism egestion rate of fecal matter factor (to be multiplied by the
        feeding rate to calculate egestion rate of fecal matter)
        :unit (kg feces)/[(kg organism) - day]
        :expression Kabam Eq. A9 (GF)
        :param epsilonL: dietary assimilation rate of lipids (fraction)
        :param epsilonN: dietary assimilation rate of NLOM (fraction)
        :param epsilonW: dietary assimilation rate of water (fraction)
        :param diet_lipid; lipid content of aquatic animal/organism diet (fraction)
        :param diet_nlom NLOM content of aquatic animal/organism diet (fraction)
        :param diet_water water content of aquatic animal/organism diet (fraction)
        :param feeding_rate: aquatic animal/organism feeding rate (kg/d)
        :return:
        """

        #this test includes two results; 'result1' represents the overall assimilation rate of the
        #aquatic animal/organism diet; and 'result' represents the product of this assimilation rate
        #and the feeding rate (this multiplication will be done in the main model routine
        #as opposed to within a method  -- the method here is limited to the assimilation factor
        #because this factor is used elsewhere as well

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        result1 = pd.Series([], dtype='float')
        expected_results = pd.Series([1.43e-9, 5.005e-5, 4.82625e-3], dtype = 'float')

        try:
            #For test purposes we'll use the zooplankton variable names and relevant constant values
            kabam_empty.epsilon_lipid_zoo = 0.72
            kabam_empty.epsilon_nlom_zoo = 0.60
            kabam_empty.epsilon_water = 0.25

            kabam_empty.v_ld_zoo = pd.Series([0.025, 0.035, 0.045], dtype = 'float')
            kabam_empty.v_nd_zoo = pd.Series([0.025, 0.035, 0.045], dtype = 'float')
            kabam_empty.v_wd_zoo = pd.Series([0.025, 0.035, 0.045], dtype = 'float')
            kabam_empty.gd_zoo = pd.Series([4.e-08, 1.e-3, 0.075], dtype = 'float')

            result1 = kabam_empty.fecal_egestion_rate_factor(kabam_empty.epsilon_lipid_zoo,
                                                                kabam_empty.epsilon_nlom_zoo,
                                                                kabam_empty.epsilon_water,
                                                                kabam_empty.v_ld_zoo,
                                                                kabam_empty.v_nd_zoo,
                                                                kabam_empty.v_wd_zoo)
            result = result1  * kabam_empty.gd_zoo
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_diet_elements_gut(self):
        """
        Fraction of diet elements (i.e., lipid, NLOM, water) in the gut
        :unit (kg lipid) / (kg digested wet weight)
        :expression Kabam Eq. A9 (VLG, VNG, VWG)
        :param (epison_lipid_*) relevant dietary assimilation rate (fraction)
        :param (v_ld_*) relevant overall diet content of diet element (kg/kg)
        :param (diet_assim_factor_*) relevant: Aquatic animal/organism egestion rate of fecal matter factor
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.2, 0.196, 0.1575], dtype = 'float')

        try:
            #for this test we'll use the lipid content for zooplankton
            kabam_empty.epsilon_lipid_zoo = 0.72
            kabam_empty.v_ld_zoo = pd.Series([0.025, 0.035, 0.045], dtype = 'float')
            kabam_empty.diet_assim_factor_zoo = pd.Series([0.035, 0.05, 0.08], dtype = 'float')

            result = kabam_empty.diet_elements_gut(kabam_empty.epsilon_lipid_zoo,
                    kabam_empty.v_ld_zoo, kabam_empty.diet_assim_factor_zoo)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_gut_organism_partition_coef(self):
        """
        Partition coefficient of the pesticide between the gastrointenstinal track and the organism
        :unit none
        :expression Kabam Eq. A9 (KGB)
        :param vlg_zoo: lipid content in the gut
        :param vng_zoo: nlom content in the gut
        :param vwg_zoo: water content in the gut
        :param kow: pesticide Kow
        :param beta_aq_animals: proportionality constant expressing the sorption capacity of NLOM to that of octanol
        :param zoo_lipid_frac: lipid content in the whole organism
        :param zoo_nlom_frac: nlom content in the whole organism
        :param zoo_water_frac: water content in the whole organism
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.991233, 1.662808, 1.560184], dtype = 'float')

        try:
            #for this test we'll use the zooplankton varialbles
            kabam_empty.beta_aq_animals = 0.035
            kabam_empty.kow = pd.Series([1.e4, 1.e5, 1.e6], dtype = 'float')
            kabam_empty.vlg_zoo = pd.Series([0.2, 0.25, 0.15], dtype = 'float')
            kabam_empty.vng_zoo = pd.Series([0.1, 0.15, 0.25], dtype = 'float')
            kabam_empty.vwg_zoo = pd.Series([0.15, 0.35, 0.05], dtype = 'float')
            kabam_empty.zoo_lipid_frac = pd.Series([0.20, 0.15, 0.10], dtype = 'float')
            kabam_empty.zoo_nlom_frac = pd.Series([0.15, 0.10, 0.05], dtype = 'float')
            kabam_empty.zoo_water_frac = pd.Series([0.65, 0.75, 0.85], dtype = 'float')

            result = kabam_empty.gut_organism_partition_coef(kabam_empty.vlg_zoo, kabam_empty.vng_zoo,
                                    kabam_empty.vwg_zoo, kabam_empty.kow, kabam_empty.beta_aq_animals,
                                    kabam_empty.zoo_lipid_frac, kabam_empty.zoo_nlom_frac,
                                    kabam_empty.zoo_water_frac)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_fecal_elim_rate_const(self):
        """
        rate constant for elimination of the pesticide through excretion of contaminated feces
        :unit per day
        :param gf_zoo: egestion rate of fecal matter (kg feces)/(kg organism-day)
        :param ed_zoo: dietary pesticide transfer efficiency (fraction)
        :param kgb_zoo: gut - partition coefficient of the pesticide between the gastrointestinal tract
                          and the organism (-)
        :param zoo_wb: wet weight of organism (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([7.5e-4, 0.0525, 5.625e-4], dtype = 'float')

        try:
            #for this test we'll use the zooplankton variables
            kabam_empty.gf_zoo = pd.Series([1.5e-9, 5.0e-5, 4.5e-3], dtype = 'float')
            kabam_empty.ed_zoo = pd.Series([0.5, 0.7, 0.25], dtype = 'float')
            kabam_empty.kgb_zoo = pd.Series([1.0, 1.5, 0.5], dtype = 'float')
            kabam_empty.zoo_wb = pd.Series([1.e-6, 1.e-3, 1.0], dtype = 'float')

            result = kabam_empty.fecal_elim_rate_const(kabam_empty.gf_zoo, kabam_empty.ed_zoo,
                                                            kabam_empty.kgb_zoo, kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_frac_pest_freely_diss(self):
        """
        Calculate Fraction of pesticide freely dissolved in water column (that can be
        absorbed via membrane diffusion)
        :unit fraction
        :expression Kabam Eq. A2
        :param conc_poc: Concentration of Particulate Organic Carbon in water column (kg OC/L)
        :param kow: octonal-water partition coefficient (-)
        :param conc_doc: Concentration of Dissolved Organic Carbon in water column (kg OC/L)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.13422819, 0.00462963, 0.00514139], dtype = 'float')

        try:
            #for this test we'll use the zooplankton variables
            kabam_empty.conc_poc = pd.Series([1.5e-3, 5.0e-3, 4.5e-4], dtype = 'float')
            kabam_empty.alpha_poc = 0.35
            kabam_empty.kow = pd.Series([1.e4, 1.e5, 1.e6], dtype = 'float')
            kabam_empty.conc_doc = pd.Series([1.5e-3, 5.0e-3, 4.5e-4], dtype = 'float')
            kabam_empty.alpha_doc = 0.08

            result = kabam_empty.frac_pest_freely_diss()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_freely_diss_watercol(self):
        """
        concentration of freely dissolved pesticide in overlying water column
        :unit g/L
        :param phi: Fraction of pesticide freely dissolved in water column (that can be
                    absorbed via membrane diffusion) (fraction)
        :param water_column_eec: Water Column 1-in-10 year EECs (ug/L)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([1.e-1, 2.4e-2, 1.], dtype = 'float')

        try:
            #for this test we'll use the zooplankton variables
            kabam_empty.phi = pd.Series([0.1, 0.004, 0.05], dtype = 'float')
            kabam_empty.water_column_eec = pd.Series([1., 6., 20.], dtype = 'float')

            result = kabam_empty.conc_freely_diss_watercol()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def  test_conc_sed_norm_4oc(self):
        """
        pesticide concentration in sediment normalized for organic carbon
        :unit g/(kg OC)
        :expression Kabam Eq. A4a
        :param pore_water_eec: freely dissolved pesticide concentration in sediment pore water
        :param k_oc: organic carbon partition coefficient (L/kg OC)

        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([2.5e4, 6.e4, 2.e6], dtype = 'float')

        try:
            #for this test we'll use the zooplankton variables
            kabam_empty.k_oc = pd.Series([2.5e4, 1.e4, 1.e5], dtype = 'float')
            kabam_empty.pore_water_eec = pd.Series([1., 6., 20.], dtype = 'float')

            result = kabam_empty.conc_sed_norm_4oc()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_conc_sed_dry_wgt(self):
        """
        Calculate concentration of chemical in solid portion of sediment
        :unit g/(kg dry)
        :expression Kabam Eq. A4
        :param c_soc: pesticide concentration in sediment normalized for organic carbon g/(kg OC)
        :param sediment_oc: fraction organic carbon in sediment (fraction)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.001, 0.0036, 0.4], dtype = 'float')

        try:
            #for this test we'll use the zooplankton variables
            kabam_empty.c_soc = pd.Series([0.025, 0.06, 2.00], dtype = 'float')
            kabam_empty.sediment_oc = pd.Series([4., 6., 20.], dtype = 'float')
            kabam_empty.sediment_oc_frac = kabam_empty.percent_to_frac(kabam_empty.sediment_oc)

            result = kabam_empty.conc_sed_dry_wgt()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_diet_pest_conc(self):
        """
        overall concentration of pesticide in aquatic animal/organism diet
        :unit g/(kg wet weight)
        :expression Kabam Eq. A1 (SUM(Pi * CDi);
        :param diet_frac_lfish: fraction of large fish diet containing prey i (Pi in Eq. A1))
        :param diet_conc_lfish: concentraiton of pesticide in prey i (CDi in Eq. A1)
        :param lipid_content_lfish: fraction of prey i that is lipid
        :notes for this test we populate all prey items for large fish even though large fish
               typically only consume medium fish
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        result1 = pd.Series([], dtype='float')
        result2 = pd.Series([], dtype='float')
        expected_results1 = pd.Series([0.2025, 0.2025, 0.205], dtype = 'float')
        expected_results2 = pd.Series([5.316667, 4.819048, 4.3], dtype = 'float')

        try:
            #for this test we'll use the large fish variables (there are 7 prey items listed
            #for large fish (sediment, phytoplankton, zooplankton, benthic invertebrates,
            # filterfeeders, small fish, and medium fish  ---  this is the order related
            #to the values in the two series below)
            kabam_empty.diet_frac_lfish = pd.Series([[0.02, 0.03, 0.10, 0.05, 0.10, 0.7],
                                                [0.0, 0.05, 0.05, 0.05, 0.10, 0.75],
                                                [0.01, 0.02, 0.03, 0.04, 0.10, 0.8]], dtype = 'float')
            kabam_empty.diet_conc_lfish = pd.Series([[0.10, 0.10, 0.20, 0.15, 0.30, 0.20],
                                                [0.10, 0.10, 0.20, 0.15, 0.30, 0.20],
                                                [0.10, 0.10, 0.20, 0.15, 0.30, 0.20]], dtype = 'float')
            kabam_empty.diet_lipid_content_lfish = pd.Series([[0.0, 0.02, 0.03, 0.03, 0.04, 0.04],
                                                [0.01, 0.025, 0.035, 0.03, 0.04, 0.045],
                                                [0.0, 0.02, 0.03, 0.03, 0.05, 0.05]], dtype = 'float')


            result1,result2 = kabam_empty.diet_pest_conc(kabam_empty.diet_frac_lfish,
                                                     kabam_empty.diet_conc_lfish,
                                                     kabam_empty.diet_lipid_content_lfish)
            npt.assert_allclose(result1, expected_results1, rtol=1e-4, atol=0, err_msg='', verbose=True)

        finally:
            tab = [result1, expected_results1, result2, expected_results2]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_pest_conc_organism(self):
        """
        concentration of pesticide in aquatic animal/organism
        :unit g/(kg wet weight)
        :expression Kabam Eq. A1 (CB)
        :param lfish_k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param lfish_k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param lfish_kd: pesticide uptake rate constant for uptake through ingestion of food (kg food/(kg organism - day)
        :param lfish_ke: rate constant for elimination of the pesticide through excretion of feces (/d)
        :param lfish_kg: animal/organism growth rate constant (/d)
        :param lfish_km: rate constant for pesticide metabolic transformation (/d)
        :param lfish_mp: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param lfish_mo: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param cwto: total pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :param total_diet_conc_lfish: concentration of pesticide in overall diet of aquatic animal/organism (g/kg wet weight)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([1.97044e-3, 1.85185e-3, 3.97389e-3], dtype = 'float')

        try:
            kabam_empty.phi = pd.Series([1.0, 1.0, 1.0], dtype = 'float')
            kabam_empty.water_column_eec =  pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')
            kabam_empty.pore_water_eec =  pd.Series([1.e-4, 1.e-5, 2.e-3], dtype = 'float')
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.lfish_k1 =  pd.Series([10., 5., 2.], dtype = 'float')
            kabam_empty.lfish_k2 = pd.Series( [10., 5., 3.], dtype = 'float')
            kabam_empty.lfish_kd =  pd.Series([0.05, 0.03, 0.02], dtype = 'float')
            kabam_empty.lfish_ke =  pd.Series([0.05, 0.02, 0.02], dtype = 'float')
            kabam_empty.lfish_kg =  pd.Series([0.1, 0.01, 0.003], dtype = 'float')
            kabam_empty.lfish_km =  pd.Series([0.0, 0.1, 0.5], dtype = 'float')
            kabam_empty.lfish_mp =  pd.Series([0.0, 0.0, 0.05], dtype = 'float')
            kabam_empty.lfish_mo =  pd.Series([1.0, 1.0, 0.95], dtype = 'float')
            kabam_empty.total_diet_conc_lfish = pd.Series( [.20, .30, .50], dtype = 'float')

            result = kabam_empty.pest_conc_organism(kabam_empty.lfish_k1, kabam_empty.lfish_k2,
                                                     kabam_empty.lfish_kd, kabam_empty.lfish_ke,
                                                     kabam_empty.lfish_kg, kabam_empty.lfish_km,
                                                     kabam_empty.lfish_mp, kabam_empty.lfish_mo,
                                                     kabam_empty.total_diet_conc_lfish)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_lipid_norm_residue_conc(self):
        """
        Lipid normalized pesticide residue in aquatic animal/organism
        :unit ug/kg-lipid
        :expresssion represents a factor (CB/VLB) used in Kabam Eqs. F4, F5, & F6
        :param cb_lfish: total pesticide concentration in animal/organism (g/kg-ww)
        :param lfish_lipid_frac: fraction of animal/organism that is lipid (fraction)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.025, 0.00833333, 0.0005], dtype = 'float')

        try:
            #for this test we'll use the large fish variables
            kabam_empty.out_cb_lfish = pd.Series([1.e-3, 5.e-4, 1.e-5], dtype = 'float')
            kabam_empty.lfish_lipid_frac = pd.Series([0.04, 0.06, 0.02], dtype = 'float')
            kabam_empty.gms_to_microgms = 1.e6

            result = kabam_empty.lipid_norm_residue_conc(kabam_empty.out_cb_lfish,
                                                              kabam_empty.lfish_lipid_frac)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_pest_conc_diet_uptake(self):
        """
        :description Pesticide concentration in animal/organism originating from uptake through diet
        :unit g/kg ww
        :expression Kabam A1 (with k1 = 0)
        :param lfish_kD: pesticide uptake rate constant for uptake through ingestion of food (kg food/kg organizm - day)
        :param total_diet_conc: overall concentration of pesticide in diet of animal/organism (g/kg-ww)
        :param lfish_k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param lfish_kE: rate constant for elimination of the pesticide through excretion of feces (/d)
        :param lfish_kG: animal/organism growth rate constant (/d)
        :param lfish_kM: rate constant for pesticide metabolic transformation (/d)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([9.8522e-4, 1.75439e-3, 2.83849e-3], dtype = 'float')

        try:

            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.lfish_k2 = pd.Series( [10., 5., 3.], dtype = 'float')
            kabam_empty.lfish_kd =  pd.Series([0.05, 0.03, 0.02], dtype = 'float')
            kabam_empty.lfish_ke =  pd.Series([0.05, 0.02, 0.02], dtype = 'float')
            kabam_empty.lfish_kg =  pd.Series([0.1, 0.01, 0.003], dtype = 'float')
            kabam_empty.lfish_km =  pd.Series([0.0, 0.1, 0.5], dtype = 'float')
            kabam_empty.total_diet_conc_lfish = pd.Series( [.20, .30, .50], dtype = 'float')

            result = kabam_empty.pest_conc_diet_uptake(kabam_empty.lfish_kd, kabam_empty.lfish_k2,
                                                            kabam_empty.lfish_ke, kabam_empty.lfish_kg,
                                                            kabam_empty.lfish_km,
                                                            kabam_empty.total_diet_conc_lfish)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_pest_conc_respir_uptake(self):
        """
        :description Pesticide concentration in animal/organism originating from uptake through respiration
        :unit g/kg ww
        :expression Kabam A1 (with kD = 0)
        :param lfish_k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param lfish_k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param lfish_kE: rate constant for elimination of the pesticide through excretion of feces (/d)
        :param lfish_kG: animal/organism growth rate constant (/d)
        :param lfish_kM: rate constant for pesticide metabolic transformation (/d)
        :param lfish_mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param lfish_mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param phi: fraction of the overlying water pesticide concentration that is freely dissolved and can be absorbed
                    via membrane diffusion (fraction)
        :param water_column_eec: total pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([9.8522167e-4, 9.746588e-5, 1.1353959e-3], dtype = 'float')

        try:
            kabam_empty.phi = pd.Series([1.0, 1.0, 1.0], dtype = 'float')
            kabam_empty.water_column_eec =  pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')
            kabam_empty.pore_water_eec =  pd.Series([1.e-4, 1.e-5, 2.e-3], dtype = 'float')
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.lfish_k1 =  pd.Series([10., 5., 2.], dtype = 'float')
            kabam_empty.lfish_k2 = pd.Series( [10., 5., 3.], dtype = 'float')
            kabam_empty.lfish_ke =  pd.Series([0.05, 0.02, 0.02], dtype = 'float')
            kabam_empty.lfish_kg =  pd.Series([0.1, 0.01, 0.003], dtype = 'float')
            kabam_empty.lfish_km =  pd.Series([0.0, 0.1, 0.5], dtype = 'float')
            kabam_empty.lfish_mp =  pd.Series([0.0, 0.0, 0.05], dtype = 'float')
            kabam_empty.lfish_mo =  pd.Series([1.0, 1.0, 0.95], dtype = 'float')

            result = kabam_empty.pest_conc_respir_uptake(kabam_empty.lfish_k1, kabam_empty.lfish_k2,
                                                     kabam_empty.lfish_ke, kabam_empty.lfish_kg,
                                                     kabam_empty.lfish_km, kabam_empty.lfish_mp,
                                                     kabam_empty.lfish_mo)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_tot_bioconc_fact(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.955, 1.00, 0.6666667], dtype = 'float')

        try:
            kabam_empty.phi = pd.Series([1.0, 1.0, 1.0], dtype = 'float')
            kabam_empty.water_column_eec =  pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')
            kabam_empty.pore_water_eec =  pd.Series([1.e-4, 1.e-5, 2.e-3], dtype = 'float')
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.lfish_k1 =  pd.Series([10., 5., 2.], dtype = 'float')
            kabam_empty.lfish_k2 = pd.Series( [10., 5., 3.], dtype = 'float')
            kabam_empty.lfish_mp =  pd.Series([0.05, 0.0, 0.05], dtype = 'float')
            kabam_empty.lfish_mo =  pd.Series([0.95, 1.0, 0.95], dtype = 'float')

            result = kabam_empty.tot_bioconc_fact(kabam_empty.lfish_k1, kabam_empty.lfish_k2,
                                                       kabam_empty.lfish_mp, kabam_empty.lfish_mo)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_lipid_norm_bioconc_fact(self):
        """
        :description Lipid normalized bioconcentration factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F2
        :param k1: pesticide uptake rate constant through respiratory area (gills, skin) (L/kg-d)
        :param k2: rate constant for elimination of the peisticide through the respiratory area (gills, skin) (/d)
        :param mP: fraction of respiratory ventilation that involves por-water of sediment (fraction)
        :param mO: fraction of respiratory ventilation that involves overlying water; 1-mP (fraction)
        :param lfish_lipid: fraction of animal/organism that is lipid (fraction)
        :param out_free_pest_conc_watercol: freely dissolved pesticide concentraiton in water column above sediment (g/L)
        :param pore_water_eec: freely dissovled pesticide concentration in pore-water of sediment (g/L)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([47.75, 25.0, 11.1111], dtype = 'float')

        try:
            kabam_empty.out_free_pest_conc_watercol = pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')
            kabam_empty.pore_water_eec =  pd.Series([1.e-4, 1.e-5, 2.e-3], dtype = 'float')
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.lfish_k1 =  pd.Series([10., 5., 2.], dtype = 'float')
            kabam_empty.lfish_k2 = pd.Series( [10., 5., 3.], dtype = 'float')
            kabam_empty.lfish_mp =  pd.Series([0.05, 0.0, 0.05], dtype = 'float')
            kabam_empty.lfish_mo =  pd.Series([0.95, 1.0, 0.95], dtype = 'float')
            kabam_empty.lfish_lipid = pd.Series([0.02, 0.04, 0.06], dtype = 'float')

            result = kabam_empty.lipid_norm_bioconc_fact(kabam_empty.lfish_k1, kabam_empty.lfish_k2,
                                                       kabam_empty.lfish_mp, kabam_empty.lfish_mo,
                                                       kabam_empty.lfish_lipid)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_tot_bioacc_fact(self):
        """
        :description Total bioaccumulation factor
        :unit (ug pesticide/kg ww) / (ug pesticide/L water)
        :expression Kabam Eq. F3
        :param cb_lfish: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param water_column_eec:  total pesticide concentraiton in water column above sediment (g/L)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.02, 25.0, 0.10], dtype = 'float')

        try:
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.out_cb_lfish = pd.Series([2.e-5, 2.5e-3, 2.e-4], dtype = 'float')
            kabam_empty.water_column_eec =  pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')

            result = kabam_empty.tot_bioacc_fact(kabam_empty.out_cb_lfish)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_lipid_norm_bioacc_fact(self):
        """
        :description Lipid normalized bioaccumulation factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F4
        :param cb_lfish: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param lfish_lipid: fraction of animal/organism that is lipid (fraction)
        :param out_free_pest_conc_watercol: freely dissolved pesticide concentration in water column above sediment (g/L)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([1.0, 625.0, 1.66666], dtype = 'float')

        try:
            kabam_empty.out_free_pest_conc_watercol = pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.out_cb_lfish = pd.Series([2.e-5, 2.5e-3, 2.e-4], dtype = 'float')
            kabam_empty.lfish_lipid = pd.Series([0.02, 0.04, 0.06], dtype = 'float')

            result = kabam_empty.lipid_norm_bioacc_fact(kabam_empty.out_cb_lfish, kabam_empty.lfish_lipid)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_biota_sed_acc_fact(self):
        """
        :description Biota-sediment accumulation factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/L water)
        :expression Kabam Eq. F5
        :param cb_lfish: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param lfish_lipid: fraction of animal/organism that is lipid (fraction)
        :param c_soc Pesticide concentration in sediment normalized for organic carbon content (g/kg OC)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.04, 1.0416666, 1.66666e-3], dtype = 'float')

        try:
            kabam_empty.c_soc = pd.Series([0.025, 0.06, 2.00], dtype = 'float')
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.out_cb_lfish = pd.Series([2.e-5, 2.5e-3, 2.e-4], dtype = 'float')
            kabam_empty.lfish_lipid = pd.Series([0.02, 0.04, 0.06], dtype = 'float')

            result = kabam_empty.biota_sed_acc_fact(kabam_empty.out_cb_lfish, kabam_empty.lfish_lipid)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_biomag_fact(self):
        """
        :description Biomagnification factor
        :unit (ug pesticide/kg lipid) / (ug pesticide/kg lipid)
        :expression Kabam Eq. F6
        :param out_cb_lfish: Concentration of pesticide in aquatic animal/organism (g/(kg wet weight)
        :param lfish_lipid: fraction of animal/organism that is lipid (fraction)
        :param lipid_norm_diet_conc: lipid normalized concentration of pesticide in aquatic
                                     animal/organism (g/(kg wet weight))
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.02, 0.625, 0.133333], dtype = 'float')

        try:
            #for this test we'll use the large fish variables (and values that may not specifically apply to large fish
            kabam_empty.out_cb_lfish = pd.Series([2.e-5, 2.5e-3, 2.e-4], dtype = 'float')
            kabam_empty.lfish_lipid = pd.Series([0.02, 0.04, 0.06], dtype = 'float')
            self.lipid_norm_diet_conc_lfish = pd.Series([0.05, 0.10, 0.025], dtype = 'float')

            result = kabam_empty.biomag_fact(kabam_empty.out_cb_lfish, kabam_empty.lfish_lipid,
                                                  self.lipid_norm_diet_conc_lfish)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_dry_food_ingest_rate_mammals(self):
        """
        :description dry food ingestion rate: Mammals (kg dry food/kg-bw day)
        :unit (kg dry food / kg-bw day)
        :expresssion  Kabam Eq. G1
        :param mammal_weights: body weight of mammal (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.14044886, 0.10654183, 0.07919266, 0.06187543,
                                      0.05158698, 0.04242409], dtype = 'float')

        try:
            #list of mammals (data in related arrays will reflect this order)
            kabam_empty.mammals = np.array(['fog/water shrew', 'rice rat/nosed mole', 'small mink', 'large mink',
                                     'small river otter', 'large river otter'], dtype = 'str')
            kabam_empty.mammal_weights = np.array([0.018, 0.085, 0.45, 1.8, 5., 15.], dtype = 'float')

            result = kabam_empty.dry_food_ingest_rate_mammals()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_dry_food_ingest_rate_birds(self):
        """
        :description dry food ingestion rate: Birds (kg dry food/kg-bw day)
        :unit (kg dry food / kg-bw day)
        :expresssion  Kabam Eq. G2
        :param bird_weights: body weight of bird (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.22796256, 0.02996559, 0.14722575,
                                      0.04013711, 0.05383955, 0.0288089], dtype = 'float')

        try:
            #list of mammals (data in related arrays will reflect this order)
            kabam_empty.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons',
                                               'small osprey', 'white pelican'], dtype = 'str')
            kabam_empty.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5], dtype = 'float')

            result = kabam_empty.dry_food_ingest_rate_birds()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_wet_food_ingestion_rates(self):
        """
        :description wet food ingestion rate for mammals and birds
        :unit (kg food ww / kg-bw day)
        :expresssion Kabam Eq. G3
        :param aq_animal_water_content: fraction of prey body weights that are water
        :param diet_birds: fraction of predator diet (mammal or bird) attributed to individual prey
        :param dry_food_ingestion_rate_birds: predator (mammal or bird) dry food ingestion rate (kg food dw / kg-bw day)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([[0.90702948, 0.09070295, 0.58823529, 0.19607843, 0.18518519, 0.11111111],
                                      [1.35869565, 0.12437811, 0.88888889, 0.4, 0.5, 0.2],
                                      [1.2, 0.18726592, 0.36363636, 0.5, 0.8333333, 0.6]], dtype = 'float')

        try:
            #the order of the food sources (aquatic animals/organisms) is: ['pytoplankton', 'zooplankton',
            # 'benthic_invertebrates', 'filterfeeders', 'small_fish', 'medium_fish', 'large_fish']
            kabam_empty.aq_animal_water_content = np.array([[0.90, 0.85,  0.76, 0.85, 0.73, 0.73, 0.73],
                                                        [0.95, 0.90,  0.80, 0.90, 0.75, 0.70, 0.75],
                                                        [0.95, 0.80,  0.70, 0.80, 0.75, 0.70, 0.75]], dtype = 'float')
            #for this test we will use variable names and data related to birds; each array element ([]) represents

            #an avian species and the fractions associated with its diet of 7 possible food sources
                #the order of avian species is: ['sandpipers', 'cranes', 'rails', 'herons', 'small osprey', 'white pelican']
                #the order of food sources is shown above
            kabam_empty.diet_birds = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0],
                                        [0, 0, 0.5, 0, 0.5, 0, 0], [0, 0, 0.5, 0, 0, 0.5, 0], [0, 0, 0, 0, 0, 1., 0],
                                        [0, 0, 0, 0, 0, 0, 1.]], dtype = 'float')
            kabam_empty.dry_food_ingestion_rate_birds = np.array([[0.2, 0.02, 0.15, 0.05, 0.05, 0.03],
                                                                       [0.25, 0.025, 0.20, 0.10, 0.15, 0.05],
                                                                       [0.3, 0.05, 0.10, 0.15, 0.25, 0.15]])
            for i in range(len(kabam_empty.aq_animal_water_content)):     #loop through model simulation runs

                result[i] = kabam_empty.wet_food_ingestion_rates(kabam_empty.aq_animal_water_content[i],
                                                               kabam_empty.diet_birds,
                                                               kabam_empty.dry_food_ingestion_rate_birds[i])
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_drinking_water_intake_mammals(self):
        """
        :description drinking water ingestion rate: Mammals
        :unit (L / day)
        :expresssion  Kabam Eq. G4
        :param mammal_weights: body weight of mammal (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([2.66306e-3, 0.01076743, 0.04825324, 0.16802753, 0.42141326, 1.13270633], \
                                      dtype = 'float')

        try:
            #list of mammals (data in related arrays will reflect this order)
            kabam_empty.mammals = np.array(['fog/water shrew', 'rice rat/nosed mole', 'small mink', 'large mink',
                                     'small river otter', 'large river otter'], dtype = 'str')
            kabam_empty.mammal_weights = np.array([0.018, 0.085, 0.45, 1.8, 5., 15.], dtype = 'float')

            result = kabam_empty.drinking_water_intake_mammals()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_drinking_water_intake_birds(self):
        """
        :description drinking water ingestion rate: Birds
        :unit (L / day)
        :expresssion  Kabam Eq. G5
        :param bird_weights: body weight of bird (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([4.29084e-3, 0.21101928, 9.93271e-3, 0.12040892, 0.06851438, 0.2275847], \
                                     dtype = 'float')

        try:
            #list of birds (data in related arrays will reflect this order)
            kabam_empty.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons',
                                               'small osprey', 'white pelican'], dtype = 'str')
            kabam_empty.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5], dtype = 'float')

            result = kabam_empty.drinking_water_intake_birds()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_dose_based_eec(self):
        """
        :description dose-based EECs (for mammals or birds)
        :unit (mg pesticide / kg-bw day)
        :expression Kabam Eq. G6
        :param cb_a2: overall concentration of pesticide in predator (mammal or bird) diet items (ug pesticide/kg-bw)
        :param diet_mammals: fraction of aquatic animal/organism in diet of predator
        :param wet_food_ingestion_rate_mammals: overall food ingestion rate (wet based) of predator (food ww/day)
        :param water_ingestion_rate_mammals: drinking water ingestion rate (L/day)
        :param mammal_weights: body weight of predator (kg)
        :param birds: included internally to provide context
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([
            [3.3309436e-4, 2.40677772e-5, 2.64847776e-4, 5.88650493e-5, 1.85733305e-5, 1.66970096e-5],
            [7.69043192e-4, 5.7714592e-5, 5.77791962e-4, 2.00004152e-4, 1.00005481e-4, 1.8000303e-4],
            [6.43629084e-4, 8.77034414e-5, 2.0028379e-4, 2.25083041e-4, 5.00109603e-4, 3.00060689e-4]], dtype = 'float')

        try:
            #use bird data and variables for this test
            #list of birds (data in related arrays will reflect this order)
            kabam_empty.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons', 'small osprey', \
                                               'white pelican'], dtype = 'str')
            kabam_empty.cb_a2 = np.array([[0.90, 0.09, 0.50, 0.20, 0.40, 0.10, 0.15],
                                               [1.2, 0.10, 0.80, 0.4, 0.5, 0.2, 0.9],
                                               [1.2, 0.20, 0.30, 0.5, 0.80, 0.6, 0.5]], dtype = 'float')
            kabam_empty.water_column_eec =  pd.Series([1.e-3, 1.e-4, 2.e-3], dtype = 'float')
            kabam_empty.diet_birds = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0],
                                        [0, 0, 0.5, 0, 0.5, 0, 0], [0, 0, 0.5, 0, 0, 0.5, 0],
                                        [0, 0, 0, 0, 0, 1., 0], [0, 0, 0, 0, 0, 0, 1.]], dtype = 'float')
            kabam_empty.wet_food_ingestion_rate_birds = np.array(
                                        [[0.90702948, 0.09070295, 0.58823529, 0.19607843, 0.18518519, 0.1111111],
                                         [1.35869565, 0.12437811, 0.88888888, 0.4, 0.5, 0.2],
                                         [1.2, 0.18726592, 0.36363636, 0.5, 0.8333333, 0.6]], dtype = 'float')
            kabam_empty.water_ingestion_rate_birds = np.array([4.29084e-3, 0.21101928, 9.93271e-3,
                                                                    0.12040892, 0.06851438, 0.2275847], dtype = 'float')
            kabam_empty.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5], dtype = 'float')

            for i in range(len(kabam_empty.cb_a2)):
                result[i] = kabam_empty.dose_based_eec(kabam_empty.water_column_eec[i],
                                                            kabam_empty.cb_a2[i],
                                                            kabam_empty.diet_birds,
                                                            kabam_empty.wet_food_ingestion_rate_birds[i],
                                                            kabam_empty.water_ingestion_rate_birds,
                                                            kabam_empty.bird_weights)
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_dietary_based_eec(self):
        """
        :description dietary-based EECs
        :unit (mg pesticide / kg-bw day)
        :expression Kabam Eq. G7
        :param pest_conc_diet: overall concentration of pesticide in predator (mammal or bird) diet (ug pesticide/kg-bw)
        :param diet_fraction: fraction of aquatic animal/organism in diet of predator
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([[3.67e-4, 2.65e-4, 4.5e-4, 3.e-4, 1.e-4, 1.5e-4],
                                     [5.66e-4, 4.64e-4, 6.5e-4, 5.e-4, 2.e-4, 9.e-4],
                                     [5.36e-4, 4.68e-4, 5.5e-4, 4.5e-4, 6.e-4, 5.e-4]], dtype = 'float')

        try:
            #use bird data and variables for this test
            #list of birds (data in related arrays will reflect this order)
            kabam_empty.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons', \
                                               'small osprey', 'white pelican'], dtype = 'str')
            kabam_empty.cb_a2 = np.array([[0.90, 0.09, 0.50, 0.20, 0.40, 0.10, 0.15],
                                               [1.2, 0.10, 0.80, 0.4, 0.5, 0.2, 0.9],
                                               [1.2, 0.20, 0.30, 0.5, 0.80, 0.6, 0.5]], dtype = 'float')
            kabam_empty.diet_birds = np.array([[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0],
                                        [0, 0, 0.5, 0, 0.5, 0, 0], [0, 0, 0.5, 0, 0, 0.5, 0],
                                        [0, 0, 0, 0, 0, 1., 0], [0, 0, 0, 0, 0, 0, 1.]], dtype = 'float')

            for i in range(len(kabam_empty.cb_a2)):
                result[i] = kabam_empty.dietary_based_eec(kabam_empty.cb_a2[i], kabam_empty.diet_birds)
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_acute_dose_based_tox_mammals(self):
        """
        :description Dose-based acute toxicity for mammals
        :unit (mg/kg-bw)
        :expression Kabam Eq. G8
        :param mammals: list of mammals (included here for context)
        :param mammalian_ld50: Mammalian acute oral LD50 (mg/kg-bw)
        :param species_of_the_tested_mammal: 'rat' or 'other'
        :param bw_rat: body weight of tested rat
        :param bw_other_mammal: body weight of 'other' tested mammal
        :param tested_bw: body weight of tested animal - to be sent to method (gms)
        :param mammal_weights: body weight of assessed animal (kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([[104.995065, 71.224971, 46.9552207, 33.2023550, 25.7184336, 19.5417836],
                             [136.9306393, 92.8889451, 61.23724357, 43.30127019, 33.5410196, 25.4856636],
                             [54.2796302, 36.82139815, 24.27458859, 17.1647262, 13.2957397, 10.10257752]], dtype = 'float')

        try:
            kabam_empty.mammals = np.array(['fog/water shrew', 'rice rat/nosed mole', 'small mink', 'large mink',
                                     'small river otter', 'large river otter'], dtype = 'str')
            kabam_empty.mammal_weights = np.array([0.018, 0.085, 0.45, 1.8, 5., 15.], dtype = 'float')
            kabam_empty.mammalian_ld50 = pd.Series([50., 75., 25.])
            kabam_empty.bw_rat = pd.Series([350., 200., 400.])
            kabam_empty.bw_other_mammal = pd.Series([450., 200., 400.])
            kabam_empty.species_of_the_tested_mammal = pd.Series(['rat', 'other', 'rat'], dtype = 'str')

            for i in range(len(kabam_empty.species_of_the_tested_mammal)):
                if (kabam_empty.species_of_the_tested_mammal[i] == 'rat'):
                    tested_bw = kabam_empty.bw_rat[i]
                else:
                    tested_bw = kabam_empty.bw_other_mammal[i]
                result[i] = kabam_empty.acute_dose_based_tox_mammals(kabam_empty.mammalian_ld50[i],tested_bw)
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_acute_dose_based_tox_birds(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([[36.9582003, 88.40320842, 44.598579, 77.96793198, 68.7215296, 89.91155422],
                             [49.80192597, 89.07393102, 56.44856978, 81.91867866, 75.30679072, 90.08433255],
                             [11.82177011, 50.57591068, 16.1696091, 41.02272544, 33.23934936, 52.02239313]], dtype = 'float')

        try:
            #use rat body weight for this test

            kabam_empty.birds = np.array(['sandpipers', 'cranes', 'rails', 'herons', \
                                               'small osprey', 'white pelican'], dtype = 'str')
            kabam_empty.bird_weights = np.array([0.02, 6.7, 0.07, 2.9, 1.25, 7.5], dtype = 'float')
            kabam_empty.avian_ld50 = pd.Series([50., 75., 25.])
            kabam_empty.bw_quail = pd.Series([150., 200., 100.])
            kabam_empty.bw_duck = pd.Series([1350., 1200., 1400.])
            kabam_empty.bw_other_bird = pd.Series([450., 200., 400.])
            kabam_empty.species_of_the_tested_bird = pd.Series(['quail', 'duck', 'other'], dtype = 'str')
            kabam_empty.mineau_scaling_factor = pd.Series([1.15, 1.10, 1.25], dtype = 'float')

            for i in range(len(kabam_empty.species_of_the_tested_bird)):
                if (kabam_empty.species_of_the_tested_bird[i] == 'quail'):
                    tested_bw = kabam_empty.bw_quail[i]
                elif  (kabam_empty.species_of_the_tested_bird[i] == 'duck'):
                    tested_bw = kabam_empty.bw_duck[i]
                else:
                    tested_bw = kabam_empty.bw_other_bird[i]
                result[i] = kabam_empty.acute_dose_based_tox_birds(kabam_empty.avian_ld50[i], tested_bw,
                                                                        kabam_empty.mineau_scaling_factor[i])
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def tested_chronic_dose_based_tox_mammals(self):
        """
        :description Dose=based chronic toxicity for mammals
        :unit (mg/kg-bw)
        :param mammalian_chronic_endpt: ppm
        :param tested_mammal_bw: body weight of tested mammal (gms)
        :param mammal_weights: body weight of assessed mammal(kg)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([[1.04995066, 0.71224971, 0.469552207, 0.33202355, 0.25718434, 0.19541784],
                             [45.64354646, 30.9629817, 20.41241452, 14.43375673, 11.18033989, 8.49522122],
                             [5.42796302, 3.68213981, 2.42745886, 1.71647262, 1.32957397, 1.01025775]], dtype = 'float')

        try:
            kabam_empty.mammals = np.array(['fog/water shrew', 'rice rat/nosed mole', 'small mink', 'large mink',
                                     'small river otter', 'large river otter'], dtype = 'str')
            kabam_empty.mammal_weights = np.array([0.018, 0.085, 0.45, 1.8, 5., 15.], dtype = 'float')
            kabam_empty.bw_rat = pd.Series([350., 200., 400.])
            kabam_empty.bw_other_mammal = pd.Series([450., 200., 400.])
            kabam_empty.species_of_the_tested_mammal = pd.Series(['rat', 'other', 'rat'], dtype = 'str')
            kabam_empty.mammalian_chronic_endpoint = pd.Series([10., 25., 50.])
            kabam_empty.mammalian_chronic_endpoint_unit = pd.Series(['ppm', 'mg/kg-bw', 'ppm'], dtype = 'str')

            for i in range(len(kabam_empty.species_of_the_tested_mammal)):
                if (kabam_empty.species_of_the_tested_mammal[i] == 'rat'):
                    tested_bw = kabam_empty.bw_rat[i]
                else:
                    tested_bw = kabam_empty.bw_other_mammal[i]
                result[i] = kabam_empty.chronic_dose_based_tox_mammals(
                    kabam_empty.mammalian_chronic_endpoint[i],
                    kabam_empty.mammalian_chronic_endpoint_unit[i], tested_bw)
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_acute_rq_dose_mammals(self):
        """
        :description Dose-based risk quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet)
         :param dose_based_eec_mammals
         :param acute_dose_based_tox_mammals
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]], dtype = 'float')

        try:
            kabam_empty.dose_based_eec_mammals = np.array([
                [1., 2., 3., 4., 5., 6.],
                [7., 8., 9., 10., 11., 12.],
                [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.dose_based_tox_mammals = np.array([
                             [2., 4., 6., 8., 10., 12.],
                             [14., 16., 18., 20., 22., 24.],
                             [26., 28., 30., 32., 34., 36.]], dtype = 'float')

            result = kabam_empty.acute_rq_dose_mammals()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_chronic_rq_dose_mammals(self):
        """
        :description Chronic dose-based risk quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet)
        :param dose_based_eec_mammals: self defined
        :param chronic_dose_based_tox_mammals: self defined
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                    [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]], dtype = 'float')

        try:
            kabam_empty.dose_based_eec_mammals = np.array([
                [1., 2., 3., 4., 5., 6.],
                [7., 8., 9., 10., 11., 12.],
                [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.chronic_dose_based_tox_mamm = np.array([
                             [2., 4., 6., 8., 10., 12.],
                             [14., 16., 18., 20., 22., 24.],
                             [26., 28., 30., 32., 34., 36.]], dtype = 'float')

            result = kabam_empty.chronic_rq_dose_mammals()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_acute_rq_diet_mammals(self):
        """
        :description Acute diet-based for risk quotient mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param mammalian_lc50; (mg/kg-diet)
        :param diet_based_eec_mammals: (mg pesticide / kg-bw day)
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                                    [1.3, 1.4, 1.5, 1.6, 1.7, 1.8]], dtype = 'float')

        try:
            kabam_empty.diet_based_eec_mammals = np.array([ [1., 2., 3., 4., 5., 6.],
                        [7., 8., 9., 10., 11., 12.], [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.mammalian_lc50 = np.array([10., 'nan', 10.], dtype = 'float')

            for i in range(len(kabam_empty.mammalian_lc50)):
                result[i] = kabam_empty.acute_rq_diet_mammals(kabam_empty.diet_based_eec_mammals[i],
                                                                   kabam_empty.mammalian_lc50[i])
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_chronic_rq_diet_mammals(self):
        """
        :description chronic diet-based  rist quotient for mammals
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param mammalian_chronic_endpt:  (ppm)
        :param diet_based_eec: diet-based eec for mammal (mg pesticide / kg
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                                    [0.065, 0.07, 0.075, 0.08, 0.085, 0.09]], dtype = 'float')

        try:
            kabam_empty.diet_based_eec_mammals = np.array([ [1., 2., 3., 4., 5., 6.],
                        [7., 8., 9., 10., 11., 12.], [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.mammalian_chronic_endpoint = np.array([10., 'nan', 10.], dtype = 'float')
            kabam_empty.mammalian_chronic_endpoint_unit = np.array(['ppm', 'mg/kg-bw', 'mg/kg-bw'], dtype = 'str')

            for i in range(len(kabam_empty.mammalian_chronic_endpoint)):
                result[i] = kabam_empty.chronic_rq_diet_mammals(kabam_empty.diet_based_eec_mammals[i],
                                                                   kabam_empty.mammalian_chronic_endpoint[i],
                                                                   kabam_empty.mammalian_chronic_endpoint_unit[i])
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_acute_rq_dose_birds(self):
        """
        :description Dose-based risk quotient for birds
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
         :param dose_based_eec_birds: self defined
         :param acute_dose_based_tox_birds: self defined
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.5, 0.5, 0.5, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
                                     [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]], dtype = 'float')

        try:
            kabam_empty.dose_based_eec_birds = np.array([[1., 2., 3., 4., 5., 6.],
                                 [7., 8., 9., 10., 11., 12.], [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.dose_based_tox_birds = np.array([  [2., 4., 6., 8., 10., 12.],
                                 [14., 16., 18., 20., 22., 24.], [26., 28., 30., 32., 34., 36.]], dtype = 'float')

            result = kabam_empty.acute_rq_dose_birds()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return
    
    def test_acute_rq_diet_birds(self):
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

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                                    [1.3, 1.4, 1.5, 1.6, 1.7, 1.8]], dtype = 'float')

        try:
            kabam_empty.diet_based_eec_birds = np.array([ [1., 2., 3., 4., 5., 6.],
                        [7., 8., 9., 10., 11., 12.], [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.avian_lc50 = np.array([10., 'nan', 10.], dtype = 'float')

            for i in range(len(kabam_empty.avian_lc50)):
                result[i] = kabam_empty.acute_rq_diet_birds(kabam_empty.diet_based_eec_birds[i],
                                                                   kabam_empty.avian_lc50[i])
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_chronic_rq_diet_birds(self):
        """
        :description chronic diet-based  rist quotient for birds
        :unit none
        :expression no known documentation; see EPA OPP Kabam spreadsheet
        :param avian_chronic_endpt:  avian noaec (mg/kg-diet)
        :param diet_based_eec: diet-based eec for mammal (mg pesticide / kg
        :return:
        """

        # create empty pandas dataframes to create empty object for this unittest
        kabam_empty = self.create_kabam_object()

        result = pd.Series([], dtype='float')
        expected_results = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                    ['nan', 'nan', 'nan', 'nan', 'nan', 'nan'],
                                    [1.3, 1.4, 1.5, 1.6, 1.7, 1.8]], dtype = 'float')

        try:
            kabam_empty.diet_based_eec_birds = np.array([ [1., 2., 3., 4., 5., 6.],
                        [7., 8., 9., 10., 11., 12.], [13., 14., 15., 16., 17., 18.]], dtype = 'float')
            kabam_empty.avian_noaec = np.array([10., 'nan', 10.], dtype = 'float')

            for i in range(len(kabam_empty.avian_noaec)):
                result[i] = kabam_empty.chronic_rq_diet_birds(kabam_empty.diet_based_eec_birds[i],
                                                                   kabam_empty.avian_noaec[i])
                npt.assert_allclose(result[i], expected_results[i], rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

if __name__ == '__main__':
    unittest.main()
    #pass