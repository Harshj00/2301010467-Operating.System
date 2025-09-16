import os

def inspect_process(pid):
    base_path = f"/proc/{pid}"
    try:
        with open(f"{base_path}/status") as f:
            status_data = f.read()
        exe_path = os.readlink(f"{base_path}/exe")
        fd_list = os.listdir(f"{base_path}/fd")

        print(f"\nProcess status (/proc/{pid}/status):\n{status_data}")
        print(f"Executable path (/proc/{pid}/exe): {exe_path}")
        print(f"Open file descriptors (/proc/{pid}/fd): {fd_list}\n")
    except FileNotFoundError:
        print(f"Process {pid} does not exist or access denied.")

if __name__ == "__main__":
    pid = input("Enter PID to inspect: ")
    inspect_process(pid)
