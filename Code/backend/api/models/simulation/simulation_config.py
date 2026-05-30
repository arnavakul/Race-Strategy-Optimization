#This file becomes the master switchboard for stochastic behaviour.

SIMULATION_CONFIG = {

    "enable_stochasticity": True,

    "driver_variation_sigma": 0.10,

    "tyre_variation_sigma": 0.05,

    "pitstop_variation_sigma": 0.30,
    
    # Future Systems

    "enable_weather_randomness": False,

    "enable_sc_randomness": False,

    "enable_vsc_randomness": False
}