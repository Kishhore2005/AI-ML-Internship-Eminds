import streamlit as st
import requests
import PyPDF2
import io
import time
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = "http://localhost:8000"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False

def check_api_health():
    """Check if the RAG API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def upload_pdf_text(text):
    """Upload extracted text to RAG system"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/upload-text",
            json=[text],
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Upload failed: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to RAG API. Make sure the server is running on http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"❌ Error uploading: {e}")
        return None

def get_relevant_context(question):
    """Get relevant context from RAG system"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/query",
            json={"question": question, "top_k": 3},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Query failed: {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Error getting context: {e}")
        return None

def generate_answer_with_groq(question, context, chat_history=None):
    """Generate answer using Groq's Llama3-8b model with chat-like responses"""
    try:
        # Reload environment variables to ensure we get the latest
        load_dotenv(override=True)
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            st.error("❌ GROQ_API_KEY not found. Please set it in your environment variables.")
            return None
        
        client = Groq(api_key=api_key)
        
        # Build conversation context
        messages = [
            {
                "role": "system",
                "content": """You are a friendly and helpful AI assistant that answers questions based on the provided context. 
                You should respond in a conversational, chat-like manner. Be helpful, engaging, and natural in your responses.
                If the context doesn't contain enough information to answer the question, politely say so and suggest what information might be needed.
                Keep your responses concise but informative."""
            }
        ]
        
        # Add chat history if available
        if chat_history:
            for msg in chat_history[-6:]:  # Keep last 6 messages for context
                messages.append({
                    "role": "user" if msg["role"] == "user" else "assistant",
                    "content": msg["content"]
                })
        
        # Add current question with context
        current_prompt = f"""Based on the following context, answer this question in a conversational way:

Context from the document:
{context}

Question: {question}

Please respond naturally as if we're having a friendly conversation about this topic."""
        
        messages.append({
            "role": "user",
            "content": current_prompt
        })
        
        # Generate response using Llama3-8b
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            st.error("❌ Invalid API key. Please check your GROQ_API_KEY in the .env file.")
            st.info("💡 Make sure your API key starts with 'gsk_' and is correct.")
            st.info("💡 Get a new key from: https://console.groq.com/")
        else:
            st.error(f"❌ Error generating answer with Groq: {e}")
        return None

def ask_question(question):
    """Ask a question using RAG + Groq with chat history"""
    try:
        # Step 1: Get relevant context from RAG
        rag_result = get_relevant_context(question)
        
        if not rag_result:
            return None
        
        # Step 2: Extract context from RAG response
        context = rag_result.get('answer', '')
        
        # Step 3: Generate better answer using Groq with chat history
        groq_answer = generate_answer_with_groq(question, context, st.session_state.chat_history)
        
        if groq_answer:
            return {
                'answer': groq_answer,
                'context': context,
                'sources': rag_result.get('sources', [])
            }
        else:
            return None
            
    except Exception as e:
        st.error(f"❌ Error asking question: {e}")
        return None

def test_groq_api():
    """Test Groq API connection"""
    try:
        load_dotenv(override=True)
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            return False, "No API key found"
        
        client = Groq(api_key=api_key)
        
        # Simple test request
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        
        return True, "API key works"
        
    except Exception as e:
        return False, str(e)

def save_pdf_to_data(uploaded_file):
    """Save uploaded PDF as temp.pdf in data folder"""
    try:
        # Create data folder if it doesn't exist
        data_folder = "data"
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        
        # Save as temp.pdf
        temp_path = os.path.join(data_folder, "temp.pdf")
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return True
    except Exception as e:
        st.error(f"Error saving PDF: {e}")
        return False

def read_temp_pdf():
    """Read temp.pdf from data folder"""
    try:
        file_path = os.path.join("data", "temp.pdf")
        if not os.path.exists(file_path):
            return None
            
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
    except Exception as e:
        st.error(f"Error reading temp.pdf: {e}")
        return None

def display_chat_history():
    """Display the chat history in a chat-like interface"""
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(message["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(message["content"])
                    
                    # Show context if available
                    if "context" in message and st.session_state.get("show_context", False):
                        with st.expander("🔍 View Context Used"):
                            st.write(message["context"])

def main():
    st.set_page_config(
        page_title="Chat RAG - PDF Q&A with Groq",
        page_icon="💬",
        layout="wide"
    )
    
    st.title("💬 Chat RAG - PDF Question & Answer with Groq")
    st.markdown("---")
    
    # Check API health silently
    if not check_api_health():
        st.error("❌ RAG API is not running! Please start the API server first with `python main.py`")
        st.info("💡 Make sure the API server is running on http://localhost:8000")
        return
    
    # Check Groq API key (hidden from frontend)
    load_dotenv(override=True)
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("❌ GROQ_API_KEY not found!")
        st.info("💡 Create a .env file with: GROQ_API_KEY=your_api_key_here")
        st.info("💡 Get your API key from: https://console.groq.com/")
        return
    
    # Two main sections
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.header("📤 Upload PDF")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file:",
            type=['pdf'],
            help="Select any PDF file from your computer."
        )
        
        if uploaded_file is not None:
            st.info(f"📄 Selected: {uploaded_file.name}")
            
            # Process the uploaded file
            if st.button("📤 Process PDF", type="primary"):
                with st.spinner("Processing PDF..."):
                    # First save the file
                    if save_pdf_to_data(uploaded_file):
                        st.success("✅ PDF saved as temp.pdf")
                        
                        # Extract text from PDF
                        text = read_temp_pdf()
                        
                        if text:
                            st.success(f"✅ Extracted {len(text)} characters from PDF")
                            
                            # Upload to RAG system
                            with st.spinner("Uploading to RAG system..."):
                                result = upload_pdf_text(text)
                                
                                if result:
                                    st.success(f"✅ Successfully uploaded PDF to RAG system!")
                                    st.info(f"📊 Documents processed: {result.get('documents_processed', 0)}")
                                    st.session_state.pdf_processed = True
                                    # Clear chat history when new PDF is processed
                                    st.session_state.chat_history = []
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to upload PDF")
                        else:
                            st.error("❌ Failed to extract text from PDF")
                    else:
                        st.error("❌ Failed to save PDF")
        
        # Show current temp.pdf status
        temp_pdf_path = os.path.join("data", "temp.pdf")
        if os.path.exists(temp_pdf_path):
            st.success("📄 temp.pdf exists in data folder")
            
            if st.button("🔄 Reprocess temp.pdf", type="primary"):
                with st.spinner("Processing temp.pdf..."):
                    text = read_temp_pdf()
                    
                    if text:
                        st.success(f"✅ Extracted {len(text)} characters from temp.pdf")
                        
                        # Upload to RAG system
                        with st.spinner("Uploading to RAG system..."):
                            result = upload_pdf_text(text)
                            
                            if result:
                                st.success(f"✅ Successfully uploaded temp.pdf to RAG system!")
                                st.info(f"📊 Documents processed: {result.get('documents_processed', 0)}")
                                st.session_state.pdf_processed = True
                                # Clear chat history when new PDF is processed
                                st.session_state.chat_history = []
                                st.rerun()
                            else:
                                st.error("❌ Failed to upload temp.pdf")
                    else:
                        st.error("❌ Failed to extract text from temp.pdf")
        else:
            st.info("📁 No temp.pdf found in data folder")
        
        # Chat controls
        st.markdown("---")
        st.subheader("💬 Chat Controls")
        
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()
        
        st.session_state.show_context = st.checkbox("Show context used", value=False)
    
    with col2:
        st.header("💬 Chat Interface")
        
        # Display chat history
        if st.session_state.chat_history:
            display_chat_history()
        else:
            st.info("👋 Hi! I'm your AI assistant. Upload a PDF and start asking questions!")
        
        # Chat input
        if st.session_state.pdf_processed:
            # Chat input using st.chat_input
            if prompt := st.chat_input("Ask me anything about the PDF..."):
                # Add user message to chat history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": prompt
                })
                
                # Display user message
                with st.chat_message("user"):
                    st.write(prompt)
                
                # Generate and display assistant response
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        result = ask_question(prompt)
                        
                        if result:
                            answer = result.get('answer', 'Sorry, I couldn\'t generate an answer.')
                            st.write(answer)
                            
                            # Add assistant response to chat history
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": answer,
                                "context": result.get('context', '')
                            })
                            
                            # Show context if enabled
                            if st.session_state.get("show_context", False):
                                with st.expander("🔍 View Context Used"):
                                    st.write(result.get('context', 'No context available'))
                        else:
                            error_msg = "Sorry, I encountered an error while processing your question. Please try again."
                            st.write(error_msg)
                            st.session_state.chat_history.append({
                                "role": "assistant",
                                "content": error_msg
                            })
        else:
            st.info("📤 Please upload and process a PDF first to start chatting!")
    
    # Instructions
    st.markdown("---")
    st.subheader("📖 How to Use")
    
    st.markdown("""
    1. **📤 Upload PDF**: Choose any PDF file from your computer
    2. **📤 Process PDF**: Extract text and add to RAG system
    3. **💬 Start Chatting**: Use the chat interface to ask questions
    4. **💡 Get AI Answers**: Groq's Llama3-8b model generates conversational responses
    5. **🔄 Reprocess**: You can reprocess temp.pdf without uploading again
    6. **🗑️ Clear Chat**: Clear chat history when needed
    """)
    
    # Sample questions
    st.subheader("💡 Sample Questions to Try")
    st.markdown("""
    - "What is this document about?"
    - "Can you summarize the main points?"
    - "What are the key findings?"
    - "What recommendations are mentioned?"
    - "Can you explain this in simple terms?"
    """)
    
    # API Key setup instructions
    st.markdown("---")
    st.subheader("🔑 API Setup")
    st.markdown("""
    1. Get your API key from [Groq Console](https://console.groq.com/)
    2. Create a `.env` file in this directory
    3. Add: `GROQ_API_KEY=your_api_key_here`
    4. Restart the application
    """)

if __name__ == "__main__":
    main() 