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


def counter_post_per_thread(Thread_list, Post_list, agent_Type, save_f):
    start_t = _set_start_time(Post_list)
    finish_t = start_t + dt.timedelta(hours=47)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for th_i in range(1, len(Thread_list) + 1):
        thread = Thread_list[th_i]
        print(" title", thread.title, th_i)
        x_times, y_nums = _extract_time(thread.pi_list, Post_list)
        if len(x_times) == 0:
            print("     this thread has not post from users.")
            continue

        ax.plot(x_times, y_nums, label=th_i, color=cm.spring((th_i - 1) / len(Thread_list)))

    minutes = mdates.MinuteLocator(interval=5)  # 5分間隔で描画
    timeFmt = mdates.DateFormatter('%H:%M')  # x軸の時刻表示フォーマットの設定
    ax.xaxis.set_major_locator(minutes)  # 上記の条件をグラフに設定
    ax.xaxis.set_major_formatter(timeFmt)  # 上記の条件をグラフに設定
    plt.xlim(start_t, finish_t)  # x軸の範囲を設定
    plt.ylim(0, 70)  # y軸の範囲を設定
    plt.title(agent_Type)
    # plt.legend(loc='upper left')  #データの名前を表示
    fig.autofmt_xdate()  # いい感じにx軸の時刻表示を調節

    plt.savefig(save_f)
    plt.show()


def time_series_analysis_main(Week, save_f,week):
    agent_Type = "claim"
    sav_name = week + agent_Type + ".png"
    counter_post_per_thread(Week.claim_thread_l, Week.claim_post_l, agent_Type, save_f/sav_name)

    agent_Type = "random"
    sav_name = week + agent_Type + ".png"
    counter_post_per_thread(Week.random_thread_l, Week.random_post_l, agent_Type, save_f/sav_name)
