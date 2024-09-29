import time
import timeit
import matplotlib.pyplot as plt

from tests.fixtures import MISSING_PERSON, create_random_names, random_names

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
    num_iterations = 1_000
    sample_sizes = [100, 1_000, 10_000, 100_000]
    print("\nTest Approach: Testing with Timeit on Increasing Orders of Magnitude")
    # 1. Create the data sets.
    # fmt: off
    print("\nCreating Samples")
    list_100x, set_100x = create_random_names(100);           print("created sample 1")
    list_1000x, set_1000x = create_random_names(1_000);       print("created sample 2")
    list_10000x, set_10000x = create_random_names(10_000);    print("created sample 3")
    list_100000x, set_100000x = create_random_names(100_000); print("created sample 4")
    # fmt: on

    # 2. Build the scope for the benchmark.
    scope = dict(globals())
    scope.update(locals())

    # 3. Run the Benchmark
    print("Running the Benchmark")
    # Benchmark results is a list of tuples in the form (avg_list_search_time, avg_set_search_time)
    benchmark_results: list[tuple[float, float]] = []
    for size in sample_sizes:
        print(f"Running benchmark on sample size {size:,}.")
        # Construct the Timers
        search_list_timer = timeit.Timer(
            stmt=f"assert MISSING_PERSON not in list_{size}x",
            globals=scope,
            timer=time.perf_counter_ns,
        )

        search_set_timer = timeit.Timer(
            stmt=f"assert MISSING_PERSON not in set_{size}x",
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
    for index, sample_size in enumerate(sample_sizes):
        row = row_fmt.format(
            sample_size, benchmark_results[index][0], benchmark_results[index][1]
        )
        print(row)

    # 5. Visualize the Results
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
