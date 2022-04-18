from matplotlib import legend
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

for i in range(1,10):
    sim = simulator.Simulator(**kwargs)
    timepoints = sim.set_timepoints([0,1,1,0,0,0])
    data = sim.generate_data()
    corr = sim.calculate_correlations()
    plt.scatter(np.linspace(0,5,6), corr)

# x_generated = sim.x_range
# for i in range(len(data)):
#     tpts = sim.timepoints

#     if tpts[i] == 0:
#         plt.scatter(x_generated, data[i])
#     else:
#         plt.scatter(x_generated, data[i])

# actual_x = np.linspace(30, 70, 40)
# actual_y = sim.sigmoid(actual_x, 45, 1)
# plt.plot(actual_x, actual_y)

plt.show()