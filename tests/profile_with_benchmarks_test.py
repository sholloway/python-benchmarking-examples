from line_profiler import profile
import pytest

from cProfile import Profile
from pstats import SortKey, Stats
from random import uniform
from time import sleep

from examples.types import TimeInSec


def numeric_process() -> None:
    initial_data: list[float] = []

    for _ in range(10):
        calculation: float = perform_calculation()
        initial_data.append(calculation)

    doubled_values = [2 * value for value in initial_data]

    return doubled_values


def perform_calculation() -> None:
    wait_time: TimeInSec = uniform(0.05, 0.1)
    sleep(wait_time)
    return wait_time


def test_profile_make_numbers() -> None:
    """
    Demonstrate manually profiling a function with cProfile.
    """
    with Profile() as profile:
        numeric_process()
        (Stats(profile).strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats())


@pytest.mark.benchmark(group="Making Numbers", disable_gc=True)
def test_benchmark_make_numbers(benchmark) -> None:
    """
    Demonstrate using pytest-benchmark with cProfile.

    Note: See the Makefile target "profile_benchmark"
    """
    benchmark(numeric_process)
