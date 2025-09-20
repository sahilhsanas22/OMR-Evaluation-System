"""
Database utilities and caching functions
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import DatabaseManager

@st.cache_resource
def init_database():
    return DatabaseManager()

@st.cache_data(ttl=30)  
def get_statistics():
    db = init_database()
    return db.get_statistics()

@st.cache_data(ttl=60)
def get_all_results_cached():
    db = init_database()
    return db.get_all_results()

@st.cache_data(ttl=60)
def get_results_by_exam_cached(exam_id):
    db = init_database()
    return db.get_results_by_exam(exam_id)

@st.cache_data(ttl=300)
def get_audit_logs_cached(limit=50):
    db = init_database()
    return db.get_audit_logs(limit)

@st.cache_data
def load_lottieurl(url):
    try:
        import requests
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None