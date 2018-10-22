import numpy as np

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
def _extract_total_eval(week1, week2):
    we1 = np.array(week1["middle"])
    week1_claim = we1[:, LIKERT_EVAL_IDX_MIDDLE["total"][0]:LIKERT_EVAL_IDX_MIDDLE["total"][-1] + 1].tolist()
    we1 = np.array(week1["last"])
    week1_random = we1[:, LIKERT_EVAL_IDX_LAST["total"][0]:LIKERT_EVAL_IDX_LAST["total"][-1] + 1].tolist()

    we2 = np.array(week2["middle"])
    week2_random = we2[:, LIKERT_EVAL_IDX_MIDDLE["total"][0]:LIKERT_EVAL_IDX_MIDDLE["total"][-1] + 1].tolist()
    we2 = np.array(week2["last"])
    week2_claim = we2[:, LIKERT_EVAL_IDX_LAST["total"][0]:LIKERT_EVAL_IDX_LAST["total"][-1] + 1].tolist()

    # 数値に変換
    week1_claim.extend(week2_claim)
    claim_list =[]
    for person in week1_claim:
        claim_list.append([int(e) for e in person])
    week1_random.extend(week2_random)
    random_list=[]
    for person in week1_random:
        random_list.append([int(e) for e in person])

    print(claim_list)

    return claim_list, random_list


def eval_total(week1, week2):
    claim_evals, random_evals = _extract_total_eval(week1, week2)

    print("claim_evals")
    [print(c) for c in claim_evals]


def significant_difference(week1, week2, middle_header, last_header):
    print("middle")
    [print(hi, hea) for hi, hea in enumerate(middle_header)]
    print("\n\n\nlast")
    [print(hi, hea) for hi, hea in enumerate(last_header)]

    claim_agent = {"week1": week1["middle"]}
    # claim_agent.extend(week2["last"])

    # random_agent = week1["last"]
    # random_agent.extend(week2["middle"])

    eval_total(week1, week2)
