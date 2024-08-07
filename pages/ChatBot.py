import streamlit as st
from dotenv import load_dotenv
from helpersloc import chat, stream_parser


load_dotenv()

st.set_page_config(
    page_title="Streamlit OpenAI Chatbot",
    initial_sidebar_state="expanded"
)

st.title("Streamlit OpenAI Chatbot")


with st.sidebar:   
    st.markdown("# Chat Options")
    
    model = st.selectbox('What model would you like to use?',('gpt-3.5-turbo', 'gpt-4'))
   
    temperature = st.number_input('Temperature', value=0.7, min_value=0.1, max_value=1.0, step=0.1,
                                            help="The temperature setting to be used when generating output from the model.")
    
    max_token_length = st.number_input('Max Token Length', value=150, min_value=100, max_value=200, step=25, 
                                            help="Maximum number of tokens to be used when generating output.")
    

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("What questions do you have about the document?"):
    # Display user prompt in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner('Generating response...'):
        llm_response = chat(user_prompt, model=model, max_tokens=max_token_length,
                            temp=temperature)

        stream_output = st.write_stream(stream_parser(llm_response))

        st.session_state.messages.append({"role": "assistant", "content": stream_output})

    last_response =  st.session_state.messages[len(st.session_state.messages)-1]['content']

    if str(last_response) != str(stream_output):
        with st.chat_message("assistant"):
            st.markdown(stream_output)
        
