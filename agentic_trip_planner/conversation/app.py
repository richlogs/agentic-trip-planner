import streamlit as st
from openai import OpenAI

from agentic_trip_planner.conversation.utils import (
    MODEL,
    PROMPT_NAME,
    PROMPT_PATH,
    format_user_question,
    load_prompt,
    make_request,
)

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
    formatted_prompt = format_user_question(prompt)
    st.session_state.messages.append(formatted_prompt)
    st.session_state.query.append(formatted_prompt)
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        response = make_request(
            client, 
            st.session_state.query, 
            previous_response=st.session_state.previous_response_id
        )
        st.markdown(response.output_text)

    st.session_state.messages.append(
        {"role": "assistant", "content": response.output_text}
    )
        
    # Save the response ID for context
    st.session_state.previous_response_id = response.id 

    # Clear query 
    st.session_state.query = []