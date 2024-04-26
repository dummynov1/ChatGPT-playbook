import os
import shutil
import multiprocessing

def move_files_to_year_wise_folders(root_dir):
    # Create a dictionary to store the year-wise folders
    year_folders = {}

    # Iterate over all files in the root directory
    for filename in os.listdir(root_dir):
        # Get the 7th and 8th characters from the end of the filename
        year = filename[-8:-6]

        # Create the year-wise folder if it doesn't exist
        year_folder = os.path.join(root_dir, year)
        if year not in year_folders:
            year_folders[year] = year_folder
            if not os.path.exists(year_folder):
                os.makedirs(year_folder)

        # Move the file to the year-wise folder
        src_file = os.path.join(root_dir, filename)
        dst_file = os.path.join(year_folder, filename)
        shutil.move(src_file, dst_file)

def parallel_move_files_to_year_wise_folders(root_dir, num_processes):
    # Create a pool of worker processes
    with multiprocessing.Pool(processes=num_processes) as pool:
        # Split the files into chunks for parallel processing
        files = os.listdir(root_dir)
        chunks = [files[i::num_processes] for i in range(num_processes)]

        # Process each chunk in parallel
        pool.starmap(move_files_to_year_wise_folder_chunk, [(root_dir, chunk) for chunk in chunks])

def move_files_to_year_wise_folder_chunk(root_dir, file_chunk):
    for filename in file_chunk:
        # Get the 7th and 8th characters from the end of the filename
        year = filename[-8:-6]

        # Create the year-wise folder if it doesn't exist
        year_folder = os.path.join(root_dir, year)
        if not os.path.exists(year_folder):
            os.makedirs(year_folder)

        # Move the file to the year-wise folder
        src_file = os.path.join(root_dir, filename)
        dst_file = os.path.join(year_folder, filename)
        shutil.move(src_file, dst_file)

if __name__ == '__main__':
    root_dir = '/path/to/root/directory'
    num_processes = multiprocessing.cpu_count()  # Use all available CPU cores
    parallel_move_files_to_year_wise_folders(root_dir, num_processes)
