import numpy as np
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from src.models.Config import Config

class DietProblem(FloatProblem):

    def __init__(self, number_of_meals: int, number_of_days: int, number_of_objectives: int,
                 food_ids: int, food_objects: list):
        super(DietProblem, self).__init__()
        self.number_of_meals = number_of_meals
        self.number_of_days = number_of_days
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = 0
        self.food_ids = food_ids
        self.food_objects = food_objects

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Fitness']

        self.lower_bound = [0.0 for _ in range(number_of_meals * number_of_days)]
        self.upper_bound = [1.0 for _ in range(number_of_meals * number_of_days)]
        
        # Cargar la configuración
        self.config = Config('config\config.ini')
        
    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        total_fitness = 0

        for i in range(self.number_of_days*self.number_of_meals): 
            c = solution.variables[i]  # comida elegida en un horario

            # Buscar la comida en el array de comidas
            meal = self.food_objects[c - 1]

            if meal is None:
                raise ValueError(f"No se encontró la comida con id {c}")

            # Calcula la función de fitness para cada comida
            fitness = self.config.alpha * abs(self.config.kc - meal['kcal']) + \
                    self.config.beta * (abs(self.config.p - meal['p']) + abs(self.config.hc - meal['hc']) + abs(self.config.g - meal['g'])) + \
                    self.config.gamma * self.pond_horario(c, i % 4 ) + \
                    self.config.sigma * self.cant_rep(c, solution)

            total_fitness += fitness ** 2

        solution.objectives[0] = total_fitness ** 0.5
        return solution

    def create_solution(self) -> FloatSolution:
        new_solution = FloatSolution(lower_bound=self.lower_bound, upper_bound=self.upper_bound, number_of_objectives=self.number_of_objectives)
        # Creao un array con 7x4=28 celdas donde cada uno representa una comida
        #print('foods_ids', self.food_ids)
        for i in range(self.number_of_days*self.number_of_meals):
                new_solution.variables[i] = np.random.choice(self.food_ids)
        print(new_solution.variables)
        return new_solution

    def pond_horario(self, c, h):
        meal = self.food_objects[c - 1]
        if meal is None:
            raise ValueError(f"No se encontró la comida con id {c}")
        pond = meal['hour_weight']
        ajuste = pond.get(h, 0)
        return ajuste

    def cant_rep(self, c, solution):
        return solution.variables.count(c)
    
    def name(self):
        return 'DietProblem'

    @property
    def number_of_constraints(self):
        return self._number_of_constraints
    
    @number_of_constraints.setter
    def number_of_constraints(self, value):
        self._number_of_constraints = value

    @property
    def number_of_objectives(self):
        return self._number_of_objectives

    @number_of_objectives.setter
    def number_of_objectives(self, value):
        self._number_of_objectives = value