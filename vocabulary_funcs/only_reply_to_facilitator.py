import vocabulary_funcs
import analysis_funcs

import matplotlib.pyplot as plt


def _tfidf_extract(ui_list, Post_list, mrph_path):
    Tfidf = vocabulary_funcs.TfidfClass(f_mrph=mrph_path)
    f_tfidf, else_tfidf = [], []
    for pi in ui_list:
        # print("   pi", pi)
        Tfidf.add_post_words(pi)
        post = Post_list[pi]
        post_tfidf = Tfidf.ref_tfidf_from_pi(pi)

        if not post.reply_to_id:
            else_tfidf.append(post_tfidf)
        elif Post_list[post.reply_to_id].user_id == "facilitator":
            f_tfidf.append(post_tfidf)
        else:
            else_tfidf.append(post_tfidf)

    return f_tfidf, else_tfidf


def _idf_extract(ui_list, Post_list, mrph_path):
    Tfidf = vocabulary_funcs.TfidfClass(f_mrph=mrph_path)
    f_tfidf, else_tfidf = [], []
    for pi in ui_list:
        # print("   pi", pi)
        Tfidf.add_post_words(pi)
        post = Post_list[pi]

        post_idf = Tfidf.ref_idf_per_pi(pi)

        if not post_idf:
            continue

        if not post.reply_to_id:
            else_tfidf.append(max(post_idf.values()))
        elif Post_list[post.reply_to_id].user_id == "facilitator":
            f_tfidf.append(max(post_idf.values()))
        else:
            else_tfidf.append(max(post_idf.values()))

    return f_tfidf, else_tfidf


def graphing(fs, us, save_f):
    # https://stats.biopapyrus.jp/python/barplot.html
    error_bar_set = dict(
        lw=1,
        capthick=1,
        capsize=2
    )

    fig = plt.figure(figsize=(16, 9))
    print(us)
    print(fs)
    u_xs = list(range(len(us[2])))
    print("usr", u_xs)
    plt.bar(u_xs, us[0], yerr=us[1], label="user", color="steelblue", width=0.4, error_kw=error_bar_set)

    f_xs = list(map(lambda x: x + 0.4, fs[2]))  # 標準偏差が見にくいので
    print("fa", f_xs)
    plt.bar(f_xs, fs[0], yerr=fs[1], label="facilitator", color="orange", width=0.4, error_kw=error_bar_set)

    u_xs = [x + 0.2 for x in u_xs]
    plt.xticks(u_xs, us[2])
    plt.legend(loc="best")
    # plt.show()
    plt.savefig(str(save_f))


def only_reply_to_facilitator(User_list, Post_list, mrph_path, save_f):
    usrs_idfs = []

    f_ave_list, f_std_list, f_x_list = [], [], []
    u_ave_list, u_std_list = [], []

    usr_name_list = list(User_list.keys())

    usr_name_list.remove("kitkat")
    usr_name_list.remove("facilitator")

    print(usr_name_list, type(usr_name_list))
    for u_idx, u_n in enumerate(usr_name_list):
        print(u_idx, ":", u_n)

    for u_idx, u_n in enumerate(usr_name_list):
        print("[", u_idx, "]", ":", "user name ", u_n)

        f_list, u_list = _idf_extract(User_list[u_n].pi_list, Post_list, mrph_path)

        if len(f_list) != 0:
            print("  ", u_n, "has reply to facilitator!!")
            f_ave, f_std = analysis_funcs.ave_and_var(f_list)
            f_ave_list.append(f_ave)
            f_std_list.append(f_std)
            f_x_list.append(u_idx)
        else:
            print("  ", u_n, "didn't reply to facilitator.")
        # print(u_list)
        u_ave, u_std = analysis_funcs.ave_and_var(u_list)
        u_ave_list.append(u_ave)
        u_std_list.append(u_std)
        # u_name_list[u_idx] = u_n + " (" + str(len(f_list)) + ")"

    graphing([f_ave_list, f_std_list, f_x_list], [u_ave_list, u_std_list, usr_name_list], save_f)
