# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:02:17 2025

Implementation of Wittkuhn et al (2021) detection method for seqeucnes
of decoded stimuli

@author: Simon Kern
"""
import numpy as np
from scipy import stats
import warnings
from scipy.stats import kendalltau
from scipy.optimize import nnls
from statsmodels.api import OLS, add_constant


def char2num(seq):
    """convert list of chars to integers eg ABC=>012"""

    if isinstance(seq, str):
        seq = list(seq.upper())
    assert ord('A')-65 == 0
    nums = [ord(c.upper())-65 for c in seq]
    assert all([0<=n<=90 for n in nums])
    return nums


def difference(proba):
    """compute difference between the rows of `values`"""
    assert len(proba)==2
    return -np.diff(proba, axis=0)[0]


def linear_regression(proba):
    """compute a pearson correlation for a row of values, sign flipped"""
    X = add_constant(np.arange(len(proba)))  # Add intercept
    model = OLS(proba, X).fit()
    slope = model.params[1]  # Coefficient for position    return -re.statistic
    return -slope


def compute_ws(proba, order=None, method='linear_regression'):
    """
    Calculate a correlation coefficient on each time step of the probability
    vector

    If no sequence is give, states are to be expected in ascending order

    Parameters
    ----------
    proba : np.ndarray
        Array containing probability estimates across time of size
        (n_classes, n_timesteps)
    order : (np.array, list, str), optional
        The expected order of the classes. If None is supplied will assume a
        linear ordering [1,2,3,4,..]. Can be supplied as numeric array or as
        sequence string in the form of capitalized letters 'ABC'.
        The default is None.
    method : str, optional
        Which method to use to calculate the regression coefficient at each
        time point. Can be either 'difference' (for two classes) or
        'linear_regression' for more classes _or_ a custom callable that
        accepts an ordered 'proba' vector as input and computes one value for
        each timestep (second dimension of the proba array).
        The default is 'linear_regression'

    Returns
    -------
    values - regression coefficient across time
    """
    assert proba.ndim == 2, f'proba must be 2d (n_classes, probabilities) but is {proba.ndim=}'
    assert np.diff(proba.shape)>1, f'proba has wrong dimension: {proba.shape=}, second should be larger'
    assert len(proba)>1, f'must at least supply two classes, but {proba.shape=}'

    if len(proba)==2:
        warnings.warn(f'Only two classes, will switch method to difference, ignoring {method=}')
        method = difference

    # convert order to int if necessary
    if order is None:
        order_int = np.arange(len(proba))
    elif isinstance(order, str) or isinstance(order[0], str):
        order_int = np.array(char2num(order))
    elif isinstance(order, (np.ndarray, list)):
        order_int = np.array(order)

    assert np.issubdtype(order_int.dtype, np.integer), 'if `order` is array, must be int'
    assert set(order_int) == set(np.arange(len(proba))), 'not each class represented in proba'

    if isinstance(method, str):
        assert (func := globals().get(method)), \
            'method string must be `pearson` or `difference` or callable'
        assert callable(func)

    elif callable(method):
        func = method
    else:
        raise ValueError(f'method must be callable or `regression` or `difference` but is {method=}')

    values = func(proba[order_int])
    values = np.array(values)
    assert len(values)==proba.shape[1], f'method output must of len {proba.shape[1]} but is {len(values)=}'
    return np.array(values)
