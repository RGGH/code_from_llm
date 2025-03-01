import os
import shutil
import requests
import subprocess
import json
from pathlib import Path
from typing import Optional

def get_api_key() -> str:
    """Fetch the OpenAI API key from the environment with proper error handling."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return api_key

def generate_script_with_openai(api_key: str, prompt: str) -> Optional[str]:
    """Generate a Python script using OpenAI API with proper error handling."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500  # Increased token limit for more complete scripts
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        response_json = response.json()
        script = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not script:
            print("Warning: Empty response from OpenAI API")
            return None
            
        return script
    except requests.exceptions.RequestException as e:
        print(f"Error making request to OpenAI API: {e}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON response from OpenAI API")
        return None

def save_script(script: str, script_path: Path) -> bool:
    """Save the script to a file with error handling."""
    try:
        with open(script_path, "w") as file:
            file.write(script)
        return True
    except IOError as e:
        print(f"Error writing script to file: {e}")
        return False

def run_python_script(script_path: Path) -> None:
    """Run the Python script with proper error handling."""
    python_command = shutil.which("python") or shutil.which("python3")
    if not python_command:
        raise RuntimeError("Python interpreter not found.")
    
    try:
        process = subprocess.run(
            [python_command, str(script_path)],
            capture_output=True,
            text=True,
            timeout=30  # Add timeout to prevent hanging
        )
        
        if process.returncode != 0:
            print(f"Error running Python script (exit code {process.returncode}):")
            print(process.stderr)
        else:
            print("Python script executed successfully:")
            print(process.stdout)
    except subprocess.TimeoutExpired:
        print("Error: Script execution timed out after 30 seconds")
    except subprocess.SubprocessError as e:
        print(f"Error executing script: {e}")

def main():
    # Script prompt
    prompt = (
        "Generate a Python script that fetches the bitcoin price from Gemini API - "
        "just give the code, so it can be run, no smalltalk! - no comments like "
        "'Here's a simple Python script that imports the `requests` library to send HTTP "
        "requests and fetch the latest Bitcoin price from the Gemini API:' - "
        "never respond with the code in ``` backticks. Only ever return pure code, no text before or after!!!"
    )
    
    try:
        # Get API key
        api_key = get_api_key()
        
        # Generate script
        script = generate_script_with_openai(api_key, prompt)
        if not script:
            return
        
        # Save script to file
        script_path = Path("bitcoin_price_script.py").resolve()
        if not save_script(script, script_path):
            return
            
        print(f"Python script generated: {script_path}")
        
        # Run the script
        run_python_script(script_path)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
