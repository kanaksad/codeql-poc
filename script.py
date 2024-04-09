import os
import subprocess
import time
import json

def run_command_in_subdirs(directory, command_template, db_dir, res_dir, timings_file):
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    initial_dir = os.getcwd()
    timings = []

    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            # Extract the last part of the directory path
            dir_name = os.path.basename(path)
            # Format the system command with the directory name
            command = command_template.format(dir_name=dir_name, db_dir=db_dir, res_dir=res_dir)
            os.chdir(path)

            # Start timing
            start_time = time.time()
            
            # Run the command using subprocess.run
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            
            # End timing
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Store timing information
            timings.append({"directory": dir_name, "command": command, "elapsed_time": elapsed_time})

            print(result.stdout)  # Print standard output of the command
            os.chdir(initial_dir)

    # Serialize timing information to a JSON file
    with open(timings_file, "w") as f:
        json.dump(timings, f, indent=4)

dataset_directory = '/home/kdas006/dataset'
db_dir = '/home/kdas006/codeql-home/playing-around/codeql-poc-repo/db'
res_dir = '/home/kdas006/codeql-home/playing-around/codeql-poc-repo/results'
timings_file = '/home/kdas006/codeql-home/playing-around/codeql-poc-repo/timings.json'

# Use {dir_name} in the command where you want the directory name to appear
create_db = "codeql database create --language=java {db_dir}/{dir_name}"
store_res = "codeql database analyze {db_dir}/{dir_name} /home/kdas006/codeql-home/codeql-repo/java/ql/src/codeql-suites/java-security-extended.qls --format=sarifv2.1.0 --sarif-add-file-contents --output={res_dir}/{dir_name}.sarif"

run_command_in_subdirs(dataset_directory, create_db, db_dir, res_dir, timings_file)
#run_command_in_subdirs(dataset_directory, store_res, db_dir, res_dir, timings_file)

