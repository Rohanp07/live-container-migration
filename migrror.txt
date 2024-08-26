import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import csv
import psutil

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

# Function to append checkpoint data to a CSV file
def append_checkpoint_data_to_csv(filename, time_taken, cpu_usage, memory_change, total_size):
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['Time Taken (s)', 'CPU Usage (%)', 'Memory Change (bytes)', 'Total Size (bytes)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Write header only once when file is created

        writer.writerow({
            'Time Taken (s)': time_taken,
            'CPU Usage (%)': cpu_usage,
            'Memory Change (bytes)': memory_change,
            'Total Size (bytes)': total_size
        })

# Event handler for monitoring directory changes
class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self, container_name):
        self.first_checkpoint_done = False
        self.previous_size = get_directory_size(directory_to_monitor)
        self.container_name = container_name

    def on_any_event(self, event):
        if event.is_directory:
            return

        current_size = get_directory_size(directory_to_monitor)

        if current_size != self.previous_size:
            size_change = current_size - self.previous_size
            self.previous_size = current_size

            if size_change > 0:
                print(f"Memory increased by {size_change} bytes.")
            elif size_change < 0:
                print(f"Memory decreased by {-size_change} bytes.")
            else:
                print("No memory change detected.")

            start_time = time.time()
            if not self.first_checkpoint_done:
                print("Executing initial checkpoint...")
                execute_command(f"sudo podman container checkpoint {self.container_name} -R -P")
                self.first_checkpoint_done = True
            else:
                print("Executing subsequent checkpoint...")
                execute_command(f"sudo podman container checkpoint {self.container_name} -R --with-previous")
            end_time = time.time()

            # Calculate time taken for checkpoint
            time_taken = end_time - start_time

            # Get CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)

            # Total size of the container directory
            total_size = current_size

            # Append data to CSV
            append_checkpoint_data_to_csv('checkpoint_data.csv', time_taken, cpu_usage, size_change, total_size)

if len(sys.argv) != 2:
    print("Usage: python3 migrror.py <container_name>")
    sys.exit(1)

container_name = sys.argv[1]
directory_to_monitor = "/var/lib/containers/storage/overlay"

event_handler = DirectoryChangeHandler(container_name)
observer = Observer()
observer.schedule(event_handler, path=directory_to_monitor, recursive=True)

observer.start()
print(f"Migration started for container '{container_name}'. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping migration...")
finally:
    observer.stop()
    observer.join()

print("Checkpointing completed.")
