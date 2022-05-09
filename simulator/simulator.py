import numpy as np
import math

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
        self.distance_values = None

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
                    y = self.sigmoid(self.x_range, self.signal_inflection_point, self.max_val, self.sharpness)

                corr = np.corrcoef(x, y)
                
                if self.timepoints[idx] == 0:
                    self.correlation_values.append(corr[0][1])
                else:
                    self.correlation_values.append(corr[0][0])
        else:
            print("No other correlation types are supported, please choose one of the following:")
            print("pearson")

        return self.correlation_values

    def calculate_distances(self):
        if self.data is None:
            return "Error: No data generated, please run generate_data() first"

        self.distance_values = []

        for idx, val in enumerate(self.data):
            if self.timepoints[idx] == 0:
                x = self.x_range
                y_bait = self.sigmoid(self.x_range, self.noise_inflection_point, self.max_val, self.sharpness)
            elif self.timepoints[idx] == 1:
                x = self.x_range
                y_bait = self.sigmoid(self.x_range, self.signal_inflection_point, self.max_val, self.sharpness)

            prey_x_range = np.random.uniform(
                    self.x_lower_bound, 
                    self.x_upper_bound, 
                    self.vals_per_timepoint
            )
            y_prey = self.sigmoid(prey_x_range, self.signal_inflection_point, self.max_val, self.sharpness)
            

            rss = np.sum((np.array(y_bait) - np.array(y_prey)) ** 2) # Calculate RSS
            
            # Append RSS to distance values
            if self.timepoints[idx] == 0:
                self.distance_values.append(rss)
            else:
                self.distance_values.append(rss)

        # Normalize distance values as values from 0 to 1
        self.distance_values = list(np.array(self.distance_values) / np.sum(np.array(self.distance_values)))
        return self.distance_values

    def sample_correlations(self, learning_data=None):
        """
        Samples in-complex and out-of-complex data from beta and normal distributions respectively
        Optionally users can pass in learning_data to estimate distribution parameters.
        
        self: Simulator
        learning_data: pandas.DataFrame
        """

        # Estimating parameters for in-complex and out-of-complex timepoints
        if learning_data is not None:
            print("Estimating beta and normal distribution paramaters")
            assert learning_data.shape[1] == 2
            # Estimate beta parameters
            # https://stats.stackexchange.com/questions/12232/calculating-the-parameters-of-a-beta-distribution-using-the-mean-and-variance)
            beta_mean = learning_data[learning_data["in_complex"] == True].mean()
            beta_variance = learning_data[learning_data["in_complex"] == True].var()
            beta_a = ((1-beta_mean)/(beta_variance ** 2) - 1/beta_mean) * (beta_mean ** 2)
            beta_b = beta_a * ((1/beta_mean) - 1)

            # Estimate normal parameters
            normal_mean = learning_data[learning_data["in_complex"] == False].mean()
            normal_variance = learning_data[learning_data["in_complex"] == False].var()
        else:
            # Based on values I eyeballed from plots
            # TODO: Come up with better estimators from actual paper data
            beta_a = 8.83
            beta_b = 2.12
            normal_mean = 0.5
            normal_variance = 0.15

        self.correlation_values = []
        
        # Generating correlations from distribution
        for pt in range(self.num_timepoints):
            if self.timepoints[pt] == 1:
                # In-complex beta distribution sampling
                self.correlation_values.append(
                    np.random.beta(a=beta_a, b=beta_b)
                )
            elif self.timepoints[pt] == 0:
                # # Out-of-complex normal distribution sampling
                self.correlation_values.append(
                    np.random.normal(loc=normal_mean, scale=normal_variance)
                )

        # Normalize to -1 to 1
        self.correlation_values = np.array(self.correlation_values)/ np.sum(np.array(self.correlation_values))
        self.correlation_values = self.correlation_values * 2
        self.correlation_values = self.correlation_values - 1
        self.correlation_values = list(self.correlation_values)

        return (self.correlation_values)
    
    def sample_distances(self, learning_data=None):
        """
        Samples in-complex and out-of-complex data from beta and normal distributions respectively
        Optionally users can pass in learning_data to estimate distribution parameters.
        
        self: Simulator
        learning_data: pandas.DataFrame
        """

        # Estimating parameters for in-complex and out-of-complex timepoints
        if learning_data is not None:
            print("Estimating beta and normal distribution paramaters")
            assert learning_data.shape[1] == 2
            # Estimate beta parameters
            # https://stats.stackexchange.com/questions/12232/calculating-the-parameters-of-a-beta-distribution-using-the-mean-and-variance)
            beta_mean = learning_data[learning_data["in_complex"] == True].mean()
            beta_variance = learning_data[learning_data["in_complex"] == True].var()
            beta_a = ((1-beta_mean)/(beta_variance ** 2) - 1/beta_mean) * (beta_mean ** 2)
            beta_b = beta_a * ((1/beta_mean) - 1)

            # Estimate normal parameters
            normal_mean = learning_data[learning_data["in_complex"] == False].mean()
            normal_variance = learning_data[learning_data["in_complex"] == False].var()
        else:
            # Based on values I eyeballed from plots
            # TODO: Come up with better estimators from actual paper data
            beta_a = 8.83
            beta_b = 2.12
            normal_mean = 0.5
            normal_variance = 0.15

        self.correlation_values = []
        
        # Generating correlations from distribution
        for pt in range(self.num_timepoints):
            if self.timepoints[pt] == 1:
                # In-complex beta distribution sampling
                self.correlation_values.append(
                    np.random.beta(a=beta_a, b=beta_b)
                )
            elif self.timepoints[pt] == 0:
                # # Out-of-complex normal distribution sampling
                self.correlation_values.append(
                    np.random.normal(loc=normal_mean, scale=normal_variance)
                )

        return self.correlation_values