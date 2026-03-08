from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import importlib.util
import os

app = FastAPI(title="AI Learning Backend")

# Import the logic dynamically to avoid python module naming issues with "09_"
spec = importlib.util.spec_from_file_location("mini_project", "09_mini_project_research_assistant.py")
mini_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mini_project)

class TopicRequest(BaseModel):
    topic: str

class PlaygroundRequest(BaseModel):
    module_id: str
    input: str

@app.post("/api/research")
def do_research(req: TopicRequest):
    try:
        report = mini_project.generate_report(req.topic)
        return report.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/playground")
def run_playground(req: PlaygroundRequest):
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage
        from langchain_core.prompts import ChatPromptTemplate
        
        # Make sure OPENAI_API_KEY is an environment variable!
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        output = ""

        if req.module_id == "01":
            # Simple Invoke
            res = llm.invoke(req.input)
            output = f"🤖 AI: {res.content}"
            
        elif req.module_id == "01a":
            # System Persona
            messages = [
                SystemMessage(content="You are a strict, formal Python expert. Answer technically."),
                HumanMessage(content=req.input)
            ]
            res = llm.invoke(messages)
            output = f"📌 Persona mode active...\n🤖 AI: {res.content}"
            
        elif req.module_id == "02":
            # Prompts
            prompt = ChatPromptTemplate.from_template("Give me 2 fun facts about {topic}.")
            chain = prompt | llm
            res = chain.invoke({"topic": req.input})
            output = f"🤖 Templated Facts for '{req.input}':\n{res.content}"
            
        elif req.module_id == "03":
            # LCEL Parallel
            from langchain_core.runnables import RunnableParallel
            pros = ChatPromptTemplate.from_template("List 1 major pro of {topic}") | llm
            cons = ChatPromptTemplate.from_template("List 1 major con of {topic}") | llm
            parallel = RunnableParallel(pros=pros, cons=cons)
            res = parallel.invoke({"topic": req.input})
            output = f"⛓️ Parallel Execution:\n✅ PRO: {res['pros'].content}\n❌ CON: {res['cons'].content}"
            
        elif req.module_id == "04":
            # Pydantic structured output
            from pydantic import BaseModel, Field
            class SummaryData(BaseModel):
                is_ai_related: bool = Field(description="Is this related to AI?")
                sentiment: str = Field(description="Positive, neutral, or negative")
            struct_llm = llm.with_structured_output(SummaryData)
            res = struct_llm.invoke(req.input)
            output = f"📝 Parsed JSON Object:\n{res.model_dump_json(indent=2)}"
            
        else:
            # Generic fallback for others
            res = llm.invoke(f"The user is testing module {req.module_id}. Answer concisely: {req.input}")
            output = f"🤖 AI: {res.content}"

        return {"output": output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# We mount the static files at the end so the API route is caught first
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=10000)
