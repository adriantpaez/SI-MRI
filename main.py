import math
import numpy as np
import database
from svd import factorization
from utils import multiply_sparse
from scipy.spatial import distance
from database import load_docs, load_vocabulary2
from config import Configuration
from tqdm import tqdm


class Vocabulary:
    def __init__(self):
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
            if word in self.itemsSet:
                if weights:
                    v[self[word]] = weights[word]
                else:
                    v[self[word]] = 1
        return v


class DataSet:
    def __init__(self, documents_file):
        if not Configuration['alreadyInit']:
            load_docs(documents_file)
            load_vocabulary2()
            database.calculate_tf()
            database.calculate_df()
        self.W = [[0 for _ in range(database.documents_len())] for _ in range(database.vocabulary_len())]
        self.__build_w__()

    def __build_w__(self):
        print("Building W matrix")
        N = database.documents_len()
        for i in tqdm(range(database.vocabulary_len()), unit=' word'):
            df = database.DF(i)
            for j in range(N):
                self.W[i][j] = database.TF(i, j) * math.log2(N / (1 + df))
        print("Building SVD...", end='')
        self.svd = factorization(self.W)
        print('OK')

    def find_relevance(self, query):
        # Query q has m dimensions (vocabulary size)
        terms, diag, docs = self.svd

        query_repres = np.matmul(query, terms)
        query_repres = multiply_sparse(query_repres, diag)

        docs = np.transpose(docs)

        return {i: distance.cosine(query_repres, elem) for i, elem in enumerate(docs)}


class MRI:
    def __init__(self, vocabulary_file, documents_file):
        # Load dataset
        self.dataSet = DataSet(documents_file)
        # Load vocabulary
        self.vocabulary = Vocabulary()

    def __call__(self, query):
        return self.dataSet.find_relevance(self.vocabulary.vectorize_query(query))


mri = MRI(vocabulary_file='vocabulary.txt', documents_file='CISI.ALL.json')
recovered = mri(['comaromi', 'study', 'history'])
for k in sorted(recovered, key=recovered.get):
    print(k)
