from api.models.simulation.rival_driver import (
    create_rival_driver
)


def create_rival_pool():

    return [

        create_rival_driver(

            name="HAM",
            
            team="Mercedes",

            pace_offset=-0.10,

            strategy=[
                ("MEDIUM", 21),
                ("HARD", 36)
            ]
        ),

        create_rival_driver(

            name="NOR",
            
            team = "McLaren",

            pace_offset=-0.05,

            strategy=[
                ("MEDIUM", 24),
                ("HARD", 33)
            ]
        ),

        create_rival_driver(

            name="LEC",
            
            team = "Ferrari",

            pace_offset=-0.05,

            strategy=[
                ("SOFT", 18),
                ("HARD", 39)
            ]
        )
    ]