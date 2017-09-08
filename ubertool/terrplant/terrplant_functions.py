from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
import pandas as pd

class TerrplantFunctions(object):
    """
    Function class for Stir.
    """

    def __init__(self):
        """Class representing the functions for Sip"""
        super(TerrplantFunctions, self).__init__()


    def run_dry(self):
        """
        EEC for runoff for dry areas
        """
        self.out_run_dry = (self.application_rate / self.incorporation_depth) * self.runoff_fraction
        return self.out_run_dry

    def run_semi(self):
        """
        EEC for runoff to semi-aquatic areas
        """
        self.out_run_semi = (self.application_rate / self.incorporation_depth) * self.runoff_fraction * 10
        return self.out_run_semi

    def spray(self):
        """
        EEC for spray drift
        """
        self.out_spray = self.application_rate * self.drift_fraction
        return self.out_spray

    def total_dry(self):
        """
        EEC total for dry areas
        """
        self.out_total_dry = self.out_run_dry + self.out_spray
        return self.out_total_dry

    def total_semi(self):
        """
        EEC total for semi-aquatic areas
        """
        self.out_total_semi = self.out_run_semi + self.out_spray
        return self.out_total_semi

    def nms_rq_dry(self):
        """
        Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a DRY area
        """
        self.out_nms_rq_dry = self.out_total_dry / self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_dry

    def loc_nms_dry(self):
        """
        Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area
        """
        msg_pass = "The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk."
        msg_fail = "The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_nms_rq_dry]
        self.out_nms_loc_dry = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        # exceed_boolean = self.out_nms_rq_dry >= 1.0
        # self.out_nms_loc_dry = exceed_boolean.map(lambda x:
        #                                          'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
        #                                          else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_nms_loc_dry

    def nms_rq_semi(self):
        """
        Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
        """
        self.out_nms_rq_semi = self.out_total_semi / self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_semi

    def loc_nms_semi(self):
        """
        Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area
        """
        msg_pass = "The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk."
        msg_fail = "The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_nms_rq_semi]
        self.out_nms_loc_semi = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_nms_rq_semi >= 1.0
        #self.out_nms_loc_semi = exceed_boolean.map(lambda x:
        #                                           'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
        #                                           else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_nms_loc_semi

    def nms_rq_spray(self):
        """
        Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
        """
        self.out_nms_rq_spray = self.out_spray / self.out_min_nms_spray
        return self.out_nms_rq_spray

    def loc_nms_spray(self):
        """
        Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift
        """
        msg_pass = "The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk."
        msg_fail = "The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_nms_rq_spray]
        self.out_nms_loc_spray = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_nms_rq_spray >= 1.0
        #self.out_nms_loc_spray = exceed_boolean.map(lambda x:
        #                                            'The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
        #                                            else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_nms_loc_spray

    def lms_rq_dry(self):
        """
        Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas
        """
        self.out_lms_rq_dry = self.out_total_dry / self.noaec_listed_seedling_emergence_monocot
        return self.out_lms_rq_dry

    def loc_lms_dry(self):
        """
        Level of concern for listed monocot seedlings exposed to pesticide via runoff in a dry area
        """
        msg_pass = "The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk."
        msg_fail = "The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_lms_rq_dry]
        self.out_lms_loc_dry = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_lms_rq_dry >= 1.0
        #self.out_lms_loc_dry = exceed_boolean.map(lambda x:
        # 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
        #  else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_lms_loc_dry

    def lms_rq_semi(self):
        """
        Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
        """
        self.out_lms_rq_semi = self.out_total_semi / self.noaec_listed_seedling_emergence_monocot
        return self.out_lms_rq_semi

    def loc_lms_semi(self):
        """
        Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas
        """
        msg_pass = "The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk."
        msg_fail = "The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_lms_rq_semi]
        self.out_lms_loc_semi = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_lms_rq_semi >= 1.0
        #self.out_lms_loc_semi = exceed_boolean.map(lambda x:
        #                                           'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
        #                                           else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_lms_loc_semi

    def lms_rq_spray(self):
        """
        Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
        """
        self.out_lms_rq_spray = self.out_spray / self.out_min_lms_spray
        return self.out_lms_rq_spray

    def loc_lms_spray(self):
        """
        Level of concern for listed monocot seedlings exposed to pesticide X via spray drift
        """
        msg_pass = "The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk."
        msg_fail = "The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_lms_rq_spray]
        self.out_lms_loc_spray = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_lms_rq_spray >= 1.0
        #self.out_lms_loc_spray = exceed_boolean.map(lambda x:
        #                                            'The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
        #                                            else 'The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_lms_loc_spray

    def nds_rq_dry(self):
        """
        Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas
        """
        self.out_nds_rq_dry = self.out_total_dry / self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_nds_rq_dry

    def loc_nds_dry(self):
        """
        Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas
        """
        msg_pass = "The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk."
        msg_fail = "The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_nds_rq_dry]
        self.out_nds_loc_dry = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_nds_rq_dry >= 1.0
        #self.out_nds_loc_dry = exceed_boolean.map(lambda x:
        #                                          'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
        #                                          else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_nds_loc_dry

    def nds_rq_semi(self):
        """
        Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
        """
        self.out_nds_rq_semi = self.out_total_semi / self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_nds_rq_semi

    def loc_nds_semi(self):
        """
        Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas
        """
        msg_pass = "The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk."
        msg_fail = "The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_nds_rq_semi]
        self.out_nds_loc_semi = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_nds_rq_semi >= 1.0
        #self.out_nds_loc_semi = exceed_boolean.map(lambda x:
        #'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
        # else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_nds_loc_semi

    def nds_rq_spray(self):
        """
        # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
        """
        self.out_nds_rq_spray = self.out_spray / self.out_min_nds_spray
        return self.out_nds_rq_spray

    def loc_nds_spray(self):
        """
        Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift
        """
        msg_pass = "The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk."
        msg_fail = "The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_nds_rq_spray]
        self.out_nds_loc_spray = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_nds_rq_spray >= 1.0
        #self.out_nds_loc_spray = exceed_boolean.map(lambda x:
        #                                            'The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
        #                                            else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_nds_loc_spray

    def lds_rq_dry(self):
        """
        Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas
        """
        self.out_lds_rq_dry = self.out_total_dry / self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_dry

    def loc_lds_dry(self):
        """
        Level of concern for listed dicot seedlings exposed to pesticideX in dry areas
        """
        msg_pass = "The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk."
        msg_fail = "The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_lds_rq_dry]
        self.out_lds_loc_dry = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_lds_rq_dry >= 1.0
        #self.out_lds_loc_dry = exceed_boolean.map(lambda x:
        #                                          'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
        #                                          else 'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_lds_loc_dry

    def lds_rq_semi(self):
        """
        Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
        """
        self.out_lds_rq_semi = self.out_total_semi / self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_semi

    def loc_lds_semi(self):
        """
        Level of concern for listed dicot seedlings exposed to pesticide X in dry areas
        """
        msg_pass = "The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk."
        msg_fail = "The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_lds_rq_semi]
        self.out_lds_loc_semi = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_lds_rq_semi >= 1.0
        #self.out_lds_loc_semi = exceed_boolean.map(lambda x:
        #                                           'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
        #                                           else 'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_lds_loc_semi

    def lds_rq_spray(self):
        """
        Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
        """
        self.out_lds_rq_spray = self.out_spray / self.out_min_lds_spray
        return self.out_lds_rq_spray

    def loc_lds_spray(self):
        """
        Level of concern for listed dicot seedlings exposed to pesticide X via spray drift
        """
        msg_pass = "The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk."
        msg_fail = "The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal."
        boo_ratios = [ratio >= 1.0 for ratio in self.out_lds_rq_spray]
        self.out_lds_loc_spray = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #exceed_boolean = self.out_lds_rq_spray >= 1.0
        #self.out_lds_loc_spray = exceed_boolean.map(
        #        lambda x:
        #           'The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
        #           else 'The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_lds_loc_spray

    def min_nms_spray(self):
        """
        determine minimum toxicity concentration used for RQ spray drift values
        non-listed monocot EC25 and NOAEC
        """
        s1 = pd.Series(self.ec25_nonlisted_seedling_emergence_monocot, name='seedling')
        s2 = pd.Series(self.ec25_nonlisted_vegetative_vigor_monocot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_nms_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_nms_spray

    def min_lms_spray(self):
        """
        determine minimum toxicity concentration used for RQ spray drift values
        listed monocot EC25 and NOAEC
        """
        s1 = pd.Series(self.noaec_listed_seedling_emergence_monocot, name='seedling')
        s2 = pd.Series(self.noaec_listed_vegetative_vigor_monocot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_lms_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_lms_spray

    def min_nds_spray(self):
        """
        determine minimum toxicity concentration used for RQ spray drift values
        non-listed dicot EC25 and NOAEC
        """
        s1 = pd.Series(self.ec25_nonlisted_seedling_emergence_dicot, name='seedling')
        s2 = pd.Series(self.ec25_nonlisted_vegetative_vigor_dicot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_nds_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_nds_spray

    def min_lds_spray(self):
        """
        determine minimum toxicity concentration used for RQ spray drift values
        listed dicot EC25 and NOAEC
        """
        s1 = pd.Series(self.noaec_listed_seedling_emergence_dicot, name='seedling')
        s2 = pd.Series(self.noaec_listed_vegetative_vigor_dicot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_lds_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_lds_spray