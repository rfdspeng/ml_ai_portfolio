# Python

* Understanding what Python is
* How do programming languages work to control the underlying hardware? Scripting language, compiled language, etc.
* Review all Python data structures (list, tuple, set, dict)
    * collections library adds more data structures
* Review all built-in Python functions, like `sorted`, `len`, `sum`, `print` (with unpacking), `isinstance`, `zip`, `input`, `eval`, `any`, `all`
* Review all Python keywords, like `in`, `and`, `or`
* Review Python data types
* `set`
* `map`, `reduce`, `filter`
* Unpacking/packing
* print with unpacking, sep, end
* list methods
* string methods
* list and string slicing
* dictionary methods
* set methods
* Generators - like a list comprehension but (x for x in y) instead of [x for x in y]
* classes
* bound vs. unbound class methods
* `in` - strings vs lists vs else
* `zip`
* list, dictionary comprehensions
* `yield`
* `nonlocal`, `global`
* Generators, iterators
* `itertools.groupby`
* lambda functions
* `getattr`
* `__sub__` and other dunder methods. Instance method can return another instance of class? Yes.
    * operator overloading
* regex
* Objects - attributes, methods, properties

Chunking a string into equal-length chunks: `zip(*[iter(string)] * k)`

## Built-in functions

https://docs.python.org/3/library/functions.html

## Packages and modules

https://docs.python.org/3/reference/import.html
* `__name__`
* `__file__`
* `repr`

## Classes

https://docs.python.org/3/tutorial/classes.html

* Classes bundle data and functionality
* Creates a new _type_ of object and allows new _instances_ of that type to be made
* Each instance can have attributes (aka data members) attached for maintaining its state
* Each instance can have methods (aka member functions) for modifying its state. Methods are declared with an explicit first argument representing the object (`self`), which is provided implicitly by the call.
* Collectively, attributes and methods may be called class members
* Allows multiple base classes
* Derived class can override any methods of its base class(es)
* A method can call the method of a base class with the same name
* Classes themselves are objects, which provides semantics for importing and renaming
* Built-in types can be used as base classes
* Most built-in operators with special syntax (arithmetic operators, subscripting, etc.) can be redefined for class instances

### Names and objects

* Objects have individuality, and multiple names (in multiple scopes) can be bound to the same object. This is known as aliasing in other languages.
* Not relevant for immutable basic types (numbers, strings, tuples), but applies for mutable objects like lists, dictionaries, and most others
* Usually benefits the program, since aliases behave like pointers: passing an object is cheap since only a pointer is passed. If a function modifies an object passed as an argument, the caller will see the change

### Python scopes and namespaces

* _Namespace_: a mapping from names to objects. Most namespaces are currently implemented as Python dictionaries.
* Example namespaces
    * Built-in names containing functions such as `abs()` and built-in exception names
    * Global names in a module
    * 

### ASLKF

`__name`: leading double underscore prevents naming conflicts in inheritance. Triggers name mangling by the Python interpreter - the attribute or method name is automatically transformed to include the class name to prevent subclasses from accidentally overriding it. Accessing `__name` from outside the class results in `AttributeError` unless you use the mangled name `_ClassName__name`.

static method

## *args, **kwargs

## Multi-line code

## Standard operators

## Slice objects

## f-strings

# Data structures

## Hash tables - add two-sum problem

A hash table is an implementation of an associative array, also known as a dictionary or a map. An associative array maps keys to values. Given a key, a hash table uses a hash function to compute an index, aka a hash code, into an array of buckets or slots from which the corresponding value can be found.

## Stacks - add valid parentheses example

# Big O notation for time and space complexity

## Two sum example
```python
def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_map = {}
        for num_idx, num in enumerate(nums):
            difference = target - num # O(1)
            if difference in num_map: # O(1)
                return [num_idx, num_map[difference]]
            num_map[num] = num_idx # O(1)
```
**Time complexity:**
* Arithmetic operations, dictionary membership check (hash table), and assignments are $O(1)$.
* The loop runs once for each element in `nums`. If the size of `nums` is $n$, the total number of iterations is $n$.
* Since each iteration does $O(1)$ work, the total time complexity is $O(1) \times n = O(n)$.

**Space complexity:** `num_map` stores up to $n$ elements, so the space complexity is $O(n)$.

## Two sum, brute-force example
```python
def twoSum(self, nums: list[int], target: int) -> list[int]:
    for num_idx in range(len(nums)):
        for num_idx2 in range(num_idx+1, len(nums)):
            if nums[num_idx] + nums[num_idx2] == target:
                return [num_idx, num_idx2]
```
**Time complexity:**
* The outer loop runs $n$ times.
* In the worst case, the inner loop runs $n-1$ times, then $n-2$, and so on until $1$.
* In the worst case, the total number of iterations across the two loops is $(n-1) + (n-2) + (n-3) + ... + 2 + 1$, which is equal to $n(n-1) \over 2$.
* Checking the condition in the `if` statement is $O(1)$.
* The total time complexity is then $O\left(\frac{n(n-1)}{2}\right)$, which simplifies to $O(n^2)$.

**Space complexity:** since this doesn't need any additional data structures, the space complexity is $O(1)$.

# Random stuff

`zip`

`sorted`

`*args, **kwargs`