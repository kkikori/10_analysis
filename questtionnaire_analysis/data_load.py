import sys
import csv
from pathlib import Path


def _loads(fn):
    datas = []

    if not fn.exists():
        print("[FILE ERROR]", fn, "is not found.")
        sys.exit()
    with fn.open("r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            datas.append(row)
    return header, datas


def data_load():
    fn = Path("/Users/ida/Dropbox")
    # fn = Path("/Users/test/Dropbox")
    questions = []

    for week in ["201810_1week", "201810_2week"]:
        for nth in ["questionnaire_middle.csv", "questionnaire_last.csv"]:
            header, data = _loads(fn / week / nth)
            questions.append(data)
            if "middle" in nth:
                middle_header = header
            else:
                last_header = header

    return middle_header, last_header, questions
