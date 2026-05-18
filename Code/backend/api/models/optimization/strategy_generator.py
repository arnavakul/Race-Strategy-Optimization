COMPOUNDS = ["SOFT","MEDIUM","HARD"]

def generate_strategies(total_laps):
    strategies = []
    
    #1 stop strategies:
    
    for compound1 in COMPOUNDS:
        for compound2 in COMPOUNDS:
            
            #the rule is to have 2 different tyre sets: 
            
            if compound1 == compound2:
                continue
            
            for stint1_laps in range(8, total_laps-8):
                
                stint2_laps = total_laps - stint1_laps
                
                strategy = [
                    (compound1,stint1_laps),
                    (compound2,stint2_laps)
                ]
                
                strategies.append(strategy)
    
    #2 stop strategy: 
    
    for compound1 in COMPOUNDS:
        for compound2 in COMPOUNDS:
            for compound3 in COMPOUNDS:
                
                used_compounds = {
                    compound1,
                    compound2,
                    compound3,
                }
            
            if len(used_compounds) < 2:
                continue
            
            for stint1 in range(8, total_laps-16):
                for stint2 in range(8, total_laps-8):
                    stint3 = (total_laps - stint1 -stint2)
                    
                    strategy = [
                            (compound1, stint1),
                            (compound2, stint2),
                            (compound3, stint3)
                    ]
                    
                    strategies.append(strategy)
    
    return strategies

if __name__ == "__main__":

    strategies = generate_strategies(57)

    print(f"Generated {len(strategies)} strategies")

    for s in strategies[:10]:
        print(s)