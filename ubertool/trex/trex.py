from __future__ import division
import numpy as np


class trex(object):
    def __init__(self, chem_name, use, formu_name, a_i, application_type, seed_treatment_formulation_name, seed_crop,
                 seed_crop_v, r_s, b_w, p_i, den, h_l, n_a, ar_lb, day_out,
                 ld50_bird, lc50_bird, noaec_bird, noael_bird, aw_bird_sm, aw_bird_md, aw_bird_lg,
                 species_of_the_tested_bird_avian_ld50, species_of_the_tested_bird_avian_lc50,
                 species_of_the_tested_bird_avian_noaec, species_of_the_tested_bird_avian_noael,
                 tw_bird_ld50, tw_bird_lc50, tw_bird_noaec, tw_bird_noael, x, ld50_mamm, lc50_mamm, noaec_mamm,
                 noael_mamm, aw_mamm_sm, aw_mamm_md, aw_mamm_lg, tw_mamm,
                 m_s_r_p):
        """
        constructor for trex model.
        :param chem_name:
        :param use:
        :param formu_name:
        :param a_i:
        :param application_type:
        :param seed_treatment_formulation_name:
        :param seed_crop:
        :param seed_crop_v:
        :param r_s:
        :param b_w:
        :param p_i:
        :param den:
        :param h_l:
        :param n_a:
        :param ar_lb:
        :param day_out:
        :param ld50_bird:
        :param lc50_bird:
        :param noaec_bird:
        :param noael_bird:
        :param aw_bird_sm:
        :param aw_bird_md:
        :param aw_bird_lg:
        :param species_of_the_tested_bird_avian_ld50:
        :param species_of_the_tested_bird_avian_lc50:
        :param species_of_the_tested_bird_avian_noaec:
        :param species_of_the_tested_bird_avian_noael:
        :param tw_bird_ld50:
        :param tw_bird_lc50:
        :param tw_bird_noaec:
        :param tw_bird_noael:
        :param x:
        :param ld50_mamm:
        :param lc50_mamm:
        :param noaec_mamm:
        :param noael_mamm:
        :param aw_mamm_sm:
        :param aw_mamm_md:
        :param aw_mamm_lg:
        :param tw_mamm:
        :param m_s_r_p:
        :return:
        """
        self.chem_name = chem_name
        self.use = use
        self.formu_name = formu_name
        self.a_i = a_i
        self.a_i_t1 = 100 * float(a_i)
        self.application_type = application_type
        self.seed_treatment_formulation_name = seed_treatment_formulation_name
        self.seed_crop = seed_crop
        self.seed_crop_v = seed_crop_v
        self.r_s = r_s
        self.b_w = b_w
        self.b_w_t1 = 12 * float(b_w)
        self.p_i = p_i
        try:
            self.p_i_t1 = 100 * float(p_i)
        except:
            self.p_i_t1 = 'N/a'
        self.den = den
        self.h_l = h_l
        self.n_a = n_a
        self.ar_lb = ar_lb
        self.day_out = day_out
        self.ld50_bird = ld50_bird
        self.lc50_bird = lc50_bird
        self.noaec_bird = noaec_bird
        self.noael_bird = noael_bird
        self.aw_bird_sm = aw_bird_sm
        self.aw_bird_md = aw_bird_md
        self.aw_bird_lg = aw_bird_lg

        self.species_of_the_tested_bird_avian_ld50 = species_of_the_tested_bird_avian_ld50
        self.species_of_the_tested_bird_avian_lc50 = species_of_the_tested_bird_avian_lc50
        self.species_of_the_tested_bird_avian_noaec = species_of_the_tested_bird_avian_noaec
        self.species_of_the_tested_bird_avian_noael = species_of_the_tested_bird_avian_noael

        self.tw_bird_ld50 = tw_bird_ld50
        self.tw_bird_lc50 = tw_bird_lc50
        self.tw_bird_noaec = tw_bird_noaec
        self.tw_bird_noael = tw_bird_noael
        self.x = x
        self.ld50_mamm = ld50_mamm
        self.lc50_mamm = lc50_mamm
        self.noaec_mamm = noaec_mamm
        self.noael_mamm = noael_mamm
        self.aw_mamm_sm = aw_mamm_sm
        self.aw_mamm_md = aw_mamm_md
        self.aw_mamm_lg = aw_mamm_lg
        self.tw_mamm = tw_mamm
        self.m_s_r_p = m_s_r_p
        # Result variables

        # Table5
        self.sa_bird_1_s = self.sa_bird_1(ar_lb[0], a_i, den, self.at_bird, self.fi_bird, 0.1, ld50_bird, aw_bird_sm,
                                          tw_bird_ld50, x, 0.02)
        self.sa_bird_2_s = self.sa_bird_2(ar_lb[0], a_i, den, m_s_r_p, self.at_bird, ld50_bird, aw_bird_sm,
                                          tw_bird_ld50, x, 0.02)
        self.sc_bird_s = self.sc_bird(ar_lb[0], a_i, den, noaec_bird)
        self.sa_mamm_1_s = self.sa_mamm_1(ar_lb[0], a_i, den, self.at_mamm, self.fi_mamm, 0.1, ld50_mamm, aw_mamm_sm,
                                          tw_mamm, 0.015)
        self.sa_mamm_2_s = self.sa_mamm_2(ar_lb[0], a_i, den, m_s_r_p, self.at_mamm, ld50_mamm, aw_mamm_sm, tw_mamm,
                                          0.015)
        self.sc_mamm_s = self.sc_mamm(ar_lb[0], a_i, den, noael_mamm, aw_mamm_sm, self.fi_mamm, 0.1, tw_mamm,
                                      self.anoael_mamm, 0.015)

        self.sa_bird_1_m = self.sa_bird_1(ar_lb[0], a_i, den, self.at_bird, self.fi_bird, 0.1, ld50_bird, aw_bird_md,
                                          tw_bird_ld50, x, 0.1)
        self.sa_bird_2_m = self.sa_bird_2(ar_lb[0], a_i, den, m_s_r_p, self.at_bird, ld50_bird, aw_bird_md,
                                          tw_bird_ld50, x, 0.1)
        self.sc_bird_m = self.sc_bird(ar_lb[0], a_i, den, noaec_bird)
        self.sa_mamm_1_m = self.sa_mamm_1(ar_lb[0], a_i, den, self.at_mamm, self.fi_mamm, 0.1, ld50_mamm, aw_mamm_md,
                                          tw_mamm, 0.035)
        self.sa_mamm_2_m = self.sa_mamm_2(ar_lb[0], a_i, den, m_s_r_p, self.at_mamm, ld50_mamm, aw_mamm_md, tw_mamm,
                                          0.035)
        self.sc_mamm_m = self.sc_mamm(ar_lb[0], a_i, den, noael_mamm, aw_mamm_md, self.fi_mamm, 0.1, tw_mamm,
                                      self.anoael_mamm, 0.035)

        self.sa_bird_1_l = self.sa_bird_1(ar_lb[0], a_i, den, self.at_bird, self.fi_bird, 0.1, ld50_bird, aw_bird_lg,
                                          tw_bird_ld50, x, 1.0)
        self.sa_bird_2_l = self.sa_bird_2(ar_lb[0], a_i, den, m_s_r_p, self.at_bird, ld50_bird, aw_bird_lg,
                                          tw_bird_ld50, x, 1.0)
        self.sc_bird_l = self.sc_bird(ar_lb[0], a_i, den, noaec_bird)
        self.sa_mamm_1_l = self.sa_mamm_1(ar_lb[0], a_i, den, self.at_mamm, self.fi_mamm, 0.1, ld50_mamm, aw_mamm_lg,
                                          tw_mamm, 1)
        self.sa_mamm_2_l = self.sa_mamm_2(ar_lb[0], a_i, den, m_s_r_p, self.at_mamm, ld50_mamm, aw_mamm_lg, tw_mamm, 1)
        self.sc_mamm_l = self.sc_mamm(ar_lb[0], a_i, den, noael_mamm, aw_mamm_lg, self.fi_mamm, 0.1, tw_mamm,
                                      self.anoael_mamm, 1)

        # Table 6
        self.eec_diet_sg = self.eec_diet(self.c_0, self.c_t, n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_diet_tg = self.eec_diet(self.c_0, self.c_t, n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_diet_bp = self.eec_diet(self.c_0, self.c_t, n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_diet_fr = self.eec_diet(self.c_0, self.c_t, n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_diet_ar = self.eec_diet(self.c_0, self.c_t, n_a, ar_lb, a_i, 94, h_l, day_out)

        # Table 7
        self.eec_dose_bird_sg_sm = self.eec_dose_bird(self.eec_diet, aw_bird_sm, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_dose_bird_sg_md = self.eec_dose_bird(self.eec_diet, aw_bird_md, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_dose_bird_sg_lg = self.eec_dose_bird(self.eec_diet, aw_bird_lg, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_dose_bird_tg_sm = self.eec_dose_bird(self.eec_diet, aw_bird_sm, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_dose_bird_tg_md = self.eec_dose_bird(self.eec_diet, aw_bird_md, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_dose_bird_tg_lg = self.eec_dose_bird(self.eec_diet, aw_bird_lg, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_dose_bird_bp_sm = self.eec_dose_bird(self.eec_diet, aw_bird_sm, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_dose_bird_bp_md = self.eec_dose_bird(self.eec_diet, aw_bird_md, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_dose_bird_bp_lg = self.eec_dose_bird(self.eec_diet, aw_bird_lg, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_dose_bird_fp_sm = self.eec_dose_bird(self.eec_diet, aw_bird_sm, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_bird_fp_md = self.eec_dose_bird(self.eec_diet, aw_bird_md, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_bird_fp_lg = self.eec_dose_bird(self.eec_diet, aw_bird_lg, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_bird_ar_sm = self.eec_dose_bird(self.eec_diet, aw_bird_sm, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 94, h_l, day_out)
        self.eec_dose_bird_ar_md = self.eec_dose_bird(self.eec_diet, aw_bird_md, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 94, h_l, day_out)
        self.eec_dose_bird_ar_lg = self.eec_dose_bird(self.eec_diet, aw_bird_lg, self.fi_bird, 0.9, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 94, h_l, day_out)
        self.eec_dose_bird_se_sm = self.eec_dose_bird(self.eec_diet, aw_bird_sm, self.fi_bird, 0.1, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_bird_se_md = self.eec_dose_bird(self.eec_diet, aw_bird_md, self.fi_bird, 0.1, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_bird_se_lg = self.eec_dose_bird(self.eec_diet, aw_bird_lg, self.fi_bird, 0.1, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)

        # Table 7_add
        self.arq_bird_sg_sm = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_sm, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 240, h_l, day_out)
        self.arq_bird_sg_md = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_md, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 240, h_l, day_out)
        self.arq_bird_sg_lg = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_lg, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 240, h_l, day_out)
        self.arq_bird_tg_sm = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_sm, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 110, h_l, day_out)
        self.arq_bird_tg_md = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_md, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 110, h_l, day_out)
        self.arq_bird_tg_lg = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_lg, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 110, h_l, day_out)
        self.arq_bird_bp_sm = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_sm, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 135, h_l, day_out)
        self.arq_bird_bp_md = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_md, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 135, h_l, day_out)
        self.arq_bird_bp_lg = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_lg, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 135, h_l, day_out)
        self.arq_bird_fp_sm = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_sm, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 15, h_l, day_out)
        self.arq_bird_fp_md = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_md, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 15, h_l, day_out)
        self.arq_bird_fp_lg = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_lg, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 15, h_l, day_out)
        self.arq_bird_ar_sm = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_sm, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 94, h_l, day_out)
        self.arq_bird_ar_md = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_md, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 94, h_l, day_out)
        self.arq_bird_ar_lg = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_lg, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.8, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 94, h_l, day_out)
        self.arq_bird_se_sm = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_sm, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.1, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 15, h_l, day_out)
        self.arq_bird_se_md = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_md, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.1, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 15, h_l, day_out)
        self.arq_bird_se_lg = self.arq_dose_bird(self.eec_dose_bird, self.eec_diet, aw_bird_lg, self.fi_bird,
                                                 self.at_bird, ld50_bird, tw_bird_ld50, x, 0.1, self.c_0, self.c_t, n_a,
                                                 ar_lb, a_i, 15, h_l, day_out)

        # Table 8
        self.arq_diet_bird_sg_a = self.arq_diet_bird(self.eec_diet, lc50_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 240,
                                                     h_l, day_out)
        self.arq_diet_bird_sg_c = self.crq_diet_bird(self.eec_diet, noaec_bird, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                     240, h_l, day_out)
        self.arq_diet_bird_tg_a = self.arq_diet_bird(self.eec_diet, lc50_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 110,
                                                     h_l, day_out)
        self.arq_diet_bird_tg_c = self.crq_diet_bird(self.eec_diet, noaec_bird, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                     110, h_l, day_out)
        self.arq_diet_bird_bp_a = self.arq_diet_bird(self.eec_diet, lc50_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 135,
                                                     h_l, day_out)
        self.arq_diet_bird_bp_c = self.crq_diet_bird(self.eec_diet, noaec_bird, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                     135, h_l, day_out)
        self.arq_diet_bird_fp_a = self.arq_diet_bird(self.eec_diet, lc50_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 15,
                                                     h_l, day_out)
        self.arq_diet_bird_fp_c = self.crq_diet_bird(self.eec_diet, noaec_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 15,
                                                     h_l, day_out)
        self.arq_diet_bird_ar_a = self.arq_diet_bird(self.eec_diet, lc50_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 94,
                                                     h_l, day_out)
        self.arq_diet_bird_ar_c = self.crq_diet_bird(self.eec_diet, noaec_bird, self.c_0, self.c_t, n_a, ar_lb, a_i, 94,
                                                     h_l, day_out)

        # Table 9
        self.eec_dose_mamm_sg_sm = self.eec_dose_mamm(self.eec_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_dose_mamm_sg_md = self.eec_dose_mamm(self.eec_diet, aw_mamm_md, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_dose_mamm_sg_lg = self.eec_dose_mamm(self.eec_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 240, h_l, day_out)
        self.eec_dose_mamm_tg_sm = self.eec_dose_mamm(self.eec_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_dose_mamm_tg_md = self.eec_dose_mamm(self.eec_diet, aw_mamm_md, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_dose_mamm_tg_lg = self.eec_dose_mamm(self.eec_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 110, h_l, day_out)
        self.eec_dose_mamm_bp_sm = self.eec_dose_mamm(self.eec_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_dose_mamm_bp_md = self.eec_dose_mamm(self.eec_diet, aw_mamm_md, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_dose_mamm_bp_lg = self.eec_dose_mamm(self.eec_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 135, h_l, day_out)
        self.eec_dose_mamm_fp_sm = self.eec_dose_mamm(self.eec_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_mamm_fp_md = self.eec_dose_mamm(self.eec_diet, aw_mamm_md, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_mamm_fp_lg = self.eec_dose_mamm(self.eec_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_mamm_ar_sm = self.eec_dose_mamm(self.eec_diet, aw_mamm_sm, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 94, h_l, day_out)
        self.eec_dose_mamm_ar_md = self.eec_dose_mamm(self.eec_diet, aw_mamm_md, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 94, h_l, day_out)
        self.eec_dose_mamm_ar_lg = self.eec_dose_mamm(self.eec_diet, aw_mamm_lg, self.fi_mamm, 0.8, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 94, h_l, day_out)
        self.eec_dose_mamm_se_sm = self.eec_dose_mamm(self.eec_diet, aw_mamm_sm, self.fi_mamm, 0.1, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_mamm_se_md = self.eec_dose_mamm(self.eec_diet, aw_mamm_md, self.fi_mamm, 0.1, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)
        self.eec_dose_mamm_se_lg = self.eec_dose_mamm(self.eec_diet, aw_mamm_lg, self.fi_mamm, 0.1, self.c_0, self.c_t,
                                                      n_a, ar_lb, a_i, 15, h_l, day_out)

        # Table 10
        self.arq_dose_mamm_sg_sm = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_sm,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 240, h_l, day_out)
        self.crq_dose_mamm_sg_sm = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 240, h_l, day_out)
        self.arq_dose_mamm_sg_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_md,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 240, h_l, day_out)
        self.crq_dose_mamm_sg_md = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 240, h_l, day_out)
        self.arq_dose_mamm_sg_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_lg,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 240, h_l, day_out)
        self.crq_dose_mamm_sg_lg = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 240, h_l, day_out)

        self.arq_dose_mamm_tg_sm = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_sm,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 110, h_l, day_out)
        self.crq_dose_mamm_tg_sm = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 110, h_l, day_out)
        self.arq_dose_mamm_tg_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_md,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 110, h_l, day_out)
        self.crq_dose_mamm_tg_md = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 110, h_l, day_out)
        self.arq_dose_mamm_tg_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_lg,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 110, h_l, day_out)
        self.crq_dose_mamm_tg_lg = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 110, h_l, day_out)

        self.arq_dose_mamm_bp_sm = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_sm,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 135, h_l, day_out)
        self.crq_dose_mamm_bp_sm = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 135, h_l, day_out)
        self.arq_dose_mamm_bp_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_md,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 135, h_l, day_out)
        self.crq_dose_mamm_bp_md = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 135, h_l, day_out)
        self.arq_dose_mamm_bp_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_lg,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 135, h_l, day_out)
        self.crq_dose_mamm_bp_lg = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 135, h_l, day_out)

        self.arq_dose_mamm_fp_sm = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_sm,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.crq_dose_mamm_fp_sm = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.arq_dose_mamm_fp_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_md,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.crq_dose_mamm_fp_md = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.arq_dose_mamm_fp_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_lg,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.crq_dose_mamm_fp_lg = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)

        self.arq_dose_mamm_ar_sm = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_sm,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 94, h_l, day_out)
        self.crq_dose_mamm_ar_sm = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_sm, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 94, h_l, day_out)
        self.arq_dose_mamm_ar_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_md,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 94, h_l, day_out)
        self.crq_dose_mamm_ar_md = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_md, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 94, h_l, day_out)
        self.arq_dose_mamm_ar_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_lg,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 94, h_l, day_out)
        self.crq_dose_mamm_ar_lg = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_lg, self.fi_mamm, tw_mamm, 0.8, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 94, h_l, day_out)

        self.arq_dose_mamm_se_sm = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_sm,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.1, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.crq_dose_mamm_se_sm = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_sm, self.fi_mamm, tw_mamm, 0.1, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.arq_dose_mamm_se_md = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_md,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.1, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.crq_dose_mamm_se_md = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_md, self.fi_mamm, tw_mamm, 0.1, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.arq_dose_mamm_se_lg = self.arq_dose_mamm(self.eec_dose_mamm, self.eec_diet, self.at_mamm, aw_mamm_lg,
                                                      self.fi_mamm, ld50_mamm, tw_mamm, 0.1, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)
        self.crq_dose_mamm_se_lg = self.crq_dose_mamm(self.eec_diet, self.eec_dose_mamm, self.anoael_mamm, noael_mamm,
                                                      aw_mamm_lg, self.fi_mamm, tw_mamm, 0.1, self.c_0, self.c_t, n_a,
                                                      ar_lb, a_i, 15, h_l, day_out)

        # table 11
        if self.lc50_mamm != 'N/a':
            self.arq_diet_mamm_sg = self.arq_diet_mamm(self.eec_diet, lc50_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                       240, h_l, day_out)
            self.arq_diet_mamm_tg = self.arq_diet_mamm(self.eec_diet, lc50_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                       110, h_l, day_out)
            self.arq_diet_mamm_bp = self.arq_diet_mamm(self.eec_diet, lc50_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                       135, h_l, day_out)
            self.arq_diet_mamm_fp = self.arq_diet_mamm(self.eec_diet, lc50_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                       15, h_l, day_out)
            self.arq_diet_mamm_ar = self.arq_diet_mamm(self.eec_diet, lc50_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i,
                                                       94, h_l, day_out)
        else:
            self.arq_diet_mamm_sg = 'N/a'
            self.arq_diet_mamm_tg = 'N/a'
            self.arq_diet_mamm_bp = 'N/a'
            self.arq_diet_mamm_fp = 'N/a'
            self.arq_diet_mamm_ar = 'N/a'

        self.crq_diet_mamm_sg = self.crq_diet_mamm(self.eec_diet, noaec_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i, 240,
                                                   h_l, day_out)
        self.crq_diet_mamm_tg = self.crq_diet_mamm(self.eec_diet, noaec_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i, 110,
                                                   h_l, day_out)
        self.crq_diet_mamm_bp = self.crq_diet_mamm(self.eec_diet, noaec_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i, 135,
                                                   h_l, day_out)
        self.crq_diet_mamm_fp = self.crq_diet_mamm(self.eec_diet, noaec_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i, 15,
                                                   h_l, day_out)
        self.crq_diet_mamm_ar = self.crq_diet_mamm(self.eec_diet, noaec_mamm, self.c_0, self.c_t, n_a, ar_lb, a_i, 94,
                                                   h_l, day_out)

        # Table12
        self.ld50_rg_bird_sm = self.ld50_rg_bird(application_type, ar_lb, a_i, p_i, r_s, b_w, aw_bird_sm, self.at_bird,
                                                 ld50_bird, tw_bird_ld50, x)
        self.ld50_rg_mamm_sm = self.ld50_rg_mamm(application_type, ar_lb, a_i, p_i, r_s, b_w, aw_mamm_sm, self.at_mamm,
                                                 ld50_mamm, tw_mamm)
        self.ld50_rg_bird_md = self.ld50_rg_bird(application_type, ar_lb, a_i, p_i, r_s, b_w, aw_bird_md, self.at_bird,
                                                 ld50_bird, tw_bird_ld50, x)
        self.ld50_rg_mamm_md = self.ld50_rg_mamm(application_type, ar_lb, a_i, p_i, r_s, b_w, aw_mamm_md, self.at_mamm,
                                                 ld50_mamm, tw_mamm)
        self.ld50_rg_bird_lg = self.ld50_rg_bird(application_type, ar_lb, a_i, p_i, r_s, b_w, aw_bird_lg, self.at_bird,
                                                 ld50_bird, tw_bird_ld50, x)
        self.ld50_rg_mamm_lg = self.ld50_rg_mamm(application_type, ar_lb, a_i, p_i, r_s, b_w, aw_mamm_lg, self.at_mamm,
                                                 ld50_mamm, tw_mamm)

        # Table13
        self.ld50_rl_bird_sm = self.ld50_rl_bird(application_type, ar_lb, a_i, p_i, b_w, aw_bird_sm, self.at_bird,
                                                 ld50_bird, tw_bird_ld50, x)
        self.ld50_rl_mamm_sm = self.ld50_rl_mamm(application_type, ar_lb, a_i, p_i, b_w, aw_mamm_sm, self.at_mamm,
                                                 ld50_mamm, tw_mamm)
        self.ld50_rl_bird_md = self.ld50_rl_bird(application_type, ar_lb, a_i, p_i, b_w, aw_bird_md, self.at_bird,
                                                 ld50_bird, tw_bird_ld50, x)
        self.ld50_rl_mamm_md = self.ld50_rl_mamm(application_type, ar_lb, a_i, p_i, b_w, aw_mamm_md, self.at_mamm,
                                                 ld50_mamm, tw_mamm)
        self.ld50_rl_bird_lg = self.ld50_rl_bird(application_type, ar_lb, a_i, p_i, b_w, aw_bird_lg, self.at_bird,
                                                 ld50_bird, tw_bird_ld50, x)
        self.ld50_rl_mamm_lg = self.ld50_rl_mamm(application_type, ar_lb, a_i, p_i, b_w, aw_mamm_lg, self.at_mamm,
                                                 ld50_mamm, tw_mamm)

        # Table14
        self.ld50_bg_bird_sm = self.ld50_bg_bird(application_type, ar_lb, a_i, p_i, aw_bird_sm, self.at_bird, ld50_bird,
                                                 tw_bird_ld50, x)
        self.ld50_bg_mamm_sm = self.ld50_bg_mamm(application_type, ar_lb, a_i, p_i, aw_mamm_sm, self.at_mamm, ld50_mamm,
                                                 tw_mamm)
        self.ld50_bg_bird_md = self.ld50_bg_bird(application_type, ar_lb, a_i, p_i, aw_bird_md, self.at_bird, ld50_bird,
                                                 tw_bird_ld50, x)
        self.ld50_bg_mamm_md = self.ld50_bg_mamm(application_type, ar_lb, a_i, p_i, aw_mamm_md, self.at_mamm, ld50_mamm,
                                                 tw_mamm)
        self.ld50_bg_bird_lg = self.ld50_bg_bird(application_type, ar_lb, a_i, p_i, aw_bird_lg, self.at_bird, ld50_bird,
                                                 tw_bird_ld50, x)
        self.ld50_bg_mamm_lg = self.ld50_bg_mamm(application_type, ar_lb, a_i, p_i, aw_mamm_lg, self.at_mamm, ld50_mamm,
                                                 tw_mamm)

        # Table15
        self.ld50_bl_bird_sm = self.ld50_bl_bird(application_type, ar_lb, a_i, aw_bird_sm, self.at_bird, ld50_bird,
                                                 tw_bird_ld50, x)
        self.ld50_bl_mamm_sm = self.ld50_bl_mamm(application_type, ar_lb, a_i, aw_mamm_sm, self.at_mamm, ld50_mamm,
                                                 tw_mamm)
        self.ld50_bl_bird_md = self.ld50_bl_bird(application_type, ar_lb, a_i, aw_bird_md, self.at_bird, ld50_bird,
                                                 tw_bird_ld50, x)
        self.ld50_bl_mamm_md = self.ld50_bl_mamm(application_type, ar_lb, a_i, aw_mamm_md, self.at_mamm, ld50_mamm,
                                                 tw_mamm)
        self.ld50_bl_bird_lg = self.ld50_bl_bird(application_type, ar_lb, a_i, aw_bird_lg, self.at_bird, ld50_bird,
                                                 tw_bird_ld50, x)
        self.ld50_bl_mamm_lg = self.ld50_bl_mamm(application_type, ar_lb, a_i, aw_mamm_lg, self.at_mamm, ld50_mamm,
                                                 tw_mamm)

    def fi_bird(self, aw_bird, mf_w_bird):
        """
        Food intake for birds
        :param aw_bird:
        :param mf_w_bird:
        :return:
        """
        try:
            aw_bird = float(aw_bird)
            mf_w_bird = float(mf_w_bird)
        except IndexError:
            raise IndexError \
                ('The body weight of the assessed bird, and/or the mass fraction of ' \
                 'water in the food must be supplied on the command line.')
        except ValueError:
            raise ValueError \
                ('The body weight of the assessed bird must be a real number, not "%g"' % aw_bird)
        except ValueError:
            raise ValueError \
                ('The mass fraction of water in the food for bird must be a real number, not "%g"' % mf_w_bird)
        if aw_bird < 0:
            raise ValueError \
                ('The body weight of the assessed bird=%g is a non-physical value.' % aw_bird)
        if mf_w_bird < 0:
            raise ValueError \
                ('The fraction of water in the food for bird=%g is a non-physical value.' % mf_w_bird)
        if mf_w_bird >= 1:
            raise ValueError \
                ('The fraction of water in the food for bird=%g must be less than 1.' % mf_w_bird)
        return (0.648 * (aw_bird ** 0.651)) / (1 - mf_w_bird)

    def fi_mamm(self, aw_mamm, mf_w_mamm):
        """
        Food intake for mammals
        :param aw_mamm:
        :param mf_w_mamm:
        :return:
        """
        try:
            aw_mamm = float(aw_mamm)
            mf_w_mamm = float(mf_w_mamm)
        except IndexError:
            raise IndexError \
                ('The body weight of mammal, and/or the mass fraction of water in the ' \
                 'food must be supplied on the command line.')
        except ValueError:
            raise ValueError \
                ('The body weight of mammal must be a real number, not "%g"' % aw_mamm)
        except ValueError:
            raise ValueError \
                ('The mass fraction of water in the food for mammals must be a real number, not "%"' % mf_w_mamm)
        if aw_mamm < 0:
            raise ValueError \
                ('The body weight of mammal=%g is a non-physical value.' % aw_mamm)
        if mf_w_mamm < 0:
            raise ValueError \
                ('The fraction of water in the food for mammals=%g is a non-physical value.' % mf_w_mamm)
        if mf_w_mamm >= 1:
            raise ValueError \
                ('The fraction of water in the food for mammals=%g must be less than 1.' % mf_w_mamm)
        return (0.621 * (aw_mamm ** 0.564)) / (1 - mf_w_mamm)

    def at_bird(self, ld50_bird, aw_bird, tw_bird, x):
        """
        acute adjusted toxicity value for birds
        :param ld50_bird:
        :param aw_bird:
        :param tw_bird:
        :param x:
        :return:
        """
        try:
            ld50_bird = float(ld50_bird)
            aw_bird = float(aw_bird)
            tw_bird = float(tw_bird)
            x = float(x)
        except IndexError:
            raise IndexError \
                ('The lethal dose, body weight of assessed bird, body weight of tested' \
                 ' bird, and/or Mineau scaling factor for birds must be supplied on' \
                 ' the command line.')
        except ValueError:
            raise ValueError \
                ('The lethal dose must be a real number, not "%mg/kg"' % ld50_bird)
        except ValueError:
            raise ValueError \
                ('The body weight of assessed bird must be a real number, not "%g"' % aw_bird)
        except ValueError:
            raise ValueError \
                ('The body weight of tested bird must be a real number, not "%g"' % tw_bird)
        except ValueError:
            raise ValueError \
                ('The Mineau scaling factor for birds must be a real number' % x)
        except ZeroDivisionError:
            raise ZeroDivisionError \
                ('The body weight of tested bird must be non-zero.')
        if ld50_bird < 0:
            raise ValueError \
                ('ld50=%g is a non-physical value.' % ld50_bird)
        if aw_bird < 0:
            raise ValueError \
                ('aw_bird=%g is a non-physical value.' % aw_bird)
        if tw_bird < 0:
            raise ValueError \
                ('tw_bird=%g is a non-physical value.' % tw_bird)
        if x < 0:
            raise ValueError \
                ('x=%g is non-physical value.' % x)
        return (ld50_bird) * ((aw_bird / tw_bird) ** (x - 1))

    def at_mamm(self, ld50_mamm, aw_mamm, tw_mamm):
        """
        acute adjusted toxicity value for mammals
        :param ld50_mamm:
        :param aw_mamm:
        :param tw_mamm:
        :return:
        """
        try:
            ld50_mamm = float(ld50_mamm)
            aw_mamm = float(aw_mamm)
            tw_mamm = float(tw_mamm)
        except IndexError:
            raise IndexError \
                ('The lethal dose, body weight of assessed mammal, and body weight of tested' \
                 ' mammal must be supplied on' \
                 ' the command line.')
        except ValueError:
            raise ValueError \
                ('The lethal dose must be a real number, not "%mg/kg"' % ld50_mamm)
        except ValueError:
            raise ValueError \
                ('The body weight of assessed mammals must be a real number, not "%g"' % aw_mamm)
        except ValueError:
            raise ValueError \
                ('The body weight of tested mammals must be a real number, not "%g"' % tw_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError \
                ('The body weight of tested mammals must be non-zero.')
        if ld50_mamm < 0:
            raise ValueError \
                ('ld50_mamm=%g is a non-physical value.' % ld50_mamm)
        if aw_mamm < 0:
            raise ValueError \
                ('aw_mamm=%g is a non-physical value.' % aw_mamm)
        if tw_mamm < 0:
            raise ValueError \
                ('tw_mamm=%g is a non-physical value.' % tw_mamm)
        return (ld50_mamm) * ((tw_mamm / aw_mamm) ** (0.25))

    def anoael_mamm(self, noael_mamm, aw_mamm, tw_mamm):
        """
        adjusted chronic toxicity (noael) value for mammals
        :param noael_mamm:
        :param aw_mamm:
        :param tw_mamm:
        :return:
        """
        try:
            noael_mamm = float(noael_mamm)
            aw_mamm = float(aw_mamm)
            tw_mamm = float(tw_mamm)
        except IndexError:
            raise IndexError \
                ('The noael, body weight of assessed mammal, and body weight of tested' \
                 ' mammal must be supplied on' \
                 ' the command line.')
        except ValueError:
            raise ValueError \
                ('The noael must be a real number, not "%mg/kg"' % noael_mamm)
        except ValueError:
            raise ValueError \
                ('The body weight of assessed mammals must be a real number, not "%g"' % aw_mamm)
        except ValueError:
            raise ValueError \
                ('The body weight of tested mammals must be a real number, not "%g"' % tw_mamm)
        except ZeroDivisionError:
            raise ZeroDivisionError \
                ('The body weight of tested mammals must be non-zero.')
        if noael_mamm < 0:
            raise ValueError \
                ('noael_mamm=%g is a non-physical value.' % noael_mamm)
        if aw_mamm < 0:
            raise ValueError \
                ('aw_mamm=%g is a non-physical value.' % aw_mamm)
        if tw_mamm < 0:
            raise ValueError \
                ('tw_mamm=%g is a non-physical value.' % tw_mamm)
        return (noael_mamm) * ((tw_mamm / aw_mamm) ** (0.25))

    def c_0(self, a_r, a_i, para):
        """
        Initial concentration
        :param a_r:
        :param a_i:
        :param para:
        :return:
        """
        try:
            a_r = float(a_r)
            a_i = float(a_i)
        except IndexError:
            raise IndexError \
                ('The application rate, and/or the percentage of active ingredient ' \
                 'must be supplied on the command line.')
        except ValueError:
            raise ValueError \
                ('The application rate must be a real number, not "%g"' % a_r)
        except ValueError:
            raise ValueError \
                ('The percentage of active ingredient must be a real number, not "%"' % a_i)
        if a_r < 0:
            raise ValueError \
                ('The application rate=%g is a non-physical value.' % a_r)
        if a_i < 0:
            raise ValueError \
                ('The percentage of active ingredient=%g is a non-physical value.' % a_i)
        return (a_r * a_i * para)

    def c_t(self, c_ini, h_l):
        """
        concentration over time
        :param c_ini:
        :param h_l:
        :return:
        """
        try:
            h_l = float(h_l)
        except IndexError:
            raise IndexError \
                ('The initial concentration, and/or the foliar dissipation half life, ' \
                 'must be supplied on the command line.')
        except ValueError:
            raise ValueError \
                ('The foliar dissipation half life must be a real number, not "%g"' % h_l)
        if h_l < 0:
            raise ValueError \
                ('The foliar dissipation half life=%g is a non-physical value.' % h_l)
        return (c_ini * np.exp(-(np.log(2) / h_l) * 1))

    def eec_diet(self, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        Dietary based eecs, new in trex1.5.1
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        if n_a == 1:
            c_temp = c_0(a_r[0], a_i, para)
            return np.array([c_temp])
        else:
            c_temp = np.ones((371, 1))  # empty array to hold the concentrations over days
            a_p_temp = 0  # application period temp
            n_a_temp = 0  # number of existing applications
            dayt = 0
            day_out_l = len(day_out)
            for i in range(0, 371):
                if i == 0:  # first day of application
                    c_temp[i] = c_0(a_r[0], a_i, para)
                    a_p_temp = 0
                    n_a_temp = n_a_temp + 1
                    dayt = dayt + 1
                elif dayt <= day_out_l - 1 and n_a_temp <= n_a:  # next application day
                    if i == day_out[dayt]:
                        c_temp[i] = c_t(c_temp[i - 1], h_l) + c_0(a_r[dayt], a_i, para)
                        n_a_temp = n_a_temp + 1
                        dayt = dayt + 1
                    else:
                        c_temp[i] = c_t(c_temp[i - 1], h_l)
            return (max(c_temp))

    def eec_dose_bird(self, eec_diet, aw_bird, fi_bird, mf_w_bird, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        Dose based eecs for birds
        :param eec_diet:
        :param aw_bird:
        :param fi_bird:
        :param mf_w_bird:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        n_a = float(n_a)
        #   i_a = float(i_a)
        aw_bird = float(aw_bird)
        mf_w_bird = float(mf_w_bird)
        #  a_r = float(a_r)
        a_i = float(a_i)
        para = float(para)
        h_l = float(h_l)

        fi_bird = fi_bird(aw_bird, mf_w_bird)
        eec_diet = eec_diet(c_0, c_t, n_a, a_r, a_i, para, h_l, day_out)
        return (eec_diet * fi_bird / aw_bird)

    # Dose based eecs for granivores birds

    # def eec_dose_bird_g(eec_diet, aw_bird, fi_bird, mf_w_bird, c_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:
    #         n_a = float(n_a)
    #       #  i_a = float(i_a)      
    #         aw_bird = float(aw_bird)
    #         mf_w_bird = float(mf_w_bird)
    #         a_r = float(a_r)
    #         a_i = float(a_i)
    #         para = float(para)
    #         h_l = float(h_l)        
    #         fi_bird = fi_bird(aw_bird, mf_w_bird)
    #         eec_diet=eec_diet(c_0, n_a, a_r, a_i, para, h_l, day)
    #         return (eec_diet*fi_bird/aw_bird)
    #     else:
    #         return(0)

    def eec_dose_mamm(self, eec_diet, aw_mamm, fi_mamm, mf_w_mamm, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        Dose based eecs for mammals
        :param eec_diet:
        :param aw_mamm:
        :param fi_mamm:
        :param mf_w_mamm:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        aw_mamm = float(aw_mamm)
        eec_diet = eec_diet(c_0, c_t, n_a, a_r, a_i, para, h_l, day_out)
        fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
        return (eec_diet * fi_mamm / aw_mamm)

    # Dose based eecs for granivores mammals

    # def eec_dose_mamm_g(eec_diet, aw_mamm, fi_mamm, mf_w_mamm, c_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:    
    #         aw_mamm = float(aw_mamm)
    #         eec_diet=eec_diet(c_0, n_a, a_r, a_i, para, h_l, day)
    #         fi_mamm = fi_mamm(aw_mamm, mf_w_mamm)
    #         return (eec_diet*fi_mamm/aw_mamm)
    #     else:
    #         return(0)

    def arq_dose_bird(self, eec_dose_bird, eec_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, c_0,
                      c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        acute dose-based risk quotients for birds
        :param eec_dose_bird:
        :param eec_diet:
        :param aw_bird:
        :param fi_bird:
        :param at_bird:
        :param ld50_bird:
        :param tw_bird:
        :param x:
        :param mf_w_bird:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        eec_dose_bird = eec_dose_bird(eec_diet, aw_bird, fi_bird, mf_w_bird, c_0, c_t, n_a, a_r, a_i, para, h_l,
                                      day_out)
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        return (eec_dose_bird / at_bird)

    # acute dose-based risk quotients for granivores birds

    # def arq_dose_bird_g(eec_dose_bird, eec_diet, aw_bird, fi_bird, at_bird, ld50_bird, tw_bird, x, mf_w_bird, c_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:
    #         eec_dose_bird = eec_dose_bird(eec_diet, aw_bird, fi_bird, mf_w_bird, c_0, n_a, a_r, a_i, para, h_l)
    #         at_bird = at_bird(ld50_bird,aw_bird,tw_bird,x)
    #         return (eec_dose_bird/at_bird)
    #     else:
    #         return (0)

    def arq_dose_mamm(self, eec_dose_mamm, eec_diet, at_mamm, aw_mamm, fi_mamm, ld50_mamm, tw_mamm, mf_w_mamm, c_0, c_t,
                      n_a, a_r, a_i, para, h_l, day_out):
        """
        acute dose-based risk quotients for mammals
        :param eec_dose_mamm:
        :param eec_diet:
        :param at_mamm:
        :param aw_mamm:
        :param fi_mamm:
        :param ld50_mamm:
        :param tw_mamm:
        :param mf_w_mamm:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        eec_dose_mamm = eec_dose_mamm(eec_diet, aw_mamm, fi_mamm, mf_w_mamm, c_0, c_t, n_a, a_r, a_i, para, h_l,
                                      day_out)
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        return (eec_dose_mamm / at_mamm)

    # acute dose-based risk quotients for granivores mammals

    # def arq_dose_mamm_g(eec_dose_mamm, at_mamm, aw_mamm, ld50_mamm, tw_mamm, mf_w_mamm, c_0, n_a, a_r, a_i, para, h_l):
    #     if para==15:    
    #         eec_dose_mamm = eec_dose_mamm(eec_diet, aw_mamm, fi_mamm, mf_w_mamm, c_0, n_a, a_r, a_i, para, h_l)
    #         at_mamm = at_mamm(ld50_mamm,aw_mamm,tw_mamm)
    #         return (eec_dose_mamm/at_mamm)
    #     else:
    #         return(0)

    def arq_diet_bird(self, eec_diet, lc50_bird, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        acute dietary-based risk quotients for birds
        :param eec_diet:
        :param lc50_bird:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        eec_diet = eec_diet(c_0, c_t, n_a, a_r, a_i, para, h_l, day_out)
        try:
            lc50_bird = float(lc50_bird)
        except IndexError:
            raise IndexError \
                ('The avian Lc50 must be supplied on the command line.')
        if lc50_bird < 0:
            raise ValueError \
                ('The avian Lc50=%g is a non-physical value.' % lc50_bird)
        return (eec_diet / lc50_bird)

    def arq_diet_mamm(self, eec_diet, lc50_mamm, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        acute dietary-based risk quotients for mammals
        :param eec_diet:
        :param lc50_mamm:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        eec_diet = eec_diet(c_0, c_t, n_a, a_r, a_i, para, h_l, day_out)
        return (eec_diet / lc50_mamm)

    def crq_diet_bird(self, eec_diet, noaec_bird, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        chronic dietary-based risk quotients for birds
        :param eec_diet:
        :param noaec_bird:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        eec_diet = eec_diet(c_0, c_t, n_a, a_r, a_i, para, h_l, day_out)
        try:
            noaec_bird = float(noaec_bird)
        except IndexError:
            raise IndexError \
                ('The avian noaec must be supplied on the command line.')
        if noaec_bird < 0:
            raise ValueError \
                ('The avian noaec=%g is a non-physical value.' % noaec_bird)
        return (eec_diet / noaec_bird)

    def crq_diet_mamm(self, eec_diet, noaec_mamm, c_0, c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        chronic dietary-based risk quotients for mammals
        :param eec_diet:
        :param noaec_mamm:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        eec_diet = eec_diet(c_0, c_t, n_a, a_r, a_i, para, h_l, day_out)
        try:
            noaec_mamm = float(noaec_mamm)
        except IndexError:
            raise IndexError \
                ('The mammlian noaec must be supplied on the command line.')
        if noaec_mamm < 0:
            raise ValueError \
                ('The mammlian noaec=%g is a non-physical value.' % noaec_mamm)
        return (eec_diet / noaec_mamm)

    def crq_dose_mamm(self, eec_diet, eec_dose_mamm, anoael_mamm, noael_mamm, aw_mamm, fi_mamm, tw_mamm, mf_w_mamm, c_0,
                      c_t, n_a, a_r, a_i, para, h_l, day_out):
        """
        chronic dose-based risk quotients for mammals
        :param eec_diet:
        :param eec_dose_mamm:
        :param anoael_mamm:
        :param noael_mamm:
        :param aw_mamm:
        :param fi_mamm:
        :param tw_mamm:
        :param mf_w_mamm:
        :param c_0:
        :param c_t:
        :param n_a:
        :param a_r:
        :param a_i:
        :param para:
        :param h_l:
        :param day_out:
        :return:
        """
        anoael_mamm = anoael_mamm(noael_mamm, aw_mamm, tw_mamm)
        eec_dose_mamm = eec_dose_mamm(eec_diet, aw_mamm, fi_mamm, mf_w_mamm, c_0, c_t, n_a, a_r, a_i, para, h_l,
                                      day_out)
        return (eec_dose_mamm / anoael_mamm)

    # chronic dose-based risk quotients for granviores mammals

    # def crq_dose_mamm_g(eec_diet, eec_dose_mamm, anoael_mamm, noael_mamm, aw_mamm, tw_mamm, mf_w_mamm, n_a, a_r, a_i, para, h_l):
    #     if para==15:    
    #         anoael_mamm=anoael_mamm(noael_mamm,aw_mamm,tw_mamm)
    #         eec_dose_mamm = eec_dose_mamm(eec_diet, aw_mamm, fi_mamm, mf_w_mamm, c_0, n_a, a_r, a_i, para, h_l)     
    #         return (eec_dose_mamm/anoael_mamm)
    #     else:
    #         return (0)

    def ld50_rg_bird(self, application_type, a_r, a_i, p_i, r_s, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
        """
        ld50ft-2 for row/band/in-furrow granular birds
        :param application_type:
        :param a_r:
        :param a_i:
        :param p_i:
        :param r_s:
        :param b_w:
        :param aw_bird:
        :param at_bird:
        :param ld50_bird:
        :param tw_bird:
        :param x:
        :return:
        """
        if application_type == 'Row/Band/In-furrow-Granular':
            at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
            # print 'r_s', r_s
            n_r = (43560 ** 0.5) / (r_s)
            # print 'n_r=', n_r
            # print 'a_r=', a_r
            # print 'b_w=', b_w
            # print 'p_i=', p_i
            # print 'a_i', a_i
            # print 'class a_r', type(a_r)
            expo_rg_bird = (max(a_r) * a_i * 453590.0) / (n_r * (43560.0 ** 0.5) * b_w) * (1 - p_i)
            return (expo_rg_bird / (at_bird * (aw_bird / 1000.0)))
        else:
            return (0)

    def ld50_rl_bird(self, application_type, a_r, a_i, p_i, b_w, aw_bird, at_bird, ld50_bird, tw_bird, x):
        """
        ld50ft-2 for row/band/in-furrow liquid birds
        :param application_type:
        :param a_r:
        :param a_i:
        :param p_i:
        :param b_w:
        :param aw_bird:
        :param at_bird:
        :param ld50_bird:
        :param tw_bird:
        :param x:
        :return:
        """
        if application_type == 'Row/Band/In-furrow-Liquid':
            at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
            expo_rl_bird = ((max(a_r) * 28349 * a_i) / (1000 * b_w)) * (1 - p_i)
            return (expo_rl_bird / (at_bird * (aw_bird / 1000.0)))
        else:
            return (0)

    def ld50_rg_mamm(self, application_type, a_r, a_i, p_i, r_s, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        """
        ld50ft-2 for row/band/in-furrow granular mammals
        :param application_type:
        :param a_r:
        :param a_i:
        :param p_i:
        :param r_s:
        :param b_w:
        :param aw_mamm:
        :param at_mamm:
        :param ld50_mamm:
        :param tw_mamm:
        :return:
        """
        if application_type == 'Row/Band/In-furrow-Granular':
            # a_r = max(ar_lb)
            at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
            n_r = (43560 ** 0.5) / (r_s)
            expo_rg_mamm = (max(a_r) * a_i * 453590) / (n_r * (43560 ** 0.5) * b_w) * (1 - p_i)
            return (expo_rg_mamm / (at_mamm * (aw_mamm / 1000.0)))
        else:
            return (0)

    def ld50_rl_mamm(self, application_type, a_r, a_i, p_i, b_w, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        """
        ld50ft-2 for row/band/in-furrow liquid mammals
        :param application_type:
        :param a_r:
        :param a_i:
        :param p_i:
        :param b_w:
        :param aw_mamm:
        :param at_mamm:
        :param ld50_mamm:
        :param tw_mamm:
        :return:
        """
        if application_type == 'Row/Band/In-furrow-Liquid':
            at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
            expo_rl_bird = ((max(a_r) * 28349 * a_i) / (1000 * b_w)) * (1 - p_i)
            return (expo_rl_bird / (at_mamm * (aw_mamm / 1000.0)))
        else:
            return (0)

    def ld50_bg_bird(self, application_type, a_r, a_i, p_i, aw_bird, at_bird, ld50_bird, tw_bird, x):
        """
        ld50ft-2 for broadcast granular birds
        :param application_type:
        :param a_r:
        :param a_i:
        :param p_i:
        :param aw_bird:
        :param at_bird:
        :param ld50_bird:
        :param tw_bird:
        :param x:
        :return:
        """
        if application_type == 'Broadcast-Granular':
            at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
            expo_bg_bird = ((max(a_r) * a_i * 453590) / 43560)
            return (expo_bg_bird / (at_bird * (aw_bird / 1000.0)))
        else:
            return (0)

    def ld50_bl_bird(self, application_type, a_r, a_i, aw_bird, at_bird, ld50_bird, tw_bird, x):
        """
        ld50ft-2 for broadcast liquid birds
        :param application_type:
        :param a_r:
        :param a_i:
        :param aw_bird:
        :param at_bird:
        :param ld50_bird:
        :param tw_bird:
        :param x:
        :return:
        """
        if application_type == 'Broadcast-Liquid':
            at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
            # expo_bl_bird=((max(a_r)*28349*a_i)/43560)*(1-p_i)
            expo_bl_bird = ((max(a_r) * 453590 * a_i) / 43560)
            return (expo_bl_bird / (at_bird * (aw_bird / 1000.0)))
        else:
            return (0)

    def ld50_bg_mamm(self, application_type, a_r, a_i, p_i, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        """
        ld50ft-2 for broadcast granular mammals
        :param application_type:
        :param a_r:
        :param a_i:
        :param p_i:
        :param aw_mamm:
        :param at_mamm:
        :param ld50_mamm:
        :param tw_mamm:
        :return:
        """
        if application_type == 'Broadcast-Granular':
            at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
            expo_bg_mamm = ((max(a_r) * a_i * 453590) / 43560)
            return (expo_bg_mamm / (at_mamm * (aw_mamm / 1000.0)))
        else:
            return (0)

    def ld50_bl_mamm(self, application_type, a_r, a_i, aw_mamm, at_mamm, ld50_mamm, tw_mamm):
        """
        ld50ft-2 for broadcast liquid mammals
        :param application_type:
        :param a_r:
        :param a_i:
        :param aw_mamm:
        :param at_mamm:
        :param ld50_mamm:
        :param tw_mamm:
        :return:
        """
        if application_type == 'Broadcast-Liquid':
            at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
            # expo_bl_mamm=((max(a_r)*28349*a_i)/43560)*(1-p_i)
            expo_bl_mamm = ((max(a_r) * a_i * 453590) / 43560)
            return (expo_bl_mamm / (at_mamm * (aw_mamm / 1000.0)))
        else:
            return (0)

    def sa_bird_1(self, a_r_p, a_i, den, at_bird, fi_bird, mf_w_bird, ld50_bird, aw_bird, tw_bird, x, nagy_bird_coef):
        """
        Seed treatment acute rq for birds method 1
        :param a_r_p:
        :param a_i:
        :param den:
        :param at_bird:
        :param fi_bird:
        :param mf_w_bird:
        :param ld50_bird:
        :param aw_bird:
        :param tw_bird:
        :param x:
        :param nagy_bird_coef:
        :return:
        """
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        # fi_bird=fi_bird(20, 0.1)    
        fi_bird = fi_bird(aw_bird, mf_w_bird)
        m_s_a_r = ((a_r_p * a_i) / 128) * den * 10000  # maximum seed application rate=application rate*10000
        nagy_bird = fi_bird * 0.001 * m_s_a_r / nagy_bird_coef
        return (nagy_bird / at_bird)

    def sa_bird_2(self, a_r_p, a_i, den, m_s_r_p, at_bird, ld50_bird, aw_bird, tw_bird, x, nagy_bird_coef):
        """
        Seed treatment acute rq for birds method 2
        :param a_r_p:
        :param a_i:
        :param den:
        :param m_s_r_p:
        :param at_bird:
        :param ld50_bird:
        :param aw_bird:
        :param tw_bird:
        :param x:
        :param nagy_bird_coef:
        :return:
        """
        at_bird = at_bird(ld50_bird, aw_bird, tw_bird, x)
        m_a_r = (m_s_r_p * ((a_i * a_r_p) / 128) * den) / 100  # maximum application rate
        av_ai = m_a_r * 1e6 / (43560 * 2.2)
        return (av_ai / (at_bird * nagy_bird_coef))

    def sc_bird(self, a_r_p, a_i, den, noaec_bird):
        """
        Seed treatment chronic rq for birds
        :param a_r_p:
        :param a_i:
        :param den:
        :param noaec_bird:
        :return:
        """
        m_s_a_r = ((a_r_p * a_i) / 128) * den * 10000  # maximum seed application rate=application rate*10000
        return (m_s_a_r / noaec_bird)

    def sa_mamm_1(self, a_r_p, a_i, den, at_mamm, fi_mamm, mf_w_bird, ld50_mamm, aw_mamm, tw_mamm, nagy_mamm_coef):
        """
        Seed treatment acute rq for mammals method 1
        :param a_r_p:
        :param a_i:
        :param den:
        :param at_mamm:
        :param fi_mamm:
        :param mf_w_bird:
        :param ld50_mamm:
        :param aw_mamm:
        :param tw_mamm:
        :param nagy_mamm_coef:
        :return:
        """
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        fi_mamm = fi_mamm(aw_mamm, mf_w_bird)
        m_s_a_r = ((a_r_p * a_i) / 128) * den * 10000  # maximum seed application rate=application rate*10000
        nagy_mamm = fi_mamm * 0.001 * m_s_a_r / nagy_mamm_coef
        return (nagy_mamm / at_mamm)

    def sa_mamm_2(self, a_r_p, a_i, den, m_s_r_p, at_mamm, ld50_mamm, aw_mamm, tw_mamm, nagy_mamm_coef):
        """
        Seed treatment acute rq for mammals method 2
        :param a_r_p:
        :param a_i:
        :param den:
        :param m_s_r_p:
        :param at_mamm:
        :param ld50_mamm:
        :param aw_mamm:
        :param tw_mamm:
        :param nagy_mamm_coef:
        :return:
        """
        at_mamm = at_mamm(ld50_mamm, aw_mamm, tw_mamm)
        m_a_r = (m_s_r_p * ((a_r_p * a_i) / 128) * den) / 100  # maximum application rate
        av_ai = m_a_r * 1000000 / (43560 * 2.2)
        return (av_ai / (at_mamm * nagy_mamm_coef))

    def sc_mamm(self, a_r_p, a_i, den, noael_mamm, aw_mamm, fi_mamm, mf_w_bird, tw_mamm, anoael_mamm, nagy_mamm_coef):
        """
        Seed treatment chronic rq for mammals
        :param a_r_p:
        :param a_i:
        :param den:
        :param noael_mamm:
        :param aw_mamm:
        :param fi_mamm:
        :param mf_w_bird:
        :param tw_mamm:
        :param anoael_mamm:
        :param nagy_mamm_coef:
        :return:
        """
        anoael_mamm = anoael_mamm(noael_mamm, aw_mamm, tw_mamm)
        fi_mamm = fi_mamm(aw_mamm, mf_w_bird)
        m_s_a_r = ((a_r_p * a_i) / 128) * den * 10000  # maximum seed application rate=application rate*10000
        nagy_mamm = fi_mamm * 0.001 * m_s_a_r / nagy_mamm_coef
        return (nagy_mamm / anoael_mamm)
