from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import logging
import json
import requests
import math

#rest_url_varroapop = os.environ['REST_SERVER_8']
rest_url_varroapop = 'http://localhost:5656'


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
        called_endpoint = (rest_url_varroapop + '/ocpu/apps/quanted/VarroaPopWrapper/R/RunVarroaPop/json')
        logging.info(called_endpoint)
        http_headers = {'Content-Type': 'application/json'}
        logging.info("JSON payload:")
        print(input_json)
        return requests.post(called_endpoint, headers=http_headers, data=input_json, timeout=60)

    def format_varroapop_payload(self):
        input_dict = self.pd_obj.to_dict('records')[0]
        input_dict = self.collapse_dates(input_dict)
        input_dict = self.rename_inputs(input_dict)
        input_dict = self.remove_unused_inputs(input_dict)
        data = json.dumps({'parameters':input_dict})
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


