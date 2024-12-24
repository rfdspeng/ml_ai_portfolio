### Ex 1
def shout(text):
    return text.upper()

print(shout("hello"))
yell = shout
print(yell("hello"))

print(type(shout))

### Ex 2
def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def greet(func, text):
    print(func(text))

text = "who are you and what are you doing here?"
greet(shout, text)
greet(whisper, text)

### Ex 3
def create_adder(x):
    def adder(y):
        return x+y
    return adder

add15 = create_adder(15)
print(add15(10))

### Decorators

def print_args(p, *args, **kwargs):
    print(f"p: {p}")
    print(f"Position arguments: {args}")
    print(f"Keyword arguments: {kwargs}")

print_args(0, 1, 2, 3, "hello", name="Bob", age=30)

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
    # time.sleep(2)
    print(math.factorial(num))

exec_time = factorial(10)
print(f"Execution time = {exec_time} seconds")

def factorial2(num):
    # time.sleep(2)
    print(math.factorial(num))

factorial2 = calculate_time(factorial2)
exec_time = factorial2(10)
print(f"Execution time = {exec_time} seconds")

### Chaining decorators

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