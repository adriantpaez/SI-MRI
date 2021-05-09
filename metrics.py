def precission(ground_truth, prediction):
    #ground truth will be just relevant docs, prediction will be relevant docs, no ranking handling by now
    tp=0
    fp=0
    for elem in prediction:
        val=elem in ground_truth
        tp+=val
        fp+= 1-val
        
    return tp/(fp+tp)


def recall(ground_truth, prediction):
    tp=0
    fn=0
    for elem in ground_truth:
        val=elem in prediction
        fn+=1-val
        tp+=val
    return tp/(tp+fn)

def f1_score(ground_truth, prediction):
    p=precission(ground_truth, prediction)
    r=recall(ground_truth, prediction)
    return (2*p*r)/(p+r)


    
