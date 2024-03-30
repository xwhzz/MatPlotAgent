import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dir', type=str, default='../workspace')
args = parser.parse_args()

current_directory = args.dir
target_directories = [d for d in os.listdir(current_directory) if os.path.isdir(d) and "example" in d]


merged_filename = "lack_library.txt"
with open(merged_filename, 'w') as merged_file:
    for directory in target_directories:
        # Step 2: Search for files within the directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                if "3" in file and "log" in file:
                    # Step 3: Read the content of each matching file
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r') as f:
                        contents = f.read()
                        if "ModuleNotFoundError:" in contents:
                            merged_file.write(f"Contents of {full_path}:\n")
                            merged_file.write(contents + "\n\n")  # Add a newline between files for clarity

print(f"All matching files have been merged into {merged_filename}.")
