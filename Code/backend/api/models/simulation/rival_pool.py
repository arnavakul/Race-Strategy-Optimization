from api.models.simulation.rival_driver import (
    create_rival_driver
)


def create_rival_pool():

    return [

        create_rival_driver(

            name="VER",

            pace_offset=-0.25,

            strategy=[
                ("MEDIUM", 21),
                ("HARD", 36)
            ]
        ),

        create_rival_driver(

            name="NOR",

            pace_offset=-0.10,

            strategy=[
                ("MEDIUM", 24),
                ("HARD", 33)
            ]
        ),

        create_rival_driver(

            name="LEC",

            pace_offset=-0.05,

            strategy=[
                ("SOFT", 18),
                ("HARD", 39)
            ]
        )
    ]