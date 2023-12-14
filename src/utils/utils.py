import pandas as pd
import matplotlib.pyplot as plt

def print_title():
    print("diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023")
    print("Integrantes:")
    print("  - Jorge Miguel Machado")
    print("  - Santiago Pereira\n")

def generate_food_array(csv_file_path):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path)

    # Convertir el DataFrame a un array de diccionarios
    food_array = df.to_dict('records')
    return food_array

def print_solution(solution, problem, model_config, food_array, with_details = False, plot = False):
    print("## Solution:")
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
            match meal:
                case 0:
                    print(f"  Breakfast:")
                case 1:
                    print(f"  Lunch:")
                case 2:
                    print(f"  Snack:")
                case 3:
                    print(f"  Dinner:")
                case _:
                    print(f"  Meal {meal + 1}:")
            portion_number = 0
            for portion in range(problem.max_portions):
                index = day * problem.number_of_meals * problem.max_portions + meal * problem.max_portions + portion
                if (the_solution[index] != problem.max_food):
                    portion_number = portion + 1
                    print(f"    {portion_number}: {food_array[the_solution[index]]['food']} [ID = {food_array[the_solution[index]]['id']}]")
                    calories_day += int(food_array[the_solution[index]]['Calories'])
                    protein_day += float(food_array[the_solution[index]]['Protein'])
                    carbs_day += float(food_array[the_solution[index]]['Carbs'])
                    fat_day += float(food_array[the_solution[index]]['Fat'])
                    if with_details:
                        print(f"      Calories: {food_array[the_solution[index]]['Calories']} - Protein: {food_array[the_solution[index]]['Protein']} - Carbs: {food_array[the_solution[index]]['Carbs']} - Fat: {food_array[the_solution[index]]['Fat']}")
        print(f"  # Day Objectives:")
        print(f"    Calories: {calories_day} - Protein: {protein_day} - Carbs: {protein_day} - Fat: {fat_day}\n")     
        calories_week += calories_day
        protein_week += protein_day
        carbs_week += carbs_day
        fat_week += fat_day
    print(f"## Week Objectives:")
    print(f"Objetives Calories: {model_config.kc} - Objetives Protein: {model_config.p} - Objetives Carbs: {model_config.hc} - Objetives Fat: {model_config.g}" )
    print(f"Total Calories: {calories_week/problem.number_of_days} - Total Protein: {protein_week/problem.number_of_days} - Total Carbs: {carbs_week/problem.number_of_days} - Total Fat: {fat_week/problem.number_of_days}\n" )
    if plot:
        plot_fitness(problem.all_fitness)
    print(f"Simplified solution: {solution.variables}")
    print(f"Fitness solution: {solution.objectives[0]}")
    print(f"Variety solution: {solution.objectives[1]}")

def print_algorithm_data(algorithm, algorithm_config, exec_time, with_details = False):
    print("## Algorithm data:")
    if with_details:
        print(f"  Algorithm: {algorithm.get_name()}")
        print(f"  Population size: {algorithm_config.population_size}")
        print(f"  Offspring population size: {algorithm_config.offspring_population_size}")
        print(f"  Mutation probability: {algorithm_config.mutation_probability}")
        print(f"  Crossover probability: {algorithm_config.crossover_probability}")
        print(f"  Probability column: {algorithm_config.probability_column}")
        print(f"  Number of evaluations: {algorithm.evaluations}")
    print(f"  Execution time: {exec_time}\n")

def print_problem_data(problem):
    print("## Problem data:")
    print(f"  Number of days: {problem.number_of_days}")
    print(f"  Number of meals: {problem.number_of_meals}")
    print(f"  Max portions: {problem.max_portions}\n")

def plot_fitness(fitness):
    xs = [x for x in range(len(fitness))]
    fig, ax = plt.subplots()
    ax.scatter(xs,fitness, s=1)
    ax.set_autoscale_on(True)
    ax.set_xlabel('Generations')
    ax.set_ylabel('Fitness')
    ax.set_title('Fitness vs Generations')
    fig.tight_layout()
    plt.show()