# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import argparse
import os
import time
import logging
import warnings
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from src.models.Args import Args
from src.models.Config import Config
from src.models.CrossoverCustom import SimplePointCrossover, ColumnCrossover, RowCrossover
from src.models.DietProblem import DietProblem
from src.models.Result import Result
from src.utils.utils import print_title, read_algorithm_config, generate_food_array, get_cross_name
# JMetal imports
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import BestSolutionSelection
from jmetal.operator import IntegerPolynomialMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.solution import get_non_dominated_solutions
from pymoo.indicators.hv import HV

# Select the crossover operator
def select_crossover(params, algorithm_config, problem):
    match params.crossover_type:
        case 'spx':
            crossover = SimplePointCrossover(probability = params.crossover_probability, probabilityColumn = algorithm_config.probability_column)
        case 'column':
            crossover = ColumnCrossover(probability = params.crossover_probability, probabilityColumn = algorithm_config.probability_column,
                number_of_columns = problem.number_of_meals, number_of_rows = problem.number_of_days,
                number_of_instances = problem.max_portions)
        case 'row':
            crossover = RowCrossover(probability = params.crossover_probability, probabilityColumn = algorithm_config.probability_column,
                number_of_columns = problem.number_of_meals, number_of_rows = problem.number_of_days,
                number_of_instances = problem.max_portions)
        case _:
            crossover = SimplePointCrossover(probability = params.crossover_probability, probabilityColumn = algorithm_config.probability_column)
    return crossover

# Execute the algorithm
def execute_algorithm(params, food_array, food_ids, model_config, algorithm_config):
    problem = DietProblem(
        number_of_days = model_config.number_of_days,
        number_of_meals = model_config.number_of_meals,
        max_portions = model_config.max_portions,
        food_ids = food_ids,
        food_objects = food_array,
        config = model_config
    )

    crossover = select_crossover(params, algorithm_config, problem)
    
    algorithm = NSGAII(
        problem = problem,
        population_size = algorithm_config.population_size,
        offspring_population_size = algorithm_config.offspring_population_size,
        mutation = IntegerPolynomialMutation(probability = params.mutation_probability),
        crossover = crossover,
        selection = BestSolutionSelection(),
        termination_criterion = StoppingByEvaluations(max_evaluations = algorithm_config.max_evaluations)
    )
    
    # Start time
    start_time = time.time()

    algorithm.run()

    # End time
    end_time = time.time()

    exec_time = end_time - start_time
    
    result = algorithm.get_result()
    front = get_non_dominated_solutions(result)

    return front, exec_time

def test_nsagii(args: Args, ae, instance, proyect_name):
    # Load the model and algorithm configurations
    model_config = Config(f'config\config_instance_{instance}.ini', 'model')
    algorithm_config = Config(f'config\config_instance_{instance}.ini', 'algorithm')

    crossover_name = get_cross_name(args.crossover_type)

    print(f"[INFO] Executing AE {ae}...")
    print(f"[AE {ae}] Crossover type: {crossover_name}")
    print(f"[AE {ae}] Crossover probability: {args.crossover_probability}")
    print(f"[AE {ae}] Mutation probability: {args.mutation_probability}")

    # Load the food array
    food_array = generate_food_array('data/foods.csv')
    food_ids = [food['id'] for food in food_array]

    # Initialize the variables
    f1_objective = []
    f2_objective = []
    execution_times = []
    fronts = []
    first_solution = []

    # Execute the algorithm
    for i in range(algorithm_config.executions):
        front, exec_time = execute_algorithm(args, food_array, food_ids, model_config, algorithm_config)
        f1_objective.extend([s.objectives[0] for s in front])
        f2_objective.extend([s.objectives[1] for s in front])
        execution_times.append(exec_time)
        if i == 0:
            first_solution = front[0].variables

        pareto_front = np.array([[s.objectives[0], s.objectives[1]] for s in front])
        fronts.append(pareto_front)

    # Calculating the statistics for the f1_objective
    median1 = np.median(f1_objective)
    max1 = np.max(f1_objective)
    min1 = np.min(f1_objective)
    std_dev1 = np.std(f1_objective)

    # Calculating the statistics for the f2_objective
    median2 = np.median(f2_objective)
    max2 = np.max(f2_objective)
    min2 = np.min(f2_objective)
    std_dev2 = np.std(f2_objective)

    # Calculating the statistics for the execution times
    median3 = np.median(execution_times)
    max3 = np.max(execution_times)
    min3 = np.min(execution_times)
    std_dev3 = np.std(execution_times)

    result = Result([min1, median1, max1, std_dev1], [min2, median2, max2, std_dev2], [min3, median3, max3, std_dev3])

    # A .txt file with the results for f1_objective, f2_objective and execution times
    with open(f'output/{proyect_name}/output_AE_{ae}.txt', 'w') as f:
            f.write(f"""NSGA-II - Instance {instance} - AE {ae} - {crossover_name}            
f1 objective:
    Median: {median1}
    Max: {max1}
    Min: {min1}
    Std. Dev.: {std_dev1}
                    
f2 objective:
    Median: {median2}
    Max: {max2}
    Min: {min2}
    Std. Dev.: {std_dev2}

Execution times:
    Median: {median3}
    Max: {max3}
    Min: {min3}
    Std. Dev.: {std_dev3}            
    
Algorithm data:
    Algorithm: NSGA-II
    Executions: {algorithm_config.executions}
    Population size: {algorithm_config.population_size}
    Offspring population size: {algorithm_config.offspring_population_size}
    Mutation probability: {args.mutation_probability}
    Crossover probability: {args.crossover_probability}
    Crossover type: {crossover_name}
    Probability of parent: {algorithm_config.probability_column}
    Number of evaluations: {algorithm_config.max_evaluations}
    Execution time: {exec_time}
                    
Problem data:
    Number of days: {model_config.number_of_days}
    Number of meals: {model_config.number_of_meals}
    Max portions: {model_config.max_portions}
                    
Model objective:
    Calories: {model_config.kc}
    Protein: {model_config.p}
    Carbs: {model_config.hc}
    Fat: {model_config.g}
                    
Model Hiperparameters:
    Alpha: {model_config.alpha}
    Beta: {model_config.beta}
    Gamma: {model_config.gamma}
    Delta: {model_config.delta}
    Sigma: {model_config.sigma}
                    
All f1: {f1_objective}
All f2: {f2_objective}
All execution times: {execution_times}
All pareto fronts: {fronts}

First front solutions: {first_solution}""")

    plt.figure()
    plt.scatter(f1_objective, f2_objective, s=1)
    plt.title(f'NSGA-II - Pareto Optimals - AE {ae} - Instance {instance} - {crossover_name}')
    plt.xlabel('f1')
    plt.ylabel('f2')
    plt.savefig(f"output/{proyect_name}/optimals_AE_{ae}.png")
    
    return result, max1, max2, fronts

def main_all(instance, proyect_name):
    print_title()
    print(f"[INFO] Instance selected: {instance}")
    print(f"[INFO] Output folder: ./output/{proyect_name}")

    # Disable the warnings of JMetal
    logging.getLogger('jmetal').setLevel(logging.WARNING)
    warnings.filterwarnings("ignore")

    # Parse the arguments
    config = read_algorithm_config()
    print(f"[INFO] Executing {len(config)} AEs of NSGA-II")

    # Create blank .csv file
    with open(f'output/{proyect_name}/output_instance_{instance}.csv', 'w') as f:
        f.write('ae,crossover_type,crossover_probability,mutation_probability,f1_min,f1_mean,f1_max,f1_sd,f2_min,f2_mean,f2_max,f2_sd,execution_time_min,execution_time_mean,execution_time_max,execution_time_sd\n')

    with open(f'output/{proyect_name}/output_hypervolume_instance_{instance}.csv', 'w') as f:
        f.write('ae,crossover_type,crossover_probability,mutation_probability,hv_min,hv_mean,hv_max,hv_sd\n')

    box_hypervolumes = []
    f1_max = 0
    f2_max = 0
    exec_fronts = []

    for i in range(len(config)):
        args = Args(config[i].get('crossover_type'), config[i].get('crossover_probability'), config[i].get('mutation_probability'))
        
        result, max1, max2, fronts = test_nsagii(args, i + 1, instance, proyect_name)

        # Append the results to the .csv file
        with open(f'output/{proyect_name}/output_instance_{instance}.csv', 'a') as f:
           f.write(f"{i + 1},{args.crossover_type},{args.crossover_probability},{args.mutation_probability},{result.f1_objective[0]},{result.f1_objective[1]},{result.f1_objective[2]},{result.f1_objective[3]},{result.f2_objective[0]},{result.f2_objective[1]},{result.f2_objective[2]},{result.f2_objective[3]},{result.execution_times[0]},{result.execution_times[1]},{result.execution_times[2]},{result.execution_times[3]}\n")

        f1_max = max1 if max1 > f1_max else f1_max
        f2_max = max2 if max2 > f2_max else f2_max
        exec_fronts.append(fronts)

    # Calculate the hypervolumes
    ref_point = np.array([f1_max * 1.1, f2_max * 1.1])

    for i in range(len(config)):
        hypervolumes = []

        for j in range(len(exec_fronts[i])):
            # Calculate the hypervolume of the pareto front
            hypervolume = HV(ref_point=ref_point)
            hv_value = hypervolume(exec_fronts[i][j])
            hypervolumes.append(hv_value)

        # Calculate the statistics for the hypervolumes
        median_hv = np.median(hypervolumes)
        max_hv = np.max(hypervolumes)
        min_hv = np.min(hypervolumes)
        std_dev_hv = np.std(hypervolumes)

        # Append the results to the .csv file
        with open(f'output/{proyect_name}/output_hypervolume_instance_{instance}.csv', 'a') as f:
            f.write(f"{i + 1},{config[i].get('crossover_type')},{config[i].get('crossover_probability')},{config[i].get('mutation_probability')},{min_hv},{median_hv},{max_hv},{std_dev_hv}\n")
        
        box_hypervolumes.append(hypervolumes)

    # Plot the boxplot of the hypervolumes
    plt.boxplot(box_hypervolumes)
    plt.title(f'Hypervolumes - NSGA-II - Instance {instance}')
    plt.ylabel('Hypervolume')
    plt.xlabel('AE')
    plt.show()

    print("[INFO] All instances executed!")

# Execute the algorithm for a single AE
def main_ae(instance, proyect_name, ae):
    print_title()
    print(f"[INFO] Instance selected: {instance}")
    print(f"[INFO] AE selected: {ae}")
    print(f"[INFO] Output folder: ./output/{proyect_name}")

    # Disable the warnings of JMetal
    logging.getLogger('jmetal').setLevel(logging.WARNING)
    warnings.filterwarnings("ignore")

    # Parse the arguments
    config = read_algorithm_config()
    print(f"[INFO] Executing AE-{ae} of NSGA-II")

    # Create blank .csv file
    with open(f'output/{proyect_name}/output_instance_{instance}_ae_{ae}.csv', 'w') as f:
        f.write('ae,crossover_type,crossover_probability,mutation_probability,f1_min,f1_mean,f1_max,f1_sd,f2_min,f2_mean,f2_max,f2_sd,execution_time_min,execution_time_mean,execution_time_max,execution_time_sd\n')

    with open(f'output/{proyect_name}/output_hypervolume_instance_{instance}_ae_{ae}.csv', 'w') as f:
        f.write('ae,crossover_type,crossover_probability,mutation_probability,hv_min,hv_mean,hv_max,hv_sd\n')

    box_hypervolumes = []
    f1_max = 0
    f2_max = 0
    
    args = Args(config[ae - 1].get('crossover_type'), config[ae - 1].get('crossover_probability'), config[ae - 1].get('mutation_probability'))
        
    result, max1, max2, fronts = test_nsagii(args, ae, instance, proyect_name)

    # Append the results to the .csv file
    with open(f'output/{proyect_name}/output_instance_{instance}_ae_{ae}.csv', 'a') as f:
        f.write(f"{ae},{args.crossover_type},{args.crossover_probability},{args.mutation_probability},{result.f1_objective[0]},{result.f1_objective[1]},{result.f1_objective[2]},{result.f1_objective[3]},{result.f2_objective[0]},{result.f2_objective[1]},{result.f2_objective[2]},{result.f2_objective[3]},{result.execution_times[0]},{result.execution_times[1]},{result.execution_times[2]},{result.execution_times[3]}\n")

    f1_max = max1 if max1 > f1_max else f1_max
    f2_max = max2 if max2 > f2_max else f2_max
    
    # Calculate the hypervolumes
    ref_point = np.array([1184 * 1.1, 230 * 1.1])

    hypervolumes = []

    for j in range(len(fronts)):
        # Calculate the hypervolume of the pareto front
        hypervolume = HV(ref_point=ref_point)
        hv_value = hypervolume(fronts[j])
        hypervolumes.append(hv_value)

    # Calculate the statistics for the hypervolumes
    median_hv = np.median(hypervolumes)
    max_hv = np.max(hypervolumes)
    min_hv = np.min(hypervolumes)
    std_dev_hv = np.std(hypervolumes)

    # Append the results to the .csv file
    with open(f'output/{proyect_name}/output_hypervolume_instance_{instance}_ae_{ae}.csv', 'a') as f:
        f.write(f"{ae},{config[ae - 1].get('crossover_type')},{config[ae - 1].get('crossover_probability')},{config[ae - 1].get('mutation_probability')},{min_hv},{median_hv},{max_hv},{std_dev_hv}\n")
        
    box_hypervolumes.append(hypervolumes)

    # Plot the boxplot of the hypervolumes
    plt.boxplot(box_hypervolumes)
    plt.title(f'Hypervolumes - NSGA-II - Instance {instance}')
    plt.ylabel('Hypervolume')
    plt.xlabel('AE')
    plt.show()

    print("[INFO] All instances executed!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Diet Problem - NSGA-II')
    parser.add_argument('instance', type=str, choices=['1', '2', '1E', '2E'], help='Instance to execute')
    parser.add_argument('proyect_name', type=str, help='Name of the proyect')
    parser.add_argument('--ae', type=int, default=0, help='Number of the AE to execute, 0 for all')
    args = parser.parse_args()

    # Create proyect folder inside 'output' folder, if an error occurs, exit 
    try:
        os.mkdir(f'output/{args.proyect_name}')
    except:
        print(f"[ERROR] An error ocurred while creating the proyect folder")
        exit()

    if args.ae == 0:
        main_all(args.instance, args.proyect_name)
    else:
        main_ae(args.instance, args.proyect_name, args.ae)