import os
import subprocess

def run_command_in_subdirs(directory, command_template, db_dir, res_dir):
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return

    initial_dir = os.getcwd()

    for entry in os.listdir(directory):
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            # Extract the last part of the directory path
            dir_name = os.path.basename(path)
            # Format the system command with the directory name
            command = command_template.format(dir_name=dir_name, db_dir=db_dir, res_dir=res_dir)
            os.chdir(path)
            # Run the command using subprocess.run
            result = subprocess.run(command, shell=True, text=True, capture_output=True)
            print(result.stdout)  # Print standard output of the command
            os.chdir(initial_dir)

dataset_directory = '/home/kdas006/dataset'
db_dir = '/home/kdas006/codeql-home/playing-around/codeql-poc-repo/db'
res_dir = '/home/kdas006/codeql-home/playing-around/codeql-poc-repo/results'
# Use {dir_name} in the command where you want the directory name to appear
create_db = "codeql database create --language=java {db_dir}/{dir_name}"

store_res = "codeql database analyze {db_dir}/{dir_name} /home/kdas006/codeql-home/codeql-repo/java/ql/src/codeql-suites/java-security-extended.qls --format=sarifv2.1.0 --sarif-add-file-contents --output={res_dir}/{dir_name}.sarif"
run_command_in_subdirs(dataset_directory, create_db, db_dir, res_dir)
run_command_in_subdirs(dataset_directory, store_res, db_dir, res_dir)

