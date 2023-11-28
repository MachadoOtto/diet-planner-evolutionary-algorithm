from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import BinaryTournamentSelection, SPXCrossover, BitFlipMutation
from jmetal.util.termination_criterion import StoppingByEvaluations
from src.models.DietProblem import DietProblem
from src.utils.utils import generate_food_array

def main():
    food_array = generate_food_array('data/comidas.csv')
    food_ids = [food['id'] for food in food_array]

    problem = DietProblem(number_of_meals=4, number_of_days=7, number_of_objectives=1, food_ids=food_ids, food_objects=food_array)

    algorithm = GeneticAlgorithm(
        problem=problem,
        population_size=100,
        offspring_population_size=50,
        mutation=BitFlipMutation(probability=0.01),
        crossover=SPXCrossover(probability=0.9),
        selection=BinaryTournamentSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=25000)
    )

    algorithm.run()
    result = algorithm.get_result()

    print(f"Fitness: {result.objectives[0]}")
    print(f"Solution: {result.variables}")

    return result

if __name__ == '__main__':
    main()
