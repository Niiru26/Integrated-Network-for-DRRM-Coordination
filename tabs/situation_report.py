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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 PDRA Wizard",
        "📝 Municipal Data Entry",
        "📊 Provincial Consolidation",
        "📈 Predictive Analysis",
        "📸 Photo Gallery",
        "📜 Reference Guide"
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
        show_reference_guide()


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
             "🌋 Other Hazard (Landslide, Earthquake, Fire)"],
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
        forecast = weather.get('forecast', {})
        
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
        
        # What to expect
        st.markdown("#### 📋 What to Expect")
        expectations = st.multiselect("Select anticipated situations", [
            "Influx of people (travelers/visitors)",
            "Vehicular accidents",
            "Fire incidents (forest/structural)",
            "Prolonged period of hot and humid weather",
            "Increase of heat-related stresses on health",
            "Thunderstorms",
            "Food poisoning",
            "Gastroenteritis cases"
        ])
        
        # Alert level
        st.markdown("#### 🚨 Alert Level Status")
        alert_level = st.selectbox("Alert Level", ["Alpha", "Blue", "Red", "White"])
        
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
        
        hazard_type = st.selectbox("Hazard Type", ["Landslide", "Earthquake", "Forest Fire", "Drought", "Other"])
        
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
# SECTION 2: MDRRMO DATA ENTRY (with Roads Management)
# =============================================================================

def show_mdrrmo_data_entry():
    """Municipal data entry with roads management"""
    
    st.markdown("### 📝 Municipal Situation Report Entry")
    st.caption("MDRRMO Staff: Enter your municipality's data here")
    
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # National Roads list with unique IDs
    national_roads = [
        {"id": 1, "name": "Bontoc - Baguio Road"},
        {"id": 2, "name": "Bontoc - Cadre Road"},
        {"id": 3, "name": "Dantay - Sagada Road"},
        {"id": 4, "name": "Junction Talubin - Barlig - Natonin - Paracelis - Calaccad Road"},
        {"id": 5, "name": "Mt. Province - Cagayan via Tabuk - Enrile Road"},
        {"id": 6, "name": "Mt. Province - Ilocos Sur Road via Kayan"},
        {"id": 7, "name": "Mt. Province - Ilocos Sur Road via Tue"},
        {"id": 8, "name": "Mt. Province - Nueva Vizcaya Road"}
    ]
    
    with st.form("municipal_report_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            municipality = st.selectbox("Municipality *", municipalities, key="mun_select")
            report_date = st.date_input("Report Date *", date.today(), key="report_date")
            report_time = st.time_input("Report Time *", datetime.now().time(), key="report_time")
            sitrep_number = st.number_input("SITREP Number *", min_value=1, value=1, step=1, key="sitrep_num")
            incident_name = st.text_input("Incident Name *", placeholder="e.g., TS PAENG", key="incident_name")
        
        with col2:
            alert_level = st.selectbox("Alert Level *", ["Alpha", "Blue", "Red", "White"], key="alert_level")
            submitted_by = st.text_input("Reported By *", placeholder="Name and Position", key="submitted_by")
            contact_number = st.text_input("Contact Number", key="contact_num")
        
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
        incidents = st.text_area("Incident/s Reported", placeholder="List all incidents per barangay", height=100, key="incidents")
        casualties = st.text_input("Casualties", placeholder="e.g., 0 dead, 2 injured, 1 missing", key="casualties")
        
        # Roads Management - FIXED with unique keys
        st.markdown("#### 🛣️ National Roads Status")
        st.caption("Select roads in your municipality and their status")
        
        roads_status = []
        for road in national_roads:
            road_id = road["id"]
            road_name = road["name"]
            # Create a unique key for each checkbox using road_id
            include = st.checkbox(road_name, key=f"road_include_{road_id}")
            
            if include:
                col1, col2 = st.columns(2)
                with col1:
                    traffic = st.selectbox(
                        "Traffic", 
                        ["Passable", "One Lane Passable", "Not Passable"], 
                        key=f"road_traffic_{road_id}"
                    )
                with col2:
                    remarks = st.text_input(
                        "Remarks", 
                        placeholder="Road section details", 
                        key=f"road_remarks_{road_id}"
                    )
                roads_status.append({
                    "road": road_name,
                    "traffic": traffic,
                    "remarks": remarks
                })
        
        # Utilities
        st.markdown("#### 🔌 Utilities")
        col1, col2 = st.columns(2)
        with col1:
            power = st.selectbox("Power Status", ["Normal", "Intermittent", "No Power"], key="power")
            power_remarks = st.text_input("Power Remarks", key="power_remarks")
        with col2:
            comm = st.selectbox("Communication Status", ["Normal", "Intermittent", "No Signal"], key="comm")
            comm_remarks = st.text_input("Communication Remarks", key="comm_remarks")
        
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
        
        # Response
        st.markdown("#### 🚑 Response Actions")
        response_actions = st.text_area("Response Actions Taken", height=100, key="response")
        
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
            report = {
                "id": int(datetime.now().timestamp() * 1000),
                "sitrep_number": sitrep_number,
                "municipality": municipality,
                "report_date": report_date.isoformat(),
                "report_time": report_time.strftime("%H:%M"),
                "incident_name": incident_name,
                "alert_level": alert_level,
                "submitted_by": submitted_by,
                "contact_number": contact_number,
                "weather": {"cloud": cloud, "wind": wind, "precipitation": precipitation},
                "incidents": incidents,
                "casualties": casualties,
                "roads": roads_status,
                "utilities": {"power": power, "power_remarks": power_remarks, "communication": comm, "comm_remarks": comm_remarks},
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
# SECTION 3: PROVINCIAL CONSOLIDATION (with Auto-Extraction)
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
    
    # Roads Summary
    st.markdown("#### 🛣️ National Roads Status")
    roads_summary = []
    for r in reports:
        for road in r.get('roads', []):
            roads_summary.append({
                "Municipality": r.get('municipality'),
                "Road": road.get('road'),
                "Traffic": road.get('traffic'),
                "Remarks": road.get('remarks')
            })
    if roads_summary:
        st.dataframe(pd.DataFrame(roads_summary), use_container_width=True, hide_index=True)
    
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
    
    # Export option
    if st.button("📥 Export as PDF"):
        st.info("PDF export coming soon")


# =============================================================================
# SECTION 4: PREDICTIVE ANALYSIS
# =============================================================================

def show_predictive_analysis():
    """Predictive analysis from historical reports"""
    
    st.markdown("### 📈 Predictive Analysis")
    st.caption("Analyze patterns and predict future impacts")
    
    reports = st.session_state.get('municipal_reports', [])
    
    if len(reports) < 5:
        st.info("Need at least 5 reports for meaningful analysis")
        return
    
    df = pd.DataFrame(reports)
    
    # Extract numeric fields
    df['affected_families'] = df['damages'].apply(lambda x: x.get('affected_families', 0) if isinstance(x, dict) else 0)
    
    # Risk by municipality
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
        df['report_date'] = pd.to_datetime(df['report_date'])
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
# SECTION 6: REFERENCE GUIDE
# =============================================================================

def show_reference_guide():
    """Reference guide for PDRA and SitRep"""
    
    st.markdown("### 📜 Reference Guide")
    st.caption("Official guidelines and reference materials")
    
    tabs = st.tabs(["PDRA Guidelines", "Hazard Classification", "Alert Levels", "Probability & Impact Scales"])
    
    with tabs[0]:
        st.markdown("""
        ### 📋 PDRA Guidelines
        
        **Legal Bases:**
        - NDRRMC Memorandum Circular No. 63, s. 2021
        - Republic Act No. 10121 – Philippine DRRM Act of 2010
        - Sendai Framework for Disaster Risk Reduction 2015-2030
        
        **Triggers for PDRA:**
        - Threat of hydro-meteorological hazards
        - Existence of slow-onset geological hazards
        - Threat to disruption of lifelines
        - Threat of disease incidence
        - Threat to environment and natural resources
        """)
    
    with tabs[1]:
        st.markdown("""
        ### 🌊 Hazard Classification (UNDRR)
        
        | Category | Examples |
        |----------|----------|
        | Hydrometeorological | Typhoons, floods, droughts, thunderstorms |
        | Geological | Earthquakes, landslides, volcanic eruptions |
        | Biological | Disease outbreaks, epidemics |
        | Technological | Industrial accidents, infrastructure failures |
        """)
    
    with tabs[2]:
        st.markdown("""
        ### 🚨 Alert Levels
        
        | Level | Description | Action |
        |-------|-------------|--------|
        | **Alpha** | Initial monitoring | Prepare resources, monitor situation |
        | **Blue** | Enhanced preparedness | Activate EOC, preposition supplies |
        | **Red** | Response operations | Full activation, response deployment |
        | **White** | All clear | Stand down, recovery phase |
        """)
    
    with tabs[3]:
        st.markdown("""
        ### 📊 Probability & Impact Scales
        
        **Probability Rating:**
        - **1 - Unlikely**: Will not happen in 72 hours
        - **2 - Less Likely**: <50% chance of affecting 2+ areas
        - **3 - Highly Likely**: >50% chance, 51-75% area exposed
        - **4 - Certain/Imminent**: 100% chance in next 72 hours
        
        **Impact Rating:**
        - **1 - Negligible**: No casualties/damage
        - **2 - Minor**: DRRMC can manage alone
        - **3 - Moderate**: Manage with minimal assistance
        - **4 - Major**: Progressive assistance required
        - **5 - Catastrophic**: Overwhelmed, full assistance needed
        """)