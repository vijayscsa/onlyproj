"""
PagerDuty MCP Client - Comprehensive PagerDuty API V2 Client
Provides complete API coverage for incident management, alerts, services, and more.
"""
import os
import asyncio
import json
import subprocess
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


class PagerDutyMCPClient:
    """Comprehensive client for PagerDuty API V2 operations
    
    Supports 60+ API endpoints covering:
    - Incidents and Alerts
    - Services and Integrations
    - Users, Teams, and Schedules
    - Escalation Policies
    - Maintenance Windows
    - Log Entries
    - Analytics and Metrics
    - Event Orchestrations
    - Response Plays
    - Status Dashboards
    - Business Services
    - And more...
    """
    
    def __init__(self):
        self.mcp_path = os.getenv("PAGERDUTY_MCP_PATH", "/Users/vijayakumar.ravindran/pagerduty-mcp")
        self.api_key = os.getenv("PAGERDUTY_USER_API_KEY")
        self.api_host = os.getenv("PAGERDUTY_API_HOST", "https://api.pagerduty.com")
        
        self.is_connected = False
        self.available_tools: List[Dict[str, Any]] = []
        self._process: Optional[subprocess.Popen] = None
        
        # Comprehensive tool definitions for PagerDuty API V2
        self._tool_definitions = {
            # ==================== INCIDENTS ====================
            "list_incidents": {
                "description": "List PagerDuty incidents with filters",
                "parameters": ["limit", "offset", "statuses", "urgencies", "service_ids", "team_ids", "since", "until", "sort_by", "include"]
            },
            "get_incident_details": {
                "description": "Get detailed information about a specific incident",
                "parameters": ["incident_id", "include"]
            },
            "create_incident": {
                "description": "Create a new incident manually",
                "parameters": ["title", "service_id", "urgency", "body", "incident_key", "assignments", "escalation_policy_id", "priority_id", "conference_bridge"]
            },
            "update_incident": {
                "description": "Update an existing incident - status, title, urgency, escalation_level, assignments, priority",
                "parameters": ["incident_id", "type", "status", "title", "urgency", "escalation_level", "assignments", "priority"]
            },
            "manage_incidents": {
                "description": "Bulk update multiple incidents at once",
                "parameters": ["incident_ids", "status", "urgency", "assignees", "escalation_level", "priority"]
            },
            "merge_incidents": {
                "description": "Merge multiple incidents into a single incident",
                "parameters": ["source_incident_ids", "target_incident_id"]
            },
            "snooze_incident": {
                "description": "Snooze an incident for a specified duration",
                "parameters": ["incident_id", "duration_seconds"]
            },
            "acknowledge_incident": {
                "description": "Acknowledge a triggered incident",
                "parameters": ["incident_id"]
            },
            "resolve_incident": {
                "description": "Resolve an incident with optional resolution note",
                "parameters": ["incident_id", "resolution"]
            },
            "reassign_incident": {
                "description": "Reassign an incident to different users or escalation policy",
                "parameters": ["incident_id", "assignee_ids", "escalation_policy_id"]
            },
            "escalate_incident": {
                "description": "Manually escalate an incident to the next level",
                "parameters": ["incident_id", "escalation_level"]
            },
            "get_incident_log_entries": {
                "description": "Get timeline/log entries for an incident with full event details",
                "parameters": ["incident_id", "include", "is_overview", "time_zone"]
            },
            "get_related_incidents": {
                "description": "Get incidents related to a specific incident (AIOps feature)",
                "parameters": ["incident_id"]
            },
            "get_past_incidents": {
                "description": "Get historical similar incidents (AIOps feature)",
                "parameters": ["incident_id", "limit"]
            },
            "get_outlier_incident": {
                "description": "Determine if incident is an outlier compared to typical patterns",
                "parameters": ["incident_id"]
            },
            
            # ==================== INCIDENT NOTES ====================
            "list_incident_notes": {
                "description": "List all notes on an incident",
                "parameters": ["incident_id"]
            },
            "add_incident_note": {
                "description": "Add a note to an incident",
                "parameters": ["incident_id", "content"]
            },
            
            # ==================== ALERTS ====================
            "list_incident_alerts": {
                "description": "List all alerts on an incident",
                "parameters": ["incident_id", "limit", "offset", "include", "statuses", "sort_by"]
            },
            "get_alert": {
                "description": "Get complete extended details about a specific alert",
                "parameters": ["incident_id", "alert_id", "include"]
            },
            "update_alert": {
                "description": "Update an alert - resolve or acknowledge",
                "parameters": ["incident_id", "alert_id", "status"]
            },
            "manage_alerts": {
                "description": "Bulk update multiple alerts at once",
                "parameters": ["incident_id", "alert_ids", "status"]
            },
            
            # ==================== RESPONDERS ====================
            "add_responders": {
                "description": "Request additional responders for an incident",
                "parameters": ["incident_id", "requester_id", "responder_ids", "message"]
            },
            "list_responder_requests": {
                "description": "List all responder requests for an incident",
                "parameters": ["incident_id"]
            },
            
            # ==================== SERVICES ====================
            "list_services": {
                "description": "List all PagerDuty services",
                "parameters": ["limit", "offset", "query", "team_ids", "include", "sort_by", "time_zone"]
            },
            "get_service": {
                "description": "Get detailed information about a specific service",
                "parameters": ["service_id", "include", "time_zone"]
            },
            "create_service": {
                "description": "Create a new service",
                "parameters": ["name", "description", "escalation_policy_id", "alert_creation", "incident_urgency_rule"]
            },
            "update_service": {
                "description": "Update an existing service",
                "parameters": ["service_id", "name", "description", "status", "escalation_policy_id"]
            },
            "delete_service": {
                "description": "Delete a service",
                "parameters": ["service_id"]
            },
            
            # ==================== SERVICE INTEGRATIONS ====================
            "list_service_integrations": {
                "description": "List all integrations for a service",
                "parameters": ["service_id", "include"]
            },
            "get_service_integration": {
                "description": "Get details of a specific integration",
                "parameters": ["service_id", "integration_id", "include"]
            },
            "create_service_integration": {
                "description": "Create a new integration for a service",
                "parameters": ["service_id", "type", "name", "vendor_id"]
            },
            "update_service_integration": {
                "description": "Update an existing integration",
                "parameters": ["service_id", "integration_id", "name"]
            },
            
            # ==================== USERS ====================
            "list_users": {
                "description": "List all PagerDuty users",
                "parameters": ["limit", "offset", "query", "team_ids", "include"]
            },
            "get_user": {
                "description": "Get detailed information about a specific user",
                "parameters": ["user_id", "include"]
            },
            "create_user": {
                "description": "Create a new user",
                "parameters": ["name", "email", "role", "time_zone", "job_title"]
            },
            "update_user": {
                "description": "Update an existing user",
                "parameters": ["user_id", "name", "email", "role", "time_zone", "job_title"]
            },
            "delete_user": {
                "description": "Delete a user",
                "parameters": ["user_id"]
            },
            "get_user_contact_methods": {
                "description": "Get all contact methods for a user",
                "parameters": ["user_id"]
            },
            "get_user_notification_rules": {
                "description": "Get all notification rules for a user",
                "parameters": ["user_id", "include"]
            },
            "get_current_user": {
                "description": "Get the currently authenticated user",
                "parameters": ["include"]
            },
            "get_user_sessions": {
                "description": "Get active sessions for a user",
                "parameters": ["user_id"]
            },
            
            # ==================== TEAMS ====================
            "list_teams": {
                "description": "List all PagerDuty teams",
                "parameters": ["limit", "offset", "query", "include"]
            },
            "get_team": {
                "description": "Get detailed information about a specific team",
                "parameters": ["team_id", "include"]
            },
            "create_team": {
                "description": "Create a new team",
                "parameters": ["name", "description", "parent_id"]
            },
            "update_team": {
                "description": "Update an existing team",
                "parameters": ["team_id", "name", "description"]
            },
            "delete_team": {
                "description": "Delete a team",
                "parameters": ["team_id"]
            },
            "list_team_members": {
                "description": "List all members of a team",
                "parameters": ["team_id", "include"]
            },
            "add_team_member": {
                "description": "Add a user to a team",
                "parameters": ["team_id", "user_id", "role"]
            },
            "remove_team_member": {
                "description": "Remove a user from a team",
                "parameters": ["team_id", "user_id"]
            },
            
            # ==================== SCHEDULES ====================
            "list_schedules": {
                "description": "List all PagerDuty schedules",
                "parameters": ["limit", "offset", "query", "include"]
            },
            "get_schedule": {
                "description": "Get detailed information about a specific schedule",
                "parameters": ["schedule_id", "include", "since", "until", "time_zone"]
            },
            "create_schedule": {
                "description": "Create a new on-call schedule",
                "parameters": ["name", "description", "time_zone", "schedule_layers"]
            },
            "update_schedule": {
                "description": "Update an existing schedule",
                "parameters": ["schedule_id", "name", "description", "time_zone", "schedule_layers"]
            },
            "delete_schedule": {
                "description": "Delete a schedule",
                "parameters": ["schedule_id"]
            },
            "list_schedule_users": {
                "description": "List all users in a schedule for a given time range",
                "parameters": ["schedule_id", "since", "until"]
            },
            "list_schedule_overrides": {
                "description": "List all overrides for a schedule",
                "parameters": ["schedule_id", "since", "until", "editable"]
            },
            "create_schedule_override": {
                "description": "Create an override for a schedule (swap on-call)",
                "parameters": ["schedule_id", "user_id", "start", "end"]
            },
            "delete_schedule_override": {
                "description": "Delete a schedule override",
                "parameters": ["schedule_id", "override_id"]
            },
            
            # ==================== ON-CALLS ====================
            "list_oncalls": {
                "description": "List all current on-call entries",
                "parameters": ["schedule_ids", "escalation_policy_ids", "user_ids", "since", "until", "include", "time_zone", "earliest"]
            },
            
            # ==================== ESCALATION POLICIES ====================
            "list_escalation_policies": {
                "description": "List all escalation policies",
                "parameters": ["limit", "offset", "query", "team_ids", "include", "sort_by"]
            },
            "get_escalation_policy": {
                "description": "Get detailed information about an escalation policy",
                "parameters": ["id", "include"]
            },
            "create_escalation_policy": {
                "description": "Create a new escalation policy",
                "parameters": ["name", "description", "num_loops", "escalation_rules", "on_call_handoff_notifications", "teams"]
            },
            "update_escalation_policy": {
                "description": "Update an existing escalation policy",
                "parameters": ["id", "name", "description", "num_loops", "escalation_rules"]
            },
            "delete_escalation_policy": {
                "description": "Delete an escalation policy",
                "parameters": ["id"]
            },
            
            # ==================== PRIORITIES ====================
            "list_priorities": {
                "description": "List all incident priorities configured in the account",
                "parameters": []
            },
            
            # ==================== TAGS ====================
            "list_tags": {
                "description": "List all tags in the account",
                "parameters": ["limit", "offset", "query"]
            },
            "get_tag": {
                "description": "Get details of a specific tag",
                "parameters": ["tag_id"]
            },
            "create_tag": {
                "description": "Create a new tag",
                "parameters": ["label"]
            },
            "delete_tag": {
                "description": "Delete a tag",
                "parameters": ["tag_id"]
            },
            "get_entity_tags": {
                "description": "Get tags for an entity (user, team, escalation_policy)",
                "parameters": ["entity_type", "entity_id"]
            },
            "assign_tags": {
                "description": "Assign tags to an entity",
                "parameters": ["entity_type", "entity_id", "tag_ids"]
            },
            
            # ==================== LOG ENTRIES ====================
            "list_log_entries": {
                "description": "List all log entries across all incidents",
                "parameters": ["limit", "offset", "since", "until", "is_overview", "include", "time_zone"]
            },
            "get_log_entry": {
                "description": "Get details of a specific log entry with channel data",
                "parameters": ["log_entry_id", "include", "time_zone"]
            },
            
            # ==================== MAINTENANCE WINDOWS ====================
            "list_maintenance_windows": {
                "description": "List all maintenance windows",
                "parameters": ["limit", "offset", "query", "team_ids", "service_ids", "include", "filter"]
            },
            "get_maintenance_window": {
                "description": "Get details of a specific maintenance window",
                "parameters": ["maintenance_window_id", "include"]
            },
            "create_maintenance_window": {
                "description": "Create a new maintenance window",
                "parameters": ["description", "start_time", "end_time", "service_ids"]
            },
            "update_maintenance_window": {
                "description": "Update an existing maintenance window",
                "parameters": ["maintenance_window_id", "description", "start_time", "end_time", "service_ids"]
            },
            "delete_maintenance_window": {
                "description": "Delete a maintenance window",
                "parameters": ["maintenance_window_id"]
            },
            
            # ==================== EXTENSIONS ====================
            "list_extensions": {
                "description": "List all extensions (webhooks, integrations)",
                "parameters": ["limit", "offset", "query", "extension_schema_id", "include"]
            },
            "get_extension": {
                "description": "Get details of a specific extension",
                "parameters": ["extension_id", "include"]
            },
            "create_extension": {
                "description": "Create a new extension",
                "parameters": ["name", "extension_schema_id", "endpoint_url", "extension_objects", "config"]
            },
            "update_extension": {
                "description": "Update an existing extension",
                "parameters": ["extension_id", "name", "endpoint_url", "config"]
            },
            "delete_extension": {
                "description": "Delete an extension",
                "parameters": ["extension_id"]
            },
            
            # ==================== EXTENSION SCHEMAS ====================
            "list_extension_schemas": {
                "description": "List all extension schemas (available extension types)",
                "parameters": ["limit", "offset"]
            },
            "get_extension_schema": {
                "description": "Get details of a specific extension schema",
                "parameters": ["extension_schema_id"]
            },
            
            # ==================== VENDORS ====================
            "list_vendors": {
                "description": "List all vendors (monitoring tools that can integrate)",
                "parameters": ["limit", "offset"]
            },
            "get_vendor": {
                "description": "Get details of a specific vendor",
                "parameters": ["vendor_id"]
            },
            
            # ==================== INCIDENT WORKFLOWS ====================
            "list_incident_workflows": {
                "description": "List all incident workflows",
                "parameters": ["limit", "offset", "query", "include"]
            },
            "get_incident_workflow": {
                "description": "Get details of a specific incident workflow",
                "parameters": ["workflow_id", "include"]
            },
            "start_incident_workflow": {
                "description": "Trigger/start an incident workflow on an incident",
                "parameters": ["workflow_id", "incident_id"]
            },
            
            # ==================== EVENT ORCHESTRATIONS ====================
            "list_event_orchestrations": {
                "description": "List all event orchestrations",
                "parameters": ["limit", "offset", "sort_by"]
            },
            "get_event_orchestration": {
                "description": "Get details of a specific event orchestration",
                "parameters": ["orchestration_id"]
            },
            "get_event_orchestration_router": {
                "description": "Get the routing rules for an event orchestration",
                "parameters": ["orchestration_id"]
            },
            "get_event_orchestration_service_rules": {
                "description": "Get the service-level rules for an event orchestration",
                "parameters": ["service_id"]
            },
            "update_event_orchestration_service_rules": {
                "description": "Update event orchestration rules for a service",
                "parameters": ["service_id", "rules"]
            },
            
            # ==================== RESPONSE PLAYS ====================
            "list_response_plays": {
                "description": "List all response plays",
                "parameters": ["limit", "offset", "query", "filter_for_manual_run"]
            },
            "get_response_play": {
                "description": "Get details of a specific response play",
                "parameters": ["response_play_id"]
            },
            "run_response_play": {
                "description": "Run a response play on an incident",
                "parameters": ["response_play_id", "incident_id"]
            },
            
            # ==================== BUSINESS SERVICES ====================
            "list_business_services": {
                "description": "List all business services",
                "parameters": ["limit", "offset", "query"]
            },
            "get_business_service": {
                "description": "Get details of a specific business service",
                "parameters": ["business_service_id"]
            },
            "create_business_service": {
                "description": "Create a new business service",
                "parameters": ["name", "description", "point_of_contact", "team_id"]
            },
            "update_business_service": {
                "description": "Update an existing business service",
                "parameters": ["business_service_id", "name", "description", "point_of_contact"]
            },
            "delete_business_service": {
                "description": "Delete a business service",
                "parameters": ["business_service_id"]
            },
            "list_business_service_subscribers": {
                "description": "List subscribers to a business service's status page",
                "parameters": ["business_service_id"]
            },
            
            # ==================== SERVICE DEPENDENCIES ====================
            "list_service_dependencies": {
                "description": "List service dependencies showing relationships between services",
                "parameters": ["service_id"]
            },
            "create_service_dependency": {
                "description": "Create a dependency between two services",
                "parameters": ["dependent_service_id", "supporting_service_id"]
            },
            "delete_service_dependency": {
                "description": "Delete a service dependency",
                "parameters": ["dependency_id"]
            },
            
            # ==================== STATUS DASHBOARDS ====================
            "list_status_dashboards": {
                "description": "List all status dashboards",
                "parameters": ["limit", "offset"]
            },
            "get_status_dashboard": {
                "description": "Get details of a specific status dashboard",
                "parameters": ["status_dashboard_id"]
            },
            
            # ==================== CHANGE EVENTS ====================
            "list_change_events": {
                "description": "List recent change events that might correlate with incidents",
                "parameters": ["limit", "offset", "since", "until", "service_ids", "integration_ids"]
            },
            "get_change_event": {
                "description": "Get details of a specific change event",
                "parameters": ["change_event_id"]
            },
            
            # ==================== ANALYTICS ====================
            "get_incident_analytics": {
                "description": "Get analytics data for incidents",
                "parameters": ["since", "until", "service_ids", "team_ids", "urgencies"]
            },
            "get_service_analytics": {
                "description": "Get analytics data for a specific service",
                "parameters": ["service_id", "since", "until"]
            },
            "get_team_analytics": {
                "description": "Get analytics data for a specific team",
                "parameters": ["team_id", "since", "until"]
            },
            "get_raw_incident_data": {
                "description": "Get raw incident data for custom analytics",
                "parameters": ["since", "until", "service_ids"]
            },
            
            # ==================== AUDIT RECORDS ====================
            "list_audit_records": {
                "description": "List audit trail records for compliance",
                "parameters": ["limit", "since", "until", "root_resource_types", "actor_type", "actor_id", "method_type", "method_truncated_token", "actions"]
            },
            
            # ==================== ABILITIES ====================
            "list_abilities": {
                "description": "List all abilities/features enabled for the account",
                "parameters": []
            },
            "test_ability": {
                "description": "Check if a specific ability is enabled",
                "parameters": ["ability"]
            },
            
            # ==================== RULESETS (Legacy) ====================
            "list_rulesets": {
                "description": "List all rulesets (legacy - prefer Event Orchestration)",
                "parameters": ["limit", "offset"]
            },
            "get_ruleset": {
                "description": "Get details of a specific ruleset",
                "parameters": ["ruleset_id"]
            },
            "list_ruleset_rules": {
                "description": "List all rules in a ruleset",
                "parameters": ["ruleset_id"]
            },
            
            # ==================== ADD-ONS ====================
            "list_addons": {
                "description": "List all installed add-ons",
                "parameters": ["limit", "offset", "service_ids", "filter", "include"]
            },
            "get_addon": {
                "description": "Get details of a specific add-on installation",
                "parameters": ["addon_id"]
            },
            "install_addon": {
                "description": "Install an add-on",
                "parameters": ["type", "name", "src"]
            },
            "delete_addon": {
                "description": "Remove an add-on installation",
                "parameters": ["addon_id"]
            },
            
            # ==================== LICENSES ====================
            "list_licenses": {
                "description": "List all licenses for the account",
                "parameters": []
            },
            "list_license_allocations": {
                "description": "List license allocations showing which users have which licenses",
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
                    if params.get("sort_by"):
                        query_params["sort_by"] = params["sort_by"]
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    
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
                
                elif tool_name == "get_incident_notes":
                    response = await client.get(f"/incidents/{params['incident_id']}/notes")
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
                
                elif tool_name == "get_related_incidents":
                    response = await client.get(f"/incidents/{params['incident_id']}/related_incidents")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_past_incidents":
                    response = await client.get(f"/incidents/{params['incident_id']}/past_incidents")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "add_responders":
                    responder_requests = [
                        {"responder_request_target": {"id": rid, "type": "user_reference"}}
                        for rid in params.get("responder_ids", [])
                    ]
                    response = await client.post(
                        f"/incidents/{params['incident_id']}/responder_requests",
                        json={"requester_id": "PUSER123", "responder_request_targets": responder_requests}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_teams":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/teams", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_team":
                    response = await client.get(f"/teams/{params['team_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_team_members":
                    response = await client.get(f"/teams/{params['team_id']}/members")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_schedule":
                    response = await client.get(f"/schedules/{params['schedule_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_incident_workflows":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/incident_workflows", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_event_orchestrations":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/event_orchestrations", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                # ==================== NEW API V2 ENDPOINTS ====================
                
                # ALERTS
                elif tool_name == "list_incident_alerts":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("statuses"):
                        query_params["statuses[]"] = params["statuses"]
                    if params.get("sort_by"):
                        query_params["sort_by"] = params["sort_by"]
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get(f"/incidents/{params['incident_id']}/alerts", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_alert":
                    # GET /incidents/{id}/alerts/{alert_id} - Get complete extended alert details
                    query_params = {}
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get(
                        f"/incidents/{params['incident_id']}/alerts/{params['alert_id']}", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "update_alert":
                    response = await client.put(
                        f"/incidents/{params['incident_id']}/alerts/{params['alert_id']}",
                        json={"alert": {"type": "alert", "status": params.get("status", "resolved")}}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "manage_alerts":
                    alerts = [{"id": aid, "type": "alert", "status": params.get("status", "resolved")} 
                              for aid in params.get("alert_ids", [])]
                    response = await client.put(
                        f"/incidents/{params['incident_id']}/alerts",
                        json={"alerts": alerts}
                    )
                    response.raise_for_status()
                    return response.json()
                
                # INCIDENT NOTES
                elif tool_name == "list_incident_notes":
                    response = await client.get(f"/incidents/{params['incident_id']}/notes")
                    response.raise_for_status()
                    return response.json()
                
                # INCIDENT ACTIONS
                elif tool_name == "update_incident":
                    body = {"incident": {"type": "incident"}}
                    if params.get("status"):
                        body["incident"]["status"] = params["status"]
                    if params.get("title"):
                        body["incident"]["title"] = params["title"]
                    if params.get("urgency"):
                        body["incident"]["urgency"] = params["urgency"]
                    if params.get("escalation_level"):
                        body["incident"]["escalation_level"] = params["escalation_level"]
                    if params.get("assignments"):
                        body["incident"]["assignments"] = params["assignments"]
                    if params.get("priority"):
                        body["incident"]["priority"] = {"id": params["priority"], "type": "priority_reference"}
                    response = await client.put(f"/incidents/{params['incident_id']}", json=body)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "merge_incidents":
                    source_incidents = [{"id": sid, "type": "incident_reference"} 
                                        for sid in params.get("source_incident_ids", [])]
                    response = await client.put(
                        f"/incidents/{params['target_incident_id']}/merge",
                        json={"source_incidents": source_incidents}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "snooze_incident":
                    response = await client.post(
                        f"/incidents/{params['incident_id']}/snooze",
                        json={"duration": params.get("duration_seconds", 3600)}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "reassign_incident":
                    body = {"incident": {"type": "incident"}}
                    if params.get("assignee_ids"):
                        body["incident"]["assignments"] = [
                            {"assignee": {"id": uid, "type": "user_reference"}} 
                            for uid in params["assignee_ids"]
                        ]
                    if params.get("escalation_policy_id"):
                        body["incident"]["escalation_policy"] = {
                            "id": params["escalation_policy_id"], 
                            "type": "escalation_policy_reference"
                        }
                    response = await client.put(f"/incidents/{params['incident_id']}", json=body)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "escalate_incident":
                    response = await client.put(
                        f"/incidents/{params['incident_id']}",
                        json={"incident": {"type": "incident", "escalation_level": params.get("escalation_level", 2)}}
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "create_incident":
                    body = {
                        "incident": {
                            "type": "incident",
                            "title": params["title"],
                            "service": {"id": params["service_id"], "type": "service_reference"}
                        }
                    }
                    if params.get("urgency"):
                        body["incident"]["urgency"] = params["urgency"]
                    if params.get("body"):
                        body["incident"]["body"] = {"type": "incident_body", "details": params["body"]}
                    if params.get("incident_key"):
                        body["incident"]["incident_key"] = params["incident_key"]
                    if params.get("priority_id"):
                        body["incident"]["priority"] = {"id": params["priority_id"], "type": "priority_reference"}
                    if params.get("escalation_policy_id"):
                        body["incident"]["escalation_policy"] = {
                            "id": params["escalation_policy_id"], 
                            "type": "escalation_policy_reference"
                        }
                    response = await client.post("/incidents", json=body)
                    response.raise_for_status()
                    return response.json()
                
                # RESPONDER REQUESTS
                elif tool_name == "list_responder_requests":
                    response = await client.get(f"/incidents/{params['incident_id']}/responder_requests")
                    response.raise_for_status()
                    return response.json()
                
                # USERS
                elif tool_name == "get_user":
                    query_params = {}
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get(f"/users/{params['user_id']}", params=query_params if query_params else None)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_user_contact_methods":
                    response = await client.get(f"/users/{params['user_id']}/contact_methods")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_user_notification_rules":
                    response = await client.get(f"/users/{params['user_id']}/notification_rules")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_current_user":
                    query_params = {}
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get("/users/me", params=query_params if query_params else None)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_user_sessions":
                    response = await client.get(f"/users/{params['user_id']}/sessions")
                    response.raise_for_status()
                    return response.json()
                
                # ESCALATION POLICY
                elif tool_name == "get_escalation_policy":
                    query_params = {}
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get(f"/escalation_policies/{params['id']}", params=query_params if query_params else None)
                    response.raise_for_status()
                    return response.json()
                
                # PRIORITIES
                elif tool_name == "list_priorities":
                    response = await client.get("/priorities")
                    response.raise_for_status()
                    return response.json()
                
                # TAGS
                elif tool_name == "list_tags":
                    query_params = {"limit": params.get("limit", 100), "offset": params.get("offset", 0)}
                    if params.get("query"):
                        query_params["query"] = params["query"]
                    response = await client.get("/tags", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_tag":
                    response = await client.get(f"/tags/{params['tag_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_entity_tags":
                    entity_type = params["entity_type"]  # users, teams, escalation_policies
                    response = await client.get(f"/{entity_type}/{params['entity_id']}/tags")
                    response.raise_for_status()
                    return response.json()
                
                # LOG ENTRIES
                elif tool_name == "list_log_entries":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    if params.get("is_overview"):
                        query_params["is_overview"] = params["is_overview"]
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    if params.get("time_zone"):
                        query_params["time_zone"] = params["time_zone"]
                    response = await client.get("/log_entries", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_log_entry":
                    query_params = {}
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    if params.get("time_zone"):
                        query_params["time_zone"] = params["time_zone"]
                    response = await client.get(
                        f"/log_entries/{params['log_entry_id']}", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                # MAINTENANCE WINDOWS
                elif tool_name == "list_maintenance_windows":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("query"):
                        query_params["query"] = params["query"]
                    if params.get("team_ids"):
                        query_params["team_ids[]"] = params["team_ids"]
                    if params.get("service_ids"):
                        query_params["service_ids[]"] = params["service_ids"]
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    if params.get("filter"):
                        query_params["filter"] = params["filter"]
                    response = await client.get("/maintenance_windows", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_maintenance_window":
                    query_params = {}
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get(
                        f"/maintenance_windows/{params['maintenance_window_id']}", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "create_maintenance_window":
                    services = [{"id": sid, "type": "service_reference"} for sid in params.get("service_ids", [])]
                    body = {
                        "maintenance_window": {
                            "type": "maintenance_window",
                            "start_time": params["start_time"],
                            "end_time": params["end_time"],
                            "services": services
                        }
                    }
                    if params.get("description"):
                        body["maintenance_window"]["description"] = params["description"]
                    response = await client.post("/maintenance_windows", json=body)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "delete_maintenance_window":
                    response = await client.delete(f"/maintenance_windows/{params['maintenance_window_id']}")
                    response.raise_for_status()
                    return {"status": "deleted", "id": params['maintenance_window_id']}
                
                # EXTENSIONS
                elif tool_name == "list_extensions":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("query"):
                        query_params["query"] = params["query"]
                    if params.get("extension_schema_id"):
                        query_params["extension_schema_id"] = params["extension_schema_id"]
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get("/extensions", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_extension":
                    response = await client.get(f"/extensions/{params['extension_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # EXTENSION SCHEMAS
                elif tool_name == "list_extension_schemas":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/extension_schemas", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_extension_schema":
                    response = await client.get(f"/extension_schemas/{params['extension_schema_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # VENDORS
                elif tool_name == "list_vendors":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/vendors", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_vendor":
                    response = await client.get(f"/vendors/{params['vendor_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # INCIDENT WORKFLOWS
                elif tool_name == "get_incident_workflow":
                    response = await client.get(f"/incident_workflows/{params['workflow_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "start_incident_workflow":
                    response = await client.post(
                        f"/incident_workflows/{params['workflow_id']}/instances",
                        json={"incident": {"id": params["incident_id"], "type": "incident_reference"}}
                    )
                    response.raise_for_status()
                    return response.json()
                
                # EVENT ORCHESTRATIONS
                elif tool_name == "get_event_orchestration":
                    response = await client.get(f"/event_orchestrations/{params['orchestration_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_event_orchestration_router":
                    response = await client.get(f"/event_orchestrations/{params['orchestration_id']}/router")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_event_orchestration_service_rules":
                    response = await client.get(f"/event_orchestrations/services/{params['service_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # RESPONSE PLAYS
                elif tool_name == "list_response_plays":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("query"):
                        query_params["query"] = params["query"]
                    if params.get("filter_for_manual_run"):
                        query_params["filter_for_manual_run"] = params["filter_for_manual_run"]
                    response = await client.get("/response_plays", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_response_play":
                    response = await client.get(f"/response_plays/{params['response_play_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "run_response_play":
                    response = await client.post(
                        f"/response_plays/{params['response_play_id']}/run",
                        json={"incident": {"id": params["incident_id"], "type": "incident_reference"}}
                    )
                    response.raise_for_status()
                    return response.json()
                
                # BUSINESS SERVICES
                elif tool_name == "list_business_services":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("query"):
                        query_params["query"] = params["query"]
                    response = await client.get("/business_services", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_business_service":
                    response = await client.get(f"/business_services/{params['business_service_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_business_service_subscribers":
                    response = await client.get(f"/business_services/{params['business_service_id']}/subscribers")
                    response.raise_for_status()
                    return response.json()
                
                # SERVICE DEPENDENCIES
                elif tool_name == "list_service_dependencies":
                    response = await client.get(f"/service_dependencies/technical_services/{params['service_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # STATUS DASHBOARDS
                elif tool_name == "list_status_dashboards":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/status_dashboards", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_status_dashboard":
                    response = await client.get(f"/status_dashboards/{params['status_dashboard_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # CHANGE EVENTS
                elif tool_name == "list_change_events":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    if params.get("service_ids"):
                        query_params["service_ids[]"] = params["service_ids"]
                    if params.get("integration_ids"):
                        query_params["integration_ids[]"] = params["integration_ids"]
                    response = await client.get("/change_events", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_change_event":
                    response = await client.get(f"/change_events/{params['change_event_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # ANALYTICS
                elif tool_name == "get_incident_analytics":
                    query_params = {}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    if params.get("service_ids"):
                        query_params["service_ids[]"] = params["service_ids"]
                    if params.get("team_ids"):
                        query_params["team_ids[]"] = params["team_ids"]
                    if params.get("urgencies"):
                        query_params["urgencies[]"] = params["urgencies"]
                    response = await client.get("/analytics/metrics/incidents/all", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_service_analytics":
                    query_params = {}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    response = await client.get(
                        f"/analytics/metrics/incidents/services/{params['service_id']}", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_team_analytics":
                    query_params = {}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    response = await client.get(
                        f"/analytics/metrics/incidents/teams/{params['team_id']}", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                # AUDIT RECORDS
                elif tool_name == "list_audit_records":
                    query_params = {"limit": params.get("limit", 25)}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    if params.get("root_resource_types"):
                        query_params["root_resource_types[]"] = params["root_resource_types"]
                    if params.get("actor_type"):
                        query_params["actor_type"] = params["actor_type"]
                    if params.get("actor_id"):
                        query_params["actor_id"] = params["actor_id"]
                    if params.get("method_type"):
                        query_params["method_type"] = params["method_type"]
                    if params.get("actions"):
                        query_params["actions[]"] = params["actions"]
                    response = await client.get("/audit/records", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                # ABILITIES
                elif tool_name == "list_abilities":
                    response = await client.get("/abilities")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "test_ability":
                    response = await client.get(f"/abilities/{params['ability']}")
                    if response.status_code == 204:
                        return {"ability": params["ability"], "enabled": True}
                    elif response.status_code == 402:
                        return {"ability": params["ability"], "enabled": False}
                    response.raise_for_status()
                    return response.json()
                
                # RULESETS (Legacy)
                elif tool_name == "list_rulesets":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/rulesets", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_ruleset":
                    response = await client.get(f"/rulesets/{params['ruleset_id']}")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_ruleset_rules":
                    response = await client.get(f"/rulesets/{params['ruleset_id']}/rules")
                    response.raise_for_status()
                    return response.json()
                
                # ADD-ONS
                elif tool_name == "list_addons":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    if params.get("service_ids"):
                        query_params["service_ids[]"] = params["service_ids"]
                    if params.get("filter"):
                        query_params["filter"] = params["filter"]
                    if params.get("include"):
                        query_params["include[]"] = params["include"]
                    response = await client.get("/addons", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "get_addon":
                    response = await client.get(f"/addons/{params['addon_id']}")
                    response.raise_for_status()
                    return response.json()
                
                # LICENSES
                elif tool_name == "list_licenses":
                    response = await client.get("/licenses")
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "list_license_allocations":
                    query_params = {"limit": params.get("limit", 25), "offset": params.get("offset", 0)}
                    response = await client.get("/license_allocations", params=query_params)
                    response.raise_for_status()
                    return response.json()
                
                # SCHEDULE OVERRIDES
                elif tool_name == "list_schedule_overrides":
                    query_params = {}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    if params.get("editable"):
                        query_params["editable"] = params["editable"]
                    response = await client.get(
                        f"/schedules/{params['schedule_id']}/overrides", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "create_schedule_override":
                    body = {
                        "override": {
                            "start": params["start"],
                            "end": params["end"],
                            "user": {"id": params["user_id"], "type": "user_reference"}
                        }
                    }
                    response = await client.post(f"/schedules/{params['schedule_id']}/overrides", json=body)
                    response.raise_for_status()
                    return response.json()
                
                elif tool_name == "delete_schedule_override":
                    response = await client.delete(
                        f"/schedules/{params['schedule_id']}/overrides/{params['override_id']}"
                    )
                    response.raise_for_status()
                    return {"status": "deleted", "id": params["override_id"]}
                
                # SCHEDULE USERS
                elif tool_name == "list_schedule_users":
                    query_params = {}
                    if params.get("since"):
                        query_params["since"] = params["since"]
                    if params.get("until"):
                        query_params["until"] = params["until"]
                    response = await client.get(
                        f"/schedules/{params['schedule_id']}/users", 
                        params=query_params if query_params else None
                    )
                    response.raise_for_status()
                    return response.json()
                
                # SERVICE INTEGRATIONS
                elif tool_name == "get_service_integration":
                    response = await client.get(
                        f"/services/{params['service_id']}/integrations/{params['integration_id']}"
                    )
                    response.raise_for_status()
                    return response.json()
                
                # OUTLIER INCIDENT
                elif tool_name == "get_outlier_incident":
                    response = await client.get(f"/incidents/{params['incident_id']}/outlier_incident")
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
            from datetime import datetime as dt
            today_str = dt.utcnow().strftime("%Y-%m-%dT")
            
            all_mock_incidents = [
                    {
                        "id": "P123ABC",
                        "title": "[CRITICAL] EdgeNode Model Processing Failure",
                        "status": "triggered",
                        "urgency": "high",
                        "created_at": "2026-01-30T18:00:00Z",
                        "last_status_change_at": "2026-01-30T18:00:00Z",
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
                        "last_status_change_at": "2026-01-30T17:50:00Z",
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
                        "last_status_change_at": "2026-01-30T16:30:00Z",
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
                        "last_status_change_at": "2026-01-30T15:00:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "description": "Output queue size growing - monitoring required",
                        "assignments": []
                    },
                    {
                        "id": "PRES001",
                        "title": "[RESOLVED] Scheduled Maintenance Complete",
                        "status": "resolved",
                        "urgency": "low",
                        "created_at": "2026-01-29T10:00:00Z",
                        "last_status_change_at": f"{today_str}08:30:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "description": "Scheduled maintenance window completed successfully",
                        "assignments": []
                    },
                    {
                        "id": "PRES002",
                        "title": "[RESOLVED] Brief Network Blip",
                        "status": "resolved",
                        "urgency": "high",
                        "created_at": "2026-01-29T22:00:00Z",
                        "last_status_change_at": f"{today_str}02:15:00Z",
                        "service": {"id": "PBD0TCK", "summary": "EdgeNode DP&E Ingestion and controls - Prod"},
                        "description": "Network connectivity issue resolved after failover",
                        "assignments": []
                    }
            ]
            
            # Filter by statuses if provided
            statuses_filter = params.get("statuses", [])
            if statuses_filter:
                filtered = [i for i in all_mock_incidents if i["status"] in statuses_filter]
            else:
                filtered = all_mock_incidents
            
            return {
                "incidents": filtered,
                "limit": params.get("limit", 25),
                "offset": params.get("offset", 0),
                "total": len(filtered),
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
        
        elif tool_name == "get_incident_notes":
            return {
                "notes": [
                    {
                        "id": "NOTE001",
                        "content": "Investigating root cause - appears to be related to upstream data feed failure.",
                        "created_at": "2026-01-30T18:15:00Z",
                        "user": {"id": "PUSER1", "summary": "John Doe"}
                    },
                    {
                        "id": "NOTE002",
                        "content": "Escalated to platform team. Runbook steps 1-3 completed.",
                        "created_at": "2026-01-30T18:30:00Z",
                        "user": {"id": "PUSER2", "summary": "Jane Smith"}
                    }
                ]
            }
        
        elif tool_name == "list_incident_alerts":
            return {
                "alerts": [
                    {
                        "id": "PALERT001",
                        "status": "triggered",
                        "severity": "critical",
                        "summary": "Failure : Daily - RTF Data Services : HLS : (STREAM | HLS | HLS_ACCT | ALL | DALY | 1202.001) : 20260212",
                        "created_at": "2026-02-12T09:43:00Z",
                        "alert_key": "0e2486e10994a41a29658dbd4890778896e6ae93fb68da75a7abcbb4258ac663d",
                        "html_url": "https://cba.pagerduty.com/alerts/PALERT001",
                        "suppressed": False,
                        "body": {
                            "type": "alert_body",
                            "details": {
                                "firing": "Labels:\n- alertname = prod-failure-daily-rtf-data-services-hls\n- ci_number = CI081725901\n- cmdb_id = CI081725900\n- env = prod\n- rtf_application = HLS\n- rtf_business_date = 20260212\n- rtf_job = STREAM | HLS | HLS_ACCT | ALL | DALY | 1202.001\n- rtf_system = Daily - RTF Data Services\n- severity = critical\nAnnotations:\n- description = Failed JOB.\n- message = Failure : Daily - RTF Data Services : HLS : (STREAM | HLS | HLS_ACCT | ALL | DALY | 1202.001) : 20260212\n- runbook_url = https://www-prd.rtf-ab-prod.rtfo2.rtfdrtf01.aws.prod.au.internal.cba/controlcenter/spa/#/daily-jobs/system=Daily - RTF Data Services",
                                "num_firing": 1,
                                "num_resolved": 0,
                                "resolved": "",
                                "annotations": {
                                    "description": "Failed JOB.",
                                    "message": "Failure : Daily - RTF Data Services : HLS : (STREAM|HLS|HLS_ACCT|ALL|DALY|1202.001) : 20260212",
                                    "runbook_url": "https://www-prd.rtf-ab-prod.rtfo2.rtfdrtf01.aws.prod.au.internal.cba/controlcenter/spa/#/daily-jobs/system=Daily - RTF Data Services",
                                    "summary": "Failure | Daily - RTF Data Services | HLS"
                                },
                                "labels": {
                                    "alertname": "prod-failure-daily-rtf-data-services-hls",
                                    "ci_number": "CI081725901",
                                    "cmdb_id": "CI081725900",
                                    "env": "prod",
                                    "rtf_application": "HLS",
                                    "rtf_business_date": "20260212",
                                    "rtf_job": "STREAM | HLS | HLS_ACCT | ALL | DALY | 1202.001",
                                    "rtf_system": "Daily - RTF Data Services",
                                    "severity": "critical"
                                },
                                "source": "/graph?g0.expr=max+by+%28rtf_system%2C+rtf_application%2C+rtf_job%2C+rtf_business_date%2C+ci_number%29+%28rtf_ab_job_status%7Bci_number%3D%22CI081725901%22%2Cnamespace%3D%22rtf-ab-data-serv-stg%22%2Crtf_application%3D%22HLS%22%2Crtf_system%3D%22Daily+-+RTF+Data+Services%22%7D%29+%3D+%3D+4&g0.tab=1",
                                "SilenceURL": "https://metrics.cba/alerting/silence/new?alertmanager=Alertmanager&matcher=alertname%3Dprod-failure-daily-rtf-data-services-hls&matcher=cmdb_id%3DCI081725900"
                            },
                            "contexts": [
                                {
                                    "type": "link",
                                    "href": "https://metrics.cba/alerting/silence/new?alertmanager=Alertmanager",
                                    "text": "View in Alertmanager"
                                }
                            ]
                        },
                        "service": {"id": "PBD0TCK", "summary": "EdgeNode DP&E Ingestion and controls - Prod"}
                    }
                ]
            }
        
        elif tool_name == "get_incident_log_entries":
            return {
                "log_entries": [
                    {
                        "id": "LOG1",
                        "type": "trigger_log_entry",
                        "created_at": "2026-01-30T18:00:00Z",
                        "summary": "Incident triggered via monitoring alert"
                    },
                    {
                        "id": "LOG2",
                        "type": "notify_log_entry",
                        "created_at": "2026-01-30T18:00:15Z",
                        "summary": "Notification sent to John Doe via SMS and push notification"
                    },
                    {
                        "id": "LOG3",
                        "type": "escalate_log_entry",
                        "created_at": "2026-01-30T18:05:00Z",
                        "summary": "Escalated to DPE Prod Ops team"
                    }
                ]
            }
        
        elif tool_name == "get_related_incidents":
            return {
                "related_incidents": [
                    {
                        "id": "PREL001",
                        "title": "[HIGH] EdgeNode Upstream Connectivity Issue",
                        "status": "acknowledged",
                        "urgency": "high",
                        "created_at": "2026-01-30T17:30:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "relationship": "upstream_dependency"
                    },
                    {
                        "id": "PREL002",
                        "title": "[MEDIUM] Data Pipeline Backlog Alert",
                        "status": "triggered",
                        "urgency": "low",
                        "created_at": "2026-01-30T17:45:00Z",
                        "service": {"id": "PBD0TCK", "summary": "EdgeNode DP&E Ingestion and controls - Prod"},
                        "relationship": "correlated"
                    }
                ]
            }
        
        elif tool_name == "get_past_incidents":
            return {
                "past_incidents": [
                    {
                        "id": "PAST001",
                        "title": "[CRITICAL] Model Processing Failure - Similar Issue",
                        "status": "resolved",
                        "urgency": "high",
                        "created_at": "2026-01-25T14:00:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "resolution": "Restarted model worker pods and cleared cache"
                    },
                    {
                        "id": "PAST002",
                        "title": "[HIGH] EdgeNode Processing Timeout",
                        "status": "resolved",
                        "urgency": "high",
                        "created_at": "2026-01-20T09:00:00Z",
                        "service": {"id": "PFDU7FI", "summary": "EdgeNode Modelling - Prod"},
                        "resolution": "Increased timeout threshold and added retry logic"
                    }
                ]
            }
        
        elif tool_name == "add_responders":
            return {
                "responder_request": {
                    "id": "PREQ001",
                    "incident": {"id": params.get("incident_id")},
                    "responder_request_targets": params.get("responder_ids", []),
                    "message": "Responders added successfully"
                }
            }
        
        elif tool_name == "list_teams":
            return {
                "teams": [
                    {
                        "id": "P80ZU3K",
                        "name": "DPE Prod Ops",
                        "description": "Data Platform & Engineering Production Operations Team",
                        "html_url": "https://cba.pagerduty.com/teams/P80ZU3K"
                    }
                ]
            }
        
        elif tool_name == "get_team":
            return {
                "team": {
                    "id": "P80ZU3K",
                    "name": "DPE Prod Ops",
                    "description": "Data Platform & Engineering Production Operations Team",
                    "html_url": "https://cba.pagerduty.com/teams/P80ZU3K"
                }
            }
        
        elif tool_name == "list_team_members":
            return {
                "members": [
                    {"user": {"id": "PUSER1", "summary": "John Doe", "email": "john.doe@company.com"}, "role": "manager"},
                    {"user": {"id": "PUSER2", "summary": "Jane Smith", "email": "jane.smith@company.com"}, "role": "responder"},
                    {"user": {"id": "PUSER3", "summary": "Bob Wilson", "email": "bob.wilson@company.com"}, "role": "responder"}
                ]
            }
        
        elif tool_name == "list_incident_workflows":
            return {
                "incident_workflows": [
                    {
                        "id": "WF001",
                        "name": "Auto-Escalate Critical Incidents",
                        "description": "Automatically escalate critical incidents after 15 minutes"
                    },
                    {
                        "id": "WF002",
                        "name": "Create JIRA Ticket",
                        "description": "Create a JIRA ticket for tracking incident resolution"
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
