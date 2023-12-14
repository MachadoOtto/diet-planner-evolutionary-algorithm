import configparser

class Config:
    
    def __init__(self, filename, type):
        config = configparser.ConfigParser()
        config.read(filename)

        if type == 'model':
            self.alpha = float(config['MODEL']['alpha'])
            self.beta = float(config['MODEL']['beta'])
            self.gamma = float(config['MODEL']['gamma'])
            self.sigma = float(config['MODEL']['sigma'])
            self.delta = float(config['MODEL']['delta'])
            self.kc = float(config['MODEL']['kc'])
            self.p = float(config['MODEL']['p'])
            self.hc = float(config['MODEL']['hc'])
            self.g = float(config['MODEL']['g'])
            self.number_of_days = int(config['MODEL']['number_of_days'])
            self.number_of_meals = int(config['MODEL']['number_of_meals'])
            self.max_portions = int(config['MODEL']['max_portions'])
        elif type == 'algorithm':
            self.population_size = int(config['ALGORITHM']['population_size'])
            self.offspring_population_size = int(config['ALGORITHM']['offspring_population_size'])
            self.max_evaluations = int(config['ALGORITHM']['max_evaluations'])
            self.mutation_probability = float(config['ALGORITHM']['mutation_probability'])
            self.crossover_probability = float(config['ALGORITHM']['crossover_probability'])
            self.probability_column = float(config['ALGORITHM']['probability_column'])
