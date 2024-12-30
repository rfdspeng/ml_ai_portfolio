# <u>`yield`</u>

The `yield` statement turns a Python function into a generator function. What does this mean?

A generator function is really an object of type `<class 'generator'>`. A generator automatically implements the `__iter__()` and `__next__()` methods, which makes it an iterator. This means you can use a generator in a for loop or call `next()` on it.

How does this work? `return` terminates the execution of a function, but `yield` only pauses it. Each time you call the function, which calls `__next__()`, the function resumes until it hits the next `yield`, at which point it pauses again.

We'll look at two examples, one where `yield` returns a value and one where `yield` returns nothing.

Number generator example:
```python
### Code 
def number_generator(x): # generator definition
    for i in range(x):
        yield i
    return "No more numbers"

numgen = number_generator(5) # generator object
print(type(numgen))
for i in numgen: # iterate using for loop
    print(i)

numgen = number_generator(5)
try:
    while True:
        print(next(numgen)) # iterate using next()
except StopIteration as e:
    print(e.value)
```
Output:
> <class 'generator'>  
> 0  
> 1  
> 2  
> 3  
> 4  
> 0  
> 1   
> 2  
> 3  
> 4  
> No more numbers  

Simple example to illustrate execution flow:
```python
def yield_func():
    print("Before yield")
    yield
    print("After yield")
    return "I'm done"

myfunc = yield_func()

for _ in myfunc:
    pass
```
Output:  
> Before yield  
> After yield  
> Before yield  
> After yield  
> I'm done  

Some notes:
* `yield` with no value is the same as `yield None`
* When the generator hits `return` or the end of the function, it throws a `StopIteration` exception (in other words, `return` with no value and no `return` are the same). You can optionally specify a `return` value, which shows up as `StopIteration.value`.
* Generator functions are one-time iterators; once exhausted, they need to be re-initialized to use them again