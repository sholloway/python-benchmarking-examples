import pytest

import time
from typing import Sequence
from faker import Faker

fake = Faker()

MISSING_PERSON: str = "John Doe"

# Define type aliases to improve readability.
type TimeInSec = float
type RandomNames = tuple[Sequence[str], set[str]]


@pytest.fixture
def random_names(size: int) -> RandomNames:
    """
    Generate a data set of random fake names.

    Returns
    The function returns a tuple of the same data represented as
    both a list and set.
    """
    data: list[str] = []
    for _ in range(size):
        data.append(fake.name())
    return data, set(data)


@pytest.mark.parametrize("size", [10000])
def test_clock_time(random_names: RandomNames) -> None:
    """
    Demonstrate manually measuring clock time.
    """
    # 1. Unpack the random names for readability.
    random_names_list, random_names_set = random_names

    # 2. Ensure that we're looking for a value that's not in the data.
    # This is because we want to do a worst case scenario test.
    assert MISSING_PERSON not in random_names_list

    # 3. Measure worst case scenario lookup in the list.
    seq_start_time: TimeInSec = time.time()
    assert MISSING_PERSON not in random_names_list
    seq_stop_time: TimeInSec = time.time()

    # 4. Measure worst case scenario lookup in the set.
    set_start_time: TimeInSec = time.time()
    assert MISSING_PERSON not in random_names_set
    set_stop_time: TimeInSec = time.time()

    seq_search_time = seq_stop_time - seq_start_time
    set_search_time = set_stop_time - set_start_time

    # 5. Assert our intuition that the set search is faster than the list search.
    assert set_search_time < seq_search_time

    # 6. Write the results to STDOUT.
    print("Test: test_clock_time")
    print(f"Sequence Search took: {seq_search_time} seconds")
    print(f"Set Search took: {set_search_time} seconds")
    print(f"Set Search saved {abs(set_search_time - seq_search_time)} seconds.")
