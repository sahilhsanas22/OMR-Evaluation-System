"""
Dashboard page for OMR Evaluation System
"""
import streamlit as st
import pandas as pd
from utils.database import get_statistics, get_all_results_cached

def show_dashboard():
    st.markdown('<h1 class="main-header">📊 OMR Evaluation Dashboard</h1>', unsafe_allow_html=True)

    with st.spinner("Loading dashboard..."):
        stats = get_statistics()

    st.markdown("### 📈 System Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h2>📋 {stats['total_results']}</h2>
            <p>Total Results</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="success-card">
            <h2>🎯 {stats['average_score']}%</h2>
            <p>Average Score</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="info-card">
            <h2>🔥 {stats['recent_activity']}</h2>
            <p>Recent Activity</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        processing_count = stats['status_counts'].get('completed', 0)
        st.markdown(f'''
        <div class="warning-card">
            <h2>✅ {processing_count}</h2>
            <p>Processed</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🔄 Processing Status")
        if stats['status_counts']:
            status_col1, status_col2 = st.columns(2)
            status_items = list(stats['status_counts'].items())
            
            for i, (status, count) in enumerate(status_items):
                target_col = status_col1 if i % 2 == 0 else status_col2
                with target_col:
                    status_icons = {
                        'pending': '⏳',
                        'processing': '🔄', 
                        'completed': '✅',
                        'error': '❌'
                    }
                    icon = status_icons.get(status, '📊')
                    st.metric(
                        label=f"{icon} {status.title()}", 
                        value=count,
                        help=f"Number of {status} results"
                    )
        else:
            st.info("No status data available")
    
    with col2:
        st.markdown("### 📊 Quick Overview")
        processing_count = stats['status_counts'].get('completed', 0)
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.metric(
                label="📋 Total Results", 
                value=stats['total_results'],
                help="Total number of OMR sheets processed"
            )
            st.metric(
                label="🔥 Recent Activity", 
                value=stats['recent_activity'],
                help="Activity in last 7 days"
            )
        
        with metric_col2:
            st.metric(
                label="🎯 Average Score", 
                value=f"{stats['average_score']}%",
                help="Overall average score across all results"
            )
            st.metric(
                label="✅ Completed", 
                value=processing_count,
                help="Successfully processed results"
            )
    
    # Recent results with caching and limit
    st.markdown("### 📋 Recent Results")
    with st.spinner("Loading recent results..."):
        recent_results = get_all_results_cached()[:3] 
    
    if recent_results:
        results_data = []
        for result in recent_results:
            results_data.append({
                'ID': result['id'],
                'Student': result['student_id'],
                'Exam': result['exam_id'],
                'Score': result['score'] or 'N/A',
                'Status': result['processing_status'],
                'Created': result['created_at'][:10] 
            })
        
        df_recent = pd.DataFrame(results_data)
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.info("🎯 No results yet! Upload some OMR sheets to get started.")