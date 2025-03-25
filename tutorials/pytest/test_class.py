# https://docs.pytest.org/en/stable/explanation/goodpractices.html#test-discovery
# pytest will find classes that start with `Test`, and then find methods inside the classes that start with `test`
# Class cannot have __init__ method

# Grouping tests can be beneficial for
    # Test organization
    # Sharing fixtures for tests only in that particular class
    # Applying marks at the class level and having them implicitly apply to all tests

# https://docs.pytest.org/en/stable/explanation/fixtures.html
# https://docs.pytest.org/en/stable/how-to/mark.html


class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x
    
    def test_two(self):
        x = "hello"
        assert hasattr(x, "check")