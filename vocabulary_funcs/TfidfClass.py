import sys
from pathlib import Path

from gensim import corpora, models

import numpy as np
import math
from collections import Counter

sys.path.append('/Users/ida/github/AskingKalliopeia/src/')
import tfidf
import mynlp

stopw_path = Path("/Users/ida/github/AskingKalliopeia/stopword.txt")


# 投稿のクラス
class TfidfClass():
    def __init__(self, f_mrph):
        self.f_mrph = f_mrph
        self.stop_word_list = tfidf.create_stop_word_list(stopw_path)
        self.dictionary = corpora.Dictionary([])
        self.pos_l = ["名詞", "動詞", "形容詞"]
        #self.pos_l = ["名詞"]
        self.courpus_tfidf = None
        self.texts = []
        self.tfidf_model = None
        self.corpus = ""
        self.pi_list = []
        self.word_idfs = {}

    def add_post_words(self, pi):
        p_phs = mynlp.read_mrph_per_post(self.f_mrph, pi)
        # 調べるポストの単語を抽出
        add_words_to_dictionary = []
        for phs in p_phs:
            # 文ごとに単語を抽出（ストップワードは除く）
            wlist = tfidf.filter_word(phs, self.pos_l, self.stop_word_list)
            add_words_to_dictionary.extend(wlist)

        # print(add_words_to_dictionary)
        # if not self.dictionary:
        # self.dictionary = corpora.Dictionary([add_words_to_dictionary])
        # else:
        self.dictionary.add_documents([add_words_to_dictionary])
        self.texts.append(add_words_to_dictionary)
        self.pi_list.append(pi)
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]
        self.tfidf_model = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf_model[self.corpus]
        self.word_idfs = self.ref_idf()

    def ref_tfidf_from_pi(self, pi):
        pidx = self.pi_list.index(pi)

        if not self.tfidf_model:
            return None

        # text_tfidf = [[self.dictionary[word[0]], word[1]] for word in self.corpus_tfidf[-1]]
        text_tfidf = [self.dictionary[word[0]] for word in self.corpus_tfidf[-1]]

        return text_tfidf

    # word_str -> 出現する文書数　を書く
    def ref_idf(self):
        idfs = self.dictionary.dfs

        word_idfs = {}
        for wi, df in idfs.items():
            word_idfs[self.dictionary[wi]] = df

        return word_idfs

    def ref_idf_per_pi(self, pi):
        corpus_size = self.dictionary.num_docs
        post_corpus = self.corpus[self.pi_list.index(pi)]
        post_words = [self.dictionary[word[0]] for word in post_corpus]

        post_idfs = {}
        for word in post_words:
            post_idfs[word] = math.log(float(corpus_size) / self.word_idfs[word]) + 1.0

        if len(post_idfs) == 0:
            return None

        return post_idfs
