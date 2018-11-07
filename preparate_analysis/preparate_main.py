import sys
import simplejson as json
import datetime as dt
import preparate_analysis as pre_analysis

sys.path.append('/Users/ida/github/AskingKalliopeia/src/')
import preparation


def _time_seikei(s):
    t = s.split("+")
    s = t[0]
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%f")


def _preparate_per_thread(original_th, Post_list):
    pi_list = []
    for o_p in original_th["posts"]:
        sentences = []
        si_list = []

        tt = _time_seikei(o_p["updated_at"])
        for sentence in o_p["sentences"]:
            new_s = preparation.SentenceClass(si=sentence["id"], body=sentence["body"],
                                              related_to=sentence["related_to"],
                                              component_type=sentence["component_type"])
            sentences.append(new_s)
            si_list.append(new_s.id)
            s_t = _time_seikei(sentence["updated_at"])
            if tt < s_t:
                tt = s_t

        usr_name = o_p["user"]["name"]
        new_p = pre_analysis.PostClass(pi=o_p["id"], \
                                      created_at=_time_seikei(o_p["created_at"]), \
                                      updated_at=tt, \
                                      body=o_p["body"], \
                                      reply_to_id=o_p["in_reply_to_id"], \
                                      usr=usr_name, \
                                      sentences=sentences, \
                                      si_list=si_list, \
                                      belong_th_i=original_th["id"]
                                      )
        pi_list.append(new_p.id)
        Post_list[new_p.id] = new_p
        thread = preparation.ThreadClass(original_th["id"], original_th["title"], pi_list, pi_list[-1])

        preparation._has_premise(thread, Post_list)
    return thread


# 投稿リストからリストを生成
def _preparate_users(Post_list):
    User_list = {}
    for pi, post in Post_list.items():
        if post.usr not in User_list.keys():
            User_list[post.usr] = pre_analysis.UserClass(post.usr)
        User_list[post.usr].add_pi_list(pi)

    return User_list

# スレッドをすべて読み取る
def _load_json(fn):
    f_lists = list(fn.glob("*.json"))
    datas = []
    for fn in f_lists:
        f = fn.open("r")
        jsonData = json.load(f)
        datas.append(jsonData)
        f.close()

    return datas


def per_week_load(paths_l):
    for agent_type, paths in paths_l.items():
        threads = _load_json(paths["threads"])
        Thread_list = {}
        Post_list = {}
        for thread in threads:
            Thread_list[thread["id"]] = _preparate_per_thread(thread, Post_list)

        User_list = _preparate_users(Post_list)


def preparate_main(paths_l):
    # week1かweek2か
    week1_C = per_week_load(paths_l[0])
