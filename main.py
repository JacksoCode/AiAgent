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

    function_name = function_call_part.name
    function_args = function_call_part.args
    actual_function = function_mapping[function_name]
    function_result = actual_function("calculator", **function_args)


    if function_name in function_mapping:
        if verbose:
            print(f"- Calling function: {function_name}({function_args})")
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
            print(f"- Calling function: {function_name}")
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"result": f"{function_result}"},
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
    verbose = "--verbose" in sys.argv

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

    counter = 0
    max_count = 20
    while counter < max_count:
        counter += 1
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools= [available_functions], 
                    system_instruction=system_prompt),
            )
            prompt_token = response.usage_metadata.candidates_token_count
            response_token = response.usage_metadata.candidates_token_count

            if (response.candidates and 
                response.candidates[0].content.parts and 
                any(part.function_call for part in response.candidates[0].content.parts)):

                function_call = response.function_calls[0]
                function_call_result = call_function(function_call, verbose)
                response_data = function_call_result.parts[0].function_response.response


                candidates = response.candidates
                for candidate in candidates:
                    messages.append(candidate.content)

                function_responding = types.Content(
                    role='tool',
                    parts=[
                        types.Part(
                            function_response=types.FunctionResponse(
                            name=function_call.name,
                            response={"result": response_data['result']}
                            )
                        )
                    ]
                )
                messages.append(function_responding)
                continue

            else:
                if response.text:
                    if verbose:
                        print("===============================")
                        print(f"User prompt: {user_prompt}")
                        print("===============================")
                        print("Final response:")
                        print("===============================")
                        print(f"{response.text}")
                        print("===============================")
                        print(f"- Prompt tokens: {prompt_token}")
                        print(f"- Response tokens: {response_token}")
                        break
                    else:
                        print("Final response:")
                        print("===============================")
                        print(f"{response.text}")
                        print("===============================")
                        break

        except Exception as e:
            print(f"Fatal Error: {e}")
            break

if __name__ == "__main__":
    main()
