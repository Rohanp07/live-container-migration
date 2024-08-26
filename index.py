import subprocess
import os
import signal

# Global variable to store the migration process
migration_process = None

def clear_terminal():
    """Clear the terminal screen."""
    os.system('clear')

def show_menu():
    """Display the menu options."""
    print("Please select an option:")
    print("1. Show running Containers (sudo podman ps)")
    print("2. Show all Containers (sudo podman ps -a)")
    print("3. Migrate a container")
    # print("4. Restore")
    print("4. Exit")

def run_command(command):
    """Run a command and display the output in the current terminal."""
    clear_terminal()
    subprocess.run(command, shell=True)
    input("\nPress any key to return to the menu...")
    clear_terminal()

def migrate_container():
    """Migrate a selected container."""
    global migration_process
    
    # Show running containers
    clear_terminal()
    subprocess.run("sudo podman ps", shell=True)
    
    # Ask for container ID or name
    container_name = input("\nEnter the container ID or name to migrate: ")
    
    # Start the migration process in the background and capture output
    clear_terminal()
    print(f"Starting migration for container '{container_name}' in the background.")
    
    migration_process = subprocess.Popen(
        ["python3", "/home/rohan/Desktop/live-container-migration/migrror.py", container_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Monitor progress
    try:
        while True:
            output = migration_process.stdout.readline()
            if output == "" and migration_process.poll() is not None:
                break
            if output:
                print(output.strip())
    except KeyboardInterrupt:
        stop_migration()

    input("\nPress any key to return to the menu...")
    clear_terminal()

def stop_migration():
    """Stop the migration process."""
    global migration_process
    if migration_process:
        migration_process.terminate()  # Send a termination signal to the process
        try:
            migration_process.wait(timeout=10)  # Wait up to 10 seconds for the process to terminate
            print("Migration process has been stopped.")
        except subprocess.TimeoutExpired:
            print("Failed to stop migration process within the timeout period.")
    else:
        print("No migration process is running.")

def main():
    while True:
        clear_terminal()
        show_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            # Show running containers
            run_command("sudo podman ps")
        elif choice == '2':
            # Show all containers
            run_command("sudo podman ps -a")
        elif choice == '3':
            # Migrate a container
            migrate_container()
        # elif choice == '4':
        #     # Restore (replace with the path to your restore script or command)
        #     script_path = "/path/to/restore_script.py"
        #     subprocess.Popen(["python3", script_path], shell=True)
        elif choice == '4':
            # Exit the program
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress any key to return to the menu...")

if __name__ == "__main__":
    main()
