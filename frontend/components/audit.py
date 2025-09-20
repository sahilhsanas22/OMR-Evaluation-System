"""
Audit page for OMR Evaluation System
"""
import streamlit as st
import pandas as pd
from utils.database import get_audit_logs_cached

def show_audit():
    """Display the audit page"""
    st.markdown('<h1 class="main-header">🔍 Audit Logs</h1>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        action_filter = st.selectbox("🎯 Action", ["All", "INSERT", "UPDATE", "DELETE"])
    with col2:
        table_filter = st.selectbox("📊 Table", ["All", "results", "metadata", "audit_logs"])
    with col3:
        limit = st.number_input("📈 Records", min_value=10, max_value=100, value=25)
    
    with st.spinner("Loading audit logs..."):
        logs = get_audit_logs_cached(limit=limit)
    
    if logs:
        df = pd.DataFrame(logs)

        if action_filter != "All":
            df = df[df['action'] == action_filter]
        if table_filter != "All":
            df = df[df['table_name'] == table_filter]

        st.markdown(f"### 📋 Showing {len(df)} audit records")

        audit_display = df[['timestamp', 'action', 'table_name', 'record_id']].copy()
        audit_display['timestamp'] = pd.to_datetime(audit_display['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(audit_display, use_container_width=True, hide_index=True)
    else:
        st.info("🔍 No audit logs found.")