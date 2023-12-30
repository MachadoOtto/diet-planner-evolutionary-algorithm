# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Result class
class Result:
    def __init__(self, f1_objective, f2_objective, execution_times):
        self.f1_objective = f1_objective
        self.f2_objective = f2_objective
        self.execution_times = execution_times