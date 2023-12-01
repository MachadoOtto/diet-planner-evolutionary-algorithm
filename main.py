from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm

from jmetal.operator import BestSolutionSelection, RandomSolutionSelection
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator import CXCrossover,DifferentialEvolutionCrossover,NullCrossover,PMXCrossover,SBXCrossover,SPXCrossover


from jmetal.util.termination_criterion import StoppingByEvaluations
from src.models.DietProblem import DietProblem
from src.utils.utils import generate_food_array
from src.models.Config import Config
from src.models.CrossoverCustom import ColumnCrossover, RowCrossover

def main():
    food_array = generate_food_array('data/iguales.csv')
    food_ids = [food['id'] for food in food_array]
    
    config = Config('config\config.ini')

    problem = DietProblem(
        number_of_meals=4,
        number_of_days=7,
        food_ids=food_ids,
        food_objects=food_array,
        config=config
    )

    algorithm = GeneticAlgorithm(
        problem=problem,
        population_size=40,
        offspring_population_size=2,
        mutation=IntegerPolynomialMutation(probability=0.1),
        crossover=ColumnCrossover(probability=0.3, probabilityColumn=config.probabilityColumn, number_of_columns=problem.number_of_meals, number_of_rows=problem.number_of_days),
        selection=RandomSolutionSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=5000)
    )

    algorithm.run()
    result = algorithm.get_result()

    #print(result.variables)
    print(f"Solution: {result.variables}")
    print(f"Fitness: {result.objectives[0]}")
    print(f"Variety: {result.objectives[1]}")

    return result

if __name__ == '__main__':
    main()
