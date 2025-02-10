# <u>Context managers</u>

Notes are based on this tutorial: https://book.pythontips.com/en/latest/context_managers.html

To read more, see [PEP343](https://peps.python.org/pep-0343/) for context managers and [PEP492](https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with) for asynchronous context managers.

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

## <u>Asynchronous context managers</u>

See [PEP492](https://peps.python.org/pep-0492/#asynchronous-context-managers-and-async-with).

An asynchronous context manager simply extends context manager functionality to asynchronous code. Instead of `__enter__` and `__exit__`, an async context manager defines `__aenter__` and `__aexit__` methods that are awaitable - that is, can suspend their execution and resume later.

Example asynchronoux context manager:
```python
class AsyncContextManager:
    async def __aenter__(self):
        await log('entering context')

    async def __aexit__(self, exc_type, exc, tb):
        await log('exiting context')
```

This is the syntax for entering and exiting an asynchronous context manager:
```python
async with EXPR as VAR:
    BLOCK
```
Which is semantically equivalent to
```python
mgr = (EXPR) # parentheses are optional. EXPR must return an async context manager.
aexit = type(mgr).__aexit__ # aexit class method
aenter = type(mgr).__aenter__ # aenter class method

# Call aenter method on the async context manager
# VAR assignment is optional
VAR = await aenter(mgr) 
try:
    BLOCK
except:
    # If the async context manager's aexit method does not properly execute, re-raise the exception caught by except
    if not await aexit(mgr, *sys.exc_info()):
        raise
else:
    await aexit(mgr, None, None, None)
```

As with regular `with` statements, you can specify multiple asynchronous context managers in a single `async with` statement.

`async with` can only be used within an `async def` function.