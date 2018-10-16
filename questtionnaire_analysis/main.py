import sys
import data_load
import quote


def main():
    header, datas = data_load.data_load()
    week1 = {"middle": datas[0], "last": datas[1]}
    week2 = {"middle": datas[2], "last": datas[3]}

    quote(datas=week1, header=header)


if __name__ == "__main__":
    main()
