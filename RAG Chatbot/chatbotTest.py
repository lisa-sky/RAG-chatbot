import streamlit as st
from openai import AzureOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import AzureOpenAIEmbeddings
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
import tempfile

# this prevents the default_tenant error
import chromadb.api
chromadb.api.client.SharedSystemClient.clear_system_cache()

from os import environ


# LLM
llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",
    temperature=0.2,
    api_version="2023-06-01-preview",
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Formatting
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Title of the chatbot
st.title("📝 File Q&A Chatbot")

# Uploading files, supporting txt and pdf, can also handle multiple files
uploaded_files = st.file_uploader("Upload your text or PDF files", type=("txt", "pdf"), accept_multiple_files=True)

# Chunking setup
chunk_size = 150
chunk_overlap = 0
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

# Ask user
question = st.chat_input(
    "Ask something about your uploaded files",
    disabled=not uploaded_files,
)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Ask something about your uploaded files!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


# IMPORTANT: if user uploads a file, and questions
if question and uploaded_files:
    documents = []
    
    # For loop to iterate
    for uploaded_file in uploaded_files:
        # Handle PDF files
        if uploaded_file.type == "application/pdf":
            # Used temp file to store the pdf
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                temp_file.write(uploaded_file.read())
                temp_file.flush() 
                
                # Load pdf
                loader = PyPDFLoader(temp_file.name)  
                pdf_docs = loader.load()
                
                # Add source metadata to the documents
                for doc in pdf_docs:
                    doc.metadata["source"] = uploaded_file.name
                documents.extend(pdf_docs)
        

        # When the user uploads txt files
        else:
            file_content = uploaded_file.read().decode("utf-8")
            documents.append(Document(page_content=file_content, metadata={"source": uploaded_file.name}))

    # Chunking 
    chunks = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=AzureOpenAIEmbeddings(model="text-embedding-3-large"))

    # Prompt template
    template = """
    You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    
    Question: {question} 
    
    Context: {context} 
    
    Answer:
    """
    prompt = PromptTemplate.from_template(template)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})

    # RAG Chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Invoking RAG chain
    answer = rag_chain.invoke(question)
    
    # Append user's question to session messages
    st.session_state.messages.append({"role": "user", "content": question})
    st.chat_message("user").write(question)


    # Display assistant's answer
    with st.chat_message("assistant"):
        st.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})



# client
    client = AzureOpenAI(
    api_key=environ['AZURE_OPENAI_API_KEY'],
    api_version="2023-03-15-preview",
    azure_endpoint=environ['AZURE_OPENAI_ENDPOINT'],
    azure_deployment=environ['AZURE_OPENAI_MODEL_DEPLOYMENT'],
    )
