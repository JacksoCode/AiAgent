import warnings
warnings.filterwarnings("ignore", 
    message="urllib3 v2 only supports OpenSSL 1.1.1+")
#Update this later(probably)

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_files_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_files, run_python_files
from functions.write_files import schema_write_files, write_files


def call_function(function_call_part, verbose=False):
    function_mapping = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_files": run_python_files,
        "write_files": write_files
    }

    for part in function_call_part:
        function_name = part.name
        function_args = part.args
        actual_function = function_mapping[function_name]
        function_result = actual_function("calculator", **function_args)


        if function_name in function_mapping:
            if verbose:
                print(f"Calling function: {function_name}({function_args})")
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"result": function_result},
                        )
                    ],
                )
            else:
                print(f"Calling function: {function_name}")
                return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_name,
                            response={"result": function_result},
                        )
                    ],
                )
        else:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    user_prompt = sys.argv[1]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info, 
            schema_get_file_content,
            schema_run_python_files,
            schema_write_files,
        ]
    )

    messages = [
        types.Content(role="user", 
        parts=[types.Part(text=user_prompt)]),
    ]

    if not user_prompt:
        print("Error: Prompt not provided")
        print("Accepted Format: main.py 'ENTER PROMPT HERE'")
        print("Example: main.py 'What's 9 + 10?'")
        sys.exit(1)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools= [available_functions], 
            system_instruction=system_prompt),
    )

    verbose = "--verbose" in sys.argv
    prompt_token = response.usage_metadata.candidates_token_count
    response_token = response.usage_metadata.candidates_token_count
    function_call = response.function_calls
    function_call_result = call_function(function_call, verbose)

    if function_call:
        try:
            response_data = function_call_result.parts[0].function_response.response

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"-> {response_data}")
                print(f"Prompt tokens: {prompt_token}")
                print(f"Response tokens: {response_token}")
            else:
                print(f"-> {response_data}")

        except (AttributeError, IndexError):
            print("Fatal Error: Function result missing critical attribute '.parts[0].function_response.response'")
    else:
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"{response.txt}")
            print(f"Prompt tokens: {prompt_token}")
            print(f"Response tokens: {response_token}")
        else:
            print(response.txt)


if __name__ == "__main__":
    main()
