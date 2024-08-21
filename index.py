import subprocess
import os
import signal

# Global variable to store the migration process PID
migration_process_pid = None

def clear_terminal():
    """Clear the terminal screen."""
    os.system('clear')

def show_menu():
    """Display the menu options."""
    print("Please select an option:")
    print("1. Show running Containers (sudo podman ps)")
    print("2. Show all Containers (sudo podman ps -a)")
    print("3. Migrate a container")
    print("4. Restore")
    print("5. Exit")

def run_command(command):
    """Run a command and display the output in the current terminal."""
    clear_terminal()
    subprocess.run(command, shell=True)
    input("\nPress any key to return to the menu...")
    clear_terminal()

def run_in_terminal(command):
    """Open a new terminal window and run a command."""
    global migration_process_pid
    process = subprocess.Popen(
        f'gnome-terminal -- bash -c "{command}; exec bash"',
        shell=True,
        preexec_fn=os.setsid  # To allow sending signals to the process group
    )
    migration_process_pid = process.pid

def migrate_container():
    """Migrate a selected container."""
    global migration_process_pid
    
    # Show running containers
    clear_terminal()
    subprocess.run("sudo podman ps", shell=True)
    
    # Ask for container ID or name
    container_name = input("\nEnter the container ID or name to migrate: ")
    
    # Start the migration process in a new terminal
    clear_terminal()
    print(f"Starting migration for container '{container_name}' in a new terminal.")
    run_in_terminal(f"python3 /home/rohan/Desktop/live-container-migration/migrror.py {container_name}")
    
    # Provide an option to stop the migration from the main terminal
    stop_migration_process = input(f"\nPress 'S' to stop the migration process or any other key to return to the menu: ").strip().lower()
    if stop_migration_process == 's':
        clear_terminal()
        stop_migration()
    else:
        print("Returning to the menu.")
    input("\nPress any key to return to the menu...")
    clear_terminal()

def stop_migration():
    """Stop the migration process."""
    global migration_process_pid
    if migration_process_pid:
        try:
            os.killpg(os.getpgid(migration_process_pid), signal.SIGTERM)  # Kill the process group
            print("Migration process has been stopped.")
        except Exception as e:
            print(f"Failed to stop migration process: {e}")
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
        elif choice == '4':
            # Restore (replace with the path to your restore script or command)
            script_path = "/path/to/restore_script.py"
            run_in_terminal(f"python3 \"{script_path}\"")
        elif choice == '5':
            # Exit the program
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
            input("\nPress any key to return to the menu...")

if __name__ == "__main__":
    main()