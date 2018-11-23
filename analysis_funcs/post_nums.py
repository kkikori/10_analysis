import csv
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


def _counter_p(p_time_list, gap_td):
    threshold = p_time_list[0]["t"] + gap_td
    pnum = 0
    if len(p_time_list) <= 1:
        return pnum

    for p_t in p_time_list[1:]:
        if p_t["t"] > threshold:
            return pnum
        #elif p_time_list[-1]["t"] < threshold:
            #return pnum
        elif p_t["usr"]:  # 管理者ユーザの投稿は除く
            pnum += 1
    return pnum


def count_gap_post(Post_list, pi_list, p_time_list, gap_td):
    # その後調べる
    gap_posts = []
    facilitator_gap_times = []
    usr_gap_times = []
    for pidx, pi in enumerate(pi_list):
        gap_ps = _counter_p(p_time_list[pidx:], gap_td)
        gap_posts.append(gap_ps)

        if Post_list[pi].user_id not in ["facilitator", "kitkat"]:
            usr_gap_times.append(gap_ps)
        elif Post_list[pi].user_id == "facilitator":
            facilitator_gap_times.append(gap_ps)

    return gap_posts, facilitator_gap_times, usr_gap_times


def _per_post_nums_detail(Post_list, agent_Type, save_f, gap_td_list):
    pi_list = sorted(Post_list.keys())

    # 時間のみを先に取り出す
    # 管理者ユーザか参加者かをtrue,falseで表す
    p_time_list = []
    for pi in pi_list:
        if Post_list[pi].user_id not in ["facilitator", "kitkat"]:
            p_time_list.append({"t": Post_list[pi].created_at, "usr": True})
        else:
            p_time_list.append({"t": Post_list[pi].created_at, "usr": False})

    # gap_tdごとに調べてファイルに書き込む
    with save_f.open("w") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerow([agent_Type])
        for gap_td in gap_td_list:
            gap_l, facilitator_l, usr_l = count_gap_post(Post_list, pi_list, p_time_list, gap_td)

            f_ave = sum(facilitator_l) / len(facilitator_l)
            u_ave = sum(usr_l) / len(usr_l)

            writer.writerow(["gap_time:", str(gap_td)])
            writer.writerow(["facilitator", f_ave])
            writer.writerow(facilitator_l)
            writer.writerow(["user", u_ave])
            writer.writerow(usr_l)
            writer.writerows([[], []])

    return


def ave_and_var(plist):
    pl = np.array(plist)
    return np.average(pl), np.std(pl)


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
        gap_l, facilitator_l, usr_l = count_gap_post(Post_list, pi_list, p_time_list, gap_td)

        f_ave, f_std = ave_and_var(facilitator_l)
        f_ave_list.append(f_ave)
        f_std_list.append(f_std)

        u_ave, u_std = ave_and_var(usr_l)
        u_ave_list.append(u_ave)
        u_std_list.append(u_std)
    fig = plt.figure()
    # グラフ化(エラーバー付折れ線グラフ)
    xtick = list(range(10, 121, 10))
    print(len(xtick), len(f_ave_list), len(f_std_list))
    plt.errorbar(xtick, f_ave_list, f_std_list, label="facilitator", color="orange", linewidth=2)
    # plt.plot(xtick, f_ave_list, label="facilitator", color="orange", linewidth=2)
    # darkcyan
    # firebrick

    x = list(map(lambda x: x + 1, xtick))  # 標準偏差が見にくいので
    plt.errorbar(x, u_ave_list, u_std_list, label="user", color="steelblue", linewidth=2)
    # plt.plot(x, u_ave_list,label="user", color="steelblue", linewidth=2)
    plt.legend(loc="upper left")

    plt.savefig(str(save_f))

    return


def post_nums_main(Week, save_f, week):
    gap_td_list = [dt.timedelta(minutes=15), dt.timedelta(minutes=30), dt.timedelta(hours=1), dt.timedelta(hours=2)]

    agent_Type = "claim"
    print("agent type ", agent_Type)
    # sav_name = week + agent_Type + "_post_nums.csv"
    # _per_post_nums_detail(Week.claim_post_l, agent_Type, save_f / sav_name, gap_td_list)
    sav_name = week + agent_Type + "_errobar_dead.png"
    #sav_name = week + agent_Type + "_linegraph.png"
    _per_post_nums(Week.claim_post_l, agent_Type, save_f / sav_name)

    agent_Type = "random"
    print("agent type ", agent_Type)
    # sav_name = week + agent_Type + "_post_nums.csv"
    # _per_post_nums_detail(Week.random_post_l, agent_Type, save_f / sav_name, gap_td_list)

    sav_name = week + agent_Type + "_errorbar_dead.png"
    _per_post_nums(Week.random_post_l, agent_Type, save_f / sav_name)
