# tabs/situation_report.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import json
import os
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected, auto_sync_table
from utils.pagasa_api import fetch_weather_data, refresh_weather_data
from utils.local_storage import save_file_to_cloud, get_file_url

def show():
    """Display Enhanced Situation Report Tab with PDRA Integration"""
    
    st.markdown("# 📡 SITUATION REPORT")
    st.caption("Enhanced Situation Report with PDRA Guided Workflow and Multi-User Data Entry")
    
    # Initialize session state
    if 'municipal_reports' not in st.session_state:
        st.session_state.municipal_reports = []
    
    if 'main_reports' not in st.session_state:
        st.session_state.main_reports = []
    
    if 'sitrep_photos' not in st.session_state:
        st.session_state.sitrep_photos = []
    
    if 'archived_sitreps' not in st.session_state:
        st.session_state.archived_sitreps = []
    
    if 'pdra_data' not in st.session_state:
        st.session_state.pdra_data = {
            "type": None,
            "hazard": {},
            "risk_matrix": {},
            "anticipated_needs": {},
            "other_matters": {}
        }
    
    # Load weather data
    if 'pagasa_weather' not in st.session_state:
        fetch_weather_data()
    
    # Create main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 PDRA Wizard",
        "📝 Municipal Data Entry",
        "📊 Provincial Consolidation",
        "📈 Predictive Analysis",
        "📸 Photo Gallery",
        "📁 Archived SitReps",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_pdra_wizard()
    
    with tab2:
        show_mdrrmo_data_entry()
    
    with tab3:
        show_pdrrmo_consolidation()
    
    with tab4:
        show_predictive_analysis()
    
    with tab5:
        show_photo_gallery()
    
    with tab6:
        show_archived_sitreps()
    
    with tab7:
        show_related_modules()


# =============================================================================
# SECTION 1: PDRA WIZARD (Step-by-Step Guided Workflow)
# =============================================================================

def show_pdra_wizard():
    """Step-by-step PDRA wizard with collapsible sections"""
    
    st.markdown("### 📋 Pre-Disaster Risk Assessment (PDRA) Wizard")
    st.caption("Complete the PDRA following the official guidelines")
    
    # Progress indicator
    steps = ["PDRA Type", "Hazard Situation", "Risk Assessment", "Anticipated Needs", "Other Matters"]
    completed = []
    
    if st.session_state.pdra_data.get("type"):
        completed.append(0)
    if st.session_state.pdra_data.get("hazard"):
        completed.append(1)
    if st.session_state.pdra_data.get("risk_matrix"):
        completed.append(2)
    if st.session_state.pdra_data.get("anticipated_needs"):
        completed.append(3)
    if st.session_state.pdra_data.get("other_matters"):
        completed.append(4)
    
    # Progress bar
    progress = len(completed) / len(steps)
    st.progress(progress)
    
    # Display progress status
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            if i in completed:
                st.markdown(f"✅ **{step}**")
            else:
                st.markdown(f"⏳ {step}")
    
    st.markdown("---")
    
    # Step 1: PDRA Type (Always expanded first)
    with st.expander("📌 Step 1: PDRA Type", expanded=not st.session_state.pdra_data.get("type")):
        pdra_type = st.radio(
            "Select PDRA Type",
            ["🌊 Weather-Related Hazard (Typhoon, Monsoon, LPA)",
             "🎉 Planned Event (Festival, Sports, Election)",
             "🔥 Other Hazard (Landslide, Earthquake, Fire, Vehicular Accident)"],
            key="pdra_type_select",
            horizontal=True
        )
        
        if st.button("✓ Confirm & Continue", key="confirm_type"):
            st.session_state.pdra_data["type"] = pdra_type
            st.rerun()
    
    # Step 2: Hazard Situation
    if st.session_state.pdra_data.get("type"):
        with st.expander("🌡️ Step 2: Hazard Situation", expanded=not st.session_state.pdra_data.get("hazard")):
            show_hazard_situation()
    
    # Step 3: Risk & Impact Assessment
    if st.session_state.pdra_data.get("hazard"):
        with st.expander("⚠️ Step 3: Risk & Impact Assessment", expanded=not st.session_state.pdra_data.get("risk_matrix")):
            show_risk_assessment()
    
    # Step 4: Anticipated Needs
    if st.session_state.pdra_data.get("risk_matrix"):
        with st.expander("📦 Step 4: Anticipated Needs", expanded=not st.session_state.pdra_data.get("anticipated_needs")):
            show_anticipated_needs()
    
    # Step 5: Other Matters
    if st.session_state.pdra_data.get("anticipated_needs"):
        with st.expander("📋 Step 5: Other Matters", expanded=not st.session_state.pdra_data.get("other_matters")):
            show_other_matters()
    
    # Display PDRA Summary if complete
    if st.session_state.pdra_data.get("other_matters"):
        st.markdown("---")
        st.markdown("### ✅ PDRA Complete!")
        
        if st.button("📄 Generate PDRA Report", type="primary"):
            generate_pdra_report()


def show_hazard_situation():
    """Display hazard situation based on PDRA type"""
    
    pdra_type = st.session_state.pdra_data.get("type", "")
    
    if "Weather" in pdra_type:
        # Weather-related hazard
        st.markdown("#### 🌦️ Weather Situation")
        
        # PAGASA integration
        weather = st.session_state.get('pagasa_weather', {})
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Fetch Latest PAGASA Data"):
                refresh_weather_data()
                st.rerun()
        
        with col2:
            last_updated = weather.get('last_fetched')
            if last_updated:
                st.caption(f"Last updated: {last_updated.strftime('%Y-%m-%d %H:%M')}")
        
        # Display current weather
        cyclones = weather.get('cyclones', {})
        if cyclones.get('has_active'):
            st.warning(f"⚠️ {cyclones.get('status', 'Active Tropical Cyclone')}")
        
        # Track map upload
        st.markdown("#### 🗺️ Track Map")
        track_map = st.file_uploader("Upload track map", type=['jpg', 'png', 'pdf'], key="track_map")
        
        if track_map:
            st.success("Track map uploaded")
        
        # Potential risk areas
        st.markdown("#### 📍 Potential Risk Areas")
        risk_areas = st.text_area("Areas Affected", placeholder="e.g., CAR, Region I, Region II, Ilocos, Cagayan")
        
        # Winds and rainfall
        col1, col2 = st.columns(2)
        with col1:
            wind_speed = st.selectbox("Wind Speed", ["<61 km/h", "62-88 km/h", "89-117 km/h", "118-220 km/h", ">220 km/h"])
        with col2:
            rainfall = st.selectbox("Rainfall Intensity", ["Light (<2.5mm/hr)", "Moderate (2.6-7.5mm/hr)", 
                                                            "Heavy (7.6-15mm/hr)", "Intense (15.1-30mm/hr)", 
                                                            "Torrential (>30mm/hr)"])
        
        # Save button
        if st.button("💾 Save Hazard Situation", key="save_hazard_weather"):
            st.session_state.pdra_data["hazard"] = {
                "type": "weather",
                "track_map": track_map.name if track_map else None,
                "risk_areas": risk_areas,
                "wind_speed": wind_speed,
                "rainfall": rainfall,
                "cyclones": cyclones.get('status') if cyclones.get('has_active') else None
            }
            st.success("Hazard situation saved!")
            st.rerun()
    
    elif "Planned Event" in pdra_type:
        # Planned event
        st.markdown("#### 🎉 Event Details")
        
        col1, col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Event Name", placeholder="e.g., 18th Lang-ay Festival")
            start_date = st.date_input("Start Date", date.today())
        with col2:
            event_location = st.text_input("Location", placeholder="e.g., Bontoc, Mountain Province")
            end_date = st.date_input("End Date", date.today() + timedelta(days=7))
        
        # Weather outlook
        st.markdown("#### 🌤️ Weather Outlook")
        
        # Get weather forecast from PAGASA
        weather = st.session_state.get('pagasa_weather', {})
        forecast = weather.get('forecast', {})
        
        if forecast.get('forecast'):
            st.info(f"**Forecast:** {forecast.get('summary', 'Check PAGASA for latest updates')}")
        
        # What to expect (multiselect that adds items)
        st.markdown("#### 📋 What to Expect")
        expectations = st.multiselect("Select anticipated situations (click to add)", [
            "Influx of people (travelers/visitors)",
            "Vehicular accidents",
            "Fire incidents (forest/structural)",
            "Prolonged period of hot and humid weather",
            "Increase of heat-related stresses on health",
            "Thunderstorms",
            "Food poisoning",
            "Gastroenteritis cases"
        ])
        
        # Display selected expectations
        if expectations:
            st.markdown("**Selected:**")
            for exp in expectations:
                st.markdown(f"- {exp}")
        
        # Alert level (White, Blue, Red only)
        st.markdown("#### 🚨 Alert Level Status")
        alert_level = st.selectbox("Alert Level", ["White", "Blue", "Red"])
        
        if st.button("💾 Save Event Details", key="save_hazard_event"):
            st.session_state.pdra_data["hazard"] = {
                "type": "planned_event",
                "event_name": event_name,
                "event_location": event_location,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "expectations": expectations,
                "alert_level": alert_level
            }
            st.success("Event details saved!")
            st.rerun()
    
    else:
        # Other hazard
        st.markdown("#### 🌋 Hazard Details")
        
        hazard_type = st.selectbox("Hazard Type", ["Landslide", "Earthquake", "Forest Fire", "Structural Fire", "Vehicular Accident", "Drought", "Other"])
        
        col1, col2 = st.columns(2)
        with col1:
            location = st.text_input("Location/Area", placeholder="e.g., Bauko, Paracelis")
            start_date = st.date_input("Start Date", date.today())
        with col2:
            intensity = st.text_input("Intensity/Magnitude", placeholder="e.g., Magnitude 5.2, Moderate")
            end_date = st.date_input("End Date", date.today() + timedelta(days=3))
        
        description = st.text_area("Description", placeholder="Describe the hazard situation")
        
        if st.button("💾 Save Hazard Details", key="save_hazard_other"):
            st.session_state.pdra_data["hazard"] = {
                "type": "other",
                "hazard_type": hazard_type,
                "location": location,
                "intensity": intensity,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "description": description
            }
            st.success("Hazard details saved!")
            st.rerun()


def show_risk_assessment():
    """Show risk matrix with probability and impact ratings"""
    
    st.markdown("#### ⚠️ Risk & Impact Assessment")
    
    # Probability Rating Scale
    st.markdown("##### 📊 Probability Rating")
    st.caption("What is the likelihood of the hazard occurring?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        prob_1 = st.button("1 - Unlikely", key="prob_1", use_container_width=True)
    with col2:
        prob_2 = st.button("2 - Less Likely", key="prob_2", use_container_width=True)
    with col3:
        prob_3 = st.button("3 - Highly Likely", key="prob_3", use_container_width=True)
    with col4:
        prob_4 = st.button("4 - Certain/Imminent", key="prob_4", use_container_width=True)
    
    probability = None
    if prob_1:
        probability = 1
        st.info("**Unlikely:** The event will not happen anywhere in the jurisdiction in the next 72 hours")
    elif prob_2:
        probability = 2
        st.info("**Less Likely:** Less than 50% possibility that the event will affect 2 or more areas")
    elif prob_3:
        probability = 3
        st.info("**Highly Likely:** More than 50% possibility that the event will happen; 51-75% of area will be exposed")
    elif prob_4:
        probability = 4
        st.warning("**Certain/Imminent:** 100% possibility that the event will affect 2 or more areas in the next 72 hours")
    
    st.markdown("---")
    
    # Impact Rating Scale
    st.markdown("##### 💥 Impact Rating")
    st.caption("What would be the severity of impacts if the hazard occurs?")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        imp_1 = st.button("1 - Negligible", key="imp_1", use_container_width=True)
    with col2:
        imp_2 = st.button("2 - Minor", key="imp_2", use_container_width=True)
    with col3:
        imp_3 = st.button("3 - Moderate", key="imp_3", use_container_width=True)
    with col4:
        imp_4 = st.button("4 - Major", key="imp_4", use_container_width=True)
    with col5:
        imp_5 = st.button("5 - Catastrophic", key="imp_5", use_container_width=True)
    
    impact = None
    if imp_1:
        impact = 1
        st.info("**Negligible:** No expected casualties or damage to properties")
    elif imp_2:
        impact = 2
        st.info("**Minor:** The DRRMC can entirely manage the impacts, no assistance needed")
    elif imp_3:
        impact = 3
        st.warning("**Moderate:** The DRRMC can manage the impacts, minimal assistance may be required")
    elif imp_4:
        impact = 4
        st.warning("**Major:** The DRRMC can manage with progressive assistance required")
    elif imp_5:
        impact = 5
        st.error("**Catastrophic:** The DRRMC will be overwhelmed; full assistance required")
    
    # Calculate risk level
    if probability and impact:
        risk_score = probability * impact
        
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
            <p><strong>Risk Score:</strong> {risk_score}/20 (Probability: {probability} x Impact: {impact})</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Save button
        if st.button("💾 Save Risk Assessment", key="save_risk"):
            st.session_state.pdra_data["risk_matrix"] = {
                "probability": probability,
                "impact": impact,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "action": action
            }
            st.success("Risk assessment saved!")
            st.rerun()


def show_anticipated_needs():
    """Show anticipated needs table"""
    
    st.markdown("#### 📦 Anticipated Needs")
    st.caption("Identify resources that may be needed during the event")
    
    # Food and Non-Food Items
    st.markdown("##### 🍚 Food and Non-Food Items")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        food_packs = st.number_input("Family Food Packs", min_value=0, value=0)
        hygiene_kits = st.number_input("Hygiene Kits", min_value=0, value=0)
    with col2:
        family_kits = st.number_input("Family Kits", min_value=0, value=0)
        sleeping_kits = st.number_input("Sleeping Kits", min_value=0, value=0)
    with col3:
        water_containers = st.number_input("Water Containers", min_value=0, value=0)
        tarpaulins = st.number_input("Tarpaulins", min_value=0, value=0)
    
    # Medicines
    st.markdown("##### 💊 Medicines")
    medicines = st.text_area("Medicines Needed", placeholder="List medicines and quantities", height=80)
    
    # Logistics and Equipment
    st.markdown("##### 🚜 Logistics and Equipment")
    
    col1, col2 = st.columns(2)
    with col1:
        handheld_radios = st.number_input("Handheld Radios", min_value=0, value=0)
        gensets = st.number_input("Generators", min_value=0, value=0)
        chainsaws = st.number_input("Chainsaws", min_value=0, value=0)
    with col2:
        clearing_equipment = st.number_input("Clearing Equipment (sets)", min_value=0, value=0)
        water_rescue = st.number_input("Water Rescue Equipment (sets)", min_value=0, value=0)
        ppe_sets = st.number_input("PPE Sets", min_value=0, value=0)
    
    # Vehicles
    st.markdown("##### 🚗 Vehicles")
    vehicles = st.text_area("Vehicles Available/Needed", placeholder="List vehicles and their status", height=80)
    
    # Save button
    if st.button("💾 Save Anticipated Needs", key="save_needs"):
        st.session_state.pdra_data["anticipated_needs"] = {
            "food_packs": food_packs,
            "hygiene_kits": hygiene_kits,
            "family_kits": family_kits,
            "sleeping_kits": sleeping_kits,
            "water_containers": water_containers,
            "tarpaulins": tarpaulins,
            "medicines": medicines,
            "handheld_radios": handheld_radios,
            "gensets": gensets,
            "chainsaws": chainsaws,
            "clearing_equipment": clearing_equipment,
            "water_rescue": water_rescue,
            "ppe_sets": ppe_sets,
            "vehicles": vehicles
        }
        st.success("Anticipated needs saved!")
        st.rerun()


def show_other_matters():
    """Show other matters section"""
    
    st.markdown("#### 📋 Other Matters")
    
    # ARG Status
    st.markdown("##### 🌧️ Automated Rain Gauge (ARG) Status")
    
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    arg_status = {}
    for mun in municipalities:
        arg_status[mun] = st.selectbox(f"{mun}", ["Operational", "Down", "Under Repair"], key=f"arg_{mun}")
    
    # Geo-tagging
    st.markdown("##### 📸 Geo-tagging for Landslide Reporting")
    use_geo_tagging = st.checkbox("Use GPS Maps Camera Lite or other geo-tagging apps for landslide reporting")
    
    # Philsensor
    st.markdown("##### 📡 Philsensor Status")
    philsensor_status = st.selectbox("Philsensor Status", ["Operational", "Down", "Data Not Available"])
    
    # Additional Notes
    st.markdown("##### 📝 Additional Notes")
    additional_notes = st.text_area("Other matters not covered", height=100)
    
    # Save button
    if st.button("✅ Complete PDRA", key="complete_pdra", type="primary"):
        st.session_state.pdra_data["other_matters"] = {
            "arg_status": arg_status,
            "use_geo_tagging": use_geo_tagging,
            "philsensor_status": philsensor_status,
            "additional_notes": additional_notes
        }
        st.success("PDRA completed successfully!")
        st.balloons()
        st.rerun()


def generate_pdra_report():
    """Generate and display PDRA report"""
    
    pdra = st.session_state.pdra_data
    
    st.markdown("---")
    st.markdown("### 📄 PDRA Report")
    st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("#### 📌 PDRA Type")
    st.markdown(pdra.get("type", "Not specified"))
    
    st.markdown("#### 🌡️ Hazard Situation")
    hazard = pdra.get("hazard", {})
    for key, value in hazard.items():
        if value:
            st.markdown(f"- **{key.replace('_', ' ').title()}:** {value}")
    
    st.markdown("#### ⚠️ Risk Assessment")
    risk = pdra.get("risk_matrix", {})
    if risk:
        st.markdown(f"- **Probability:** {risk.get('probability')}/4")
        st.markdown(f"- **Impact:** {risk.get('impact')}/5")
        st.markdown(f"- **Risk Score:** {risk.get('risk_score')}/20")
        st.markdown(f"- **Risk Level:** {risk.get('risk_level')}")
        st.markdown(f"- **Action:** {risk.get('action')}")
    
    st.markdown("#### 📦 Anticipated Needs")
    needs = pdra.get("anticipated_needs", {})
    if needs:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"- Food Packs: {needs.get('food_packs', 0)}")
            st.markdown(f"- Hygiene Kits: {needs.get('hygiene_kits', 0)}")
            st.markdown(f"- Family Kits: {needs.get('family_kits', 0)}")
        with col2:
            st.markdown(f"- Generators: {needs.get('gensets', 0)}")
            st.markdown(f"- Chainsaws: {needs.get('chainsaws', 0)}")
            st.markdown(f"- PPE Sets: {needs.get('ppe_sets', 0)}")
    
    st.markdown("#### 📋 Other Matters")
    other = pdra.get("other_matters", {})
    if other:
        st.markdown(f"- **Philsensor Status:** {other.get('philsensor_status', 'N/A')}")
        st.markdown(f"- **Geo-tagging:** {'Enabled' if other.get('use_geo_tagging') else 'Not enabled'}")
    
    # Export option
    if st.button("📥 Export PDRA Report"):
        st.info("Export functionality coming soon")


# =============================================================================
# SECTION 2: MDRRMO DATA ENTRY (Improved with all your requests)
# =============================================================================

def show_mdrrmo_data_entry():
    """Municipal data entry with improved fields"""
    
    st.markdown("### 📝 Municipal Situation Report Entry")
    st.caption("MDRRMO Staff: Enter your municipality's data here")
    
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # Response action templates based on event type
    response_templates = {
        "Structural Fire": ["Fire suppression operations", "Evacuation of affected residents", "Establishment of temporary shelter", "Damage assessment", "Distribution of relief goods"],
        "Vehicular Accident": ["Rescue operations", "Traffic management", "Medical assistance", "Clearing operations", "Investigation"],
        "Landslide": ["Search and rescue", "Road clearing", "Evacuation of affected families", "Damage assessment", "Relief distribution"],
        "Flood": ["Pre-emptive evacuation", "Rescue operations", "Relief distribution", "Damage assessment", "Clearing operations"],
        "Typhoon": ["Pre-emptive evacuation", "Storm tracking", "Relief prepositioning", "Damage assessment", "Clearing operations"],
        "General": ["Monitoring", "Assessment", "Coordination with agencies", "Public information", "Resource mobilization"]
    }
    
    with st.form("municipal_report_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            municipality = st.selectbox("Municipality *", municipalities, key="mun_select")
            report_date = st.date_input("Report Date *", date.today(), key="report_date")
            report_time = st.time_input("Report Time *", datetime.now().time(), key="report_time")
            sitrep_number = st.number_input("SITREP Number *", min_value=1, value=1, step=1, key="sitrep_num")
            incident_name = st.text_input("Incident Name *", placeholder="e.g., TS PAENG, Structural Fire", key="incident_name")
        
        with col2:
            alert_level = st.selectbox("Alert Level *", ["White", "Blue", "Red"], key="alert_level")
            submitted_by = st.text_input("Reported By *", placeholder="Name and Position", key="submitted_by")
            mdrrmo_hotline = st.text_input("MDRRMO Hotline", placeholder="Contact number", key="hotline")
        
        st.markdown("---")
        
        # Weather Section
        st.markdown("#### 🌦️ Weather Conditions")
        col1, col2, col3 = st.columns(3)
        with col1:
            cloud = st.selectbox("Cloud Condition", ["Clear", "Partly Cloudy", "Cloudy", "Light Rains", "Moderate Rains", "Heavy Rains"], key="cloud")
        with col2:
            wind = st.selectbox("Wind Condition", ["Calm", "Light", "Moderate", "Strong", "Gale", "Storm"], key="wind")
        with col3:
            precipitation = st.selectbox("Precipitation", ["None", "Light", "Moderate", "Heavy", "Torrential"], key="precip")
        
        # Incidents
        st.markdown("#### 📋 Incidents Reported")
        st.info("Note: Report all incidents including vehicular accidents, structural fires, etc.")
        incidents = st.text_area("Incident/s Reported", placeholder="List all incidents per barangay", height=100, key="incidents")
        casualties = st.text_input("Casualties", placeholder="e.g., 0 dead, 2 injured, 1 missing", key="casualties")
        
        # Municipal Road Status (changed from National Roads)
        st.markdown("#### 🛣️ Municipal Road Status")
        st.caption("Report status of roads within your municipality")
        
        col1, col2 = st.columns(2)
        with col1:
            municipal_roads_status = st.selectbox("Municipal Roads Status", ["Fully Passable", "Partially Passable", "Not Passable", "Under Repair"], key="mun_roads")
        with col2:
            municipal_roads_remarks = st.text_input("Remarks", placeholder="Specific road sections affected", key="mun_roads_remarks")
        
        # Utilities with Affected Barangays
        st.markdown("#### 🔌 Utilities")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Power Status**")
            power = st.selectbox("Power Status", ["Normal", "Intermittent", "No Power"], key="power")
            # Power Remarks with dropdown
            power_remarks_options = ["No information", "Ongoing repair", "Weather-related", "Technical issue", "Scheduled maintenance", "Other"]
            power_remarks = st.selectbox("Power Remarks", power_remarks_options, key="power_remarks")
            affected_barangays_power = st.text_input("Affected Barangays (Power)", placeholder="List affected barangays", key="affected_power")
        
        with col2:
            st.markdown("**Communication Status**")
            comm = st.selectbox("Communication Status", ["Normal", "Intermittent", "No Signal"], key="comm")
            # Communication Remarks with dropdown
            comm_remarks_options = ["No information", "Network issue", "Equipment failure", "Weather-related", "Technical issue", "Other"]
            comm_remarks = st.selectbox("Communication Remarks", comm_remarks_options, key="comm_remarks")
            affected_barangays_comm = st.text_input("Affected Barangays (Communication)", placeholder="List affected barangays", key="affected_comm")
        
        # Displaced Population
        st.markdown("#### 🏠 Displaced Population")
        col1, col2 = st.columns(2)
        with col1:
            families_ec = st.number_input("Families in ECs", min_value=0, value=0, key="families_ec")
            persons_ec = st.number_input("Persons in ECs", min_value=0, value=0, key="persons_ec")
        with col2:
            families_outside = st.number_input("Families Outside ECs", min_value=0, value=0, key="families_outside")
            persons_outside = st.number_input("Persons Outside ECs", min_value=0, value=0, key="persons_outside")
        
        # Damages
        st.markdown("#### 🏚️ Damage Assessment")
        col1, col2 = st.columns(2)
        with col1:
            totally_damaged = st.number_input("Totally Damaged Houses", min_value=0, value=0, key="totally")
            partially_damaged = st.number_input("Partially Damaged Houses", min_value=0, value=0, key="partially")
        with col2:
            affected_families = st.number_input("Affected Families", min_value=0, value=0, key="affected_families")
            affected_persons = st.number_input("Affected Persons", min_value=0, value=0, key="affected_persons")
        
        # Resources
        st.markdown("#### 📦 Resources Provided")
        col1, col2, col3 = st.columns(3)
        with col1:
            food_packs = st.number_input("Food Packs", min_value=0, value=0, key="food_packs")
        with col2:
            hygiene_kits = st.number_input("Hygiene Kits", min_value=0, value=0, key="hygiene_kits")
        with col3:
            family_kits = st.number_input("Family Kits", min_value=0, value=0, key="family_kits")
        
        # Response Actions with Template Selection
        st.markdown("#### 🚑 Response Actions")
        
        # Event type selection for template
        event_type_for_template = st.selectbox("Event Type for Response Template", 
                                               ["General", "Structural Fire", "Vehicular Accident", "Landslide", "Flood", "Typhoon"],
                                               key="event_type_template")
        
        # Show template buttons
        if event_type_for_template in response_templates:
            st.markdown("**Quick Add Response Actions (click to add):**")
            template_cols = st.columns(len(response_templates[event_type_for_template]))
            for i, action in enumerate(response_templates[event_type_for_template]):
                with template_cols[i % 4]:
                    if st.button(action, key=f"template_{action[:10]}"):
                        # This will add to the text area - handled by JavaScript-like behavior
                        st.session_state.temp_response = st.session_state.get('temp_response', '') + f"\n• {action}"
                        st.rerun()
        
        # Response actions text area
        default_response = st.session_state.get('temp_response', '')
        response_actions = st.text_area("Response Actions Taken", value=default_response, height=120, key="response")
        
        # Needs
        st.markdown("#### 🎯 Needs Assessment")
        col1, col2, col3 = st.columns(3)
        with col1:
            priority1 = st.text_area("Priority 1 Needs", placeholder="Food, Medical, Water", height=80, key="priority1")
        with col2:
            priority2 = st.text_area("Priority 2 Needs", placeholder="Shelter, Clothing", height=80, key="priority2")
        with col3:
            priority3 = st.text_area("Priority 3 Needs", placeholder="Cash for Work", height=80, key="priority3")
        
        # Photo
        st.markdown("#### 📸 Photo Documentation")
        photo = st.file_uploader("Upload photo", type=['jpg', 'jpeg', 'png'], key="photo_upload")
        photo_caption = st.text_input("Photo Caption", key="photo_caption")
        
        submitted = st.form_submit_button("💾 Submit Report", type="primary")
        
        if submitted and municipality and incident_name:
            # Clear temp response
            if 'temp_response' in st.session_state:
                del st.session_state.temp_response
            
            report = {
                "id": int(datetime.now().timestamp() * 1000),
                "sitrep_number": sitrep_number,
                "municipality": municipality,
                "report_date": report_date.isoformat(),
                "report_time": report_time.strftime("%H:%M"),
                "incident_name": incident_name,
                "alert_level": alert_level,
                "submitted_by": submitted_by,
                "mdrrmo_hotline": mdrrmo_hotline,
                "weather": {"cloud": cloud, "wind": wind, "precipitation": precipitation},
                "incidents": incidents,
                "casualties": casualties,
                "municipal_roads": {"status": municipal_roads_status, "remarks": municipal_roads_remarks},
                "utilities": {
                    "power": {"status": power, "remarks": power_remarks, "affected_barangays": affected_barangays_power},
                    "communication": {"status": comm, "remarks": comm_remarks, "affected_barangays": affected_barangays_comm}
                },
                "displaced": {"families_in_ec": families_ec, "persons_in_ec": persons_ec,
                             "families_outside": families_outside, "persons_outside": persons_outside},
                "damages": {"totally_damaged": totally_damaged, "partially_damaged": partially_damaged,
                           "affected_families": affected_families, "affected_persons": affected_persons},
                "resources": {"food_packs": food_packs, "hygiene_kits": hygiene_kits, "family_kits": family_kits},
                "response_actions": response_actions,
                "needs": {"priority1": priority1, "priority2": priority2, "priority3": priority3},
                "photo": {"file": photo.name if photo else None, "caption": photo_caption},
                "created_at": datetime.now().isoformat(),
                "status": "Submitted"
            }
            
            auto_sync_add('municipal_reports', 'municipal_reports', report)
            st.success(f"✅ Report for {municipality} submitted!")
            st.balloons()
            st.rerun()


# =============================================================================
# SECTION 3: PROVINCIAL CONSOLIDATION
# =============================================================================

def show_pdrrmo_consolidation():
    """Provincial consolidation with auto-extraction from municipal reports"""
    
    st.markdown("### 📊 Provincial Situation Report Consolidation")
    st.caption("Auto-extracted data from municipal reports")
    
    # Load municipal reports
    auto_sync_table('municipal_reports', 'municipal_reports')
    reports = st.session_state.get('municipal_reports', [])
    
    if not reports:
        st.info("No municipal reports submitted yet.")
        return
    
    df = pd.DataFrame(reports)
    
    # Auto-extract summary data
    st.markdown("#### 📈 Summary Statistics (Auto-Extracted)")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Municipalities Reporting", df['municipality'].nunique())
    with col2:
        st.metric("Total Reports", len(df))
    with col3:
        total_affected = sum([r.get('damages', {}).get('affected_families', 0) for r in reports])
        st.metric("Total Affected Families", f"{total_affected:,}")
    with col4:
        active_alerts = len([r for r in reports if r.get('alert_level') != 'White'])
        st.metric("Active Alerts", active_alerts)
    
    # Weather Summary Table
    st.markdown("#### 🌦️ Weather Summary by Municipality")
    weather_data = []
    for r in reports:
        weather = r.get('weather', {})
        weather_data.append({
            "Municipality": r.get('municipality'),
            "Cloud": weather.get('cloud', 'N/A'),
            "Wind": weather.get('wind', 'N/A'),
            "Precipitation": weather.get('precipitation', 'N/A'),
            "Alert Level": r.get('alert_level', 'N/A')
        })
    st.dataframe(pd.DataFrame(weather_data), use_container_width=True, hide_index=True)
    
    # Incidents Summary
    st.markdown("#### 📋 Incidents Reported")
    incidents_data = []
    for r in reports:
        incidents_data.append({
            "Municipality": r.get('municipality'),
            "Incidents": r.get('incidents', 'None reported'),
            "Casualties": r.get('casualties', 'None')
        })
    st.dataframe(pd.DataFrame(incidents_data), use_container_width=True, hide_index=True)
    
    # Municipal Roads Summary
    st.markdown("#### 🛣️ Municipal Roads Status")
    roads_data = []
    for r in reports:
        roads = r.get('municipal_roads', {})
        roads_data.append({
            "Municipality": r.get('municipality'),
            "Status": roads.get('status', 'N/A'),
            "Remarks": roads.get('remarks', '')
        })
    st.dataframe(pd.DataFrame(roads_data), use_container_width=True, hide_index=True)
    
    # Utilities Summary
    st.markdown("#### 🔌 Utilities Status")
    utils_data = []
    for r in reports:
        utils = r.get('utilities', {})
        power = utils.get('power', {})
        comm = utils.get('communication', {})
        utils_data.append({
            "Municipality": r.get('municipality'),
            "Power": power.get('status', 'N/A'),
            "Power Remarks": power.get('remarks', ''),
            "Power Affected Barangays": power.get('affected_barangays', ''),
            "Communication": comm.get('status', 'N/A'),
            "Comm Remarks": comm.get('remarks', ''),
            "Comm Affected Barangays": comm.get('affected_barangays', '')
        })
    st.dataframe(pd.DataFrame(utils_data), use_container_width=True, hide_index=True)
    
    # Damages Summary
    st.markdown("#### 🏚️ Damage Summary")
    total_totally = sum([r.get('damages', {}).get('totally_damaged', 0) for r in reports])
    total_partially = sum([r.get('damages', {}).get('partially_damaged', 0) for r in reports])
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Totally Damaged Houses", total_totally)
    with col2:
        st.metric("Partially Damaged Houses", total_partially)
    
    # Resources Summary
    st.markdown("#### 📦 Resources Distributed")
    total_food = sum([r.get('resources', {}).get('food_packs', 0) for r in reports])
    total_hygiene = sum([r.get('resources', {}).get('hygiene_kits', 0) for r in reports])
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Food Packs", total_food)
    with col2:
        st.metric("Hygiene Kits", total_hygiene)
    
    # Generate Consolidated Report button
    st.markdown("---")
    if st.button("📄 Generate Consolidated Provincial SITREP", type="primary", use_container_width=True):
        generate_consolidated_report(reports)


def generate_consolidated_report(reports):
    """Generate consolidated provincial SITREP"""
    
    # Calculate totals
    total_families_ec = sum([r.get('displaced', {}).get('families_in_ec', 0) for r in reports])
    total_persons_ec = sum([r.get('displaced', {}).get('persons_in_ec', 0) for r in reports])
    total_families_out = sum([r.get('displaced', {}).get('families_outside', 0) for r in reports])
    total_persons_out = sum([r.get('displaced', {}).get('persons_outside', 0) for r in reports])
    
    st.markdown("---")
    st.markdown("### 📄 Consolidated Provincial SITREP")
    st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.markdown("#### 📊 DISPLACED POPULATION")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Inside Evacuation Centers**")
        st.markdown(f"- Families: {total_families_ec:,}")
        st.markdown(f"- Persons: {total_persons_ec:,}")
    with col2:
        st.markdown("**Outside Evacuation Centers**")
        st.markdown(f"- Families: {total_families_out:,}")
        st.markdown(f"- Persons: {total_persons_out:,}")
    
    st.markdown("#### 🏚️ DAMAGES")
    total_totally = sum([r.get('damages', {}).get('totally_damaged', 0) for r in reports])
    total_partially = sum([r.get('damages', {}).get('partially_damaged', 0) for r in reports])
    st.markdown(f"- **Totally Damaged Houses:** {total_totally}")
    st.markdown(f"- **Partially Damaged Houses:** {total_partially}")
    
    st.markdown("#### 📦 RESOURCES PROVIDED")
    total_food = sum([r.get('resources', {}).get('food_packs', 0) for r in reports])
    total_hygiene = sum([r.get('resources', {}).get('hygiene_kits', 0) for r in reports])
    st.markdown(f"- **Food Packs:** {total_food}")
    st.markdown(f"- **Hygiene Kits:** {total_hygiene}")
    
    # Save to main reports
    main_report = {
        "id": int(datetime.now().timestamp() * 1000),
        "title": f"SITREP {datetime.now().strftime('%Y%m%d')}",
        "date": datetime.now().isoformat(),
        "municipalities": [r.get('municipality') for r in reports],
        "displaced": {
            "families_in_ec": total_families_ec,
            "persons_in_ec": total_persons_ec,
            "families_outside": total_families_out,
            "persons_outside": total_persons_out
        },
        "damages": {
            "totally_damaged": total_totally,
            "partially_damaged": total_partially
        },
        "resources": {
            "food_packs": total_food,
            "hygiene_kits": total_hygiene
        },
        "created_at": datetime.now().isoformat()
    }
    
    auto_sync_add('main_reports', 'main_reports', main_report)
    st.success("✅ Consolidated report saved!")


# =============================================================================
# SECTION 4: PREDICTIVE ANALYSIS (with summary statistics)
# =============================================================================

def show_predictive_analysis():
    """Predictive analysis from historical reports with summary statistics"""
    
    st.markdown("### 📈 Predictive Analysis")
    st.caption("Analyze patterns and predict future impacts")
    
    reports = st.session_state.get('municipal_reports', [])
    
    if len(reports) < 5:
        st.info("Need at least 5 reports for meaningful analysis")
        return
    
    df = pd.DataFrame(reports)
    
    # Extract date fields
    if 'report_date' in df.columns:
        df['report_date'] = pd.to_datetime(df['report_date'])
        df['year'] = df['report_date'].dt.year
        df['quarter'] = df['report_date'].dt.quarter
        df['month'] = df['report_date'].dt.month
    
    # Extract numeric fields
    df['affected_families'] = df['damages'].apply(lambda x: x.get('affected_families', 0) if isinstance(x, dict) else 0)
    
    # Summary Statistics by Quarter
    st.markdown("#### 📊 Summary Statistics by Quarter")
    if 'quarter' in df.columns and 'year' in df.columns:
        quarterly = df.groupby(['year', 'quarter'])['affected_families'].sum().reset_index()
        fig = px.bar(quarterly, x='quarter', y='affected_families', color='year', 
                     title="Affected Families by Quarter", barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary Statistics by Year
    st.markdown("#### 📊 Summary Statistics by Year")
    if 'year' in df.columns:
        yearly = df.groupby('year')['affected_families'].sum().reset_index()
        fig = px.bar(yearly, x='year', y='affected_families', title="Affected Families by Year")
        st.plotly_chart(fig, use_container_width=True)
    
    # Summary by Event Type
    st.markdown("#### 📊 Summary by Incident Type")
    if 'incident_name' in df.columns:
        incident_counts = df['incident_name'].value_counts().reset_index()
        incident_counts.columns = ['Incident Type', 'Count']
        fig = px.pie(incident_counts, values='Count', names='Incident Type', title="Incidents by Type")
        st.plotly_chart(fig, use_container_width=True)
    
    # Risk by municipality
    st.markdown("#### 🎯 Municipal Risk Assessment")
    risk_data = []
    for mun in df['municipality'].unique():
        mun_data = df[df['municipality'] == mun]
        avg_affected = mun_data['affected_families'].mean()
        risk_score = min(avg_affected / 10, 100)
        risk_data.append({
            "Municipality": mun,
            "Risk Score": round(risk_score, 1),
            "Risk Level": "High" if risk_score > 50 else "Medium" if risk_score > 20 else "Low"
        })
    
    risk_df = pd.DataFrame(risk_data).sort_values('Risk Score', ascending=False)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    
    # Trend chart
    if 'report_date' in df.columns:
        timeline = df.groupby('report_date')['affected_families'].sum().reset_index()
        fig = px.line(timeline, x='report_date', y='affected_families', title="Affected Families Trend")
        st.plotly_chart(fig, use_container_width=True)


# =============================================================================
# SECTION 5: PHOTO GALLERY
# =============================================================================

def show_photo_gallery():
    """Display photo gallery from all reports"""
    
    st.markdown("### 📸 Situation Report Photo Gallery")
    st.caption("Photos from municipal reports")
    
    reports = st.session_state.get('municipal_reports', [])
    
    photos = []
    for r in reports:
        photo = r.get('photo', {})
        if photo.get('file'):
            photos.append({
                "municipality": r.get('municipality'),
                "caption": photo.get('caption'),
                "file": photo.get('file'),
                "date": r.get('report_date')
            })
    
    if not photos:
        st.info("No photos uploaded yet")
        return
    
    cols = st.columns(3)
    for i, photo in enumerate(photos):
        with cols[i % 3]:
            st.markdown(f"**{photo.get('municipality')}**")
            st.caption(photo.get('caption', 'No caption'))
            st.caption(f"Date: {photo.get('date', 'N/A')}")
            st.markdown("---")


# =============================================================================
# SECTION 6: ARCHIVED SITREPS
# =============================================================================

def show_archived_sitreps():
    """Store and manage archived situation reports"""
    
    st.markdown("### 📁 Archived Situation Reports")
    st.caption("Store, view, and manage previous situation reports")
    
    # Initialize archived reports
    if 'archived_sitreps' not in st.session_state:
        st.session_state.archived_sitreps = []
    
    # Upload new archive
    with st.expander("📤 Upload Archived SitRep", expanded=False):
        with st.form("upload_archive_form"):
            col1, col2 = st.columns(2)
            with col1:
                archive_title = st.text_input("Report Title", placeholder="e.g., SITREP #01 - TS PAENG")
                archive_date = st.date_input("Report Date", date.today())
            with col2:
                archive_type = st.selectbox("Report Type", ["SITREP", "PDRA Report", "Consolidated Report", "Annual Report"])
                archive_incident = st.text_input("Incident Name", placeholder="e.g., Typhoon Paeng")
            
            archive_description = st.text_area("Description", placeholder="Brief description of the report")
            uploaded_file = st.file_uploader("Upload File", type=['pdf', 'docx', 'xlsx'], key="archive_upload")
            
            submitted = st.form_submit_button("📎 Upload to Archive")
            
            if submitted and archive_title and uploaded_file:
                # Save to local storage
                folder = "local_storage/sitrep_archives"
                os.makedirs(folder, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{uploaded_file.name}"
                file_path = os.path.join(folder, filename)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                archive = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": archive_title,
                    "date": archive_date.isoformat(),
                    "type": archive_type,
                    "incident": archive_incident,
                    "description": archive_description,
                    "file_path": file_path,
                    "filename": filename,
                    "file_size": get_file_size(file_path),
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.archived_sitreps.append(archive)
                st.success(f"✅ '{archive_title}' archived!")
                st.rerun()
    
    # Display archived reports
    if st.session_state.archived_sitreps:
        df = pd.DataFrame(st.session_state.archived_sitreps)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.selectbox("Filter by Type", ["All"] + list(df['type'].unique()))
        with col2:
            search = st.text_input("Search", placeholder="Search by title...")
        
        filtered = df.copy()
        if type_filter != "All":
            filtered = filtered[filtered['type'] == type_filter]
        if search:
            filtered = filtered[filtered['title'].str.contains(search, case=False)]
        
        st.dataframe(filtered[['title', 'date', 'type', 'incident', 'file_size']], use_container_width=True, hide_index=True)
        
        # Action buttons for each archive
        for archive in filtered.to_dict('records'):
            with st.expander(f"📄 {archive['title']} ({archive['date']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Type:** {archive['type']}")
                    st.markdown(f"**Incident:** {archive.get('incident', 'N/A')}")
                    st.markdown(f"**Description:** {archive.get('description', 'No description')}")
                with col2:
                    st.markdown(f"**Uploaded:** {archive.get('uploaded_at', 'N/A')[:10]}")
                    st.markdown(f"**File Size:** {archive.get('file_size', 'N/A')}")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if archive.get('file_path') and os.path.exists(archive['file_path']):
                        with open(archive['file_path'], "rb") as f:
                            st.download_button("📥 Download", f, file_name=archive['filename'], key=f"dl_archive_{archive['id']}")
                with col2:
                    st.button("🖨️ Print", key=f"print_archive_{archive['id']}")
                with col3:
                    if st.button("🗑️ Delete", key=f"del_archive_{archive['id']}"):
                        if archive.get('file_path') and os.path.exists(archive['file_path']):
                            os.remove(archive['file_path'])
                        st.session_state.archived_sitreps = [a for a in st.session_state.archived_sitreps if a['id'] != archive['id']]
                        st.rerun()
    else:
        st.info("No archived reports yet. Use the upload form above to add reports.")


# =============================================================================
# SECTION 7: RELATED MODULES
# =============================================================================

def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How Situation Report connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 DRRM Intelligence
        - Situation reports feed into hazard event database
        - Incident data validates risk models
        - Response effectiveness tracked over time
        - Historical data for predictive analytics
        
        ### 📋 Plan Management
        - Incident data informs DRRM plan updates
        - Response gaps identify needed PPAs
        - Resource allocation based on incident patterns
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 Climate Change
        - Weather patterns from situation reports
        - Climate adaptation effectiveness
        - Early warning system validation
        
        ### 📚 Trainings
        - Response actions linked to training
        - Capacity gaps identified from incidents
        - Training effectiveness measurement
        
        ### 📁 Knowledge Repository
        - Archived SITREPs stored for reference
        - PDRA guidelines and templates
        - Best practices documentation
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()
    with col2:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col3:
        if st.button("📚 Go to Trainings", use_container_width=True):
            st.session_state.navigation = "📚 TRAININGS"
            st.rerun()
    with col4:
        if st.button("📁 Go to Knowledge Repository", use_container_width=True):
            st.session_state.navigation = "📁 KNOWLEDGE REPOSITORY"
            st.rerun()


def get_file_size(file_path):
    """Get file size in human-readable format"""
    if not file_path or not os.path.exists(file_path):
        return "0 B"
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"