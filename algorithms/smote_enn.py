import sys
import os
import numpy as np
from utils.data import *
from utils.functions import *
from smote import smote


def enn(X, Y, neighbours=3):
    hold = {}
    _X = {}
    _Y = {}

    for sample_id in Y:

        # search for the N nearest samples
        n_list = nn_search(X, sample_id, Y.keys(), neighbours=neighbours)

        # count labels
        labels = {-1: 0, 1: 0}

        for n in n_list:
            labels[Y[n[0]]] += 1

        max_label = -1 if labels[-1] > labels[1] else 1

        # keep only instances that classify correctly
        hold[sample_id] = 1 if Y[sample_id] == max_label else 0

    for sample_id in Y:

        if hold[sample_id]:
            _X[sample_id] = X[sample_id]
            _Y[sample_id] = Y[sample_id]

    num_pos = sum([1 for sample_id in _Y if _Y[sample_id] == 1])
    num_neg = sum([1 for sample_id in _Y if not _Y[sample_id] == -1])

    return _X, _Y, num_pos, num_neg


if __name__ == '__main__':

    exp_name = sys.argv[1]
    neighbours_smote = int(sys.argv[2])
    neighbours_enn = int(sys.argv[3])

    path = './' + exp_name

    os.makedirs(path)

    problems = ['1']

    for p in problems:

        X, Y, num_pos, num_neg = read_data(p)

        X, Y, num_pos, num_neg = smote(X, Y, num_pos, num_neg, neighbours_smote)

        X, Y, num_pos, num_neg = enn(X, Y, neighbours_enn)

        path_file = path + '/%s_X.tsv' % p

        save_data(path_file, X, Y)
