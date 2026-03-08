from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load your OPENAI_API_KEY from .env file
load_dotenv()

# 1. Create the LLM (gpt-4o-mini is fast + cheap)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# 2. Send a simple human message
print("=== Simple Invoke ===")
response = llm.invoke("What is LangChain in one sentence?")
print(response.content)