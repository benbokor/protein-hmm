import numpy as np
# import numpy.typings as npt
import math
# from typing import List, Tuple

# signal_func_types: Final = ["sigmoid", "linear", "affine"] 
# noise_func_types: Final = ["sigmoid", "linear", "affine"] 
# sample_noise_distributions: Final = ["normal", "uniform"]

class Simulator():
    def __init__(self, shape, sample_noise_dist, signal_func_type, noise_func_type):
        """
        shape - number of values at each timepoint and the number of time points respectively
        sample_noise_dist
        """
        
        self.timepoints = shape[1]
        self.vals_per_timepoint = shape[0]
        self.sample_noise_dist = sample_noise_dist
        self.signal_func_type = signal_func_type
        self.noise_func_type = noise_func_type

        self.signal_inflection_point = 45
        self.signal_upper_bound = 70
        self.signal_lower_bound = 30
        self.max_val = 1

        self.noise_inflection_point = 45
        self.noise_upper_bound = 70
        self.noise_lower_bound = 30

        self.data = None


    # Internal Function Definitions
    def affine(self, intercept, slope, ub, lb):
        return slope * np.arange(lb, ub) + intercept

    def linear(self, slope, ub, lb):
        return self.affine(self, 0, slope, ub, lb)

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
        for pt in self.timepoints:
            signal_xrange = np.random.uniform(
                    self.signal_lower_bound, 
                    self.signal_upper_bound, 
                    self.vals_per_timepoint
            )

            noise_xrange = np.random.uniform(
                    self.noise_lower_bound, 
                    self.noise_upper_bound, 
                    self.vals_per_timepoint
            )
            
            if pt == 0:
                if self.signal_func_type == "sigmoid":
                    noise = self.sigmoid(noise_xrange, self.signal_inflection_point, self.max_val)
                    self.data.append(noise)
            elif pt == 1:
                if self.noise_func_type == "sigmoid":
                    signal = self.sigmoid(signal_xrange, self.noise_inflection_point, self.max_val)
                    self.data.append(signal)

        return self.data

kwargs = {
    "shape":(6,6), 
    "sample_noise_dist": "uniform", 
    "signal_func_type": "sigmoid", 
    "noise_func_type": "sigmoid"
}

sim = Simulator(**kwargs)
timepoints = sim.set_timepoints([0,1,1,0,0,0])
data = sim.generate_data()

print(data)