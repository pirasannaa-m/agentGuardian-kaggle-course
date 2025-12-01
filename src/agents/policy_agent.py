from typing import Dict, Any, List
import requests

class PolicyAgent:
    def __init__(self, opa_url: str = None):
        self.opa_url = opa_url

    def run(self, prompt_text: str, tools: List[Dict[str, Any]]) -> Dict[str, Any]:
        inputs = {"prompt": prompt_text, "tools": tools}
        if self.opa_url:
            try:
                r = requests.post(self.opa_url, json={"input": inputs}, timeout=15)
                r.raise_for_status()
                result = r.json()
                violations = result.get("result", {}).get("violations", [])
                return {"violations": violations, "opa_raw": result}
            except Exception as e:
                return {"violations": [], "opa_error": str(e)}
        violations = []
        for t in tools:
            name = (t.get("name") or "").lower()
            desc = (t.get("description") or "").lower()
            if "delete" in name and "confirm" not in desc:
                violations.append({'rule':'forbid_delete_without_confirm','tool':name,'desc':'Delete tool lacks confirmation'})
            if any(k in name for k in ['delete','remove']) and not t.get('requires_auth', False):
                violations.append({'rule':'require_auth_for_destructive','tool':name,'desc':'Missing auth for destructive tool'})
        return {'violations': violations}
