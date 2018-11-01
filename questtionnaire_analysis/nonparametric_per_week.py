import numpy as np
from scipy import stats
import my_ks
import copy
import csv
from pathlib import Path

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
# week_t = "week1" or "week2"
def _extract_eval(week, target, week_t):
    we = np.array(week["middle"])
    middle_l = we[:, LIKERT_EVAL_IDX_MIDDLE[target][0]:LIKERT_EVAL_IDX_MIDDLE[target][-1] + 1].tolist()
    we = np.array(week["last"])
    last_l = we[:, LIKERT_EVAL_IDX_LAST[target][0]:LIKERT_EVAL_IDX_LAST[target][-1] + 1].tolist()

    # 数値に変換
    middle_list = []
    for person in middle_l:
        middle_list.append([int(e) for e in person])
    last_list = []
    for person in last_l:
        last_list.append([int(e) for e in person])

    if "1" in week_t:
        return np.array(middle_list).T.tolist(), np.array(last_list).T.tolist()
    return np.array(last_list).T.tolist(), np.array(middle_list).T.tolist()


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


def _per_week_test_save(week, target, q_str_l, week_t):
    claim_evals, random_evals = _extract_eval(week, target, week_t)

    write_lists = []
    for i in range(len(claim_evals)):
        write_lists.append([q_str_l[i]])

        # 詳細記入
        claims = copy.deepcopy(claim_evals[i])
        claims.insert(0, "claim")
        write_lists.append(claims)
        randoms = copy.deepcopy(random_evals[i])
        randoms.insert(0, "random")
        write_lists.append(randoms)
        write_lists.append(["", "average", "median", "var"])
        claim_np = np.array(claim_evals[i])
        claims = ["claim", np.average(claim_np), np.median(claim_np), np.var(claim_np)]
        write_lists.append(claims)
        claim_np = np.array(random_evals[i])
        claims = ["random", np.average(claim_np), np.median(claim_np), np.var(claim_np)]
        write_lists.append(claims)

        r = stats.wilcoxon(claim_evals[i], random_evals[i])
        write_lists.append(["wilcoxon test", r.statistic, r.pvalue])
        print(r.statistic, r)
        r = stats.ks_2samp(claim_evals[i], random_evals[i])
        write_lists.append(["ks test", r.statistic, r.pvalue])
        r = my_ks.myks_test(claim_evals[i], random_evals[i])
        write_lists.append(["my-ks test", r.statistic, r.pvalue])
        write_lists.append([])

    f_p = Path("/Users/ida/Amazon Drive/201810実験結果")
    fn = week_t + "_" + target + ".csv"
    fn_p = f_p / fn
    with fn_p.open("w") as f :
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerows(write_lists)
    f.close()


def significant_difference_per_week(week1, week2, middle_header, last_header):
    target = "agent"

    # 問題文の抽出
    qi_l = LIKERT_EVAL_IDX_MIDDLE[target]
    q_str_l = [middle_header[si] for si in qi_l]

    print("\n\n\nweek1", "-" * 100)
    #_per_week_test(week1, target, q_str_l, "week1")
    _per_week_test_save(week1, target, q_str_l, "week1")

    print("\n\n\nweek2", "-" * 100)
    #_per_week_test(week2, target, q_str_l, "week2")
    _per_week_test_save(week2, target, q_str_l, "week2")
