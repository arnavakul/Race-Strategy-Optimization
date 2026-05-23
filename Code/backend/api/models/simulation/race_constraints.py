VALID_DRY_COMPOUNDS = [
    "SOFT",
    "MEDIUM",
    "HARD"
]

VALID_WET_COMPOUNDS = [
    "INTERMEDIATE",
    "WET"
]

ALL_COMPOUNDS = (
    VALID_DRY_COMPOUNDS + VALID_WET_COMPOUNDS
)

def is_wet_race(strategy):
    for compound, _ in strategy:
        if compound in VALID_WET_COMPOUNDS:
            return True
    return False

def validate_total_laps(strategy,race_laps):
    
    total = sum(laps for _, laps in strategy)
    
    return total == race_laps

def validate_stint_lengths(strategy):
    for compound, laps in strategy:
        if laps <= 0:
            return False
        if compound not in ALL_COMPOUNDS:
            return False
        
    return True

def validate_compound_rules(strategy):
    wet_race = is_wet_race(strategy)
    
    used_compounds = set(compound for compound, _ in strategy)
    
    if wet_race:
        return True
    
    dry_used = used_compounds.intersection(VALID_DRY_COMPOUNDS)
    
    if len(dry_used) <2: 
        return False
    return True 

def validate_strategy(strategy, race_laps):
    if not validate_total_laps(strategy,race_laps):
        return False
    
    if not validate_stint_lengths(strategy):
        return False
    
    if not validate_compound_rules(strategy):
        return False
    
    return True
