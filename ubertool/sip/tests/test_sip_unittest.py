import datetime
import inspect
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
from tabulate import tabulate
import unittest

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from sip_exe import Sip

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
sip_empty = Sip(df_empty, df_empty)

test = {}


class TestSip(unittest.TestCase):
    """
    Unit tests for Sip.
    """
    print("sip unittests conducted at " + str(datetime.datetime.today()))

    def setUp(self):
        """
        Setup routine for sip unittest.
        :return:
        """
        pass
        # sip2 = sip_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for sip unittest.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    def test_sip_unit_fw_bird(self):
        """
        unittest for function sip.fw_bird:
        :return:
        """
        expected_results = [0.0162, 0.0162, 0.0162]
        result = [0.,0.,0.]
        try:
            for i in range(0,3):
                result[i] = sip_empty.fw_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_fw_mamm(self):
        """
        unittest for function sip.fw_mamm:
        :return:
        """
        expected_results = [0.172, 0.172, 0.172]
        result = [0.,0.,0.]
        try:
            for i in range(0,3):
                result[i] = sip_empty.fw_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_dose_bird(self):
        """
        unittest for function sip.dose_bird:
        :return:
        """
        expected_results = [1000000., 4805.50175, 849727.21122]
        try:
            #(self.out_fw_bird * self.solubility)/(self.bodyweight_assessed_bird / 1000.)
            sip_empty.out_fw_bird = pd.Series([10., 0.329, 1.8349], dtype='float')
            sip_empty.solubility = pd.Series([100., 34.9823, 453.83], dtype='float')
            sip_empty.bodyweight_assessed_bird = pd.Series([1.0, 2.395, 0.98], dtype='float')
            result = sip_empty.dose_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_dose_mamm(self):
        """
        unittest for function sip.dose_mamm:
        :return:
        """
        expected_results = [8000000., 48205.7595, 3808036.37889]
        try:
            #(self.out_fw_mamm * self.solubility)/(self.bodyweight_assessed_mammal / 1000)
            sip_empty.out_fw_mamm = pd.Series([20., 12.843, 6.998], dtype='float')
            sip_empty.solubility = pd.Series([400., 34.9823, 453.83], dtype='float')
            sip_empty.bodyweight_assessed_mammal = pd.Series([1., 9.32, 0.834], dtype='float')
            result = sip_empty.dose_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_at_bird(self):
        """
        unittest for function sip.at_bird:
        :return:
        """
        expected_results = [1000., 687.9231, 109.3361]
        try:
            #(self.ld50_avian_water) * ((self.bodyweight_assessed_bird / self.bodyweight_tested_bird)**(self.mineau_scaling_factor - 1.))
            sip_empty.ld50_avian_water = pd.Series([2000., 938.34, 345.83], dtype='float')
            sip_empty.bodyweight_assessed_bird = pd.Series([100., 39.49, 183.54], dtype='float')
            sip_empty.bodyweight_tested_bird = pd.Series([200., 73.473, 395.485], dtype='float')
            sip_empty.mineau_scaling_factor = pd.Series([2., 1.5, 2.5], dtype='float')
            result = sip_empty.at_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_at_mamm(self):
        """
        unittest for function sip.at_mamm:
        :return:
        """
        expected_results = [11.89207, 214.0572, 412.6864]
        try:
            #(self.ld50_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
            sip_empty.ld50_mammal_water = pd.Series([10., 250., 500.], dtype='float')
            sip_empty.bodyweight_tested_mammal = pd.Series([200., 39.49, 183.54], dtype='float')
            sip_empty.bodyweight_assessed_mammal = pd.Series([100., 73.473, 395.485], dtype='float')
            result = sip_empty.at_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_fi_bird(self):
        """
        unittest for function sip.fi_bird:
        :return:
        """
        expected_results = [0.012999, 0.03407565, 0.025681]
        try:
            #0.0582 * ((bw_grams / 1000.)**0.651)
            sip_empty.bw_grams = pd.Series([100., 439.43, 284.59], dtype='float')
            result = sip_empty.fi_bird(sip_empty.bw_grams)
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_act(self):
        """
        unittest for function sip.test_act:
        :return:
        """
        expected_results = [10.5737, 124.8032, 416.4873]
        try:
            #(self.noael_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
            sip_empty.noael_mammal_water = pd.Series([10., 120., 400.], dtype='float')
            sip_empty.bodyweight_tested_mammal = pd.Series([500., 385.45, 673.854], dtype='float')
            sip_empty.bodyweight_assessed_mammal = pd.Series([400., 329.45, 573.322], dtype='float')
            result = sip_empty.act()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_det(self):
        """
        unittest for function sip.det
        return:
        """
    #
    #     '''
    #     Dose Equiv. Toxicity:
    #
    #     The FI value (kg-diet) is multiplied by the reported NOAEC (mg/kg-diet) and then divided by
    #     the test animal's body weight to derive the dose-equivalent chronic toxicity value (mg/kg-bw):
    #
    #     Dose Equiv. Toxicity = (NOAEC * FI) / BW
    #
    #     NOTE: The user enters the lowest available NOAEC for the mallard duck, for the bobwhite quail,
    #     and for any other test species. The model calculates the dose equivalent toxicity values for
    #     all of the modeled values (Cells F20-24 and results worksheet) and then selects the lowest dose
    #     equivalent toxicity value to represent the chronic toxicity of the chemical to birds.
    #     '''
    #     try:
    #         # result =
    #         # self.assertEquals(result, )
    #         pass
    #     finally:
    #         pass
    #    return
    #
    #
    # def test_det_duck(self):
    #     """
    #     unittest for function sip.det_duck:
    #     :return:
    #     """
    #     try:
    #         # det_duck = (self.noaec_duck * self.fi_bird(1580.)) / (1580. / 1000.)
    #         sip_empty.noaec_duck = pd.Series([1.], dtype='int')
    #         sip_empty.fi_bird = pd.Series([1.], dtype='int')
    #         result = sip_empty.det_duck()
    #         npt.assert_array_almost_equal(result, 1000., 4, '', True)
    #     finally:
    #         pass
    #     return
    #
    # def test_det_quail(self):
    #     """
    #     unittest for function sip.det_quail:
    #     :return:
    #     """
    #     try:
    #         # det_quail = (self.noaec_quail * self.fi_bird(178.)) / (178. / 1000.)
    #         sip_empty.noaec_quail = pd.Series([1.], dtype='int')
    #         sip_empty.fi_bird = pd.Series([1.], dtype='int')
    #         result = sip_empty.det_quail()
    #         npt.assert_array_almost_equal(result, 1000., 4, '', True)
    #     finally:
    #         pass
    #     return
    #
    # def test_det_other_1(self):
    #     """
    #     unittest for function sip.det_other_1:
    #     :return:
    #     """
    #     try:
    #         #det_other_1 = (self.noaec_bird_other_1 * self.fi_bird(self.bodyweight_bird_other_1)) / (self.bodyweight_bird_other_1 / 1000.)
    #         #det_other_2 = (self.noaec_bird_other_2 * self.fi_bird(self.bodyweight_bird_other_1)) / (self.bodyweight_bird_other_1 / 1000.)
    #         sip_empty.noaec_bird_other_1 = pd.Series([400.]) # mg/kg-diet
    #         sip_empty.bodyweight_bird_other_1 = pd.Series([100]) # grams
    #         result = sip_empty.det_other_1()
    #         npt.assert_array_almost_equal(result, 4666, 4)
    #     finally:
    #         pass
    #     return
    #
    #   The following tests are configured such that:
        #   1. four values are provided for each needed input
        #   2. the four input values generate four values of out_det_* per bird type
        #   3. the inputs per bird type are set so that calculations of out_det_* will result in
        #      each bird type having one minimum among the bird types;
        #      thus all four calculations result in one minimum per bird type

        expected_results = [4.2174, 4.96125, 7.97237, 10.664648]
        try:
            sip_empty.noaec_quail = pd.Series([100., 300., 75., 150.], dtype='float')
            sip_empty.noaec_duck = pd.Series([400., 100., 200., 350.], dtype='float')
            sip_empty.noaec_bird_other_1 = pd.Series([50., 200., 300., 250.], dtype='float')
            sip_empty.noaec_bird_other_2 = pd.Series([350., 400., 250., 100.], dtype='float')
            sip_empty.bodyweight_bird_other_1 = pd.Series([345.34, 453.54, 649.29, 294.56], dtype='float')
            sip_empty.bodyweight_bird_other_2 = pd.Series([123.84, 85.743, 127.884, 176.34], dtype='float')
            result = sip_empty.det()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_acute_bird(self):
        """
        unittest for function sip.acute_bird:
        :return:
        """
        expected_results = [10., 5.22093, 0.479639]
        try:
            # self.out_acute_bird = self.out_dose_bird / self.out_at_bird
            sip_empty.out_dose_bird = pd.Series([100., 121.23, 43.994], dtype='float')
            sip_empty.out_at_bird = pd.Series([10., 23.22, 91.723], dtype='float')
            result = sip_empty.acute_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_acuconb(self):
        """
        unittest for function sip.acuconb:
        Message stating whether or not a risk is present
        :return:
        """
        # if self.out_acuconb == -1:
        #     if self.out_acute_bird == None:
        #         raise ValueError\
        #         ('acute_bird variable equals None and therefor this function cannot be run.')
        # if self.out_acute_bird < 0.1:
        #     self.out_acuconb = ('Drinking water exposure alone is NOT a potential concern for birds')
        # else:
        #     self.out_acuconb = ('Exposure through drinking water alone is a potential concern for birds')
        expected_results = pd.Series(["Exposure through drinking water alone is a potential concern "
                            "for birds", "Drinking water exposure alone is NOT a potential "
                            "concern for birds", "Exposure through drinking water alone is a "
                            "potential concern for birds"])
        try:
            sip_empty.out_acute_bird = pd.Series([0.2, 0.09, 0.1], dtype='float')
            result = sip_empty.acuconb()
            pdt.assert_series_equal(result, expected_results,  True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_acute_mamm(self):
        """
        unittest for function sip.acute_mamm:
        :return:
        """
        # self.out_acute_mamm = self.out_dose_mamm / self.out_at_mamm
        expected_results = [10., 14.68657, 2.124852]
        try:
            sip_empty.out_dose_mamm = pd.Series([100., 34.44, 159.349], dtype='float')
            sip_empty.out_at_mamm = pd.Series([10., 2.345, 74.993], dtype='float')
            result = sip_empty.acute_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_acuconm(self):
        """
        unittest for function sip.acuconm:
        Message stating whether or not a risk is present
        :return:
        """
        # if self.out_acuconm == -1:
        #     if self.out_acute_mamm == None:
        #         raise ValueError\
        #         ('acute_mamm variable equals None and therefor this function cannot be run.')
        #     if self.out_acute_mamm < 0.1:
        #         self.out_acuconm = ('Drinking water exposure alone is NOT a potential concern for mammals')
        #     else:
        #         self.out_acuconm = ('Exposure through drinking water alone is a potential concern for mammals')
        #     return self.out_acuconm
        expected_results = pd.Series(["Drinking water exposure alone is NOT a potential concern "
                                      "for mammals", "Exposure through drinking water alone is a "
                                      "potential concern for mammals", "Drinking water exposure "
                                      "alone is NOT a potential concern for mammals"])
        try:
            sip_empty.out_acute_mamm = pd.Series([0.09, 0.2, 0.002])
            result = sip_empty.acuconm()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_chron_bird(self):
        """
        unittest for function sip.chron_bird:
        :return:
        """
        #self.out_chron_bird = self.out_dose_bird / self.out_det
        expected_results = [0.5, 0.10891, 2.39857]
        try:
            sip_empty.out_dose_bird = pd.Series([5., 1.32, 19.191], dtype='float')
            sip_empty.out_det = pd.Series([10., 12.12, 8.001], dtype='float')
            result = sip_empty.chron_bird()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_chronconb(self):
        """
        unittest for function sip.chronconb:
        :return:
        """
        expected_results = pd.Series(["Drinking water exposure alone is NOT "
                                      "a potential concern for birds", "Exposure through "
                                      "drinking water alone is a potential concern for "
                                      "birds", "Drinking water exposure alone is NOT a "
                                      "potential concern for birds"])
        try:
            sip_empty.out_chron_bird = pd.Series([0.12, 3., 0.97], dtype='float')
            result = sip_empty.chronconb()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_chron_mamm(self):
        """
        unittest for function sip.chron_mamm:
        :return:
        """
        # self.out_chron_mamm = self.out_dose_mamm / self.out_act
        expected_results = [2.0, 14.1333, 244.7245]
        try:
            sip_empty.out_dose_mamm = pd.Series([8., 34.344, 23.983], dtype='float')
            sip_empty.out_act = pd.Series([4., 2.43, 0.098], dtype='float')
            result = sip_empty.chron_mamm()
            npt.assert_allclose(result, expected_results, rtol=1e-4, atol=0, err_msg='', verbose=True )
        finally:
            tab = [result, expected_results]
            print("\n")
            print(inspect.currentframe().f_code.co_name)
            print(tabulate(tab, headers='keys', tablefmt='rst'))
        return

    def test_sip_unit_chronconm(self):
        """
        unittest for function sip.chronconm:
        :return:
        """
        expected_results = pd.Series(["Drinking water exposure alone is NOT a potential "
                            "concern for mammals", "Exposure through drinking water alone "
                            "is a potential concern for mammals", "Drinking water exposure "
                            "alone is NOT a potential concern for mammals"])
        try:
            sip_empty.out_chron_mamm = pd.Series([0.5, 1.0, 0.09], dtype='float')
            result = sip_empty.chronconm()
            pdt.assert_series_equal(result, expected_results, True)
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
