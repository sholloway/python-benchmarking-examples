
from examples.hello import Greeter

class TestHello:
    def test_setup(self) -> None:
        greeter = Greeter()
        assert greeter.introduction() == "Hello"