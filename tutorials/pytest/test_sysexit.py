import pytest

def f():
    raise SystemExit(1)

# Assert that a certain exception is raised
def test_mytest():
    with pytest.raises(SystemExit):
        f()