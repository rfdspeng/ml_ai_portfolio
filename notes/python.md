# Modules

https://docs.python.org/3/tutorial/modules.html



# Classes

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

## Names and objects

* Objects have individuality, and multiple names (in multiple scopes) can be bound to the same object. This is known as aliasing in other languages.
* Not relevant for immutable basic types (numbers, strings, tuples), but applies for mutable objects like lists, dictionaries, and most others
* Usually benefits the program, since aliases behave like pointers: passing an object is cheap since only a pointer is passed. If a function modifies an object passed as an argument, the caller will see the change

## Python scopes and namespaces

* _Namespace_: a mapping from names to objects. Most namespaces are currently implemented as Python dictionaries.
* Example namespaces
    * Built-in names containing functions such as `abs()` and built-in exception names
    * Global names in a module
    * Local names in a function invocation
    * The set of attributes of an object also form a namespace
* There is no relation between names in different namespaces, e.g. two different modules may both define a function `maximize` without confusion. Users of the modules must prefix it with the module name.
* An attribute is any name following a dot
    * In `z.real`, `real` is an attribute of object `z`
    * References to names in modules are attribute references. In `modname.funcname`, `modname` is a module object and `functname` is an attribute of it. The module's attributes and the global names defined in the module share the same namespace!
    * Attributes may be read-only or writable. For an example writable case, `modname.the_answer = 42`. Writable attributes may be deleted with `del`, e.g. `del modname.the_answer` will remove `the_answer` from `modname`.
* Namespaces are created at different moments and have different lifetimes
    * Built-in namespace is created when the Python interpreter starts up and is never deleted
    * Global namespace for a module is created when the module definition is read in and normally lasts until the interpreter quits
    * The statements executed by the top-level invocation of the interpreter (either from a script or interactively) are considered part of a module called `__main__`