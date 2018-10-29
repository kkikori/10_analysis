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
def _extract_eval(week1, week2, target):
    we1 = np.array(week1["middle"])
    week1_claim = we1[:, LIKERT_EVAL_IDX_MIDDLE[target][0]:LIKERT_EVAL_IDX_MIDDLE[target][-1] + 1].tolist()
    we1 = np.array(week1["last"])
    week1_random = we1[:, LIKERT_EVAL_IDX_LAST[target][0]:LIKERT_EVAL_IDX_LAST[target][-1] + 1].tolist()

    we2 = np.array(week2["middle"])
    week2_random = we2[:, LIKERT_EVAL_IDX_MIDDLE[target][0]:LIKERT_EVAL_IDX_MIDDLE[target][-1] + 1].tolist()
    we2 = np.array(week2["last"])
    week2_claim = we2[:, LIKERT_EVAL_IDX_LAST[target][0]:LIKERT_EVAL_IDX_LAST[target][-1] + 1].tolist()

    # 数値に変換
    week1_claim.extend(week2_claim)
    claim_list = []
    for person in week1_claim:
        claim_list.append([int(e) for e in person])
    week1_random.extend(week2_random)
    random_list = []
    for person in week1_random:
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


def eval_total(week1, week2, middle_header):
    target = "total"

    claim_evals, random_evals = _extract_eval(week1, week2, target)

    for i in range(len(claim_evals)):
        qi = LIKERT_EVAL_IDX_MIDDLE[target][i]

        print("\n", middle_header[qi])
        _print_detail(claim_evals[i], random_evals[i])
        r = stats.wilcoxon(claim_evals[i], random_evals[i])

        print(r)
        print(stats.ks_2samp(claim_evals[i], random_evals[i]))
        print(my_ks.myks_test(claim_evals[i], random_evals[i]))


def eval_csv_save(week1, week2, middle_header):
    target = "agent"

    claim_evals, random_evals = _extract_eval(week1, week2, target)

    write_lists = []
    for i in range(len(claim_evals)):
        qi = LIKERT_EVAL_IDX_MIDDLE[target][i]
        write_lists.append([middle_header[qi]])

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
        claims = ["claim", np.average(claim_np), np.median(claim_np), np.var(claim_np)]
        write_lists.append(claims)

        r = stats.wilcoxon(claim_evals[i], random_evals[i])
        write_lists.append(["wilcoxon test", r.statistic, r.pvalue])
        print(r.statistic, r)
        r = stats.ks_2samp(claim_evals[i], random_evals[i])
        write_lists.append(["ks test", r.statistic, r.pvalue])
        r = my_ks.myks_test(claim_evals[i], random_evals[i])
        write_lists.append(["my-ks test", r.statistic, r.pvalue])
        write_lists.append([])

    f_n = Path("/Users/ida/Amazon Drive/201810実験結果/eval_agent.csv")

    with f_n.open("w") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerows(write_lists)
    f.close()
    print(type(write_lists))
    #[print(f) for f in write_lists]

def significant_difference(week1, week2, middle_header, last_header):
    print("middle")
    [print(hi, hea) for hi, hea in enumerate(middle_header)]
    print("\n\n\nlast")
    [print(hi, hea) for hi, hea in enumerate(last_header)]

    claim_agent = {"week1": week1["middle"]}
    # claim_agent.extend(week2["last"])

    # random_agent = week1["last"]
    # random_agent.extend(week2["middle"])

    #eval_total(week1, week2, middle_header)
    eval_csv_save(week1, week2, middle_header)
