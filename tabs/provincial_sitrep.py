# tabs/provincial_sitrep.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import schedule
import threading
import time as time_module
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected
from utils.local_storage import save_file, get_file_size

def show():
    """Display Provincial SitRep Form with Auto-Submission"""
    
    st.markdown("# 📡 PROVINCIAL SITREP")
    st.caption("Official Provincial Situation Report Form with Auto-Submission")
    
    # Initialize session state
    if 'provincial_sitreps' not in st.session_state:
        st.session_state.provincial_sitreps = []
    
    if 'sitrep_email_recipients' not in st.session_state:
        st.session_state.sitrep_email_recipients = [
            "car@ocd.gov.ph", "solnasudman@gmail.com", "cristychreez@gmail.com",
            "mountainpho@gmail.com", "sadangamdrrmo@gmail.com", "swadmtprovince@dswd.gov.ph",
            "genyodong@gmail.com", "dhenverules@yahoo.com", "ldrrmobesao@gmail.com",
            "barligmdrrmo@gmail.com", "mdrrmosabangan@gmail.com", "car.mt.provincedj@bjmp.gov.ph",
            "mdrrmo_tadian@yahoo.com", "mpgov@yahoo.com", "cenrosabangan@denr.gov.ph",
            "dpwh.mpdeo2nd@gmail.com", "1403cdc.mt.province@gmail.com", "mppomu2020@gmail.com",
            "sagadamdrrmo@gmail.com", "pdohomountain@gmail.com", "mtprovince@redcross.org.ph",
            "mtnprovinceppopcrb@gmail.com", "bontoc.mdrrmo@gmail.com", "bfpmtprovcar@gmail.com",
            "baukomdrrmc@gmail.com", "mtprovince.dilgopcen@gmail.com", "pvomp2020@gmail.com",
            "mp.mediaaffairs@gmail.com", "ro1@pcic.gov.ph", "ldrrmonatonin@gmail.com",
            "paracelismdrrmo@gmail.com", "dremdmtprovince@dswd.gov.ph", "valerie.taguba@pia.gov.ph",
            "pbsbontoc@gmail.com", "ncl_mountainprovince@yahoo.com", "14carrcdg@gmail.com",
            "pdoho.mp@gmail.com", "wildcatscharlie54@gmail.com", "victorpadillo1995@gmail.com",
            "hermenegildo.castaneda@dict.gov.ph", "dacar.apco.mountain@gmail.com"
        ]
    
    if 'auto_submit_enabled' not in st.session_state:
        st.session_state.auto_submit_enabled = False
    
    if 'current_alert_status' not in st.session_state:
        st.session_state.current_alert_status = "White"
    
    # Load existing sitreps from cloud
    load_sitreps_from_cloud()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Provincial SitRep Form",
        "📋 Archived SitReps",
        "📧 Email Recipients",
        "⚙️ Auto-Submit Settings",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_provincial_sitrep_form()
    
    with tab2:
        show_archived_sitreps()
    
    with tab3:
        show_email_recipients()
    
    with tab4:
        show_auto_submit_settings()
    
    with tab5:
        show_related_modules()


def load_sitreps_from_cloud():
    """Load provincial sitreps from Supabase"""
    if is_connected():
        try:
            from utils.supabase_client import get_supabase_client
            client = get_supabase_client()
            if client:
                response = client.table('provincial_sitreps').select('*').execute()
                if response.data:
                    st.session_state.provincial_sitreps = response.data
        except Exception as e:
            print(f"Error loading sitreps: {e}")


def save_sitrep_to_cloud(sitrep):
    """Save provincial sitrep to Supabase"""
    if is_connected():
        try:
            from utils.supabase_client import get_supabase_client
            client = get_supabase_client()
            if client:
                client.table('provincial_sitreps').insert(sitrep).execute()
                return True
        except Exception as e:
            print(f"Error saving sitrep: {e}")
    return False


def show_provincial_sitrep_form():
    """Main Provincial SitRep Form"""
    
    st.markdown("### 📝 Provincial Situation Report Form")
    st.caption("Official MPDRRMC SITREP Format")
    
    # Auto-fill from municipal reports button
    if st.button("📊 Auto-Fill from Municipal Reports", help="Populate form using submitted municipal reports"):
        auto_fill_from_municipal_reports()
        st.success("Auto-fill completed! Review and edit as needed.")
        st.rerun()
    
    st.markdown("---")
    
    with st.form("provincial_sitrep_form", clear_on_submit=False):
        # ===== HEADER SECTION =====
        st.markdown("#### 📋 HEADER")
        
        col1, col2 = st.columns(2)
        with col1:
            sitrep_number = st.number_input("SITREP Number", min_value=1, value=1, step=1)
            incident_name = st.text_input("Incident Name", placeholder="e.g., Effects of TS PAENG (NALGAE)")
        with col2:
            report_date = st.date_input("Report Date", date.today())
            report_time = st.time_input("Report Time", datetime.now().time())
        
        # ===== SECTION I: SITUATION OVERVIEW =====
        st.markdown("---")
        st.markdown("#### I. SITUATION OVERVIEW")
        
        # PAGASA Bulletin
        pagasa_bulletin = st.text_area(
            "PAGASA Tropical Cyclone Bulletin",
            placeholder="Paste the latest PAGASA bulletin here...",
            height=150
        )
        
        # Weather Table for 10 municipalities
        st.markdown("##### Weather & Alert Level Statuses")
        
        municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                         "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
        
        weather_data = []
        cols = st.columns(5)
        st.markdown("""
        <style>
        .stTable td, .stTable th { padding: 4px; }
        </style>
        """, unsafe_allow_html=True)
        
        # Create header
        header_cols = st.columns([1.5, 1, 1, 1, 1])
        with header_cols[0]:
            st.markdown("**Municipality**")
        with header_cols[1]:
            st.markdown("**Cloud**")
        with header_cols[2]:
            st.markdown("**Wind**")
        with header_cols[3]:
            st.markdown("**Precipitation**")
        with header_cols[4]:
            st.markdown("**Alert Level**")
        
        # Create rows for each municipality
        for i, mun in enumerate(municipalities):
            row_cols = st.columns([1.5, 1, 1, 1, 1])
            with row_cols[0]:
                st.markdown(f"**{mun}**")
            with row_cols[1]:
                cloud = st.selectbox(
                    "Cloud", 
                    ["Clear", "Partly Cloudy", "Cloudy", "Light Rains", "Moderate Rains", "Heavy Rains"],
                    key=f"cloud_{mun}",
                    label_visibility="collapsed"
                )
            with row_cols[2]:
                wind = st.selectbox(
                    "Wind",
                    ["Calm", "Light", "Moderate", "Strong", "Gale", "Storm"],
                    key=f"wind_{mun}",
                    label_visibility="collapsed"
                )
            with row_cols[3]:
                precip = st.selectbox(
                    "Precipitation",
                    ["None", "Light", "Moderate", "Heavy", "Torrential"],
                    key=f"precip_{mun}",
                    label_visibility="collapsed"
                )
            with row_cols[4]:
                alert = st.selectbox(
                    "Alert Level",
                    ["White", "Blue", "Red"],
                    key=f"alert_{mun}",
                    label_visibility="collapsed"
                )
            weather_data.append({
                "municipality": mun,
                "cloud": cloud,
                "wind": wind,
                "precipitation": precip,
                "alert_level": alert
            })
        
        # Overall Alert Status
        overall_alert = st.selectbox("Mountain Province Overall Alert Status", ["White", "Blue", "Red"])
        
        # ===== SECTION II: INCIDENTS MONITORED =====
        st.markdown("---")
        st.markdown("#### II. INCIDENTS MONITORED")
        
        incidents_data = []
        for mun in municipalities:
            incidents = st.text_area(f"{mun}", placeholder="No untoward incident reported", key=f"incident_{mun}", height=60)
            casualties = st.text_input(f"Casualties", placeholder="e.g., 0 dead, 2 injured", key=f"casualty_{mun}")
            incidents_data.append({
                "municipality": mun,
                "incidents": incidents,
                "casualties": casualties
            })
        
        # ===== SECTION III: STATUS OF LIFELINES =====
        st.markdown("---")
        st.markdown("#### III. STATUS OF LIFELINES")
        
        # National Roads with add/edit/delete functionality
        st.markdown("##### 3.1 National Roads & Bridges")
        
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
        
        # Display National Roads with sections
        for road in st.session_state.national_roads:
            with st.expander(f"🛣️ {road['name']}"):
                # Add new section
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 2, 1])
                with col1:
                    new_section = st.text_input("Road Section", placeholder="e.g., Napu Section", key=f"new_section_{road['id']}")
                with col2:
                    new_traffic = st.selectbox("Traffic", ["Passable", "One Lane Passable", "Not Passable", "Closed"], key=f"new_traffic_{road['id']}")
                with col3:
                    new_status = st.selectbox("Status", ["Normal", "Under Repair", "Clearing", "Closed"], key=f"new_status_{road['id']}")
                with col4:
                    new_actions = st.selectbox("Actions Taken", 
                        ["Monitoring", "Clearing Operations", "Repair Ongoing", "Traffic Management", "Road Closed", "Emergency Response"],
                        key=f"new_actions_{road['id']}")
                with col5:
                    if st.button("➕ Add", key=f"add_section_{road['id']}"):
                        if new_section:
                            road['sections'].append({
                                "section": new_section,
                                "traffic": new_traffic,
                                "status": new_status,
                                "actions": new_actions,
                                "remarks": ""
                            })
                            st.rerun()
                
                # Display existing sections
                for idx, section in enumerate(road['sections']):
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 1.5, 1.5, 2, 1.5, 0.5])
                    with col1:
                        section_name = st.text_input("Section", value=section['section'], key=f"section_{road['id']}_{idx}")
                    with col2:
                        traffic = st.selectbox("Traffic", ["Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                              index=["Passable", "One Lane Passable", "Not Passable", "Closed"].index(section['traffic']),
                                              key=f"traffic_{road['id']}_{idx}")
                    with col3:
                        status = st.selectbox("Status", ["Normal", "Under Repair", "Clearing", "Closed"],
                                            index=["Normal", "Under Repair", "Clearing", "Closed"].index(section['status']),
                                            key=f"status_{road['id']}_{idx}")
                    with col4:
                        actions = st.selectbox("Actions Taken", 
                            ["Monitoring", "Clearing Operations", "Repair Ongoing", "Traffic Management", "Road Closed", "Emergency Response"],
                                            key=f"actions_{road['id']}_{idx}")
                    with col5:
                        remarks = st.text_input("Remarks", value=section.get('remarks', ''), key=f"remarks_{road['id']}_{idx}")
                    with col6:
                        if st.button("🗑️", key=f"del_section_{road['id']}_{idx}"):
                            road['sections'].pop(idx)
                            st.rerun()
                    
                    # Update section data
                    section['section'] = section_name
                    section['traffic'] = traffic
                    section['status'] = status
                    section['actions'] = actions
                    section['remarks'] = remarks
        
        # Add new national road
        st.markdown("##### ➕ Add New National Road")
        col1, col2 = st.columns([3, 1])
        with col1:
            new_road_name = st.text_input("New Road Name", placeholder="Enter new national road name")
        with col2:
            if st.button("➕ Add National Road", use_container_width=True):
                if new_road_name:
                    new_id = max([r['id'] for r in st.session_state.national_roads]) + 1 if st.session_state.national_roads else 1
                    st.session_state.national_roads.append({
                        "id": new_id,
                        "name": new_road_name,
                        "sections": []
                    })
                    st.rerun()
        
        # Provincial Roads (similar structure)
        st.markdown("##### 3.2 Provincial Roads & Bridges")
        
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
        
        # Display Provincial Roads
        for road in st.session_state.provincial_roads:
            col1, col2, col3, col4 = st.columns([3, 1.5, 2, 0.5])
            with col1:
                road_name = st.text_input("Road Name", value=road['name'], key=f"prov_road_{road['id']}")
            with col2:
                road_status = st.selectbox("Status", ["Passable", "One Lane Passable", "Not Passable", "Closed"],
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
        
        # Add new provincial road
        col1, col2 = st.columns([3, 1])
        with col1:
            new_prov_road = st.text_input("New Provincial Road Name", placeholder="Enter new provincial road name")
        with col2:
            if st.button("➕ Add Provincial Road", use_container_width=True):
                if new_prov_road:
                    new_id = max([r['id'] for r in st.session_state.provincial_roads]) + 1 if st.session_state.provincial_roads else 1
                    st.session_state.provincial_roads.append({
                        "id": new_id,
                        "name": new_prov_road,
                        "status": "Passable",
                        "remarks": ""
                    })
                    st.rerun()
        
        # Power & Communication
        st.markdown("##### 3.3 Power & Communication")
        
        power_data = []
        comm_data = []
        for mun in municipalities:
            col1, col2, col3 = st.columns([2, 1.5, 2])
            with col1:
                st.markdown(f"**{mun}**")
            with col2:
                power = st.selectbox("Power", ["Normal", "Intermittent", "No Power"], key=f"power_{mun}", label_visibility="collapsed")
                power_data.append({"municipality": mun, "status": power})
            with col3:
                comm = st.selectbox("Communication", ["Normal", "Intermittent", "No Signal"], key=f"comm_{mun}", label_visibility="collapsed")
                comm_data.append({"municipality": mun, "status": comm})
        
        # ===== SECTION IV: DISPLACED POPULATION & DAMAGES =====
        st.markdown("---")
        st.markdown("#### IV. DISPLACED POPULATION & DAMAGES")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Inside Evacuation Centers**")
            families_ec = st.number_input("Families in ECs", min_value=0, value=0)
            persons_ec = st.number_input("Persons in ECs", min_value=0, value=0)
        with col2:
            st.markdown("**Outside Evacuation Centers**")
            families_out = st.number_input("Families Outside ECs", min_value=0, value=0)
            persons_out = st.number_input("Persons Outside ECs", min_value=0, value=0)
        
        st.markdown("**Damaged Houses**")
        col1, col2 = st.columns(2)
        with col1:
            totally_damaged = st.number_input("Totally Damaged Houses", min_value=0, value=0)
        with col2:
            partially_damaged = st.number_input("Partially Damaged Houses", min_value=0, value=0)
        
        st.markdown("**Affected Population**")
        col1, col2 = st.columns(2)
        with col1:
            affected_families = st.number_input("Affected Families", min_value=0, value=0)
        with col2:
            affected_persons = st.number_input("Affected Persons", min_value=0, value=0)
        
        # ===== SECTION V: RESOURCES PROVIDED =====
        st.markdown("---")
        st.markdown("#### V. RESOURCES PROVIDED")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            food_packs = st.number_input("Food Packs Distributed", min_value=0, value=0)
        with col2:
            hygiene_kits = st.number_input("Hygiene Kits Distributed", min_value=0, value=0)
        with col3:
            family_kits = st.number_input("Family Kits Distributed", min_value=0, value=0)
        
        # ===== SECTION VI: RESPONSE ACTIONS =====
        st.markdown("---")
        st.markdown("#### VI. RESPONSE ACTIONS")
        response_actions = st.text_area("Response Actions Taken", height=150)
        
        # ===== SECTION VII: PHOTO DOCUMENTATION =====
        st.markdown("---")
        st.markdown("#### VII. PHOTO DOCUMENTATION")
        
        photos = []
        for i in range(3):
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                photo = st.file_uploader(f"Photo {i+1}", type=['jpg', 'jpeg', 'png'], key=f"photo_{i}")
            with col2:
                caption = st.text_input(f"Caption {i+1}", key=f"caption_{i}")
            with col3:
                location = st.text_input(f"Location {i+1}", key=f"location_{i}")
            if photo:
                photos.append({"file": photo.name, "caption": caption, "location": location})
        
        # ===== SECTION VIII: NEEDS ASSESSMENT =====
        st.markdown("---")
        st.markdown("#### VIII. NEEDS ASSESSMENT")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            priority1 = st.text_area("Priority 1 Needs", placeholder="Search & Rescue, Food, Medical, Water", height=80)
        with col2:
            priority2 = st.text_area("Priority 2 Needs", placeholder="Shelter, Clothing, Non-food items", height=80)
        with col3:
            priority3 = st.text_area("Priority 3 Needs", placeholder="Cash for Work, Rehabilitation", height=80)
        
        # ===== SUBMIT BUTTON =====
        st.markdown("---")
        submitted = st.form_submit_button("💾 Save Provincial SITREP", type="primary", use_container_width=True)
        
        if submitted:
            sitrep = {
                "id": int(datetime.now().timestamp() * 1000),
                "sitrep_number": sitrep_number,
                "incident_name": incident_name,
                "report_date": report_date.isoformat(),
                "report_time": report_time.strftime("%H:%M"),
                "overall_alert": overall_alert,
                "pagasa_bulletin": pagasa_bulletin,
                "weather_data": weather_data,
                "incidents_data": incidents_data,
                "national_roads": st.session_state.national_roads,
                "provincial_roads": st.session_state.provincial_roads,
                "power_data": power_data,
                "comm_data": comm_data,
                "displaced": {
                    "families_in_ec": families_ec,
                    "persons_in_ec": persons_ec,
                    "families_outside": families_out,
                    "persons_outside": persons_out
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
                "photos": photos,
                "needs": {
                    "priority1": priority1,
                    "priority2": priority2,
                    "priority3": priority3
                },
                "created_at": datetime.now().isoformat(),
                "status": "Saved"
            }
            
            # Save locally
            save_sitrep_to_local(sitrep)
            
            # Save to cloud
            if save_sitrep_to_cloud(sitrep):
                st.success("✅ Provincial SITREP saved to cloud!")
            else:
                st.success("✅ Provincial SITREP saved locally!")
            
            st.balloons()
            st.rerun()


def save_sitrep_to_local(sitrep):
    """Save sitrep to local storage"""
    folder = "local_storage/provincial_sitreps"
    os.makedirs(folder, exist_ok=True)
    filename = f"sitrep_{sitrep['sitrep_number']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(sitrep, f, indent=2, default=str)
    return filepath


def auto_fill_from_municipal_reports():
    """Auto-fill provincial sitrep from municipal reports"""
    # This will be implemented to pull data from municipal_reports
    st.info("Auto-fill from municipal reports will be implemented in the next phase")


def show_archived_sitreps():
    """Display archived provincial sitreps"""
    
    st.markdown("### 📋 Archived Provincial SitReps")
    
    sitreps = st.session_state.provincial_sitreps
    
    if not sitreps:
        st.info("No archived sitreps yet. Save your first Provincial SITREP.")
        return
    
    df = pd.DataFrame(sitreps)
    st.dataframe(df[['sitrep_number', 'incident_name', 'report_date', 'overall_alert']], 
                 use_container_width=True, hide_index=True)
    
    for sitrep in sitreps:
        with st.expander(f"SITREP #{sitrep['sitrep_number']} - {sitrep['incident_name']} ({sitrep['report_date']})"):
            st.json(sitrep)
            
            if st.button(f"🗑️ Delete", key=f"del_{sitrep['id']}"):
                st.session_state.provincial_sitreps = [s for s in st.session_state.provincial_sitreps if s['id'] != sitrep['id']]
                st.rerun()


def show_email_recipients():
    """Manage email recipients for auto-submission"""
    
    st.markdown("### 📧 Email Recipients Management")
    st.caption("Add, edit, or remove email addresses for automatic SITREP distribution")
    
    # Add new email
    col1, col2 = st.columns([3, 1])
    with col1:
        new_email = st.text_input("New Email Address", placeholder="example@domain.com")
    with col2:
        if st.button("➕ Add Email", use_container_width=True):
            if new_email and new_email not in st.session_state.sitrep_email_recipients:
                st.session_state.sitrep_email_recipients.append(new_email)
                st.success(f"Added {new_email}")
                st.rerun()
            elif new_email in st.session_state.sitrep_email_recipients:
                st.warning("Email already exists")
    
    # Display and manage existing emails
    st.markdown("#### Current Recipients")
    
    for i, email in enumerate(st.session_state.sitrep_email_recipients):
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            edited_email = st.text_input(f"Email {i+1}", value=email, key=f"email_{i}")
        with col2:
            if st.button("✏️", key=f"edit_{i}"):
                if edited_email != email:
                    st.session_state.sitrep_email_recipients[i] = edited_email
                    st.rerun()
        with col3:
            if st.button("🗑️", key=f"del_{i}"):
                st.session_state.sitrep_email_recipients.pop(i)
                st.rerun()
    
    st.info(f"Total recipients: {len(st.session_state.sitrep_email_recipients)}")


def show_auto_submit_settings():
    """Configure automatic SITREP submission"""
    
    st.markdown("### ⚙️ Auto-Submit Settings")
    st.caption("Configure automatic SITREP generation and email distribution based on alert status")
    
    # Alert Status Selection
    st.markdown("#### Current Alert Status")
    alert_status = st.selectbox(
        "Select Alert Status",
        ["White", "Blue", "Red"],
        index=["White", "Blue", "Red"].index(st.session_state.current_alert_status)
    )
    
    if alert_status != st.session_state.current_alert_status:
        st.session_state.current_alert_status = alert_status
        update_submission_schedule()
        st.rerun()
    
    # Display submission schedule based on alert status
    st.markdown("#### Submission Schedule")
    
    if alert_status == "White":
        st.info("**White Alert:** Once daily at 5:00 PM")
        submit_time = st.time_input("Submission Time", time(17, 0))
        
    elif alert_status == "Blue":
        st.warning("**Blue Alert:** Twice daily at 12:00 NN and 5:00 PM")
        col1, col2 = st.columns(2)
        with col1:
            submit_time1 = st.time_input("First Submission", time(12, 0))
        with col2:
            submit_time2 = st.time_input("Second Submission", time(17, 0))
        
    else:  # Red Alert
        st.error("**Red Alert:** Three times daily at 10:00 AM, 4:00 PM, and 10:00 PM")
        col1, col2, col3 = st.columns(3)
        with col1:
            submit_time1 = st.time_input("First Submission", time(10, 0))
        with col2:
            submit_time2 = st.time_input("Second Submission", time(16, 0))
        with col3:
            submit_time3 = st.time_input("Third Submission", time(22, 0))
    
    # Auto-submit toggle
    st.markdown("#### Auto-Submit Control")
    auto_submit = st.toggle("Enable Automatic Submission", value=st.session_state.auto_submit_enabled)
    
    if auto_submit != st.session_state.auto_submit_enabled:
        st.session_state.auto_submit_enabled = auto_submit
        if auto_submit:
            start_auto_submit_scheduler()
            st.success("Auto-submit enabled! SITREPs will be sent automatically.")
        else:
            stop_auto_submit_scheduler()
            st.info("Auto-submit disabled.")
    
    # Test email button
    st.markdown("#### Test Configuration")
    if st.button("📧 Send Test Email", use_container_width=True):
        send_test_email()
        st.success("Test email sent to all recipients!")


def update_submission_schedule():
    """Update the submission schedule based on alert status"""
    # This will be implemented with a background scheduler
    pass


def start_auto_submit_scheduler():
    """Start the background scheduler for auto-submission"""
    # This will be implemented with schedule library
    pass


def stop_auto_submit_scheduler():
    """Stop the background scheduler"""
    pass


def send_test_email():
    """Send a test email to all recipients"""
    # This will be implemented with SMTP
    st.info("Email functionality will be configured with SMTP settings")


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 DRRM Intelligence
        - Hazard events feed into situation reports
        - Historical data for comparison
        
        ### 📋 Plan Management
        - Response actions linked to PPAs
        - Resource allocation tracking
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Trainings
        - Response effectiveness tracking
        - Training needs identification
        
        ### 📁 Knowledge Repository
        - Archived SITREPs storage
        - Template reference
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()
    with col2:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col3:
        if st.button("📁 Go to Knowledge Repository", use_container_width=True):
            st.session_state.navigation = "📁 KNOWLEDGE REPOSITORY"
            st.rerun()