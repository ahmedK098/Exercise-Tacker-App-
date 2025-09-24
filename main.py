import subprocess
import time
import threading

# List the files you want to run
scripts_to_run = ['app.py', 'tracker.py']

# This list will store the Popen objects so we can terminate them later
processes = [] 

def run_script(script_name):
    """Function to run a script using subprocess.Popen."""
    print(f"Starting {script_name}...")
    # Start the script as a separate OS process
    process = subprocess.Popen(['python', script_name])
    # Add the subprocess object to the global list for tracking
    processes.append(process) 

# Start each script in a separate thread
threads = []
for script in scripts_to_run:
    # Create a new thread targeting the run_script function
    thread = threading.Thread(target=run_script, args=(script,))
    thread.daemon = True # Allows main program to exit if threads are still running
    thread.start()
    threads.append(thread)

print("Both scripts are now running concurrently.")

try:
    # Keep the main script running to prevent the subprocesses from being terminated
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminating scripts...")
    # Cleanly terminate all running subprocesses
    for process in processes:
        process.terminate()
        process.wait()
    print("All scripts terminated.")