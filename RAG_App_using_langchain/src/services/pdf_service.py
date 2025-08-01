import os
from pdfminer.high_level import extract_text
from langchain.text_splitter import CharacterTextSplitter

class PDFService:
    """Service for handling PDF processing and text extraction"""
    
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extract text content from a PDF file"""
        try:
            return extract_text(pdf_path)
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    @staticmethod
    def get_text_chunks(raw_text, chunk_size=1000, chunk_overlap=200):
        """Split text into chunks for processing"""
        try:
            splitter = CharacterTextSplitter(
                separator="\n", 
                chunk_size=chunk_size, 
                chunk_overlap=chunk_overlap, 
                length_function=len
            )
            return splitter.split_text(raw_text)
        except Exception as e:
            raise Exception(f"Error splitting text into chunks: {str(e)}")
    
    @staticmethod
    def save_uploaded_file(uploaded_file, file_path=None):
        """Save uploaded file to the data folder with its original name"""
        try:
            data_folder = "data"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)
            
            if file_path is None:
                file_path = os.path.join(data_folder, uploaded_file.name)
            
            # For FastAPI UploadFile
            if hasattr(uploaded_file, 'file'):
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.file.read())
            else:
                # For Streamlit uploaded file
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
            
            return file_path
        except Exception as e:
            raise Exception(f"Error saving uploaded file: {str(e)}")
    
    @staticmethod
    def cleanup_temp_file(file_path="temp.pdf"):
        """Clean up temporary files"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Warning: Could not cleanup temp file {file_path}: {str(e)}") 