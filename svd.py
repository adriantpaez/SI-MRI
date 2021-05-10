from numpy.linalg import svd


def factorization(adj, reduced_dimension=None):
    if reduced_dimension:
        terms=np.array([elem[:reduced_dimension] for elem in terms])
        diag=diag[:reduced_dimension]
        docs=docs[:reduced_dimension][:]
        
    return terms, diag, docs
