# import simulator
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# from scipy.interpolate import make_interp_spline, BSpline

sample_data = pd.read_csv("/Users/darvesh/protein-hmm/data/TPP_sampleData_filtered.csv")

cols = ["gene_name", "G1_S", "lateS", "M", "G1", "lateS", "asynch"]
abundance = pd.DataFrame(columns=cols)
stability = pd.DataFrame(columns=cols)

def calculate_abundance(fc_37, fc_40):
    return (np.log(fc_37) + np.log(fc_40))/2
    
def calculate_stability(fc, abundance):
    stability = 0
    for i in range(len(fc)):
        stability += (np.log(fc[i]) - abundance)
    
    return stability


def populate_abundance_stability(data, phase_names, abundance_df, stability_df):
    unique_gene_names = data["gene_name"].unique().tolist()

    for name in unique_gene_names:
        gene = sample_data[sample_data["gene_name"] == name].dropna()
        abundance = {"gene_name": [gene]}
        stability = {"gene_name": [gene]}

        for phase in phase_names:
            abundance[phase] = [calculate_abundance(gene[phase][0], gene[phase][1])]
            stability[phase] = [calculate_stability(gene[phase], abundance[phase][0])]

        abundance.head()

        pd.concat([abundance_df, abundance], ignore_index=True, axis=0)
        pd.concat([stability_df, stability], ignore_index=True, axis=0)
        
    return abundance_df, stability_df

test_data = sample_data[0:6]
phase_names = ["G1_S.median", "lateS.median", "M.median", "G1.median", "lateS.median", "asynch.median"]

ab, stab = populate_abundance_stability(data=test_data, phase_names=phase_names, abundance_df=abundance, stability_df=stability)