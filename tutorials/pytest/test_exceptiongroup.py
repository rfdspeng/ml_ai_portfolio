import pytest

def f():
    raise ExceptionGroup(
        "Group message",
        [
            RuntimeError(),
        ],
    )

# Assert that an expected exception is part of a raised ExceptionGroup
def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        f()
    
    assert excinfo.group_contains(RuntimeError)
    assert not excinfo.group_contains(TypeError)