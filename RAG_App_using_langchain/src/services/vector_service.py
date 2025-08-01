from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

class VectorService:
    """Service for handling vector store operations and embeddings"""
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize the vector service with specified embedding model"""
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.vector_store = None
    
    def create_vector_store(self, text_chunks):
        """Create FAISS vector store from text chunks"""
        try:
            self.vector_store = FAISS.from_texts(text_chunks, embedding=self.embeddings)
            return self.vector_store
        except Exception as e:
            raise Exception(f"Error creating vector store: {str(e)}")
    
    def similarity_search(self, query, k=4):
        """Perform similarity search on the vector store"""
        if self.vector_store is None:
            raise Exception("Vector store not initialized. Please create vector store first.")
        
        try:
            return self.vector_store.similarity_search(query, k=k)
        except Exception as e:
            raise Exception(f"Error performing similarity search: {str(e)}")
    
    def save_vector_store(self, path="database/faiss_index"):
        """Save vector store to disk"""
        if self.vector_store is None:
            raise Exception("No vector store to save")
        
        try:
            os.makedirs(path, exist_ok=True)
            self.vector_store.save_local(path)
            return path
        except Exception as e:
            raise Exception(f"Error saving vector store: {str(e)}")
    
    def load_vector_store(self, path="database/faiss_index"):
        """Load vector store from disk"""
        try:
            if os.path.exists(path):
                self.vector_store = FAISS.load_local(path, self.embeddings)
                return self.vector_store
            else:
                raise Exception(f"Vector store not found at {path}")
        except Exception as e:
            raise Exception(f"Error loading vector store: {str(e)}")
    
    def is_loaded(self):
        """Check if vector store is loaded"""
        return self.vector_store is not None
    
    def get_vector_store_info(self):
        """Get information about the current vector store"""
        if self.vector_store is None:
            return {"status": "not_initialized"}
        
        try:
            return {
                "status": "initialized",
                "index_size": len(self.vector_store.index_to_docstore_id),
                "embedding_dimension": self.vector_store.embedding_function.client.get_sentence_embedding_dimension()
            }
        except Exception as e:
            return {"status": "error", "message": str(e)} 