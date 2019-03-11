from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import logging
import json
import requests
import math
import pandas as pd
import os

#rest_url_varroapop = os.environ.get('OPENCPU_REST_SERVER')

if not os.environ.get('OPENCPU_REST_SERVER'):
    rest_url_varroapop = 'http://172.20.100.18:5656'

rest_url_varroapop = 'http://127.0.0.1:5050'


class VarroapopFunctions(object):
    """
    Function class for Stir.
    """

    def __init__(self):
        """Class representing the functions for VarroaPop"""
        super(VarroapopFunctions, self).__init__()


    def call_varroapop_api(self):
        logging.info("=========== formatting Varroapop JSON payload")
        input_json = self.format_varroapop_payload()
        logging.info("=========== calling Varroapop windows REST API")
        called_endpoint = (rest_url_varroapop + '/varroapop/run/')
        logging.info(called_endpoint)
        http_headers = {'Content-Type': 'application/json'}
        logging.info("JSON payload:")
        print(input_json)
        return requests.post(called_endpoint, headers=http_headers, data=input_json, timeout=60)


    def fill_model_out_attr(self, output_json):
        outputs = json.loads(json.loads(output_json)[0])
        self.out_date = self.out_date.append(pd.Series(outputs.get('Date')))
        self.out_colony_size = self.out_colony_size.append(pd.Series(outputs.get('Colony.Size')))
        self.out_adult_drones = self.out_adult_drones.append(pd.Series(outputs.get('Adult.Drones')))
        self.out_adult_workers = self.out_adult_workers.append(pd.Series(outputs.get('Adult.Workers')))
        self.out_foragers = self.out_foragers.append(pd.Series(outputs.get('Foragers')))
        self.out_capped_drone_brood = self.out_capped_drone_brood.append(pd.Series(outputs.get('Capped.Drone.Brood')))
        self.out_capped_worker_brood = self.out_capped_worker_brood.append(pd.Series(outputs.get('Capped.Worker.Brood')))
        self.out_drone_larvae = self.out_drone_larvae.append(pd.Series(outputs.get('Drone.Larvae')))
        self.out_worker_larvae =self.out_worker_larvae.append(pd.Series(outputs.get('Worker.Larvae')))
        self.out_drone_eggs = self.out_drone_eggs.append(pd.Series(outputs.get('Drone.Eggs')))
        self.out_worker_eggs = self.out_worker_eggs.append(pd.Series(outputs.get('Worker.Eggs')))
        self.out_free_mites = self.out_free_mites.append(pd.Series(outputs.get('Free.Mites')))
        self.out_drone_brood_mites =self.out_drone_brood_mites.append(pd.Series(outputs.get('Drone.Brood.Mites')))
        self.out_worker_brood_mites =self.out_worker_brood_mites.append(pd.Series(outputs.get('Worker.Brood.Mites')))
        self.out_drone_mites_per_cell = self.out_drone_mites_per_cell.append(pd.Series(outputs.get('Mites.Drone.Cell')))
        self.out_worker_mites_per_cell = self.out_worker_mites_per_cell.append(pd.Series(outputs.get('Mites.Worker.Cell')))
        self.out_mites_dying = self.out_mites_dying.append(pd.Series(outputs.get('Mites.Dying')))
        self.out_proportion_mites_dying =self.out_proportion_mites_dying.append(pd.Series(outputs.get('Proportion.Mites.Dying')))
        self.out_colony_pollen = self.out_colony_pollen.append(pd.Series(outputs.get('Colony.Pollen..g.')))
        self.out_chemical_conc_pollen =self.out_chemical_conc_pollen.append(pd.Series(outputs.get('Pollen.Pesticide.Concentration')))
        self.out_colony_nectar = self.out_colony_nectar.append(pd.Series(outputs.get('Colony.Nectar')))
        self.out_chemical_conc_nectar =self.out_chemical_conc_nectar.append(pd.Series(outputs.get('Nectar.Pesticide.Concentration')))
        self.out_dead_drone_larvae = self.out_dead_drone_larvae.append(pd.Series(outputs.get('Dead.Drone.Larvae')))
        self.out_dead_worker_larvae =self.out_dead_worker_larvae.append(pd.Series(outputs.get('Dead.Worker.Larvae')))
        self.out_dead_drone_adults = self.out_dead_drone_adults.append(pd.Series(outputs.get('Dead.Drone.Adults')))
        self.out_dead_worker_adults = self.out_dead_worker_adults.append(pd.Series(outputs.get('Dead.Worker.Adults')))
        self.out_dead_foragers = self.out_dead_foragers.append(pd.Series(outputs.get('Dead.Foragers')))
        self.out_queen_strength = self.out_queen_strength.append(pd.Series(outputs.get('Queen.Strength')))
        self.out_average_temp_c = self.out_average_temp_c.append(pd.Series(outputs.get('Average.Temperature..celsius.')))
        self.out_rain_inch = self.out_rain_inch.append(pd.Series(outputs.get('Rain')))


    def fill_summary_stats(self):
        self.out_mean_colony_size = self.out_mean_colony_size.append(pd.Series(self.out_colony_size.mean()))
        self.out_max_colony_size = self.out_max_colony_size.append(pd.Series(self.out_colony_size.max()))
        self.out_min_colony_size = self.out_min_colony_size.append(pd.Series(self.out_colony_size.min()))
        self.out_total_bee_mortality = self.out_total_bee_mortality.append(pd.Series(sum([self.out_dead_drone_adults.sum(),
                                                                                      self.out_dead_drone_larvae.sum(),
                                                                                      self.out_dead_worker_adults.sum(),
                                                                                      self.out_dead_worker_larvae.sum(),
                                                                                      self.out_dead_foragers.sum()])))
        self.out_max_chemical_conc_pollen = self.out_max_chemical_conc_pollen.append(pd.Series(self.out_chemical_conc_pollen.max()))
        self.out_max_chemical_conc_nectar = self.out_max_chemical_conc_nectar.append(pd.Series(self.out_chemical_conc_nectar.max()))


    def fill_sessionid(self, sessionid):
        self.out_api_sessionid = self.out_api_sessionid.append(pd.Series(sessionid))


    def format_varroapop_payload(self):
        input_dict = self.pd_obj.to_dict('records')[0]
        weather_loc = input_dict.pop('weather_location')
        print('Weather location: '+ weather_loc )
        input_dict = self.collapse_dates(input_dict)
        input_dict = self.rename_inputs(input_dict)
        input_dict = self.remove_unused_inputs(input_dict)
        data = json.dumps({'parameters':input_dict, 'weather_file':weather_loc})
        return data


    def collapse_dates(self, input_dict):
        sim_start_keys = ['SimStart_month', 'SimStart_day', 'SimStart_year']
        input_dict['SimStart'] = "/".join([str(int(input_dict.get(key))) for key in sim_start_keys])
        sim_end_keys = ['SimEnd_month', 'SimEnd_day', 'SimEnd_year']
        input_dict['SimEnd'] = "/".join([str(int(input_dict.get(key))) for key in sim_end_keys])
        requeen_date_keys = ['RQReQueenDate_month', 'RQReQueenDate_day', 'RQReQueenDate_year']
        input_dict['RQReQueenDate'] = "/".join([str(int(input_dict.get(key))) for key in requeen_date_keys])
        imm_start_keys = ['ImmStart_month', 'ImmStart_day', 'ImmStart_year']
        input_dict['ImmStart'] = "/".join([str(int(input_dict.get(key))) for key in imm_start_keys])
        imm_end_keys = ['ImmEnd_month', 'ImmEnd_day', 'ImmEnd_year']
        input_dict['ImmEnd'] = "/".join([str(int(input_dict.get(key))) for key in imm_end_keys])
        vt_treatment_start_keys = ['VTTreatmentStart_month', 'VTTreatmentStart_day', 'VTTreatmentStart_year']
        input_dict['VTTreatmentStart'] = "/".join([str(int(input_dict.get(key))) for key in vt_treatment_start_keys])
        foliar_app_date_keys = ['FoliarAppDate_month', 'FoliarAppDate_day', 'FoliarAppDate_year']
        input_dict['FoliarAppDate'] = "/".join([str(int(input_dict.get(key))) for key in foliar_app_date_keys])
        foliar_forage_begin_keys = ['FoliarForageBegin_month', 'FoliarForageBegin_day', 'FoliarForageBegin_year']
        input_dict['FoliarForageBegin'] = "/".join([str(int(input_dict.get(key))) for key in foliar_forage_begin_keys])
        foliar_forage_end_keys = ['FoliarForageEnd_month', 'FoliarForageEnd_day', 'FoliarForageEnd_year']
        input_dict['FoliarForageEnd'] = "/".join([str(int(input_dict.get(key))) for key in foliar_forage_end_keys])
        soil_forage_begin_keys = ['SoilForageBegin_month', 'SoilForageBegin_day', 'SoilForageBegin_year']
        input_dict['SoilForageBegin'] = "/".join([str(int(input_dict.get(key))) for key in soil_forage_begin_keys])
        soil_forage_end_keys = ['SoilForageEnd_month', 'SoilForageEnd_day', 'SoilForageEnd_year']
        input_dict['SoilForageEnd'] = "/".join([str(int(input_dict.get(key))) for key in soil_forage_end_keys])
        seed_forage_begin_keys = ['SeedForageBegin_month', 'SeedForageBegin_day', 'SeedForageBegin_year']
        input_dict['SeedForageBegin'] = "/".join([str(int(input_dict.get(key))) for key in seed_forage_begin_keys])
        seed_forage_end_keys = ['SeedForageEnd_month', 'SeedForageEnd_day', 'SeedForageEnd_year']
        input_dict['SeedForageEnd'] = "/".join([str(int(input_dict.get(key))) for key in seed_forage_end_keys])
        sup_pollen_begin_keys = ['SupPollenBegin_month', 'SupPollenBegin_day', 'SupPollenBegin_year']
        input_dict['SupPollenBegin'] = "/".join([str(int(input_dict.get(key))) for key in sup_pollen_begin_keys])
        sup_pollen_end_keys = ['SupPollenEnd_month', 'SupPollenEnd_day', 'SupPollenEnd_year']
        input_dict['SupPollenEnd'] = "/".join([str(int(input_dict.get(key))) for key in sup_pollen_end_keys])
        sup_nectar_begin_keys = ['SupNectarBegin_month', 'SupNectarBegin_day', 'SupNectarBegin_year']
        input_dict['SupNectarBegin'] = "/".join([str(int(input_dict.get(key))) for key in sup_nectar_begin_keys])
        sup_nectar_end_keys = ['SupNectarEnd_month', 'SupNectarEnd_day', 'SupNectarEnd_year']
        input_dict['SupNectarEnd'] = "/".join([str(int(input_dict.get(key))) for key in sup_nectar_end_keys])
        inputs_to_remove = sum([sim_start_keys,sim_end_keys,requeen_date_keys,imm_start_keys,
                                         imm_end_keys,vt_treatment_start_keys,foliar_app_date_keys,
                                         foliar_forage_begin_keys, foliar_forage_end_keys,soil_forage_begin_keys,
                                         soil_forage_end_keys, seed_forage_begin_keys, seed_forage_end_keys,
                                         sup_pollen_begin_keys, sup_pollen_end_keys, sup_nectar_begin_keys, sup_nectar_end_keys], [])
        [input_dict.pop(k, None) for k in inputs_to_remove]
        return input_dict


    def rename_inputs(self, input_dict):
        input_dict['EAppRate'] = input_dict.pop('ar_lb')
        input_dict['AIKOW'] = math.exp(input_dict.pop('l_kow'))
        input_dict['AIKOC'] = input_dict.pop('k_oc')
        return input_dict


    def remove_unused_inputs(self, input_dict):
        keys = list(input_dict.keys())
        to_remove = [i for i in keys if i[0].islower()]
        for k in to_remove:
         input_dict.pop(k, None)
        return input_dict


    def get_input_file(self, api_sessionid):
        file_endpoint = (rest_url_varroapop + '/varroapop/files/input/{}/'.format(api_sessionid))
        return requests.get(file_endpoint+'vp_input.txt')


    def get_log_file(self, api_sessionid):
        file_endpoint = (rest_url_varroapop + '/varroapop/files/logs/{}/'.format(api_sessionid))
        return requests.get(file_endpoint+'vp_log.txt')


    def get_results_file(self, api_sessionid):
        file_endpoint = (rest_url_varroapop + '/varroapop/files/output/{}/'.format(api_sessionid))
        return requests.get(file_endpoint+'vp_results.txt')




