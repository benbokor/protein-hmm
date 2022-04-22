from time import time
from tokenize import single_quoted
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
        self.noise_inflection_point = 55
        self.x_upper_bound = 70
        self.x_lower_bound = 30
        self.max_val = 1
        self.sharpness = 0.6
        self.x_range = None

        self.noise_upper_bound = 0.1
        self.noise_lower_bound = 0.01

        self.correlation_type = correlation_type
        self.data = None
        self.correlation_values = None

    def sigmoid(self, x, inflection_point, max_val, sharpness):
        # Make this a proper numpy operation later
        a = []
        for item in x:
            numerator = max_val
            denominator = 1 + math.exp(sharpness * (item - inflection_point))
            a.append(numerator/denominator)
        return a

    def set_timepoints(self, pts):
        self.timepoints = pts
        return self.timepoints

    def generate_data(self):
        if self.signal_func_type == "affine_zero_slope":
            print("Inflection point will be ignored")

        self.data = []
        self.x_range = np.random.uniform(
                    self.x_lower_bound, 
                    self.x_upper_bound, 
                    self.vals_per_timepoint
        )
        self.x_range = sorted(self.x_range)

        for pt in range(self.num_timepoints):    
            if self.timepoints[pt] == 1:
                if self.signal_func_type == "sigmoid":
                    noise = self.sigmoid(self.x_range, self.noise_inflection_point, self.max_val, self.sharpness)

                    for i in range(len(noise)):
                        choice = np.random.choice([True,False])

                        if choice:
                            noise[i] += np.random.uniform(
                                self.noise_lower_bound, 
                                self.noise_upper_bound
                            )
                        else:
                            noise[i] -= np.random.uniform(
                                self.noise_lower_bound, 
                                self.noise_upper_bound
                            )

                    self.data.append(noise)
            elif self.timepoints[pt] == 0:
                if self.noise_func_type == "sigmoid":
                    signal = self.sigmoid(self.x_range, self.signal_inflection_point, self.max_val, self.sharpness)
                    
                    for i in range(len(signal)):
                        choice = np.random.choice([True,False])

                        if choice:
                            signal[i] += np.random.uniform(
                                self.noise_lower_bound, 
                                self.noise_upper_bound
                            )
                        else:
                            signal[i] -= np.random.uniform(
                                self.noise_lower_bound, 
                                self.noise_upper_bound
                            )
                    
                    self.data.append(signal)

        return self.data

    def calculate_correlations(self):
        if self.data is None:
            return "Error: No data generated, please run generate_data() first"

        self.correlation_values = []

        if self.correlation_type == "pearson":
            for idx, val in enumerate(self.data):
                if self.timepoints[idx] == 0:
                    x = self.x_range
                    y = self.sigmoid(self.x_range, self.noise_inflection_point, self.max_val, self.sharpness)
                elif self.timepoints[idx] == 1:
                    x = self.x_range
                    y = self.sigmoid(self.x_range, self.noise_inflection_point, self.max_val, self.sharpness)

                corr = np.corrcoef(x, y)
                
                if self.timepoints[idx] == 0:
                    self.correlation_values.append(corr[0][1])
                else:
                    self.correlation_values.append(corr[0][0])
        else:
            print("No other correlation types are supported, please choose one of the following:")
            print("pearson")

        return self.correlation_values