import unittest
import os.path
import sys
import numpy.testing as npt
import pandas as pd

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

    def setUp(self):
        """
        Setup routine for trex unit tests.
        :return:
        """
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

    def test_conc_initial(self):
        """
        unittest for function conc_initial:
        conc_0 = (app_rate * self.frac_act_ing * food_multiplier)
        """
        expected_results = [12.7160, 9.8280, 11.2320]
        try:
            # specify an app_rates Series (that is a series of lists, each list representing
            # a set of application rates for 'a' model simulation) and then extract the
            # 1st elements from each list to form a pd.Series of rates (using app_rate_parsing
            # method) representing the first day of application per model simulation
            trex_empty.app_rates = pd.Series([[0.34, 1.384, 13.54], [0.78, 11.34, 3.54],
                                          [2.34, 1.384, 3.4]], dtype='float')
            # parse app_rates Series of lists
            trex_empty.app_rate_parsing()
            trex_empty.food_multiplier_init_sg = pd.Series([110., 15., 240.], dtype='float')
            trex_empty.frac_act_ing = pd.Series([0.34, 0.84, 0.02], dtype='float')
            # just using a random food_multiplier variable for testing purposes
            result = trex_empty.conc_initial(trex_empty.food_multiplier_init_sg)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_conc_timestep(self):
        """
        unittest for function conc_timestep:
        """
        expected_results = [6.25e-5, 0.039685, 7.8886e-30]
        try:
            trex_empty.foliar_diss_hlife = pd.Series([.25, 0.75, 0.01], dtype='float')
            conc_0 = pd.Series([0.001, 0.1, 10.0])
            result = trex_empty.conc_timestep(conc_0)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_percent_to_frac(self):
        """
        unittest for function percent_to_frac:
        """
        expected_results = [.04556, .1034, .9389]
        try:
            trex_empty.percent_incorp = pd.Series([4.556, 10.34, 93.89], dtype='float')
            result = trex_empty.percent_to_frac(trex_empty.percent_incorp)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_inches_to_feet(self):
        """
        unittest for function inches_to_feet:
        """
        expected_results = [.37966, .86166, 7.82416]
        try:
            trex_empty.bandwidth = pd.Series([4.556, 10.34, 93.89], dtype='float')
            result = trex_empty.inches_to_feet(trex_empty.bandwidth)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_at_bird(self):
        """
        unittest for function at_bird:
        adjusted_toxicity = self.ld50_bird * (aw_bird / self.tw_bird_ld50) ** (self.mineau_sca_fact - 1)
        """
        expected_results = [69.17640, 146.8274, 56.00997]
        try:
            trex_empty.ld50_bird = pd.Series([100., 125., 90.], dtype='float')
            trex_empty.tw_bird_ld50 = pd.Series([175., 100., 200.], dtype='float')
            trex_empty.mineau_sca_fact = pd.Series([1.15, 0.9, 1.25], dtype='float')
            trex_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
            result = trex_empty.at_bird(trex_empty.aw_bird_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_fi_bird(self):
        """
        unittest for function fi_bird:
        food_intake = (0.648 * (aw_bird ** 0.651)) / (1 - mf_w_bird)
        """
        expected_results = [4.19728, 22.7780, 59.31724]
        try:
            trex_empty.mf_w_bird_1 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            trex_empty.aw_bird_sm = pd.Series([15., 20., 30.], dtype='float')
            result = trex_empty.fi_bird(trex_empty.aw_bird_sm, trex_empty.mf_w_bird_1)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_sc_bird(self):
        """
        unittest for function sc_bird:
        m_s_a_r = ((self.app_rate * self.frac_act_ing) / 128) * self.density * 10000  # maximum seed application rate=application rate*10000
        risk_quotient = m_s_a_r / self.noaec_bird        """
        expected_results = [40.9992, 1226.925, 68.1328]
        try:
            trex_empty.app_rates[0] = pd.Series([2.1, 12.3, 4.56], dtype='float')
            trex_empty.frac_act_ing = pd.Series([0.15, 0.20, 0.34], dtype='float')
            trex_empty.density = pd.Series([8.33, 7.98, 6.75], dtype='float')
            trex_empty.noaec_bird = pd.Series([5., 1.25, 12.], dtype='float')
            result = trex_empty.sc_bird(trex_empty.app_rates[0])
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_at_mamm(self):
        """
        unittest for function at_mamm:
        adjusted_toxicity = self.ld50_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
        """
        expected_results = [705.5036, 529.5517, 830.6143]
        try:
            trex_empty.ld50_mamm = pd.Series([321., 275., 432.], dtype='float')
            trex_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
            trex_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
            result = trex_empty.at_mamm(trex_empty.aw_mamm_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_anoael_mamm(self):
        """
        unittest for function anoael_mamm:
        adjusted_toxicity = self.noael_mamm * ((self.tw_mamm / aw_mamm) ** 0.25)
        """
        expected_results = [5.49457, 9.62821, 2.403398]
        try:
            trex_empty.noael_mamm = pd.Series([2.5, 5.0, 1.25], dtype='float')
            trex_empty.tw_mamm = pd.Series([350., 275., 410.], dtype='float')
            trex_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
            result = trex_empty.anoael_mamm(trex_empty.aw_mamm_sm)
            npt.assert_allclose(result,expected_results,rtol=1e-4, atol=0, err_msg='', verbose=True)
        finally:
            pass
        return

    def test_fi_mamm(self):
        """
        unittest for function fi_mamm:
        food_intake = (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)
        """
        expected_results = [3.17807, 16.82064, 42.2851]
        try:
            trex_empty.mf_w_mamm_1 = pd.Series([0.1, 0.8, 0.9], dtype='float')
            trex_empty.aw_mamm_sm = pd.Series([15., 20., 30.], dtype='float')
            result = trex_empty.fi_mamm(trex_empty.aw_mamm_sm, trex_empty.mf_w_mamm_1)
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