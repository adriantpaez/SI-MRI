from parse import parse_queries, parse_rel
from main import mri
from metrics import recall, precission, f1_score

def test(query_file, rel_file):
    queries=parse_queries(query_file)
    rels=parse_rel(rel_file)

    for i,key in enumerate(queries): 
        try:   
            ground_truth=rels[key]
            predicted=[f'{elem}' for elem in mri(queries[key], len(rels[key]))]
            print(f'recall_{i}: {recall(ground_truth, predicted)}')
            print(f'precission_{i}: {precission(ground_truth, predicted)}')
        except KeyError:
             pass
        
        
    
        
test('CISI.QRY.json', 'CISI.REL.json')   
    