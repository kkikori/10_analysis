import datetime as dt

import analysis_funcs
import matplotlib.pyplot as plt


def increase_rate_total_compare(w1, w2, save_f):
    print("increase_rate_total_compare")

    fig = plt.figure()
    # グラフ化(エラーバー付折れ線グラフ)
    x = list(range(10, 121, 10))
    # claim agent : tomato
    # random agent : gold
    # users : steelblue

    plt.plot(x, w1[1], label="users_w1_1", color="steelblue", linewidth=1,linestyle="dashed")
    plt.plot(x, w1[3], label="users_w1_2", color="steelblue", linewidth=1,linestyle="dashed")
    plt.plot(x, w2[1], label="users_w2_2", color="steelblue", linewidth=1,linestyle="dashed")
    plt.plot(x, w2[3], label="users_w2_1", color="steelblue", linewidth=1,linestyle="dashed")

    plt.plot(x, w1[2], label="random_agent_w1", color="orange", linewidth=2)
    plt.plot(x, w2[2], label="random_agent_w1", color="gold", linewidth=2)
    plt.plot(x, w1[0], label="agent_w1", color="red", linewidth=2)
    plt.plot(x, w2[0], label="agent_w2", color="tomato", linewidth=2)

    save_f = save_f / "total.png"
    #plt.legend(loc="upper left")
    plt.savefig(str(save_f))
    # plt.show()


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

    for gap_t in range(10, 121, 10):
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

    fig = plt.figure()
    # グラフ化(エラーバー付折れ線グラフ)
    xtick = list(range(10, 121, 10))
    # print(len(xtick), len(f_ave_list), len(f_std_list))
    # plt.errorbar(xtick, f_ave_list, f_std_list, label="facilitator", color="orange", linewidth=2)
    plt.plot(xtick, f_ave_list, label="facilitator", color="orange", linewidth=2)
    # darkcyan
    # firebrick

    x = list(map(lambda x: x + 1, xtick))  # 標準偏差が見にくいので
    # plt.errorbar(x, u_ave_list, u_std_list, label="user", color="steelblue", linewidth=2)
    plt.plot(x, u_ave_list, label="user", color="steelblue", linewidth=2)
    plt.legend(loc="upper left")

    plt.savefig(str(save_f))

    return f_ave_list, u_ave_list


def increase_rate_main(Week, save_f, week):
    agent_Type = "claim"
    print("agent type ", agent_Type)
    # sav_name = week + agent_Type + "_post_nums.csv"
    # _per_post_nums_detail(Week.claim_post_l, agent_Type, save_f / sav_name, gap_td_list)
    # sav_name = week + agent_Type + "_error_bar.png"
    sav_name = week + agent_Type + "_linegraph.png"
    c_f, c_u = _per_post_nums(Week.claim_post_l, agent_Type, save_f / sav_name)

    agent_Type = "random"
    print("agent type ", agent_Type)
    # sav_name = week + agent_Type + "_post_nums.csv"
    # _per_post_nums_detail(Week.random_post_l, agent_Type, save_f / sav_name, gap_td_list)

    # sav_name = week + agent_Type + "_error_bar.png"
    sav_name = week + agent_Type + "_linegraph.png"
    r_f, r_u = _per_post_nums(Week.random_post_l, agent_Type, save_f / sav_name)

    return c_f, c_u, r_f, r_u
