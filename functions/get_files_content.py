import os
from google import genai
from google.genai import types
from functions.config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    absolute_file_path = os.path.abspath(os.path.join(
        working_directory, file_path
        )
    )
    wrk_directory_path = os.path.abspath(working_directory)

    if not absolute_file_path.startswith(wrk_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        final_form = ""
        with open(absolute_file_path, "r") as f:
            file_content_string = f.read(CHARACTER_LIMIT)
            final_form += file_content_string

        if len(final_form) >= CHARACTER_LIMIT:
            return f'{final_form} ...File "{file_path}" truncated at 10000 characters'
        else:
            return final_form

    except Exception as e:
        return f"Error reading files: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The requested file to read.",
            ),
        },
    ),
)
