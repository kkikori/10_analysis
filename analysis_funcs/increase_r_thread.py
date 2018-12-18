import datetime as dt
import analysis_funcs
from pathlib import Path

def _per_post_nums(Post_list, Thread_list):
    thi_list = sorted(list(Thread_list.keys()))
    thi_list.remove(1)

    # 時間のみを先に出す
    # 管理者ユーザか参加者かをtrue,falseで表す
    p_time_list = {}
    for thi in thi_list:
        thread = Thread_list[thi]
        thread_times = []
        for pi in thread.pi_list:
            if Post_list[pi].user_id not in ["facilitator", "kitkat"]:
                thread_times.append({"t": Post_list[pi].created_at, "usr": True})
            else:
                thread_times.append({"t": Post_list[pi].created_at, "usr": False})
        p_time_list[thi] = thread_times

    f_ave_list, f_std_list = [], []
    u_ave_list, u_std_list = [], []

    for gap_t in range(10, 121, 10):
        gap_td = dt.timedelta(minutes=gap_t)

        facilitator_l, usr_l = [], []
        for thi, th_times in p_time_list.items():
            f_l, u_l = analysis_funcs.count_gap_post(Thread_list[thi].pi_list, th_times, gap_td)
            facilitator_l.extend(f_l)
            usr_l.extend(u_l)

        f_ave, f_std = analysis_funcs.ave_and_var(facilitator_l)
        f_ave_list.append(f_ave)
        f_std_list.append(f_std)

        u_ave, u_std = analysis_funcs.ave_and_var(usr_l)
        u_ave_list.append(u_ave)
        u_std_list.append(u_std)

        # print("gap_t", gap_t)
        # print("facilitator", facilitator_l)
        # print("uer", usr_l)

    return f_ave_list, u_ave_list


def per_week(Week):
    agent_Type = "claim"
    c_f, c_u = _per_post_nums(Week.claim_post_l, Week.claim_th_l)
    agent_Type = "random"
    r_f, r_u = _per_post_nums(Week.random_post_l, Week.random_th_l)
    return c_f, c_u, r_f, r_u


def increase_rate2_main(Week1, Week2):
    print("increase_rate2_main")
    save_f = Path("/Users/ida/Amazon Drive/201810結果")
    c_f, c_u, r_f, r_u = per_week(Week1)
    w1 = [c_f, c_u, r_f, r_u]
    c_f, c_u, r_f, r_u = per_week(Week2)
    w2 = [c_f, c_u, r_f, r_u]

    analysis_funcs.increase_rate_total_compare(w1, w2, save_f / "increase_rate2")
