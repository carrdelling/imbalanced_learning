import sys
import os
import numpy as np
from utils.data import *
from utils.functions import *
from smote import smote


def enn(X, Y, num_pos, num_neg, neighbours=3):
    hold = {}
    _X = {}
    _Y = {}

    for af_id in Y:

        # search for the N nearest samples
        n_list = nn_search(X, af_id, Y.keys(), neighbours=neighbours)

        # count labels
        labels = {-1: 0, 1: 0}

        for n in n_list:
            labels[Y[n[0]]] += 1

        max_label = -1 if labels[-1] > labels[1] else 1

        # keep only instances that classify correctly
        hold[af_id] = 1 if Y[af_id] == max_label else 0

    for af_id in Y:

        if hold[af_id]:
            _X[af_id] = X[af_id]
            _Y[af_id] = Y[af_id]

    num_pos = sum([1 for af_id in _Y if _Y[af_id] == 1])
    num_neg = sum([1 for af_id in _Y if not _Y[af_id] == -1])

    return _X, _Y, num_pos, num_neg


if __name__ == '__main__':

    exp_name = sys.argv[1]
    neighbours_smote = int(sys.argv[2])
    neighbours_enn = int(sys.argv[3])

    path = './' + exp_name

    os.makedirs(path)

    programs = ['53f476220189604629c2662d']

    for p in programs:

        X, Y, num_pos, num_neg = read_data(p)

        X, Y, num_pos, num_neg = smote(X, Y, num_pos, num_neg, neighbours_smote)

        X, Y, num_pos, num_neg = enn(X, Y, num_pos, num_neg, neighbours_enn)

        path_file = path + '/%s_X.tsv' % p

        save_data(path_file, X, Y)
