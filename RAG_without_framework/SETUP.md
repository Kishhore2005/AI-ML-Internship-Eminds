# Setup Guide for Simple RAG with Groq

## 🔑 Groq API Setup

### Step 1: Get Groq API Key
1. Go to [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Create a new API key
4. Copy your API key

### Step 2: Create Environment File
Create a `.env` file in the project directory:

```bash
# Create .env file
echo "GROQ_API_KEY=your_actual_api_key_here" > .env
```

Or manually create `.env` file with:
```
GROQ_API_KEY=your_actual_api_key_here
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start the Application
```bash
# Start RAG API server
python main.py

# In another terminal, start Streamlit app
streamlit run simple_rag.py
```

## 🚀 How It Works

1. **Upload PDF** → Extract text → Store in RAG system
2. **Ask Question** → RAG finds relevant context → Groq generates intelligent answer
3. **Get Answer** → Llama3-8b model provides detailed, accurate responses

## 🔧 Features

- ✅ **PDF Processing**: Extract text from any PDF
- ✅ **RAG Retrieval**: Find relevant document chunks
- ✅ **Groq Integration**: Use Llama3-8b for intelligent answers
- ✅ **Simple Interface**: Just upload and ask questions
- ✅ **Context Viewing**: See what context was used

## 💡 Benefits of Groq Integration

- **Better Answers**: Llama3-8b provides more intelligent responses
- **Contextual Understanding**: Model understands context better
- **Accurate Responses**: More precise answers based on document content
- **Natural Language**: More human-like responses

## ⚠️ Important Notes

- Keep your API key secure and never commit it to version control
- Groq has usage limits - check their pricing
- The first run may take longer as models load 