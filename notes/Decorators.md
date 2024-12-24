# <u>Python functions are objects</u>

Decorators allow programmers to modify the behavior of a function or class. Decorators wrap a function around another function, extending the functionality of the wrapped function without permanently modifying it.

First, you need to understand that Python functions are first class objects, which means that they can be used or passed as arguments. What does this mean?
* A function is an instance of type `Object`
* You can store a function in a variable
* You can pass a function as a parameter to another function
* You can return a function from a function
* You can store a function in data structures like hash tables, lists, etc.

**Example: treating a function as an object.**
```python
def shout(text):
    return text.upper()

print(shout("hello"))
yell = shout
print(yell("hello"))
```
Output:  
> HELLO  
> HELLO  

Since functions are objects, `yell = shout` creates a new variable `yell` that points to the function object referenced by `shout`.

**Example: passing a function as an argument.**
```python
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def greet(func, text):
    print(func(text))

text = "who are you and what are you doing here?"
greet(shout, text) # pass shout and call it inside greet
greet(whisper, text) # pass whisper and call it inside greet
```
Output:  
> WHO ARE YOU AND WHAT ARE YOU DOING HERE?  
> who are you and what are you doing here?  

**Example: return a function from a function.**
```python
def create_adder(x):
    def adder(y):
        return x+y
    return adder

add15 = create_adder(15)
print(add15(10))
```
Output:  
> 25  

# <u>Decorators</u>

A decorator is a function that takes a function as an argument, does something with it to modify its behavior, and returns the modified function (so it uses all the concepts from the previous examples).

Let's take a look at an example.
```python
import time, math

# Simple decorator to calculate function execution time
# Pass any function (func) into the decorator
def calculate_time(func):

    # This defines how to decorate func
    def decorated_func(*args, **kwargs):
        begin = time.time()
        func(*args, **kwargs)
        end = time.time()
        return end-begin
    
    return decorated_func

# factorial is func
@calculate_time
def factorial(num):
    time.sleep(2)
    print(math.factorial(num))

exec_time = factorial(10)
print(f"Execution time = {exec_time} seconds")
```
Output:  
> 3628800  
> Execution time = 2.0251359939575195 seconds  

This code is equivalent and explicitly shows what the decorator syntax is doing:
```python
def factorial2(num):
    time.sleep(2)
    print(math.factorial(num))

factorial2 = calculate_time(factorial2)
exec_time = factorial2(10)
print(f"Execution time = {exec_time} seconds")
```

**You can chain decorators:**
```python
def decor1(func):
    def inner():
        x = func()
        return x*x
    return inner

def decor2(func):
    def inner():
        x = func()
        return x*2
    return inner

# This is equivalent to num1 = decor1(decor2(num1))
@decor1
@decor2
def num1():
    return 10

# This is equivalent to num2 = decor2(decor1(num2))
@decor2
@decor1
def num2():
    return 10

print(num1())
print(num2())
```
Output:  
> 400  
> 200  