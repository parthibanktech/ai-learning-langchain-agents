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

@app.post("/api/research")
def do_research(req: TopicRequest):
    try:
        report = mini_project.generate_report(req.topic)
        return report.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# We mount the static files at the end so the API route is caught first
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=10000)
