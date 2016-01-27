from flask_restful import Resource
import terrplant
from flask import request
import pandas as pd


class TerrplantHandler(Resource):
    def get(self, jid):
        return {'result': 'model=terrplant, jid=%s' % jid}

    def post(self, jid):
        pd_obj = pd.DataFrame.from_dict(request.json["inputs"], dtype='float64')
        terrplant = terrplant.Terrplant(pd_obj, None)
        terrplant.execute_model()
        inputs_json, outputs_json, exp_out_json = terrplant.get_dict_rep(terrplant)

        return {
            'user_id': 'admin',
            'inputs': inputs_json,
            'outputs': outputs_json,
            'exp_out': exp_out_json,
            '_id': jid,
            'run_type': "single"
        }

    @staticmethod
    def get_model_inputs():
        return terrplant.TerrplantInputs()

    @staticmethod
    def get_model_outputs():
        return terrplant.TerrplantOutputs()