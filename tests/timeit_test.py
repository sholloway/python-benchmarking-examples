import time
import timeit
from typing import Sequence

import pandas as pd
from great_tables import GT, md, html
import numpy as np
import matplotlib.pyplot as plt

from tests.fixtures import (
    MISSING_PERSON,
    create_random_names,
    random_names,
    perf_data_a,
    perf_data_b,
)

from examples.types import RandomNames, TimeInNS, TimeInSec


def test_default_timeit(random_names: RandomNames) -> None:
    """
    Demonstrate how to leverage timeit using the default timer.
    This uses time.perf_counter() to determine how long a code
    snippet took to run over a series of iterations.
    """
    # 1. Unpack the random names for readability.
    # These are added to the scope below.
    random_names_list, random_names_set = random_names

    # 2. Build the scope for the benchmark.
    scope = dict(globals())
    scope.update(locals())

    # 3. Construct a timer.
    search_list_timer = timeit.Timer(
        stmt="assert MISSING_PERSON not in random_names_list", globals=scope
    )

    # 4. Run timeit and write the results to STDOUT.
    # fmt: off
    print("\nTest Approach: Using Timeit with Default Settings")
    print(f"Sequence Search Run 1x:      {search_list_timer.timeit(number=1)} seconds")
    print(f"Sequence Search Run 1000x:   {search_list_timer.timeit(number=1000)} seconds")
    print(f"Sequence Search Run 10,000x: {search_list_timer.timeit(number=10_000)} seconds")
    # fmt: on


def test_precise_timeit(random_names: RandomNames) -> None:
    """
    Demonstrate how to leverage timeit using a more precise timer.
    This uses time.perf_counter_ns() to determine how long a code
    snippet took to run over a series of iterations.
    """
    # 1. Unpack the random names for readability.
    # These are added to the scope below.
    random_names_list, random_names_set = random_names

    # 2. Build the scope for the benchmark.
    scope = dict(globals())
    scope.update(locals())

    # 3. Construct a timer.
    search_list_timer = timeit.Timer(
        stmt="assert MISSING_PERSON not in random_names_list",
        globals=scope,
        timer=time.perf_counter_ns,
    )

    # 4. Run timeit and write the results to STDOUT.
    # fmt: off
    print("\nTest Approach: Using Timeit with time.perf_counter_ns()")
    print(f"Sequence Search Run 1x:      {search_list_timer.timeit(number=1):,} nanoseconds")
    print(f"Sequence Search Run 1000x:   {search_list_timer.timeit(number=1000):,} nanoseconds")
    print(f"Sequence Search Run 10,000x: {search_list_timer.timeit(number=10_000):,} nanoseconds")
    # fmt: on


def test_bound_timeit(random_names: RandomNames) -> None:
    """
    Demonstrate how to determine how many times a piece of code can run in a fixed interval
    using timeit.autorange().
    """
    # 1. Unpack the random names for readability.
    # These are added to the scope below.
    random_names_list, random_names_set = random_names

    # 2. Build the scope for the benchmark.
    scope = dict(globals())
    scope.update(locals())

    # 3. Construct a timer.
    search_list_timer = timeit.Timer(
        stmt="assert MISSING_PERSON not in random_names_list",
        globals=scope,
        timer=time.perf_counter_ns,
    )

    # 4. Run timeit with autorange. This runs the timed code
    #    repeatedly until at least 0.2 seconds elapses.
    num_iter, total_time = search_list_timer.autorange()

    print("\nTest Approach: Using Timeit with autorange()")
    print(f"Sequence Search Run {num_iter}x: {total_time:,} nanoseconds")


def test_visualize_timeit_results() -> None:
    """
    Demonstrate creating a benchmark over increasing scale.

    Run timeit on increasingly larger data volumes.
    Visualize the results using a 2D plot.
    """
    print("\nTest Approach: Testing with Timeit on Increasing Orders of Magnitude")
    num_iterations: int = 500
    min_samples: int = 100
    max_samples: int = 100_000
    increment_size: int = 1_000

    # 1. Create the data sets.
    print("\nCreating Samples")
    master_samples_list, _ = create_random_names(max_samples)
    print(f"Created {max_samples:,} Samples")

    # 3. Run the Benchmark
    print("Running the Benchmarks\n")
    # Benchmark results is a list of tuples in the form (avg_list_search_time, avg_set_search_time)
    benchmark_results: list[tuple[float, float]] = []
    samples_range = range(min_samples, max_samples, increment_size)

    for size in samples_range:
        print(f"Running benchmark on sample size {size:,}.", end="\r")
        # Get the Sample Set
        samples_list = master_samples_list[:size]
        samples_set = set(samples_list)

        # Build the scope for the benchmark.
        scope = dict(globals())
        scope.update(locals())

        # Construct the Timers
        search_list_timer = timeit.Timer(
            stmt="assert MISSING_PERSON not in samples_list",
            globals=scope,
            timer=time.perf_counter_ns,
        )

        search_set_timer = timeit.Timer(
            stmt="assert MISSING_PERSON not in samples_set",
            globals=scope,
            timer=time.perf_counter_ns,
        )

        # Run the code 10k times each.
        total_search_list_time: TimeInNS = search_list_timer.timeit(
            number=num_iterations
        )
        total_search_set_time: TimeInNS = search_set_timer.timeit(number=num_iterations)

        # Calculate the average time each code snippet took in nanoseconds.
        avg_list_search_time: float = total_search_list_time / num_iterations
        avg_set_search_time: float = total_search_set_time / num_iterations
        benchmark_results.append((avg_list_search_time, avg_set_search_time))

    # 4. Tabulate the Results
    header_fmt = "{:<15} {:<22} {:<15}"
    row_fmt = "{:<15,} {:<22,.2f} {:<20,.2f}"
    print(
        header_fmt.format(
            "Sample Size", "List Search Time (ns)", "Set Search Time (ns)"
        )
    )
    for index, sample_size in enumerate(samples_range):
        row = row_fmt.format(
            sample_size, benchmark_results[index][0], benchmark_results[index][1]
        )
        print(row)

    # 5. Visualize the Results
    sample_sizes = [size for size in samples_range]
    plt.scatter(
        x=sample_sizes,
        y=[result[0] for result in benchmark_results],
        color="blue",
        label="In List",
    )
    plt.scatter(
        x=sample_sizes,
        y=[result[1] for result in benchmark_results],
        color="red",
        label="In Set",
    )
    plt.grid()
    plt.title("Runtime: In List vs In Set")
    plt.xlabel("Data Set Size")
    plt.ylabel("Operation time in nanoseconds")
    plt.legend()
    plt.show()


def test_visualizing_distributions_with_boxplot(
    perf_data_a: Sequence[TimeInNS], perf_data_b: Sequence[TimeInNS]
) -> None:
    """
    Demonstrate how to visualize the performance distribution of a benchmark.

    Given multiple sets of performance data, compare them using a boxplot diagram.
    """
    # 1. Organize the data to display
    data_sets = [perf_data_a, perf_data_b]
    labels = ["A", "B"]
    colors = ["orange", "red"]

    # 2. Create the boxplot visualization.
    fig, ax = plt.subplots()
    bplot = plt.boxplot(
        x=data_sets,
        patch_artist=True,  # Turn on colors
        showfliers=False,
        tick_labels=labels,
    )
    plt.ylabel("Performance Data")

    # 3. Set the colors on the various boxes.
    for box, color in zip(bplot["boxes"], colors):
        box.set_facecolor(color)

    plt.show()


def test_tabulating_distributions(
    perf_data_a: Sequence[TimeInNS], perf_data_b: Sequence[TimeInNS]
) -> None:
    """
    Demonstrate how to create a table that compares the percentiles of multiple benchmarks.
    """
    # 1. Calculate the percentiles to display.
    # Get the percentiles you want to display
    percentiles = [25, 50, 75, 99, 100]
    a_percentiles: list[float] = np.percentile(perf_data_a, percentiles).tolist()
    b_percentiles: list[float] = np.percentile(perf_data_b, percentiles).tolist()

    # 2. Enrich the data by calculating the interquartile (IQR).
    percentiles.append("IQR")
    a_percentiles.append(a_percentiles[2] - a_percentiles[0])
    b_percentiles.append(b_percentiles[2] - b_percentiles[0])

    # 3. Build a data frame with Pandas.
    data = {
        "Percentiles": percentiles,
        "Data A": a_percentiles,
        "Data B": b_percentiles,
    }
    dataframe = pd.DataFrame(data)

    # 4. Create and stylize the table.
    table = GT(data=dataframe)

    # 5. Display the table.
    table.show()
