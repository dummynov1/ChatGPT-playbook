import os
import shutil
import multiprocessing

def copy_file(file_path, dest_folder):
    try:
        shutil.copy(file_path, dest_folder)
    except Exception as e:
        print(f"Error copying file {file_path}: {str(e)}")

def process_file(file_path, source_folder, dest_folder):
    filename = os.path.basename(file_path)
    year = filename[-8:-6]  # extract year from filename
    year_folder = os.path.join(dest_folder, year)
    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
    copy_file(file_path, year_folder)

def main(source_folder, dest_folder, num_processes):
    files = [os.path.join(source_folder, f) for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.starmap(process_file, [(file, source_folder, dest_folder) for file in files])

if __name__ == "__main__":
    source_folder = '/path/to/source/folder'
    dest_folder = '/path/to/destination/folder'
    num_processes = multiprocessing.cpu_count()  # use all available CPU cores
    main(source_folder, dest_folder, num_processes)
