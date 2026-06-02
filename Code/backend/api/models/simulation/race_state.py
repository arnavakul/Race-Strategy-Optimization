#It will be the single source for all the strategic races.
#Every major simulation system will read/write from this.

from api.models.simulation.tyre_set_model import (
    create_tyre_set
)

class RaceState:

    def __init__(self):

        self.current_stint = 1

        self.pitstop_count = 0

        self.used_compounds = set()

        self.current_compound = None

        self.current_tyre_age = 0

        self.current_tyre_set = None

        self.is_legal_race = False

        self.stint_history = []

        self.strategy_events = []
        
        self.weather_lock_remaining = 0

        self.tyre_inventory = {

            "SOFT": [

                create_tyre_set("SOFT")

                for _ in range(6)
            ],

            "MEDIUM": [

                create_tyre_set("MEDIUM")

                for _ in range(4)
            ],

            "HARD": [

                create_tyre_set("HARD")

                for _ in range(3)
            ],

            "INTERMEDIATE": [

                create_tyre_set("INTERMEDIATE")

                for _ in range(8)
            ],

            "WET": [

                create_tyre_set("WET")

                for _ in range(6)
            ]
        }

    # Register tyre compound usage
    def register_compound_usage(
        self,
        compound
    ):

        self.used_compounds.add(compound)

        self.current_compound = compound

        self.current_tyre_set = (
            self.get_tyre_set(compound)
        )

    # Register pitstop
    def register_pitstop(self):

        self.pitstop_count += 1

        self.current_stint += 1

        self.current_tyre_age = 0

        # Heat cycle added after stint usage
        if self.current_tyre_set is not None:

            self.current_tyre_set[
                "heat_cycles"
            ] += 1

    # Increase tyre age
    def increment_tyre_age(self):

        self.current_tyre_age += 1

    # Fetch tyre set from inventory
    def get_tyre_set(
    self,
        compound
    ):

        available_sets = self.tyre_inventory[
            compound
        ]

        if len(available_sets) == 0:

            DEBUG_TYRES = False

            if DEBUG_TYRES:

                print(
                    f"\nWARNING: "
                    f"Emergency tyre allocation "
                    f"used for {compound}"
                )

            return create_tyre_set(

                compound=compound,

                freshness=0.85,

                heat_cycles=1,

                used_laps=0
            )

        return available_sets.pop(0)

    # FIA legality validation
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

        # Wet race exemption
        if len(used_wet) > 0:

            self.is_legal_race = True

            return True

        used_dry = self.used_compounds.intersection(
            dry_compounds
        )

        # Dry race requires 2 dry compounds
        if len(used_dry) >= 2:

            self.is_legal_race = True

        else:

            self.is_legal_race = False

        return self.is_legal_race

    # Strategy event logger
    def log_event(
        self,
        message
    ):

        self.strategy_events.append(message)

    # Store stint history
    def add_stint_record(
        self,
        compound,
        laps
    ):

        self.stint_history.append({

            "stint": self.current_stint,

            "compound": compound,

            "laps": laps
        })
    def activate_weather_lock(
    self,
    laps=5
    ):
        self.weather_lock_remaining = laps  
    
    def decrement_weather_lock(self):

        if self.weather_lock_remaining > 0:

            self.weather_lock_remaining -= 1
    
    
    