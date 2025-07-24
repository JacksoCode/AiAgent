import warnings
warnings.filterwarnings("ignore", 
    message="urllib3 v2 only supports OpenSSL 1.1.1+")
#Update this later(probably)

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.run_python import schema_run_python_files
from functions.write_files import schema_write_files

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

    if verbose:
        print(response.text)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_token}")
    if function_call:
        for part in function_call:
            print(f"Calling function: {part.name}({part.args})")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
