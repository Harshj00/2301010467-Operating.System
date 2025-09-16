import os

def task1_create_processes(n):
    for _ in range(n):
        pid = os.fork()
        if pid == 0:  # child process
            print(f"Child PID: {os.getpid()}, Parent PID: {os.getppid()}, Message: Hello from child")
            os._exit(0)
    for _ in range(n):
        os.wait()

if __name__ == "__main__":
    n = int(input("Enter number of child processes to create: "))
    task1_create_processes(n)
