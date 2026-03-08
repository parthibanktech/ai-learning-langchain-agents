"""
09 - Real-World Mini Project: AI Research Assistant
=====================================================
Learn: Put it ALL together — prompts + chains + tools + memory + structured output.

This builds a mini product that:
  ✅ Takes a research topic from the user
  ✅ Searches (simulated) and fetches info
  ✅ Generates a structured report (Pydantic)
  ✅ Maintains conversation history across turns
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from pydantic import BaseModel, Field
from langgraph.prebuilt import create_react_agent
from typing import List

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# ── Pydantic Output Model ─────────────────────────────────────────────────
class ResearchReport(BaseModel):
    topic: str = Field(description="The research topic")
    summary: str = Field(description="2-3 sentence executive summary")
    key_points: List[str] = Field(description="Top 5 key takeaways")
    use_cases: List[str] = Field(description="3 real-world use cases")
    difficulty: str = Field(description="Beginner / Intermediate / Advanced")
    next_steps: str = Field(description="What to learn or do next")

# ── Tools ─────────────────────────────────────────────────────────────────
KNOWLEDGE = {
    "vector database": "Vector databases store high-dimensional embeddings and enable semantic search. Popular options: Pinecone, Weaviate, Chroma, FAISS. Used in RAG systems to find similar content.",
    "langchain": "LangChain 1.x is a framework to build LLM apps using chains, agents, and RAG. Uses LCEL (pipe | operator) for composition. Integrates with LangGraph for agents.",
    "transformer": "Transformers are neural network architectures using attention mechanisms. Introduced in 'Attention Is All You Need' (2017). Foundation of all modern LLMs like GPT, BERT, LLaMA.",
    "prompt engineering": "Prompt engineering is the art of crafting inputs to LLMs to get desired outputs. Techniques: few-shot, chain-of-thought, role prompting, structured output.",
    "fine tuning": "Fine-tuning trains a pre-trained model on specific data to improve performance on a domain. Methods: full fine-tune, LoRA, QLoRA. Requires labeled data and GPU compute.",
}

@tool
def research_topic(topic: str) -> str:
    """Research and retrieve information about an AI/ML topic."""
    for key, info in KNOWLEDGE.items():
        if key in topic.lower():
            return info
    return f"Found general information: {topic} is an important concept in AI/ML ecosystem."

@tool
def compare_technologies(tech1: str, tech2: str) -> str:
    """Compare two AI technologies across key dimensions."""
    return f"""
Comparison: {tech1} vs {tech2}
- Purpose: Different use cases and goals
- Maturity: Both are production-ready in 2025
- Integration: Often used together in production systems
- Learning curve: Depends on background
- Community: Both have strong open-source communities
"""

# ── Part 1: Structured Report Generator ──────────────────────────────────
def generate_report(topic: str) -> ResearchReport:
    """Generate a structured research report on any AI topic."""
    print(f"\n📊 Generating research report on: '{topic}'...")

    structured_llm = llm.with_structured_output(ResearchReport)

    # First research the topic
    info = research_topic.invoke(topic)

    prompt = f"""
    Based on this information about {topic}:
    {info}
    
    Generate a comprehensive research report. Be specific and practical.
    """
    return structured_llm.invoke(prompt)

# ── Part 2: Conversational Research Agent ────────────────────────────────
def create_research_agent():
    """Creates an agent that can research and compare topics."""
    return create_react_agent(
        model=llm,
        tools=[research_topic, compare_technologies],
        prompt="""You are an expert AI research assistant. 
        Research topics thoroughly and give crisp, actionable answers.
        Always back up your answers with the tools available."""
    )

# ── Demo ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 AI Research Assistant Demo")
    print("=" * 60)

    # Demo 1: Structured Report
    report = generate_report("vector database")
    print(f"\n{'='*60}")
    print(f"📋 RESEARCH REPORT: {report.topic.upper()}")
    print(f"{'='*60}")
    print(f"\n📌 SUMMARY:\n{report.summary}")
    print(f"\n🎯 KEY POINTS:")
    for i, point in enumerate(report.key_points, 1):
        print(f"   {i}. {point}")
    print(f"\n💼 USE CASES:")
    for uc in report.use_cases:
        print(f"   • {uc}")
    print(f"\n📈 DIFFICULTY: {report.difficulty}")
    print(f"\n👉 NEXT STEPS: {report.next_steps}")

    # Demo 2: Agent for conversational research
    print(f"\n{'='*60}")
    print("🤖 CONVERSATIONAL AGENT MODE")
    print(f"{'='*60}")

    agent = create_research_agent()

    questions = [
        "What is LangChain and how is it used?",
        "Compare LangChain and prompt engineering",
    ]

    for q in questions:
        print(f"\n❓ {q}")
        result = agent.invoke({"messages": [("human", q)]})
        last_msg = result["messages"][-1]
        print(f"🤖 {last_msg.content[:500]}")
