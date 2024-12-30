![Computer Architecture](https://www.tutorialspoint.com/operating_system/images/conceptual_view.jpg)

At a very high level:
* The OS is the software interface between physical hardware (CPU, memory, devices) and application software. The kernel is the core of the OS.
* In the hierarchy, application software is at the top, followed by the OS, and then physical hardware.

To virtualize hardware or OS means to create a simulation of it so that multiple independent instances can run on the same physical resource:
* Virtual machines virtualize OS and below (hardware). Each VM is virtually a computer with its own OS, kernel, and hardware.
* Containers virtualize only the OS environment (filesystem, processes, and networking) and uses the host computer's kernel to access hardware.