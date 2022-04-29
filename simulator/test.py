import unittest
import simulator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class TestSimulator(unittest.TestCase):

    def test_instantiation(self):
        kwargs = {
            "shape":(6,6),                      # (6 time points, 6 values per timepoint)
            "sample_noise_dist": "uniform",     # ~ U[lower bound, upper bound]
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
        sim = simulator.Simulator(**kwargs)
        sim.set_timepoints([0,1,1,0,0,0])
        self.assertEqual(len(sim.timepoints), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()