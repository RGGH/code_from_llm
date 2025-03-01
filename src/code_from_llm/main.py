import shutil
import os
import requests
import subprocess
from pathlib import Path

# Fetch the OpenAI API key from the environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment")

url = "https://api.openai.com/v1/chat/completions"
prompt = ("Generate a Python script that fetches the bitcoin price from Gemini API - just give the code, so it can be run, "
          "no smalltalk! - no comments like 'Here's a simple Python script that imports the `requests` library to send HTTP "
          "requests and fetch the latest Bitcoin price from the Gemini API:' - no backticks either ok, just code")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": prompt}],
    "max_tokens": 100
}

response = requests.post(url, headers=headers, json=data)
response_json = response.json()

script = response_json.get("choices", [{}])[0].get("message", {}).get("content", "print('No response from AI')")

# Write the Python script to a file
script_path = Path("script.py").resolve()
with open(script_path, "w") as file:
    file.write(script)

print("Python script generated:", script_path)

python_command = shutil.which("python") or shutil.which("python3")
if not python_command:
    raise RuntimeError("Python interpreter not found.")

# Run the Python script
process = subprocess.run([python_command, str(script_path)], capture_output=True, text=True)

if process.returncode != 0:
    print("Error running Python script:", process.stderr)
else:
    print("Python script output:", process.stdout)

