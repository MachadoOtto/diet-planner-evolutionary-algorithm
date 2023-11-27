from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import BinaryTournamentSelection, SinglePointCrossover, BitFlipMutation
from src.models.DietProblem import DietProblem

problem = DietProblem(...)
algorithm = GeneticAlgorithm(
    problem=problem,
    population_size=100,
    offspring_population_size=50,
    mutation=BitFlipMutation(probability=0.01),
    crossover=SinglePointCrossover(probability=0.9),
    selection=BinaryTournamentSelection(),
    termination_criterion=StoppingByEvaluations(max_evaluations=25000)
)

algorithm.run()
result = algorithm.get_result()
