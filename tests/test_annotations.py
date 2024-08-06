import glob
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "example", glob.glob(str(Path(__file__).parent.parent / "examples" / "*.py"))
)
def test_example_runnable(example):
    # Load the example file
    module = compile(open(example).read(), "test", "exec")
    # Execute it to see if it throws any errors
    exec(module)
