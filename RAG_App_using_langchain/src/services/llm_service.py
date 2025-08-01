from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq

class LLMService:
    """Service for handling LLM operations and conversation chains"""
    
    def __init__(self, model_name="llama3-8b-8192"):
        """Initialize the LLM service with specified model"""
        self.model_name = model_name
        # Direct API key - replace with your actual Groq API key
        self.groq_api_key = "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"
        self.llm = None
        self.chain = None
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the LLM with Groq API"""
        if not self.groq_api_key:
            raise Exception("Groq API key not found")
        
        try:
            self.llm = ChatGroq(
                groq_api_key=self.groq_api_key,
                model_name=self.model_name
            )
        except Exception as e:
            raise Exception(f"Error initializing LLM: {str(e)}")
    
    def create_conversational_chain(self, prompt_template=None):
        """Create a conversational chain for question answering"""
        if not prompt_template:
            prompt_template = """Use the following context to answer the question.
            
            Context:
            {context}

            Question:
            {question}

            Answer:"""
        
        try:
            prompt = PromptTemplate(
                template=prompt_template, 
                input_variables=["context", "question"]
            )
            self.chain = load_qa_chain(llm=self.llm, prompt=prompt, chain_type="stuff")
            return self.chain
        except Exception as e:
            raise Exception(f"Error creating conversational chain: {str(e)}")
    
    def get_response(self, documents, question):
        """Get response from the LLM chain"""
        if self.chain is None:
            self.create_conversational_chain()
        
        try:
            response = self.chain.run(input_documents=documents, question=question)
            return response
        except Exception as e:
            raise Exception(f"Error getting response from LLM: {str(e)}")
    
    def get_model_info(self):
        """Get information about the current LLM model"""
        return {
            "model_name": self.model_name,
            "provider": "Groq",
            "chain_type": "stuff" if self.chain else "not_initialized"
        }
    
    def update_model(self, new_model_name):
        """Update the LLM model"""
        try:
            self.model_name = new_model_name
            self._initialize_llm()
            self.chain = None  # Reset chain to use new model
            return True
        except Exception as e:
            raise Exception(f"Error updating model: {str(e)}") 