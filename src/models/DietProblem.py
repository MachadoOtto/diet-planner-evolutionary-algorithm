import numpy as np
import re
#from jmetal.core.problem import FloatProblem
#from jmetal.core.solution import FloatSolution
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from src.models.Config import Config

class DietProblem(IntegerProblem):

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

        self.lower_bound = [1 for _ in range(number_of_meals * number_of_days)]
        self.upper_bound = [len(food_ids) for _ in range(number_of_meals * number_of_days)]

        # Cargar la configuración
        self.config = Config('config\config.ini')
        
    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        total_fitness = 0
        #print('solution.variables: ' + str(solution.variables))
        for day in range(self.number_of_days): 
            fitness_day = 0
            kcal_acc = 0
            p_acc = 0
            hc_acc = 0
            g_acc = 0
            for food in range(self.number_of_meals):
                
                c = solution.variables[day * self.number_of_meals + food]  # comida elegida en un horario
                
                # Buscar la comida en el array de comidas
                meal = self.food_objects[c - 1]
            
                if meal is None:
                    raise ValueError(f"No se encontró la comida con id {c}")
                
                #acumular los valores de cada comida en un dia
                kcal_acc += meal['kcal']    
                p_acc += meal['p']
                hc_acc += meal['hc']
                g_acc += meal['g'] 
                
            fitness_day = self.config.alpha * abs(self.config.kc - kcal_acc) + \
                self.config.beta * (abs(self.config.p - p_acc) + abs(self.config.hc - hc_acc) + abs(self.config.g - g_acc)) + \
                self.config.gamma * self.pond_horario(c, food) + \
                self.config.sigma * self.cant_rep(c, solution)
            #print('fitness_day: ' + str(fitness_day))
            #total_fitness += fitness_day# santiago
            total_fitness += fitness_day ** 2
        
        #print('fitness_semanal: ' + str(total_fitness/self.number_of_days))
        
        solution.objectives[0] = total_fitness ** 0.5
        print('total_fitness: ' + str(total_fitness ** 0.5))
        return solution

    def create_solution(self) -> IntegerSolution:
        new_solution = IntegerSolution(lower_bound=self.lower_bound, upper_bound=self.upper_bound, number_of_objectives=self.number_of_objectives)
        # Creao un array con 7x4=28 celdas donde cada uno representa una comida
        for i in range(self.number_of_days*self.number_of_meals):
            new_solution.variables[i] = np.random.choice(self.food_ids)
        #print('Nueva solución: ')
        #print(new_solution.variables)
        return new_solution

    def pond_horario(self, c, h):
        meal = self.food_objects[c - 1]
        ponds = meal['ponderacion_horaria']

        if meal is None:
            raise ValueError(f"No se encontró la comida con id {c}")
        ponds = ponds.split(',')        
        match = re.search(r':(.*)', ponds[h])
        pond = re.sub('}','',match.group(1).strip())
        ajuste = float(pond)
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