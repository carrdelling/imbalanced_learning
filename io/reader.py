class Reader(object):
    def __init__(self):

        self.x = {}
        self.y = {}
        self.x_names = {}
        self.y_names = {}
        self.dataset_name = 'unknown'

    def _parse_sample(self, columns):

        sample_features = {}

        for feature_id, value in enumerate(columns[:-1]):
            sample_features[feature_id] = float(value)
        class_sample = columns[-1]

        return sample_features, class_sample

    def _get_class_id(self, class_sample):

        for class_id, class_name in self.y_names.items():

            if class_name == class_sample:
                sample_class_id = class_id
                break
        else:
            sample_class_id = len(self.y_names)
            self.y_names[sample_class_id] = class_sample

        return sample_class_id


class PlainTextReader(Reader):

    def parse_file(self, input_path, separator=','):

        n_columns = None
        self.dataset_name = input_path.strip().split('/')[-1]

        with open(input_path, 'r') as data_in:
            for sample_id, line in enumerate(data_in):

                columns = line.strip().split(separator)

                # all samples must have the same number of columns
                if not n_columns:
                    n_columns = len(columns)
                elif n_columns != len(columns):
                    continue

                sample_features, class_sample = self._parse_sample(columns)
                sample_class_id = self._get_class_id(class_sample)

                self.x[sample_id] = sample_features
                self.y[sample_id] = sample_class_id

        self.x_names = {i: 'feature_%s' % i for i in xrange(len(self.x[0]) - 1)}
        self.x_names[len(self.x_names)] = 'class'

        return self.x, self.y, self.x_names, self.y_names, self.dataset_name


class ArffReader(Reader):

    def parse_file(self, input_path):

        reading_data = False

        with open(input_path, 'r') as data_in:
            for line in data_in:

                # comments line
                if line[0] == '%':
                    continue

                if '@relation' == line[:9]:
                    self.dataset_name = line.strip().split(' ')[1]

                if '@data' == line[:5]:
                    reading_data = True
                    continue

                if '@attribute' == line[:10]:
                    # no type check on this version (numeric & real supported)
                    att_name = line.strip().split(' ')[1]
                    self.x_names[len(self.x_names)] = att_name

                if reading_data:
                    columns = line.strip().split(',')

                    if len(columns) != len(self.x_names):
                        # TODO throw an exception here
                        continue

                    sample_features, class_sample = self._parse_sample(columns)
                    sample_class_id = self._get_class_id(class_sample)
                    sample_id = len(self.x)

                    self.x[sample_id] = sample_features
                    self.y[sample_id] = sample_class_id

        return self.x, self.y, self.x_names, self.y_names, self.dataset_name


if __name__ == "__main__":

    input_file = '../test/datasets/glass.txt'

    reader = PlainTextReader()

    x_data, y_data, x_names, y_names, dataset_name = reader.parse_file(
        input_file)

    count = 0

    print x_names
    print y_names
    print dataset_name
    print x_data[0]
    print y_data[0]
