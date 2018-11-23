import analysis_funcs
import datetime as dt
import time


import numpy as np
from scipy import stats


def _per_post_nums(Post_list, gap_t_th):
    pi_list = sorted(Post_list.keys())

    # 時間のみを先に取り出す
    # 管理者ユーザか参加者かをtrue,falseで表す
    p_time_list = []
    for pi in pi_list:
        if Post_list[pi].user_id not in ["facilitator", "kitkat"]:
            p_time_list.append({"t": Post_list[pi].created_at, "usr": True})
        else:
            p_time_list.append({"t": Post_list[pi].created_at, "usr": False})

    f_ave_list, u_ave_list = [], []

    for gap_t in range(10, gap_t_th, 10):
        gap_td = dt.timedelta(minutes=gap_t)
        gap_l, facilitator_l, usr_l = analysis_funcs.count_gap_post(Post_list, pi_list, p_time_list, gap_td)

        f_ave, _ = analysis_funcs.ave_and_var(facilitator_l)
        f_ave_list.append(f_ave)
        u_ave, u_std = analysis_funcs.ave_and_var(usr_l)
        u_ave_list.append(u_ave)

    return f_ave_list, u_ave_list


# post_nums.pyの検定version
def test_post_nums(Week1, Week2, save_f):
    for gap_t_th in range(11, 121, 10):
        w1_c_f, w1_c_u = _per_post_nums(Week1.claim_post_l, gap_t_th)
        w1_r_f, w1_r_u = _per_post_nums(Week1.random_post_l, gap_t_th)
        w2_c_f, w2_c_u = _per_post_nums(Week2.claim_post_l, gap_t_th)
        w2_r_f, w2_r_u = _per_post_nums(Week2.random_post_l, gap_t_th)

        w1_c_delta = [f - c for f, c in zip(w1_c_f, w1_c_u)]
        w1_r_delta = [f - c for f, c in zip(w1_r_f, w1_r_u)]
        w2_c_delta = [f - c for f, c in zip(w2_c_f, w2_c_u)]
        w2_r_delta = [f - c for f, c in zip(w2_r_f, w2_r_u)]

        w1_c_delta.extend(w2_c_delta)
        w1_r_delta.extend(w2_r_delta)
        time.sleep(2)
        r = stats.wilcoxon(w1_c_delta, w1_r_delta)
        print("gap_t_th", gap_t_th)
        print(r)
