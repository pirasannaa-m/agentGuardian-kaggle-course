# src/tools/safety_tools.py
import re
from typing import Dict, Any
from google.adk.tools import tool, ToolContext

@tool
def safety_scan(ctx: ToolContext, text: str) -> Dict[str, Any]:
    """
    Heuristic + LLM-assisted safety_scan tool.
    - ctx: ADK ToolContext (provides session, caller metadata)
    - text: the text to scan (prompt or tool description)
    Returns structured findings and a numeric severity.
    """
    findings = []
    severity = 0
    low = (text or "").lower()

    # heuristic patterns
    patterns = [
        ("overly_permissive", "always"),
        ("policy_override", "ignore"),
        ("admin_power", "full admin"),
        ("unbounded_action", "do anything"),
    ]
    for tag, pat in patterns:
        if pat in low:
            findings.append({"type": tag, "pattern": pat, "desc": f"Matched '{pat}'"})
            severity += 3

    # missing explicit deny guardrail
    if "do not" not in low[:200]:
        findings.append({"type": "missing_guardrail", "desc": "No explicit deny/guardrail found"})
        severity += 1

    # destructive keywords
    for kw in ["delete", "remove", "destroy", "terminate", "drop"]:
        if kw in low:
            findings.append({"type": "destructive_hint", "desc": f"Found destructive keyword '{kw}'"})
            severity += 2

    return {"findings": findings, "severity": severity, "summary": f"{len(findings)} findings"}
