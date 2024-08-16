import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Function to execute a shell command
def execute_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command '{command}' failed with error: {e}")

# Function to calculate the total size of a directory
def get_directory_size(directory):
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

# Event handler for monitoring directory changes
class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.first_checkpoint_done = False
        self.previous_size = get_directory_size(directory_to_monitor)

    def on_any_event(self, event):
        # Ignore directories or events not related to file changes
        if event.is_directory:
            return

        # Calculate the directory size after the event
        current_size = get_directory_size(directory_to_monitor)

        # Check if there was a memory change
        if current_size != self.previous_size:
            size_change = current_size - self.previous_size
            self.previous_size = current_size

            if size_change > 0:
                print(f"Memory increased by {size_change} bytes.")
            elif size_change < 0:
                print(f"Memory decreased by {-size_change} bytes.")
            else:
                print("No memory change detected.")

            # Perform the appropriate checkpoint
            if not self.first_checkpoint_done:
                print("Executing initial checkpoint...")
                execute_command("sudo podman container checkpoint -l -R -P")
                self.first_checkpoint_done = True
            else:
                print("Executing subsequent checkpoint...")
                execute_command("sudo podman container checkpoint -l -R --with-previous")

# Directory to monitor
directory_to_monitor = "/var/lib/containers/storage/overlay"

# Initialize the event handler and observer
event_handler = DirectoryChangeHandler()
observer = Observer()
observer.schedule(event_handler, path=directory_to_monitor, recursive=True)

# Start the observer
observer.start()

try:
    # Run the observer for 10 seconds
    time.sleep(10)
finally:
    # Stop the observer after 10 seconds
    observer.stop()
    observer.join()

print("Monitoring completed.")
