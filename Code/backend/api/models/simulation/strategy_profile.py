# Responsible for:
# - aggressive strategies
# - conservative strategies
# - balanced strategies
# - pit decision weighting

STRATEGY_PROFILES = {

    "AGGRESSIVE": {

        "undercut_chance": 0.85,

        "extend_chance": 0.10
    },

    "BALANCED": {

        "undercut_chance": 0.50,

        "extend_chance": 0.35
    },

    "CONSERVATIVE": {

        "undercut_chance": 0.20,

        "extend_chance": 0.70
    }
}