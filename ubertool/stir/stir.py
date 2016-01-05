from __future__ import division
#import logging
import pandas as pd
import sys


class Stir(object):
    """
    Estimate inhalation risk of chemicals to birds and mammals.
    """
    def __init__(self, run_type, pd_obj, pd_obj_exp):
        """  Constructor """
        # run_type can be single, batch or qaqc
        # 0 to run calculation, else it wont
        self.run_type = run_type
        self.pd_obj = pd_obj
        self.pd_obj_exp = pd_obj_exp
        # Execute model methods if requested
        if self.run_type != "empty":
            self.execute_model()

    def execute_model(self):
        """ Called by constructor to populate class and run methods. """
        self.populate_input_properties()
        self.create_output_properties()
        self.run_methods()
        self.create_output_dataframe()
        # Callable from Bottle that returns JSON
        self.json = self.json(self.pd_obj, self.pd_obj_out, self.pd_obj_exp)

    def populate_input_properties(self):
        """ Set all input properties for class """
        # Inputs: Assign object attribute variables from the input Pandas DataFrame
        self.chemical_name = self.pd_obj["chemical_name"]
        self.application_rate = self.pd_obj["application_rate"]
        self.column_height = self.pd_obj["column_height"]
        self.spray_drift_fraction = self.pd_obj["spray_drift_fraction"]
        self.direct_spray_duration = self.pd_obj["direct_spray_duration"]
        self.molecular_weight = self.pd_obj["molecular_weight"]
        self.vapor_pressure = self.pd_obj["vapor_pressure"]
        self.avian_oral_ld50 = self.pd_obj["avian_oral_ld50"]
        self.body_weight_assessed_bird = self.pd_obj["body_weight_assessed_bird"]
        self.body_weight_tested_bird = self.pd_obj["body_weight_tested_bird"]
        self.mineau_scaling_factor = self.pd_obj["mineau_scaling_factor"]
        self.mammal_inhalation_lc50 = self.pd_obj["mammal_inhalation_lc50"]
        self.duration_mammal_inhalation_study = self.pd_obj["duration_mammal_inhalation_study"]
        self.body_weight_assessed_mammal = self.pd_obj["body_weight_assessed_mammal"]
        self.body_weight_tested_mammal = self.pd_obj["body_weight_tested_mammal"]
        self.mammal_oral_ld50 = self.pd_obj["mammal_oral_ld50"]

    def create_output_properties(self):
        """ Set all output properties for class """
        # Outputs: Assign object attribute variables to Pandas Series
        self.sat_air_conc = pd.Series(name="sat_air_conc")
        self.inh_rate_avian = pd.Series(name="inh_rate_avian")
        self.vid_avian = pd.Series(name="vid_avian")
        self.inh_rate_mammal = pd.Series(name="inh_rate_mammal")
        self.vid_mammal = pd.Series(name="vid_mammal")
        self.ar2 = pd.Series(name="ar2")
        self.air_conc = pd.Series(name="air_conc")
        self.sid_avian = pd.Series(name="sid_avian")
        self.sid_mammal = pd.Series(name="sid_mammal")
        self.cf = pd.Series(name="cf")
        self.mammal_inhalation_ld50 = pd.Series(name="mammal_inhalation_ld50")
        self.adjusted_mammal_inhalation_ld50 = pd.Series(name="adjusted_mammal_inhalation_ld50")
        self.estimated_avian_inhalation_ld50 = pd.Series(name="estimated_avian_inhalation_ld50")
        self.adjusted_avian_inhalation_ld50 = pd.Series(name="adjusted_avian_inhalation_ld50")
        self.ratio_vid_avian = pd.Series(name="ratio_vid_avian")
        self.ratio_sid_avian = pd.Series(name="ratio_sid_avian")
        self.ratio_vid_mammal = pd.Series(name="ratio_vid_mammal")
        self.ratio_sid_mammal = pd.Series(name="ratio_sid_mammal")
        self.loc_vid_avian = pd.Series(name="loc_vid_avian")
        self.loc_sid_avian = pd.Series(name="loc_sid_avian")
        self.loc_vid_mammal = pd.Series(name="loc_vid_mammal")
        self.loc_sid_mammal = pd.Series(name="loc_sid_mammal")

    def run_methods(self):
        """ Execute all algorithm methods for model logic """
        try:
            self.calc_sat_air_conc()  # eq. 1
            self.calc_inh_rate_avian()  # eq. 2
            self.calc_vid_avian()  # eq. 3
            self.calc_inh_rate_mammal()  # eq. 4
            self.calc_vid_mammal()  # eq. 5
            self.calc_conc_air()  # eq. 6
            self.calc_sid_avian()  # eq. 7
            self.calc_sid_mammal()  # eq. 8
            self.calc_convert_mammal_inhalation_lc50_to_ld50()  # eq. 9
            self.calc_adjusted_mammal_inhalation_ld50()  # eq. 10
            self.calc_estimated_avian_inhalation_ld50()  # eq. 11
            self.calc_adjusted_avian_inhalation_ld50()  # eq. 12
            self.return_ratio_vid_avian()  # results #1
            self.return_loc_vid_avian()  # results #2
            self.return_ratio_sid_avian()  # results #3
            self.return_loc_sid_avian()  # results #4
            self.return_ratio_vid_mammal()  # results #5
            self.return_loc_vid_mammal()  # results #6
            self.return_ratio_sid_mammal()  # results #7
            self.return_loc_sid_mammal()  # results #8
        except:
            print "run_methods error:", sys.exc_info()[0]

    def create_output_dataframe(self):
        """ Combine all output properties into numpy pandas dataframe """
        # Create DataFrame containing output value Series
        pd_obj_out = pd.DataFrame(
            dict(sat_air_conc=self.sat_air_conc,
                 inh_rate_avian=self.inh_rate_avian,
                 vid_avian=self.vid_avian,
                 inh_rate_mammal=self.inh_rate_mammal,
                 vid_mammal=self.vid_mammal,
                 ar2=self.ar2,
                 air_conc=self.air_conc,
                 sid_avian=self.sid_avian,
                 sid_mammal=self.sid_mammal,
                 cf=self.cf,
                 mammal_inhalation_ld50=self.mammal_inhalation_ld50,
                 adjusted_mammal_inhalation_ld50=self.adjusted_mammal_inhalation_ld50,
                 estimated_avian_inhalation_ld50=self.estimated_avian_inhalation_ld50,
                 adjusted_avian_inhalation_ld50=self.adjusted_avian_inhalation_ld50,
                 ratio_vid_avian=self.ratio_vid_avian,
                 ratio_sid_avian=self.ratio_sid_avian,
                 ratio_vid_mammal=self.ratio_vid_mammal,
                 ratio_sid_mammal=self.ratio_sid_mammal,
                 loc_vid_avian=self.loc_vid_avian,
                 loc_sid_avian=self.loc_sid_avian,
                 loc_vid_mammal=self.loc_vid_mammal,
                 loc_sid_mammal=self.loc_sid_mammal))
        # create pandas properties for acceptance testing
        self.pd_obj_out = pd_obj_out

    def json(self, pd_obj, pd_obj_out, pd_obj_exp):
        """
            Convert DataFrames to JSON, returning a tuple
            of JSON strings (inputs, outputs, exp_out)
        """

        pd_obj_json = pd_obj.to_json()
        pd_obj_out_json = pd_obj_out.to_json()
        try:
            pd_obj_exp_json = pd_obj_exp.to_json()
        except:
            pd_obj_exp_json = "{}"

        return pd_obj_json, pd_obj_out_json, pd_obj_exp_json

    def calc_sat_air_conc(self):
        """
        # eq. 1 saturated air concentration in mg/m^3
        """
        # if self.sat_air_conc == -1:
        #    self.vapor_pressure = float(self.vapor_pressure)
        #    self.molecular_weight = float(self.molecular_weight)
        air_vol = 24.45
        pressure = 760.0
        conv = 1000000.0
        self.sat_air_conc = (self.vapor_pressure * self.molecular_weight * conv) / (pressure * air_vol)
        return self.sat_air_conc

    def calc_inh_rate_avian(self):
        """
        eq. 2 Avian inhalation rate
        """
        # if self.inh_rate_avian == -1:
        #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
        magic1 = 284.
        magic2 = 0.77
        conversion = 60.
        activity_factor = 3.
        self.inh_rate_avian = magic1 * (self.body_weight_assessed_bird ** magic2) * conversion * activity_factor
        return self.inh_rate_avian

    def calc_vid_avian(self):
        """
        eq. 3  Maximum avian vapor inhalation dose
        """
        # if self.vid_avian == -1:
        #    self.sat_air_conc = float(self.sat_air_conc)
        #    self.inh_rate_avian = float(self.inh_rate_avian)
        #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
        duration_hours = 1.
        conversion_factor = 1000000.  # cm3/m3
        # 1 (hr) is duration of exposure
        self.vid_avian = (self.sat_air_conc * self.inh_rate_avian * duration_hours) / (
            conversion_factor * self.body_weight_assessed_bird)
        return self.vid_avian

    def calc_inh_rate_mammal(self):
        """
        eq. 4 Mammalian inhalation rate
        """
        # if self.inh_rate_mammal == -1:
        #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
        magic1 = 379.0
        magic2 = 0.8
        minutes_conversion = 60.
        activity_factor = 3.
        self.inh_rate_mammal = magic1 * (
            self.body_weight_assessed_mammal ** magic2) * minutes_conversion * activity_factor
        return self.inh_rate_mammal

    def calc_vid_mammal(self):
        """
        eq. 5 Maximum mammalian vapor inhalation dose
        """
        # if self.vid_mammal == -1:
        #    self.sat_air_conc = float(self.sat_air_conc) # eq. 1
        #    self.inh_rate_mammal = float(self.inh_rate_mammal) # eq. 4
        #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
        duration_hours = 1.
        conversion_factor = 1000000.
        # 1 hr = duration of exposure
        self.vid_mammal = (self.sat_air_conc * self.inh_rate_mammal * duration_hours) / (
            conversion_factor * self.body_weight_assessed_mammal)
        return self.vid_mammal

    def calc_conc_air(self):
        """
        eq. 6 Air column concentration after spray
        """
        # if self.air_conc == -1:
        #    self.application_rate = float(self.application_rate)
        #    self.column_height = float(self.column_height)
        conversion_factor = 100.  # cm/m
        # conversion of application rate from lbs/acre to mg/cm2
        cf_g_lbs = 453.59237
        cf_mg_g = 1000.
        cf_cm2_acre = 40468564.2
        self.ar2 = (self.application_rate * cf_g_lbs * cf_mg_g) / cf_cm2_acre
        self.air_conc = self.ar2 / (self.column_height * conversion_factor)
        return self.air_conc

    def calc_sid_avian(self):
        """
        eq. 7 Avian spray droplet inhalation dose
        """
        # if self.sid_avian == -1:
        #    self.air_conc = float(self.air_conc)
        #    self.inh_rate_avian = float(self.inh_rate_avian)
        #    self.direct_spray_duration = float(self.direct_spray_duration)
        #    self.spray_drift_fraction = float(self.spray_drift_fraction)
        #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
        self.sid_avian = (self.air_conc * self.inh_rate_avian * (
            self.direct_spray_duration / 60.0) * self.spray_drift_fraction) / (self.body_weight_assessed_bird)
        return self.sid_avian

    def calc_sid_mammal(self):
        """
        eq. 8 Mammalian spray droplet inhalation dose
        """
        # if self.sid_mammal == -1:
        #    self.air_conc = float(self.air_conc)
        #    self.inh_rate_mammal = float(self.inh_rate_mammal)
        #    self.direct_spray_duration = float(self.direct_spray_duration)
        #    self.spray_drift_fraction = float(self.spray_drift_fraction)
        #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
        self.sid_mammal = (self.air_conc * self.inh_rate_mammal * (
            self.direct_spray_duration / 60.0) * self.spray_drift_fraction) / (self.body_weight_assessed_mammal)
        return self.sid_mammal

    def calc_convert_mammal_inhalation_lc50_to_ld50(self):
        """
        eq. 9 Conversion of mammalian LC50 to LD50
        """
        # if self.mammal_inhalation_ld50 == -1:
        #    self.mammal_inhalation_lc50 = float(self.mammal_inhalation_lc50)
        #    #conversion factor
        #    self.inh_rate_mammal = float(self.inh_rate_mammal)
        #    self.body_weight_tested_mammal = float(self.body_weight_tested_mammal)
        #    self.duration_mammal_inhalation_study = float(self.duration_mammal_inhalation_study)
        self.cf = ((self.inh_rate_mammal * 0.001) / self.body_weight_tested_mammal)
        activity_factor = 1.
        absorption = 1.
        self.mammal_inhalation_ld50 = self.mammal_inhalation_lc50 * absorption * self.cf * self.duration_mammal_inhalation_study * activity_factor
        return self.mammal_inhalation_ld50

    def calc_adjusted_mammal_inhalation_ld50(self):
        """
        eq. 10 Adjusted mammalian inhalation LD50
        """
        # if self.adjusted_mammal_inhalation_ld50 == -1:
        #    self.mammal_inhalation_ld50 = float(self.mammal_inhalation_ld50)
        #    self.body_weight_assessed_mammal = float(self.body_weight_assessed_mammal)
        #    self.body_weight_tested_mammal = float(self.body_weight_tested_mammal)
        magicpower = 0.25
        self.adjusted_mammal_inhalation_ld50 = self.mammal_inhalation_ld50 * (
                                                                                 self.body_weight_tested_mammal / self.body_weight_assessed_mammal) ** magicpower
        return self.adjusted_mammal_inhalation_ld50

    def calc_estimated_avian_inhalation_ld50(self):
        """
        eq. 11 Estimated avian inhalation LD50
        """
        # if self.estimated_avian_inhalation_ld50 == -1:
        #    self.avian_oral_ld50 = float(self.avian_oral_ld50)
        #    self.mammal_inhalation_ld50 = float(self.mammal_inhalation_ld50)
        #    self.mammal_oral_ld50 = float(self.mammal_oral_ld50)
        three_five = 3.5
        self.estimated_avian_inhalation_ld50 = (self.avian_oral_ld50 * self.mammal_inhalation_ld50) / (
            three_five * self.mammal_oral_ld50)
        return self.estimated_avian_inhalation_ld50

    def calc_adjusted_avian_inhalation_ld50(self):
        """
        eq. 12 Adjusted avian inhalation LD50
        """
        # if self.adjusted_avian_inhalation_ld50 == -1:
        #    self.estimated_avian_inhalation_ld50 = float(self.estimated_avian_inhalation_ld50)
        #    self.body_weight_assessed_bird = float(self.body_weight_assessed_bird)
        #    self.body_weight_tested_bird = float(self.body_weight_tested_bird)
        #    self.mineau_scaling_factor = float(self.mineau_scaling_factor)
        self.adjusted_avian_inhalation_ld50 = self.estimated_avian_inhalation_ld50 * (
                                                                                         self.body_weight_assessed_bird / self.body_weight_tested_bird) ** (
                                                                                         self.mineau_scaling_factor - 1)
        return self.adjusted_avian_inhalation_ld50

    def return_ratio_vid_avian(self):
        """
        results #1: Ratio of avian vapor dose to adjusted inhalation LD50
        """
        # if self.ratio_vid_avian == -1:
        #    self.vid_avian = float(self.vid_avian)
        #    self.adjusted_avian_inhalation_ld50 = float(self.adjusted_avian_inhalation_ld50)
        self.ratio_vid_avian = self.vid_avian / self.adjusted_avian_inhalation_ld50
        return self.ratio_vid_avian

    def return_loc_vid_avian(self):
        """
        results #2: Level of Concern for avian vapor phase risk
        """
        # if self.ratio_vid_avian < 0.1:
        #    self.loc_vid_avian = 'Exposure not Likely Significant'
        # else:
        #    self.loc_vid_avian = 'Proceed to Refinements'
        exceed_boolean = self.ratio_vid_avian < 0.1
        self.loc_vid_avian = exceed_boolean.map(lambda x:
                                                'Exposure not Likely Significant' if x == True
                                                else 'Proceed to Refinements')
        return self.loc_vid_avian

    def return_ratio_sid_avian(self):
        """
        results #3: Ratio of avian droplet inhalation dose to adjusted inhalation LD50
        """
        # if self.ratio_sid_avian == -1:
        #    self.sid_avian = float(self.sid_avian)
        #    self.adjusted_avian_inhalation_ld50 = float(self.adjusted_avian_inhalation_ld50)
        self.ratio_sid_avian = self.sid_avian / self.adjusted_avian_inhalation_ld50
        return self.ratio_sid_avian

    def return_loc_sid_avian(self):
        """
        results #4: Level of Concern for avian droplet inhalation risk
        """
        # if self.ratio_sid_avian < 0.1:
        #    self.loc_sid_avian = 'Exposure not Likely Significant'
        # else:
        #    self.loc_sid_avian = 'Proceed to Refinements'
        exceed_boolean = self.ratio_sid_avian < 0.1
        self.loc_sid_avian = exceed_boolean.map(lambda x:
                                                'Exposure not Likely Significant' if x == True
                                                else 'Proceed to Refinements')
        return self.loc_sid_avian

    def return_ratio_vid_mammal(self):
        """
        results #5: Ratio of mammalian vapor dose to adjusted inhalation LD50
        """
        # if self.ratio_vid_mammal == -1:
        #    self.vid_mammal = float(self.vid_mammal)
        #    self.adjusted_mammal_inhalation_ld50 = float(self.adjusted_mammal_inhalation_ld50)
        self.ratio_vid_mammal = self.vid_mammal / self.adjusted_mammal_inhalation_ld50
        return self.ratio_vid_mammal

    def return_loc_vid_mammal(self):
        """
        results #6: Level of Concern for mammalian vapor phase risk
        """
        # if self.ratio_vid_mammal < 0.1:
        #    self.loc_vid_mammal = 'Exposure not Likely Significant'
        # else:
        #    self.loc_vid_mammal = 'Proceed to Refinements'
        exceed_boolean = self.ratio_vid_mammal < 0.1
        self.loc_vid_mammal = exceed_boolean.map(lambda x:
                                                 'Exposure not Likely Significant' if x == True
                                                 else 'Proceed to Refinements')
        return self.loc_vid_mammal

    def return_ratio_sid_mammal(self):
        """
        results #7: Ratio of mammalian droplet inhalation dose to adjusted inhalation LD50
        """
        # if self.ratio_sid_mammal == -1:
        #    self.sid_mammal = float(self.sid_mammal)
        #    self.adjusted_mammal_inhalation_ld50 = float(self.adjusted_mammal_inhalation_ld50)
        self.ratio_sid_mammal = self.sid_mammal / self.adjusted_mammal_inhalation_ld50
        return self.ratio_sid_mammal

    def return_loc_sid_mammal(self):
        """
        results #8: Level of Concern for mammaliam droplet inhalation risk
        """
        # if self.ratio_sid_mammal < 0.1:
        #    self.loc_sid_mammal = 'Exposure not Likely Significant'
        # else:
        #    self.loc_sid_mammal = 'Proceed to Refinements'
        exceed_boolean = self.ratio_sid_mammal < 0.1
        self.loc_sid_mammal = exceed_boolean.map(lambda x:
                                                 'Exposure not Likely Significant' if x == True
                                                 else 'Proceed to Refinements')
        return self.loc_sid_mammal


def main():
    """
    main callable
    :return:
    """
    test_stir = stir(True, True, 1, 1, 1, 1, 1, 1, 1, 1)
    print vars(test_stir)
    stir_json = toJSON(test_stir)
    new_stir = fromJSON(stir_json)
    print vars(new_stir)


if __name__ == '__main__':
    main()
