import viewer_discussion


def _post_post(token, post, titles):
    if not post.reply_to_id:
        print("    new thread is created")

        data = {
            "title": titles[0],
            "body": post.body
        }
        print("        data", data)
        viewer_discussion.create_thread(token, data)
        titles.pop(0)
    else:
        print("    new post")
        data = {
            "body": post.body,
            "in_reply_to_id": post.reply_to_id
        }
        viewer_discussion.create_post(token, data)


    return titles


# dummy_discussion_mainから呼び出される
def create_post_main(user_list, post_list, titles):
    print("create_post_main")
    for pi, post in post_list.items():
        print("pi", pi, post.user_id)
        token = user_list[post.user_id]
        titles = _post_post(token, post, titles)

    return
