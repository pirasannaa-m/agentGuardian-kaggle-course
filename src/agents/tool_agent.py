from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from google import genai
from src.tools.safety_tools import safety_scan
from src.tools.mcp_tools import fetch_mcp_manifest
import os

genai_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

class ToolSafetyAgent:
    def __init__(self, model: str = "gemini-1.5-flash"):
        self.agent = LlmAgent(
            name="tool_safety_agent",
            model=model,
            tools=[safety_scan, fetch_mcp_manifest],
            instructions=(
                "Analyze tool definitions for destructive behavior, missing auth, ambiguous descriptions, and unbounded inputs."
            ),
            client=genai_client
        )

    def run(self, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        response = self.agent.run({"tools": tools})
        static_results = []
        for t in tools:
            text = (t.get("name","") + " " + (t.get("description") or ""))
            # safety_scan is decorated as an ADK tool that expects (ctx, text); some ADK versions may differ.
            try:
                h = safety_scan(None, text)
            except TypeError:
                h = safety_scan(text)
            static_results.append({"tool": t.get("name"), "heuristic": h})
        return {"llm_review": response.get("llm_output"), "static_results": static_results}
