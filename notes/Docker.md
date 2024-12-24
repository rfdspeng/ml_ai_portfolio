# <u>Docker introduction</u>

To begin, you need to understand a little bit about computer HW-SW architecture. At a very high level:
* The OS is the software interface between physical hardware (CPU, memory, devices) and application software. The kernel is the core of the OS.
* In the hierarchy, application software is at the top, followed by the OS, and then physical hardware.

**To virtualize hardware or OS** means to create a simulation of it so that multiple isolated, independent instances can run on the same physical resource:
* Virtual machines virtualize OS and below (hardware). Each VM is virtually a computer with its own OS, kernel, and hardware.
* Containers virtualize only the OS environment (filesystem, processes, and networking) and uses the host computer's kernel to access hardware.
* In both cases, you are creating an isolated environment.

**Docker is a containerization technology**. A container, which is an instance of an image, is like a very lightweight virtual machine. The Docker image contains all the information needed to create a container, including any software needed (like OS, specific software versions, and libraries). For example, you can containerize a web application and deploy it on any server and get consistent behavior.

|Virtual Machine|Container|
|---------------|---------|
|Full OS with separate kernel (5G Ubuntu installation)|Shares host OS's kernel (30MB Ubuntu container)|
|VMs virtualize OS, kernel, and hardware|Containers only virtualize the OS environment|
|Slower to start|Starts instantly|
|Resource-intensive|Efficient with minimal overhead|

Docker is the most popular platform for containerization and has three main components:
* Image: read-only template with instructions for creating a container
* Container: a running instance of an image
* Docker engine: the runtime (software that manages the execution of programs) that builds, runs, and manages containers. Includes the Docker daemon, CLI, and APIs.

# <u>Working with Docker</u>

You can download Docker Desktop, but this section will focus on working with Docker in a Linux terminal.

Go to hub.docker.com to search for images, e.g. Ubuntu, Python, miniconda. This will allow you to create containers that emulate an Ubuntu OS, an OS with Python installed, or an OS with miniconda installed.

Docker setup: 
* `sudo apt install -y docker.io`  
* `docker --version`  
* `sudo systemctl start docker`: launches the Docker engine
* `sudo systemctl enable docker`: enables Docker to start automatically on system boot
* `docker info`: query Docker runtime info

## <u>Basic Docker commands</u>
* `docker pull image_name:(tag_name)`: pull image_name from Docker hub, e.g. `ubuntu`  
* `docker images`: see all pulled images, especially REPOSITORY (name) and TAG (tag_name)
* `docker rmi image_name`: remove image_name  
* `docker run image_name`: create container  
* `docker container ls`: show running containers
* `docker ps`: show running containers (equivalent to `docker container ls`)
* `docker ps -a`: show all containers  
* `docker ps -a -q`: show all containers, IDs only  
* `docker ps --size`: show container size
* `docker stop container_id`: stop container  
* `docker start -i container_id`: resume an exited container in interactive mode (`-i`)
* `docker rm container_id`: remove container
* `docker rm $(docker ps -a -q)`: remove all containers 

Ubuntu image in interactive mode:  
* `docker run -it ubuntu`: create Ubuntu container in interactive mode, and you can work in the container just like in any other Linux terminal. `-it` means interactive mode with a terminal. You can also run `docker run -it ubuntu bash` for a bash terminal.

## <u>Creating a custom image and container using a Dockerfile</u>

https://docs.docker.com/reference/dockerfile/

The Dockerfile contains the instructions for building the image and running the container. 

`FROM`, `RUN`, `COPY`, and `WORKDIR` commands build the layers of the image. They configure the environment. These layers are cached, which means that if you rebuild the image, Docker can skip the layers that have already been built. 

Each `RUN` command runs in its own non-interactive shell, which means that this installs miniconda in `/`, not `/root`.
```bash
RUN cd /root
RUN wget miniconda_url
RUN bash miniconda.sh
```
To install miniconda in `/root`, you need to run all of these shell commands in the same `RUN`.
```bash
RUN cd /root && \
    wget miniconda_url && \
    bash miniconda.sh
```

For efficiency and to reduce the number of layers in the image, it's recommended to group related commands under a single `RUN` using `&&`.

`CMD` is the default command for the container at runtime and can be overridden by providing a command when starting the container.

`ENTRYPOINT` is a runtime command that is always executed; it cannot be overridden, only appended to.

`CMD ["python", "app.py"]` can be overridden at runtime by `docker run image_name python other_script.py`.

`ENTRYPOINT ["python", "app.py"]` means `python app.py` is always run when the container starts. It doesn't make sense to add another command at runtime.

You can combine `ENTRYPOINT` with `CMD`. In the command below, `python` is always called, and `app.py` is the default script. You can overwrite the default script at runtime using `docker run image_name other_script.py`.
```bash
ENTRYPOINT["python"]
CMD ["app.py"]
```

Like `RUN`, each `CMD` and `ENTRYPOINT` runs its own non-interactive shell.

**Example Dockerfiles:**
```bash
FROM python:3.8-slim # this is the base image, which is the first layer of our custom image. In this case, the base image has Ubuntu and Python installed.

RUN apt-get update # update packages

RUN apt-get install -y git # install required packages

COPY sample.py /app/sample.py # copy file(s) from the host directory (where Dockerfile resides) into /app directory of the container

WORKDIR /app # set working directory. This applies to any subsequent instructions in the Dockerfile and is the working directory for the container at runtime

CMD ["python", "sample.py"] # runtime command. JSON array syntax is used for consistent behavior.
```
```bash
FROM python:3.8-slim

RUN apt-get update

RUN apt-get install python3-pip -y

COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```
```bash
FROM python:3.12-slim

# Set Miniconda path
ENV PATH="/root/miniconda3/bin:${PATH}"

# Install system dependencies and Miniconda
RUN apt update && apt upgrade -y && apt install wget -y && \
    cd /root && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /root/miniconda3 && \
    /root/miniconda3/bin/conda --version

# Copy application files
WORKDIR /root/app
COPY book_rec_app.py .
COPY environment.yml .
COPY .streamlit ./.streamlit

# Create conda environment
RUN conda env create -n myenv --file environment.yml

# Expose port for Streamlit
EXPOSE 8501

# Start Streamlit using activated conda environment
ENTRYPOINT ["bash", "-c", "source activate myenv && streamlit run book_rec_app.py"]
```

To build the image, use the command `docker build -t image_name:tag_name Dockerfile_dir`. 
* `image_name:tag_name` gives a name to your image; `tag_name` is optional and will default to `latest`. Usually `tag_name` is used for versioning, e.g. `v1` or `1.0.0` or whatever you want. 
* `Dockerfile_dir` is the directory where the Dockerfile resides. Generally, this will be `.` for current directory.

To re-tag the image after building, use `docker tag image_name:tag_name image_name_new:tag_name_new`. You will see both images when you run `docker images`, and they will have the same Image ID.

## <u>Size</u>

The output of docker ps --size includes two size metrics:

    Container Size (3.32kB):
        This indicates the amount of writable storage used by the container.
        It reflects changes made to the container since it started, such as newly created files, modifications to existing files, or installed packages.
        In this case, the container has added or changed 3.32kB of data compared to the image it was based on.

    Virtual Size (5.81GB):
        This represents the total size of the image the container is running on, including all its base layers.
        It shows the size of the entire file system the container has access to, which includes the read-only layers of the image and the writable layer.

Key Notes:

    Writable Layer (Container Size): Tracks changes specific to this container.
    Virtual Size: Combines the base image size and the writable layer for the container.
    If the container is running an image that is 5.81GB in size (e.g., an OS plus additional software), this virtual size reflects that.

Why the Distinction?

    Efficient Storage: Docker uses a layered file system, meaning the container uses the base image layers without duplicating them. The writable layer is the only layer unique to the container, which is why it tends to be small.
    Debugging/Optimization: The writable layer size can help identify containers that are growing unexpectedly, signaling inefficient processes or excessive file creation.

If you see unexpectedly large writable sizes, you may need to check logs, temporary files, or cache buildup inside the container.

Not quite! The 5.81GB virtual size does not mean your container is consuming 5.81GB of storage on your local host. Here's why:
Layered File System

Docker uses a layered file system where:

    The image layers (base OS, libraries, etc.) are shared among containers running the same image.
        If you have multiple containers based on the same image, the image layers are stored only once.
        In this case, the 5.81GB virtual size is primarily the image's read-only layers, shared across any containers using the same image.

    The writable layer (3.32kB in your case) is the container-specific part, unique to each container.
        This writable layer is typically very small unless the container writes or modifies a lot of files.

Actual Disk Usage

    If the base image (5.81GB) is already present on your host, the extra space consumed by the container is just the writable layer (3.32kB).
    If this is the first time you've pulled the image, Docker would download and store the entire 5.81GB image on your host.

To Check Actual Disk Usage:

Run:

docker system df

This will provide a breakdown of:

    Space used by images.
    Space used by containers.
    Space used by volumes and build cache.

Summary

Your container appears to use 5.81GB because it includes the size of the base image (virtual size), but:

    If the image is shared by other containers, it isn't duplicated.
    The actual additional storage used by your container is the writable layer (3.32kB).

## </u>Container networking</u>

A container has its own IP address and ports and can talk to its host machine and to other containers running on the host machine through virtual networks.

There are 3 default virtual networks: `bridge`, `host`, and `none`. When you create a new container with `docker run`, you can specify which network the container is connected to. If you do not specify, the container is added to the `bridge` network. A container on the `host` network is effectively added to the host machine's network, which directly exposes the container to other devices on the host machine's network. The `none` bridge completely isolates the container from everything else. Beyond these 3, you can create new virtual networks. To create a new virtual network, use `docker network create <network-name>`. After this, you can then add new containers to `<network-name>`.

You can talk to a container with its container ID, but you can also specify a name for the container when you create it with `docker run`. This allows you to talk to a container using its name.

By default, when `docker run` creates a new container, it adds the container to a network called `bridge`. Containers on the same network can talk to each other. 

Here's the full command with options: `docker run --name <container-name> --network <network-name> <image-name>`

Example command: `docker run --name my-web-app --network bridge nginx`. This starts a container, with `nginx` installed, named `my-web-app` and connected to `bridge`.

Instead of specifying a network, you can specify a container to connect to: `docker run --name <container-name> --network container:<container-to-connect-name> <image-name>`

Let's say you create a container that has an exposed port (e.g. 8000 for the backend of a web application or 8501 for a Streamlit application). To allow devices connected to the host machine to talk to your container, you can create a port forwarding rule when you create the container: `docker run -d -p <host-port>:<container-port> <image-name>`. (The `-d` option runs the container in detached mode, i.e. in the background.)

Example command: `docker run -d -p 8501:8501 streamlit-app` will allow devices connected to the host machine to access the Streamlit application running on port 8501 on the container. In this case, the host port is the same number as the container port, but you can specify a different number. For example, `85010:8501` means that host port 85010 will forward to container port 8501.

Persistent memory after deleting container.
* `docker volume create app_data`: for persistent storage
* In Dockerfile: `VOLUME <folder-name>`. `<folder-name>` isn't equal to `app_data`? `<folder-name>` is the directory within the container that you want to map to the persistent storage
* `docker run -v app_data:<folder-name>`: `app_data` is a folder in our local computer (host machine). Mapping.

`docker exec -it container_id`: run container in interactive mode

`docker network ls`: see available networks

`docker run -e ENV_VAR=VALUE image_name`: set environment variable inside the container

