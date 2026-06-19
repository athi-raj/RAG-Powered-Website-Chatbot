import streamlit as st
from main import ingest
from src.rag.pipeline import ask

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 RAG Website Chatbot")
st.caption("Paste any website URL → I crawl it → Ask me anything about it.")

# ── Sidebar: URL input ──
with st.sidebar:
    st.header("⚙️ Setup")
    url = st.text_input("Website URL", placeholder="https://docs.python.org")

    if st.button("🚀 Crawl & Index", use_container_width=True):
        if url:
            with st.spinner("Crawling website... this may take a minute."):
                ingest(url)
                st.session_state.url      = url
                st.session_state.messages = []
            st.success(f"✅ Indexed!")
        else:
            st.warning("Please enter a URL.")

    if "url" in st.session_state:
        st.info(f"Active: {st.session_state.url}")

# ── Chat area ──
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("sources"):
            with st.expander("📎 Sources"):
                for s in msg["sources"]:
                    st.markdown(f"- [{s}]({s})")

if prompt := st.chat_input("Ask something about the website..."):
    if "url" not in st.session_state:
        st.warning("Please crawl a website first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                result = ask(st.session_state.url, prompt)
            st.write(result["answer"])
            if result["sources"]:
                with st.expander("📎 Sources"):
                    for s in result["sources"]:
                        st.markdown(f"- [{s}]({s})")

        st.session_state.messages.append({
            "role":    "assistant",
            "content": result["answer"],
            "sources": result["sources"]
        })
