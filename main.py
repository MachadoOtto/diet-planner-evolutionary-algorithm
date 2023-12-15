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
    fitness_objective = []
    variety_objective = []
    execution_times = []

    # Execute the algorithm
    for i in range(algorithm_config.executions):
        front, exec_time = execute_algorithm(args, food_array, food_ids, model_config, algorithm_config)
        fitness_objective.extend([s.objectives[0] for s in front])
        variety_objective.extend([s.objectives[1] for s in front])
        execution_times.append(exec_time)
    
    # Calculating the statistics for the fitness_objective
    median1 = np.median(fitness_objective)
    max1 = np.max(fitness_objective)
    min1 = np.min(fitness_objective)
    std_dev1 = np.std(fitness_objective)

    # Calculating the statistics for the variety_objective
    median2 = np.median(variety_objective)
    max2 = np.max(variety_objective)
    min2 = np.min(variety_objective)
    std_dev2 = np.std(variety_objective)

    # Calculating the statistics for the execution times
    median3 = np.median(execution_times)
    max3 = np.max(execution_times)
    min3 = np.min(execution_times)
    std_dev3 = np.std(execution_times)

    result = Result([min1, median1, max1, std_dev1], [min2, median2, max2, std_dev2], [min3, median3, max3, std_dev3])

    # A .txt file with the results for fitness_objective, variety_objective and execution times
    with open(f'output/{proyect_name}/output_AE_{ae}.txt', 'w') as f:
            f.write(f"""NSGA-II - Instance {instance} - AE {ae} - {crossover_name}            
Fitness objective:
    Median: {median1}
    Max: {max1}
    Min: {min1}
    Std. Dev.: {std_dev1}
                    
Variety objective:
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
                    
All fitness: {fitness_objective}
All variety: {variety_objective}
All execution times: {execution_times}""")

    plt.figure()
    plt.scatter(fitness_objective, variety_objective, s=1)
    plt.title(f'NSGA-II - Pareto Optimals - AE {ae} - Instance {instance} - {crossover_name}')
    plt.xlabel('Fitness')
    plt.ylabel('Variety')
    plt.savefig(f"output/{instance}/optimals_AE_{ae}.png")
    
    return result

def main(instance, proyect_name):
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
        f.write('ae,crossover_type,crossover_probability,mutation_probability,fitness_min,fitness_mean,fitness_max,fitness_sd,variety_min,variety_mean,variety_max,variety_sd,execution_time_min,execution_time_mean,execution_time_max,execution_time_sd\n')


    for i in range(len(config)):
        args = Args(config[i].get('crossover_type'), config[i].get('crossover_probability'), config[i].get('mutation_probability'))
        
        result = test_nsagii(args, i + 1, instance, proyect_name)

        # Append the results to the .csv file
        with open(f'output/{proyect_name}/output_instance_{instance}.csv', 'a') as f:
           f.write(f"{i + 1},{args.crossover_type},{args.crossover_probability},{args.mutation_probability},{result.fitness_objective[0]},{result.fitness_objective[1]},{result.fitness_objective[2]},{result.fitness_objective[3]},{result.variety_objective[0]},{result.variety_objective[1]},{result.variety_objective[2]},{result.variety_objective[3]},{result.execution_times[0]},{result.execution_times[1]},{result.execution_times[2]},{result.execution_times[3]}\n")

    print("[INFO] All instances executed!")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Diet Problem - NSGA-II')
    parser.add_argument('instance', type=int, choices=[1, 2], help='Instance to execute')
    parser.add_argument('proyect_name', type=str, help='Name of the proyect')
    args = parser.parse_args()

    # Create proyect folder inside 'output' folder, if an error occurs, exit 
    try:
        os.mkdir(f'output/{args.proyect_name}')
    except:
        print(f"[ERROR] An error ocurred while creating the proyect folder")
        exit()

    main(args.instance, args.proyect_name)