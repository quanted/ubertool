from __future__ import division
import pandas as pd
from ..base.uber_model import UberModel, ModelSharedInputs
from .terrplant_functions import TerrplantFunctions

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
        self.application_rate = pd.Series([], dtype="float")
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
        self.out_run_dry = pd.Series([], dtype="float", name="out_run_dry")
        self.out_run_semi = pd.Series([], dtype="float", name="out_run_semi")
        self.out_total_dry = pd.Series([], dtype="float", name="out_total_dry")
        self.out_total_semi = pd.Series([], dtype="float", name="out_total_semi")
        self.out_spray = pd.Series([], dtype="float", name="out_spray")
        self.out_min_nms_spray = pd.Series([], dtype="float", name="out_min_nms_spray")
        self.out_min_lms_spray = pd.Series([], dtype="float", name="out_min_lms_spray")
        self.out_min_nds_spray = pd.Series([], dtype="float", name="out_min_nds_spray")
        self.out_min_lds_spray = pd.Series([], dtype="float", name="out_min_lds_spray")
        self.out_nms_rq_dry = pd.Series([], dtype="float", name="out_nms_rq_dry")
        self.out_nms_loc_dry = pd.Series([], dtype="object", name="out_nms_loc_dry")
        self.out_nms_rq_semi = pd.Series([], dtype="float", name="out_nms_rq_semi")
        self.out_nms_loc_semi = pd.Series([], dtype="object", name="out_nms_loc_semi")
        self.out_nms_rq_spray = pd.Series([], dtype="float", name="out_nms_rq_spray")
        self.out_nms_loc_spray = pd.Series([], dtype="object", name="out_nms_loc_spray")
        self.out_lms_rq_dry = pd.Series([], dtype="float", name="out_lms_rq_dry")
        self.out_lms_loc_dry = pd.Series([], dtype="object", name="out_lms_loc_dry")
        self.out_lms_rq_semi = pd.Series([], dtype="float", name="out_lms_rq_semi")
        self.out_lms_loc_semi = pd.Series([], dtype="object", name="out_lms_loc_semi")
        self.out_lms_rq_spray = pd.Series([], dtype="float", name="out_lms_rq_spray")
        self.out_lms_loc_spray = pd.Series([], dtype="object", name="out_lms_loc_spray")
        self.out_nds_rq_dry = pd.Series([], dtype="float", name="out_nds_rq_dry")
        self.out_nds_loc_dry = pd.Series([], dtype="object", name="out_nds_loc_dry")
        self.out_nds_rq_semi = pd.Series([], dtype="float", name="out_nds_rq_semi")
        self.out_nds_loc_semi = pd.Series([], dtype="object", name="out_nds_loc_semi")
        self.out_nds_rq_spray = pd.Series([], dtype="float", name="out_nds_rq_spray")
        self.out_nds_loc_spray = pd.Series([], dtype="object", name="out_nds_loc_spray")
        self.out_lds_rq_dry = pd.Series([], dtype="float", name="out_lds_rq_dry")
        self.out_lds_loc_dry = pd.Series([], dtype="object", name="out_lds_loc_dry")
        self.out_lds_rq_semi = pd.Series([], dtype="float", name="out_lds_rq_semi")
        self.out_lds_loc_semi = pd.Series([], dtype="object", name="out_lds_loc_semi")
        self.out_lds_rq_spray = pd.Series([], dtype="float", name="out_lds_rq_spray")
        self.out_lds_loc_spray = pd.Series([], dtype="object", name="out_lds_loc_spray")


class Terrplant(UberModel, TerrplantInputs, TerrplantOutputs, TerrplantFunctions):
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
            pass


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
