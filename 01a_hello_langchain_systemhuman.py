from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load your OPENAI_API_KEY from .env file
load_dotenv()

# 1. Create the LLM (gpt-4o-mini is fast + cheap)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# 2. Use System + Human message for context
print("\n=== With System Message ===")
messages = [
    SystemMessage(content="You are a helpful assistant. Always give short, crisp answers. You are a python tutor expert in langchain."),
    HumanMessage(content="What is a system message, what is a human message in openai library?"),
]
response = llm.invoke(messages)
print(response.content)