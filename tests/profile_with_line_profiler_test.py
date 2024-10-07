from random import uniform
from time import sleep
from line_profiler import profile

from examples.types import TimeInSec


@profile
def numeric_process() -> None:
    initial_data: list[float] = []

    for _ in range(10):
        calculation: float = perform_calculation()
        initial_data.append(calculation)

    # fmt: off
    doubled_values = [
        2 * value 
        for value in initial_data
    ]
    return doubled_values
    # fmt: on


def perform_calculation() -> None:
    wait_time: TimeInSec = uniform(0.05, 0.1)
    sleep(wait_time)
    return wait_time


class TestWithLineProfiler:
    def test_line_profiler(self) -> None:
        numeric_process()
