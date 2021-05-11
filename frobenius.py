from svd import factorization
import numpy as np
import math

def find_best_aproximation(m):
    min_norm=math.inf
    min_r=200
    for r in range(200, 1000):
        u, d, vt=factorization(m, r)

        reconstructed_m=np.dot(u, np.dot(np.diag(d), vt))
        subs=np.substract(m, reconstructed_m)
        norm= np.linalg.norm(subs, 'fro')
        if norm <min_norm:
            min_norm=norm
            min_r=r
    return min_r
    
    
    