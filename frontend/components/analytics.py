"""
Analytics page for OMR Evaluation System
"""
import streamlit as st
import pandas as pd
from utils.database import get_all_results_cached

def show_analytics():
    """Display the analytics page"""
    st.markdown('<h1 class="main-header">📈 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    with st.spinner("Loading analytics..."):
        results = get_all_results_cached()
    
    if results:
        df = pd.DataFrame(results)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Basic Statistics")
            if 'score' in df.columns and df['score'].notna().any():
                avg_score = df['score'].mean()
                max_score = df['score'].max()
                min_score = df['score'].min()
                
                st.metric("Average Score", f"{avg_score:.1f}%")
                st.metric("Highest Score", f"{max_score}%")
                st.metric("Lowest Score", f"{min_score}%")
        
        with col2:
            st.markdown("### 📈 Summary")
            total_results = len(df)
            completed = len(df[df['processing_status'] == 'completed'])
            pending = len(df[df['processing_status'] == 'pending'])
            
            st.metric("Total Results", total_results)
            st.metric("Completed", completed)
            st.metric("Pending", pending)

        if 'score' in df.columns and df['score'].notna().any() and len(df) > 0:
            st.markdown("### 📈 Score Distribution")

            score_counts = df['score'].value_counts().sort_index()
            if len(score_counts) > 0:
                st.bar_chart(score_counts)
    else:
        st.info("📊 No data available for analytics yet!")