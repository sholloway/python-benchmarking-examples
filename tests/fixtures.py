import numpy as np
import pytest

import random
from typing import Sequence

from faker import Faker
from examples.types import RandomNames, TimeInNS

fake = Faker()

DATA_SET_SIZE: int = 10_000
MISSING_PERSON: str = "John Doe"


def create_random_names(size: int) -> RandomNames:
    data: list[str] = []
    for _ in range(size):
        data.append(fake.name())
    return data, set(data)


# Note that we want to use the same data set in all the tests
# to enable comparing apples to apples.
@pytest.fixture(scope="session")
def random_names() -> RandomNames:
    """
    Generate a data set of random fake names.

    Returns
    The function returns a tuple of the same data represented as
    both a list and set.
    """
    names_seq, names_set = create_random_names(DATA_SET_SIZE)

    # Ensure that we're looking for a value that's not in the data.
    # This is because we want to do a worst case scenario test.
    assert MISSING_PERSON not in names_seq

    return names_seq, names_set


@pytest.fixture(scope="session")
def perf_data_a() -> Sequence[TimeInNS]:
    return np.random.default_rng().normal(loc=100, scale=4, size=200).tolist()


@pytest.fixture(scope="session")
def perf_data_b() -> Sequence[TimeInNS]:
    return np.random.default_rng().gumbel(loc=75, scale=5, size=200).tolist()
