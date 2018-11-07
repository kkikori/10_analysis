import sys
import preparate_analysis
from pathlib import Path
import simplejson as json


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


def main():
    paths_l = _preparate_path()
    [print(path) for path in paths_l]
    preparate_analysis.data_load(paths_l)


if __name__ == "__main__":
    main()
