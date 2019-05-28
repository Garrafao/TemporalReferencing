import numpy as np
from composes.matrix.linalg import Linalg


class RegressionLearner(object):
    """
    Implements a set of regression methods.

    Supported regression methods are least squares regression and
    ridge regression. Ridge regression can be used with generalized
    cross validation. (Hastie, Tibshirani and Friedman, Second edition,
    page 244)
    """


    def __init__(self):
        '''
        Constructor
        '''

    def has_intercept(self):
        return self._intercept


class LstsqRegressionLearner(RegressionLearner):
    """
    This class performs Least Squares Regression.

    It finds the matrix X which solves:

    :math:`X = argmin(||AX - B||_2)`

    It can be used with intercept or without (by default intercept=True).

    """

    def __init__(self, intercept=True):
        self._intercept = intercept

    def train(self, matrix_a, matrix_b):
        return Linalg.lstsq_regression(matrix_a, matrix_b, self._intercept)


class RidgeRegressionLearner(RegressionLearner):
    """
    This class performs Ridge Regression.

    It finds the matrix X which solves:

    :math:`X = argmin(||AX - B||_2 + \\lambda||X||_2)`

    It can be used with intercept or without (by default intercept=True).
    Cross validation can be used with default :math:`\\lambda` range of
    :math:`linspace(0, 5, 11)`. By default Generalized cross validation is performed.
    If cross validation is set False it requires the input of a :math:`\\lambda` value.

    """

    def __init__(self, intercept=True, param_range=None, crossvalidation=True, param=None):
        self._intercept = intercept
        self._param_range = param_range if param_range is not None else np.linspace(0.0, 5, 11)

        self._param = param
        self._crossvalidation = crossvalidation

        if param:
            self._crossvalidation = False
            self._param = param

        if not self._crossvalidation and self._param is None:
            raise ValueError("Cannot run (no-crossvalidation) RidgeRegression with no lambda value!")


    def train(self, matrix_a, matrix_b):
        """
        If cross validation is set to True, it performs generalized
        cross validation. (Hastie, Tibshirani and Friedman, Second edition,
        page 244).
        """

        if not self._crossvalidation:
            return Linalg.ridge_regression(matrix_a, matrix_b, self._param,
                                           self._intercept)[0]

        else:
            min_err_param = 0
            min_err = np.Inf
            gcv_err = np.Inf

            N = matrix_a.shape[0]
            for param in self._param_range:

                mat_x, S_trace, err1 = Linalg.ridge_regression(matrix_a, matrix_b, param,
                                                               self._intercept)

                nom = pow(1 - S_trace / N, 2) * N
                if nom != 0:
                    gcv_err = (err1 * err1) / nom

                if gcv_err < min_err:
                    min_err = gcv_err
                    min_err_param = param

            #print "lambda:", min_err_param
            return Linalg.ridge_regression(matrix_a, matrix_b, min_err_param,
                                           self._intercept)[0]
