"""
05 - Chat History & Memory (Conversation)
==========================================
Learn: How to build a chatbot that REMEMBERS previous messages.

Key Concept: LLMs are stateless by default - you must manually track history.
LangChain uses RunnableWithMessageHistory to manage this cleanly.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# ── Method 1: Manual History (understand the basics) ─────────────────────
print("=== Method 1: Manual History ===")
chat_history = []  # List of messages

def chat(user_input: str) -> str:
    chat_history.append(HumanMessage(content=user_input))
    response = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    return response.content

print("User: Hi, my name is Parthiban and I love AI.")
print("AI:", chat("Hi, my name is Parthiban and I love AI."))

print("\nUser: What is my name?")
print("AI:", chat("What is my name?"))  # It REMEMBERS!

print("\nUser: What topic do I love?")
print("AI:", chat("What topic do I love?"))  # Still remembers!

# ── Method 2: RunnableWithMessageHistory (production approach) ─────────────
print("\n=== Method 2: RunnableWithMessageHistory ===")

# Store: maps session_id → message history
store: dict = {}

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Prompt with MessagesPlaceholder (injects history automatically)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise."),
    MessagesPlaceholder(variable_name="history"),  # history auto-injected here
    ("human", "{input}"),
])

chain = prompt | llm | StrOutputParser()

# Wrap with history management
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# Each session_id is a separate conversation
config = {"configurable": {"session_id": "user_abc"}}

print("Turn 1:")
r1 = chain_with_history.invoke({"input": "My favorite language is Python."}, config=config)
print(f"AI: {r1}")

print("\nTurn 2:")
r2 = chain_with_history.invoke({"input": "What's my favorite language?"}, config=config)
print(f"AI: {r2}")  # Should remember Python!

print("\nTurn 3:")
r3 = chain_with_history.invoke({"input": "Write a hello world in it."}, config=config)
print(f"AI: {r3}")

# Check what's stored
print(f"\n📦 Session 'user_abc' has {len(store['user_abc'].messages)} messages stored.")
