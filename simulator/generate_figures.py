import simulator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
Data from Paper
"""
# Actual proteasome correlations
proteasome_corr = pd.read_csv("../data/TPP_proteasome_correlations.csv")

# Filtering for PSMA1 PSMA2 interactions
psma1 = proteasome_corr[proteasome_corr["bait"] == "PSMA1"]

unique_prey = psma1["prey"].unique().tolist()
NUM_PREY = len(unique_prey)

plt.figure(figsize=(8,5))

for i in range(NUM_PREY):
    psma1_prey = psma1[psma1["prey"] == unique_prey[i]]
    psma1_prey.reset_index(inplace=True, drop=True)

    plt.scatter(psma1_prey["t"], psma1_prey["corr"])

plt.savefig("../figures/all_psma1_correlations.png")

"""
Simulator vs Real Data
"""