#rival driver sim

def create_rival_driver(
    name,
    team,
    pace_offset,
    strategy
):
    return {
        "name": name,
        
        "team":team,
        
        "pace_offset": pace_offset,
        
        "strategy": strategy,
        
        "current_stint": 0,

        "current_compound": strategy[0][0],

        "current_tyre_age": 0,

        "pitstops": 0,

        "total_time": 0.0,

        "finished": False
    }