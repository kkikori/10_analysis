from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import math


# 使わないからいらないかも
# claims,randomsに分けて，問ごとにリストにまとめている
def _extract_target(week1, week2, target, LIKERT_EVAL_IDX_LAST):
    claims = []
    randoms = []
    q_s = len(LIKERT_EVAL_IDX_LAST[target])
    for nth in range(q_s):
        kari_c = []
        kari_q = []
        for user, user_l in week1.items():
            cv, rv = user_l.extract_value(target, nth)
            kari_c.append(int(cv))
            kari_q.append(int(rv))
        claims.append(kari_c)
        randoms.append(kari_q)

    for nth in range(q_s):
        kari_c = []
        kari_q = []
        for user, user_l in week2.items():
            cv, rv = user_l.extract_value(target, nth)
            kari_c.append(int(cv))
            kari_q.append(int(rv))
        claims[nth].extend(kari_c)
        randoms[nth].extend(kari_q)

    return claims, randoms


# 平均順位の計算
def calc_average_of_the_ranks(datas):
    ranks_dic = {}
    for delta in datas:
        d_abs = math.fabs(delta)
        if d_abs not in ranks_dic.keys():
            ranks_dic[d_abs] = 0
        ranks_dic[d_abs] += 1

    d_abss = sorted(ranks_dic.keys())

    total_sum = 0
    average_rank_dic = {}
    for diff in d_abss:
        tie_n = ranks_dic[diff]
        if diff == 0:
            continue
        ave_rank = sum(list(range(total_sum + 1, total_sum + tie_n + 1))) / tie_n
        average_rank_dic[int(diff)] = ave_rank
        total_sum += tie_n

    return average_rank_dic


def calc_wilcoxon(week1, week2, target, nth):
    week1.update(week2)

    # 差分のリスト
    d_l = [usr_c.dif_cr(target, nth) for usr_c in week1.values()]
    print(d_l)
    # 差分値の平均順位
    ave_rank_dic = calc_average_of_the_ranks(d_l)
    print(ave_rank_dic)

    # 検定統計量(statistic)を求める
    d_minus_s = 0.0
    d_plus_s = 0.0
    for d in d_l:
        if d < 0:
            d_minus_s += ave_rank_dic[math.fabs(d)]
        elif d > 0:
            d_plus_s += ave_rank_dic[d]

    statistic = min([d_minus_s, d_plus_s])

    while 0 in d_l:
        d_l.remove(0)
    n_dash = len(d_l)

    print(n_dash, statistic)


# 各ユーザの評価値の変化の描画
def graphing(week1, week2, target, nth):
    week1.update(week2)
    # ユーザごとのの評価値の差分(claim-random)
    d_l = [usr_c.dif_cr(target, nth) for usr_c in week1.values()]
    print(d_l)
    d_counter = Counter(d_l)
    print(d_counter)

    min_d = min(d_counter.keys())
    max_d = max(d_counter.keys())

    labels = []
    values = []
    for v in range(min_d, max_d + 1):
        values.append(d_counter[v])
        labels.append(v)

    left = list(range(min_d, max_d + 1))
    plt.bar(np.array(left), np.array(values), linewidth=0, align="center", tick_label=labels)
    plt.show()


def my_wilcoxon(week1, week2, target, middle_header, LIKERT_EVAL_IDX_MIDDLE):
    for nth, q_s in enumerate(LIKERT_EVAL_IDX_MIDDLE[target]):
        print(middle_header[LIKERT_EVAL_IDX_MIDDLE[target][nth]])
        # graphing(week1, week2, target, nth)
        calc_wilcoxon(week1, week2, target, nth)
