import time

from examples.types import RandomNames, TimeInNS, TimeInSec
from tests.fixtures import MISSING_PERSON, random_names


def test_stop_watch(random_names: RandomNames) -> None:
    """
    Demonstrate manually measuring clock time.
    """
    # 1. Unpack the random names for readability.
    random_names_list, random_names_set = random_names

    # 2. Measure worst case scenario lookup in the list.
    seq_start_time: TimeInSec = time.time()
    assert MISSING_PERSON not in random_names_list
    seq_stop_time: TimeInSec = time.time()
    seq_search_time: TimeInSec = seq_stop_time - seq_start_time

    # 3. Measure worst case scenario lookup in the set.
    set_start_time: TimeInSec = time.time()
    assert MISSING_PERSON not in random_names_set
    set_stop_time: TimeInSec = time.time()
    set_search_time: TimeInSec = set_stop_time - set_start_time

    # 4. Assert our intuition that the set search is faster than the list search.
    assert set_search_time < seq_search_time

    # 5. Write the results to STDOUT.
    print("\nTest Approach: Simple Stopwatch With time.time()")
    print(f"Sequence Search took: {seq_search_time} seconds")
    print(f"Set Search took: {set_search_time} seconds")
    print(f"Set Search saved {abs(set_search_time - seq_search_time)} seconds.")


def test_better_stop_watch(random_names: RandomNames) -> None:
    """
    Demonstrate manually measuring clock time but using a more precise clock
    and eliminating floating point errors.
    """
    # 1. Unpack the random names for readability.
    random_names_list, random_names_set = random_names

    # 2. Measure worst case scenario lookup in the list.
    seq_start_time: TimeInNS = time.perf_counter_ns()
    assert MISSING_PERSON not in random_names_list
    seq_stop_time: TimeInNS = time.perf_counter_ns()
    seq_search_time: TimeInNS = seq_stop_time - seq_start_time

    # 3. Measure worst case scenario lookup in the set.
    set_start_time: TimeInNS = time.perf_counter_ns()
    assert MISSING_PERSON not in random_names_set
    set_stop_time: TimeInNS = time.perf_counter_ns()
    set_search_time: TimeInNS = set_stop_time - set_start_time

    # 5. Assert our intuition that the set search is faster than the list search.
    assert set_search_time < seq_search_time

    # 6. Write the results to STDOUT.
    print("\nTest Approach: Better Stopwatch with time.perf_counter_ns()")
    print(f"Sequence Search took: {seq_search_time:,} nanoseconds")
    print(f"Set Search took: {set_search_time:,} nanoseconds")
    print(f"Set Search saved {abs(set_search_time - seq_search_time):,} nanoseconds.")


def test_process_time(random_names: RandomNames) -> None:
    """
    Demonstrate manually measuring time spent in the Python process.
    This ignores time spent sleeping and time spent while the CPU is doing other things.
    """
    # 1. Unpack the random names for readability.
    random_names_list, random_names_set = random_names

    # 2. Measure worst case scenario lookup in the list.
    seq_start_time: TimeInNS = time.process_time_ns()
    assert MISSING_PERSON not in random_names_list
    seq_stop_time: TimeInNS = time.process_time_ns()
    seq_search_time: TimeInNS = seq_stop_time - seq_start_time

    # 3. Measure worst case scenario lookup in the set.
    set_start_time: TimeInNS = time.process_time_ns()
    assert MISSING_PERSON not in random_names_set
    set_stop_time: TimeInNS = time.process_time_ns()
    set_search_time: TimeInNS = set_stop_time - set_start_time

    # 5. Assert our intuition that the set search is faster than the list search.
    assert set_search_time < seq_search_time

    # 6. Write the results to STDOUT.
    print("\nTest Approach: Measure Code Efficiency with time.process_time_ns()")
    print(f"Sequence Search took: {seq_search_time:,} nanoseconds")
    print(f"Set Search took: {set_search_time:,} nanoseconds")
    print(f"Set Search saved {abs(set_search_time - seq_search_time):,} nanoseconds.")
