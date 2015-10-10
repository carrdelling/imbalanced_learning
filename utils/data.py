import sys
import os


def read_data(problem_id):
    print '--- loading X training data for', problem_id
    pos_labels = ['0', '1']

    X = {}
    Y = {}
    num_pos = 0
    num_neg = 0

    input_X = open('./training_data/' + problem_id + '_X.tsv')

    for line in input_X:
        items = line.strip().split('\t')

        sample_id = items[0]
        features = items[1:]

        X[sample_id] = {}
        for feature in features:
            X[sample_id][feature] = 1.0

    input_X.close()

    print '--- X loaded'

    input_Y = open('./training_data/' + problem_id + '_Y.tsv')

    for line in input_Y:

        sample_id, label = line.strip().split('\t')
        Y[sample_id] = 1 if label in pos_labels else -1

        if label == '1':
            num_pos += 1
        else:
            num_neg += 1

    input_Y.close()

    print '--- loaded positives %d, negatives %d' % (num_pos, num_neg)

    return X, Y, num_pos, num_neg


def save_data(path_file, X, Y):
    num_pos = sum([1 for sample_id in Y if Y[sample_id] == 1])
    num_neg = sum([1 for sample_id in Y if Y[sample_id] == -1])

    with open(path_file, 'w') as output:
        for sample_id in sorted(X):
            features = []
            for feature in sorted(X[sample_id]):
                features.append(feature)
            line = '%s\t%s\n' % (sample_id, '\t'.join(features))
            output.write(line)

    path_file = path_file.replace('_X.tsv', '_Y.tsv')

    with open(path_file, 'w') as output:

        for sample_id in sorted(Y):
            line = '%s\t%d\n' % (sample_id, Y[sample_id])
            output.write(line)

    print '--- saved positives %d, negatives %d' % (num_pos, num_neg)


if __name__ == '__main__':

    exp_name = sys.argv[1]

    path = './' + exp_name

    os.makedirs(path)

    problems = ['1']

    for p in problems:

        X, Y, num_pos, num_neg = read_data(p)

        path_file = path + '/%s_X.tsv' % p

        save_data(path_file, X, Y)
