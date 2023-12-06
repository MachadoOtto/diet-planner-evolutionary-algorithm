import pandas as pd
import numpy as np

foods = pd.read_csv('nutrients.csv')
foods['food'] = foods['Food'].astype(str) + ' - ' + foods['Measure']

foods = foods.drop(['Food', 'Measure', 'Sat.Fat','Fiber','Grams'], axis=1)
foods['id'] = range(len(foods))

order=['id','food','Category','Calories','Protein','Carbs','Fat']
foods = foods[order]

foods['Calories'] = foods['Calories'].replace(',', '', regex=True)
foods['Calories'] = foods['Calories'].replace('"', '', regex=True)
foods['Calories'] = foods['Calories'].fillna(0).astype(float)

foods['Protein'] = foods['Protein'].replace('t\'', 0)
foods['Protein'] = foods['Protein'].replace('t', 0)
foods['Protein'] = (foods['Protein'].fillna(0)).astype(float)

foods['Carbs'] = foods['Carbs'].replace('t\'', 0)
foods['Carbs'] = foods['Carbs'].replace('t', 0)
foods['Carbs'] = (foods['Carbs'].fillna(0)).astype(float)

foods['Fat'] = foods['Fat'].replace('t\'', 0)
foods['Fat'] = foods['Fat'].replace('t', 0)
foods['Fat'] = (foods['Fat'].fillna(0)).astype(float)

foods['Calories'] = foods['Calories'].replace('', 0)
foods['Protein'] = foods['Protein'].replace('', 0)
foods['Carbs'] = foods['Carbs'].replace('', 0)
foods['Fat'] = foods['Fat'].replace('', 0)

conditions = [
    foods['Category'].str.contains('Breads, cereals, fastfood,grains'),
    foods['Category'].str.contains('Meat, Poultry'),
    foods['Category'].str.contains('Desserts, sweets'), 
    foods['Category'].str.contains('Dairy products'),
    foods['Category'].str.contains('Vegetables A-E') | foods['Category'].str.contains('Vegetables R-Z') | foods['Category'].str.contains('Vegetables F-P'),
    foods['Category'].str.contains('Fruits G-P') | foods['Category'].str.contains('Fruits A-F') | foods['Category'].str.contains('Fruits R-Z'),
    foods['Category'].str.contains('Fish, Seafood'),
    foods['Category'].str.contains('Fats, Oils, Shortenings'),
    foods['Category'].str.contains('Seeds and Nuts'),
    foods['Category'].str.contains('Drinks,Alcohol, Beverages'),
    foods['Category'].str.contains('Soups'),
    foods['Category'].str.contains('Jams, Jellies')
]

values = [
    "{0: 1, 1: 0.2, 2: 0.9, 3: 0.3}",
    "{0: 0.0, 1: 0.9, 2: 0.0, 3: 0.6}",
    "{0: 0, 1: 0.3, 2: 0.1, 3: 0.3}",
    "{0: 1, 1: 0.2, 2: 0.9, 3: 0.3}",
    "{0: 0.1, 1: 0.9, 2: 0.2, 3: 0.8}",
    "{0: 1, 1: 0.2, 2: 0.9, 3: 0.3}",
    "{0: 0.1, 1: 0.9, 2: 0.2, 3: 1.0}",
    "{0: 0.1, 1: 0.1, 2: 0.3, 3: 0.2}",
    "{0: 1, 1: 0.2, 2: 0.8, 3: 0.3}",
    "{0: 0.0, 1: 0.0, 2: 0.0, 3: 0.1}",
    "{0: 0.0, 1: 0.1, 2: 0.0, 3: 0.1}",
    "{0: 0.0, 1: 0.1, 2: 0.3, 3: 0.1}"
]

foods['hourly_weighting'] = np.select(conditions, values, default='OOOOOOOOOO')
foods = foods.drop(['Category'], axis=1) 

# Agrego duplicados para darle variedad a la solución
new_rows = []
for index, row in foods.iterrows():
    new_row = {'id': row['id'] + len(foods),
               'food': '2X' + row['food'] ,
               'Calories': row['Calories'] * 2,
               'Protein': row['Protein'] * 2,
               'Carbs': row['Carbs'] * 2,
               'Fat': row['Fat'] * 2,
               'hourly_weighting': row['hourly_weighting']}
    new_rows.append(new_row)
new_rows_df = pd.DataFrame(new_rows)
foods = pd.concat([foods, new_rows_df], ignore_index=True)

foods.to_csv('format_nutrients.csv', index=False)
foods.to_excel('format_nutrients.xlsx', index=False)