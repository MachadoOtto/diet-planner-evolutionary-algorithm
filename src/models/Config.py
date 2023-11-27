import configparser

class Config:
    def __init__(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)

        self.alpha = float(config['DEFAULT']['alpha'])
        self.beta = float(config['DEFAULT']['beta'])
        self.gamma = float(config['DEFAULT']['gamma'])
        self.sigma = float(config['DEFAULT']['sigma'])
        self.kc = float(config['DEFAULT']['kc'])
        self.p = float(config['DEFAULT']['p'])
        self.hc = float(config['DEFAULT']['hc'])
        self.g = float(config['DEFAULT']['g'])
