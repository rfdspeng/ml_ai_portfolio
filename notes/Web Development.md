Web development is creating, building, and maintaining websites. It's split into two parts: frontend and backend.

**Frontend development is essentially the UI** - it's what the user interacts with on their web browser (and it's sometimes referred to as the client side of the application).
* Key responsibilities
  * Visual layout and structure of the web pages
  * Responsiveness across devices (desktop, mobile), meaning the website adapts to different screen sizes, resolutions, and orientations.
    * Layout adjusts to fit different screen sizes
    * Text remains legible without excessive zooming or scrolling
    * Images and videos scale appropriately
    * Buttons and navigation are easy to use, even on small screens
  * Responsiveness also includes performance - making sure the website loads quickly. Performance optimization techniques:
    * Reducing the size and complexity of CSS and JavaScript files so they download and execute faster
    * Bundling CSS/JS files into one, reducing the number of HTTP requests
    * Breaking large files into smaller chunks that only load when needed
    * Lazy-loading images and videos - defer loading images and videos until they are needed (e.g. when they are about to scroll into the viewport or when the user interacts with them), which reduces initial page load time
    * Using content deliver networks (CDNs) - a network of servers distributed across multiple locations to deliver content quickly to users based on their geographical location. This also offloads the traffic from your main server, reducing hosting cost.
  * Interactive features (buttons, forms, animations)
  * Seamless and intuitive user experience (UX)
* Technologies
  * HTML (Hypertext Markup Language) defines the structure of the web page
  * CSS (Cascading Style Sheets) styles the appearance of the web page
  * JavaScript adds interactivity and dynamic behavior
  * Frameworks/libraries
    * React, Angular, Vue.js (interactive UIs)
    * Bootstrap, Tailwind CSS (styling and layout)
  * Tools: Figma, Adobe XD (for design); Webpack, Babel (for development workflow)

**Backend development is the server side, which is invisible to the user** - it handles logic, databases, authentication, and communication between the frontend and the server.
* Key responsibilities
  * Server-side logic
    * User authentication: checking if the username and password match the database records
    * Business logic: applying rules to data before responding to client requests, e.g. calculating a user's total shopping cart cost including discounts and taxes
    * Storing, retrieving, or updating data in a database
    * Uploading or downloading files securely, e.g. saving uploaded profile pictures to a cloud storage service
    * Real-time operations: handling live updates or notifications, e.g. a chat server pushing new messages to users in real-time
  * Server-side APIs (to allow the frontend and other systems to interact with the backend)
    * REST API - can you go over this in more detail?
    * GraphQL API - can you go over this in more detail?
    * WebSocket API: enable real-time updates like live chat or stock price updates. For example, the server might push a message like `{"from": "John", "text": "Hello!"}` to the client. Is this in JSON format?
  * Security, scalability, performance
* Technologies
  * Languages: Python (Django, Flask), JavaScript (Node.js), Java (Spring), Ruby (Rails), PHP (Laravel)
  * Databases
    * SQL-based: MySQL, PostgreSQL
    * NoSQL-based: MongoDB, Firebase
  * Server technologies: Apache, Nginx, Gunicorn
  * Tools: Docker, Kubernetes, AWS, Google Cloud (for deployment and scaling)

Frontend and backend communication (REST APIs or GraphQL) - if there is no full-stack developer, then does backend handle this?

DevOps tools (Docker, CI/CD pipelines) for deploying full applications - if there is no full-stack developer, then is there a dedicated DevOps engineer?



Streamlit for front end

Model serving. Terms: uvicorn, wsgi, asgi, nginx

nginx is a reverse proxy server. Helps in load balancing. Makes your laptop or EC2 instance a web server such that if there are multiple concurrent requests, it will try to balance the load.

Let's say 10 people are using your AI application, which is served via Flask (wsgi). The way it works is requests are served sequentially. Serve first, then second, then third, etc. This is very slow. Serial processing - wait for each request to be complete before serving the next.

FastAPI (asgi) is asynchronous - multiple requests are served concurrently. This is preferred.

Let's say you have 1 million people requesting. Your EC2 instance would crash. 

Instead, you would have 100 EC2 instances, each with your AI application installed and accessible via FastAPI. The 101st EC2 instance would have nginx installed to do load balancing among the 100 EC2 instances (like a manager). It would direct traffic to lower-load instances (reverse proxy server). Also serves the static files (what's that?).

nginx directs your HTTP request to an instance. Each instance also has uvicorn installed. It takes HTTP request (which is in HTML) and converts it to Python-readable format/input (Fast/Flask are Python libraries) - what exactly is this format?. Gives it to Fast/Flask, which returns a message usually in JSON format. JSON back to uvicorn, which then converts to HTML. Then back to nginx for serving purpose on client side web browser.

What is `curl`?

I need a diagram of this shit.

# Questions
* Is Streamlit async or sync? Also, what does this mean exactly?

# <u>General SWE concepts</u>

## <u>Process vs. thread</u>

Everything below is generated by Google Search AI, so make sure to double-check and revise later.

_"thread vs process"_

A process is a single application or program that has its own address space in memory. Processes are isolated from each other, which increases security and stability. However, this isolation can make communication more complex and slower. 

A thread is a subprocess within an application or program that shares its address space with other threads in the same process. Threads are lightweight and can communicate quickly and efficiently with each other. However, the lack of isolation between threads can lead to issues like data races and deadlocks if not managed properly. 

Here are some other differences between processes and threads:
* Memory: Different processes cannot share the same memory space, but different threads in the same process can. 
* Switching: Switching threads does not require interacting with the operating system, but switching processes does. 
* Effect on other processes: If one process is obstructed, it will not affect the operation of another process. However, if one thread is obstructed, it will affect the execution of another process. 

## <u>Locking</u>

Everything below is generated by Google Search AI, so make sure to double-check and revise later.

_"fastapi lock"_

Locking is used to handle concurrent access to shared resources, ensuring data integrity and preventing race conditions.

Important Considerations:
* Granularity: Lock only the specific part of your code that needs protection.
* Deadlocks: Be careful to avoid deadlocks when using multiple locks.
* Timeouts: Set appropriate timeouts for locks to prevent them from being held indefinitely.
* Distributed Environments: For distributed systems, use a centralized locking mechanism like Redis. 

Choosing the Right Locking Mechanism:
* Simple, Single-Process Applications: Mutex locks are sufficient.
* Distributed Systems: Use a distributed lock manager like Redis.
* File-Based Locking: Useful when managing access to files on the filesystem. 

https://stackoverflow.com/questions/34524/what-is-a-mutex

A mutex is a programming concept that is frequently used to solve multi-threading problems. My question to the community:

What is a mutex and how do you use it?

**Answer**
When I am having a big heated discussion at work, I use a rubber chicken which I keep in my desk for just such occasions. The person holding the chicken is the only person who is allowed to talk. If you don't hold the chicken you cannot speak. You can only indicate that you want the chicken and wait until you get it before you speak. Once you have finished speaking, you can hand the chicken back to the moderator who will hand it to the next person to speak. This ensures that people do not speak over each other, and also have their own space to talk.

Replace Chicken with Mutex and person with thread and you basically have the concept of a mutex.

Of course, there is no such thing as a rubber mutex. Only rubber chicken. My cats once had a rubber mouse, but they ate it.

Of course, before you use the rubber chicken, you need to ask yourself whether you actually need 5 people in one room and would it not just be easier with one person in the room on their own doing all the work. Actually, this is just extending the analogy, but you get the idea.

# <u>FastAPI</u>

FastAPI is a Python library for developing the backend of web applications. You define the path operations and functions with FastAPI. It uses Uvicorn, which is an ASGI (asynchronous server gateway interface), which supports asynchronous code execution.

What exactly is the flow from the POV of the client? It's client -> Uvicorn -> FastAPI serves the request. Which part of this is the server? Which part is the API? Which part is frontend-backend?

Is FastAPI built on asyncio, Starlette, and Pydantic?

In the client-server model, the client sends a request to the server, which serves the request by processing the request and sending the response (data or service) to the client. For example, the client could be your web browser asking the web server for a web page.

Example:
* **Client action**: you type a URL into your browser, like www.example.com
* **Request sent**: your browser sends a request to the server at www.example.com asking for the webpage associated with that address
* **Server action**: the server receives the request, retrieves the webpage data (the frontend), and sends it back to your browser
* **Response received**: your browser displays the webpage content

## <u>Introduction to Python types</u>

Python supports type hints (also called type annotations). They're a syntax that allow declaring the type of a variable, which allows your editors and tools to give you better support. For example, your editor can check for type mismatches and suggest methods based on the variable type.

Here's a simple example. The type hints indicate that `first_name` and `last_name` are strings.
```python
def get_full_name(first_name: str, last_name: str):
  full_name = first_name.title() + " " + last_name.title()
  return full_name
```

Simple types: `str`, `int`, `float`, `bool`, `bytes`

Generic types: `dict`, `list`, `set`, `tuple`

Generic types are data structures that contain internal values with their own types. In older versions of Python, you needed to use the Python module `typing`; in Python 3.10+, you (mostly) don't.

For example, here's how you declare a variable `items` that is a `list` of `str`.
```python
def process_items(items: list[str]):
    for item in items:
        print(item)
```
The type in the square brackets (`str` in this case) is called a type parameter.

Declare a `3-ple` consisting of `int`, `int`, `str`, and a `set` consisting of `bytes` values:
```python
def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t, items_s
```

Declare a `dict` with `str` keys and `float` values:
```python
def process_items(prices: dict[str, float]):
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
```

Declare a variable that can be either `int` or `str` (also known as a union):
```python
def process_item(item: int | str):
    print(item)
```

Declare a variable that can be either `str` or `None` (`= None` is how you set the default value):
```python
def say_hi(name: str | None = None):
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
```

You can also declare classes as types:
```python
class Person:
    def __init__(self, name: str):
        self.name = name

def get_person_name(one_person: Person):
    return one_person.name
```
`one_person` is an instance of the class `Person`.

### <u>Pydantic</u>

Pydantic is a Python library to perform data validation.

You declare the "shape" of the data as a class with attributes. Each attribute has a type.

Then, you create an instance of that class with the desired values for each attribute. Pydantic will validate the values, convert them to the appropriate type, and return the instance. Then you get editor support for instances of that class.

Example:
```python
from datetime import datetime

from pydantic import BaseModel

# This is the data "shape" declaration
# Each datum has 4 attributes: id (int), name (str), signup_ts (datetime or None), and friends (a list of ints)
class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

# These are the values you will instantiate your datum with
external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data) # instantiate a datum
print(user)
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123
```

### <u>Type hints with metadata annotations</u>

In addition to providing type hints, you can pass annotations:
```python
from typing import Annotated

def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"
```

`name`'s type is still `str`. The second field is metadata that you can pass to FastAPI about how you want your application to behave.

### <u>Type hints in FastAPI</u>

FastAPI uses these type hints to
* **Define requirements** from request path parameters, query parameters, headers, bodies, dependencies, etc.
* **Convert data** from the request to the required type
* **Validate data** coming from each request and generating automatic errors returned to the client when the data is invalid
* **Document** the API using OpenAPI, which is then used by automatic interactive documentation user interfaces

## <u>Concurrency and `async`/`await`</u>

### <u>TLDR</u>

* Case 1: If you're using third party libraries that tell you to call them with `await`, like `results = await some_library()`, then declare your path operation functions with `async def`, like
```python
@app.get("/")
async def read_results():
  results = await some_library()
  return results
```

**You can only use `await` inside of functions created with `async def`.**

* Case 2: If you're using a third party library that communicates with something and doesn't support `await`, then declare your path operation functions with `def`:
```python
@app.get("/")
def read_results():
  results = some_library()
  return results
```

* Case 3: If your application (somehow) doesn't communicate with anything else and wait for it to respond, use `async def`.

* Case 4: If you just don't know, use `def`.

You can mix `def` and `async def` as much as you need in your path operation functions, and FastAPI will do the right thing. In any of the cases, FastAPI will work asynchronously and be extremely fast, but by following the cases, FastAPI will be able to do some performance optimizations.

### <u>Technical details</u>

Modern versions of Python support asynchronous code using coroutines with `async` and `await`. What does this mean?

**Asynchronous code** means that the language has a way to tell the program that at some point in the code, the program will need to wait for something else (let's call this _slow-file_) to finish before continuing. While waiting for _slow-file_ to finish, the program can go and do other work. The program will come back to _slow-file_ every chance it gets to see if it's done. This is also called **concurrency**.

When _slow-file_ is done, the program will take the results from _slow-file_ and continue on with the rest of the code.

_slow-file_ normally refers to I/O operations (also called **I/O-bound operations**, since most of the execution time is consumed by waiting for I/O operations) that are slow compared to the processor or RAM, like waiting for
* Data from the client to arrive
* Data to be sent to the client from your program
* Reading a file from disk
* Saving a file onto disk
* A remote API operation
* A database operation
* A database query to return the results

**Why is this called asynchronous code?** Because the program doesn't have to be "synchronized" to _slow-file_. When _slow-file_ is done, it can wait in line for the program to come back.

In contrast, in **synchronous code** (also known as sequential code), the program executes the code sequentially, waiting for each task to finish before moving on to the next. While waiting, the program does nothing. Because the program is blocked from continuing, this is also known as **blocking code** or **blocking I/O**.

**Parallelism** is different from **concurrency**. In parallelism, you have multiple processors (CPU, GPU, etc.) that are assigned to do tasks in parallel. Since most of the execution time is spent on actual work, not waiting, these operations are called **CPU-bound operations**. Common examples are things that require a lot of math, like audio and image processing, machine learning, deep learning.

Here's a simple analogy to explain concurrency vs. parallelism:
* **Concurrency**: You have two tasks, laundry and studying. You start the laundry, and while waiting for the machine to finish, you switch to studying. Once the laundry is done, you fold the clothes. This is concurrency: one processor (you) is switching between tasks to keep them moving.
(Without concurrency, you’d sit and wait for the laundry to finish before starting to study.)
* **Parallelism**: You need to clean the house, so you and your 3 roommates each tackle a room. Now, 4 tasks are happening simultaneously, one per person. This is parallelism: multiple processors (you and your roommates) are executing tasks at the same time.

### <u>`async` and `await`</u>

In modern Python, asynchronous code is defined with the keywords `async` and `await`.

It's simple: define asynchronous functions using `async def`. Inside of an asynchronous function, and _only_ inside of an asynchronous function, you can use `await` or call other asynchronous functions.
```python
import asyncio
from third_party_lib import get_clothes, wash, dry, fold, study

# In this dummy example, get_clothes, fold, and study are synchronous functions
# wash and dry are asynchronous functions

async def washer(clothes):
  clothes = await wash(clothes)
  return clothes

async def dryer(clothes):
  clothes = await dry(clothes)
  return clothes

async def do_laundry(clothes):
  laundry = await washer(clothes)
  laundry = await dryer(laundry)
  laundry = fold(laundry)
  return laundry

async def main():
  clothes = get_clothes()

  # create_task creates tasks that can be run concurrently
  # to_thread allows a synchronous task to be run without blocking the event loop
  laundry_task = asyncio.create_task(do_laundry(clothes))
  study_task = asyncio.create_task(asyncio.to_thread(study))

  # gather executes the tasks concurrently and waits for all to finish
  # It returns their results as a list, in the same order the tasks are passed in
  laundry, _ = await asyncio.gather(laundry_task, study_task)
  print("Laundry and studying complete!")

# Run the main event loop
asyncio.run(main())
```

This is an example of concurrency on a single-threaded event loop. Tasks appear to run in parallel, but they're interleaved efficiently using `await` and the event loop. What does this mean?

The event loop is the coordinator that juggles the tasks, and a single thread means that only one task is processed at a time. Using concurrency, we can make it seem like the tasks are running in parallel even though we only have one thread.

FastAPI utilizes the event loop provided by the ASGI server (like Uvicorn), so developers don’t need to manage the event loop manually. All you need to do is define your path operation functions as `async def` or `def` and use `await` for I/O operations, and FastAPI will handle the rest. A function with `async def` is also called a **coroutine**, which allows non-blocking execution.

## <u>Path operations</u>
Example script:
```python
# FastAPI is a Python class that provides all the functionality for your API
from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()

# Create a path operation
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

**Path operation**:
* The path is the part of the URL starting from the first /. For example, in a URL like `https://example.com/items/foo`, the path is `/items/foo`. path is also commonly called an endpoint or route. When building an API, the path is the main way to separate concerns and resources.
* Operation refers to one of the HTTP methods. In HTTP protocol, you (the client) communicate to each path using one (or more) of these methods.
  * `POST`: to create data
  * `GET`: to read data
  * `PUT`: to update data
  * `DELETE`: to delete data
  * `OPTIONS`
  * `HEAD`
  * `PATCH`
  * `TRACE`

`@app.get("/")` is called a path operation decorator. It means that the function below handles requests to the path `/` using the `GET` operation. `@app.post()`, `@app.put()`, `@app.delete()` etc. correspond to the other operations.

`async def root()` defines the path operation function (a Python function). It's called by FastAPI whenever it receives a request to `/` using a `GET` operation. In this case, `root` is an `async` function, but you can also define a normal function. In web development, a path operation function is more commonly referred to as a route handler.

Your path operation function can return `dict`, `list`, and singular values like `str`, `int`, etc. You can also return Pydantic models. FastAPI automatically converts many types of objects and models to JSON, including ORMs.

You can run your script in the command line using `fastapi dev myscript.py`. FastAPI will spin up a local server that you can access in your browser at `localhost:8000` along with interactive API documentation at `localhost:8000/docs` and `localhost:8000/redoc`.
  
FastAPI also generates a schema using OpenAPI that you can view at `localhost:8000/openapi.json`.
* A schema is a definition or description of something
* A data schema refers to the shape of some data, like JSON
* An API schema defines your API paths, the parameters they take, etc.
* OpenAPI defines an API schema and a data schema (JSON Schema) for the data sent and received by your API. The OpenAPI schema powers the interactive API documentation and can be used to automatically generate code for clients that communicate with your API

## <u>Path parameters</u>

You can declare **path parameters (variables)** with the same syntax as Python format strings, e.g.
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id):
  return {"item_id": item_id}
```

If you go to `localhost:8000/items/foo`, you'll see a response of `{"item_id": "foo"}`.

You can also declare the type of path parameter, e.g.
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
  return {"item_id": item_id}
```

## <u>Query parameters</u>

### <u>Query parameter models</u>

If you have a group of related query parameters, it's good practice to declare them using a Pydantic model. This allows you to easily re-use the model in multiple places.

Example:
```python
from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# Query parameter model
class FilterParams(BaseModel):
    # This line is optional. It forbids the client from sending query parameters not declared in the model.
    model_config = {"extra": "forbid"}
    
    # Query parameters
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

# filter_query has type FilterParams and is declared as a Query()
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
```

FastAPI will extract the data for each query parameter (e.g. `limit`, `offset`, `order_by`, `tags`) from the client request and instantiate the Pydantic model (`FilterParams`).

## <u>Request body</u>

When the client sends data to your API, it sends it as a **request body**. A **response body** is the data your API sends to the client.

Your API almost always has to send a response body, but clients don't necessarily need to send a request body - sometimes they only request a path, possibly with some query parameters. (The request body is not part of the path).

To declare a request body in a path, you can use Pydantic models.

The client should send data via `POST` (the most common), `PUT`, `DELETE`, or `PATCH`. Sending a request body with `GET` is undefined except in certain complex/extreme use cases.

Here's a simple example:
```python
from fastapi import FastAPI
from pydantic import BaseModel

# This is the data model, which inherits from BaseModel
# This defines the request body format
# description and tax are optional, with default values of None
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/") # Use POST for sending data from the client
async def create_item(item: Item): # declare that this path expects a request body as defined by Item
    return item
```

What does the above code mean? It means that the `/items` path expects a JSON object of the form
```python
{
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}

# Since description and tax are optional, this is also a valid request body
{
    "name": "Foo",
    "price": 45.2
}
```



## <u>Dependencies</u>

In software, **dependency injection** is where an object (the **dependent object**) receives the other objects (the **dependencies**) it needs to function from an external source, rather than creating them itself. The dependent object, which receives the injection, doesn't know how to construct its dependencies.

There are three types of injection:
* Constructor injection: inject dependencies through a class constructor where the required objects are passed as parameters
* Setter injection: inject dependencies after the object is created
* Interface injection: some frameworks support interface injection, where the dependent class provides a method that the injector calls to inject the dependency

```python
# Dependency
class Service:
    def operation(self):
        return "Service Operation"

# Dependent with constructor injection
class Client:
    def __init__(self, service):
        self.service = service

    def do_work(self):
        return self.service.operation()

service = Service()
client = Client(service)
print(client.do_work())  # Outputs: Service Operation

# Dependent with setter injection
class Client:
    def set_service(self, service):
        self.service = service

    def do_work(self):
        return self.service.operation()

service = Service()
client = Client()
client.set_service(service)
print(client.do_work())  # Outputs: Service Operation
```

Dependency injection is beneficial because it makes your code modular:
* You can easily change the dependency by injecting a different one without changing the dependent. This also simplifies testing because you can inject mock dependencies.
* If the dependency requirement changes, you can easily update all dependents by updating the dependency.
* In some cases, you may reuse the dependency object, injecting the same object to multiple dependents rather than creating new dependencies

Dependency injection is a concept that doesn't require a framework, but there are dependency injection frameworks like Spring for Java or Python's `injector` library.

FastAPI provides a framework to inject dependencies into your path operation functions using the `Depends` class. `Depends` takes a single argument, a callable, which means it can take a function or a class. `Annotated` is not required, but it is recommended by FastAPI.

Here's a simple example of dependency injection in FastAPI:
```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

# Dependency (in this case, a function)
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Dependent #1
@app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)) # this is the version without Annotated (according to ChatGPT)
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# Dependent #2
@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

What's happening in this example? At runtime, when there's a new request to an endpoint, FastAPI recognizes that there is a dependency and calls `common_parameters`. `common_parameters` expects 3 query parameters, `q`, `skip`, and `limit`. FastAPI takes care of passing the query parameters to `common_parameters` and injects the results of `common_parameters` to `commons`.

You can further simplify this code with **type aliasing**:

```python
# Type alias definition
CommonsDep = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonsDep):
    return commons

@app.get("/users/")
async def read_users(commons: CommonsDep):
    return commons
```

Dependency functions can be defined as `async def` or `def`.

Dependencies are recursive - that is, you can define dependencies within dependencies, and FastAPI will resolve the dependencies for you.

Now let's see how to inject a dependency class:
```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response
```

When a class is passed to `Depends`, FastAPI analyzes the `__init__` method as the callable. Note that the syntax of calling `CommonQueryParams` is exactly the same as calling the function `common_parameters`.

In this example, `CommonQueryParams` is both the type hint and the injectable dependency. FastAPI provides a shortcut for this case, where `Annotated[CommonQueryParams, Depends(CommonQueryParams)]` is equivalent to `Annotated[CommonQueryParams, Depends()]`.

## <u>Project directory structure</u>

```python
.
├── app                     # Python package, app
│   ├── __init__.py
│   ├── main.py             # Python module, app.main
│   ├── dependencies.py     # Python module, app.dependencies
│   └── routers
│   │   ├── __init__.py     # Python subpackage, app.routers
│   │   ├── items.py        # Python submodule, app.routers.items
│   │   └── users.py        # Python submodule, app.routers.users
│   └── internal            # Python subpackage, app.internal
│       ├── __init__.py
│       └── admin.py        # Python submodule, app.internal.admin
```

This is the recommended project directory structure.

`__init__.py`, which is typically empty, turns a folder into a Python package (a collection of Python modules). `.py` files inside a Python package are modules. In the example above, since `app` is a package and `main` is a module, you can `import app.main` or `from app import main`.

`main.py` is the "entry point" of your FastAPI application:
* Creates an instance of FastAPI
* Import and include routers from other files
* Configures middleware, global dependencies, and app-wide settings (whatever this means)
* Use `uvicorn` to run the app if `main.py` is executed directly (whatever this means)
* `main.py` does not include any path operations

The `routers` subpackage contains the submodules that define the critical path operations of your app. You do that with the `APIRouter` class, which you use in the same way as the `FastAPI` class. For example:
```python
# app/routers/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}

@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
```

Then you can import router into `main.py`:
```python
# app/main.py
from fastapi import FastAPI
from .routers import users # import routers.users

app = FastAPI()

app.include_router(users.router) # import routers.users.router

@app.get("/")
async def root():
  return {"message": "Hello this is main"}
```

## <u>Using the request directly</u>

`Request` class documentation: https://www.starlette.io/requests/

Typically, you declare the parts of the request that you need along with their types (e.g. path parameters, request body). FastAPI validates that data, converting it and generating documentation for your API. However, in some situations, you may want to access that request - a `Request` object - directly. FastAPI won't validate/convert/document any data that you get directly.

You can do this by declaring a path operation function parameter with type `Request`:
```python
@app.get("/printurl")
async def printurl(request: Request):
  print(request.url)
```

When you instantiate `app = FastAPI()`, you can store state variables in `app.state`. You can access these variables via `Request.app.state`.

## <u>Websockets</u>



## <u>Lifespan events</u>

