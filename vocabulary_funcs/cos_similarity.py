import math
import numpy as np
import vocabulary_funcs


def _word_counter(corpus, wordsn):
    words_tf = list(np.zeros(wordsn))
    for text in Tfidf.corpus:
        for word in text:
            words_tf[word[0]] += word[1]


def calc_cos(dictA, dictB):
    lengthA = 0.0
    for word in dictA:
        lengthA += word[1] * word[1]
    lengthA = math.sqrt(lengthA)

    lengthB = 0.0
    for word in dictB:
        lengthA += word[1] * word[1]
    lengthB = math.sqrt(lengthB)

    # AとBの内積を計算
    dotProduct = 0.0
    for wordA in dictA:
        for wordB in dictB:
            if wordA[0] == wordB[0]:
                dotProduct += wordA[1] * wordB[1]

    # cos類似度を計算
    cos = dotProduct / (lengthA * lengthB)
    return cos


def cos_similarity_main(Thread_list, f_mrph, save_f):
    tfidf_lists = {}

    for th_i, thread in Thread_list.items():
        if th_i == 1:
            continue
        Tfidf = vocabulary_funcs.TfidfClass(f_mrph=f_mrph)
        for pi in thread.pi_list:
            Tfidf.add_post_words(pi=pi)

        tfidf_lists[th_i] = Tfidf

    thi_l = sorted(Thread_list.keys())
    thi_l.remove()

    for A_thi in thi_l:
        cos_l = []
        for B_thi in thi_l:
            if A_thi == B_thi:
                cos_l.append("-")
            else:
                corpusA = tfidf_lists[A_thi].corpus
                cos_l.append(calc_cos())
