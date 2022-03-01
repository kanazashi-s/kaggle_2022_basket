import yaml

def load_config(path):
    with open(path, 'r') as yml:
        return yaml.load(yml)