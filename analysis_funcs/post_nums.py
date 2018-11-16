import csv
import datetime as dt


def _counter_p(p_time_list, gap_td):
    threshold = p_time_list[0]["t"] + gap_td
    pnum = -1
    for p_t in p_time_list:
        if p_t["t"] > threshold:
            if pnum == -1:
                pnum = 0
            return pnum
        elif p_t["usr"]:  # 管理者ユーザでない場合
            pnum += 1
    if pnum == -1:
        pnum = 0
    return pnum


def _count_gap_post(Post_list, pi_list, p_time_list, gap_td):
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


def _per_post_nums(Post_list, agent_Type, save_f, gap_td_list):
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
            gap_l, facilitator_l, usr_l = _count_gap_post(Post_list, pi_list, p_time_list, gap_td)
            writer.writerow(["gap_time:", str(gap_td)])
            writer.writerow(["facilitator"])
            writer.writerow(facilitator_l)
            writer.writerow(["user"])
            writer.writerow(usr_l)
            writer.writerows([[], []])

    return


def post_nums_main(Week, save_f, week):
    gap_td_list = [dt.timedelta(minutes=15), dt.timedelta(minutes=30), dt.timedelta(hours=1), dt.timedelta(hours=2)]

    agent_Type = "claim"
    print("agent type ", agent_Type)
    sav_name = week + agent_Type + "_post_nums.csv"
    _per_post_nums(Week.claim_post_l, agent_Type, save_f / sav_name, gap_td_list)


    agent_Type = "random"
    print("agent type ", agent_Type)
    sav_name = week + agent_Type + "_post_nums.csv"
    _per_post_nums(Week.random_post_l, agent_Type, save_f / sav_name, gap_td_list)