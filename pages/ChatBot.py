import streamlit as st
from config import config
from dotenv import load_dotenv
from llm import chat, stream_parser

load_dotenv()

API_KEY = config.OPENAI_API_KEY

st.set_page_config(
    page_title="CatLib (OpenAi+Streamlit)",
    initial_sidebar_state="expanded"  # Corrected to "expanded"
)

st.title("CatLib")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("# Chat Option")
    
    model = st.selectbox("OpenAI Model", ["gpt-3.5-turbo", "gpt-4"])
    temperature = st.number_input("Temperature", value=0.7, min_value=0.1, max_value=1.0, step=0.1)
    max_token_length = st.number_input("Max Token Length", value=200, min_value=50, max_value=250)  # Corrected "max_token_lenght"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if user_prompt := st.chat_input("What questions do you have?"):
    with st.chat_message("user"):
        st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        
        with st.spinner("Generating response ..."):
            llm_response = chat(user_prompt, model=model, max_token=max_token_length, temp=temperature)
            stream_output = stream_parser(llm_response)
            
            st.session_state.messages.append({"role": "assistant", "content": stream_output})
            
            with st.chat_message("assistant"):
                st.markdown(stream_output)
