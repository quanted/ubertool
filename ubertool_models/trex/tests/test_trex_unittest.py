import unittest
import numpy.testing as npt
import pandas as pd
import pandas.util.testing as pdt

from .. import sip_model_rest as sip_model

# create empty pandas dataframes to create empty sip object for testing
df_empty = pd.DataFrame()
# create an empty sip object
trex_empty = trex2_model.sip("empty", df_empty, df_empty)

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

# unittest will
# 1) call the setup method,
# 2) then call every method starting with "test",
# 3) then the teardown method
if __name__ == '__main__':
    unittest.main()
    #pass