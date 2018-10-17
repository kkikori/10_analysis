import numpy as np

LIKERT_EVAL_IDX = {
    "middle": {
        "total": [4, 5, 6, 7, 8, 9],
        "agent": [12, 13, 14, 15, 16, 17],
        "system": [19, 20],
        "estimator": [21, 22, 23, 24, 25, 26, 27, 28, 29]
    },
    "last": {
        "total": [2, 3, 4, 5, 6, 7],
        "agent": [10, 11, 12, 13, 14, 15],
        "estimator": [22, 23, 24, 25, 26, 27, 28, 29, 30],
        "system": [17, 18, 19]
    }
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


def _extract_total_eval(week1, week2):
    week1_evals =


def eval_total(week1, week2):
    claim_evals, random_evals = _extract_total_eval(week1, week2)


def significant_difference(week1, week2, middle_header, last_header):
    print("middle")
    [print(hi, hea) for hi, hea in enumerate(middle_header)]
    print("\n\n\nlast")
    [print(hi, hea) for hi, hea in enumerate(last_header)]

    claim_agent = {"week1": week1["middle"]}
    #claim_agent.extend(week2["last"])

    #random_agent = week1["last"]
    #random_agent.extend(week2["middle"])
