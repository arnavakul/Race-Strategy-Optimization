# | Function             | Purpose                |
# | -------------------- | ---------------------- |
# | Rival gap estimation | relative race position |
# | Rival pit detection  | opponent strategy      |
# | Undercut opportunity | attack timing          |
# | Overcut opportunity  | extension timing       |
# Responsible for:
# - rival pressure
# - undercut opportunities
# - overcut opportunities
# - rival pit reactions

import random

#generate gap to rival
def generate_rival_gap():
    return random.uniform(
        0.5,6
    )

#generate undercut opportunity 
def should_attempt_undercut(rival_gap):
    
    if rival_gap <= 2.0:
        return True
    return False

#generate overcut opportunity 
def should_attempt_overcut(rival_gap):
    
    if rival_gap > 2.0:
        return True
    return False

