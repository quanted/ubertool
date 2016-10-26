import importlib
import pandas as pd
from pandas import compat
import logging


class UberModel(object):
    """
    Collection of static methods used across all the ubertool models.
    """

    def __init__(self):
        """Main utility class for building Ubertool model classes for model execution."""
        super(UberModel, self).__init__()
        self.name = self.__class__.__name__
        self.pd_obj = None
        self.pd_obj_exp = None
        self.pd_obj_out = None

    def populate_inputs(self, pd_obj, model_obj):
        """
        Validate and assign user-provided model inputs to their respective class attributes
        :param pd_obj: Pandas DataFrame object of model input parameters
        :param model_obj:
        """
        try:
            # Import the model's input class (e.g. TerrplantInputs) to compare user supplied inputs to
            mod_name = model_obj.name.lower() + '.' + model_obj.name.lower() + '_exe'
            module = importlib.import_module(mod_name)
            model_inputs = getattr(module, model_obj.name + "Inputs")
            model_inputs_obj = model_inputs()
        except ValueError as err:
            logging.info(mod_name)
            logging.info(err.args)

        # Create temporary DataFrame where each column name is the same as ModelInputs attributes
        df = pd.DataFrame()
        for input_param in model_inputs_obj.__dict__:
            df[input_param] = getattr(self, input_param)

        # Compare column names of temporary DataFrame (created above) to user-supply DataFrame from JSON
        if df.columns.sort_values().equals(pd_obj.columns.sort_values()):
            # If the user-supplied DataFrame has the same column names as required by TRexInputs...
            # set each Series in the DataFrame to the corresponding TRexInputs attribute (member variable)
            for column in pd_obj.columns:
                setattr(model_obj, column, pd_obj[column])
        else:
            msg_err1 = "Inputs parameters do not have all required inputs. Please see API documentation.\n"
            msg_err2 = "Expected: " + str(df.columns.sort_values()) + "\n"
            msg_err3 = "Received: " + str(pd_obj.columns.sort_values()) + "\n"
            raise ValueError(msg_err1 + msg_err2 + msg_err3)

    def populate_outputs(self, model_obj):
        # Create temporary DataFrame where each column name is the same as TRexOutputs attributes
        """
        Create and return Model Output DataFrame where each column name is a model output parameter
        :param model: string, name of the model as referred to in class names (e.g. terrplant, sip, stir, etc..)
        :param model_obj: class instance, instance of the model class for which the
        :return:
        """
        # Import the model's output class (e.g. TerrplantOutputs) to create a DF to store the model outputs in
        mod_name = model_obj.name.lower() + '.' + model_obj.name.lower() + '_exe'
        module = importlib.import_module(mod_name)
        model_outputs = getattr(module, model_obj.name + "Outputs")
        model_outputs_obj = model_outputs()
        df = pd.DataFrame()
        for input_param in model_outputs_obj.__dict__:
            df[input_param] = getattr(self, input_param)
            setattr(model_obj, input_param, df[input_param])
        return df

    def fill_output_dataframe(self, model_obj):
        """ Combine all output properties into numpy pandas dataframe """
        for column in model_obj.pd_obj_out:
            try:
                model_obj.pd_obj_out[column] = getattr(model_obj, column)
            except:
                print("output dataframe error on " + column)

    def get_dict_rep(self, model_obj):
        """
        Convert DataFrames to dictionary, returning a tuple (inputs, outputs, exp_out)
        :param model_obj: model instance
        :return: (dict(input DataFrame), dict(outputs DataFrame), dict(expected outputs DataFrame))
        """
        try:
            return self.to_dict(model_obj.pd_obj), \
                   self.to_dict(model_obj.pd_obj_out), \
                   self.to_dict(model_obj.pd_obj_exp)
        except AttributeError:
            return self.to_dict(model_obj.pd_obj), \
                   self.to_dict(model_obj.pd_obj_out), \
                   {}

    @staticmethod
    def to_dict(df):
        """
        This is an override of the the pd.DataFrame.to_dict() method where the keys in
        return dictionary are cast to strings. This fixes an error where duck typing would
        sometimes allow non-String keys, which fails when Flask serializes the dictionary to
        JSON string to return the HTTP response.

        Original method returns: dict((str(k), v.to_dict()) for k, v in compat.iteritems(df))
        :param df:
        :return:
        """
        out = {}
        for k, v in compat.iteritems(df):
            col = k
            for row, value in compat.iteritems(v):
                out[col] = {str(row): value}
        return out


class ModelSharedInputs(object):
    def __init__(self):
        """
        Container for the shared model inputs amongst most models (e.g. version, chemical name, & PC Code)
        """
        super(ModelSharedInputs, self).__init__()
        self.version = pd.Series([], dtype="object")
        self.chemical_name = pd.Series([], dtype="object")
        self.pc_code = pd.Series([], dtype="object")
