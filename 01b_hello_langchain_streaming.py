import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load your OPENAI_API_KEY from .env file
load_dotenv()

# 1. Create the LLM (gpt-4o-mini is fast + cheap)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

# 2. Streaming - see tokens as they arrive
print("\n=== Streaming ===")
for chunk in llm.stream("Tell me a fun fact about AI in one sentence."):
    print(chunk.content, end="", flush=True)
print()  # newline at end
