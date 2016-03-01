import logging
import numpy.testing as npt
import os.path
import pandas as pd
import pandas.util.testing as pdt
import sys
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

    def test_unit_fw_bird(self):
        """
        unittest for function sip.fw_bird:
        :return:
        """
        try:
            result = sip_empty.fw_bird()
            npt.assert_array_almost_equal(result, 0.0162, 4, '', True)
        finally:
            pass
        return

    def test_unit_fw_mamm(self):
        """
        unittest for function sip.fw_mamm:
        :return:
        """
        try:
            result = sip_empty.fw_mamm()
            npt.assert_array_almost_equal(result, 0.172, 4, '', True)
        finally:
            pass
        return

    def test_unit_dose_bird(self):
        """
        unittest for function sip.dose_bird:
        :return:
        """
        try:
            #(self.out_fw_bird * self.solubility)/(self.bodyweight_assessed_bird / 1000.)
            sip_empty.out_fw_bird = pd.Series([10.], dtype='int')
            sip_empty.solubility = pd.Series([100.], dtype='int')
            sip_empty.bodyweight_assessed_bird = pd.Series([1.], dtype='int')
            result = sip_empty.dose_bird()
            npt.assert_array_almost_equal(result, 1000000., 4, '', True)
        finally:
            pass
        return

    def test_unit_dose_mamm(self):
        """
        unittest for function sip.dose_mamm:
        :return:
        """
        try:
            #(self.out_fw_mamm * self.solubility)/(self.bodyweight_assessed_mammal / 1000)
            sip_empty.out_fw_mamm = pd.Series([20.], dtype='int')
            sip_empty.solubility = pd.Series([400.], dtype='int')
            sip_empty.bodyweight_assessed_mammal = pd.Series([1.], dtype='int')
            result = sip_empty.dose_mamm()
            npt.assert_array_almost_equal(result, 8000000., 4, '', True)
        finally:
            pass
        return

    def test_unit_at_bird(self):
        """
        unittest for function sip.at_bird:
        :return:
        """
        try:
            #(self.ld50_avian_water) * ((self.bodyweight_assessed_bird / self.bodyweight_tested_bird)**(self.mineau_scaling_factor - 1.))
            sip_empty.ld50_avian_water = pd.Series([2000.], dtype='int')
            sip_empty.bodyweight_assessed_bird = pd.Series([100.], dtype='int')
            sip_empty.bodyweight_tested_bird = pd.Series([200.], dtype='int')
            sip_empty.mineau_scaling_factor = pd.Series([2.], dtype='int')
            result = sip_empty.at_bird()
            npt.assert_array_almost_equal(result, 1000., 4, '', True)
        finally:
            pass
        return

    def test_unit_at_mamm(self):
        """
        unittest for function sip.at_mamm:
        :return:
        """
        try:
            #(self.ld50_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
            sip_empty.ld50_mammal_water = pd.Series([10.], dtype='int')
            sip_empty.bodyweight_tested_mammal = pd.Series([100.], dtype='int')
            sip_empty.bodyweight_assessed_mammal = pd.Series([200.], dtype='int')
            result = sip_empty.at_mamm()
            npt.assert_array_almost_equal(result, 8.408964, 4, '', True)
        finally:
            pass
        return

    def test_unit_fi_bird(self):
        """
        unittest for function sip.fi_bird:
        :return:
        """
        try:
            #0.0582 * ((bw_grams / 1000.)**0.651)
            sip_empty.bw_grams = pd.Series([100.], dtype='int')
            print(sip_empty.bw_grams)
            result = sip_empty.fi_bird(sip_empty.bw_grams)
            npt.assert_array_almost_equal(result, 0.012999, 4, '', True)
        finally:
            pass
        return

    def test_unit_act(self):
        """
        unittest for function sip.test_act:
        :return:
        """
        try:
            #(self.noael_mammal_water) * ((self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal)**0.25)
            sip_empty.noael_mammal_water = pd.Series([10.], dtype='int')
            sip_empty.bodyweight_tested_mammal = pd.Series([500.], dtype='int')
            sip_empty.bodyweight_assessed_mammal = pd.Series([400.], dtype='int')
            result = sip_empty.act()
            npt.assert_array_almost_equal(result, 10.5737, 4, '', True)
        finally:
            pass
        return

    # #Weird equation. Let's talk about this one.
    # def unit_test_det(self):
    #     """
    #     unittest for function sip.det
    #     return:
    #     """
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

    def test_unit_acute_bird(self):
        """
        unittest for function sip.acute_bird:
        :return:
        """
        try:
            # self.out_acute_bird = self.out_dose_bird / self.out_at_bird
            sip_empty.out_dose_bird = pd.Series([100.], dtype='int')
            sip_empty.out_at_bird = pd.Series([10.], dtype='int')
            result = sip_empty.acute_bird()
            npt.assert_array_almost_equal(result, 10., 4)
        finally:
            pass
        return

    def test_unit_acuconb(self):
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
        try:
            sip_empty.out_acute_bird = pd.Series([0.2])
            result = sip_empty.acuconb()
            exp = pd.Series(["Exposure through drinking water alone is a potential concern for birds"])
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_unit_acute_mamm(self):
        """
        unittest for function sip.acute_mamm:
        :return:
        """
        # self.out_acute_mamm = self.out_dose_mamm / self.out_at_mamm
        try:
            sip_empty.out_dose_mamm = pd.Series([100.], dtype='int')
            sip_empty.out_at_mamm = pd.Series([10.], dtype='int')
            result = sip_empty.acute_mamm()
            npt.assert_array_almost_equal(result, 10., 4)
        finally:
            pass
        return

    def test_unit_acuconm(self):
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
        try:
            sip_empty.out_acute_mamm = pd.Series([0.2])
            result = sip_empty.acuconm()
            exp = pd.Series(["Exposure through drinking water alone is a potential concern for mammals"])
            pdt.assert_series_equal(result, exp)
        finally:
            pass
        return

    def test_unit_chron_bird(self):
        """
        unittest for function sip.chron_bird:
        :return:
        """
        #self.out_chron_bird = self.out_dose_bird / self.out_det
        try:
            sip_empty.out_dose_bird = pd.Series([5.], dtype='int')
            sip_empty.out_det = pd.Series([10.], dtype='int')
            result = sip_empty.chron_bird()
            npt.assert_array_almost_equal(result, 0.5, 4, '', True)
        finally:
            pass
        return

    def test_unit_chronconb(self):
        """
        unittest for function sip.chronconb:
        :return:
        """
        try:
            sip_empty.out_chron_bird = pd.Series([3])
            result = sip_empty.chronconb()
            exp = pd.Series(["Exposure through drinking water alone is a potential concern for birds"])
            pdt.assert_series_equal(result, exp)
        finally:
            logging.info("chron bird result")
            logging.info(result)
            logging.info("chron bird result")
            logging.info(exp)
        return

    def test_unit_chron_mamm(self):
        """
        unittest for function sip.chron_mamm:
        :return:
        """
        # self.out_chron_mamm = self.out_dose_mamm / self.out_act
        sip_empty.out_dose_mamm = pd.Series([8.], dtype='int')
        sip_empty.out_act = pd.Series([4.], dtype='int')
        result = sip_empty.chron_mamm()
        npt.assert_array_almost_equal(result, 2, 4, '', True)
        return

    def test_unit_chronconm(self):
        """
        unittest for function sip.chronconm:
        :return:
        """
        try:
            sip_empty.out_chron_mamm = pd.Series([0.5])
            result = sip_empty.chronconm()
            exp = pd.Series(["Drinking water exposure alone is NOT a potential concern for mammals"])
            pdt.assert_series_equal(result, exp)
        finally:
            logging.info("chron mamm result")
            logging.info(result)
            logging.info("chron mamm result")
            logging.info(exp)
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
