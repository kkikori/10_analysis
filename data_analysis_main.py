import sys
import data_analysis
from pathlib import Path
import simplejson as json


def _preparate_path():
    fn = Path("file_paths.json")
    f = fn.open("r")
    jsonData = json.load(f)

    week_paths = []
    for week in jsonData:
        data_root = week.pop("root")
        root_path = Path(data_root)
        for rorc, v in week.items():
            paths = {}
            for fn, fp in v.items():
                paths[fn] = root_path / fp
        week_paths[rorc] = paths


def main():
    paths_l = _preparate_path()
    data_analysis.data_load(paths_l)


if __name__ == "__main__":
    main()
