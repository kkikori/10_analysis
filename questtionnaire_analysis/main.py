import sys
import data_load
import quote
import nonparametric_test
import nonparametric_per_week


def aggregated＿quote(week1, week2, header):
    # 投票の集計
    print("week1 : ")
    quote.quote(datas=week1, header=header)
    print("week2 : ")
    quote.quote(datas=week2, header=header)


def main():
    middle_header, last_header, datas = data_load.data_load()
    week1 = {"middle": datas[0], "last": datas[1]}
    week2 = {"middle": datas[2], "last": datas[3]}

    # aggregated＿quote(week1, week2, header)
    #nonparametric_test.significant_difference(week1, week2, middle_header, last_header)
    nonparametric_per_week.significant_difference_per_week(week1, week2, middle_header, last_header)

if __name__ == "__main__":
    main()
