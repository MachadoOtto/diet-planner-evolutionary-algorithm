import copy
import random
from typing import List
from jmetal.core.operator import Crossover
from jmetal.core.solution import PermutationSolution

class ColumnCrossover(Crossover[PermutationSolution, PermutationSolution]):
    def __init__(self, probability: float, probabilityColumn: float, number_of_columns: int, number_of_rows: int, number_of_instances: int):
        super(ColumnCrossover, self).__init__(probability=probability)
        self.probabilityColumn = probabilityColumn
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        
    def execute(self, parents: List[PermutationSolution]) -> List[PermutationSolution]:
        if len(parents) != 2:
            raise Exception("The number of parents is not two: {}".format(len(parents)))

        offspring = copy.deepcopy(parents[::-1])
        rand = random.random()
        
        if rand <= self.probability:
            for i in range (0, self.number_of_columns):
                if random.random() <= self.probabilityColumn:
                    for j in range(0, self.number_of_rows * self.number_of_instances):
                        offspring[0].variables[i * self.number_of_rows * self.number_of_instances + j] = parents[0].variables[i * self.number_of_rows * self.number_of_instances + j]
                        offspring[1].variables[i * self.number_of_rows * self.number_of_instances + j] = parents[1].variables[i * self.number_of_rows * self.number_of_instances + j]

        return offspring

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self):
        return "Column crossover"


class RowCrossover(Crossover[PermutationSolution, PermutationSolution]):
    def __init__(self, probability: float, probabilityColumn: float, number_of_columns: int, number_of_rows: int, number_of_instances: int):
        super(RowCrossover, self).__init__(probability=probability)
        self.probabilityColumn = probabilityColumn
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.number_of_instances = number_of_instances
        
    def execute(self, parents: List[PermutationSolution]) -> List[PermutationSolution]:
        if len(parents) != 2:
            raise Exception("The number of parents is not two: {}".format(len(parents)))

        offspring = copy.deepcopy(parents[::-1])
        rand = random.random()
        
        if rand <= self.probability:
            for i in range (0, self.number_of_rows):
                if random.random() <= self.probabilityColumn:
                    for j in range(0, self.number_of_columns):
                        for k in range(0, self.number_of_instances):
                            offspring[0].variables[k + i * self.number_of_instances + j * self.number_of_instances * self.number_of_rows] = parents[0].variables[k + i * self.number_of_instances + j * self.number_of_instances * self.number_of_rows]
                            offspring[1].variables[k + i * self.number_of_instances + j * self.number_of_instances * self.number_of_rows] = parents[1].variables[k + i * self.number_of_instances + j * self.number_of_instances * self.number_of_rows]
        return offspring

    def get_number_of_parents(self) -> int:
        return 2

    def get_number_of_children(self) -> int:
        return 2

    def get_name(self):
        return "Column crossover"
