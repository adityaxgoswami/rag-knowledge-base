# 🧠 RAG Knowledge Base

An AI-powered Retrieval-Augmented Generation (RAG) application that enables users to upload documents and interact with them through natural language queries.

Built using **LangChain**, **ChromaDB**, **Hugging Face**, and **Streamlit**, this project combines semantic search with Large Language Models (LLMs) to provide accurate, context-aware answers grounded in uploaded documents.

---

## 🚀 Features

* 📄 Upload and process PDF, TXT, and Markdown documents
* 🌐 Ingest content directly from URLs
* 🔍 Semantic document retrieval using vector embeddings
* 🤖 Context-aware question answering with Hugging Face LLMs
* 📚 Source attribution and page-level citations
* 💾 Persistent vector storage with ChromaDB
* 🎨 Interactive Streamlit web interface
* ⚡ Fast retrieval using embedding-based similarity search

---

## 📸 Demo

### Upload Documents

> Upload one or more documents to build your knowledge base.

```text
Supported formats:
- PDF
- TXT
- Markdown
```

**Screenshot**

```md
![Document Upload](assets/upload.png)
```

---

### Ask Questions

Query your documents using natural language.

Example:

```text
What is the title of this document?
```

Response:

```text
The title of the document is
"SEO Optimizer - Complete Feature Documentation".
```

**Screenshot**

```md
![Question Answering](assets/chat-demo.png)
```

---

### Source Attribution

Every response includes references to the source document and page number.

Example:

```text
Sources

SEO Optimizer.pdf — page 1
SEO Optimizer.pdf — page 2
```

**Screenshot**

```md
![Sources](assets/sources.png)
```

---

## 🏗️ Architecture

```text
                ┌─────────────────┐
                │ Uploaded Files  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Document Loader │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Text Splitter   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Embeddings      │
                │ (MiniLM)        │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ ChromaDB        │
                │ Vector Store    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Retriever       │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Hugging Face    │
                │ LLM             │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Final Answer    │
                └─────────────────┘
```

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### LLM Framework

* LangChain

### Vector Database

* ChromaDB

### Embeddings

* sentence-transformers/all-MiniLM-L6-v2

### Large Language Model

* Hugging Face Inference API
* ChatHuggingFace
* HuggingFaceEndpoint

### Document Processing

* PyPDFLoader
* TextLoader
* UnstructuredMarkdownLoader
* WebBaseLoader

---

## 📂 Project Structure

```text
rag-knowledge-base/
│
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── rag/
│   ├── chain.py
│   ├── ingest.py
│   └── retriever.py
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/adityaxgoswami/rag-knowledge-base.git
cd rag-knowledge-base
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

You can obtain a token from:

https://huggingface.co/settings/tokens

---

### 5. Run Application

```bash
streamlit run app.py
```

---

## 💡 Usage

### Upload Documents

* PDF
* TXT
* Markdown

### Ask Questions

Examples:

```text
What is the title of this document?

Summarize the key features.

What are the main modules described?

Explain the architecture.
```

### Ingest Web Pages

Paste a URL and ingest web content into the knowledge base.

---

## 📊 Retrieval-Augmented Generation Workflow

1. User uploads documents
2. Documents are chunked into smaller segments
3. Chunks are embedded using MiniLM embeddings
4. Embeddings are stored in ChromaDB
5. User asks a question
6. Relevant chunks are retrieved via semantic search
7. Retrieved context is sent to the LLM
8. LLM generates a grounded answer
9. Sources are displayed to the user

---

## 🔒 Security Notes

* API keys are stored in environment variables
* `.env` is excluded via `.gitignore`
* Chroma vector database is stored locally
* Uploaded documents are processed locally before embedding

---

## 🎯 Future Improvements

* Conversation memory
* Multi-user support
* Document management dashboard
* Hybrid search (keyword + semantic)
* Support for DOCX and PowerPoint files
* OCR support for scanned PDFs
* Authentication and user workspaces
* Streaming responses
* Citation highlighting inside documents

---

## 👨‍💻 Author

**Aditya Goswami**

* GitHub: https://github.com/adityaxgoswami
* LinkedIn: https://www.linkedin.com/in/adityaxgoswami/
* Email: adityagoswami2424@gmail.com

---

## 📄 License

This project is licensed under the MIT License.

See the LICENSE file for details.
