# rag/ingest.py
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader, UnstructuredMarkdownLoader,
    WebBaseLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import config, os

def get_loader(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext == ".md":
        return UnstructuredMarkdownLoader(file_path)
    elif ext in (".txt", ""):
        return TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def ingest_files(file_info: list[dict]) -> int:
    docs = []

    for file in file_info:

        path = file["path"]
        original_name = file["name"]

        loader = get_loader(path)
        loaded = loader.load()

        # Store original uploaded filename
        for d in loaded:
            d.metadata["source"] = original_name

        docs.extend(loaded)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name=config.EMBED_MODEL
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.CHROMA_DIR
    )

    # Persist DB
    try:
        vectorstore.persist()
    except:
        pass

    return len(chunks)

def ingest_url(url: str) -> int:
    loader = WebBaseLoader(url)
    docs = loader.load()
    for d in docs:
        d.metadata["source"] = url
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBED_MODEL)
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=config.CHROMA_DIR
    )
    return len(chunks)