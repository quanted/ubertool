from __future__ import division  #brings in Python 3.0 mixed type calculation rules
import logging
import numpy as np
import pandas as pd

class SipFunctions(object):
    """
    Function class for Sip.
    """

    def __init__(self):
        """Class representing the functions for Sip"""
        super(SipFunctions, self).__init__()

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
        fw_bird = 0.0162
        self.out_fw_bird = pd.Series([fw_bird for x in range(self.no_of_runs)])
        return self.out_fw_bird

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
        fw_mamm = 0.172
        self.out_fw_mamm = pd.Series([fw_mamm for x in range(self.no_of_runs)])
        return self.out_fw_mamm

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
        conv = 1000.0
        self.out_dose_bird = (self.out_fw_bird * self.solubility) / (self.bodyweight_assessed_bird / conv)
        return self.out_dose_bird

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
        conv = 1000.0
        self.out_dose_mamm = (self.out_fw_mamm * self.solubility) / (self.bodyweight_assessed_mammal / conv)
        return self.out_dose_mamm

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
        self.out_at_bird = self.ld50_avian_water * (
            (self.bodyweight_assessed_bird / self.ld50_bodyweight_tested_bird) ** (self.mineau_scaling_factor - 1.))
        return self.out_at_bird

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
        self.out_at_mamm = self.ld50_mammal_water * (
            (self.ld50_bodyweight_tested_mammal / self.bodyweight_assessed_mammal) ** 0.25)
        return self.out_at_mamm

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
        #bw_grams is the bodyweight of test bird (it's a series with a value per model simulation run)
        fi_bird = 0.0582 * ((bw_grams / 1000.) ** 0.651)
        return fi_bird

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
            # Body weight of bobtail quail is 178 g (assigned across all model simulation runs)
            bw_quail_series = pd.Series([self.bodyweight_bobwhite_quail for x in range(self.no_of_runs)])
            self.out_det_quail = (self.noaec_quail * self.fi_bird(bw_quail_series)) / (bw_quail_series / 1000.)
        except Exception:
            pass
        try:
            # Body weight of mallard duck is 1580 g (assigned across all model simulation runs)
            bw_duck_series = pd.Series([self.bodyweight_mallard_duck for x in range(self.no_of_runs)])
            self.out_det_duck = (self.noaec_duck * self.fi_bird(bw_duck_series)) / (bw_duck_series / 1000.)
        except Exception:
            pass

        try:
            self.out_det_other_1 = (self.noaec_bird_other_1 * self.fi_bird(self.noaec_bodyweight_bird_other_1)) / (
                self.noaec_bodyweight_bird_other_1 / 1000.)
        except Exception:
            pass
            # self.out_det_other_1 = pd.Series(None, list(range(self.chemical_name.size)))

        try:
            self.out_det_other_2 = (self.noaec_bird_other_2 * self.fi_bird(self.noaec_bodyweight_bird_other_2)) / (
                self.noaec_bodyweight_bird_other_2 / 1000.)
        except Exception:
            pass
            # self.out_det_other_2 = pd.Series(None, list(range(self.chemical_name.size)))

        # Create DataFrame containing method Series created above
        df_noaec = pd.DataFrame({
            'out_det_quail': self.out_det_quail,
            'out_det_duck': self.out_det_duck,
            'out_det_other_1': self.out_det_other_1,
            'out_det_other_2': self.out_det_other_2
        })

        # Create a Series of the minimum values for each row/model run of the above DataFrame
        self.out_det = df_noaec.min(axis=1, numeric_only=True)

        return self.out_det

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
        self.out_act = self.noael_mammal_water * (
            (self.noael_bodyweight_tested_mammal / self.bodyweight_assessed_mammal) ** 0.25)

        # MAMMILIAN:  If only a NOAEC value (in mg/kg-diet) is available, the model user should divide the NOAEC
        # by 20 to determine the equivalent chronic daily dose (NOAEL)

        return self.out_act

    # Acute exposures for birds
    def acute_bird(self):
        """
        For acute exposures, if the ratio of the upper bound dose to the adjusted LD50 value is <0.1,
        the risk assessor can conclude that pesticide exposure to mammals or birds through drinking
        water by itself is not an exposure route of concern. If the ratio of the upper bound dose to
        the adjusted LD50 value is  >=0.1, the risk assessor can conclude that pesticide exposure to
        mammals or birds through drinking water by itself is an exposure route of concern.
        """
        self.out_acute_bird = self.out_dose_bird / self.out_at_bird
        return self.out_acute_bird

    def acuconb(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for birds'
        msg_fail = 'Exposure through drinking water alone is a potential concern for birds'
        boo_ratios = [ratio < 0.1 for ratio in self.out_acute_bird]
        self.out_acuconb = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        #boolean = self.out_acute_bird < 0.1
        #self.out_acuconb = boolean.map(lambda x:
        #                               'Drinking water exposure alone is NOT a potential concern for birds'
        #                               if x is True else
        #                               'Exposure through drinking water alone is a potential concern for birds')
        return self.out_acuconb

    # Acute exposures for mammals
    def acute_mamm(self):
        """
        For acute exposures, if the ratio of the upper bound dose to the adjusted LD50 value is <0.1,
        the risk assessor can conclude that pesticide exposure to mammals or birds through drinking
        water by itself is not an exposure route of concern. If the ratio of the upper bound dose to
        the adjusted LD50 value is >=0.1, the risk assessor can conclude that pesticide exposure to
        mammals or birds through drinking water by itself is an exposure route of concern.
        """
        self.out_acute_mamm = self.out_dose_mamm / self.out_at_mamm
        return self.out_acute_mamm

    def acuconm(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for mammals'
        msg_fail = 'Exposure through drinking water alone is a potential concern for mammals'
        boo_ratios = [ratio < 0.1 for ratio in self.out_acute_mamm]
        self.out_acuconm = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        return self.out_acuconm

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
        self.out_chron_bird = self.out_dose_bird / self.out_det
        return self.out_chron_bird

    def chronconb(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for birds'
        msg_fail = 'Exposure through drinking water alone is a potential concern for birds'
        boo_ratios = [ratio < 1 for ratio in self.out_chron_bird]
        self.out_chronconb = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        return self.out_chronconb

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
        self.out_chron_mamm = self.out_dose_mamm / self.out_act
        return self.out_chron_mamm

    def chronconm(self):
        """
        Message stating whether or not a risk is present
        """
        msg_pass = 'Drinking water exposure alone is NOT a potential concern for mammals'
        msg_fail = 'Exposure through drinking water alone is a potential concern for mammals'
        boo_ratios = [ratio < 1 for ratio in self.out_chron_mamm]
        self.out_chronconm = pd.Series([msg_pass if boo else msg_fail for boo in boo_ratios])
        return self.out_chronconm
