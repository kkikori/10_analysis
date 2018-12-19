import viewer_discussion as viewer


# うまくいかず
def overwrites(post_list, token):
    for pi, post in post_list.items():
        for s in post.sentences:
            d = {"component_type": s.component_type, "related_to_id": s.related_to}
            viewer.updated_sentence(s.id, token, d)


def _ref_si(original_post_list, pi, sidx, ref_silist):
    rep_pi = original_post_list[pi].reply_to_id
    ri = original_post_list[pi].sentences[sidx].related_to
    # 関連先がない時
    if not ri:
        return None
    # 投稿内関係の場合
    if ri in original_post_list[pi].si_list:
        ii = original_post_list[pi].si_list.index(ri)
        return ref_silist[pi][ii]
    else:
        original_si = original_post_list[rep_pi].si_list.index(ri)
        return ref_silist[rep_pi][original_si]


def _post_list(thread_post):
    posts2s = {}
    for post in thread_post:
        si_ = []
        for s in post["sentences"]:
            si_.append(s["id"])
        posts2s[post["id"]] = si_
    return posts2s


def overwrites_10(POST_LIST, token):
    threads = viewer.get_threads_data(token)

    for thread in threads:
        ref_silist = _post_list(thread["posts"])
        for post in thread["posts"]:
            if post["user"]["name"] in ["facilitator","kitkat"]:
                continue
            pi = post["id"]
            original_sentences = POST_LIST[pi].sentences
            for sidx, s in enumerate(post["sentences"]):
                print("original_sentences",len(original_sentences))
                print("post",post["body"])
                ctype = original_sentences[sidx].component_type
                ri = _ref_si(POST_LIST, pi, sidx, ref_silist)
                d = {"component_type": ctype, "related_to_id": ri}
                viewer.updated_sentence(s["id"], token, d)
