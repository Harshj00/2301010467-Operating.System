import os

def task2_exec_command(n, cmd):
    for _ in range(n):
        pid = os.fork()
        if pid == 0:
            try:
                os.execvp(cmd[0], cmd)
            except FileNotFoundError:
                print(f"Command not found: {cmd[0]}")
            os._exit(1)
    for _ in range(n):
        os.wait()

if __name__ == "__main__":
    n = int(input("Enter number of child processes to create: "))
    cmd = input("Enter command to execute (e.g., ls -l): ").split()
    task2_exec_command(n, cmd)
