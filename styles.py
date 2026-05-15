import streamlit as st

def apply_design():
    st.markdown("""
    <style>
    /* Dark Mode Glassmorphism */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card Styling */
    .stMetric, .stAlert, .stMarkdown div[data-testid="stVerticalBlock"] > div {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)