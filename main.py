import argparse
import time
import logging
import warnings
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import BestSolutionSelection, RandomSolutionSelection
from jmetal.operator import IntegerPolynomialMutation
#from jmetal.operator import CXCrossover,DifferentialEvolutionCrossover,NullCrossover,PMXCrossover,SBXCrossover,SPXCrossover
from jmetal.util.termination_criterion import StoppingByEvaluations
from src.models.DietProblem import DietProblem
from src.utils.utils import print_title, generate_food_array, print_solution, print_algorithm_data, print_problem_data
from src.models.Config import Config
from src.models.CrossoverCustom import ColumnCrossover, RowCrossover
 
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

    algorithm = GeneticAlgorithm(
        problem = problem,
        population_size = algorithm_config.population_size,
        offspring_population_size = algorithm_config.offspring_population_size,
        mutation=IntegerPolynomialMutation(probability = algorithm_config.mutation_probability),
        crossover=RowCrossover(probability = algorithm_config.crossover_probability, probabilityColumn = algorithm_config.probability_column,
            number_of_columns = problem.number_of_meals, number_of_rows = problem.number_of_days,
            number_of_instances = problem.max_portions),
        selection = RandomSolutionSelection(),
        termination_criterion = StoppingByEvaluations(max_evaluations = algorithm_config.max_evaluations)
    )

    # Start time
    start_time = time.time()

    algorithm.run()

    # End time
    end_time = time.time()

    exec_time = end_time - start_time

    result = algorithm.get_result()

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
    args = parser.parse_args()

    if not args.debug:
        logging.getLogger('jmetal').setLevel(logging.WARNING)
        warnings.filterwarnings("ignore")

    execute_algorithm(args)

if __name__ == '__main__':
    main()   
    