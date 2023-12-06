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
    food_array = generate_food_array('data/format_nutrients.csv')
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
        population_size=100,
        offspring_population_size=2,
        mutation=IntegerPolynomialMutation(probability=0.1),
        crossover=RowCrossover(probability=0.3, probabilityColumn=config.probabilityColumn, number_of_columns=problem.number_of_meals, number_of_rows=problem.number_of_days),
        selection=RandomSolutionSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=10000)
    )

    algorithm.run()
    result = algorithm.get_result()

    #print(result.variables)
    print(f"Solution: {result.variables}")
    print(f"Fitness: {result.objectives[0]}")
    print(f"Variety: {result.objectives[1]}")

    return result

def get_solution_analysis(solution):
    print(solution)
    food_array = generate_food_array('data/format_nutrients.csv')
    for day in range(7):
        print(f"Day {day + 1}:")
        calories = 0
        protein = 0
        carbs = 0
        fat = 0 
        for meal in range(4):
            print(f"    {meal + 1}: {food_array[solution[day * 4 + meal]]['food']}")
            calories += int(food_array[solution[day * 4 + meal]]['Calories'])
            protein += float(food_array[solution[day * 4 + meal]]['Protein'])
            carbs += float(food_array[solution[day * 4 + meal]]['Carbs'])
            fat += float(food_array[solution[day * 4 + meal]]['Fat'])
        print(f"    Calories: {calories} - Protein: {protein} - Carbs: {carbs} - Fat: {fat}" )     

if __name__ == '__main__':
    solution = main()
    get_solution_analysis(solution.variables)


    
    