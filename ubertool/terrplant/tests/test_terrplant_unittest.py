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
from terrplant_exe import Terrplant

# create empty pandas dataframes to create empty terrplant object for testing
df_empty = pd.DataFrame()
# create an empty sip object
terrplant_empty = Terrplant(df_empty, df_empty)

test = {}


class TestTerrplant(unittest.TestCase):
    """
    Unit tests for terrplant.
    """
    def setUp(self):
        """
        Setup routine for terrplant unit tests.
        :return:
        """
        pass
        # setup the test as needed
        # e.g. pandas to open terrplant qaqc csv
        #  Read qaqc csv and create pandas DataFrames for inputs and expected outputs

    def tearDown(self):
        """
        Teardown routine for terrplant unit tests.
        :return:
        """
        pass
        # teardown called after each test
        # e.g. maybe write test results to some text file

# each of these functions are queued by "run_methods" and have outputs defined as properties in the terrplant qaqc csv
    def test_rundry(self):
        """
        unittest for function terrplant.rundry
        """
        #(self.application_rate/self.incorporation_depth) * self.runoff_fraction
        expected_results = [0.5, 4.41, 6.048]
        try:
            terrplant_empty.application_rate = pd.Series([10, 21, 56], dtype='int')
            terrplant_empty.incorporation_depth = pd.Series([2, 1, 4], dtype='int')
            terrplant_empty.runoff_fraction = pd.Series([0.1, 0.21, 0.432 ], dtype='float')
            result = terrplant_empty.run_dry()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_runsemi(self):
        """
        unittest for function terrplant.runsemi
        """
        #self.out_runsemi = (self.application_rate/self.incorporation_depth) * self.runoff_fraction * 10
        expected_results = [5.0, 2.5, 19.0]
        try:
            terrplant_empty.application_rate = pd.Series([10, 20, 30], dtype='int')
            terrplant_empty.incorporation_depth = pd.Series([2, 4, 3], dtype='int')
            terrplant_empty.runoff_fraction = pd.Series([0.1, 0.05, 0.19], dtype='float')
            result = terrplant_empty.run_semi()
            npt.assert_array_almost_equal(result,expected_results, 4, '', True)
        finally:
            pass
        return

    def test_spray(self):
        """
        unittest for function terrplant.spray
        """
        #self.out_spray = self.application_rate * self.drift_fraction
        expected_results = [5.0, 5.36, 19.05]
        try:
            terrplant_empty.application_rate = pd.Series([10, 20, 30], dtype='int')
            terrplant_empty.drift_fraction = pd.Series([0.5, .268, 0.635], dtype='float')
            result = terrplant_empty.spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_totaldry(self):
        """
        unittest for function terrplant.totaldry
        """
        #self.out_totaldry = self.out_rundry + self.out_spray
        expected_results =[5.5, 15.65, 35.32]
        try:
            terrplant_empty.out_run_dry = pd.Series([0.5, 3.65, 12.32], dtype='float')
            terrplant_empty.out_spray = pd.Series([5.0, 12.0, 23.0], dtype='float')
            result = terrplant_empty.total_dry()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_totalsemi(self):
        """
        unittest for function terrplant.totalsemi
        """
        #self.out_totalsemi = self.out_runsemi + self.out_spray
        expected_results = [5.034, 46.52, 71.669, ]
        try:
            terrplant_empty.out_run_semi = pd.Series([5.0, 12.32, 59.439], dtype='float')
            terrplant_empty.out_spray = pd.Series([0.034, 34.2, 12.23], dtype='float')
            result = terrplant_empty.total_semi()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_nms_rq_dry(self):
        """
        unittest for function terrplant.nms_rq_dry
        """
        #self.out_nms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_monocot
        expected_results = [110.0, 1.45211, 0.0669796]
        try:
            terrplant_empty.out_total_dry = pd.Series([5.5, 17.89, 23.12345], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05, 12.32, 345.231], dtype='float')
            result = terrplant_empty.nms_rq_dry()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)

        finally:
            pass
        return

    def test_nms_loc_dry(self):
        """
        unittest for function terrplant.nms_loc_dry
        """
        # if self.out_nms_rq_dry >= 1.0:
        #     self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a dry area indicates a potential risk.')
        # else:
        #     self.out_nms_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a dry area indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for non-listed monocot seedlings exposed to the "
                            "pesticide via runoff to dry areas indicates a potential risk.",
                            "The risk quotient for non-listed monocot seedlings exposed to "
                            "the pesticide via runoff to dry areas indicates that potential "
                            "risk is minimal.", "The risk quotient for non-listed monocot "
                            "seedlings exposed to the pesticide via runoff to dry areas indicates "
                            "a potential risk."])
        try:
            terrplant_empty.out_nms_rq_dry = pd.Series([1.0, 0.5, 3.5], dtype='float')
            result = terrplant_empty.loc_nms_dry()
            pdt.assert_series_equal(result,expected_results, True)
        finally:
            pass
        return

    def test_nms_rq_semi(self):
        """
        unittest for function terrplant.nms_rq_semi
        """
        #self.out_nms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_monocot
        expected_results = [200.0, 4.197279, 16.18354]
        try:
            terrplant_empty.out_total_semi = pd.Series([10., 1.234, 23.984], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.05, 0.294, 1.482], dtype='float')
            result = terrplant_empty.nms_rq_semi()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_out_nms_loc_semi(self):
        """
        unittest for function terrplant.nms_loc_semi
        """
        # if self.out_nms_rq_semi >= 1.0:
        #     self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
        # else:
        #     self.out_nms_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for non-listed monocot seedlings exposed to the "
                                      "pesticide via runoff to semi-aquatic areas indicates a potential "
                                      "risk.", "The risk quotient for non-listed monocot seedlings exposed "
                                      "to the pesticide via runoff to semi-aquatic areas indicates that "
                                      "potential risk is minimal.", "The risk quotient for non-listed monocot "
                                      "seedlings exposed to the pesticide via runoff to semi-aquatic areas "
                                      "indicates a potential risk."])
        try:
            terrplant_empty.out_nms_rq_semi = pd.Series([1.0, 0.45, 2.7], dtype='float')
            result = terrplant_empty.loc_nms_semi()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_nms_rq_spray(self):
        """
        unittest for function terrplant.nms_rq_spray
        """
        #self.out_nms_rq_spray = self.out_spray/out__min_nms_spray
        expected_results = [215.5062, 1.896628, 16.60117]
        try:
            terrplant_empty.out_spray = pd.Series([5.045, 2.43565, 9.04332], dtype='float')
            terrplant_empty.out_min_nms_spray = pd.Series([0.02341, 1.2842, 0.54474], dtype='float')
            result = terrplant_empty.nms_rq_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_nms_loc_spray(self):
        """
        unittest for function terrplant.nms_loc_spray
        """
        # if self.out_nms_rq_spray >= 1.0:
        #     self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to'\
        # ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_nms_loc_spray = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        # ' pesticide via spray drift indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for non-listed monocot seedlings exposed to the pesticide via "
                            "spray drift indicates a potential risk.", "The risk quotient for non-listed monocot "
                            "seedlings exposed to the pesticide via spray drift indicates that potential risk "
                            "is minimal.", "The risk quotient for non-listed monocot seedlings exposed to the "
                            "pesticide via spray drift indicates a potential risk."])
        try:
            terrplant_empty.out_nms_rq_spray = pd.Series([2.2, 0.0056, 1.0], dtype='float')
            result = terrplant_empty.loc_nms_spray()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lms_rq_dry(self):
        """
        unittest for function terrplant.lms_rq_dry
        """
        #self.out_lms_rq_dry = self.out_totaldry/self.ec25_nonlisted_seedling_emergence_dicot
        expected_results = [550.0, 3.40279, 234.0831]
        try:
            terrplant_empty.out_total_dry = pd.Series([5.5, 1.094, 19.5436], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.01, 0.3215, 0.08349], dtype='float')
            result = terrplant_empty.lms_rq_dry()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_lms_loc_dry(self):
        """
        unittest for function terrplant.lms_loc_dry
        """
        # if self.out_lms_rq_dry >= 1.0:
        #     self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a dry area indicates a potential risk.')
        # else:
        #     self.out_lms_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to a dry area indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for listed monocot seedlings exposed to the pesticide "
                            "via runoff to dry areas indicates a potential risk.", "The risk quotient "
                            "for listed monocot seedlings exposed to the pesticide via runoff to dry "
                            "areas indicates that potential risk is minimal.", "The risk quotient for "
                            "listed monocot seedlings exposed to the pesticide via runoff to dry areas "
                            "indicates a potential risk."])
        try:
            terrplant_empty.out_lms_rq_dry = pd.Series([1.6, 0.045, 1.0], dtype='float')
            result = terrplant_empty.loc_lms_dry()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lms_rq_semi(self):
        """
        unittest for function terrplant.lms_rq_semi
        """
        #self.out_lms_rq_semi = self.out_totalsemi/self.ec25_nonlisted_seedling_emergence_dicot
        expected_results = [1000.0, 0.0217295, 72.19618]
        try:
            terrplant_empty.out_total_semi = pd.Series([10., 0.099, 24.5467], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.01, 4.556, 0.34], dtype='float')
            result = terrplant_empty.lms_rq_semi()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_lms_loc_semi(self):
        """
        unittest for function terrplant.lms_loc_semi
        """
        # if self.out_lms_rq_semi >= 1.0:
        #     self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to a semi-aquatic area indicates a potential risk.')
        # else:
        #     self.out_lms_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to a semi-aquatic area indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for listed monocot seedlings exposed to the pesticide via "
                            "runoff to semi-aquatic areas indicates a potential risk.", "The risk quotient "
                            "for listed monocot seedlings exposed to the pesticide via runoff to "
                            "semi-aquatic areas indicates that potential risk is minimal.", "The risk "
                            "quotient for listed monocot seedlings exposed to the pesticide via runoff "
                            "to semi-aquatic areas indicates a potential risk."])
        try:
            terrplant_empty.out_lms_rq_semi = pd.Series([1.0, 0.9, 6.456], dtype= 'float')
            result = terrplant_empty.loc_lms_semi()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lms_rq_spray(self):
        """
        unittest for function terrplant.lms_rq_spray
        """
        #self.out_lms_rq_spray = self.out_spray/self.ec25_nonlisted_seedling_emergence_dicot
        expected_results = [500.0, 3.754362, 0.04772294]
        try:
            terrplant_empty.out_spray = pd.Series([5., 9.1231, 0.09231], dtype='float')
            terrplant_empty.out_min_lms_spray = pd.Series([0.01, 2.43, 1.93429], dtype='float')
            result = terrplant_empty.lms_rq_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_lms_loc_spray(self):
        """
        unittest for function terrplant.lms_loc_spray
        """
        # if self.out_lms_rq_spray >= 1.0:
        #     self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_lms_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for listed monocot seedlings exposed "
                                      "to the pesticide via spray drift indicates a potential "
                                      "risk.", "The risk quotient for listed monocot seedlings "
                                      "exposed to the pesticide via spray drift indicates that "
                                      "potential risk is minimal.", "The risk quotient for "
                                      "listed monocot seedlings exposed to the pesticide via "
                                      "spray drift indicates a potential risk."])
        try:
            terrplant_empty.out_lms_rq_spray = pd.Series([1.1, 0.99, 3.129], dtype= 'float')
            result = terrplant_empty.loc_lms_spray()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_nds_rq_dry(self):
        """
        unittest for function terrplant.nds_rq_dry
        """
        #self.out_nds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_monocot
        expected_results = [275., 1.012424, 9.062258]
        try:
            terrplant_empty.out_total_dry = pd.Series([5.5, 1.0023, 19.32436], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.02, 0.99, 2.1324], dtype='float')
            result = terrplant_empty.nds_rq_dry()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_nds_loc_dry(self):
        """
        unittest for function terrplant.nds_loc_dry
        """
        # if self.out_nds_rq_dry >= 1.0:
        #     self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_nds_loc_dry = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for non-listed dicot seedlings exposed to the "
                                      "pesticide via runoff to dry areas indicates a potential "
                                      "risk.", "The risk quotient for non-listed dicot seedlings "
                                      "exposed to the pesticide via runoff to dry areas indicates "
                                      "that potential risk is minimal.", "The risk quotient for "
                                      "non-listed dicot seedlings exposed to the pesticide via runoff "
                                      "to dry areas indicates a potential risk."])
        try:
            terrplant_empty.out_nds_rq_dry = pd.Series([2.7, 0.923, 1.0], dtype='float')
            result = terrplant_empty.loc_nds_dry()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_nds_rq_semi(self):
        """
        unittest for function terrplant.nds_rq_semi
        """
        #self.out_nds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_monocot
        expected_results = [500., 3.464141, 0.999986]
        try:
            terrplant_empty.out_total_semi = pd.Series([10., 3.4295, 12.82323], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.02, 0.99, 12.8234], dtype='float')
            result = terrplant_empty.nds_rq_semi()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_nds_loc_semi(self):
        """
        unittest for function terrplant.nds_loc_semi
        """
        # if self.out_nds_rq_semi >= 1.0:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for non-listed dicot seedlings exposed to the "
                                      "pesticide via runoff to semi-aquatic areas indicates a potential "
                                      "risk.", "The risk quotient for non-listed dicot seedlings exposed "
                                      "to the pesticide via runoff to semi-aquatic areas indicates that "
                                      "potential risk is minimal.", "The risk quotient for non-listed "
                                      "dicot seedlings exposed to the pesticide via runoff to semi-aquatic "
                                      "areas indicates a potential risk."])
        try:
            terrplant_empty.out_nds_rq_semi = pd.Series([1.7, 0.001, 2.3134], dtype='float')
            result = terrplant_empty.loc_nds_semi()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_nds_rq_spray(self):
        """
        unittest for function terrplant.nds_rq_spray
        """
        #self.out_nds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_monocot
        expected_results = [235.5158, 0.2584818, 1.994142]
        try:
            terrplant_empty.out_spray = pd.Series([5., 0.9912, 23.9321], dtype='float')
            terrplant_empty.out_min_nds_spray = pd.Series([0.02123, 3.8347, 12.0012], dtype='float')
            result = terrplant_empty.nds_rq_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_nds_loc_spray(self):
        """
        unittest for function terrplant.nds_loc_spray
        """
        # if self.out_nds_rq_spray >= 1.0:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_nds_loc_semi = ('The risk quotient for non-listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for non-listed dicot seedlings exposed to the "
                                      "pesticide via spray drift indicates a potential risk.", "The "
                                      "risk quotient for non-listed dicot seedlings exposed to the "
                                      "pesticide via spray drift indicates that potential risk is "
                                      "minimal.", "The risk quotient for non-listed dicot seedlings "
                                      "exposed to the pesticide via spray drift indicates a potential risk."])
        try:
            terrplant_empty.out_nds_rq_spray = pd.Series([1.2, 0.439, 3.9921], dtype='float')
            result = terrplant_empty.loc_nds_spray()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lds_rq_dry(self):
        """
        unittest for function terrplant.lds_rq_dry
        """
        #self.out_lds_rq_dry = self.out_totaldry/self.noaec_listed_seedling_emergence_dicot
        expected_results = [55., 1.001862, 6.043703]
        try:
            terrplant_empty.out_total_dry = pd.Series([5.5, 0.991843, 12.7643], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1, .99, 2.112], dtype='float')
            result = terrplant_empty.lds_rq_dry()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_lds_loc_dry(self):
        """
        unittest for function terrplant.lds_loc_dry
        """
        # if self.out_lds_rq_dry >= 1.0:
        #     self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to dry areas indicates a potential risk.')
        # else:
        #     self.out_lds_loc_dry = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to dry areas indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for listed dicot seedlings exposed to the "
                                      "pesticide via runoff to dry areas indicates a potential "
                                      "risk.", "The risk quotient for listed dicot seedlings exposed "
                                      "to the pesticide via runoff to dry areas indicates that "
                                      "potential risk is minimal.", "The risk quotient for listed "
                                      "dicot seedlings exposed to the pesticide via runoff to dry "
                                      "areas indicates a potential risk."])
        try:
            terrplant_empty.out_lds_rq_dry = pd.Series([1.5, 0.00856, 4.2893], dtype= 'float')
            result = terrplant_empty.loc_lds_dry()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lds_rq_semi(self):
        """
        unittest for function terrplant.lds_rq_semi
        """
        #self.out_lds_rq_semi = self.out_totalsemi/self.noaec_listed_seedling_emergence_dicot
        expected_results = [100., 2502.0289, 16.08304]
        try:
            terrplant_empty.out_total_semi = pd.Series([10., 0.8632, 34.2321], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.1, 0.000345, 2.12846], dtype='float')
            result = terrplant_empty.lds_rq_semi()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_lds_loc_semi(self):
        """
        unittest for function terrplant.lds_loc_semi
        """
        # if self.out_lds_rq_semi >= 1.0:
        #     self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via runoff to semi-aquatic areas indicates a potential risk.')
        # else:
        #     self.out_lds_loc_semi = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for listed dicot seedlings exposed to the "
                                      "pesticide via runoff to semi-aquatic areas indicates a potential "
                                      "risk.", "The risk quotient for listed dicot seedlings exposed to "
                                      "the pesticide via runoff to semi-aquatic areas indicates that "
                                      "potential risk is minimal.", "The risk quotient for listed dicot "
                                      "seedlings exposed to the pesticide via runoff to semi-aquatic "
                                      "areas indicates a potential risk."])
        try:
            terrplant_empty.out_lds_rq_semi = pd.Series([4.5, 0.0028, 1.0], dtype= 'float')
            result = terrplant_empty.loc_lds_semi()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lds_rq_spray(self):
        """
        unittest for function terrplant.lds_rq_spray
        """
        #self.out_lds_rq_spray = self.out_spray/self.noaec_listed_seedling_emergence_dicot
        expected_results = [250., 0.7105719, 1.28799]
        try:
            terrplant_empty.out_spray = pd.Series([5.0, 0.94435, 12.7283], dtype='float')
            terrplant_empty.out_min_lds_spray = pd.Series([0.02, 1.329, 9.8823], dtype='float')
            result = terrplant_empty.lds_rq_spray()
            npt.assert_array_almost_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_lds_loc_spray(self):
        """
        unittest for function terrplant.lds_loc_spray
        """
        # if self.out_lds_rq_spray >= 1.0:
        #     self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to'\
        #     ' the pesticide via spray drift indicates a potential risk.')
        # else:
        #     self.out_lds_loc_spray = ('The risk quotient for listed monocot seedlings exposed to the'\
        #     ' pesticide via spray drift indicates that potential risk is minimal.')
        expected_results = pd.Series(["The risk quotient for listed dicot seedlings exposed to the "
                                      "pesticide via spray drift indicates a potential risk.", "The "
                                      "risk quotient for listed dicot seedlings exposed to the "
                                      "pesticide via spray drift indicates that potential risk is "
                                      "minimal.", "The risk quotient for listed dicot seedlings "
                                      "exposed to the pesticide via spray drift indicates a potential "
                                      "risk."])
        try:
            terrplant_empty.out_lds_rq_spray = pd.Series([1.8, 0.956, 3.25], dtype='float')
            result = terrplant_empty.loc_lds_spray()
            pdt.assert_series_equal(result, expected_results, True)
        finally:
            pass
        return

    def test_min_nms_spray(self):
        """
        unittest for function terrplant.min_nms_spray
        """
        expected_results = [0.0501, 0.9999, 1.9450]
        try:
            terrplant_empty.ec25_nonlisted_seedling_emergence_monocot = pd.Series([0.0501, 1.0004, 12.943], dtype='float')
            terrplant_empty.ec25_nonlisted_vegetative_vigor_monocot = pd.Series([0.0801, 0.9999, 1.9450], dtype='float')
            result = terrplant_empty.min_nms_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_min_lms_spray(self):
        """
        unittest for function terrplant.min_lms_spray
        """
        expected_results = [0.0205, 1.9234, 0.000453]
        try:
            terrplant_empty.noaec_listed_vegetative_vigor_monocot = pd.Series([0.0211, 1.9234, 0.001112], dtype='float')
            terrplant_empty.noaec_listed_seedling_emergence_monocot = pd.Series([0.0205, 3.231, 0.000453], dtype='float')
            result = terrplant_empty.min_lms_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_min_nds_spray(self):
        """
        unittest for function terrplant.min_nds_spray
        """
        expected_results = [0.0325, 0.00342, 1.3456]
        try:
            terrplant_empty.ec25_nonlisted_vegetative_vigor_dicot = pd.Series([0.0325, 3.432, 1.3456], dtype='float')
            terrplant_empty.ec25_nonlisted_seedling_emergence_dicot = pd.Series([0.5022, 0.00342, 1.34567], dtype='float')
            result = terrplant_empty.min_nds_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

    def test_min_lds_spray(self):
        """
        unittest for function terrplant.min_lds_spray
        """
        expected_results = [0.3206, 1.00319, 12.32]
        try:
            terrplant_empty.noaec_listed_seedling_emergence_dicot = pd.Series([0.3206, 1.0032, 43.4294], dtype='float')
            terrplant_empty.noaec_listed_vegetative_vigor_dicot = pd.Series([0.5872, 1.00319, 12.32], dtype='float')
            result = terrplant_empty.min_lds_spray()
            npt.assert_array_almost_equal(result, expected_results, 4, '', True)
        finally:
            pass
        return

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()