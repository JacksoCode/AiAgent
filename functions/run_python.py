import os
import subprocess
from google import genai
from google.genai import types


def run_python_files(working_directory, file_path, args=[]):
    absolute_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_path = os.path.abspath(working_directory)

    if not absolute_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if os.path.isfile(absolute_path) == False:
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:

        commands = ["python", file_path]
        full_commands = commands + args

        final_form = subprocess.run(full_commands, timeout=30, capture_output=True, cwd=working_directory, text=True)

        if final_form.stdout == "" and final_form.stderr == "":
            return "No output produced"

        if final_form.returncode != 0:
            return f"STDOUT: {final_form.stdout}\nSTDERR: {final_form.stderr}\nProcess exited with code {final_form.returncode}"

        else:
            return f"STDOUT: {final_form.stdout}\nSTDERR: {final_form.stderr}" 

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_files = types.FunctionDeclaration(
    name="run_python_files",
    description="Execute Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The requested Python file to execute, realtive to the working directory",
            ),            
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass through the requested Python file. If none are present then execute the file without any additional arguments",
            ),
        },
    ),
)
