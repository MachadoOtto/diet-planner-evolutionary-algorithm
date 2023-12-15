# diet-planner-evolutionary-algorithm - Algoritmos Evolutivos - FING 2023
# Integrantes:
#   - Jorge Miguel Machado
#   - Santiago Pereira

# Args class
class Args:
    def __init__(self, crossover_type, crossover_probability, mutation_probability):
        self.crossover_type = crossover_type
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability