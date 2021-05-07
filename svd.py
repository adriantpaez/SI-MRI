from numpy.linalg import svd


def factorization(adj):
    return svd(adj, full_matrices=False)


print(factorization([[1,2,3,4], [5, 6, 7, 8], [9, 10, 11, 12]]))

    