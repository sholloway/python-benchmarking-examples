"""
Demonstrate creating a benchmark that compares the performance 
distributions of initializing a list versus initializing a tuple.

Outputs a table with the following columns:
 	min: The fastest round.
 	max: The slowest round
 	mean: The average round
    median: The 50th-percentile.
    StdDev: The standard deviation. Lower values suggest more consistent performance.
    IQR: (Interquartile Range): A statistical measure that represents the range 
        between the first quartile (25th percentile) and the third quartile 
        (75th percentile) of a dataset. 
        A larger IQR could indicate more variability in performance, 
        while a smaller IQR suggests more consistent performance.
    Outliers: Data points that significantly deviate from the rest of the data in a dataset.
    Ops: 1000 operations per second. Higher the better.
    Rounds: The number of times a benchmark round was ran.
    Iterations: The number of iterations per round.
"""

import pytest

init_values = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)


@pytest.mark.benchmark(group="Test Initialization", disable_gc=True)
def test_lists(benchmark):
    """
    Benchmark the performance of calling list((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
    """
    benchmark(list, init_values)


@pytest.mark.benchmark(group="Test Initialization", disable_gc=True)
def test_tuples(benchmark):
    """
    Benchmark the performance of calling tuple((0, 1, 2, 3, 4, 5, 6, 7, 8, 9))
    """
    benchmark(tuple, init_values)
