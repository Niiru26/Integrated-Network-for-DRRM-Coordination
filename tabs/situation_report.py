# tabs/situation_report.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import os
import json
import plotly.express as px
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
    
    # Create main form
    with st.form("situation_report_form", clear_on_submit=False):
        
        # ===== HEADER SECTION =====
        show_header_section()
        
        # ===== SECTION I: SITUATION OVERVIEW =====
        show_situation_overview()
        
        # ===== SECTION II: RISK COMMUNICATION MONITOR =====
        show_risk_communication_monitor()
        
        # ===== SECTION III: RISK AND IMPACT ASSESSMENT =====
        show_risk_impact_assessment()
        
        # ===== SECTION IV: EARLY FLOOD WARNING SYSTEM =====
        show_early_flood_warning_system()
        
        # ===== SECTION V: PDRA - PROBABILITY & IMPACT RATINGS =====
        show_pdra_ratings()
        
        # ===== SECTION VI: INCIDENTS MONITORED =====
        show_incidents_monitored()
        
        # ===== SECTION VII: STATUS OF LIFELINES =====
        show_lifelines_status()
        
        # ===== SECTION VIII: DISPLACED POPULATION & DAMAGES =====
        show_displaced_damages()
        
        # ===== SECTION IX: RESOURCES PROVIDED =====
        show_resources_provided()
        
        # ===== SECTION X: RESPONSE ACTIONS =====
        show_response_actions()
        
        # ===== SECTION XI: PHOTO DOCUMENTATION =====
        show_photo_documentation()
        
        # ===== SECTION XII: NEEDS ASSESSMENT =====
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
    
    # Basic info
    if 'sitrep_number' not in st.session_state:
        st.session_state.sitrep_number = 1
    if 'incident_name' not in st.session_state:
        st.session_state.incident_name = ""
    if 'report_date' not in st.session_state:
        st.session_state.report_date = date.today()
    if 'report_time' not in st.session_state:
        st.session_state.report_time = datetime.now().time()
    
    # Weather data for 10 municipalities
    if 'weather_data' not in st.session_state:
        municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                         "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
        st.session_state.weather_data = {mun: {"cloud": "Clear", "wind": "Calm", "precip": "None", "alert": "White"} for mun in municipalities}
    
    # Risk communication monitor
    if 'risk_communications' not in st.session_state:
        st.session_state.risk_communications = []
    
    # Risk assessment data
    if 'risk_assessment' not in st.session_state:
        st.session_state.risk_assessment = {}
    
    # Flood warning system
    if 'flood_warning_systems' not in st.session_state:
        st.session_state.flood_warning_systems = [
            {"river_basin": "Chico River", "drainage_area": 82574, "head_water": "Eastern slopes of Mount Data", 
             "watershed_area": 93984.71, "monitoring_station": "Chico Karayan Bridge", 
             "yellow_line": "Alert/Ready", "orange_line": "Pre-emptive evacuation", "red_line": "Evacuation"},
            {"river_basin": "Mallig River", "drainage_area": 26026, "head_water": "Eastern slope of mountain ranges dividing Paracelis & Natonin", 
             "watershed_area": 11461.55, "monitoring_station": "", "yellow_line": "", "orange_line": "", "red_line": ""},
            {"river_basin": "Siffu River", "drainage_area": 56304, "head_water": "Northeastern slopes of mountain ridges dividing Barlig & Banaue, Ifugao", 
             "watershed_area": 61892.37, "monitoring_station": "", "yellow_line": "", "orange_line": "", "red_line": ""},
            {"river_basin": "Tanudan River", "drainage_area": 25370, "head_water": "Provincial boundary near Mount Polis", 
             "watershed_area": 0, "monitoring_station": "", "yellow_line": "", "orange_line": "", "red_line": ""},
            {"river_basin": "Abit River", "drainage_area": 0, "head_water": "Northern slope of Mount Data, Bauko", 
             "watershed_area": 38969.27, "monitoring_station": "", "yellow_line": "", "orange_line": "", "red_line": ""},
            {"river_basin": "Layaen River", "drainage_area": 0, "head_water": "Besao", 
             "watershed_area": 10607, "monitoring_station": "", "yellow_line": "", "orange_line": "", "red_line": ""}
        ]
    
    # PDRA ratings
    if 'pdra_probability' not in st.session_state:
        st.session_state.pdra_probability = None
    if 'pdra_impact' not in st.session_state:
        st.session_state.pdra_impact = None
    
    # Incidents data
    if 'incidents_data' not in st.session_state:
        municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                         "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
        st.session_state.incidents_data = {mun: {"incidents": "", "casualties": ""} for mun in municipalities}
    
    # Lifelines
    if 'national_roads' not in st.session_state:
        st.session_state.national_roads = [
            {"id": 1, "name": "Bontoc - Baguio Road (S00504LZ)", "sections": []},
            {"id": 2, "name": "Bontoc - Cadre Road (S03996LZ)", "sections": []},
            {"id": 3, "name": "Dantay - Sagada Road (S00509LZ)", "sections": []},
            {"id": 4, "name": "Junction Talubin - Barlig - Natonin - Paracelis - Calaccad Road (S00534LZ)", "sections": []},
            {"id": 5, "name": "Mt. Province - Cagayan via Tabuk - Enrile Road (S00514LZ)", "sections": []},
            {"id": 6, "name": "Mt. Province - Ilocos Sur Road via Kayan (S00531LZ)", "sections": []},
            {"id": 7, "name": "Mt. Province - Ilocos Sur Road via Tue (S00530LZ)", "sections": []},
            {"id": 8, "name": "Mt. Province - Nueva Vizcaya Road (S00512LZ)", "sections": []}
        ]
    
    if 'provincial_roads' not in st.session_state:
        st.session_state.provincial_roads = [
            {"id": 1, "name": "Abatan - Bagnen Road", "status": "Passable", "remarks": ""},
            {"id": 2, "name": "Abatan - Maba-ay Road", "status": "Passable", "remarks": ""},
            {"id": 3, "name": "Balicanao - Am-am Road", "status": "Passable", "remarks": ""},
            {"id": 4, "name": "Bontoc - Mainit Road", "status": "Passable", "remarks": ""},
            {"id": 5, "name": "Bontoc - Maligcong Road", "status": "Passable", "remarks": ""},
            {"id": 6, "name": "Sagada - Payeo Road", "status": "Passable", "remarks": ""},
            {"id": 7, "name": "Tadian - Nacawang Road", "status": "Passable", "remarks": ""},
            {"id": 8, "name": "Natonin - Toboy - Aguinaldo Road", "status": "Passable", "remarks": ""}
        ]
    
    if 'municipal_roads' not in st.session_state:
        st.session_state.municipal_roads = []
    
    if 'barangay_roads' not in st.session_state:
        st.session_state.barangay_roads = []
    
    if 'power_data' not in st.session_state:
        municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                         "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
        st.session_state.power_data = {mun: "Normal" for mun in municipalities}
        st.session_state.comm_data = {mun: "Normal" for mun in municipalities}
    
    # Displaced and damages
    if 'displaced' not in st.session_state:
        st.session_state.displaced = {"families_ec": 0, "persons_ec": 0, "families_out": 0, "persons_out": 0}
    if 'damages' not in st.session_state:
        st.session_state.damages = {"totally_damaged": 0, "partially_damaged": 0, "affected_families": 0, "affected_persons": 0}
    
    # Resources
    if 'resources' not in st.session_state:
        st.session_state.resources = {"food_packs": 0, "hygiene_kits": 0, "family_kits": 0}
    
    # Response
    if 'response_actions' not in st.session_state:
        st.session_state.response_actions = ""
    
    # Photos
    if 'photos' not in st.session_state:
        st.session_state.photos = []
    
    # Needs
    if 'needs' not in st.session_state:
        st.session_state.needs = {"priority1": "", "priority2": "", "priority3": ""}
    
    # Sitreps archive
    if 'saved_sitreps' not in st.session_state:
        st.session_state.saved_sitreps = []


def load_sitreps_from_cloud():
    """Load saved sitreps from Supabase"""
    if is_connected():
        try:
            from utils.supabase_client import get_supabase_client
            client = get_supabase_client()
            if client:
                response = client.table('situation_reports').select('*').execute()
                if response.data:
                    st.session_state.saved_sitreps = response.data
        except Exception as e:
            print(f"Error loading sitreps: {e}")


def show_header_section():
    """Display professional letterhead header"""
    
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h2>REPUBLIC OF THE PHILIPPINES</h2>
        <h3>PROVINCE OF MOUNTAIN PROVINCE</h3>
        <h3>PROVINCIAL DISASTER RISK REDUCTION AND MANAGEMENT COUNCIL</h3>
        <h4>Emergency Operations Center</h4>
        <p>Appong Street, Jungle Town, Poblacion, Bontoc, Mountain Province</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("**TO:** DIR. ALBERT A MOGOL AFP (Ret.)")
        st.markdown("*Regional Director, OCD-CAR & Chairperson, Cordillera RDRRMC*")
        st.markdown("")
        st.markdown("**THRU:** BONIFACIO C. LACWASAN, JR.")
        st.markdown("*Provincial Governor and Chairperson, PDRRMC*")
        st.markdown("")
        st.markdown("**FROM:** ATTY. EDWARD F. CHUMAWAR, JR.")
        st.markdown("*PDRRM Officer*")
    
    with col2:
        sitrep_number = st.number_input("SITREP Number", min_value=1, value=st.session_state.sitrep_number, key="header_sitrep")
        incident_name = st.text_input("Incident Name", value=st.session_state.incident_name, placeholder="e.g., Effects of TS PAENG (NALGAE)", key="header_incident")
        report_date = st.date_input("Report Date", value=st.session_state.report_date, key="header_date")
        report_time = st.time_input("Report Time", value=st.session_state.report_time, key="header_time")
        
        st.session_state.sitrep_number = sitrep_number
        st.session_state.incident_name = incident_name
        st.session_state.report_date = report_date
        st.session_state.report_time = report_time
    
    st.markdown("---")
    st.markdown(f"**SUBJECT:** SITREP #{sitrep_number}: {incident_name}")
    st.markdown(f"**DATE/TIME:** {report_date.strftime('%d %B %Y')}; {report_time.strftime('%H%M')}H")
    st.markdown("---")


def show_situation_overview():
    """Section I: Situation Overview with weather table"""
    
    st.markdown("### I. SITUATION OVERVIEW")
    
    # PAGASA Bulletin
    pagasa_bulletin = st.text_area(
        "PAGASA Tropical Cyclone Bulletin",
        value=st.session_state.get('pagasa_bulletin', ''),
        placeholder="Paste the latest PAGASA bulletin here...",
        height=150,
        key="pagasa_bulletin"
    )
    st.session_state.pagasa_bulletin = pagasa_bulletin
    
    st.markdown("#### Weather & Alert Level Statuses")
    
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                     "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # Create header
    col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
    with col1:
        st.markdown("**Municipality**")
    with col2:
        st.markdown("**Cloud**")
    with col3:
        st.markdown("**Wind**")
    with col4:
        st.markdown("**Precipitation**")
    with col5:
        st.markdown("**Alert Level**")
    
    # Create rows
    for mun in municipalities:
        col1, col2, col3, col4, col5 = st.columns([1.5, 1, 1, 1, 1])
        with col1:
            st.markdown(f"**{mun}**")
        with col2:
            cloud = st.selectbox(
                "Cloud", 
                ["Clear", "Partly Cloudy", "Cloudy", "Light Rains", "Moderate Rains", "Heavy Rains"],
                index=["Clear", "Partly Cloudy", "Cloudy", "Light Rains", "Moderate Rains", "Heavy Rains"].index(st.session_state.weather_data[mun]["cloud"]),
                key=f"cloud_{mun}",
                label_visibility="collapsed"
            )
        with col3:
            wind = st.selectbox(
                "Wind",
                ["Calm", "Light", "Moderate", "Strong", "Gale", "Storm"],
                index=["Calm", "Light", "Moderate", "Strong", "Gale", "Storm"].index(st.session_state.weather_data[mun]["wind"]),
                key=f"wind_{mun}",
                label_visibility="collapsed"
            )
        with col4:
            precip = st.selectbox(
                "Precipitation",
                ["None", "Light", "Moderate", "Heavy", "Torrential"],
                index=["None", "Light", "Moderate", "Heavy", "Torrential"].index(st.session_state.weather_data[mun]["precip"]),
                key=f"precip_{mun}",
                label_visibility="collapsed"
            )
        with col5:
            alert = st.selectbox(
                "Alert Level",
                ["White", "Blue", "Red"],
                index=["White", "Blue", "Red"].index(st.session_state.weather_data[mun]["alert"]),
                key=f"alert_{mun}",
                label_visibility="collapsed"
            )
        
        st.session_state.weather_data[mun] = {"cloud": cloud, "wind": wind, "precip": precip, "alert": alert}
    
    # Overall Alert Status
    overall_alert = st.selectbox(
        "Mountain Province Overall Alert Status",
        ["White", "Blue", "Red"],
        index=["White", "Blue", "Red"].index(st.session_state.get('overall_alert', 'White'))
    )
    st.session_state.overall_alert = overall_alert


def show_risk_communication_monitor():
    """Section for tracking issuances and communications"""
    
    st.markdown("### II. RISK COMMUNICATION MONITOR")
    st.caption("Tracking of advisories, memoranda, and their dissemination")
    
    # Add new issuance
    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1.5, 1, 1])
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
    
    if st.button("➕ Add Issuance", key="add_issuance"):
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


def show_risk_impact_assessment():
    """Risk and Impact Assessment table for landslides and flooding"""
    
    st.markdown("### III. RISK AND IMPACT ASSESSMENT")
    st.caption("Barangays susceptible to landslides and flooding based on PAGASA GSM and WRF models and MGB data")
    
    # Risk options
    risk_options = ["", "VHL", "HL", "ML", "DF", "VHF", "HF", "MF"]
    
    # Barangay data
    barangay_risks = {
        "BARLIG": ["Chupac", "Fiangtin", "Gawana", "Kaleo", "Latang", "Lias Kanluran", "Lias Silangan", "Lingoy", "Lunas", "Macalana", "Ogo-og"],
        "BAUKO": ["Bagnen Oriente", "Bagnen Proper", "Balintaugan", "Banao", "Bila", "Guinzadan Central", "Guinzadan Norte", "Guinzadan Sur", "Lagawa", "Leseb", "Mabaay", "Mayag", "Monamon Norte", "Monamon Sur", "Mount Data", "Otucan Norte", "Otucan Sur", "Poblacion", "Sadsadan", "Sinto", "Tapapan"],
        "BESAO": ["Agawa", "Besao East", "Gueday", "Lacmaan", "Suquib"],
        "BONTOC": ["Alab Oriente", "Alab Proper", "Balili", "Bayyo", "Bontoc Ili", "Caluttit", "Caneo", "Dalican", "Gonogon", "Guina-ang", "Mainit", "Maligcong", "Poblacion", "Samoki", "Talubin", "Tocucan"],
        "NATONIN": ["Alunogan", "Balangao", "Banao", "Banawel", "Butac", "Maducayan", "Poblacion", "Pudo", "Saliok", "Santa Isabel", "Tonglayan"],
        "PARACELIS": ["Anonat", "Bacarri", "Bananao", "Bantay", "Bunot", "Buringal", "Butigue", "Palitod", "Poblacion"],
        "SABANGAN": ["Napua", "Pingad", "Poblacion", "Supang", "Tambingan", "Bao-Angan", "Bun-Ayan", "Busa", "Camatagan", "Capinitan", "Data", "Gayang", "Lagan", "Losad", "Namatec"],
        "SADANGA": ["Anabel", "Bekigan", "Belwang", "Betwagan", "Demang", "Poblacion", "Sacasacan", "Saclit"],
        "SAGADA": ["Ambasing", "Angkeling", "Antadao", "Balugan", "Bangaan", "Dagdag", "Demang", "Fidelisan", "Kilong", "Madongo", "Nacagang", "Poblacion", "Suyo", "Taccong", "Tanulong", "Tetep-an Norte", "Tetep-an Sur"],
        "TADIAN": ["Bana-ao", "Cadad-anan", "Cagubatan", "Dacudac", "Lenga", "Pandayan"]
    }
    
    # Create expandable sections for each municipality
    for municipality, barangays in barangay_risks.items():
        with st.expander(f"📍 {municipality}", expanded=False):
            st.markdown(f"##### {municipality}")
            
            # Header
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
            with col1:
                st.markdown("**Barangay**")
            with col2:
                st.markdown("**VH Landslide**")
            with col3:
                st.markdown("**H Landslide**")
            with col4:
                st.markdown("**M Landslide**")
            with col5:
                st.markdown("**Debris Flow**")
            with col6:
                st.markdown("**VH Flood**")
            with col7:
                st.markdown("**H Flood**")
            with col8:
                st.markdown("**M Flood**")
            
            # Create rows for each barangay
            for barangay in barangays:
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 1, 1, 1, 1, 1, 1, 1])
                with col1:
                    st.markdown(barangay)
                with col2:
                    vh_landslide = st.selectbox("VH Landslide", risk_options, key=f"{municipality}_{barangay}_vh_landslide", label_visibility="collapsed")
                with col3:
                    h_landslide = st.selectbox("H Landslide", risk_options, key=f"{municipality}_{barangay}_h_landslide", label_visibility="collapsed")
                with col4:
                    m_landslide = st.selectbox("M Landslide", risk_options, key=f"{municipality}_{barangay}_m_landslide", label_visibility="collapsed")
                with col5:
                    debris_flow = st.selectbox("Debris Flow", risk_options, key=f"{municipality}_{barangay}_debris", label_visibility="collapsed")
                with col6:
                    vh_flood = st.selectbox("VH Flood", risk_options, key=f"{municipality}_{barangay}_vh_flood", label_visibility="collapsed")
                with col7:
                    h_flood = st.selectbox("H Flood", risk_options, key=f"{municipality}_{barangay}_h_flood", label_visibility="collapsed")
                with col8:
                    m_flood = st.selectbox("M Flood", risk_options, key=f"{municipality}_{barangay}_m_flood", label_visibility="collapsed")
                
                # Store in session state
                key = f"{municipality}_{barangay}"
                st.session_state.risk_assessment[key] = {
                    "vh_landslide": vh_landslide,
                    "h_landslide": h_landslide,
                    "m_landslide": m_landslide,
                    "debris_flow": debris_flow,
                    "vh_flood": vh_flood,
                    "h_flood": h_flood,
                    "m_flood": m_flood
                }


def show_early_flood_warning_system():
    """Early Flood Warning System table with add/edit/delete"""
    
    st.markdown("### IV. EARLY FLOOD WARNING SYSTEM")
    st.caption("Monitoring stations and water level indicators for major river basins")
    
    # Add new river basin
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.5, 1, 1.5, 1, 1.5, 1, 1, 0.5])
    with col1:
        new_river = st.text_input("River Basin", placeholder="New river basin", key="new_river")
    with col2:
        new_drainage = st.number_input("Drainage Area (ha)", min_value=0, value=0, key="new_drainage")
    with col3:
        new_headwater = st.text_input("Head Water", key="new_headwater")
    with col4:
        new_watershed = st.number_input("Watershed Area (ha)", min_value=0, value=0, key="new_watershed")
    with col5:
        new_station = st.text_input("Monitoring Station", key="new_station")
    with col6:
        new_yellow = st.text_input("Yellow Line", placeholder="Alert/Ready", key="new_yellow")
    with col7:
        new_orange = st.text_input("Orange Line", placeholder="Pre-emptive evacuation", key="new_orange")
    with col8:
        new_red = st.text_input("Red Line", placeholder="Evacuation", key="new_red")
    
    if st.button("➕ Add River Basin", key="add_river"):
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
            
            if st.button(f"🗑️ Delete {river['river_basin']}", key=f"del_river_{i}"):
                st.session_state.flood_warning_systems.pop(i)
                st.rerun()


def show_pdra_ratings():
    """Probability and Impact Rating Scales under PDRA"""
    
    st.markdown("### V. PRE-DISASTER RISK ASSESSMENT (PDRA)")
    st.caption("Probability and Impact Ratings for hazard assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Probability Rating")
        st.caption("What is the likelihood of the hazard occurring?")
        
        prob_options = {
            "1 - Unlikely": "The event will not happen anywhere in the jurisdiction in the next 72 hours",
            "2 - Less Likely": "Less than 50% possibility that the event will affect 2 or more areas",
            "3 - Highly Likely": "More than 50% possibility that the event will happen; 51-75% of area will be exposed",
            "4 - Certain/Imminent": "100% possibility that the event will affect 2 or more areas in the next 72 hours"
        }
        
        probability = st.radio(
            "Select Probability Rating",
            list(prob_options.keys()),
            key="pdra_probability_radio"
        )
        
        if probability:
            st.info(prob_options[probability])
            st.session_state.pdra_probability = int(probability[0])
    
    with col2:
        st.markdown("#### 💥 Impact Rating")
        st.caption("What would be the severity of impacts if the hazard occurs?")
        
        impact_options = {
            "1 - Negligible": "No expected casualties or damage to properties",
            "2 - Minor": "The DRRMC can entirely manage the impacts, no assistance needed",
            "3 - Moderate": "The DRRMC can manage the impacts, minimal assistance may be required",
            "4 - Major": "The DRRMC can manage with progressive assistance required",
            "5 - Catastrophic": "The DRRMC will be overwhelmed; full assistance required"
        }
        
        impact = st.radio(
            "Select Impact Rating",
            list(impact_options.keys()),
            key="pdra_impact_radio"
        )
        
        if impact:
            st.info(impact_options[impact])
            st.session_state.pdra_impact = int(impact[0])
    
    # Calculate risk level
    if st.session_state.pdra_probability and st.session_state.pdra_impact:
        risk_score = st.session_state.pdra_probability * st.session_state.pdra_impact
        
        st.markdown("---")
        st.markdown("#### 🎯 Risk Level Assessment")
        
        if risk_score <= 4:
            risk_level = "🟢 LOW RISK"
            risk_color = "green"
            action = "Requires monitoring and standby for assistance"
        elif risk_score <= 8:
            risk_level = "🟡 MEDIUM RISK"
            risk_color = "yellow"
            action = "Requires planning and preparatory action"
        elif risk_score <= 12:
            risk_level = "🟠 HIGH RISK"
            risk_color = "orange"
            action = "Requires high priority for action"
        else:
            risk_level = "🔴 EXTREME RISK"
            risk_color = "red"
            action = "Requires immediate action"
        
        st.markdown(f"""
        <div style='background-color: {risk_color}; padding: 15px; border-radius: 10px; text-align: center; color: white;'>
            <h3>{risk_level}</h3>
            <p>{action}</p>
            <p><strong>Risk Score:</strong> {risk_score}/20 (Probability: {st.session_state.pdra_probability} x Impact: {st.session_state.pdra_impact})</p>
        </div>
        """, unsafe_allow_html=True)


def show_incidents_monitored():
    """Section II: Incidents Monitored"""
    
    st.markdown("### VI. INCIDENTS MONITORED")
    
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                     "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    for mun in municipalities:
        with st.expander(f"📋 {mun}", expanded=False):
            incidents = st.text_area(
                "Incident/s Reported",
                value=st.session_state.incidents_data[mun]["incidents"],
                placeholder="No untoward incident reported",
                height=60,
                key=f"incidents_{mun}"
            )
            casualties = st.text_input(
                "Casualties",
                value=st.session_state.incidents_data[mun]["casualties"],
                placeholder="e.g., 0 dead, 2 injured, 1 missing",
                key=f"casualties_{mun}"
            )
            st.session_state.incidents_data[mun] = {"incidents": incidents, "casualties": casualties}


def show_lifelines_status():
    """Section III: Status of Lifelines"""
    
    st.markdown("### VII. STATUS OF LIFELINES")
    
    # National Roads
    st.markdown("#### 7.1 National Roads & Bridges")
    st.caption("Select roads and provide status updates")
    
    for road in st.session_state.national_roads:
        with st.expander(f"🛣️ {road['name']}", expanded=False):
            # Add new section
            col1, col2, col3, col4 = st.columns([2, 1.5, 2, 1])
            with col1:
                new_section = st.text_input("Road Section", placeholder="e.g., Napu Section", key=f"new_section_{road['id']}")
            with col2:
                new_traffic = st.selectbox("Traffic Situation", ["Passable", "One Lane Passable", "Not Passable", "Closed"], key=f"new_traffic_{road['id']}")
            with col3:
                new_actions = st.text_input("Actions Taken", placeholder="e.g., Clearing operations ongoing", key=f"new_actions_{road['id']}")
            with col4:
                if st.button("➕ Add", key=f"add_section_{road['id']}"):
                    if new_section:
                        road['sections'].append({
                            "section": new_section,
                            "traffic": new_traffic,
                            "actions": new_actions,
                            "remarks": ""
                        })
                        st.rerun()
            
            # Display existing sections
            for idx, section in enumerate(road['sections']):
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 2, 2, 0.5])
                with col1:
                    section_name = st.text_input("Section", value=section['section'], key=f"section_{road['id']}_{idx}")
                with col2:
                    traffic = st.selectbox("Traffic Situation", ["Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                          index=["Passable", "One Lane Passable", "Not Passable", "Closed"].index(section['traffic']),
                                          key=f"traffic_{road['id']}_{idx}")
                with col3:
                    actions = st.text_input("Actions Taken", value=section.get('actions', ''), key=f"actions_{road['id']}_{idx}")
                with col4:
                    remarks = st.text_input("Remarks", value=section.get('remarks', ''), key=f"remarks_{road['id']}_{idx}")
                with col5:
                    if st.button("🗑️", key=f"del_section_{road['id']}_{idx}"):
                        road['sections'].pop(idx)
                        st.rerun()
                
                section['section'] = section_name
                section['traffic'] = traffic
                section['actions'] = actions
                section['remarks'] = remarks
    
    # Provincial Roads
    st.markdown("#### 7.2 Provincial Roads & Bridges")
    
    for road in st.session_state.provincial_roads:
        col1, col2, col3, col4 = st.columns([3, 1.5, 2, 0.5])
        with col1:
            road_name = st.text_input("Road Name", value=road['name'], key=f"prov_road_{road['id']}")
        with col2:
            road_status = st.selectbox("Traffic Situation", ["Passable", "One Lane Passable", "Not Passable", "Closed"],
                                      index=["Passable", "One Lane Passable", "Not Passable", "Closed"].index(road['status']),
                                      key=f"prov_status_{road['id']}")
        with col3:
            road_remarks = st.text_input("Remarks", value=road.get('remarks', ''), key=f"prov_remarks_{road['id']}")
        with col4:
            if st.button("🗑️", key=f"del_prov_road_{road['id']}"):
                st.session_state.provincial_roads = [r for r in st.session_state.provincial_roads if r['id'] != road['id']]
                st.rerun()
        
        road['name'] = road_name
        road['status'] = road_status
        road['remarks'] = road_remarks
    
    # Municipal and Barangay Roads
    st.markdown("#### 7.3 Municipal & Barangay Roads")
    st.caption("For auto-fetch from Municipal SitReps in future version")
    
    with st.expander("➕ Add Municipal/Barangay Road", expanded=False):
        col1, col2, col3, col4 = st.columns([2, 1.5, 2, 1])
        with col1:
            mun_road = st.text_input("Road Name", key="mun_road_name")
            mun_barangay = st.text_input("Barangay/Municipality", key="mun_barangay")
        with col2:
            mun_traffic = st.selectbox("Traffic Situation", ["Passable", "One Lane Passable", "Not Passable", "Closed"], key="mun_traffic")
        with col3:
            mun_actions = st.text_input("Actions Taken", key="mun_actions")
        with col4:
            if st.button("➕ Add", key="add_mun_road"):
                if mun_road:
                    st.session_state.municipal_roads.append({
                        "road": mun_road,
                        "location": mun_barangay,
                        "traffic": mun_traffic,
                        "actions": mun_actions,
                        "remarks": ""
                    })
                    st.rerun()
    
    # Display municipal roads
    for i, road in enumerate(st.session_state.municipal_roads):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1.5, 2, 2, 0.5])
        with col1:
            road_name = st.text_input("Road", value=road['road'], key=f"mun_road_{i}")
        with col2:
            location = st.text_input("Location", value=road.get('location', ''), key=f"mun_loc_{i}")
        with col3:
            traffic = st.selectbox("Traffic", ["Passable", "One Lane Passable", "Not Passable", "Closed"],
                                  index=["Passable", "One Lane Passable", "Not Passable", "Closed"].index(road['traffic']),
                                  key=f"mun_traffic_{i}")
        with col4:
            actions = st.text_input("Actions", value=road.get('actions', ''), key=f"mun_actions_{i}")
        with col5:
            remarks = st.text_input("Remarks", value=road.get('remarks', ''), key=f"mun_remarks_{i}")
        with col6:
            if st.button("🗑️", key=f"del_mun_road_{i}"):
                st.session_state.municipal_roads.pop(i)
                st.rerun()
        
        road['road'] = road_name
        road['location'] = location
        road['traffic'] = traffic
        road['actions'] = actions
        road['remarks'] = remarks
    
    # Power & Communication
    st.markdown("#### 7.4 Power & Communication")
    
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                     "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    st.markdown("| Municipality | Power Status | Communication Status |")
    st.markdown("|--------------|--------------|---------------------|")
    
    for mun in municipalities:
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        with col1:
            st.markdown(f"**{mun}**")
        with col2:
            power = st.selectbox("Power", ["Normal", "Intermittent", "No Power"], 
                                index=["Normal", "Intermittent", "No Power"].index(st.session_state.power_data[mun]),
                                key=f"power_{mun}",
                                label_visibility="collapsed")
            st.session_state.power_data[mun] = power
        with col3:
            comm = st.selectbox("Communication", ["Normal", "Intermittent", "No Signal"],
                               index=["Normal", "Intermittent", "No Signal"].index(st.session_state.comm_data[mun]),
                               key=f"comm_{mun}",
                               label_visibility="collapsed")
            st.session_state.comm_data[mun] = comm


def show_displaced_damages():
    """Section IV: Displaced Population & Damages"""
    
    st.markdown("### VIII. DISPLACED POPULATION & DAMAGES")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Inside Evacuation Centers**")
        families_ec = st.number_input("Families in ECs", min_value=0, value=st.session_state.displaced["families_ec"], key="families_ec")
        persons_ec = st.number_input("Persons in ECs", min_value=0, value=st.session_state.displaced["persons_ec"], key="persons_ec")
    with col2:
        st.markdown("**Outside Evacuation Centers**")
        families_out = st.number_input("Families Outside ECs", min_value=0, value=st.session_state.displaced["families_out"], key="families_out")
        persons_out = st.number_input("Persons Outside ECs", min_value=0, value=st.session_state.displaced["persons_out"], key="persons_out")
    
    st.session_state.displaced = {
        "families_ec": families_ec,
        "persons_ec": persons_ec,
        "families_out": families_out,
        "persons_out": persons_out
    }
    
    st.markdown("**Damaged Houses**")
    col1, col2 = st.columns(2)
    with col1:
        totally_damaged = st.number_input("Totally Damaged Houses", min_value=0, value=st.session_state.damages["totally_damaged"], key="totally_damaged")
    with col2:
        partially_damaged = st.number_input("Partially Damaged Houses", min_value=0, value=st.session_state.damages["partially_damaged"], key="partially_damaged")
    
    st.markdown("**Affected Population**")
    col1, col2 = st.columns(2)
    with col1:
        affected_families = st.number_input("Affected Families", min_value=0, value=st.session_state.damages["affected_families"], key="affected_families")
    with col2:
        affected_persons = st.number_input("Affected Persons", min_value=0, value=st.session_state.damages["affected_persons"], key="affected_persons")
    
    st.session_state.damages.update({
        "totally_damaged": totally_damaged,
        "partially_damaged": partially_damaged,
        "affected_families": affected_families,
        "affected_persons": affected_persons
    })


def show_resources_provided():
    """Section V: Resources Provided"""
    
    st.markdown("### IX. RESOURCES PROVIDED")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        food_packs = st.number_input("Food Packs Distributed", min_value=0, value=st.session_state.resources["food_packs"], key="food_packs")
    with col2:
        hygiene_kits = st.number_input("Hygiene Kits Distributed", min_value=0, value=st.session_state.resources["hygiene_kits"], key="hygiene_kits")
    with col3:
        family_kits = st.number_input("Family Kits Distributed", min_value=0, value=st.session_state.resources["family_kits"], key="family_kits")
    
    st.session_state.resources = {
        "food_packs": food_packs,
        "hygiene_kits": hygiene_kits,
        "family_kits": family_kits
    }


def show_response_actions():
    """Section VI: Response Actions"""
    
    st.markdown("### X. RESPONSE ACTIONS")
    
    response_actions = st.text_area(
        "Response Actions Taken",
        value=st.session_state.response_actions,
        height=150,
        key="response_actions",
        placeholder="List all response actions taken by the PDRRMC and MDRRMCs..."
    )
    st.session_state.response_actions = response_actions


def show_photo_documentation():
    """Section VII: Photo Documentation"""
    
    st.markdown("### XI. PHOTO DOCUMENTATION")
    
    # Upload new photo
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        photo = st.file_uploader("Select Photo", type=['jpg', 'jpeg', 'png'], key="new_photo")
    with col2:
        caption = st.text_input("Caption", key="photo_caption")
    with col3:
        location = st.text_input("Location", key="photo_location")
    
    if photo and st.button("📸 Add Photo", key="add_photo"):
        st.session_state.photos.append({
            "file": photo.name,
            "caption": caption,
            "location": location,
            "uploaded_at": datetime.now().isoformat()
        })
        st.rerun()
    
    # Display existing photos
    for i, photo in enumerate(st.session_state.photos):
        col1, col2, col3 = st.columns([2, 2, 0.5])
        with col1:
            st.markdown(f"**Photo:** {photo['file']}")
        with col2:
            st.markdown(f"**Caption:** {photo['caption']}")
        with col3:
            if st.button("🗑️", key=f"del_photo_{i}"):
                st.session_state.photos.pop(i)
                st.rerun()


def show_needs_assessment():
    """Section VIII: Needs Assessment"""
    
    st.markdown("### XII. NEEDS ASSESSMENT")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        priority1 = st.text_area("Priority 1 Needs", value=st.session_state.needs["priority1"], height=80, key="priority1",
                                 placeholder="Search & Rescue, Food, Medical, Water")
    with col2:
        priority2 = st.text_area("Priority 2 Needs", value=st.session_state.needs["priority2"], height=80, key="priority2",
                                 placeholder="Shelter, Clothing, Non-food items")
    with col3:
        priority3 = st.text_area("Priority 3 Needs", value=st.session_state.needs["priority3"], height=80, key="priority3",
                                 placeholder="Cash for Work, Rehabilitation")
    
    st.session_state.needs = {
        "priority1": priority1,
        "priority2": priority2,
        "priority3": priority3
    }


def save_complete_report():
    """Save the complete report to session state and cloud"""
    
    report = {
        "id": int(datetime.now().timestamp() * 1000),
        "sitrep_number": st.session_state.sitrep_number,
        "incident_name": st.session_state.incident_name,
        "report_date": st.session_state.report_date.isoformat(),
        "report_time": st.session_state.report_time.strftime("%H:%M"),
        "overall_alert": st.session_state.get('overall_alert', 'White'),
        "pagasa_bulletin": st.session_state.get('pagasa_bulletin', ''),
        "weather_data": st.session_state.weather_data,
        "risk_communications": st.session_state.risk_communications,
        "risk_assessment": st.session_state.risk_assessment,
        "flood_warning_systems": st.session_state.flood_warning_systems,
        "pdra_probability": st.session_state.pdra_probability,
        "pdra_impact": st.session_state.pdra_impact,
        "incidents_data": st.session_state.incidents_data,
        "national_roads": st.session_state.national_roads,
        "provincial_roads": st.session_state.provincial_roads,
        "municipal_roads": st.session_state.municipal_roads,
        "power_data": st.session_state.power_data,
        "comm_data": st.session_state.comm_data,
        "displaced": st.session_state.displaced,
        "damages": st.session_state.damages,
        "resources": st.session_state.resources,
        "response_actions": st.session_state.response_actions,
        "photos": st.session_state.photos,
        "needs": st.session_state.needs,
        "created_at": datetime.now().isoformat()
    }
    
    # Save locally
    folder = "local_storage/situation_reports"
    os.makedirs(folder, exist_ok=True)
    filename = f"sitrep_{st.session_state.sitrep_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Save to session state
    st.session_state.saved_sitreps.append(report)
    
    # Save to cloud
    if is_connected():
        try:
            from utils.supabase_client import get_supabase_client
            client = get_supabase_client()
            if client:
                client.table('situation_reports').insert(report).execute()
        except Exception as e:
            print(f"Error saving to cloud: {e}")