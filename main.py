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

    def vectorize_query(self, query):
        v = [0 for _ in range(len(self.items))]
        tf = {}
        N = database.documents_len()
        # calculates frequency of term in query
        for word in query:
            word = word.lower()
            try:
                tf[word] += 1
            except KeyError:
                tf[word] = 1

        # calculates td idf for query as pseudo document
        for word in query:
            word = word.lower()
            try:
                index = self.__indexes__[word]
                v[index] = tf[word] * (math.log2((N + 1) / (0.5 + database.DF(index))))
            except KeyError:
                pass
        return v


class DataSet:
    def __init__(self, documents_file):
        if not Configuration['alreadyInit']:
            load_docs(documents_file)
            load_vocabulary2()
            database.calculate_tf()
            database.calculate_df()
        self.W = np.matrix([[0 for _ in range(database.documents_len())] for _ in range(database.vocabulary_len())])
        self.__build_w__()

    def __build_w__(self):
        if Configuration['alreadyInit']:
            print("Load W from W.npy file")
            self.W = np.load('W.npy')
        else:
            print("Building W matrix")
            N = database.documents_len()
            for i in tqdm(range(database.vocabulary_len()), unit=' word'):
                df = database.DF(i)
                for j in range(N):
                    self.W[i, j] = database.TF(i, j) * math.log2((N + 1) / (0.5 + df))
            print("Save W matrix to W.npy file")
            np.save('W', self.W)
        self.svd = factorization(self.W, 300)

    def find_relevance(self, query, k=None):
        '''
        Finds documents ordered by relevance in terms of query, using latent semantic indexing. If k is not None, it retrieves k better ranked documents, it returns all ordered documents otherwise.

        query: vector with size 1 x len(vocabulary)
        '''

        # SVD low rank factorization with k=200
        terms, diag, docs = self.svd

        # Inverse of diagonal eigenvalue matrix (200 x 200 -> 200 x 200)
        diag = [1 / x for x in diag]

        # query needs to be represented in low rank space
        # q_200 (200 x 1) = Inverse of diagonal (200 x 200) * Transpose of term matrix (200 x len(vocabulary)) * original query (len(vocabulary) x 1)
        query_repres = np.dot(np.transpose(terms), query)
        query_repres = multiply_sparse(diag, query_repres)

        # cosine distance is used to find latent relation between query (200 x 1) and each document (1 x 200).
        # transpond document to make it (200 x 1)
        docs = np.transpose(docs)
        recovered = {i+1: distance.cosine(query_repres, elem) for i, elem in enumerate(docs)}

        # retrieval of k most relevant documents to query
        for elem in sorted(recovered, key=recovered.get):
            yield elem
            k -= 1
            if not k:
                return


class MRI:
    def __init__(self, documents_file):
        # Load dataset
        self.dataSet = DataSet(documents_file)
        # Load vocabulary
        self.vocabulary = Vocabulary()

    def __call__(self, query, k=None):
        return self.dataSet.find_relevance(self.vocabulary.vectorize_query(query), k)


mri = MRI(documents_file='CRAN/CRAN.ALL.json')
