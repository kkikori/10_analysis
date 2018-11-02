from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import math


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


def calc_wilcoxon(week1, week2, target, nth):
    week1.update(week2)
    d_l = [usr_c.dif_cr(target, nth) for usr_c in week1.values()]

    d_abs_l = {}
    for delta in d_l:
        d_abs = math.fabs(delta)
        if d_abs == 0:
            continue
        elif d_abs not in d_abs_l.keys():
            d_abs_l[d_abs] = 0
        d_abs_l[d_abs] += 1



# 各ユーザの評価値の変化
def graphing(week1, week2, target, nth):
    week1.update(week2)

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
        graphing(week1, week2, target, nth)
