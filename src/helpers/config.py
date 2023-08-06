import yaml


with open("config.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)
WINDOW = CONFIG["window"]
BALL = CONFIG["ball"]
RHYTHM = CONFIG["rhythm"]
MIXER = CONFIG["mixer"]
