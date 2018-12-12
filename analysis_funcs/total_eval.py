import csv
import analysis_funcs
from pathlib import Path


def _check_num(post):
    claim_num, else_num, premise_num = 0, 0, 0
    has_premise = []

    for s in post.sentences:
        if s.component_type == "CLAIM":
            claim_num += 1
            print(list(set(s.has_premise)))
            has_premise.append(len(list(set(s.has_premise))))
        elif s.component_type == "PREMISE":
            premise_num += 1
        else:
            else_num += 1
    sentence_num = len(post.sentences)
    if claim_num == 0:
        claim_rate = 0
    else:
        claim_rate = float(claim_num) / float(sentence_num)

    return claim_num, premise_num, else_num, sentence_num, claim_rate, has_premise


def check_num_plist(Post_list):
    claim_num, else_num, premise_num = 0, 0, 0
    has_premises, sentence_nums, claim_rates = [], [], []

    for pi, post in Post_list.items():
        cn, pn, en, sn, cr, hp = _check_num(post)
        claim_num += cn
        premise_num += pn
        else_num += en
        sentence_nums.append(sn)
        if cr != 0:
            claim_rates.append(cr)
        has_premises.extend(hp)

    return claim_num, premise_num, else_num, has_premises, sentence_nums, claim_rates


def nums_info(Post_list, save_f):
    claim_num, else_num, premise_num, has_premises, sentence_nums, claim_rates = check_num_plist(Post_list)

    with save_f.open("a") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerow(["claim num", claim_num])
        writer.writerow(["premise num", premise_num])
        writer.writerow(["else num", else_num])

        ave, var = analysis_funcs.ave_and_var(has_premises)
        writer.writerow(["has premises", ave, var])
        writer.writerow(has_premises)

        ave, var = analysis_funcs.ave_and_var(sentence_nums)
        writer.writerow(["sentence nums", ave, var])
        writer.writerow(sentence_nums)

        ave, var = analysis_funcs.ave_and_var(claim_rates)
        writer.writerow(["claim rates", ave, var])
        writer.writerow(claim_rates)

        writer.writerows([[], []])


def rep_to_facilitator(Post_list,save_f):
    rep_to_aiad = {}
    for pi, post in Post_list.items():
        if not post.reply_to_id:
            continue
        rep_post = Post_list[post.reply_to_id]
        if rep_post.user_id != "facilitator":
            continue
        rep_to_aiad[pi] = post
    claim_num, else_num, premise_num, has_premises, sentence_nums, claim_rates = check_num_plist(rep_to_aiad)

    with save_f.open("a") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerow(["post nums",len(rep_to_aiad)])
        writer.writerow(["claim num", claim_num])
        writer.writerow(["premise num", premise_num])
        writer.writerow(["else num", else_num])

        ave, var = analysis_funcs.ave_and_var(has_premises)
        writer.writerow(["has premises", ave, var])
        writer.writerow(has_premises)

        ave, var = analysis_funcs.ave_and_var(sentence_nums)
        writer.writerow(["sentence nums", ave, var])
        writer.writerow(sentence_nums)

        ave, var = analysis_funcs.ave_and_var(claim_rates)
        writer.writerow(["claim rates", ave, var])
        writer.writerow(claim_rates)

        writer.writerows([[], []])


def total_eval(Week1, Week2):
    #save_f = Path("/Users/ida/Amazon Drive/201810結果/主張の数とか/全体情報.csv")
    save_f = Path("/Users/ida/Amazon Drive/201810結果/主張の数とか/facilitator_nums.csv")

    agent_Type = "claim"
    print("agent type ", agent_Type)
    #nums_info(Week1.claim_post_l, save_f)
    rep_to_facilitator(Week1.claim_post_l, save_f)
    agent_Type = "random"
    print("agent type ", agent_Type)
    #nums_info(Week1.random_post_l, save_f)
    rep_to_facilitator(Week1.random_post_l, save_f)

    agent_Type = "claim"
    print("agent type ", agent_Type)
    # nums_info(Week2.claim_post_l, save_f)
    rep_to_facilitator(Week2.claim_post_l, save_f)
    agent_Type = "random"
    print("agent type ", agent_Type)
    # nums_info(Week2.random_post_l, save_f)
    rep_to_facilitator(Week2.random_post_l, save_f)

