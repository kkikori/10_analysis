import sys
from pathlib import Path
import simplejson as json

import preparate_analysis
import viewer_discussion


# ファイルパスの準備
def _preparate_path():
    fn = Path("file_paths.json")
    f = fn.open("r")
    jsonData = json.load(f)

    week_paths = []
    for week in jsonData:
        data_root = week.pop("root")
        root_path = Path(data_root)
        sss = {}
        for rorc, v in week.items():
            paths = {}
            for fn, fp in v.items():
                paths[fn] = root_path / fp
            sss[rorc] = paths
        week_paths.append(sss)

    return week_paths


def _ref_titles(thread_list):
    th_titles = {}
    for th_i, thread in thread_list.items():
        th_titles[th_i] = thread.title

    this = sorted(th_titles.keys())
    titles = [th_titles[thi] for thi in this]
    return titles


def viewer_main(post_list, thread_list):
    usr_token_l = viewer_discussion.create_user_main(True)
    titles = _ref_titles(thread_list)
    print(titles)
    #viewer_discussion.create_post_main(usr_token_l, post_list,titles)
    viewer_discussion.overwrites_10(post_list, usr_token_l["facilitator"])


def main():
    paths_l = _preparate_path()
    Week1, Week2 = preparate_analysis.preparate_main(paths_l)

    viewer_main(Week1.claim_post_l, Week1.claim_th_l)


if __name__ == "__main__":
    main()
