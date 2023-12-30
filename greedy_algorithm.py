# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
from src.models.Config import Config
from src.utils.utils import generate_food_array
import re
import numpy as np
import time
import argparse

# Greedy algorithm
def greedy_diet(foods, config, meals_per_day=4, days=7, foods_per_meal=4):
    # Order the foods by f1
    foods.sort(key=lambda x: f1(x, config))

    # Initialize the diet
    diet = np.empty((days*meals_per_day*foods_per_meal), dtype=object)
    daily_nutrition_limits = {'Calories': config.kc, 'Protein': config.p, 'Carbs': config.hc, 'Fat': config.g}
    food_counts_total = np.zeros(len(foods), dtype=int)
    total_f1 = 0
    total_f2 = 0

    for day in range(days):
        food_counts_day = np.zeros(len(foods), dtype=int)
        f1_day = 0
        kcal_acc = 0
        p_acc = 0
        hc_acc = 0
        g_acc = 0
        daily_nutrition_limits = {'Calories': config.kc, 'Protein': config.p, 'Carbs': config.hc, 'Fat': config.g}

        portion_counter = [0 for _ in range(foods_per_meal)]
        pond_meal = 0

        for meal in range(meals_per_day*foods_per_meal):
            for food in foods:
                # Check if the food is already in the diet
                if food['id'] not in diet:
                    if all(food[nutrient] <= daily_nutrition_limits[nutrient] for nutrient in ['Calories', 'Protein', 'Carbs', 'Fat']):
                        # Add the food to the diet
                        diet[day*meals_per_day*foods_per_meal + (meal % foods_per_meal)*foods_per_meal + portion_counter[meal % foods_per_meal]] = food['id']
                        food_counts_day[food['id']] += 1
                        food_counts_total[food['id']] += 1
                        portion_counter[meal % foods_per_meal] += 1

                        # Update the daily nutrition limits
                        for nutrient in ['Calories', 'Protein', 'Carbs', 'Fat']:
                            daily_nutrition_limits[nutrient] -= food[nutrient]

                        # Accumulate the values of each meal in one day
                        kcal_acc += float(food['Calories'])    
                        p_acc +=    float(food['Protein'])
                        hc_acc +=   float(food['Carbs'])
                        g_acc +=    float(food['Fat'])
                        pond_meal += pond_horario(foods, food['id'], meal % foods_per_meal)**2

                        break
        
        # Calculate f1_day and update total_f1
        print(f"Day: {day}, Calories: {kcal_acc}, Protein: {p_acc}, Carbs: {hc_acc}, Fat: {g_acc}, Pond: {pond_meal**0.5}\n")
        f1_day = f1_column(config, kcal_acc, p_acc, hc_acc, g_acc, pond_meal**0.5)
        total_f1 += f1_day ** 2

        # Calculate f2_score_day and update total_f2
        f2_score_day = np.sum(food_counts_day > 1)
        total_f2 += config.delta * f2_score_day

    # Calculates the f2 score for the whole solution
    f2_score_total = np.sum(food_counts_total > 1)
    total_f2 += config.sigma * f2_score_total

    total_f1 = total_f1 ** 0.5

    return diet, total_f1, total_f2

# f1 function
def f1(food, config):
    kcal = food['Calories']
    p = food['Protein']
    hc = food['Carbs']
    g = food['Fat']
    return config.alpha * abs(config.kc - kcal) + \
           config.beta * (abs(config.p - p) + abs(config.hc - hc) + abs(config.g - g))

# f1 function
def f1_column(config, kcal: float, p: float, hc: float, g: float, pond_meal: float) -> float:
        return config.alpha * abs(config.kc - kcal) + \
                config.beta * (abs(config.p - p) + abs(config.hc - hc) + abs(config.g - g)) + \
                config.gamma * (1 - pond_meal)

# Pond function
def pond_horario(food_objects, c: int, h: int) -> float:
        meal = food_objects[c]
        ponds = meal['hourly_weighting']
        if meal is None:
            raise ValueError(f"No se encontró la comida con id {c}")
        
        ponds = ponds.split(',')        
        match = re.search(r':(.*)', ponds[h])
        pond = re.sub('}', '', match.group(1).strip())

        return float(pond)

def main(instance):
    # Load the model and algorithm configurations
    model_config = Config(f'config\config_{instance}.ini', 'model')

    # Load the food array
    food_array = generate_food_array('data/foods.csv')

    start = time.time() 

    # Run the greedy algorithm
    diet, f1, f2 = greedy_diet(food_array, model_config, meals_per_day=4, days=7, foods_per_meal=4)

    end = time.time()

    print(f"f1: {f1}")
    print(f"f2: {f2}")
    print(f"Execution Time: {end - start}")
    print(f"Solution: {diet}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the greedy algorithm')
    parser.add_argument('instance', type=str, help='Instance name')
    args = parser.parse_args()

    main(args.instance)