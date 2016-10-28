import importlib
import pandas as pd
from pandas import compat
from parser import Parser
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

    def _validate(self, model_inputs, user_inputs):
        """
        Compare the user supplied inputs with the ModelInputs() class attributes, ensuring they match by name

        :param model_inputs: ModelInputs() class instance
        :return: Boolean
        """
        # Create temporary DataFrame where each column name is the same as ModelInputs attributes
        df = pd.DataFrame()
        for input_param in model_inputs.__dict__:
            df[input_param] = getattr(self, input_param)

        # Compare column names of temporary DataFrame (created above) to user-supply DataFrame from JSON
        if df.columns.sort_values().equals(user_inputs.columns.sort_values()):
            return True
        else:
            msg_err1 = "Inputs parameters do not have all required inputs. Please see API documentation.\n"
            msg_err2 = "Expected: " + str(df.columns.sort_values()) + "\n"
            msg_err3 = "Received: " + str(user_inputs.columns.sort_values()) + "\n"
            raise ValueError(msg_err1 + msg_err2 + msg_err3)

    @staticmethod
    def _convert_index(df_in):
        """ Attempt to covert indices of input DataFrame to duck typed dtype """
        parser = Parser(df_in)
        df = parser.convert_axes()
        return df

    def populate_inputs(self, df_in):
        """
        Validate and assign user-provided model inputs to their respective class attributes
        :param df_in: Pandas DataFrame object of model input parameters
        """
        df = self._convert_index(df_in)
        try:
            # Import the model's input class (e.g. TerrplantInputs) to compare user supplied inputs to
            mod_name = self.name.lower() + '.' + self.name.lower() + '_exe'
            module = importlib.import_module(mod_name)
            model_inputs_class = getattr(module, self.name + "Inputs")
            model_inputs = model_inputs_class()
        except ValueError as err:
            logging.info(mod_name)
            logging.info(err.args)

        if self._validate(model_inputs, df):
            # If the user-supplied DataFrame has the same column names as required by TRexInputs...
            # set each Series in the DataFrame to the corresponding TRexInputs attribute (member variable)
            # user_inputs_df = self._sanitize(df)
            for column in df.columns:
                setattr(self, column, df[column])

    def populate_outputs(self):
        # Create temporary DataFrame where each column name is the same as TRexOutputs attributes
        """
        Create and return Model Output DataFrame where each column name is a model output parameter
        :param model: string, name of the model as referred to in class names (e.g. terrplant, sip, stir, etc..)
        :param model_obj: class instance, instance of the model class for which the
        :return:
        """
        # Import the model's output class (e.g. TerrplantOutputs) to create a DF to store the model outputs in
        mod_name = self.name.lower() + '.' + self.name.lower() + '_exe'
        module = importlib.import_module(mod_name)
        model_outputs = getattr(module, self.name + "Outputs")
        model_outputs_obj = model_outputs()
        df = pd.DataFrame()
        for input_param in model_outputs_obj.__dict__:
            df[input_param] = getattr(self, input_param)
            setattr(self, input_param, df[input_param])
        return df

    def fill_output_dataframe(self):
        """ Combine all output properties into Pandas Dataframe """
        for column in self.pd_obj_out.columns:
            try:
                output = getattr(self, column)
                if isinstance(output, pd.Series):
                    # Ensure model output is a Pandas Series. Only Series can be
                    # reliably put into a Pandas DataFrame.
                    self.pd_obj_out[column] = output
                else:
                    print('"{}" is not a Pandas Series. Returned outputs must be a Pandas Series'.format(column))

            except:
                print("output dataframe error on " + column)

    def get_dict_rep(self):
        """
        Convert DataFrames to dictionary, returning a tuple (inputs, outputs, exp_out)
        :param model_obj: model instance
        :return: (dict(input DataFrame), dict(outputs DataFrame), dict(expected outputs DataFrame))
        """
        try:
            return self.to_dict(self.pd_obj), \
                   self.to_dict(self.pd_obj_out), \
                   self.to_dict(self.pd_obj_exp)
        except AttributeError:
            return self.to_dict(self.pd_obj), \
                   self.to_dict(self.pd_obj_out), \
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
