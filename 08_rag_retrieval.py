"""
08 - RAG: Retrieval Augmented Generation
=========================================
Learn: How to make LLMs answer questions from YOUR documents.

Key Concept:
  1. Load docs → Split into chunks → Embed → Store in vector DB
  2. User asks → Find relevant chunks → LLM answers with context

Install extra:
    pip install faiss-cpu tiktoken langchain-community
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# ── Step 1: Your Documents (simulate a knowledge base) ────────────────────
print("📄 Step 1: Loading documents...")
docs = [
    Document(page_content="""
    LangChain is a framework for building LLM-powered applications.
    Key features: LCEL chains, tools, agents, RAG, memory.
    Version 1.0 was released in October 2025.
    It integrates with OpenAI, Anthropic, Ollama, and many other LLM providers.
    """, metadata={"source": "langchain_intro.txt"}),

    Document(page_content="""
    LangGraph is a library built on top of LangChain for building stateful, 
    multi-step, and multi-actor AI applications. It works like a state machine.
    It supports cycles (loops), conditional routing, and human-in-the-loop.
    LangGraph 1.0 was released alongside LangChain 1.0 in October 2025.
    Ideal for complex agents and multi-agent systems.
    """, metadata={"source": "langgraph_intro.txt"}),

    Document(page_content="""
    LangSmith is the observability and debugging platform for LangChain apps.
    It lets you trace every step of your chain or agent execution.
    You can compare models, track costs, and debug failures.
    Use LANGCHAIN_TRACING_V2=true to enable tracing automatically.
    LangSmith has a free tier for developers.
    """, metadata={"source": "langsmith_intro.txt"}),

    Document(page_content="""
    Retrieval Augmented Generation (RAG) is a technique to ground LLMs in 
    external knowledge. Steps: (1) Embed documents into vectors,
    (2) Store in a vector database like FAISS or Chroma,
    (3) On query: embed the question and find top-k similar chunks,
    (4) Feed those chunks as context to the LLM.
    RAG reduces hallucinations and keeps responses factual.
    """, metadata={"source": "rag_explained.txt"}),
]

# ── Step 2: Split into chunks ─────────────────────────────────────────────
print("✂️  Step 2: Splitting into chunks...")
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"   Created {len(chunks)} chunks from {len(docs)} documents.")

# ── Step 3: Create Vector Store ───────────────────────────────────────────
print("🔢 Step 3: Embedding and storing in FAISS...")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})  # return top 3 chunks
print("   Vector store ready!")

# ── Step 4: Build RAG Chain ───────────────────────────────────────────────
print("⛓️  Step 4: Building RAG chain...")

rag_prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based ONLY on the context below.
If the answer isn't in the context, say "I don't have that information."

Context:
{context}

Question: {question}

Answer:
""")

def format_docs(docs):
    return "\n\n".join(f"[{d.metadata['source']}]\n{d.page_content}" for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# ── Step 5: Ask Questions! ────────────────────────────────────────────────
print("\n" + "="*60)
print("🎯 RAG DEMO - Asking questions about our docs:")
print("="*60)

questions = [
    "What is LangSmith and how do I enable tracing?",
    "When was LangGraph 1.0 released?",
    "How does RAG reduce hallucinations?",
    "What are the key features of LangChain?",
    "What is the capital of France?",  # Not in docs → should say "I don't have that information"
]

for q in questions:
    print(f"\n❓ {q}")
    answer = rag_chain.invoke(q)
    print(f"✅ {answer}")
