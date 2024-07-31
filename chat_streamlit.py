import streamlit as st
import ollama

# System prompt templates
prompt_templates = [
    "Behave as if you are a professional writer.",
    "Provide concise and accurate information.",
    "Act as a friendly assistant who helps with all questions.",
    "Explain complex topics in a simple and understandable way.",
    "Offer detailed explanations with examples.",
    "Explain as though you are tired of hearing from the user, always cynical and impatient"
]

st.title("💬 Streamlit Chatbot")

# Initialize messages in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["system_prompt"] = ""
    st.session_state["full_message"] = ""
    st.session_state["system_prompt_updated"] = False

# Sidebar for system prompt selection or input
with st.sidebar:
    st.header("System Prompt")
    
    # Show the current system prompt
    st.write(f"**Current System Prompt:** {st.session_state.get('system_prompt', 'Not set')}")
    
    selected_prompt = st.selectbox("Choose a system prompt:", ["Custom"] + prompt_templates)
    
    if selected_prompt == "Custom":
        st.session_state["system_prompt"] = st.text_area("Enter your custom system prompt:", st.session_state["system_prompt"])
    else:
        st.session_state["system_prompt"] = selected_prompt

    if st.button("Update System Prompt"):
        # Update the system prompt in messages
        if len(st.session_state["messages"]) == 0 or st.session_state["messages"][0]["role"] != "system":
            st.session_state["messages"] = [{"role": "system", "content": st.session_state["system_prompt"]}]
        else:
            st.session_state["messages"][0]["content"] = st.session_state["system_prompt"]
        
        st.session_state["system_prompt_updated"] = True
        st.session_state["full_message"] = ""

# Clear old assistant messages if system prompt is updated
if st.session_state.get("system_prompt_updated"):
    st.session_state["messages"] = [msg for msg in st.session_state["messages"] if msg["role"] == "system"]
    st.session_state["system_prompt_updated"] = False
        
### Write Message History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message(msg["role"], avatar="🧑‍💻").write(msg["content"])
    else:
        st.chat_message(msg["role"], avatar="🤖").write(msg["content"])

## Generator for Streaming Tokens
def generate_response():
    response = ollama.chat(model='llama2', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="🧑‍💻").write(prompt)
    st.session_state["full_message"] = ""
    st.chat_message("assistant", avatar="🤖").write_stream(generate_response)
    st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]})   