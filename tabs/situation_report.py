# tabs/situation_report.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import os
import json
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected
from utils.local_storage import save_file, get_file_size

def show():
    """Display Complete Situation Report Tab with all sections"""
    
    st.markdown("# 📡 SITUATION REPORT")
    st.caption("Official MPDRRMC Situation Report Form with Complete Sections")
    
    # Initialize session state for all data
    init_session_state()
    
    # Load existing data from cloud
    load_sitreps_from_cloud()
    
    # ===== RISK COMMUNICATION MONITOR (OUTSIDE FORM) =====
    show_risk_communication_monitor()
    
    # ===== EARLY FLOOD WARNING SYSTEM (OUTSIDE FORM) =====
    show_early_flood_warning_system()
    
    # ===== PHOTO DOCUMENTATION (OUTSIDE FORM) =====
    show_photo_documentation()
    
    # ===== MAIN FORM STARTS HERE =====
    with st.form("situation_report_form", clear_on_submit=False):
        
        # ===== HEADER SECTION =====
        show_header_section()
        
        # ===== SECTION I: SITUATION OVERVIEW =====
        show_situation_overview()
        
        # ===== SECTION II: RISK AND IMPACT ASSESSMENT =====
        show_risk_impact_assessment()
        
        # ===== SECTION III: PDRA - PROBABILITY & IMPACT RATINGS =====
        show_pdra_ratings()
        
        # ===== SECTION IV: INCIDENTS MONITORED =====
        show_incidents_monitored()
        
        # ===== SECTION V: STATUS OF LIFELINES =====
        show_lifelines_status()
        
        # ===== SECTION VI: DISPLACED POPULATION & DAMAGES =====
        show_displaced_damages()
        
        # ===== SECTION VII: RESOURCES PROVIDED =====
        show_resources_provided()
        
        # ===== SECTION VIII: RESPONSE ACTIONS =====
        show_response_actions()
        
        # ===== SECTION IX: NEEDS ASSESSMENT =====
        show_needs_assessment()
        
        # ===== SUBMIT BUTTON =====
        st.markdown("---")
        submitted = st.form_submit_button("💾 Save Situation Report", type="primary", use_container_width=True)
        
        if submitted:
            save_complete_report()
            st.success("✅ Situation Report saved successfully!")
            st.balloons()
            st.rerun()


def init_session_state():
    """Initialize all session state variables"""
    # [Keep all your existing initialization code here]
    pass


def load_sitreps_from_cloud():
    """Load saved sitreps from Supabase"""
    # [Keep existing code]
    pass


def show_header_section():
    """Display professional letterhead header"""
    # [Keep existing code]
    pass


def show_situation_overview():
    """Section I: Situation Overview with weather table"""
    # [Keep existing code - already fixed]
    pass


def show_risk_communication_monitor():
    """Section for tracking issuances and communications - OUTSIDE FORM"""
    
    st.markdown("### II. RISK COMMUNICATION MONITOR")
    st.caption("Tracking of advisories, memoranda, and their dissemination")
    
    # Add new issuance - using columns outside form
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1.5, 1, 1, 0.5])
    with col1:
        new_issuance = st.text_input("Issuance", placeholder="e.g., Cordillera RDRRMC Memo No. 25", key="new_issuance")
    with col2:
        rec_date = st.date_input("Rec Date", date.today(), key="rec_date")
    with col3:
        rec_time = st.time_input("Rec Time", datetime.now().time(), key="rec_time")
    with col4:
        action = st.selectbox("Action", ["✓", "✗", "Pending"], key="action_select")
    with col5:
        diss_date = st.date_input("Diss Date", date.today(), key="diss_date")
    with col6:
        diss_time = st.time_input("Diss Time", datetime.now().time(), key="diss_time")
    with col7:
        if st.button("➕ Add", key="add_issuance_btn"):
            if new_issuance:
                st.session_state.risk_communications.append({
                    "issuance": new_issuance,
                    "received_date": rec_date.isoformat(),
                    "received_time": rec_time.strftime("%H:%M"),
                    "action": action,
                    "disseminated_date": diss_date.isoformat(),
                    "disseminated_time": diss_time.strftime("%H:%M")
                })
                st.rerun()
    
    # Display existing issuances
    if st.session_state.risk_communications:
        st.markdown("#### Current Issuances")
        
        for i, comm in enumerate(st.session_state.risk_communications):
            col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 0.5])
            with col1:
                st.markdown(comm['issuance'])
            with col2:
                st.markdown(comm['received_date'])
            with col3:
                st.markdown(comm['received_time'])
            with col4:
                st.markdown(comm['action'])
            with col5:
                st.markdown(comm['disseminated_date'])
            with col6:
                st.markdown(comm['disseminated_time'])
            with col7:
                if st.button("🗑️", key=f"del_issuance_{i}"):
                    st.session_state.risk_communications.pop(i)
                    st.rerun()
    
    st.markdown("---")


def show_risk_impact_assessment():
    """Risk and Impact Assessment table for landslides and flooding"""
    # [Keep existing code - already fixed]
    pass


def show_early_flood_warning_system():
    """Early Flood Warning System table - OUTSIDE FORM"""
    
    st.markdown("### IV. EARLY FLOOD WARNING SYSTEM")
    st.caption("Monitoring stations and water level indicators for major river basins")
    
    # Add new river basin - using columns outside form
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns([1.5, 1, 1.5, 1, 1.5, 1, 1, 1, 0.5])
    with col1:
        new_river = st.text_input("River Basin", placeholder="New river basin", key="new_river")
    with col2:
        new_drainage = st.number_input("Drainage (ha)", min_value=0, value=0, key="new_drainage")
    with col3:
        new_headwater = st.text_input("Head Water", key="new_headwater")
    with col4:
        new_watershed = st.number_input("Watershed (ha)", min_value=0, value=0, key="new_watershed")
    with col5:
        new_station = st.text_input("Monitoring Station", key="new_station")
    with col6:
        new_yellow = st.text_input("Yellow Line", placeholder="Alert/Ready", key="new_yellow")
    with col7:
        new_orange = st.text_input("Orange Line", placeholder="Pre-emptive evacuation", key="new_orange")
    with col8:
        new_red = st.text_input("Red Line", placeholder="Evacuation", key="new_red")
    with col9:
        if st.button("➕ Add", key="add_river_btn"):
            if new_river:
                st.session_state.flood_warning_systems.append({
                    "river_basin": new_river,
                    "drainage_area": new_drainage,
                    "head_water": new_headwater,
                    "watershed_area": new_watershed,
                    "monitoring_station": new_station,
                    "yellow_line": new_yellow,
                    "orange_line": new_orange,
                    "red_line": new_red
                })
                st.rerun()
    
    # Display existing river basins
    st.markdown("#### River Basins Monitoring")
    
    for i, river in enumerate(st.session_state.flood_warning_systems):
        with st.expander(f"🌊 {river['river_basin']}", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                drainage = st.number_input("Drainage Area (ha)", value=river['drainage_area'], key=f"drainage_{i}")
                headwater = st.text_input("Head Water", value=river['head_water'], key=f"headwater_{i}")
                watershed = st.number_input("Watershed Area (ha)", value=river['watershed_area'], key=f"watershed_{i}")
            with col2:
                station = st.text_input("Monitoring Station", value=river['monitoring_station'], key=f"station_{i}")
                yellow = st.text_input("Yellow Line", value=river['yellow_line'], key=f"yellow_{i}")
                orange = st.text_input("Orange Line", value=river['orange_line'], key=f"orange_{i}")
                red = st.text_input("Red Line", value=river['red_line'], key=f"red_{i}")
            
            # Update values
            river['drainage_area'] = drainage
            river['head_water'] = headwater
            river['watershed_area'] = watershed
            river['monitoring_station'] = station
            river['yellow_line'] = yellow
            river['orange_line'] = orange
            river['red_line'] = red
            
            if st.button(f"🗑️ Delete", key=f"del_river_{i}"):
                st.session_state.flood_warning_systems.pop(i)
                st.rerun()
    
    st.markdown("---")


def show_pdra_ratings():
    """Probability and Impact Rating Scales under PDRA"""
    # [Keep existing code]
    pass


def show_incidents_monitored():
    """Section II: Incidents Monitored"""
    # [Keep existing code]
    pass


def show_lifelines_status():
    """Section III: Status of Lifelines"""
    # [Keep existing code]
    pass


def show_displaced_damages():
    """Section IV: Displaced Population & Damages"""
    # [Keep existing code]
    pass


def show_resources_provided():
    """Section V: Resources Provided"""
    # [Keep existing code]
    pass


def show_response_actions():
    """Section VI: Response Actions"""
    # [Keep existing code]
    pass


def show_photo_documentation():
    """Photo Documentation - OUTSIDE FORM"""
    
    st.markdown("### XI. PHOTO DOCUMENTATION")
    
    # Upload new photo - using columns outside form
    col1, col2, col3, col4 = st.columns([2, 2, 1, 0.5])
    with col1:
        photo = st.file_uploader("Select Photo", type=['jpg', 'jpeg', 'png'], key="new_photo")
    with col2:
        caption = st.text_input("Caption", key="photo_caption")
    with col3:
        location = st.text_input("Location", key="photo_location")
    with col4:
        if st.button("📸 Add", key="add_photo_btn"):
            if photo:
                st.session_state.photos.append({
                    "file": photo.name,
                    "caption": caption,
                    "location": location,
                    "uploaded_at": datetime.now().isoformat()
                })
                st.rerun()
    
    # Display existing photos
    if st.session_state.photos:
        for i, photo_item in enumerate(st.session_state.photos):
            col1, col2, col3, col4 = st.columns([2, 2, 2, 0.5])
            with col1:
                st.markdown(f"**Photo:** {photo_item['file']}")
            with col2:
                st.markdown(f"**Caption:** {photo_item['caption']}")
            with col3:
                st.markdown(f"**Location:** {photo_item['location']}")
            with col4:
                if st.button("🗑️", key=f"del_photo_{i}"):
                    st.session_state.photos.pop(i)
                    st.rerun()
    
    st.markdown("---")


def show_needs_assessment():
    """Section XII: Needs Assessment"""
    # [Keep existing code]
    pass


def save_complete_report():
    """Save the complete report to session state and cloud"""
    # [Keep existing code]
    pass