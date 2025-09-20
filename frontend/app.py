import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.config import setup_page_config, load_custom_css
from utils.navigation import create_sidebar

from components.dashboard import show_dashboard
from components.upload import show_upload
from components.results import show_results
from components.analytics import show_analytics
from components.audit import show_audit

def main():
    setup_page_config()
    
    load_custom_css()
    
    selected_page = create_sidebar()
    
    if selected_page == "Dashboard":
        show_dashboard()
    elif selected_page == "Upload":
        show_upload()
    elif selected_page == "Results":
        show_results()
    elif selected_page == "Analytics":
        show_analytics()
    elif selected_page == "Audit":
        show_audit()
    
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <h3>🚀 OMR Evaluation System v2.0</h3>
            <p>Built with ❤️ using Streamlit | Powered by Python & SQLite</p>
            <p>Modular Architecture for Better Maintainability</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()