from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_pinecone import PineconeVectorStore
from utils import *
import streamlit as st


template = """
Answer the question based on the context.
Context: {context}
Question: {question}
"""

load_dotenv()

def main():
    process_individual_pdfs()
    prompt = ChatPromptTemplate.from_template(template)
    model = ChatOpenAI(api_key=openai_api_key, model_name="gpt-3.5-turbo").with_structured_output(CitedAnswer)
    vector_store = PineconeVectorStore(index=index, embedding=embeddings, text_key="text")
    retriever = vector_store.as_retriever()
    chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model )
    st.title("PDF Chatbot with Citations")
    query = st.text_input("Ask a question about the documents:")
    if st.button("Submit"):
        if query:
            with st.spinner("Processing..."):
                response = chain.invoke(query)
                st.write("Answer:", response.answer)
                st.write("Citations:", ', '.join(response.citations))
        else:
            st.error("Please enter a question.")    
            
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
  