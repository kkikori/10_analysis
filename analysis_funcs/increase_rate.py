import datetime as dt

import analysis_funcs
import matplotlib.pyplot as plt


def _increase_rate(pidx, p_time_list, gap_td):
    before_posts = 0
    threshold = p_time_list[pidx]["t"] - gap_td
    if pidx == 0 or p_time_list[0]["t"] > threshold:
        return False
    for p_t in p_time_list[:pidx]:
        if p_t["t"] > threshold:
            before_posts += 1
    if before_posts == 0:
        return False

    threshold = p_time_list[pidx]["t"] + gap_td
    after_posts = 0
    if pidx > len(p_time_list) - 2 or p_time_list[-1]["t"] < threshold:
        return False
    for p_t in p_time_list[pidx + 1:]:
        if p_t["t"] > threshold:
            break
        elif p_t["usr"]:  # 管理者ユーザの投稿は除く
            after_posts += 1

    increase_r = (float((after_posts - before_posts)) / float(before_posts)) * 100
    # print(after_posts, before_posts, increase_r)
    return increase_r


def count_gap_post(Post_list, pi_list, p_time_list, gap_td):
    facilitator_gap_times = []
    usr_gap_times = []
    for pidx, pi in enumerate(pi_list):
        # 変化させるとこTODO
        gap_ps = _increase_rate(pidx, p_time_list, gap_td)
        if not gap_ps:
            continue

        if Post_list[pi].user_id not in ["facilitator", "kitkat"]:
            usr_gap_times.append(gap_ps)
        elif Post_list[pi].user_id == "facilitator":
            facilitator_gap_times.append(gap_ps)

    return facilitator_gap_times, usr_gap_times


def _per_post_nums(Post_list, agent_Type, save_f):
    pi_list = sorted(Post_list.keys())

    # 時間のみを先に取り出す
    # 管理者ユーザか参加者かをtrue,falseで表す
    p_time_list = []
    for pi in pi_list:
        if Post_list[pi].user_id not in ["facilitator", "kitkat"]:
            p_time_list.append({"t": Post_list[pi].created_at, "usr": True})
        else:
            p_time_list.append({"t": Post_list[pi].created_at, "usr": False})

    f_ave_list, f_std_list = [], []
    u_ave_list, u_std_list = [], []

    for gap_t in range(10, 11, 10):
        gap_td = dt.timedelta(minutes=gap_t)
        facilitator_l, usr_l = count_gap_post(Post_list, pi_list, p_time_list, gap_td)

        f_ave, f_std = analysis_funcs.ave_and_var(facilitator_l)
        f_ave_list.append(f_ave)
        f_std_list.append(f_std)

        u_ave, u_std = analysis_funcs.ave_and_var(usr_l)
        u_ave_list.append(u_ave)
        u_std_list.append(u_std)

        print("gap_t", gap_t)
        print("facilitator", facilitator_l)
        print("uer", usr_l)

    return


def increase_rate_main(Week, save_f, week):
    gap_td_list = [dt.timedelta(minutes=15), dt.timedelta(minutes=30), dt.timedelta(hours=1), dt.timedelta(hours=2)]

    agent_Type = "claim"
    print("agent type ", agent_Type)
    # sav_name = week + agent_Type + "_post_nums.csv"
    # _per_post_nums_detail(Week.claim_post_l, agent_Type, save_f / sav_name, gap_td_list)
    sav_name = week + agent_Type + "_increase_rate.png"
    # sav_name = week + agent_Type + "_linegraph.png"
    _per_post_nums(Week.claim_post_l, agent_Type, save_f / sav_name)

    agent_Type = "random"
    print("agent type ", agent_Type)
    # sav_name = week + agent_Type + "_post_nums.csv"
    # _per_post_nums_detail(Week.random_post_l, agent_Type, save_f / sav_name, gap_td_list)

    sav_name = week + agent_Type + "_increase_rate.png"
    _per_post_nums(Week.random_post_l, agent_Type, save_f / sav_name)
