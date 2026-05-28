# Responsible for:
# - VSC deployment
# - VSC duration
# - VSC lap slowdown

import random

def check_virtual_safety_Car():
    return random.random() < 0.006

def generate_vsc_duration():
    return random.randint(
        2,5
    )

def get_vsc_multiplier():
    return 1.12