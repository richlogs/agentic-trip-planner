import streamlit as st
from openai import OpenAI
from yaml import safe_load

from agentic_trip_planner.conversation.utils import load_prompt, make_request, format_user_question, MODEL, PROMPT_PATH, PROMPT_NAME
# MODEL = "gpt-4.1-nano"
# PROMPT_PATH = 'agentic_trip_planner/conversation/config/prompt.yaml'
# PROMPT_NAME = "trip_planner"


# def load_prompt(path: str, prompt_name: str):
#     """Load the configuration file."""
#     with open(path, 'r') as file:
#         config = safe_load(file)
    
#     prompt = config.get(prompt_name)

#     if prompt is None:
#         raise ValueError(f"Prompt '{prompt_name}' not found in the configuration file.")
#     return prompt


# def make_request(client: OpenAI, prompt: list[dict], previous_response: str = None):
#     """Make a request to the OpenAI API."""
#     response = client.responses.create(
#         model=MODEL,
#         input=prompt,
#         previous_response_id=previous_response,
#     )
#     return response


# def format_user_question(question: str):
#     """Format the user question for the prompt."""
#     return {"role": "user", "content": question}

st.title("Trip Planning Assistant")

client = OpenAI()
developer_prompt = load_prompt(PROMPT_PATH, PROMPT_NAME)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query" not in st.session_state:
    st.session_state.query = [developer_prompt]

if "previous_response_id" not in st.session_state:
    st.session_state.previous_response_id = None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("How can I help?"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.query.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        response = client.responses.create(
            model=st.session_state["openai_model"],
            input=st.session_state.query,
            stream=False,
            previous_response_id=st.session_state.previous_response_id,
        )
        st.markdown(response.output_text)
        st.session_state.query = []

    st.session_state.messages.append({"role": "assistant", "content": response.output_text})
        
    # Save the response ID for context
    st.session_state.previous_response_id = response.id  # or stream.response.id depending on client

    # Clear query 