import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from rag.retriever import get_retriever
import config

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = (
    st.secrets.get("HUGGINGFACEHUB_API_TOKEN")
    or os.getenv("HUGGINGFACEHUB_API_TOKEN")
)

PROMPT_TEMPLATE = """
You are an AI assistant answering questions about uploaded documents.

Use ONLY the supplied context.

Rules:
1. Do not make up information.
2. If the answer is not present, say:
   "I couldn't find that in your documents."
3. Be concise and accurate.
4. Cite relevant document information naturally.

Context:
{context}

Question:
{question}

Answer:
"""


def format_docs(docs):
    return "\n\n".join(
        f"[Source: {d.metadata.get('source', '?')}, Page: {d.metadata.get('page', '')}]\n{d.page_content}"
        for d in docs
    )


def get_llm():
    if not HUGGINGFACEHUB_API_TOKEN:
        raise ValueError(
            "HUGGINGFACEHUB_API_TOKEN not found in environment"
        )
    llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation"
)

    model = ChatHuggingFace(llm=llm)
    return model

def build_chain():
    llm = get_llm()
    retriever = get_retriever()

    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    retrieved_docs = {}

    def retrieve_and_store(question):
        docs = retriever.invoke(question)

        print(f"Retrieved {len(docs)} docs")

        retrieved_docs["docs"] = docs
        return docs

    chain = (
        {
            "context": RunnableLambda(retrieve_and_store)
            | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retrieved_docs


def ask(chain_tuple, question):
    chain, retrieved_docs = chain_tuple

    try:
        answer = chain.invoke(question)
        answer = answer.strip()

        if "Answer:" in answer:
            answer = answer.split("Answer:")[-1].strip()

        sources = []

        for doc in retrieved_docs.get("docs", []):
            meta = doc.metadata

            src = meta.get("source", "unknown")
            page = meta.get("page", "")

            source = src + (
                f" — page {page + 1}"
                if page != ""
                else ""
            )

            if source not in sources:
                sources.append(source)

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        return {
            "answer": f"Error generating response: {str(e)}",
            "sources": []
        }