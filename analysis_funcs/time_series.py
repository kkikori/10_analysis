import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm  # http://matplotlib.org/examples/color/colormaps_reference.html

import datetime as dt


def _set_start_time(Post_list):
    pi_list = Post_list.keys()
    pi_list = sorted(pi_list)

    return Post_list[pi_list[0]].created_at


def _extract_time(pi_list, Post_list):
    post_num = 0

    x_times = []
    y_nums = []

    for pi in pi_list:
        if Post_list[pi].user_id in ["facilitator", "kitkat"]:
            continue
        x_times.append(Post_list[pi].created_at)
        y_nums.append(post_num)
        post_num += 1

    return x_times, y_nums


# スレッドごとの投稿数の増加
def counter_post_per_thread(Thread_list, Post_list, agent_Type, save_f):
    start_t = _set_start_time(Post_list)
    finish_t = start_t + dt.timedelta(hours=47)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for th_i in range(1, len(Thread_list) + 1):
        thread = Thread_list[th_i]
        print(" title", th_i, thread.title)
        x_times, y_nums = _extract_time(thread.pi_list, Post_list)
        if len(x_times) == 0:
            print("     this thread has not post from users.")
            continue

        ax.plot(x_times, y_nums, label=th_i, color=cm.spring((th_i - 1) / len(Thread_list)))

    print(len(x_times))
    print(len(y_nums))
    minutes = mdates.MinuteLocator(interval=120)  # interval分間隔で描画
    timeFmt = mdates.DateFormatter('%H:%M')  # x軸の時刻表示フォーマットの設定
    ax.xaxis.set_major_locator(minutes)  # 上記の条件をグラフに設定
    ax.xaxis.set_major_formatter(timeFmt)  # 上記の条件をグラフに設定
    plt.xlim(start_t, finish_t)  # x軸の範囲を設定
    plt.ylim(0, 30)  # y軸の範囲を設定
    plt.title(agent_Type)
    # plt.legend(loc='upper left')  #データの名前を表示
    fig.autofmt_xdate()  # いい感じにx軸の時刻表示を調節

    plt.savefig(str(save_f))
    # plt.show()
    print(save_f)


def counter_post_per_user(User_list, Post_list, agent_Type, save_f):
    start_t = _set_start_time(Post_list)
    finish_t = start_t + dt.timedelta(hours=47)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    sort_uilist = sorted(User_list.keys())
    for u_i in sort_uilist:
        if u_i in ["facilitator", "kitkat"]:
            continue
        user = User_list[u_i]
        print(" user", user.name, u_i)
        x_times, y_nums = _extract_time(user.pi_list, Post_list)
        if len(x_times) == 0:
            print("     this thread has not post from users.")
            continue

        ax.plot(x_times, y_nums, label=user.name, color=cm.summer((u_i - 1) / len(User_list)))
        ax.plot(x_times[-1], y_nums[-1], marker='o', color=cm.summer((u_i - 1) / len(User_list)))

    days = mdates.MinuteLocator(interval=5)
    daysFmt = mdates.DateFormatter('%H:%M')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    plt.xlim(start_t, finish_t)
    plt.ylim(0, 40)
    plt.title(agent_Type)
    plt.legend(loc='upper left')
    fig.autofmt_xdate()
    plt.savefig(str(save_f))
    plt.show()


def time_series_analysis_main(Week, save_f, week):
    # スレッドごとの投稿リスト
    agent_Type = "claim"
    sav_name = week + agent_Type + "_time_series_thread" + ".png"
    counter_post_per_thread(Week.claim_th_l, Week.claim_post_l, agent_Type, save_f / sav_name)

    agent_Type = "random"
    sav_name = week + agent_Type + "_time_series_thread" + ".png"
    counter_post_per_thread(Week.random_th_l, Week.random_post_l, agent_Type, save_f / sav_name)

    # スレッドごとの投稿リスト
    agent_Type = "claim"
    sav_name = week + agent_Type + "_time_series_user" + ".png"
    counter_post_per_thread(Week.claim_usr_l, Week.claim_post_l, agent_Type, save_f / sav_name)

    agent_Type = "random"
    sav_name = week + agent_Type + "_time_series_user" + ".png"
    counter_post_per_thread(Week.random_usr_l, Week.random_post_l, agent_Type, save_f / sav_name)
