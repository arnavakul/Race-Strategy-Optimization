#It will be the single source for all the strategic races. 
#Every major simulation system will read/write from this.

class RaceState:
    def __init__(self):
        self.current_stint=1
        
        self.pitstop_count = 0
        
        self.used_compounds = set()
        
        self.current_compound = None
        
        self.current_tyre_age = 0
        
        self.is_legal_race = False
        
        self.stint_history = []
        
        self.strategy_events = []
        
        self.tyre_inventory = {
            "SOFT": 6,
            "MEDIUM": 4,
            "HARD": 3,
            "INTERMEDIATE": 3,
            "WET": 2
        }
    
    def register_compound_usage(self,compound):
        self.used_compounds.add(compound)
        self.current_compound = compound
        self.consume_tyre_set(compound)
    
    def register_pitstop(self):
        self.pitstop_count +=1
        self.current_stint +=1
        self.current_tyre_age = 0
    
    def increment_tyre_age(self):
        self.current_tyre_age +=1
    
    def consume_tyre_set(self,compound):
        
        if self.tyre_inventory[compound] > 0:
            
            self.tyre_inventory[compound] -= 1
        else:
            
            raise ValueError(
                f"No remaining tyre sets for {compound}"
            )
            
    def validate_fia_legality(self):
        
        dry_compounds = {
            "SOFT",
            "MEDIUM",
            "HARD"
        }
        wet_compounds = {
            "INTERMEDIATE",
            "WET"
        }

        used_wet = self.used_compounds.intersection(
            wet_compounds
        )

        if len(used_wet) > 0:

            self.is_legal_race = True

            return True

        used_dry = self.used_compounds.intersection(
            dry_compounds
        )

        if len(used_dry) >= 2:

            self.is_legal_race = True

        else:

            self.is_legal_race = False

        return self.is_legal_race

    def log_event(self, message):

        self.strategy_events.append(message)
        
    def add_stint_record(self, compound, laps):

        self.stint_history.append({

            "stint": self.current_stint,

            "compound": compound,

            "laps": laps
    })