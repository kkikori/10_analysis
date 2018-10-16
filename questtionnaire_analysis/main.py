import sys
import data_load
import quote
import mykruskal


def aggregated＿quote(week1, week2, header):
    # 投票の集計
    print("week1 : ")
    quote.quote(datas=week1, header=header)
    print("week2 : ")
    quote.quote(datas=week2, header=header)


def main():
    header, datas = data_load.data_load()
    week1 = {"middle": datas[0], "last": datas[1]}
    week2 = {"middle": datas[2], "last": datas[3]}

    # aggregated＿quote(week1, week2, header)
    mykruskal.significant_difference(week1, week2, header)


if __name__ == "__main__":
    main()
