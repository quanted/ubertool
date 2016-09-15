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
    """
    print("kabam unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for trex unit tests.
        :return:
        """

        self.kabam_empty = object
        # create empty pandas dataframes to create empty object for testing
        df_empty = pd.DataFrame()
        # create an empty kabam object
        self.kabam_empty = Kabam(df_empty, df_empty)

        pass
        # setup the test as needed
        # e.g. pandas to open trex qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for trex unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file


    def test_ventilation_rate(self):
        """
        unittest for method ventilation_rate;
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 0.00394574, 0.468885], dtype = 'float')

        try:
            self.kabam_empty.zoo_wb = pd.Series(['nan', 1.e-07, 1.e-4], dtype = 'float')
            self.kabam_empty.conc_do = pd.Series([5.0, 10.0, 7.5], dtype='float')

            result = self.kabam_empty.ventilation_rate(self.kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_pest_uptake_eff_gills(self):
        """
        Pesticide uptake efficiency by gills
        unit: fraction
        Kabam Eq. A5.2a (Ew)
        :param log kow: octanol-water partition coefficient ()
        :return:
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 0.540088, 0.540495], dtype = 'float')

        try:
            self.kabam_empty.log_kow = pd.Series(['nan', 5., 6.], dtype = 'float')
            self.kabam_empty.kow = 10.**(self.kabam_empty.log_kow)

            result = self.kabam_empty.pest_uptake_eff_bygills()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_phytoplankton_k1_calc(self):
        """
        Uptake rate constant through respiratory area for phytoplankton
        unit: L/kg*d
        Kabam Eq. A5.1  (K1:unique to phytoplankton)
        :param log kow: octanol-water partition coefficient ()

        :return:
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([1639.34426, 8695.6521, 15267.1755], dtype = 'float')

        try:

            self.kabam_empty.log_kow = pd.Series([4., 5., 6.], dtype = 'float')
            self.kabam_empty.kow = 10.**(self.kabam_empty.log_kow)
            result = self.kabam_empty.phytoplankton_k1_calc()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_aq_animal_k1_calc(self):
        """
        Uptake rate constant through respiratory area for aquatic animals
        unit: L/kg*d
        Kabam Eq. A5.2 (K1)
        :param pest_uptake_eff_bygills: Pesticide uptake efficiency by gills of aquatic animals (fraction)
        :param vent_rate: Ventilation rate of aquatic animal (L/d)
        :param wet_wgt: wet weight of animal (kg)

        :return:
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 1201.13849, 169.37439], dtype = 'float')

        try:
            pest_uptake_eff_bygills = pd.Series(['nan', 0.0304414, 0.0361228], dtype = 'float')
            vent_rate = pd.Series(['nan', 0.00394574, 0.468885], dtype = 'float')
            wet_wgt = pd.Series(['nan', 1.e-07, 1.e-4], dtype = 'float')

            result = self.kabam_empty.aq_animal_k1_calc(pest_uptake_eff_bygills, vent_rate, wet_wgt)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_animal_water_part_coef(self):
        """
        Organism-Water partition coefficient (based on organism wet weight)
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

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([650.87, 11000.76, 165000.64], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            self.kabam_empty.zoo_lipid_frac = pd.Series([0.03, 0.04, 0.06], dtype = 'float')
            self.kabam_empty.zoo_nlom_frac = pd.Series([0.10, 0.20, 0.30,], dtype = 'float')
            self.kabam_empty.zoo_water_frac = pd.Series([0.87, 0.76, 0.64], dtype = 'float')
            self.kabam_empty.kow = pd.Series([1.e4, 1.e5, 1.e6], dtype = 'float')
            beta = 0.35

            result = self.kabam_empty.animal_water_part_coef(self.kabam_empty.zoo_lipid_frac,
                                            self.kabam_empty.zoo_nlom_frac,
                                            self.kabam_empty.zoo_water_frac, beta)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return


    def test_aq_animal_k2_calc(self):
        """
        Elimination rate constant through the respiratory area
        :unit (per day)
        :expression Kabam Eq. A6 (K2)
        :param zoo_k1: Uptake rate constant through respiratory area for aquatic animals
        :param k_bw_zoo (Kbw): Organism-Water partition coefficient (based on organism wet weight ()
        :return:
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([2.5186969, 0.79045921, 0.09252798], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            self.kabam_empty.zoo_k1 = pd.Series([1639.34426, 8695.6521, 15267.1755], dtype = 'float')
            self.kabam_empty.k_bw_zoo = pd.Series([650.87, 11000.76, 165000.64], dtype = 'float')

            result = self.kabam_empty.aq_animal_k2_calc(self.kabam_empty.zoo_k1, self.kabam_empty.k_bw_zoo)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_animal_grow_rate_const(self):
        """
        Aquatic animal/organism growth rate constant
        :unit (per day)
        :expression Kabam Eq. A7.1 & A7.2
        :param zoo_wb: wet weight of animal/organism (kg)
        :param water_temp: water temperature (degrees C)
        :return:
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.01255943, 0.00125594, 0.00251], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            self.kabam_empty.zoo_wb = pd.Series([1.e-7, 1.e-2, 1.0], dtype = 'float')
            self.kabam_empty.water_temp = pd.Series([10., 15., 20.], dtype = 'float')

            result = self.kabam_empty.animal_grow_rate_const(self.kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_dietary_trans_eff(self):
        """
        Aquatic animal/organizm dietary pesticide transfer efficiency
        :unit fraction
        :expression Kabam Eq. A8a (Ed)
        :param kow: octanol-water partition coefficient ()
        :return:
        """
        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.499251, 0.492611, 0.434783], dtype = 'float')

        try:
            self.kabam_empty.kow = pd.Series([1.e4, 1.e5, 1.e6], dtype = 'float')

            result = self.kabam_empty.dietary_trans_eff()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_aq_animal_feeding_rate(self):
        """
        Aquatic animal feeding rate (except filterfeeders)
        :unit kg/d
        :expression Kabam Eq. A8b1 (Gd)
        :param wet_wgt: wet weight of animal/organism (kg)
        :return:
        """
        result = pd.Series([], dtype='float')
        expected_results = pd.Series([4.497792e-08, 1.0796617e-3, 0.073042572], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            self.kabam_empty.zoo_wb = pd.Series([1.e-7, 1.e-2, 1.], dtype = 'float')
            self.kabam_empty.water_temp = pd.Series([10., 15., 20.])

            result = self.kabam_empty.aq_animal_feeding_rate(self.kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_filterfeeder_feeding_rate(self):
        """
        Filter feeder feeding rate
        :unit kg/d
        :expression Kabam Eq. A8b2 (Gd)
        :param self.gv_filterfeeders: filterfeeder ventilation rate (L/d)
        :param self.conc_ss: Concentration of Suspended Solids (Css - kg/L)
        :param particle_scav_eff: efficiency of scavenging of particles absorbed from water (fraction)
        :return:
        """
        result = pd.Series([], dtype='float')
        expected_results = pd.Series(['nan', 1.97287e-7, 0.03282195], dtype = 'float')

        try:
            self.kabam_empty.gv_filterfeeders = pd.Series(['nan', 0.00394574, 0.468885], dtype = 'float')
            self.kabam_empty.conc_ss = pd.Series([0.00005, 0.00005, 0.07], dtype = 'float')
            self.kabam_empty.particle_scav_eff = 1.0

            result = self.kabam_empty.filterfeeders_feeding_rate()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_diet_uptake_rate_const(self):
        """
        pesticide uptake rate constant for uptake through ingestion of food rate
        :unit kg food/kg organism - day
        :expression Kabam Eq. A8 (kD)
        :param dietary_trans_eff: dietary pesticide transfer efficiency (fraction)
        :param feeding rate: animal/organism feeding rate (kg/d)
        :param wet weight of aquatic animal/organism (kg)
        :return:
        """

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.22455272, 0.05318532, 0.031755767 ], dtype = 'float')

        try:
            #For test purpose we'll use the zooplankton variable names
            self.kabam_empty.ed_zoo = pd.Series([0.499251, 0.492611, 0.434783], dtype = 'float')
            self.kabam_empty.gd_zoo = pd.Series([4.497792e-08, 1.0796617e-3, 0.073042572], dtype = 'float')
            self.kabam_empty.zoo_wb = pd.Series([1.e-7, 1.e-2, 1.0])

            result = self.kabam_empty.diet_uptake_rate_const(self.kabam_empty.ed_zoo,    \
                     self.kabam_empty.gd_zoo, self.kabam_empty.zoo_wb)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return
        dietary_uptake_constantt = pd.Series([], dtype = 'float')

        dietary_uptake_constant = dietary_trans_eff * feeding_rate / wet_wgt
        return dietary_uptake_constant

    def test_overall_diet_content(self):
        """
        Overall fraction of aquatic animal/organism diet attibuted to diet food component (i.e., lipids or NLOM or water)
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

        result = pd.Series([], dtype='float')
        expected_results = pd.Series([0.025, 0.03355, 0.0465], dtype = 'float')

        try:
            #For test purpose we'll use the small fish diet variables
            self.kabam_empty.sfish_diet_sediment = pd.Series([0.0, 0.01, 0.05], dtype = 'float')
            self.kabam_empty.sfish_diet_phytoplankton = pd.Series([0.0, 0.01, 0.05], dtype = 'float')
            self.kabam_empty.sfish_diet_zooplankton = pd.Series([0.5, 0.4, 0.5], dtype = 'float')
            self.kabam_empty.sfish_diet_benthic_invertebrates = pd.Series([0.5, 0.57, 0.35], dtype = 'float')
            self.kabam_empty.sfish_diet_filterfeeders = pd.Series([0.0, 0.01, 0.05], dtype = 'float')

            self.kabam_empty.sediment_lipid = pd.Series([0.0, 0.01, 0.0], dtype = 'float')
            self.kabam_empty.phytoplankton_lipid = pd.Series([0.02, 0.015, 0.03], dtype = 'float')
            self.kabam_empty.zoo_lipid = pd.Series([0.03, 0.04, 0.05], dtype = 'float')
            self.kabam_empty.beninv_lipid = pd.Series([0.02, 0.03, 0.05], dtype = 'float')
            self.kabam_empty.filterfeeders_lipid = pd.Series([0.01, 0.02, 0.05], dtype = 'float')

            diet_elements = pd.Series([], dtype = 'float')
            content_fracs = pd.Series([], dtype = 'float')

            for i in range(len(self.kabam_empty.sfish_diet_sediment)):
                diet_elements = [self.kabam_empty.sfish_diet_sediment[i],
                                 self.kabam_empty.sfish_diet_phytoplankton[i],
                                 self.kabam_empty.sfish_diet_zooplankton[i],
                                 self.kabam_empty.sfish_diet_benthic_invertebrates[i],
                                 self.kabam_empty.sfish_diet_filterfeeders[i]]

                content_fracs = [self.kabam_empty.sediment_lipid[i],
                                 self.kabam_empty.phytoplankton_lipid[i],
                                 self.kabam_empty.zoo_lipid[i],
                                 self.kabam_empty.beninv_lipid[i],
                                 self.kabam_empty.filterfeeders_lipid[i]]

                result[i] = self.kabam_empty.overall_diet_content(diet_elements, content_fracs)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return



# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass