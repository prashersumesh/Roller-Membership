import os
import subprocess

# Path to the PDFs directory
pdfs_directory = "src/membership/PDFs"

# Path to the log file
log_file = "log.csv"

# Path to the script to run
script_to_run = "src/gdrive.py"

# Delete all files in the PDFs directory
def delete_files_in_directory(directory):
    if os.path.exists(directory):
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):  # Only delete files, not subdirectories
                os.remove(file_path)
                print(f"Deleted: {file_path}")
    else:
        print(f"Directory does not exist: {directory}")

# Delete the log file
def delete_log_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Deleted log file: {file_path}")
    else:
        print(f"Log file does not exist: {file_path}")

# Run the script
def run_script(script_path):
    if os.path.exists(script_path):
        subprocess.run(["python", script_path], check=True)
        print(f"Executed script: {script_path}")
    else:
        print(f"Script does not exist: {script_path}")

# Execute the operations
if __name__ == "__main__":
    delete_files_in_directory(pdfs_directory)
    delete_log_file(log_file)
    run_script(script_to_run)
