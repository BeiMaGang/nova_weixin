# -*- coding: utf-8 -*-
"""
Created by suun on 5/28/2018
"""
import math
from jieba import cut_for_search


class BM25(object):
    def __init__(self):
        self.D = self.avgdl = self.text = self.docs = self.f = self.df = self.idf = None
        self.k1 = 1.25
        self.b = 0.75

    @staticmethod
    def get_segment(sentence):
        return list(cut_for_search(sentence=sentence))

    def build_from_segmented_lines(self, texts):
        self.D = len(texts)
        self.avgdl = 0.0
        self.text = texts
        self.docs = []
        self.f = []
        self.df = {}
        self.idf = {}
        for line in self.text:
            self.docs.append(self.get_segment(line))

        for sentence in self.docs:
            self.avgdl += len(sentence)
        self.avgdl /= self.D

        for sentence in self.docs:
            tf = {}
            for word in sentence:
                tf[word] = tf.get(word, 0) + 1
            self.f.append(tf)
            for word in tf.keys():
                self.df[word] = self.df.get(word, 0) + 1
        for key, value in self.df.items():
            self.idf[key] = math.log(self.D + 1) - math.log(value + 1)

    def build_from_file(self, filename):
        raws = open(filename, 'r').readlines()
        self.build_from_segmented_lines(raws)

    def sim(self, sentence, index):
        score = 0.0
        for word in sentence:
            if word not in self.f[index]:
                continue
            d = len(self.docs[index])
            wf = self.f[index][word]
            score += (self.idf[word] * wf * (self.k1 + 1) / (
                    wf + self.k1 * (1 - self.b + self.b * d / self.avgdl)))
        return score

    def sim_all(self, sentence):
        # sentence = [str(item).split('/')[0] for item in HanLP.segment(sentence)]
        sentence = self.get_segment(sentence)
        scores = {}
        for index in range(self.D):
            scores[self.text[index]] = self.sim(sentence, index)
        ret = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return ret[:3]
