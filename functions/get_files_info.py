import os

def get_files_info(working_directory, directory="."):
    relative_path = os.path.join(working_directory, directory)
    print(f"This is the realative path: {relative_path}")

    print(f"And this is the absolute path: {os.path.abspath(directory)}")

    if os.path.abspath(directory) not in working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(directory) == False:
        return f'Error: "{directory}" is not a directory'

    r_path_list = os.listdir(relative_path)
    print(f"This is a path list: {r_path_list}")

    for r in r_path_list:
        return f"{r}: file_size={os.path.getsize(r)}, is_dir={os.path.isdir(r)}"
