from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm

from jmetal.operator import BestSolutionSelection, RandomSolutionSelection
from jmetal.operator import IntegerPolynomialMutation
from jmetal.operator import CXCrossover,DifferentialEvolutionCrossover,NullCrossover,PMXCrossover,SBXCrossover,SPXCrossover


from jmetal.util.termination_criterion import StoppingByEvaluations
from src.models.DietProblem import DietProblem
from src.utils.utils import generate_food_array

def main():
    food_array = generate_food_array('data/iguales.csv')
    food_ids = [food['id'] for food in food_array]

    problem = DietProblem(number_of_meals=4, number_of_days=7, number_of_objectives=1, food_ids=food_ids, food_objects=food_array)

    algorithm = GeneticAlgorithm(
        problem=problem,
        population_size=4,
        offspring_population_size=2,
        mutation=IntegerPolynomialMutation(probability=0.1),
        crossover=CXCrossover(probability=0.0),
        selection=RandomSolutionSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=30)
    )

    algorithm.run()
    result = algorithm.get_result()

    #print(result.variables)
    print(f"Solution: {result.variables}")
    print(f"Fitness: {result.objectives[0]}")

    return result

if __name__ == '__main__':
    main()
