import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt


# Streamlit UI
st.set_page_config(page_title="Bedrock Chat Application", page_icon="🤖")

st.title("Bedrock Chat Application")
st.markdown(
    "Chat with an AI assistant powered by AWS Bedrock and a Knowledge Base of heavy machinery documents."
)

# Sidebar configuration
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox(
    "Select LLM Model",
    [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
    ]
)
kb_id = st.sidebar.text_input("Knowledge Base ID", "your-knowledge-base-id")
temperature = st.sidebar.select_slider(
    "Temperature", [i / 10 for i in range(0, 11)], value=1.0
)
top_p = st.sidebar.select_slider(
    "Top_P", [i / 10 for i in range(0, 11)], value=1.0
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Validate prompt category
    try:
        if valid_prompt(prompt, model_id):
            # Query Knowledge Base
            try:
                kb_results = query_knowledge_base(prompt, kb_id)
            except Exception as e:
                st.warning(f"Could not query KB: {e}")
                kb_results = []

            # Prepare context from KB results
            if kb_results:
                context = ""
                for result in kb_results:
                    text = result["content"].get("text", "")
                    metadata = result.get("metadata", {})
                    source = metadata.get("documentName", "Unknown Source")
                    context += f"{text} (Source: {source})\n"
            else:
                context = "No relevant documents found.\n"

            # Generate response with KB context
            full_prompt = f"Context: {context}\nUser: {prompt}\nAI:"
            with st.spinner("Generating response..."):
                response = generate_response(full_prompt, model_id, temperature, top_p, kb_results)
        else:
            response = "I'm unable to answer this. Please try a question related to heavy machinery."

    except Exception as e:
        response = f"An error occurred: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
<<<<<<< HEAD
    st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st
import boto3
from botocore.exceptions import ClientError
import json
from bedrock_utils import query_knowledge_base, generate_response, valid_prompt


# Streamlit UI
st.set_page_config(page_title="Bedrock Chat Application", page_icon="🤖")

st.title("Bedrock Chat Application")
st.markdown(
    "Chat with an AI assistant powered by AWS Bedrock and a Knowledge Base of heavy machinery documents."
)

# Sidebar configuration
st.sidebar.header("Configuration")
model_id = st.sidebar.selectbox(
    "Select LLM Model",
    [
        "anthropic.claude-3-haiku-20240307-v1:0",
        "anthropic.claude-3-5-sonnet-20240620-v1:0",
    ]
)
kb_id = st.sidebar.text_input("Knowledge Base ID", "your-knowledge-base-id")
temperature = st.sidebar.select_slider(
    "Temperature", [i / 10 for i in range(0, 11)], value=1.0
)
top_p = st.sidebar.select_slider(
    "Top_P", [i / 10 for i in range(0, 11)], value=1.0
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Validate prompt category
    try:
        if valid_prompt(prompt, model_id):
            # Query Knowledge Base
            try:
                kb_results = query_knowledge_base(prompt, kb_id)
            except Exception as e:
                st.warning(f"Could not query KB: {e}")
                kb_results = []

            # Prepare context from KB results
            if kb_results:
                context = ""
                for result in kb_results:
                    text = result["content"].get("text", "")
                    metadata = result.get("metadata", {})
                    source = metadata.get("documentName", "Unknown Source")
                    context += f"{text} (Source: {source})\n"
            else:
                context = "No relevant documents found.\n"

            # Generate response with KB context
            full_prompt = f"Context: {context}\nUser: {prompt}\nAI:"
            with st.spinner("Generating response..."):
                response = generate_response(full_prompt, model_id, temperature, top_p, kb_results)
        else:
            response = "I'm unable to answer this. Please try a question related to heavy machinery."

    except Exception as e:
        response = f"An error occurred: {e}"

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
=======
>>>>>>> c202b51 (Initial commit - Heavy Machinery RAG System)

    st.session_state.messages.append({"role": "assistant", "content": response})