import random
from jmetal.core.problem import FloatProblem
from jmetal.core.solution import FloatSolution
from src.models.Config import Config

class DietProblem(FloatProblem):

    def __init__(self, number_of_variables: int, number_of_objectives: int):
        super(DietProblem, self).__init__()
        self.number_of_variables = number_of_variables
        self.number_of_objectives = number_of_objectives
        self.number_of_constraints = 0

        self.obj_directions = [self.MINIMIZE]
        self.obj_labels = ['Fitness']

        self.lower_bound = [0.0 for _ in range(number_of_variables)]
        self.upper_bound = [1.0 for _ in range(number_of_variables)]
        
        # Cargar la configuración
        self.config = Config('config.ini')

    def evaluate(self, solution: FloatSolution) -> FloatSolution:
        # Cargar los parámetros de la configuración
        alpha = self.config.alpha
        beta = self.config.beta
        gamma = self.config.gamma
        sigma = self.config.sigma

        kc = self.config.kc
        p = self.config.p
        hc = self.config.hc
        g = self.config.g

        total_fitness = 0

        for i in range(solution.number_of_variables):
            c = solution.variables[i]  # comida elegida en un horario
            h = ...  # define h

            # Calcula la función de fitness para cada comida
            fitness = alpha * abs(kc - c.kcal) + beta * (abs(p - c.p) + abs(hc - c.hc) + abs(g - c.g)) + gamma * self.pond_horario(c, h) + sigma * self.cant_rep(c, solution)

            total_fitness += fitness ** 2

        solution.objectives[0] = total_fitness ** 0.5
        return solution

    def create_solution(self) -> FloatSolution:
        new_solution = FloatSolution(lower_bound=self.lower_bound, upper_bound=self.upper_bound, number_of_objectives=self.number_of_objectives)
        for i in range(self.number_of_variables):
            new_solution.variables[i] = random.uniform(self.lower_bound[i], self.upper_bound[i])
        return new_solution

    def pond_horario(self, c, h):
        # Esta función retorna qué tan bien se ajusta una comida a un horario.
        # Deberás definir la lógica de esta función según tus necesidades.
        # Por ejemplo, podrías tener un diccionario que mapee cada comida a un rango de horarios preferidos,
        # y luego verificar si h está en el rango de horarios preferidos para c.
        return ...

    def cant_rep(self, c, solution):
        # Esta función retorna la cantidad de veces que aparece c en la semana.
        # Puedes implementarla simplemente contando el número de veces que c aparece en solution.variables.
        return solution.variables.count(c)
