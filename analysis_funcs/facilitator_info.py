from collections import defaultdict
import csv


# コメント数の把握＋保存
def _per_facilitator_self(facilitator, Post_list, User_list, agent_Type, save_f):
    csv_rows = []
    # print(facilitator.pi_list)
    csv_rows.append([agent_Type])
    csv_rows.append(["agent comments : ", len(facilitator.pi_list)])
    csv_rows.append(["usr name", "comments", "replies from agent"])

    reply_to_usr = defaultdict(int)
    for pi in facilitator.pi_list:
        post = Post_list[pi]
        rep_post = Post_list[post.reply_to_id]
        reply_to_usr[rep_post.user_id] += 1

    for ui, num in reply_to_usr.items():
        usr = User_list[ui]
        csv_rows.append([ui, len(usr.pi_list), num])
        # print(ui, len(usr.pi_list), num)

    with save_f.open("a") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerows(csv_rows)
        writer.writerow([])
    f.close()

    return


def facilitator_self(Week, save_f):
    agent_Type = "claim"
    print("agent type ", agent_Type)
    _per_facilitator_self(Week.claim_usr_l["facilitator"], Week.claim_post_l, Week.claim_usr_l, agent_Type, save_f)

    agent_Type = "random"
    print("agent type ", agent_Type)
    _per_facilitator_self(Week.random_usr_l["facilitator"], Week.random_post_l, Week.random_usr_l, agent_Type, save_f)
