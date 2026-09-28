import streamlit as st
import asyncio
import json
import httpx
from datetime import datetime
from typing import Dict, List, Any
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="SentinelCore - Incident Command & RCA",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_BASE_URL = "http://backend:8000/api/v1"

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    .sub-header {
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    .card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #334155;
    }
    .card-title {
        font-size: 1.125rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .live-badge {
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    .status-healthy { color: #34d399; }
    .status-degraded { color: #fbbf24; }
    .status-critical { color: #f87171; animation: pulse 2s infinite; }
    .log-entry {
        display: flex;
        gap: 1rem;
        padding: 0.5rem;
        border-radius: 6px;
        transition: background-color 0.2s;
        font-family: monospace;
        font-size: 0.875rem;
    }
    .log-entry:hover { background-color: #334155; }
    .log-time { color: #64748b; width: 80px; flex-shrink: 0; }
    .log-service { font-weight: 600; color: #cbd5e1; width: 120px; flex-shrink: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .log-message { color: #94a3b8; flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .log-level-info { color: #60a5fa; }
    .log-level-warn { color: #fbbf24; }
    .log-level-error { color: #f87171; }
    .log-level-fatal { color: #f87171; animation: pulse 1s infinite; }
    .agent-thought {
        padding-left: 1.5rem;
        border-left: 2px solid #334155;
        margin-bottom: 1.5rem;
        position: relative;
    }
    .agent-thought::before {
        content: '';
        position: absolute;
        left: -6px;
        top: 4px;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: rgba(59, 130, 246, 0.2);
        border: 2px solid rgba(59, 130, 246, 0.3);
    }
    .agent-thought-content {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
    }
    .agent-name { color: #93c5fd; font-weight: 600; font-size: 0.875rem; }
    .agent-time { color: #64748b; font-size: 0.75rem; }
    .agent-message { color: #cbd5e1; font-size: 0.875rem; line-height: 1.6; }
    .rca-section h4 { color: #a5b4fc; font-weight: 600; margin-bottom: 0.5rem; }
    .rca-text { color: #cbd5e1; font-size: 0.875rem; line-height: 1.7; }
    .confidence-badge {
        background: rgba(52, 211, 153, 0.1);
        color: #34d399;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'agent_thoughts' not in st.session_state:
    st.session_state.agent_thoughts = [
        {"id": 1, "time": "10:00:00", "agent": "LeadOrchestrator", "message": "Incident detected. Initiating diagnostic workflow..."},
        {"id": 2, "time": "10:00:02", "agent": "LogAnalyzer", "message": "Analyzing burst of 5xx errors in auth-service."},
        {"id": 3, "time": "10:00:05", "agent": "MetricsAgent", "message": "High CPU detected on payment-gateway prior to crash."}
    ]
if 'health_nodes' not in st.session_state:
    st.session_state.health_nodes = [
        {"name": "auth-service", "status": "critical", "icon": "Shield"},
        {"name": "payment-gateway", "status": "degraded", "icon": "Globe"},
        {"name": "user-db", "status": "healthy", "icon": "Database"},
        {"name": "frontend-proxy", "status": "healthy", "icon": "Server"}
    ]

def get_status_class(status: str) -> str:
    return f"status-{status}"

def get_status_icon(status: str) -> str:
    icons = {"healthy": "●", "degraded": "●", "critical": "●"}
    return icons.get(status, "●")

def render_health_grid():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-header">
        <span class="card-title">Service Health</span>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    for idx, node in enumerate(st.session_state.health_nodes):
        with cols[idx]:
            status_class = get_status_class(node["status"])
            icon = get_status_icon(node["status"])
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #0f172a; border-radius: 12px; border: 1px solid #334155;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{node['icon']}</div>
                <div style="font-weight: 500; color: #e2e8f0; font-size: 0.875rem; margin-bottom: 0.25rem;">{node['name']}</div>
                <div class="{status_class}" style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">
                    {icon} {node['status'].capitalize()}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_telemetry_stream():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-header">
        <span class="card-title">Live Telemetry</span>
        <span class="live-badge">● Live</span>
    </div>
    """, unsafe_allow_html=True)
    
    log_container = st.container(height=300, border=False)
    
    with log_container:
        if st.session_state.logs:
            for log in reversed(st.session_state.logs[-50:]):
                level_class = f"log-level-{log['level'].lower()}"
                level_icons = {"INFO": "INFO", "WARN": "WARN", "ERROR": "ERROR", "FATAL": "FATAL"}
                icon = level_icons.get(log['level'], "LOG")
                st.markdown(f"""
                <div class="log-entry">
                    <span class="log-time">{log['timestamp']}</span>
                    <span class="{level_class}">{icon}</span>
                    <span class="log-service">{log['service']}</span>
                    <span class="log-message">{log['message']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; color: #64748b; padding: 2rem;">Awaiting telemetry...</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_agent_timeline():
    st.markdown('<div class="card" style="height: 100%; display: flex; flex-direction: column;">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-header">
        <span class="card-title">Agent Swarm</span>
        <span style="display: flex; gap: 0.25rem;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #3b82f6; animation: pulse 1.5s infinite;"></span>
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #3b82f6;"></span>
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    timeline_container = st.container()
    with timeline_container:
        for idx, thought in enumerate(st.session_state.agent_thoughts):
            is_last = idx == len(st.session_state.agent_thoughts) - 1
            st.markdown(f"""
            <div class="agent-thought">
                <div class="agent-thought-content">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span class="agent-name">{thought['agent']}</span>
                        <span class="agent-time">{thought['time']}</span>
                    </div>
                    <p class="agent-message">{thought['message']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_rca_report():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="card-header">
        <span class="card-title">RCA Report</span>
        <span class="confidence-badge">92% Confidence</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="rca-section">
        <h3 style="color: #f1f5f9; font-weight: 700; margin-bottom: 1rem;">Auth Service Degradation</h3>
        
        <h4>Root Cause</h4>
        <p class="rca-text">
            A recent database migration executed an <code>ALTER TABLE</code> operation on the <code>users</code> table, 
            triggering a table lock. This exhausted connection pools in the <code>auth-service</code>, 
            resulting in a cascading failure of 5xx errors.
        </p>
        
        <h4 style="margin-top: 1rem;">Remediation Steps</h4>
        <ul class="rca-text" style="padding-left: 1.5rem;">
            <li>Kill the blocking database migration transaction.</li>
            <li>Restart <code>auth-service</code> pods to clear dead connections.</li>
            <li>Schedule heavy migrations during maintenance windows.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

async def fetch_telemetry_stream():
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("GET", f"{API_BASE_URL}/stream/telemetry") as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        log_entry = {
                            "timestamp": datetime.fromisoformat(data.get("timestamp", datetime.utcnow().isoformat())).strftime("%H:%M:%S"),
                            "level": data.get("level", "INFO"),
                            "service": data.get("service", "unknown"),
                            "message": data.get("message", "")
                        }
                        st.session_state.logs.append(log_entry)
                        if len(st.session_state.logs) > 100:
                            st.session_state.logs = st.session_state.logs[-100:]
    except Exception as e:
        pass

async def fetch_agent_stream():
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            async with client.stream("GET", f"{API_BASE_URL}/stream/agents") as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        thought = {
                            "id": len(st.session_state.agent_thoughts) + 1,
                            "time": datetime.utcnow().strftime("%H:%M:%S"),
                            "agent": data.get("agent", "Unknown"),
                            "message": data.get("message", "")
                        }
                        st.session_state.agent_thoughts.append(thought)
    except Exception as e:
        pass

def trigger_incident_workflow(incident_description: str):
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                f"{API_BASE_URL}/agents/trigger",
                json={"incident_description": incident_description}
            )
            if response.status_code == 200:
                st.success("Workflow triggered successfully!")
            else:
                st.error(f"Failed to trigger workflow: {response.text}")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def main():
    st.markdown('<h1 class="main-header">SentinelCore</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Incident Command & Root Cause Analysis</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        render_health_grid()
        render_telemetry_stream()
        render_rca_report()
    
    with col2:
        render_agent_timeline()
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("""
        <div class="card-header">
            <span class="card-title">Trigger Incident</span>
        </div>
        """, unsafe_allow_html=True)
        
        incident_desc = st.text_area(
            "Incident Description",
            placeholder="Describe the incident...",
            height=100,
            label_visibility="collapsed"
        )
        
        if st.button("Trigger Workflow", use_container_width=True, type="primary"):
            if incident_desc:
                trigger_incident_workflow(incident_desc)
            else:
                st.warning("Please enter an incident description")
        
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Refresh Data", use_container_width=False):
        st.rerun()

if __name__ == "__main__":
    main()