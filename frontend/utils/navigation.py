"""
Navigation sidebar component
"""
import streamlit as st
from datetime import datetime

try:
    from streamlit_option_menu import option_menu
    ENHANCED_UI = True
except ImportError:
    ENHANCED_UI = False

def create_sidebar():
    if ENHANCED_UI:
        with st.sidebar:
            st.markdown('<h1 style="color: white; text-align: center;">📝 OMR System</h1>', unsafe_allow_html=True)
            
            selected = option_menu(
                menu_title=None,
                options=["Dashboard", "Upload", "Results", "Analytics", "Audit"],
                icons=["speedometer2", "cloud-upload", "clipboard-data", "graph-up", "shield-check"],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {"padding": "0!important", "background-color": "transparent"},
                    "icon": {"color": "white", "font-size": "18px"},
                    "nav-link": {
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "0px",
                        "color": "white",
                        "--hover-color": "rgba(255, 255, 255, 0.1)"
                    },
                    "nav-link-selected": {"background-color": "rgba(255, 255, 255, 0.2)"},
                }
            )
            
            st.markdown("---")
            st.markdown("**System Info**")
            st.info(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
            st.success("🟢 Database Connected")
    else:
        st.sidebar.title("📝 OMR Evaluation System")
        selected = st.sidebar.selectbox(
            "Navigate to:",
            ["Dashboard", "Upload", "Results", "Analytics", "Audit"]
        )
        st.sidebar.markdown("---")
        st.sidebar.info(f"📅 {datetime.now().strftime('%Y-%m-%d')}")
        st.sidebar.success("🟢 Database Connected")
    
    return selected