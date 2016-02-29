from __future__ import division
import logging
import os.path
import pandas as pd
import sys
#find parent directory and import base (travis)
parentddir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
sys.path.append(parentddir)
from base.uber_model import UberModel, ModelSharedInputs

#print(sys.path)
#print(os.path)


class SipInputs(ModelSharedInputs):
    """
    Input class for SIP.
    """

    def __init__(self):
        """Class representing the inputs for SIP"""
        super(SipInputs, self).__init__()
        self.solubility = pd.Series([], dtype="float")
        self.bodyweight_tested_bird = pd.Series([], dtype="float")
        self.bodyweight_bird_other_1 = pd.Series([], dtype="float")
        self.bodyweight_bird_other_2 = pd.Series([], dtype="float")
        self.bodyweight_tested_mammal = pd.Series([], dtype="float")
        self.ld50_avian_water = pd.Series([], dtype="float")
        #self.ld50_species_tested_mammal = pd.Series([], dtype="object")
        self.noaec_quail = pd.Series([], dtype="float")
        self.noaec_duck = pd.Series([], dtype="float")
        self.noaec_bird_other_1 = pd.Series([], dtype="float")
        self.noaec_bird_other_2 = pd.Series([], dtype="float")
        self.noael_bodyweight_tested_mammal = pd.Series([], dtype="float")
        #self.noael_species_tested_mammal = pd.Series([], dtype="object")
        #self.species_tested_bird = pd.Series([], dtype="object")
        self.ld50_mammal_water = pd.Series([], dtype="float")
        self.noael_mammal_water = pd.Series([], dtype="float")
        self.mineau_scaling_factor = pd.Series([], dtype="float")


class SipOutputs(object):
    """
    Output class for SIP.
    """

    def __init__(self):
        """Class representing the outputs for SIP"""
        super(SipOutputs, self).__init__()
        self.fw_bird_out = pd.Series(name="fw_bird_out")
        self.fw_mamm_out = pd.Series(name="fw_mamm_out")
        self.dose_bird_out = pd.Series(name="dose_bird_out")
        self.dose_mamm_out = pd.Series(name="dose_mamm_out")
        self.at_bird_out = pd.Series(name="at_bird_out")
        self.at_mamm_out = pd.Series(name="at_mamm_out")
        self.fi_bird_out = pd.Series(name="fi_bird_out")
        self.det_out = pd.Series(name="det_out")
        self.act_out = pd.Series(name="act_out")
        self.acute_bird_out = pd.Series(name="acute_bird_out")
        self.acuconb_out = pd.Series(name="acuconb_out")
        self.acute_mamm_out = pd.Series(name="acute_mamm_out")
        self.acuconm_out = pd.Series(name="acuconm_out")
        self.chron_bird_out = pd.Series(name="chron_bird_out")
        self.chronconb_out = pd.Series(name="chronconb_out")
        self.chron_mamm_out = pd.Series(name="chron_mamm_out")
        self.chronconm_out = pd.Series(name="chronconm_out", dtype = object)
        self.det_quail = pd.Series(name="det_quail")
        self.det_duck = pd.Series(name="det_duck")
        self.det_other_1 = pd.Series(name="det_other_1")
        self.det_other_2 = pd.Series(name="det_other_2")


class Sip(UberModel, SipInputs, SipOutputs):
    """
    Estimate chemical exposure from drinking water alone in birds and mammals.
    """

    def __init__(self, pd_obj, pd_obj_exp):
        """Class representing the Terrplant model and containing all its methods"""
        super(Sip, self).__init__()
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        self.pd_obj_out = None

        # Class member variables that are not user inputs
        self.bodyweight_assessed_bird = 20.
        self.bodyweight_assessed_mammal = 1000.

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
        """ Execute all algorithm methods for model logic """
        try:
            self.fw_bird()
            self.fw_mamm()
            self.dose_bird()
            self.dose_mamm()
            self.at_bird()
            self.at_mamm()
            self.det()
            self.act()
            self.acute_bird()
            self.acuconb()
            self.acute_mamm()
            self.acuconm()
            self.chron_bird()
            self.chronconb()
            self.chron_mamm()
            self.chronconm()
        except TypeError:
            print "Type Error: Your variables are not set correctly."

    # Begin model methods
    def fw_bird(self):
        """
        For birds, the daily water intake rate is calculated using the equation below.
        This equation is representative of passerine birds, which represent the majority
        of bird species visiting agricultural areas and which have higher daily water flux
        requirements than other birds.  As a result, the equations represent the most
        conservative estimate of pesticide concentrations in water. The resulting daily
        water intake rate for the 20 g bird is 0.0162 L.

            Flux(water) = (1.180 * BW^0.874) / 1000

            where: BW = 20 g
        """
        """
        Using fixed value to correctly handle floating point decimals as compared to spreadsheet implementation
        """
        self.fw_bird_out = 0.0162
        return self.fw_bird_out

    # Daily water intake rate for mammals
    def fw_mamm(self):
        """
        For mammals, the daily water intake rate is calculated using the equation below.
        This equation is representative of eutherian herbivore mammals, which have higher
        daily water flux requirements compared to other mammals that visit agricultural areas.
        The only equation that would generate higher estimates of daily water flux corresponds
        to marsupial carnivores, which are not considered to be representative of the majority
        of mammals that visit agricultural areas.  The resulting daily water intake rate for a
        1000 g mammal is 0.172 L.

            Flux(water) = (0.708 * BW^0.795) / 1000

            where: BW = 1000 g
        """
        """
        Using fixed value to correctly handle floating point decimals as compared to spreadsheet implementation
        """
        self.fw_mamm_out = 0.172
        return self.fw_mamm_out

    # Upper bound estimate of exposure for birds
    def dose_bird(self):
        """
        The model calculates the upper bound estimate of exposure in drinking water
        (dose-based; units in mg/kg-bw) by multiplying the daily water intake rate (L)
        by the chemical solubility (mg/L) and then dividing by the body weight (in kg)
        of the assessed animal (See equation below). In cases where water characteristics
        (e.g., pH) influence the solubility of a chemical in water, the user should select
        the highest available water solubility for use in SIP.

            Dose = (Flux(water) * solubility) / BW

            where: BW = body weight (kg) of the assessed bird (e.g. mallard duck, bobtail quail, other)
        """
        self.dose_bird_out = (self.fw_bird_out * self.solubility) / (self.bodyweight_assessed_bird / 1000.)
        return self.dose_bird_out

    # Upper bound estimate of exposure for mammals
    def dose_mamm(self):
        """
        The model calculates the upper bound estimate of exposure in drinking water
        (dose-based; units in mg/kg-bw) by multiplying the daily water intake rate (L)
        by the chemical solubility (mg/L) and then dividing by the body weight (in kg)
        of the assessed animal (See equation below). In cases where water characteristics
        (e.g., pH) influence the solubility of a chemical in water, the user should select
        the highest available water solubility for use in SIP.

            Dose = (Flux(water) * solubility) / BW

            where: BW = body weight (kg) of the assessed animal (e.g. laboratory rat, other)
        """
        self.dose_mamm_out = (self.fw_mamm_out * self.solubility) / (self.bodyweight_assessed_mammal / 1000.)
        return self.dose_mamm_out

    # Acute adjusted toxicity value for birds
    def at_bird(self):
        """
        LD50 values for mammals and birds are adjusted using the same approach employed
        by T-REX (USEPA 2008). These equations are provided below. In these equations,
        AT = adjusted toxicity value (mg/kg-bw); LD50 = endpoint reported by toxicity study
        (mg/kg-bw); TW = body weight of tested animal (350g rat, 1580g mallard duck, 178 g
        Northern bobwhite quail or weight defined by the model user for an alternative species);

        AT = LD50* (AW / TW)^(x-1)

        where:
            AW = body weight of assessed animal (g)
            x = Mineau scaling factor.  Chemical specific values for x may be located in the
            worksheet titled "Mineau scaling factors." If no chemical specific data are available,
            the default value of 1.15 should be used for this parameter.
        """
        self.at_bird_out = self.ld50_avian_water * (
            (self.bodyweight_assessed_bird / self.bodyweight_tested_bird) ** (self.mineau_scaling_factor - 1.))
        return self.at_bird_out

    # Acute adjusted toxicity value for mammals
    def at_mamm(self):
        """
        LD50 values for mammals and birds are adjusted using the same approach employed
        by T-REX (USEPA 2008). These equations are provided below. In these equations,
        AT = adjusted toxicity value (mg/kg-bw); LD50 = endpoint reported by toxicity study
        (mg/kg-bw); TW = body weight of tested animal (350g rat, 1580g mallard duck, 178 g
        Northern bobwhite quail or weight defined by the model user for an alternative species);

        AT = LD50* (TW / AW)^0.25

        where:
            AW = body weight of assessed animal (g)
            x = Mineau scaling factor.  Chemical specific values for x may be located in the
            worksheet titled "Mineau scaling factors." If no chemical specific data are available,
            the default value of 1.15 should be used for this parameter.
        """
        self.at_mamm_out = self.ld50_mammal_water * (
            (self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal) ** 0.25)
        return self.at_mamm_out

    # Adjusted chronic toxicity values for birds
    # FI = Food Intake Rate
    def fi_bird(self, bw_grams):
        """
        Daily Food Intake Rate:

        Chronic avian toxicity studies produce endpoints based on concentration in food, not dose.
        The endpoint is a No Observed Adverse Effects Concentration (NOAEC) that is assumed to be
        relevant to all birds, regardless of body weight.  In order to convert a reported avian
        NOAEC (mg/kg-diet) value to a dose equivalent toxicity value for the assessed animal,
        the daily food (dry) intake of the test bird is considered. The daily food intake rate
        (FI; units in kg-food) of the test bird is calculated using the equation below.

        FI = 0.0582 * BW^0.651

        where:
            BW = body weight in kg (USEPA 1993). This equation corresponds to a daily food intake
            rate for all birds, which generates a lower food intake rate compared to passerines.
            The equation is more conservative because it results in a lower dose-equivalent toxicity value.
        """
        self.fi_bird_out = 0.0582 * ((bw_grams / 1000.) ** 0.651)
        return self.fi_bird_out

    # Dose-equivalent chronic toxicity value for birds
    def det(self):
        """
        Dose Equiv. Toxicity:

        The FI value (kg-diet) is multiplied by the reported NOAEC (mg/kg-diet) and then divided by
        the test animal's body weight to derive the dose-equivalent chronic toxicity value (mg/kg-bw):

        Dose Equiv. Toxicity = (NOAEC * FI) / BW

        NOTE: The user enters the lowest available NOAEC for the mallard duck, for the bobwhite quail,
        and for any other test species. The model calculates the dose equivalent toxicity values for
        all of the modeled values (Cells F20-24 and results worksheet) and then selects the lowest dose
        equivalent toxicity value to represent the chronic toxicity of the chemical to birds.
        """
        try:
            # Body weight of bobtail quail is 178 g
            self.det_quail = (self.noaec_quail * self.fi_bird(178.)) / (178. / 1000.)
        except Exception as e:
            print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)
            # TODO: vectorize
            self.det_quail = None

        try:
            # Body weight of mallard duck is 1580 g
            self.det_duck = (self.noaec_duck * self.fi_bird(1580.)) / (1580. / 1000.)
        except Exception as e:
            print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)
            # TODO: vectorize
            self.det_duck = None

        try:
            self.det_other_1 = (self.noaec_bird_other_1 * self.fi_bird(self.bodyweight_bird_other_1)) / (
                self.bodyweight_bird_other_1 / 1000.)
        except Exception as e:
            print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)
            # TODO: Vectorize
            self.det_other_1 = None

        try:
            self.det_other_2 = (self.noaec_bird_other_2 * self.fi_bird(self.bodyweight_bird_other_2)) / (
                self.bodyweight_bird_other_2 / 1000.)
        except Exception as e:
            print "Error '{0}' occured. Arguments {1}.".format(e.message, e.args)
            # TODO: vectorize
            self.det_other_2 = None

        # Create DataFrame containing method Series created above
        df_noaec = pd.DataFrame({
            'det_quail': self.det_quail,
            'det_duck': self.det_duck,
            'det_other_1': self.det_other_1,
            'det_other_2': self.det_other_2
        })

        # Create a Series of the minimum values for each row/model run of the above DataFrame
        self.det_out = df_noaec.min(axis=1, numeric_only=True)

        return self.det_out

    # Adjusted chronic toxicty value for mammals
    def act(self):
        """
        SIP relies upon the No Observed Adverse Effects Level (NOAEL; mg/kg-bw) from a chronic mammalian study.
        If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC by 20 to
        determine the equivalent chronic daily dose. This approach is consistent with that of T-REX, which
        relies upon the standard FDA lab rat conversion. (USEPA 2008). Mammalian NOAEL values are adjusted
        using the same approach employed by T-REX (USEPA 2008). The equation for mammals is provided below
        (variables are defined above).

        AT = NOAEL * (TW / AW)^0.25
        """
        self.act_out = self.noael_mammal_water * (
            (self.bodyweight_tested_mammal / self.bodyweight_assessed_mammal) ** 0.25)

        # MAMMILIAN:  If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC
        # by 20 to determine the equivalent chronic daily dose (NOAEL)

        return self.act_out

    # Acute exposures for birds
    def acute_bird(self):
        """
        For acute exposures, if the ratio of the upper bound dose to the adjusted LD50 value is <0.1,
        the risk assessor can conclude that pesticide exposure to mammals or birds through drinking
        water by itself is not an exposure route of concern. If the ratio of the upper bound dose to
        the adjusted LD50 value is  >=0.1, the risk assessor can conclude that pesticide exposure to
        mammals or birds through drinking water by itself is an exposure route of concern.
        """
        self.acute_bird_out = self.dose_bird_out / self.at_bird_out
        return self.acute_bird_out

    def acuconb(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for birds'
        msg_fail = 'Exposure through drinking water alone is a potential concern for birds'
        boo_ratios = [ratio < 0.1 for ratio in self.acute_bird_out]
        self.acuconb_out = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #boolean = self.acute_bird_out < 0.1
        #self.acuconb_out = boolean.map(lambda x:
        #                               'Drinking water exposure alone is NOT a potential concern for birds'
        #                               if x is True else
        #                               'Exposure through drinking water alone is a potential concern for birds')
        return self.acuconb_out

    # Acute exposures for mammals
    def acute_mamm(self):
        """
        For acute exposures, if the ratio of the upper bound dose to the adjusted LD50 value is <0.1,
        the risk assessor can conclude that pesticide exposure to mammals or birds through drinking
        water by itself is not an exposure route of concern. If the ratio of the upper bound dose to
        the adjusted LD50 value is >=0.1, the risk assessor can conclude that pesticide exposure to
        mammals or birds through drinking water by itself is an exposure route of concern.
        """
        self.acute_mamm_out = self.dose_mamm_out / self.at_mamm_out
        return self.acute_mamm_out

    def acuconm(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for mammals'
        msg_fail = 'Exposure through drinking water alone is a potential concern for mammals'
        boo_ratios = [ratio < 0.1 for ratio in self.acute_mamm_out]
        self.acuconm_out = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        return self.acuconm_out

    # Chronic Exposures for birds
    def chron_bird(self):
        """
        For chronic exposures, if the ratio of the upper bound dose to the adjusted chronic
        toxicity value is <1, the risk assessor can conclude that pesticide exposure to mammals
        or birds through drinking water by itself is not an exposure route of concern. If the
        ratio of the upper bound dose to the adjusted chronic toxicity value is >=1, the risk
        assessor can conclude that pesticide exposure to mammals or birds through drinking water
        by itself is an exposure route of concern.
        """
        self.chron_bird_out = self.dose_bird_out / self.det_out
        return self.chron_bird_out

    def chronconb(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for birds'
        msg_fail = 'Exposure through drinking water alone is a potential concern for birds'
        boo_ratios = [ratio < 1 for ratio in self.chron_bird_out]
        self.chronconb_out = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        return self.chronconb_out

    # Chronic exposures for mammals
    def chron_mamm(self):
        """
        For chronic exposures, if the ratio of the upper bound dose to the adjusted chronic
        toxicity value is <1, the risk assessor can conclude that pesticide exposure to mammals
        or birds through drinking water by itself is not an exposure route of concern. If the
        ratio of the upper bound dose to the adjusted chronic toxicity value is >=1, the risk
        assessor can conclude that pesticide exposure to mammals or birds through drinking water
        by itself is an exposure route of concern.
        """
        self.chron_mamm_out = self.dose_mamm_out / self.act_out
        return self.chron_mamm_out

    def chronconm(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for mammals'
        msg_fail = 'Exposure through drinking water alone is a potential concern for mammals'
        boo_ratios = [ratio < 1 for ratio in self.chron_mamm_out]
        self.chronconm_out = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        return self.chronconm_out
