# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import argparse
import re
from scipy.stats import mannwhitneyu

def execute_mann_witney_test(data1, data2):
    stat, p = mannwhitneyu(data1, data2)

    print('stat=%.3f, p=%.3f' % (stat, p))
    output_text = f'stat={stat}, p={p}\n'

    if p > 0.05:
        print('Probably the same distribution')
        output_text += 'Probably the same distribution\n'
    else:
        print('Probably different distributions')
        output_text += 'Probably different distributions\n'
    
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
def main(instance1_name, instance2_name, ae_quantity):
    with open(f'output/output_mann_witney_test_{instance1_name}_{instance2_name}.txt', 'w') as f:
        f.write(f"Mann-Witney Test for {instance1_name} and {instance2_name} Instances\n\n")

    for i in range(ae_quantity):
        print(f"[INFO] Test for AE {i+1}")
        with open(f'output/output_mann_witney_test_{instance1_name}_{instance2_name}.txt', 'a') as f:
            f.write(f"AE {i+1}\n")

        # Load the results from the file
        fitness_1, variety_1 = load_results_from_file(f'./output/{instance1_name}/output_AE_{i+1}.txt')
        fitness_2, variety_2 = load_results_from_file(f'./output/{instance2_name}/output_AE_{i+1}.txt')

        print("# Fitness")
        output_text = execute_mann_witney_test(fitness_1, fitness_2)
        with open(f'output/output_mann_witney_test_{instance1_name}_{instance2_name}.txt', 'a') as f:
            f.write('# Fitness\n')
            f.write(output_text)
        
        print("# Variety")
        output_text = execute_mann_witney_test(variety_1, variety_2)
        with open(f'output/output_mann_witney_test_{instance1_name}_{instance2_name}.txt', 'a') as f:
            f.write('# Variety\n')
            f.write(output_text)
            f.write('\n')
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Diet Problem - Mann-Witney Test')
    parser.add_argument('instance1_name', type=str, help='Instance 1 name')
    parser.add_argument('instance2_name', type=str, help='Instance 2 name')
    parser.add_argument('ae_quantity', type=int, help='Quantity of AEs')

    args = parser.parse_args()

    main(args.instance1_name, args.instance2_name, args.ae_quantity)