# <u>Context managers</u>
Use a context manager to acquire and release resources, e.g. opening and closing a file, locking and unlocking access to a mutable variable, opening and closing a database connection, creating and cleaning up temporary directories. Context managers are important for making sure that the resources are properly acquired and released even if exceptions occur in the intervening code block (acquire resource -> intervening code block -> release resource).

The `with` statement is the most popular way to use context managers.

This code opens `"some_file"` -> writes to it -> closes it.
```python
with open("some_file", "w") as file:
    file.write("Hola!")
```

Which is equivalent to this:
```python
file = open("some_file", "w")
try:
    file.write("Hola!")
finally:
    file.close()
```

## <u>Implementing a context manager as a class</u>

To better understand how it works, let's implement a file-opening context manager as a class.
```python
# File is our context manager class
# A context manager is required to have __enter__ and __exit__ methods
class File:
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        print("Entering context...")
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        print("Exited context.")

with File("sample.txt", "a") as file:
    file.write("Implementing a context manager as a class\n")
```

So what happens when we use `with` with `File`?
1. `File("sample.txt", "a")` instantiates the `File` context manager
2. The `with` statement stores the `__exit__` method of `File`
3. `with` calls the `__enter__` method. In our example, `__enter__` returns the file object, which is passed to the variable `file`.
4. The code block happens (in our case, we write to `file`)
5. `with` calls the stored `__exit__` method. In this case, `__exit__` closes the file.

## <u>Handling exceptions</u>

If an exception occurs in the code block, Python passes the `type`, `value`, and `traceback` of the exception to the `__exit__` method, which allows you to decide how to handle the exception and exit the context.

Let's force an exception in our example:
```python
with File("sample.txt", "a") as file:
    file.unknown_method()
```

This raises an `AttributeError: '_io.TextIOWrapper' object has no attribute 'unknown_method'`. How do we fix this?

When an exception occurs, `with` will raise an exception unless `__exit__` returns `True`. Our `__exit__` method returns `None` (since there is no `return` statement). We can handle the exception by simply adding `return True`:
```python
def __exit__(self, type, value, traceback):
    self.file_obj.close()
    print("Exited context.")
    return True
```

## <u>Implementing a context manager as a generator</u>

We can also use `contextlib.contextmanager` and a generator function to implement a context manager.
```python
from contextlib import contextmanager

@contextmanager # this decorator turns open_file into a contextlib._GeneratorContextManager
def open_file(name):
    print("Entering context...")
    f = open(name, "a")
    try:
        yield f # yield turns open_file into a generator function
    finally:
        f.close()
        print("Exited context.")

with open_file("sample.txt") as file:
    file.write("Implementing a context manager as a generator\n")
```

Everything before `yield` is executed as the `__enter__` method; everything after `yield` is executed as the `__exit__` method.