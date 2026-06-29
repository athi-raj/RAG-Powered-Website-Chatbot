# RAG-Powered Website Chatbot

An intelligent chatbot that ingests any website URL, recursively crawls linked pages, and answers user queries using Retrieval-Augmented Generation (RAG).

## How It Works
1. **Web Crawling** — Recursively scrapes a seed URL and all linked pages using BeautifulSoup / Scrapy
2. **Content Processing** — Cleans HTML, chunks text, and tags metadata via LangChain / LlamaIndex
3. **Vector Embedding** — Encodes chunks into dense vectors using Sentence Transformers
4. **Vector Storage** — Indexes embeddings in FAISS / ChromaDB with caching for low-latency retrieval
5. **Semantic Retrieval** — Embeds user query and retrieves top-k relevant chunks via ANN similarity search
6. **LLM Generation** — Constructs a grounded prompt and generates accurate responses using GPT-4 / Gemini

## Features

- Recursive website crawling with deduplication and robots.txt compliance
- Automated text cleaning, chunking, and preprocessing pipeline
- Semantic search with vector embeddings and similarity matching
- RAG pipeline for context-aware, hallucination-reduced responses
- Support for structured and unstructured web content
- Optimized caching and retrieval for low-latency responses
- Interactive chatbot UI for real-time question answering

## Tech Stack

| Layer | Tools |
|---|---|
| Crawling | BeautifulSoup, Scrapy |
| Orchestration | LangChain, LlamaIndex |
| Embeddings | Sentence Transformers |
| Vector Store | FAISS, ChromaDB |
| LLM | OpenAI GPT-4, Gemini |
| Interface | Flask, Streamlit |
| Language | Python |



## Topics

`rag` `llm` `vector-search` `web-scraping` `langchain` `faiss` `chromadb` `chatbot` `nlp` `python` `openai` `sentence-transformers`
