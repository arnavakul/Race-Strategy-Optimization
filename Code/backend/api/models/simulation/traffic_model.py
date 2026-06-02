# Traffic Model

# In F1, traffic means:

# A faster car catches a slower car
# ↓
# Can't use full pace
# ↓
# Dirty air
# ↓
# Tyre overheating
# ↓
# Lap time loss

def calculate_dirty_air_penalty(
    gap_ahead
):

    if gap_ahead is None:
        return 0.0

    if gap_ahead > 2.0:
        return 0.0

    elif gap_ahead > 1.0:
        return 0.15

    elif gap_ahead > 0.5:
        return 0.30

    return 0.50


def in_traffic(
    gap_ahead
):

    if gap_ahead is None:
        return False

    return gap_ahead < 2.0