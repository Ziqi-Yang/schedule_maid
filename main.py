import yaml
import XiaoYiJiang


# read config from config.yaml
with open("_config.yaml") as f:
    a = yaml.load(f.read(),Loader=yaml.loader.Loader)


