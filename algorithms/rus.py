import numpy as np
from utils.data import *


def rus(X, Y, num_pos, num_neg, ratio):
    _Y = {}
    _X = {}

    hold = min(int(ratio * num_pos), num_neg)

    selection = ([1] * hold) + [0] * (num_neg - hold)

    np.random.shuffle(selection)

    c_neg = 0
    for sample_id in Y:
        if Y[sample_id] != 1:
            if selection[c_neg] == 1:
                _Y[sample_id] = Y[sample_id]
                _X[sample_id] = X[sample_id]
            c_neg += 1
        else:
            _Y[sample_id] = Y[sample_id]
            _X[sample_id] = X[sample_id]

    return _X, _Y, num_pos, hold


if __name__ == '__main__':

    exp_name = sys.argv[1]
    ratio = float(sys.argv[2])

    path = './' + exp_name

    os.makedirs(path)

    problems = ['1']

    for p in problems:

        X, Y, num_pos, num_neg = read_data(p)

        X, Y, num_pos, num_neg = rus(X, Y, num_pos, num_neg, ratio)

        path_file = path + '/%s_X.tsv' % p

        save_data(path_file, X, Y)
