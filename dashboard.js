const modules = [
    {
        id: "01",
        title: "Hello LangChain",
        file: "01_hello_langchain_simple.py",
        desc: "The absolute entry point. Learn how to initialize a Chat Model and send your first message to GPT-4o-mini.",
        notes: "At this stage, you are learning the 'ChatModel' interface. In LangChain 0.3+, we use the .invoke() method which is consistent across all components.",
        type: "Foundation",
        features: [
            { icon: "fas fa-plug", title: "Direct Connect", desc: "Initialize ChatOpenAI easily." },
            { icon: "fas fa-comment", title: "Chat Models", desc: "Interact with modern LLMs like GPT." }
        ],
        breakdown: [
            { code: "llm = ChatOpenAI(model='gpt-4o-mini')", explanation: "Creates a connection to OpenAI's miniature flagship model." },
            { code: "response = llm.invoke('Hello')", explanation: "The standard 'invoke' pattern returning a BaseMessage object." }
        ],
        fullSource: `from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

print("=== Simple Invoke ===")
response = llm.invoke("What is LangChain in one sentence?")
print(response.content)`,
        output: "🧑 User: What is LangChain?\n🤖 AI: LangChain is a framework designed to simplify the creation of applications using large language models (LLMs).",
        simulation: (input) => `🤖 AI: Based on your input "${input}", LangChain is a powerful framework for building LLM-powered apps!`
    },
    {
        id: "01a",
        title: "System & Human Messages",
        file: "01a_hello_langchain_systemhuman.py",
        desc: "Learn to differentiate between System instructions and Human queries.",
        notes: "System messages set the 'behavior' of the AI, while Human messages provide the task. This is the key to creating focused AI personas.",
        type: "Foundation",
        features: [
            { icon: "fas fa-user-shield", title: "System Persona", desc: "Define how the AI should act (e.g. 'You are a pirate')." },
            { icon: "fas fa-user", title: "Human Message", desc: "The actual core query from the end user." }
        ],
        breakdown: [
            { code: "SystemMessage(content='...')", explanation: "Defines the background rules for the model." },
            { code: "[sys, human]", explanation: "Sending a list of messages creates a conversational context." }
        ],
        fullSource: `from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(model="gpt-4o-mini")
messages = [
    SystemMessage(content="You are a helpful assistant that specialized in Python."),
    HumanMessage(content="How do I use lists?")
]
response = llm.invoke(messages)
print(response.content)`,
        output: "📌 System: You are a specialized Python assistant.\n🧑 Human: How do I use lists?\n🤖 AI: Python lists are built-in data structures used to store collections of items...",
        simulation: (input) => `🤖 AI Persona: As a Python expert, regarding your question "${input}", the best practice would be to use structured data types.`
    },
    {
        id: "02",
        title: "Prompt Templates",
        file: "02_prompt_templates.py",
        desc: "Move beyond static strings. Use templates to define consistent instructions while injecting dynamic user data.",
        notes: "Prompt engineering is about consistency. Templates allow you to control the 'frame' of the conversation.",
        type: "Prompt Engineering",
        features: [
            { icon: "fas fa-brackets-curly", title: "Variables", desc: "Use {input} placeholders for dynamic data." },
            { icon: "fas fa-copy", title: "Reusability", desc: "Define a persona once, use it for 1000 tasks." }
        ],
        breakdown: [
            { code: "ChatPromptTemplate.from_template('...')", explanation: "Parses the string and identifiers '{variable}' syntax." },
            { code: "chain = prompt | llm", explanation: "Templates integrate perfectly with the pipe operator." }
        ],
        fullSource: `from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Tell me a funny joke about {topic}")
chain = prompt | llm
print(chain.invoke({"topic": "AI"}).content)`,
        output: "❓ Topic: AI\n🤖 AI: Why did the neural network go to the doctor? Because it had too many layers and was feeling a bit dense!",
        simulation: (input) => `🤖 Template Engine: Generating a professional response for [${input}]...\nAI: Done! Your custom prompt has been processed.`
    },
    {
        id: "03",
        title: "LCEL Chains",
        file: "03_lcel_chains.py",
        desc: "Composition over complexity. Use the Pipe (|) operator to build complex workflows like LEGO blocks.",
        notes: "LCEL is the secret sauce. It handles streaming, batching, and async out of the box.",
        type: "Composition",
        features: [
            { icon: "fas fa-link", title: "Pipe Operator", desc: "The | syntax makes code looks like a pipeline." },
            { icon: "fas fa-project-diagram", title: "Parallelism", desc: "Run multiple tasks at once with RunnableParallel." }
        ],
        breakdown: [
            { code: "chain = prompt | llm | parser", explanation: "Data flows through these steps sequentially." },
            { code: "RunnableParallel()", explanation: "Executes multiple branches of logic in parallel." }
        ],
        fullSource: `from langchain_core.runnables import RunnableParallel
# ... imports ...
pros_chain = prompt | llm
cons_chain = prompt | llm
parallel = RunnableParallel(pros=pros_chain, cons=cons_chain)
result = parallel.invoke({"topic": "LangChain"})`,
        output: "⛓️ Running Parallel Chain...\n✅ PROS: Modular, fast, community-driven.\n❌ CONS: Learning curve, rapid changes.",
        simulation: (input) => `⛓️ Workflow Pipeline: Processing "${input}" through parallel nodes...\nBranch 1 (Pros): Optimized.\nBranch 2 (Cons): Minimum overhead.`
    },
    {
        id: "04",
        title: "Output Parsers",
        file: "04_output_parsers.py",
        desc: "Convert raw text into reliable Python objects. Get JSON, Lists, or Pydantic models every time.",
        notes: "LLMs are unpredictable, but your code shouldn't be. Parsers force the AI to follow a schema.",
        type: "Structured Data",
        features: [
            { icon: "fas fa-brackets-square", title: "JSON Parser", desc: "Ensure the AI returns valid JSON objects." },
            { icon: "fas fa-shield-check", title: "Pydantic", desc: "Strict type validation for production safety." }
        ],
        breakdown: [
            { code: "JsonOutputParser()", explanation: "Automatically parses AI text into a Python dictionary." },
            { code: "llm.with_structured_output()", explanation: "Forces the model to stick to a Pydantic schema." }
        ],
        fullSource: `from pydantic import BaseModel, Field
class User(BaseModel):
    name: str = Field(description="The user name")
    age: int = Field(description="The user age")

structured_llm = llm.with_structured_output(User)
user = structured_llm.invoke("Parthiban is 25 years old")`,
        output: "📝 Requesting JSON...\n✅ Parsed Output: { 'name': 'Parthiban', 'age': 25 }",
        simulation: (input) => `📝 Parser active. Validating input: "${input}"\n✅ Success! Converted raw text into a safe Python Object.`
    },
    {
        id: "05",
        title: "Chat History",
        file: "05_memory_chat_history.py",
        desc: "Build AI with memory. Track conversation history across multiple turns using specialized stores.",
        notes: "Standard LLMs forget everything. Memory allows the model to enter 'Conversation' mode.",
        type: "Context",
        features: [
            { icon: "fas fa-brain", title: "Memory", desc: "Stateless to stateful transformation." },
            { icon: "fas fa-history", title: "Persistence", desc: "Save history to databases or memory." }
        ],
        breakdown: [
            { code: "MessagesPlaceholder", explanation: "Injects previous history into the prompt dynamically." },
            { code: "RunnableWithMessageHistory", explanation: "The high-level manager for conversational state." }
        ],
        fullSource: `from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}
def get_history(sid): return store.get(sid, ChatMessageHistory())

# Wrap chain with history manager
chain_with_history = RunnableWithMessageHistory(chain, get_history)`,
        output: "🧑 User: I'm Parthiban.\n🤖 AI: Hello Parthiban!\n🧑 User: Who am I?\n🤖 AI: You are Parthiban.",
        simulation: (input) => `🧠 Memory Updated. Stored session data for: "${input}"\nAI: I will remember that during our next turn!`
    },
    {
        id: "06",
        title: "Tool Calling",
        file: "06_tools_tool_calling.py",
        desc: "Give your AI 'Skills'. Allow the model to execute real Python code to solve math, search web, or call APIs.",
        notes: "The @tool decorator builds a bridge between natural language and your custom Python functions.",
        type: "Agency",
        features: [
            { icon: "fas fa-tools", title: "Functional Tools", desc: "Expose your Python functions to the LLM." },
            { icon: "fas fa-bolt", title: "Dynamic Picking", desc: "The LLM decides which skill to use." }
        ],
        breakdown: [
            { code: "@tool", explanation: "Extracts metadata from your function for the LLM's brain." },
            { code: "llm.bind_tools(tools)", explanation: "Enables the LLM to trigger function calls when needed." }
        ],
        fullSource: `@tool
def calculate(expression: str):
    """Solve a math problem."""
    return eval(expression)

llm_with_tools = llm.bind_tools([calculate])
# LLM selects 'calculate' when it sees math`,
        output: "🧑 User: 2 + 5?\n🔧 calling: calculate({'expression': '2+5'})\n🤖 AI: The answer is 7.",
        simulation: (input) => `🔧 Detecting Intent... Input: "${input}"\n⚡ Triggering Tool: "calculate"\n📤 Result: 15.54 (Simulated)`
    },
    {
        id: "07",
        title: "ReAct Agents",
        file: "07_agents.py",
        desc: "Autonomous reasoning. Build agents that enter a loop: Think -> Act -> Observe -> Repeat.",
        notes: "Agents use LangGraph to manage complex loops and self-correction cycles.",
        type: "Intelligence",
        features: [
            { icon: "fas fa-sync", title: "Looping", desc: "The agent can try multiple times until successful." },
            { icon: "fas fa-route", title: "Autonomous Planning", desc: "Solves multi-step problems logic-first." }
        ],
        breakdown: [
            { code: "create_react_agent()", explanation: "Builds a graph that manages the Think-Act-Observe loop." },
            { code: "agent.invoke()", explanation: "Starts the autonomous execution process." }
        ],
        fullSource: `from langgraph.prebuilt import create_react_agent

tools = [search_web, calculate]
agent = create_react_agent(llm, tools)

print("Starting Agentic Loop...")
result = agent.invoke({"messages": [("human", "What is 15% of India's GDP?")]})`,
        output: "🚀 Agent Activated.\n🔍 Plan: Search GDP -> Calculate 15% -> Respond\n🤖 AI: India's GDP is $4.2T, so 15% is...",
        simulation: (input) => `🚀 Autonomous Agent engaged for: "${input}"\nStep 1: Reasoning...\nStep 2: Activating Tools...\n✅ Final Answer ready!`
    },
    {
        id: "08",
        title: "RAG Retrieval",
        file: "08_rag_retrieval.py",
        desc: "Ground the AI in your data. Implement Retrieval Augmented Generation using Vector Databases like FAISS.",
        notes: "RAG allows the AI to peek at your private PDFs or text files before answering, reducing hallucinations.",
        type: "Knowledge",
        features: [
            { icon: "fas fa-database", title: "Vector DB", desc: "FAISS index for high-speed semantic search." },
            { icon: "fas fa-search-plus", title: "Contextual RAG", desc: "Feed real snippets to the LLM." }
        ],
        breakdown: [
            { code: "FAISS.from_documents()", explanation: "Converts text into searchable mathematical vectors." },
            { code: "retriever | format_docs", explanation: "A mini-pipeline that provides filtered context." }
        ],
        fullSource: `from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

vectorstore = FAISS.from_documents(chunks, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | prompt | llm)`,
        output: "📁 Loading intro.txt...\n🔍 Query: 'When was LangGraph released?'\n🤖 AI: It was released in October 2025.",
        simulation: (input) => `🔍 Scanning Knowledge Base for: "${input}"\n📄 Found 3 relevant documents.\n🤖 Building factual answer... Done.`
    },
    {
        id: "09",
        title: "Final: Research Assistant",
        file: "09_mini_project_research_assistant.py",
        desc: "The Masterpiece. A complete AI product that researches, analyzes, and writes structured technical reports.",
        notes: "This combines every previous skill into an end-to-end industrial-grade AI product.",
        type: "Product",
        features: [
            { icon: "fas fa-microchip", title: "Full Orchestration", desc: "Memory + Tools + RAG in one sync." },
            { icon: "fas fa-file-invoice", title: "Pro Reports", desc: "Pydantic-guaranteed data structure." }
        ],
        breakdown: [
            { code: "class ResearchReport", explanation: "Defines the professional data format." },
            { code: "create_react_agent()", explanation: "Handles the conversational research loop." }
        ],
        fullSource: `class ResearchReport(BaseModel):
    summary: str
    key_points: List[str]

report_llm = llm.with_structured_output(ResearchReport)
# Full Agentic Loop + Research Tools + Final Structured Polish`,
        output: "🛠️ Initializing Sentinel-Assistant...\n🧪 Researching Topic...\n✅ Final Research Report Generated.",
        simulation: (input) => `🎓 Sentinel AI Researcher: Starting deep-dive into "${input}"...\n- Knowledge nodes consulted.\n- Comparison matrices built.\n📝 Report complete!`
    }
];

let activeModule = modules[0];
const navigator = document.getElementById('navigator');
const displayArea = document.getElementById('displayArea');
const placeholder = document.getElementById('contentPlaceholder');
const content = document.getElementById('actualContent');

// Initialize modules
modules.forEach(mod => {
    const card = document.createElement('div');
    card.className = 'module-card';
    card.innerHTML = `
        <span class="module-num">${mod.id}</span>
        <span class="module-title">${mod.title}</span>
    `;
    card.onclick = () => activateModuleHandler(mod, card);
    navigator.appendChild(card);
});

function activateModuleHandler(mod, element) {
    activeModule = mod;

    // UI Update
    document.querySelectorAll('.module-card').forEach(c => c.classList.remove('active'));
    element.classList.add('active');

    placeholder.style.display = 'none';
    content.style.display = 'block';

    // Reset Playground
    document.getElementById('playInput').value = "";
    document.getElementById('terminalText').innerText = "";

    // Content Update
    document.getElementById('moduleType').innerText = mod.type;
    document.getElementById('moduleTitle').innerText = mod.title;
    document.getElementById('moduleDesc').innerText = mod.desc;
    document.getElementById('moduleNotes').innerText = mod.notes;
    document.getElementById('sourceCodeArea').innerText = mod.fullSource;

    // Features
    const grid = document.getElementById('featureGrid');
    grid.innerHTML = mod.features.map(f => `
        <div class="feature-item">
            <i class="${f.icon}"></i>
            <h4>${f.title}</h4>
            <p>${f.desc}</p>
        </div>
    `).join('');

    // Code Breakdown
    const bList = document.getElementById('breakdownList');
    bList.innerHTML = mod.breakdown.map(b => `
        <div class="code-line-item">
            <code class="code-snippet">${b.code}</code>
            <div class="line-explanation">${b.explanation}</div>
        </div>
    `).join('');

    // Terminal Initial Typing Effect
    typeTerminal(mod.output);
}

async function executePlayground() {
    const userInput = document.getElementById('playInput').value;
    if (!userInput) return;

    const term = document.getElementById('terminalText');
    term.innerText = "⏳ Processing runtime request via Python Engine...";

    try {
        const response = await fetch('/api/playground', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ module_id: activeModule.id, input: userInput })
        });

        if (!response.ok) {
            throw new Error(`Backend Error ${response.status}`);
        }

        const result = await response.json();
        typeTerminal(result.output);

    } catch (e) {
        console.warn("⚠️ API Failed, falling back to local simulation: " + e.message);
        // Fallback to local simulation if python api isn't connected
        setTimeout(() => {
            const simResponse = activeModule.simulation(userInput);
            typeTerminal("[⚠ LOCAL SIMULATION] " + simResponse);
        }, 1200);
    }
}

function typeTerminal(text) {
    const term = document.getElementById('terminalText');
    term.innerText = '';
    let i = 0;

    function type() {
        if (i < text.length) {
            term.innerText += text.charAt(i);
            i++;
            setTimeout(type, 10);
        }
    }
    type();
}
