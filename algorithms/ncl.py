from utils.data import *
from utils.functions import *


def ncl(X, Y, neighbours=3):
    _X = {}
    _Y = {}

    remove = set()

    for sample_id in Y:

        # search for the N nearest samples
        n_list = nn_search(X, sample_id, Y.keys(), neighbours=neighbours)

        # count labels
        labels = {-1: 0, 1: 0}

        for n in n_list:
            labels[Y[n[0]]] += 1

        if labels[-1] == neighbours and Y[sample_id] == 1:
            for (_af_id, _) in n_list:
                remove.add(_af_id)

        if labels[1] == neighbours and Y[sample_id] == 0:
            remove.add(sample_id)

    for sample_id in Y:
        if sample_id not in remove:
            _X[sample_id] = X[sample_id]
            _Y[sample_id] = Y[sample_id]

    num_pos = sum([1 for sample_id in _Y if _Y[sample_id] == 1])
    num_neg = sum([1 for sample_id in _Y if not _Y[sample_id] == -1])

    return _X, _Y, num_pos, num_neg


if __name__ == '__main__':

    exp_name = sys.argv[1]
    neighbours = int(sys.argv[2])

    path = './' + exp_name

    os.makedirs(path)

    problems = ['q']

    for p in problems:

        X, Y, num_pos, num_neg = read_data(p)

        X, Y, num_pos, num_neg = ncl(X, Y, neighbours)

        path_file = path + '/%s_X.tsv' % p

        save_data(path_file, X, Y)
