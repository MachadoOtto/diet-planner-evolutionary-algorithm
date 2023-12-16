# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import numpy as np
import re
import argparse
from scipy import stats
from pprint import pprint
import pandas as pd
from utils import read_algorithm_config
from decimal import *

def load_fitness(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract All fitness
    match_fitness = re.search(r'All fitness: (\[.*?\])', content)

    all_fitness = eval(match_fitness.group(1)) if match_fitness else None

    return all_fitness

def execute_anova(instance_name_1, instance_name_2):
    config = read_algorithm_config()
    ae_quantity = len(config)

    groups = []

    # Load all fitness
    for i in range(ae_quantity):
        # Load the results from the file
        all_fitness = load_fitness(f'./output/{instance_name_1}/output_AE_{i+1}.txt')
        all_fitness += load_fitness(f'./output/{instance_name_2}/output_AE_{i+1}.txt')
        groups.append(all_fitness)

    # Initialize matrix to store results
    results = np.zeros((ae_quantity, ae_quantity, 1))

    # For each pair of groups
    for i in range(ae_quantity):
        for j in range(ae_quantity):
            # Perform ANOVA
            f_val, p_val = stats.f_oneway(groups[i], groups[j])
            
            # Store F value and p value in the matrix
            results[i, j] = p_val # < 0.05

    # Create a dataframe with matrix results and index and columns as the names of the groups
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    for i in range(ae_quantity):
        getcontext().prec = 6
        data = pd.DataFrame(results[i, :, 0])
        print(str(data))
        df2.insert(i, i, data<0.05)
        df.insert(i, i, data)

    df.to_csv(f'./output/anova_test_{instance_name_1}_{instance_name_2}.csv')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ANOVA Test')
    parser.add_argument('instance_name_1', type=str, help='Instance name 1')
    parser.add_argument('instance_name_2', type=str, help='Instance name 2')
    args = parser.parse_args()

    execute_anova(args.instance_name_1, args.instance_name_2)