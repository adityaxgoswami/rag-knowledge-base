# rag/retriever.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import config

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBED_MODEL)
    vectorstore = Chroma(
        persist_directory=config.CHROMA_DIR,
        embedding_function=embeddings
    )
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": config.TOP_K}
    )