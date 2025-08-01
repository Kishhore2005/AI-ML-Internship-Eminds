import streamlit as st
import os
import sys

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.pdf_service import PDFService
from src.services.vector_service import VectorService
from src.services.llm_service import LLMService

# Page configuration
st.set_page_config(page_title="RAG PDF Chatbot", layout="wide")
st.title("📄 RAG-based PDF Chatbot using Groq")

# Initialize session state
if 'vector_service' not in st.session_state:
    st.session_state.vector_service = None
if 'llm_service' not in st.session_state:
    st.session_state.llm_service = None
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📤 Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Process PDF", type="primary"):
            with st.spinner("Processing PDF..."):
                try:
                    # Save uploaded file
                    temp_path = PDFService.save_uploaded_file(uploaded_file)
                    
                    # Extract text
                    raw_text = PDFService.extract_text_from_pdf(temp_path)
                    text_chunks = PDFService.get_text_chunks(raw_text)
                    
                    # Create vector store
                    st.session_state.vector_service = VectorService()
                    vector_store = st.session_state.vector_service.create_vector_store(text_chunks)
                    
                    # Initialize LLM service with default model
                    st.session_state.llm_service = LLMService(model_name="llama3-8b-8192")
                    
                    # Save vector store
                    save_path = st.session_state.vector_service.save_vector_store()
                    
                    st.session_state.pdf_processed = True
                    st.success(f"✅ PDF processed successfully! Created {len(text_chunks)} text chunks.")
                    
                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")

with col2:
    st.header("💬 Chat Interface")
    
    if st.session_state.pdf_processed and st.session_state.vector_service:
        query = st.text_input("Ask something about the PDF", placeholder="What is this document about?")
        
        if query and st.button("Ask", type="primary"):
            with st.spinner("Generating answer..."):
                try:
                    # Perform similarity search
                    docs = st.session_state.vector_service.similarity_search(query, k=4)
                    
                    # Get LLM response
                    response = st.session_state.llm_service.get_response(docs, query)
                    
                    # Display response
                    st.subheader("📢 Answer")
                    st.write(response)
                    
                    # Display model info
                    model_info = st.session_state.llm_service.get_model_info()
                    st.caption(f"🤖 Model: {model_info['model_name']} | Provider: {model_info['provider']}")
                    
                except Exception as e:
                    st.error(f"❌ Error generating answer: {str(e)}")
    else:
        st.info("📤 Please upload and process a PDF first to start chatting.")

# Simple status display
if st.session_state.pdf_processed:
    st.sidebar.success("✅ PDF Processed")
    if st.session_state.llm_service:
        model_info = st.session_state.llm_service.get_model_info()
        st.sidebar.info(f"🤖 Model: {model_info['model_name']}")
else:
    st.sidebar.info("📄 No PDF processed yet")
