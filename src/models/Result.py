# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Result class
class Result:
    def __init__(self, fitness_objective, variety_objective, execution_times):
        self.fitness_objective = fitness_objective
        self.variety_objective = variety_objective
        self.execution_times = execution_times