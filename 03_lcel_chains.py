"""
03 - LCEL Chains (LangChain Expression Language)
=================================================
Learn: How to compose chains using the | pipe operator

Key Concept: LCEL lets you chain components like LEGO blocks:
    prompt | llm | output_parser
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# ── 1. Basic Chain: prompt | llm | parser ──────────────────────────────────
print("=== Basic Chain ===")
prompt = ChatPromptTemplate.from_template(
    "Summarize this topic in exactly 2 sentences: {topic}"
)
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"topic": "Generative AI"})
print(result)

# ── 2. Chain with Custom Transform ────────────────────────────────────────
print("\n=== Chain with Custom Function ===")
def make_bold(text: str) -> str:
    """Wrap each line with markdown bold."""
    return "\n".join(f"**{line}**" for line in text.strip().split("\n") if line)

chain2 = (
    ChatPromptTemplate.from_template("List 3 benefits of {thing}, each on a new line.")
    | llm
    | StrOutputParser()
    | RunnableLambda(make_bold)
)
result2 = chain2.invoke({"thing": "learning LangChain"})
print(result2)

# ── 3. Parallel Chain: process two things at once ─────────────────────────
print("\n=== Parallel Chains ===")
from langchain_core.runnables import RunnableParallel

pros_chain = (
    ChatPromptTemplate.from_template("List 2 pros of {technology} in bullet points.")
    | llm | StrOutputParser()
)
cons_chain = (
    ChatPromptTemplate.from_template("List 2 cons of {technology} in bullet points.")
    | llm | StrOutputParser()
)

parallel = RunnableParallel(pros=pros_chain, cons=cons_chain)
result3 = parallel.invoke({"technology": "LangChain"})
print("PROS:", result3["pros"])
print("CONS:", result3["cons"])

# ── 4. Chain Chaining: output of one feeds next ────────────────────────────
print("\n=== Sequential Chain (output → input) ===")
generate_idea = (
    ChatPromptTemplate.from_template("Give me one creative app idea using {technology}.")
    | llm | StrOutputParser()
)
build_plan = (
    ChatPromptTemplate.from_template("Create a 3-step plan to build this app:\n{idea}")
    | llm | StrOutputParser()
)
# Chain them: first get idea, then build plan
full_chain = (
    {"idea": generate_idea, "technology": RunnablePassthrough()}
    | RunnableLambda(lambda x: {"idea": x["idea"]})
    | build_plan
)
result4 = full_chain.invoke({"technology": "AI agents"})
print(result4)
