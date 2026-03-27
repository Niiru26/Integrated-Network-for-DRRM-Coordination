"""
INDC - Integrated Network for DRRM Coordination
Main Application Entry Point
"""

import streamlit as st
import pandas as pd
from tabs.drrm_intelligence import show as show_drrm    
from utils.database import init_session_state
from tabs.plan_management import show as show_plan_management
from tabs.about_indc import show as show_about_indc     
from tabs.situation_report import show as show_situation_report
from tabs.trainings import show as show_trainings       
from tabs.ldrrmf_utilization import show as show_ldrrmf 
from utils.project_state import create_state_snapshot_button
from utils.supabase_client import is_connected, sync_all

# Page configuration
st.set_page_config(
    page_title="INDC - DRRM Coordination System",       
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Auto-sync on startup (once per session)
if 'auto_synced' not in st.session_state:
    try:
        if is_connected():
            with st.spinner("Syncing with cloud..."):
                sync_all()
            st.success("✅ Connected to cloud")
        else:
            st.warning("⚠️ Offline mode - using local storage")
    except Exception as e:
        st.warning(f"⚠️ Cloud connection issue: {e}")
    st.session_state.auto_synced = True

# Custom CSS for metrics
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    # ===== LOGO AND TITLE SECTION =====
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("mpdrrmc_logo.png", width=100, use_container_width=False)

    st.markdown("""
    <div style='text-align: center; margin-top: 5px; margin-bottom: 10px;'>
        <h1 style='color: #1E3A8A; margin: 0; padding: 0; font-size: 2rem; font-weight: bold; letter-spacing: 1px; line-height: 1.2;'>MPDRRMO</h1>
        <p style='color: #2563EB; margin: 4px 0 0 0; padding: 0; font-size: 1.3rem; font-weight: 500; line-height: 1.3;'>
            Climate & Disaster Risk<br>Data Governance Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation menu - all tabs available
    menu_options = {
        "🎯 COMMAND CENTER": "dashboard",
        "📊 DRRM INTELLIGENCE": "drrm_intelligence",
        "📋 PLAN MANAGEMENT": "plan_management",  
        "📚 TRAININGS": "trainings",
        "💰 LDRRMF UTILIZATION": "ldrrmf",        
        "📡 SITUATION REPORT": "situation_report",
        "📄 DOCUMENT STUDIO": "document_studio",  
        "🏛️ ABOUT INDC": "about_indc"
    }

    choice = st.radio("Navigation", list(menu_options.keys()), label_visibility="collapsed")

    st.markdown("---")

    # Quick stats
    if 'disaster_events' in st.session_state and not st.session_state.disaster_events.empty:
        st.markdown("### 📊 Quick Stats")
        st.metric("Total Events", len(st.session_state.disaster_events))

        if 'fatalities' in st.session_state.disaster_events.columns:
            st.metric("Total Fatalities", int(st.session_state.disaster_events['fatalities'].sum()))

    # Cloud connection status (just for info)
    st.markdown("---")
    try:
        if is_connected():
            st.success("☁️ Cloud Connected")
        else:
            st.warning("⚠️ Offline Mode - Data saved locally")
    except:
        st.warning("⚠️ Checking connection...")

    # Add the chat continuity button
    create_state_snapshot_button()

    st.markdown("---")
    st.caption("© 2026 MPDRRMO | Mountain Province")   

# Main content routing
if choice == "🎯 COMMAND CENTER":
    st.markdown("<h1 class='main-header'>🎯 COMMAND CENTER</h1>", unsafe_allow_html=True)
    st.markdown("### The MPDRRMO Climate & Disaster Risk Data Governance Platform")
    st.caption("Integrated Network for Disaster Risk Reduction and Climate Change Adaptation")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Incidents", "3")
    with col2:
        st.metric("Response Teams", "12")
    with col3:
        st.metric("Evacuation Centers", "15")
    with col4:
        st.metric("Response Readiness", "78%")

    st.markdown("### 📋 Recent Activities")

    # Safely show activities if there are events        
    if 'disaster_events' in st.session_state and not st.session_state.disaster_events.empty:
        df = st.session_state.disaster_events.head(5)   
        activities = pd.DataFrame({
            'Time': df.get('start_date', ['N/A'] * len(df)),
            'Activity': df.get('local_name', ['N/A'] * len(df)),
            'Status': ['Recorded'] * len(df)
        })
        st.dataframe(activities, width='stretch', hide_index=True)
    else:
        st.info("No recent activities. Add events in DRRM Intelligence tab.")

    # Training Summary on Dashboard
    if "trainings" in st.session_state and st.session_state.trainings:
        st.markdown("### 📚 Recent Trainings")    
        recent_trainings = st.session_state.trainings[-3:]
        for t in recent_trainings:
            st.write(f"**{t.get('title')}** - {t.get('date')} ({t.get('participants')} participants)")      

    # Fund Summary on Dashboard
    if "ldrrmf_records" in st.session_state and st.session_state.ldrrmf_records:
        total_fund = sum(r.get("amount", 0) for r in st.session_state.ldrrmf_records)
        st.metric("Total LDRRMF Utilized", f"₱{total_fund:,.2f}")

elif choice == "📊 DRRM INTELLIGENCE":
    show_drrm()

elif choice == "📋 PLAN MANAGEMENT":
    show_plan_management()

elif choice == "📚 TRAININGS":
    show_trainings()

elif choice == "💰 LDRRMF UTILIZATION":
    show_ldrrmf()

elif choice == "📡 SITUATION REPORT":
    show_situation_report()

elif choice == "📄 DOCUMENT STUDIO":
    st.markdown("<h1 class='main-header'>📄 DOCUMENT STUDIO</h1>", unsafe_allow_html=True)
    st.info("Document Studio tab - Coming Soon")    
    st.markdown("""
    ### Features Coming Soon:
    - AI-powered report generation
    - Document templates
    - Auto-fill from database
    - PDF export
    """)

elif choice == "🏛️ ABOUT INDC":
    show_about_indc()

else:
    st.info("Tab coming soon!")