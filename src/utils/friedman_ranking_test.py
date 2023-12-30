# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import numpy as np
import re
import argparse
from scipy import stats
from utils import read_algorithm_config
from pymoo.indicators.hv import HV
import pandas as pd

# Execute the Friedman Test
def execute_friedman_test(name, data):
    print(f"[INFO] Friedman Test for {name} Objective")

    # Calculate the Friedman statistic
    chi2, p_value = stats.friedmanchisquare(*data)

    # Determine the significance
    alpha = 0.05
    if p_value < alpha:
        print("There are statistically significant differences between at least two configurations.")
    else:
        print("There is not enough evidence to reject the null hypothesis.")
    return chi2, p_value

# Load the results from the file
def load_results_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    match_pareto = re.search(r'All pareto fronts:(.|\s)*', content)

    string = match_pareto.group(0)
    string = string.replace('All pareto fronts:', '')
    string = string.replace('array', '')

    paretos = eval(string)

    return paretos

# Main function
def main(proyect_name):
    config = read_algorithm_config()
    ae_quantity = len(config)
    print(f"[INFO] Executing Friedman Tests for {proyect_name}...")

    ae_hypervolumes = []

    for i in range(ae_quantity):
        # Load the results from the file
        paretos = load_results_from_file(f'./output/{proyect_name}/output_AE_{i+1}.txt')

        max_f1 = 0
        max_f2 = 0

        for j in range(len(paretos)):
            f1_m = max(sublist[0] for sublist in paretos[j])
            f2_m = max(sublist[1] for sublist in paretos[j])

            max_f1 = f1_m if f1_m > max_f1 else max_f1
            max_f2 = f2_m if f2_m > max_f2 else max_f2
            
        ref_point = np.array([max_f1 * 1.1, max_f2 * 1.1])
        hypervolumes = []

        for j in range(len(paretos)):
            # Calculate the hypervolume of the pareto front
            hypervolume = HV(ref_point=ref_point)
            hv_value = hypervolume(np.array(paretos[j]))
            hypervolumes.append(hv_value)

        ae_hypervolumes.append(hypervolumes)

    # Execute the Friedman Test For All Hypervolumes
    friedman_stat, friedman_p_value = execute_friedman_test(f'Hypervolumes', ae_hypervolumes)
    print(f"Friedman Statistic: {friedman_stat}")
    print(f"p-value: {friedman_p_value}\n")

    # Execute the Ranking
    print(f"[INFO] Ranking for {proyect_name}...")

    df = pd.read_csv(f'output/{proyect_name}/output_hypervolume_{proyect_name}.csv')

    hv_means = df['hv_mean'].to_numpy()
    hv_sd = df['hv_sd'].to_numpy()

    hv_means -= hv_sd / 2
    hv_means_norm = (hv_means - np.mean(hv_means)) / np.std(hv_means)

    # Ranking
    ranking = len(hv_means_norm) - stats.rankdata(hv_means_norm) + 1

    with open(f'output/{proyect_name}/output_friedman_test_ranking.txt', 'w') as f:
        f.write(f"Friedman Test and Ranking for {proyect_name}\n")
        f.write(f"Friedman Statistic: {friedman_stat}\n")
        f.write(f"p-value: {friedman_p_value}\n")
        f.write(f"Ranks: {ranking}\n")
    print(f"Ranks: {ranking}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diet Problem - Friedman Ranking Test')
    parser.add_argument('proyect_name', type=str, help='Name of the proyect')

    args = parser.parse_args()

    main(args.proyect_name)