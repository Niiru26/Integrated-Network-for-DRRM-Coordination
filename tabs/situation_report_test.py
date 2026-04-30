# tabs/situation_report.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import json
import plotly.express as px
import plotly.graph_objects as go
def format_currency(amount):
    """Format amount as currency with comma separators and 2 decimal places"""
    return f"₱{amount:,.2f}"
from utils.supabase_client import is_connected

# Define municipalities list at module level
municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                  "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]

# ===== GLOBAL CSS FOR SCROLL BEHAVIOR =====
st.markdown("""
<style>
    /* Prevent automatic scrolling to top */
    .stApp [data-testid="stVerticalBlock"] {
        scroll-behavior: smooth;
    }
    .stApp {
        scroll-behavior: smooth;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CLOUD SYNC FUNCTIONS
# ============================================================

def load_sitreps_from_cloud():
    """Load provincial sitreps from Supabase"""
    if is_connected():
        try:
            from utils.supabase_client import get_supabase_client
            client = get_supabase_client()
            if client:
                response = client.table("provincial_sitreps").select("*").order("created_at", desc=True).execute()
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
                client.table("provincial_sitreps").insert(sitrep).execute()
                return True
        except Exception as e:
            print(f"Error saving sitrep: {e}")
    return False


def save_sitrep_to_local(sitrep):
    """Save sitrep to local storage"""
    folder = "local_storage/provincial_sitreps"
    os.makedirs(folder, exist_ok=True)
    filename = f"sitrep_{sitrep.get('sitrep_number', '0')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(folder, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sitrep, f, indent=2, default=str)
    return filepath


def send_test_email():
    """Send a test email to all recipients"""
    st.info("Email functionality will be configured with SMTP settings.")


# ============================================================
# TAB FUNCTIONS
# ============================================================

def show_archived_sitreps():
    """Display archived provincial sitreps"""
    st.markdown("### 📋 Archived Situation Reports")
    sitreps = st.session_state.get("provincial_sitreps", [])
    if not sitreps:
        st.info("No archived sitreps yet. Save your first Situation Report.")
        return
    for sitrep in sitreps:
        with st.expander(f"SITREP #{sitrep.get('sitrep_number', 'N/A')} - {sitrep.get('incident_name', 'Untitled')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Date:** {sitrep.get('report_date', 'N/A')}")
                st.markdown(f"**Time:** {sitrep.get('report_time', 'N/A')}")
            with col2:
                st.markdown(f"**Alert Status:** {sitrep.get('overall_alert', 'N/A')}")
                st.markdown(f"**CPA Level:** {sitrep.get('pdr_cpa_level', 'N/A')}")
            if st.button(f"Delete", key=f"del_{sitrep.get('id')}"):
                st.session_state.provincial_sitreps = [s for s in st.session_state.provincial_sitreps if s.get('id') != sitrep.get('id')]
                st.rerun()


def show_email_recipients():
    """Manage email recipients"""
    st.markdown("### 📧 Email Recipients Management")
    if "sitrep_email_recipients" not in st.session_state:
        st.session_state.sitrep_email_recipients = []
    col1, col2 = st.columns([3, 1])
    with col1:
        new_email = st.text_input("New Email Address", placeholder="example@domain.com")
    with col2:
        if st.button("Add Email", use_container_width=True):
            if new_email and new_email not in st.session_state.sitrep_email_recipients:
                st.session_state.sitrep_email_recipients.append(new_email)
                st.rerun()
    for i, email in enumerate(st.session_state.sitrep_email_recipients):
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            edited_email = st.text_input(f"Email {i+1}", value=email, key=f"email_{i}")
        with col2:
            if st.button("Edit", key=f"edit_{i}"):
                if edited_email != email:
                    st.session_state.sitrep_email_recipients[i] = edited_email
                    st.rerun()
        with col3:
            if st.button("Delete", key=f"del_{i}"):
                st.session_state.sitrep_email_recipients.pop(i)
                st.rerun()
    st.info(f"Total recipients: {len(st.session_state.sitrep_email_recipients)}")


def show_auto_submit_settings():
    """Configure automatic SITREP submission"""
    st.markdown("### ⚙️ Auto-Submit Settings")
    if "auto_submit_enabled" not in st.session_state:
        st.session_state.auto_submit_enabled = False
    if "current_alert_status" not in st.session_state:
        st.session_state.current_alert_status = "White"
    alert_status = st.selectbox("Select Alert Status", ["White", "Blue", "Red"])
    if alert_status != st.session_state.current_alert_status:
        st.session_state.current_alert_status = alert_status
    if alert_status == "White":
        st.info("White Alert: Once daily at 5:00 PM")
    elif alert_status == "Blue":
        st.warning("Blue Alert: Twice daily at 12:00 NN and 5:00 PM")
    else:
        st.error("Red Alert: Three times daily at 10:00 AM, 4:00 PM, and 10:00 PM")
    auto_submit = st.toggle("Enable Automatic Submission", value=st.session_state.auto_submit_enabled)
    st.session_state.auto_submit_enabled = auto_submit
    if st.button("Send Test Email", use_container_width=True):
        send_test_email()


def show_related_modules():
    """Show connections to other modules"""
    st.markdown("### 🔗 Related Modules")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📊 DRRM Intelligence
        - Hazard events feed into situation reports
        ### 📋 Plan Management
        - Response actions linked to PPAs
        """)
    with col2:
        st.markdown("""
        ### 📚 Trainings
        - Response effectiveness tracking
        ### 📁 Knowledge Repository
        - Archived SITREPs storage
        """)


def show_predictive_analysis():
    """Show predictive analysis based on historical SITREP data"""
    st.markdown("### 📊 Predictive Analysis")
    sitreps = st.session_state.get("provincial_sitreps", [])
    if len(sitreps) < 2:
        st.info("Need at least 2 SITREPs to generate predictive analysis")
        return
    st.info("Predictive analysis will be displayed here based on historical data.")


# ============================================================
# COMPLETE BARANGAY VULNERABILITY TABLE
# ============================================================

def get_barangay_vulnerability_data():
    """Return complete barangay vulnerability data for reference"""
    return {
        "Barlig": {
            "barangays": ["Chupac", "Fiangtin", "Gawana", "Kaleo", "Latang", "Lias Kanluran", "Lias Silangan", "Lingoy", "Lunas", "Macalana", "Ogo-og"],
            "landslide_risk": {"Chupac": "HL", "Fiangtin": "VHL", "Gawana": "VHL", "Kaleo": "VHL", "Latang": "VHL", "Lias Kanluran": "HL", "Lias Silangan": "HL", "Lingoy": "VHL", "Lunas": "HL", "Macalana": "VHL", "Ogo-og": "VHL"},
            "flood_risk": {}
        },
        "Bauko": {
            "barangays": ["Bagnen Oriente", "Bagnen Proper", "Balintaugan", "Banao", "Bila", "Guinzadan Central", "Guinzadan Norte", "Guinzadan Sur", "Lagawa", "Leseb", "Mabaay", "Mayag", "Monamon Norte", "Monamon Sur", "Mount Data", "Otucan Norte", "Otucan Sur", "Poblacion", "Sadsadan", "Sinto", "Tapapan"],
            "landslide_risk": {"Bagnen Oriente": "VHL", "Balintaugan": "VHL", "Bila": "VHL", "Guinzadan Norte": "VHL", "Leseb": "VHL", "Mabaay": "VHL", "Otucan Norte": "VHL", "Otucan Sur": "VHL", "Sadsadan": "VHL", "Tapapan": "VHL"},
            "flood_risk": {"Guinzadan Norte": "HF", "Lagawa": "HF", "Leseb": "HF", "Mabaay": "HF", "Monamon Norte": "HF", "Monamon Sur": "HF", "Otucan Sur": "HF", "Sadsadan": "HF", "Tapapan": "HF"}
        },
        "Besao": {
            "barangays": ["Agawa", "Besao East", "Gueday", "Lacmaan", "Suquib"],
            "landslide_risk": {"Agawa": "VHL", "Gueday": "VHL", "Suquib": "VHL"},
            "flood_risk": {}
        },
        "Bontoc": {
            "barangays": ["Alab Oriente", "Alab Proper", "Balili", "Bayyo", "Bontoc Ili", "Caluttit", "Caneo", "Dalican", "Gonogon", "Guina-ang", "Mainit", "Maligcong", "Poblacion", "Samoki", "Talubin", "Tocucan"],
            "landslide_risk": {"Balili": "HL", "Gonogon": "HL", "Talubin": "HL"},
            "flood_risk": {"Balili": "HF", "Gonogon": "HF", "Talubin": "HF"}
        },
        "Natonin": {
            "barangays": ["Alunogan", "Balangao", "Banao", "Banawel", "Butac", "Maducayan", "Poblacion", "Pudo", "Saliok", "Santa Isabel", "Tonglayan"],
            "landslide_risk": {"Balangao": "HL", "Banawel": "HL", "Poblacion": "HL", "Saliok": "HL"},
            "flood_risk": {"Balangao": "HF", "Banawel": "HF", "Poblacion": "HF", "Saliok": "HF"}
        },
        "Paracelis": {
            "barangays": ["Anonat", "Bacarri", "Bananao", "Bantay", "Bunot", "Buringal", "Butigue", "Palitod", "Poblacion"],
            "landslide_risk": {"Anonat": "HL", "Bacarri": "HL", "Bananao": "HL", "Bantay": "HL", "Bunot": "HL", "Buringal": "HL", "Butigue": "HL", "Palitod": "HL"},
            "flood_risk": {"Anonat": "VHF", "Bacarri": "VHF", "Bantay": "VHF", "Buringal": "VHF", "Butigue": "HF", "Palitod": "HF"}
        },
        "Sabangan": {
            "barangays": ["Napua", "Pingad", "Poblacion", "Supang", "Tambingan", "Bao-Angan", "Bun-Ayan", "Busa", "Camatagan", "Capinitan", "Data", "Gayang", "Lagan", "Losad", "Namatec"],
            "landslide_risk": {"Supang": "VHL", "Data": "VHL"},
            "flood_risk": {"Napua": "HF", "Pingad": "HF", "Poblacion": "HF", "Supang": "HF", "Tambingan": "HF", "Bao-Angan": "HF", "Bun-Ayan": "HF", "Busa": "HF", "Camatagan": "HF", "Capinitan": "HF", "Data": "HF", "Gayang": "HF", "Lagan": "HF", "Losad": "HF", "Namatec": "HF"}
        },
        "Sadanga": {
            "barangays": ["Anabel", "Bekigan", "Belwang", "Betwagan", "Demang", "Poblacion", "Sacasacan", "Saclit"],
            "landslide_risk": {},
            "flood_risk": {}
        },
        "Sagada": {
            "barangays": ["Ambasing", "Angkeling", "Antadao", "Balugan", "Bangaan", "Dagdag", "Demang", "Fidelisan", "Kilong", "Madongo", "Nacagang", "Poblacion", "Suyo", "Taccong", "Tanulong", "Tetep-an Norte", "Tetep-an Sur"],
            "landslide_risk": {"Ambasing": "VHL", "Angkeling": "VHL", "Antadao": "VHL", "Balugan": "VHL", "Bangaan": "VHL", "Dagdag": "VHL", "Demang": "VHL", "Kilong": "VHL", "Madongo": "VHL", "Nacagang": "VHL", "Poblacion": "VHL", "Suyo": "VHL", "Taccong": "VHL", "Tanulong": "VHL", "Tetep-an Sur": "VHL"},
            "flood_risk": {}
        },
        "Tadian": {
            "barangays": ["Bana-ao", "Cadad-anan", "Cagubatan", "Dacudac", "Lenga", "Pandayan"],
            "landslide_risk": {"Cadad-anan": "VHL", "Cagubatan": "VHL", "Dacudac": "VHL", "Lenga": "VHL", "Pandayan": "VHL"},
            "flood_risk": {"Cadad-anan": "HF", "Dacudac": "HF", "Lenga": "HF"}
        }
    }


# ============================================================
# PDR ASSESSMENT (PDRA) FUNCTION - FULL INTERACTIVE TOOL
# ============================================================

def show_pdr_assessment():
    """PDR Assessment (PDRA) Tool - Separate tab for Operation L!sto framework"""
    
    st.markdown("### 📋 Pre-Disaster Risk Assessment (PDRA)")
    st.caption("Based on DILG CODIX advisories, PAGASA forecasts, and the Operation L!sto framework")
    
    # Initialize session state variables for PDRA
    if "pdra_conducted_date" not in st.session_state:
        st.session_state.pdra_conducted_date = date.today()
    if "pdra_conducted_time" not in st.session_state:
        st.session_state.pdra_conducted_time = datetime.now().time()
    if "pdra_cpa_level" not in st.session_state:
        st.session_state.pdra_cpa_level = ""
    if "pdra_actions_list" not in st.session_state:
        st.session_state.pdra_actions_list = []
    if "pdra_imminent_declared" not in st.session_state:
        st.session_state.pdra_imminent_declared = False
    if "pdra_confirmed" not in st.session_state:
        st.session_state.pdra_confirmed = False
    if "pdra_optional_notes" not in st.session_state:
        st.session_state.pdra_optional_notes = ""
    
    # PDRA Conducted Date and Time
    col1, col2 = st.columns(2)
    with col1:
        conducted_date = st.date_input(
            "PDRA Conducted Date",
            value=st.session_state.pdra_conducted_date,
            key="pdra_date_input"
        )
        st.session_state.pdra_conducted_date = conducted_date
    with col2:
        conducted_time = st.time_input(
            "PDRA Conducted Time",
            value=st.session_state.pdra_conducted_time,
            key="pdra_time_input"
        )
        st.session_state.pdra_conducted_time = conducted_time
    
    st.markdown("---")
    
    # Get the selected hazard types from session state
    selected_hazard_types = st.session_state.get("selected_hazard_types", [])
    
    # Define weather-related hazards
    weather_hazards = [
        "Tropical Depression", "Tropical Storm", "Severe Tropical Storm", 
        "Typhoon", "Super Typhoon", "Southwest Monsoon (Habagat)", 
        "Northeast Monsoon (Amihan)", "Low Pressure Area (LPA)", 
        "Shear Line", "Intertropical Convergence Zone (ITCZ)", 
        "Thunderstorm", "Flood/Flashflood", "Landslide"
    ]
    
    # Check if any selected hazard is weather-related
    is_weather_hazard = any(h in weather_hazards for h in selected_hazard_types)
    
    if is_weather_hazard:
        # ===== FULL OPERATION L!STO PDRA FOR WEATHER HAZARDS =====
        st.success(f"✅ Weather hazard detected. Full PDRA tool is available.")
        
        st.markdown("**Critical Preparedness Action (CPA) Level**")
        st.caption("Based on DILG CODIX advisory from PAGASA forecast")
        
        # Determine current index for radio button
        current_cpa = st.session_state.pdra_cpa_level
        if current_cpa == "Alpha (Yellow)":
            cpa_index = 0
        elif current_cpa == "Bravo (Orange)":
            cpa_index = 1
        elif current_cpa == "Charlie (Red)":
            cpa_index = 2
        else:
            cpa_index = 0
        
        # Radio buttons for CPA selection
        selected_cpa = st.radio(
            "Select CPA Level",
            ["Alpha (Yellow)", "Bravo (Orange)", "Charlie (Red)"],
            index=cpa_index,
            key="pdra_cpa_radio",
            help="Select the CPA level based on DILG CODIX advisory"
        )
        
        # Confirm button to prevent scrolling
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("✅ Confirm Selection", key="confirm_pdra"):
                st.session_state.pdra_cpa_level = selected_cpa
                st.session_state.pdra_confirmed = True
                st.session_state.pdra_conducted_date = conducted_date
                st.session_state.pdra_conducted_time = conducted_time
                
                # Set default actions based on CPA level
                if selected_cpa == "Alpha (Yellow)":
                    default_actions = [
                        "Convene the Local DRRM Council (LDRRMC)",
                        "Issue directives to relevant local offices",
                        "Prepare administrative and logistical support (budgets, cash advances)",
                        "Activate the Emergency Operations Center (EOC) on standby",
                        "Check inventory of resources and supplies",
                        "Monitor alerts and advisories from PAGASA and DILG CODIX",
                        "Coordinate with province and neighboring LGUs",
                        "SITREP reporting as needed"
                    ]
                elif selected_cpa == "Bravo (Orange)":
                    default_actions = [
                        "Activate the Incident Command System (ICS)",
                        "Check inventory of relief goods and supplies",
                        "Put Search, Rescue, and Retrieval (SRR) teams on standby",
                        "Issue advisory for discretionary/pre-emptive evacuation if needed",
                        "Pre-position response teams and equipment",
                        "Activate designated evacuation centers",
                        "Intensified dissemination of warnings and advisories (every 6 hours)",
                        "SITREP reporting every 12 hours"
                    ]
                else:  # Charlie (Red)
                    default_actions = [
                        "Implement forced/mandatory evacuation in high-risk areas",
                        "Mobilize security and medical teams to vulnerable areas",
                        "Enlist volunteers to augment local responders",
                        "Pre-position clearing equipment and emergency assets",
                        "Full activation of Incident Command System (ICS)",
                        "Activate all response clusters",
                        "Request augmentation from provincial/regional level if needed",
                        "SITREP reporting every 6 hours"
                    ]
                
                if not st.session_state.pdra_actions_list:
                    st.session_state.pdra_actions_list = default_actions.copy()
                
                st.rerun()
        
        # Display confirmed PDRA results
        if st.session_state.pdra_confirmed and st.session_state.pdra_cpa_level:
            cpa_level = st.session_state.pdra_cpa_level
            
            # Set color and thresholds based on CPA level
            if cpa_level == "Alpha (Yellow)":
                cpa_color = "#ffc107"
                alert_status = "White"
                wind_speed = "Up to 70 km/h"
                rainfall = "Moderate to Heavy (2.6-15.0 mm/h)"
                distance = "51-100 km from critical storm track"
            elif cpa_level == "Bravo (Orange)":
                cpa_color = "#fd7e14"
                alert_status = "Blue"
                wind_speed = "Up to 88 km/h"
                rainfall = "Heavy to Intense (7.6-30 mm/h)"
                distance = "1-50 km from most critical areas"
            else:  # Charlie (Red)
                cpa_color = "#dc3545"
                alert_status = "Red"
                wind_speed = "Up to 130 km/h"
                rainfall = "Intense to Torrential (>30 mm/h)"
                distance = "Directly within storm's track/diameter"
            
            # Display CPA Level Card
            st.markdown(f"""
            <div style="background-color:{cpa_color}; color:white; padding:15px; border-radius:8px; margin:15px 0;">
                <strong style="font-size:18px;">CPA LEVEL: {cpa_level}</strong><br>
                <small>Alert Status: {alert_status}</small><br>
                <small>Wind Speed: {wind_speed} | Rainfall: {rainfall}</small><br>
                <small>Distance: {distance}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # State of Imminent Disaster Declaration (for Charlie level)
            if cpa_level == "Charlie (Red)":
                st.markdown("---")
                st.markdown("#### ⚖️ State of Imminent Disaster Declaration")
                st.caption("Under Republic Act No. 12287 (Declaration of State of Imminent Disaster Act of 2025)")
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    declare_imminent = st.checkbox(
                        "Recommend Declaration of State of Imminent Disaster",
                        value=st.session_state.pdra_imminent_declared,
                        key="pdra_imminent_checkbox"
                    )
                with col2:
                    if declare_imminent:
                        st.session_state.pdra_imminent_declared = True
                        st.success("✅ Recommendation recorded. Forward to Governor for declaration.")
                        st.info("""
                        **Next Steps:**
                        1. Submit PDRA results to Provincial Governor
                        2. Governor issues declaration within 24 hours
                        3. Declaration enables: Quick Response Fund, pre-emptive evacuation authority, emergency procurement
                        """)
                    else:
                        st.session_state.pdra_imminent_declared = False
            
            st.markdown("**📋 Critical Preparedness Actions:**")
            
            # Define CPA-specific action lists (keeping only the display part)
            alpha_actions = [
                "**Upon Alert:**",
                "• Checked risk maps",
                "• Issued directives, as necessary",
                "• Convened the MDRRMC",
                "• Prepared administrative and logistical support",
                "",
                "**Within 24 Hours After Alert:**",
                "• Conducted PDRA",
                "• Monitored alerts and reviewed geohazard and risk maps",
                "• Assessed local risks and scenarios",
                "• Determined the need for pre-emptive or mandatory evacuation",
                "• Prepared cash advances and vouchers",
                "• Checked the list of resources needed",
                "• Procured or borrowed additional resources",
                "• Revisited memoranda of agreement with the private sector",
                "• Activated and staffed the MDRRMO Operations Center for 24/7 monitoring",
                "• Activated the Incident Management Team and response clusters",
                "• Mobilized teams and enlisted volunteers",
                "• Checked the functionality and readiness of equipment and teams",
                "• Checked the availability of medicines and supplies in evacuation centers",
                "• Checked access to safe and clean water in evacuation centers",
                "• Issued alerts and warnings to communities",
                "• Disseminated alerts and warnings through radio and media groups",
                "• Prepared evacuation centers, when necessary",
                "• Placed teams on standby and alert",
                "• Secured communications, power, and water supply",
                "• Ensured advisories reached communities",
                "• Assisted in the pre-evacuation of livelihood assets, when possible",
                "• Submitted the PDRA report to the province and concerned agencies",
                "• Coordinated status updates with the province and concerned authorities",
                "• Submitted regular situational reports (SitReps) to the PDRRMO",
                "",
                "**Within 24 Hours Before Landfall:**",
                "• Issued directives suspending or cancelling classes and work, when necessary",
                "• Issued restrictions on fishing and other water-related activities, when necessary",
                "• Issued restrictions on land travel, when necessary",
                "• Conducted an MDRRMC meeting to review updates on critical preparations",
                "• Implemented pre-emptive or voluntary evacuation, when necessary",
                "• Estimated the number of evacuees, when necessary",
                "• Deployed teams to monitor landslide-prone and flood-prone areas",
                "• Ensured the evacuation of people in high-risk areas",
                "• Enforced mandatory evacuation, when necessary"
            ]
            
            bravo_actions = [
                "**Upon Alert:**",
                "• Issued directives",
                "• Convened the MDRRMC and instructed the LDRRMO to coordinate with MDRRMC members",
                "• Prepared administrative and logistical support",
                "",
                "**Within 24 Hours After Alert:**",
                "• Conducted PDRA",
                "• Activated and staffed the MDRRMO Operations Center for 24/7 monitoring",
                "• Activated the Incident Management Team and response clusters",
                "• Prepared cash advances and vouchers",
                "• Checked the list of resources needed",
                "• Checked the inventory of supplies, vehicles, and relief goods",
                "• Procured or borrowed additional resources",
                "• Revisited memoranda of agreement with the private sector",
                "• Mobilized teams and enlisted volunteers",
                "• Checked the functionality and readiness of teams and equipment",
                "• Implemented pre-emptive or voluntary evacuation, when necessary",
                "• Assessed additional structures or areas for possible use as evacuation centers",
                "• Deployed teams to monitor landslide-prone and flood-prone areas",
                "• Issued suspension of work in critical areas, such as slope protection structures",
                "• Secured communications, power, and water supply",
                "• Secured jail facilities",
                "• Ensured adequate markers to guide evacuees and response teams",
                "• Estimated the number of evacuees, when necessary",
                "• Ensured adequate medicines and supplies in evacuation centers",
                "• Ensured clean and functional evacuation center facilities, including toilets",
                "• Ensured access to safe and clean water in evacuation centers",
                "• Issued alerts and warnings to communities",
                "• Disseminated alerts and warnings through radio and media groups",
                "• Announced pre-emptive or voluntary evacuation, when necessary",
                "• Prepared evacuation centers, when necessary",
                "• Prepared the list and profile of evacuees, when necessary",
                "• Assisted in the pre-evacuation of livelihood stocks, when possible",
                "• Submitted the PDRA report to the province and concerned agencies",
                "• Gathered and consolidated reports from cluster heads",
                "• Submitted status reports to the PDRRMC Emergency Operations Center",
                "• Continued external coordination with neighboring EOCs",
                "• Submitted regular SitReps to the PDRRMC EOC",
                "",
                "**Within 24 Hours Before Landfall:**",
                "• Issued directives suspending or cancelling classes and work, when necessary",
                "• Issued suspension of works in critical areas, such as slope protection structures",
                "• Issued land travel bans, when necessary",
                "• Conducted an MDRRMC meeting to discuss updates on critical preparations",
                "• Ensured that people in high-risk areas were evacuated",
                "• Enforced mandatory evacuation, when necessary",
                "• Conducted patrols",
                "• Ensured unobstructed routes for safe and faster response actions",
                "• Ensured that information and advisories reached communities",
                "• Issued suspension of tourism activities",
                "• Issued suspension of public transportation operations"
            ]
            
            charlie_actions = [
                "**Upon Alert:**",
                "• Issued directives",
                "• Convened the MDRRMC and instructed the LDRRMO to coordinate with MDRRMC members",
                "• Prepared administrative and logistical support",
                "",
                "**Within 24 Hours After Alert:**",
                "• Conducted PDRA",
                "• Activated and staffed the MDRRMO Operations Center for 24/7 monitoring",
                "• Activated the Incident Management Team and response clusters",
                "• Prepared cash advances and vouchers",
                "• Checked the list of resources needed",
                "• Checked the inventory of supplies, vehicles, and relief goods",
                "• Procured or borrowed additional resources",
                "• Revisited memoranda of agreement with the private sector",
                "• Mobilized teams and enlisted volunteers",
                "• Checked the functionality and readiness of teams and equipment",
                "• Started pre-emptive and voluntary evacuation",
                "• Assessed additional structures or places for possible use as evacuation centers",
                "• Deployed teams to monitor landslide-prone and flood-prone areas",
                "• Secured communications, power, and water supply",
                "• Secured jail facilities",
                "• Ensured adequate markers to guide evacuees and response teams",
                "• Estimated the number of evacuees",
                "• Ensured sufficient medicines, equipment, and supplies in evacuation centers",
                "• Ensured clean and functional evacuation center facilities",
                "• Ensured access to safe and clean water in evacuation centers",
                "• Issued alerts and warnings to communities",
                "• Disseminated alerts and warnings through radio and media groups",
                "• Announced pre-emptive or voluntary evacuation",
                "• Prepared evacuation centers",
                "• Prepared the list and profile of evacuees",
                "• Assisted in the pre-evacuation of livelihood stocks, when possible",
                "• Monitored weather advisories and bulletins from DOST-PAGASA and MGB",
                "• Submitted the PDRA report to the PDRRMC EOC",
                "• Gathered and consolidated reports from cluster heads",
                "• Submitted status and situation reports to PDRRMC EOC",
                "• Continued external coordination with neighboring EOCs and the PDRRMC EOC",
                "• Submitted regular SitReps to the PDRRMC EOC",
                "",
                "**Within 24 Hours Before Landfall:**",
                "• Issued suspension of classes and work",
                "• Issued fishing bans and other water-related activity restrictions",
                "• Issued land travel bans",
                "• Conducted an MDRRMC meeting to discuss updates on critical preparations",
                "• Ensured that people in high-risk areas were evacuated",
                "• Enforced mandatory evacuation, when necessary",
                "• Conducted patrols",
                "• Ensured unobstructed routes for safe and faster response actions",
                "• Ensured that warnings and advisories reached communities",
                "• Declared a State of Imminent Disaster, when necessary"
            ]
            
            # Select the appropriate action list based on CPA level
            if "Alpha" in cpa_level:
                action_list = alpha_actions
            elif "Bravo" in cpa_level:
                action_list = bravo_actions
            else:
                action_list = charlie_actions
            
            # Display the actions
            for action in action_list:
                if action.startswith("**"):
                    st.markdown(action)
                elif action == "":
                    st.markdown("")
                else:
                    st.markdown(action)
            
            # ===== ENHANCED PDRA DECISION TOOL =====
            with st.expander("📊 Enhanced PDRA Decision Tool (Based on Operation L!sto Manual)", expanded=False):
                st.markdown("""
                <div style="background-color:#2c3e50; color:white; padding:10px; border-radius:5px; margin-bottom:15px;">
                    <h4 style="color:white; margin:0;">🎯 CPA to Alert Level Mapping</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # CPA Mapping Table
                st.markdown("""
                | CPA Level | Alert Status | Warning Threshold | General Action |
                |-----------|--------------|-------------------|----------------|
                | 🟡 **Alpha (Yellow)** | 🟢 White Alert | 7.5-15 mm rain (Yellow) | **MONITOR** weather condition |
                | 🟠 **Bravo (Orange)** | 🔵 Blue Alert | 15-30 mm rain (Orange) | **PREPARE** - Alert for possible evacuation |
                | 🔴 **Charlie (Red)** | 🔴 Red Alert | >30 mm rain (Red) | **RESPOND** - Evacuation, State of Calamity |
                """)
                
                st.markdown("---")
                
                # Water Level Threshold
                st.markdown("### 🌊 Water Level Warning System")
                st.markdown("""
                | Warning | Threshold | Action |
                |---------|-----------|--------|
                | 🟡 Yellow (60% bank full) | Water level at 60% | **MONITOR** - Inform LDRRMC, disseminate warnings |
                | 🟠 Orange (80% bank full) | Water level at 80% | **PREPARE** - Convene LDRRMC, activate EOC, pre-emptive evacuation |
                | 🔴 Red (100% bank full) | Water level at or above 100% | **RESPOND** - Forced evacuation, declare State of Calamity |
                """)
                
                st.markdown("---")
                
                # General Action Areas
                st.markdown("### 📋 General Action Areas")
                st.markdown("""
                | Action Level | Description | Key Activities |
                |-----------|-------------|----------------|
                | **MONITOR** | Yellow Warning / Alpha CPA | Inform LDRRMC and BDRRMC, disseminate public warnings, issue advisory prohibiting fishing/river crossing, monitor PAGASA and ALERTO updates |
                | **PREPARE** | Orange Warning / Bravo CPA | Convene LDRRMC, activate EOC, activate Incident Command System (ICS), preposition response clusters, implement pre-emptive evacuation |
                | **RESPOND** | Red Warning / Charlie CPA | Activate all response clusters, implement forced evacuation, declare State of Calamity if necessary, submit SITREP to higher LDRRMC, conduct RDANA |
                """)
                
                st.markdown("---")
                
                # Critical Areas
                st.markdown("### 🗺️ Critical Areas (Flood-Prone)")
                st.caption("Based on flood hazard maps - update based on your locality")
                
                critical_areas = [
                    "Barlig: Chupac, Fiangtin, Gawana, Kaleo, Latang",
                    "Bauko: Guinzadan Norte, Leseb, Mabaay, Otucan Sur, Sadsadan",
                    "Besao: Agawa, Gueday, Suquib",
                    "Bontoc: Balili, Gonogon, Talubin",
                    "Natonin: Balangao, Banawel, Poblacion, Saliok",
                    "Paracelis: Anonat, Bacarri, Bantay, Buringal",
                    "Sabangan: All barangays (flood-prone)",
                    "Sadanga: Sacasacan, Betwagan",
                    "Sagada: Ambasing, Dagdag, Poblacion, Suyo",
                    "Tadian: Cadad-anan, Dacudac, Lenga"
                ]
                
                for area in critical_areas:
                    st.markdown(f"- {area}")
                
                st.markdown("---")
                
                # Responses to Alert Warning
                st.markdown("### 🚨 Responses to Alert Warning")
                st.markdown("""
                | Alert Warning | Required Responses |
                |---------------|-------------------|
                | 🟡 **Yellow Warning** | • Inform LDRRMC and BDRRMC<br>• Disseminate public warnings and IEC<br>• Issue advisory prohibiting fishing and river crossing<br>• Monitor PAGASA and ALERTO updates |
                | 🟠 **Orange Warning** | • Convene LDRRMC<br>• Activate Emergency Operation Center (EOC)<br>• Activate Incident Command System (ICS)<br>• Preposition Response Clusters (Security, Humanitarian)<br>• Implement pre-emptive evacuation if applicable |
                | 🔴 **Red Warning** | • Activate all Response Clusters<br>• Implement forced evacuation if applicable<br>• Declare State of Calamity if necessary<br>• Submit SITREP to higher LDRRMC<br>• Conduct Rapid Damage Assessment and Needs Analysis (RDANA) |
                """)
                
                st.markdown("---")
                
                # Source Reference
                st.caption("Source: Rodriguez, M. S., Aying, J. G., Epino, E. V., & Languayan, K. B. (2021). *Disaster preparedness manual for localized weather disturbances*. Ateneo Center for Environment and Sustainability, Ateneo de Zamboanga University.")
    
   
    # ===== PDRA REFERENCE GUIDE (Expandable) =====
    with st.expander("📘 PDRA Reference Guide - Operation L!sto (Click to expand)", expanded=False):
        st.markdown("""
        ### 📘 Pre-Disaster Risk Assessment (PDRA) Reference Guide
        
        **Source:** Rodriguez, M. S., Aying, J. G., Epino, E. V., & Languayan, K. B. (2021). *Disaster preparedness manual for localized weather disturbances*. Ateneo Center for Environment and Sustainability, Ateneo de Zamboanga University.
        
        ---
        
        ### CPA to Alert Level Mapping
        
        | CPA Level | Your SOP Alert | Wind Speed | Rainfall | Distance |
        |-----------|----------------|------------|----------|----------|
        | **Alpha (Yellow)** | 🟢 White Alert | Up to 70 km/h | Moderate to Heavy (2.6-15.0 mm/h) | 51-100 km from critical track |
        | **Bravo (Orange)** | 🔵 Blue Alert | Up to 88 km/h | Heavy to Intense (7.6-30 mm/h) | 1-50 km from critical areas |
        | **Charlie (Red)** | 🔴 Red Alert | Up to 130 km/h | Intense to Torrential (>30 mm/h) | Directly within storm's track |
        
        ---
        
        ### Required Actions by CPA Level
        
        **Alpha (Yellow) - White Alert: Prepare & Monitor**
        - Convene LDRRMC
        - Issue directives to relevant local offices
        - Prepare administrative and logistical support
        - Activate Emergency Operations Center (EOC) on standby
        
        **Bravo (Orange) - Blue Alert: Mobilize & Standby**
        - Activate Incident Command System (ICS)
        - Check inventory of relief goods and supplies
        - Put SRR teams on standby
        - Issue advisory for discretionary/pre-emptive evacuation
        
        **Charlie (Red) - Red Alert: Respond & Evacuate**
        - Implement forced/mandatory evacuation
        - Mobilize security and medical teams
        - Enlist volunteers to augment responders
        - Pre-position clearing equipment and emergency assets
        - **Recommend Declaration of State of Imminent Disaster**
        
        ---
        
        ### Republic Act No. 12287 (2025)
        *Declaration of State of Imminent Disaster Act*
        
        **Trigger:** Charlie (Red) CPA Level based on PDRA + PAGASA forecasts
        
        **Benefits of Declaration:**
        - Access to Quick Response Fund
        - Pre-emptive evacuation authority
        - Emergency procurement
        - Pre-positioning of supplies
        
        *Source: DILG-LGA (2018). Operation L!sto disaster preparedness manual v.3.*
        """)


# ============================================================
# MAIN SITREP FORM FUNCTION
# ============================================================

def show_provincial_sitrep_form():
    """Main SitRep Form - Complete with descriptive titles and proper section ordering"""

    st.markdown("### 📝 Situation Report Form")
    
    # ===== CUSTOM CSS FOR TIGHTER SPACING =====
    st.markdown("""
    <style>
    /* Tighter spacing for headers */
    .stMarkdown h3, .stMarkdown h4 {
        margin-bottom: 5px !important;
        margin-top: 5px !important;
    }
    /* Tighter spacing for section boxes */
    .section-header {
        padding: 8px 12px !important;
        margin-bottom: 10px !important;
        border-radius: 8px;
    }
    .subsection-header {
        padding: 6px 10px !important;
        margin-bottom: 8px !important;
        border-radius: 5px;
    }
    /* Tighter spacing for expanders */
    .streamlit-expanderHeader {
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
    }
    /* Reduce line spacing in text */
    p, li, .caption {
        margin-bottom: 2px !important;
        line-height: 1.3 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ===== LETTERHEAD PLACEHOLDER =====
    with st.expander("📄 Letterhead (Placeholder)", expanded=False):
        st.info("""
        **LETTERHEAD PLACEHOLDER**
        
        The official letterhead will be inserted here in the final version.
        This space is reserved for:
        - Office Logo
        - Republic of the Philippines
        - Province of Mountain Province
        - Office of the Provincial Disaster Risk Reduction and Management Officer
        """)

    st.markdown("---")

    # ===== HEADER SECTION =====
    st.markdown("#### 📋 REPORT HEADER")

    # Initialize permanent values
    if "for_name" not in st.session_state:
        st.session_state.for_name = "DIR. ALBERT A MOGOL AFP (Ret.)"
    if "for_title" not in st.session_state:
        st.session_state.for_title = "REGIONAL DIRECTOR, OCD-CAR & Chairperson, Cordillera RDRRMC"
    if "thru_name" not in st.session_state:
        st.session_state.thru_name = "BONIFACIO C. LACWASAN, JR."
    if "thru_title" not in st.session_state:
        st.session_state.thru_title = "Provincial Governor and Chairperson, PDRRMC"
    if "from_name" not in st.session_state:
        st.session_state.from_name = "ATTY. EDWARD F. CHUMAWAR, JR."
    if "from_title" not in st.session_state:
        st.session_state.from_title = "PDRRM Officer"

    # FOR Section - Compact
    with st.expander("📌 FOR (Click to Edit if Needed)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_for_name = st.text_input("FOR Name", value=st.session_state.for_name, key="edit_for_name")
        with col2:
            new_for_title = st.text_input("FOR Title", value=st.session_state.for_title, key="edit_for_title")
        if st.button("Save FOR Changes"):
            st.session_state.for_name = new_for_name
            st.session_state.for_title = new_for_title
            st.success("FOR information updated!")
            st.rerun()

    st.markdown(f"**FOR:** {st.session_state.for_name}")
    st.markdown(f"{st.session_state.for_title}")
    st.markdown("---")

    # THRU Section - Compact
    with st.expander("📌 THRU (Click to Edit if Needed)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_thru_name = st.text_input("THRU Name", value=st.session_state.thru_name, key="edit_thru_name")
        with col2:
            new_thru_title = st.text_input("THRU Title", value=st.session_state.thru_title, key="edit_thru_title")
        if st.button("Save THRU Changes"):
            st.session_state.thru_name = new_thru_name
            st.session_state.thru_title = new_thru_title
            st.success("THRU information updated!")
            st.rerun()

    st.markdown(f"**THRU:** {st.session_state.thru_name}")
    st.markdown(f"{st.session_state.thru_title}")
    st.markdown("---")

    # FROM Section - Compact
    with st.expander("📌 FROM (Click to Edit if Needed)", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_from_name = st.text_input("FROM Name", value=st.session_state.from_name, key="edit_from_name")
        with col2:
            new_from_title = st.text_input("FROM Title", value=st.session_state.from_title, key="edit_from_title")
        if st.button("Save FROM Changes"):
            st.session_state.from_name = new_from_name
            st.session_state.from_title = new_from_title
            st.success("FROM information updated!")
            st.rerun()

    st.markdown(f"**FROM:** {st.session_state.from_name}")
    st.markdown(f"{st.session_state.from_title}")
    st.markdown("---")

    # ===== ENHANCED SUBJECT LINE GENERATOR =====
    st.markdown("**SUBJECT:**")
    
    # Initialize session state for subject
    if "sitrep_num" not in st.session_state:
        st.session_state.sitrep_num = 1
    if "generated_subject" not in st.session_state:
        st.session_state.generated_subject = ""
    if "incident_name" not in st.session_state:
        st.session_state.incident_name = ""
    if "incident_location" not in st.session_state:
        st.session_state.incident_location = ""
    if "operational_phase" not in st.session_state:
        st.session_state.operational_phase = ""
    if "selected_hazard_types" not in st.session_state:
        st.session_state.selected_hazard_types = []
    
    # ===== Row 1: SITREP Number =====
    col1, col2 = st.columns([1, 3])
    with col1:
        sitrep_number = st.number_input(
            "SITREP #",
            min_value=1,
            value=st.session_state.sitrep_num,
            step=1,
            key="sitrep_num_input",
            help="Sequential number. Starts at 1, continues until Terminal Report"
        )
    
    # ===== Row 2: Incident Type =====
    st.markdown("**Incident Type (Select all that apply):**")
    st.caption("Select one or more hazard types. This will sync with DRRM Intelligence classification.")
    
    # Define hazard categories
    hydrometeorological_hazards = [
        "Tropical Depression", "Tropical Storm", "Severe Tropical Storm",
        "Typhoon", "Super Typhoon", "Southwest Monsoon (Habagat)",
        "Northeast Monsoon (Amihan)", "Low Pressure Area (LPA)",
        "Shear Line", "Intertropical Convergence Zone (ITCZ)",
        "Thunderstorm", "Flood/Flashflood", "Landslide",
        "Storm Surge", "La Niña", "El Niño"
    ]
    
    geological_hazards = [
        "Earthquake", "Earthquake-Induced Landslide",
        "Volcanic Eruption", "Ground Fissure", "Liquefaction"
    ]
    
    other_hazards = [
        "Structural Fire", "Forest/Grass Fire", "Vehicular Accident",
        "Aviation Accident", "Armed Conflict", "Missing Person",
        "Found Cadaver", "Drowning", "Medical Emergency",
        "Attempted Suicide", "Shooting Incident", "Stabbing Incident",
        "Chemical Spill", "Infrastructure Collapse", "Power Outage",
        "Water Shortage", "Disease Outbreak"
    ]
    
    # Display Hydrometeorological Hazards
    with st.expander("🌊 HYDROMETEOROLOGICAL HAZARDS", expanded=True):
        cols = st.columns(3)
        for idx, hazard in enumerate(hydrometeorological_hazards):
            with cols[idx % 3]:
                is_selected = hazard in st.session_state.selected_hazard_types
                if st.checkbox(hazard, value=is_selected, key=f"hazard_hydro_{idx}"):
                    if hazard not in st.session_state.selected_hazard_types:
                        st.session_state.selected_hazard_types.append(hazard)
                else:
                    if hazard in st.session_state.selected_hazard_types:
                        st.session_state.selected_hazard_types.remove(hazard)
    
    # Display Geological Hazards
    with st.expander("🌋 GEOLOGICAL HAZARDS", expanded=True):
        cols = st.columns(3)
        for idx, hazard in enumerate(geological_hazards):
            with cols[idx % 3]:
                is_selected = hazard in st.session_state.selected_hazard_types
                if st.checkbox(hazard, value=is_selected, key=f"hazard_geo_{idx}"):
                    if hazard not in st.session_state.selected_hazard_types:
                        st.session_state.selected_hazard_types.append(hazard)
                else:
                    if hazard in st.session_state.selected_hazard_types:
                        st.session_state.selected_hazard_types.remove(hazard)
    
    # Display Other Hazards
    with st.expander("📋 OTHER HAZARDS / INCIDENTS", expanded=True):
        cols = st.columns(3)
        for idx, hazard in enumerate(other_hazards):
            with cols[idx % 3]:
                is_selected = hazard in st.session_state.selected_hazard_types
                if st.checkbox(hazard, value=is_selected, key=f"hazard_other_{idx}"):
                    if hazard not in st.session_state.selected_hazard_types:
                        st.session_state.selected_hazard_types.append(hazard)
                else:
                    if hazard in st.session_state.selected_hazard_types:
                        st.session_state.selected_hazard_types.remove(hazard)
    
    # Display selected hazards summary
    if st.session_state.selected_hazard_types:
        st.info(f"**Selected Hazard Types:** {', '.join(st.session_state.selected_hazard_types)}")
    else:
        st.warning("⚠️ No hazard type selected. Please select at least one.")
    
    st.markdown("---")
    
    # ===== Row 3: Incident Name =====
    st.markdown("**Incident Name:**")
    st.caption("Be specific. For typhoons, use the PAGASA name. For other incidents, describe briefly.")
    
    # Generate suggestions based on selected hazards
    suggested_names = []
    if st.session_state.selected_hazard_types:
        primary = st.session_state.selected_hazard_types[0]
        if "Typhoon" in primary or "Tropical" in primary:
            suggested_names = ["Typhoon ENTER_NAME", "Severe Tropical Storm ENTER_NAME", "Tropical Depression ENTER_NAME"]
        elif "Monsoon" in primary:
            suggested_names = ["Southwest Monsoon (Habagat)", "Northeast Monsoon (Amihan)"]
        elif "Earthquake" in primary:
            suggested_names = ["7.0 Magnitude Earthquake", "5.5 Magnitude Aftershock"]
        elif "Fire" in primary:
            suggested_names = ["Structural Fire at", "Forest Fire at"]
        elif "Landslide" in primary:
            suggested_names = ["Landslide at", "Rain-Induced Landslide at"]
        elif "Flood" in primary:
            suggested_names = ["Flashflood at", "Flooding at"]
        else:
            suggested_names = [f"{primary} at", f"{primary} Incident"]
    
    col1, col2 = st.columns([3, 1])
    with col1:
        if suggested_names:
            selected_suggestion = st.selectbox(
                "Quick Select (Optional)",
                options=["[Type custom name below]"] + suggested_names,
                key="incident_name_suggestion",
                label_visibility="collapsed"
            )
            if selected_suggestion != "[Type custom name below]":
                st.session_state.incident_name = selected_suggestion
        with col2:
            st.write("")
    
    incident_name = st.text_input(
        "Incident Name",
        value=st.session_state.incident_name,
        placeholder="e.g., Typhoon UWAN, 7.0 Magnitude Earthquake, Structural Fire at Poblacion",
        key="incident_name_input",
        help="For typhoons, use the PAGASA name. For other incidents, provide a brief descriptive name."
    )
    st.session_state.incident_name = incident_name
    
    st.markdown("---")
    
    # ===== Row 4: Location =====
    location = st.text_input(
        "Location (optional)",
        value=st.session_state.incident_location,
        placeholder="e.g., Bontoc, Mountain Province | Barangay X, Municipality Y",
        key="incident_location_input",
        help="Specific location of incident. Leave blank if province-wide."
    )
    
    st.markdown("---")
    
    # ===== Row 5: Operational Phase =====
    st.markdown("**Operational Phase:**")
    
    # Determine if weather-related
    weather_hazards = hydrometeorological_hazards
    is_weather_related = any(h in st.session_state.selected_hazard_types for h in weather_hazards)
    
    if is_weather_related:
        operational_phase = st.selectbox(
            "Select Operational Phase",
            options=[
                "Monitoring of",
                "Preparations for the Possible Effects of",
                "Monitoring the Effects of",
                "Impacts of",
                "Terminal Report on the Recovery Efforts on the Impacts of"
            ],
            index=0,
            key="operational_phase_weather",
            help="Select the phase that best describes the current situation"
        )
        
        if operational_phase == "Preparations for the Possible Effects of":
            st.warning("""
            ⚠️ **PDRA Required:** Before sending this SITREP, ensure you have:
            1. Conducted the PDR Assessment (go to the 'PDR Assessment' tab)
            2. Confirmed the CPA Level (Alpha/Bravo/Charlie)
            3. Reviewed the Critical Preparedness Actions
            """)
    else:
        operational_phase = st.selectbox(
            "Select Operational Phase",
            options=[
                "Initial Report on",
                "Response Operations on",
                "Search and Rescue Operations on",
                "Recovery Operations on",
                "Update on",
                "Investigation on",
                "Final Report on",
                "Terminal Report on"
            ],
            index=0,
            key="operational_phase_nonweather",
            help="Select the phase for this incident"
        )
    
    # Store values
    st.session_state.sitrep_num = sitrep_number
    st.session_state.incident_name = incident_name
    st.session_state.incident_location = location
    st.session_state.operational_phase = operational_phase
    
    # ===== Generate Subject Line Preview =====
    st.markdown("---")
    st.markdown("**📋 Subject Line Preview:**")
    
    if incident_name:
        hazard_str = ", ".join(st.session_state.selected_hazard_types) if st.session_state.selected_hazard_types else "Incident"
        
        if operational_phase == "Impacts of":
            subject_line = f"SITREP #{sitrep_number}: {operational_phase} {incident_name} ({hazard_str}) - Damage & Needs Assessment"
        elif operational_phase == "Terminal Report on the Recovery Efforts on the Impacts of":
            subject_line = f"SITREP #{sitrep_number}: {operational_phase} {incident_name}"
        elif location:
            subject_line = f"SITREP #{sitrep_number}: {operational_phase} {incident_name} ({location})"
        else:
            subject_line = f"SITREP #{sitrep_number}: {operational_phase} {incident_name}"
        
        st.info(f"📋 **{subject_line}**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Use This Subject Line", key="use_subject_enhanced"):
                st.session_state.generated_subject = subject_line
                st.success("Subject line saved!")
        with col2:
            if st.button("➕ Next SITREP (#" + str(sitrep_number + 1) + ")", key="next_sitrep_enhanced"):
                st.session_state.sitrep_num = sitrep_number + 1
                st.session_state.generated_subject = ""
                st.session_state.incident_name = ""
                st.session_state.incident_location = ""
                st.session_state.selected_hazard_types = []
                st.rerun()
    else:
        st.warning("Please enter Incident Name to generate subject line")
    
    if st.session_state.generated_subject:
        st.success(f"📋 **Current Subject Line:** {st.session_state.generated_subject}")
    
    # Save hazard types for PDRA compatibility
    st.session_state.selected_hazard_type = ", ".join(st.session_state.selected_hazard_types) if st.session_state.selected_hazard_types else ""
    st.session_state.pdra_hazard_type = st.session_state.selected_hazard_type
    
    st.markdown("---")
    
    # ===== DATE AND TIME =====
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**DATE:**")
        report_date = st.date_input("Report Date", value=date.today(), key="report_date", label_visibility="collapsed")
    with col2:
        st.markdown("**TIME:**")
        report_time = st.time_input("Report Time", value=datetime.now().time(), key="report_time", label_visibility="collapsed")
    
    st.markdown("---")
    
    # ============================================================
    # SECTION I: SITUATION OVERVIEW
    # ============================================================
    
    st.markdown("""
    <div class="section-header" style="background-color:#e8f4f8;">
        <h3 style="color:#000000; margin:0;">I. SITUATION OVERVIEW</h3>
        <p style="margin:5px 0 0 0; color:#333; font-size:14px;">
        <em>This section contains summarized weather information from PAGASA and local monitoring data. It provides the current weather situation, 
        alert levels per municipality, and real-time sensor data to help users understand the environmental conditions before any disaster impacts.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== 1. PAGASA WEATHER BULLETIN =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">1. PAGASA Weather Bulletin</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>Official weather advisories from PAGASA. This includes tropical cyclone bulletins for typhoons and daily weather forecasts 
        for other weather disturbances.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get hazard types from session state (now using selected_hazard_types list)
    selected_hazard_types = st.session_state.get("selected_hazard_types", [])
    
    tropical_cyclone_hazards = [
        "Tropical Depression", "Tropical Storm", "Severe Tropical Storm", 
        "Typhoon", "Super Typhoon"
    ]
    
    weather_hazards_forecast = [
        "Southwest Monsoon (Habagat)", "Northeast Monsoon (Amihan)", 
        "Low Pressure Area (LPA)", "Shear Line", "Intertropical Convergence Zone (ITCZ)",
        "Thunderstorm", "Flood/Flashflood", "Landslide"
    ]
    
    # Check if any selected hazard matches the categories
    is_tropical_cyclone = any(h in tropical_cyclone_hazards for h in selected_hazard_types)
    is_weather_forecast = any(h in weather_hazards_forecast for h in selected_hazard_types)
    
    if is_tropical_cyclone:
        with st.container(border=True):
            st.markdown("**Tropical Cyclone Bulletin Information**")
            
            col1, col2 = st.columns(2)
            with col1:
                bulletin_no = st.selectbox(
                    "Bulletin No.", 
                    options=["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "Final"], 
                    key="tc_bulletin_no"
                )
            with col2:
                issue_time = st.text_input(
                    "Issue Time", 
                    value=st.session_state.get("issue_time", ""), 
                    key="tc_issue_time",
                    placeholder="e.g., 11:00 PM, 27 May 2023"
                )
            
            typhoon_name = st.text_input(
                "Typhoon Name", 
                value=st.session_state.get("typhoon_name", ""), 
                key="tc_typhoon_name",
                placeholder="e.g., Betty (MAWAR)"
            )
            
            st.markdown("**Location of Center**")
            location_center = st.text_area(
                "Location of Center", 
                value=st.session_state.get("location_center", ""), 
                key="tc_location_center",
                height=68, 
                placeholder="e.g., 895 km East of Central Luzon (16.9°N, 130.5°E)"
            )
            
            st.markdown("**Intensity**")
            col1, col2 = st.columns(2)
            with col1:
                intensity_category = st.selectbox(
                    "Category", 
                    options=["", "Tropical Depression", "Tropical Storm", "Severe Tropical Storm", "Typhoon", "Super Typhoon"], 
                    key="tc_intensity_category"
                )
            with col2:
                wind_speed = st.text_input(
                    "Wind Speed", 
                    value="", 
                    key="tc_wind_speed",
                    placeholder="e.g., 175 km/h"
                )
            
            intensity = st.text_area(
                "Full Intensity Details", 
                value=st.session_state.get("intensity", ""), 
                key="tc_intensity",
                height=68, 
                placeholder="e.g., Maximum sustained winds of 175 km/h near the center, gustiness of up to 215 km/h"
            )
            
            st.markdown("**Present Movement**")
            col1, col2 = st.columns(2)
            with col1:
                movement_direction = st.selectbox(
                    "Direction", 
                    options=["", "West", "East", "North", "South", "Northwest", "Northeast", "Southwest", "Southeast", "Westward", "Eastward", "Northward", "Southward"], 
                    key="tc_movement_direction"
                )
            with col2:
                movement_speed = st.text_input(
                    "Speed", 
                    value="", 
                    key="tc_movement_speed",
                    placeholder="e.g., 25 km/h"
                )
            
            present_movement = st.text_input(
                "Full Movement Description", 
                value=st.session_state.get("present_movement", ""), 
                key="tc_present_movement",
                placeholder="e.g., Westward at 25 km/h"
            )
            
            extent_winds = st.text_input(
                "Extent of Tropical Cyclone Winds", 
                value=st.session_state.get("extent_winds", ""), 
                key="tc_extent_winds",
                placeholder="e.g., Strong to typhoon-force winds extend outwards up to 740 km from the center"
            )
            
            st.markdown("**Track and Intensity Outlook**")
            track_outlook = st.text_area(
                "Track and Intensity Outlook", 
                value=st.session_state.get("track_outlook", ""), 
                key="tc_track_outlook",
                height=80, 
                placeholder="e.g., BETTY WEAKENS INTO A TYPHOON"
            )
            
            st.markdown("**Tropical Cyclone Wind Signal (TCWS)**")
            tcws = st.text_area(
                "TCWS Information", 
                value=st.session_state.get("tcws", ""), 
                key="tc_tcws",
                height=60, 
                placeholder="e.g., TCWS #1 still in effect at western portion of Mountain Province"
            )
            
            bulletin_text = f"""Tropical Cyclone Bulletin No. {bulletin_no}
Typhoon: {typhoon_name}
Issued at: {issue_time}
Location of Center: {location_center}
Intensity: {intensity}
Present Movement: {present_movement}
Extent of Tropical Cyclone Winds: {extent_winds}
Track and Intensity Outlook: {track_outlook}
TCWS: {tcws}"""
    
    elif is_weather_forecast:
        with st.container(border=True):
            synopsis = st.text_area(
                "Synopsis", 
                value=st.session_state.get("synopsis", ""), 
                key="wf_synopsis",
                height=60
            )
            forecast_weather = st.text_area(
                "Forecast Weather Conditions", 
                value=st.session_state.get("forecast_weather", ""), 
                key="wf_forecast_weather",
                height=60
            )
            
            col1, col2 = st.columns(2)
            with col1:
                temp_min = st.text_input(
                    "Min Temperature", 
                    value=st.session_state.get("temp_min", ""), 
                    key="wf_temp_min",
                    placeholder="e.g., 24.9°C"
                )
            with col2:
                temp_max = st.text_input(
                    "Max Temperature", 
                    value=st.session_state.get("temp_max", ""), 
                    key="wf_temp_max",
                    placeholder="e.g., 35.0°C"
                )
            
            col1, col2 = st.columns(2)
            with col1:
                wind_speed = st.text_input(
                    "Wind Speed", 
                    value=st.session_state.get("wind_speed_forecast", ""), 
                    key="wf_wind_speed",
                    placeholder="e.g., Light to Moderate"
                )
            with col2:
                wind_direction = st.text_input(
                    "Wind Direction", 
                    value=st.session_state.get("wind_direction", ""), 
                    key="wf_wind_direction",
                    placeholder="e.g., Northwest"
                )
            
            rainfall_warning = st.text_area(
                "Rainfall Warning / Thunderstorm Advisory", 
                value=st.session_state.get("rainfall_warning", ""), 
                key="wf_rainfall_warning",
                height=60
            )
            
            bulletin_text = f"""Daily Weather Forecast:
Synopsis: {synopsis}
Forecast Weather Conditions: {forecast_weather}
Temperature: Min {temp_min} / Max {temp_max}
Wind: {wind_speed} / {wind_direction}
Rainfall Warning: {rainfall_warning}"""
    
    else:
        bulletin_text = st.text_area(
            "Weather Bulletin Information", 
            value=st.session_state.get("bulletin_text", ""), 
            height=150, 
            key="generic_bulletin"
        )
    
    st.markdown("---")
    
    # ===== 2. WEATHER & ALERT LEVEL STATUSES =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">2. Weather & Alert Level Statuses</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>Per municipality weather conditions and alert levels. This table helps track local variations in weather and preparedness across the province's 10 municipalities.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.caption("Source: MDRRMOs | Based on PAGASA weather terminologies")
    
    # Column headers
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown("**Municipality**")
    with col2:
        st.markdown("**Cloud Condition**")
    with col3:
        st.markdown("**Wind Condition**")
    with col4:
        st.markdown("**Alert Status**")
    
    weather_data = []
    for mun in municipalities:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.markdown(f"**{mun}**")
        with col2:
            cloud = st.selectbox("Cloud", ["", "Clear", "Cloudy", "Light Rains", "Heavy Rains"], key=f"cloud_{mun}", label_visibility="collapsed")
        with col3:
            wind = st.selectbox("Wind", ["", "Calm", "Light", "Moderate", "Strong"], key=f"wind_{mun}", label_visibility="collapsed")
        with col4:
            alert = st.selectbox("Alert", ["", "White", "Blue", "Red"], key=f"alert_{mun}", label_visibility="collapsed")
        weather_data.append({"municipality": mun, "cloud": cloud, "wind": wind, "alert": alert})
    
    overall_alert = st.selectbox("Overall Alert Status", ["", "White", "Blue", "Red"], key="overall_alert")
    st.markdown("---")

    # ===== OVERALL ALERT IS SET BY THE WIDGET ABOVE =====
    # No manual assignment needed - the overall_alert variable already contains the selected value


    # ===== 3. CAMPBELL SCIENTIFIC SENSOR DATA =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">3. Campbell Scientific Sensor Data</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>Real-time weather sensor data (placeholder for future integration). Once integrated, it will provide automated real-time updates on temperature, solar radiation, and rainfall.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📊 Real-Time Weather Sensor Data (Campbell Scientific) - Placeholder", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌡️ Temperature", "-- °C", delta=None)
        with col2:
            st.metric("☀️ Solar Radiation", "-- W/m²", delta=None)
        with col3:
            st.metric("💧 Rainfall", "-- mm", delta=None)
        st.info("📌 **Integration Note:** This section is ready to receive data from Campbell Scientific sensors via API.")
    
    st.markdown("---")

    # ============================================================
    # SECTION II: DISASTER PREPAREDNESS
    # ============================================================
    
    st.markdown("""
    <div class="section-header" style="background-color:#e8f4f8;">
        <h3 style="color:#000000; margin:0;">II. DISASTER PREPAREDNESS</h3>
        <p style="margin:5px 0 0 0; color:#333; font-size:14px;">
        <em>This section covers all preparedness measures, risk assessment activities, and operational readiness of response clusters and municipalities. 
        It documents what has been done BEFORE a disaster impacts the province, including PDRA findings and cluster readiness.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
# ===== START OF SECTION: PDRA SECTION =====

    # ===== 1. PRE-DISASTER RISK ASSESSMENT (PDRA) =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">1. Pre-Disaster Risk Assessment (PDRA)</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>The PDRA is a process to evaluate a hazard's level of risk given the degree of exposure and vulnerability. This section shows the PDRA results, 
        including alert status, critical activities conducted, anticipated needs, and duty officers.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display PDRA date/time and CPA level
    if st.session_state.get("pdra_confirmed", False) and st.session_state.get("pdra_cpa_level"):
        cpa_level = st.session_state.pdra_cpa_level
        
        if cpa_level == "Alpha (Yellow)":
            alert_status = "White Alert"
            alert_icon = "🟢"
        elif cpa_level == "Bravo (Orange)":
            alert_status = "Blue Alert"
            alert_icon = "🔵"
        else:
            alert_status = "Red Alert"
            alert_icon = "🔴"
        
        conducted_date = st.session_state.get("pdra_conducted_date", "Not set")
        conducted_time = st.session_state.get("pdra_conducted_time", "Not set")
        
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**📅 PDRA Conducted:** {conducted_date} at {conducted_time}")
            with col2:
                st.markdown(f"**🚨 Alert Status:** {alert_icon} {alert_status}")
            
            st.markdown("---")
            
            # ===== CRITICAL PREPAREDNESS ACTIONS (CPAs) WITH CHECKBOXES =====
            st.markdown("**📋 Critical Preparedness Actions Conducted (Select all that apply)**")
            st.caption("Check the CPAs that were actually conducted. Selected items will be saved in the SITREP.")
            
            # Initialize session state for CPA selections if not exists
            if "selected_upon_alert" not in st.session_state:
                st.session_state.selected_upon_alert = []
            if "selected_within_24hrs" not in st.session_state:
                st.session_state.selected_within_24hrs = []
            if "selected_before_landfall" not in st.session_state:
                st.session_state.selected_before_landfall = []
            
            # ===== UPON ALERT CPAs =====
            st.markdown("**🟡 UPON ALERT**")
            st.caption("Initial actions immediately after receiving alert/warning")
            
            upon_alert_cpas = [
                "Checked risk maps",
                "Issued directives",
                "Convened the MDRRMC",
                "Instructed the LDRRMO to coordinate with MDRRMC members",
                "Prepared administrative and logistical support"
            ]
            
            cols = st.columns(2)
            for idx, cpa in enumerate(upon_alert_cpas):
                with cols[idx % 2]:
                    is_checked = cpa in st.session_state.selected_upon_alert
                    checked = st.checkbox(cpa, value=is_checked, key=f"pdra_upon_alert_{idx}")
                    if checked and cpa not in st.session_state.selected_upon_alert:
                        st.session_state.selected_upon_alert.append(cpa)
                    elif not checked and cpa in st.session_state.selected_upon_alert:
                        st.session_state.selected_upon_alert.remove(cpa)
            
            st.markdown("---")
            
            # ===== WITHIN 24 HOURS AFTER ALERT CPAs =====
            st.markdown("**🟠 WITHIN 24 HOURS AFTER ALERT**")
            st.caption("Actions taken within 24 hours after alert issuance")
            
            within_24hrs_cpas = [
                "Conducted PDRA",
                "Activated and staffed the MDRRMO Operations Center for 24/7 monitoring",
                "Activated the Incident Management Team and response clusters",
                "Prepared cash advances and vouchers",
                "Checked the list of resources needed",
                "Conducted inventory of supplies, vehicles, and relief goods",
                "Procured or borrowed additional resources",
                "Revisited memoranda of agreement with the private sector",
                "Mobilized teams and enlisted volunteers",
                "Checked functionality of communication and rescue equipment",
                "Monitored alerts and weather advisories",
                "Assessed local risks and scenarios",
                "Determined need for pre-emptive or mandatory evacuation",
                "Prepositioned food packs and non-food items",
                "Identified and prepared evacuation centers",
                "Prepared list and profile of evacuees",
                "Estimated number of evacuees",
                "Ensured adequate medicines, water, and sanitation in evacuation centers",
                "Secured communications, power, and water supply",
                "Secured jail facilities",
                "Issued alerts and warnings to communities",
                "Disseminated alerts through media and barangays",
                "Implemented pre-emptive or voluntary evacuation",
                "Assisted in pre-evacuation of livelihood stocks",
                "Deployed teams to monitor landslide-prone and flood-prone areas",
                "Submitted PDRA report",
                "Gathered and consolidated reports from cluster heads",
                "Submitted status reports to province and concerned agencies",
                "Submitted regular SitReps to PDRRMO",
                "Continued external coordination with neighboring LGUs"
            ]
            
            cols = st.columns(2)
            for idx, cpa in enumerate(within_24hrs_cpas):
                with cols[idx % 2]:
                    is_checked = cpa in st.session_state.selected_within_24hrs
                    checked = st.checkbox(cpa, value=is_checked, key=f"pdra_within_24hrs_{idx}")
                    if checked and cpa not in st.session_state.selected_within_24hrs:
                        st.session_state.selected_within_24hrs.append(cpa)
                    elif not checked and cpa in st.session_state.selected_within_24hrs:
                        st.session_state.selected_within_24hrs.remove(cpa)
            
            st.markdown("---")
            
            # ===== WITHIN 24 HOURS BEFORE LANDFALL CPAs =====
            st.markdown("**🔴 WITHIN 24 HOURS BEFORE LANDFALL**")
            st.caption("Actions taken within 24 hours before expected landfall")
            
            before_landfall_cpas = [
                "Issued suspension or cancellation of classes and work",
                "Issued fishing bans and water activity restrictions",
                "Issued land travel bans",
                "Conducted MDRRMC meeting on critical preparations",
                "Placed teams on standby and alert",
                "Announced pre-emptive or voluntary evacuation",
                "Ensured evacuation of people in high-risk areas",
                "Enforced mandatory evacuation",
                "Conducted patrols",
                "Ensured unobstructed routes for response",
                "Ensured warnings and advisories reached communities",
                "Declared State of Imminent Disaster"
            ]
            
            cols = st.columns(2)
            for idx, cpa in enumerate(before_landfall_cpas):
                with cols[idx % 2]:
                    is_checked = cpa in st.session_state.selected_before_landfall
                    checked = st.checkbox(cpa, value=is_checked, key=f"pdra_before_landfall_{idx}")
                    if checked and cpa not in st.session_state.selected_before_landfall:
                        st.session_state.selected_before_landfall.append(cpa)
                    elif not checked and cpa in st.session_state.selected_before_landfall:
                        st.session_state.selected_before_landfall.remove(cpa)
            
            st.markdown("---")
            
            # ===== SELECTED CPAs SUMMARY =====
            st.markdown("### ✅ Selected CPAs (Will be saved in SITREP)")
            
            total_selected = len(st.session_state.selected_upon_alert) + len(st.session_state.selected_within_24hrs) + len(st.session_state.selected_before_landfall)
            
            if total_selected > 0:
                if st.session_state.selected_upon_alert:
                    st.markdown("**🟡 Upon Alert:**")
                    for cpa in st.session_state.selected_upon_alert:
                        st.markdown(f"• {cpa}")
                
                if st.session_state.selected_within_24hrs:
                    st.markdown("**🟠 Within 24 Hours After Alert:**")
                    for cpa in st.session_state.selected_within_24hrs:
                        st.markdown(f"• {cpa}")
                
                if st.session_state.selected_before_landfall:
                    st.markdown("**🔴 Within 24 Hours Before Landfall:**")
                    for cpa in st.session_state.selected_before_landfall:
                        st.markdown(f"• {cpa}")
            else:
                st.info("No CPAs selected yet. Check the boxes above to select CPAs that were conducted.")
            
            st.markdown("---")
            
            # ===== ANTICIPATED NEEDS ASSESSMENT =====
            st.markdown("**📊 Anticipated Needs Assessment (for State of Imminent Disaster)**")
            st.caption("Based on PDRA results - select anticipated needs. Selected items will be saved in the SITREP.")
            
            if "selected_anticipated_needs" not in st.session_state:
                st.session_state.selected_anticipated_needs = []
            
            anticipated_needs_list = [
                "Search and Rescue operations",
                "Immediate restoration of lifelines (power, water, communication)",
                "Relief supplies and food assistance",
                "Emergency medical supplies and health support",
                "Clothing and shelter materials",
                "Non-food items (hygiene kits, blankets, sleeping mats)",
                "Family tents and temporary shelter",
                "Water, sanitation, and hygiene (WASH) supplies",
                "Evacuation center support (cots, lamps, cooking utensils)",
                "Cash-for-work assistance for early recovery",
                "Farm implements and seeds for agricultural recovery",
                "Livestock feed and veterinary support",
                "Infrastructure repair and reconstruction materials",
                "Heavy equipment for clearing operations",
                "Communication equipment for response teams",
                "Transportation support for relief delivery",
                "Fuel for response vehicles and generators",
                "Psychosocial support and counseling services",
                "Protection services for vulnerable groups (children, elderly, PWDs)",
                "Duty officers and response team augmentation"
            ]
            
            cols = st.columns(2)
            for idx, need in enumerate(anticipated_needs_list):
                with cols[idx % 2]:
                    is_checked = need in st.session_state.selected_anticipated_needs
                    checked = st.checkbox(need, value=is_checked, key=f"anticipated_need_{idx}")
                    if checked and need not in st.session_state.selected_anticipated_needs:
                        st.session_state.selected_anticipated_needs.append(need)
                    elif not checked and need in st.session_state.selected_anticipated_needs:
                        st.session_state.selected_anticipated_needs.remove(need)
            
            # Selected Anticipated Needs Summary
            st.markdown("### ✅ Selected Anticipated Needs (Will be saved in SITREP)")
            if st.session_state.selected_anticipated_needs:
                for need in st.session_state.selected_anticipated_needs:
                    st.markdown(f"• {need}")
            else:
                st.info("No anticipated needs selected yet. Check the boxes above to select needs.")
            
            st.markdown("---")
            
            # ===== STATE OF IMMINENT DISASTER DECLARATION =====
            st.markdown("**⚖️ State of Imminent Disaster Declaration Recommendation**")
            st.caption("Under RA 12287 (Declaration of State of Imminent Disaster Act of 2025)")
            
            col1, col2 = st.columns(2)
            with col1:
                recommend_imminent = st.checkbox(
                    "Recommend Declaration of State of Imminent Disaster",
                    key="pdra_recommend_imminent",
                    help="Based on PDRA results and RA 12287 criteria"
                )
            with col2:
                if recommend_imminent:
                    st.text_area(
                        "Justification for Recommendation",
                        key="pdra_imminent_justification",
                        height=100,
                        placeholder="Example:\n- Severe projected impacts\n- 4-day lead time\n- Vulnerable populations at risk"
                    )
            
            st.markdown("**👥 Duty Officers at MPDRRMC OpCen:**")
            st.text_area(
                "Duty Officers", 
                key="duty_officers", 
                height=100, 
                placeholder="List duty officers and their assignments...\n\nExample:\n- SDO: Juan Dela Cruz\n- TLA: Maria Santos\n- ATA: Pedro Reyes"
            )
        
        st.markdown("""
        <p><em>📌 To update PDRA (change CPA level, edit actions), go to the <strong>"PDR Assessment"</strong> tab.</em></p>
        """, unsafe_allow_html=True)
    else:
        st.info("📌 No PDRA conducted yet. Go to the 'PDR Assessment' tab to conduct one.")

# ===== END OF SECTION: PDRA SECTION =====
    
    # ===== 2. OPERATIONAL READINESS OF RESPONSE CLUSTERS =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">2. Operational Readiness of Response Clusters</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>The response clusters are on stand-by and can be activated as the need arises. This section tracks the readiness status of each cluster, its lead agency, 
        composition, and response roles. Based on the National Disaster Response Plan 2024.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Response clusters based on National Disaster Response Plan 2024
    cluster_data = [
        {"cluster": "1. Law and Order", "lead": "Philippine National Police", "members": "BFP, DILG, AFP, OPSSO, BJMP, LTO, PIO", "status": "Standby"},
        {"cluster": "2. Logistics", "lead": "Office of the Provincial DRRM Officer", "members": "OPAGO, OPVET, BJMP, BFP, DSWD, PRC-MP, OPHO, DPWH-MPFDEO, DPWH-MPSDEO, OGSO, OPIO", "status": "Standby"},
        {"cluster": "3. Search, Rescue and Retrieval", "lead": "Bureau of Fire Protection", "members": "PRC-MP, PNP, OPDRRMO, BJMP, PHO, AFP, DICT, DILG, OPIO, PIA", "status": "Standby"},
        {"cluster": "4. Education", "lead": "Department of Education", "members": "DSWD-SWAD, PNP, OPHO, PRC, BFP, OPVET, MPSU, OPIO, PIA", "status": "Standby"},
        {"cluster": "5. Emergency Telecommunications", "lead": "Department of Information Communication Technology", "members": "OPIO, PIA, OPDRRMO, RADYO PILIPINAS, PNP", "status": "Standby"},
        {"cluster": "6. Debris Clearing and Civil Works", "lead": "Department of Public Works and Highways", "members": "OPE, BFP, PNP, OPVET, OPDRRMO, DENR, GSO, OPIO, PIA, RADYO PILIPINAS", "status": "Standby"},
        {"cluster": "7. Protection", "lead": "Office of the Provincial Social Welfare and Development Officer", "members": "DSWD-SWAD, BJMP, PRC, PNP, PHO, AFP, BFP, OPDRRMO, OPIO, PIA, RADYO PILIPINAS", "status": "Standby"},
        {"cluster": "8. Camp Coordination and Camp Management", "lead": "Office of the Provincial Social Welfare and Development Officer", "members": "DSWD-SWAD, PRC-MP, DEPED, BJMP, AFP, BFP, OPDRRMO, OPIO, PIA, RADYO PILIPINAS", "status": "Standby"},
        {"cluster": "9. Food and Non-Food", "lead": "Department of Social Welfare and Development", "members": "OPAG, OPVET, PRC-MP, OPSDWDO, BFP, BJMP, AFP, OPIO, PIA, RADYO PILIPINAS", "status": "Standby"},
        {"cluster": "10. Health", "lead": "Office of the Provincial Health Officer", "members": "DSWD-SWAD, OPVET, PRC, BFP, DEPED, MHOs, DILG, OPDRRMO, DICT, OPIO", "status": "Standby"},
        {"cluster": "11. Management of the Dead and the Missing", "lead": "Department of the Interior and Local Government", "members": "PRC-MP, BFP, OPHO, DSWD, DEPED, PNP, DPWH, OPSWDO, OPIO", "status": "Standby"},
        {"cluster": "12. Shelter", "lead": "Department of Social Welfare and Development", "members": "MSWDOs, MDRRMOs, BFP, OPIO", "status": "Standby"},
        {"cluster": "13. Early Recovery", "lead": "Office of the Provincial DRRM Officer", "members": "PRC-MP, OPHO, BFP, AFP, BJMP, DICT", "status": "Standby"},
        {"cluster": "14. Crisis Communications", "lead": "Philippine Information Agency", "members": "OPIO, PNP, RADYO PILIPINAS", "status": "Standby"}
    ]
    
    # Display clusters in a grid layout (2 columns)
    for i in range(0, len(cluster_data), 2):
        col1, col2 = st.columns(2)
        
        # First cluster in the pair
        with col1:
            cluster = cluster_data[i]
            with st.container(border=True):
                st.markdown(f"**{cluster['cluster']}**")
                st.caption(f"*Lead: {cluster['lead']}*")
                st.caption(f"*Members: {cluster['members']}*")
                status = st.selectbox(
                    "Status", 
                    ["Standby", "Activated", "Deployed", "Demobilized"], 
                    index=["Standby", "Activated", "Deployed", "Demobilized"].index(cluster['status']),
                    key=f"cluster_status_{cluster['cluster'].replace(' ', '_')}", 
                    label_visibility="collapsed"
                )
                cluster['status'] = status
        
        # Second cluster in the pair (if exists)
        if i + 1 < len(cluster_data):
            with col2:
                cluster = cluster_data[i + 1]
                with st.container(border=True):
                    st.markdown(f"**{cluster['cluster']}**")
                    st.caption(f"*Lead: {cluster['lead']}*")
                    st.caption(f"*Members: {cluster['members']}*")
                    status = st.selectbox(
                        "Status", 
                        ["Standby", "Activated", "Deployed", "Demobilized"], 
                        index=["Standby", "Activated", "Deployed", "Demobilized"].index(cluster['status']),
                        key=f"cluster_status_{cluster['cluster'].replace(' ', '_')}", 
                        label_visibility="collapsed"
                    )
                    cluster['status'] = status
    
    st.markdown("---")
    
    # ===== 3. MDRRMO OPERATIONS CENTER PREPAREDNESS ACTIVITIES =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">3. MDRRMO Operations Center Preparedness Activities</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>Based on Operation L!sto Critical Preparedness Actions (CPA). Select activities that apply, then click "Save Selected Activities" to add them to the list below. 
        Check and uncheck freely without scrolling - only saved when you click Save.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== CPA ACTIVITIES BY TIME BLOCK =====
    cpa_upon_alert = [
        "Checked risk maps",
        "Issued directives",
        "Convened the MDRRMC",
        "Instructed the LDRRMO to coordinate with MDRRMC members",
        "Prepared administrative and logistical support"
    ]
    
    cpa_within_24hrs_after = [
        "Conducted PDRA",
        "Activated and staffed the MDRRMO Operations Center for 24/7 monitoring, coordination, and reporting",
        "Activated the Incident Management Team and response clusters",
        "Conducted coordination with MDRRMC members, response clusters, barangays, and response partners",
        "Prepared cash advances and vouchers",
        "Checked the list of resources needed",
        "Conducted inventory of supplies, vehicles, relief goods, and other resources",
        "Procured or borrowed additional resources",
        "Revisited memoranda of agreement with the private sector",
        "Mobilized teams and enlisted volunteers",
        "Checked the functionality and readiness of communication, rescue, response, and early warning equipment",
        "Monitored alerts, weather advisories, and hazard/risk maps",
        "Assessed local risks and scenarios",
        "Determined the need for pre-emptive or mandatory evacuation",
        "Prepositioned food packs, non-food items, and equipment",
        "Identified available evacuation centers, including additional structures or places, and assessed their readiness",
        "Prepared evacuation centers",
        "Prepared the list and profile of evacuees",
        "Estimated the number of evacuees",
        "Ensured adequate medicines, equipment, supplies, water, and sanitation facilities in evacuation centers",
        "Secured communications, power, and water supply",
        "Secured jail facilities",
        "Ensured adequate markers to guide evacuees and response teams",
        "Issued alerts and warnings to communities",
        "Disseminated alerts and warnings through social media, radio, media groups, barangays, and communities",
        "Implemented pre-emptive or voluntary evacuation",
        "Assisted in the pre-evacuation of livelihood stocks, when possible",
        "Deployed teams to monitor landslide-prone and flood-prone areas",
        "Submitted the PDRA report",
        "Gathered and consolidated reports from cluster heads",
        "Submitted status and situation reports to the province and concerned agencies",
        "Submitted regular SitReps to the PDRRMO",
        "Continued external coordination with neighboring LGUs, the province, and NGAs"
    ]
    
    cpa_within_24hrs_before = [
        "Issued suspension or cancellation of classes and work",
        "Issued fishing bans and other water-related activity restrictions",
        "Issued land travel bans, when necessary",
        "Conducted an MDRRMC meeting on updates to critical preparations",
        "Placed teams on standby and on alert",
        "Announced pre-emptive or voluntary evacuation",
        "Ensured evacuation of people in high-risk areas",
        "Enforced mandatory evacuation, when necessary",
        "Conducted patrols",
        "Ensured unobstructed routes for safe and faster response actions and service delivery",
        "Ensured that warnings and advisories reached communities",
        "Declared a State of Imminent Disaster, when necessary"
    ]
    
    mdrmo_activities = []
    
    for mun in municipalities:
        # Initialize session state for this municipality
        if f"mdrmo_selected_{mun}" not in st.session_state:
            st.session_state[f"mdrmo_selected_{mun}"] = []
        
        # Temporary checkbox state (not saved until button click)
        if f"mdrmo_temp_{mun}" not in st.session_state:
            st.session_state[f"mdrmo_temp_{mun}"] = []
        
        with st.expander(f"🏛️ {mun}", expanded=False):
            st.markdown(f"**{mun} MDRRMO Operations Center**")
            
            # ===== UPON ALERT SECTION =====
            st.markdown("**📋 UPON ALERT**")
            st.caption("Initial actions immediately after receiving alert/warning")
            upon_cols = st.columns(2)
            for idx, activity in enumerate(cpa_upon_alert):
                col_idx = idx % 2
                with upon_cols[col_idx]:
                    is_checked = activity in st.session_state[f"mdrmo_temp_{mun}"]
                    checked = st.checkbox(activity, value=is_checked, key=f"temp_upon_{mun}_{idx}")
                    if checked and activity not in st.session_state[f"mdrmo_temp_{mun}"]:
                        st.session_state[f"mdrmo_temp_{mun}"].append(activity)
                    if not checked and activity in st.session_state[f"mdrmo_temp_{mun}"]:
                        st.session_state[f"mdrmo_temp_{mun}"].remove(activity)
            
            st.markdown("---")
            
            # ===== WITHIN 24 HOURS AFTER ALERT SECTION =====
            st.markdown("**📋 WITHIN 24 HOURS AFTER ALERT**")
            st.caption("Actions taken within 24 hours after alert issuance")
            after_cols = st.columns(2)
            for idx, activity in enumerate(cpa_within_24hrs_after):
                col_idx = idx % 2
                with after_cols[col_idx]:
                    is_checked = activity in st.session_state[f"mdrmo_temp_{mun}"]
                    checked = st.checkbox(activity, value=is_checked, key=f"temp_after_{mun}_{idx}")
                    if checked and activity not in st.session_state[f"mdrmo_temp_{mun}"]:
                        st.session_state[f"mdrmo_temp_{mun}"].append(activity)
                    if not checked and activity in st.session_state[f"mdrmo_temp_{mun}"]:
                        st.session_state[f"mdrmo_temp_{mun}"].remove(activity)
            
            st.markdown("---")
            
            # ===== WITHIN 24 HOURS BEFORE LANDFALL SECTION =====
            st.markdown("**📋 WITHIN 24 HOURS BEFORE LANDFALL**")
            st.caption("Actions taken within 24 hours before expected landfall")
            before_cols = st.columns(2)
            for idx, activity in enumerate(cpa_within_24hrs_before):
                col_idx = idx % 2
                with before_cols[col_idx]:
                    is_checked = activity in st.session_state[f"mdrmo_temp_{mun}"]
                    checked = st.checkbox(activity, value=is_checked, key=f"temp_before_{mun}_{idx}")
                    if checked and activity not in st.session_state[f"mdrmo_temp_{mun}"]:
                        st.session_state[f"mdrmo_temp_{mun}"].append(activity)
                    if not checked and activity in st.session_state[f"mdrmo_temp_{mun}"]:
                        st.session_state[f"mdrmo_temp_{mun}"].remove(activity)
            
            st.markdown("---")
            


    # ============================================================
    # SECTION III: HAZARD IMPACT & RESPONSE
    # ============================================================
    
    st.markdown("""
    <div class="section-header" style="background-color:#e8f4f8;">
        <h3 style="color:#000000; margin:0;">III. HAZARD IMPACT & RESPONSE</h3>
        <p style="margin:5px 0 0 0; color:#333; font-size:14px;">
        <em>This section documents the actual impacts of the hazard, including incidents monitored, agency response status, incoming advisories, damages, 
        resources provided, and needs assessment. It answers the question: 'What has happened and what is being done about it?'</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== 1. INCIDENTS MONITORED =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">1. Incidents Monitored</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>This table tracks all reported incidents per municipality. Users can add, edit, or delete incidents including incident type, casualties, description, and status. 
        This provides a comprehensive log of all incidents during the disaster.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    incident_types = [
        "Select...",
        "🌊 Flood/Flashflood",
        "🏔️ Landslide",
        "🌋 Earthquake",
        "🌀 Tropical Cyclone (Effects)",
        "🔥 Forest/Grass Fire",
        "⚡ Thunderstorm/Lightning",
        "🚗 Vehicular Accident",
        "🏠 Structural Fire",
        "💧 Drowning",
        "🔍 Missing Person",
        "⚰️ Found Cadaver",
        "⚠️ Attempted Suicide",
        "🔫 Armed Conflict/Shooting",
        "🏥 Medical Emergency",
        "📋 Other"
    ]
    
    status_options = ["Ongoing", "Resolved", "Monitoring", "For Turn-over"]
    
    if "incidents_table" not in st.session_state:
        st.session_state.incidents_table = []
    
    if st.session_state.incidents_table:
        for idx, incident in enumerate(st.session_state.incidents_table):
            with st.container(border=True):
                col1, col2, col3, col4, col5 = st.columns([1.5, 2, 1, 1, 0.5])
                with col1:
                    st.markdown(f"**{incident.get('municipality', '')}**")
                with col2:
                    st.markdown(f"*{incident.get('incident_type', '')}*")
                with col3:
                    st.markdown(f"Casualties: {incident.get('dead', 0)}D / {incident.get('injured', 0)}I / {incident.get('missing', 0)}M")
                with col4:
                    st.markdown(f"Status: {incident.get('status', '')}")
                with col5:
                    if st.button("🗑️", key=f"del_incident_{idx}"):
                        st.session_state.incidents_table.pop(idx)
                        st.rerun()
                if incident.get("description"):
                    st.caption(f"📝 {incident.get('description', '')}")
    
    with st.expander("➕ Add Incident Report", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            municipality = st.selectbox("Municipality", municipalities, key="incident_mun")
        with col2:
            incident_type_sel = st.selectbox("Incident Type", incident_types, key="incident_type_sel")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dead = st.number_input("Dead", min_value=0, value=0, key="incident_dead")
        with col2:
            injured = st.number_input("Injured", min_value=0, value=0, key="incident_injured")
        with col3:
            missing = st.number_input("Missing", min_value=0, value=0, key="incident_missing")
        
        description = st.text_area("Description", key="incident_desc", placeholder="Brief description of the incident...")
        status = st.selectbox("Status", status_options, key="incident_status")
        
        if st.button("➕ Add Incident", key="add_incident_btn"):
            if incident_type_sel != "Select...":
                st.session_state.incidents_table.append({
                    "municipality": municipality,
                    "incident_type": incident_type_sel,
                    "dead": dead,
                    "injured": injured,
                    "missing": missing,
                    "description": description,
                    "status": status,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.success(f"Incident added for {municipality}")
                st.rerun()
            else:
                st.warning("Please select an incident type")
    
    if st.session_state.incidents_table:
        total_dead = sum(i.get("dead", 0) for i in st.session_state.incidents_table)
        total_injured = sum(i.get("injured", 0) for i in st.session_state.incidents_table)
        total_missing = sum(i.get("missing", 0) for i in st.session_state.incidents_table)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Dead", total_dead)
        with col2:
            st.metric("Total Injured", total_injured)
        with col3:
            st.metric("Total Missing", total_missing)
    
    st.markdown("---")
    
    # ===== 2. INCOMING ADVISORIES AND DISSEMINATION LOG / RISK COMMUNICATION =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">2. Incoming Advisories and Dissemination Log / Risk Communication</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>This log tracks issuances, directives, and advisories received from warning agencies (OCD, DILG, PAGASA, MGB, PHIVOLCS) and the actions taken to disseminate them 
        to council members and stakeholders. This provides accountability for communication during the response phase.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if "risk_communication_log" not in st.session_state:
        st.session_state.risk_communication_log = []
    
    if st.session_state.risk_communication_log:
        for idx, comm in enumerate(st.session_state.risk_communication_log):
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 0.5])
                with col1:
                    st.markdown(f"**Issuance:** {comm.get('issuance', '')}")
                    st.caption(f"Received: {comm.get('received_date', '')} at {comm.get('received_time', '')}")
                with col2:
                    st.markdown(f"**Actions Taken:** {comm.get('actions_taken', '')}")
                    st.caption(f"Disseminated: {comm.get('disseminated_date', '')} at {comm.get('disseminated_time', '')}")
                with col3:
                    if st.button("🗑️", key=f"del_comm_{idx}"):
                        st.session_state.risk_communication_log.pop(idx)
                        st.rerun()
    
    with st.expander("➕ Log Issuance/Advisory", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            issuance = st.text_input("Issuance/Advisory/Memorandum", key="comm_issuance", placeholder="e.g., Cordillera RDRRMC Memorandum No. 25, s. 2023")
            received_date = st.date_input("Received Date", key="comm_received_date")
            received_time = st.time_input("Received Time", key="comm_received_time")
        with col2:
            actions_taken = st.text_area("Actions Taken", key="comm_actions", height=100, placeholder="e.g., Email sent to PDRRMC Members, SMS blast to MDRRMOs")
            disseminated_date = st.date_input("Disseminated Date", key="comm_disseminated_date")
            disseminated_time = st.time_input("Disseminated Time", key="comm_disseminated_time")
        
        if st.button("➕ Log Entry", key="add_comm_btn"):
            if issuance:
                st.session_state.risk_communication_log.append({
                    "issuance": issuance,
                    "received_date": received_date.strftime("%Y-%m-%d"),
                    "received_time": received_time.strftime("%H:%M"),
                    "actions_taken": actions_taken,
                    "disseminated_date": disseminated_date.strftime("%Y-%m-%d"),
                    "disseminated_time": disseminated_time.strftime("%H:%M")
                })
                st.success("Communication logged")
                st.rerun()
            else:
                st.warning("Please enter issuance/advisory")
    
    st.markdown("---")
    
    # ===== 3. MPDRRMC MEMBER RESPONSE ACTIVITIES =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">3. MPDRRMC Member Response Activities</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>This section tracks the response activities of all MPDRRMC members, including the MPDRRMO Operations Center, 
        10 Municipal DRRM Offices, and other member agencies.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
# ===== START OF SECTION: PART A MPDRRMO CHECKLIST =====

    # ============================================================
    # PART A: MPDRRMO OPERATIONS CENTER - RESPONSE CHECKLIST
    # ============================================================
    
    st.markdown("""
    <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin-bottom:10px;">
        <strong>🏛️ PART A: MPDRRMO Operations Center - Response Checklist</strong>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Select activities completed. Hover over any activity to see required logistics and duty positions. Selected items will be saved in the SITREP.")
    
    # ===== GET CURRENT ALERT LEVEL =====
    # Read the overall_alert value set by the Weather & Alert Status table widget
    # Do NOT assign to st.session_state.overall_alert as it's already a widget key
    current_alert = st.session_state.get("overall_alert", "White")
    
    # Map White/Blue/Red to WHITE/BLUE/RED for display
    alert_mapping = {"White": "WHITE", "Blue": "BLUE", "Red": "RED"}
    current_alert_level = alert_mapping.get(current_alert, "WHITE")
    
    # Store the mapped value for reference (different key, no widget conflict)
    st.session_state.current_alert_level = current_alert_level
    
    alert_badge_color = {"WHITE": "#2ecc71", "BLUE": "#3498db", "RED": "#e74c3c"}
    st.markdown(f"""
    <div style="background-color:{alert_badge_color.get(current_alert_level, '#2ecc71')}; 
                color:white; padding:5px 10px; border-radius:5px; margin-bottom:15px; display:inline-block;">
        🔔 Current Alert Level: {current_alert_level}
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if "mpdrmmo_checklist" not in st.session_state:
        st.session_state.mpdrmmo_checklist = {}
    
    # Define activities
    mpdrmmo_activities_data = {
        # COORDINATION / REPORTING
        "coord_1": {"name": "Maintain duty roster and turnover", "min_alert": "WHITE", "category": "📋 COORDINATION / REPORTING", "logistics": "Duty roster; attendance sheet; turnover log", "duty_positions": "SDO, IT, AS, DD"},
        "coord_2": {"name": "Receive, log, validate, and route incoming reports", "min_alert": "WHITE", "category": "📋 COORDINATION / REPORTING", "logistics": "Logbooks; phones; email; scanner/printer", "duty_positions": "SDO, AS, IT"},
        "coord_3": {"name": "Activate Blue Alert duty team and 24/7 OpCen", "min_alert": "BLUE", "category": "📋 COORDINATION / REPORTING", "logistics": "Alert team roster; shift schedule; duty board", "duty_positions": "SDO, TLA, IT, AS, EO, PRO, DD"},
        "coord_4": {"name": "Facilitate PDRA and emergency meetings", "min_alert": "BLUE", "category": "📋 COORDINATION / REPORTING", "logistics": "Notice of meeting; agenda; attendance sheets", "duty_positions": "SDO, TLA, AS, IT"},
        "coord_5": {"name": "Prepare SitRep section inputs and matrices", "min_alert": "BLUE", "category": "📋 COORDINATION / REPORTING", "logistics": "SitRep template; matrix files; damage tables", "duty_positions": "TLA, ATA, ATB, ATC, EO, AS, IT, PRO"},
        "coord_6": {"name": "Consolidate and submit SitReps and official reports", "min_alert": "BLUE", "category": "📋 COORDINATION / REPORTING", "logistics": "SitRep master file; report tracker; email/SMS", "duty_positions": "TLA, SDO, ATA, ATB, ATC, IT, AS, PRO"},
        # RISK ASSESSMENT
        "risk_1": {"name": "Monitor official advisories and incident feeds", "min_alert": "WHITE", "category": "⚠️ RISK ASSESSMENT", "logistics": "Radio; TV; internet; email; social media", "duty_positions": "SDO, IT, AS"},
        "risk_2": {"name": "Conduct PDRA and assess scenarios", "min_alert": "BLUE", "category": "⚠️ RISK ASSESSMENT", "logistics": "PDRA templates; hazard maps; advisories", "duty_positions": "SDO, TLA, ATA, EO"},
        "risk_3": {"name": "Compile weather bulletin and forecast updates", "min_alert": "BLUE", "category": "⚠️ RISK ASSESSMENT", "logistics": "PAGASA bulletins; weather forecast", "duty_positions": "ATA, IT, AS"},
        # RESOURCE READINESS
        "resource_1": {"name": "Maintain OpCen, ICT, vehicle, and supply readiness", "min_alert": "WHITE", "category": "🔧 RESOURCE READINESS", "logistics": "Computers; internet; vehicle keys; fuel", "duty_positions": "IT, AS, DD"},
        "resource_2": {"name": "Prepare admin and financial support", "min_alert": "BLUE", "category": "🔧 RESOURCE READINESS", "logistics": "Cash advance; vouchers; purchase requests", "duty_positions": "SDO, AS"},
        "resource_3": {"name": "Inventory vehicles, relief stocks, and equipment", "min_alert": "BLUE", "category": "🔧 RESOURCE READINESS", "logistics": "Inventory sheets; vehicle status board", "duty_positions": "SDO, EO, DD, AS"},
        # WARNING AND INFORMATION
        "warning_1": {"name": "Draft and disseminate routine updates", "min_alert": "WHITE", "category": "📢 WARNING AND INFORMATION", "logistics": "SMS credits; official phones; email; website", "duty_positions": "SDO, IT, AS"},
        "warning_2": {"name": "Issue and disseminate alerts and advisories", "min_alert": "BLUE", "category": "📢 WARNING AND INFORMATION", "logistics": "Message templates; SMS; email groups", "duty_positions": "SDO, PRO, IT, AS"},
        # EVACUATION READINESS
        "evac_1": {"name": "Prepare evacuation readiness data and facilities", "min_alert": "BLUE", "category": "🚪 EVACUATION READINESS", "logistics": "Evacuation center list; profiling forms", "duty_positions": "EO, ATA, AS, SDO"},
        "evac_2": {"name": "Announce and implement pre-emptive evacuation", "min_alert": "BLUE", "category": "🚪 EVACUATION READINESS", "logistics": "Evacuation notices; transport list", "duty_positions": "SDO, PRO, EO, ATA, DD"},
    }
    
    # Filter by alert level
    alert_order = {"WHITE": 1, "BLUE": 2, "RED": 3}
    current_order = alert_order.get(current_alert_level, 1)
    
    # Group by category
    categories = {}
    for act_id, act_data in mpdrmmo_activities_data.items():
        if alert_order.get(act_data["min_alert"], 1) <= current_order:
            cat = act_data["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((act_id, act_data))
    
    # Display checkboxes
    for category, activities in categories.items():
        st.markdown(f"**{category}**")
        cols = st.columns(2)
        for idx, (act_id, act_data) in enumerate(activities):
            with cols[idx % 2]:
                key = f"mpdrmmo_{act_id}"
                is_checked = st.session_state.mpdrmmo_checklist.get(key, False)
                tooltip = f"📦 Logistics: {act_data['logistics']}\n\n👥 Duty Positions: {act_data['duty_positions']}"
                checked = st.checkbox(act_data["name"], value=is_checked, key=key, help=tooltip)
                st.session_state.mpdrmmo_checklist[key] = checked
        st.markdown("---")
    
    # ===== SELECTED ACTIVITIES SUMMARY =====
    st.markdown("### ✅ Selected MPDRRMO Activities (Will be saved in SITREP)")
    
    selected_activities = [act_id for act_id, checked in st.session_state.mpdrmmo_checklist.items() if checked]
    
    if selected_activities:
        for act_id in selected_activities:
            # Get the display name from the data
            for aid, adata in mpdrmmo_activities_data.items():
                if f"mpdrmmo_{aid}" == act_id:
                    st.markdown(f"• {adata['name']}")
                    break
    else:
        st.info("No activities selected yet. Check the boxes above to select completed activities.")
    
    # Custom activity
    with st.expander("➕ Add Custom Activity (if not listed above)"):
        col1, col2 = st.columns([4, 1])
        with col1:
            custom_activity = st.text_input("Custom Activity", key="mpdrmmo_custom", placeholder="Enter activity not in the checklist...", label_visibility="collapsed")
        with col2:
            if st.button("➕ Add", key="add_mpdrmmo_custom"):
                if custom_activity:
                    custom_key = f"mpdrmmo_custom_{len(st.session_state.mpdrmmo_checklist)}"
                    st.session_state.mpdrmmo_checklist[custom_key] = True
                    st.success(f"Added: {custom_activity}")
                    st.rerun()
    
    # Reference expander
    with st.expander("📘 Reference: Team Member Codes", expanded=False):
        st.markdown("""
        | Code | Position |
        |------|----------|
        | **SSDO** | Senior Staff Duty Officer |
        | **SDO** | Staff Duty Officer |
        | **TLA** | Team Leader (Alert Team A) |
        | **ATA** | Alert Team A Member |
        | **ATB** | Alert Team B Member |
        | **ATC** | Alert Team C Member |
        | **IT** | IT Support Staff |
        | **AS** | Administrative Support Staff |
        | **EO** | Engineering Officer |
        | **PRO** | Public Relations Officer |
        | **DD** | Duty Driver |
        """)
    
    st.markdown("---")

# ===== END OF SECTION: PART A MPDRRMO CHECKLIST =====
    
# ===== START OF SECTION: PART B MUNICIPAL DRRM OFFICES =====

    # ============================================================
    # PART B: MUNICIPAL DRRM OFFICES (10 Municipalities)
    # ============================================================
    
    st.markdown("""
    <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin-bottom:10px;">
        <strong>🏛️ PART B: MUNICIPAL DRRM OFFICES (10 Municipalities)</strong>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Based on Operation L!sto Framework - Critical Response and Early Recovery Actions. Select activities completed by each municipality. Selected items will be saved in the SITREP.")
    
    # ===== CRITICAL RESPONSE AND EARLY RECOVERY ACTIONS (for Municipal DRRM Offices) =====
    municipal_response_actions = [
        "Conducted RDANA",
        "Conducted an MDRRMC meeting on the LGU situation and emergency response plan",
        "Procured / bought additional relief goods, when needed",
        "Conducted search and rescue, when needed",
        "Coordinated management of the dead and missing, when necessary",
        "Continued monitoring of alerts and advisories",
        "Continued situational reporting / coordination with OPDRRMO",
        "Coordinated status and support needs with OPDRRMO",
        "Consolidated and submitted the RDANA report",
        "Issued suspension of tourism activities",
        "Issued suspension of public transportation operations"
    ]
    
    # Initialize session state for municipal response activities
    if "municipal_response_activities_selected" not in st.session_state:
        st.session_state.municipal_response_activities_selected = {}
    
    # Track data for saving
    municipal_response_data = []
    
    for idx, mun in enumerate(municipalities, start=1):
        with st.expander(f"{idx}. 🏛️ {mun}", expanded=False):
            st.markdown(f"**{mun} MDRRMO - Critical Response and Early Recovery Actions**")
            st.caption("Actions taken within 12 hours after landfall. Select all that apply.")
            
            # Initialize session state for this municipality if not exists
            if mun not in st.session_state.municipal_response_activities_selected:
                st.session_state.municipal_response_activities_selected[mun] = []
            
            # Temporary list for checkboxes
            temp_selected = st.session_state.municipal_response_activities_selected[mun].copy()
            
            # Display checkboxes in 2 columns
            cols = st.columns(2)
            for act_idx, activity in enumerate(municipal_response_actions):
                with cols[act_idx % 2]:
                    is_checked = activity in temp_selected
                    checked = st.checkbox(activity, value=is_checked, key=f"mun_resp_{mun}_{act_idx}")
                    if checked and activity not in temp_selected:
                        temp_selected.append(activity)
                    elif not checked and activity in temp_selected:
                        temp_selected.remove(activity)
            
            st.markdown("---")
            
            # Save button for this municipality
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("💾 Save Selected Activities", key=f"save_mun_resp_{mun}"):
                    st.session_state.municipal_response_activities_selected[mun] = temp_selected.copy()
                    st.success(f"Saved {len(st.session_state.municipal_response_activities_selected[mun])} activities for {mun}")
                    st.rerun()
            with col2:
                st.caption("Click Save to add checked activities to the list below.")
            
            st.markdown("---")
            
            # Display selected activities for this municipality
            st.markdown(f"**✅ Selected Activities for {mun} (Will be saved in SITREP)**")
            if st.session_state.municipal_response_activities_selected[mun]:
                for activity in st.session_state.municipal_response_activities_selected[mun]:
                    st.markdown(f"• {activity}")
            else:
                st.info("No activities selected yet. Check items above and click 'Save Selected Activities'.")
            
            st.markdown("---")
            
            # Add custom activity
            st.markdown("**Add Custom Activity:**")
            col1, col2 = st.columns([4, 1])
            with col1:
                custom_activity = st.text_input("Custom Activity", key=f"mun_custom_{mun}", placeholder="Enter a unique activity not listed above...", label_visibility="collapsed")
            with col2:
                if st.button("➕ Add", key=f"add_mun_custom_{mun}"):
                    if custom_activity and custom_activity not in st.session_state.municipal_response_activities_selected[mun]:
                        st.session_state.municipal_response_activities_selected[mun].append(custom_activity)
                        st.success(f"Added: {custom_activity}")
                        st.rerun()
                    elif custom_activity and custom_activity in st.session_state.municipal_response_activities_selected[mun]:
                        st.warning("This activity is already in the list.")
                    else:
                        st.warning("Please enter an activity.")
            
            st.caption(f"📋 **Total activities saved for {mun}:** {len(st.session_state.municipal_response_activities_selected[mun])}")
    
    # Prepare data for saving
    for mun in municipalities:
        municipal_response_data.append({
            "municipality": mun,
            "activities": st.session_state.municipal_response_activities_selected.get(mun, [])
        })
    
    st.markdown("---")

# ===== END OF SECTION: PART B MUNICIPAL DRRM OFFICES =====
            
    
# ===== START OF SECTION: PART C MEMBER AGENCIES =====

    # ============================================================
    # PART C: OTHER MPDRRMC MEMBER AGENCIES
    # ============================================================
    
    st.markdown("""
    <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin-bottom:10px;">
        <strong>🏢 PART C: OTHER MPDRRMC MEMBER AGENCIES</strong>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Status and activities of member agencies. Add, edit, or delete activities as needed. Selected items will be saved in the SITREP.")
    
    # Initialize agency response list
    if "agency_response_list" not in st.session_state:
        st.session_state.agency_response_list = [
            {"id": 1, "agency": "1. DSWD-SWAD", "status": "Standby", "activities": [], "resources": ""},
            {"id": 2, "agency": "2. Provincial Social Welfare and Development", "status": "Standby", "activities": [], "resources": ""},
            {"id": 3, "agency": "3. MPPPO (PNP)", "status": "Red Alert", "activities": [], "resources": ""},
            {"id": 4, "agency": "4. 1403rd Community Defense Center", "status": "Standby", "activities": [], "resources": ""},
            {"id": 5, "agency": "5. DILG", "status": "Standby", "activities": [], "resources": ""},
            {"id": 6, "agency": "6. Philippine Red Cross (MP Chapter)", "status": "Standby", "activities": [], "resources": ""},
            {"id": 7, "agency": "7. 69th Infantry Battalion", "status": "Standby", "activities": [], "resources": ""},
            {"id": 8, "agency": "8. BFP - Mountain Province", "status": "Red Alert", "activities": [], "resources": ""}
        ]
    
    # Initialize DSWD inventory
    if "dswd_inventory" not in st.session_state:
        st.session_state.dswd_inventory = [
            {"id": 1, "item": "Family Food Packs", "uom": "pack", "satellite": 1090, "lgu": 1416, "total": 2506},
            {"id": 2, "item": "Hygiene Kits", "uom": "kit", "satellite": 98, "lgu": 30, "total": 128},
            {"id": 3, "item": "Family Kits", "uom": "kit", "satellite": 120, "lgu": 30, "total": 150},
            {"id": 4, "item": "Kitchen Kit", "uom": "kit", "satellite": 128, "lgu": 30, "total": 158},
            {"id": 5, "item": "Sleeping Kit", "uom": "kit", "satellite": 124, "lgu": 30, "total": 154},
            {"id": 6, "item": "Malong", "uom": "piece", "satellite": 176, "lgu": 0, "total": 176},
            {"id": 7, "item": "Modular Tent", "uom": "set", "satellite": 22, "lgu": 0, "total": 22},
            {"id": 8, "item": "Laminated Sack", "uom": "rolls", "satellite": 5, "lgu": 0, "total": 5}
        ]
    
    status_options_agency = ["Standby", "Activated", "Deployed", "Demobilized", "Red Alert"]
    
    # Display each agency
    for idx, agency in enumerate(st.session_state.agency_response_list):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 1.5, 0.5])
            with col1:
                st.markdown(f"**{agency.get('agency', '')}**")
            with col2:
                current_status = agency.get('status', 'Standby')
                status_index = status_options_agency.index(current_status) if current_status in status_options_agency else 0
                new_status = st.selectbox("Status", status_options_agency, index=status_index, key=f"agency_status_{idx}")
                agency['status'] = new_status
            with col3:
                if st.button("🗑️ Delete Agency", key=f"del_agency_{idx}"):
                    st.session_state.agency_response_list.pop(idx)
                    st.rerun()
            
            st.markdown("---")
            
            # ===== ACTIVITIES MANAGEMENT (Add, Edit, Delete) =====
            st.markdown("**📋 Activities Conducted:**")
            
            # Initialize activities list if not exists
            if "activities" not in agency:
                agency["activities"] = []
            
            # Display existing activities with edit/delete
            if agency["activities"]:
                st.markdown("**✅ Current Activities (Will be saved in SITREP):**")
                for act_idx, activity in enumerate(agency["activities"]):
                    col1, col2, col3 = st.columns([5, 0.5, 0.5])
                    with col1:
                        edited_activity = st.text_input(
                            f"Activity {act_idx+1}", 
                            value=activity, 
                            key=f"agency_act_{idx}_{act_idx}",
                            label_visibility="collapsed"
                        )
                        if edited_activity != activity:
                            agency["activities"][act_idx] = edited_activity
                            st.rerun()
                    with col2:
                        if st.button("✏️", key=f"edit_agency_act_{idx}_{act_idx}"):
                            pass
                    with col3:
                        if st.button("🗑️", key=f"del_agency_act_{idx}_{act_idx}"):
                            agency["activities"].pop(act_idx)
                            st.rerun()
            else:
                st.info("No activities added yet. Use the form below to add activities.")
            
            st.markdown("---")
            
            # Add new activity
            st.markdown("**➕ Add New Activity:**")
            col1, col2 = st.columns([4, 1])
            with col1:
                new_activity = st.text_input(
                    "New Activity", 
                    key=f"new_agency_act_{idx}", 
                    placeholder="Enter activity description...",
                    label_visibility="collapsed"
                )
            with col2:
                if st.button("➕ Add", key=f"add_agency_act_{idx}"):
                    if new_activity and new_activity not in agency["activities"]:
                        agency["activities"].append(new_activity)
                        st.rerun()
                    elif new_activity and new_activity in agency["activities"]:
                        st.warning("This activity is already in the list.")
                    else:
                        st.warning("Please enter an activity.")
            
            st.markdown("---")
            
            # Resources
            st.markdown("**📦 Resources Provided:**")
            edited_resources = st.text_area(
                "Resources", 
                value=agency.get('resources', ''), 
                key=f"agency_res_{idx}", 
                height=60,
                placeholder="List resources provided by this agency..."
            )
            agency['resources'] = edited_resources
            
            # Special DSWD-SWAD Inventory Table (only for DSWD)
            if agency['agency'] == "1. DSWD-SWAD":
                st.markdown("---")
                st.markdown("**📦 INVENTORY OF PRE-POSITIONED FOOD AND NON-FOOD ITEMS (NFI)**")
                
                # Display inventory table
                inv_to_remove = []
                for inv_idx, inv_item in enumerate(st.session_state.dswd_inventory):
                    col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1.5, 1.5, 1.5, 0.5])
                    with col1:
                        inv_item["item"] = st.text_input("Item", value=inv_item["item"], key=f"inv_item_{inv_item['id']}", label_visibility="collapsed")
                    with col2:
                        inv_item["uom"] = st.text_input("UOM", value=inv_item["uom"], key=f"inv_uom_{inv_item['id']}", label_visibility="collapsed")
                    with col3:
                        inv_item["satellite"] = st.number_input("Satellite", value=inv_item["satellite"], key=f"inv_sat_{inv_item['id']}", label_visibility="collapsed")
                    with col4:
                        inv_item["lgu"] = st.number_input("LGU", value=inv_item["lgu"], key=f"inv_lgu_{inv_item['id']}", label_visibility="collapsed")
                    with col5:
                        inv_item["total"] = inv_item["satellite"] + inv_item["lgu"]
                        st.text_input("Total", value=inv_item["total"], key=f"inv_total_{inv_item['id']}", disabled=True, label_visibility="collapsed")
                    with col6:
                        if st.button("🗑️", key=f"del_inv_{inv_item['id']}"):
                            inv_to_remove.append(inv_idx)
                
                for inv_idx in sorted(inv_to_remove, reverse=True):
                    st.session_state.dswd_inventory.pop(inv_idx)
                    st.rerun()
                
                if st.button("➕ Add Inventory Item", key="add_inv_item"):
                    new_id = max([i["id"] for i in st.session_state.dswd_inventory]) + 1 if st.session_state.dswd_inventory else 1
                    st.session_state.dswd_inventory.append({"id": new_id, "item": "", "uom": "", "satellite": 0, "lgu": 0, "total": 0})
                    st.rerun()
    
    # Add new agency
    with st.expander("➕ Add New Agency", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_agency_name = st.text_input("Agency Name", key="new_agency_name")
            new_agency_status = st.selectbox("Status", status_options_agency, key="new_agency_status")
        with col2:
            new_agency_resources = st.text_input("Resources Provided", key="new_agency_resources")
        
        st.markdown("**Initial Activities (one per line):**")
        new_agency_activities_text = st.text_area("Activities", key="new_agency_activities", height=80, placeholder="Enter activities, one per line...")
        
        if st.button("➕ Add Agency", key="add_agency_btn"):
            if new_agency_name:
                new_id = max([a.get("id", 0) for a in st.session_state.agency_response_list]) + 1 if st.session_state.agency_response_list else 1
                activities_list = [act.strip() for act in new_agency_activities_text.split("\n") if act.strip()]
                st.session_state.agency_response_list.append({
                    "id": new_id,
                    "agency": new_agency_name,
                    "status": new_agency_status,
                    "activities": activities_list if activities_list else [],
                    "resources": new_agency_resources
                })
                st.success(f"Added: {new_agency_name}")
                st.rerun()
            else:
                st.warning("Please enter Agency Name")
    
    st.markdown("---")

# ===== END OF SECTION: PART C MEMBER AGENCIES =====
    
    # ===== 4. STATUS OF LIFELINES =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">4. Status of Lifelines</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>This section reports the operational status of critical lifelines including power, communication, and road networks. It helps identify disruptions 
        in essential services that affect response operations and community well-being.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 4.1 Power & Communication
    st.markdown("**4.1 Power & Communication**")
    st.caption("Source: MDRRMOs, MOPRECO")
    
    # Column headers
    col1, col2, col3 = st.columns([2, 1.5, 2])
    with col1:
        st.markdown("**Municipality**")
    with col2:
        st.markdown("**Power Status**")
    with col3:
        st.markdown("**Communication Status**")
    
    power_data = []
    comm_data = []
    
    for mun in municipalities:
        col1, col2, col3 = st.columns([2, 1.5, 2])
        with col1:
            st.markdown(f"**{mun}**")
        with col2:
            power = st.selectbox("Power", ["", "Normal", "Intermittent", "No Power"], key=f"power_{mun}", label_visibility="collapsed")
            if power:
                power_data.append({"municipality": mun, "status": power})
        with col3:
            comm = st.selectbox("Communication", ["", "Normal", "Intermittent", "No Signal"], key=f"comm_{mun}", label_visibility="collapsed")
            if comm:
                comm_data.append({"municipality": mun, "status": comm})
    
    st.markdown("---")
    
    # 4.2 National Roads & Bridges
    st.markdown("**4.2 National Roads & Bridges**")
    st.caption("Source: MPFDEO & MPSDEO | Based on updated DPWH inventory")
    
    # Pre-populated National Roads based on DPWH inventory
    default_national_roads = [
        # ===== MPFDEO - SECONDARY ROADS =====
        {"id": 1, "name": "Baguio – Bontoc Road (S00504LZ) K0342+(-801) - K0291+560; L: 50.036", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        {"id": 2, "name": "Dantay – Sagada Road (S00509LZ) K0385+(-280) - K0398+103; L: 13.523", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        {"id": 3, "name": "Maba-ay – Abatan Road (S04032LZ) K0356+(-560) - K0367+013; L: 11.573", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        {"id": 4, "name": "Mt. Province – Cagayan via Tabuk – Enrile Road (S00514LZ) K0392+(-332) - K0420+983; L: 29.238", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        {"id": 5, "name": "Mt. Province – Ilocos Sur Road via Tue (S00530LZ) K0387+(-029) - K0418+652; L: 31.567", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        {"id": 6, "name": "Mt. Province – Nueva Viscaya Road (S00513LZ) K0363+(-785) - K0386+255; L: 24.650", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        {"id": 7, "name": "Sagada – Besao – Quirino Road (S04034LZ) K0396+(-140) - K0428+590; L: 32.730", "sections": [], "district": "MPFDEO", "classification": "Secondary"},
        
        # ===== MPFDEO - TERTIARY ROADS =====
        {"id": 8, "name": "Bontoc – Cadre Road (S03996LZ) K0392+(-558) - K0392+628; L: 1.186", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 9, "name": "Eyeb – Motorpool Road (S00516LZ) CH. 0 – CH. 73; L: 0.073", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 10, "name": "Government Center – Cadre Road (S00510LZ) CH. 0 – CH. 150; L: 0.150", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 11, "name": "Junction Talubin – Barlig – Natonin – Paracelis – Calaccad Road (S00534LZ) K0377+(-944) - K0387+008; L: 10.908", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 12, "name": "Mt. Data Access Road (S00305LZ) CH. 0 – CH. 490; L: 0.490", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 13, "name": "Mt. Province – Cervantes, Ilocos Sur Road via Dacudac – Pilipil Road (S04033LZ) CH. 0 – CH. 26646; L: 26.646", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 14, "name": "Mt. Province – Ilocos Sur Road via Kayan Road (S00531LZ) K0398+(-246) - K0400+403; L: 3.017", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 15, "name": "Mt. Province – Ilocos Sur Road via Kayan Road (S00532LZ) K0386+(-034) - K0397+711; L: 11.815", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 16, "name": "Mt. Province – Nueva Viscaya Road (S00512LZ) CH. 0 – CH. 162; L: 0.162", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 17, "name": "Otucan Diversion Road (S00524LZ) K0412+(-071) - K0413+879; L: 1.950", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        {"id": 18, "name": "PC Barracks Road (S00508LZ) CH. 0 – CH. 165; L: 0.165", "sections": [], "district": "MPFDEO", "classification": "Tertiary"},
        
        # ===== MPSDEO - TERTIARY ROADS =====
        {"id": 19, "name": "Bananao Road (S03999LZ) K0467+(-1424) - K0467+648; L: 2.07", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
        {"id": 20, "name": "Jct Talubin – Barlig – Natonin – Paracelis – Calaccad Road (S00593LZ) K0464+(-1177) - K0480+969; L: 103.64", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
        {"id": 21, "name": "Jct Talubin – Barlig – Natonin – Paracelis – Calaccad Road (S00594LZ) K0459+(-336) - K0462+1200; L: 103.64", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
        {"id": 22, "name": "Mt. Province – Ifugao – Kiling – Paracelis Section Road (S00596LZ) K0456+(-694) - K0477+390; L: 22.24", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
        {"id": 23, "name": "Mt. Province – Isabela Road (S00535LZ) K0465+(-1039) - K0489+203; L: 25.63", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
        {"id": 24, "name": "Mt. Province – Isabela Road (S00541LZ)", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
        {"id": 25, "name": "Paracelis – Mallig – Roxas Road (S04031LZ); L: 18.64", "sections": [], "district": "MPSDEO", "classification": "Tertiary"},
    ]
    
    if "national_roads" not in st.session_state:
        st.session_state.national_roads = default_national_roads
    
    # Display roads grouped by district and classification
    with st.expander("Manage National Roads", expanded=False):
        
        # TABLE HEADERS for National Roads
        st.markdown("""
        <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin-bottom:10px;">
            <strong>📋 National Roads Management</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Column headers for the expander content
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 0.5])
        with col1:
            st.markdown("**Road Name / Details**")
        with col2:
            st.markdown("**Road Section**")
        with col3:
            st.markdown("**Traffic Situation**")
        with col4:
            st.markdown("**Actions**")
        with col5:
            st.markdown("**Delete**")
        
        st.markdown("---")
        
        # Filter roads by district
        mpfdeo_secondary = [r for r in st.session_state.national_roads if r.get("district") == "MPFDEO" and r.get("classification") == "Secondary"]
        mpfdeo_tertiary = [r for r in st.session_state.national_roads if r.get("district") == "MPFDEO" and r.get("classification") == "Tertiary"]
        mpsdeo_tertiary = [r for r in st.session_state.national_roads if r.get("district") == "MPSDEO" and r.get("classification") == "Tertiary"]
        
        # Add new national road
        st.markdown("**➕ Add New National Road**")
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            new_road_name = st.text_input("New National Road Name", key="new_national_road_name", placeholder="e.g., New Road Name with code and length")
        with col2:
            new_road_district = st.selectbox("District", ["MPFDEO", "MPSDEO"], key="new_road_district")
        with col3:
            new_road_class = st.selectbox("Classification", ["Secondary", "Tertiary"], key="new_road_classification")
        if st.button("Add National Road", key="add_national_road_btn"):
            if new_road_name:
                new_id = max([r["id"] for r in st.session_state.national_roads]) + 1 if st.session_state.national_roads else 1
                st.session_state.national_roads.append({
                    "id": new_id, 
                    "name": new_road_name, 
                    "sections": [],
                    "district": new_road_district,
                    "classification": new_road_class
                })
                st.success(f"Added: {new_road_name}")
                st.rerun()
        
        st.markdown("---")
        
        # Display MPFDEO Secondary Roads
        if mpfdeo_secondary:
            st.markdown("""
            <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin:15px 0 10px 0;">
                <strong>🏗️ MPFDEO - SECONDARY ROADS</strong>
            </div>
            """, unsafe_allow_html=True)
            
            for road in mpfdeo_secondary:
                with st.expander(f"🛣️ {road['name']}"):
                    # Edit Road Name
                    st.markdown("**✏️ Edit Road Information**")
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        edited_road_name = st.text_input("Road Name / Details", value=road['name'], key=f"edit_nat_road_name_{road['id']}")
                    with col2:
                        if st.button("💾 Save", key=f"save_nat_road_name_{road['id']}"):
                            if edited_road_name:
                                road['name'] = edited_road_name
                                st.success("Road name updated!")
                                st.rerun()
                    with col3:
                        if st.button("🗑️ Delete Road", key=f"del_nat_road_{road['id']}"):
                            st.session_state.national_roads = [r for r in st.session_state.national_roads if r["id"] != road["id"]]
                            st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**📋 Road Sections**")
                    
                    # Section headers
                    col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                    with col1:
                        st.markdown("**Section Name**")
                    with col2:
                        st.markdown("**Traffic Situation**")
                    with col3:
                        st.markdown("**Actions Taken**")
                    with col4:
                        st.markdown("**Delete**")
                    
                    if road["sections"]:
                        for idx, section in enumerate(road["sections"]):
                            col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                            with col1:
                                section_name = st.text_input("", value=section.get("section", ""), key=f"nat_section_{road['id']}_{idx}", label_visibility="collapsed")
                            with col2:
                                traffic = st.selectbox("", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                                      index=["", "Passable", "One Lane Passable", "Not Passable", "Closed"].index(section.get("traffic", "")) if section.get("traffic") in ["", "Passable", "One Lane Passable", "Not Passable", "Closed"] else 0,
                                                      key=f"nat_traffic_{road['id']}_{idx}", label_visibility="collapsed")
                            with col3:
                                actions = st.text_input("", value=section.get("actions", ""), key=f"nat_actions_{road['id']}_{idx}", label_visibility="collapsed")
                            with col4:
                                if st.button("🗑️", key=f"nat_del_section_{road['id']}_{idx}"):
                                    road["sections"].pop(idx)
                                    st.rerun()
                            
                            # Update section data
                            section["section"] = section_name
                            section["traffic"] = traffic
                            section["actions"] = actions
                    
                    # Add new section row
                    col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                    with col1:
                        new_section = st.text_input("New Section Name", key=f"nat_new_section_{road['id']}", placeholder="e.g., Barangay X to Barangay Y", label_visibility="collapsed")
                    with col2:
                        new_traffic = st.selectbox("Traffic Situation", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], index=0, key=f"nat_new_traffic_{road['id']}", label_visibility="collapsed")
                    with col3:
                        new_actions = st.text_input("Actions Taken", key=f"nat_new_actions_{road['id']}", placeholder="e.g., Clearing operations ongoing", label_visibility="collapsed")
                    with col4:
                        if st.button("➕ Add", key=f"nat_add_section_{road['id']}"):
                            if new_section:
                                road["sections"].append({"section": new_section, "traffic": new_traffic, "actions": new_actions})
                                st.rerun()
        
        # Display MPFDEO Tertiary Roads
        if mpfdeo_tertiary:
            st.markdown("""
            <div style="background-color:#34495e; color:white; padding:8px 12px; border-radius:5px; margin:15px 0 10px 0;">
                <strong>🏗️ MPFDEO - TERTIARY ROADS</strong>
            </div>
            """, unsafe_allow_html=True)
            
            for road in mpfdeo_tertiary:
                with st.expander(f"🛣️ {road['name']}"):
                    # Edit Road Name
                    st.markdown("**✏️ Edit Road Information**")
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        edited_road_name = st.text_input("Road Name / Details", value=road['name'], key=f"edit_nat_road_name_{road['id']}")
                    with col2:
                        if st.button("💾 Save", key=f"save_nat_road_name_{road['id']}"):
                            if edited_road_name:
                                road['name'] = edited_road_name
                                st.success("Road name updated!")
                                st.rerun()
                    with col3:
                        if st.button("🗑️ Delete Road", key=f"del_nat_road_{road['id']}"):
                            st.session_state.national_roads = [r for r in st.session_state.national_roads if r["id"] != road["id"]]
                            st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**📋 Road Sections**")
                    
                    # Section headers
                    col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                    with col1:
                        st.markdown("**Section Name**")
                    with col2:
                        st.markdown("**Traffic Situation**")
                    with col3:
                        st.markdown("**Actions Taken**")
                    with col4:
                        st.markdown("**Delete**")
                    
                    if road["sections"]:
                        for idx, section in enumerate(road["sections"]):
                            col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                            with col1:
                                section_name = st.text_input("", value=section.get("section", ""), key=f"nat_section_{road['id']}_{idx}", label_visibility="collapsed")
                            with col2:
                                traffic = st.selectbox("", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                                      index=["", "Passable", "One Lane Passable", "Not Passable", "Closed"].index(section.get("traffic", "")) if section.get("traffic") in ["", "Passable", "One Lane Passable", "Not Passable", "Closed"] else 0,
                                                      key=f"nat_traffic_{road['id']}_{idx}", label_visibility="collapsed")
                            with col3:
                                actions = st.text_input("", value=section.get("actions", ""), key=f"nat_actions_{road['id']}_{idx}", label_visibility="collapsed")
                            with col4:
                                if st.button("🗑️", key=f"nat_del_section_{road['id']}_{idx}"):
                                    road["sections"].pop(idx)
                                    st.rerun()
                            
                            # Update section data
                            section["section"] = section_name
                            section["traffic"] = traffic
                            section["actions"] = actions
                    
                    # Add new section row
                    col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                    with col1:
                        new_section = st.text_input("New Section Name", key=f"nat_new_section_{road['id']}", placeholder="e.g., Barangay X to Barangay Y", label_visibility="collapsed")
                    with col2:
                        new_traffic = st.selectbox("Traffic Situation", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], index=0, key=f"nat_new_traffic_{road['id']}", label_visibility="collapsed")
                    with col3:
                        new_actions = st.text_input("Actions Taken", key=f"nat_new_actions_{road['id']}", placeholder="e.g., Clearing operations ongoing", label_visibility="collapsed")
                    with col4:
                        if st.button("➕ Add", key=f"nat_add_section_{road['id']}"):
                            if new_section:
                                road["sections"].append({"section": new_section, "traffic": new_traffic, "actions": new_actions})
                                st.rerun()
        
        # Display MPSDEO Tertiary Roads
        if mpsdeo_tertiary:
            st.markdown("""
            <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin:15px 0 10px 0;">
                <strong>🏗️ MPSDEO - TERTIARY ROADS</strong>
            </div>
            """, unsafe_allow_html=True)
            
            for road in mpsdeo_tertiary:
                with st.expander(f"🛣️ {road['name']}"):
                    # Edit Road Name
                    st.markdown("**✏️ Edit Road Information**")
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        edited_road_name = st.text_input("Road Name / Details", value=road['name'], key=f"edit_nat_road_name_{road['id']}")
                    with col2:
                        if st.button("💾 Save", key=f"save_nat_road_name_{road['id']}"):
                            if edited_road_name:
                                road['name'] = edited_road_name
                                st.success("Road name updated!")
                                st.rerun()
                    with col3:
                        if st.button("🗑️ Delete Road", key=f"del_nat_road_{road['id']}"):
                            st.session_state.national_roads = [r for r in st.session_state.national_roads if r["id"] != road["id"]]
                            st.rerun()
                    
                    st.markdown("---")
                    st.markdown("**📋 Road Sections**")
                    
                    # Section headers
                    col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                    with col1:
                        st.markdown("**Section Name**")
                    with col2:
                        st.markdown("**Traffic Situation**")
                    with col3:
                        st.markdown("**Actions Taken**")
                    with col4:
                        st.markdown("**Delete**")
                    
                    if road["sections"]:
                        for idx, section in enumerate(road["sections"]):
                            col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                            with col1:
                                section_name = st.text_input("", value=section.get("section", ""), key=f"nat_section_{road['id']}_{idx}", label_visibility="collapsed")
                            with col2:
                                traffic = st.selectbox("", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                                      index=["", "Passable", "One Lane Passable", "Not Passable", "Closed"].index(section.get("traffic", "")) if section.get("traffic") in ["", "Passable", "One Lane Passable", "Not Passable", "Closed"] else 0,
                                                      key=f"nat_traffic_{road['id']}_{idx}", label_visibility="collapsed")
                            with col3:
                                actions = st.text_input("", value=section.get("actions", ""), key=f"nat_actions_{road['id']}_{idx}", label_visibility="collapsed")
                            with col4:
                                if st.button("🗑️", key=f"nat_del_section_{road['id']}_{idx}"):
                                    road["sections"].pop(idx)
                                    st.rerun()
                            
                            # Update section data
                            section["section"] = section_name
                            section["traffic"] = traffic
                            section["actions"] = actions
                    
                    # Add new section row
                    col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                    with col1:
                        new_section = st.text_input("New Section Name", key=f"nat_new_section_{road['id']}", placeholder="e.g., Barangay X to Barangay Y", label_visibility="collapsed")
                    with col2:
                        new_traffic = st.selectbox("Traffic Situation", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], index=0, key=f"nat_new_traffic_{road['id']}", label_visibility="collapsed")
                    with col3:
                        new_actions = st.text_input("Actions Taken", key=f"nat_new_actions_{road['id']}", placeholder="e.g., Clearing operations ongoing", label_visibility="collapsed")
                    with col4:
                        if st.button("➕ Add", key=f"nat_add_section_{road['id']}"):
                            if new_section:
                                road["sections"].append({"section": new_section, "traffic": new_traffic, "actions": new_actions})
                                st.rerun()
    
    st.markdown("---")
        
    # 4.3 Provincial Roads & Bridges
    st.markdown("**4.3 Provincial Roads & Bridges**")
    st.caption("Source: PEO")
    
    default_provincial_roads = [
        {"id": 1, "name": "Abatan – Bagnen", "sections": []},
        {"id": 2, "name": "Balicanao – Am-am", "sections": []},
        {"id": 3, "name": "Boga – Sengyew", "sections": []},
        {"id": 4, "name": "Guinzadan – Banao - Andanum", "sections": []},
        {"id": 5, "name": "Guinzadan – Cagubatan", "sections": []},
        {"id": 6, "name": "Lamagan – Bansa – Mosgok", "sections": []},
        {"id": 7, "name": "Sinto – Mankingao – Pua", "sections": []},
        {"id": 8, "name": "Mt. Data – Binaca – Pitpitan", "sections": []},
        {"id": 9, "name": "Otucan – Bila", "sections": []},
        {"id": 10, "name": "Kurva – Pactil – Pua – Balicanao", "sections": []},
        {"id": 11, "name": "Sadsadan – Balicanao – Salin", "sections": []},
        {"id": 12, "name": "Sadsadan – Sumey-ang – Banata", "sections": []},
        {"id": 13, "name": "Sadsadan – Cuba", "sections": []},
        {"id": 14, "name": "Sinto – Bebe", "sections": []},
        {"id": 15, "name": "Sinto – Lam-ayan", "sections": []},
        {"id": 16, "name": "Bagnen – Balintaugan", "sections": []},
        {"id": 17, "name": "Kin-iway – Agawa", "sections": []},
        {"id": 18, "name": "Kini-iway, Besao – Tubo, Abra Provincial Road", "sections": []},
        {"id": 19, "name": "Bontoc – Mainit", "sections": []},
        {"id": 20, "name": "Bontoc – Maligcong", "sections": []},
        {"id": 21, "name": "Bontoc – Mission", "sections": []},
        {"id": 22, "name": "Caluttit – Hospital", "sections": []},
        {"id": 23, "name": "Plaza – Caluttit", "sections": []},
        {"id": 24, "name": "Talubin – Caneo", "sections": []},
        {"id": 25, "name": "Saliok – Maducayan", "sections": []},
        {"id": 26, "name": "Bacarri – Addang - Tawang", "sections": []},
        {"id": 27, "name": "Abba – Bacarri – Nansuso", "sections": []},
        {"id": 28, "name": "Marat – Babba", "sections": []},
        {"id": 29, "name": "Tapinit – Licoy", "sections": []},
        {"id": 30, "name": "Basilan Road", "sections": []},
        {"id": 31, "name": "Catubangan – Nanolao – Kiling", "sections": []},
        {"id": 32, "name": "Ambango – Data", "sections": []},
        {"id": 33, "name": "Pingad – Gayang", "sections": []},
        {"id": 34, "name": "Sabangan – Ambango – Bagnen", "sections": []},
        {"id": 35, "name": "Tabbac – Kalawitan", "sections": []},
        {"id": 36, "name": "Tabbac – Namatec", "sections": []},
        {"id": 37, "name": "Ampawilen – Sadanga", "sections": []},
        {"id": 38, "name": "Mamaga – Saclit", "sections": []},
        {"id": 39, "name": "Ambasing – Balugan", "sections": []},
        {"id": 40, "name": "Ambasing – Teba-ang – Ampacao", "sections": []},
        {"id": 41, "name": "Pegeo – Tetep-an", "sections": []},
        {"id": 42, "name": "Batalao – Kiltepan", "sections": []},
        {"id": 43, "name": "Antadao – Kilong – Baang", "sections": []},
        {"id": 44, "name": "Taccong – Nacagang", "sections": []},
        {"id": 45, "name": "Madepdepas – Taccong – Balangagan", "sections": []},
        {"id": 46, "name": "Sagada – Bangaan – Aguid", "sections": []},
        {"id": 47, "name": "Balili – Mabisil – Sumaguing", "sections": []},
        {"id": 48, "name": "Mabisil – Suyo", "sections": []},
        {"id": 49, "name": "Asdan – Kayan", "sections": []},
        {"id": 50, "name": "Balili – Pandayan", "sections": []},
        {"id": 51, "name": "Masla – Duagan", "sections": []},
        {"id": 52, "name": "Nacawang – Mabalite", "sections": []},
        {"id": 53, "name": "Tadian – Nacawang Road", "sections": []},
    ]
    
    if "provincial_roads" not in st.session_state:
        st.session_state.provincial_roads = default_provincial_roads
    
    with st.expander("Manage Provincial Roads", expanded=False):
        
        # Table headers
        st.markdown("""
        <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin-bottom:10px;">
            <strong>📋 Provincial Roads Management</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Column headers
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 0.5])
        with col1:
            st.markdown("**Road Name**")
        with col2:
            st.markdown("**Road Section**")
        with col3:
            st.markdown("**Traffic Situation**")
        with col4:
            st.markdown("**Actions**")
        with col5:
            st.markdown("**Delete**")
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_prov_road = st.text_input("New Provincial Road Name", key="new_provincial_road_name")
        with col2:
            if st.button("Add Provincial Road", key="add_provincial_road_btn"):
                if new_prov_road:
                    new_id = max([r["id"] for r in st.session_state.provincial_roads]) + 1 if st.session_state.provincial_roads else 1
                    st.session_state.provincial_roads.append({"id": new_id, "name": new_prov_road, "sections": []})
                    st.success(f"Added: {new_prov_road}")
                    st.rerun()
        
        for road in st.session_state.provincial_roads:
            with st.expander(f"🛣️ {road['name']}"):
                st.markdown("**✏️ Edit Road Information**")
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    edited_road_name = st.text_input("Road Name / Details", value=road['name'], key=f"edit_prov_road_name_{road['id']}")
                with col2:
                    if st.button("💾 Save", key=f"save_prov_road_name_{road['id']}"):
                        if edited_road_name:
                            road['name'] = edited_road_name
                            st.success("Road name updated!")
                            st.rerun()
                with col3:
                    if st.button("🗑️ Delete Road", key=f"del_prov_road_{road['id']}"):
                        st.session_state.provincial_roads = [r for r in st.session_state.provincial_roads if r["id"] != road["id"]]
                        st.rerun()
                
                st.markdown("---")
                st.markdown("**📋 Road Sections**")
                
                # Section headers
                col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                with col1:
                    st.markdown("**Section Name**")
                with col2:
                    st.markdown("**Traffic Situation**")
                with col3:
                    st.markdown("**Actions Taken**")
                with col4:
                    st.markdown("**Delete**")
                
                if road["sections"]:
                    for idx, section in enumerate(road["sections"]):
                        col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                        with col1:
                            section_name = st.text_input("", value=section.get("section", ""), key=f"prov_section_{road['id']}_{idx}", label_visibility="collapsed")
                        with col2:
                            traffic = st.selectbox("", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                                  index=["", "Passable", "One Lane Passable", "Not Passable", "Closed"].index(section.get("traffic", "")) if section.get("traffic") in ["", "Passable", "One Lane Passable", "Not Passable", "Closed"] else 0,
                                                  key=f"prov_traffic_{road['id']}_{idx}", label_visibility="collapsed")
                        with col3:
                            actions = st.text_input("", value=section.get("actions", ""), key=f"prov_actions_{road['id']}_{idx}", label_visibility="collapsed")
                        with col4:
                            if st.button("🗑️", key=f"prov_del_section_{road['id']}_{idx}"):
                                road["sections"].pop(idx)
                                st.rerun()
                        
                        # Update section data
                        section["section"] = section_name
                        section["traffic"] = traffic
                        section["actions"] = actions
                
                # Add new section row
                col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                with col1:
                    new_section = st.text_input("New Section Name", key=f"prov_new_section_{road['id']}", placeholder="e.g., Barangay X to Barangay Y", label_visibility="collapsed")
                with col2:
                    new_traffic = st.selectbox("Traffic Situation", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], index=0, key=f"prov_new_traffic_{road['id']}", label_visibility="collapsed")
                with col3:
                    new_actions = st.text_input("Actions Taken", key=f"prov_new_actions_{road['id']}", placeholder="e.g., Clearing operations ongoing", label_visibility="collapsed")
                with col4:
                    if st.button("➕ Add", key=f"prov_add_section_{road['id']}"):
                        if new_section:
                            road["sections"].append({"section": new_section, "traffic": new_traffic, "actions": new_actions})
                            st.rerun()
    
    st.markdown("---")
    
    # 4.4 Municipal & Barangay Roads
    st.markdown("**4.4 Municipal & Barangay Roads**")
    st.caption("Source: MEO | Add roads and sections as needed")
    
    if "municipal_roads" not in st.session_state:
        st.session_state.municipal_roads = []
    
    with st.expander("Manage Municipal/Barangay Roads", expanded=False):
        
        # Table headers
        st.markdown("""
        <div style="background-color:#2c3e50; color:white; padding:8px 12px; border-radius:5px; margin-bottom:10px;">
            <strong>📋 Municipal/Barangay Roads Management</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Column headers
        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 0.5])
        with col1:
            st.markdown("**Road Name**")
        with col2:
            st.markdown("**Road Section**")
        with col3:
            st.markdown("**Traffic Situation**")
        with col4:
            st.markdown("**Actions**")
        with col5:
            st.markdown("**Delete**")
        
        st.markdown("---")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_mun_road = st.text_input("Municipal/Barangay Road Name", key="new_municipal_road_name")
        with col2:
            if st.button("Add Municipal Road", key="add_municipal_road_btn"):
                if new_mun_road:
                    new_id = max([r["id"] for r in st.session_state.municipal_roads]) + 1 if st.session_state.municipal_roads else 1
                    st.session_state.municipal_roads.append({"id": new_id, "name": new_mun_road, "sections": []})
                    st.success(f"Added: {new_mun_road}")
                    st.rerun()
        
        for road in st.session_state.municipal_roads:
            with st.expander(f"🛣️ {road['name']}"):
                st.markdown("**✏️ Edit Road Information**")
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    edited_road_name = st.text_input("Road Name / Details", value=road['name'], key=f"edit_mun_road_name_{road['id']}")
                with col2:
                    if st.button("💾 Save", key=f"save_mun_road_name_{road['id']}"):
                        if edited_road_name:
                            road['name'] = edited_road_name
                            st.success("Road name updated!")
                            st.rerun()
                with col3:
                    if st.button("🗑️ Delete Road", key=f"del_mun_road_{road['id']}"):
                        st.session_state.municipal_roads = [r for r in st.session_state.municipal_roads if r["id"] != road["id"]]
                        st.rerun()
                
                st.markdown("---")
                st.markdown("**📋 Road Sections**")
                
                # Section headers
                col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                with col1:
                    st.markdown("**Section Name**")
                with col2:
                    st.markdown("**Traffic Situation**")
                with col3:
                    st.markdown("**Actions Taken**")
                with col4:
                    st.markdown("**Delete**")
                
                if road["sections"]:
                    for idx, section in enumerate(road["sections"]):
                        col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                        with col1:
                            section_name = st.text_input("", value=section.get("section", ""), key=f"mun_section_{road['id']}_{idx}", label_visibility="collapsed")
                        with col2:
                            traffic = st.selectbox("", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], 
                                                  index=["", "Passable", "One Lane Passable", "Not Passable", "Closed"].index(section.get("traffic", "")) if section.get("traffic") in ["", "Passable", "One Lane Passable", "Not Passable", "Closed"] else 0,
                                                  key=f"mun_traffic_{road['id']}_{idx}", label_visibility="collapsed")
                        with col3:
                            actions = st.text_input("", value=section.get("actions", ""), key=f"mun_actions_{road['id']}_{idx}", label_visibility="collapsed")
                        with col4:
                            if st.button("🗑️", key=f"mun_del_section_{road['id']}_{idx}"):
                                road["sections"].pop(idx)
                                st.rerun()
                        
                        # Update section data
                        section["section"] = section_name
                        section["traffic"] = traffic
                        section["actions"] = actions
                
                # Add new section row
                col1, col2, col3, col4 = st.columns([2.5, 2, 2.5, 1])
                with col1:
                    new_section = st.text_input("New Section Name", key=f"mun_new_section_{road['id']}", placeholder="e.g., Barangay X to Barangay Y", label_visibility="collapsed")
                with col2:
                    new_traffic = st.selectbox("Traffic Situation", ["", "Passable", "One Lane Passable", "Not Passable", "Closed"], index=0, key=f"mun_new_traffic_{road['id']}", label_visibility="collapsed")
                with col3:
                    new_actions = st.text_input("Actions Taken", key=f"mun_new_actions_{road['id']}", placeholder="e.g., Clearing operations ongoing", label_visibility="collapsed")
                with col4:
                    if st.button("➕ Add", key=f"mun_add_section_{road['id']}"):
                        if new_section:
                            road["sections"].append({"section": new_section, "traffic": new_traffic, "actions": new_actions})
                            st.rerun()
    
    st.markdown("---")
    
    # ===== 5. DISPLACED POPULATION & DAMAGES =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">5. Displaced Population & Damages</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>This section quantifies the impact on population and housing. It tracks families and persons in evacuation centers and outside, as well as damaged houses. 
        This data is critical for resource mobilization.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        families_ec = st.number_input("Families in ECs", min_value=0, value=0, key="families_ec")
        persons_ec = st.number_input("Persons in ECs", min_value=0, value=0, key="persons_ec")
    with col2:
        families_out = st.number_input("Families Outside ECs", min_value=0, value=0, key="families_out")
        persons_out = st.number_input("Persons Outside ECs", min_value=0, value=0, key="persons_out")
    
    col1, col2 = st.columns(2)
    with col1:
        totally_damaged = st.number_input("Totally Damaged Houses", min_value=0, value=0, key="totally_damaged")
        affected_families = st.number_input("Affected Families", min_value=0, value=0, key="affected_families")
    with col2:
        partially_damaged = st.number_input("Partially Damaged Houses", min_value=0, value=0, key="partially_damaged")
        affected_persons = st.number_input("Affected Persons", min_value=0, value=0, key="affected_persons")
    
    st.markdown("---")
    
    # ===== 6. SUMMARY OF DAMAGES (NDRRMC/PDNA COMPLIANT) =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">6. SUMMARY OF DAMAGES</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>Source: MDRRMCs | Consolidated reports from Municipal Disaster Risk Reduction and Management Councils.<br>
        This section follows the NDRRMC/PDNA format for standardized damage assessment and reporting.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize damages data structure (updated with float values)
    if "damages_ndrrmc" not in st.session_state:
        st.session_state.damages_ndrrmc = {
            # Affected Population (integers)
            "affected_barangays": 0,
            "affected_families": 0,
            "affected_persons": 0,
            "displaced_families": 0,
            "displaced_persons": 0,
            "injuries": 0,
            "deaths": 0,
            "partially_damaged_houses": 0,
            "totally_damaged_houses": 0,
            
            # Sector I: Social (floats for currency)
            "sector_social": {
                "partially_damaged_cost": 0.0,
                "totally_damaged_cost": 0.0,
                "sub_total": 0.0
            },
            
            # Sector II: Agriculture
            "sector_agriculture": {
                "assorted_vegetables": {"cost": 0.0, "area": 0.0, "unit": "hectares"},
                "rice": {"cost": 0.0, "area": 0.0, "unit": "hectares"},
                "corn": {"cost": 0.0, "area": 0.0, "unit": "hectares"},
                "sugarcane": {"cost": 0.0, "area": 0.0, "unit": "hectares"},
                "banana": {"cost": 0.0, "area": 0.0, "unit": "hectares"},
                "coffee": {"cost": 0.0, "area": 0.0, "unit": "hectares"},
                "fishery": {"cost": 0.0, "quantity": 0, "unit": "kg"},
                "livestock": {"cost": 0.0, "heads": 0, "unit": "heads"},
                "sub_total": 0.0
            },
            
            # Sector III: Infrastructure (9 Clusters) - all as floats
            "sector_infrastructure": {
                "cluster1_agricultural_infra_a": {
                    "irrigation_cis": 0.0, "rice_fields": 0.0, "rice_granaries": 0.0, "sub_total": 0.0
                },
                "cluster2_agricultural_infra_b": {
                    "farm_animal_shelter": 0.0, "fishpond": 0.0, "sub_total": 0.0
                },
                "cluster3_agricultural_infra_c": {
                    "farm_to_market_roads": 0.0, "footpath_retaining_walls_riprap": 0.0, "sub_total": 0.0
                },
                "cluster4_road_networks": {
                    "national_roads": 0.0, "provincial_roads": 0.0, "municipal_roads": 0.0, "barangay_roads": 0.0, "sub_total": 0.0
                },
                "cluster5_schools": {
                    "elementary": 0.0, "secondary": 0.0, "tertiary": 0.0, "sub_total": 0.0
                },
                "cluster6_health_educational_facilities": {
                    "barangay_health_stations": 0.0, "hospitals_rural_health_units": 0.0, "day_care_centers": 0.0, "sub_total": 0.0
                },
                "cluster7_bridges_flood_controls_drainages": {
                    "foot_bridges": 0.0, "flood_controls": 0.0, "water_drainages": 0.0, "sub_total": 0.0
                },
                "cluster8_municipal_buildings": {
                    "government_buildings": 0.0, "quarantine_facilities": 0.0, "waterworks_system": 0.0, "other_facilities": 0.0, "sub_total": 0.0
                },
                "cluster9_provincial_buildings": {
                    "provincial_government_offices": 0.0, "provincial_commercial_centers": 0.0, "other_provincial_buildings": 0.0, "sub_total": 0.0
                },
                "grand_total": 0.0
            },
            
            # Per Municipality Summary
            "per_municipality": {
                "Barlig": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Bauko": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Besao": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Bontoc": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Natonin": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Paracelis": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Sabangan": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Sadanga": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Sagada": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0},
                "Tadian": {"social": 0.0, "agriculture": 0.0, "infrastructure": 0.0, "total": 0.0}
            },
            
            "report_date": None,
            "report_time": None,
            "narrative_summary": ""
        }
    
    # Display report date/time reference
    col1, col2 = st.columns(2)
    with col1:
        report_date_damages = st.date_input("Report Date", value=date.today(), key="damages_report_date")
    with col2:
        report_time_damages = st.time_input("Report Time", value=datetime.now().time(), key="damages_report_time")
    
    st.session_state.damages_ndrrmc["report_date"] = report_date_damages.strftime("%B %d, %Y")
    st.session_state.damages_ndrrmc["report_time"] = report_time_damages.strftime("%H%MH")
    
    st.markdown("---")
    
    # ===== A. AFFECTED POPULATION =====
    st.markdown("### A. Affected Population")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.session_state.damages_ndrrmc["affected_barangays"] = st.number_input(
            "Total Number of Affected Barangays", min_value=0, value=st.session_state.damages_ndrrmc["affected_barangays"], 
            key="damages_affected_barangays"
        )
        st.session_state.damages_ndrrmc["affected_families"] = st.number_input(
            "Total Number of Affected Families", min_value=0, value=st.session_state.damages_ndrrmc["affected_families"],
            key="damages_affected_families"
        )
        st.session_state.damages_ndrrmc["affected_persons"] = st.number_input(
            "Total Number of Affected Persons", min_value=0, value=st.session_state.damages_ndrrmc["affected_persons"],
            key="damages_affected_persons"
        )
    
    with col2:
        st.session_state.damages_ndrrmc["displaced_families"] = st.number_input(
            "Total Number of Displaced Families (inside and outside ECs)", min_value=0, 
            value=st.session_state.damages_ndrrmc["displaced_families"], key="damages_displaced_families"
        )
        st.session_state.damages_ndrrmc["displaced_persons"] = st.number_input(
            "Total Number of Displaced Persons or Evacuees", min_value=0,
            value=st.session_state.damages_ndrrmc["displaced_persons"], key="damages_displaced_persons"
        )
        st.session_state.damages_ndrrmc["injuries"] = st.number_input(
            "Total Number of Injuries", min_value=0, value=st.session_state.damages_ndrrmc["injuries"],
            key="damages_injuries"
        )
    
    with col3:
        st.session_state.damages_ndrrmc["deaths"] = st.number_input(
            "Total Number of Deaths", min_value=0, value=st.session_state.damages_ndrrmc["deaths"],
            key="damages_deaths"
        )
        st.session_state.damages_ndrrmc["partially_damaged_houses"] = st.number_input(
            "Total Number of Partially Damaged Houses", min_value=0,
            value=st.session_state.damages_ndrrmc["partially_damaged_houses"], key="damages_partially_damaged_houses"
        )
        st.session_state.damages_ndrrmc["totally_damaged_houses"] = st.number_input(
            "Total Number of Totally Damaged Houses", min_value=0,
            value=st.session_state.damages_ndrrmc["totally_damaged_houses"], key="damages_totally_damaged_houses"
        )
    
    st.markdown("---")
    
    # ===== B. SUMMARY OF DAMAGES PER SECTOR =====
    st.markdown("### B. Summary of Damages per Sector")
    
    # ----- SECTOR I: SOCIAL -----
    st.markdown("#### SECTOR I: SOCIAL (Damages to Residential Houses)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        partially_damaged_cost = st.number_input(
            "Partially Damaged (₱)", min_value=0.0, value=float(st.session_state.damages_ndrrmc["sector_social"]["partially_damaged_cost"]),
            step=10000.0, format="%0.2f", key="social_partial_cost"
        )
    with col2:
        totally_damaged_cost = st.number_input(
            "Totally Damaged (₱)", min_value=0.0, value=float(st.session_state.damages_ndrrmc["sector_social"]["totally_damaged_cost"]),
            step=10000.0, format="%0.2f", key="social_total_cost"
        )
    with col3:
        social_sub_total = partially_damaged_cost + totally_damaged_cost
        st.metric("Sub-Total", format_currency(social_sub_total))
    
    st.session_state.damages_ndrrmc["sector_social"]["partially_damaged_cost"] = partially_damaged_cost
    st.session_state.damages_ndrrmc["sector_social"]["totally_damaged_cost"] = totally_damaged_cost
    st.session_state.damages_ndrrmc["sector_social"]["sub_total"] = social_sub_total
    
    # ----- SECTOR II: AGRICULTURE -----
    st.markdown("#### SECTOR II: AGRICULTURE")
    
    with st.expander("🌾 Crops and Livestock Damages", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Assorted Vegetables**")
            veg_area = st.number_input("Area (hectares)", min_value=0.0, step=0.1, format="%.1f",
                                       value=float(st.session_state.damages_ndrrmc["sector_agriculture"]["assorted_vegetables"]["area"]),
                                       key="agri_veg_area")
            veg_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                       value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["assorted_vegetables"]["cost"]),
                                       key="agri_veg_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["assorted_vegetables"] = {"cost": veg_cost, "area": veg_area, "unit": "hectares"}
        
        with col2:
            st.markdown("**Rice**")
            rice_area = st.number_input("Area (hectares)", min_value=0.0, step=0.1, format="%.1f",
                                        value=float(st.session_state.damages_ndrrmc["sector_agriculture"]["rice"]["area"]),
                                        key="agri_rice_area")
            rice_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                        value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["rice"]["cost"]),
                                        key="agri_rice_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["rice"] = {"cost": rice_cost, "area": rice_area, "unit": "hectares"}
        
        with col3:
            st.markdown("**Corn**")
            corn_area = st.number_input("Area (hectares)", min_value=0.0, step=0.1, format="%.1f",
                                        value=float(st.session_state.damages_ndrrmc["sector_agriculture"]["corn"]["area"]),
                                        key="agri_corn_area")
            corn_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                        value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["corn"]["cost"]),
                                        key="agri_corn_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["corn"] = {"cost": corn_cost, "area": corn_area, "unit": "hectares"}
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Sugarcane**")
            sugarcane_area = st.number_input("Area (hectares)", min_value=0.0, step=0.1, format="%.1f",
                                             value=float(st.session_state.damages_ndrrmc["sector_agriculture"]["sugarcane"]["area"]),
                                             key="agri_sugarcane_area")
            sugarcane_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                             value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["sugarcane"]["cost"]),
                                             key="agri_sugarcane_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["sugarcane"] = {"cost": sugarcane_cost, "area": sugarcane_area, "unit": "hectares"}
        
        with col2:
            st.markdown("**Banana**")
            banana_area = st.number_input("Area (hectares)", min_value=0.0, step=0.1, format="%.1f",
                                          value=float(st.session_state.damages_ndrrmc["sector_agriculture"]["banana"]["area"]),
                                          key="agri_banana_area")
            banana_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                          value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["banana"]["cost"]),
                                          key="agri_banana_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["banana"] = {"cost": banana_cost, "area": banana_area, "unit": "hectares"}
        
        with col3:
            st.markdown("**Coffee**")
            coffee_area = st.number_input("Area (hectares)", min_value=0.0, step=0.1, format="%.1f",
                                          value=float(st.session_state.damages_ndrrmc["sector_agriculture"]["coffee"]["area"]),
                                          key="agri_coffee_area")
            coffee_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                          value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["coffee"]["cost"]),
                                          key="agri_coffee_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["coffee"] = {"cost": coffee_cost, "area": coffee_area, "unit": "hectares"}
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Fishery**")
            fishery_qty = st.number_input("Quantity Lost (kg)", min_value=0, step=100,
                                          value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["fishery"]["quantity"]),
                                          key="agri_fishery_qty")
            fishery_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                           value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["fishery"]["cost"]),
                                           key="agri_fishery_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["fishery"] = {"cost": fishery_cost, "quantity": fishery_qty, "unit": "kg"}
        
        with col2:
            st.markdown("**Livestock**")
            livestock_heads = st.number_input("Number of Heads Lost", min_value=0, step=10,
                                              value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["livestock"]["heads"]),
                                              key="agri_livestock_heads")
            livestock_cost = st.number_input("Cost (₱)", min_value=0, step=5000,
                                             value=int(st.session_state.damages_ndrrmc["sector_agriculture"]["livestock"]["cost"]),
                                             key="agri_livestock_cost")
            st.session_state.damages_ndrrmc["sector_agriculture"]["livestock"] = {"cost": livestock_cost, "heads": livestock_heads, "unit": "heads"}
    
    agriculture_sub_total = (
        veg_cost + rice_cost + corn_cost + sugarcane_cost + banana_cost + coffee_cost +
        fishery_cost + livestock_cost
    )
    st.session_state.damages_ndrrmc["sector_agriculture"]["sub_total"] = agriculture_sub_total
    st.metric("SECTOR II Sub-Total", f"₱{agriculture_sub_total:,.2f}")
    
    # ----- SECTOR III: INFRASTRUCTURE -----
    st.markdown("#### SECTOR III: INFRASTRUCTURE")
    
    # Cluster 1
    st.markdown("**Cluster 1: AGRICULTURAL INFRASTRUCTURE - A**")
    col1, col2, col3 = st.columns(3)
    with col1:
        irrigation = st.number_input("Irrigation (CIS) (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                     value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster1_agricultural_infra_a"]["irrigation_cis"]),
                                     key="infra_irrigation")
    with col2:
        rice_fields = st.number_input("Rice Fields (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                      value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster1_agricultural_infra_a"]["rice_fields"]),
                                      key="infra_rice_fields")
    with col3:
        rice_granaries = st.number_input("Rice Granaries (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster1_agricultural_infra_a"]["rice_granaries"]),
                                         key="infra_rice_granaries")
    cluster1_subtotal = irrigation + rice_fields + rice_granaries
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster1_agricultural_infra_a"] = {
        "irrigation_cis": irrigation, "rice_fields": rice_fields, "rice_granaries": rice_granaries, "sub_total": cluster1_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster1_subtotal))
    
    # Cluster 2
    st.markdown("**Cluster 2: AGRICULTURAL INFRASTRUCTURE - B**")
    col1, col2 = st.columns(2)
    with col1:
        farm_animal_shelter = st.number_input("Farm Animal Shelter (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                              value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster2_agricultural_infra_b"]["farm_animal_shelter"]),
                                              key="infra_farm_animal")
    with col2:
        fishpond = st.number_input("Fishpond (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                   value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster2_agricultural_infra_b"]["fishpond"]),
                                   key="infra_fishpond")
    cluster2_subtotal = farm_animal_shelter + fishpond
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster2_agricultural_infra_b"] = {
        "farm_animal_shelter": farm_animal_shelter, "fishpond": fishpond, "sub_total": cluster2_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster2_subtotal))
    
    # Cluster 3
    st.markdown("**Cluster 3: AGRICULTURAL INFRASTRUCTURE - C**")
    col1, col2 = st.columns(2)
    with col1:
        farm_to_market = st.number_input("Farm to Market Roads (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster3_agricultural_infra_c"]["farm_to_market_roads"]),
                                         key="infra_farm_to_market")
    with col2:
        footpath = st.number_input("Footpath/Retaining Walls/Riprap (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                   value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster3_agricultural_infra_c"]["footpath_retaining_walls_riprap"]),
                                   key="infra_footpath")
    cluster3_subtotal = farm_to_market + footpath
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster3_agricultural_infra_c"] = {
        "farm_to_market_roads": farm_to_market, "footpath_retaining_walls_riprap": footpath, "sub_total": cluster3_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster3_subtotal))
    
    # Cluster 4
    st.markdown("**Cluster 4: ROAD NETWORKS**")
    col1, col2 = st.columns(2)
    with col1:
        national_roads = st.number_input("National Roads (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster4_road_networks"]["national_roads"]),
                                         key="infra_national_roads")
        municipal_roads = st.number_input("Municipal Roads (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                          value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster4_road_networks"]["municipal_roads"]),
                                          key="infra_municipal_roads")
    with col2:
        provincial_roads = st.number_input("Provincial Roads (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                           value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster4_road_networks"]["provincial_roads"]),
                                           key="infra_provincial_roads")
        barangay_roads = st.number_input("Barangay Roads / Farm-to-Market Roads (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster4_road_networks"]["barangay_roads"]),
                                         key="infra_barangay_roads")
    cluster4_subtotal = national_roads + provincial_roads + municipal_roads + barangay_roads
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster4_road_networks"] = {
        "national_roads": national_roads, "provincial_roads": provincial_roads,
        "municipal_roads": municipal_roads, "barangay_roads": barangay_roads, "sub_total": cluster4_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster4_subtotal))
    
    # Cluster 5
    st.markdown("**Cluster 5: SCHOOLS**")
    col1, col2, col3 = st.columns(3)
    with col1:
        elementary = st.number_input("Elementary (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                     value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster5_schools"]["elementary"]),
                                     key="infra_elementary")
    with col2:
        secondary = st.number_input("Secondary (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                    value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster5_schools"]["secondary"]),
                                    key="infra_secondary")
    with col3:
        tertiary = st.number_input("Tertiary (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                   value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster5_schools"]["tertiary"]),
                                   key="infra_tertiary")
    cluster5_subtotal = elementary + secondary + tertiary
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster5_schools"] = {
        "elementary": elementary, "secondary": secondary, "tertiary": tertiary, "sub_total": cluster5_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster5_subtotal))
    
    # Cluster 6
    st.markdown("**Cluster 6: HEALTH FACILITIES and EDUCATIONAL FACILITIES**")
    col1, col2, col3 = st.columns(3)
    with col1:
        bhs = st.number_input("Barangay Health Stations (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                              value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster6_health_educational_facilities"]["barangay_health_stations"]),
                              key="infra_bhs")
    with col2:
        hospitals = st.number_input("Hospitals/Rural Health Units (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                    value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster6_health_educational_facilities"]["hospitals_rural_health_units"]),
                                    key="infra_hospitals")
    with col3:
        day_care = st.number_input("Day Care Centers (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                   value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster6_health_educational_facilities"]["day_care_centers"]),
                                   key="infra_day_care")
    cluster6_subtotal = bhs + hospitals + day_care
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster6_health_educational_facilities"] = {
        "barangay_health_stations": bhs, "hospitals_rural_health_units": hospitals,
        "day_care_centers": day_care, "sub_total": cluster6_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster6_subtotal))
    
    # Cluster 7
    st.markdown("**Cluster 7: BRIDGES, FLOOD CONTROLS AND WATER DRAINAGES**")
    col1, col2, col3 = st.columns(3)
    with col1:
        foot_bridges = st.number_input("Foot Bridges (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                       value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster7_bridges_flood_controls_drainages"]["foot_bridges"]),
                                       key="infra_foot_bridges")
    with col2:
        flood_controls = st.number_input("Flood Controls (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster7_bridges_flood_controls_drainages"]["flood_controls"]),
                                         key="infra_flood_controls")
    with col3:
        water_drainages = st.number_input("Water Drainages (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                          value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster7_bridges_flood_controls_drainages"]["water_drainages"]),
                                          key="infra_water_drainages")
    cluster7_subtotal = foot_bridges + flood_controls + water_drainages
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster7_bridges_flood_controls_drainages"] = {
        "foot_bridges": foot_bridges, "flood_controls": flood_controls,
        "water_drainages": water_drainages, "sub_total": cluster7_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster7_subtotal))
    
    # Cluster 8
    st.markdown("**Cluster 8: BUILDING FACILITIES OWNED BY THE MUNICIPAL LOCAL GOVERNMENT UNITS**")
    col1, col2 = st.columns(2)
    with col1:
        govt_buildings = st.number_input("Government Buildings (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster8_municipal_buildings"]["government_buildings"]),
                                         key="infra_muni_govt")
        waterworks = st.number_input("Waterworks System (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                     value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster8_municipal_buildings"]["waterworks_system"]),
                                     key="infra_muni_waterworks")
    with col2:
        quarantine = st.number_input("Quarantine Facilities (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                     value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster8_municipal_buildings"]["quarantine_facilities"]),
                                     key="infra_muni_quarantine")
        other_facilities = st.number_input("Other Facilities (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                           value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster8_municipal_buildings"]["other_facilities"]),
                                           key="infra_muni_other")
    cluster8_subtotal = govt_buildings + quarantine + waterworks + other_facilities
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster8_municipal_buildings"] = {
        "government_buildings": govt_buildings, "quarantine_facilities": quarantine,
        "waterworks_system": waterworks, "other_facilities": other_facilities, "sub_total": cluster8_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster8_subtotal))
    
    # Cluster 9
    st.markdown("**Cluster 9: BUILDING FACILITIES OWNED BY THE PROVINCIAL GOVERNMENT OF MOUNTAIN PROVINCE**")
    col1, col2, col3 = st.columns(3)
    with col1:
        provincial_offices = st.number_input("Provincial Government Office Buildings (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                             value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster9_provincial_buildings"]["provincial_government_offices"]),
                                             key="infra_prov_offices")
    with col2:
        commercial_centers = st.number_input("Provincial Government Commercial Centers (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                             value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster9_provincial_buildings"]["provincial_commercial_centers"]),
                                             key="infra_prov_commercial")
    with col3:
        other_prov_buildings = st.number_input("Other Buildings Owned by the PLGU (₱)", min_value=0.0, step=10000.0, format="%0.2f",
                                               value=float(st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster9_provincial_buildings"]["other_provincial_buildings"]),
                                               key="infra_prov_other")
    cluster9_subtotal = provincial_offices + commercial_centers + other_prov_buildings
    st.session_state.damages_ndrrmc["sector_infrastructure"]["cluster9_provincial_buildings"] = {
        "provincial_government_offices": provincial_offices, "provincial_commercial_centers": commercial_centers,
        "other_provincial_buildings": other_prov_buildings, "sub_total": cluster9_subtotal
    }
    st.metric("Sub-Total", format_currency(cluster9_subtotal))
    
    # Calculate Infrastructure Grand Total
    infrastructure_grand_total = (
        cluster1_subtotal + cluster2_subtotal + cluster3_subtotal + cluster4_subtotal +
        cluster5_subtotal + cluster6_subtotal + cluster7_subtotal + cluster8_subtotal + cluster9_subtotal
    )
    st.session_state.damages_ndrrmc["sector_infrastructure"]["grand_total"] = infrastructure_grand_total
    
    st.markdown("---")
    st.markdown(f"**SECTOR III (Infrastructure) GRAND TOTAL:** {format_currency(infrastructure_grand_total)}")
    
    # ===== C. SUMMARY OF DAMAGES PER CLUSTER =====
    st.markdown("### C. Summary of Damages per Cluster")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("SECTOR I: SOCIAL", f"₱{social_sub_total:,.2f}")
    with col2:
        st.metric("SECTOR II: AGRICULTURE", f"₱{agriculture_sub_total:,.2f}")
    with col3:
        st.metric("SECTOR III: INFRASTRUCTURE", f"₱{infrastructure_grand_total:,.2f}")
    
    total_damages = social_sub_total + agriculture_sub_total + infrastructure_grand_total
    st.markdown(f"### **TOTAL DAMAGES: ₱{total_damages:,.2f}**")
    
    st.markdown("---")
    
    # ===== D. SUMMARY OF DAMAGES PER MUNICIPALITY =====
    st.markdown("### D. Summary of Damages per Municipality per Cluster")
    st.caption("Breakdown of damages by municipality across the three sectors.")
    
    municipalities_list = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
    with col1:
        st.markdown("**MUNICIPALITY**")
    with col2:
        st.markdown("**SOCIAL (₱)**")
    with col3:
        st.markdown("**AGRICULTURE (₱)**")
    with col4:
        st.markdown("**INFRASTRUCTURE (₱)**")
    
    for mun in municipalities_list:
        col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
        with col1:
            st.markdown(f"**{mun}**")
        with col2:
            social_val = st.number_input(f"social_{mun}", min_value=0.0, step=10000.0, format="%0.2f",
                                         value=float(st.session_state.damages_ndrrmc["per_municipality"][mun]["social"]),
                                         key=f"mun_social_{mun}", label_visibility="collapsed")
        with col3:
            agri_val = st.number_input(f"agri_{mun}", min_value=0.0, step=10000.0, format="%0.2f",
                                       value=float(st.session_state.damages_ndrrmc["per_municipality"][mun]["agriculture"]),
                                       key=f"mun_agri_{mun}", label_visibility="collapsed")
        with col4:
            infra_val = st.number_input(f"infra_{mun}", min_value=0.0, step=10000.0, format="%0.2f",
                                        value=float(st.session_state.damages_ndrrmc["per_municipality"][mun]["infrastructure"]),
                                        key=f"mun_infra_{mun}", label_visibility="collapsed")
        
        total_mun = social_val + agri_val + infra_val
        st.session_state.damages_ndrrmc["per_municipality"][mun] = {
            "social": social_val, "agriculture": agri_val, "infrastructure": infra_val, "total": total_mun
        }
    
    st.markdown("---")
    col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
    with col1:
        st.markdown("**TOTAL**")
    with col2:
        total_social = sum(st.session_state.damages_ndrrmc["per_municipality"][m]["social"] for m in municipalities_list)
        st.markdown(f"**{format_currency(total_social)}**")
    with col3:
        total_agri = sum(st.session_state.damages_ndrrmc["per_municipality"][m]["agriculture"] for m in municipalities_list)
        st.markdown(f"**{format_currency(total_agri)}**")
    with col4:
        total_infra_mun = sum(st.session_state.damages_ndrrmc["per_municipality"][m]["infrastructure"] for m in municipalities_list)
        st.markdown(f"**{format_currency(total_infra_mun)}**")
    
    # ===== E. NARRATIVE SUMMARY =====
    st.markdown("### E. Narrative Summary of Damages")
    
    damage_narrative = st.text_area(
        "Consolidated Narrative Report",
        value=st.session_state.damages_ndrrmc.get("narrative_summary", ""),
        height=120,
        placeholder="""Example:
"During the monitoring period, consolidated reports from the Municipal Disaster Risk Reduction and Management Councils provided a glimpse on the extent of the impact as of [DATE]. A total of XX barangays were affected affecting XX families or XX persons. A total of XX families or XX persons were displaced. XX were injured while XX were reported dead.

On damages, a total of XX houses were partially damaged while XX were totally damaged. The agriculture sector suffered the most damage with an estimated cost of Php XX million, affecting XX hectares of rice, corn, and vegetable crops. Infrastructure damage was estimated at Php XX million, with road networks and bridges sustaining the most damage. The total estimated cost of damages is Php XX million." """
    )
    st.session_state.damages_ndrrmc["narrative_summary"] = damage_narrative
    
    st.markdown("---")
    st.caption("📌 Source: MDRRMCs | Data as of {} at {}".format(
        st.session_state.damages_ndrrmc["report_date"] or "N/A",
        st.session_state.damages_ndrrmc["report_time"] or "N/A"
    ))
    
    st.markdown("---")
    
    # ===== 7. IMPACT & NEEDS ASSESSMENT =====
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">7. Impact & Needs Assessment</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>This section provides analysis of the disaster's overall impact on communities, livelihoods, and environment, combined with priority needs assessment. 
        Impact & Needs shall be the basis for the formulation of Recovery & Rehabilitation Plan and for recommending a State of Calamity under RA 10121.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize impact assessment data
    if "impact_needs_assessment" not in st.session_state:
        st.session_state.impact_needs_assessment = {
            "overall_impact": "",
            "affected_sectors": [],
            "priority_needs": [],
            "recovery_recommendations": "",
            "rdana_conducted": False,
            "rdana_date": None,
            "gap_analysis": ""
        }
    
    # RDANA Status
    col1, col2 = st.columns(2)
    with col1:
        rdana_conducted = st.checkbox("RDANA Conducted?", value=st.session_state.impact_needs_assessment.get("rdana_conducted", False), key="rdana_conducted_check")
        st.session_state.impact_needs_assessment["rdana_conducted"] = rdana_conducted
    with col2:
        if rdana_conducted:
            rdana_date = st.date_input("RDANA Date", value=st.session_state.impact_needs_assessment.get("rdana_date") or date.today(), key="rdana_date")
            st.session_state.impact_needs_assessment["rdana_date"] = rdana_date
    
    st.markdown("---")
    
    # Overall Impact Assessment
    st.markdown("**📊 Overall Impact Assessment**")
    impact_assessment = st.text_area(
        "Impact Analysis", 
        value=st.session_state.impact_needs_assessment.get("overall_impact", ""),
        key="impact_assessment", 
        height=150, 
        placeholder="""Describe the overall impact of the disaster:

• Social Impact: Number of affected population, displacement, casualties, health issues, psychosocial impact
• Economic Impact: Damage to livelihoods, agriculture, businesses, infrastructure
• Environmental Impact: Landslides, flooding, erosion, debris
• Institutional Impact: Disruption to government services, schools, health facilities"""
    )
    st.session_state.impact_needs_assessment["overall_impact"] = impact_assessment
    
    st.markdown("---")
    
    # Affected Sectors
    st.markdown("**🏘️ Sectors Significantly Affected**")
    sector_options = [
        "Agriculture/Fisheries", "Commerce/Trade", "Education", "Energy/Power", 
        "Environment/Natural Resources", "Health", "Infrastructure/Public Works", 
        "Livelihood/Employment", "Social Protection", "Tourism", "Transportation", 
        "Water/Sanitation"
    ]
    
    affected_sectors = st.multiselect(
        "Select affected sectors",
        options=sector_options,
        default=st.session_state.impact_needs_assessment.get("affected_sectors", []),
        key="affected_sectors_select"
    )
    st.session_state.impact_needs_assessment["affected_sectors"] = affected_sectors
    
    st.markdown("---")
    
    # Priority Needs
    st.markdown("**🎯 Priority Needs Assessment (By Response Cluster)**")
    
    if "priority_needs_list" not in st.session_state:
        st.session_state.priority_needs_list = st.session_state.impact_needs_assessment.get("priority_needs", [])
    
    if st.session_state.priority_needs_list:
        st.markdown("**Current Priority Needs:**")
        needs_to_remove = []
        for idx, need in enumerate(st.session_state.priority_needs_list):
            with st.container(border=True):
                col1, col2, col3 = st.columns([4, 1, 0.5])
                with col1:
                    st.markdown(f"**Priority {idx+1}:** {need.get('description', '')}")
                    st.caption(f"*Cluster: {need.get('cluster', 'Unassigned')} | Status: {need.get('status', 'Pending')}*")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_need_{idx}"):
                        st.session_state.edit_need_idx = idx
                        st.rerun()
                with col3:
                    if st.button("🗑️", key=f"del_need_{idx}"):
                        needs_to_remove.append(idx)
        
        for idx in sorted(needs_to_remove, reverse=True):
            st.session_state.priority_needs_list.pop(idx)
            st.rerun()
    
    # Add new priority need
    with st.expander("➕ Add Priority Need", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            need_cluster = st.selectbox("Response Cluster", [
                "Food & Non-Food", "Health", "Water & Sanitation", "Shelter", 
                "Protection", "Education", "Livelihood", "Logistics", 
                "Camp Coordination", "Early Recovery"
            ], key="need_cluster")
        with col2:
            need_status = st.selectbox("Status", ["Pending", "Partially Addressed", "Addressed", "For Monitoring"], key="need_status")
        
        need_description = st.text_area("Need Description", key="need_desc", height=80, placeholder="e.g., 5,000 family food packs for displaced families")
        
        if st.button("➕ Add to Priority Needs", key="add_need_btn"):
            if need_description:
                st.session_state.priority_needs_list.append({
                    "cluster": need_cluster,
                    "description": need_description,
                    "status": need_status,
                    "date_identified": datetime.now().strftime("%Y-%m-%d")
                })
                st.session_state.impact_needs_assessment["priority_needs"] = st.session_state.priority_needs_list
                st.success("Priority need added!")
                st.rerun()
            else:
                st.warning("Please provide a need description")
    
    st.markdown("---")
    
    # ===== STATE OF CALAMITY DECLARATION RECOMMENDATION SECTION =====
    st.markdown("### ⚖️ State of Calamity Declaration Recommendation")
    st.caption("Based on RDANA results and NDRRMC Memorandum Order No. 60, s. 2019")
    
    # Severity Assessment
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Severity Assessment Summary**")
        
        severity_level = st.selectbox(
            "Overall Severity Level",
            ["Negligible", "Minor", "Moderate", "Major", "Catastrophic"],
            key="severity_level",
            help="Based on the impact matrix - this feeds into the Declaration Advisor"
        )
        
        composite_score = st.number_input(
            "Composite Weighted Score (0-24+)",
            min_value=0, max_value=50, value=0, step=1,
            key="composite_score",
            help="Calculated from sector matrix: (Severity×2) + Spread + Duration. Score ≥ 20 triggers recommendation."
        )
        
        # Display decision rule based on score
        if composite_score >= 20:
            st.success("✅ Score ≥ 20 - Threshold reached for declaration recommendation")
        elif composite_score >= 15:
            st.warning("⚠️ Score 15-19 - LDRRMC deliberation recommended")
        elif composite_score > 0:
            st.info("ℹ️ Score below 15 - Continue monitoring")
    
    with col2:
        st.markdown("**Critical Triggers Present**")
        critical_triggers = st.multiselect(
            "Select applicable critical triggers",
            [
                "Deaths, missing persons, or multiple serious injuries",
                "Mass displacement or large-scale evacuation",
                "Major roads, bridges, power, water, or communications significantly disrupted",
                "Multiple barangays or communities isolated / inaccessible",
                "Essential services seriously disrupted",
                "Local response capacity insufficient, augmentation needed",
                "Significant damage to housing, livelihoods, agriculture, or public infrastructure"
            ],
            key="critical_triggers",
            help="If any critical trigger is present, immediate LDRRMC deliberation is recommended"
        )
        
        if critical_triggers:
            st.warning(f"⚠️ {len(critical_triggers)} critical trigger(s) identified - Immediate deliberation recommended")
    
    st.markdown("---")
    
    # Declaration Recommendation
    col1, col2 = st.columns(2)
    
    with col1:
        recommend_calamity = st.checkbox(
            "Recommend Declaration of State of Calamity",
            key="recommend_calamity",
            help="Based on RDANA results and NDRRMC guidelines - this feeds into the Declaration Advisor"
        )
    
    with col2:
        if recommend_calamity:
            calamity_justification = st.text_area(
                "Justification / Basis for Recommendation",
                key="calamity_justification",
                height=100,
                placeholder="""Example:
- Composite weighted score: 22
- Critical triggers present: Deaths (2), Mass displacement (500 families)
- Local capacity: Overwhelmed, augmentation requested
- Damage assessment: ₱50M in infrastructure, 1,500 houses damaged"""
            )
    
    # Decision rule reference
    with st.expander("📋 Decision Rules for State of Calamity (Reference)", expanded=False):
        st.markdown("""
        **Based on NDRRMC Memorandum Order No. 60, s. 2019**
        
        | Condition | Recommended Action |
        |-----------|-------------------|
        | Composite score < 15, no critical trigger | No declaration; continue response |
        | Composite score 15-19 | LDRRMC deliberation |
        | Composite score ≥ 20 | **Recommend declaration** |
        | Any critical trigger present | Immediate LDRRMC deliberation |
        
        **Critical Triggers Defined:**
        - Deaths, missing persons, or multiple serious injuries
        - Mass displacement or large-scale evacuation
        - Major lifeline disruption
        - Multiple barangays isolated
        - Local capacity insufficient
        - Significant damage to housing/livelihoods
        
        *For detailed scoring matrix, refer to the Declaration Advisor tab.*
        """)
    
    st.markdown("---")
    
    # Recovery Recommendations
    st.markdown("**🔄 Recovery & Rehabilitation Recommendations**")
    recovery_recommendations = st.text_area(
        "Recommendations for Recovery and Rehabilitation",
        value=st.session_state.impact_needs_assessment.get("recovery_recommendations", ""),
        key="recovery_recs",
        height=120,
        placeholder="""Based on the impact and needs assessment, provide recommendations for:
• Short-term recovery (0-3 months)
• Medium-term rehabilitation (3-6 months)
• Long-term rebuilding and resilience (6+ months)"""
    )
    st.session_state.impact_needs_assessment["recovery_recommendations"] = recovery_recommendations
    
    st.markdown("---")
    
    # Gap Analysis
    st.markdown("**⚠️ Resource Gaps and Constraints**")
    gap_analysis = st.text_area(
        "Identified Gaps, Constraints, and Needed Augmentation",
        value=st.session_state.impact_needs_assessment.get("gap_analysis", ""),
        key="gap_analysis",
        height=100,
        placeholder="""What resources are lacking? What constraints are affecting response?"""
    )
    st.session_state.impact_needs_assessment["gap_analysis"] = gap_analysis
    
    st.markdown("---")
    st.caption("📌 Impact & Needs Assessment shall be the basis for the formulation of Recovery & Rehabilitation Plan and for State of Calamity declaration under RA 10121.")
    
    st.markdown("---")

    # ============================================================
    # SECTION IV: PHOTO DOCUMENTATION
    # ============================================================
    
    st.markdown("""
    <div class="section-header" style="background-color:#e8f4f8;">
        <h3 style="color:#000000; margin:0;">IV. PHOTO DOCUMENTATION</h3>
        <p style="margin:5px 0 0 0; color:#333; font-size:14px;">
        <em>This section contains visual documentation of incidents, response operations, and damage assessment. Photos provide critical evidence for post-disaster analysis, 
        reporting, and resource mobilization.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="subsection-header" style="background-color:#d4edda;">
        <h4 style="color:#000000; margin:0;">1. Incident and Response Photos</h4>
        <p style="margin:5px 0 0 0; color:#333; font-size:13px;">
        <em>Upload photos of incidents, response operations, and damage assessment. Each photo should include a descriptive caption. Supported formats: JPG, JPEG, PNG.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize photos list in session state
    if "photos_list" not in st.session_state:
        st.session_state.photos_list = [{"id": 1, "photo": None, "caption": ""}]
    
    # Display existing photos
    photos_to_remove = []
    for photo_item in st.session_state.photos_list:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 0.5])
            with col1:
                photo = st.file_uploader(f"Photo", type=["jpg", "jpeg", "png"], key=f"photo_{photo_item['id']}", label_visibility="collapsed")
                if photo:
                    photo_item["photo"] = photo
            with col2:
                caption = st.text_input(f"Caption", key=f"caption_{photo_item['id']}", label_visibility="collapsed")
                if caption:
                    photo_item["caption"] = caption
            with col3:
                if st.button("🗑️", key=f"del_photo_{photo_item['id']}"):
                    photos_to_remove.append(photo_item["id"])
            st.markdown("---")
    
    # Remove marked photos
    for photo_id in photos_to_remove:
        st.session_state.photos_list = [p for p in st.session_state.photos_list if p["id"] != photo_id]
        st.rerun()
    
    # Add photo button
    if st.button("➕ Add Another Photo"):
        new_id = max([p["id"] for p in st.session_state.photos_list]) + 1 if st.session_state.photos_list else 1
        st.session_state.photos_list.append({"id": new_id, "photo": None, "caption": ""})
        st.rerun()
    
    # Prepare photos for saving
    photos = []
    for photo_item in st.session_state.photos_list:
        if photo_item.get("photo") is not None:
            photos.append({"file": photo_item["photo"].name, "caption": photo_item.get("caption", "")})
    
    st.markdown("---")

    # ===== SAVE BUTTON =====
    with st.form("sitrep_form_final", clear_on_submit=False):
        submitted = st.form_submit_button("💾 Save Situation Report", type="primary", use_container_width=True)
        
        if submitted:
            # ============================================================
            # PREPARE ACTIVITIES FOR SAVING
            # ============================================================
            
            mdrmo_activities_save = []
            for ma in mdrmo_activities:
                mdrmo_activities_save.append({
                    "municipality": ma["municipality"],
                    "activities": "\n".join([f"• {a}" for a in ma["activities"]]) if ma["activities"] else "No activities reported"
                })
            
            # Get damages data
            damages_data = st.session_state.get("damages_ndrrmc", {})
            
            # ============================================================
            # COLLECT SELECTED CPA AND ANTICIPATED NEEDS DATA
            # ============================================================
            
            selected_upon_alert = st.session_state.get("selected_upon_alert", [])
            selected_within_24hrs = st.session_state.get("selected_within_24hrs", [])
            selected_before_landfall = st.session_state.get("selected_before_landfall", [])
            selected_anticipated_needs = st.session_state.get("selected_anticipated_needs", [])
            duty_officers_text = st.session_state.get("duty_officers", "")
            
            # ============================================================
            # DECLARATION RECOMMENDATIONS
            # ============================================================
            
            imminent_declaration = {
                "recommend": st.session_state.get("pdra_recommend_imminent", False),
                "justification": st.session_state.get("pdra_imminent_justification", "")
            }
            
            calamity_declaration = {
                "severity_level": st.session_state.get("severity_level", ""),
                "composite_score": st.session_state.get("composite_score", 0),
                "critical_triggers": st.session_state.get("critical_triggers", []),
                "recommend": st.session_state.get("recommend_calamity", False),
                "justification": st.session_state.get("calamity_justification", "")
            }
            
            # ============================================================
            # PART A: MPDRRMO RESPONSE CHECKLIST
            # ============================================================
            
            mpdrmmo_checklist = st.session_state.get("mpdrmmo_checklist", {})
            current_alert_part_a = st.session_state.get("overall_alert", "White")
            alert_mapping_part_a = {"White": "WHITE", "Blue": "BLUE", "Red": "RED"}
            current_alert_level_part_a = alert_mapping_part_a.get(current_alert_part_a, "WHITE")
            completed_activities = [k.replace("mpdrmmo_", "") for k, v in mpdrmmo_checklist.items() if v]
            mpdrmmo_checklist_data = {
                "alert_level": current_alert_level_part_a,
                "completed_count": len(completed_activities),
                "completed_activities": completed_activities,
                "all_checkboxes": mpdrmmo_checklist
            }
            
            # ============================================================
            # BUILD SITREP DICTIONARY
            # ============================================================
            
            sitrep = {
                "id": int(datetime.now().timestamp() * 1000),
                "for_name": st.session_state.for_name,
                "for_title": st.session_state.for_title,
                "thru_name": st.session_state.thru_name,
                "thru_title": st.session_state.thru_title,
                "from_name": st.session_state.from_name,
                "from_title": st.session_state.from_title,
                "sitrep_number": sitrep_number,
                "incident_name": incident_name,
                "hazard_type": st.session_state.selected_hazard_type,
                "report_date": report_date.isoformat(),
                "report_time": report_time.strftime("%H:%M"),
                "overall_alert": overall_alert,
                "weather_bulletin": bulletin_text,
                "bulletin_no": st.session_state.get("tc_bulletin_no", ""),
                "issue_time": st.session_state.get("tc_issue_time", ""),
                "location_center": st.session_state.get("tc_location_center", ""),
                "intensity": st.session_state.get("tc_intensity", ""),
                "present_movement": st.session_state.get("tc_present_movement", ""),
                "extent_winds": st.session_state.get("tc_extent_winds", ""),
                "track_outlook": st.session_state.get("tc_track_outlook", ""),
                "tcws": st.session_state.get("tc_tcws", ""),
                "synopsis": st.session_state.get("wf_synopsis", ""),
                "forecast_weather": st.session_state.get("wf_forecast_weather", ""),
                "temp_min": st.session_state.get("wf_temp_min", ""),
                "temp_max": st.session_state.get("wf_temp_max", ""),
                "wind_speed_forecast": st.session_state.get("wf_wind_speed", ""),
                "wind_direction": st.session_state.get("wf_wind_direction", ""),
                "rainfall_warning": st.session_state.get("wf_rainfall_warning", ""),
                "weather_data": weather_data,
                "incidents_table": st.session_state.incidents_table,
                "risk_communication_log": st.session_state.risk_communication_log,
                "municipal_response_activities": municipal_response_data,
                "agency_response_list": st.session_state.agency_response_list,
                "dswd_inventory": st.session_state.dswd_inventory,
                "mdrmo_activities": mdrmo_activities_save,
                "power_data": power_data,
                "comm_data": comm_data,
                "national_roads": st.session_state.national_roads,
                "provincial_roads": st.session_state.provincial_roads,
                "municipal_roads": st.session_state.municipal_roads,
                
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
                
                "damages_ndrrmc": damages_data,
                
                "impact_assessment": st.session_state.impact_needs_assessment.get("overall_impact", ""),
                "needs_summary": {
                    "priority_needs": st.session_state.get("priority_needs_list", []),
                    "recovery_recommendations": st.session_state.impact_needs_assessment.get("recovery_recommendations", ""),
                    "gap_analysis": st.session_state.impact_needs_assessment.get("gap_analysis", ""),
                    "affected_sectors": st.session_state.impact_needs_assessment.get("affected_sectors", []),
                    "rdana_conducted": st.session_state.impact_needs_assessment.get("rdana_conducted", False),
                    "rdana_date": str(st.session_state.impact_needs_assessment.get("rdana_date", "")) if st.session_state.impact_needs_assessment.get("rdana_date") else ""
                },
                
                # Selected CPAs and Anticipated Needs
                "selected_upon_alert_cpas": selected_upon_alert,
                "selected_within_24hrs_cpas": selected_within_24hrs,
                "selected_before_landfall_cpas": selected_before_landfall,
                "selected_anticipated_needs": selected_anticipated_needs,
                "duty_officers_text": duty_officers_text,
                
                "imminent_declaration": imminent_declaration,
                "calamity_declaration": calamity_declaration,
                "mpdrmmo_checklist": mpdrmmo_checklist_data,
                
                "photos": photos,
                
                "pdra_conducted_date": str(st.session_state.get("pdra_conducted_date", "")),
                "pdra_conducted_time": str(st.session_state.get("pdra_conducted_time", "")),
                "pdra_cpa_level": st.session_state.get("pdra_cpa_level", ""),
                "pdra_actions_list": st.session_state.get("pdra_actions_list", []),
                "pdra_imminent_declared": st.session_state.get("pdra_imminent_declared", False),
                "pdra_optional_notes": st.session_state.get("pdra_optional_notes", ""),
                
                "created_at": datetime.now().isoformat()
            }
            
            save_sitrep_to_local(sitrep)
            save_sitrep_to_cloud(sitrep)
            st.success("✅ Situation Report saved!")
            st.balloons()
            st.rerun()

# ============================================================
# MAIN SHOW FUNCTION
# ============================================================

def show():
    """Display Situation Report Form with PDR Assessment (PDRA) sub-tab"""

    st.markdown("# 📡 SITUATION REPORT")
    st.caption("MPDRRMC Situation Report (SITREP)")

    if "provincial_sitreps" not in st.session_state:
        st.session_state.provincial_sitreps = []

    load_sitreps_from_cloud()

    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Situation Report Form",
        "📋 PDR Assessment",
        "📋 Archived Reports",
        "📊 Predictive Analysis",
        "📧 Email Recipients",
        "⚙️ Auto-Submit Settings"
    ])

    with tab1:
        show_provincial_sitrep_form()
    with tab2:
        show_pdr_assessment()
    with tab3:
        show_archived_sitreps()
    with tab4:
        show_predictive_analysis()
    with tab5:
        show_email_recipients()
    with tab6:
        show_auto_submit_settings()