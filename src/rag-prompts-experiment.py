import streamlit as st
import json
from openai import OpenAI
import copy
from dotenv import load_dotenv

# Setting up OpenAI client
load_dotenv()
client = OpenAI()

# Initialize session state
if 'placeholders' not in st.session_state:
    st.session_state.placeholders = ['']

if 'prompts' not in st.session_state:
    st.session_state.prompts = ['']

if 'results' not in st.session_state:
    st.session_state.results = ''

# Function to add a new placeholder
def add_placeholder():
    st.session_state.placeholders.append('')

def remove_placeholder(index):
    st.session_state.placeholders.pop(index)

def add_prompt():
    st.session_state.prompts.append('')

def remove_prompt(index):
    st.session_state.prompts.pop(index)

def get_config(): 
    return json.loads(st.session_state.config_data)

def get_placeholders(): 
    return [st.session_state[f"placeholder_{i}"] for i in range(len(st.session_state.placeholders))]

def get_prompts():
    return [st.session_state[f"prompt_{i}"] for i in range(len(st.session_state.prompts))]

def get_default_config_as_string():
    return """{
  "model": "gpt-3.5-turbo",
  "input": [],
  "text": {
    "format": {
      "type": "text"
    }
  },
  "reasoning": { },
  "tools": [],
  "temperature": 1,
  "max_output_tokens": 2048,
  "top_p": 1,
  "store": true
}"""

def submit_prompts(config_data):
    results = []

    original_prompts = get_prompts()
    placeholders = get_placeholders()

    # Replace special characters in placeholders
    for i, placeholder in enumerate(placeholders):
        if placeholder:
            placeholders[i] = placeholder \
                .replace("\\n", "\n") \
                .replace("\\t", "\t") \
                .replace("\\r", "\r")

    # Replace special characters in prompts
    for i, prompt in enumerate(original_prompts):
        original_prompts[i] = prompt \
            .replace("\\n", "\n") \
            .replace("\\t", "\t") \
            .replace("\\r", "\r")

    # Replace placeholders in prompts
    updated_prompts = copy.deepcopy(original_prompts)
    for i, placeholder in enumerate(placeholders):
        if placeholder:  # Skip empty placeholders
            for j in range(len(updated_prompts)):
                updated_prompts[j] = updated_prompts[j].replace(f"{{{i}}}", placeholder)

            results.append(f"Placeholder {{{i}}}: {placeholder}")
    
    arguments = copy.deepcopy(config_data)
    if "input" not in arguments:
        arguments["input"] = []

    for i, prompt in enumerate(updated_prompts):
        # Append prompt to conversation
        user_input = {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": prompt
                }
            ]
        }
        arguments["input"].append(dict(user_input))

        response = client.responses.create(**arguments)
        result = response.output_text
        
        print(arguments)
        print(result)

        results.append(f"Prompt {i}: {original_prompts[i]}\nResult {i}: {result}")

        # Append result to conversation
        assistant_input = {
            "role": "assistant",
            "content": [
                {
                    "type": "output_text",
                    "text": result
                }
            ]
        }
        arguments["input"].append(dict(assistant_input))

    st.session_state.results = "\n\n".join(results)

# Setting up UI 
st.title("RAG Prompts Experiment")

# Text area for configuration
st.subheader("Configuration")
config = st.text_area(
    "Configuration",
    value=get_default_config_as_string(),
    key="config",
    height=150
)

# Validate JSON input
try:
    config_data = json.loads(config)
except json.JSONDecodeError:
    st.error("Invalid JSON")

# Display placeholders section
st.subheader("Placeholders")
for i, placeholder in enumerate(st.session_state.placeholders):
    cols = st.columns([4, 1], vertical_alignment="bottom")
    with cols[0]:
        st.text_input(f"Placeholder {i}", key=f"placeholder_{i}")
    with cols[1]:
        st.button("Delete", key=f"delete_{i}", on_click=lambda: remove_placeholder(i))

st.button("Add Placeholder", on_click=add_placeholder)

# Display prompts section
st.subheader("Prompts")
for i, prompt in enumerate(st.session_state.prompts):
    cols = st.columns([4, 1], vertical_alignment="bottom")
    with cols[0]:
        st.text_input(f"Prompt {i}", key=f"prompt_{i}")
    with cols[1]:
        st.button("Delete", key=f"delete_prompt_{i}", on_click=lambda: remove_prompt(i))

st.button("Add Prompt", on_click=add_prompt)

# Display logs section
st.subheader("Results")
if config_data and any(get_prompts()): 
    cols = st.columns([1, 2, 4])
    with cols[0]:
        st.button("Submit", on_click=lambda: submit_prompts(config_data))
    with cols[1]:
        auto_run = st.checkbox("Auto-submit", value=True)
        if auto_run:
            submit_prompts(config_data)

    st.text_area("Results", value=st.session_state.results, height=300)

else: 
    st.info("Please fill in the configuration and prompts to run the experiment")