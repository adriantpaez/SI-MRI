from numpy.linalg import svd
import numpy as np


def factorization(adj, reduced_dimension=None):
    terms, diag, docs=svd(adj, full_matrices=False)
    if reduced_dimension:
        terms=np.array([elem[:reduced_dimension] for elem in terms])
        diag=diag[:reduced_dimension]
        docs=docs[:reduced_dimension][:]
        
    return terms, diag, docs
