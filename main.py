import argparse
import time
import logging
import warnings
from datetime import datetime
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.algorithm.multiobjective import NSGAII
from jmetal.operator import BestSolutionSelection, RandomSolutionSelection
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator import SPXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.lab.visualization.plotting import Plot
from jmetal.util.solution import get_non_dominated_solutions
from src.models.DietProblem import DietProblem
from src.utils.utils import print_title, generate_food_array, print_solution, print_algorithm_data, print_problem_data, plot_NSGAII
from src.models.Config import Config
from src.models.CrossoverCustom import SimplePointCrossover, ColumnCrossover, RowCrossover
 
def execute_algorithm(args):
    print("## Executing algorithm...")
    food_array = generate_food_array('data/foods.csv')
    food_ids = [food['id'] for food in food_array]

    model_config = Config('config\config.ini', 'model')
    algorithm_config = Config('config\config.ini', 'algorithm')

    problem = DietProblem(
        number_of_days = model_config.number_of_days,
        number_of_meals = model_config.number_of_meals,
        max_portions = model_config.max_portions,
        food_ids = food_ids,
        food_objects = food_array,
        config = model_config
    )

    crossover_name = 'Simple Point Crossover'
    match args.crossover:
        case 'spx':
            crossover = SimplePointCrossover(probability = algorithm_config.crossover_probability, probabilityColumn = algorithm_config.probability_column)
        case 'column':
            crossover = ColumnCrossover(probability = algorithm_config.crossover_probability, probabilityColumn = algorithm_config.probability_column,
                number_of_columns = problem.number_of_meals, number_of_rows = problem.number_of_days,
                number_of_instances = problem.max_portions)
            crossover_name = 'Column Crossover'
        case 'row':
            crossover = RowCrossover(probability = algorithm_config.crossover_probability, probabilityColumn = algorithm_config.probability_column,
                number_of_columns = problem.number_of_meals, number_of_rows = problem.number_of_days,
                number_of_instances = problem.max_portions)
            crossover_name = 'Row Crossover'
        case _:
            crossover = SimplePointCrossover(probability = algorithm_config.crossover_probability, probabilityColumn = algorithm_config.probability_column)

    if args.nsgaii:
        algorithm = NSGAII(
            problem = problem,
            population_size = algorithm_config.population_size,
            offspring_population_size = algorithm_config.offspring_population_size,
            mutation = IntegerPolynomialMutation(probability = algorithm_config.mutation_probability),
            crossover = crossover,
            selection = BestSolutionSelection(),
            termination_criterion = StoppingByEvaluations(max_evaluations = algorithm_config.max_evaluations)
        )
    else:
        algorithm = GeneticAlgorithm(
            problem = problem,
            population_size = algorithm_config.population_size,
            offspring_population_size = algorithm_config.offspring_population_size,
            mutation = IntegerPolynomialMutation(probability = algorithm_config.mutation_probability),
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
    print(f"## Algorithm finished! Execution time: {exec_time}")

    result = algorithm.get_result()

    print("## Parsing results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.nsgaii:
        #print(f"Evaluations: {algorithm.evaluations}")
        #print(f"All fitness: {problem.all_fitness}")
        #print(f"All variety: {problem.all_variety}")

        # Save the results
        with open(f'output/nsgaii/output_{timestamp}.txt', 'w') as f:
            f.write(f"NSGA-II - {crossover_name} - {timestamp}\n\n")
            f.write("## Algorithm data:\n")
            f.write(f"  Algorithm: {algorithm.get_name()}\n")
            f.write(f"  Population size: {algorithm_config.population_size}\n")
            f.write(f"  Offspring population size: {algorithm_config.offspring_population_size}\n")
            f.write(f"  Mutation probability: {algorithm_config.mutation_probability}\n")
            f.write(f"  Crossover probability: {algorithm_config.crossover_probability}\n")
            f.write(f"  Probability column: {algorithm_config.probability_column}\n")
            f.write(f"  Number of evaluations: {algorithm.evaluations}\n")
            f.write(f"  Execution time: {exec_time}\n\n")
            f.write("## Problem data:\n")
            f.write(f"  Number of days: {problem.number_of_days}\n")
            f.write(f"  Number of meals: {problem.number_of_meals}\n")
            f.write(f"  Max portions: {problem.max_portions}\n\n")
            f.write(f"Evaluations: {algorithm.evaluations}\n")
            f.write(f"All fitness: {problem.all_fitness}\n")
            f.write(f"All variety: {problem.all_variety}\n")

        front = get_non_dominated_solutions(result)

        plot_front = Plot(axis_labels=['x', 'y'])
        plot_front.plot(front, label='NSGAII-ZDT1')

        plot_NSGAII(algorithm, problem, timestamp)
    else:
        if args.verbose:
            print_problem_data(problem)
        print_algorithm_data(algorithm, algorithm_config, exec_time, args.verbose)
        print_solution(result, problem, model_config, food_array, args.verbose, args.plot)

    return result, problem

def main():
    print_title()

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="output detailed information about the solutions", action="store_true")
    parser.add_argument("-d", "--debug", help="enable debug mode", action="store_true")
    parser.add_argument("-p", "--plot", help="plot the fitness of the algorithm", action="store_true")
    parser.add_argument("-n", "--nsgaii", help="use NSGAII algorithm", action="store_true")
    parser.add_argument("-c", "--crossover", help="select crossover operator", choices=['spx','column','row'])
    
    args = parser.parse_args()

    if not args.debug:
        logging.getLogger('jmetal').setLevel(logging.WARNING)
        warnings.filterwarnings("ignore")

    execute_algorithm(args)

if __name__ == '__main__':
    main()   
    