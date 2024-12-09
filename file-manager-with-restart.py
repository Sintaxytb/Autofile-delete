import os
import shutil
import time
from pathlib import Path
from send2trash import send2trash

def analyze_file(file_path):
    """
    Analyze a single file and display its details.
    :param file_path: Full path to the file to analyze.
    """
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    file_size = os.path.getsize(file_path)  # Size in bytes
    file_extension = os.path.splitext(file_path)[1]
    last_access_time = time.ctime(os.path.getatime(file_path))  # Human-readable format

    print(f"File Analysis:")
    print(f"Path: {file_path}")
    print(f"Size: {file_size} bytes")
    print(f"Extension: {file_extension}")
    print(f"Last Accessed: {last_access_time}")

def move_file_to_recycle_bin(file_path):
    """
    Move a specific file to the recycle bin.
    :param file_path: Full path to the file to move.
    """
    try:
        send2trash(file_path)
        print(f"Success: The file '{file_path}' has been moved to the recycle bin.")
    except Exception as e:
        print(f"Error: Failed to move the file to the recycle bin. Reason: {e}")

def move_old_files_to_temp(folder_path, days_threshold):
    """
    Detect files in a folder that have not been accessed for a given number of days
    and move them to a temporary folder.
    :param folder_path: Path to the folder to analyze.
    :param days_threshold: Number of days since last access to qualify as "old."
    """
    temp_folder = Path(os.getenv('TEMP')) / "Old_Files"
    temp_folder.mkdir(exist_ok=True)

    current_time = time.time()
    age_threshold = days_threshold * 86400  # Convert days to seconds
    moved_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                last_access_time = os.path.getatime(file_path)
                file_age = current_time - last_access_time

                if file_age > age_threshold:
                    target_path = temp_folder / os.path.relpath(file_path, folder_path)
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(file_path, target_path)
                    moved_files.append(file_path)
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    if moved_files:
        print(f"Moved {len(moved_files)} file(s) to temporary folder: {temp_folder}")
        for f in moved_files:
            print(f" - {f}")
    else:
        print("No files met the criteria for being moved.")

def main():
    """
    Main menu that runs the file manager functionality.
    """
    while True:
        print("\nChoose an option:")
        print("1. Analyze a specific file")
        print("2. Move a specific file to the recycle bin")
        print("3. Detect and move old files to a temporary folder")
        print("4. Exit")
        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            file_path = input("Enter the full path of the file to analyze: ").strip()
            analyze_file(file_path)

        elif choice == "2":
            file_path = input("Enter the full path of the file to move to recycle bin: ").strip()
            if os.path.exists(file_path):
                analyze_file(file_path)  # Show details before moving
                confirm = input(f"Are you sure you want to move '{file_path}' to the recycle bin? (yes/no): ").strip().lower()
                if confirm == "yes":
                    move_file_to_recycle_bin(file_path)
            else:
                print("The specified file does not exist.")

        elif choice == "3":
            folder_path = input("Enter the folder path to scan for old files: ").strip()
            if os.path.exists(folder_path):
                days_threshold = int(input("Enter the number of days of inactivity to qualify as 'old': ").strip())
                move_old_files_to_temp(folder_path, days_threshold)
            else:
                print("The specified folder does not exist.")

        elif choice == "4":
            print("Exiting the script. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the script
if __name__ == "__main__":
    main()
