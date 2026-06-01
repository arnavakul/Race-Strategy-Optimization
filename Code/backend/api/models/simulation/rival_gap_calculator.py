def calculate_real_gap(

    our_total_time,

    rival_total_time
):

    return (

        rival_total_time

        - our_total_time
    )

def get_closest_rival_gap(
    our_total_time,
    rivals
):

    gaps = []

    for rival in rivals:

        gap = (

            rival["total_time"]

            - our_total_time
        )

        gaps.append(
            gap
        )

    if not gaps:

        return 999.0

    return min(

        gaps,

        key=lambda x: abs(x)
    )