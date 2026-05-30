from api.models.simulation.tyre_set_model import (
    create_tyre_set
)

for i in range(10):

    tyre = create_tyre_set(
        "SOFT"
    )

    print(
        tyre["performance_offset"]
    )