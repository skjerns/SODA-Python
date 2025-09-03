# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 11:06:17 2025

some of these tests dont actually test anything meaningfull automatically,
they are creating plots that can be assessed individually later

@author: Simon
"""

import sys; sys.path.append('..')
import os
import unittest
import core
import numpy as np
import scipy
from scipy import io
from tqdm import tqdm
from tdlm import plotting
import matplotlib.pyplot as plt
import tdlm
from scipy import stats
import math


class TestCore(unittest.TestCase):


    def test_with_sinus_multi(self):
        pass

    def test_with_gaussians_multi(self):

        mu = 0
        variance = 1
        sigma = math.sqrt(variance)
        proba = np.zeros([5, 100])

        for i in range(5):
            x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
            p = stats.norm.pdf(x, loc=i*0.3, scale=sigma)
            proba[i, :] = p

        samples = proba[:, ::15]
        rs = core.compute_ws(proba)
        fig = plt.plot(rs)

    def test_with_gaussians_diffference(self):

        mu = 0
        variance = 1
        sigma = math.sqrt(variance)
        x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
        p = stats.norm.pdf(x, mu, sigma)
        proba = np.zeros([2, 100])
        dist = 3
        for i in range(2):
            proba[i, i*dist:] = p[:len(p)-i*dist]

        samples = proba[:, ::15]
        rs = core.compute_ws(proba)
        plt.gca().clear()
        plt.plot(rs)


if __name__=='__main__':
    unittest.main()
