import statistics

from api.models.optimization.stochastic_models import StochasticModels


def print_stats(name, samples):
    print(f"\n{name}")
    print("-" * 50)
    print(f"Samples : {len(samples)}")
    print(f"Mean    : {statistics.mean(samples):.5f}")
    print(f"Std Dev : {statistics.stdev(samples):.5f}")
    print(f"Min     : {min(samples):.5f}")
    print(f"Max     : {max(samples):.5f}")


def test_driver_variation():
    samples = [
        StochasticModels.sample_driver_variation()
        for _ in range(1000)
    ]

    print_stats("DRIVER VARIATION", samples)


def test_tyre_variation():
    samples = [
        StochasticModels.sample_tyre_variation()
        for _ in range(1000)
    ]

    print_stats("TYRE VARIATION", samples)


def test_pitstop_noise():
    samples = [
        StochasticModels.sample_pitstop_noise()
        for _ in range(1000)
    ]

    print_stats("PITSTOP VARIATION", samples)


if __name__ == "__main__":
    test_driver_variation()
    test_tyre_variation()
    test_pitstop_noise()