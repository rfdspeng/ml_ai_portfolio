# <u>An overview by Khan Academy</u>

https://www.khanacademy.org/computing/ap-computer-science-principles/algorithms-101/x2d2f703b37b450a3:parallel-and-distributed-computing/a/distributed-computing

## <u>Distribution of parallel processes</u>

Distributed computing is all about using multiple networked computers to complete massive tasks that would take a single computer way too long to finish.

Distributed computing is often used in tandem with parallel computing. Parallel computing on a single computer uses multiple processors to process tasks in parallel, whereas distributed parallel computing uses multiple computing devices to process those tasks.

Let's say you have an application that detects cats in images. In a distributed system, a managing computer would send pictures to multiple worker computers, and each worker computer would report back their result.
* Manager -> pet1.jpg -> worker 1
* Manager -> pet2.jpg -> worker 2

**Speedup** is a measure of performance for your distributed system. Speedup is equal to $Time\ to\ complete\ job\ sequentially \over Time\ to\ complete\ job\ using\ distributed\ system$

There is some overhead associated with the computers talking over the network. Sending messages back and forth takes some time. Therefore, for distributed computing to be worth it, the time saved by distributing the processing must be greater than the time added by the overhead.

In the simplest architecture, the manager talks to the workers. In more complex architectures, workers need to communicate with other workers (also known as **nodes**). For example, this is required to distribute ML model training.

One way to reduce the communication overhead is to use **cluster computing**: co-located computers on a local network that all work on similar tasks. In a computer cluster, a message does not have to travel very far and more importantly, does not have to travel over the public Internet.

Setting up a cluster requires physical space, hardware operations, and money. Many companies now offer cloud computing services which give programmers access to managed clusters (like AWS). The companies manage the hardware operations, provide tools to upload programs, and charge based on usage.

## <u>Distribution by functionality</u>

Another way to distribute computing is to use different devices to execute different pieces of functionality.

Imagine a zoo with an array of security cameras. The cameras send their video data to a computer cluster located in the zoo headquarters, and that cluster runs video analysis algorithms to detect escaped animals. The cluster also sends the data to a cloud computing server, which analyzes TB of data to discover historical trends.

Each device in this distributed network works on a different piece of the problem, based on their strengths and weaknesses. 
* The security cameras only have enough processing power and storage to record digital video footage.
* The local cluster has enough processing power and storage to perform the urgent task of detecting animal escapes.
* The cloud computing server has the most processing and storage, so it works on the heaviest (but not time-critical) task.

## <u>The web is a giant example of distributed computing</u>

Your computer does processing to read this website: sending HTTP requests to get website data, interpreting the JavaScript returned by the website, and constantly updating the screen as you scroll the page.

Our servers do a lot of work while responding to HTTP requests and send data out to high-powered analytics servers for further processing.

Every application that uses the Internet is an example of distributed computing, but each application makes different decisions about how it distributes the computing. Another example: smart home assistants do a small amount of language processing locally to determine that you've asked for help, but then send the audio to high-powered servers to parse the full question.

The Internet enables distributed computing at a worldwide scale, both to distribute parallel computation and to distribute functionality.

# <u>An overview by AWS</u>

https://aws.amazon.com/what-is/distributed-computing/

## <u>Advantages of distributed computing</u>

_Scalability_

Distributed systems can grow with your workload and requirements. You can add new nodes (computing devices) to the distributed computing network when needed.

_Availability_

Your distributed system will not crash if one of the computers goes down (fault tolerance).

_Consistency_

Computers in a distributed system share information and duplicate data between them, but the system automatically manages data consistency across all the computers.

_Transparency_

You can interact with the system as if it's a single computer without worrying about the setup and configuration of individual machines. You can have different hardware, middleware, software, and OS that work together to make the system function smoothly.

_Efficiency_

Distributed systems offer faster performance with optimum resource use of the underlying hardware. That means you can manage any workload without worrying about volume spikes or underuse of hardware.

## <u>Distributed computing use cases</u>

As mentioned in the Khan Academy lecture, mobile and web apps are examples of distributed computing because several machines work together in the backend for the app to respond to your requests.

However, when you scale up distributed systems, they can solve more complex challenges, e.g.

_Healthcare and life sciences_

Modeling and simulating complex life science data. Image analysis, medical drug research, and gene structure analysis.

_Engineering research_

Simulating complex physics and mechanics concepts to improve product design, build complex structures, and design faster vehicles.

_Financial services_

Running high-speed economic simulations that assess portfolio risks, predict market movements, and support financial decision-making.

_Energy and environment_

Analyzing large volumes of data from sensors to improve operations and transition to sustainable and climate-friendly solutions.

## <u>Types of distributed computing architecture</u>

In distributed computing, you design applications that can run on several computers instead of on one computer, and you do this by designing the software so different computers perform different functions and communicate to develop the overall solution.

**<u>Client-server architecture</u>**

Two functions: clients and servers.

Clients have limited information and processing ability - they make requests to the servers for data.

Servers synchronize and manage access to resources. They respond to clients with data or status information. Typically, one server can handle requests from several clients.

Client-server architecture is good for security and ease of management - you only have to focus on securing the server computers, and any changes to databases requires changes to the server only. However, servers can cause communication bottlenecks when they're hit with too many requests.

**<u>Three-tier architecture</u>**

You still have clients, but servers are split into application and database servers.

Application servers act as the middle tier for communication. They contain the application logic or the core functions.

Database servers act as the third tier to store and manage the data. They are responsible for data retrieval and consistency.

Dividing server responsibility reduces communication bottlenecks.

**<u>N-tier architecture</u>**

N-tier models include several different client-server systems communicating with each other to solve the same problem. Most modern distributed systems use an n-tier architecture with different enterprise applications working together as one system behind the scenes.

**<u>Peer-to-peer architecture</u>**

P2P systems assign equal responsibilities to all networked computers. There is no separation between client and server, and any computer can perform all responsibilities. P2P is popular for content sharing, file streaming, and blockchain networks.

## <u>Loose and tight coupling</u>

Computers in a distributed system need to communicate with each other. Communication protocols or rules create a dependency between components of a distributed system, and this is called coupling.

In **loose coupling**, components are weakly connected so changes to one component do not affect the other. For example, client and server computers can be loosely coupled by time: Messages from the client are added to a server queue, and the client can continue to perform other functions until the server responds to its message.

High-performing distributed systems often use **tight coupling**. Fast LANs typically connect several computers to create a **cluster**. In cluster computing, each computer is set to perform the same task. Central control systems, called clustering middleware, control and schedule the tasks and coordinate communication between the different computers.

## <u>Parallel vs. distributed computing</u>

Parallel computing is a particularly tightly coupled form of distributed computing in which one computer or multiple computers in a network carry out many calculations or processes simultaneously. In parallel processing, all processors have access to shared memory for exchanging information between them. In distributed processing, each process has private memory (distributed memory).

## <u>AWS high-performance computing</u>

* AWS EC2
* AWS Batch
* AWS ParallelCluster

Questions
* Is it difficult to build a scalable computing architecture? What's involved exactly if cloud computing is fully managed?
* REST is a stateless API that is good for scaling
* Is everything in AWS distributed? Zilliz talks about distributed object storage, S3 (and MinIO).
* What is microservices architecture?