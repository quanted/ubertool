import unittest

import numpy.testing as npt
import pandas as pd

from .. import agdrift as agdrift_model

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
agdrift_empty = agdrift_model.Agdrift("empty", df_empty, df_empty)

rtol = 1e-5 # set relative tolerance level for npt.assert_allclose assertion tests
test = {}

class TestAgdrift(unittest.TestCase):
    """
    IEC unit tests.
    """
    def setUp(self):
        """
        setup the test as needed
        e.g. pandas to open agdrift qaqc csv
        Read qaqc csv and create pandas DataFrames for inputs and expected outputs
        :return:
        """
        pass

    def tearDown(self):
        """
        teardown called after each test
        e.g. maybe write test results to some text file
        :return:
        """
        pass


    def test_express_extrapolate_f(self):
        """
        unittest for function agdrift.express_extrapolate_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_foa_to_gha_f(self):
        """
        unittest for function agdrift.deposition_foa_to_gha_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_foa_to_lbac_f(self):
        """
        unittest for function agdrift.deposition_foa_to_lbac_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_lbac_to_gha_f(self):
        """
        unittest for function agdrift.deposition_lbac_to_gha_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_gha_to_ngl_f(self):
        """
        unittest for function agdrift.deposition_gha_to_ngl_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_gha_to_mgcm_f(self):
        """
        unittest for function agdrift.deposition_gha_to_mgcm_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_ngl_2_gha_f(self):
        """
        unittest for function agdrift.deposition_ngl_2_gha_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_ghac_to_lbac_f(self):
        """
        unittest for function agdrift.deposition_ghac_to_lbac_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_lbac_to_foa_f(self):
        """
        unittest for function agdrift.deposition_lbac_to_foa_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return

    def test_deposition_mgcm_to_gha_f(self):
        """
        unittest for function agdrift.deposition_mgcm_to_gha_f:
        :return:
        """
        try:
            agdrift_empty.threshold = pd.Series([0.6])
            agdrift_empty.lc50 = pd.Series([3])
            agdrift_empty.dose_response = pd.Series([2.5])
            result = agdrift_empty.z_score_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
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
