def func(x):
    return x+1

# pytest will find all files of the form test_*.py or *_test.py
# pytest will find functions that start with `test` prefix
# https://docs.pytest.org/en/stable/explanation/goodpractices.html#test-discovery
def test_answer():
    assert func(3) == 5