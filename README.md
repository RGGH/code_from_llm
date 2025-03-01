# code_from_llm

## Overview

`code_from_llm` is a Python project that interacts with OpenAI's GPT API to generate and execute Python scripts dynamically. It sends a prompt to OpenAI, retrieves a Python script, saves it to a file, and executes it automatically.

## Features
- Fetches a Python script from OpenAI's GPT model based on a predefined prompt.
- Writes the generated script to `script.py`.
- Determines the correct Python interpreter (`python` or `python3`).
- Executes the generated script and prints the output.

## Requirements

- Python 3.8+
- An OpenAI API key
- `requests` library

## Installation

Clone the repository:

```sh
git clone https://github.com/RGGH/code_from_llm.git
cd code_from_llm
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Usage

Set your OpenAI API key as an environment variable:

```sh
export OPENAI_API_KEY="your_api_key_here"
```

Run the script:

```sh
python main.py
```

## Output

- The generated script is saved as `script.py`.
- The script is executed, and its output is displayed in the terminal.

## License

This project is licensed under the MIT License.


