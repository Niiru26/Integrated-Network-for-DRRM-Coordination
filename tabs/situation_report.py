# tabs/situation_report.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import os
import json
from utils.supabase_client import is_connected

def show():
    """Display Simplified Situation Report Tab"""
    
    st.markdown("# 📡 SITUATION REPORT")
    st.caption("Official MPDRRMC Situation Report Form")
    
    # Create the main form - everything in ONE form
    with st.form("situation_report_form", clear_on_submit=False):
        
        # ===== HEADER SECTION =====
        st.markdown("### HEADER")
        
        col1, col2 = st.columns(2)
        with col1:
            sitrep_number = st.number_input("SITREP Number", min_value=1, value=1, step=1)
            incident_name = st.text_input("Incident Name", placeholder="e.g., Effects of TS PAENG (NALGAE)")
        with col2:
            report_date = st.date_input("Report Date", date.today())
            report_time = st.time_input("Report Time", datetime.now().time())
        
        st.markdown("---")
        
        # ===== I. SITUATION OVERVIEW =====
        st.markdown("### I. SITUATION OVERVIEW")
        
        pagasa_bulletin = st.text_area(
            "PAGASA Tropical Cyclone Bulletin",
            placeholder="Paste the latest PAGASA bulletin here...",
            height=100
        )
        
        st.markdown("#### Weather & Alert Level Statuses")
        
        municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                         "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
        
        weather_data = {}
        for mun in municipalities:
            col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
            with col1:
                st.markdown(f"**{mun}**")
            with col2:
                cloud = st.selectbox("Cloud", ["Clear", "Cloudy", "Light Rains", "Heavy Rains"], key=f"cloud_{mun}", label_visibility="collapsed")
            with col3:
                wind = st.selectbox("Wind", ["Calm", "Light", "Moderate", "Strong"], key=f"wind_{mun}", label_visibility="collapsed")
            with col4:
                alert = st.selectbox("Alert", ["White", "Blue", "Red"], key=f"alert_{mun}", label_visibility="collapsed")
            weather_data[mun] = {"cloud": cloud, "wind": wind, "alert": alert}
        
        overall_alert = st.selectbox("Overall Alert Status", ["White", "Blue", "Red"])
        
        st.markdown("---")
        
        # ===== II. RISK COMMUNICATION MONITOR =====
        st.markdown("### II. RISK COMMUNICATION MONITOR")
        
        st.markdown("| Issuance | Received Date | Received Time | Action | Disseminated Date | Disseminated Time |")
        st.markdown("|----------|---------------|---------------|--------|-------------------|-------------------|")
        
        # Simple text input for issuances
        num_issuances = st.number_input("Number of issuances to report", min_value=0, max_value=10, value=0)
        
        issuances = []
        for i in range(num_issuances):
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                issuance = st.text_input(f"Issuance {i+1}", key=f"issuance_{i}")
            with col2:
                rec_date = st.date_input("Rec Date", key=f"rec_date_{i}")
            with col3:
                rec_time = st.time_input("Rec Time", key=f"rec_time_{i}")
            with col4:
                action = st.selectbox("Action", ["✓", "✗", "Pending"], key=f"action_{i}")
            with col5:
                diss_date = st.date_input("Diss Date", key=f"diss_date_{i}")
            with col6:
                diss_time = st.time_input("Diss Time", key=f"diss_time_{i}")
            issuances.append({
                "issuance": issuance, "rec_date": rec_date, "rec_time": rec_time,
                "action": action, "diss_date": diss_date, "diss_time": diss_time
            })
        
        st.markdown("---")
        
        # ===== III. RISK AND IMPACT ASSESSMENT =====
        st.markdown("### III. RISK AND IMPACT ASSESSMENT")
        st.caption("Barangays susceptible to landslides and flooding")
        
        # Simplified - just a few key barangays
        risk_data = {}
        sample_barangays = ["Chupac (Barlig)", "Gawana (Barlig)", "Bagnen Oriente (Bauko)", "Poblacion (Bontoc)"]
        
        for barangay in sample_barangays:
            col1, col2, col3 = st.columns([1.5, 1, 1])
            with col1:
                st.markdown(barangay)
            with col2:
                landslide = st.selectbox("Landslide Risk", ["", "VHL", "HL", "ML"], key=f"landslide_{barangay}", label_visibility="collapsed")
            with col3:
                flood = st.selectbox("Flood Risk", ["", "VHF", "HF", "MF"], key=f"flood_{barangay}", label_visibility="collapsed")
            risk_data[barangay] = {"landslide": landslide, "flood": flood}
        
        st.markdown("---")
        
        # ===== IV. PDRA RATINGS =====
        st.markdown("### IV. PRE-DISASTER RISK ASSESSMENT (PDRA)")
        
        col1, col2 = st.columns(2)
        with col1:
            probability = st.selectbox("Probability Rating", ["", "1 - Unlikely", "2 - Less Likely", "3 - Highly Likely", "4 - Certain/Imminent"])
        with col2:
            impact = st.selectbox("Impact Rating", ["", "1 - Negligible", "2 - Minor", "3 - Moderate", "4 - Major", "5 - Catastrophic"])
        
        st.markdown("---")
        
        # ===== V. INCIDENTS MONITORED =====
        st.markdown("### V. INCIDENTS MONITORED")
        
        incidents_data = {}
        for mun in municipalities:
            with st.expander(f"📋 {mun}"):
                incidents = st.text_area("Incidents", placeholder="No untoward incident reported", key=f"incident_{mun}", height=60)
                casualties = st.text_input("Casualties", placeholder="e.g., 0 dead, 2 injured", key=f"casualty_{mun}")
                incidents_data[mun] = {"incidents": incidents, "casualties": casualties}
        
        st.markdown("---")
        
        # ===== VI. STATUS OF LIFELINES =====
        st.markdown("### VI. STATUS OF LIFELINES")
        
        st.markdown("#### National Roads")
        national_roads_status = st.text_area("National Roads Status", placeholder="Report status of national roads", height=80)
        
        st.markdown("#### Provincial Roads")
        provincial_roads_status = st.text_area("Provincial Roads Status", placeholder="Report status of provincial roads", height=80)
        
        st.markdown("#### Power & Communication")
        power_comm_data = {}
        for mun in municipalities:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(mun)
            with col2:
                power = st.selectbox("Power", ["Normal", "Intermittent", "No Power"], key=f"power_{mun}", label_visibility="collapsed")
            with col3:
                comm = st.selectbox("Comm", ["Normal", "Intermittent", "No Signal"], key=f"comm_{mun}", label_visibility="collapsed")
            power_comm_data[mun] = {"power": power, "comm": comm}
        
        st.markdown("---")
        
        # ===== VII. DISPLACED POPULATION & DAMAGES =====
        st.markdown("### VII. DISPLACED POPULATION & DAMAGES")
        
        col1, col2 = st.columns(2)
        with col1:
            families_ec = st.number_input("Families in ECs", min_value=0, value=0)
            persons_ec = st.number_input("Persons in ECs", min_value=0, value=0)
        with col2:
            families_out = st.number_input("Families Outside ECs", min_value=0, value=0)
            persons_out = st.number_input("Persons Outside ECs", min_value=0, value=0)
        
        col1, col2 = st.columns(2)
        with col1:
            totally_damaged = st.number_input("Totally Damaged Houses", min_value=0, value=0)
            partially_damaged = st.number_input("Partially Damaged Houses", min_value=0, value=0)
        with col2:
            affected_families = st.number_input("Affected Families", min_value=0, value=0)
            affected_persons = st.number_input("Affected Persons", min_value=0, value=0)
        
        st.markdown("---")
        
        # ===== VIII. RESOURCES PROVIDED =====
        st.markdown("### VIII. RESOURCES PROVIDED")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            food_packs = st.number_input("Food Packs", min_value=0, value=0)
        with col2:
            hygiene_kits = st.number_input("Hygiene Kits", min_value=0, value=0)
        with col3:
            family_kits = st.number_input("Family Kits", min_value=0, value=0)
        
        st.markdown("---")
        
        # ===== IX. RESPONSE ACTIONS =====
        st.markdown("### IX. RESPONSE ACTIONS")
        response_actions = st.text_area("Response Actions Taken", height=100)
        
        st.markdown("---")
        
        # ===== X. NEEDS ASSESSMENT =====
        st.markdown("### X. NEEDS ASSESSMENT")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            priority1 = st.text_area("Priority 1", placeholder="Food, Medical, Water", height=80)
        with col2:
            priority2 = st.text_area("Priority 2", placeholder="Shelter, Clothing", height=80)
        with col3:
            priority3 = st.text_area("Priority 3", placeholder="Cash for Work", height=80)
        
        st.markdown("---")
        
        # ===== XI. PHOTO DOCUMENTATION =====
        st.markdown("### XI. PHOTO DOCUMENTATION")
        
        photos = []
        for i in range(3):
            col1, col2 = st.columns(2)
            with col1:
                photo = st.file_uploader(f"Photo {i+1}", type=['jpg', 'jpeg', 'png'], key=f"photo_{i}")
            with col2:
                caption = st.text_input(f"Caption {i+1}", key=f"caption_{i}")
            if photo:
                photos.append({"file": photo.name, "caption": caption})
        
        st.markdown("---")
        
        # ===== SUBMIT BUTTON =====
        submitted = st.form_submit_button("💾 Save Situation Report", type="primary", use_container_width=True)
        
        if submitted:
            # Create report dictionary
            report = {
                "sitrep_number": sitrep_number,
                "incident_name": incident_name,
                "report_date": report_date.isoformat(),
                "report_time": report_time.strftime("%H:%M"),
                "pagasa_bulletin": pagasa_bulletin,
                "weather_data": weather_data,
                "overall_alert": overall_alert,
                "issuances": issuances,
                "risk_data": risk_data,
                "probability": probability,
                "impact": impact,
                "incidents_data": incidents_data,
                "national_roads_status": national_roads_status,
                "provincial_roads_status": provincial_roads_status,
                "power_comm_data": power_comm_data,
                "displaced": {
                    "families_ec": families_ec,
                    "persons_ec": persons_ec,
                    "families_out": families_out,
                    "persons_out": persons_out
                },
                "damages": {
                    "totally_damaged": totally_damaged,
                    "partially_damaged": partially_damaged,
                    "affected_families": affected_families,
                    "affected_persons": affected_persons
                },
                "resources": {
                    "food_packs": food_packs,
                    "hygiene_kits": hygiene_kits,
                    "family_kits": family_kits
                },
                "response_actions": response_actions,
                "needs": {
                    "priority1": priority1,
                    "priority2": priority2,
                    "priority3": priority3
                },
                "photos": photos,
                "created_at": datetime.now().isoformat()
            }
            
            # Save locally
            folder = "local_storage/situation_reports"
            os.makedirs(folder, exist_ok=True)
            filename = f"sitrep_{sitrep_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = os.path.join(folder, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, default=str)
            
            st.success(f"✅ Situation Report #{sitrep_number} saved successfully!")
            st.balloons()