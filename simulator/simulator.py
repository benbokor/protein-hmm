from time import time
import numpy as np
import matplotlib.pyplot as plt
# import numpy.typings as npt
import math
# from typing import Final, List, Tuple

# signal_func_types: Final = ["sigmoid", "linear", "affine"] 
# noise_func_types: Final = ["sigmoid", "linear", "affine"] 
# sample_noise_distributions: Final = ["normal", "uniform"]
# correlation_types: Final = ["pearson"]

class Simulator():
    def __init__(self, shape, sample_noise_dist, signal_func_type, noise_func_type, correlation_type="pearson"):
        """
        shape - number of values at each timepoint and the number of time points respectively
        sample_noise_dist
        """
        
        self.timepoints = None
        self.num_timepoints = shape[1]
        self.vals_per_timepoint = shape[0]
        self.sample_noise_dist = sample_noise_dist
        self.signal_func_type = signal_func_type
        self.noise_func_type = noise_func_type

        self.signal_inflection_point = 45
        self.signal_upper_bound = 70
        self.signal_lower_bound = 30
        self.max_val = 1
        self.signal_xrange = None

        self.noise_inflection_point = 45
        self.noise_upper_bound = 70
        self.noise_lower_bound = 30
        self.noise_xrange = None

        self.correlation_type = correlation_type
        self.data = None
        self.correlation_values = None

    def sigmoid(self, x, inflection_point, max_val):
        # Make this a proper numpy operation later
        a = []
        for item in x:
            a.append(max_val/(1+math.exp(item - inflection_point)))
        return a

    def set_timepoints(self, pts):
        self.timepoints = pts
        return self.timepoints

    def print_vars(self):
        print(vars(self))

    def generate_data(self):
        if self.signal_func_type == "affine_zero_slope":
            print("Inflection point will be ignored")

        self.data = []
        for pt in range(self.num_timepoints):
            self.signal_xrange = np.random.uniform(
                    self.signal_lower_bound, 
                    self.signal_upper_bound, 
                    self.vals_per_timepoint
            )

            self.noise_xrange = np.random.uniform(
                    self.noise_lower_bound, 
                    self.noise_upper_bound, 
                    self.vals_per_timepoint
            )
            
            if self.timepoints[pt] == 0:
                if self.signal_func_type == "sigmoid":
                    noise = self.sigmoid(self.noise_xrange, self.signal_inflection_point, self.max_val)
                    self.data.append(noise)
            elif self.timepoints[pt] == 1:
                if self.noise_func_type == "sigmoid":
                    signal = self.sigmoid(self.signal_xrange, self.noise_inflection_point, self.max_val)
                    self.data.append(signal)

        return self.data

    def calculate_correlations(self):
        if self.data is None:
            return "Error: No data generated, please run generate_data() first"

        self.correlation_values = []

        if self.correlation_type == "pearson":
            for idx, val in enumerate(self.data):
                if self.timepoints[idx] == 0:
                    x = self.noise_xrange
                    y = self.sigmoid(self.signal_xrange, self.noise_inflection_point, self.max_val)
                elif self.timepoints[idx] == 1:
                    x = self.noise_xrange
                    y = self.sigmoid(self.signal_xrange, self.noise_inflection_point, self.max_val)

                corr = np.corrcoef(x, y)
                
                if self.timepoints[idx] == 0:
                    self.correlation_values.append(corr[0][1])
                else:
                    self.correlation_values.append(corr[0][0])
        else:
            print("No other correlation types are supported, please choose one of the following:")
            print("pearson")

        return self.correlation_values