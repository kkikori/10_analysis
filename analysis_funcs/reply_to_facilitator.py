import csv


def _post_csv(post):
    r_list = [post.id, post.user_id, post.created_at]
    s_s = ""
    for s in post.sentences:
        s_s += s.body
    r_list.append(s_s)
    return r_list


# リプライを持つファシリテータの投稿の抽出
def has_reply(Post_list, agent_Type, save_f):
    csv_rows = []
    for pi, post in Post_list.items():
        if not post.reply_to_id:
            continue
        rep_post = Post_list[post.reply_to_id]
        if rep_post.user_id != "facilitator":
            continue
        csv_rows.append(["-------" * 10])
        rep_rep_post = Post_list[rep_post.reply_to_id]

        print(_post_csv(rep_rep_post))
        csv_rows.append(_post_csv(rep_rep_post))
        csv_rows.append(_post_csv(rep_post))
        csv_rows.append(_post_csv(post))

    print(csv_rows)
    # 書き込み
    with save_f.open("a") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerow([agent_Type])
        writer.writerows(csv_rows)
        writer.writerows([[], []])


def reply_to_facilitator(Week, save_f):
    agent_Type = "claim"
    print("agent type ", agent_Type)
    has_reply(Week.claim_post_l, agent_Type, save_f)

    agent_Type = "random"
    print("agent type ", agent_Type)
    has_reply(Week.random_post_l, agent_Type, save_f)
