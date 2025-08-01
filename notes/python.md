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