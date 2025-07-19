import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")
#Update this later(probably)

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]

    if user_prompt == None:
        print("Error: Prompt not provided")
        print("Accepted Format: main.py 'ENTER PROMPT HERE'")
        print("Example: main.py 'What's 9 + 10?'")
        sys.exit(1)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages)

    verbose = "--verbose" in sys.argv

    prompt_token = response.usage_metadata.candidates_token_count
    response_token = response.usage_metadata.candidates_token_count

    if verbose == True:
        print(response.text)
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token}")
        print(f"Response tokens: {response_token}")
    else:
        print(response.text)


if __name__ == "__main__":
    main()
