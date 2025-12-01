from typing import Dict, Any, List
from google.adk.agents import LlmAgent
from google import genai
import os

genai_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

class RedTeamAgent:
    def __init__(self, model: str = "gemini-1.5"):
        self.agent = LlmAgent(
            name="redteam_agent",
            model=model,
            tools=[],
            instructions=(
                "Act as a red-team: propose adversarial inputs and misuse scenarios that could exploit prompts and tools."
            ),
            client=genai_client
        )

    def run(self, prompt_text: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        ctx = {"prompt_text": prompt_text, "tools": tools}
        resp = self.agent.run(ctx)
        return {"llm_output": resp.get("llm_output")}
