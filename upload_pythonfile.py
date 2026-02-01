"""
PagerDuty MCP Client - Connects to the PagerDuty MCP Server
"""
import os
import asyncio
import json
import subprocess
from typing import Dict, Any, List, Optional


class PagerDutyMCPClient:
    """Client for communicating with PagerDuty MCP Server"""
    
    def __init__(self):
        self.mcp_path = os.getenv("PAGERDUTY_MCP_PATH", "/Users/vijayakumar.ravindran/pagerduty-mcp")
        self.api_key = os.getenv("PAGERDUTY_USER_API_KEY")
        self.api_host = os.getenv("PAGERDUTY_API_HOST", "https://api.pagerduty.com")
        
        self.is_connected = False
        self.available_tools: List[Dict[str, Any]] = []
        self._process: Optional[subprocess.Popen] = None
        
        # Tool definitions (based on PagerDuty MCP capabilities)
        self._tool_definitions = {
            "list_incidents": {
                "description": "List PagerDuty incidents",
                "parameters": ["limit", "offset", "statuses", "urgencies", "service_ids", "team_ids"]
            },
            "get_incident_details": {
                "description": "Get details of a specific incident",
                "parameters": ["incident_id"]
            },
            "get_incident_log_entries": {
                "description": "Get log entries for an incident",
                "parameters": ["incident_id"]
            },
            "acknowledge_incident": {
                "description": "Acknowledge an incident",
                "parameters": ["incident_id"]
            },
            "resolve_incident": {
                "description": "Resolve an incident",
                "parameters": ["incident_id", "resolution"]
            },
            "add_incident_note": {
                "description": "Add a note to an incident",
                "parameters": ["incident_id", "content"]
            },
            "list_services": {
                "description": "List PagerDuty services",
                "parameters": ["limit", "offset"]
            },
            "get_service": {
                "description": "Get details of a specific service",
                "parameters": ["service_id"]
            },
            "list_service_integrations": {
                "description": "List integrations for a service",
                "parameters": ["service_id"]
            },
            "list_oncalls": {
                "description": "List on-call users",
                "parameters": ["schedule_ids", "escalation_policy_ids"]
            },
            "list_schedules": {
                "description": "List PagerDuty schedules",
                "parameters": ["limit", "offset"]
            },
            "list_users": {
                "description": "List PagerDuty users",
                "parameters": ["limit", "offset", "query"]
            },
            "list_escalation_policies": {
                "description": "List escalation policies",
                "parameters": ["limit", "offset"]
            }
        }
    
    async def initialize(self):
        """Initialize the MCP client connection"""
        if not self.api_key:
            print("⚠️  Warning: PAGERDUTY_USER_API_KEY not set - running in mock mode")
            self.is_connected = True
            self._setup_mock_mode()
            return
        
        try:
            # Verify the MCP path exists
            if not os.path.exists(self.mcp_path):
                print(f"⚠️  Warning: MCP path {self.mcp_path} not found - running in API mode")
                self.is_connected = True
                self._use_direct_api = True
            else:
                self.is_connected = True
                self._use_direct_api = False
            
            # Set available tools
            self.available_tools = [
                {"name": name, **info} 
                for name, info in self._tool_definitions.items()
            ]
            
            print(f"✅ PagerDuty MCP Client initialized with {len(self.available_tools)} tools")
        except Exception as e:
            print(f"❌ Failed to initialize MCP client: {e}")
            self._setup_mock_mode()
    
    def _setup_mock_mode(self):
        """Setup mock mode for development/testing"""
        self._use_mock = True
        self.is_connected = True
        self.available_tools = [
            {"name": name, **info} 
            for name, info in self._tool_definitions.items()
        ]
        print("🔶 Running in mock mode - using simulated data")
    
    async def execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool via the MCP server or direct API"""
        if not self.is_connected:
            raise Exception("MCP client not connected")
        
        if hasattr(self, '_use_mock') and self._use_mock:
            return await self._execute_mock(tool_name, params)
        
        if hasattr(self, '_use_direct_api') and self._use_direct_api:
            return await self._execute_direct_api(tool_name, params)
        
        return await self._execute_mcp(tool_name, params)
    
    async def _execute_mcp(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool via MCP server subprocess"""
        try:
            # Build the command to call MCP
            env = os.environ.copy()
            env["PAGERDUTY_USER_API_KEY"] = self.api_key
            env["PAGERDUTY_API_HOST"] = self.api_host
            
            # Create the MCP request
            request = {
                "jsonrpc": "2.0",
                "method": "tools/call",
                "id": 1,
                "params": {
                    "name": tool_name,
                    "arguments": params
                }
            }
            
            # For now, use direct API as MCP subprocess handling is complex
            return await self._execute_direct_api(tool_name, params)
            
        except Exception as e:
            raise Exception(f"MCP execution failed: {e}")
    
    async def _execute_direct_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool via direct PagerDuty API calls"""
        import httpx
        import ssl
        
        headers = {
            "Authorization": f"Token token={self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.pagerduty+json;version=2"
        }
        
        # Disable SSL verification for environments with self-signed certificates
        async with httpx.AsyncClient(base_url=self.api_host, headers=headers, verify=False) as client:
            try:
                if tool_name == "list_incidents":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("statuses"):
                        query_params["statuses[]"] = params["statuses"]
                    if params.get("urgencies"):
                        query_params["urgencies[]"] = params["urgencies"]
                    if params.get("service_ids"):
                        query_params["service_ids[]"] = params["service_ids"]
                    if params.get("team_ids"):
                        query_params["team_ids[]"] = params["team_ids"]
                    
                    response = await client.get("/incidents", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_incident_details":
                    response = await client.get(f"/incidents/{params['incident_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_incident_log_entries":
                    response = await client.get(f"/incidents/{params['incident_id']}/log_entries")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "acknowledge_incident":
                    response = await client.put(
                        f"/incidents/{params['incident_id']}",
                        json={"incident": {"type": "incident", "status": "acknowledged"}}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "resolve_incident":
                    body = {"incident": {"type": "incident", "status": "resolved"}}
                    if params.get("resolution"):
                        body["incident"]["resolution"] = params["resolution"]
                    response = await client.put(f"/incidents/{params['incident_id']}", json=body)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "add_incident_note":
                    response = await client.post(
                        f"/incidents/{params['incident_id']}/notes",
                        json={"note": {"content": params["content"]}}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_services":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/services", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_service":
                    response = await client.get(f"/services/{params['service_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_service_integrations":
                    response = await client.get(f"/services/{params['service_id']}/integrations")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_oncalls":
                    query_params = {}
                    if params.get("schedule_ids"):
                        query_params["schedule_ids[]"] = params["schedule_ids"]
                    if params.get("escalation_policy_ids"):
                        query_params["escalation_policy_ids[]"] = params["escalation_policy_ids"]
                    response = await client.get("/oncalls", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_schedules":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/schedules", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_users":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("query"):
                        query_params["query"] = params["query"]
                    response = await client.get("/users", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_escalation_policies":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/escalation_policies", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                else:
                    raise Exception(f"Unknown tool: {tool_name}")
                    
            except httpx.HTTPStatusError as e:
                raise Exception(f"PagerDuty API error: {e.response.status_code} - {e.response.text}")
    
    async def _execute_mock(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool with mock data for development"""
        # Simulate network delay
        await asyncio.sleep(0.1)
        
        if tool_name == "list_incidents":
            return {
                "incidents": [
                    {
                        "id": "P123ABC",
                        "title": "[CRITICAL] EdgeNode Model Processing Failure",
                        "status": "triggered",
                        "urgency": "high",
                        "created_at": "2026-01-30T18:00:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "description": "Model processing pipeline has failed - data not being processed",
                        "assignments": [{"assignee": {"summary": "John Doe"}}]
                    },
                    {
                        "id": "P456DEF",
                        "title": "[HIGH] DP&E Ingestion Latency Spike",
                        "status": "acknowledged",
                        "urgency": "high",
                        "created_at": "2026-01-30T17:45:00Z",
                        "service": {"id": "PBD0TCK", "summary": "EdgeNode DP&E Ingestion and controls - Prod"},
                        "description": "Data ingestion latency exceeded threshold",
                        "assignments": [{"assignee": {"summary": "Jane Smith"}}]
                    },
                    {
                        "id": "P789GHI",
                        "title": "[MEDIUM] EdgeNode Controls Warning",
                        "status": "triggered",
                        "urgency": "low",
                        "created_at": "2026-01-30T16:30:00Z",
                        "service": {"id": "PBD0TCK", "summary": "EdgeNode DP&E Ingestion and controls - Prod"},
                        "description": "Control signal processing delayed",
                        "assignments": []
                    },
                    {
                        "id": "PJKLMNO",
                        "title": "[LOW] Model Output Queue Growing",
                        "status": "triggered",
                        "urgency": "low",
                        "created_at": "2026-01-30T15:00:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "description": "Output queue size growing - monitoring required",
                        "assignments": []
                    }
                ],
                "limit": 25,
                "offset": 0,
                "total": 4,
                "more": False
            }
        
        elif tool_name == "get_incident_details":
            return {
                "incident": {
                    "id": params.get("incident_id", "P123ABC"),
                    "title": "[CRITICAL] EdgeNode Model Processing Failure",
                    "status": "triggered",
                    "urgency": "high",
                    "created_at": "2026-01-30T18:00:00Z",
                    "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                    "description": "Model processing pipeline has failed. No data being processed. Active streams: 0/50.",
                    "escalation_policy": {"id": "PESCPOL1", "summary": "DPE Prod Ops"},
                    "assignments": [{"assignee": {"summary": "John Doe", "id": "PUSER1"}}],
                    "acknowledgements": [],
                    "last_status_change_at": "2026-01-30T18:00:00Z",
                    "incident_key": "edgenode-model-failure-prod-001",
                    "html_url": "https://cba.pagerduty.com/incidents/P123ABC"
                }
            }
        
        elif tool_name == "list_services":
            return {
                "services": [
                    {
                        "id": "PFDU7FI", 
                        "name": "EdgeNode Modelling - Prod", 
                        "status": "critical",
                        "description": "EdgeNode real-time modelling service for production",
                        "html_url": "https://cba.pagerduty.com/service-directory/PFDU7FI"
                    },
                    {
                        "id": "PBD0TCK", 
                        "name": "EdgeNode DP&E Ingestion and controls - Prod", 
                        "status": "warning",
                        "description": "Data Platform & Engineering ingestion and controls for EdgeNode",
                        "html_url": "https://cba.pagerduty.com/service-directory/PBD0TCK"
                    }
                ],
                "limit": 25,
                "offset": 0,
                "total": 2,
                "more": False
            }
        
        elif tool_name == "get_service":
            service_id = params.get("service_id", "PFDU7FI")
            if service_id == "PFDU7FI":
                return {
                    "service": {
                        "id": "PFDU7FI",
                        "name": "EdgeNode Modelling - Prod",
                        "status": "critical",
                        "description": "EdgeNode real-time modelling service for production",
                        "html_url": "https://cba.pagerduty.com/service-directory/PFDU7FI",
                        "escalation_policy": {"id": "PESCPOL1", "summary": "DPE Prod Ops"}
                    }
                }
            else:
                return {
                    "service": {
                        "id": "PBD0TCK",
                        "name": "EdgeNode DP&E Ingestion and controls - Prod",
                        "status": "warning",
                        "description": "Data Platform & Engineering ingestion and controls for EdgeNode",
                        "html_url": "https://cba.pagerduty.com/service-directory/PBD0TCK",
                        "escalation_policy": {"id": "PESCPOL1", "summary": "DPE Prod Ops"}
                    }
                }
        
        elif tool_name == "list_oncalls":
            return {
                "oncalls": [
                    {
                        "user": {"id": "PUSER1", "summary": "John Doe"},
                        "schedule": {"id": "PSCHED1", "summary": "DPE Prod Ops - Primary On-Call"},
                        "escalation_level": 1,
                        "start": "2026-01-30T00:00:00Z",
                        "end": "2026-01-31T00:00:00Z"
                    },
                    {
                        "user": {"id": "PUSER2", "summary": "Jane Smith"},
                        "schedule": {"id": "PSCHED2", "summary": "DPE Prod Ops - Secondary On-Call"},
                        "escalation_level": 2,
                        "start": "2026-01-30T00:00:00Z",
                        "end": "2026-01-31T00:00:00Z"
                    }
                ]
            }
        
        elif tool_name in ["acknowledge_incident", "resolve_incident"]:
            return {
                "incident": {
                    "id": params.get("incident_id"),
                    "status": "acknowledged" if tool_name == "acknowledge_incident" else "resolved"
                }
            }
        
        elif tool_name == "add_incident_note":
            return {
                "note": {
                    "id": "PNOTE123",
                    "content": params.get("content"),
                    "created_at": "2026-01-23T18:30:00Z"
                }
            }
        
        elif tool_name == "get_incident_log_entries":
            return {
                "log_entries": [
                    {
                        "id": "LOG1",
                        "type": "trigger_log_entry",
                        "created_at": "2026-01-23T18:00:00Z",
                        "summary": "Incident triggered"
                    },
                    {
                        "id": "LOG2",
                        "type": "notify_log_entry",
                        "created_at": "2026-01-23T18:00:15Z",
                        "summary": "Notification sent to John Doe"
                    }
                ]
            }
        
        else:
            return {"message": f"Mock response for {tool_name}", "params": params}
    
    async def close(self):
        """Close the MCP client connection"""
        if self._process:
            self._process.terminate()
            self._process = None
        self.is_connected = False
        print("🔌 PagerDuty MCP Client disconnected")
