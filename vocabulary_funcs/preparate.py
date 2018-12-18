from pathlib import Path
import vocabulary_funcs
import analysis_funcs

import matplotlib.pyplot as plt

Unamelist = ["panda", "dolphin", "elephant", "owl", "squirrel", "rabbit", "mouse", "lion"]


def _idf_extract(pi_list, Post_list, mrph_path, u_tfidf, f_tfidf):
    Tfidf = vocabulary_funcs.TfidfClass(f_mrph=mrph_path)

    for pi in pi_list:
        post = Post_list[pi]
        if post.user_id in ["facilitator", "kitkat"]:
            continue
        Tfidf.add_post_words(pi)
        post = Post_list[pi]
        post_idf = Tfidf.ref_idf_per_pi(pi)

        if not post_idf:
            continue

        uidx = Unamelist.index(post.user_id)
        if not post.reply_to_id:
            u_tfidf[uidx].append(max(post_idf.values()))
        elif Post_list[post.reply_to_id].user_id == "facilitator":
            f_tfidf[uidx].append(max(post_idf.values()))
        else:
            u_tfidf[uidx].append(max(post_idf.values()))

    print("f_tfidf", f_tfidf)
    return u_tfidf, f_tfidf

# 全体で見るやつ
def only_rep2agent_over(Post_list, mrph_path, save_f):
    u_tfidf = [[], [], [], [], [], [], [], []]
    f_tfidf = [[], [], [], [], [], [], [], []]

    u_ave_list, u_std_list = [], []
    f_ave_list, f_std_list, f_x_list = [], [], []

    pi_list = sorted(list(Post_list.keys()))
    u_tfidf, f_tfidf = _idf_extract(pi_list, Post_list, mrph_path, u_tfidf, f_tfidf)
    for uidx, u_n in enumerate(Unamelist):
        if len(f_tfidf[uidx]) != 0:
            f_ave, f_std = analysis_funcs.ave_and_var(f_tfidf[uidx])
            f_ave_list.append(f_ave)
            f_std_list.append(f_std)
            f_x_list.append(uidx)
        u_ave, u_std = analysis_funcs.ave_and_var(u_tfidf[uidx])
        u_ave_list.append(u_ave)
        u_std_list.append(u_std)

    print(Unamelist)
    vocabulary_funcs.graphing_idf([f_ave_list, f_std_list, f_x_list], [u_ave_list, u_std_list, Unamelist], save_f)


def only_rep2agent(Thread_list, Post_list, mrph_path, save_f):
    thi_list = sorted(list(Thread_list.keys()))
    thi_list.remove(1)

    u_ave_list, u_std_list = [], []
    f_ave_list, f_std_list, f_x_list = [], [], []

    u_tfidf = [[], [], [], [], [], [], [], []]
    f_tfidf = [[], [], [], [], [], [], [], []]

    for thi in thi_list:
        thread = Thread_list[thi]
        print(thi, " : ", thread.title)
        u_tfidf, f_tfidf = _idf_extract(thread.pi_list, Post_list, mrph_path, u_tfidf, f_tfidf)

    for uidx, u_n in enumerate(Unamelist):
        if len(f_tfidf[uidx]) != 0:
            f_ave, f_std = analysis_funcs.ave_and_var(f_tfidf[uidx])
            f_ave_list.append(f_ave)
            f_std_list.append(f_std)
            f_x_list.append(uidx)
        u_ave, u_std = analysis_funcs.ave_and_var(u_tfidf[uidx])
        u_ave_list.append(u_ave)
        u_std_list.append(u_std)

    print(Unamelist)

    print("f_ave_list", f_ave_list)

    print("f_std_list", f_std_list)
    # [print(k) for k in f_std_list]
    print("f_x_list", f_x_list)
    # [print(k) for k in f_x_list]

    print("u_ave_list", u_ave_list)
    # [print(k) for k in u_ave_list]
    print("u_std_list", u_std_list)
    # [print(k) for k in u_std_list]


    vocabulary_funcs.graphing_idf([f_ave_list, f_std_list, f_x_list], [u_ave_list, u_std_list, Unamelist], save_f)


def vocab_usr(Week, save_f, week):
    agent_Type = "claim"
    print("agent type ", agent_Type)
    # sav_n = week + agent_Type + "_errorbar.png"
    # sav_n = week + agent_Type + "_errorbar_thread.png"
    sav_n = week + agent_Type + "_errorbar_over.png"
    # vocabulary_funcs.only_reply_to_facilitator(Week.claim_usr_l, Week.claim_post_l, Week.claim_mrph, save_f / sav_n)
    # only_rep2agent(Week.claim_th_l, Week.claim_post_l, Week.claim_mrph, save_f / sav_n)
    only_rep2agent_over(Week.claim_post_l, Week.claim_mrph, save_f / sav_n)

    agent_Type = "random"
    print("agent type ", agent_Type)
    # sav_n = week + agent_Type + "_errorbar.png"
    # sav_n = week + agent_Type + "_errorbar_thread.png"
    sav_n = week + agent_Type + "_errorbar_over.png"
    # vocabulary_funcs.only_reply_to_facilitator(Week.random_usr_l, Week.random_post_l, Week.random_mrph, save_f / sav_n)
    # only_rep2agent(Week.random_th_l, Week.random_post_l, Week.random_mrph, save_f / sav_n)
    only_rep2agent_over(Week.random_post_l, Week.random_mrph, save_f / sav_n)


def vocab_main(Week1, Week2):
    # 結果保存用ファイル名
    result_fn = Path("/Users/ida/Amazon Drive/201810結果/Vocabs")

    # vocab_usr(Week1, result_fn / "vocab_only_rep2f", "Agroup")
    # vocab_usr(Week2, result_fn / "vocab_only_rep2f", "Bgroup")



    vocab_usr(Week1, result_fn / "similarity", "Agroup")
    vocab_usr(Week2, result_fn / "similarity", "Bgroup")
