# Tools for LLM experimentation
A personal set of tools for experimenting with Large Language Models (LLMs), mostly OpenAI.

## Installation Instructions
To install the required Python packages, follow these steps:
1. Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).
2. Open a terminal or command prompt.
3. Navigate to the project directory
4. Install the required packages using `pip`:
    ```sh
    pip install -r src/requirements.txt
    ```

This will install all the necessary dependencies listed in the `src/requirements.txt` file.

## Usage Instructions
To use the tools, follow these steps:
1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the desired script using Python:
    ```sh
    streamlit run src/<script_name>.py
    ```

### Scripts
- `rag-prompts-experiment.py`: An RAG prompts experiment using OpenAI's API with support for placeholders. 