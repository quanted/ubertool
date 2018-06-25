from __future__ import division
import pandas as pd
import os.path
import sys
import logging

# parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# sys.path.append(parentddir)

from base.uber_model import UberModel, ModelSharedInputs
from .varroapop_functions import VarroapopFunctions

class VarroapopInputs(ModelSharedInputs):
    """
    Input class for Varroapop.
    """

    def __init__(self):
        """Class representing the inputs for Varroapop"""
        super(VarroapopInputs, self).__init__()
        self.weather_location = pd.Series([], dtype="object")
        self.SimStart_month = pd.Series([], dtype="object")
        self.SimStart_day = pd.Series([], dtype="object")
        self.SimStart_year = pd.Series([], dtype="object")
        self.SimEnd_month = pd.Series([], dtype="object")
        self.SimEnd_day = pd.Series([], dtype="object")
        self.SimEnd_year = pd.Series([], dtype="object")
        self.ICQueenStrength = pd.Series([], dtype="float")
        self.ICForagerLifespan = pd.Series([], dtype="float")
        self.ForagerMaxProp = pd.Series([], dtype="float")
        self.ICWorkerAdults= pd.Series([], dtype="float")
        self.ICWorkerBrood = pd.Series([], dtype="float")
        self.ICWorkerLarvae = pd.Series([], dtype="float")
        self.ICWorkerEggs = pd.Series([], dtype="float")
        self.ICDroneAdults = pd.Series([], dtype="float")
        self.ICDroneBrood = pd.Series([], dtype="float")
        self.ICDroneLarvae = pd.Series([], dtype="float")
        self.ICDroneEggs = pd.Series([], dtype="float")
        self.RQEnableReQueen = pd.Series([], dtype="object")
        self.RQScheduled = pd.Series([], dtype="object")
        self.RQReQueenDate_month = pd.Series([], dtype="object")
        self.RQReQueenDate_day = pd.Series([], dtype="object")
        self.RQReQueenDate_year = pd.Series([], dtype="object")
        self.RQonce = pd.Series([], dtype="object")

        self.enable_mites = pd.Series([], dtype="object")
        self.ICWorkerAdultInfest = pd.Series([], dtype="float")
        self.ICWorkerBroodInfest = pd.Series([], dtype="float")
        self.ICDroneAdultInfest = pd.Series([], dtype="float")
        self.ICDroneBroodInfest = pd.Series([], dtype="float")
        self.ICWorkerMiteOffspring = pd.Series([], dtype="float")
        self.ICWorkerMiteSurvivorship = pd.Series([], dtype="float")
        self.ICDroneMiteOffspring = pd.Series([], dtype="float")
        self.ICDroneMiteSurvivorship = pd.Series([], dtype="float")
        self.ImmEnabled = pd.Series([], dtype="object")
        self.ImmType = pd.Series([], dtype="object")
        self.ImmStart_month = pd.Series([], dtype="object")
        self.ImmStart_day = pd.Series([], dtype="object")
        self.ImmStart_year = pd.Series([], dtype="object")
        self.ImmEnd_month = pd.Series([], dtype="object")
        self.ImmEnd_day = pd.Series([], dtype="object")
        self.ImmEnd_year = pd.Series([], dtype="object")
        self.TotalImmMites = pd.Series([], dtype="float")
        self.PctImmMitesResistant = pd.Series([], dtype="float")
        self.VTEnable = pd.Series([], dtype="object")
        self.VTTreatmentStart_month = pd.Series([], dtype="object")
        self.VTTreatmentStart_day = pd.Series([], dtype="object")
        self.VTTreatmentStart_year = pd.Series([], dtype="object")
        self.VTTreatmentDuration = pd.Series([], dtype="float")
        self.VTMortality = pd.Series([], dtype="float")
        self.InitMitePctResistant = pd.Series([], dtype="float")

        self.enable_pesticides = pd.Series([], dtype="object")
        self.chemical_name = pd.Series([], dtype="object")
        self.application_type = pd.Series([], dtype="object")
        self.ar_lb = pd.Series([], dtype="float")
        self.FoliarAppDate_month = pd.Series([], dtype="object")
        self.FoliarAppDate_day = pd.Series([], dtype="object")
        self.FoliarAppDate_year = pd.Series([], dtype="object")
        self.FoliarForageBegin_month = pd.Series([], dtype="object")
        self.FoliarForageBegin_day = pd.Series([], dtype="object")
        self.FoliarForageBegin_year = pd.Series([], dtype="object")
        self.FoliarForageEnd_month = pd.Series([], dtype="object")
        self.FoliarForageEnd_day = pd.Series([], dtype="object")
        self.FoliarForageEnd_year = pd.Series([], dtype="object")
        self.AIContactFactor = pd.Series([], dtype="float")
        self.SoilForageBegin_month = pd.Series([], dtype="object")
        self.SoilForageBegin_day = pd.Series([], dtype="object")
        self.SoilForageBegin_year = pd.Series([], dtype="object")
        self.SoilForageEnd_month = pd.Series([], dtype="object")
        self.SoilForageEnd_day = pd.Series([], dtype="object")
        self.SoilForageEnd_year = pd.Series([], dtype="object")
        self.ESoilConcentration = pd.Series([], dtype="float")
        self.l_kow = pd.Series([], dtype="float")
        self.k_oc = pd.Series([], dtype="float")
        self.ESoilTheta = pd.Series([], dtype="float")
        self.ESoilP = pd.Series([], dtype="float")
        self.ESoilFoc = pd.Series([], dtype="float")
        self.SeedForageBegin_month = pd.Series([], dtype="object")
        self.SeedForageBegin_day = pd.Series([], dtype="object")
        self.SeedForageBegin_year = pd.Series([], dtype="object")
        self.SeedForageEnd_month = pd.Series([], dtype="object")
        self.SeedForageEnd_day = pd.Series([], dtype="object")
        self.SeedForageEnd_year = pd.Series([], dtype="object")
        self.ESeedConcentration = pd.Series([], dtype="float")
        self.AIHalfLife = pd.Series([], dtype="float")
        self.AIAdultLD50 = pd.Series([], dtype="float")
        self.AIAdultSlope = pd.Series([], dtype="float")
        self.AILarvaLD50 = pd.Series([], dtype="float")
        self.AILarvaSlope = pd.Series([], dtype="float")
        self.AIAdultLD50Contact = pd.Series([], dtype="float")
        self.AIAdultSlopeContact = pd.Series([], dtype="float")
        self.FoliarEnabled = pd.Series([], dtype="object")
        self.SoilEnabled = pd.Series([], dtype="object")
        self.SeedEnabled = pd.Series([], dtype="object")

        self.InitColPollen = pd.Series([], dtype="float")
        self.InitColNectar = pd.Series([], dtype="float")
        self.MaxColPollen = pd.Series([], dtype="float")
        self.MaxColNectar = pd.Series([], dtype="float")
        self.NeedResourcesToLive = pd.Series([], dtype="float")
        self.IPollenTrips = pd.Series([], dtype="float")
        self.INectarTrips = pd.Series([], dtype="float")
        self.IPollenLoad = pd.Series([], dtype="float")
        self.INectarLoad = pd.Series([], dtype="float")
        self.SupPollenEnable = pd.Series([], dtype="object")
        self.SupPollenAmount = pd.Series([], dtype="float")
        self.SupPollenBegin_month = pd.Series([], dtype="object")
        self.SupPollenBegin_day = pd.Series([], dtype="object")
        self.SupPollenBegin_year = pd.Series([], dtype="object")
        self.SupPollenEnd_month = pd.Series([], dtype="object")
        self.SupPollenEnd_day = pd.Series([], dtype="object")
        self.SupPollenEnd_year = pd.Series([], dtype="object")
        self.SupNectarEnable = pd.Series([], dtype="object")
        self.SupNectarAmount = pd.Series([], dtype="float")
        self.SupNectarBegin_month = pd.Series([], dtype="object")
        self.SupNectarBegin_day = pd.Series([], dtype="object")
        self.SupNectarBegin_year = pd.Series([], dtype="object")
        self.SupNectarEnd_month = pd.Series([], dtype="object")
        self.SupNectarEnd_day = pd.Series([], dtype="object")
        self.SupNectarEnd_year = pd.Series([], dtype="object")
        self.CL4Pollen = pd.Series([], dtype="float")
        self.CL4Nectar = pd.Series([], dtype="float")
        self.CL5Pollen = pd.Series([], dtype="float")
        self.CL5Nectar = pd.Series([], dtype="float")
        self.CLDPollen = pd.Series([], dtype="float")
        self.CLDNectar = pd.Series([], dtype="float")
        self.CA13Pollen = pd.Series([], dtype="float")
        self.CA13Nectar = pd.Series([], dtype="float")
        self.CA410Pollen = pd.Series([], dtype="float")
        self.CA410Nectar = pd.Series([], dtype="float")
        self.CA1120Pollen = pd.Series([], dtype="float")
        self.CA1120Nectar = pd.Series([], dtype="float")
        self.CADPollen = pd.Series([], dtype="float")
        self.CADNectar = pd.Series([], dtype="float")
        self.CForagerPollen = pd.Series([], dtype="float")
        self.CForagerNectar = pd.Series([], dtype="float")





class VarroapopOutputs(object):
    """
    Output class for Varroapop.
    """

    def __init__(self):
        """Class representing the outputs for Varroapop"""
        super(VarroapopOutputs, self).__init__()
        self.out_date = pd.Series([], dtype='object', name="out_date")
        self.out_colony_size = pd.Series([], dtype='float', name="out_colony_size")
        self.out_adult_drones = pd.Series([], dtype='float', name="out_adult_drones")
        self.out_adult_workers = pd.Series([], dtype='float', name="out_adult_workers")
        self.out_foragers = pd.Series([], dtype='float', name="out_foragers")
        self.out_capped_drone_brood = pd.Series([], dtype='float', name="out_capped_drone_brood")
        self.out_capped_worker_brood = pd.Series([], dtype='float', name="out_capped_worker_brood")
        self.out_drone_larvae = pd.Series([], dtype='float', name="out_drone_larvae")
        self.out_worker_larvae = pd.Series([], dtype='float', name="out_worker_larvae")
        self.out_drone_eggs = pd.Series([], dtype='float', name="out_drone_eggs")
        self.out_worker_eggs = pd.Series([], dtype='float', name="out_worker_eggs")
        self.out_free_mites = pd.Series([], dtype='float', name="out_free_mites")
        self.out_drone_brood_mites = pd.Series([], dtype='float', name="out_drone_brood_mites")
        self.out_worker_brood_mites = pd.Series([], dtype='float', name="out_worker_brood_mites")
        self.out_drone_mites_per_cell = pd.Series([], dtype='float', name="out_drone_mites_per_cell")
        self.out_worker_mites_per_cell = pd.Series([], dtype='float', name="out_worker_mites_per_cell")
        self.out_mites_dying = pd.Series([], dtype='float', name="out_mites_dying")
        self.out_proportion_mites_dying = pd.Series([], dtype='float', name="out_proportion_mites_dying")
        self.out_colony_pollen = pd.Series([], dtype='float', name="out_colony_pollen")
        self.out_chemical_conc_pollen = pd.Series([], dtype='float', name="out_chemical_conc_pollen")
        self.out_colony_nectar = pd.Series([], dtype='float', name="out_colony_nectar")
        self.out_chemical_conc_nectar = pd.Series([], dtype='float', name="out_chemical_conc_nectar")
        self.out_dead_drone_larvae = pd.Series([], dtype='float', name="out_dead_drone_larave")
        self.out_dead_worker_larvae = pd.Series([], dtype='float', name="out_dead_worker_larave")
        self.out_dead_drone_adults = pd.Series([], dtype='float', name="out_dead_drone_adults")
        self.out_dead_worker_adults = pd.Series([], dtype='float', name="out_dead_worker_adults")
        self.out_dead_foragers = pd.Series([], dtype='float', name="out_dead_foragers")
        self.out_queen_strength = pd.Series([], dtype='float', name="out_queen_strength")
        self.out_average_temp_c = pd.Series([], dtype='float', name="out_average_temp_c")
        self.out_rain_inch = pd.Series([], dtype='float', name="out_rain_inch")

        #summary stats
        self.out_mean_colony_size = pd.Series([], dtype='float', name="out_mean_colony_size")
        self.out_max_colony_size = pd.Series([], dtype='float', name="out_max_colony_size")
        self.out_min_colony_size = pd.Series([], dtype='float', name="out_min_colony_size")
        self.out_total_bee_mortality = pd.Series([], dtype='float', name="out_total_bee_mortality")
        self.out_max_chemical_conc_pollen = pd.Series([], dtype='float', name="out_max_chemical_conc_pollen")
        self.out_max_chemical_conc_nectar = pd.Series([], dtype='float', name="out_max_chemical_conc_nectar")

        #ocpu session id (for fetching files later)
        self.out_api_sessionid = pd.Series([], dtype='object', name="out_api_sessionid")


class Varroapop(UberModel, VarroapopInputs, VarroapopOutputs, VarroapopFunctions):
    """
    Age-structured honey bee colony model with mite population dynamics and chemical exposure scenarios
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Varroapop model and containing all its methods"""
        super(Varroapop, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

    def execute_model(self):
        """
        Callable to execute the running of the model:
            1) Populate input parameters
            2) Create output DataFrame to hold the model outputs
            3) Call the model's API to generate outputs
            4) Fill the output DataFrame with the generated model outputs
        """
        self.populate_inputs(self.pd_obj)
        self.pd_obj_out = self.populate_outputs()
        self.run_methods()
        self.fill_output_dataframe()

    # Begin model methods
    def run_methods(self):
        """ Call the Varroapop API to run model"""
        try:
            logging.info("Calling VarroaPop API.....")
            r_api_request = self.call_varroapop_api()
            #print(r_api_request.headers)
            #print(r_api_request.text)
            self.fill_model_out_attr(r_api_request.content)
            self.fill_summary_stats()
            self.fill_sessionid(r_api_request.headers.get('X-ocpu-session'))
            return

        except Exception as e:
            logging.info("Exception while calling VarroaPop API!")
            logging.info(e)
            pass


class VarroapopFiles(VarroapopFunctions):

    def __init__(self, api_sessionid):
        self.api_sessionid = api_sessionid

    def fetch_input(self):
        return self.get_input_file(self.api_sessionid)

    def fetch_log(self):
        return self.get_log_file(self.api_sessionid)

    def fetch_results(self):
        return self.get_results_file(self.api_sessionid)
