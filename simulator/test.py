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

    def test_generate_data(self):
        kwargs = {
            "shape":(6,6),     
            "sample_noise_dist": "uniform",
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
        sim = simulator.Simulator(**kwargs)
        sim.set_timepoints([0,1,1,0,0,0])
        data = sim.generate_data()
        self.assertIsNotNone(data)

    def test_calculate_correlations(self):
        kwargs = {
            "shape":(6,6),                      
            "sample_noise_dist": "uniform",     
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
        sim = simulator.Simulator(**kwargs)
        sim.set_timepoints([0,1,1,0,0,0])
        sim.generate_data()
        corr = sim.calculate_correlations()
        self.assertEqual(len(corr), 6)
        self.assertGreater(corr[1], corr[4])

    def test_calculate_distances(self):
        kwargs = {
            "shape":(6,6),                      
            "sample_noise_dist": "uniform",     
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
        sim = simulator.Simulator(**kwargs)
        sim.set_timepoints([0,1,1,0,0,0])
        sim.generate_data()
        distances = sim.calculate_distances()

        # Add better assertions if time permits
        self.assertIsNotNone(distances)

    def test_sample_correlations(self):
        kwargs = {
            "shape":(6,6),                      
            "sample_noise_dist": "uniform",     
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
        sim = simulator.Simulator(**kwargs)
        sim.set_timepoints([0,1,1,0,0,0])
        sim.generate_data()
        correlations = sim.sample_correlations()

        # Add better assertions if time permits
        self.assertIsNotNone(correlations)

    def test_sample_distances(self):
        kwargs = {
            "shape":(6,6),                      
            "sample_noise_dist": "uniform",     
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
        sim = simulator.Simulator(**kwargs)
        sim.set_timepoints([0,1,1,0,0,0])
        sim.generate_data()
        distances = sim.sample_distances()

        # Add better assertions if time permits
        self.assertIsNotNone(distances)



if __name__ == '__main__':
    unittest.main()