import os
import subprocess
import time

def task1_process_creation(n):
    """
    Task 1: Create N child processes using os.fork().
    Each child prints its PID, Parent PID, and a custom message.
    Parent waits for all children using os.wait().
    """
    print(f"\n--- Task 1: Creating {n} child processes ---")
    for _ in range(n):
        pid = os.fork()
        if pid == 0:
            # Child process
            print(f"Child PID: {os.getpid()}, Parent PID: {os.getppid()} - Hello from child!")
            os._exit(0)
    # Parent waits for all children to finish
    for _ in range(n):
        os.wait()
    print("Task 1 complete: All child processes finished.\n")

def task2_command_execution(commands):
    """
    Task 2: Modify Task 1 to have each child execute a Linux command using os.execvp().
    Commands is a list of command argument lists, e.g., [["ls", "-l"], ["date"], ["ps"]]
    """
    print("\n--- Task 2: Command Execution by child processes ---")
    for cmd in commands:
        pid = os.fork()
        if pid == 0:
            # Child executes the command
            try:
                print(f"Child PID {os.getpid()} executing command: {' '.join(cmd)}")
                os.execvp(cmd[0], cmd)
            except Exception as e:
                print(f"Execution failed: {e}")
            os._exit(1)  # Exit if exec fails
    # Parent waits for all children
    for _ in commands:
        os.wait()
    print("Task 2 complete: All commands executed.\n")

def task3_zombie_orphan():
    """
    Task 3: Demonstrate Zombie and Orphan processes.
    Zombie: Fork a child and skip wait() in parent.
    Orphan: Parent exits before child finishes.
    Use ps -el | grep defunct externally to verify zombies.
    """
    print("\n--- Task 3: Zombie and Orphan Processes ---")
    pid = os.fork()
    if pid == 0:
        # Child process
        print(f"Child PID {os.getpid()} running; Parent PID {os.getppid()}")
        time.sleep(10)  # Sleep long enough to observe zombie/orphan state
        print("Child done")
        os._exit(0)
    else:
        # Parent process
        print(f"Parent PID {os.getpid()} created child {pid}")
        # Intentionally NOT calling os.wait() to create a zombie process
        print("Parent sleeping 5 seconds before exiting (to create orphan)")
        time.sleep(5)
        print("Parent exiting now")
        os._exit(0)

def task4_inspect_proc(pid):
    """
    Task 4: Inspect process info from /proc/[pid]
    Prints process name, state, memory usage, executable path, and open file descriptors.
    """
    print(f"\n--- Task 4: Inspecting /proc/{pid} ---")
    try:
        with open(f"/proc/{pid}/status", "r") as f:
            status = f.read()
        print("Process Status:")
        print(status)
    except Exception as e:
        print(f"Error reading /proc/{pid}/status: {e}")
        return

    try:
        exe_path = os.readlink(f"/proc/{pid}/exe")
        print(f"\nExecutable Path:\n{exe_path}")
    except Exception as e:
        print(f"Error reading /proc/{pid}/exe: {e}")

    try:
        fd_list = os.listdir(f"/proc/{pid}/fd")
        print("\nOpen File Descriptors:")
        for fd in fd_list:
            try:
                link = os.readlink(f"/proc/{pid}/fd/{fd}")
                print(f"FD {fd}: {link}")
            except Exception as e:
                print(f"FD {fd}: Permission denied or error")
    except Exception as e:
        print(f"Error reading /proc/{pid}/fd: {e}")

def cpu_intensive_task():
    """
    Simple CPU-intensive task: count to a large number.
    """
    count = 0
    for _ in range(10**7):
        count += 1
    print(f"PID {os.getpid()} finished counting.")

def task5_process_prioritization(children_nice):
    """
    Task 5: Create CPU-intensive child processes,
    Assign different nice values and observe execution order.
    children_nice: list of nice values to assign to each child.
    """
    print("\n--- Task 5: Process Prioritization using nice values ---")
    pids = []
    for nice_val in children_nice:
        pid = os.fork()
        if pid == 0:
            # Child process
            os.nice(nice_val)
            print(f"Child PID {os.getpid()} started with nice value {nice_val}")
            cpu_intensive_task()
            os._exit(0)
        else:
            pids.append(pid)
    for pid in pids:
        os.waitpid(pid, 0)
    print("Task 5 complete: All prioritized processes finished.\n")

if __name__ == "__main__":
    try:
        # Task 1: Create 3 child processes
        task1_process_creation(3)

        # Task 2: Execute commands
        commands = [["ls", "-l"], ["date"], ["ps", "aux"]]
        task2_command_execution(commands)

        # Task 3: Run zombie and orphan demonstration
        # WARNING: This will cause a zombie process to appear until the child exits.
        print("Running Task 3: zombie/orphan demo (run 'ps -el | grep defunct' in another terminal to observe)")
        task3_zombie_orphan()

        # Task 4: Inspect process info - ask user for PID
        pid_input = input("\nEnter a PID to inspect from /proc (or press Enter to skip): ").strip()
        if pid_input.isdigit():
            task4_inspect_proc(pid_input)
        else:
            print("Skipping Task 4")

        # Task 5: Process prioritization with different nice values
        nice_values = [0, 5, 10]
        task5_process_prioritization(nice_values)

    except KeyboardInterrupt:
        print("\nScript interrupted. Exiting.")
