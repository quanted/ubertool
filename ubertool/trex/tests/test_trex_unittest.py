import unittest
import os.path
import sys
import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt

#find parent directory and import model
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)

from trex_exe import TRex

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty trex object
trex_empty = TRex(df_empty, df_empty)

test = {}

class TestTrex(unittest.TestCase):
    def setup(self):
        pass
        # trex2 = trex2_model.sip(0, pd_obj_inputs, pd_obj_exp_out)
        # setup the test as needed
        # e.g. pandas to open sip qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def teardown(self):
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

    # def unit_test_fw_bird(self):
    #     '''
    #     unittest for function sip.fw_bird:
    #     '''
    #     try:
    #         result = sip_empty.fw_bird()
    #         npt.assert_array_almost_equal(result, 0.0162, 4, '', True)
    #     finally:
    #         pass
    #     return
    #
    # def unit_test_acuconb(self):
    #     '''
    #     unittest for function sip.acuconb:
    #     '''
    #     """
    #     Message stating whether or not a risk is present
    #     """
    #     try:
    #         sip_empty.acute_bird_out = pd.Series([0.2])
    #         result = sip_empty.acuconb()
    #         exp = pd.Series(["Exposure through drinking water alone is a potential concern for birds"])
    #         pdt.assert_series_equal(result, exp)
    #     finally:
    #         pass
    #     return

    def test_c_0_sg(self):
        """
        unittest for function c_0_sg:
        """
        expected_results = [190.9440, 7254.374, 93727.87]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_0_cg()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_0_tg(self):
        """
        unittest for function c_0_tg:
        """
        expected_results = [87.51600, 3324.922, 42958.61]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_0_tg()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_0_blp(self):
        """
        unittest for function c_0_blp:
        """
        expected_results = [315.9000, 343.7856, 52721.93]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 1.84, 110.32], dtype='float')
            result = trex_empty.c_0_blp()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_0_fp(self):
        """
        unittest for function c_0_fp:
        """
        expected_results = [35.1000, 453.3984, 5857.992]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_0_fp()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_0_arthro(self):
        """
        unittest for function c_0_arthro:
        """
        expected_results = [74.7864, 2841.297, 36710.08]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_0_arthro()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_mean_sg(self):
        """
        unittest for function c_mean_sg:
        """
        expected_results = [67.62600, 2569.258, 33195.29]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_mean_sg()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_mean_tg(self):
        """
        unittest for function c_mean_tg:
        """
        expected_results = [28.64160, 1088.156, 14059.18]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_mean_tg()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_mean_blp(self):
        """
        unittest for function c_mean_blp:
        """
        expected_results = [35.80200, 1360.195, 17573.98]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_mean_blp()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_mean_fp(self):
        """
        unittest for function c_0_fp:
        """
        expected_results = [5.569200, 211.5859, 2733.730]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_0_fp()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_c_mean_arthro(self):
        """
        unittest for function c_mean_arthro:
        """
        expected_results = [51.71400, 1964.726, 25384.63]
        try:
            trex_empty.first_app_lb = pd.Series([0.34, 1.384, 3.54], dtype='float')
            trex_empty.self.a_i = pd.Series([2.34, 21.84, 110.32], dtype='float')
            result = trex_empty.c_mean_arthro()
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return



# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass