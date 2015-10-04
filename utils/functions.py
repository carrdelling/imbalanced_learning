import numpy as np
from math import sqrt

cache = {}

def similarity(a,b,X):

	if a not in cache or b not in cache[a]:
		if a not in cache:
			cache[a] = {}
		if b not in cache:
			cache[b] = {}

		cache[a][b] = cosine_similarity(X[a],X[b])
		cache[b][a] = cache[a][b]

	return cache[a][b]

def cosine_similarity(first,second):
   	"compute cosine similarity of first to second: (v1 dot v2)/(||v1||*||v2||)"

	a_set = set(first.keys())
	b_set = set(second.keys())
	a = float(len(a_set))
	b = float(len(b_set))
	a_b = float(len(a_set & b_set))
	sim = a_b / (sqrt(a)*sqrt(b))

	return sim

def jaccard_similarity(first,second):

	#compute the jaccard similarity between both sets
	a_set = set(first.keys())
	b_set = set(second.keys())
	a = float(len(a_set))
	b = float(len(b_set))
	a_b = float(len(a_set & b_set))
	sim = a_b / (a + b + a_b)

	return sim

def nn_search(X, query,instances,neighbours=1):

	instances.remove(query)
	np.random.shuffle(instances)
	n_list = [('None',-1)] * neighbours
	
	for ins in instances:
				
		#compute similarity
		sim = similarity(query,ins,X)
				
		#save only the best neighbors
		index = -1

		for c, (_,_sim) in enumerate(n_list):

			if _sim >= sim:
				break
			else:
				index = c   

		if index == 0:
			n_list[0] = (ins,sim)
		elif index > 0:
			n_list = n_list[1:index+1] + [(ins,sim)] + n_list[index+1:]

	return n_list
