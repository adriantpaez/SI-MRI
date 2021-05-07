def multiply_sparse(vector, diag):
    result=[0 for _ in vector]    
    for i,elem in enumerate(vector):
        result[i]=elem*diag[i]
    return result
