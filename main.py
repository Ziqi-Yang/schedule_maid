import yaml
from yaml.loader import Loader

# read config from config.yaml
with open("config.yaml") as f:
    a = yaml.load(f.read(),Loader=Loader)
    