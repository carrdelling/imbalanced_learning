import sys
import os
import numpy as np
from utils.data import *


def rus(X, Y, num_pos, num_neg, ratio):

	_Y = {}
	_X = {}

	hold = min(int(ratio * num_pos),num_neg)

	selection = ([1] * hold) + [0] * (num_neg - hold)

	np.random.shuffle(selection)

	c_neg = 0
	for af_id in Y:
		if Y[af_id] != 1:
			if selection[c_neg] == 1:
				_Y[af_id] = Y[af_id] 
				_X[af_id] = X[af_id]
			c_neg += 1
		else:
			_Y[af_id] = Y[af_id]
			_X[af_id] = X[af_id]
	
	return _X, _Y, num_pos, hold

if __name__ == '__main__':

	exp_name = sys.argv[1]
	ratio = float(sys.argv[2])

	path = './'+exp_name

	os.makedirs(path)
 			
	programs = ['53f476220189604629c2662d']

	for p in programs:
		
		X, Y, num_pos, num_neg = read_data(p)

		X, Y, num_pos, num_neg = rus(X, Y, num_pos, num_neg, ratio)

		path_file = path +'/%s_X.tsv' % p

		save_data(path_file,X,Y)
		