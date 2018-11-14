import numpy as np
import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm  # http://matplotlib.org/examples/color/colormaps_reference.html

import datetime as dt

import analysis_funcs


def change_aspect_ratio(ax, ratio):
    '''
    This function change aspect ratio of figure.
    Parameters:
        ax: ax (matplotlit.pyplot.subplots())
            Axes object
        ratio: float or int
            relative x axis width compared to y axis width.
    '''
    aspect = (1 / ratio) * (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.set_aspect(aspect)


def _extract_time(pi_list, Post_list, u_i=False, u_num=False):
    x_times = []
    y_nums = []

    for pi in pi_list:
        x_times.append(Post_list[pi].created_at)

        if not u_i:
            y_nums.append(Post_list[pi].belong_th_i)
        else:
            y = 0.6 * float(u_i / u_num) - 0.3
            y_nums.append(Post_list[pi].belong_th_i + y)

    return x_times, y_nums


def effects(User_list, Post_list,th_num ,agent_Type, save_f):
    start_t, finish_t = analysis_funcs._set_start_time(Post_list)
    finish_t = finish_t
    print(finish_t)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for u_i, u_n in enumerate(User_list.keys()):
        if u_n in ["facilitator", "kitkat"]:
            continue
        user = User_list[u_n]
        x_times, y_nums = _extract_time(user.pi_list, Post_list, u_i, len(User_list))

        ax.scatter(x_times, y_nums, s=1, label=user.name, color=cm.spring((u_i - 1) / len(User_list)))

    x_times, y_nums = _extract_time(User_list["facilitator"].pi_list, Post_list)
    ax.scatter(x_times, y_nums, s=1, label="facilitator", color="k")

    days = mdates.MinuteLocator(interval=120)
    daysFmt = mdates.DateFormatter('%H')
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(daysFmt)
    plt.xlim(start_t, finish_t)
    # plt.ylim(1, 13)
    plt.yticks(np.arange(1, th_num+1, 1))
    # plt.title(agent_Type)
    plt.hlines(list(range(1, th_num+1)), start_t, finish_t, "gray", linestyle=":", lw=0.1)  # グリット線の代わり

    # plt.legend(loc='upper left')  # ラベルの表示
    fig.autofmt_xdate()  # 時刻をいい感じに表示
    change_aspect_ratio(ax, 6)  # グラフの縦横比変更
    plt.savefig(str(save_f), dpi=500)
    # plt.show()


def facilitator_effect_main(Week, save_f, week):
    # スレッドごとの投稿リスト
    agent_Type = "claim"
    sav_name = week + agent_Type + "_facilitator_effect" + ".png"
    effects(Week.claim_usr_l, Week.claim_post_l, len(Week.claim_th_l), agent_Type, save_f / sav_name)

    agent_Type = "random"
    sav_name = week + agent_Type + "_facilitator_effect" + ".png"
    effects(Week.random_usr_l, Week.random_post_l, len(Week.random_th_l), agent_Type, save_f / sav_name)
