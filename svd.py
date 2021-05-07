from numpy.linalg import svd


def factorization(adj):
    return svd(adj, full_matrices=False)
