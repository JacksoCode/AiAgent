import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    relative_path = os.path.join(working_directory, directory)
    absolute_path = os.path.abspath(relative_path)
    wrk_directory = os.path.abspath(working_directory)

    if not absolute_path.startswith(wrk_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if os.path.isdir(absolute_path) == False:
        return f'Error: "{directory}" is not a directory'

    try:
        path_list = os.listdir(absolute_path)
        final_form = ""
        for p in path_list:
            relative_sub_path = os.path.join(absolute_path, p)
            sub_path = os.path.abspath(relative_sub_path)
            final_form += f"- {p}: file_size={os.path.getsize(sub_path)}, is_dir={os.path.isdir(sub_path)}\n"

        return final_form

    except Exception as e:
        return f"Error listing files: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
