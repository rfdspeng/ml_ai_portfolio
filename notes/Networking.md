# <u>General terminology</u>

* **Networking**: devices communicating over a network or networks
* **Device**: any computing entity that can connect to a network. Each device is uniquely identified by their IP address. Port numbers direct this communication to specific applications or services on the device. Devices can be
  * Personal computers, smartphones, tablets, IoT devices
  * Servers (physical, like data centers, or virtual, like AWS instances) and clients
  * Routers and switches (networking hardware)
  * Printers and other peripherals
* **Servers and clients**: servers provide specific services or resources to clients. A server runs software to manage and distribute resources (like Apache for web hosting or MySQL for databases). A client is a piece of software that requests services from a server.
  * Web servers host web pages that are accessible to users via a web browser (the client)
  * File servers store and manage files that are accessible to users via either file manager applications like Windows Explorer or specialized software like Google Drive and OneDrive
  * Mail servers handle email that users can access via mail applications like Outlook. When you access Gmail via browser, you're still talking to a web server, and the web server talks to the mail server.
  * Database servers manage databases
* **IP address**: unique identifier for a device on a network. It can be public (assigned by your IPS for internet access) or private (used within local networks). IPv4 addresses are commonly used (e.g. 192.168.1.1), but IPv6 is becoming more common as IPv4 addresses run out.
  * Not every device always has a unique IP address at all times. Devices in private networks behind a router share the same public IP. Private addresses are only unique within your private network, like your home Wi-Fi. They aren't directly accessible from the Internet. Typically, these IPv4 addresses are reserved for private networks:
    * 10.0.0.0 to 10.255.255.255
    * 172.16.0.0 to 172.31.255.255
    * 192.168.0.0 to 192.168.255.255
  * You may host certain applications on your local computer, e.g. a website or a virtual machine. On your local computer, you can access these applications via the IPv4 address `127.0.0.1` or the IPv6 address `::1` or even more simply, `localhost`. These all mean the same thing in networking: *myself*. For example, if you host a website on port 8080, you can navigate to it in your web browser at 127.0.0.1:8080 or localhost:8080.
* **Port number**: a port number is appended to a device's IP address to identify specific services that the device supports. For example, HTTP requests are typically routed to port 80, and on the flip side, an HTTP server listens to port 80 by default.
  * Ports 1 to 1024 are reserved for well-known services. Common ports and their corresponding communication protocols:
    * Port 80: HTTP
    * Port 443: HTTPS
    * Port 22: SSH
    * Port 25: SMTP (sending emails)
    * Port 110: POP3 (retrieving emails)
    * Port 143: IMAP (retrieving emails)
    * Port 53: DNS
  * Ports 1024 to 49151 are often used for locally-hosted applications to avoid conflicts with reserved ports. For example, 8080 is commonly used for web servers and 2222 is commonly used for VMs.
  * Ports 49152 to 65535 are called ephemeral ports and are used for "ephemeral" or dynamic use.
* **Port forwarding**: bridges an external network and an internal network. It's an application of network address translation: external IP addresses and ports are mapped to internal IP addresses and ports when packets traverse a network gateway like a router or firewall. For example, if you host a public web server within a private LAN, you can use port forwarding to allow other Internet-connected devices to access the server via the router's public IP.
* **Endpoint**: in networks, an endpoint is simply an IP address-port combination. An endpoint is one side of a network communication, which includes both client and server. An API endpoint is slightly different, consisting of IP + port + path_to_resource, e.g. 192.168.1.1:80/api.
* **Firewalls**: a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules. Firewalls are used to block traffic based on source/destination IPs, source/destination ports, and protocols (e.g. TCP vs. UDP).
* **DNS**: stands for Domain Name Service. It maps the IP address of a web server (like 93.184.216.34) to a domain name (example.com) that is easy to remember. The browser assumes port 80 unless otherwise specified.

# <u>TCP-IP network model</u>

[TCP-IP explanation](https://cheapsslsecurity.com/blog/what-is-the-tcp-model-an-exploration-of-tcp-ip-layers/ )

TCP-IP (Transmission Control Protocol-Internet Protocol) is a networking standard.

Communication between two devices is established via a three-way handshake (or SYN-SYN-ACK):
1. The client sends a SYN packet to the server asking to open a connection.
2. The server responds by sending a SYN-ACK, acknowledging receipt of the SYN packet and confirming that it's ready to connect.
3. The client responds with ACK to validate the connection and packet transmission begins.

![Three-way handshake](https://cheapsslsecurity.com/blog/wp-content/uploads/2022/06/tcp-3-way-handshake-1024x392.png)

Let's say you send an email to a coworker. How does TCP-IP take your email and put it in your coworker's inbox? First, TCP-IP splits your email into packets - if the connection between your computer and the mail server is unstable or noisy, this reduces the probability that your entire email is lost in transmission. If, say, 1 packet is lost, then you only need to re-transmit the lost packet. The packets go through 4 layers, and then on the receive side, they go through the same 4 layers in reverse to re-assemble the message.

![TCP-IP transmission/reception](https://cheapsslsecurity.com/blog/wp-content/uploads/2022/06/tcp-ip-model-process-1024x575.png)

Let's take a look at the layers of the TCP-IP model.

![TCP-IP layers](https://cheapsslsecurity.com/blog/wp-content/uploads/2022/06/tcp-ip-model-layers-and-their-functions.png)

**Layer 1, the highest layer, is the application layer.** It's what you, as the user, interacts with when sending and receiving data. It generates the data and requests the connection.

Layer 1 protocols:
* Simple Mail Transfer Protocol (SMTP): used to send emails
* Hypertext Transfer Protocol/Secure (HTTP/HTTPS): used for web access (browsing the internet)
* File Transfer Protocol (FTP): used to transmit files
* Secure Shell (SSH): used to securely access and manage remote servers

**Layer 2 is the transport layer.** It establishes the data connection between the two endpoints, splits the data into packets, determines the parameters of the transmission (amount of data, their destination, and transmission rate), and obtains acknowledgement from the recipient that the data is received.

Layer 2 protocols:
* Transmission Control Protocol (TCP): reliable, ordered delivery (web browsing, email, SSH)
* User Datagram Protocol (UDP): faster but unreliable (video streaming, gaming)

**Layer 3 is the Internet or IP layer.** It's responsible for sending the packets and is like a road traffic controller that directs the flow and speed of traffic.

Layer 3 protocols:
* Internet Protocol Versions 4 and 6 (IPv4/IPv6): used for routing data across the network
* Internet Control Message Protocol (ICMP): provides information to the endpoints in case of network problems

**Layer 4 is the physical layer**, which is responsible for the actual physical transmission of data via cables or wireless signals. This layer is standardized by communication standards like Ethernet and Wi-Fi. 

# <u>HTTP</u>

Can you explain how HTTP works? What kind of files and data are sent between web server and web client? Take a look at your notes on web development and front end

# <u>SSH</u>

"A cryptographic network protocol for operating network services securely over an unsecured network. Its most notable applications are remote login and command-line execution."
* Secure communication, usually over a network. Client-server architecture. Operates at the application layer (the highest layer) of the TCP/IP model.
* Used to remotely access and manage servers
* Designed for Unix-like operating systems
* Uses public-key cryptography, also known as asymmetric cryptography. Uses a pair of keys, one public, one private. The public key may be shared without compromising security. The public key is used to encrypt a message, yielding a ciphertext, and the private key is needed to decrypt the ciphertext to obtain the original message. 

A cryptographic network protocol used for securely connecting to remote machines over an unsecured network.
* Operates at the application layer (the highest layer) of the TCP/IP model
* Client-server architecture. Commonly used to remotely access and manage servers. Server-side port is 22 by default.
* Designed for Unix-like operating systems
* Allows port forwarding
* Supports secure file transfer through protocols like SCP (Secure Copy) and SFTP (SSH File Transfer Protocol)
* Uses key-based authentication and password-based authentication

## <u>Authentication</u>

SSH uses public-key cryptography (also known as asymmetric cryptography). There are two keys: the public key is placed on the remote server, and the private key is placed on your local machine. The public key is used to encrypt a message, yielding a ciphertext, and the private key is needed to decrypt the ciphertext to obtain the original message. 

The keys may be generated automatically at login, in which case the user is prompted for a password for authentication.

When the keys are manually generated by the user, the authentication is performed when the key pair is created, which means the user can login without a password prompt. The public key is placed on all devices that must allow access to the owner of the matching private key, i.e. the user can use the same key pair to remotely access multiple devices.

To manually create a key pair using your terminal, run either of these commands:  
`ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`  
`ssh-keygen -t ed25519 -C "your_email@example.com"`  

RSA is a legacy cryptographical algorithm, so Ed25519 is preferred if supported. The public key needs to be copied to the server's `~/.ssh/authorized_keys` file, and generally, the private key goes under your machine's `~/.ssh/` folder. The permissions for the private key must be set to 400 (user has read-only access).

The public key may be shared without compromising security since a user needs both the public and private keys for remote access.

## <u>SSH client</u>

In any shell, Windows or Linux, `ssh -V` will tell you if you have an SSH client installed.

These are some common commands for requesting SSH access into a server:
* `ssh -p 2222 username@localhost`: SSH into the VM hosted on your local machine using port 2222 with port forwarding (to 22 on the VM)
* `ssh -i your_private_key username@public_dns`: SSH into cloud machine @ public_dns using your private key. You can also use the public IP address instead of the public DN.

You can also specify servers in the SSH config file, typically ~/.ssh/config. For example, these configurations are equivalent to the SSH commands above.  
>Host local-vm
>    HostName localhost  
>    Port 2222  
>    User ryanwtsai  

>Host cloud-server    
>    HostName ec2-18-218-73-55.us-east-2.compute.amazonaws.com   
>    User ubuntu    
>    IdentityFile ~/.ssh/aws-ec2.pem  

With these in your config file, you can instead use the command `ssh host`, e.g.
* `ssh local-vm`
* `ssh cloud-server`

## <u>SSH server</u>

The server-side device must have SSH server software installed, which is also known as the Secure Shell Daemon (`sshd`). `sshd` listens on the SSH port (22 by default) for incoming connections. The SSH service may be configured via `/etc/ssh/sshd_config`. For example, you can
* Change the port (e.g. from 22 to 2222) to reduce exposure to brute-force attacks: `Port 2222`
* Disable root login via SSH (for security, do not allow the root user/superuser to log in): `PermitRootLogin no`

After editing `sshd_config`, you need to restart `sshd` via `sudo systemctl restart ssh`.

## <u>SSH tunneling via port forwarding</u>

You can create an encrypted tunnel from your local machine to a remote machine by using port forwarding: `ssh -L local_port:localhost:remote_port username@remote_host`.

For example, you might use a command like `ssh -L 8080:localhost:80 username@remote_host -i your_private_key` (if you have a private key for remote_host). This opens an encrypted tunnel for HTTP traffic between your machine and the remote machine, allowing you to access the private web server hosted on the remote machine by going to `http://localhost:8080` in your web client.

Let's break down the `-L` option for port forwarding:
* `8080`: the port on your local machine
* `localhost`: `localhost` is self-referential, but it's from the point of view of the remote machine, so in this case, `localhost` resolves to the remote machine
* `80`: the port on the remote machine

When you visit `http://localhost:8080`, your request is securely tunneled to the remote server, which sees the request as coming from itself at `localhost:80`.

Practical applications:
* **Accessing services on remote servers that are not publicly available.** Examples:
  * `ssh -L 8080:localhost:80 username@remote_host`: tunneling to a server that is configured to listen only on `localhost`. Request path: `local_machine:8080 -> remote_host:80`.
  * `ssh -L 8443:intranet.company.com:443 username@corporate_server`: tunneling to a private company server to access company services. Request path: `local_machine:8443 -> corporate_server -> intranet.company.com:443`.
* **Bypassing network restrictions.** If you're on a restricted network that blocks access to certain websites or services, you can set up an SSH tunnel through a server you control to bypass those restrictions, e.g. `ssh -L 8080:example.com:80 username@remote_server`. Request path: `local_machine:8080 -> remote_server -> example.com:80`.