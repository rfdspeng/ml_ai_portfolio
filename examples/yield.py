"""
Number generator example
"""

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

"""
yield vs. return example
"""
def yield_func():
    print("Before yield")
    yield
    print("After yield")
    return "I'm done"

myfunc = yield_func()

for _ in myfunc:
    pass

myfunc = yield_func()
try:
    while True:
        next(myfunc)
except StopIteration as e:
    print(e.value)

print(dir(myfunc))