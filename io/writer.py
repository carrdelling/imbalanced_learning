import os


class Writer(object):
    def __init__(self):
        self.file_contents = []


class PlainTextWriter(Writer):

    def write_dataset(self, out_path, x_data, y_data, y_names,
                      dataset_name='unknown'):

        # check that the data set has the same number of rows in x and y
        if len(x_data) != len(y_data):
            # TODO throw an exception here
            return

        full_path = os.path.join(out_path, dataset_name + '.txt')

        with open(full_path, 'w') as out_file:
            for i in sorted(x_data):
                columns = []
                for j in sorted(x_data[i]):
                    columns.append(str(x_data[i][j]))
                columns.append(y_names[y_data[i]])

                self.file_contents.append(','.join(columns))

            out_file.write('\n'.join(self.file_contents))


class ArffWriter(Writer):

    def write_dataset(self, out_path, x_data, y_data, x_names, y_names,
                      dataset_name='unknown'):

        # check that the data set has the same number of rows in x and y
        if len(x_data) != len(y_data):
            # TODO throw an exception here
            return

        full_path = os.path.join(out_path, dataset_name + '.arff')

        with open(full_path, 'w') as out_file:

            relation = '@relation %s' % dataset_name
            self.file_contents.append(relation)

            for attribute in sorted(x_names):
                if attribute != len(x_names) - 1:
                    # only real valued attributes supported
                    attribute_desc = '@attribute %s Real' % x_names[attribute]
                else:
                    # class attribute
                    list_classes = ','.join(
                        [y_names[c] for c in sorted(y_names)])
                    attribute_desc = '@attribute %s {%s}' % (
                    x_names[attribute], list_classes)

                self.file_contents.append(attribute_desc)

            self.file_contents.append('@data')

            for sample in sorted(x_data):
                sample_line = []

                for attribute in sorted(x_data[sample]):
                    sample_line.append(str(x_data[sample][attribute]))
                sample_line.append(y_names[y_data[sample]])

                self.file_contents.append(','.join(sample_line))

            out_file.write('\n'.join(self.file_contents))


if __name__ == '__main__':

    from reader import ArffReader

    input_file = '../test/datasets/glass.arff'

    reader = ArffReader()

    x_data, y_data, x_names, y_names, dataset_name = reader.parse_file(
        input_file)

    writer = ArffWriter()

    out_path = '../test/datasets/'
    dataset_name = 'glass2'

    writer.write_dataset(out_path, x_data, y_data, x_names, y_names, dataset_name)
