# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd

# Obtain from the .csv file the min, mean, max, and std using pandas
df = pd.read_csv('./output/instance_1/output_hypervolume_instance_1.csv')

means = df['hv_mean']
std = df['hv_sd']
whislo = df['hv_min']
whishi = df['hv_max']

q1 = means + std * stats.norm.ppf(0.25)
q3 = means + std * stats.norm.ppf(0.75)

keys = ['med', 'q1', 'q3', 'whislo', 'whishi']
stats = [dict(zip(keys, vals)) for vals in zip(means, q1, q3, whislo, whishi)]
plt.subplot().bxp(stats, showfliers=False)
plt.title('Hypervolumes - Instance 1')
plt.xlabel('AE')
plt.ylabel('Hypervolume')
plt.savefig('./output/instance_1/hypervolumes_instance_1.png')

# Obtain from the .csv file the min, mean, max, and std using pandas
df = pd.read_csv('./output/instance_2/output_hypervolume_instance_2.csv')

means = df['hv_mean']
std = df['hv_sd']
whislo = df['hv_min']
whishi = df['hv_max']

q1 = means + std * stats.norm.ppf(0.25)
q3 = means + std * stats.norm.ppf(0.75)

keys = ['med', 'q1', 'q3', 'whislo', 'whishi']
stats = [dict(zip(keys, vals)) for vals in zip(means, q1, q3, whislo, whishi)]
plt.subplot().bxp(stats, showfliers=False)
plt.title('Hypervolumes - Instance 2')
plt.xlabel('AE')
plt.ylabel('Hypervolume')
plt.savefig('./output/instance_2/hypervolumes_instance_2.png')