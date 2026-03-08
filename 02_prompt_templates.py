"""
02 - Prompt Templates
======================
Learn: How to create reusable, dynamic prompts using ChatPromptTemplate

Key Concept: Templates let you define prompts ONCE and fill in variables later.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

# 1. Basic ChatPromptTemplate with variables
print("=== ChatPromptTemplate ===")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {topic}. Keep answers under 3 sentences."),
    ("human", "Explain {concept} to me like I'm 10 years old."),
])

# Format the prompt (inspect it before sending)
formatted = prompt.format_messages(topic="machine learning", concept="neural networks")
print("Formatted Prompt:")
for msg in formatted:
    print(f"  [{msg.type.upper()}]: {msg.content}")

# Invoke LLM with filled template
response = llm.invoke(formatted)
print(f"\nResponse: {response.content}")

# 2. Template with multiple variables
print("\n=== Email Writer Template ===")
email_prompt = ChatPromptTemplate.from_template("""
Write a professional email for the following:
- From: {sender}
- To: {receiver}
- Purpose: {purpose}
- Tone: {tone}

Keep it under 100 words.
""")

email_chain = email_prompt | llm  # pipe operator to chain!
response = email_chain.invoke({
    "sender": "Parthiban",
    "receiver": "Team",
    "purpose": "schedule a meeting next Monday",
    "tone": "friendly but professional"
})
print(response.content)

# 3. Simple PromptTemplate (for non-chat models or simpler use)
print("\n=== Simple PromptTemplate ===")
simple_prompt = PromptTemplate.from_template(
    "What are the top 3 skills needed to become a {role}? List them briefly."
)
filled = simple_prompt.format(role="Data Scientist")
print(f"Prompt: {filled}")
response = llm.invoke(filled)
print(f"Response: {response.content}")
