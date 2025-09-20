"""
Results page for OMR Evaluation System
"""
import streamlit as st
import pandas as pd
from utils.database import get_results_by_exam_cached, get_all_results_cached, init_database

def show_results():
    """Display the results page"""
    st.markdown('<h1 class="main-header">📋 Review Results</h1>', unsafe_allow_html=True)

    st.markdown("### 🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        exam_filter = st.text_input("🔎 Exam ID", placeholder="Filter by exam")
    
    with col2:
        status_filter = st.selectbox("📊 Status", 
                                   ["All", "pending", "processing", "completed", "error"])
    
    with col3:
        limit_results = st.number_input("📈 Limit", min_value=5, max_value=100, value=20)
    
    with col4:
        if st.button("🔄 Refresh", type="secondary"):
            st.cache_data.clear()  
            st.rerun()

    with st.spinner("Loading results..."):
        if exam_filter:
            results = get_results_by_exam_cached(exam_filter)
        else:
            results = get_all_results_cached()
    
    if status_filter != "All":
        results = [r for r in results if r['processing_status'] == status_filter]

    results = results[:limit_results]
    
    if results:
        st.markdown(f"### 📊 Found {len(results)} results")

        results_data = []
        for result in results:
            results_data.append({
                'ID': result['id'],
                'Student ID': result['student_id'],
                'Exam ID': result['exam_id'],
                'Score': result['score'] or 'N/A',
                'Status': result['processing_status'],
                'Questions': result['total_questions'] or 'N/A',
                'Created': result['created_at'][:16] if result['created_at'] else 'N/A'  # Date + time
            })
        
        df_results = pd.DataFrame(results_data)

        selected_rows = st.dataframe(
            df_results, 
            use_container_width=True, 
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row"
        )
        
        if selected_rows and len(selected_rows.selection.rows) > 0:
            selected_idx = selected_rows.selection.rows[0]
            selected_result = results[selected_idx]
            
            st.markdown("### 📄 Result Details")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Student ID", selected_result['student_id'])
                st.metric("Exam ID", selected_result['exam_id'])
            
            with col2:
                st.metric("Score", f"{selected_result['score'] or 'N/A'}")
                st.metric("Status", selected_result['processing_status'])
            
            with col3:
                st.metric("Questions", selected_result['total_questions'] or 'N/A')
                st.write(f"**Created:** {selected_result['created_at']}")
    else:
        st.info("🔍 No results found matching your criteria.")