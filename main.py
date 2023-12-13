from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm

from jmetal.operator import BestSolutionSelection, RandomSolutionSelection
from jmetal.operator import IntegerPolynomialMutation
#from jmetal.operator import CXCrossover,DifferentialEvolutionCrossover,NullCrossover,PMXCrossover,SBXCrossover,SPXCrossover


from jmetal.util.termination_criterion import StoppingByEvaluations
from src.models.DietProblem import DietProblem
from src.utils.utils import generate_food_array
from src.models.Config import Config
from src.models.CrossoverCustom import ColumnCrossover, RowCrossover

def main():
    food_array = generate_food_array('data/format_nutrients.csv')
    food_ids = [food['id'] for food in food_array]
    #food_ids = [int(i) for i in food_ids]
    
    config = Config('config\config.ini')

    problem = DietProblem(
        number_of_meals=4,
        number_of_days=7,
        max_portions=4,
        food_ids=food_ids,
        food_objects=food_array,
        config=config
    )

    algorithm = GeneticAlgorithm(
        problem=problem,
        population_size=100,
        offspring_population_size=1,
        mutation=IntegerPolynomialMutation(probability=0.1),
        crossover=RowCrossover(probability=0.2, probabilityColumn=config.probabilityColumn,
            number_of_columns=problem.number_of_meals, number_of_rows=problem.number_of_days,
            number_of_instances=problem.max_portions),
        selection=RandomSolutionSelection(),
        termination_criterion=StoppingByEvaluations(max_evaluations=10000)
    )

    algorithm.run()
    result = algorithm.get_result()

    print(f"Solution: {result.variables}")
    print(f"Fitness: {result.objectives[0]}")
    print(f"Variety: {result.objectives[1]}")

    return result, problem


def plot_fitness(fitness):
    import matplotlib.pyplot as plt    
    xs = [x for x in range(len(fitness))]
    fig, ax = plt.subplots()
    ax.scatter(xs,fitness, s=1)
    ax.set_autoscale_on(True)
    ax.set_xlabel('Generations')
    ax.set_ylabel('Fitness')
    ax.set_title('Fitness vs Generations')
    fig.tight_layout()
    plt.show()


def get_solution_analysis(solution, problem):
    food_array = generate_food_array('data/format_nutrients.csv')
    config = Config('config\config.ini')
    calories_week = 0
    protein_week = 0
    carbs_week = 0
    fat_week = 0 
    the_solution = solution.variables
    for day in range(problem.number_of_days):
        print(f"Day {day + 1}:")
        calories_day = 0
        protein_day = 0
        carbs_day = 0
        fat_day = 0 
        for meal in range(problem.number_of_meals): 
            print(f"  Meal {meal + 1}:")
            for portion in range(problem.max_portions):
                index = day * problem.number_of_meals * problem.max_portions + meal * problem.max_portions + portion
                if (the_solution[index] != problem.max_food):
                    print(f"    {portion + 1}: {food_array[the_solution[index]]['food']}")
                    calories_day += int(food_array[the_solution[index]]['Calories'])
                    protein_day += float(food_array[the_solution[index]]['Protein'])
                    carbs_day += float(food_array[the_solution[index]]['Carbs'])
                    fat_day += float(food_array[the_solution[index]]['Fat'])
        print(f"    Calories: {calories_day} - Protein: {protein_day} - Carbs: {protein_day} - Fat: {fat_day}" )     
        calories_week += calories_day
        protein_week += protein_day
        carbs_week += carbs_day
        fat_week += fat_day
    print(f"Objetives calories: {config.kc} - Objetives protein: {config.p} - Objetives carbs: {config.hc} - Objetives fat: {config.g}" )
    print(f"Total Calories: {calories_week/problem.number_of_days} - Total Protein: {protein_week/problem.number_of_days} - Total Carbs: {carbs_week/problem.number_of_days} - Total Fat: {fat_week/problem.number_of_days}" )
    #plot_fitness(problem.all_fitness)
    problem.evaluate(solution)
    print(f"Fitness solution: {solution.objectives[0]}")
    print(f"Variety solution: {solution.objectives[1]}")



if __name__ == '__main__':
    solution, problem = main()
    get_solution_analysis(solution, problem)


    
    