import pytest

def wasteful_func():
    a = [0] * int(1e6)
    b = [0] * int(2e6)
    del b
    return a

# @pytest.mark.limit_memory("22 MB")
def test_array_allocation() -> None:
    """
    Demonstrate allocating and releasing memory.
    
    See the profile_memory make target.
    """
    large_list = wasteful_func()
    assert len(large_list) == 1e6