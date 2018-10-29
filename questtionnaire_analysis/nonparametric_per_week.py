import numpy as np
from scipy import stats
import my_ks

LIKERT_EVAL_IDX_MIDDLE = {
    "total": [4, 5, 6, 7, 8],
    "agent": [12, 13, 14, 15, 16, 17],
    "system": [19, 20],
    "estimator": [21, 22, 23, 24, 25, 26, 27, 28, 29]
}

LIKERT_EVAL_IDX_LAST = {
    "total": [2, 3, 4, 5, 6],
    "agent": [10, 11, 12, 13, 14, 15],
    "estimator": [22, 23, 24, 25, 26, 27, 28, 29, 30],
    "system": [17, 18, 19]
}

EVAL_FREE_IDX = {
    "middle": {
        "total": [10, 11],
        "agent": [18],
        "estimator": [30],
        "system": [31]
    },
    "last": {
        "total": [8, 9],
        "agent": [16],
        "system": [20, 21],
        "estimator": [31],
    }
}


# データの取り出し
# target = "total" or "agent"
def _extract_eval(week, target):
    we = np.array(week["middle"])
    claim_l = we[:, LIKERT_EVAL_IDX_MIDDLE[target][0]:LIKERT_EVAL_IDX_MIDDLE[target][-1] + 1].tolist()
    we = np.array(week["last"])
    random_l = we[:, LIKERT_EVAL_IDX_LAST[target][0]:LIKERT_EVAL_IDX_LAST[target][-1] + 1].tolist()

    # 数値に変換
    claim_list = []
    for person in claim_l:
        claim_list.append([int(e) for e in person])
    random_list = []
    for person in random_l:
        random_list.append([int(e) for e in person])

    return np.array(claim_list).T.tolist(), np.array(random_list).T.tolist()


# 平均などの詳細
def _print_detail(claim_evals, random_evals):
    claims = np.array(claim_evals)
    randams = np.array(random_evals)
    print("claim  :", "average", np.average(claims), "median", np.median(claims), np.var(claims))
    print("         ", claim_evals)
    print("random :", "average", np.average(randams), "median", np.median(randams), np.var(randams))
    print("         ", random_evals)


def _per_week_test(week, target, q_str_l):
    claim_evals, random_evals = _extract_eval(week, target)

    for i in range(len(claim_evals)):
        print("\n", q_str_l[i])
        _print_detail(claim_evals[i], random_evals[i])
        print(stats.wilcoxon(claim_evals[i], random_evals[i]))
        print(stats.ks_2samp(claim_evals[i], random_evals[i]))
        print(my_ks.myks_test(claim_evals[i], random_evals[i]))


def significant_difference_per_week(week1, week2, middle_header, last_header):
    target = "agent"

    # 問題文の抽出
    qi_l = LIKERT_EVAL_IDX_MIDDLE[target]
    q_str_l = [middle_header[si] for si in qi_l]

    print("\n\n\nweek1","-"*100)
    _per_week_test(week1, target, q_str_l)

    print("\n\n\nweek2","-"*100)
    _per_week_test(week2, target, q_str_l)
