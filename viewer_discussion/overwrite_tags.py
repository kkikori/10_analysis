import viewer_discussion


# うまくいかず
def overwrites(post_list, token):
    for pi, post in post_list.items():
        for s in post.sentences:
            d = {"component_type": s.component_type, "related_to_id": s.related_to}
            viewer_discussion.updated_sentence(s.id, token, d)
