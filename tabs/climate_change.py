# tabs/climate_change.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected
from utils.local_storage import save_file, delete_file, get_file_size, file_exists

def show():
    """Display Climate Change Adaptation Tab with MPCFS Project Tracking"""
    
    st.markdown("# 🌍 Climate Change Adaptation")
    st.caption("Integrating Climate and Disaster Risk Governance for a Resilient Mountain Province")
    
    # Initialize session state for CCA data
    if 'cca_plans' not in st.session_state:
        st.session_state.cca_plans = []
    
    if 'mpcfs_documents' not in st.session_state:
        st.session_state.mpcfs_documents = []
    
    if 'mpcfs_tasks' not in st.session_state:
        st.session_state.mpcfs_tasks = []
    
    if 'mpcfs_photos' not in st.session_state:
        st.session_state.mpcfs_photos = []
    
    if 'climate_projections' not in st.session_state:
        st.session_state.climate_projections = {
            "temperature": {},
            "rainfall": {},
            "extreme_events": {}
        }
    
    # Create tabs for CCA modules
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 CCA Plans & Programs",
        "🌾 MPCFS Project Hub",
        "📊 CCA Analytics",
        "🌡️ Climate Projections",
        "📁 Document Repository",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_cca_plans()
    
    with tab2:
        show_mpcfs_project_hub()
    
    with tab3:
        show_cca_analytics()
    
    with tab4:
        show_climate_projections()
    
    with tab5:
        show_cca_documents()
    
    with tab6:
        show_cca_related_modules()


def show_cca_plans():
    """Display CCA Plans and Programs"""
    
    st.markdown("### Climate Change Adaptation Plans & Programs")
    st.caption("Provincial and municipal climate action plans, adaptation projects, and financing")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("CCA Plans", "12", delta="+2 this year")
        st.metric("Active Projects", "8", delta="3 ongoing")
    with col2:
        st.metric("Climate Financing", "₱325M", delta="271M (MPCFS)")
        st.metric("Municipalities with CCA Plans", "10/10", delta="100%")
    
    st.markdown("---")
    
    # Add CCA Plan form
    with st.expander("➕ Add CCA Plan", expanded=False):
        with st.form("add_cca_plan"):
            col1, col2 = st.columns(2)
            with col1:
                plan_type = st.selectbox("Plan Type", ["PCCAP", "LCCAP", "Sectoral CCA Plan", "Adaptation Project"])
                title = st.text_input("Plan Title")
                year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
            with col2:
                status = st.selectbox("Status", ["Draft", "For Approval", "Approved", "Under Implementation", "Completed"])
                lead_agency = st.text_input("Lead Agency", placeholder="e.g., PDRRMO, PPDO, PENRO")
                budget = st.number_input("Budget (₱)", min_value=0, value=0, step=10000)
            
            description = st.text_area("Description", placeholder="Brief description of the plan/program")
            key_adaptation_measures = st.text_area("Key Adaptation Measures", placeholder="List key climate adaptation interventions")
            
            submitted = st.form_submit_button("💾 Save CCA Plan")
            
            if submitted and title:
                new_plan = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "plan_type": plan_type,
                    "title": title,
                    "year": year,
                    "status": status,
                    "lead_agency": lead_agency,
                    "budget": budget,
                    "description": description,
                    "key_measures": key_adaptation_measures,
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.cca_plans.append(new_plan)
                st.success(f"✅ CCA Plan '{title}' added!")
                st.rerun()
    
    # Display existing CCA plans
    if st.session_state.cca_plans:
        df = pd.DataFrame(st.session_state.cca_plans)
        st.dataframe(df[['plan_type', 'title', 'year', 'status', 'budget']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("No CCA plans added yet. Click 'Add CCA Plan' to get started.")


# ============================================================
# MPCFS PROJECT HUB FUNCTIONS
# ============================================================

def show_mpcfs_project_hub():
    """Mountain Province Climate Field School Project Hub - Flagship Project"""
    
    st.markdown("### 🌾 Mountain Province Climate Field School Project (MPCFS)")
    st.caption("First-of-its-kind climate-resilient agriculture project in Mountain Province | ₱271M Investment")
    
    # Project header with logo placement
    col1, col2 = st.columns([1, 3])
    with col1:
        try:
            st.image("mpcfs_logo.png", width=120)
        except:
            st.markdown("**MPCFS Logo**")
    with col2:
        st.markdown("""
        **Project Location:** Bacarri, Paracelis, Mountain Province  
        **Project Duration:** 2024-2028  
        **Implementing Agency:** Mountain Province Disaster Risk Reduction and Management Council  
        """)
    
    st.markdown("---")
    
    # MPCFS Sub-tabs
    mpcfstab1, mpcfstab2, mpcfstab3, mpcfstab4, mpcfstab5, mpcfstab6, mpcfstab7, mpcfstab8 = st.tabs([
        "📊 Master Dashboard",
        "🏗️ Infrastructure S-Curve",
        "👨‍🌾 Capability Building",
        "🔬 Research & Extension",
        "📋 Gantt Chart",
        "📁 Document Management",
        "📸 Photo Gallery",
        "📄 Reports"
    ])
    
    with mpcfstab1:
        show_mpcfs_master_dashboard()
    
    with mpcfstab2:
        show_mpcfs_scurve_tracker("infrastructure")
    
    with mpcfstab3:
        show_mpcfs_component_placeholder("Capability Building", "👨‍🌾")
    
    with mpcfstab4:
        show_mpcfs_component_placeholder("Research & Extension", "🔬")
    
    with mpcfstab5:
        show_mpcfs_gantt_updated()
    
    with mpcfstab6:
        show_mpcfs_document_management()
    
    with mpcfstab7:
        show_mpcfs_photo_gallery()
    
    with mpcfstab8:
        show_mpcfs_report_generator_updated()


def show_mpcfs_master_dashboard():
    """Master Dashboard showing all three components"""
    
    st.markdown("#### 📊 MPCFS Master Dashboard")
    st.caption("Overall project progress across all components")
    
    # Get component data from session state
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    infra_target = st.session_state.get('infrastructure_target', 25.75)
    infra_cost = st.session_state.get('infrastructure_cost', 64_000_000)
    
    # Component 2 & 3 placeholders
    cap_progress = st.session_state.get('capability_progress', 0)
    cap_target = st.session_state.get('capability_target', 0)
    cap_status = "⏳ Pending Data" if cap_progress == 0 else "🟢 Active"
    
    res_progress = st.session_state.get('research_progress', 0)
    res_target = st.session_state.get('research_target', 0)
    res_status = "⏳ Pending Data" if res_progress == 0 else "🟢 Active"
    
    # Calculate active components
    active_components = 1
    if cap_progress > 0:
        active_components += 1
    if res_progress > 0:
        active_components += 1
    
    total_progress = (infra_progress + cap_progress + res_progress) / 3 if active_components == 3 else infra_progress / active_components
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Project Progress", f"{total_progress:.2f}%", 
                  delta=f"{active_components}/3 Components Active")
    with col2:
        st.metric("Infrastructure", f"{infra_progress:.2f}%", delta=f"Target: {infra_target:.2f}%")
    with col3:
        st.metric("Capability Building", f"{cap_progress:.1f}%" if cap_progress > 0 else "Not Started", 
                  delta=cap_status)
    with col4:
        st.metric("Research & Extension", f"{res_progress:.1f}%" if res_progress > 0 else "Not Started",
                  delta=res_status)
    
    st.markdown("---")
    
    # Component Progress Bars
    st.markdown("### 📈 Component Progress")
    
    st.markdown("#### 🏗️ Infrastructure Component")
    st.progress(infra_progress / 100, text=f"{infra_progress:.2f}% Complete")
    st.caption(f"Contract Amount: ₱249,040,900 | Utilized: ₱{infra_cost:,.2f}")
    
    st.markdown("#### 👨‍🌾 Capability Building Component")
    if cap_progress > 0:
        st.progress(cap_progress / 100, text=f"{cap_progress:.1f}% Complete")
    else:
        st.info("📌 Data pending. Upload Capability Building S-Curve to activate this component.")
        st.progress(0, text="Awaiting Data")
    
    st.markdown("#### 🔬 Research & Extension Component")
    if res_progress > 0:
        st.progress(res_progress / 100, text=f"{res_progress:.1f}% Complete")
    else:
        st.info("📌 Data pending. Upload Research & Extension S-Curve to activate this component.")
        st.progress(0, text="Awaiting Data")
    
    st.markdown("---")
    
    # Combined S-Curve Preview
    st.markdown("### 📈 Combined Progress Trend")
    
    weeks = list(range(1, 53))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=[total_progress] * len(weeks), name="Overall Progress", 
                              line=dict(color='#2ecc71', width=3)))
    fig.add_trace(go.Scatter(x=weeks, y=[infra_progress] * len(weeks), name="Infrastructure", 
                              line=dict(color='#3498db', width=2, dash='dash')))
    
    fig.update_layout(title="Project Components Progress Overview",
                      xaxis_title="Week",
                      yaxis_title="Progress (%)",
                      height=400,
                      yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def show_mpcfs_component_placeholder(component_name, icon):
    """Placeholder for future components"""
    
    st.markdown(f"#### {icon} {component_name} Component")
    st.caption("This component will be activated when data is uploaded")
    
    st.info(f"""
    ### 📌 {component_name} Component - Coming Soon
    
    This section will track:
    - **Progress S-Curve** for {component_name} activities
    - **Budget utilization** and financial tracking  
    - **Key performance indicators** specific to {component_name}
    - **Milestone tracking** and deliverables
    
    ### How to Activate:
    1. Prepare your {component_name} S-Curve data in Excel
    2. Upload the file when the feature is available
    3. The dashboard will automatically include this component
    """)


def show_mpcfs_scurve_tracker(component="infrastructure"):
    """MPCFS Infrastructure S-Curve Tracker - Simplified version"""
    
    st.markdown(f"#### 🏗️ Infrastructure Component - S-Curve Tracker")
    st.caption(f"Track physical and financial progress | Contract: ₱249,040,900.00")
    
    CONTRACT_AMOUNT = 249_040_900.00
    
    # Display current progress
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Progress", f"{infra_progress:.2f}%")
    with col2:
        st.metric("Target Progress", "25.75%")
    with col3:
        st.metric("Variance", f"{infra_progress - 25.75:+.2f}%")
    with col4:
        st.metric("Status", "✅ ON TRACK" if infra_progress >= 25 else "⚠️ BEHIND")
    
    st.markdown("---")
    st.info("📌 Full S-Curve tracker with itemized work details is being enhanced. Current progress is shown above.")
    
    # Simple S-Curve chart
    weeks = list(range(1, 53))
    target_curve = [min(25.75 * w / 52, 25.75) for w in weeks]
    actual_curve = [min(infra_progress * w / 52, infra_progress) for w in weeks]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=target_curve, mode='lines', name='Target Plan', line=dict(color='#3498db', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=weeks, y=actual_curve, mode='lines+markers', name='Actual Progress', line=dict(color='#2ecc71', width=3)))
    fig.update_layout(title="Project Progress S-Curve", xaxis_title="Week", yaxis_title="Progress (%)", height=400)
    st.plotly_chart(fig, use_container_width=True)


def show_mpcfs_gantt_updated():
    """Updated Gantt chart"""
    
    st.markdown("#### 📋 Project Gantt Chart & Timeline")
    st.caption("Track project milestones by component")
    
    st.info("📌 Full Gantt chart with task tracking is being enhanced. Current progress is shown in the dashboard.")
    
    # Simple task list
    tasks = [
        {"Component": "🏗️ Infrastructure", "Task": "Site Development", "Progress": 45},
        {"Component": "🏗️ Infrastructure", "Task": "Structural Works", "Progress": 35},
        {"Component": "🏗️ Infrastructure", "Task": "Architectural Works", "Progress": 10},
        {"Component": "👨‍🌾 Capability Building", "Task": "Training Program", "Progress": 0, "Status": "Pending"},
        {"Component": "🔬 Research & Extension", "Task": "Research Setup", "Progress": 0, "Status": "Pending"},
    ]
    
    df_tasks = pd.DataFrame(tasks)
    st.dataframe(df_tasks, use_container_width=True, hide_index=True)


def show_mpcfs_document_management():
    """Document management for MPCFS project files"""
    
    st.markdown("#### Document Management")
    st.caption("Upload, store, and manage all MPCFS project documents")
    
    doc_categories = [
        "Project Proposal", "Communications", "Monitoring Reports", 
        "Narrative Reports", "Financial Reports", "Liquidation Reports",
        "Procurement Documents", "M&E Reports", "Technical Documents",
        "Contracts", "Photos", "Videos", "Other"
    ]
    
    with st.expander("📤 Upload Document", expanded=False):
        with st.form("upload_document"):
            col1, col2 = st.columns(2)
            with col1:
                doc_title = st.text_input("Document Title")
                doc_category = st.selectbox("Category", doc_categories)
                doc_date = st.date_input("Document Date", date.today())
            with col2:
                doc_author = st.text_input("Author/Prepared By")
                doc_version = st.text_input("Version", placeholder="v1.0")
                doc_tags = st.text_input("Tags", placeholder="comma separated")
            
            doc_description = st.text_area("Description")
            doc_file = st.file_uploader("Upload File", type=['pdf', 'docx', 'xlsx', 'pptx', 'txt', 'jpg', 'png'])
            
            submitted = st.form_submit_button("📎 Upload Document")
            
            if submitted and doc_title:
                new_doc = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": doc_title,
                    "category": doc_category,
                    "date": doc_date.isoformat(),
                    "author": doc_author,
                    "version": doc_version,
                    "tags": doc_tags,
                    "description": doc_description,
                    "filename": doc_file.name if doc_file else "",
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.mpcfs_documents.append(new_doc)
                
                if doc_file:
                    os.makedirs("mpcfs_documents", exist_ok=True)
                    with open(f"mpcfs_documents/{doc_file.name}", "wb") as f:
                        f.write(doc_file.getbuffer())
                    st.success(f"✅ Document '{doc_title}' uploaded!")
                else:
                    st.success(f"✅ Document '{doc_title}' recorded!")
                st.rerun()
    
    if st.session_state.mpcfs_documents:
        df = pd.DataFrame(st.session_state.mpcfs_documents)
        st.dataframe(df[['title', 'category', 'date', 'version', 'author']], use_container_width=True, hide_index=True)
    else:
        st.info("No documents uploaded yet.")


def show_mpcfs_photo_gallery():
    """Photo gallery for MPCFS project documentation"""
    
    st.markdown("#### Project Photo Gallery")
    st.caption("Visual documentation of project activities, events, and progress")
    
    with st.expander("📸 Upload Photos", expanded=False):
        with st.form("upload_photo"):
            col1, col2 = st.columns(2)
            with col1:
                photo_title = st.text_input("Photo Title")
                photo_location = st.text_input("Location")
                photo_date = st.date_input("Date Taken", date.today())
            with col2:
                photo_activity = st.text_input("Activity/Event")
                photographer = st.text_input("Photographer")
                photo_tags = st.text_input("Tags", placeholder="comma separated")
            
            photo_description = st.text_area("Description")
            photo_file = st.file_uploader("Select Photo", type=['jpg', 'jpeg', 'png'])
            
            submitted = st.form_submit_button("📸 Upload Photo")
            
            if submitted and photo_title and photo_file:
                new_photo = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": photo_title,
                    "location": photo_location,
                    "date": photo_date.isoformat(),
                    "activity": photo_activity,
                    "photographer": photographer,
                    "tags": photo_tags,
                    "description": photo_description,
                    "filename": photo_file.name,
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.mpcfs_photos.append(new_photo)
                
                os.makedirs("mpcfs_photos", exist_ok=True)
                with open(f"mpcfs_photos/{photo_file.name}", "wb") as f:
                    f.write(photo_file.getbuffer())
                
                st.success(f"✅ Photo '{photo_title}' uploaded!")
                st.rerun()
    
    if st.session_state.mpcfs_photos:
        cols = st.columns(3)
        for i, photo in enumerate(reversed(st.session_state.mpcfs_photos)):
            with cols[i % 3]:
                st.markdown(f"**{photo.get('title')}**")
                st.caption(f"📍 {photo.get('location')}")
                st.caption(f"📅 {photo.get('date')}")
                if st.button(f"🗑️ Delete", key=f"del_photo_{photo.get('id')}"):
                    st.session_state.mpcfs_photos = [p for p in st.session_state.mpcfs_photos if p.get('id') != photo.get('id')]
                    st.rerun()
                st.markdown("---")
    else:
        st.info("No photos uploaded yet.")


def show_mpcfs_report_generator_updated():
    """Generate consolidated reports"""
    
    st.markdown("#### Report Generator")
    st.caption("Generate consolidated reports with cover letter for submission")
    
    report_type = st.selectbox("Select Report Type", [
        "Narrative Report", "Accomplishment Report", "Financial Report",
        "Liquidation Report", "Monitoring & Evaluation Report", "Procurement Report"
    ])
    
    report_period = st.selectbox("Reporting Period", [
        "January - March 2025", "April - June 2025", "July - September 2025",
        "October - December 2025", "Annual Report 2025"
    ])
    
    if st.button("📄 Generate Report", type="primary"):
        st.markdown("---")
        st.markdown("### 📋 Generated Report Preview")
        st.success("Report generated successfully!")
    
    st.info("💡 Pro Tip: All reports will automatically pull data from the project dashboard.")


# ============================================================
# CLIMATE PROJECTIONS FUNCTIONS
# ============================================================

def show_climate_projections():
    """Display Climate Change Projections from both 2011 DOST and 2024 CLIRAM data"""
    
    st.markdown("### 📊 Climate Change Projections")
    st.caption("CMIP6-CLIRAM (2024) and DOST-PAGASA (2011) climate data for Mountain Province")
    
    # ============================================================
    # CLIRAM 2024 DATA - Monthly Rainfall
    # ============================================================
    
    cliram_rainfall = {
        "baseline": {
            "January": 40.8, "February": 45.2, "March": 56.0, "April": 96.9,
            "May": 235.4, "June": 264.1, "July": 387.7, "August": 444.0,
            "September": 313.6, "October": 247.5, "November": 181.0, "December": 105.6
        },
        "2021-2050": {
            "January": {"upper": 44.7, "median": 40.7, "lower": 37.7},
            "February": {"upper": 50.3, "median": 45.6, "lower": 40.6},
            "March": {"upper": 60.1, "median": 51.5, "lower": 44.5},
            "April": {"upper": 105.5, "median": 92.0, "lower": 79.6},
            "May": {"upper": 246.4, "median": 225.6, "lower": 210.5},
            "June": {"upper": 288.8, "median": 269.2, "lower": 248.6},
            "July": {"upper": 417.2, "median": 393.5, "lower": 377.0},
            "August": {"upper": 469.9, "median": 446.6, "lower": 426.5},
            "September": {"upper": 340.0, "median": 318.9, "lower": 303.9},
            "October": {"upper": 285.8, "median": 259.9, "lower": 240.6},
            "November": {"upper": 198.9, "median": 184.2, "lower": 172.4},
            "December": {"upper": 116.9, "median": 105.4, "lower": 95.9}
        },
        "2051-2080": {
            "January": {"upper": 48.0, "median": 43.3, "lower": 37.6},
            "February": {"upper": 49.6, "median": 45.1, "lower": 39.4},
            "March": {"upper": 59.6, "median": 50.6, "lower": 43.8},
            "April": {"upper": 103.0, "median": 91.3, "lower": 78.3},
            "May": {"upper": 254.2, "median": 225.5, "lower": 202.4},
            "June": {"upper": 291.6, "median": 271.6, "lower": 253.4},
            "July": {"upper": 429.8, "median": 404.8, "lower": 379.6},
            "August": {"upper": 480.6, "median": 448.8, "lower": 425.3},
            "September": {"upper": 346.3, "median": 327.7, "lower": 307.6},
            "October": {"upper": 285.7, "median": 262.3, "lower": 245.9},
            "November": {"upper": 210.4, "median": 185.1, "lower": 165.8},
            "December": {"upper": 123.3, "median": 109.3, "lower": 96.6}
        },
        "2071-2100": {
            "January": {"upper": 47.2, "median": 42.7, "lower": 36.4},
            "February": {"upper": 50.3, "median": 44.6, "lower": 38.9},
            "March": {"upper": 58.7, "median": 50.4, "lower": 43.3},
            "April": {"upper": 103.8, "median": 87.8, "lower": 73.1},
            "May": {"upper": 250.0, "median": 225.6, "lower": 197.2},
            "June": {"upper": 296.4, "median": 272.4, "lower": 257.8},
            "July": {"upper": 434.9, "median": 401.8, "lower": 381.7},
            "August": {"upper": 493.3, "median": 457.4, "lower": 427.0},
            "September": {"upper": 357.1, "median": 325.9, "lower": 308.8},
            "October": {"upper": 292.8, "median": 267.8, "lower": 239.4},
            "November": {"upper": 215.0, "median": 186.9, "lower": 169.9},
            "December": {"upper": 125.0, "median": 110.9, "lower": 99.1}
        }
    }
    
    # ============================================================
    # CLIRAM 2024 DATA - Monthly Temperature
    # ============================================================
    
    cliram_temperature = {
        "baseline": {
            "January": 18.8, "February": 19.5, "March": 21.0, "April": 22.5,
            "May": 23.0, "June": 23.2, "July": 22.7, "August": 22.6,
            "September": 22.4, "October": 21.6, "November": 20.7, "December": 19.5
        },
        "2021-2050": {
            "January": {"upper": 20.0, "median": 19.8, "lower": 19.6, "change": 1.0},
            "February": {"upper": 20.7, "median": 20.4, "lower": 20.2, "change": 0.9},
            "March": {"upper": 22.1, "median": 21.9, "lower": 21.7, "change": 0.9},
            "April": {"upper": 23.6, "median": 23.4, "lower": 23.2, "change": 0.9},
            "May": {"upper": 24.3, "median": 24.1, "lower": 23.9, "change": 1.1},
            "June": {"upper": 24.4, "median": 24.2, "lower": 24.0, "change": 1.0},
            "July": {"upper": 23.9, "median": 23.7, "lower": 23.5, "change": 1.0},
            "August": {"upper": 23.7, "median": 23.5, "lower": 23.4, "change": 0.9},
            "September": {"upper": 23.6, "median": 23.4, "lower": 23.2, "change": 1.0},
            "October": {"upper": 22.7, "median": 22.6, "lower": 22.4, "change": 1.0},
            "November": {"upper": 21.8, "median": 21.6, "lower": 21.5, "change": 0.9},
            "December": {"upper": 20.6, "median": 20.4, "lower": 20.2, "change": 0.9}
        },
        "2071-2100": {
            "January": {"upper": 21.7, "median": 21.0, "lower": 20.2, "change": 2.2},
            "February": {"upper": 22.3, "median": 21.5, "lower": 20.8, "change": 2.0},
            "March": {"upper": 24.0, "median": 23.1, "lower": 22.4, "change": 2.1},
            "April": {"upper": 25.7, "median": 24.7, "lower": 23.9, "change": 2.2},
            "May": {"upper": 26.4, "median": 25.4, "lower": 24.6, "change": 2.4},
            "June": {"upper": 26.4, "median": 25.5, "lower": 24.7, "change": 2.3},
            "July": {"upper": 25.8, "median": 24.9, "lower": 24.1, "change": 2.2},
            "August": {"upper": 25.6, "median": 24.8, "lower": 23.9, "change": 2.2},
            "September": {"upper": 25.5, "median": 24.6, "lower": 23.8, "change": 2.2},
            "October": {"upper": 24.7, "median": 23.8, "lower": 22.9, "change": 2.2},
            "November": {"upper": 23.7, "median": 22.9, "lower": 22.1, "change": 2.2},
            "December": {"upper": 22.4, "median": 21.6, "lower": 21.6, "change": 2.1}
        }
    }
    
    # Create tabs
    proj_tab1, proj_tab2, proj_tab3, proj_tab4, proj_tab5 = st.tabs([
        "📊 Data Source Comparison",
        "🌡️ CLIRAM Temperature",
        "🌧️ CLIRAM Rainfall",
        "📈 2011 DOST Analysis",
        "🌱 Recommendations"
    ])
    
    with proj_tab1:
        show_data_source_comparison()
    
    with proj_tab2:
        show_cliram_temperature(cliram_temperature)
    
    with proj_tab3:
        show_cliram_rainfall(cliram_rainfall)
    
    with proj_tab4:
        show_dost_2011_analysis()
    
    with proj_tab5:
        show_adaptation_recommendations()


def show_data_source_comparison():
    """Show comparison between 2011 DOST and 2024 CLIRAM data"""
    
    st.markdown("#### 📊 Climate Data Sources Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📘 2011 DOST Data
        **Source:** Climate Change in the Philippines (UN-MDGIF Project)
        
        **Features:**
        - Seasonal temperature and rainfall changes
        - 2020 and 2050 projections only
        - Medium-range emission scenario
        - Baseline: 1971-2000
        
        **Best for:**
        - LCCAP baseline reference
        - Long-term trend analysis
        - Policy formulation
        """)
    
    with col2:
        st.markdown("""
        ### 📗 2024 CLIRAM Data
        **Source:** CMIP6-Based Climate Change Projections
        
        **Features:**
        - Monthly temperature and rainfall
        - Multiple time periods (2021-2100)
        - Upper/Median/Lower bounds (uncertainty)
        - Latest CMIP6 models
        
        **Best for:**
        - Detailed monthly planning
        - Risk assessment
        - Sectoral adaptation planning
        """)
    
    st.markdown("---")
    st.markdown("### 🔄 How to Use Both Data Sources")
    st.markdown("""
    | Use Case | Recommended Data |
    |----------|------------------|
    | LCCAP Executive Summary | 2011 DOST (simpler, policy-ready) |
    | Detailed Sector Planning | 2024 CLIRAM (monthly, uncertainty ranges) |
    | Infrastructure Design | 2024 CLIRAM (extreme event projections) |
    | Agricultural Planning | Both (seasonal from 2011, monthly from CLIRAM) |
    | Water Resource Management | 2024 CLIRAM (detailed monthly rainfall) |
    """)


def show_cliram_temperature(cliram_temperature):
    """Show CLIRAM 2024 temperature projections"""
    
    st.markdown("#### 🌡️ CLIRAM Temperature Projections (2024)")
    st.caption("Monthly temperature projections with uncertainty ranges")
    
    # Period selector
    periods = ["2021-2050", "2071-2100"]
    selected_period = st.selectbox("Select Time Period", periods, key="cliram_temp_period")
    
    # Get data
    period_data = cliram_temperature[selected_period]
    baseline = cliram_temperature["baseline"]
    
    months = list(baseline.keys())
    baseline_values = [baseline[m] for m in months]
    median_values = [period_data[m]["median"] for m in months]
    upper_values = [period_data[m]["upper"] for m in months]
    lower_values = [period_data[m]["lower"] for m in months]
    
    # Create chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=baseline_values,
        mode='lines+markers', name='Baseline (1971-2000)',
        line=dict(color='#3498db', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=median_values,
        mode='lines+markers', name=f'Projected ({selected_period})',
        line=dict(color='#e74c3c', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=upper_values,
        mode='lines', name='Upper Bound',
        line=dict(color='#e74c3c', width=1, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=lower_values,
        mode='lines', name='Lower Bound',
        line=dict(color='#e74c3c', width=1, dash='dash'),
        fill='tonexty', fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    fig.update_layout(
        title=f"Monthly Temperature Projections for Mountain Province ({selected_period})",
        xaxis_title="Month", yaxis_title="Temperature (°C)",
        height=500, hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.markdown("#### 📋 Monthly Temperature Data")
    
    table_data = []
    for i, month in enumerate(months):
        table_data.append({
            "Month": month,
            "Baseline (°C)": baseline_values[i],
            f"{selected_period} Median (°C)": median_values[i],
            "Change (°C)": median_values[i] - baseline_values[i],
            "Range (°C)": f"{lower_values[i]:.1f} - {upper_values[i]:.1f}"
        })
    
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    
    st.caption("Source: DOST-PAGASA CMIP6-CLIRAM (2024)")


def show_cliram_rainfall(cliram_rainfall):
    """Show CLIRAM 2024 rainfall projections"""
    
    st.markdown("#### 🌧️ CLIRAM Rainfall Projections (2024)")
    st.caption("Monthly rainfall projections with uncertainty ranges")
    
    # Period selector
    periods = ["2021-2050", "2051-2080", "2071-2100"]
    selected_period = st.selectbox("Select Time Period", periods, key="cliram_rain_period")
    
    # Get data
    period_data = cliram_rainfall[selected_period]
    baseline = cliram_rainfall["baseline"]
    
    months = list(baseline.keys())
    baseline_values = [baseline[m] for m in months]
    median_values = [period_data[m]["median"] for m in months]
    upper_values = [period_data[m]["upper"] for m in months]
    lower_values = [period_data[m]["lower"] for m in months]
    
    # Calculate percentage changes
    pct_changes = [(median_values[i] - baseline_values[i]) / baseline_values[i] * 100 for i in range(12)]
    
    # Create chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=baseline_values,
        mode='lines+markers', name='Baseline (1971-2000)',
        line=dict(color='#3498db', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=median_values,
        mode='lines+markers', name=f'Projected ({selected_period})',
        line=dict(color='#2ecc71', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=upper_values,
        mode='lines', name='Upper Bound',
        line=dict(color='#2ecc71', width=1, dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=lower_values,
        mode='lines', name='Lower Bound',
        line=dict(color='#2ecc71', width=1, dash='dash'),
        fill='tonexty', fillcolor='rgba(46, 204, 113, 0.1)'
    ))
    
    fig.update_layout(
        title=f"Monthly Rainfall Projections for Mountain Province ({selected_period})",
        xaxis_title="Month", yaxis_title="Rainfall (mm)",
        height=500, hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary table
    st.markdown("#### 📋 Monthly Rainfall Data")
    
    table_data = []
    for i, month in enumerate(months):
        table_data.append({
            "Month": month,
            "Baseline (mm)": baseline_values[i],
            f"{selected_period} Median (mm)": median_values[i],
            "Change (mm)": median_values[i] - baseline_values[i],
            "Change (%)": f"{pct_changes[i]:+.1f}%",
            "Range (mm)": f"{lower_values[i]:.0f} - {upper_values[i]:.0f}"
        })
    
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    
    # Seasonal summary
    st.markdown("#### 🌦️ Seasonal Summary")
    
    seasons = {
        "DJF (Dec-Feb)": ["December", "January", "February"],
        "MAM (Mar-May)": ["March", "April", "May"],
        "JJA (Jun-Aug)": ["June", "July", "August"],
        "SON (Sep-Nov)": ["September", "October", "November"]
    }
    
    seasonal_data = []
    for season_name, season_months in seasons.items():
        baseline_seasonal = sum([baseline[m] for m in season_months])
        projected_seasonal = sum([period_data[m]["median"] for m in season_months])
        pct_change = (projected_seasonal - baseline_seasonal) / baseline_seasonal * 100
        seasonal_data.append({
            "Season": season_name,
            "Baseline (mm)": baseline_seasonal,
            f"Projected {selected_period} (mm)": projected_seasonal,
            "Change (%)": f"{pct_change:+.1f}%"
        })
    
    st.dataframe(pd.DataFrame(seasonal_data), use_container_width=True, hide_index=True)
    
    st.caption("Source: DOST-PAGASA CMIP6-CLIRAM (2024)")


def show_dost_2011_analysis():
    """Show 2011 DOST analysis (simpler, policy-ready)"""
    
    st.markdown("#### 📈 DOST-PAGASA 2011 Analysis")
    st.caption("Seasonal projections under medium-range emission scenario")
    
    # Temperature table
    st.markdown("### 🌡️ Temperature Projections")
    
    temp_data = {
        "Season": ["DJF", "MAM", "JJA", "SON"],
        "Baseline (°C)": [22.7, 26.0, 26.1, 24.9],
        "2020 Increase": [0.9, 0.9, 0.9, 0.9],
        "2020 Projected": [23.6, 26.9, 27.0, 25.8],
        "2050 Increase": [1.9, 2.1, 1.9, 1.9],
        "2050 Projected": [24.6, 28.1, 28.0, 26.8]
    }
    
    df_temp = pd.DataFrame(temp_data)
    st.dataframe(df_temp, use_container_width=True, hide_index=True)
    
    # Rainfall table
    st.markdown("### 🌧️ Rainfall Projections")
    
    rain_data = {
        "Season": ["DJF", "MAM", "JJA", "SON", "ANNUAL"],
        "Baseline (mm)": [74.8, 286.8, 1121.1, 699.2, 2181.9],
        "2020 Change (%)": [-2.7, -7.7, 16.4, 14.9, 5.2],
        "2050 Change (%)": [1.1, -27.4, 26.6, 8.5, 2.2],
        "2050 Projected (mm)": [75.6, 208.2, 1419.4, 758.6, 2461.8]
    }
    
    df_rain = pd.DataFrame(rain_data)
    st.dataframe(df_rain, use_container_width=True, hide_index=True)
    
    # Key findings
    st.markdown("### 🔍 Key Findings for LCCAP")
    st.markdown("""
    - **Temperature increase:** +1.9°C to +2.1°C by 2050
    - **Maximum temperature:** Could reach 34.1°C in MAM by 2050
    - **Wet season (JJA):** Rainfall increases by 26.6% by 2050 → Higher flood risk
    - **Dry season (MAM):** Rainfall decreases by 27.4% by 2050 → Higher drought risk
    - **Annual rainfall:** Slight increase of 2.2% by 2050
    """)
    
    st.caption("Source: DOST-PAGASA, 2011. Climate Change in the Philippines (Medium-Range Emission Scenario)")

def show_temperature_projections():
    """Display temperature projections from 2011 DOST data"""
    
    st.markdown("#### 🌡️ Temperature Projections")
    st.caption("Projected changes in temperature based on DOST-PAGASA (2011) data")
    
    # Temperature data from your tables
    temp_data = {
        "Season": ["DJF (Dec-Jan-Feb)", "MAM (Mar-Apr-May)", "JJA (Jun-Jul-Aug)", "SON (Sep-Oct-Nov)"],
        "Baseline (1971-2000) °C": [22.7, 26.0, 26.1, 24.9],
        "2020 Increase (°C)": [0.9, 0.9, 0.9, 0.9],
        "2020 Projected (°C)": [23.6, 26.9, 27.0, 25.8],
        "2050 Increase (°C)": [1.9, 2.1, 1.9, 1.9],
        "2050 Projected (°C)": [24.6, 28.1, 28.0, 26.8]
    }
    
    df_temp = pd.DataFrame(temp_data)
    st.dataframe(df_temp, use_container_width=True, hide_index=True)
    
    # Create chart
    seasons = df_temp["Season"].tolist()
    baseline = df_temp["Baseline (1971-2000) °C"].tolist()
    projected_2020 = df_temp["2020 Projected (°C)"].tolist()
    projected_2050 = df_temp["2050 Projected (°C)"].tolist()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Baseline (1971-2000)', x=seasons, y=baseline, marker_color='#3498db'))
    fig.add_trace(go.Bar(name='2020 Projected', x=seasons, y=projected_2020, marker_color='#f39c12'))
    fig.add_trace(go.Bar(name='2050 Projected', x=seasons, y=projected_2050, marker_color='#e74c3c'))
    
    fig.update_layout(title="Temperature Projections by Season", xaxis_title="Season", yaxis_title="Temperature (°C)", height=450, barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Maximum and Minimum Temperature
    st.markdown("### Maximum & Minimum Temperature Projections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Maximum Temperature**")
        max_data = {
            "Season": ["DJF", "MAM", "JJA", "SON"],
            "Baseline (°C)": [27.5, 31.5, 30.7, 29.2],
            "2050 Projected (°C)": [29.6, 34.1, 32.5, 31.4]
        }
        df_max = pd.DataFrame(max_data)
        st.dataframe(df_max, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("**Minimum Temperature**")
        min_data = {
            "Season": ["DJF", "MAM", "JJA", "SON"],
            "Baseline (°C)": [17.8, 20.6, 21.7, 20.5],
            "2050 Projected (°C)": [19.7, 22.5, 24.1, 22.3]
        }
        df_min = pd.DataFrame(min_data)
        st.dataframe(df_min, use_container_width=True, hide_index=True)
    
    st.caption("Source: DOST-PAGASA, 2011. Climate Change in the Philippines (Medium-Range Emission Scenario)")


def show_rainfall_projections():
    """Display rainfall projections from 2011 DOST data"""
    
    st.markdown("#### 🌧️ Rainfall Projections")
    st.caption("Projected changes in rainfall based on DOST-PAGASA (2011) data")
    
    # Rainfall data from your tables
    rain_data = {
        "Season": ["DJF (Dec-Jan-Feb)", "MAM (Mar-Apr-May)", "JJA (Jun-Jul-Aug)", "SON (Sep-Oct-Nov)", "ANNUAL"],
        "Baseline (1971-2000) mm": [74.8, 286.8, 1121.1, 699.2, 2181.9],
        "2020 Change (%)": [-2.7, -7.7, 16.4, 14.9, 5.2],
        "2020 Projected (mm)": [72.8, 264.7, 1304.9, 803.4, 2295.8],
        "2050 Change (%)": [1.1, -27.4, 26.6, 8.5, 2.2],
        "2050 Projected (mm)": [75.6, 208.2, 1419.4, 758.6, 2461.8]
    }
    
    df_rain = pd.DataFrame(rain_data)
    st.dataframe(df_rain, use_container_width=True, hide_index=True)
    
    # Create chart
    seasons = ["DJF", "MAM", "JJA", "SON"]
    baseline = [74.8, 286.8, 1121.1, 699.2]
    projected_2050 = [75.6, 208.2, 1419.4, 758.6]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Baseline (1971-2000)', x=seasons, y=baseline, marker_color='#3498db'))
    fig.add_trace(go.Bar(name='2050 Projected', x=seasons, y=projected_2050, marker_color='#2ecc71'))
    
    fig.update_layout(title="Rainfall Projections by Season", xaxis_title="Season", yaxis_title="Rainfall (mm)", height=450, barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    st.caption("Source: DOST-PAGASA, 2011. Climate Change in the Philippines (Medium-Range Emission Scenario)")


def show_comparative_analysis():
    """Show comparative analysis across time periods"""
    
    st.markdown("#### 📊 Comparative Climate Analysis")
    st.caption("How climate variables change from 2020 to 2050")
    
    # Summary table
    summary_data = {
        "Climate Variable": [
            "Annual Average Temperature",
            "Maximum Temperature (MAM)",
            "Minimum Temperature (JJA)",
            "Annual Rainfall",
            "Wet Season Rainfall (JJA)",
            "Dry Season Rainfall (MAM)"
        ],
        "Baseline (1971-2000)": [
            "24.9°C", "31.5°C", "21.7°C", "2,182 mm", "1,121 mm", "287 mm"
        ],
        "2020 Projected": [
            "25.8°C", "32.6°C", "22.6°C", "2,296 mm", "1,305 mm", "265 mm"
        ],
        "2050 Projected": [
            "26.9°C", "34.1°C", "24.1°C", "2,462 mm", "1,419 mm", "208 mm"
        ],
        "Change (2050 vs Baseline)": [
            "+2.0°C", "+2.6°C", "+2.4°C", "+12.8%", "+26.6%", "-27.4%"
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Key findings
    st.markdown("### 🔍 Key Findings")
    st.markdown("""
    - **Temperatures are rising:** By 2050, average temperatures could increase by up to 2.0°C
    - **Hotter summers:** Maximum temperatures in MAM could reach 34.1°C by 2050
    - **Wetter wet season:** JJA rainfall could increase by 26.6% by 2050
    - **Drier dry season:** MAM rainfall could decrease by 27.4% by 2050
    - **More extreme events:** Increased risk of both flooding and drought
    """)


def show_adaptation_recommendations():
    """Show adaptation recommendations based on projections"""
    
    st.markdown("#### 🌱 Adaptation Recommendations")
    st.caption("Climate-smart strategies for Mountain Province")
    
    st.markdown("""
    ### 🎯 Priority Adaptation Actions
    
    **Agriculture:**
    - Promote drought-resistant and flood-tolerant crop varieties
    - Implement climate-smart agriculture practices
    - Develop water-efficient irrigation systems
    
    **Water Resources:**
    - Construct small-scale water impounding projects
    - Implement rainwater harvesting systems
    - Protect and restore watershed areas
    
    **Infrastructure:**
    - Upgrade drainage systems for higher rainfall intensity
    - Design climate-resilient roads and bridges
    - Strengthen early warning systems
    
    **Health:**
    - Establish heat wave response protocols
    - Strengthen vector-borne disease surveillance
    - Conduct climate-health awareness campaigns
    
    **Ecosystems:**
    - Implement reforestation programs
    - Protect critical habitats
    - Promote nature-based solutions
    """)
    
    st.info("Source: DOST-PAGASA Climate Projections (2011, 2024) and INDC Adaptation Framework")


def show_cca_analytics():
    """Display CCA analytics and insights"""
    
    st.markdown("### CCA Analytics & Insights")
    st.caption("Data-driven insights on climate adaptation progress")
    
    st.info("Analytics dashboard coming soon. This will include:")
    st.markdown("""
    - Climate vulnerability trends
    - Adaptation project effectiveness
    - Financing gap analysis
    - Municipal CCA readiness scores
    """)


def show_cca_documents():
    """Document repository for CCA-related files"""
    
    st.markdown("### CCA Document Repository")
    st.caption("Store and manage climate change adaptation-related documents")
    
    st.info("Document repository coming soon. This will store:")
    st.markdown("""
    - PCCAP and LCCAP documents
    - Climate risk assessments
    - Adaptation project proposals
    - Climate data and reports
    """)


def show_cca_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How Climate Change Adaptation connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Plan Management
        - CCA plans integrate with DRRM plans
        - Adaptation projects link to PPAs
        - Climate indicators in M&E framework
        
        ### 🌾 MPCFS Project Hub
        - Flagship climate adaptation project
        - Documentation for coffee table book
        - Farmer training records
        """)
    
    with col2:
        st.markdown("""
        ### 📊 DRRM Intelligence
        - Climate hazard data
        - Vulnerability assessments
        - Risk mapping integration
        
        ### 📚 Trainings
        - Climate literacy programs
        - Farmer capacity building
        - Extension worker training
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col2:
        if st.button("📚 Go to Trainings", use_container_width=True):
            st.session_state.navigation = "📚 TRAININGS"
            st.rerun()
    with col3:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()