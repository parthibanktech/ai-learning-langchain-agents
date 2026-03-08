"""
07 - Agents with LangChain
===========================
Learn: How to build an autonomous agent that reasons, picks tools, and loops.

Key Concept: Agent = LLM + Tools + Loop (ReAct pattern)
The agent THINKS → picks a tool → sees the result → THINKS again → repeats.

Uses LangGraph's create_react_agent (the modern standard in LangChain 1.x)
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent  # modern standard

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ── Define Tools ──────────────────────────────────────────────────────────
@tool
def search_web(query: str) -> str:
    """Search the web for current information on a topic."""
    # Simulated search results
    results = {
        "langchain": "LangChain 1.2.10 is the latest version (Feb 2026). It supports LCEL, agents via LangGraph, and RAG.",
        "openai": "OpenAI's latest model is GPT-4o (2025). It supports vision, function calling, and 128k context.",
        "india gdp": "India's GDP (2025 estimate): $4.2 trillion, making it the 4th largest economy globally.",
    }
    for key in results:
        if key in query.lower():
            return results[key]
    return f"No results found for: {query}. Try rephrasing."

@tool
def calculate(expression: str) -> str:
    """Evaluate a math expression. Example: '100 * 0.18' for 18% of 100."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

@tool
def get_stock_price(company: str) -> str:
    """Get the latest stock price for a company."""
    prices = {
        "apple": "$189.50",
        "google": "$158.20",
        "infosys": "₹1,842",
        "tcs": "₹4,290",
    }
    return prices.get(company.lower(), f"Stock data not found for {company}.")

# ── Create Agent ──────────────────────────────────────────────────────────
tools = [search_web, calculate, get_stock_price]

# create_react_agent is the official modern way (LangChain 1.x + LangGraph)
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="You are a helpful research assistant. Use tools to find accurate information."
)

# ── Run Agent ─────────────────────────────────────────────────────────────
def run_agent(question: str):
    print(f"\n{'='*60}")
    print(f"🧑 Question: {question}")
    print("="*60)

    result = agent.invoke({"messages": [("human", question)]})

    # Print the conversation trace
    for msg in result["messages"]:
        role = msg.__class__.__name__
        if hasattr(msg, 'content') and msg.content:
            icon = {"HumanMessage": "🧑", "AIMessage": "🤖", "ToolMessage": "🔧"}.get(role, "📌")
            print(f"{icon} [{role}]: {msg.content[:200]}")
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"   ⚡ Tool call: {tc['name']}({tc['args']})")

# Test the agent with multi-step reasoning
run_agent("What is the latest version of LangChain and what year was it released?")
run_agent("What is the stock price of TCS and Infosys? Which one is higher?")
run_agent("If I invest ₹50,000 in TCS and the stock goes up 15%, how much profit will I make?")
