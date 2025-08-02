# How does a Python interpreter work?

https://www.tutorialspoint.com/how-does-a-python-interpreter-work

Google AI Overview:

The Python interpreter processes and executes code in several distinct stages:

    Lexical Analysis (Tokenization):
    . 

The interpreter reads the source code and breaks it down into a stream of tokens. Tokens are the smallest meaningful units of the program, such as keywords (e.g., if, for), operators (e.g., +, =), identifiers (variable names), and literals (numbers, strings). This stage essentially converts the raw text into a structured sequence of recognizable elements.
Parsing:
.
The stream of tokens from the lexical analysis stage is then analyzed to create a hierarchical representation of the code, known as an Abstract Syntax Tree (AST). The AST represents the grammatical structure of the code, ensuring it adheres to Python's syntax rules. This stage identifies the relationships between different parts of the code, such as function definitions, loops, and conditional statements. 
Bytecode Compilation:
.
The AST is then compiled into bytecode. Bytecode is a low-level, platform-independent set of instructions that the Python Virtual Machine (PVM) can understand and execute. This intermediate representation is stored in .pyc files for faster loading in subsequent executions. 
Execution:
.
The PVM executes the bytecode instructions. The PVM interprets each bytecode instruction, translating it into machine-executable code and performing the corresponding operations, such as managing memory, calling functions, handling variables, and executing control flow structures like loops and conditionals. This stage is where the program's logic is actually carried out.
Garbage Collection:
.
Throughout the execution stage, Python employs automatic garbage collection to manage memory. This process identifies and reclaims memory that is no longer in use, preventing memory leaks and optimizing resource utilization.

# Modules

https://docs.python.org/3/tutorial/modules.html

A module is a file with statements and definitions (variables, classes, functions, etc.) that can be _imported_ into other modules or the _main_ module (the collection of variables that you have access to in a script executed at the top level and in calculator mode). Modules are good for splitting up a long program into logically related parts and reusing code.
* The file name is the module name with `.py` appended
* Within a module's namespace, its name is available as the value of the global variable `__name__` (as a string)
* `import modname` imports the module into the current namespace. `modname` refers to the module object, and you can access its definitions (attributes) via `modname.varname`, `modname.funcname`, `modname.classname`, etc.
* You can assign a local name to attributes you frequently use, e.g. `funcname = modname.funcname`
* A module can contain executable statements (intended to initialize the module). They are executed only the _first_ time the module name is encountered in an import statement (and also if the file is executed as a script).
* Each module has its own private namespace, which is used as the global namespace by all functions defined in the module (does not clash with a user's global variables)
* Modules can import other modules. Import statements are typically at the top of the file, outside of any functions or classes, and the imported names are added to the module's global namespace.
* You can import names from a module without importing the module's namespace, e.g. `from modname import func1, func2`
* You can rebind names via `import modname as mod`, `from modname import func1 as f1, func2 as f2`
* Each module is only imported once per interpreter session. If you change your modules, you must restart the interpreter or reload the module via `importlib.reload(modulename)`

## Executing modules as scripts

When you run a module with `python modname.py <arguments>`, the module code will be executed (same as import) but with `__name__` set to `"__main__"`. Adding this code at the end of the module makes it usable as a script:
```python
if __name__ == "__main__":
    import sys
    funcname(sys.argv[1])
```
This code is only run if the module is executed as the "main" file, not when it's imported. This is often used either to provide a convenient user interface to a module or for testing purposes (e.g. running as a script executes a test suite).

## The module search path

When `modname` is imported, the interpreter first searches for a built-in module with that name. These module names are listed in `sys.builtin_module_names`. If not found, then it searches for `modname.py` in a list of directories given by the variable `sys.path`.

`sys.path` is initialized from
* The directory containing the input script. If no directory, then it is the current directory, e.g. when executing an interactive shell, a `-c` command, or `-m` module
* PYTHONPATH (shell environment variable)
* The installation-dependent default (by convention including a `site-packages` directory, handled by the `site` module)

After initialization, Python programs can modify `sys.path`.

The directory containing the script being run is placed at the beginning of the search path, ahead of the standard library. That means that scripts in that directory will be loaded instead of modules of the same name in the standard library. **This is an error unless the replacement is intended.**

## "Compiled" Python files

## Standard modules

See the Python Library Reference for the library of standard modules.
* Some are built into the interpreter
* `sys` and `sys.path` are important to know

## `dir()`

`dir(modname)` returns a sorted list of strings that are the names the module defines.

`dir()`, without arguments, lists the names in the current namespace.

It does not list the names of built-in functions and variables. Use `dir(builtins)` for that.

## Packages

Packages structure Python's module namespace by using "dotted module names". `A.B` refers to submodule `B` in package `A`. Names defined in different modules don't clash; similarly, module names in different packages don't clash.

Example package structure:
```
sound/                          Top-level package
      __init__.py               Initialize the sound package
      formats/                  Subpackage for file format conversions
              __init__.py
              wavread.py
              wavwrite.py
              aiffread.py
              aiffwrite.py
              auread.py
              auwrite.py
              ...
      effects/                  Subpackage for sound effects
              __init__.py
              echo.py
              surround.py
              reverse.py
              ...
      filters/                  Subpackage for filters
              __init__.py
              equalizer.py
              vocoder.py
              karaoke.py
              ...
```

When importing the package, Python searches through `sys.path` looking for the package subdirectory.

`__init__.py` are required to make Python treat directories as packages. This prevents directories with a common name from unintentionally hiding modules that occur later in the module search path.
* Can be empty
* Can also execute initialization code for the package or set the `__all__` variable

You can import individual modules:
* `import sound.effects.echo`. It must be referenced with its full name, e.g. `sound.effects.echo.echofilter(args)`
* `from sound.effects import echo`. This shortens the reference to `echo.echofilter(args)`.
* `from sound.effects.echo import echofilter`. This imports the function directly, e.g. `echofilter(args)`.

When using `from package import item`, item can be a submodule, subpackage, or any other name (function, class, variable). `import` first tests whether the item is in the package; if not, it assumes item is a module and attempts to load it.

When using `import item.subitem.subsubitem`, each item except for the last must be a package. The last item can be a module or package but cannot be a class/function/variable.

### Importing * from a package

What happens when we try `from sound.effects import *`?
* If the package's `__init__.py` code defines a list named `__all__`, it is taken as the list of module names to import
* If `__all__` is not defined, then only the package `sound.effects` is imported (possibly running initialization code in `__init__.py`) along with the names defined in the package. 
    * Names defined and submodules loaded in `__init__.py
    * Submodules of the package explicitly loaded by previous `import` statements

Importing * is not recommended for production. The preferred way is `from package import specific_submodule` unless you need submodules with the same name from different packages.

### Intra-package references

Use absolute imports to refer to submodules of sibling packages (in the example above, the sibling packages are conversions, effects, and filters). For example, if `sound.filters.vocoder` may import from effects using `from sound.effects import echo`.

Alternatively, you can use relative imports.

### Packages in multiple directories

# Errors and exceptions

https://docs.python.org/3/tutorial/errors.html#raising-exceptions

Two types of errors: _syntax errors_ (aka parsing errors) and _exceptions_.

Prior to execution, Python parses the the code. If there is code it does not understand (due to syntax mistakes), it will raise a `SyntaxError`.

_Exceptions_ are errors detected during execution and are not unconditionally fatal.

## Handling exceptions

Exceptions may be handled via try-except statements.
```python
while True:
    try:
        x = int(input("Please enter a number: "))
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")
```
How it works:
* `try` clause is executed
* If no exception, then `except` clause is skipped and `try` statement finishes executing
* If exception during `try`, the rest of the clause is skipped. If the exception type matches `except`, then `except` clause is executed and program continues.
* If an exception during `try` does not match `except` type, then the exception is passed on to outer `try` statements, and if no handler is found, it is an _unhandled exception_ and execution stops with an error message.

A `try` statement may have more than one `except` clause to specify handlers for different exceptions.
* At most one handler will be executed
* Handlers only handle exceptions that occur in the `try` clause, not in other handlers of the same `try`
* `except` clause may name multiple exceptions like `except (RuntimeError, TypeError, NameError)`
* A class in an `except` clause matches exceptions which are instances of the class itself or one of its derived classes
* You may bind a variable name to an exception instance via `except Exception as e`
    * An exception may have associated values, called its arguments, accessible via `e.args`
    * Built-in exceptions define `__str__()` method to print all arguments, i.e. `print(e)`

`BaseException` is the common base class of all exceptions.
* `Exception` is the base class of non-fatal exceptions
* Exceptions that are not derived from `Exception` are not typically handled because they indicate the program should terminate
    * `SystemExit`, raised by `sys.exit()`
    * `KeyboardInterrupt`, raised when the user wishes to interrupt the program

`Exception` can be used as a wildcard that catches (almost) everything, but it's good practice to be as specific as possible with the types of exceptions we intend to handle and allow unexpected exceptions to propagate on. A common pattern is to print the exception and then re-raise it, which allows a caller to handle the exception.
```python
import sys

try:
    f = open('myfile.txt')
    s = f.readline()
    i = int(s.strip())
except OSError as err:
    print("OS error:", err)
except ValueError:
    print("Could not convert data to an integer.")
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
    raise
```

try-except has an optional `else` clause that must follow all `except` clauses. It is executed if no exception is raised in `try`.

## Raising exceptions

`raise` statement forces a specified exception to occur.
* `raise` may be called with an exception instance or class
    * Instance: `raise NameError("HiThere")`
    * Class: `raise ValueError`. When a class is passed, it is implicitly instantiated by calling its constructor with no arguments, i.e. `raise ValueError` is equivalent to `raise ValueError()`
* `raise` with no arguments simply re-raises the exception if you don't intend to handle it

## Exception chaining

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
* `globals()` returns the global namespace, `locals()` returns the current namespace
* There is no relation between names in different namespaces, e.g. two different modules may both define a function `maximize` without confusion. Users of the modules must prefix it with the module name.
* An attribute is any name following a dot
    * In `z.real`, `real` is an attribute of object `z`
    * References to names in modules are attribute references. In `modname.funcname`, `modname` is a module object and `functname` is an attribute of it. The module's attributes and the global names defined in the module share the same namespace!
    * Attributes may be read-only or writable. For an example writable case, `modname.the_answer = 42`. Writable attributes may be deleted with `del`, e.g. `del modname.the_answer` will remove `the_answer` from `modname`.
* Namespaces are created at different moments and have different lifetimes
    * Built-in namespace is created when the Python interpreter starts up and is never deleted (the names are in the `builtins` module)
    * Global namespace for a module is created when the module definition is read in and normally lasts until the interpreter quits
    * The statements executed by the top-level invocation of the interpreter (either from a script or interactively) are considered part of a module called `__main__`, so they have their own global namespace
    * The local namespace for a function is created when the function is called, and deleted when the function returns or raises an exception that isn't handled within the function
* _Scope_: a textual region of a Python program where a namespace is directly accessible. "Directly accessible" means that an unqualified reference to a name attempts to find the name in the namespace.
    * Scopes are determined statically (based on the structure of the code)
    * Scopes are used dynamically - Python resolves unqualified references at runtime. During execution, there are 3 or 4 nested scopes whose namespaces are directly accessible (also known as LEGB):
        * Local: The innermost scope, which is searched first, contains the local names
        * Enclosing: The scopes of any enclosing functions, which are searched starting with the nearest enclosing scope, contain non-local but also non-global names
        * Global: The next-to-last scope contains the current module's global names
        * Built-in: The outermost scope, searched last, is the namespace containing built-in names
    * If a name is declared `global`, all references and assignments go directly to the global scope
    * To rebind variables found outside of the local scope, use the `nonlocal` statement. Otherwise, those variables are read-only - attempting to write to such a variable creates a new local variable, leaving the identically named outer variable unchanged.
    * Within the textually current function, the local scope references the local names in that function. Outside of functions, the local scope and the global scope are the same. Class definitions create another local scope.
    * **Important**: scopes are determined textually. The global scope of a function defined in a module is that module's namespace, no matter from where or by what alias the function is called.
    * If no `global` or `nonlocal` statement is in effect, assignments to names always go into the innermost scope. Assignments do not copy data - they bind names to objects. The same is true for deletions: `del x` removes the binding of `x` from the namespace referenced by the local scope. In fact, all operations that introduce new names use the local scope: in particular, `import` statements and function definitions bind the module or function name in the local scope.
    * `global` indicates a variable that lives in the global scope and should be rebound there
    ` nonlocal` indicates that a variable lives in an enclosing scope and should be rebound there