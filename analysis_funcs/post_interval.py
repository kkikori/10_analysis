except_usr_id = ["facilitator", "kitkat"]


# 　ファシリテータ間の投稿間隔時間を抽出し，リストで返す．
def _facilitator_has_reply(Post_list):
    interval_times = []
    for pi, post in Post_list.items():
        if not post.reply_to_id or post.user_id in except_usr_id:
            continue
        rep_post = Post_list[post.reply_to_id]
        if rep_post.user_id != "facilitator":
            continue
        print("")

        rep_rep_post = Post_list[rep_post.reply_to_id]
        if rep_rep_post.user_id == post.user_id:
            interval_times.append(post.created_at - rep_rep_post.created_at)

    interval_seconds = []
    for it in interval_times:
        print(it, it.total_seconds())
        interval_seconds.append(it.total_seconds())

    return interval_seconds


def interval_analysis_main(Post_list, User_list):
    print("a")
