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

# <u>REST APIs</u>

Microservices

