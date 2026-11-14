import streamlit as st
import os
from dotenv import load_dotenv
from pypdf import PdfReader 
import docx2txt
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = api_key



def load_cv(uploaded_file):
    text = ""
    if uploaded_file.name.endswith('.pdf'):
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    elif uploaded_file.name.endswith('.docx'):
        text = docx2txt.process(uploaded_file)
    return text

def clean_text(text):
    text = text.replace('\n', ' ')
    return " ".join(text.split())

def chunk_document(text, chunk_size=500, overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=overlap
    )
    return text_splitter.split_text(text)

def build_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def create_vector_store(chunks, embeddings):
    documents = [Document(page_content=t) for t in chunks]
    return Chroma.from_documents(documents, embeddings)

def retrieve_relevant_chunks(question, store, k=3):
    return store.similarity_search(question, k=k)

def build_prompt(question, context):
    prompt = f"""
    Tu es un assistant spécialisé dans l'analyse de CV. 
    Utilise UNIQUEMENT le contexte ci-dessous pour répondre à la question.
    
    CONTEXTE:
    {context}
    
    QUESTION:
    {question}
    
    CONSIGNE STRICTE: Si la réponse n'est pas dans le contexte, réponds exactement : 
    "Désolé, je ne peux répondre qu'aux questions concernant le contenu du CV chargé."
    """
    return prompt

def generate_answer(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(prompt)
    return response.content

def answer_cv_only(question, store):
    relevant_docs = retrieve_relevant_chunks(question, store)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    prompt = build_prompt(question, context)
    return generate_answer(prompt)

def reload_vector_store(uploaded_file):
    raw_text = load_cv(uploaded_file)
    
    if not raw_text or len(raw_text.strip()) == 0:
        st.error("Le fichier a été lu mais aucun texte n'a été extrait. Est-ce un PDF scané (image) ?")
    else:
        st.write(f" {len(raw_text)} caractères extraits du document.")
        with st.expander("Voir un aperçu du texte extrait"):
            st.text(raw_text[:500])

    clean_txt = clean_text(raw_text)
    chunks = chunk_document(clean_txt)
    embeddings = build_embeddings()
    st.session_state.messages = []
    return create_vector_store(chunks, embeddings)