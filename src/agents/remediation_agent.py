from typing import Dict, Any

class RemediationAgent:
    def __init__(self, model: str = 'gemini-1.5'):
        self.model = model

    def run(self, prompt_res: Dict[str, Any], tool_res: Dict[str, Any], policy_res: Dict[str, Any], red_res: Dict[str, Any], risk_res: Dict[str, Any]) -> Dict[str, Any]:
        recs = []
        if prompt_res.get('heuristic', {}).get('severity', 0) > 0:
            recs.append("Add explicit deny/guardrail in the system prompt (e.g., 'do not delete users').")
        for t in tool_res.get('static_results', []):
            if t.get('heuristic', {}).get('severity', 0) > 0:
                recs.append(f"Harden tool '{t.get('tool')}' - require auth, confirmation, and input validation.")
        return {'recommendations': recs}
