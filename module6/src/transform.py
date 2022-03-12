import numpy as np

def reverse(operations):
    return operations[::-1]

class Transform:
    """class to perform transformations on matrix"""
    def __init__(self, *operations):
        self.operations = operations

    def transform (self, target):
        for op in self.operations:
            target = op.transform(target)
        return target

    def reverse(self, target):
        for op in reverse(self.operations):
            target = op.reverse(target)
        return target

class Identity:
    @staticmethod
    def transform(matrix_2d):
        return matrix_2d
    @staticmethod
    def reverse(matrix_2d):
        return matrix_2d

class Rotate90:
    def __init__(self, n_rotations):
        self.n_rotations = n_rotations
        self.op = np.rot90

    def transform(self, matrix_2d):
        return self.op(matrix_2d, self.n_rotations)

    def reverse(self, trans_matrix_2d):
        return self.op(trans_matrix_2d, -self.n_rotations)

class Flip:
    def __init__(self, op):
        self.op = op

    def transform(self, matrix_2d):
        return self.op(matrix_2d)

    def reverse(self, trans_matrix_2d):
        return self.transform(trans_matrix_2d)