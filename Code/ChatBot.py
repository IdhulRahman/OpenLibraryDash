import os
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize embeddings
def initialize_embeddings():
    return OpenAIEmbeddings(api_key=OPENAI_API_KEY)

# Convert CSV data to text format
def convert_csv_to_text(df):
    text = ""
    for _, row in df.iterrows():
        text += " ".join(map(str, row.values)) + "\n"
    return text

# Load the knowledge base from FAISS
def load_knowledge_base(text_data):
    embeddings = initialize_embeddings()
    documents = [{"page_content": text_data}]
    faiss_db = FAISS.from_documents(documents=documents, embedding=embeddings)
    return faiss_db

# Load the prompt template with character context
def load_prompt():
    prompt = """
    You are Catlib, a friendly librarian and a passionate Manchester United fan. You love books and football with equal enthusiasm.
    You need to answer the question based on the content in the CSV file.
    Given below is the context and question of the user.
    context = {context}
    question = {question}
    If the answer is not in the CSV, respond with "I don't know what the hell you are asking about."
    """
    return ChatPromptTemplate.from_template(prompt)

# Load the language model
def load_llm():
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=OPENAI_API_KEY)

# Main function to run the Streamlit app
def main():
    st.title("CSV Bot")
    st.write("Welcome to the CSV bot, operated by Catlib, your librarian and Manchester United fan!")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        text_data = convert_csv_to_text(df)
        knowledge_base = load_knowledge_base(text_data)
        llm = load_llm()
        prompt = load_prompt()

        query = st.text_input('Enter your question here:')

        if query:
            # Search for similar embeddings
            similar_embeddings = knowledge_base.similarity_search(query)
            
            if similar_embeddings:
                # Create a retriever from the found documents
                retriever = FAISS.from_documents(documents=similar_embeddings, embedding=initialize_embeddings()).as_retriever()

                # Generate the context string
                context = "\n\n".join(doc.page_content for doc in similar_embeddings)
                
                # Create the RAG chain
                rag_chain = (
                    {"context": context, "question": query}
                    | prompt
                    | llm
                    | StrOutputParser()
                )

                # Get the response and display it
                response = rag_chain.invoke({"context": context, "question": query})
                st.write("Response:", response)
            else:
                st.write("No similar content found.")

if __name__ == '__main__':
    main()
