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
            agdrift_empty.distance = pd.Series([130.])
            agdrift_empty.out_y = agdrift_empty.pond_airblast_orchard
            agdrift_empty.application_rate = pd.Series([2.2])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            result = agdrift_empty.deposition_foa_to_gha_f()
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
            agdrift_empty.distance = pd.Series([75.])
            agdrift_empty.out_y = agdrift_empty.pond_aerial_vf2f
            agdrift_empty.application_rate = pd.Series([1.7])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            result = agdrift_empty.deposition_foa_to_lbac_f()
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
            agdrift_empty.distance = pd.Series([12.])
            agdrift_empty.out_y = agdrift_empty.pond_ground_high_f2m
            agdrift_empty.application_rate = pd.Series([2.5])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            result = agdrift_empty.deposition_lbac_to_gha_f()
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
            agdrift_empty.distance = pd.Series([128.])
            agdrift_empty.out_y = agdrift_empty.pond_ground_high_f2m
            agdrift_empty.application_rate = pd.Series([5.2])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
            agdrift_empty.aquatic_type = pd.Series([2.])
            result = agdrift_empty.deposition_gha_to_ngl_f()
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
            agdrift_empty.distance = pd.Series([190.])
            agdrift_empty.out_y = agdrift_empty.pond_ground_low_f2m
            agdrift_empty.application_rate = pd.Series([2.1])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
            result = agdrift_empty.deposition_gha_to_mgcm_f()
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
            agdrift_empty.distance = pd.Series([223.])
            agdrift_empty.out_y = agdrift_empty.pond_aerial_f2m
            agdrift_empty.application_rate = pd.Series([5.8])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
            agdrift_empty.out_deposition_ngl = agdrift_empty.deposition_gha_to_ngl_f()
            agdrift_empty.aquatic_type = pd.Series([1.])
            result = agdrift_empty.deposition_ngl_2_gha_f()
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
            agdrift_empty.distance = pd.Series([270.])
            agdrift_empty.out_y = agdrift_empty.pond_airblast_vineyard
            agdrift_empty.application_rate = pd.Series([6.5])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
            result = agdrift_empty.deposition_ghac_to_lbac_f()
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
            agdrift_empty.distance = pd.Series([200.])
            agdrift_empty.out_y = agdrift_empty.pond_ground_low_f2m
            agdrift_empty.application_rate = pd.Series([3.5])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            result = agdrift_empty.deposition_lbac_to_foa_f()
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
            agdrift_empty.distance = pd.Series([76.])
            agdrift_empty.out_y = agdrift_empty.pond_airblast_vineyard
            agdrift_empty.application_rate = pd.Series([0.23])
            agdrift_empty.out_init_avg_dep_foa = agdrift_empty.express_extrapolate_f()
            agdrift_empty.out_avg_depo_lbac = agdrift_empty.deposition_foa_to_lbac_f()
            agdrift_empty.out_avg_depo_gha = agdrift_empty.deposition_lbac_to_gha_f()
            agdrift_empty.out_deposition_mgcm = agdrift_empty.deposition_gha_to_mgcm_f()
            result = agdrift_empty.deposition_mgcm_to_gha_f()
            #npt.assert_array_almost_equal(result, -0.554622, 4, '', True)
            npt.assert_allclose(result,-0.554622,rtol,0,'',True)
        finally:
            pass
        return
    
# unittest will
# 1) call the setup method
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass
