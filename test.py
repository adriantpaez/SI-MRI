from mri.main import mri
from mri.metrics import metrics
from mri.parse import parse_queries, parse_rel


def test(query_file, rel_file):
    queries = parse_queries(query_file)
    rels = parse_rel(rel_file)
    av_r = 0
    av_p = 0
    av_f1 = 0
    k = 0
    for i, key in enumerate(queries):
        try:
            ground_truth = [elem for elem in rels[key]]
            print(queries[key])
            predicted = [f'{elem}' for elem in mri(queries[key], 10)]
            r, p, f1 = metrics(ground_truth, predicted)
            av_r += r
            av_p += p
            av_f1 += f1
            k += 1
        except KeyError:
            pass
    print(f'average recall: {av_r / k}')

    print(f'average precission: {av_p / k}')

    print(f'average f1: {av_f1 / k}')


test('CISI/CISI.QRY.json', 'CISI/CISI.REL.json')
