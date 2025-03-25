https://realpython.com/async-io-python/: this article covers 3 things:
1. Asynchronous IO (async IO): a language-agnostic paradigm (model) that has implementations across a host of programming languages
2. `async`/`await`: two Python keywords that are used to define **coroutines**
3. `asyncio`: the Python packages that provides a foundation and API for running and managing coroutines

**Coroutines**, specialized generator functions, are the heart of async IO in Python.

# <u>The 10,000-foot view of async IO</u>

Multiprocessing, threading, parallelism, concurrency - where does async IO fit in?

**Parallelism** means performing multiple operations at the same time. **Multiprocessing** is one way to effect parallelism by spreading tasks over a computer's CPUs or cores. Multiprocessing is well-suited for CPU-bound tasks like mathematical computations.

**Concurrency** is slightly broader than parallelism. It suggests that multiple tasks can run in an overlapping manner. (Concurrency does not imply parallelism.)

**Threading** is a **concurrent execution model** where multiple **threads** take turns executing tasks. One process can contain multiple threads. Threading is better for IO-bound tasks where there's a lot of waiting. While one thread is waiting for a task to finish (e.g. reading a file from disk, loading a model, retrieving data from a database), another thread can execute on its task. This is very different from CPU-bound tasks where the processors are actively working the entire time.

To recap, concurrency encompasses both multiprocessing, ideal for CPU-bound tasks, and threading, suited for IO-bound tasks. Multiprocessing is a form of parallelism, with parallelism being a subset of concurrency. The Python standard library has offered longstanding support for both through its `multiprocessing`, `threading`, and `concurrent.futures` packages.

**Async IO** is the latest concurrency design added to CPython (to be clear, async IO already existed), enabled through the `asyncio` package and `async`/`await` keywords. Async IO is a single-threaded, single-process design: it uses **cooperative multitasking** to give a feeling of concurrency despite using a single thread in a single process. **Coroutines** can be scheduled concurrently, but they're not inherently concurrent. Async IO is closer to threading than multiprocessing, but it's distinct from both.

Here's an analogy for async IO: let's say you have two tasks, studying and doing laundry. The smart way to do both is to start the washer and then study while the machine runs. When the laundry finishes, you take a quick break from studying to move your clothes to the dryer and later fold your clothes and put them away. In this analogy, you are the event loop, coordinating tasks and deciding when to switch focus between waiting and execution. You don't fully commit to either task, but you keep switching attention based on task readiness. For example, you occasionally check the laundry's progress while studying. Without asynchronous IO, laundry would be **blocking** - that is, blocking execution on anything else from the time it starts to the time it finishes (or returns, in a function). You would have to sit by the laundry machines and do nothing until they finish.

One final definition: what does it mean to be **asynchronous**?
* Asynchronous routines are able to "pause" while waiting on their ultimate result and let other routines run in the meantime
* Asynchronous code, through this "pausing" mechanism, facilitates concurrent execution. Asynchronous code gives the look and feel of concurrency.

![Concurrency parallelism diagram](https://realpython.com/cdn-cgi/image/width=504,format=auto/https://files.realpython.com/media/Screen_Shot_2018-10-17_at_3.18.44_PM.c02792872031.jpg)

# <u>The `asyncio` package and `async`/`await`</u>

**Async IO is all about coroutines. In Python, a coroutine is a specialized generator function; a coroutine can suspend its execution before reaching `return` and pass control to another coroutine for some time.**

This is the `Hello World` example of async IO:
```python
import asyncio
import time
import sys

if len(sys.argv) > 1:
    async_flag = sys.argv[1]
else:
    async_flag = False

if async_flag: # asynchronous code
    async def count(): # coroutine
        print("One")
        await asyncio.sleep(1)
        print("Two")
        await asyncio.sleep(1)

    async def main(): # coroutine
        await asyncio.gather(count(), count(), count()) # use gather() to run coroutines concurrently

else: # synchronous code
    def count():
        print("One")
        time.sleep(1)
        print("Two")
        time.sleep(1)

    def main():
        count()
        count()
        count()

s = time.perf_counter()
if async_flag:
    asyncio.run(main()) # run() starts an event loop to run the passed coroutine and shuts down the event loop after coroutine finishes
else:
    main()
elapsed = time.perf_counter() - s
print(f"Program executed in {elapsed:0.2f} seconds.")
```
For `async_flag == False`, output =  
> One  
> Two  
> One  
> Two  
> One  
> Two  
> Program executed in 6.14 seconds.  

For `async_flag == True`, output =  
> One  
> One  
> One  
> Two  
> Two  
> Two  
> Program executed in 1.00 seconds.  

`time.sleep` is a stand-in for time-consuming blocking code, while `asyncio.sleep` is a stand-in for time-consuming non-blocking code. In other words, `asyncio.sleep` is a coroutine that can be `await`-ed. `asyncio.run` starts up the event loop (aka coordinator), which talks to each task (or call to `count`). When each task reaches `await asyncio.sleep(1)`, it yells up to the event loop and gives control back to it, saying, "I'm going to be sleeping for 1 second. Go ahead and let something else meaningful be done in the meantime."

## <u>The rules of async IO</u>

* `async def` introduces either a native coroutine or an asynchronous generator
* `await` passes function control back to the event loop (and suspends execution of the surrounding coroutine.) In the code below, `await` tells the event loop to suspend execution of `g` until `f` returns and to go run something else in the meantime.
```python
async def g():
    # Pause here and come back to g() when f() is ready
    r = await f()
    return r
```
* A function defined with `async def` may use `await`, `return`, or `yield`, but these are all optional
    * Using `await` and/or `return` creates a coroutine. To call a coroutine, you must `await` it (call it using `await`) to get its results.
    * Using `yield` is less common and creates an asynchronous generator, which you can iterate over with `async for`
    * Using `yield from` raises a `SyntaxError`
* Using `await` outside of a coroutine raises a `SyntaxError`
```python
async def f(x):
    y = await z(x)  # OK - `await` and `return` allowed in coroutines
    return y

async def g(x):
    yield x  # OK - this is an async generator

async def m(x):
    yield from gen(x)  # No - SyntaxError

def m(x):
    y = await z(x)  # Still no - SyntaxError (no `async def` here)
    return y
```

When you `await f()`, `f()` must be an object that is awaitable. This can be (1) another coroutine or (2) an object with an `__await__` method that returns an iterator. If you're writing a program, for the majority of the time, `f` will be a coroutine.

