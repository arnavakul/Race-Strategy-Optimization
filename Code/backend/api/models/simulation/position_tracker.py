#position tracking engine 

#creates a engine or a timing table: 

# What this does

# Suppose:

# our_time = 5050

# VER = 5040
# NOR = 5048
# LEC = 5054

# It creates:

# [
#     {"driver":"PLAYER","total_time":5050},
#     {"driver":"VER","total_time":5040},
#     {"driver":"NOR","total_time":5048},
#     {"driver":"LEC","total_time":5054}
# ]


def build_timing_table(our_total_time,rivals):
    timing_table = []
    
    timing_table.append(
        {
            "driver":"PLAYER",
            "total_time":our_total_time
        }
    )
    
    for rival in rivals:
        
        timing_table.append(
            {
                "driver": rival["name"],
                "total_time": rival["total_time"]
            }
        )
    
    return timing_table


#checking for the positions 

# What this does

# Sorts:

# 5040
# 5048
# 5050
# 5054

# into:

# P1 VER
# P2 NOR
# P3 PLAYER
# P4 LEC

def calculate_positions(our_total_time, rivals):
    
    timing_table = build_timing_table(
        our_total_time,rivals
    )
    
    timing_table.sort(
        key=lambda x: x["total_time"]
    )
    
    for position, car in enumerate(timing_table,start=1):
        car["position"] = position
    return timing_table

#Helper function to get the position of the player.
def get_player_position(timing_table):
    
    for car in timing_table:
        
        if car["driver"] == "PLAYER":
            
            return car["position"]
    return None

#Get the details of the race_leader
def get_race_leader(
    timing_table
):

    return timing_table[0]["driver"]

# Working Example
# Leader:5040

# Player:5050

# Return:10 sec

# Meaning:10 sec behind leader

def gap_to_leader(timing_table):
    
    leader_time = timing_table[0]["total_time"]
    
    player_time = None
    
    for car in timing_table:
        
        if car["driver"] == "PLAYER":
            
            player_time = car["total_time"]
            
            break
    
    return(
        player_time - leader_time
    )



#gives the gap ahead to the car
def gap_to_car_ahead(timing_table):
    
    for i, car in enumerate(timing_table):
        
        if car["driver"] == "PLAYER":
            if i==0:
                
                return 0.0
            
            return (
                car["total_time"] - timing_table[i-1]["total_time"]
            )
    return None


def gap_to_car_behind(timing_table):
    
    for i, car in enumerate(
        timing_table
    ):
        
        if car["driver"] == "PLAYER":
            
            if i== len(timing_table) - 1:
                
                return 0.0
            
            return(
                timing_table[i+1]["total_time"] - car["total_time"]
            )
    return None

if __name__ == "__main__":

    rivals = [

        {
            "name":"VER",
            "total_time":5040
        },

        {
            "name":"NOR",
            "total_time":5048
        },

        {
            "name":"LEC",
            "total_time":5054
        }
    ]

    table = calculate_positions(
        5050,
        rivals
    )

    print(table)
    
    print(
        "Leader:",
        get_race_leader(
            table
        )
    )

    print(
        "Player Position:",
        get_player_position(
            table
        )
    )

    print(
        "Gap Leader:",
        gap_to_leader(
            table
        )
    )

    print(
        "Gap Ahead:",
        gap_to_car_ahead(
            table
        )
    )

    print(
        "Gap Behind:",
        gap_to_car_behind(
            table
        )
    )