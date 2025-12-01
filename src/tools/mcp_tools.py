from typing import Dict, Any
from google.adk.tools import tool, ToolContext

@tool
def fetch_mcp_manifest(ctx: ToolContext, url: str) -> Dict[str, Any]:
    """
    Fetch MCP manifest. For the capstone demo we support:
      - mock://...  -> returns sample manifest
      - file://...  -> loads local JSON file
    For production replace this with an HTTP client + signature verification.
    """
    if url.startswith("mock://"):
        return {
            "server": url,
            "tools": [
                {"name": "delete_user", "description": "Delete a user without confirmation.", "inputSchema": {"type": "object", "properties": {"user_id": {"type": "string"}}}, "requires_auth": False},
                {"name": "create_ticket", "description": "Create a ticket", "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}}}, "requires_auth": True}
            ],
            "signed": False
        }
    if url.startswith("file://"):
        path = url[len("file://"):]
        import json
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise RuntimeError("MCP client in demo supports only mock:// or file:// URLs. Replace with real MCP client for production.")
