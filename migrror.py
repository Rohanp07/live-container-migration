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

# Event handler for monitoring directory changes
class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.first_checkpoint_done = False
        self.last_modified_files = set()

    def on_any_event(self, event):
        # Ignore directories or events not related to file changes
        if event.is_directory:
            return
        
        # Check if the file was recently modified by our own operation
        if event.src_path in self.last_modified_files:
            self.last_modified_files.remove(event.src_path)
            return

        # Determine which command to execute
        if not self.first_checkpoint_done:
            print("Executing initial checkpoint...")
            execute_command("sudo podman container checkpoint -l -R -P")
            self.first_checkpoint_done = True
        else:
            print("Executing subsequent checkpoint...")
            execute_command("sudo podman container checkpoint -l -R --with-previous")
        
        # After executing the command, mark the changed files
        self.mark_recently_modified_files()

    def mark_recently_modified_files(self):
        # List files that have been recently modified by the checkpoint operation
        for root, _, files in os.walk(directory_to_monitor):
            for file in files:
                filepath = os.path.join(root, file)
                self.last_modified_files.add(filepath)

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
