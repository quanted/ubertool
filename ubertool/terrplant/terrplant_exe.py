from __future__ import division
import pandas as pd
from base.uber_model import UberModel, ModelSharedInputs


class TerrplantInputs(ModelSharedInputs):
    """
    Input class for Terrplant.
    """

    def __init__(self):
        """Class representing the inputs for TerrPlant"""
        super(TerrplantInputs, self).__init__()
        self.incorporation_depth = pd.Series([], dtype="float")
        self.runoff_fraction = pd.Series([], dtype="float")
        self.drift_fraction = pd.Series([], dtype="float")
        self.chemical_name = pd.Series([], dtype="object")
        self.use = pd.Series([], dtype="object")
        self.application_method = pd.Series([], dtype="object")
        self.application_form = pd.Series([], dtype="object")
        self.application_rate = pd.Series([], dtype="object")
        self.solubility = pd.Series([], dtype="float")
        self.ec25_nonlisted_seedling_emergence_monocot = pd.Series([], dtype="float")
        self.ec25_nonlisted_seedling_emergence_dicot = pd.Series([], dtype="float")
        self.noaec_listed_seedling_emergence_monocot = pd.Series([], dtype="float")
        self.noaec_listed_seedling_emergence_dicot = pd.Series([], dtype="float")
        self.ec25_nonlisted_vegetative_vigor_monocot = pd.Series([], dtype="float")
        self.ec25_nonlisted_vegetative_vigor_dicot = pd.Series([], dtype="float")
        self.noaec_listed_vegetative_vigor_monocot = pd.Series([], dtype="float")
        self.noaec_listed_vegetative_vigor_dicot = pd.Series([], dtype="float")


class TerrplantOutputs(object):
    """
    Output class for terrplant.
    """

    def __init__(self):
        """Class representing the outputs for TerrPlant"""
        super(TerrplantOutputs, self).__init__()
        self.out_run_dry = pd.Series(name="out_run_dry")
        self.out_run_semi = pd.Series(name="out_run_semi")
        self.out_total_dry = pd.Series(name="out_total_dry")
        self.out_total_semi = pd.Series(name="out_total_semi")
        self.out_spray = pd.Series(name="out_spray")
        self.out_min_nms_spray = pd.Series(name="out_min_nms_spray")
        self.out_min_lms_spray = pd.Series(name="out_min_lms_spray")
        self.out_min_nds_spray = pd.Series(name="out_min_nds_spray")
        self.out_min_lds_spray = pd.Series(name="out_min_lds_spray")
        self.out_nms_rq_dry = pd.Series(name="out_nms_rq_dry")
        self.out_nms_loc_dry = pd.Series(name="out_nms_loc_dry")
        self.out_nms_rq_semi = pd.Series(name="out_nms_rq_semi")
        self.out_nms_loc_semi = pd.Series(name="out_nms_loc_semi")
        self.out_nms_rq_spray = pd.Series(name="out_nms_rq_spray")
        self.out_nms_loc_spray = pd.Series(name="out_nms_loc_spray")
        self.out_lms_rq_dry = pd.Series(name="out_lms_rq_dry")
        self.out_lms_loc_dry = pd.Series(name="out_lms_loc_dry")
        self.out_lms_rq_semi = pd.Series(name="out_lms_rq_semi")
        self.out_lms_loc_semi = pd.Series(name="out_lms_loc_semi")
        self.out_lms_rq_spray = pd.Series(name="out_lms_rq_spray")
        self.out_lms_loc_spray = pd.Series(name="out_lms_loc_spray")
        self.out_nds_rq_dry = pd.Series(name="out_nds_rq_dry")
        self.out_nds_loc_dry = pd.Series(name="out_nds_loc_dry")
        self.out_nds_rq_semi = pd.Series(name="out_nds_rq_semi")
        self.out_nds_loc_semi = pd.Series(name="out_nds_loc_semi")
        self.out_nds_rq_spray = pd.Series(name="out_nds_rq_spray")
        self.out_nds_loc_spray = pd.Series(name="out_nds_loc_spray")
        self.out_lds_rq_dry = pd.Series(name="out_lds_rq_dry")
        self.out_lds_loc_dry = pd.Series(name="out_lds_loc_dry")
        self.out_lds_rq_semi = pd.Series(name="out_lds_rq_semi")
        self.out_lds_loc_semi = pd.Series(name="out_lds_loc_semi")
        self.out_lds_rq_spray = pd.Series(name="out_lds_rq_spray")
        self.out_lds_loc_spray = pd.Series(name="out_lds_loc_spray")


class Terrplant(UberModel, TerrplantInputs, TerrplantOutputs):
    """
    Estimates of exposure to terrestrial plants from single pesticide applications through runoff or drift.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Terrplant model and containing all its methods"""
        super(Terrplant, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Run the model's methods to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

    def run_methods(self):
        """Execute the model's methods to generate the model output"""
        try:
            self.run_dry()
            self.run_semi()
            self.spray()
            self.total_dry()
            self.total_semi()
            self.min_nms_spray()
            self.min_lms_spray()
            self.min_nds_spray()
            self.min_lds_spray()
            self.nms_rq_dry()
            self.loc_nms_dry()
            self.nms_rq_semi()
            self.loc_nms_semi()
            self.nms_rq_spray()
            self.loc_nms_spray()
            self.lms_rq_dry()
            self.loc_lms_dry()
            self.lms_rq_semi()
            self.loc_lms_semi()
            self.lms_rq_spray()
            self.loc_lms_spray()
            self.nds_rq_dry()
            self.loc_nds_dry()
            self.nds_rq_semi()
            self.loc_nds_semi()
            self.nds_rq_spray()
            self.loc_nds_spray()
            self.lds_rq_dry()
            self.loc_lds_dry()
            self.lds_rq_semi()
            self.loc_lds_semi()
            self.lds_rq_spray()
            self.loc_lds_spray()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

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
        #exceed_boolean = self.out_nms_rq_dry >= 1.0
        #self.out_nms_loc_dry = exceed_boolean.map(lambda x:
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
        #                                          'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
        #                                          else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
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
        #                                           'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
        #                                           else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
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


class TerrplantApiMetadata(object):
    """
    API class for Terrplant.
    """

    def __init__(self):
        """
        metadata constructor
        """
        pass

    def post(self):
        """
        Post routine for terrplant API.
        :return:
        """
        description = "Run TerrPlant with the user-supplied JSON"
        # parameters =
