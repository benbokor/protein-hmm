import simulator
import numpy as np
import matplotlib.pyplot as plt

kwargs = {
    "shape":(6,6),                      # (6 time points, 6 values per timepoint)
    "sample_noise_dist": "uniform",     # ~ U[lower bound, upper bound]
    "signal_func_type": "sigmoid",      
    "noise_func_type": "sigmoid",
    "correlation_type": "pearson"
}

sim = simulator.Simulator(**kwargs)
timepoints = sim.set_timepoints([0,1,1,0,0,0])
data = sim.generate_data()

# corr = sim.calculate_correlations()
# print(corr)

x_noise = sim.noise_xrange
x_signal = sim.signal_xrange

for i in range(len(data)):
    tpts = sim.timepoints

    if tpts[i] == 0:
        plt.scatter(x_noise, data[i])
    else:
        plt.scatter(x_signal, data[i])

plt.savefig("tmp.png")