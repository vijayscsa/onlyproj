"""
AIOps Agentic UI - Python Agent Service
FastAPI application with LangChain agent and PagerDuty MCP integration
"""
import os
import uuid
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from agents.aiops_agent import AIOpsAgent
from agents.workflows import TriageWorkflow
from mcp.pagerduty_client import PagerDutyMCPClient
from config.services_config import (
    ALLOWED_SERVICES,
    ALLOWED_TEAM,
    get_allowed_service_ids,
    get_allowed_service_names,
    get_team_id,
    is_service_id_allowed
)

load_dotenv()

# Global instances
agent: Optional[AIOpsAgent] = None
mcp_client: Optional[PagerDutyMCPClient] = None
triage_workflow: Optional[TriageWorkflow] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    global agent, mcp_client, triage_workflow
    
    print("🚀 Starting AIOps Python Agent Service...")
    
    # Initialize MCP client
    mcp_client = PagerDutyMCPClient()
    await mcp_client.initialize()
    
    # Initialize agent
    agent = AIOpsAgent(mcp_client=mcp_client)
    
    # Initialize workflow
    triage_workflow = TriageWorkflow(agent=agent)
    
    print("✅ All components initialized successfully")
    
    yield
    
    # Cleanup
    print("🛑 Shutting down AIOps Python Agent Service...")
    if mcp_client:
        await mcp_client.close()


app = FastAPI(
    title="AIOps Agentic UI - Python Agent",
    description="AI-powered incident management and analysis service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:8005", "http://localhost:8006", "http://127.0.0.1:3001", "http://127.0.0.1:8006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Request/Response Models ==============

class ChatRequest(BaseModel):
    message: str
    conversationId: Optional[str] = None
    clientId: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversationId: str
    toolsUsed: List[str] = []
    timestamp: str


class QueryRequest(BaseModel):
    query: str
    context: Dict[str, Any] = {}


class TriageRequest(BaseModel):
    incidentIds: List[str]


class IncidentNoteRequest(BaseModel):
    content: str


class ResolveRequest(BaseModel):
    resolution: Optional[str] = None


# ============== Health Endpoints ==============

@app.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "aiops-python-agent",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "agent": "initialized" if agent else "not_initialized",
            "mcp_client": "connected" if mcp_client and mcp_client.is_connected else "disconnected"
        }
    }


@app.get("/health/pagerduty")
async def pagerduty_health():
    """Check PagerDuty connectivity"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        # Try to list services as connectivity check
        result = await mcp_client.execute_tool("list_services", {"limit": 1})
        return {
            "status": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


# ============== Chat Endpoints ==============

@app.post("/api/chat", response_model=ChatResponse)
@app.post("/api/agents/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI agent"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    conversation_id = request.conversationId or str(uuid.uuid4())
    
    try:
        result = await agent.chat(
            message=request.message,
            conversation_id=conversation_id
        )
        
        return ChatResponse(
            response=result["response"],
            conversationId=conversation_id,
            toolsUsed=result.get("tools_used", []),
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
@app.post("/api/agents/query")
async def execute_query(request: QueryRequest):
    """Execute a specific AIOps query"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        result = await agent.execute_query(
            query=request.query,
            context=request.context
        )
        return {
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tools")
@app.get("/api/agents/tools")
async def list_tools():
    """List available agent tools"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    return {
        "tools": mcp_client.available_tools,
        "timestamp": datetime.utcnow().isoformat()
    }


# ============== Incident Endpoints ==============

@app.get("/api/incidents")
async def list_incidents(
    status: Optional[str] = None,
    urgency: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    since: Optional[str] = None,
    open_only: bool = False,
    filter_services: bool = False
):
    """List incidents from PagerDuty - filtered by team
    
    Args:
        status: Filter by specific status (triggered, acknowledged, resolved)
        urgency: Filter by urgency (high, low)
        limit: Number of incidents to return (default 100)
        offset: Pagination offset
        since: ISO8601 date string to filter incidents created after this date
        open_only: If True, only return triggered and acknowledged incidents
        filter_services: If True, also filter by specific allowed service IDs
    """
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        params = {
            "limit": limit, 
            "offset": offset,
            "team_ids": [get_team_id()],
            "sort_by": "created_at:desc"  # Sort by most recent first
        }
        
        # Optionally filter by specific service IDs
        if filter_services:
            allowed_service_ids = get_allowed_service_ids()
            params["service_ids"] = allowed_service_ids
        
        # Add since filter for date range
        if since:
            params["since"] = since
        
        # Filter by status
        if status:
            params["statuses"] = [status]
        elif open_only:
            # Only open (non-resolved) incidents
            params["statuses"] = ["triggered", "acknowledged"]
            
        if urgency:
            params["urgencies"] = [urgency]
        
        result = await mcp_client.execute_tool("list_incidents", params)
        return result
    except Exception as e:
        print(f"⚠️ Error in list_incidents: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def _safe_int(val, default=0):
    """Safely convert a value to int, returning default if None or invalid."""
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


@app.get("/api/incidents/stats/summary")
async def get_incident_stats():
    """Get incident statistics summary - filtered by team only.
    
    Uses the same parameter pattern as the working /api/incidents endpoint
    (team_ids only, no service_ids) to ensure compatibility.
    Each API call is independently wrapped so one failure doesn't break everything.
    
    IMPORTANT: PagerDuty API v2 may NOT return a 'total' field, or may return null.
    We must always count the incidents array directly to be safe.
    """
    try:
        if not mcp_client:
            raise HTTPException(status_code=503, detail="MCP client not initialized")
        
        team_id = get_team_id()
        now = datetime.utcnow()
        today_midnight_str = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
        
        triggered_total = 0
        acknowledged_total = 0
        resolved_today_count = 0
        high_urgency = 0
        low_urgency = 0
        
        # Fetch triggered incidents (same pattern as working /api/incidents)
        try:
            triggered_result = await mcp_client.execute_tool("list_incidents", {
                "statuses": ["triggered"], 
                "limit": 100,
                "team_ids": [team_id]
            })
            if triggered_result and isinstance(triggered_result, dict):
                triggered_list = triggered_result.get("incidents") or []
                # Always use len() as primary count — PagerDuty API v2 may omit 'total' or set it to null
                triggered_total = _safe_int(triggered_result.get("total"), len(triggered_list))
                high_urgency += len([i for i in triggered_list if i.get("urgency") == "high"])
                low_urgency += len([i for i in triggered_list if i.get("urgency") == "low"])
        except Exception as e:
            print(f"⚠️ Error fetching triggered incidents: {e}", flush=True)
        
        # Fetch acknowledged incidents
        try:
            acknowledged_result = await mcp_client.execute_tool("list_incidents", {
                "statuses": ["acknowledged"], 
                "limit": 100,
                "team_ids": [team_id]
            })
            if acknowledged_result and isinstance(acknowledged_result, dict):
                acknowledged_list = acknowledged_result.get("incidents") or []
                acknowledged_total = _safe_int(acknowledged_result.get("total"), len(acknowledged_list))
                high_urgency += len([i for i in acknowledged_list if i.get("urgency") == "high"])
                low_urgency += len([i for i in acknowledged_list if i.get("urgency") == "low"])
        except Exception as e:
            print(f"⚠️ Error fetching acknowledged incidents: {e}", flush=True)
        
        # Fetch resolved incidents (broader window, filter client-side)
        try:
            thirty_days_ago = (now - timedelta(days=30)).isoformat() + "Z"
            resolved_result = await mcp_client.execute_tool("list_incidents", {
                "statuses": ["resolved"], 
                "limit": 100,
                "team_ids": [team_id],
                "since": thirty_days_ago
            })
            if resolved_result and isinstance(resolved_result, dict):
                resolved_all = resolved_result.get("incidents") or []
                for inc in resolved_all:
                    status_changed = inc.get("last_status_change_at", "")
                    if status_changed and status_changed >= today_midnight_str:
                        resolved_today_count += 1
        except Exception as e:
            print(f"⚠️ Error fetching resolved incidents: {e}", flush=True)
        
        return {
            "triggered": triggered_total,
            "acknowledged": acknowledged_total,
            "resolved": resolved_today_count,
            "high_urgency": high_urgency,
            "low_urgency": low_urgency,
            "total_open": triggered_total + acknowledged_total,
            "timestamp": now.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"CRITICAL ERROR in get_incident_stats: {e}", flush=True)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Stats summary error: {str(e)}")


@app.get("/api/incidents/{incident_id}")
async def get_incident(incident_id: str):
    """Get enriched incident details with alerts, custom details, annotations, and notes.
    
    This endpoint returns the full PagerDuty incident data PLUS:
    - All alerts with their complete body (custom details, labels, annotations, firing info)
    - Incident notes
    - First trigger log entry for channel/integration info
    This matches what you see in the PagerDuty portal.
    """
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        # Fetch incident details, alerts, notes, and log entries in parallel
        import asyncio
        
        async def safe_execute(tool_name, params):
            """Execute a tool call safely, returning None on failure."""
            try:
                result = await mcp_client.execute_tool(tool_name, params)
                return result if isinstance(result, dict) else {}
            except Exception as e:
                print(f"⚠️ Error in {tool_name}: {e}", flush=True)
                return {}
        
        incident_task = safe_execute("get_incident_details", {"incident_id": incident_id})
        alerts_task = safe_execute("list_incident_alerts", {"incident_id": incident_id, "limit": 50})
        notes_task = safe_execute("get_incident_notes", {"incident_id": incident_id})
        log_task = safe_execute("get_incident_log_entries", {"incident_id": incident_id})
        
        results = await asyncio.gather(incident_task, alerts_task, notes_task, log_task)
        incident_data, alerts_data, notes_data, log_data = results
        
        incident = incident_data.get("incident") or incident_data or {}
        alerts = alerts_data.get("alerts") or []
        notes = notes_data.get("notes") or []
        log_entries = log_data.get("log_entries") or []
        
        # Enrich incident with alerts data (custom details, labels, annotations, runbook URLs)
        enriched_alerts = []
        for alert in alerts:
            enriched_alert = {
                "id": alert.get("id"),
                "status": alert.get("status"),
                "severity": alert.get("severity"),
                "summary": alert.get("summary"),
                "created_at": alert.get("created_at"),
                "html_url": alert.get("html_url"),
                "alert_key": alert.get("alert_key"),
                "suppressed": alert.get("suppressed", False),
            }
            
            # Extract full alert body with custom details
            body = alert.get("body") or {}
            if body:
                enriched_alert["body"] = body
                # Extract custom details specifically
                details = body.get("details") or body.get("cef_details") or {}
                if isinstance(details, dict):
                    enriched_alert["custom_details"] = details
                    # Extract known important fields
                    enriched_alert["labels"] = details.get("labels") or details.get("firing") or {}
                    enriched_alert["annotations"] = details.get("annotations") or {}
                    enriched_alert["source"] = details.get("source") or details.get("Source") or ""
                    enriched_alert["runbook_url"] = (
                        details.get("runbook_url") or 
                        (details.get("annotations") or {}).get("runbook_url") or 
                        ""
                    )
                    enriched_alert["description"] = (
                        details.get("description") or
                        (details.get("annotations") or {}).get("description") or
                        ""
                    )
                    enriched_alert["num_firing"] = details.get("num_firing")
                    enriched_alert["num_resolved"] = details.get("num_resolved")
                elif isinstance(details, str):
                    enriched_alert["custom_details"] = {"text": details}
            
            # Extract CEF (Common Event Format) details
            cef = alert.get("body", {}).get("cef_details") or {}
            if cef:
                enriched_alert["cef_details"] = cef
            
            enriched_alerts.append(enriched_alert)
        
        # Build the enriched response
        response = {
            "incident": incident,
            "alerts": enriched_alerts,
            "notes": notes,
            "log_entries": log_entries[:20],  # Last 20 log entries
            "alert_count": len(enriched_alerts),
            "note_count": len(notes),
        }
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/incidents/{incident_id}/alerts")
async def get_incident_alerts(incident_id: str):
    """Get all alerts for an incident with full body/custom details.
    
    Returns the complete alert data including labels, annotations,
    custom details, firing info, runbook URLs — everything shown in PagerDuty portal.
    """
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("list_incident_alerts", {
            "incident_id": incident_id,
            "limit": 100
        })
        return result if isinstance(result, dict) else {"alerts": []}
    except Exception as e:
        print(f"⚠️ Error fetching alerts for {incident_id}: {e}", flush=True)
        return {"alerts": []}


@app.get("/api/incidents/{incident_id}/log_entries")
async def get_incident_log(incident_id: str):
    """Get incident log entries"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("get_incident_log_entries", {"incident_id": incident_id})
        return result if isinstance(result, dict) else {"log_entries": []}
    except Exception as e:
        print(f"⚠️ Error fetching log entries for {incident_id}: {e}", flush=True)
        return {"log_entries": []}


@app.get("/api/incidents/{incident_id}/related")
async def get_related_incidents(incident_id: str):
    """Get related incidents for an incident.
    
    NOTE: PagerDuty's Related Incidents API requires AIOps add-on.
    Returns empty array gracefully if the feature is not available.
    """
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("get_related_incidents", {"incident_id": incident_id})
        return result if isinstance(result, dict) else {"related_incidents": []}
    except Exception as e:
        print(f"⚠️ Related incidents not available for {incident_id}: {e}", flush=True)
        # Return empty rather than 500 — this is an optional AIOps feature
        return {"related_incidents": []}


@app.get("/api/incidents/{incident_id}/past")
async def get_past_incidents(incident_id: str):
    """Get past incidents related to an incident.
    
    NOTE: PagerDuty's Past Incidents API requires AIOps add-on.
    Returns empty array gracefully if the feature is not available.
    """
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("get_past_incidents", {"incident_id": incident_id})
        return result if isinstance(result, dict) else {"past_incidents": []}
    except Exception as e:
        print(f"⚠️ Past incidents not available for {incident_id}: {e}", flush=True)
        # Return empty rather than 500 — this is an optional AIOps feature
        return {"past_incidents": []}


@app.post("/api/incidents/{incident_id}/responders")
async def add_responders(incident_id: str, responder_ids: list = None):
    """Add responders to an incident"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("add_responders", {
            "incident_id": incident_id,
            "responder_ids": responder_ids or []
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/incidents/{incident_id}/acknowledge")
async def acknowledge_incident(incident_id: str):
    """Acknowledge an incident"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("acknowledge_incident", {"incident_id": incident_id})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str, request: ResolveRequest):
    """Resolve an incident"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        params = {"incident_id": incident_id}
        if request.resolution:
            params["resolution"] = request.resolution
        
        result = await mcp_client.execute_tool("resolve_incident", params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/incidents/{incident_id}/notes")
async def add_incident_note(incident_id: str, request: IncidentNoteRequest):
    """Add a note to an incident"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        result = await mcp_client.execute_tool("add_incident_note", {
            "incident_id": incident_id,
            "content": request.content
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== Service Endpoints ==============

@app.get("/api/services")
async def list_services(limit: int = 25, offset: int = 0):
    """List services from PagerDuty - returns only allowed services"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    try:
        # Only return the allowed services
        allowed_service_ids = get_allowed_service_ids()
        services = []
        
        for service_id in allowed_service_ids:
            try:
                service_result = await mcp_client.execute_tool("get_service", {"service_id": service_id})
                if service_result.get("service"):
                    services.append(service_result["service"])
            except Exception as e:
                print(f"Warning: Could not fetch service {service_id}: {e}")
        
        return {
            "services": services,
            "limit": limit,
            "offset": offset,
            "total": len(services),
            "more": False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/services/{service_id}")
async def get_service(service_id: str):
    """Get service details - only for allowed services"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    # Validate service is allowed
    if not is_service_id_allowed(service_id):
        raise HTTPException(status_code=403, detail=f"Service {service_id} is not in the allowed services list")
    
    try:
        result = await mcp_client.execute_tool("get_service", {"service_id": service_id})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/services/{service_id}/integrations")
async def get_service_integrations(service_id: str):
    """Get service integrations - only for allowed services"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    # Validate service is allowed
    if not is_service_id_allowed(service_id):
        raise HTTPException(status_code=403, detail=f"Service {service_id} is not in the allowed services list")
    
    try:
        result = await mcp_client.execute_tool("list_service_integrations", {"service_id": service_id})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/services/{service_id}/incidents")
async def get_service_incidents(service_id: str, status: Optional[str] = None, limit: int = 25):
    """Get incidents for a service - only for allowed services"""
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP client not initialized")
    
    # Validate service is allowed
    if not is_service_id_allowed(service_id):
        raise HTTPException(status_code=403, detail=f"Service {service_id} is not in the allowed services list")
    
    try:
        params = {
            "service_ids": [service_id], 
            "limit": limit,
            "team_ids": [get_team_id()]
        }
        if status:
            params["statuses"] = [status]
        
        result = await mcp_client.execute_tool("list_incidents", params)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== Analysis Endpoints ==============

@app.post("/api/analyze/{incident_id}")
@app.post("/api/agents/analyze/{incident_id}")
async def analyze_incident(incident_id: str):
    """Analyze an incident using AI"""
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    try:
        # Use agent to analyze
        analysis = await agent.analyze_incident(incident_id)
        
        return {
            "incident_id": incident_id,
            "analysis": analysis,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/triage")
@app.post("/api/agents/triage")
async def triage_incidents(request: TriageRequest):
    """Get triage recommendations for incidents"""
    if not triage_workflow:
        raise HTTPException(status_code=503, detail="Triage workflow not initialized")
    
    try:
        result = await triage_workflow.run(request.incidentIds)
        return {
            "recommendations": result,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============== WebSocket for Streaming ==============

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for streaming chat responses"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "chat":
                message = data.get("message", "")
                conversation_id = data.get("conversationId", str(uuid.uuid4()))
                
                try:
                    # Stream response
                    async for chunk in agent.stream_chat(message, conversation_id):
                        await websocket.send_json({
                            "type": "chunk",
                            "content": chunk,
                            "conversationId": conversation_id
                        })
                    
                    await websocket.send_json({
                        "type": "complete",
                        "conversationId": conversation_id
                    })
                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
                    
    except WebSocketDisconnect:
        print("WebSocket client disconnected")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PYTHON_API_PORT", 8006))
    uvicorn.run(app, host="0.0.0.0", port=port)
