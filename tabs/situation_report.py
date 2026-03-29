# tabs/situation_report.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected, auto_sync_table
from utils.pagasa_api import fetch_weather_data, refresh_weather_data
import plotly.express as px
import json

def show():
    """Display Situation Report Tab with Multi-User Data Entry"""
    
    # Load weather data on first load
    if 'pagasa_weather' not in st.session_state:
        with st.spinner("Fetching weather data from PAGASA..."):
            fetch_weather_data()
    
    st.markdown("# 📡 SITUATION REPORT")
    st.caption("Enhanced Situation Report Form with Multi-User Data Entry and Predictive Analysis")
    
    # Show sync status and user info
    col_status, col_weather = st.columns([2, 1])
    with col_status:
        if is_connected():
            st.success("☁️ Real-time Collaboration Enabled - Multiple users can input data simultaneously")
        else:
            st.warning("⚠️ Offline Mode - Single user only")
    
    with col_weather:
        # Weather widget in the top right
        with st.container():
            st.markdown("### 🌦️ Current Weather")
            
            weather = st.session_state.get('pagasa_weather', {})
            cyclones = weather.get('cyclones', {})
            rainfall = weather.get('rainfall', {})
            forecast = weather.get('forecast', {})
            today_forecast = forecast.get('forecast', [{}])[0] if forecast.get('forecast') else {}
            
            if cyclones.get('has_active'):
                st.error(f"⚠️ {cyclones.get('status', 'Active Cyclone')[:50]}")
            else:
                st.success("✅ No active cyclones")
            
            if rainfall.get('has_advisory'):
                level = rainfall.get('advisory_level')
                if level == "Red":
                    st.error(f"🔴 {level} Rainfall Advisory")
                elif level == "Orange":
                    st.warning(f"🟠 {level} Rainfall Advisory")
                else:
                    st.warning(f"🟡 {level} Rainfall Advisory")
            
            if today_forecast:
                st.caption(f"🌡️ {today_forecast.get('temp_min', 'N/A')}°C - {today_forecast.get('temp_max', 'N/A')}°C")
                st.caption(f"💨 {today_forecast.get('wind_speed', 'N/A')}")
            
            if st.button("🔄 Refresh", key="refresh_weather_top"):
                refresh_weather_data()
                st.rerun()
    
    # Initialize session state for reports
    if 'municipal_reports' not in st.session_state:
        st.session_state.municipal_reports = []
    
    if 'main_reports' not in st.session_state:
        st.session_state.main_reports = []
    
    if 'sitrep_photos' not in st.session_state:
        st.session_state.sitrep_photos = []
    
    # Create tabs for different user roles and views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 MDRRMO Data Entry",
        "📊 PDRRMO Consolidation",
        "📈 Predictive Analysis",
        "📸 Photo Documentation",
        "📋 Archived Reports",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_mdrrmo_data_entry()
    
    with tab2:
        show_pdrrmo_consolidation()
    
    with tab3:
        show_predictive_analysis()
    
    with tab4:
        show_photo_documentation()
    
    with tab5:
        show_archived_reports()
    
    with tab6:
        show_related_modules()


def show_mdrrmo_data_entry():
    """MDRRMO Data Entry Form - for municipal staff to input their data"""
    
    st.markdown("### Municipal Situation Report Entry")
    st.caption("MDRRMO Staff: Enter your municipality's data here. All entries are automatically synced for PDRRMO consolidation.")
    
    # Select municipality
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    with st.form("sitrep_entry_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            municipality = st.selectbox("Select Municipality *", municipalities, key="sitrep_municipality")
            report_date = st.date_input("Report Date *", date.today(), key="sitrep_date")
            report_time = st.time_input("Report Time *", datetime.now().time(), key="sitrep_time")
            sitrep_number = st.number_input("SITREP Number *", min_value=1, value=1, step=1, key="sitrep_number")
        
        with col2:
            incident_name = st.text_input("Incident Name *", placeholder="e.g., SITREP #01: Effects of TS PAENG (NALGAE)", key="sitrep_incident")
            alert_level = st.selectbox("Alert Level *", ["Alpha", "Blue", "Red", "White"], key="sitrep_alert")
            submitted_by = st.text_input("Reported By *", placeholder="Name and Position", key="sitrep_submitted_by")
            contact_number = st.text_input("Contact Number", placeholder="Mobile number for follow-up", key="sitrep_contact")
        
        st.markdown("---")
        st.markdown("### I. SITUATION OVERVIEW")
        
        # Weather section
        st.markdown("#### 🌦️ Weather Conditions")
        
        # Auto-fill with PAGASA data if available
        default_cloud = "Partly Cloudy"
        default_wind = "Light Wind"
        default_precip = "Light"
        
        if 'pagasa_weather' in st.session_state:
            forecast = st.session_state.pagasa_weather.get('forecast', {}).get('forecast', [])
            if forecast:
                today_weather = forecast[0]
                weather_desc = today_weather.get('weather', '').lower()
                if 'rain' in weather_desc:
                    if 'light' in weather_desc:
                        default_cloud = "Light Rains"
                        default_precip = "Light"
                    elif 'moderate' in weather_desc:
                        default_cloud = "Moderate Rains"
                        default_precip = "Moderate"
                    elif 'heavy' in weather_desc:
                        default_cloud = "Heavy Rains"
                        default_precip = "Heavy"
                elif 'cloudy' in weather_desc:
                    default_cloud = "Cloudy"
                elif 'clear' in weather_desc:
                    default_cloud = "Clear"
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cloud_condition = st.selectbox("Cloud Condition",
                ["Clear", "Partly Cloudy", "Cloudy", "Light Rains", "Moderate Rains", "Heavy Rains", "Torrential Rains"],
                key="sitrep_cloud")
        with col2:
            wind_condition = st.selectbox("Wind Condition",
                ["Calm", "Light Wind", "Moderate Wind", "Strong Wind", "Gale Force", "Storm Force"],
                key="sitrep_wind")
        with col3:
            precipitation = st.selectbox("Precipitation",
                ["None", "Light", "Moderate", "Heavy", "Torrential"],
                key="sitrep_precip")
        
        st.markdown("#### 📢 PAGASA Advisories")
        pagasa_bulletin = st.text_area("Latest PAGASA Tropical Cyclone Bulletin",
                                        placeholder="Paste or summarize the latest PAGASA bulletin...",
                                        height=100,
                                        key="sitrep_pagasa_bulletin")
        pagasa_link = st.text_input("PAGASA Reference Link", 
                                    placeholder="https://www.pagasa.dost.gov.ph/tropical-cyclone/severe-weather-bulletin",
                                    key="sitrep_pagasa_link")
        
        st.markdown("---")
        st.markdown("### II. INCIDENTS MONITORED")
        
        col1, col2 = st.columns(2)
        with col1:
            incidents_reported = st.text_area("Incident/s Reported", placeholder="List all incidents per barangay", height=100, key="sitrep_incidents")
            casualties = st.text_input("Casualties", placeholder="e.g., 0 dead, 2 injured, 1 missing", key="sitrep_casualties")
        with col2:
            affected_areas = st.text_area("Affected Areas/Barangays", placeholder="List barangays affected", height=100, key="sitrep_affected_areas")
            actions_taken = st.text_area("Initial Actions Taken", placeholder="Response actions already implemented", height=100, key="sitrep_actions")
        
        st.markdown("---")
        st.markdown("### III. STATUS OF LIFELINES")
        
        st.markdown("#### Roads")
        col1, col2 = st.columns(2)
        with col1:
            national_roads_status = st.selectbox("National Roads Status", 
                ["Fully Passable", "One Lane Passable", "Not Passable", "Closed"], 
                key="sitrep_national_roads")
            national_roads_remarks = st.text_input("Remarks", placeholder="Specific sections affected", key="sitrep_national_remarks")
        with col2:
            provincial_roads_status = st.selectbox("Provincial Roads Status", 
                ["Fully Passable", "One Lane Passable", "Not Passable", "Closed"], 
                key="sitrep_provincial_roads")
            provincial_roads_remarks = st.text_input("Remarks", placeholder="Specific sections affected", key="sitrep_provincial_remarks")
        
        st.markdown("#### Utilities")
        col1, col2, col3 = st.columns(3)
        with col1:
            power_status = st.selectbox("Power Status", ["Normal", "Intermittent", "No Power"], key="sitrep_power")
            power_remarks = st.text_input("Remarks", placeholder="Areas affected", key="sitrep_power_remarks")
        with col2:
            water_status = st.selectbox("Water Status", ["Normal", "Intermittent", "No Supply"], key="sitrep_water")
            water_remarks = st.text_input("Remarks", placeholder="Areas affected", key="sitrep_water_remarks")
        with col3:
            comm_status = st.selectbox("Communication Status", ["Normal", "Intermittent", "No Signal"], key="sitrep_comm")
            comm_remarks = st.text_input("Remarks", placeholder="Network/s affected", key="sitrep_comm_remarks")
        
        st.markdown("---")
        st.markdown("### IV. DISPLACED POPULATION")
        
        col1, col2 = st.columns(2)
        with col1:
            families_in_ec = st.number_input("Families in ECs", min_value=0, value=0, key="sitrep_families_ec")
            persons_in_ec = st.number_input("Persons in ECs", min_value=0, value=0, key="sitrep_persons_ec")
        with col2:
            families_outside = st.number_input("Families Outside ECs", min_value=0, value=0, key="sitrep_families_out")
            persons_outside = st.number_input("Persons Outside ECs", min_value=0, value=0, key="sitrep_persons_out")
        
        st.markdown("---")
        st.markdown("### V. DAMAGE ASSESSMENT")
        
        col1, col2 = st.columns(2)
        with col1:
            totally_damaged = st.number_input("Totally Damaged Houses", min_value=0, value=0, key="sitrep_totally_damaged")
            partially_damaged = st.number_input("Partially Damaged Houses", min_value=0, value=0, key="sitrep_partially_damaged")
        with col2:
            affected_families = st.number_input("Affected Families", min_value=0, value=0, key="sitrep_affected_families")
            affected_persons = st.number_input("Affected Persons", min_value=0, value=0, key="sitrep_affected_persons")
        
        st.markdown("---")
        st.markdown("### VI. RESOURCES PROVIDED")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            food_packs = st.number_input("Food Packs Distributed", min_value=0, value=0, key="sitrep_food_packs")
        with col2:
            hygiene_kits = st.number_input("Hygiene Kits Distributed", min_value=0, value=0, key="sitrep_hygiene_kits")
        with col3:
            family_kits = st.number_input("Family Kits Distributed", min_value=0, value=0, key="sitrep_family_kits")
        
        st.markdown("---")
        st.markdown("### VII. RESPONSE ACTIVITIES")
        
        response_activities = st.text_area("Response Actions Taken", 
            placeholder="List response activities, deployments, and operations", 
            height=100,
            key="sitrep_response")
        
        st.markdown("### VIII. NEEDS ASSESSMENT")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            priority1 = st.text_area("Priority 1 Needs", placeholder="Search & Rescue, Food, Medical, Water", height=80, key="sitrep_priority1")
        with col2:
            priority2 = st.text_area("Priority 2 Needs", placeholder="Shelter, Clothing, Non-food items", height=80, key="sitrep_priority2")
        with col3:
            priority3 = st.text_area("Priority 3 Needs", placeholder="Cash for Work, Rehabilitation", height=80, key="sitrep_priority3")
        
        st.markdown("### IX. REMARKS")
        remarks = st.text_area("Additional Remarks", placeholder="Other relevant information", height=80, key="sitrep_remarks")
        
        submitted = st.form_submit_button("💾 Submit Situation Report", type="primary")
        
        if submitted:
            if not municipality or not incident_name:
                st.error("Please fill in all required fields (*)")
                return
            
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
                "weather": {
                    "cloud": cloud_condition,
                    "wind": wind_condition,
                    "precipitation": precipitation,
                    "pagasa_bulletin": pagasa_bulletin,
                    "pagasa_link": pagasa_link
                },
                "incidents": {
                    "reported": incidents_reported,
                    "casualties": casualties,
                    "affected_areas": affected_areas,
                    "actions_taken": actions_taken
                },
                "lifelines": {
                    "national_roads": {"status": national_roads_status, "remarks": national_roads_remarks},
                    "provincial_roads": {"status": provincial_roads_status, "remarks": provincial_roads_remarks},
                    "power": {"status": power_status, "remarks": power_remarks},
                    "water": {"status": water_status, "remarks": water_remarks},
                    "communication": {"status": comm_status, "remarks": comm_remarks}
                },
                "displaced": {
                    "families_in_ec": families_in_ec,
                    "persons_in_ec": persons_in_ec,
                    "families_outside": families_outside,
                    "persons_outside": persons_outside
                },
                "damages": {
                    "totally_damaged_houses": totally_damaged,
                    "partially_damaged_houses": partially_damaged,
                    "affected_families": affected_families,
                    "affected_persons": affected_persons
                },
                "resources": {
                    "food_packs": food_packs,
                    "hygiene_kits": hygiene_kits,
                    "family_kits": family_kits
                },
                "response_activities": response_activities,
                "needs": {
                    "priority1": priority1,
                    "priority2": priority2,
                    "priority3": priority3
                },
                "remarks": remarks,
                "created_at": datetime.now().isoformat(),
                "status": "Submitted"
            }
            
            auto_sync_add('municipal_reports', 'municipal_reports', report)
            st.success(f"✅ Situation Report #{sitrep_number} for {municipality} submitted and synced!")
            st.balloons()
            st.rerun()


def show_pdrrmo_consolidation():
    """PDRRMO Consolidation View - Aggregates all municipal reports"""
    
    st.markdown("### Provincial Situation Report Consolidation")
    st.caption("Consolidated data from all municipalities - Auto-updates as new reports come in")
    
    auto_sync_table('municipal_reports', 'municipal_reports')
    reports = st.session_state.get('municipal_reports', [])
    
    if not reports:
        st.info("No situation reports submitted yet. MDRRMO staff can enter data in the Data Entry tab.")
        return
    
    df = pd.DataFrame(reports)
    
    st.markdown("#### 📊 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Municipalities Reporting", df['municipality'].nunique())
    with col2:
        st.metric("Total Reports", len(df))
    with col3:
        total_affected = df['damages'].apply(lambda x: x.get('affected_families', 0) if isinstance(x, dict) else 0).sum()
        st.metric("Affected Families", f"{total_affected:,}")
    with col4:
        active_alerts = len(df[df['alert_level'] != 'White'])
        st.metric("Active Alerts", active_alerts)
    
    st.markdown("#### 📋 Municipal Reports")
    
    for idx, row in df.iterrows():
        with st.expander(f"📋 {row['municipality']} - SITREP #{row['sitrep_number']} ({row['report_date']}) | Alert: {row.get('alert_level', 'N/A')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Incident:** {row.get('incident_name', 'N/A')}")
                st.markdown(f"**Reported By:** {row.get('submitted_by', 'N/A')}")
                
                weather = row.get('weather', {})
                st.markdown(f"**Weather:** {weather.get('cloud', 'N/A')}, {weather.get('wind', 'N/A')}")
                
                damages = row.get('damages', {})
                st.markdown(f"**Damaged Houses:** {damages.get('totally_damaged_houses', 0)} Total / {damages.get('partially_damaged_houses', 0)} Partial")
            
            with col2:
                displaced = row.get('displaced', {})
                st.markdown(f"**Displaced:** {displaced.get('families_in_ec', 0)} in ECs")
                st.markdown(f"**Affected:** {damages.get('affected_families', 0)} families")
                
                resources = row.get('resources', {})
                st.markdown(f"**Resources:** {resources.get('food_packs', 0)} food packs")
            
            st.markdown(f"**Incidents:** {row.get('incidents', {}).get('reported', 'None reported')}")
            st.markdown(f"**Response:** {row.get('response_activities', 'None reported')}")
            
            needs = row.get('needs', {})
            st.markdown(f"**Needs:** P1: {needs.get('priority1', 'N/A')}")


def show_predictive_analysis():
    """Predictive and Projective Analysis using historical data"""
    
    st.markdown("### Predictive & Projective Analysis")
    st.caption("Analysis of historical situation reports to predict future impacts")
    
    auto_sync_table('municipal_reports', 'municipal_reports')
    reports = st.session_state.get('municipal_reports', [])
    
    if len(reports) < 3:
        st.info("Need at least 3 reports for meaningful predictive analysis. Continue collecting data.")
        return
    
    df = pd.DataFrame(reports)
    
    # Extract numeric fields
    df['affected_families'] = df['damages'].apply(lambda x: x.get('affected_families', 0) if isinstance(x, dict) else 0)
    df['totally_damaged'] = df['damages'].apply(lambda x: x.get('totally_damaged_houses', 0) if isinstance(x, dict) else 0)
    
    st.markdown("#### 📊 Historical Trends")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(df.groupby('municipality')['affected_families'].sum().reset_index(),
                     x='municipality', y='affected_families',
                     title='Total Affected Families by Municipality')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.pie(df, values='totally_damaged', names='municipality', title='Distribution of Damaged Houses')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### 🔮 Risk Assessment")
    
    risk_scores = []
    for municipality in df['municipality'].unique():
        mun_data = df[df['municipality'] == municipality]
        avg_affected = mun_data['affected_families'].mean()
        risk_score = min(avg_affected / 10, 100)
        risk_scores.append({
            "Municipality": municipality,
            "Risk Score": round(risk_score, 1),
            "Risk Level": "High" if risk_score > 50 else "Medium" if risk_score > 20 else "Low",
            "Reports": len(mun_data)
        })
    
    risk_df = pd.DataFrame(risk_scores).sort_values('Risk Score', ascending=False)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)


def show_photo_documentation():
    """Photo documentation section"""
    
    st.markdown("### Photo Documentation")
    st.caption("Visual documentation of incidents, damages, and response activities")
    
    if 'sitrep_photos' not in st.session_state:
        st.session_state.sitrep_photos = []
    
    st.markdown("#### 📸 Upload Photos")
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    col1, col2 = st.columns(2)
    with col1:
        photo_municipality = st.selectbox("Municipality", municipalities, key="photo_municipality")
        photo_location = st.text_input("Location", placeholder="Specific barangay or sitio", key="photo_location")
        photo_description = st.text_area("Description", placeholder="What does this photo show?", key="photo_description")
    with col2:
        photo_incident = st.text_input("Related Incident", placeholder="e.g., Landslide", key="photo_incident")
        photo_date = st.date_input("Photo Date", date.today(), key="photo_date")
        photographer = st.text_input("Photographer", placeholder="Name", key="photo_photographer")
    
    uploaded_files = st.file_uploader("Select photos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True, key="photo_upload")
    
    if uploaded_files and st.button("📸 Add Photos", key="add_photos"):
        for file in uploaded_files:
            photo = {
                "id": int(datetime.now().timestamp() * 1000),
                "municipality": photo_municipality,
                "location": photo_location,
                "description": photo_description,
                "incident": photo_incident,
                "date": photo_date.isoformat(),
                "photographer": photographer,
                "filename": file.name,
                "uploaded_at": datetime.now().isoformat()
            }
            st.session_state.sitrep_photos.append(photo)
        st.success(f"✅ {len(uploaded_files)} photos added!")
        st.rerun()
    
    if st.session_state.sitrep_photos:
        st.markdown("#### 📷 Photo Gallery")
        for photo in reversed(st.session_state.sitrep_photos):
            with st.expander(f"📸 {photo.get('municipality')} - {photo.get('location')} ({photo.get('date')})"):
                st.markdown(f"**Description:** {photo.get('description', 'No description')}")
                st.markdown(f"**Incident:** {photo.get('incident', 'N/A')}")
                st.markdown(f"**Photographer:** {photo.get('photographer', 'Unknown')}")
                if st.button(f"🗑️ Delete", key=f"del_photo_{photo.get('id')}"):
                    st.session_state.sitrep_photos = [p for p in st.session_state.sitrep_photos if p.get('id') != photo.get('id')]
                    st.rerun()


def show_archived_reports():
    """View archived situation reports"""
    
    st.markdown("### Archived Situation Reports")
    
    auto_sync_table('municipal_reports', 'municipal_reports')
    auto_sync_table('main_reports', 'main_reports')
    
    reports = st.session_state.get('municipal_reports', [])
    main_reports = st.session_state.get('main_reports', [])
    
    if not reports and not main_reports:
        st.info("No archived reports found.")
        return
    
    if main_reports:
        st.markdown("#### 📄 Consolidated Reports")
        for report in sorted(main_reports, key=lambda x: x.get('created_at', ''), reverse=True):
            with st.expander(f"SITREP #{report.get('sitrep_number', 'N/A')}: {report.get('title', 'Untitled')}"):
                st.json(report)
    
    if reports:
        st.markdown("#### 🏘️ Municipal Reports")
        for report in sorted(reports, key=lambda x: x.get('created_at', ''), reverse=True)[:20]:
            with st.expander(f"{report.get('municipality', 'Unknown')} - SITREP #{report.get('sitrep_number')} ({report.get('report_date', 'Unknown')})"):
                st.json(report)


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Situation Report - Related Modules")
    st.caption("How Situation Report connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 DRRM Intelligence
        **Connection:** Situation reports feed into predictive analytics and risk assessment
        
        - **Risk Analysis:** Incident data validates hazard models
        - **Trend Analysis:** Historical reports identify patterns
        - **Vulnerability Assessment:** Affected populations highlight vulnerable areas
        
        ### 📋 Plan Management
        **Connection:** Incident data validates and updates DRRM plans
        
        - **Plan Validation:** Actual incidents test plan assumptions
        - **Resource Allocation:** Damage data informs budget priorities
        - **PPA Adjustment:** Response gaps identify needed programs
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Trainings
        **Connection:** Response effectiveness links to training needs assessment
        
        - **Capacity Gaps:** Response challenges identify training needs
        - **Skill Validation:** Actual response tests training effectiveness
        - **Certification Tracking:** Link trained responders to actual response
        
        ### 💰 LDRRMF Utilization
        **Connection:** Disaster impacts drive fund allocation and resource mobilization
        
        - **Emergency Funding:** Damage assessments trigger fund releases
        - **Resource Tracking:** Relief goods distribution tracked against needs
        - **Recovery Budget:** Rehabilitation needs inform budget planning
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links to Related Modules")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True, key="link_drrm"):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()
    with col2:
        if st.button("📋 Go to Plan Management", use_container_width=True, key="link_plan"):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col3:
        if st.button("📚 Go to Trainings", use_container_width=True, key="link_trainings"):
            st.session_state.navigation = "📚 TRAININGS"
            st.rerun()
    with col4:
        if st.button("💰 Go to LDRRMF", use_container_width=True, key="link_ldrrmf"):
            st.session_state.navigation = "💰 LDRRMF UTILIZATION"
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Current Data Summary")
    
    reports = st.session_state.get('municipal_reports', [])
    if reports:
        df = pd.DataFrame(reports)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Reports", len(df))
        with col2:
            st.metric("Municipalities", df['municipality'].nunique())
        with col3:
            active = len(df[df['alert_level'] != 'White']) if 'alert_level' in df.columns else 0
            st.metric("Active Alerts", active)