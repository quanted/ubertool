from __future__ import division
from ..base.ubertool import UberModel
import pandas as pd


class TerrplantInputs(object):
    def __init__(self):
        """Class representing the inputs for TerrPlant"""
        super(TerrplantInputs, self).__init__()
        self.version_terrplant = pd.Series([], dtype="object")
        self.application_rate = pd.Series([], dtype="float")
        self.incorporation_depth = pd.Series([], dtype="float")
        self.runoff_fraction = pd.Series([], dtype="float")
        self.drift_fraction = pd.Series([], dtype="float")
        self.chemical_name = pd.Series([], dtype="object")
        self.pc_code = pd.Series([], dtype="object")
        self.use = pd.Series([], dtype="object")
        self.application_method = pd.Series([], dtype="object")
        self.application_form = pd.Series([], dtype="object")
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
    def __init__(self):
        """Class representing the outputs for TerrPlant"""
        super(TerrplantOutputs, self).__init__()
        self.out_rundry = pd.Series(name="out_rundry").astype("float")
        self.out_runsemi = pd.Series(name="out_runsemi").astype("float")
        self.out_totaldry = pd.Series(name="out_totaldry").astype("float")
        self.out_totalsemi = pd.Series(name="out_totalsemi").astype("float")
        self.out_spray = pd.Series(name="out_spray").astype("float")
        self.out_min_nms_spray = pd.Series(name="out_min_nms_spray").astype("float")
        self.out_min_lms_spray = pd.Series(name="out_min_lms_spray").astype("float")
        self.out_min_nds_spray = pd.Series(name="out_min_nds_spray").astype("float")
        self.out_min_lds_spray = pd.Series(name="out_min_lds_spray").astype("float")
        self.out_nms_rq_dry = pd.Series(name="out_nms_rq_dry").astype("float")
        self.out_nms_loc_dry = pd.Series(name="out_nms_loc_dry").astype("float")
        self.out_nms_rq_semi = pd.Series(name="out_nms_rq_semi").astype("float")
        self.out_nms_loc_semi = pd.Series(name="out_nms_loc_semi").astype("float")
        self.out_nms_rq_spray = pd.Series(name="out_nms_rq_spray").astype("float")
        self.out_nms_loc_spray = pd.Series(name="out_nms_loc_spray").astype("float")
        self.out_lms_rq_dry = pd.Series(name="out_lms_rq_dry").astype("float")
        self.out_lms_loc_dry = pd.Series(name="out_lms_loc_dry").astype("float")
        self.out_lms_rq_semi = pd.Series(name="out_lms_rq_semi").astype("float")
        self.out_lms_loc_semi = pd.Series(name="out_lms_loc_semi").astype("float")
        self.out_lms_rq_spray = pd.Series(name="out_lms_rq_spray").astype("float")
        self.out_lms_loc_spray = pd.Series(name="out_lms_loc_spray").astype("float")
        self.out_nds_rq_dry = pd.Series(name="out_nds_rq_dry").astype("float")
        self.out_nds_loc_dry = pd.Series(name="out_nds_loc_dry").astype("float")
        self.out_nds_rq_semi = pd.Series(name="out_nds_rq_semi").astype("float")
        self.out_nds_loc_semi = pd.Series(name="out_nds_loc_semi").astype("float")
        self.out_nds_rq_spray = pd.Series(name="out_nds_rq_spray").astype("float")
        self.out_nds_loc_spray = pd.Series(name="out_nds_loc_spray").astype("float")
        self.out_lds_rq_dry = pd.Series(name="out_lds_rq_dry").astype("float")
        self.out_lds_loc_dry = pd.Series(name="out_lds_loc_dry").astype("float")
        self.out_lds_rq_semi = pd.Series(name="out_lds_rq_semi").astype("float")
        self.out_lds_loc_semi = pd.Series(name="out_lds_loc_semi").astype("float")
        self.out_lds_rq_spray = pd.Series(name="out_lds_rq_spray").astype("float")
        self.out_lds_loc_spray = pd.Series(name="out_lds_loc_spray").astype("float")


class Terrplant(UberModel, TerrplantInputs, TerrplantOutputs):
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
        self.populate_inputs(self.pd_obj, self)
        self.pd_obj_out = self.populate_outputs(self)
        self.run_methods()
        self.fill_output_dataframe(self)

    def run_methods(self):
        """Execute the model's methods to generate the model output"""
        try:
            self.rundry()
            self.runsemi()
            self.spray()
            self.totaldry()
            self.totalsemi()
            self.minnmsspray()
            self.minlmsspray()
            self.minndsspray()
            self.minldsspray()
            self.nmsRQdry()
            self.LOCnmsdry()
            self.nmsRQsemi()
            self.LOCnmssemi()
            self.nmsRQspray()
            self.LOCnmsspray()
            self.lmsRQdry()
            self.LOClmsdry()
            self.lmsRQsemi()
            self.LOClmssemi()
            self.lmsRQspray()
            self.LOClmsspray()
            self.ndsRQdry()
            self.LOCndsdry()
            self.ndsRQsemi()
            self.LOCndssemi()
            self.ndsRQspray()
            self.LOCndsspray()
            self.ldsRQdry()
            self.LOCldsdry()
            self.ldsRQsemi()
            self.LOCldssemi()
            self.ldsRQspray()
            self.LOCldsspray()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    def rundry(self):
        '''
        EEC for runoff for dry areas
        '''
        self.out_rundry = (self.application_rate / self.incorporation_depth) * self.runoff_fraction
        return self.out_rundry

    def runsemi(self):
        '''
        EEC for runoff to semi-aquatic areas
        '''
        self.out_runsemi = (self.application_rate / self.incorporation_depth) * self.runoff_fraction * 10
        return self.out_runsemi

    def spray(self):
        '''
        EEC for spray drift
        '''
        self.out_spray = self.application_rate * self.drift_fraction
        return self.out_spray

    def totaldry(self):
        '''
        EEC total for dry areas
        '''
        self.out_totaldry = self.out_rundry + self.out_spray
        return self.out_totaldry

    def totalsemi(self):
        '''
        EEC total for semi-aquatic areas
        '''
        self.out_totalsemi = self.out_runsemi + self.out_spray
        return self.out_totalsemi

    def nmsRQdry(self):
        '''
        Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a DRY area
        '''
        self.out_nms_rq_dry = self.out_totaldry / self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_dry

    def LOCnmsdry(self):
        '''
        Level of concern for non-listed monocot seedlings exposed to pesticide X in a dry area
        '''
        exceed_boolean = self.out_nms_rq_dry >= 1.0
        self.out_nms_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_nms_loc_dry

    def nmsRQsemi(self):
        '''
        Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
        '''
        self.out_nms_rq_semi = self.out_totalsemi / self.ec25_nonlisted_seedling_emergence_monocot
        return self.out_nms_rq_semi

    def LOCnmssemi(self):
        '''
        Level of concern for non-listed monocot seedlings exposed to pesticide X in a semi-aquatic area
        '''
        exceed_boolean = self.out_nms_rq_semi >= 1.0
        self.out_nms_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_nms_loc_semi

    def nmsRQspray(self):
        '''
        Risk Quotient for NON-LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
        '''
        self.out_nms_rq_spray = self.out_spray / self.out_min_nms_spray
        return self.out_nms_rq_spray

    def LOCnmsspray(self):
        '''
        Level of concern for non-listed monocot seedlings exposed to pesticide via spray drift
        '''
        exceed_boolean = self.out_nms_rq_spray >= 1.0
        self.out_nms_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for non-listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_nms_loc_spray

    def lmsRQdry(self):
        '''
        Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a DRY areas
        '''
        self.out_lms_rq_dry = self.out_totaldry / self.noaec_listed_seedling_emergence_monocot
        return self.out_lms_rq_dry

    def LOClmsdry(self):
        '''
        Level of concern for listed monocot seedlings exposed to pesticide via runoff in a dry area
        '''
        exceed_boolean = self.out_lms_rq_dry >= 1.0
        self.out_lms_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_lms_loc_dry

    def lmsRQsemi(self):
        '''
        Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X in a SEMI-AQUATIC area
        '''
        self.out_lms_rq_semi = self.out_totalsemi / self.noaec_listed_seedling_emergence_monocot
        return self.out_lms_rq_semi

    def LOClmssemi(self):
        '''
        Level of concern for listed monocot seedlings exposed to pesticide X in semi-aquatic areas
        '''
        exceed_boolean = self.out_lms_rq_semi >= 1.0
        self.out_lms_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for listed monocot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_lms_loc_semi

    def lmsRQspray(self):
        '''
        Risk Quotient for LISTED MONOCOT seedlings exposed to Pesticide X via SPRAY drift
        '''
        self.out_lms_rq_spray = self.out_spray / self.out_min_lms_spray
        return self.out_lms_rq_spray

    def LOClmsspray(self):
        '''
        Level of concern for listed monocot seedlings exposed to pesticide X via spray drift
        '''
        exceed_boolean = self.out_lms_rq_spray >= 1.0
        self.out_lms_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for listed monocot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_lms_loc_spray

    def ndsRQdry(self):
        '''
        Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in DRY areas
        '''
        self.out_nds_rq_dry = self.out_totaldry / self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_nds_rq_dry

    def LOCndsdry(self):
        '''
        Level of concern for non-listed dicot seedlings exposed to pesticide X in dry areas
        '''
        exceed_boolean = self.out_nds_rq_dry >= 1.0
        self.out_nds_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_nds_loc_dry

    def ndsRQsemi(self):
        '''
        Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
        '''
        self.out_nds_rq_semi = self.out_totalsemi / self.ec25_nonlisted_seedling_emergence_dicot
        return self.out_nds_rq_semi

    def LOCndssemi(self):
        '''
        Level of concern for non-listed dicot seedlings exposed to pesticide X in semi-aquatic areas
        '''
        exceed_boolean = self.out_nds_rq_semi >= 1.0
        self.out_nds_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_nds_loc_semi

    def ndsRQspray(self):
        '''
        # Risk Quotient for NON-LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
        '''
        self.out_nds_rq_spray = self.out_spray / self.out_min_nds_spray
        return self.out_nds_rq_spray

    def LOCndsspray(self):
        '''
        Level of concern for non-listed dicot seedlings exposed to pesticide X via spray drift
        '''
        exceed_boolean = self.out_nds_rq_spray >= 1.0
        self.out_nds_loc_spray = exceed_boolean.map(lambda x:
                                                    'The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates a potential risk.' if x == True
                                                    else 'The risk quotient for non-listed dicot seedlings exposed to the pesticide via spray drift indicates that potential risk is minimal.')
        return self.out_nds_loc_spray

    def ldsRQdry(self):
        '''
        Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in DRY areas
        '''
        self.out_lds_rq_dry = self.out_totaldry / self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_dry

    def LOCldsdry(self):
        '''
        Level of concern for listed dicot seedlings exposed to pesticideX in dry areas
        '''
        exceed_boolean = self.out_lds_rq_dry >= 1.0
        self.out_lds_loc_dry = exceed_boolean.map(lambda x:
                                                  'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates a potential risk.' if x == True
                                                  else 'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to dry areas indicates that potential risk is minimal.')
        return self.out_lds_loc_dry

    def ldsRQsemi(self):
        '''
        Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X in SEMI-AQUATIC areas
        '''
        self.out_lds_rq_semi = self.out_totalsemi / self.noaec_listed_seedling_emergence_dicot
        return self.out_lds_rq_semi

    def LOCldssemi(self):
        '''
        Level of concern for listed dicot seedlings exposed to pesticide X in dry areas
        '''
        exceed_boolean = self.out_lds_rq_semi >= 1.0
        self.out_lds_loc_semi = exceed_boolean.map(lambda x:
                                                   'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates a potential risk.' if x == True
                                                   else 'The risk quotient for listed dicot seedlings exposed to the pesticide via runoff to semi-aquatic areas indicates that potential risk is minimal.')
        return self.out_lds_loc_semi

    def ldsRQspray(self):
        '''
        Risk Quotient for LISTED DICOT seedlings exposed to Pesticide X via SPRAY drift
        '''
        self.out_lds_rq_spray = self.out_spray / self.out_min_lds_spray
        return self.out_lds_rq_spray

    def LOCldsspray(self):
        '''
        Level of concern for listed dicot seedlings exposed to pesticide X via spray drift
        '''
        exceed_boolean = self.out_lds_rq_spray >= 1.0
        self.out_lds_loc_spray = exceed_boolean.map(
                lambda
                    x: 'The risk quotient for listed dicot seedlings exposed to the pesticide via spray drift indicates '
                       'a potential risk.' if x == True else 'The risk quotient for listed dicot seedlings exposed to '
                                                             'the pesticide via spray drift indicates that potential '
                                                             'risk is minimal.')
        return self.out_lds_loc_spray

    def minnmsspray(self):
        '''
        determine minimum toxicity concentration used for RQ spray drift values
        non-listed monocot EC25 and NOAEC
        '''
        s1 = pd.Series(self.ec25_nonlisted_seedling_emergence_monocot, name='seedling')
        s2 = pd.Series(self.ec25_nonlisted_vegetative_vigor_monocot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_nms_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_nms_spray

    def minlmsspray(self):
        '''
        determine minimum toxicity concentration used for RQ spray drift values
        listed monocot EC25 and NOAEC
        '''
        s1 = pd.Series(self.noaec_listed_seedling_emergence_monocot, name='seedling')
        s2 = pd.Series(self.noaec_listed_vegetative_vigor_monocot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_lms_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_lms_spray

    def minndsspray(self):
        '''
        determine minimum toxicity concentration used for RQ spray drift values
        non-listed dicot EC25 and NOAEC
        '''
        s1 = pd.Series(self.ec25_nonlisted_seedling_emergence_dicot, name='seedling')
        s2 = pd.Series(self.ec25_nonlisted_vegetative_vigor_dicot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_nds_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_nds_spray

    def minldsspray(self):
        '''
        determine minimum toxicity concentration used for RQ spray drift values
        listed dicot EC25 and NOAEC
        '''
        s1 = pd.Series(self.noaec_listed_seedling_emergence_dicot, name='seedling')
        s2 = pd.Series(self.noaec_listed_vegetative_vigor_dicot, name='vegetative')
        df = pd.concat([s1, s2], axis=1)
        self.out_min_lds_spray = pd.DataFrame.min(df, axis=1)
        return self.out_min_lds_spray


class TerrplantApiMetadata(object):
    def __init__(self):
        '''
        metadata constructor
        '''
        pass

    def post(self):
        description = "Run TerrPlant with the user-supplied JSON"
        # parameters =
