import numpy as np
import re
from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from src.models.Config import Config

class DietProblem(IntegerProblem):
    def __init__(self, number_of_meals: int, number_of_days: int, max_portions:int, food_ids: int, 
            food_objects: list, config: Config):
        super(DietProblem, self).__init__()
        self.number_of_meals = number_of_meals
        self.number_of_days = number_of_days
        self.max_portions = max_portions
        self.number_of_objectives = 2
        self.number_of_constraints = 0
        self.food_ids = food_ids
        self.food_objects = food_objects
        self.max_food = len(food_ids)

        # Set objectives
        self.obj_directions = [self.MINIMIZE, self.MAXIMIZE]
        self.obj_labels = ['Fitness', 'Variety']

        # Set bounds for variables
        self.lower_bound = [0 for _ in range(number_of_meals * number_of_days*max_portions)]
        self.upper_bound = [self.max_food for _ in range(number_of_meals * number_of_days*max_portions)]

        # Load configuration
        self.config = config

        self.all_fitness = []
        
    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        total_fitness = 0
        total_variety = 0
        
        fitness_penalty_no_portions = 1000
        # Array to count the number of times each food appears in the entire solution
        food_counts_total = np.zeros(self.max_food, dtype=int)
        
        for day in range(self.number_of_days):
            # Array to count the number of times each food appears in the day
            food_counts_day = np.zeros(self.max_food, dtype=int)
           
            fitness_day = 0
            kcal_acc = 0
            p_acc = 0
            hc_acc = 0
            g_acc = 0
            null_portions = 0
            for food in range(self.number_of_meals):
                pond_meal = 0
                for portion in range (self.max_portions):
                    c = solution.variables[day * self.number_of_meals * self.max_portions + food * self.max_portions + portion]
                    
                    if (c == self.max_food):
                        null_portions += 1
                        if (null_portions == self.max_portions):
                            fitness_day += fitness_penalty_no_portions

                    else:
                        # Add one to the each food counter 
                        food_counts_day[c] += 1
                        food_counts_total[c] += 1

                        # Search for meal in the food array
                        meal = self.food_objects[c]

                        if meal is None:
                            raise ValueError(f"No meal found with id {c}")

                        # Accumulate the values of each meal in one day
                        kcal_acc += float(meal['Calories'])    
                        p_acc +=    float(meal['Protein'])
                        hc_acc +=   float(meal['Carbs'])
                        g_acc +=    float(meal['Fat'])
                        pond_meal += self.pond_horario(c, food)**2

                    if (portion == self.max_portions - 1):
                        null_portions = 0   
                        
            # Calculate fitness_day and update total_fitness
            fitness_day = self.fitness_column(kcal_acc, p_acc, hc_acc, g_acc, pond_meal**0.5)
            total_fitness += fitness_day ** 2

            # Calculate variety_score_day and update total_variety
            variety_score_day = np.sum(food_counts_day > 1)
            total_variety += self.config.delta * variety_score_day

        # Calculates the variety score for the whole solution
        variety_score_total = np.sum(food_counts_total > 1)
        total_variety += self.config.sigma * variety_score_total
        
        self.all_fitness.append(total_fitness ** 0.5)

        solution.objectives[0] = total_fitness ** 0.5
        solution.objectives[1] = 1/total_variety
        #print('total_fitness: ' + str(solution.objectives[0]))
        #print('total_variety: ' + str(solution.objectives[1]))
        return solution

    def create_solution(self) -> IntegerSolution:
        new_solution = IntegerSolution(lower_bound=self.lower_bound, upper_bound=self.upper_bound, number_of_objectives=self.number_of_objectives)
        # Create an array with number_of_days * number_of_days cells where each cell represents a meal
        for i in range(self.number_of_days * self.number_of_meals * self.max_portions):
            new_solution.variables[i] = np.random.choice(self.food_ids + [self.max_food])
        return new_solution
    
    def fitness_column(self, kcal: float, p: float, hc: float, g: float, pond_meal: float) -> float:
        return self.config.alpha * abs(self.config.kc - kcal) + \
                self.config.beta * (abs(self.config.p - p) + abs(self.config.hc - hc) + abs(self.config.g - g)) + \
                self.config.gamma * pond_meal

    def pond_horario(self, c: int, h: int) -> float:
        meal = self.food_objects[c]
        ponds = meal['hourly_weighting']
        if meal is None:
            raise ValueError(f"No se encontró la comida con id {c}")
        
        ponds = ponds.split(',')        
        match = re.search(r':(.*)', ponds[h])
        pond = re.sub('}', '', match.group(1).strip())

        return float(pond)
    
    def name(self) -> str:
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
