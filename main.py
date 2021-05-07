import math
import os
from tqdm import tqdm
import numpy as np
from svd import factorization
from utils import multiply_sparse
from scipy.spatial import distance
import string

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
    
    def vectorize_query(self, query, weights=None):
        v=[0 for _ in range(len(self.items))]
        for word in query:
            if weights:
                v[self[word]]=weights[word]
            else:
                v[self[word]]=1
        return v


class DataSet:
    def __init__(self, documents_folder, vocabulary: Vocabulary):
        self.documents = [f'{documents_folder}/{f}' for f in os.listdir(documents_folder)]
        self.vocabulary = vocabulary
        self.W = [[0 for _ in range(len(self.documents))] for _ in range(len(self.vocabulary))]
        self.__tf__ = [[0 for _ in range(len(self.documents))] for _ in range(len(self.vocabulary))]
        self.__df__ = [0 for _ in range(len(self.vocabulary))]
        self.__calculate_tf_idf__()

    def __calculate_tf_idf__(self):
        for j, d in tqdm(enumerate(self.documents)):
            try:
                with open(d) as f:
                    doc =f.read()
                    doc=doc.translate(str.maketrans('', '', string.punctuation+'\n'))
                    doc=doc.split(' ')
                    for w in doc:
                        w=w.lower()
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
                self.W[i][j] = self.__tf__[i][j] * math.log2(N / (1+self.__df__[i]))
        self.svd=factorization(self.W)
        
    def find_relevance(self,query):
        #query q has m dimensions (vocabulary size)
        terms, diag, docs=self.svd
        
        query_repres=np.matmul(query, terms)
        query_repres=multiply_sparse(query_repres, diag)

        docs=np.transpose(docs)

        return {i: distance.cosine(query_repres, elem) for i,elem in enumerate(docs)}
        
        
class MRI:
    def __init__(self, vocabulary_file, documents_folder):
        # Load vocabulary
        self.vocabulary = Vocabulary(vocabulary_file)
        # Load dataset
        self.dataSet = DataSet(documents_folder, self.vocabulary)
        
    def __call__(self, query):
        return self.dataSet.find_relevance(self.vocabulary.vectorize_query(query))
        


mri=MRI(vocabulary_file='vocabulary1.txt', documents_folder='data1')
recovered=mri(['dentista'])
for k in sorted(recovered, key=recovered.get):
    print(k)
