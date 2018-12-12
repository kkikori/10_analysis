from collections import Counter

import numpy as np
from scipy import stats

from questtionnaire_analysis import my_ks
import pandas as pd
import matplotlib.pyplot as plt
from gensim import corpora, models


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


def graf_errorbar():
    data = pd.DataFrame([np.random.normal(10, 7, 100), np.random.normal(20, 5, 100) \
                            , np.random.normal(10, 2, 100), np.random.normal(40, 10, 100)])  # 100×4の行列

    x = np.arange(0, 4)
    y = data.T.mean()  # 4つの要素についての計算に直したいのでdata.Tで転置。その後meanで各列の平均をとっている
    e = np.sqrt(data.T.var())  # エラーバーとして標準偏差を採用

    # エラーバー付き折れ線
    plt.errorbar(x, y, e, label='The Graph')

    data = pd.DataFrame([np.random.normal(10, 7, 100), np.random.normal(20, 5, 100) \
                            , np.random.normal(10, 2, 100), np.random.normal(40, 10, 100)])  # 100×4の行列

    x = np.arange(0, 4)
    y = data.T.mean()  # 4つの要素についての計算に直したいのでdata.Tで転置。その後meanで各列の平均をとっている
    e = np.sqrt(data.T.var())  # エラーバーとして標準偏差を採用
    plt.errorbar(x, y, e, label='The Graph2')

    plt.legend(loc="upper left")  # グラフラベルを左上に表示するオプション
    plt.xlim(-1, 4)
    plt.ylim(0, 55)
    plt.show()


def idf_test():
    docs = [["a", "b", "c", "b"], ["a", "a", "a", "b"], ["c", "d", "e"]]
    dct = corpora.Dictionary(docs)
    print(len(dct))
    corpus = [dct.doc2bow(line) for line in docs]
    print(corpus)
    model = models.TfidfModel(corpus)  # fit model
    vector = model[corpus[2]]
    print(vector)
    print(dct.id2token)
    print(dct.dfs)
    for wi, df in dct.dfs.items():
        print(dct[wi], df)
        # idfidf = models.tfidfmodel.precompute_idfs(wglobal=sma,dfs=dct,total_docs=len(docs))
        # print(idfidf)


if __name__ == "__main__":
    idf_test()
    # graf_errorbar()
    # main()
