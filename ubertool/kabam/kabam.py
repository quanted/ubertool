from __future__ import division
import math
import numpy as np


class Kabam(object):
    """
    Hydrophobic organic pesticide bioaccumulation in aquatic components of a food web to terrestrial
    exposure in birds and mammals
    """
    def __init__(self, chemical_name, l_kow, k_oc, c_wdp, water_column_EEC, c_wto, mineau_scaling_factor, x_poc, x_doc,
                 c_ox, w_t, c_ss, oc, k_ow, Species_of_the_tested_bird, bw_quail, bw_duck, bwb_other, avian_ld50,
                 avian_lc50, avian_noaec, m_species, bw_rat, bwm_other, mammalian_ld50, mammalian_lc50,
                 mammalian_chronic_endpoint, lf_p_sediment, lf_p_phytoplankton, lf_p_zooplankton,
                 lf_p_benthic_invertebrates, lf_p_filter_feeders, lf_p_small_fish, lf_p_medium_fish, mf_p_sediment,
                 mf_p_phytoplankton, mf_p_zooplankton, mf_p_benthic_invertebrates, mf_p_filter_feeders, mf_p_small_fish,
                 sf_p_sediment, sf_p_phytoplankton, sf_p_zooplankton, sf_p_benthic_invertebrates, sf_p_filter_feeders,
                 ff_p_sediment, ff_p_phytoplankton, ff_p_zooplankton, ff_p_benthic_invertebrates, beninv_p_sediment,
                 beninv_p_phytoplankton, beninv_p_zooplankton, zoo_p_sediment, zoo_p_phyto, s_lipid, s_NLOM, s_water,
                 v_lb_phytoplankton, v_nb_phytoplankton, v_wb_phytoplankton, wb_zoo, v_lb_zoo, v_nb_zoo, v_wb_zoo,
                 wb_beninv, v_lb_beninv, v_nb_beninv, v_wb_beninv, wb_ff, v_lb_ff, v_nb_ff, v_wb_ff, wb_sf, v_lb_sf,
                 v_nb_sf, v_wb_sf, wb_mf, v_lb_mf, v_nb_mf, v_wb_mf, wb_lf, v_lb_lf, v_nb_lf, v_wb_lf, kg_phytoplankton,
                 kd_phytoplankton, ke_phytoplankton, mo_phytoplankton, mp_phytoplankton, km_phytoplankton, km_zoo,
                 k1_phytoplankton, k2_phytoplankton, k1_zoo, k2_zoo, kd_zoo, ke_zoo, k1_beninv, k2_beninv, kd_beninv,
                 ke_beninv, km_beninv, k1_ff, k2_ff, kd_ff, ke_ff, km_ff, k1_sf, k2_sf, kd_sf, ke_sf, km_sf, k1_mf,
                 k2_mf, kd_mf, ke_mf, km_mf, k1_lf, k2_lf, kd_lf, ke_lf, km_lf, rate_constants, s_respire,
                 phyto_respire, zoo_respire, beninv_respire, ff_respire, sfish_respire, mfish_respire, lfish_respire):
        """Kabam constructor."""
        self.chemical_name = chemical_name
        self.l_kow = l_kow
        self.k_oc = k_oc
        self.c_wdp = c_wdp
        self.water_column_EEC = water_column_EEC
        self.c_wto = c_wto
        self.mineau_scaling_factor = mineau_scaling_factor
        self.x_poc = x_poc
        self.x_doc = x_doc
        self.c_ox = c_ox
        self.w_t = w_t
        self.c_ss = c_ss
        self.oc = oc
        self.k_ow = k_ow
        self.Species_of_the_tested_bird = Species_of_the_tested_bird
        self.bw_quail = bw_quail
        self.bw_duck = bw_duck
        self.bwb_other = bwb_other
        if Species_of_the_tested_bird == '178':
            self.bw_bird = self.bw_quail
        elif Species_of_the_tested_bird == '1580':
            self.bw_bird = self.bw_duck
        else:
            self.bw_bird = self.bwb_other
        self.avian_ld50 = avian_ld50
        self.avian_lc50 = avian_lc50
        self.avian_noaec = avian_noaec
        self.m_species = m_species
        self.bw_rat = bw_rat
        self.bwm_other = bwm_other
        if m_species == '350':
            self.bw_mamm = self.bw_rat
        else:
            self.bw_mamm = self.bwm_other
        self.mammalian_ld50 = mammalian_ld50
        self.mammalian_lc50 = mammalian_lc50
        self.mammalian_chronic_endpoint = mammalian_chronic_endpoint
        self.lf_p_sediment = lf_p_sediment
        self.lf_p_phytoplankton = lf_p_phytoplankton
        self.lf_p_zooplankton = lf_p_zooplankton
        self.lf_p_benthic_invertebrates = lf_p_benthic_invertebrates
        self.lf_p_filter_feeders = lf_p_filter_feeders
        self.lf_p_small_fish = lf_p_small_fish
        self.lf_p_medium_fish = lf_p_medium_fish
        self.mf_p_sediment = mf_p_sediment
        self.mf_p_phytoplankton = mf_p_phytoplankton
        self.mf_p_zooplankton = mf_p_zooplankton
        self.mf_p_benthic_invertebrates = mf_p_benthic_invertebrates
        self.mf_p_filter_feeders = mf_p_filter_feeders
        self.mf_p_small_fish = mf_p_small_fish
        self.sf_p_sediment = sf_p_sediment
        self.sf_p_phytoplankton = sf_p_phytoplankton
        self.sf_p_zooplankton = sf_p_zooplankton
        self.sf_p_benthic_invertebrates = sf_p_benthic_invertebrates
        self.sf_p_filter_feeders = sf_p_filter_feeders
        self.ff_p_sediment = ff_p_sediment
        self.ff_p_phytoplankton = ff_p_phytoplankton
        self.ff_p_zooplankton = ff_p_zooplankton
        self.ff_p_benthic_invertebrates = ff_p_benthic_invertebrates
        self.beninv_p_sediment = beninv_p_sediment
        self.beninv_p_phytoplankton = beninv_p_phytoplankton
        self.beninv_p_zooplankton = beninv_p_zooplankton
        self.zoo_p_sediment = zoo_p_sediment
        self.zoo_p_phyto = zoo_p_phyto
        self.s_lipid = s_lipid
        self.s_NLOM = s_NLOM
        self.s_water = s_water
        self.v_lb_phytoplankton = v_lb_phytoplankton
        self.v_nb_phytoplankton = v_nb_phytoplankton
        self.v_wb_phytoplankton = v_wb_phytoplankton
        self.wb_zoo = wb_zoo
        self.v_lb_zoo = v_lb_zoo
        self.v_nb_zoo = v_nb_zoo
        self.v_wb_zoo = v_wb_zoo
        self.wb_beninv = wb_beninv
        self.v_lb_beninv = v_lb_beninv
        self.v_nb_beninv = v_nb_beninv
        self.v_wb_beninv = v_wb_beninv
        self.wb_ff = wb_ff
        self.v_lb_ff = v_lb_ff
        self.v_nb_ff = v_nb_ff
        self.v_wb_ff = v_wb_ff
        self.wb_sf = wb_sf
        self.v_lb_sf = v_lb_sf
        self.v_nb_sf = v_nb_sf
        self.v_wb_sf = v_wb_sf
        self.wb_mf = wb_mf
        self.v_lb_mf = v_lb_mf
        self.v_nb_mf = v_nb_mf
        self.v_wb_mf = v_wb_mf
        self.wb_lf = wb_lf
        self.v_lb_lf = v_lb_lf
        self.v_nb_lf = v_nb_lf
        self.v_wb_lf = v_wb_lf
        self.kg_phytoplankton = kg_phytoplankton
        self.kd_phytoplankton = kd_phytoplankton
        self.ke_phytoplankton = ke_phytoplankton
        self.mo_phytoplankton = mo_phytoplankton
        self.mp_phytoplankton = mp_phytoplankton
        self.km_phytoplankton = km_phytoplankton
        self.km_zoo = km_zoo
        self.k1_phytoplankton = k1_phytoplankton
        self.k2_phytoplankton = k2_phytoplankton
        self.k1_zoo = k1_zoo
        self.k2_zoo = k2_zoo
        self.kd_zoo = kd_zoo
        self.ke_zoo = ke_zoo
        self.k1_beninv = k1_beninv
        self.k2_beninv = k2_beninv
        self.kd_beninv = kd_beninv
        self.ke_beninv = ke_beninv
        self.km_beninv = km_beninv
        self.k1_ff = k1_ff
        self.k2_ff = k2_ff
        self.kd_ff = kd_ff
        self.ke_ff = ke_ff
        self.km_ff = km_ff
        self.k1_sf = k1_sf
        self.k2_sf = k2_sf
        self.kd_sf = kd_sf
        self.ke_sf = ke_sf
        self.km_sf = km_sf
        self.k1_mf = k1_mf
        self.k2_mf = k2_mf
        self.kd_mf = kd_mf
        self.ke_mf = ke_mf
        self.km_mf = km_mf
        self.k1_lf = k1_lf
        self.k2_lf = k2_lf
        self.kd_lf = kd_lf
        self.ke_lf = ke_lf
        self.km_lf = km_lf
        # self.k_bw_phytoplankton=k_bw_phytoplankton
        # self.k_bw_zoo=k_bw_zoo
        # self.k_bw_beninv=k_bw_beninv
        # self.k_bw_ff=k_bw_ff
        # self.k_bw_sf=k_bw_sf
        # self.k_bw_mf=k_bw_mf
        # self.k_bw_lf=k_bw_lf
        self.rate_constants = rate_constants
        self.s_respire = s_respire
        self.phyto_respire = phyto_respire
        self.zoo_respire = zoo_respire
        self.beninv_respire = beninv_respire
        self.ff_respire = ff_respire
        self.sfish_respire = sfish_respire
        self.mfish_respire = mfish_respire
        self.lfish_respire = lfish_respire

        # outputs
        if self.rate_constants == 'a':
            self.k_bw_phytoplankton_f()
            self.k1_phytoplankton_f()
            self.k2_phytoplankton_f()
            self.ew_zoo_f()
            self.gv_zoo_f()
            self.k_bw_zoo_f()
            self.ed_zoo_f()
            self.gd_zoo_f()
            self.k1_zoo_f()
            self.k2_zoo_f()
            self.kd_zoo_f()
            self.v_nd_zoo_f()
            self.v_wd_zoo_f()
            self.v_ld_zoo_f()
            self.gf_zoo_f()
            self.vlg_zoo_f()
            self.vng_zoo_f()
            self.vwg_zoo_f()
            self.kgb_zoo_f()
            self.ke_zoo_f()

            self.k_bw_beninv_f()
            self.ed_beninv_f()
            self.gd_beninv_f()
            self.kg_beninv_f()
            self.v_ld_beninv_f()
            self.v_nd_beninv_f()
            self.v_wd_beninv_f()
            self.gf_beninv_f()
            self.vlg_beninv_f()
            self.vng_beninv_f()
            self.vwg_beninv_f()
            self.kgb_beninv_f()
            self.ew_beninv_f()
            self.gv_beninv_f()
            self.k1_beninv_f()
            self.k2_beninv_f()
            self.kd_beninv_f()
            self.ke_beninv_f()

            self.gv_ff_f()
            self.ew_ff_f()
            self.k_bw_ff_f()
            self.ed_ff_f()
            self.gd_ff_f()
            self.kg_ff_f()
            self.v_ld_ff_f()
            self.v_nd_ff_f()
            self.v_wd_ff_f()
            self.gf_ff_f()
            self.vlg_ff_f()
            self.vng_ff_f()
            self.vwg_ff_f()
            self.kgb_ff_f()
            self.k1_ff_f()
            self.k2_ff_f()
            self.kd_ff_f()
            self.ke_ff_f()

            self.gv_sf_f()
            self.ew_sf_f()
            self.k_bw_sf_f()
            self.ed_sf_f()
            self.gd_sf_f()
            self.kg_sf_f()
            self.v_ld_sf_f()
            self.v_nd_sf_f()
            self.v_wd_sf_f()
            self.gf_sf_f()
            self.vlg_sf_f()
            self.vng_sf_f()
            self.vwg_sf_f()
            self.kgb_sf_f()
            self.k1_sf_f()
            self.k2_sf_f()
            self.kd_sf_f()
            self.ke_sf_f()

            self.gv_mf_f()
            self.ew_mf_f()
            self.k_bw_mf_f()
            self.ed_mf_f()
            self.gd_mf_f()
            self.kg_mf_f()
            self.v_ld_mf_f()
            self.v_nd_mf_f()
            self.v_wd_mf_f()
            self.gf_mf_f()
            self.vlg_mf_f()
            self.vng_mf_f()
            self.vwg_mf_f()
            self.kgb_mf_f()
            self.k1_mf_f()
            self.k2_mf_f()
            self.kd_mf_f()
            self.ke_mf_f()

            self.gv_lf_f()
            self.ew_lf_f()
            self.k_bw_lf_f()
            self.ed_lf_f()
            self.gd_lf_f()
            self.kg_lf_f()
            self.v_ld_lf_f()
            self.v_nd_lf_f()
            self.v_wd_lf_f()
            self.gf_lf_f()
            self.vlg_lf_f()
            self.vng_lf_f()
            self.vwg_lf_f()
            self.kgb_lf_f()
            self.k1_lf_f()
            self.k2_lf_f()
            self.kd_lf_f()
            self.ke_lf_f()

        else:
            self.k1_phytoplankton = k1_phytoplankton
            self.k2_phytoplankton = k2_phytoplankton
            self.kd_phytoplankton = kd_phytoplankton
            self.ke_phytoplankton = ke_phytoplankton
            self.km_phytoplankton = km_phytoplankton
            self.k1_zoo = k1_zoo
            self.k2_zoo = k2_zoo
            self.kd_zoo = kd_zoo
            self.ke_zoo = ke_zoo
            self.km_zoo = km_zoo
            self.k1_beninv = k1_beninv
            self.k2_beninv = k2_beninv
            self.kd_beninv = kd_beninv
            self.ke_beninv = ke_beninv
            self.km_beninv = km_beninv
            self.k1_ff = k1_ff
            self.k2_ff = k2_ff
            self.kd_ff = kd_ff
            self.ke_ff = ke_ff
            self.km_ff = km_ff
            self.k1_sf = k1_sf
            self.k2_sf = k2_sf
            self.kd_sf = kd_sf
            self.ke_sf = ke_sf
            self.km_sf = km_sf
            self.k1_mf = k1_mf
            self.k2_mf = k2_mf
            self.kd_mf = kd_mf
            self.ke_mf = ke_mf
            self.km_mf = km_mf
            self.k1_lf = k1_lf
            self.k2_lf = k2_lf
            self.kd_lf = kd_lf
            self.ke_lf = ke_lf
            self.km_lf = km_lf
        self.run_methods()

    def run_methods(self):
        """
        Execute all subroutines in proper order.
        :return:
        """
        self.phi_f()
        self.c_soc_f()
        self.c_s_f()
        self.sed_om_f()
        self.water_d()
        # self.k_bw_phytoplankton_f()
        # self.k1_phytoplankton_f()
        # self.k2_phytoplankton_f()
        self.cb_phytoplankton_f()
        self.cbl_phytoplankton_f()
        self.cbf_phytoplankton_f()
        self.cbr_phytoplankton_f()
        self.cbfl_phytoplankton_f()
        self.cbaf_phytoplankton_f()
        self.cbafl_phytoplankton_f()
        self.cbsafl_phytoplankton_f()
        # self.gv_zoo_f()
        # self.ew_zoo_f()
        # self.k1_zoo_f()
        # self.k_bw_zoo_f()
        # self.k2_zoo_f()
        # self.ed_zoo_f()
        # self.gd_zoo_f()
        # self.kd_zoo_f()
        self.kg_zoo_f()
        # self.v_ld_zoo_f()
        # self.v_nd_zoo_f()
        # self.v_wd_zoo_f()
        # self.gf_zoo_f()
        # self.vlg_zoo_f()
        # self.vng_zoo_f()
        # self.vwg_zoo_f()
        # self.kgb_zoo_f()
        # self.ke_zoo_f()
        self.diet_zoo_f()
        self.cb_zoo_f()
        self.cbl_zoo_f()
        self.cbd_zoo_f()
        self.cbr_zoo_f()
        self.cbf_zoo_f()
        self.cbfl_zoo_f()
        self.cbaf_zoo_f()
        self.cbafl_zoo_f()
        self.cbsafl_zoo_f()
        self.bmf_zoo_f()
        # self.gv_beninv_f()
        # self.ew_beninv_f()
        # self.k1_beninv_f()
        # self.k_bw_beninv_f()
        # # self.k2_beninv_f()
        # self.ed_beninv_f()
        # self.gd_beninv_f()
        # # self.kd_beninv_f()
        self.kg_beninv_f()
        # self.v_ld_beninv_f()
        # self.v_nd_beninv_f()
        # self.v_wd_beninv_f()
        # self.gf_beninv_f()
        # self.vlg_beninv_f()
        # self.vng_beninv_f()
        # self.vwg_beninv_f()
        # self.kgb_beninv_f()
        # self.ke_beninv_f()
        self.diet_beninv_f()
        self.cb_beninv_f()
        self.cbl_beninv_f()
        self.cbd_beninv_f()
        self.cbr_beninv_f()
        self.cbf_beninv_f()
        self.cbfl_beninv_f()
        self.cbaf_beninv_f()
        self.cbafl_beninv_f()
        self.cbsafl_beninv_f()
        self.bmf_beninv_f()
        # self.gv_ff_f()
        # self.ew_ff_f()
        # # self.k1_ff_f()
        # self.k_bw_ff_f()
        # # self.k2_ff_f()
        # self.ed_ff_f()
        # self.gd_ff_f()
        # # self.kd_ff_f()
        self.kg_ff_f()
        # self.v_ld_ff_f()
        # self.v_nd_ff_f()
        # self.v_wd_ff_f()
        # self.gf_ff_f()
        # self.vlg_ff_f()
        # self.vng_ff_f()
        # self.vwg_ff_f()
        # self.kgb_ff_f()
        # self.ke_ff_f()
        self.diet_ff_f()
        self.cb_ff_f()
        self.cbl_ff_f()
        self.cbd_ff_f()
        self.cbr_ff_f()
        self.cbf_ff_f()
        self.cbfl_ff_f()
        self.cbaf_ff_f()
        self.cbafl_ff_f()
        self.cbsafl_ff_f()
        self.bmf_ff_f()
        # self.gv_sf_f()
        # self.ew_sf_f()
        # # self.k1_sf_f()
        # self.k_bw_sf_f()
        # # self.k2_sf_f()
        # self.ed_sf_f()
        # self.gd_sf_f()
        # # self.kd_sf_f()
        self.kg_sf_f()
        # self.v_ld_sf_f()
        # self.v_nd_sf_f()
        # self.v_wd_sf_f()
        # self.gf_sf_f()
        # self.vlg_sf_f()
        # self.vng_sf_f()
        # self.vwg_sf_f()
        # self.kgb_sf_f()
        # self.ke_sf_f()
        self.diet_sf_f()
        self.cb_sf_f()
        self.cbl_sf_f()
        self.cbd_sf_f()
        self.cbr_sf_f()
        self.cbf_sf_f()
        self.cbfl_sf_f()
        self.cbaf_sf_f()
        self.cbafl_sf_f()
        self.cbsafl_sf_f()
        self.bmf_sf_f()
        # self.gv_mf_f()
        # self.ew_mf_f()
        # # self.k1_mf_f()
        # self.k_bw_mf_f()
        # # self.k2_mf_f()
        # self.ed_mf_f()
        # self.gd_mf_f()
        # # self.kd_mf_f()
        self.kg_mf_f()
        # self.v_ld_mf_f()
        # self.v_nd_mf_f()
        # self.v_wd_mf_f()
        # self.gf_mf_f()
        # self.vlg_mf_f()
        # self.vng_mf_f()
        # self.vwg_mf_f()
        # self.kgb_mf_f()
        # self.ke_mf_f()
        self.diet_mf_f()
        self.cb_mf_f()
        self.cbl_mf_f()
        self.cbd_mf_f()
        self.cbr_mf_f()
        self.cbf_mf_f()
        self.cbfl_mf_f()
        self.cbaf_mf_f()
        self.cbafl_mf_f()
        self.cbsafl_mf_f()
        self.cbmf_mf_f()
        # self.gv_lf_f()
        # self.ew_lf_f()
        # # self.k1_lf_f()
        # self.k_bw_lf_f()
        # # self.k2_lf_f()
        # self.ed_lf_f()
        # self.gd_lf_f()
        # # self.kd_lf_f()
        self.kg_lf_f()
        # self.v_ld_lf_f()
        # self.v_nd_lf_f()
        # self.v_wd_lf_f()
        # self.gf_lf_f()
        # self.vlg_lf_f()
        # self.vng_lf_f()
        # self.vwg_lf_f()
        # self.kgb_lf_f()
        # self.ke_lf_f()
        self.diet_lf_f()
        self.cb_lf_f()
        self.cbl_lf_f()
        self.cbd_lf_f()
        self.cbr_lf_f()
        self.cbf_lf_f()
        self.cbfl_lf_f()
        self.cbaf_lf_f()
        self.cbafl_lf_f()
        self.cbsafl_lf_f()
        self.cbmf_lf_f()
        self.mweight_f()
        self.dfir_f()
        self.wet_food_ingestion_m_f()
        self.drinking_water_intake_m_f()
        self.db4_f()
        self.db5_f()
        self.aweight_f()
        self.dfir_a_f()
        self.wet_food_ingestion_a_f()
        self.drinking_water_intake_a_f()
        self.db4a_f()
        self.db5a_f()
        self.acute_dose_based_m_f()
        self.chronic_dose_based_m_f()
        self.acute_dose_based_a_f()
        self.acute_rq_dose_m_f()
        self.chronic_rq_dose_m_f()
        self.acute_rq_diet_m_f()
        self.chronic_rq_diet_m_f()
        self.acute_rq_dose_a_f()
        self.acute_rq_diet_a_f()
        self.chronic_rq_diet_a_f()

    def phi_f(self):
        """
        Calculate Fraction of freely dissolved in water column
        :return:
        """
        self.phi = 1 / (1 + (self.x_poc * 0.35 * self.k_ow) + (self.x_doc * 0.08 * self.k_ow))
        return self.phi

    def c_soc_f(self):
        """
        Normalized pesticide concentration in sediment
        :return:
        """
        self.c_soc = self.k_oc * self.c_wdp
        return self.c_soc

    def c_s_f(self):
        """
        Calculate concentration of chemical in sediment
        :return:
        """
        self.c_s = self.c_soc * self.oc
        return self.c_s

    def sed_om_f(self):
        """
        Calculate organic matter fraction in sediment
        :return:
        """
        self.sed_om = self.c_s / self.oc
        return self.sed_om

    def water_d(self):
        """
        Water freely dissolved
        :return:
        """
        self.water_d = self.phi * self.c_wto * 1000000
        return self.water_d


    def k_bw_phytoplankton_f(self):
        """
        Phytoplankton water partition coefficient
        :return:
        """
        self.k_bw_phytoplankton = (self.v_lb_phytoplankton * self.k_ow) + (
            self.v_nb_phytoplankton * 0.35 * self.k_ow) + self.v_wb_phytoplankton
        return self.k_bw_phytoplankton


    def k1_phytoplankton_f(self):
        """
        Rate constant for uptake through respiratory area
        :return:
        """
        self.k1_phytoplankton = 1 / (6.0e-5 + (5.5 / self.k_ow))
        return self.k1_phytoplankton


    def k2_phytoplankton_f(self):
        """
        Rate constant for elimination through the gills for phytoplankton
        :return:
        """
        self.k2_phytoplankton = self.k1_phytoplankton / self.k_bw_phytoplankton
        return self.k2_phytoplankton

    def cb_phytoplankton_f(self):
        """
        Phytoplankton pesticide tissue residue
        :return:
        """
        self.cb_phytoplankton = (self.k1_phytoplankton * (
            self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp)) / (
                                    self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton)
        return self.cb_phytoplankton

    def cbl_phytoplankton_f(self):
        """
        Lipid normalized pesticide residue in phytoplankton
        :return:
        """
        self.cbl_phytoplankton = (1e6 * self.cb_phytoplankton) / self.v_lb_phytoplankton
        return self.cbl_phytoplankton

    def cbf_phytoplankton_f(self):
        """
        Phytoplankton total bioconcentration factor
        :return:
        """
        # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
        self.ke_phytoplankton = 0
        self.km_phytoplankton = 0
        self.kg_phytoplankton = 0
        self.cbf_phytoplankton = ((self.k1_phytoplankton * (
            self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp)) / (
                                      self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton)) / self.c_wto
        return self.cbf_phytoplankton

    def cbr_phytoplankton_f(self):
        """
        Phytoplankton
        """
        self.ke_phytoplankton = 0
        self.km_phytoplankton = 0
        self.cbr_phytoplankton = ((self.k1_phytoplankton * (
            self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp)) / (
                                      self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton))
        return self.cbr_phytoplankton

    def cbfl_phytoplankton_f(self):
        """
        Phytoplankton lipid normalized total bioconcentration factor
        :return:
        """
        # kd_phytoplankton = 0 #kd_phytoplankton is always = 0
        self.ke_phytoplankton = 0
        self.km_phytoplankton = 0
        self.kg_phytoplankton = 0
        self.cbfl_phytoplankton = ((self.k1_phytoplankton * (
            self.mo_phytoplankton * self.c_wto * self.phi + self.mp_phytoplankton * self.c_wdp) / (
                                        self.k2_phytoplankton + self.ke_phytoplankton + self.kg_phytoplankton + self.km_phytoplankton)) / self.v_lb_phytoplankton) / (
                                      self.c_wto * self.phi)
        return self.cbfl_phytoplankton

    def cbaf_phytoplankton_f(self):
        """
        Phytoplankton bioaccumulation factor
        :return:
        """
        self.cbaf_phytoplankton = (1e6 * self.cb_phytoplankton) / self.water_column_EEC
        return self.cbaf_phytoplankton

    def cbafl_phytoplankton_f(self):
        """
        Phytoplankton lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_phytoplankton = self.cbl_phytoplankton / self.water_d
        return self.cbafl_phytoplankton

    def cbsafl_phytoplankton_f(self):
        """
        Phytoplankton biota-sediment accumulation factor
        :return:
        """
        self.cbsafl_phytoplankton = (self.cb_phytoplankton / self.v_lb_phytoplankton) / self.sed_om
        return self.cbsafl_phytoplankton

    ##################zooplankton
    def gv_zoo_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_zoo = (1400 * (self.wb_zoo ** 0.65)) / self.c_ox
        return self.gv_zoo

    def ew_zoo_f(self):
        """
        Rate constant for elimination through the gills for zooplankton
        :return:
        """
        self.ew_zoo = (1 / (1.85 + (155 / self.k_ow)))
        return self.ew_zoo

    def k1_zoo_f(self):
        """
        Uptake rate constant through respiratory area for phytoplankton
        :return:
        """
        self.k1_zoo = self.ew_zoo * self.gv_zoo / self.wb_zoo
        return self.k1_zoo

    def k_bw_zoo_f(self):
        """
        Zooplankton water partition coefficient
        :return:
        """
        self.k_bw_zoo = (self.v_lb_zoo * self.k_ow) + (self.v_nb_zoo * 0.035 * self.k_ow) + self.v_wb_zoo
        return self.k_bw_zoo

    def k2_zoo_f(self):
        """
        Elimination rate constant through the gills for zooplankton
        :return:
        """
        self.k2_zoo = self.k1_zoo / self.k_bw_zoo
        return self.k2_zoo

    def ed_zoo_f(self):
        """
        Zooplankton dietary pesticide transfer efficiency
        :return:
        """
        self.ed_zoo = 1 / ((.0000003) * self.k_ow + 2.0)
        return self.ed_zoo

    def gd_zoo_f(self):
        """
        Zooplankton feeding rate
        :return:
        """
        self.gd_zoo = 0.022 * self.wb_zoo ** 0.85 * math.exp(0.06 * self.w_t)
        return self.gd_zoo

    def kd_zoo_f(self):
        """
        Zooplankton rate constant pesticide uptake by food ingestion
        :return:
        """
        self.kd_zoo = self.ed_zoo * (self.gd_zoo / self.wb_zoo)
        return self.kd_zoo


    def kg_zoo_f(self):
        """
        Zooplankton growth rate constant
        :return:
        """
        if self.w_t < 17.5:
            self.kg_zoo = 0.0005 * self.wb_zoo ** -0.2
        else:
            self.kg_zoo = 0.00251 * self.wb_zoo ** -0.2
        return self.kg_zoo

    def v_ld_zoo_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_zoo = self.zoo_p_sediment * self.s_lipid + self.zoo_p_phyto * self.v_lb_phytoplankton
        return self.v_ld_zoo

    def v_nd_zoo_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_zoo = self.zoo_p_sediment * self.s_NLOM + self.zoo_p_phyto * self.v_nb_phytoplankton
        return self.v_nd_zoo

    def v_wd_zoo_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_zoo = self.zoo_p_sediment * self.s_water + self.zoo_p_phyto * self.v_wb_phytoplankton
        return self.v_wd_zoo

    def gf_zoo_f(self):
        """
        Egestion rate of fecal matter
        :return:
        """
        self.gf_zoo = (((1 - .72) * self.v_ld_zoo) + ((1 - .72) * self.v_nd_zoo) + (
            (1 - .25) * self.v_wd_zoo)) * self.gd_zoo
        # rr=self.zoo_p_phyto
        # if rr==0:
        #   rr==0.00000001
        # return rr
        return self.gf_zoo

    def vlg_zoo_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_zoo = (1 - 0.72) * self.v_ld_zoo * self.gd_zoo / self.gf_zoo
        return self.vlg_zoo

    def vng_zoo_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_zoo = (1 - 0.72) * self.v_nd_zoo * self.gd_zoo / self.gf_zoo
        return self.vng_zoo

    def vwg_zoo_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_zoo = (1 - 0.25) * self.v_wd_zoo * self.gd_zoo / self.gf_zoo
        return self.vwg_zoo

    def kgb_zoo_f(self):
        """
        Partition coefficient of the pesticide between the gastrointenstinal track and the organism
        :return:
        """
        self.kgb_zoo = (self.vlg_zoo * self.k_ow + self.vng_zoo * 0.035 * self.k_ow + self.vwg_zoo) / (
            self.v_lb_zoo * self.k_ow + self.v_nb_zoo * 0.035 * self.k_ow + self.v_wb_zoo)
        return self.kgb_zoo

    def ke_zoo_f(self):
        """
        Dietary elimination rate constant
        :return:
        """
        self.ke_zoo = self.gf_zoo * self.ed_zoo * self.kgb_zoo / self.wb_zoo
        #   self.ke_zoo = self.zoo_p_phyto
        return self.ke_zoo

    def diet_zoo_f(self):
        """
        Diet fraction
        :return:
        """
        self.diet_zoo = self.c_s * self.zoo_p_sediment + self.cb_phytoplankton * self.zoo_p_phyto
        return self.diet_zoo

    def cb_zoo_f(self):
        """
        Zooplankton pesticide tissue residue
        :return:
        """
        self.cb_zoo = (self.k1_zoo * (1.0 * self.phi * self.c_wto + 0 * self.c_wdp) + self.kd_zoo * self.diet_zoo) / (
            self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)
        # print "cb_zoo =", self.cb_zoo
        return self.cb_zoo

    def cbl_zoo_f(self):
        """
        Zooplankton pesticide tissue residue lipid normalized
        :return:
        """
        self.cbl_zoo = (1e6 * self.cb_zoo) / self.v_lb_zoo
        return self.cbl_zoo

    def cbd_zoo_f(self):
        """
        Zooplankton pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_zoo = (0 * (1.0) * self.phi * self.c_wto + (0 * self.c_wdp) + (self.kd_zoo * (self.diet_zoo))) / (
            self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)
        # print "cbd_zoo =", self.cbd_zoo
        return self.cbd_zoo

    def cbr_zoo_f(self):
        """
        Zooplankton pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_zoo = (self.k1_zoo * (1. * self.phi * self.c_wto + 0 * self.c_wdp) + (0 * self.diet_zoo)) / (
            self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)
        return self.cbr_zoo

    def cbf_zoo_f(self):
        """
        Zooplankton total bioconcentration factor
        :return:
        """
        self.kd_zoo = 0
        self.ke_zoo = 0
        #    km_zoo = 0 km_zoo is always = 0
        self.kg_zoo = 0
        self.cbf_zoo = ((self.k1_zoo * (1. * self.phi * self.c_wto + 0 * self.c_wdp) + self.kd_zoo * self.diet_zoo) / (
            self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)) / self.c_wto
        return self.cbf_zoo

    def cbfl_zoo_f(self):
        """
        Zooplankton lipid normalized total bioconcentration factor
        :return:
        """
        self.kd_zoo = 0
        self.ke_zoo = 0
        #    km_zoo = 0 km_zoo is always = 0
        self.kg_zoo = 0
        self.cbfl_zoo = (
                            (self.k1_zoo * (
                            1.0 * self.phi * self.c_wto + 0 * self.c_wdp) + self.kd_zoo * self.diet_zoo) / (
                                self.k2_zoo + self.ke_zoo + self.kg_zoo + 0)) / self.v_lb_zoo / (self.c_wto * self.phi)
        return self.cbfl_zoo

    def cbaf_zoo_f(self):
        """
        Zooplankton bioaccumulation factor
        :return:
        """
        self.cbaf_zoo = (1e6 * self.cb_zoo) / self.water_column_EEC
        return self.cbaf_zoo

    def cbafl_zoo_f(self):
        """
        Zooplankton lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_zoo = self.cbl_zoo / self.water_d
        return self.cbafl_zoo

    def cbsafl_zoo_f(self):
        """
        Zooplankton bioaccumulation
        :return:
        """
        self.cbsafl_zoo = (self.cb_zoo / self.v_lb_zoo) / self.sed_om
        return self.cbsafl_zoo

    def bmf_zoo_f(self):
        """
        Zooplankton biomagnification factor
        :return:
        """
        self.bmf_zoo = (self.cb_zoo / self.v_lb_zoo) / (
            self.zoo_p_phyto * self.cb_phytoplankton / self.v_lb_phytoplankton)
        return self.bmf_zoo

    ################################ benthic invertebrates
    ############################################################
    def gv_beninv_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_beninv = (1400 * ((self.wb_beninv ** 0.65) / self.c_ox))
        return self.gv_beninv

    def ew_beninv_f(self):
        """
        Rate constant for elimination through the gills for benthic invertebrates
        :return:
        """
        self.ew_beninv = (1 / (1.85 + (155 / self.k_ow)))
        return self.ew_beninv

    def k1_beninv_f(self):
        """
        Uptake rate constant through respiratory area for benthic invertebrates
        :return:
        """
        self.k1_beninv = ((self.ew_beninv * self.gv_beninv) / self.wb_beninv)
        return self.k1_beninv

    def k_bw_beninv_f(self):
        """
        Benthic invertebrate water partition coefficient
        :return:
        """
        self.k_bw_beninv = (self.v_lb_beninv * self.k_ow) + (self.v_nb_beninv * 0.035 * self.k_ow) + self.v_wb_beninv
        return self.k_bw_beninv

    def k2_beninv_f(self):
        """
        Elimination rate constant through the gills for zooplankton
        :return:
        """
        self.k2_beninv = self.k1_beninv / self.k_bw_beninv
        return self.k2_beninv

    def ed_beninv_f(self):
        """
        Zoo plankton dietary pesticide transfer efficiency
        :return:
        """
        self.ed_beninv = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_beninv

    def gd_beninv_f(self):
        """
        Zooplankton feeding rate
        :return:
        """
        self.gd_beninv = 0.022 * self.wb_beninv ** 0.85 * math.exp(0.06 * self.w_t)
        return self.gd_beninv

    def kd_beninv_f(self):
        """
        Zooplankton rate constant pesticide uptake by food ingestion
        :return:
        """
        self.kd_beninv = self.ed_beninv * (self.gd_beninv / self.wb_beninv)
        return self.kd_beninv

    def kg_beninv_f(self):
        """
        Benthic invertebrate growth rate constant
        :return:
        """
        if self.w_t < 17.5:
            self.kg_beninv = 0.0005 * self.wb_beninv ** -0.2
        else:
            self.kg_beninv = 0.00251 * self.wb_beninv ** -0.2
        return self.kg_beninv

    def v_ld_beninv_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_beninv = self.beninv_p_sediment * self.s_lipid + self.beninv_p_phytoplankton * self.v_lb_phytoplankton + self.beninv_p_zooplankton * self.v_lb_zoo
        return self.v_ld_beninv

    def v_nd_beninv_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_beninv = self.beninv_p_sediment * self.s_NLOM + self.beninv_p_phytoplankton * self.v_nb_phytoplankton + self.beninv_p_zooplankton * self.v_nb_zoo
        return self.v_nd_beninv

    def v_wd_beninv_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_beninv = self.beninv_p_sediment * self.s_water + self.beninv_p_phytoplankton * self.v_wb_phytoplankton + self.beninv_p_zooplankton * self.v_wb_zoo
        return self.v_wd_beninv

    def gf_beninv_f(self):
        """
        Egestion rate of fecal matter
        :return:
        """
        self.gf_beninv = ((1 - 0.75) * self.v_ld_beninv + (1 - 0.75) * self.v_nd_beninv + (
            1 - 0.25) * self.v_wd_beninv) * self.gd_beninv
        return self.gf_beninv

    def vlg_beninv_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_beninv = (1 - 0.75) * self.v_ld_beninv * self.gd_beninv / self.gf_beninv
        return self.vlg_beninv

    def vng_beninv_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_beninv = (1 - 0.75) * self.v_nd_beninv * self.gd_beninv / self.gf_beninv
        return self.vng_beninv

    def vwg_beninv_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_beninv = (1 - 0.25) * self.v_wd_beninv * self.gd_beninv / self.gf_beninv
        return self.vwg_beninv
        # partition coefficient of the pesticide between the gastrointenstinal track and the organism

    def kgb_beninv_f(self):
        """
        Kgb ben inverts
        :return:
        """
        self.kgb_beninv = (self.vlg_beninv * self.k_ow + self.vng_beninv * 0.035 * self.k_ow + self.vwg_beninv) / (
            self.v_lb_beninv * self.k_ow + self.v_nb_beninv * 0.035 * self.k_ow + self.v_wb_beninv)
        return self.kgb_beninv

    def ke_beninv_f(self):
        """
        Dietary elimination rate constant
        :return:
        """
        self.ke_beninv = self.gf_beninv * self.ed_beninv * (self.kgb_beninv / self.wb_beninv)
        return self.ke_beninv

    def diet_beninv_f(self):
        """
        Diet fraction benthic inverts
        :return:
        """
        self.diet_beninv = self.c_s * self.beninv_p_sediment + self.cb_phytoplankton * self.beninv_p_phytoplankton + self.cb_zoo * self.beninv_p_zooplankton
        return self.diet_beninv

    def cb_beninv_f(self):
        """
        Benthic invertebrates pesticide tissue residue
        :return:
        """
        self.cb_beninv = (self.k1_beninv * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv) / (
                             self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)
        return self.cb_beninv

    def cbl_beninv_f(self):
        """
        Benthic invertebrates
        :return:
        """
        self.cbl_beninv = (1e6 * self.cb_beninv) / self.v_lb_beninv
        return self.cbl_beninv

    def cbd_beninv_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_beninv = (0 * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv) / (
                              self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)
        return self.cbd_beninv

    def cbr_beninv_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_beninv = (self.k1_beninv * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_beninv) / (
                              self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)
        return self.cbr_beninv

    def cbf_beninv_f(self):
        """
        Benthic invertebrate total bioconcentration factor
        :return:
        """
        self.kd_beninv = 0
        self.ke_beninv = 0
        # km_beninv = 0    is always 0
        self.kg_beninv = 0
        self.cbf_beninv = ((self.k1_beninv * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv) / (
                               self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)) / self.c_wto
        return self.cbf_beninv

    def cbfl_beninv_f(self):
        """
        Benthic invertebrate lipid normalized total bioconcentration factor
        :return:
        """
        self.kd_beninv = 0
        self.ke_beninv = 0
        # km_beninv = 0    is always 0
        self.kg_beninv = 0
        self.cbfl_beninv = (((self.k1_beninv * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_beninv * self.diet_beninv)) / self.v_lb_beninv / (
                                self.k2_beninv + self.ke_beninv + self.kg_beninv + 0)) / (self.c_wto * self.phi)
        return self.cbfl_beninv

    def cbaf_beninv_f(self):
        """
        Benthic invertebrates bioaccumulation factor
        :return:
        """
        self.cbaf_beninv = (1e6 * self.cb_beninv) / self.water_column_EEC
        return self.cbaf_beninv

    def cbafl_beninv_f(self):
        """
        Benthic invertebrate lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_beninv = self.cbl_beninv / self.water_d
        return self.cbafl_beninv

    def cbsafl_beninv_f(self):
        """
        Benthic inverts
        :return:
        """
        self.cbsafl_beninv = (self.cb_beninv / self.v_lb_beninv) / self.sed_om
        return self.cbsafl_beninv

    def bmf_beninv_f(self):
        """
        Benthic invertebrates biomagnification factor
        :return:
        """
        self.bmf_beninv = (self.cb_beninv / self.v_lb_beninv) / (
            (self.beninv_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (
                self.beninv_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.bmf_beninv

    #####################################################
    ###### filter feeders
    ################################################
    def gv_ff_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_ff = (1400.0 * ((self.wb_ff ** 0.65) / self.c_ox))
        return self.gv_ff

    def ew_ff_f(self):
        """
        Rate constant for elimination through the gills for filter feeders
        :return:
        """
        self.ew_ff = (1.0 / (1.85 + (155.0 / self.k_ow)))
        return self.ew_ff

    def k1_ff_f(self):
        """
        Uptake rate constant through respiratory area for filter feeders
        :return:
        """
        self.k1_ff = ((self.ew_ff * self.gv_ff) / self.wb_ff)
        return self.k1_ff

    def k_bw_ff_f(self):
        """
        Filter feeder water partition coefficient
        :return:
        """
        self.k_bw_ff = (self.v_lb_ff * self.k_ow) + (self.v_nb_ff * 0.035 * self.k_ow) + self.v_wb_ff
        return self.k_bw_ff

    def k2_ff_f(self):
        """
        Elimination rate constant through the gills for filter feeders
        :return:
        """
        self.k2_ff = self.k1_ff / self.k_bw_ff
        return self.k2_ff

    def ed_ff_f(self):
        """
        Filter feeder dietary pesticide transfer efficiency
        :return:
        """
        self.ed_ff = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_ff

    def gd_ff_f(self):
        """
        Filter feeder feeding rate
        :return:
        """
        self.gd_ff = self.gv_ff * self.c_ss * 1
        return self.gd_ff

    def kd_ff_f(self):
        """
        Filter feeder rate constant pesticide uptake by food ingestion
        :return:
        """
        self.kd_ff = self.ed_ff * (self.gd_ff / self.wb_ff)
        return self.kd_ff

    def kg_ff_f(self):
        """
        Filter feeder growth rate constant
        :return:
        """
        if self.w_t < 17.5:
            self.kg_ff = 0.0005 * self.wb_ff ** -0.2
        else:
            self.kg_ff = 0.00251 * self.wb_ff ** -0.2
        return self.kg_ff

    def v_ld_ff_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_ff = self.ff_p_sediment * self.s_lipid + self.ff_p_phytoplankton * self.v_lb_phytoplankton + self.ff_p_zooplankton * self.v_lb_zoo
        return self.v_ld_ff

    def v_nd_ff_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_ff = self.ff_p_sediment * self.s_NLOM + self.ff_p_phytoplankton * self.v_nb_phytoplankton + self.ff_p_zooplankton * self.v_nb_zoo
        return self.v_nd_ff

    def v_wd_ff_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_ff = self.ff_p_sediment * self.s_water + self.ff_p_phytoplankton * self.v_wb_phytoplankton + self.ff_p_zooplankton * self.v_wb_zoo
        return self.v_wd_ff

    def gf_ff_f(self):
        """
        Gf ff
        :return:
        """
        self.gf_ff = ((1 - 0.75) * self.v_ld_ff + (1 - 0.75) * self.v_nd_ff + (1 - 0.25) * self.v_wd_ff) * self.gd_ff
        return self.gf_ff

    def vlg_ff_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_ff = (1 - 0.75) * self.v_ld_ff * self.gd_ff / self.gf_ff
        return self.vlg_ff

    def vng_ff_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_ff = (1 - 0.75) * self.v_nd_ff * self.gd_ff / self.gf_ff
        return self.vng_ff

    def vwg_ff_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_ff = (1 - 0.25) * self.v_wd_ff * self.gd_ff / self.gf_ff
        return self.vwg_ff

    def kgb_ff_f(self):
        """
        Kgb ff
        :return:
        """
        self.kgb_ff = (self.vlg_ff * self.k_ow + self.vng_ff * 0.035 * self.k_ow + self.vwg_ff) / (
            self.v_lb_ff * self.k_ow + self.v_nb_ff * 0.035 * self.k_ow + self.v_wb_ff)
        return self.kgb_ff

    def ke_ff_f(self):
        """
        Ke ff
        :return:
        """
        self.ke_ff = (self.gf_ff * self.ed_ff * self.kgb_ff) / self.wb_ff
        return self.ke_ff

    def diet_ff_f(self):
        """
        Diet filter feeders
        :return:
        """
        self.diet_ff = self.c_s * self.ff_p_sediment + self.cb_phytoplankton * self.ff_p_phytoplankton + self.cb_zoo * self.ff_p_zooplankton + self.cb_beninv * self.ff_p_benthic_invertebrates
        return self.diet_ff

    def cb_ff_f(self):
        """
        Benthic invertebrates pesticide tissue residue
        :return:
        """
        self.cb_ff = (self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (
            self.k2_ff + self.ke_ff + self.kg_ff + 0)
        return self.cb_ff

    def cbl_ff_f(self):
        """
        Filter feeders
        :return:
        """
        self.cbl_ff = (1e6 * self.cb_ff) / self.v_lb_ff
        return self.cbl_ff

    def cbd_ff_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_ff = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (
            self.k2_ff + self.ke_ff + self.kg_ff + 0)
        return self.cbd_ff

    def cbr_ff_f(self):
        """
        Benthic invertebrates pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.kd_ff = 0
        self.cbr_ff = (self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_ff) / (
            self.k2_ff + self.ke_ff + self.kg_ff + 0)
        return self.cbr_ff

    def cbf_ff_f(self):
        """
        Filter feeder total bioconcentration factor
        :return:
        """
        self.kd_ff = 0
        self.ke_ff = 0
        #  km_ff = 0  is always = 0
        self.kg_ff = 0
        self.cbf_ff = ((self.k1_ff * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (
            self.k2_ff + self.ke_ff + self.kg_ff + 0)) / self.c_wto
        return self.cbf_ff

    def cbfl_ff_f(self):
        """
        Filter feeder lipid normalized bioconcentration factor
        :return:
        """
        self.kd_ff = 0
        self.ke_ff = 0
        #  km_ff = 0  is always = 0
        self.kg_ff = 0
        self.cbfl_ff = (((self.k1_ff * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_ff * self.diet_ff) / (
                             self.k2_ff + self.ke_ff + self.kg_ff + 0))) / self.v_lb_ff / (self.c_wto * self.phi)
        return self.cbfl_ff

    def cbaf_ff_f(self):
        """
        Filter feeder bioaccumulation factor
        :return:
        """
        self.cbaf_ff = (1e6 * self.cb_ff) / self.water_column_EEC
        return self.cbaf_ff

    def cbafl_ff_f(self):
        """
        Filter feeder lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_ff = self.cbl_ff / self.water_d
        return self.cbafl_ff

    def cbsafl_ff_f(self):
        """
        Filter feeder biota-sediment bioaccumulation factor
        :return:
        """
        self.cbsafl_ff = (self.cb_ff / self.v_lb_ff) / self.sed_om
        return self.cbsafl_ff

    def bmf_ff_f(self):
        """
        Filter feeder biomagnification factor
        :return:
        """
        self.bmf_ff = (self.cb_ff / self.v_lb_ff) / (
            (self.ff_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (
                self.ff_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (
                self.ff_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.bmf_ff

    #########################################################################
    ############# small fish
    def gv_sf_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_sf = (1400.0 * ((self.wb_sf ** 0.65) / self.c_ox))
        return self.gv_sf

    def ew_sf_f(self):
        """
        Rate constant for elimination through the gills for small fish
        :return:
        """
        self.ew_sf = (1.0 / (1.85 + (155.0 / self.k_ow)))
        return self.ew_sf

    def k1_sf_f(self):
        """
        Uptake rate constant through respiratory area for small fish
        :return:
        """
        self.k1_sf = ((self.ew_sf * self.gv_sf) / self.wb_sf)
        return self.k1_sf

    def k_bw_sf_f(self):
        """
        Small fish water partition coefficient
        :return:
        """
        self.k_bw_sf = (self.v_lb_sf * self.k_ow) + (self.v_nb_sf * 0.035 * self.k_ow) + self.v_wb_sf
        return self.k_bw_sf

    def k2_sf_f(self):
        """
        Elimination rate constant through the gills for small fish
        :return:
        """
        self.k2_sf = self.k1_sf / self.k_bw_sf
        return self.k2_sf

    def ed_sf_f(self):
        """
        Small fish dietary pesticide transfer efficiency
        :return:
        """
        self.ed_sf = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_sf

    def gd_sf_f(self):
        """
        Small fish feeding rate
        :return:
        """
        self.gd_sf = 0.022 * self.wb_sf ** 0.85 * math.exp(0.06 * self.w_t)
        return self.gd_sf

    def kd_sf_f(self):
        """
        Small fish rate constant pesticide uptake by food ingestion
        :return:
        """
        self.kd_sf = self.ed_sf * self.gd_sf / self.wb_sf
        return self.kd_sf

    def kg_sf_f(self):
        """
        Small fish growth rate constant
        :return:
        """
        if self.w_t < 17.5:
            self.kg_sf = 0.0005 * self.wb_sf ** -0.2
        else:
            self.kg_sf = 0.00251 * self.wb_sf ** -0.2
        return self.kg_sf

        # overall lipid content of diet

    def v_ld_sf_f(self):
        """
        Small fish lipid
        :return:
        """
        self.v_ld_sf = self.sf_p_sediment * self.s_lipid + self.sf_p_phytoplankton * self.v_lb_phytoplankton + self.sf_p_benthic_invertebrates * self.v_lb_beninv + self.sf_p_zooplankton * self.v_lb_zoo + self.sf_p_filter_feeders * self.v_lb_ff
        return self.v_ld_sf

    def v_nd_sf_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_sf = self.sf_p_sediment * self.s_NLOM + self.sf_p_phytoplankton * self.v_nb_phytoplankton + self.sf_p_benthic_invertebrates * self.v_nb_beninv + self.sf_p_zooplankton * self.v_nb_zoo + self.sf_p_filter_feeders * self.v_nb_ff
        return self.v_nd_sf

    def v_wd_sf_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_sf = self.sf_p_sediment * self.s_water + self.sf_p_phytoplankton * self.v_wb_phytoplankton + self.sf_p_benthic_invertebrates * self.v_wb_beninv + self.sf_p_zooplankton * self.v_wb_zoo + self.sf_p_filter_feeders * self.v_wb_ff
        return self.v_wd_sf

    def gf_sf_f(self):
        """
        Small fish
        :return:
        """
        self.gf_sf = ((1 - 0.92) * self.v_ld_sf + (1 - 0.6) * self.v_nd_sf + (1 - 0.25) * self.v_wd_sf) * self.gd_sf
        return self.gf_sf

    def vlg_sf_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_sf = (1 - 0.92) * self.v_ld_sf * self.gd_sf / self.gf_sf
        return self.vlg_sf

    def vng_sf_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_sf = (1 - 0.6) * self.v_nd_sf * self.gd_sf / self.gf_sf
        return self.vng_sf

    def vwg_sf_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_sf = (1 - 0.25) * self.v_wd_sf * self.gd_sf / self.gf_sf
        return self.vwg_sf

    def kgb_sf_f(self):
        """
        Small fish
        :return:
        """
        self.kgb_sf = (self.vlg_sf * self.k_ow + self.vng_sf * 0.035 * self.k_ow + self.vwg_sf) / (
            self.v_lb_sf * self.k_ow + self.v_nb_sf * 0.035 * self.k_ow + self.v_wb_sf)
        return self.kgb_sf

    def ke_sf_f(self):
        """
        Small fish
        :return:
        """
        self.ke_sf = self.gf_sf * self.ed_sf * (self.kgb_sf / self.wb_sf)
        return self.ke_sf

    def diet_sf_f(self):
        """
        Diet small fish
        :return:
        """
        self.diet_sf = self.c_s * self.sf_p_sediment + self.cb_phytoplankton * self.sf_p_phytoplankton + self.cb_zoo * self.sf_p_zooplankton + self.cb_beninv * self.sf_p_benthic_invertebrates + self.cb_ff * self.sf_p_filter_feeders
        return self.diet_sf


    def cb_sf_f(self):
        """
        Small fish pesticide tissue residue
        :return:
        """
        self.cb_sf = (self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (
            self.k2_sf + self.ke_sf + self.kg_sf + 0)
        return self.cb_sf

    def cbl_sf_f(self):
        """
        Small fish lipid normalized pesticide tissue residue
        :return:
        """
        self.cbl_sf = (1e6 * self.cb_sf) / self.v_lb_sf
        return self.cbl_sf

    def cbd_sf_f(self):
        """
        Small fish pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_sf = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (
            self.k2_sf + self.ke_sf + self.kg_sf + 0)
        return self.cbd_sf

    def cbr_sf_f(self):
        """
        Small fish pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_sf = (self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_sf) / (
            self.k2_sf + self.ke_sf + self.kg_sf + 0)
        return self.cbr_sf

    def cbf_sf_f(self):
        """
        Small fish total bioconcentration factor
        :return:
        """
        self.kd_sf = 0
        self.ke_sf = 0
        #    km_sf = 0 always = 0
        self.kg_sf = 0
        self.cbf_sf = ((self.k1_sf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (
            self.k2_sf + self.ke_sf + self.kg_sf + 0)) / self.c_wto
        return self.cbf_sf

    def cbfl_sf_f(self):
        """
        Small fish lipid normalized bioconcentration factor
        :return:
        """
        self.kd_sf = 0
        self.ke_sf = 0
        #    km_sf = 0 always = 0
        self.kg_sf = 0
        self.cbfl_sf = (((self.k1_sf * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_sf * self.diet_sf) / (
                             self.k2_sf + self.ke_sf + self.kg_sf + 0)) / self.v_lb_sf) / (self.c_wto * self.phi)
        return self.cbfl_sf

    def cbaf_sf_f(self):
        """
        Small fish bioaccumulation factor
        :return:
        """
        self.cbaf_sf = (1e6 * self.cb_sf) / self.water_column_EEC
        return self.cbaf_sf

    def cbafl_sf_f(self):
        """
        Small fish lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_sf = self.cbl_sf / self.water_d
        return self.cbafl_sf

    def cbsafl_sf_f(self):
        """
        Small fish
        :return:
        """
        self.cbsafl_sf = (self.cb_sf / self.v_lb_sf) / self.sed_om
        return self.cbsafl_sf

    def bmf_sf_f(self):
        """
        Small fish biomagnification factor
        :return:
        """
        self.bmf_sf = (self.cb_sf / self.v_lb_sf) / ((self.sf_p_filter_feeders * self.cb_ff / self.v_lb_ff) + (
            self.sf_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (
                                                         self.sf_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (
                                                         self.sf_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.bmf_sf

    ############ medium fish
    def gv_mf_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_mf = (1400.0 * ((self.wb_mf ** 0.65) / self.c_ox))
        return self.gv_mf

    def ew_mf_f(self):
        """
        Rate constant for elimination through the gills for medium fish
        :return:
        """
        self.ew_mf = (1.0 / (1.85 + (155.0 / self.k_ow)))
        return self.ew_mf

    def k1_mf_f(self):
        """
        Uptake rate constant through respiratory area for medium fish
        :return:
        """
        self.k1_mf = ((self.ew_mf * self.gv_mf) / self.wb_mf)
        return self.k1_mf

    def k_bw_mf_f(self):
        """
        Medium fish water partition coefficient
        :return:
        """
        self.k_bw_mf = (self.v_lb_mf * self.k_ow) + (self.v_nb_mf * 0.035 * self.k_ow) + self.v_wb_mf
        return self.k_bw_mf

    def k2_mf_f(self):
        """
        Elimination rate constant through the gills for medium fish
        :return:
        """
        self.k2_mf = self.k1_mf / self.k_bw_mf
        return self.k2_mf

    def ed_mf_f(self):
        """
        Medium fish dietary pesticide transfer efficiency
        :return:
        """
        self.ed_mf = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_mf

    def gd_mf_f(self):
        """
        Medium fish feeding rate
        :return:
        """
        self.gd_mf = 0.022 * self.wb_mf ** 0.85 * math.exp(0.06 * self.w_t)
        return self.gd_mf

    def kd_mf_f(self):
        """
        Medium fish rate constant pesticide uptake by food ingestion
        :return:
        """
        self.kd_mf = self.ed_mf * self.gd_mf / self.wb_mf
        return self.kd_mf

    def kg_mf_f(self):
        """
        Medium fish growth rate constant
        :return:
        """
        if self.w_t < 17.5:
            self.kg_mf = 0.0005 * self.wb_mf ** -0.2
        else:
            self.kg_mf = 0.00251 * self.wb_mf ** -0.2
        return self.kg_mf

    def v_ld_mf_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_mf = self.mf_p_sediment * self.s_lipid + self.mf_p_phytoplankton * self.v_lb_phytoplankton + self.mf_p_benthic_invertebrates * self.v_lb_beninv + self.mf_p_zooplankton * self.v_lb_zoo + self.mf_p_filter_feeders * self.v_lb_ff + self.mf_p_small_fish * self.v_lb_sf
        return self.v_ld_mf

    def v_nd_mf_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_mf = self.mf_p_sediment * self.s_NLOM + self.mf_p_phytoplankton * self.v_nb_phytoplankton + self.mf_p_benthic_invertebrates * self.v_nb_beninv + self.mf_p_zooplankton * self.v_nb_zoo + self.mf_p_filter_feeders * self.v_nb_ff + self.mf_p_small_fish * self.v_nb_sf
        return self.v_nd_mf

    def v_wd_mf_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_mf = self.mf_p_sediment * self.s_water + self.mf_p_phytoplankton * self.v_wb_phytoplankton + self.mf_p_benthic_invertebrates * self.v_wb_beninv + self.mf_p_zooplankton * self.v_wb_zoo + self.mf_p_filter_feeders * self.v_wb_ff + self.mf_p_small_fish * self.v_wb_sf
        return self.v_wd_mf

    def gf_mf_f(self):
        """
        Medium fish
        :return:
        """
        self.gf_mf = ((1 - 0.92) * self.v_ld_mf + (1 - 0.6) * self.v_nd_mf + (1 - 0.25) * self.v_wd_mf) * self.gd_mf
        return self.gf_mf

    def vlg_mf_f(self):
        """
    # lipid content in gut
        :return:
        """
        self.vlg_mf = (1 - 0.92) * self.v_ld_mf * self.gd_mf / self.gf_mf
        return self.vlg_mf

    def vng_mf_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_mf = (1 - 0.6) * self.v_nd_mf * self.gd_mf / self.gf_mf
        return self.vng_mf

    def vwg_mf_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_mf = (1 - 0.25) * self.v_wd_mf * self.gd_mf / self.gf_mf
        return self.vwg_mf

    def kgb_mf_f(self):
        """
        Medium fish
        :return:
        """
        self.kgb_mf = (self.vlg_mf * self.k_ow + self.vng_mf * 0.035 * self.k_ow + self.vwg_mf) / (
            self.v_lb_mf * self.k_ow + self.v_nb_mf * 0.035 * self.k_ow + self.v_wb_mf)
        return self.kgb_mf

    def ke_mf_f(self):
        """

        :return:
        """
        self.ke_mf = self.gf_mf * self.ed_mf * (self.kgb_mf / self.wb_mf)
        return self.ke_mf

    def diet_mf_f(self):
        """
        Diet medium fish
        :return:
        """
        self.diet_mf = self.c_s * self.mf_p_sediment + self.cb_phytoplankton * self.mf_p_phytoplankton + self.cb_zoo * self.mf_p_zooplankton + self.cb_beninv * self.mf_p_benthic_invertebrates + self.cb_ff * self.mf_p_filter_feeders + self.cb_sf * self.mf_p_small_fish
        return self.diet_mf

    def cb_mf_f(self):
        """
        Medium fish pesticide tissue residue
        :return:
        """
        self.cb_mf = (self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (
            self.k2_mf + self.ke_mf + self.kg_mf + 0)
        return self.cb_mf

    def cbl_mf_f(self):
        """
        Medium fish lipid normalized pesticide tissue residue
        :return:
        """
        self.cbl_mf = (1e6 * self.cb_mf) / self.v_lb_mf
        return self.cbl_mf

    def cbd_mf_f(self):
        """
        Medium fish pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_mf = (0 * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (
            self.k2_mf + self.ke_mf + self.kg_mf + 0)
        return self.cbd_mf

    def cbr_mf_f(self):
        """
        Medium fish pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_mf = (self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + 0 * self.diet_mf) / (
            self.k2_mf + self.ke_mf + self.kg_mf + 0)
        return self.cbr_mf

    def cbf_mf_f(self):
        """
        Medium fish total bioconcentration factor
        :return:
        """
        self.kd_mf = 0
        self.ke_mf = 0
        # km_mf = 0    
        self.kg_mf = 0
        self.cbf_mf = ((self.k1_mf * (0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (
            self.k2_mf + self.ke_mf + self.kg_mf + 0)) / self.c_wto
        return self.cbf_mf

    def cbfl_mf_f(self):
        """
        Medium fish lipid normalized bioconcentration factor
        :return:
        """
        self.kd_mf = 0
        self.ke_mf = 0
        # km_mf = 0    
        self.kg_mf = 0
        self.cbfl_mf = ((((self.k1_mf * (
            0.95 * self.phi * self.c_wto + 0.05 * self.c_wdp) + self.kd_mf * self.diet_mf) / (
                              self.k2_mf + self.ke_mf + self.kg_mf + 0))) / self.v_lb_mf) / (self.c_wto * self.phi)
        return self.cbfl_mf

    def cbaf_mf_f(self):
        """
        Medium fish bioaccumulation factor
        :return:
        """
        self.cbaf_mf = (1e6 * self.cb_mf) / self.water_column_EEC
        return self.cbaf_mf

    def cbafl_mf_f(self):
        """
        Medium fish lipid normalized factor
        :return:
        """
        self.cbafl_mf = self.cbl_mf / self.water_d
        return self.cbafl_mf

    def cbsafl_mf_f(self):
        """
        Medium fish
        :return:
        """
        self.cbsafl_mf = (self.cb_mf / self.v_lb_mf) / self.sed_om
        return self.cbsafl_mf

    def cbmf_mf_f(self):
        """
        Medium fish biomagnification factor
        :return:
        """
        self.cbmf_mf = (self.cb_mf / self.v_lb_mf) / (
            (self.mf_p_small_fish * self.cb_sf / self.v_lb_sf) + (
            self.mf_p_filter_feeders * self.cb_ff / self.v_lb_ff) + (
                self.mf_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (
                self.mf_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (
                self.mf_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.cbmf_mf

    ############ large fish
    def gv_lf_f(self):
        """
        Ventilation rate
        :return:
        """
        self.gv_lf = (1400.0 * ((self.wb_lf ** 0.65) / self.c_ox))
        return self.gv_lf

    def ew_lf_f(self):
        """
        Rate constant for elimination through the gills for large fish
        :return:
        """
        self.ew_lf = (1.0 / (1.85 + (155.0 / self.k_ow)))
        return self.ew_lf

    def k1_lf_f(self):
        """
        Uptake rate constant through respiratory area for large fish
        :return:
        """
        self.k1_lf = ((self.ew_lf * self.gv_lf) / self.wb_lf)
        return self.k1_lf

    def k_bw_lf_f(self):
        """
        Large fish water partition coefficient
        :return:
        """
        self.k_bw_lf = (self.v_lb_lf * self.k_ow) + (self.v_nb_lf * 0.035 * self.k_ow) + self.v_wb_lf
        return self.k_bw_lf

    def k2_lf_f(self):
        """
        Elimination rate constant through the gills for large fish
        :return:
        """
        self.k2_lf = self.k1_lf / self.k_bw_lf
        return self.k2_lf

    def ed_lf_f(self):
        """
        Large fish dietary pesticide transfer efficiency
        :return:
        """
        self.ed_lf = 1 / (.0000003 * self.k_ow + 2.0)
        return self.ed_lf

    def gd_lf_f(self):
        """
        Large fish feeding rate
        :return:
        """
        self.gd_lf = 0.022 * self.wb_lf ** 0.85 * math.exp(0.06 * self.w_t)
        return self.gd_lf

    def kd_lf_f(self):
        """
        Large fish rate constant pesticide uptake by food ingestion
        :return:
        """
        self.kd_lf = self.ed_lf * self.gd_lf / self.wb_lf
        return self.kd_lf

    def kg_lf_f(self):
        """
        Medium fish growth rate constant
        :return:
        """
        if self.w_t < 17.5:
            self.kg_lf = 0.0005 * self.wb_lf ** -0.2
        else:
            self.kg_lf = 0.00251 * self.wb_lf ** -0.2
        return self.kg_lf

    def v_ld_lf_f(self):
        """
        Overall lipid content of diet
        :return:
        """
        self.v_ld_lf = self.lf_p_sediment * self.s_lipid + self.lf_p_phytoplankton * self.v_lb_phytoplankton + self.lf_p_benthic_invertebrates * self.v_lb_beninv + self.lf_p_zooplankton * self.v_lb_zoo + self.lf_p_filter_feeders * self.v_lb_ff + self.lf_p_small_fish * self.v_lb_sf + self.lf_p_medium_fish * self.v_lb_mf
        return self.v_ld_lf

    def v_nd_lf_f(self):
        """
        Overall nonlipid content of diet
        :return:
        """
        self.v_nd_lf = self.lf_p_sediment * self.s_NLOM + self.lf_p_phytoplankton * self.v_nb_phytoplankton + self.lf_p_benthic_invertebrates * self.v_nb_beninv + self.lf_p_zooplankton * self.v_nb_zoo + self.lf_p_filter_feeders * self.v_nb_ff + self.lf_p_small_fish * self.v_nb_sf + self.lf_p_medium_fish * self.v_nb_mf
        return self.v_nd_lf

    def v_wd_lf_f(self):
        """
        Overall water content of diet
        :return:
        """
        self.v_wd_lf = self.lf_p_sediment * self.s_water + self.lf_p_phytoplankton * self.v_wb_phytoplankton + self.lf_p_benthic_invertebrates * self.v_wb_beninv + self.lf_p_zooplankton * self.v_wb_zoo + self.lf_p_filter_feeders * self.v_wb_ff + self.lf_p_small_fish * self.v_wb_sf + self.lf_p_medium_fish * self.v_wb_mf
        return self.v_wd_lf

    def gf_lf_f(self):
        """
        Large fiah
        :return:
        """
        self.gf_lf = ((1 - 0.92) * self.v_ld_lf + (1 - 0.6) * self.v_nd_lf + (1 - 0.25) * self.v_wd_lf) * self.gd_lf
        return self.gf_lf

    def vlg_lf_f(self):
        """
        Lipid content in gut
        :return:
        """
        self.vlg_lf = (1 - 0.92) * self.v_ld_lf * self.gd_lf / self.gf_lf
        return self.vlg_lf

    def vng_lf_f(self):
        """
        Non lipid content in gut
        :return:
        """
        self.vng_lf = (1 - 0.6) * self.v_nd_lf * self.gd_lf / self.gf_lf
        return self.vng_lf

    def vwg_lf_f(self):
        """
        Water content in the gut
        :return:
        """
        self.vwg_lf = (1 - 0.25) * self.v_wd_lf * self.gd_lf / self.gf_lf
        return self.vwg_lf

    def kgb_lf_f(self):
        """
        Large fish
        :return:
        """
        self.kgb_lf = (self.vlg_lf * self.k_ow + self.vng_lf * 0.035 * self.k_ow + self.vwg_lf) / (
            self.v_lb_lf * self.k_ow + self.v_nb_lf * 0.035 * self.k_ow + self.v_wb_lf)
        return self.kgb_lf

    def ke_lf_f(self):
        """
        Large fish
        :return:
        """
        self.ke_lf = self.gf_lf * self.ed_lf * (self.kgb_lf / self.wb_lf)
        return self.ke_lf

    def diet_lf_f(self):
        """
        Large fish
        :return:
        """
        self.diet_lf = self.c_s * self.lf_p_sediment + self.cb_phytoplankton * self.lf_p_phytoplankton + self.cb_zoo * self.lf_p_zooplankton + self.cb_beninv * self.lf_p_benthic_invertebrates + self.cb_ff * self.lf_p_filter_feeders + self.cb_sf * self.lf_p_small_fish + self.cb_mf * self.lf_p_medium_fish
        return self.diet_lf

    def cb_lf_f(self):
        """
        Large fish pesticide tissue residue
        :return:
        """
        self.cb_lf = (self.k1_lf * (1.0 * self.phi * self.c_wto + 0.00 * self.c_wdp) + self.kd_lf * self.diet_lf) / (
            self.k2_lf + self.ke_lf + self.kg_lf + 0)
        return self.cb_lf

    def cbl_lf_f(self):
        """
        Large fish lipid normalized pesticide tissue residue
        :return:
        """
        self.cbl_lf = (1e6 * self.cb_lf) / self.v_lb_lf
        return self.cbl_lf

    def cbd_lf_f(self):
        """
        Large fish pesticide concentration originating from uptake through diet k1=0
        :return:
        """
        self.cbd_lf = (0 * (1.0 * self.phi * self.c_wto + 0.0 * self.c_wdp) + self.kd_lf * self.diet_lf) / (
            self.k2_lf + self.ke_lf + self.kg_lf + 0)
        return self.cbd_lf

    def cbr_lf_f(self):
        """
        Large fish pesticide concentration originating from uptake through respiration (kd=0)
        :return:
        """
        self.cbr_lf = (self.k1_lf * (1.0 * self.phi * self.c_wto + 0.0 * self.c_wdp) + 0 * self.diet_lf) / (
            self.k2_lf + self.ke_lf + self.kg_lf + 0)
        return self.cbr_lf

    def cbf_lf_f(self):
        """
        Large fish total bioconcentration factor
        :return:
        """
        self.kd_lf = 0
        self.ke_lf = 0
        # km_lf = 0
        self.kg_lf = 0
        self.cbf_lf = ((self.k1_lf * (1.0 * self.phi * self.c_wto + 0.00 * self.c_wdp) + self.kd_lf * self.diet_lf) / (
            self.k2_lf + self.ke_lf + self.kg_lf + 0)) / self.c_wto
        return self.cbf_lf

    def cbfl_lf_f(self):
        """
        Large fish lipid normalized total bioconcentration factor
        :return:
        """
        self.kd_lf = 0
        self.ke_lf = 0
        # km_lf = 0
        self.kg_lf = 0
        self.cbfl_lf = ((
                            (self.k1_lf * (
                            1.0 * self.phi * self.c_wto + 0.00 * self.c_wdp) + self.kd_lf * self.diet_lf) / (
                                self.k2_lf + self.ke_lf + self.kg_lf + 0)) / self.v_lb_lf) / (self.c_wto * self.phi)
        return self.cbfl_lf

    def cbaf_lf_f(self):
        """
        Large fish bioaccumulation factor
        :return:
        """
        self.cbaf_lf = (1e6 * self.cb_lf) / self.water_column_EEC
        return self.cbaf_lf

    def cbafl_lf_f(self):
        """
        Large fish lipid normalized bioaccumulation factor
        :return:
        """
        self.cbafl_lf = self.cbl_lf / self.water_d
        return self.cbafl_lf

    def cbsafl_lf_f(self):
        """
        Large fish biota-sediment accumulation factors
        :return:
        """
        self.cbsafl_lf = (self.cb_lf / self.v_lb_lf) / self.sed_om
        return self.cbsafl_lf

    def cbmf_lf_f(self):
        """
        Large fish biomagnification factor
        :return:
        """
        self.cbmf_lf = (self.cb_lf / self.v_lb_lf) / (
            (self.lf_p_medium_fish * self.cb_mf / self.v_lb_mf) + (self.lf_p_small_fish * self.cb_sf / self.v_lb_sf) + (
                self.lf_p_filter_feeders * self.cb_ff / self.v_lb_ff) + (
                self.lf_p_benthic_invertebrates * self.cb_beninv / self.v_lb_beninv) + (
                self.lf_p_zooplankton * self.cb_zoo / self.v_lb_zoo) + (
                self.lf_p_phytoplankton * self.cb_phytoplankton / self.v_lb_phytoplankton))
        return self.cbmf_lf

    ################################## Mammals EECs
    def mweight_f(self):
        """
        Mammals
        :return:
        """
        self.cb_a = np.array(
            [[self.cb_phytoplankton, self.cb_zoo, self.cb_beninv, self.cb_ff, self.cb_sf, self.cb_mf, self.cb_lf]])
        self.cb_a2 = self.cb_a * 1000000
        # array of mammal weights
        self.mweight = np.array([[0.018, 0.085, 0.45, 1.8, 5, 15]])
        return self.mweight

    def dfir_f(self):
        """
        Mammals
        :return:
        """
        self.dfir = (0.0687 * self.mweight ** 0.822) / self.mweight
        return self.dfir

    def wet_food_ingestion_m_f(self):
        """
        Mammals
        :return:
        """
        # creation of array for mammals of dry food ingestion rate
        # array of percent water in biota
        self.v_wb_a = np.array([[self.v_wb_phytoplankton, self.v_wb_zoo, self.v_wb_beninv, self.v_wb_ff, self.v_wb_sf,
                                 self.v_wb_mf, self.v_wb_lf]])
        # array of % diet of food web for each mammal
        self.diet_mammal = np.array(
            [[0, 0, 1, 0, 0, 0, 0], [0, 0, .34, .33, .33, 0, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0],
             [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])
        self.denom1 = self.diet_mammal * self.v_wb_a
        self.denom1 = (
            [[0., 0., 0.76, 0., 0., 0., 0.], [0., 0., 0.2584, 0.2805, 0.2409, 0., 0.], [0., 0., 0., 0., 0., 0.73, 0.],
             [0., 0., 0., 0., 0., 0.73, 0.], [0., 0., 0., 0., 0., 0.73, 0.], [0., 0., 0., 0., 0., 0., 0.73]])
        self.denom2 = np.cumsum(self.denom1, axis=1)
        self.denom3 = self.denom2[:,
                      6]  # selects out seventh row of array which is the cumulative sums of the products
        self.denom4 = 1 - self.denom3
        # wet food ingestion rate for mammals
        self.wet_food_ingestion_m = self.dfir / self.denom4
        return self.wet_food_ingestion_m

    def drinking_water_intake_m_f(self):
        """
        Array of drinking water intake rate for mammals
        :return:
        """
        self.drinking_water_intake_m = .099 * self.mweight ** 0.9
        return self.drinking_water_intake_m

    def db4_f(self):
        """
        Mammals
        :return:
        """
        self.db1 = self.cb_a2 * self.diet_mammal
        self.db2 = np.cumsum(self.db1, axis=1)
        self.db3 = self.db2[:, 6]
        # dose based  EEC
        self.db4 = (self.db3 / 1000) * self.wet_food_ingestion_m + (self.water_column_EEC / 1000) * (
            self.drinking_water_intake_m / self.mweight)
        return self.db4

    def db5_f(self):
        """
        Mammals
        :return:
        """
        # dietary based EEC
        self.db5 = self.db3 / 1000
        return self.db5

    ################################## Avian EECs
    def aweight_f(self):
        """
        Avian
        :return:
        """
        self.aweight = np.array([[0.02, 6.7, 0.07, 2.9, 1.25, 7.5]])
        return self.aweight

    def dfir_a_f(self):
        """
        Avian
        :return:
        """
        self.dfir_a = (0.0582 * self.aweight ** 0.651) / self.aweight
        return self.dfir_a

    def wet_food_ingestion_a_f(self):
        """
        Avian
        :return:
        """
        self.v_wb_a = np.array([[self.v_wb_phytoplankton, self.v_wb_zoo, self.v_wb_beninv, self.v_wb_ff, self.v_wb_sf,
                                 self.v_wb_mf, self.v_wb_lf]])
        self.diet_avian = np.array(
            [[0, 0, .33, 0.33, 0.34, 0, 0], [0, 0, .33, .33, 0, 0.34, 0], [0, 0, 0.5, 0, 0.5, 0, 0],
             [0, 0, 0.5, 0, 0, 0.5, 0], [0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 1]])
        self.denom1a = self.diet_avian * self.v_wb_a
        self.denom2a = np.cumsum(self.denom1a, axis=1)
        self.denom3a = self.denom2a[:,
                       6]  # selects out seventh row of array which is the cumulative sums of the products
        self.denom4a = 1 - self.denom3a
        self.wet_food_ingestion_a = self.dfir_a / self.denom4a
        return self.wet_food_ingestion_a

    def drinking_water_intake_a_f(self):
        """
        Avian drinking water intake
        :return:
        """
        self.drinking_water_intake_a = 0.059 * self.aweight ** 0.67
        return self.drinking_water_intake_a

    def db4a_f(self):
        """
        Avian
        :return:
        """
        self.db1a = self.cb_a2 * self.diet_avian
        self.db2a = np.cumsum(self.db1a, axis=1)
        self.db3a = self.db2a[:, 6]
        # dose based  EEC
        self.db4a = (self.db3a / 1000) * self.wet_food_ingestion_a + (self.water_column_EEC / 1000) * (
            self.drinking_water_intake_a / self.aweight)
        return self.db4a

    def db5a_f(self):
        """
        Avian
        :return:
        """
        # dietary based EEC
        self.db5a = (self.db3a / 1000)
        return self.db5a

        ##################################### toxicity values
        #################################### mammal

    def acute_dose_based_m_f(self):
        """
        Dose based acute toxicity for mammals
        :return:
        """
        self.acute_dose_based_m = self.mammalian_ld50 * ((float(self.bw_mamm) / 1000) / self.mweight) ** 0.25
        return self.acute_dose_based_m

    def chronic_dose_based_m_f(self):
        """
        Dose based chronic toxicity for mammals
        :return:
        """
        self.chronic_dose_based_m = (self.mammalian_chronic_endpoint / 20) * (
            ((float(self.bw_mamm) / 1000) / self.mweight) ** 0.25)
        return self.chronic_dose_based_m

    def acute_dose_based_a_f(self):
        """
        Dose based acute toxicity for birds
        :return:
        """
        self.acute_dose_based_a = self.avian_ld50 * (self.aweight / (float(self.bw_bird) / 1000)) ** (
            self.mineau_scaling_factor - 1)
        return self.acute_dose_based_a

    ##################################### RQ Values
    def acute_rq_dose_m_f(self):
        """
        RQ dose based for mammals
        :return:
        """
        self.acute_rq_dose_m = self.db4 / self.acute_dose_based_m
        return self.acute_rq_dose_m

    def chronic_rq_dose_m_f(self):
        """
        Chronic RQ
        :return:
        """
        self.chronic_rq_dose_m = self.db4 / self.chronic_dose_based_m
        return self.chronic_rq_dose_m

    def acute_rq_diet_m_f(self):
        """
        Acute RQ diet based for mammals
        :return:
        """
        self.acute_rq_diet_m = self.db5 / self.mammalian_lc50
        return self.acute_rq_diet_m

    def chronic_rq_diet_m_f(self):
        """
        Chronic RQ diet based for mammals
        :return:
        """
        self.chronic_rq_diet_m = self.db5 / self.mammalian_chronic_endpoint
        return self.chronic_rq_diet_m

    def acute_rq_dose_a_f(self):
        """
        RQ dose based for birds
        :return:
        """
        self.acute_rq_dose_a = self.db4a / self.acute_dose_based_a
        return self.acute_rq_dose_a

    def acute_rq_diet_a_f(self):
        """
        RQ diet based for birds
        :return:
        """
        self.acute_rq_diet_a = self.db5a / self.avian_lc50
        return self.acute_rq_diet_a

    def chronic_rq_diet_a_f(self):
        """
        Chronic RQ diet for birds
        :return:
        """
        self.chronic_rq_diet_a = self.db5a / self.avian_noaec
        return self.chronic_rq_diet_a
