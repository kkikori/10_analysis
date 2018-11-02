from wilcoxon import my_wilcoxon

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


class UsrClass():
    def __init__(self, claim_idx, random_idx):
        self.claim_term = []
        self.random_term = []
        self.claim_idx = claim_idx  # LIKERT_EVAL_IDX_MIDDLE or LIKERT_EVAL_IDX_LAST
        self.random_idx = random_idx

    def extract_value(self, target, nth):
        idx = self.claim_idx[target][nth]
        claim_v = self.claim_term[idx]
        idx = self.random_idx[target][nth]
        random_v = self.random_term[idx]

        return claim_v, random_v

    def dif_cr(self, target, nth):
        claim_v, random_v = self.extract_value(target, nth)
        return int(claim_v) - int(random_v)


# ユーザ単位にデータ型を整理
# target = "total" or "agent"
# period1, period2 = "middle" or "last"
def reshapes(week, t_claim, t_random):
    if t_claim == "middle":
        claim_idxs = LIKERT_EVAL_IDX_MIDDLE
        random_idxs = LIKERT_EVAL_IDX_LAST
    else:
        random_idxs = LIKERT_EVAL_IDX_MIDDLE
        claim_idxs = LIKERT_EVAL_IDX_LAST

    User_list = {}
    for row in week[t_claim]:
        usr = UsrClass(claim_idx=claim_idxs, random_idx=random_idxs)
        usr.claim_term = row
        User_list[row[1]] = usr

    for row in week[t_random]:
        User_list[row[1]].random_term = row

    return User_list




def significant_difference(week1, week2, middle_header, last_header):
    target = "total"
    week1_user_list = reshapes(week1, "middle", "last")
    week2_user_list = reshapes(week2, "last", "middle")

    my_wilcoxon(week1_user_list, week2_user_list, target, middle_header, LIKERT_EVAL_IDX_MIDDLE)
