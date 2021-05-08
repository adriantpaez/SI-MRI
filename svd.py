from numpy.linalg import svd


def factorization(adj, reduced_dimension=None):
    if reduced_dimension:
        terms, diag, docs=svd(adj, full_matrices=False)
        return terms[:reduced_dimension][:], diag[:reduced_dimension], [elem[:reduced_dimension] for elem in docs]
    return svd(adj, full_matrices=False)


print(factorization([[1,2,3,4], [5,6,7,8], [9, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20]], reduced_dimension=3))