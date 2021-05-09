from parse import parse_queries, parse_rel
from main import mri
from metrics import recall, precission, f1_score

def test(query_file, rel_file):
    queries=parse_queries(query_file)
    rels=parse_rel(rel_file)

    for key in queries: 
        try:   
            ground_truth=rels[key]
            predicted=[elem for elem in mri(queries[key], len(rels[key]))]
            print(recall(ground_truth, predicted))
        except KeyError:
            pass
        
        
    
        
test('CISI.QRY.json', 'CISI.REL.json')   
    