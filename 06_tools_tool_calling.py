"""
06 - Tools & Tool Calling
==========================
Learn: How to give LLMs the ability to "call" Python functions.

Key Concept: Tools = functions the LLM can decide to call.
The LLM reads the function signature + docstring to decide WHEN to use it.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ── 1. Define Tools using @tool decorator ─────────────────────────────────
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # Simulated — replace with a real API call
    weather_db = {
        "mumbai": "30°C, Humid, Partly Cloudy",
        "delhi":  "22°C, Clear Sky, Slight Breeze",
        "bangalore": "25°C, Pleasant, Light Rain",
    }
    return weather_db.get(city.lower(), f"Weather data not available for {city}.")

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency from one type to another."""
    # Simulated rates (USD base)
    rates = {"USD": 1.0, "INR": 83.5, "EUR": 0.92, "GBP": 0.79}
    if from_currency not in rates or to_currency not in rates:
        return f"Unknown currency: {from_currency} or {to_currency}"
    converted = amount * (rates[to_currency] / rates[from_currency])
    return f"{amount} {from_currency} = {converted:.2f} {to_currency}"

@tool
def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression like '2 + 2 * 10'."""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# ── 2. Bind tools to LLM ──────────────────────────────────────────────────
tools = [get_weather, convert_currency, calculate]
llm_with_tools = llm.bind_tools(tools)

# ── 3. Manual Tool Calling Loop ───────────────────────────────────────────
print("=== Manual Tool Calling Loop ===")

# Map tool names → functions
tool_map = {t.name: t for t in tools}

def run_with_tools(user_question: str):
    print(f"\n🧑 User: {user_question}")
    messages = [HumanMessage(content=user_question)]

    # LLM decides which tool(s) to call
    response = llm_with_tools.invoke(messages)
    messages.append(response)
   # print("response " , response ," message" , messages)

    if not response.tool_calls:
        print(f"🤖 AI: {response.content}")
        return

    # Execute all requested tool calls
    for tool_call in response.tool_calls: 
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        print(f"🔧 Calling tool: {tool_name}({tool_args})")

        result = tool_map[tool_name].invoke(tool_args)
        print(f"📤 Tool result: {result}")

        messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

    # Final LLM response after tool results
    final_response = llm_with_tools.invoke(messages)
    print(f"🤖 AI: {final_response.content}")

# Test all tools
run_with_tools("What is the weather in Mumbai?")
run_with_tools("Convert 500 USD to INR")
run_with_tools("What is 15% of 2500?")
run_with_tools("What's the weather in Delhi and also convert 100 EUR to INR?")
