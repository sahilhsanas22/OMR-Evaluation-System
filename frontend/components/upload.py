"""
Upload page for OMR Evaluation System
"""
import streamlit as st
import os
from utils.database import init_database

def show_upload():
    st.markdown('<h1 class="main-header">📤 Upload OMR Sheets</h1>', unsafe_allow_html=True)

    st.markdown("### 📝 Upload Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        student_id = st.text_input("👤 Student ID", placeholder="Enter student ID", key="student_id")
        exam_id = st.text_input("📚 Exam ID", placeholder="Enter exam ID", key="exam_id")
    
    with col2:
        total_questions = st.number_input("❓ Total Questions", min_value=1, max_value=200, value=50)
        upload_type = st.selectbox("📁 File Type", ["Image (PNG/JPG)", "PDF Document"])
    
    st.markdown("### 📎 File Upload")
    uploaded_files = st.file_uploader(
        "Drop your OMR sheets here or click to browse",
        type=['png', 'jpg', 'jpeg', 'pdf'],
        accept_multiple_files=True,
        help="Supported formats: PNG, JPG, JPEG, PDF"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) selected!")

        if len(uploaded_files) <= 5:  
            cols = st.columns(min(3, len(uploaded_files)))
            for i, file in enumerate(uploaded_files[:3]):
                with cols[i]:
                    st.info(f"📄 {file.name}")
                    st.caption(f"Size: {file.size} bytes")
        else:
            st.info(f"📁 {len(uploaded_files)} files ready for upload")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Upload and Process", type="primary", use_container_width=True):
            if student_id and exam_id and uploaded_files:
                db = init_database()
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, uploaded_file in enumerate(uploaded_files):
                    progress = (i + 1) / len(uploaded_files)
                    progress_bar.progress(progress)
                    status_text.text(f"Processing {uploaded_file.name}...")
                    
                    file_path = os.path.join("uploads", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    result_id = db.insert_result(
                        student_id=student_id,
                        exam_id=exam_id,
                        upload_filename=uploaded_file.name,
                        total_questions=total_questions
                    )
                    
                    db.log_audit("INSERT", "results", result_id, 
                                new_values={"student_id": student_id, "exam_id": exam_id})
                
                progress_bar.progress(1.0)
                status_text.text("✅ All files processed successfully!")
                
                st.balloons()
                st.success("🎉 Upload completed! Files are being processed.")
            else:
                st.error("❌ Please fill in all required fields and select files.")