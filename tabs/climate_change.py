# tabs/climate_change.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import os
import copy
import json
import hashlib
import numpy as np
import io
import base64
from datetime import datetime, date, timedelta
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
    
    # MPCFS Sub-tabs - UPDATED with Master Dashboard first
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


def show_mpcfs_dashboard():
    """Project dashboard with key metrics and progress tracking"""
    
    st.markdown("#### Project Dashboard")
    
    # Progress by component
    components_data = {
        "Component": [
            "Climate Field School Establishment",
            "Farmer Training & Capacity Building",
            "Demonstration Farms",
            "Research & Documentation",
            "Knowledge Management",
            "Monitoring & Evaluation"
        ],
        "Progress": [65, 48, 52, 35, 28, 42],
        "Target": [70, 50, 55, 40, 35, 45]
    }
    
    df = pd.DataFrame(components_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Actual Progress", x=df["Component"], y=df["Progress"], marker_color="#2ecc71"))
    fig.add_trace(go.Bar(name="Target", x=df["Component"], y=df["Target"], marker_color="#f39c12"))
    fig.update_layout(title="Progress by Component", height=400, barmode="group")
    st.plotly_chart(fig, use_container_width=True)
    
    # Quarterly progress
    st.markdown("#### Quarterly Progress Tracking")
    quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025"]
    progress = [15, 28, 35, 40, 42]
    
    fig = px.line(x=quarters, y=progress, markers=True, title="Overall Project Progress Trend")
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Progress (%)", yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    # Key achievements
    st.markdown("#### Key Achievements")
    achievements = [
        "✅ Climate Field School facility construction at 65% completion",
        "✅ 1,247 farmers trained in climate-resilient agriculture techniques",
        "✅ 3 demonstration farms established across Paracelis",
        "✅ Baseline survey completed with 2,500+ farmer respondents",
        "✅ Project Management Office fully operational"
    ]
    for achievement in achievements:
        st.markdown(achievement)


def show_mpcfs_gantt():
    """Gantt chart for project timeline and task tracking"""
    
    st.markdown("#### Project Gantt Chart & Timeline")
    st.caption("Track project milestones, tasks, and deadlines")
    
    tasks = [
        {"Task": "Project Inception & Planning", "Start": "2024-01-01", "Finish": "2024-03-31", "Complete": 100},
        {"Task": "Field School Construction", "Start": "2024-04-01", "Finish": "2025-06-30", "Complete": 65},
        {"Task": "Farmer Training Program", "Start": "2024-05-01", "Finish": "2026-12-31", "Complete": 48},
        {"Task": "Demo Farm Establishment", "Start": "2024-06-01", "Finish": "2025-03-31", "Complete": 52},
        {"Task": "Research & Documentation", "Start": "2024-07-01", "Finish": "2027-12-31", "Complete": 35},
        {"Task": "Knowledge Management", "Start": "2025-01-01", "Finish": "2028-06-30", "Complete": 28},
        {"Task": "Monitoring & Evaluation", "Start": "2024-04-01", "Finish": "2028-12-31", "Complete": 42},
        {"Task": "Coffee Table Book Production", "Start": "2027-01-01", "Finish": "2028-12-31", "Complete": 10},
        {"Task": "Project Close-out", "Start": "2028-10-01", "Finish": "2028-12-31", "Complete": 0}
    ]
    
    df_tasks = pd.DataFrame(tasks)
    df_tasks["Start"] = pd.to_datetime(df_tasks["Start"])
    df_tasks["Finish"] = pd.to_datetime(df_tasks["Finish"])
    
    fig = go.Figure()
    for i, task in df_tasks.iterrows():
        fig.add_trace(go.Bar(
            x=[(task["Finish"] - task["Start"]).days],
            y=[task["Task"]],
            orientation='h',
            marker=dict(color='#2ecc71', opacity=0.8),
            text=f"{task['Complete']}% Complete",
            textposition='outside'
        ))
    
    fig.update_layout(title="Project Timeline", xaxis_title="Duration (Days)", height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("#### Task Status")
    for task in tasks:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{task['Task']}**")
        with col2:
            st.markdown(f"{task['Complete']}% Complete")
        with col3:
            if task['Complete'] >= 90:
                st.success("✅")
            elif task['Complete'] >= 50:
                st.warning("🟡 In Progress")
            else:
                st.info("⏳ Pending")


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
                    save_path = f"mpcfs_documents/{doc_file.name}"
                    os.makedirs("mpcfs_documents", exist_ok=True)
                    with open(save_path, "wb") as f:
                        f.write(doc_file.getbuffer())
                    st.success(f"✅ Document '{doc_title}' uploaded and saved locally!")
                else:
                    st.success(f"✅ Document '{doc_title}' recorded!")
                st.rerun()
    
    if st.session_state.mpcfs_documents:
        df = pd.DataFrame(st.session_state.mpcfs_documents)
        categories = ["All"] + list(df['category'].unique())
        selected_category = st.selectbox("Filter by Category", categories)
        
        if selected_category != "All":
            df = df[df['category'] == selected_category]
        
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
                
                save_path = f"mpcfs_photos/{photo_file.name}"
                os.makedirs("mpcfs_photos", exist_ok=True)
                with open(save_path, "wb") as f:
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


def show_mpcfs_report_generator():
    """Generate consolidated reports with cover letter"""
    
    st.markdown("#### Report Generator")
    st.caption("Generate consolidated reports with cover letter for submission")
    
    report_type = st.selectbox("Select Report Type", [
        "Narrative Report", "Accomplishment Report", "Financial Report",
        "Liquidation Report", "Monitoring & Evaluation Report", "Procurement Report"
    ])
    
    report_period = st.selectbox("Reporting Period", [
        "January - March 2024", "April - June 2024", "July - September 2024",
        "October - December 2024", "Annual Report 2024"
    ])
    
    if st.button("📄 Generate Report", type="primary"):
        st.markdown("---")
        st.markdown("### 📋 Generated Report Preview")
        st.success("Report generated successfully!")
    
    st.info("💡 Pro Tip: All reports will automatically pull data from the project dashboard.")


def show_mpcfs_coffee_table_book():
    """Coffee table book generator"""
    
    st.markdown("#### 📖 Coffee Table Book Generator")
    st.caption("Compile project experiences, beneficiary stories, and documentation")
    
    st.markdown("""
    ### About the MPCFS Coffee Table Book
    
    This feature will document the journey of the Mountain Province Climate Field School Project, capturing:
    - **Beneficiary Stories**: Personal accounts from farmers and community members
    - **Project Milestones**: Key achievements and turning points
    - **Photo Gallery**: Visual documentation of project activities
    - **Lessons Learned**: Insights and best practices for replication
    """)
    
    if st.button("📖 Generate Coffee Table Book", type="primary"):
        st.success("Coffee table book generation will be available in the next phase.")

def show_mpcfs_master_dashboard():
    """Master Dashboard showing all three components"""
    
    st.markdown("#### 📊 MPCFS Master Dashboard")
    st.caption("Overall project progress across all components")
    
    # Get component data from session state
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    infra_target = st.session_state.get('infrastructure_target', 25.75)
    
    # Handle cost properly
    infra_cost_raw = st.session_state.get('infrastructure_cost', 64_000_000)
    if isinstance(infra_cost_raw, list):
        current_week_val = next((x for x in reversed(infra_cost_raw) if x > 0), 64_000_000)
        infra_cost = current_week_val
    else:
        infra_cost = infra_cost_raw
    
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
    
    # Key metrics row - ALL with 2 decimal places
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Project Progress", f"{total_progress:.2f}%", 
                  delta=f"{active_components}/3 Components Active")
    with col2:
        st.metric("Infrastructure", f"{infra_progress:.2f}%", delta=f"Target: {infra_target:.2f}%")
    with col3:
        st.metric("Capability Building", f"{cap_progress:.2f}%" if cap_progress > 0 else "Not Started", 
                  delta=cap_status)
    with col4:
        st.metric("Research & Extension", f"{res_progress:.2f}%" if res_progress > 0 else "Not Started",
                  delta=res_status)
    
    st.markdown("---")
    
    # Component Progress Bars - 2 decimal places
    st.markdown("### 📈 Component Progress")
    
    # Infrastructure
    st.markdown("#### 🏗️ Infrastructure Component")
    st.progress(infra_progress / 100, text=f"{infra_progress:.2f}% Complete")
    st.caption(f"Contract Amount: ₱249,040,900 | Utilized: ₱{infra_cost:,.2f}")
    
    # Capability Building
    st.markdown("#### 👨‍🌾 Capability Building Component")
    if cap_progress > 0:
        st.progress(cap_progress / 100, text=f"{cap_progress:.2f}% Complete")
    else:
        st.info("📌 Data pending. Upload Capability Building S-Curve to activate this component.")
        st.progress(0, text="Awaiting Data")
    
    # Research & Extension
    st.markdown("#### 🔬 Research & Extension Component")
    if res_progress > 0:
        st.progress(res_progress / 100, text=f"{res_progress:.2f}% Complete")
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
    
    # Quick stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Completed Milestones**")
        st.markdown("- Infrastructure: Site development in progress")
        st.markdown("- Farmer training modules prepared")
        st.markdown("- Demo farm sites identified")
    
    with col2:
        st.markdown("**🎯 Next Milestones**")
        st.markdown("- Complete Infrastructure foundation by Q2 2025")
        st.markdown("- Launch Capability Building program")
        st.markdown("- Establish research protocols")
        
def show_mpcfs_scurve_tracker(component="infrastructure"):
    """MPCFS Infrastructure S-Curve Tracker - COMPLETE FIXED VERSION"""
    
    import copy
    import json
    import hashlib
    from datetime import datetime
    
    component_titles = {
        "infrastructure": {"name": "Infrastructure", "icon": "🏗️", "amount": 249_040_900.00},
        "capability": {"name": "Capability Building", "icon": "👨‍🌾", "amount": 0},
        "research": {"name": "Research & Extension", "icon": "🔬", "amount": 0}
    }
    
    comp = component_titles[component]
    
    st.markdown(f"#### {comp['icon']} {comp['name']} Component - S-Curve Tracker")
    st.caption(f"Track physical and financial progress | Contract: ₱{comp['amount']:,.2f}")
    
    CONTRACT_AMOUNT = comp['amount'] if comp['amount'] > 0 else 249_040_900.00
    prefix = f"{component}_"
    
    # ============================================================
    # WORK ITEMS DATA (from your Excel)
    # ============================================================
    
    if f'{prefix}work_items' not in st.session_state:
        work_items = [
            {"no": "A.1.1 (8)", "description": "Provision of Field Office", "category": "Civil Works", "contract_amount": 1_360_800, "planned_amount": 1_360_800, "actual_amount": 353_808},
            {"no": "A.1.2 (2)", "description": "Provision of 4x4 Vehicle", "category": "Civil Works", "contract_amount": 2_289_000, "planned_amount": 2_289_000, "actual_amount": 595_140},
            {"no": "B.3", "description": "Permits and Clearances", "category": "Civil Works", "contract_amount": 315_000, "planned_amount": 315_000, "actual_amount": 315_000},
            {"no": "B.5", "description": "Billboard and Signboard", "category": "Civil Works", "contract_amount": 10_500, "planned_amount": 10_500, "actual_amount": 2_783},
            {"no": "B.7 (2)", "description": "Safety and Health Program", "category": "Civil Works", "contract_amount": 3_061_108, "planned_amount": 3_061_108, "actual_amount": 795_888},
            {"no": "B.9", "description": "Mobilization/Demobilization", "category": "Civil Works", "contract_amount": 2_174_130, "planned_amount": 2_174_130, "actual_amount": 1_087_065},
            {"no": "B.13", "description": "Geotechnical Investigation", "category": "Civil Works", "contract_amount": 315_000, "planned_amount": 315_000, "actual_amount": 315_000},
            {"no": "B.25", "description": "Engineering & Architectural Design", "category": "Civil Works", "contract_amount": 424_499, "planned_amount": 424_499, "actual_amount": 424_499},
            {"no": "101(1)", "description": "Removal of Structures", "category": "Civil Works", "contract_amount": 9_419, "planned_amount": 9_419, "actual_amount": 9_419},
            {"no": "404", "description": "Reinforcing Steel Bar", "category": "Structural", "contract_amount": 3_529_569, "planned_amount": 796_999, "actual_amount": 2_834_045},
            {"no": "405", "description": "Structural Concrete Class A", "category": "Structural", "contract_amount": 4_908_408, "planned_amount": 475_053, "actual_amount": 1_740_048},
            {"no": "803(1)a", "description": "Structure Excavation", "category": "Structural", "contract_amount": 1_562_882, "planned_amount": 1_562_882, "actual_amount": 1_357_263},
            {"no": "804(4)", "description": "Gravel Fill", "category": "Structural", "contract_amount": 1_572_897, "planned_amount": 1_572_897, "actual_amount": 1_336_224},
            {"no": "1706(1)", "description": "Overhaul", "category": "Structural", "contract_amount": 724_377, "planned_amount": 724_377, "actual_amount": 560_761},
            {"no": "900(1)c2", "description": "Concrete Footing/Slab on Fill", "category": "Structural", "contract_amount": 4_259_204, "planned_amount": 3_293_796, "actual_amount": 3_561_496},
            {"no": "900(1)", "description": "Concrete Columns/Beams", "category": "Structural", "contract_amount": 10_295_803, "planned_amount": 5_183_185, "actual_amount": 3_449_789},
            {"no": "902(1) a", "description": "Reinforcing Steel", "category": "Structural", "contract_amount": 23_180_568, "planned_amount": 9_746_376, "actual_amount": 7_625_371},
            {"no": "903(1)", "description": "Formworks/Falseworks", "category": "Structural", "contract_amount": 3_163_252, "planned_amount": 1_239_654, "actual_amount": 948_291},
            {"no": "1047 (1)", "description": "Structural Steel", "category": "Structural", "contract_amount": 35_288_325, "planned_amount": 7_410_548, "actual_amount": 28_583_543},
            {"no": "1047 (2)a", "description": "Steel Trusses", "category": "Structural", "contract_amount": 4_375_482, "planned_amount": 0, "actual_amount": 823_223},
            {"no": "1047 (3)a", "description": "Anchor Bolts", "category": "Structural", "contract_amount": 3_747_979, "planned_amount": 0, "actual_amount": 3_453_257},
            {"no": "1047 (5)", "description": "Steel Plates", "category": "Structural", "contract_amount": 4_480_181, "planned_amount": 1_409_494, "actual_amount": 3_071_727},
            {"no": "1001(11)", "description": "Septic Vault", "category": "Architectural", "contract_amount": 1_086_528, "planned_amount": 0, "actual_amount": 543_264},
        ]
        
        st.session_state[f'{prefix}work_items'] = work_items
    
    # ============================================================
    # S-CURVE WEEKLY DATA (from your Excel)
    # ============================================================
    
    if f'{prefix}original_plan_weekly' not in st.session_state:
        # Original Plan cumulative (at Week 80 = 64.31%)
        original_plan_weekly = [
            0.99, 1.12, 1.27, 1.47, 1.59, 1.72, 1.90, 2.00, 2.09, 2.17, 2.24, 2.47, 2.80, 3.10, 3.41, 3.73,
            4.03, 4.33, 4.63, 4.98, 5.32, 5.66, 6.01, 6.21, 6.91, 7.62, 9.34, 11.06, 12.79, 14.74, 16.71, 18.34,
            19.97, 21.70, 23.70, 25.71, 27.64, 29.54, 31.39, 33.18, 34.90, 36.54, 38.17, 39.81, 41.39, 42.93,
            44.40, 45.31, 45.66, 46.21, 46.90, 47.50, 48.10, 48.70, 49.32, 49.94, 50.56, 51.19, 51.82, 52.50,
            53.22, 53.65, 54.42, 55.35, 56.10, 56.85, 57.60, 58.23, 58.86, 59.49, 60.09, 60.49, 61.01, 61.55,
            62.04, 62.53, 63.01, 63.50, 63.98, 64.31, 64.43, 64.55, 65.03, 65.52, 65.96, 66.36, 66.76, 67.37,
            67.99, 68.62, 69.26, 69.90, 70.44, 70.96, 71.46, 71.96, 72.47, 72.97, 73.48, 74.00, 74.50, 75.00,
            75.33, 75.69, 76.05, 76.41, 76.77, 77.12, 77.46, 77.79, 78.12, 78.46, 78.80, 79.14, 79.48, 79.88,
            80.26, 80.63, 81.00, 81.37, 81.82, 82.27, 82.80, 83.23, 83.65, 84.08, 84.74, 85.63, 86.52, 87.48,
            88.66, 90.23, 91.80, 93.79, 95.79, 97.61, 99.16, 99.34, 99.96, 100.00
        ]
        while len(original_plan_weekly) < 193:
            original_plan_weekly.append(100.00)
        
        # Revised Plan cumulative (at Week 80 = 16.02%)
        revised_plan_weekly = [
            0.98, 1.10, 1.24, 1.43, 1.54, 1.66, 1.83, 1.91, 2.00, 2.08, 2.16, 2.29, 2.55, 2.82, 3.11, 3.39,
            3.68, 3.97, 4.26, 4.55, 4.82, 5.10, 5.38, 5.86, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24,
            6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24,
            6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.24, 6.56,
            6.95, 7.44, 7.93, 8.42, 8.93, 9.52, 10.11, 10.71, 11.31, 11.99, 12.68, 13.31, 13.94, 14.63, 15.32,
            16.02, 16.72, 17.44, 18.22, 19.00, 19.77, 20.55, 21.33, 22.12, 22.97, 23.79, 24.63, 25.50, 26.36,
            27.25, 28.14, 29.03, 29.91, 30.80, 31.69, 32.58, 33.37, 34.17, 35.26, 36.03, 36.52, 37.00, 37.37,
            37.73, 38.03, 38.34, 38.64, 38.94, 39.24, 39.55, 39.86, 40.19, 40.50, 40.82, 41.14, 41.62, 42.27,
            42.96, 43.64, 44.33, 45.03, 45.72, 46.45, 47.22, 48.00, 48.77, 49.45, 50.14, 50.82, 51.51, 52.53,
            53.57, 54.57, 55.44, 56.33, 57.44, 58.57, 59.69, 60.82, 61.88, 63.05, 64.20, 65.27, 66.35, 67.42,
            68.50, 69.55, 70.60, 71.50, 72.23, 73.10, 74.03, 74.97, 75.90, 76.82, 77.53, 78.27, 79.06, 79.86,
            80.70, 81.53, 82.37, 83.24, 83.96, 84.53, 85.11, 85.69, 85.94, 86.35, 86.84, 87.32, 87.66, 87.98,
            88.19, 88.64, 89.09, 89.54, 90.05, 90.79, 91.86, 92.98, 94.49, 96.00, 97.42, 98.58, 99.03, 99.47, 99.50, 100.00
        ]
        while len(revised_plan_weekly) < 193:
            revised_plan_weekly.append(100.00)
        
        # Actual progress weekly (at Week 80 = 25.75%)
        actual_weekly = [
            0.88, 0.91, 0.95, 1.00, 1.05, 1.10, 1.45, 1.62, 2.12, 2.45, 2.85, 3.21, 3.44, 3.85, 3.95, 4.05,
            4.17, 4.30, 4.40, 4.50, 4.61, 4.70, 4.81, 4.89, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
            5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
            5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 7.33,
            9.88, 11.61, 13.40, 15.45, 17.73, 20.02, 22.30, 24.59, 24.67, 24.75, 24.83, 24.92, 25.14, 25.34, 25.55, 25.75
        ]
        while len(actual_weekly) < 193:
            actual_weekly.append(25.75)
        
        st.session_state[f'{prefix}original_plan_weekly'] = original_plan_weekly
        st.session_state[f'{prefix}revised_plan_weekly'] = revised_plan_weekly
        st.session_state[f'{prefix}actual_weekly'] = actual_weekly
    
    # ============================================================
    # CALCULATIONS
    # ============================================================
    
    work_items = st.session_state[f'{prefix}work_items']
    actual_weekly = st.session_state[f'{prefix}actual_weekly']
    
    total_planned_original = sum(item.get('planned_amount', 0) for item in work_items)
    total_actual_amount = sum(item.get('actual_amount', 0) for item in work_items)
    
    # Current progress at Week 80
    overall_progress = 25.75  # From your Excel
    overall_original_plan = 16.02  # Revised Plan at Week 80 (not original!)
    overall_revised_plan = 25.75  # Target at Week 80
    
    # Calculate correct slippage
    slippage_vs_original_plan = 25.75 - 64.31  # Actual vs Original Plan at Week 80 = -38.56%
    slippage_vs_revised_plan = 25.75 - 16.02  # Actual vs Revised Plan at Week 80 = +9.73%
    
    total_actual_cost = total_actual_amount
    
    # Find current week index (Week 80)
    current_week_idx = 79  # Week 80 (0-indexed)
    
    # Update session state
    st.session_state['infrastructure_progress'] = overall_progress
    st.session_state['infrastructure_target_original'] = 64.31
    st.session_state['infrastructure_target_revised'] = overall_revised_plan
    st.session_state['infrastructure_cost'] = total_actual_cost
    
    # ============================================================
    # KPI CARDS with Color Highlighting for editable areas
    # ============================================================
    
    st.markdown("### 📊 Key Performance Indicators")
    st.markdown("> 💡 **Tip:** Edit the 🟢 **highlighted columns** in the table below to update progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Progress", 
            f"{overall_progress:.2f}%",
            delta=f"₱{total_actual_cost:,.0f} / ₱{CONTRACT_AMOUNT:,.0f}"
        )
    
    with col2:
        st.metric(
            "Slippage vs Original Plan", 
            f"{slippage_vs_original_plan:+.2f}%",
            delta=f"Target at Week 80: 64.31%",
            delta_color="inverse" if slippage_vs_original_plan < 0 else "normal"
        )
    
    with col3:
        st.metric(
            "Slippage vs Revised Plan", 
            f"{slippage_vs_revised_plan:+.2f}%",
            delta=f"Target at Week 80: {overall_revised_plan:.2f}%",
            delta_color="normal" if slippage_vs_revised_plan >= 0 else "inverse"
        )
    
    with col4:
        if slippage_vs_revised_plan > 1:
            status = "✅ AHEAD"
        elif slippage_vs_revised_plan < -1:
            status = "🔴 BEHIND"
        else:
            status = "🟡 ON TRACK"
        st.metric("Overall Status", status, delta="As of Week 80 (Mar 31, 2026)")
    
    st.markdown("---")
    
    # ============================================================
    # S-CURVE CHART
    # ============================================================
    
    st.markdown("### 📈 S-Curve: Planned vs Actual Progress")
    st.markdown("**📍 As of: Week 80 (March 31, 2026)**")
    
    weeks = list(range(1, 194))
    original_weekly = st.session_state[f'{prefix}original_plan_weekly']
    revised_weekly = st.session_state[f'{prefix}revised_plan_weekly']
    actual_weekly_data = st.session_state[f'{prefix}actual_weekly']
    
    fig = go.Figure()
    
    # Original Plan (Blue, dashed) - reaches 64.31% at Week 80
    fig.add_trace(go.Scatter(
        x=weeks[:len(original_weekly)], 
        y=original_weekly,
        mode='lines', 
        name='Original Plan',
        line=dict(color='#1f77b4', width=2, dash='dash'),
        opacity=0.8
    ))
    
    # Revised Plan (Orange, dotted) - reaches 16.02% at Week 80
    fig.add_trace(go.Scatter(
        x=weeks[:len(revised_weekly)], 
        y=revised_weekly,
        mode='lines', 
        name='Revised Plan',
        line=dict(color='#ff7f0e', width=2, dash='dot'),
        opacity=0.8
    ))
    
    # Actual Progress (Green, solid) - reaches 25.75% at Week 80
    fig.add_trace(go.Scatter(
        x=weeks[:current_week_idx + 1], 
        y=actual_weekly_data[:current_week_idx + 1],
        mode='lines+markers', 
        name='Actual Progress',
        line=dict(color='#2ca02c', width=3),
        marker=dict(size=4, symbol='circle', color='#2ca02c')
    ))
    
    # Projected Actual (dotted green)
    if current_week_idx < 192:
        fig.add_trace(go.Scatter(
            x=weeks[current_week_idx + 1:], 
            y=[overall_progress] * (192 - current_week_idx),
            mode='lines', 
            name='Projected (if no change)',
            line=dict(color='#2ca02c', width=2, dash='dot'),
            opacity=0.6
        ))
    
    # Current week vertical line
    fig.add_vline(
        x=current_week_idx + 1, 
        line_dash="dash", 
        line_color="#7f7f7f", 
        line_width=1.5,
        annotation_text=f"Week {current_week_idx + 1}",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title=dict(text="Project Progress S-Curve (September 2024 - May 2028)", font=dict(size=14, color="#2c3e50")),
        xaxis=dict(title="Week Number", title_font=dict(size=12), tickfont=dict(size=10), gridcolor="#e0e0e0", showgrid=True),
        yaxis=dict(title="Cumulative Progress (%)", title_font=dict(size=12), tickfont=dict(size=10), range=[0, 105], gridcolor="#e0e0e0", showgrid=True),
        height=450,
        hovermode='x unified',
        legend=dict(x=0.02, y=0.98, bgcolor='rgba(255,255,255,0.9)', bordercolor="#d0d0d0", borderwidth=1, font=dict(size=11)),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ============================================================
    # TARGET SUMMARY
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📋 **Original Plan at Week 80:** 64.31%")
    with col2:
        st.info(f"📋 **Revised Plan at Week 80:** {overall_revised_plan:.2f}%")
    with col3:
        st.success(f"✅ **Actual Progress at Week 80:** {overall_progress:.2f}%")
    
    st.markdown("---")
    
    # ============================================================
    # ITEMIZED WORK DETAILS TABLE with TOTAL ROW
    # ============================================================
    
    st.markdown("### 📋 Itemized Work Details")
    st.markdown("> 🟢 **GREEN highlighted columns** are editable. Edit then click **💾 SAVE ALL CHANGES**")
    
    # Category filter
    categories = ["All", "Civil Works", "Structural", "Architectural", "Electrical", "Mechanical", "Equipment"]
    selected_category = st.selectbox("🔍 Filter by Category", categories, key=f"{prefix}_category")
    
    # Filter work items
    if selected_category != "All":
        filtered_items = [item for item in work_items if item.get('category', 'Other') == selected_category]
    else:
        filtered_items = work_items
    
    if filtered_items:
        df_items = pd.DataFrame(filtered_items)
        
        # Calculate percentages
        df_items['Planned %'] = (df_items['planned_amount'] / df_items['contract_amount']) * 100
        df_items['Actual %'] = (df_items['actual_amount'] / df_items['contract_amount']) * 100
        df_items['Slippage %'] = df_items['Actual %'] - df_items['Planned %']
        
        # Status: Completed if Actual % >= 99.5%
        df_items['Status'] = df_items['Actual %'].apply(
            lambda x: '✅ Completed' if x >= 99.5 else ('🟡 In Progress' if x > 0 else '⚪ Not Started')
        )
        
        display_df = df_items[[
            'no', 'description', 'category', 'contract_amount',
            'planned_amount', 'actual_amount', 'Planned %', 
            'Actual %', 'Slippage %', 'Status'
        ]].copy()
        
        display_df.columns = [
            'Item No.', 'Description', 'Category', 'Contract (₱)',
            'Planned (₱)', '🟢 Actual (₱)', 'Planned (%)',
            '🟢 Actual (%)', 'Slippage (%)', 'Status'
        ]
        
        # Display editable table
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            key=f"{prefix}_data_editor",
            column_config={
                "Item No.": st.column_config.TextColumn("Item No.", width="small", disabled=True),
                "Description": st.column_config.TextColumn("Description", width="large", disabled=True),
                "Category": st.column_config.TextColumn("Category", width="small", disabled=True),
                "Contract (₱)": st.column_config.NumberColumn("Contract (₱)", format="₱%.2f", disabled=True),
                "Planned (₱)": st.column_config.NumberColumn("Planned (₱)", format="₱%.2f", disabled=True),
                "🟢 Actual (₱)": st.column_config.NumberColumn("🟢 Actual (₱)", min_value=0, step=10000, format="₱%.2f"),
                "Planned (%)": st.column_config.NumberColumn("Planned (%)", format="%.2f", disabled=True),
                "🟢 Actual (%)": st.column_config.NumberColumn("🟢 Actual (%)", min_value=0.0, max_value=100.0, step=0.5, format="%.2f"),
                "Slippage (%)": st.column_config.NumberColumn("Slippage (%)", format="%+.2f", disabled=True),
                "Status": st.column_config.TextColumn("Status", disabled=True),
            }
        )
        
                # Add TOTAL ROW - FIXED formatting
        st.markdown("---")
        st.markdown("### 📊 Summary Totals")
        
        total_contract = sum(df_items['contract_amount'])
        total_planned = sum(df_items['planned_amount'])
        total_actual = sum(df_items['actual_amount'])
        total_planned_pct = (total_planned / total_contract) * 100
        total_actual_pct = (total_actual / total_contract) * 100
        
        # Format numbers in millions
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Contract", f"₱{total_contract/1_000_000:.2f}M")
        with col2:
            st.metric("Total Planned", f"₱{total_planned/1_000_000:.2f}M", f"{total_planned_pct:.2f}%")
        with col3:
            st.metric("🟢 Total Actual", f"₱{total_actual/1_000_000:.2f}M", f"{total_actual_pct:.2f}%")
        with col4:
            st.metric("Variance", f"₱{(total_actual - total_planned)/1_000_000:+.2f}M")
        with col5:
            st.metric("Overall Progress", f"{total_actual_pct:.2f}%")
        
        # Save button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 SAVE ALL CHANGES", type="primary", use_container_width=True, key=f"{prefix}_save"):
                for idx, row in edited_df.iterrows():
                    for original_item in work_items:
                        if original_item['no'] == row['Item No.']:
                            original_item['actual_amount'] = row['🟢 Actual (₱)']
                            break
                st.session_state[f'{prefix}work_items'] = work_items
                st.success("✅ All changes saved! Progress recalculated.")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All to Zero", use_container_width=True, key=f"{prefix}_reset"):
                for item in work_items:
                    item['actual_amount'] = 0
                st.session_state[f'{prefix}work_items'] = work_items
                st.success("✅ Reset complete. Ready for new data entry.")
                st.rerun()
        
        with col3:
            st.caption(f"📊 Overall Progress: {total_actual_pct:.2f}% | Total Cost: ₱{total_actual:,.2f}")
    
    st.markdown("---")
    
    # ============================================================
    # SUMMARY STATISTICS
    # ============================================================
    
    st.markdown("### 📊 Progress Summary by Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    completed_items = len([i for i in work_items if (i['actual_amount']/i['contract_amount'])*100 >= 99.5])
    in_progress = len([i for i in work_items if 0 < (i['actual_amount']/i['contract_amount'])*100 < 99.5])
    not_started = len([i for i in work_items if i['actual_amount'] == 0])
    
    with col1:
        st.metric("✅ Completed", completed_items)
    with col2:
        st.metric("🟡 In Progress", in_progress)
    with col3:
        st.metric("⚪ Not Started", not_started)
    with col4:
        st.metric("📦 Total Items", len(work_items))
    
    st.markdown("---")
    
    # ============================================================
    # EXPORT OPTIONS
    # ============================================================
    
    st.markdown("### 📎 Export Data")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Export Work Items to CSV", use_container_width=True):
            export_df = pd.DataFrame(work_items)
            csv = export_df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV", 
                data=csv, 
                file_name=f"mpcfs_{component}_work_items_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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


def show_climate_projections():
    """Display Climate Change Projections from DOST data"""
    
    st.markdown("### 📊 Climate Change Projections")
    st.caption("Future climate scenarios based on DOST-PAGASA projections")
    
    proj_tab1, proj_tab2, proj_tab3, proj_tab4 = st.tabs([
        "🌡️ Temperature Projections",
        "🌧️ Rainfall Projections",
        "⚡ Extreme Events",
        "📝 Narrative Analysis"
    ])
    
    with proj_tab1:
        show_temperature_projections()
    
    with proj_tab2:
        show_rainfall_projections()
    
    with proj_tab3:
        show_extreme_events_projections()
    
    with proj_tab4:
        show_projection_narrative()


def show_temperature_projections():
    """Display temperature projections"""
    
    st.markdown("#### 🌡️ Temperature Projections")
    st.caption("Projected changes in temperature based on DOST-PAGASA data")
    
    with st.expander("📊 Input Projection Data (DOST)", expanded=False):
        with st.form("temp_projection_form"):
            st.markdown("**Baseline (1971-2000)**")
            col1, col2 = st.columns(2)
            with col1:
                baseline_temp_avg = st.number_input("Average Temperature (°C)", value=22.1, step=0.1)
            with col2:
                baseline_hot_nights = st.number_input("Hot Nights per Year", value=15, step=1)
            
            st.markdown("**Future Projections (2020-2050)**")
            col1, col2 = st.columns(2)
            with col1:
                future_temp_avg = st.number_input("Future Average Temp (°C)", value=23.8, step=0.1)
            with col2:
                future_hot_nights = st.number_input("Future Hot Nights per Year", value=45, step=1)
            
            scenario = st.selectbox("Climate Scenario", ["RCP 4.5 (Moderate)", "RCP 8.5 (High Emissions)"])
            
            submitted = st.form_submit_button("💾 Save Projection Data")
            
            if submitted:
                st.session_state.climate_projections["temperature"] = {
                    "baseline": {"mean": baseline_temp_avg, "hot_nights": baseline_hot_nights},
                    "near_term": {"mean": future_temp_avg, "hot_nights": future_hot_nights},
                    "scenario": scenario,
                    "updated_at": datetime.now().isoformat()
                }
                st.success("✅ Temperature projection data saved!")
                st.rerun()
    
    temp_data = st.session_state.climate_projections.get("temperature", {})
    
    if temp_data:
        periods = ["Baseline\n(1971-2000)", "Near-term\n(2020-2050)"]
        mean_temps = [temp_data.get("baseline", {}).get("mean", 0), temp_data.get("near_term", {}).get("mean", 0)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=periods, y=mean_temps, text=mean_temps, textposition='outside',
                              marker_color=['#3498db', '#e74c3c']))
        fig.update_layout(title='Temperature Projections (°C)', xaxis_title='Period', yaxis_title='Temperature (°C)')
        st.plotly_chart(fig, use_container_width=True)
        
        hot_nights = [temp_data.get("baseline", {}).get("hot_nights", 0), temp_data.get("near_term", {}).get("hot_nights", 0)]
        fig2 = px.bar(x=periods, y=hot_nights, title='Hot Nights per Year', color=hot_nights, color_continuous_scale='Reds')
        st.plotly_chart(fig2, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            temp_increase = temp_data.get("near_term", {}).get("mean", 0) - temp_data.get("baseline", {}).get("mean", 0)
            st.metric("Temperature Increase", f"+{temp_increase:.1f}°C")
        with col2:
            nights_increase = temp_data.get("near_term", {}).get("hot_nights", 0) - temp_data.get("baseline", {}).get("hot_nights", 0)
            st.metric("Additional Hot Nights", f"+{nights_increase} days/year")
    else:
        st.info("No temperature projection data yet. Use the form above to input DOST data.")


def show_rainfall_projections():
    """Display rainfall projections"""
    
    st.markdown("#### 🌧️ Rainfall Projections")
    st.caption("Projected changes in rainfall patterns")
    
    with st.expander("📊 Input Rainfall Projection Data", expanded=False):
        with st.form("rainfall_projection_form"):
            st.markdown("**Baseline (1971-2000)**")
            baseline_annual_rainfall = st.number_input("Annual Rainfall (mm)", value=2500, step=50)
            baseline_rainy_days = st.number_input("Rainy Days per Year", value=150, step=5)
            
            st.markdown("**Future Projections (2020-2050)**")
            future_annual_rainfall = st.number_input("Future Annual Rainfall (mm)", value=2750, step=50)
            future_rainy_days = st.number_input("Future Rainy Days per Year", value=165, step=5)
            
            submitted = st.form_submit_button("💾 Save Rainfall Data")
            
            if submitted:
                st.session_state.climate_projections["rainfall"] = {
                    "baseline": {"annual": baseline_annual_rainfall, "rainy_days": baseline_rainy_days},
                    "near_term": {"annual": future_annual_rainfall, "rainy_days": future_rainy_days},
                    "updated_at": datetime.now().isoformat()
                }
                st.success("✅ Rainfall projection data saved!")
                st.rerun()
    
    rain_data = st.session_state.climate_projections.get("rainfall", {})
    
    if rain_data:
        periods = ["Baseline", "Near-term"]
        annual_rainfall = [rain_data.get("baseline", {}).get("annual", 0), rain_data.get("near_term", {}).get("annual", 0)]
        fig = px.bar(x=periods, y=annual_rainfall, title='Annual Rainfall (mm)', color=annual_rainfall)
        st.plotly_chart(fig, use_container_width=True)
        
        rainy_days = [rain_data.get("baseline", {}).get("rainy_days", 0), rain_data.get("near_term", {}).get("rainy_days", 0)]
        fig2 = px.bar(x=periods, y=rainy_days, title='Rainy Days per Year', color=rainy_days)
        st.plotly_chart(fig2, use_container_width=True)
        
        rain_increase = rain_data.get("near_term", {}).get("annual", 0) - rain_data.get("baseline", {}).get("annual", 0)
        days_increase = rain_data.get("near_term", {}).get("rainy_days", 0) - rain_data.get("baseline", {}).get("rainy_days", 0)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Rainfall Change", f"+{rain_increase:.0f} mm")
        with col2:
            st.metric("Additional Rainy Days", f"+{days_increase} days/year")
    else:
        st.info("No rainfall projection data yet.")


def show_extreme_events_projections():
    """Display extreme events projections"""
    
    st.markdown("#### ⚡ Extreme Events Projections")
    st.caption("Projected changes in extreme weather events")
    
    with st.expander("📊 Input Extreme Events Data", expanded=False):
        with st.form("extreme_events_form"):
            st.markdown("**Baseline Frequency (1971-2000)**")
            baseline_typhoons = st.number_input("Typhoons per Year", value=3, step=1)
            baseline_landslides = st.number_input("Landslide Events per Year", value=4, step=1)
            
            st.markdown("**Future Projections (2020-2050)**")
            future_typhoons = st.number_input("Future Typhoons per Year", value=4, step=1)
            future_landslides = st.number_input("Future Landslide Events per Year", value=7, step=1)
            
            submitted = st.form_submit_button("💾 Save Extreme Events Data")
            
            if submitted:
                st.session_state.climate_projections["extreme_events"] = {
                    "baseline": {"typhoons": baseline_typhoons, "landslides": baseline_landslides},
                    "near_term": {"typhoons": future_typhoons, "landslides": future_landslides},
                    "updated_at": datetime.now().isoformat()
                }
                st.success("✅ Extreme events data saved!")
                st.rerun()
    
    extreme_data = st.session_state.climate_projections.get("extreme_events", {})
    
    if extreme_data:
        events = ['Typhoons', 'Landslides']
        baseline_values = [extreme_data.get("baseline", {}).get("typhoons", 0), extreme_data.get("baseline", {}).get("landslides", 0)]
        future_values = [extreme_data.get("near_term", {}).get("typhoons", 0), extreme_data.get("near_term", {}).get("landslides", 0)]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Baseline', x=events, y=baseline_values, marker_color='#3498db'))
        fig.add_trace(go.Bar(name='Near-term (2020-2050)', x=events, y=future_values, marker_color='#e74c3c'))
        fig.update_layout(title='Extreme Events Frequency', barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            typhoon_increase = future_values[0] - baseline_values[0]
            st.metric("Typhoon Increase", f"+{typhoon_increase} per year")
        with col2:
            landslide_increase = future_values[1] - baseline_values[1]
            st.metric("Landslide Increase", f"+{landslide_increase} per year")
    else:
        st.info("No extreme events data yet.")


def show_projection_narrative():
    """Generate narrative from projection data"""
    
    st.markdown("#### 📝 Climate Projection Narrative")
    st.caption("What these projections mean for Mountain Province")
    
    temp_data = st.session_state.climate_projections.get("temperature", {})
    rain_data = st.session_state.climate_projections.get("rainfall", {})
    extreme_data = st.session_state.climate_projections.get("extreme_events", {})
    
    if temp_data or rain_data or extreme_data:
        st.markdown("### 🔍 Analysis of Climate Projections")
        
        if temp_data:
            baseline_temp = temp_data.get("baseline", {}).get("mean", 0)
            future_temp = temp_data.get("near_term", {}).get("mean", 0)
            temp_increase = future_temp - baseline_temp
            
            st.markdown(f"""
            ### 🌡️ Temperature
            
            Based on DOST-PAGASA projections, Mountain Province is expected to experience a temperature increase 
            of **{temp_increase:.1f}°C** by 2050.
            
            **What this means:**
            - Higher temperatures will affect agriculture and water resources
            - Increased energy demand for cooling
            - Higher risk of heat-related illnesses
            """)
        
        if rain_data:
            baseline_rain = rain_data.get("baseline", {}).get("annual", 0)
            future_rain = rain_data.get("near_term", {}).get("annual", 0)
            rain_increase = future_rain - baseline_rain
            
            st.markdown(f"""
            ### 🌧️ Rainfall Patterns
            
            Annual rainfall is projected to increase by **{rain_increase:.0f} mm** by 2050.
            
            **What this means:**
            - More intense rainfall events increase landslide and flood risks
            - Agriculture faces both more wet days and more intense rainfall
            - Infrastructure needs to adapt to heavier rainfall
            """)
        
        if extreme_data:
            baseline_typhoons = extreme_data.get("baseline", {}).get("typhoons", 0)
            future_typhoons = extreme_data.get("near_term", {}).get("typhoons", 0)
            typhoon_increase = future_typhoons - baseline_typhoons
            
            st.markdown(f"""
            ### ⚡ Extreme Events
            
            Typhoons are projected to increase from {baseline_typhoons:.0f} to {future_typhoons:.0f} per year.
            
            **What this means:**
            - More frequent disaster declarations
            - Greater strain on emergency services
            - Increased need for early warning systems
            """)
        
        st.markdown("### 🎯 Recommended Adaptation Actions")
        st.markdown("""
        - Strengthen road drainage systems for increased rainfall
        - Promote climate-resilient crop varieties
        - Enhance early warning systems
        - Prepare for increased heat-related illnesses
        """)
    else:
        st.info("No projection data available. Please input temperature, rainfall, and extreme events data first.")


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
    
    ### Expected Data Format:
    - Weekly progress percentages
    - Budget allocation
    - Target milestones
    - Actual accomplishments
    """)
    
    # Show a preview placeholder chart
    st.markdown("#### Preview (Awaiting Data)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[0, 0, 0, 0, 0], mode='lines+markers', name='Progress'))
    fig.update_layout(title=f"{component_name} Progress Preview", height=300, yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button(f"📤 Upload {component_name} Data", type="primary", use_container_width=True):
        st.success(f"✅ {component_name} data upload feature will be available soon!")

def show_mpcfs_gantt_updated():
    """Updated Gantt chart with Infrastructure components + Add/Edit for future components"""
    
    st.markdown("#### 📋 Project Gantt Chart & Timeline")
    st.caption("Track project milestones by Infrastructure sub-components")
    
    # Initialize session state for Gantt tasks if not exists
    if 'gantt_tasks' not in st.session_state:
        st.session_state.gantt_tasks = [
            # ============================================================
            # INFRASTRUCTURE COMPONENT - Active
            # ============================================================
            
            # Civil Works
            {"Component": "🏗️ Infrastructure", "SubComponent": "Civil Works", "Task": "Site Development & Preparation", "Start": "2024-04-01", "Finish": "2024-12-31", "Complete": 45.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Civil Works", "Task": "Foundation & Excavation", "Start": "2024-09-01", "Finish": "2025-03-31", "Complete": 60.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Civil Works", "Task": "Gravel Fill & Subbase", "Start": "2025-01-01", "Finish": "2025-06-30", "Complete": 40.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Civil Works", "Task": "PCC Pavement", "Start": "2025-04-01", "Finish": "2025-10-31", "Complete": 0.00, "status": "active"},
            
            # Structural
            {"Component": "🏗️ Infrastructure", "SubComponent": "Structural", "Task": "Reinforcing Steel Installation", "Start": "2024-10-01", "Finish": "2025-12-31", "Complete": 35.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Structural", "Task": "Structural Concrete Works", "Start": "2024-11-01", "Finish": "2026-03-31", "Complete": 30.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Structural", "Task": "Structural Steel Erection", "Start": "2025-04-01", "Finish": "2026-06-30", "Complete": 25.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Structural", "Task": "Formworks & Falseworks", "Start": "2025-01-01", "Finish": "2025-12-31", "Complete": 20.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Structural", "Task": "Metal Deck Panel Installation", "Start": "2025-06-01", "Finish": "2026-03-31", "Complete": 0.00, "status": "active"},
            
            # Architectural
            {"Component": "🏗️ Infrastructure", "SubComponent": "Architectural", "Task": "CHB Wall Construction", "Start": "2025-06-01", "Finish": "2026-06-30", "Complete": 10.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Architectural", "Task": "Plumbing & Sanitary", "Start": "2025-09-01", "Finish": "2026-09-30", "Complete": 5.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Architectural", "Task": "Ceiling & Finishing", "Start": "2026-01-01", "Finish": "2026-12-31", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Architectural", "Task": "Painting & Tiling", "Start": "2026-04-01", "Finish": "2027-03-31", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Architectural", "Task": "Doors & Windows Installation", "Start": "2026-07-01", "Finish": "2027-06-30", "Complete": 0.00, "status": "active"},
            
            # Electrical
            {"Component": "🏗️ Infrastructure", "SubComponent": "Electrical", "Task": "Conduits & Wiring", "Start": "2026-01-01", "Finish": "2026-12-31", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Electrical", "Task": "Panelboards & Breakers", "Start": "2026-06-01", "Finish": "2027-03-31", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Electrical", "Task": "Lighting Fixtures", "Start": "2026-09-01", "Finish": "2027-06-30", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Electrical", "Task": "Solar Panel System", "Start": "2027-01-01", "Finish": "2027-12-31", "Complete": 0.00, "status": "active"},
            
            # Mechanical
            {"Component": "🏗️ Infrastructure", "SubComponent": "Mechanical", "Task": "Fire Protection System", "Start": "2026-07-01", "Finish": "2027-06-30", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Mechanical", "Task": "Water Pumping System", "Start": "2026-10-01", "Finish": "2027-09-30", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Mechanical", "Task": "Generator Installation", "Start": "2027-04-01", "Finish": "2027-12-31", "Complete": 0.00, "status": "active"},
            
            # Equipment
            {"Component": "🏗️ Infrastructure", "SubComponent": "Equipment", "Task": "Furniture & Fixtures", "Start": "2027-07-01", "Finish": "2028-03-31", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Equipment", "Task": "Laboratory Equipment", "Start": "2027-10-01", "Finish": "2028-06-30", "Complete": 0.00, "status": "active"},
            {"Component": "🏗️ Infrastructure", "SubComponent": "Equipment", "Task": "AWS Installation", "Start": "2027-12-01", "Finish": "2028-08-31", "Complete": 0.00, "status": "active"},
            
            # ============================================================
            # CAPABILITY BUILDING COMPONENT - Coming Soon
            # ============================================================
            {"Component": "👨‍🌾 Capability Building", "SubComponent": "Training", "Task": "Training Needs Assessment", "Start": "2025-01-01", "Finish": "2025-06-30", "Complete": 0.00, "status": "pending"},
            {"Component": "👨‍🌾 Capability Building", "SubComponent": "Training", "Task": "Curriculum Development", "Start": "2025-07-01", "Finish": "2025-12-31", "Complete": 0.00, "status": "pending"},
            {"Component": "👨‍🌾 Capability Building", "SubComponent": "Training", "Task": "Farmer Training Program", "Start": "2026-01-01", "Finish": "2027-12-31", "Complete": 0.00, "status": "pending"},
            {"Component": "👨‍🌾 Capability Building", "SubComponent": "Extension", "Task": "Extension Services Setup", "Start": "2026-06-01", "Finish": "2027-06-30", "Complete": 0.00, "status": "pending"},
            
            # ============================================================
            # RESEARCH & EXTENSION COMPONENT - Coming Soon
            # ============================================================
            {"Component": "🔬 Research & Extension", "SubComponent": "Research", "Task": "Baseline Research Setup", "Start": "2025-04-01", "Finish": "2025-12-31", "Complete": 0.00, "status": "pending"},
            {"Component": "🔬 Research & Extension", "SubComponent": "Research", "Task": "Data Collection", "Start": "2026-01-01", "Finish": "2027-06-30", "Complete": 0.00, "status": "pending"},
            {"Component": "🔬 Research & Extension", "SubComponent": "Research", "Task": "Analysis & Documentation", "Start": "2027-07-01", "Finish": "2028-06-30", "Complete": 0.00, "status": "pending"},
            {"Component": "🔬 Research & Extension", "SubComponent": "Extension", "Task": "Extension Services Rollout", "Start": "2026-06-01", "Finish": "2028-12-31", "Complete": 0.00, "status": "pending"},
        ]
    
    # ============================================================
    # ADD/EDIT TASKS SECTION (for future components)
    # ============================================================
    
    with st.expander("➕ Add / Edit Tasks (for Capability Building & Research & Extension)", expanded=False):
        st.markdown("**Add New Task**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            new_component = st.selectbox("Component", ["👨‍🌾 Capability Building", "🔬 Research & Extension"])
        with col2:
            new_subcomponent = st.text_input("SubComponent", placeholder="e.g., Training, Research, Extension")
        with col3:
            new_task = st.text_input("Task Name", placeholder="Enter task description")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            new_start = st.date_input("Start Date", datetime(2025, 1, 1))
        with col2:
            new_finish = st.date_input("Finish Date", datetime(2025, 12, 31))
        with col3:
            new_complete = st.number_input("Complete (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0)
        with col4:
            new_status = st.selectbox("Status", ["pending", "active"])
        
        if st.button("➕ Add Task", type="primary", use_container_width=True):
            if new_task:
                st.session_state.gantt_tasks.append({
                    "Component": new_component,
                    "SubComponent": new_subcomponent if new_subcomponent else "General",
                    "Task": new_task,
                    "Start": new_start.strftime("%Y-%m-%d"),
                    "Finish": new_finish.strftime("%Y-%m-%d"),
                    "Complete": new_complete,
                    "status": new_status
                })
                st.success(f"✅ Task '{new_task}' added!")
                st.rerun()
        
        st.markdown("---")
        st.markdown("**Edit Existing Tasks**")
        
        # Editable task table for future components - FIXED date handling
        pending_tasks = [t for t in st.session_state.gantt_tasks if t['Component'] in ["👨‍🌾 Capability Building", "🔬 Research & Extension"]]
        if pending_tasks:
            df_pending = pd.DataFrame(pending_tasks)
            
            # Convert date strings to date objects for editing
            df_pending['Start'] = pd.to_datetime(df_pending['Start']).dt.date
            df_pending['Finish'] = pd.to_datetime(df_pending['Finish']).dt.date
            
            edited_pending = st.data_editor(
                df_pending[['Component', 'SubComponent', 'Task', 'Start', 'Finish', 'Complete']],
                use_container_width=True,
                hide_index=True,
                key="edit_pending_tasks",
                column_config={
                    "Component": st.column_config.TextColumn("Component", disabled=True),
                    "SubComponent": st.column_config.TextColumn("SubComponent"),
                    "Task": st.column_config.TextColumn("Task"),
                    "Start": st.column_config.DateColumn("Start Date"),
                    "Finish": st.column_config.DateColumn("Finish Date"),
                    "Complete": st.column_config.NumberColumn("Complete (%)", min_value=0, max_value=100, step=5),
                }
            )
            
            if st.button("💾 Save Task Changes", use_container_width=True):
                # Update tasks - convert dates back to string format
                for idx, row in edited_pending.iterrows():
                    if idx < len(pending_tasks):
                        for original in st.session_state.gantt_tasks:
                            if original['Task'] == pending_tasks[idx]['Task'] and original['Component'] == pending_tasks[idx]['Component']:
                                original['SubComponent'] = row['SubComponent']
                                original['Task'] = row['Task']
                                original['Start'] = row['Start'].strftime("%Y-%m-%d")
                                original['Finish'] = row['Finish'].strftime("%Y-%m-%d")
                                original['Complete'] = row['Complete']
                                break
                st.success("✅ Tasks updated!")
                st.rerun()
        else:
            st.info("No pending tasks. Add tasks using the form above.")
    
    st.markdown("---")
    
    # ============================================================
    # DISPLAY GANTT CHART (All components)
    # ============================================================
    
    st.markdown("### 📊 Project Timeline")
    
    # Filter to show Infrastructure as active, others as planned
    all_tasks = st.session_state.gantt_tasks
    
    df_tasks = pd.DataFrame(all_tasks)
    df_tasks["Start"] = pd.to_datetime(df_tasks["Start"])
    df_tasks["Finish"] = pd.to_datetime(df_tasks["Finish"])
    
    # Color mapping
    colors = {
        "🏗️ Infrastructure": "#2ecc71",
        "👨‍🌾 Capability Building": "#3498db",
        "🔬 Research & Extension": "#9b59b6"
    }
    
    # Create figure
    fig = go.Figure()
    
    for i, task in df_tasks.iterrows():
        duration = (task["Finish"] - task["Start"]).days
        color = colors.get(task["Component"], "#95a5a6")
        
        # Add opacity for pending tasks
        opacity = 0.8 if task.get('status') == 'active' else 0.4
        
        fig.add_trace(go.Bar(
            x=[duration],
            y=[f"{task['Component']} - {task['SubComponent']}: {task['Task']}"],
            orientation='h',
            marker=dict(color=color, opacity=opacity),
            text=f"{task['Complete']:.0f}% Complete" if task['Complete'] > 0 else "Pending",
            textposition='outside',
            hoverinfo='text',
            hovertext=f"Component: {task['Component']}<br>Task: {task['Task']}<br>Start: {task['Start'].strftime('%Y-%m-%d')}<br>Finish: {task['Finish'].strftime('%Y-%m-%d')}<br>Progress: {task['Complete']:.0f}%"
        ))
    
    fig.update_layout(
        title="Project Timeline by Component",
        xaxis_title="Duration (Days)",
        height=700,
        showlegend=False,
        hovermode='closest'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # ============================================================
    # TASK STATUS TABLE
    # ============================================================
    
    st.markdown("### 📋 Task Status by Component")
    
    # Infrastructure Component (Active)
    st.markdown("#### 🏗️ INFRASTRUCTURE COMPONENT (Active)")
    infra_tasks = [t for t in all_tasks if t['Component'] == "🏗️ Infrastructure"]
    
    # Group by SubComponent
    subcomponents = ["Civil Works", "Structural", "Architectural", "Electrical", "Mechanical", "Equipment"]
    for subcomp in subcomponents:
        sub_tasks = [t for t in infra_tasks if t.get('SubComponent') == subcomp]
        if sub_tasks:
            st.markdown(f"**{subcomp}**")
            for task in sub_tasks:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"📌 {task['Task']}")
                with col2:
                    st.markdown(f"{task['Complete']:.0f}% Complete")
                with col3:
                    if task['Complete'] >= 90:
                        st.success("✅ Completed")
                    elif task['Complete'] >= 50:
                        st.warning("🟡 In Progress")
                    elif task['Complete'] > 0:
                        st.info("📋 Started")
                    else:
                        st.info("⏳ Not Started")
            st.markdown("---")
    
    # Capability Building Component (Planned)
    st.markdown("#### 👨‍🌾 CAPABILITY BUILDING COMPONENT (Planned - Data Coming Soon)")
    cap_tasks = [t for t in all_tasks if t['Component'] == "👨‍🌾 Capability Building"]
    if cap_tasks:
        for task in cap_tasks:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"📌 {task['Task']}")
            with col2:
                st.markdown(f"{task['Complete']:.0f}% Complete" if task['Complete'] > 0 else "⏳ Pending")
            with col3:
                st.info("📋 Planned for Q2 2025")
        st.markdown("---")
    else:
        st.info("No tasks added yet. Use the 'Add / Edit Tasks' section above.")
    
    # Research & Extension Component (Planned)
    st.markdown("#### 🔬 RESEARCH & EXTENSION COMPONENT (Planned - Data Coming Soon)")
    res_tasks = [t for t in all_tasks if t['Component'] == "🔬 Research & Extension"]
    if res_tasks:
        for task in res_tasks:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"📌 {task['Task']}")
            with col2:
                st.markdown(f"{task['Complete']:.0f}% Complete" if task['Complete'] > 0 else "⏳ Pending")
            with col3:
                st.info("📋 Planned for Q2 2025")
        st.markdown("---")
    else:
        st.info("No tasks added yet. Use the 'Add / Edit Tasks' section above.")
    
    # ============================================================
    # SUMMARY
    # ============================================================
    
    st.markdown("### 📊 Gantt Chart Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_tasks = len(all_tasks)
    active_tasks = len([t for t in all_tasks if t.get('status') == 'active'])
    pending_tasks_count = len([t for t in all_tasks if t.get('status') == 'pending'])
    completed_tasks = len([t for t in all_tasks if t['Complete'] >= 95])
    
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Active (Infrastructure)", active_tasks)
    with col3:
        st.metric("Planned (Future)", pending_tasks_count)
    with col4:
        st.metric("Completed", completed_tasks)

def show_mpcfs_dashboard():
    """Project dashboard with key metrics and progress tracking"""
    
    st.markdown("#### Project Dashboard")
    
    # Get real infrastructure data
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    
    # Progress by component with 2 decimal places
    components_data = {
        "Component": [
            "Climate Field School Establishment",
            "Farmer Training & Capacity Building",
            "Demonstration Farms",
            "Research & Documentation",
            "Knowledge Management",
            "Monitoring & Evaluation"
        ],
        "Progress": [infra_progress, 48.00, 52.00, 35.00, 28.00, 42.00],
        "Target": [70.00, 50.00, 55.00, 40.00, 35.00, 45.00]
    }
    
    df = pd.DataFrame(components_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Actual Progress", x=df["Component"], y=df["Progress"], 
                          text=[f"{x:.2f}%" for x in df["Progress"]], textposition='outside',
                          marker_color="#2ecc71"))
    fig.add_trace(go.Bar(name="Target", x=df["Component"], y=df["Target"],
                          text=[f"{x:.2f}%" for x in df["Target"]], textposition='outside',
                          marker_color="#f39c12"))
    fig.update_layout(title="Progress by Component", height=400, barmode="group")
    st.plotly_chart(fig, use_container_width=True)
    
    # Quarterly progress with 2 decimal places
    st.markdown("#### Quarterly Progress Tracking")
    quarters = ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025"]
    progress = [15.00, 28.00, 35.00, 40.00, infra_progress]
    
    fig = px.line(x=quarters, y=progress, markers=True, title="Overall Project Progress Trend")
    fig.update_layout(xaxis_title="Quarter", yaxis_title="Progress (%)", yaxis_range=[0, 100])
    fig.update_traces(text=[f"{x:.2f}%" for x in progress], textposition="top center")
    st.plotly_chart(fig, use_container_width=True)
    
    # Key achievements
    st.markdown("#### Key Achievements")
    achievements = [
        f"✅ Climate Field School facility construction at {infra_progress:.2f}% completion",
        "✅ 1,247 farmers trained in climate-resilient agriculture techniques",
        "✅ 3 demonstration farms established across Paracelis",
        "✅ Baseline survey completed with 2,500+ farmer respondents",
        "✅ Project Management Office fully operational"
    ]
    for achievement in achievements:
        st.markdown(achievement)

def show_mpcfs_report_generator_updated():
    """Generate PDF reports with issues tracking and S-Curve - FIXED"""
    
    st.markdown("#### 📄 Report Generator")
    st.caption("Generate PDF reports with progress data, issues log, and S-Curve")
    
    # Initialize issues log if not exists
    if 'mpcfs_issues' not in st.session_state:
        st.session_state.mpcfs_issues = []
    
    # Get current progress data
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    total_budget = 249_040_900.00
    total_cost = st.session_state.get('infrastructure_cost', 64_000_000)
    if isinstance(total_cost, list):
        total_cost = next((x for x in reversed(total_cost) if x > 0), 64_000_000)
    
    # ============================================================
    # ISSUES MANAGEMENT SECTION - FIXED
    # ============================================================
    
    st.markdown("### ⚠️ Issues & Concerns Log")
    st.caption("Track project issues, attach photos, and link to work items")
    
    # Add New Issue Form - FIXED: Clear form after save
    with st.expander("➕ Add New Issue", expanded=False):
        with st.form(key="add_issue_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                issue_title = st.text_input("Issue Title", placeholder="e.g., Weather delay at foundation site", key="issue_title_input")
                priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"], key="issue_priority")
                
                # Get work items for linking
                work_items = st.session_state.get('infrastructure_work_items', [])
                work_item_options = ["None"] + [f"{item.get('no', '')} - {item.get('description', '')[:50]}" for item in work_items]
                work_item_link = st.selectbox("Linked Work Item", work_item_options, key="issue_work_item")
                
            with col2:
                reported_by = st.selectbox("Reported By", ["Project Engineer", "Finance Officer", "Project Manager", "Other"], key="issue_reported_by")
                issue_date = st.date_input("Date Reported", datetime.now().date(), key="issue_date")
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], key="issue_status")
            
            issue_description = st.text_area("Description", placeholder="Detailed description of the issue...", key="issue_description")
            action_taken = st.text_area("Action Taken / Resolution", placeholder="What has been done to address this?", key="issue_action")
            
            # Photo upload
            issue_photo = st.file_uploader("Attach Photo", type=['jpg', 'jpeg', 'png', 'gif'], key="issue_photo")
            
            submitted = st.form_submit_button("💾 Save Issue", use_container_width=True)
            
            if submitted and issue_title:
                new_issue = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": issue_title,
                    "description": issue_description,
                    "priority": priority,
                    "work_item": work_item_link if work_item_link != "None" else None,
                    "reported_by": reported_by,
                    "date": issue_date.isoformat(),
                    "status": status,
                    "action_taken": action_taken,
                    "photo": issue_photo.name if issue_photo else None,
                    "created_at": datetime.now().isoformat()
                }
                
                # Save photo if uploaded
                if issue_photo:
                    os.makedirs("mpcfs_issues", exist_ok=True)
                    with open(f"mpcfs_issues/{issue_photo.name}", "wb") as f:
                        f.write(issue_photo.getbuffer())
                
                st.session_state.mpcfs_issues.append(new_issue)
                st.success(f"✅ Issue '{issue_title}' added!")
                # Form clears automatically due to clear_on_submit=True
    
    # Display Issues Table
    if st.session_state.mpcfs_issues:
        st.markdown("#### 📋 Current Issues Log")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "🔴 High", "🟡 Medium", "🟢 Low"])
        with col3:
            show_resolved = st.checkbox("Show Resolved Issues", value=True)
        
        # Filter issues
        filtered_issues = st.session_state.mpcfs_issues
        if status_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['status'] == status_filter]
        if priority_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['priority'] == priority_filter]
        if not show_resolved:
            filtered_issues = [i for i in filtered_issues if i['status'] not in ["Resolved", "Closed"]]
        
        # Display as table
        if filtered_issues:
            df_issues = pd.DataFrame(filtered_issues)
            display_cols = ['title', 'priority', 'status', 'reported_by', 'date', 'work_item']
            available_cols = [c for c in display_cols if c in df_issues.columns]
            st.dataframe(df_issues[available_cols], use_container_width=True, hide_index=True)
            
            # Update issue status section
            st.markdown("---")
            st.markdown("#### Update Issue Status")
            
            issue_to_update = st.selectbox("Select Issue to Update", [f"{i['title']} (ID: {i['id']})" for i in filtered_issues])
            if issue_to_update:
                selected_id = int(issue_to_update.split("ID: ")[1].rstrip(")"))
                selected_issue = next((i for i in st.session_state.mpcfs_issues if i['id'] == selected_id), None)
                
                if selected_issue:
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                                  index=["Open", "In Progress", "Resolved", "Closed"].index(selected_issue['status']))
                    with col2:
                        new_action = st.text_area("Update Action Taken", value=selected_issue.get('action_taken', ''))
                    
                    if st.button("Update Issue Status"):
                        for i in st.session_state.mpcfs_issues:
                            if i['id'] == selected_id:
                                i['status'] = new_status
                                i['action_taken'] = new_action
                                break
                        st.success("✅ Issue updated!")
                        st.rerun()
        else:
            st.info("No issues match the selected filters.")
    else:
        st.info("No issues logged yet. Click 'Add New Issue' to get started.")
    
    st.markdown("---")
    
    # ============================================================
    # REPORT GENERATION - FIXED with S-Curve image
    # ============================================================
    
    st.markdown("### 📄 Generate PDF Report")
    
    col1, col2 = st.columns(2)
    with col1:
        report_type = st.selectbox("Select Report Type", [
            "📊 Progress Report",
            "💰 Financial Report", 
            "📋 Accomplishment Report",
            "📑 Liquidation Report",
            "📈 Monitoring & Evaluation Report",
            "📚 Consolidated Progress Report"
        ])
    
    with col2:
        report_period = st.selectbox("Reporting Period", [
            "January - March 2025",
            "April - June 2025", 
            "July - September 2025",
            "October - December 2025",
            "Annual Report 2025",
            "January - March 2026 (Current)"
        ])
    
    include_issues = st.checkbox("Include Open Issues in Report", value=True)
    include_chart = st.checkbox("Include S-Curve Chart", value=True)
    
    # Generate Report Button
    if st.button("📄 Generate Report Preview", type="primary", use_container_width=True):
        
        open_issues = [i for i in st.session_state.mpcfs_issues if i['status'] not in ["Resolved", "Closed"]]
        
        # Create S-Curve chart as base64 image if requested
        chart_base64 = ""
        if include_chart:
            try:
                # Create a simple S-Curve figure
                weeks = list(range(1, 53))
                target_curve = [min(25.75 * w / 52, 25.75) for w in weeks]
                actual_curve = [min(infra_progress * w / 52, infra_progress) for w in weeks]
                
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(weeks, target_curve, 'b--', label='Target Plan', linewidth=2)
                ax.plot(weeks, actual_curve, 'g-', label='Actual Progress', linewidth=2)
                ax.axvline(x=40, color='r', linestyle='--', alpha=0.5)
                ax.set_xlabel('Week')
                ax.set_ylabel('Progress (%)')
                ax.set_title('Project Progress S-Curve')
                ax.legend()
                ax.grid(True, alpha=0.3)
                ax.set_ylim(0, 100)
                
                # Save to bytes
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
                buf.seek(0)
                chart_base64 = base64.b64encode(buf.getvalue()).decode()
                plt.close()
            except:
                chart_base64 = ""
        
        # Create HTML report content
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>MPCFS Progress Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    margin: 40px;
                    color: #333;
                    line-height: 1.6;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #2ecc71;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .title {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .subtitle {{
                    font-size: 14px;
                    color: #7f8c8d;
                    margin-top: 5px;
                }}
                .as-of {{
                    font-size: 12px;
                    color: #e74c3c;
                    margin-top: 10px;
                    font-weight: bold;
                }}
                .section {{
                    margin-bottom: 30px;
                    page-break-inside: avoid;
                }}
                .section-title {{
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #ecf0f1;
                    padding: 10px;
                    margin-bottom: 15px;
                    border-left: 4px solid #2ecc71;
                }}
                .kpi-grid {{
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                .kpi-card {{
                    border: 1px solid #ddd;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    background-color: #f9f9f9;
                }}
                .kpi-value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .kpi-label {{
                    font-size: 12px;
                    color: #7f8c8d;
                    margin-top: 5px;
                }}
                .table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                .table th, .table td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }}
                .table th {{
                    background-color: #2ecc71;
                    color: white;
                }}
                .issue-high {{
                    border-left: 4px solid #e74c3c;
                    padding-left: 10px;
                    margin-bottom: 10px;
                    background-color: #fef9f9;
                }}
                .issue-medium {{
                    border-left: 4px solid #f39c12;
                    padding-left: 10px;
                    margin-bottom: 10px;
                    background-color: #fffaf5;
                }}
                .issue-low {{
                    border-left: 4px solid #27ae60;
                    padding-left: 10px;
                    margin-bottom: 10px;
                    background-color: #f5fff5;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 10px;
                    color: #7f8c8d;
                }}
                .chart-container {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .chart-image {{
                    max-width: 100%;
                    height: auto;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">MOUNTAIN PROVINCE CLIMATE FIELD SCHOOL (MPCFS)</div>
                <div class="subtitle">{report_type} | {report_period}</div>
                <div class="subtitle">Bacarri, Paracelis, Mountain Province</div>
                <div class="as-of">📍 As of: March 31, 2026</div>
                <div class="subtitle">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">📊 Executive Summary</div>
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-value">{infra_progress:.2f}%</div>
                        <div class="kpi-label">Infrastructure Progress</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-value">₱{total_cost:,.2f}</div>
                        <div class="kpi-label">Cost Utilized</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-value">{len(open_issues)}</div>
                        <div class="kpi-label">Open Issues</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">💰 Financial Summary</div>
                <table class="table">
                    <tr><th>Item</th><th>Amount (₱)</th></tr>
                    <tr><td>Total Contract Amount</td><td>{total_budget:,.2f}</td></tr>
                    <tr><td>Actual Cost Utilized</td><td>{total_cost:,.2f}</td></tr>
                    <tr><td>Remaining Budget</td><td>{total_budget - total_cost:,.2f}</td></tr>
                    <tr><td>Financial Utilization Rate</td><td>{(total_cost/total_budget)*100:.1f}%</td></tr>
                </table>
            </div>
        """
        
        if include_chart and chart_base64:
            report_html += f"""
            <div class="section">
                <div class="section-title">📈 S-Curve Chart</div>
                <div class="chart-container">
                    <img src="data:image/png;base64,{chart_base64}" class="chart-image">
                </div>
            </div>
            """
        
        if include_issues and open_issues:
            report_html += """
            <div class="section">
                <div class="section-title">⚠️ Open Issues & Concerns</div>
            """
            for issue in open_issues:
                priority_class = "issue-high" if "High" in issue['priority'] else ("issue-medium" if "Medium" in issue['priority'] else "issue-low")
                report_html += f"""
                <div class="{priority_class}">
                    <strong>{issue['title']}</strong><br>
                    <strong>Priority:</strong> {issue['priority']} | <strong>Status:</strong> {issue['status']}<br>
                    <strong>Reported:</strong> {issue['reported_by']} on {issue['date'][:10]}<br>
                    <strong>Description:</strong> {issue['description']}<br>
                    <strong>Action Taken:</strong> {issue.get('action_taken', 'None yet')}
                </div>
                """
            report_html += "</div>"
        
        report_html += f"""
            <div class="section">
                <div class="section-title">🎯 Key Accomplishments</div>
                <ul>
                    <li>Infrastructure component at {infra_progress:.2f}% completion as of March 31, 2026</li>
                    <li>Foundation and structural works progressing</li>
                    <li>Project management systems fully operational</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>This is an official report generated by the INDC System - MPCFS Module</p>
                <p>Mountain Province Disaster Risk Reduction and Management Council</p>
            </div>
        </body>
        </html>
        """
        
        # Display preview
        st.markdown("---")
        st.markdown("### 📋 Report Preview")
        st.components.v1.html(report_html, height=600, scrolling=True)
        
        # Download options
        st.markdown("### 📥 Download Report")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📄 Download as HTML (Print to PDF)",
                data=report_html,
                file_name=f"MPCFS_{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        with col2:
            st.info("💡 **How to save as PDF:**\n1. Click 'Download as HTML'\n2. Open the HTML file in browser\n3. Press Ctrl+P (or Cmd+P on Mac)\n4. Select 'Save as PDF'\n5. Click Save")
        
        st.success(f"✅ Report generated successfully with {len(open_issues)} open issues included!")

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

            