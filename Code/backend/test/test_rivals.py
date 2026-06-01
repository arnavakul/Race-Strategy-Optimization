from api.models.simulation.rival_pool import (
    create_rival_pool
)

from api.models.simulation.rival_race_executor import (
    simulate_rival_lap
)


if __name__ == "__main__":

    rivals = create_rival_pool()

    for lap in range(1, 6):

        print(
            f"\nLAP {lap}"
        )

        for rival in rivals:

            lap_time = simulate_rival_lap(

                rival=rival,

                track="monza_2022",

                current_lap=lap,

                total_laps=57
            )

            print(

                rival["name"],

                round(lap_time, 3),

                round(
                    rival["total_time"],
                    3
                )
            )