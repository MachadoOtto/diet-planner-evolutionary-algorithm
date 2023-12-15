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

# Execute the Anderson-Darling Test
def execute_anderson_darling_test(name, data):
    print(f"[INFO] Anderson-Darling Test for {name} Objective")

    result_test = stats.anderson(data, dist='norm')
    sl_values = []
    is_normal = False

    print("Anderson-Darling Statistic:", result_test.statistic)
    
    for i in range(len(result_test.critical_values)):
        sl, cv = result_test.significance_level[i], result_test.critical_values[i]
    
        if result_test.statistic < result_test.critical_values[i]:
            print(f"Level of significance: {sl}% - Critical value: {cv} - The data seems to be normal")
            is_normal = True
            sl_values.append(sl)

        else:
            print(f"Level of significance: {sl}% - Critical value: {cv} - The data does not seem to be normal")
            is_normal = False

    return is_normal, sl_values

# Execute the Shapiro-Wilk Test
def execute_shapiro_wilk_test(name, data):
    print(f"[INFO] Shapiro-Wilk Test for {name} Objective")

    stat, p = stats.shapiro(data)

    print('stat=%.3f, p=%.3f' % (stat, p))

    if p > 0.05:
        print('Probably the same distribution')
        return True, p
    else:
        print('Probably different distributions')
        return False, p

# Load the results from the file
def load_results_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract from NSGA-II - Instancia 22 - AE 12 - Column Crossover
    match_fitness = re.search(r'All fitness: (\[.*?\])', content)
    match_variety = re.search(r'All variety: (\[.*?\])', content)

    all_fitness = eval(match_fitness.group(1)) if match_fitness else None
    all_variety = eval(match_variety.group(1)) if match_variety else None

    return all_fitness, all_variety

# Main function
def main(proyect_name):
    config = read_algorithm_config()
    ae_quantity = len(config)
    print(f"[INFO] Executing {ae_quantity} normality tests for {proyect_name}...")

    # Create result .csv file
    with open(f'output/{proyect_name}/output_normality_test.txt', 'w') as f:
        f.write(f"ae,crossover_type,crossover_probability,mutation_probability,fitness_anderon_darling_test,fitness_anderson_darling_sl_values,variety_anderson_darling_test,variety_anderson_darling_sl_values,fitness_shapiro_wilk_test,fitness_shapiro_wilk_p_value,variety_shapiro_wilk_test,variety_shapiro_wilk_p_value\n")

    for i in range(ae_quantity):
        # Load the results from the file
        all_fitness, all_variety = load_results_from_file(f'./output/{proyect_name}/output_AE_{i+1}.txt')

        # Execute the Anderson-Darling Test
        fitness_is_normal, fitness_p_value = execute_anderson_darling_test('Fitness', all_fitness)
        variety_is_normal, variety_p_value = execute_anderson_darling_test('Variety', all_variety)

        # Execute the Shapiro-Wilk Test
        fitness_is_normal_2, fitness_p_value_2 = execute_shapiro_wilk_test('Fitness', all_fitness)
        variety_is_normal_2, variety_p_value_2 = execute_shapiro_wilk_test('Variety', all_variety)

        # Write the results in the .csv file
        with open(f'output/{proyect_name}/output_normality_test.txt', 'a') as f:
            f.write(f"{i+1},{config[i]['crossover_type']},{config[i]['crossover_probability']},{config[i]['mutation_probability']},{fitness_is_normal},{fitness_p_value},{variety_is_normal},{variety_p_value},{fitness_is_normal_2},{fitness_p_value_2},{variety_is_normal_2},{variety_p_value_2}\n")
            
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diet Problem - Normality Test')
    parser.add_argument('proyect_name', type=str, help='Name of the proyect')

    args = parser.parse_args()

    main(args.proyect_name)