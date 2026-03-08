"""
04 - Output Parsers: Get Structured Data from LLMs
====================================================
Learn: How to extract clean, structured output (JSON, Lists, Pydantic models)
       from raw LLM responses.

Key Concept: LLMs return text — parsers convert it to Python objects.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, CommaSeparatedListOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ── 1. StrOutputParser (most common - returns plain string) ──────────────
print("=== StrOutputParser ===")
chain = (
    ChatPromptTemplate.from_template("What is {topic}?")
    | llm
    | StrOutputParser()
)
print(chain.invoke({"topic": "LangChain"}))

# ── 2. CommaSeparatedListOutputParser ────────────────────────────────────
print("\n=== CommaSeparatedListOutputParser ===")
list_parser = CommaSeparatedListOutputParser()
chain2 = (
    ChatPromptTemplate.from_template(
        "List 5 programming languages. {format_instructions}"
    )
    | llm
    | list_parser
)
langs = chain2.invoke({"format_instructions": list_parser.get_format_instructions()})
print(f"Type: {type(langs)} → {langs}")

# ── 3. JsonOutputParser ───────────────────────────────────────────────────
print("\n=== JsonOutputParser ===")
json_chain = (
    ChatPromptTemplate.from_template(
        "Give me a JSON object with fields: name, age, and skills (list) "
        "for a fictional AI engineer named {name}."
    )
    | ChatOpenAI(model="gpt-4o-mini", temperature=1)
    | JsonOutputParser()
)
data = json_chain.invoke({"name": "Priya"})
print(f"Name: {data['name']}, Age: {data['age']}, Skills: {data['skills']}")

# ── 4. Pydantic Structured Output (Best for production!) ──────────────────
print("\n=== Pydantic Structured Output (with_structured_output) ===")

class JobPosting(BaseModel):
    title: str = Field(description="Job title")
    company: str = Field(description="Company name")
    required_skills: List[str] = Field(description="List of required skills")
    salary_range: str = Field(description="Salary range (e.g. $80k-$120k)")

# with_structured_output is the modern way (LangChain 0.3+)
structured_llm = llm.with_structured_output(JobPosting)

job = structured_llm.invoke(
    "Create a realistic job posting for a Senior AI Engineer at a startup."
)
print(f"Title: {job.title}")
print(f"Company: {job.company}")
print(f"Skills: {job.required_skills}")
print(f"Salary: {job.salary_range}")
