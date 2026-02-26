Kindly get me the below section "High-Level Operational Cycle" (totally it contain 7 process) into an .excalidraw visual diagram 


High-Level Operational Cycle (repeats continuously)

1. Incident Creation in PagerDuty
Monitoring system (Datadog, New Relic, Prometheus, etc.) detects anomaly
→ creates triggered incident in PagerDuty (urgency = high / severity = critical or high)
→ PagerDuty notifies on-call person via push / email / phone (as usual)

2. Polling Detection (your local Python process)
Every ~60 seconds (configurable via POLL_INTERVAL_SECONDS)
Your run.py script calls the local PagerDuty MCP tool:
pagerduty_mcp_call("list_incidents", {"statuses": ["triggered"], "urgencies": ["high"], "since": last_check_timestamp, ...})
MCP Server → translates to real PagerDuty REST API call (using your stored PD API token)
Returns list of new matching incidents since last poll

3.New High-Severity Incident Detected
If no new incidents → loop sleeps again
If 1+ new high-urgency triggered incidents appear → process each one independently

4.Agent Invocation per Incident (LangGraph ReAct loop)
For each incident (identified by incident_id):
LangGraph creates/loads thread memory using thread_id = "incident_{inc_id}" (so it remembers previous reasoning for the same incident across poll cycles)
Initial user message sent to Claude-4.5-sonnet:
"New incident arrived: ID=XXXX. Investigate, decide action."
ReAct-style reasoning loop begins (can run 5–20+ internal turns depending on complexity):a. LLM thinks → decides it needs more context
b. Calls tool → pagerduty_mcp_call("get_incident", {"id": "PXXXXXX"})
→ MCP Server fetches full incident details (title, description, service, urgency, status, HTML_url, etc.)
c. LLM receives data → thinks again → calls more tools, examples:
list_alerts_for_incident or get_service
list_oncall_users / get_schedule (to know who is on-call)
list_recent_incidents for the same service (pattern matching)
get_notes or list_incident_timeline
d. If you later added runbook RAG tool → LLM calls search_runbooks("database latency spikes")
e. LLM evaluates confidence internally based on prompt instructions
f. Eventually reaches decision point → outputs final structured JSON block (as enforced in system prompt)


5.Decision & Action Phase
LLM final output contains (among other fields):JSON{
  "incident_id": "PXXXXXX",
  "decision": "auto_ack_and_note" | "auto_remediate" | "escalate_with_note" | "escalate_only",
  "confidence": 92,
  "summary_for_teams": "... markdown ...",
  "actions_taken": ["get_incident", "acknowledge_incident", "add_note"],
  "next_steps_recommended": "..."
}Your code currently only reads — to enable real actions you would:
Gate write calls behind high confidence + human approval (e.g., post proposal to Teams → wait for reaction)
Or (riskier, for true auto-resolve) directly call write tools like:
pagerduty_mcp_call("acknowledge_incident", {"id": "...", "note": "Auto-acknowledged by AI Co-Pilot – investigating DB connection pool exhaustion"})
or even resolve_incident / run remediation via another MCP (Kubernetes / AWS, etc.)

6.Output to Microsoft Teams
Script formats nice markdown message:
"AI Co-Pilot Report
Incident: PXXXXXX – API latency > 500msDecision: escalate_with_note
Confidence: 92%
Summary: ...
Actions taken: fetched details, checked on-call, added diagnostic note
Next steps: ..."
Sends via Incoming Webhook to your configured Teams channel
→ Team sees near real-time AI triage / summary / suggested next steps
→ Reduces need to open PagerDuty UI immediately for many P2/P3 alerts

7.Loop Continues – Statefulness
Next poll (60 s later) → same incident still triggered?
Agent re-loads thread memory → sees previous actions & reasoning
→ can continue (e.g. "still no resolution after 5 min → escalate further" or "metrics improved → propose resolve")
Once resolved (manually or auto) → no longer appears in triggered list → processing stops for that ID
