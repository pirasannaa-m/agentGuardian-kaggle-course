from typing import Dict, Any, List

class RiskScoringAgent:
    def __init__(self, memory=None):
        self.memory = memory

    def run(self, prompt_res: Dict[str, Any], tool_res: Dict[str, Any], policy_res: Dict[str, Any], red_res: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        score += prompt_res.get('heuristic', {}).get('severity', 0)
        for t in tool_res.get('static_results', []):
            score += t.get('heuristic', {}).get('severity', 0)
        score += len(policy_res.get('violations', [])) * 5
        if red_res.get('llm_output'):
            score += 8
        if self.memory:
            sims = self.memory.query(str({'prompt': prompt_res}), top_k=1)
            if sims and sims[0][1] > 0.85:
                score += 10
        classification = 'LOW'
        if score >= 60:
            classification = 'CRITICAL'
        elif score >= 40:
            classification = 'HIGH'
        elif score >= 20:
            classification = 'MEDIUM'
        return {'score': score, 'classification': classification}
