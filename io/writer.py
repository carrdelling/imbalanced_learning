import os


class Writer(object):
    def __init__(self):
        pass


class PlainTextWriter(object):
    def __init__(self):
        pass

    def write_dataset(self, out_path, x_data, y_data, y_names,
                      dataset_name='unknown'):

        file_contents = []

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

                file_contents.append(','.join(columns))

            out_file.write('\n'.join(file_contents))


if __name__ == '__main__':

    from reader import PlainTextReader

    input_file = '../test/datasets/glass.txt'

    reader = PlainTextReader()

    x_data, y_data, x_names, y_names, dataset_name = reader.parse_file(
        input_file)

    writer = PlainTextWriter()

    out_path = '../test/datasets/'
    dataset_name = 'glass2'

    writer.write_dataset(out_path, x_data, y_data, y_names, dataset_name)
