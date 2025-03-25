# pytest provides builtin fixtures/function arguments to request arbitrary resources, like a unique temporary directory
# List the name tmp_path in the test function signature and 
# pytest will lookup and call a fixture factory to create the resource before performing the test function call. 
# Before the test runs, pytest creates a unique-per-test-invocation temporary directory
def test_needsfiles(tmp_path):
    print(tmp_path)
    assert 0