
import streamlit as st
import tempfile
import os

from rag.ingest import ingest_files, ingest_url
from rag.chain import build_chain, ask

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Personal Knowledge Base")


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def load_chain():
    st.session_state.chain = build_chain()


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────

with st.sidebar:

    st.header("📄 Add Documents")

    uploaded = st.file_uploader(
        "Upload files (PDF, TXT, MD)",
        accept_multiple_files=True,
        type=["pdf", "txt", "md"]
    )

    if uploaded:
        st.caption(f"{len(uploaded)} file(s) selected")

    if uploaded and st.button("Ingest Files"):

        with st.spinner("Chunking and embedding..."):

            file_info = []

            for f in uploaded:

                tmp = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=os.path.splitext(f.name)[1]
                )

                tmp.write(f.read())
                tmp.flush()

                file_info.append({
                    "path": tmp.name,
                    "name": f.name
                })

            count = ingest_files(file_info)

        st.success(f"✅ Stored {count} chunks")

        with st.spinner("Reloading chain..."):
            load_chain()

        st.success("🚀 Chain ready. Start asking!")

    st.divider()

    url = st.text_input("Or paste a URL")

    if url and st.button("Ingest URL"):

        with st.spinner("Loading page..."):

            count = ingest_url(url)

        st.success(f"✅ Stored {count} chunks")

        with st.spinner("Reloading chain..."):
            load_chain()

        st.success("🚀 Chain ready. Start asking!")

    st.divider()

    if st.button("Clear Conversation"):

        st.session_state.messages = []


# ─────────────────────────────────────────────────────────────
# Init
# ─────────────────────────────────────────────────────────────

if "chain" not in st.session_state:

    with st.spinner("Initialising..."):
        load_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []


# ─────────────────────────────────────────────────────────────
# Chat History
# ─────────────────────────────────────────────────────────────

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

        if msg.get("sources"):

            with st.expander("📚 Sources"):

                for source in msg["sources"]:
                    st.markdown(f"- {source}")


# ─────────────────────────────────────────────────────────────
# Chat Input
# ─────────────────────────────────────────────────────────────

if prompt := st.chat_input(
    "Ask anything about your documents..."
):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                result = ask(
                    st.session_state.chain,
                    prompt
                )

                answer = result.get(
                    "answer",
                    "No response generated."
                )

                sources = result.get(
                    "sources",
                    []
                )

                st.markdown(answer)

                if sources:

                    with st.expander("📚 Sources"):

                        for source in sources:
                            st.markdown(f"- {source}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except Exception as e:

                error_msg = f"❌ Error: {str(e)}"

                st.error(error_msg)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "sources": []
                })

