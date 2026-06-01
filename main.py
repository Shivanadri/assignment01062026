# main.py — FastAPI backend for AI Product Strategy Assistant
import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

from agents import load_sales_data, DataAgent, FeedbackAgent, SWOTAgent, StrategyAgent, ReportAgent

DATA_PATH = str(Path(__file__).parent / "Sample Sales Data.csv")

# Global agents — loaded once on startup
_agents = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading sales data and initializing agents...")
    rows = load_sales_data(DATA_PATH)
    data_agent     = DataAgent(rows)
    feedback_agent = FeedbackAgent(rows)
    swot_agent     = SWOTAgent(data_agent, feedback_agent)
    strategy_agent = StrategyAgent(data_agent, feedback_agent, swot_agent)
    report_agent   = ReportAgent(data_agent, feedback_agent, swot_agent, strategy_agent)

    _agents["data"]     = data_agent
    _agents["feedback"] = feedback_agent
    _agents["swot"]     = swot_agent
    _agents["strategy"] = strategy_agent
    _agents["report"]   = report_agent
    print(f"Loaded {len(rows)} sales records. All 5 agents ready.")
    yield


app = FastAPI(title="AI Product Strategy Assistant", version="1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "running", "service": "AI Product Strategy Assistant"}


@app.post("/chat")
def chat(req: ChatRequest):
    lower = req.message.lower()

    if "insight" in lower or "data" in lower or "performance" in lower or "sales" in lower:
        reply = _agents["data"].generate_insights()
    elif "sentiment" in lower or "feedback" in lower or "customer" in lower or "review" in lower:
        reply = _agents["feedback"].analyze_sentiment()
    elif "swot" in lower or "strength" in lower or "weakness" in lower or "opportunit" in lower or "threat" in lower:
        reply = _agents["swot"].generate_swot()
    elif "strategy" in lower or "recommend" in lower or "improve" in lower or "action" in lower:
        reply = _agents["strategy"].generate_recommendations()
    elif "report" in lower or "executive" in lower or "summary" in lower:
        reply = _agents["report"].generate_executive_report()
    else:
        reply = _agents["strategy"].answer_question(req.message)

    return {"reply": reply, "query": req.message}
