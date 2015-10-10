import sys
import os

programs = {'4e3c1579d52bc5665d000018': 'American Express - Amex BA',
            '53a2b8990189601952ea8b2c': 'Avon - Avon Rep BAU',
            '54fdd84afcd08c00120acf53': 'Fitbit Default',
            '53f476220189604629c2662d': 'Lloyds UK Wealth',
            '50759457b0b6111b2d16dc81': 'P&O - Cruises',
            '54ae89310189607ad62320c5': 'Sage Default',
            '52e91ea3c259084c27d12f48': 'Sky - Core',
            '53c9128f0189602d360fde13': 'Sky - Sky Store',
            '50d34107b0b6111360e71f88': 'Starwood Hotels - Starwood Hotels',
            '55536919d120ab000f02f86f': 'Super AMEX',
            '511e1f8201896020393b671b': 'Thomson - Thomson',
            '54d8a1e20189603f6b5571e9': 'VW UK',
            '554c982680efc4000125fc1e': 'Citrix GTW Global',
            '5152e60f0189604e77191176': 'Hilton - Hilton HHonours Q2',
            '53d9132401896036a9cb77a6': 'M&S - France',
            '52e27bb6c259084c27d12e2a': 'Rackspace - Rackspace'}


def read_data(program_id):
    print '--- loading X training data for', program_id
    pos_labels = ['0', '1']

    X = {}
    Y = {}
    num_pos = 0
    num_neg = 0

    input_X = open('./training_data/' + program_id + '_X.tsv')

    for line in input_X:
        items = line.strip().split('\t')

        af_id = items[0]
        features = items[1:]

        X[af_id] = {}
        for feature in features:
            X[af_id][feature] = 1.0

    input_X.close()

    print '--- X loaded'

    input_Y = open('./training_data/' + program_id + '_Y.tsv')

    for line in input_Y:

        af_id, label = line.strip().split('\t')
        Y[af_id] = 1 if label in pos_labels else -1

        if label == '1':
            num_pos += 1
        else:
            num_neg += 1

    input_Y.close()

    print '--- loaded positives %d, negatives %d' % (num_pos, num_neg)

    return X, Y, num_pos, num_neg


def save_data(path_file, X, Y):
    num_pos = sum([1 for af_id in Y if Y[af_id] == 1])
    num_neg = sum([1 for af_id in Y if Y[af_id] == -1])

    with open(path_file, 'w') as output:
        for af_id in sorted(X):
            features = []
            for feature in sorted(X[af_id]):
                features.append(feature)
            line = '%s\t%s\n' % (af_id, '\t'.join(features))
            output.write(line)

    path_file = path_file.replace('_X.tsv', '_Y.tsv')

    with open(path_file, 'w') as output:

        for af_id in sorted(Y):
            line = '%s\t%d\n' % (af_id, Y[af_id])
            output.write(line)

    print '--- saved positives %d, negatives %d' % (num_pos, num_neg)


if __name__ == '__main__':

    exp_name = sys.argv[1]

    path = './' + exp_name

    os.makedirs(path)

    programs = ['53f476220189604629c2662d']

    for p in programs:

        X, Y, num_pos, num_neg = read_data(p)

        path_file = path + '/%s_X.tsv' % p

        save_data(path_file, X, Y)
