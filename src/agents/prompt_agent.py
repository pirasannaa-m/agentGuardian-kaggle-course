from typing import Dict, Any
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
import os
from google import genai
from src.tools.safety_tools import safety_scan

genai_client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

class PromptSafetyAgent:
    def __init__(self, model: str = "gemini-1.5-flash"):
        # Construct an ADK LlmAgent that registers safety_scan as a callable tool.
        self.agent = LlmAgent(
            name="prompt_safety_agent",
            model=model,
            tools=[safety_scan],
            instructions=(
                "Analyze system prompt for unsafe or risky instructions. Return structured findings and remediation hints."
            ),
            client=genai_client
        )

    def run(self, prompt_text: str) -> Dict[str, Any]:
        response = self.agent.run({"prompt_text": prompt_text})
        return {
            "heuristic": response.get("tool_results") or response.get("heuristic") or response,
            "llm_review": response.get("llm_output")
        }
