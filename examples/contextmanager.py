with open("sample.txt", "w") as file:
    file.write("Default context manager using with\n")

class File:
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        print("Entering context...")
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        print("Exited context.")
        return True

with File("sample.txt", "a") as file:
    file.write("Implementing a context manager as a class\n")

with File("sample.txt", "a") as file:
    file.unknown_method()

from contextlib import contextmanager

@contextmanager
def open_file(name):
    print("Entering context...")
    f = open(name, "a")
    try:
        yield f
    finally:
        f.close()
        print("Exited context.")

with open_file("sample.txt") as file:
    file.write("Implementing a context manager as a generator\n")

print(type(open_file("sample.txt")))