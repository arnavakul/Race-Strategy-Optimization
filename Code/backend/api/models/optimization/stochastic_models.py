#uncertainity engine. 
#Generate those small uncertainties.

import random

from api.models.simulation.simulation_config import (
    SIMULATION_CONFIG
)

class StochasticModels: 
    
    @staticmethod
    def sample_driver_variation() -> float:
        sigma = SIMULATION_CONFIG[
            "driver_variation_sigma"
        ]        
        return random.gauss(0.0, sigma)
    
    @staticmethod
    def sample_tyre_variation() -> float:

        sigma = SIMULATION_CONFIG[
            "tyre_variation_sigma"
        ]

        return random.gauss(0.0, sigma)

    @staticmethod
    def sample_pitstop_noise() -> float:

        sigma = SIMULATION_CONFIG[
            "pitstop_variation_sigma"
        ]

        noise = random.gauss(0.0, sigma)

        return max(
            -1.0,
            min(1.0, noise)
        )
