# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Imports
import matplotlib.pyplot as plt

nombres = ['AE 1', 'AE 2', 'AE 3', 'AE 4', 'AE 5', 'AE 6', 'AE 7', 'AE 8', 'AE 9', 'AE 10', 'AE 11', 'AE 12', 'AE 13', 'AE 14', 'AE 15', 'AE 16', 'AE 17', 'AE 18', 'Greedy']
medias = [605.6571661, 1126.486608, 1376.959415, 601.3043589, 1118.59412, 1375.946595, 601.1260004, 1061.001527, 1360.043105, 631.7652148, 1135.961871, 1312.162652, 617.4194476, 1024.86713, 1381.234482, 616.960027, 1057.70959, 1331.88944, 405.2576378897479]
tiempos = [6.847947359, 6.64448905, 6.679475188, 6.503451109, 6.498239875, 6.51768589, 6.483181357, 6.44544065, 6.522842288, 6.460286617, 6.497743368, 6.469290495, 6.66612041, 6.535984278, 6.567613959, 6.621400714, 6.658402801, 6.650698066, 3.7665982246398926]

# Crear una figura y un conjunto de subtramas
fig, ax = plt.subplots()

# Colorear la barra 'Greedy' de otro color
colors = ['blue' if name != 'Greedy' else 'green' for name in nombres]

# Crear la gráfica de barras para 'medias'
ax.bar(nombres, medias, color=colors)
ax.set_title('Medias de Mejor Fitness vs Greedy - Instancia 1')
ax.set_xlabel('Nombres')
ax.set_ylabel('Medias')
plt.xticks(rotation=90)  # Rotar los nombres para que se vean mejor
plt.savefig('./output/instancia1/medias_fitness_vs_greedy.png')

# Crear una nueva figura y un conjunto de subtramas para 'tiempos'
fig, ax = plt.subplots()

# Crear la gráfica de barras para 'tiempos'
ax.bar(nombres, tiempos, color=colors)
ax.set_title('Tiempos de Ejecución de AE vs Greedy - Instancia 1')
ax.set_xlabel('Nombres')
ax.set_ylabel('Tiempos')
plt.xticks(rotation=90)  # Rotar los nombres para que se vean mejor
plt.savefig('./output/instancia1/tiempos_ejecucion_vs_greedy.png')

medias2 = [789.1304011, 1654.529338, 1985.006523, 846.5101602, 1681.504791, 1936.750093, 788.2288206, 1688.61874, 1941.028891, 840.0872277, 1649.987161, 2050.919439, 773.1936261, 1582.94196, 1960.101335, 818.2326575, 1612.202759, 2000.03594, 183.0633819993209]
tiempos2 = [6.686064959, 6.713873863, 6.700763226, 6.699622393, 6.761747003, 6.626593709, 6.7441957, 6.516157031, 6.620147824, 6.62976408, 6.572646737, 6.609245658, 6.635425925, 6.11563313, 5.988518119, 6.010091543, 5.950300694, 5.847665429, 3.856283187866211]

# Crear una figura y un conjunto de subtramas
fig, ax = plt.subplots()

# Crear la gráfica de barras para 'medias'
ax.bar(nombres, medias2, color=colors)
ax.set_title('Medias de Mejor Fitness vs Greedy - Instancia 2')
ax.set_xlabel('Nombres')
ax.set_ylabel('Medias')
plt.xticks(rotation=90)  # Rotar los nombres para que se vean mejor
plt.savefig('./output/instancia2/medias_fitness_vs_greedy.png')

# Crear una nueva figura y un conjunto de subtramas para 'tiempos'
fig, ax = plt.subplots()

# Crear la gráfica de barras para 'tiempos'
ax.bar(nombres, tiempos2, color=colors)
ax.set_title('Tiempos de Ejecución de AE vs Greedy - Instancia 2')
ax.set_xlabel('Nombres')
ax.set_ylabel('Tiempos')
plt.xticks(rotation=90)  # Rotar los nombres para que se vean mejor
plt.savefig('./output/instancia2/tiempos_ejecucion_vs_greedy.png')

minimos = [417.7849918, 586.0414161, 832.1600108, 404.0836108, 625.4857505, 736.0228267, 401.4236118, 683.2747679, 861.8106623, 366.9876211, 554.9301622, 975.7559278, 463.7047761, 583.4142475, 842.8100271, 398.4542413, 767.5205004, 749.0517479, 405.2576378897479]
minimos2 = [478.0584874, 1024.263266, 1214.680798, 453.5793275, 1191.530625, 1388.34048, 456.4410341, 1134.779467, 1193.825303, 539.7546897, 1064.886282, 1473.680613, 507.6117811, 986.7328654, 855.4761593, 423.3342932, 1079.068973, 1416.582633, 183.0633819993209]

# Crear una figura y un conjunto de subtramas
fig, ax = plt.subplots()

# Crear la gráfica de barras para 'medias'
ax.bar(nombres, minimos, color=colors)
ax.set_title('Minimos de Mejor Fitness vs Greedy - Instancia 1')
ax.set_xlabel('Nombres')
ax.set_ylabel('Minimos')
plt.xticks(rotation=90)  # Rotar los nombres para que se vean mejor
plt.savefig('./output/instancia1/minimos_fitness_vs_greedy.png')

# Crear una figura y un conjunto de subtramas
fig, ax = plt.subplots()

# Crear la gráfica de barras para 'medias'
ax.bar(nombres, minimos2, color=colors)
ax.set_title('Minimos de Mejor Fitness vs Greedy - Instancia 2')
ax.set_xlabel('Nombres')
ax.set_ylabel('Minimos')
plt.xticks(rotation=90)  # Rotar los nombres para que se vean mejor
plt.savefig('./output/instancia2/minimos_fitness_vs_greedy.png')