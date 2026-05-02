from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from agent.models import AgentRequest
from agent.orchestrator import route_intent

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(title="Swiggy Smart Agent", version="1.0.0")

# CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend directory to serve static files
if FRONTEND_DIR.exists():
    app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return HTMLResponse(content=index_path.read_text(encoding="utf-8"), status_code=200)
    return HTMLResponse(content="Frontend not found.", status_code=404)


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": app.version}

@app.post("/agent")
async def run_agent(payload: AgentRequest):
    context = payload.model_dump(exclude={"input"})
    response = route_intent(payload.input, context=context)
    return JSONResponse(content=response)

