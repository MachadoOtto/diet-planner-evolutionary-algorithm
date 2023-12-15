# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import numpy as np
import re
import argparse
from scipy import stats

# Execute the Anderson-Darling Test
def execute_anderson_darling_test(name, data):
    print(f"[INFO] Test for {name} Objective")

    result_test = stats.anderson(data, dist='norm')

    print("Anderson-Darling Statistic:", result_test.statistic)
    output_text = f"Anderson-Darling Test for {name} Objective\n"

    for i in range(len(result_test.critical_values)):
        sl, cv = result_test.significance_level[i], result_test.critical_values[i]
        if result_test.statistic < result_test.critical_values[i]:
            print(f"Level of significance: {sl}% - Critical value: {cv} - The data seems to be normal")
            output_text += f"Level of significance: {sl}% - Critical value: {cv} - The data seems to be normal\n"
        else:
            print(f"Level of significance: {sl}% - Critical value: {cv} - The data does not seem to be normal")
            output_text += f"Level of significance: {sl}% - Critical value: {cv} - The data does not seem to be normal\n"

    return output_text

# Load the results from the file
def load_results_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    match_fitness = re.search(r'All fitness: (\[.*?\])', content)
    match_variety = re.search(r'All variety: (\[.*?\])', content)

    all_fitness = eval(match_fitness.group(1)) if match_fitness else None
    all_variety = eval(match_variety.group(1)) if match_variety else None

    return all_fitness, all_variety

# Main function
def main(proyect_name, ae_quantity):
    total_fitness = []
    total_variety = []

    for i in range(ae_quantity):
        # Load the results from the file
        all_fitness, all_variety = load_results_from_file(f'./output/{proyect_name}/output_AE_{i+1}.txt')

        total_fitness.extend(all_fitness)
        total_variety.extend(all_variety)

    # Execute the Anderson-Darling Test
    output_text = execute_anderson_darling_test('Fitness', total_fitness)
    with open(f'output/{proyect_name}/output_anderson_darling_test.txt', 'w') as f:
        f.write(output_text)
        f.write('\n')
    print()
    output_text = execute_anderson_darling_test('Variety', total_variety)
    with open(f'output/{proyect_name}/output_anderson_darling_test.txt', 'a') as f:
        f.write(output_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diet Problem - Anderson-Darling Test')
    parser.add_argument('proyect_name', type=str, help='Name of the proyect')
    parser.add_argument('ae_quantity', type=int, help='Quantity of AEs')

    args = parser.parse_args()

    main(args.proyect_name, args.ae_quantity)