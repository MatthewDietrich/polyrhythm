import yaml

from src.app import App


with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

App(config).run()