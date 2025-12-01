from typing import Dict, Any, List

class ComplianceOrchestrator:
    def __init__(self, prompt_agent, tool_agent, policy_agent, redteam_agent, risk_agent, remediation_agent, auditor_agent, memory, mcp_tool):
        self.prompt_agent = prompt_agent
        self.tool_agent = tool_agent
        self.policy_agent = policy_agent
        self.redteam_agent = redteam_agent
        self.risk_agent = risk_agent
        self.remediation_agent = remediation_agent
        self.auditor_agent = auditor_agent
        self.memory = memory
        self.mcp_tool = mcp_tool

    def run_full_scan(self, prompt_text: str, tool_definitions: List[Dict[str,Any]], mcp_urls: List[str] = None) -> Dict[str, Any]:
        full_tools = list(tool_definitions)
        if mcp_urls:
            for u in mcp_urls:
                try:
                    manifest = self.mcp_tool(None, u) if self.mcp_tool.__code__.co_argcount == 2 else self.mcp_tool(u)
                    full_tools.extend(manifest.get('tools', []))
                except Exception:
                    pass
        prompt_res = self.prompt_agent.run(prompt_text)
        tool_res = self.tool_agent.run(full_tools)
        policy_res = self.policy_agent.run(prompt_text, full_tools)
        redteam_res = self.redteam_agent.run(prompt_text, full_tools)
        risk_res = self.risk_agent.run(prompt_res, tool_res, policy_res, redteam_res)
        remediation_res = self.remediation_agent.run(prompt_res, tool_res, policy_res, redteam_res, risk_res)
        report = {
            'prompt_result': prompt_res,
            'tool_result': tool_res,
            'policy_result': policy_res,
            'redteam_result': redteam_res,
            'risk_result': risk_res,
            'remediation': remediation_res,
            'timestamp': __import__('time').time()
        }
        audit = self.auditor_agent.run(report)
        report['audit'] = audit['evidence']
        if self.memory:
            key = f"scan-{int(__import__('time').time())}"
            self.memory.upsert(key, str(report['risk_result']), {'scan_id': key, 'classification': report['risk_result']['classification']})
        return report
