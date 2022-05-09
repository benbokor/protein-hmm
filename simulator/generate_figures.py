import simulator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing

"""
Initializations
"""
kwargs = {
            "shape":(6,6),                      # (6 time points, 6 values per timepoint)
            "sample_noise_dist": "uniform",     # ~ U[lower bound, upper bound]
            "signal_func_type": "sigmoid",      
            "noise_func_type": "sigmoid",
            "correlation_type": "pearson"
        }
plt.figure(figsize=(8,5))


"""
Data from Paper
"""
# Actual proteasome correlations
proteasome_corr = pd.read_csv("../data/TPP_proteasome_correlations.csv")

# Filtering for PSMA1 PSMA2 interactions
psma1 = proteasome_corr[proteasome_corr["bait"] == "PSMA1"]

unique_prey = psma1["prey"].unique().tolist()
NUM_PREY = len(unique_prey)


for i in range(NUM_PREY):
    psma1_prey = psma1[psma1["prey"] == unique_prey[i]]
    psma1_prey.reset_index(inplace=True, drop=True)

    plt.scatter(psma1_prey["t"], psma1_prey["corr"])

plt.savefig("../figures/all_psma1_correlations.png")


"""
Simulator Data Generation
"""
phases = ["earlyS.median", "lateS.median", "S_G2.median", "M.median", "G1.median", "asynch.median"]
corr_generated_data = []

plt.figure(figsize=(8,5))

for i in range(100):
    sim = simulator.Simulator(**kwargs)
    sim.set_timepoints([0,1,1,0,0,0])
    sim.generate_data()
    corr = sim.calculate_correlations()
    corr = np.array(corr)
    corr = (corr + 1).reshape(1,-1)
    normalized_values = preprocessing.normalize(corr)
    plt.scatter(phases, normalized_values)


plt.title("Simulation - Generated Data")
plt.savefig("../figures/simulation_generated_data.png")


"""
Simulator Data Sampling - Correlations
"""
corr_data = []
phases = ["earlyS.median", "lateS.median", "S_G2.median", "M.median", "G1.median", "asynch.median"]

for _ in range(100):
    corr_data.append(sim.sample_correlations())

corr_df = pd.DataFrame(corr_data)

plt.figure(figsize=(8,5))

for i in range(100):
    plt.scatter(phases, corr_df.iloc[i])

plt.title("Simulation - Sampling Correlations")
plt.savefig("../figures/simulation_sampling_correlations.png")



"""
Simulator Data Sampling - Distances
"""
distance_data = []
phases = ["earlyS.median", "lateS.median", "S_G2.median", "M.median", "G1.median", "asynch.median"]

for _ in range(100):
    distance_data.append(sim.sample_distances())

distance_df = pd.DataFrame(distance_data)

plt.figure(figsize=(8,5))

for i in range(100):
    plt.scatter(phases, distance_df.iloc[i])

plt.title("Simulation - Sampling Correlations")
plt.savefig("../figures/simulation_sampling_distances.png")