# | System         | Purpose           |
# | -------------- | ----------------- |
# | SC probability | random deployment |
# | SC duration    | how many laps     |
# | Lap slowdown   | reduced pace      |
# | SC state       | active/inactive   |
# Responsible for:
# - safety car deployment
# - safety car duration
# - race neutralization
# - lap slowdown effects

import random

#deploy sc randomly
def check_safety_car():
    return random.random() <0.035

#generate sc duration
def generate_safety_car_duration():
    return random.randint(2,5)

#sc lap time slow down
def get_safety_car_multiplier():
    return 1.35
