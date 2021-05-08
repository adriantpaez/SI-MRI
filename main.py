import math
import numpy as np
import database
from svd import factorization
from utils import multiply_sparse
from scipy.spatial import distance
from database import load_docs, load_vocabulary
from config import Configuration


class Vocabulary:
    def __init__(self, vocabulary_file):
        if not Configuration['alreadyInit']:
            load_vocabulary(vocabulary_file)
        self.items = database.vocabulary_vector()
        self.itemsSet = set(self.items)
        self.__indexes__ = {}
        for i, w in enumerate(self.items):
            self.__indexes__[w] = i

    def __getitem__(self, word):
        return self.__indexes__[word]

    def vectorize_query(self, query, weights=None):
        v = [0 for _ in range(len(self.items))]
        for word in query:
            if weights:
                v[self[word]] = weights[word]
            else:
                v[self[word]] = 1
        return v


class DataSet:
    def __init__(self, documents_file, vocabulary: Vocabulary):
        if not Configuration['alreadyInit']:
            load_docs(documents_file)
        self.vocabulary = vocabulary
        self.W = [[0 for _ in range(database.documents_len())] for _ in range(database.vocabulary_len())]
        self.__calculate_tf_idf__()

    def __calculate_tf_idf__(self):
        database.calculate_tf()
        database.calculate_df()

        N = database.documents_len()
        for i in range(database.vocabulary_len()):
            df = database.DF(i)
            for j in range(N):
                self.W[i][j] = database.TF(i, j) * math.log2(N / (1 + df))
        self.svd = factorization(self.W)

    def find_relevance(self, query):
        # Query q has m dimensions (vocabulary size)
        terms, diag, docs = self.svd

        query_repres = np.matmul(query, terms)
        query_repres = multiply_sparse(query_repres, diag)

        docs = np.transpose(docs)

        return {i: distance.cosine(query_repres, elem) for i, elem in enumerate(docs)}


class MRI:
    def __init__(self, vocabulary_file, documents_file):
        # Load vocabulary
        self.vocabulary = Vocabulary(vocabulary_file)
        # Load dataset
        self.dataSet = DataSet(documents_file, self.vocabulary)

    def __call__(self, query):
        return self.dataSet.find_relevance(self.vocabulary.vectorize_query(query))


mri = MRI(vocabulary_file='vocabulary.txt', documents_file='CISI.ALL.json')
recovered = mri(['cat', 'dog', 'gem'])
for k in sorted(recovered, key=recovered.get):
    print(k)
