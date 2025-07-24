import os
from google import genai
from google.genai import types


def write_files(working_directory, file_path, content):

    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_path = os.path.abspath(working_directory)

    if not absolute_path.startswith(working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:

        file_directory = os.path.dirname(absolute_path)

        os.makedirs(file_directory, exist_ok=True)

        with open(absolute_path, "w") as f:
             f.write(content)
             return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error writing files: {e}"

schema_write_files = types.FunctionDeclaration(
    name="write_files",
    description="Write or create new files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The requested file to write or to overwrite, if file does not exist then write it",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write or overwrite to the new file.",
            ),
        },
    ),
)
