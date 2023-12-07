import pandas as pd

def generate_food_array(csv_file_path):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file_path)

    # Convertir el DataFrame a un array de diccionarios
    food_array = df.to_dict('records')
    return food_array