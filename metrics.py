def metrics(gt, p):
    intersection=sum([1 for elem in gt if elem in p])
    r=intersection/len(gt)
    p=intersection/len(p)
    f1=(2*r*p)/(r+p) if r+p>0 else 0
    return r, p, f1
