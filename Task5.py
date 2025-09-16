import os
import time

def cpu_intensive_task():
    count = 0
    for _ in range(10_000_000):
        count += 1
    print(f"Process {os.getpid()} completed CPU-intensive task.")

def priority_test(n):
    nice_values = [0, 5, 10, 15, 20][:n]
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            os.nice(nice_values[i])
            start_time = time.time()
            cpu_intensive_task()
            end_time = time.time()
            print(f"PID {os.getpid()} with nice {nice_values[i]} took {end_time - start_time:.2f} seconds")
            os._exit(0)
    for _ in range(n):
        os.wait()

if __name__ == "__main__":
    n = int(input("Enter number of child processes (up to 5): "))
    priority_test(n)
