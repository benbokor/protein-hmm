import simulator

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

corr = sim.calculate_correlations()
print(corr)