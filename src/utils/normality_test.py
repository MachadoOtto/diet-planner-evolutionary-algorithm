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

# Execute the Anderson-Darling Test
def execute_anderson_darling_test(name, data):
    print(f"[INFO] Anderson-Darling Test for {name} Objective")

    result_test = stats.anderson(data, dist='norm')
    is_significate = []

    print("Anderson-Darling Statistic:", result_test.statistic)
    
    for i in range(len(result_test.critical_values)):
        sl, cv = result_test.significance_level[i], result_test.critical_values[i]
    
        if result_test.statistic < result_test.critical_values[i]:
            print(f"Level of significance: {sl}% - Critical value: {cv} - The data seems to be normal")
            is_significate.append(True)

        else:
            print(f"Level of significance: {sl}% - Critical value: {cv} - The data does not seem to be normal")
            is_significate.append(False)

    return is_significate, result_test.statistic, result_test.critical_values, result_test.significance_level

# Execute the Shapiro-Wilk Test
def execute_shapiro_wilk_test(name, data):
    print(f"[INFO] Shapiro-Wilk Normality Test for {name} Objective")

    stat, p = stats.shapiro(data)

    print('stat=%.3f, p=%.3f' % (stat, p))

    if p > 0.05:
        print('Normal distribution')
        return True, stat, p
    else:
        print('Not normal distribution')
        return False, stat, p

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
    print(f"[INFO] Executing {ae_quantity} normality tests for {proyect_name}...")

    # Create result .csv file
    with open(f'output/{proyect_name}/output_anderson_test.txt', 'w') as f:
        f.write(f"ae,crossover_type,crossover_probability,mutation_probability,anderson_is_normal,anderson_statistic,anderson_critical,anderson_significance\n")

    with open(f'output/{proyect_name}/output_shapiro_test.txt', 'w') as f:
        f.write(f"ae,crossover_type,crossover_probability,mutation_probability,shapiro_wilk_is_normal,shapiro_wilk_statistic,shapiro_wilk_p_value\n")

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

        # Execute the Anderson-Darling Test
        anderson_is_normal, anderson_stat, anderson_critical, anderson_significance = execute_anderson_darling_test(f'Hypervolume - AE {i+1}', hypervolumes)

        # Write the results in the .csv file
        with open(f'output/{proyect_name}/output_anderson_test.txt', 'a') as f:
            f.write(f"{i+1},{config[i]['crossover_type']},{config[i]['crossover_probability']},{config[i]['mutation_probability']},{anderson_is_normal},{anderson_stat},{anderson_critical},{anderson_significance}\n")

        # Execute the Shapiro-Wilk Test
        shapiro_is_normal, shapiro_stat, shapiro_p_value = execute_shapiro_wilk_test(f'Hypervolume - AE {i+1}', hypervolumes)

        # Write the results in the .csv file
        with open(f'output/{proyect_name}/output_shapiro_test.txt', 'a') as f:
            f.write(f"{i+1},{config[i]['crossover_type']},{config[i]['crossover_probability']},{config[i]['mutation_probability']},{shapiro_is_normal},{shapiro_stat},{shapiro_p_value}\n")
            
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diet Problem - Normality Test')
    parser.add_argument('proyect_name', type=str, help='Name of the proyect')

    args = parser.parse_args()

    main(args.proyect_name)