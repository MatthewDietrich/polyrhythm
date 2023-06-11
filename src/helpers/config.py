import yaml


with open('config.yaml', 'r') as f:
    CONFIG = yaml.safe_load(f)
WINDOW_CONFIG = CONFIG['window']
BALL_CONFIG = CONFIG['ball']
RHYTHM_CONFIG = CONFIG['rhythm']
MIXER_CONFIG = CONFIG['mixer']