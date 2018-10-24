from collections import namedtuple, Counter
from scipy import stats
import numpy as np


# 累積相対度数を調べる
def _cumulative_relative_frequency(values, data, sample_n):
    # https://bellcurve.jp/statistics/glossary/1394.html
    dosuu = Counter(data.tolist())

    total_n = 0
    frequency_lsit = []

    for v in values:
        total_n += dosuu[v]
        frequency_lsit.append(total_n / sample_n)

    return np.array(frequency_lsit)


Ks_2sampResult = namedtuple('myKs_2sampResult', ('statistic', 'pvalue'))


def myks_test(data1, data2):
    # https://bellcurve.jp/statistics/glossary/1360.html
    data1 = np.sort(data1)
    data2 = np.sort(data2)
    n1 = data1.shape[0]
    n2 = data2.shape[0]

    data_all = np.concatenate([data1, data2])
    values = list(range(np.min(data_all), np.max(data_all) + 1))
    data1_frequency = _cumulative_relative_frequency(values, data1, n1)
    data2_frequency = _cumulative_relative_frequency(values, data2, n2)

    d = np.max(np.absolute(data1_frequency - data2_frequency))
    en = np.sqrt(n1 * n2 / float(n1 + n2))
    prob = stats.distributions.kstwobign.sf(d * en)

    return Ks_2sampResult(d * en, prob)
