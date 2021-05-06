import math
import os

DATA_FOLDER = "./data"

VOCABULARY = []


class Vocabulary:
    def __init__(self, vocabulary_file):
        self.items: set = None
        self.__indexes__ = {}
        print(f'Loading vocabulary from {vocabulary_file}:', end=' ')
        with open(vocabulary_file) as f:
            self.items = set([w.strip().lower() for w in f.read().split('\n')])
        for i, w in enumerate(self.items):
            self.__indexes__[w] = i

        print(f'{len(self.items)} terms to vocabulary')

    def __getitem__(self, word):
        return self.__indexes__[word]

    def __len__(self):
        return len(self.items)


class DataSet:
    def __init__(self, documents_folder, vocabulary: Vocabulary):
        self.documents = [f'{documents_folder}/{f}' for f in os.listdir(documents_folder)]
        self.vocabulary = vocabulary
        self.W = [[0 for _ in range(len(self.documents))] for _ in range(len(self.vocabulary))]
        self.__tf__ = [[0 for _ in range(len(self.documents))] for _ in range(len(self.vocabulary))]
        self.__df__ = [0 for _ in range(len(self.vocabulary))]
        self.__calculate_tf_idf__()

    def __calculate_tf_idf__(self):
        for j, d in enumerate(self.documents):
            try:
                with open(d) as f:
                    for w in f.read().split(' '):
                        if w in self.vocabulary.items:
                            i = self.vocabulary[w]
                            self.__tf__[i][j] += 1
                    for w in self.vocabulary.items:
                        i = self.vocabulary[w]
                        if self.__tf__[i][j] != 0:
                            self.__df__[i] += 1
            except UnicodeDecodeError:
                continue

        N = len(self.documents)
        for i in range(len(self.vocabulary)):
            for j in range(len(self.documents)):
                self.W[i][j] = self.__tf__[i][j] * math.log2(N / self.__df__[i])


class MRI:
    def __init__(self, vocabulary_file, documents_folder):
        # Load vocabulary
        self.vocabulary = Vocabulary(vocabulary_file)
        self.dataSet = DataSet(documents_folder, self.vocabulary)


MRI(vocabulary_file='vocabulary.txt', documents_folder='data')
