# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import pandas as pd
import matplotlib.pyplot as plt

# Utils functions

# Print the title
def print_title():
    print("diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023")
    print("Integrantes:")
    print("  - Jorge Miguel Machado")
    print("  - Santiago Pereira\n")

# Read the algorithm config
def read_algorithm_config():
    df = pd.read_csv('data/algorithms_config.csv')
    algorithm_config = df.to_dict('records')
    return algorithm_config

# Generate the food array
def generate_food_array(csv_file_path):
    df = pd.read_csv(csv_file_path)
    food_array = df.to_dict('records')
    return food_array

# Get the crossover name
def get_cross_name(crossover_type):
    match crossover_type:
        case 'spx':
            return 'Simple Point Crossover'
        case 'column':
            return 'Column Crossover'
        case 'row':
            return 'Row Crossover'
        case _:
            return 'Simple Point Crossover'