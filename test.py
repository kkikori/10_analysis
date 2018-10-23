import sys
from collections import Counter
from scipy import stats
import numpy as np
import my_ks


def _Kru(data1, data2):
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    print("data1", data1)
    print("data2", data2)
    n1 = data1.shape[0]
    n2 = data2.shape[0]
    print(n1)
    print(n2)

    data_all = np.concatenate([data1, data2])
    print(data_all)
    cdf1 = np.searchsorted(data1, data_all, side="right")
    print("cdf1", cdf1)

    cdf1 = np.searchsorted(data1, data_all, side="right") / (1.0 * n1)
    print("cdf1", cdf1)
    cdf2 = np.searchsorted(data2, data_all, side="right") / (1.0 * n2)
    d = np.max(np.absolute(cdf1 - cdf2))
    en = np.sqrt(n1 * n2 / float(n1 + n2))
    prob = stats.distributions.kstwobign.sf((en + 0.12 + 0.11 / en) * d)
    print("prob", prob)


def kss():
    d1 = [2, 3, 1, 2, 4, 4, 6, 5, 2, 3, 4, 2, 2, 5, 2, 3]
    d2 = [2, 2, 1, 2, 2, 3, 2, 2, 3, 5, 2, 3, 3, 3, 2, 5]
    d1_d = [1, 6, 3, 3, 2, 1, 0]
    d2_d = [1, 8, 5, 0, 2, 0, 0]
    print(stats.ks_2samp(d1, d2))
    print(stats.ks_2samp(d1_d, d2_d))
    print(my_ks.myks_test(d1, d2))
    # _Kru(d1, d2)


def main():
    print(list(range(-3, 0)))
    k = [1, 2, 2, 3, 4]
    cc = Counter(k)
    print(cc)
    print("cc[10]", cc[10])
    cc.update([1, 5])
    print(cc)
    kss()


if __name__ == "__main__":
    main()
