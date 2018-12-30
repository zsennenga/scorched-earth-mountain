import os


def load_file_as_binary(filename):
    with open(filename, mode='rb') as file_:
        return file_.read()


def pad_matrix(matrix, height, pad_value):
    return [pad_array(array, height, pad_value) for array in matrix]


def pad_array(array, pad_to, pad_with=0):
    if len(array) < pad_to:
        difference = pad_to - len(array)

        array = array + (difference * [pad_with])

    return array


def rotate_matrix_90_degrees_right(matrix):
    return list(zip(*matrix[::-1]))


def rotate_matrix_90_degrees_left(matrix):
    return rotate_matrix_90_degrees_right(
        rotate_matrix_90_degrees_right(
            rotate_matrix_90_degrees_right(
                matrix
            )
        )
    )


def mirror_array(array):
    return array[::-1]


def unpad(matrix, unpad_value):
    trimmed_arrays = []

    for array in matrix:
        reversed_ = array[::-1]
        index = 0
        for index, element in enumerate(reversed_):
            if element != unpad_value:
                break

        trimmed_arrays.append(reversed_[index:][::-1])

    return trimmed_arrays


def path_to_filename(path):
    return os.path.basename(os.path.expanduser(path)).split('.')[0]
