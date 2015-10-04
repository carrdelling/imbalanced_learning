import sys
import os
import numpy as np
from utils.data import *
from utils.functions import nn_search

def smote(X, Y, num_pos, num_neg, neighbours=5):

	neighbours = min(neighbours,num_pos)

	_Y = {}
	_X = {}
	
	new_samples = 0

	Y_pos = [x for x in Y if Y[x] == 1]
	np.random.shuffle(Y_pos)

	#extract features of the positive samples
	Y_data = {}

	for af_id in Y_pos:
		Y_data[af_id] = set(X[af_id].keys())

	generate = True
	while generate: 

		#for each positive sample
		for af_id in Y_pos:
			positives = list(Y_pos)
			
			n_list = nn_search(X, af_id, positives,neighbours=neighbours)

			#choose a random best neighbor
			best = n_list[np.random.randint(neighbours)][0]

			#perform a crossover with the initial positive sample
			new_sample = set()
			common = Y_data[af_id] & Y_data[best]
			for feature in set(Y_data[af_id] | Y_data[best]):
				if feature in common or np.random.rand() < 0.5:
					new_sample.add(feature)

			#create the new sample
			s_id = 'syn_%d' % new_samples 
			_Y[s_id] = 1
			_X[s_id] = {}

			for feature in new_sample:
				_X[s_id][feature] = 1.0			

			new_samples += 1

			if new_samples + num_pos >= num_neg:
				generate = False
				break

	# add the original samples
	for af_id in Y:
		_Y[af_id] = Y[af_id]
		_X[af_id] = X[af_id]

	return _X, _Y, num_pos+new_samples, num_neg 


if __name__ == '__main__':

	exp_name = sys.argv[1]
	neighbours = int(sys.argv[2])

	path = './'+exp_name

	os.makedirs(path)
 			
	programs = ['53f476220189604629c2662d']

	for p in programs:
		
		X, Y, num_pos, num_neg = read_data(p)

		X, Y, num_pos, num_neg = smote(X, Y, num_pos, num_neg, neighbours)

		path_file = path +'/%s_X.tsv' % p

		save_data(path_file,X,Y)
