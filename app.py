"""A Streamlit Web Application for Question Answering From PDF Documents Build with LangChain and OpenAI GPT-3."""

import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback

load_dotenv("config.env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)



def main():
    st.set_page_config(page_title="Ask your PDF", page_icon="📄", layout="centered")
    st.header("🦜️🔗Question Answering From PDF Documents")
    st.subheader("Powered by LangChain and OpenAI GPT-3")
    
    # Take PDF file as user input
    pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    # Check pdf_file is not None
    if pdf_file is not None:
        pdf_reader = PdfReader(pdf_file)
        # Extract the text from PDF
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Show the text 
        # st.write(text)
            
        # split into chunks
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        # create embeddings
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)
        
        # show user input
        user_question = st.text_input("Ask a question about your PDF:")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                print(cb)
                
            st.write(response)

    


if __name__ == "__main__":
    main()