import vocabulary_funcs
import numpy as np
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt


def ref_vocab_tf(Post_list, mrph_path):
    Tfidf = vocabulary_funcs.TfidfClass(f_mrph=mrph_path)
    for pi, post in Post_list.items():
        Tfidf.add_post_words(pi)

    words_tf = list(np.zeros(len(Tfidf.dictionary)))
    for text in Tfidf.corpus:
        for word in text:
            words_tf[word[0]] += word[1]

    tf_counter = Counter(words_tf)

    return tf_counter


def _extract_nums(coun, MAX_T):
    xticks = list(range(1, MAX_T + 2))
    yticks = list(np.zeros(len(xticks)))

    for x in range(len(xticks)):
        yticks[x] = coun[x]

    for kaisuu, kosuu in coun.items():
        if kaisuu > MAX_T:
            yticks[-1] += kosuu
        else:
            # print(kaisuu)
            yticks[int(kaisuu)] = kosuu

    return xticks, yticks


def graphing(datas, labels, title, save_f):
    MAX_T = 15
    fig = plt.figure(figsize=(16,9))

    for data, label in zip(datas, labels):
        x, y = _extract_nums(data, MAX_T)
        print("x", x)
        print("y", y)
        plt.plot(x, y, marker="o", label=label, linewidth=3, markeredgewidth=0)
    plt.legend(loc="best")
    plt.title(title)
    plt.xticks()
    plt.savefig(str(save_f))
    # plt.show()


def vocab_total(Week1, Week2):
    Agroup_1 = ref_vocab_tf(Week1.claim_post_l, Week1.claim_mrph)
    print("A-group 1 preparated")
    Agroup_2 = ref_vocab_tf(Week1.random_post_l, Week1.random_mrph)
    print("A-group 2 preparated")

    Bgroup_1 = ref_vocab_tf(Week2.random_post_l, Week2.random_mrph)
    print("B-group 1 preparated")
    Bgroup_2 = ref_vocab_tf(Week2.claim_post_l, Week2.claim_mrph)
    print("B-group 2 preparated")

    # 結果保存用ファイル名
    result_fn = Path("/Users/ida/Amazon Drive/201810結果/Vocabs/total_eval")

    graphing(datas=[Agroup_1, Bgroup_1], labels=["Agroup", "Bgroup"], title="Thema 1",
             save_f=result_fn / "テーマ1.png")
    graphing(datas=[Agroup_2, Bgroup_2], labels=["Agroup", "Bgroup"], title="Thema 2",
             save_f=result_fn / "テーマ2.png")
