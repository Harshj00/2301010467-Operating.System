import os
import time

def create_zombie():
    pid = os.fork()
    if pid == 0:
        print(f"Child PID {os.getpid()} exiting immediately to become zombie.")
        os._exit(0)
    else:
        print("Parent sleeping for 15 seconds. Check for zombies with 'ps -el | grep defunct' in another terminal.")
        time.sleep(15)
        print("Parent exiting.")

def create_orphan():
    pid = os.fork()
    if pid == 0:
        print(f"Child PID {os.getpid()} running, will be orphaned. Sleeping for 15 seconds.")
        time.sleep(15)
        print("Child finished.")
    else:
        print("Parent exiting immediately, orphaning child.")
        os._exit(0)

if __name__ == "__main__":
    choice = input("Choose scenario:\n1. Zombie process\n2. Orphan process\nEnter choice (1 or 2): ")
    if choice == "1":
        create_zombie()
    elif choice == "2":
        create_orphan()
    else:
        print("Invalid choice.")
