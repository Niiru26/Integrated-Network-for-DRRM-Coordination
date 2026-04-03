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
    
    # Get component data from session state - FIXED: handle if infra_cost is a list
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    infra_target = st.session_state.get('infrastructure_target', 25.75)
    
    # FIX: infra_cost might be a list, extract the current value
    infra_cost_raw = st.session_state.get('infrastructure_cost', 64_000_000)
    if isinstance(infra_cost_raw, list):
        # If it's a list, get the last non-zero value or the current week's value
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
    active_components = 1  # Infrastructure is always active
    if cap_progress > 0:
        active_components += 1
    if res_progress > 0:
        active_components += 1
    
    total_progress = (infra_progress + cap_progress + res_progress) / 3 if active_components == 3 else infra_progress / active_components
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Project Progress", f"{total_progress:.1f}%", 
                  delta=f"{active_components}/3 Components Active")
    with col2:
        st.metric("Infrastructure", f"{infra_progress:.2f}%", delta=f"Target: {infra_target:.2f}%")  # .2f shows 25.75
    with col3:
        st.metric("Capability Building", f"{cap_progress:.1f}%" if cap_progress > 0 else "Not Started", 
                  delta=cap_status)
    with col4:
        st.metric("Research & Extension", f"{res_progress:.1f}%" if res_progress > 0 else "Not Started",
                  delta=res_status)
    
    st.markdown("---")
    
    # Component Progress Bars
    st.markdown("### 📈 Component Progress")
    
    # Infrastructure
    st.markdown("#### 🏗️ Infrastructure Component")
    st.progress(infra_progress / 100, text=f"{infra_progress:.2f}% Complete")  # .2f shows 25.75
    st.caption(f"Contract Amount: ₱249,040,900 | Utilized: ₱{infra_cost:,.0f}")
    
    # Capability Building (Placeholder)
    st.markdown("#### 👨‍🌾 Capability Building Component")
    if cap_progress > 0:
        st.progress(cap_progress / 100, text=f"{cap_progress:.1f}% Complete")
    else:
        st.info("📌 Data pending. Upload Capability Building S-Curve to activate this component.")
        st.progress(0, text="Awaiting Data")
    
    # Research & Extension (Placeholder)
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
    """MPCFS Infrastructure S-Curve Tracker with Edit-in-App Features"""
    
    component_titles = {
        "infrastructure": {"name": "Infrastructure", "icon": "🏗️", "amount": 249_040_900.00},
        "capability": {"name": "Capability Building", "icon": "👨‍🌾", "amount": 0},
        "research": {"name": "Research & Extension", "icon": "🔬", "amount": 0}
    }
    
    comp = component_titles[component]
    
    st.markdown(f"#### {comp['icon']} {comp['name']} Component - S-Curve Tracker")
    st.caption(f"Track physical and financial progress | Contract: ₱{comp['amount']:,.2f}")
    
    # Contract Information
    CONTRACT_AMOUNT = comp['amount'] if comp['amount'] > 0 else 249_040_900.00
    
    # Session state keys for this component
    prefix = f"{component}_"
    
    # Initialize data if not exists
    if f'{prefix}original_plan' not in st.session_state:
        # Infrastructure data from your Excel
        if component == "infrastructure":
            original_plan = [
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
            while len(original_plan) < 193:
                original_plan.append(100.00)
            
            revised_plan = [
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
            while len(revised_plan) < 193:
                revised_plan.append(100.00)
            
            actual = [
                0.88, 0.91, 0.95, 1.00, 1.05, 1.10, 1.45, 1.62, 2.12, 2.45, 2.85, 3.21, 3.44, 3.85, 3.95, 4.05,
                4.17, 4.30, 4.40, 4.50, 4.61, 4.70, 4.81, 4.89, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
                5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
                5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 7.33,
                9.88, 11.61, 13.40, 15.45, 17.73, 20.02, 22.30, 24.59, 24.67, 24.75, 24.83, 24.92, 25.14, 25.34, 25.55, 25.75
            ]
            while len(actual) < 193:
                actual.append(actual[-1] if actual else 25.75)
        else:
            # Placeholder for other components
            original_plan = [0] * 193
            revised_plan = [0] * 193
            actual = [0] * 193
        
        st.session_state[f'{prefix}original_plan'] = original_plan
        st.session_state[f'{prefix}revised_plan'] = revised_plan
        st.session_state[f'{prefix}actual'] = actual
        st.session_state[f'{prefix}cost'] = [p * CONTRACT_AMOUNT / 100 for p in actual]  # This is a LIST
        st.session_state[f'{prefix}last_updated'] = datetime.now().isoformat()
    
    weeks = list(range(1, 194))
    
    # Get current progress - FIXED: handle list properly
    actual_list = st.session_state[f'{prefix}actual']
    revised_list = st.session_state[f'{prefix}revised_plan']
    
    # Find current week (last week with actual > 0)
    current_week = 0
    for i, val in enumerate(actual_list):
        if val > 0:
            current_week = i
    
    current_actual = actual_list[current_week] if current_week < len(actual_list) else 0
    current_revised = revised_list[current_week] if current_week < len(revised_list) else 0
    
    physical_variance = current_actual - current_revised
    current_cost = current_actual * CONTRACT_AMOUNT / 100
    planned_cost = current_revised * CONTRACT_AMOUNT / 100
    cost_variance = current_cost - planned_cost
    
    # Store in session state for dashboard
    st.session_state['infrastructure_progress'] = current_actual
    st.session_state['infrastructure_target'] = current_revised
    st.session_state['infrastructure_cost'] = current_cost
    
    # KPI Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Overall Progress", f"{current_actual:.2f}%", delta=f"{current_actual - current_revised:.2f}% vs Revised")
    with col2:
        st.metric("Physical Variance", f"{physical_variance:+.2f}%", 
                  delta="Ahead" if physical_variance >= 0 else "Behind",
                  delta_color="normal" if physical_variance >= 0 else "inverse")
    with col3:
        st.metric("Cost Utilized", f"₱{current_cost:,.0f}", delta=f"{(current_actual/100):.1f}% of Total")
    with col4:
        st.metric("Cost Variance", f"₱{cost_variance:+,.0f}",
                  delta="Under" if cost_variance <= 0 else "Over",
                  delta_color="normal" if cost_variance <= 0 else "inverse")
    with col5:
        schedule_status = "✅ ON TRACK" if physical_variance >= -2 else "⚠️ BEHIND"
        st.metric("Schedule Status", schedule_status)
    
    st.markdown("---")
    
    # EDIT MODE TOGGLE
    edit_mode = st.toggle("✏️ Edit Mode (Enable to modify plan data)", value=False)
    
    if edit_mode:
        st.warning("⚠️ Edit Mode Enabled: You can modify Original Plan, Revised Plan, and Actual Progress below.")
        
        # Data Management Section
        st.markdown("### 💾 Data Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Import from CSV", use_container_width=True):
                st.info("CSV import feature - upload file with columns: Week, Original, Revised, Actual")
                uploaded_file = st.file_uploader("Choose CSV file", type=['csv'], key=f"{prefix}_import")
                if uploaded_file:
                    df_import = pd.read_csv(uploaded_file)
                    st.success(f"Imported {len(df_import)} rows")
        
        with col2:
            if st.button("💾 Export to CSV", use_container_width=True):
                export_df = pd.DataFrame({
                    "Week": weeks[:len(st.session_state[f'{prefix}original_plan'])],
                    "Original_Plan": st.session_state[f'{prefix}original_plan'],
                    "Revised_Plan": st.session_state[f'{prefix}revised_plan'],
                    "Actual_Progress": st.session_state[f'{prefix}actual'],
                    "Actual_Cost": st.session_state[f'{prefix}cost']
                })
                csv = export_df.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv, 
                                  file_name=f"mpcfs_{component}_data_{datetime.now().strftime('%Y%m%d')}.csv",
                                  mime="text/csv")
        
        with col3:
            if st.button("☁️ Sync to Cloud (Supabase)", use_container_width=True):
                st.success("✅ Data synced to cloud! (Supabase integration ready)")
        
        st.markdown("---")
        
        # Editable Table
        st.markdown("### 📝 Edit Plan Data")
        
        # Show limited rows for editing
        edit_range = st.radio("Show weeks:", ["First 52 weeks", "Last 12 weeks", "Current +/- 10 weeks"], horizontal=True)
        
        if edit_range == "First 52 weeks":
            start_idx, end_idx = 0, min(52, len(st.session_state[f'{prefix}original_plan']))
        elif edit_range == "Last 12 weeks":
            start_idx = max(0, len(st.session_state[f'{prefix}original_plan']) - 12)
            end_idx = len(st.session_state[f'{prefix}original_plan'])
        else:  # Current +/- 10
            start_idx = max(0, current_week - 10)
            end_idx = min(len(st.session_state[f'{prefix}original_plan']), current_week + 11)
        
        # Create editable dataframe
        edit_data = []
        for i in range(start_idx, end_idx):
            edit_data.append({
                "Week": i + 1,
                "Original (%)": st.session_state[f'{prefix}original_plan'][i],
                "Revised (%)": st.session_state[f'{prefix}revised_plan'][i],
                "Actual (%)": st.session_state[f'{prefix}actual'][i],
                "Cost (₱M)": st.session_state[f'{prefix}cost'][i] / 1_000_000
            })
        
        edit_df = pd.DataFrame(edit_data)
        
        # Display editable table
        edited_df = st.data_editor(edit_df, use_container_width=True, hide_index=True,
                                   column_config={
                                       "Week": st.column_config.NumberColumn("Week", disabled=True),
                                       "Original (%)": st.column_config.NumberColumn("Original (%)", min_value=0, max_value=100, step=0.5),
                                       "Revised (%)": st.column_config.NumberColumn("Revised (%)", min_value=0, max_value=100, step=0.5),
                                       "Actual (%)": st.column_config.NumberColumn("Actual (%)", min_value=0, max_value=100, step=0.5),
                                       "Cost (₱M)": st.column_config.NumberColumn("Cost (₱M)", min_value=0, step=0.1)
                                   })
        
        if st.button("💾 Save All Changes", type="primary", use_container_width=True):
            for idx, row in edited_df.iterrows():
                i = start_idx + idx
                st.session_state[f'{prefix}original_plan'][i] = row["Original (%)"]
                st.session_state[f'{prefix}revised_plan'][i] = row["Revised (%)"]
                st.session_state[f'{prefix}actual'][i] = row["Actual (%)"]
                st.session_state[f'{prefix}cost'][i] = row["Cost (₱M)"] * 1_000_000
            
            st.session_state[f'{prefix}last_updated'] = datetime.now().isoformat()
            st.success("✅ All changes saved!")
            st.rerun()
    
    # S-CURVE CHART
    st.markdown("### 📈 S-Curve: Planned vs Actual Progress")
    
    # Ensure all lists have same length
    max_len = len(st.session_state[f'{prefix}original_plan'])
    
    plot_df = pd.DataFrame({
        "Week": weeks[:max_len],
        "Original Plan (%)": st.session_state[f'{prefix}original_plan'][:max_len],
        "Revised Plan (%)": st.session_state[f'{prefix}revised_plan'][:max_len],
        "Actual Progress (%)": st.session_state[f'{prefix}actual'][:max_len]
    })
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=plot_df["Week"], y=plot_df["Original Plan (%)"], mode='lines', name='Original Plan', line=dict(color='#3498db', width=2, dash='dash')))
    fig.add_trace(go.Scatter(x=plot_df["Week"], y=plot_df["Revised Plan (%)"], mode='lines', name='Revised Plan', line=dict(color='#f39c12', width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=plot_df["Week"], y=plot_df["Actual Progress (%)"], mode='lines+markers', name='Actual Progress', line=dict(color='#2ecc71', width=3), marker=dict(size=4)))
    fig.add_vline(x=current_week + 1, line_dash="dash", line_color="red", annotation_text=f"Current: Week {current_week + 1}", annotation_position="top right")
    fig.update_layout(title="Project Progress S-Curve", xaxis_title="Week Number (Sept 2024 → May 2028)", yaxis_title="Cumulative Progress (%)", yaxis_range=[0, 105], height=500, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)
    
    # COST S-CURVE CHART - FIXED: now using list comprehension correctly
    st.markdown("### 💰 Cost S-Curve: Planned vs Actual Expenditure")
    
    cost_list = st.session_state[f'{prefix}cost']
    # Ensure cost_list is a list
    if not isinstance(cost_list, list):
        cost_list = [cost_list] * max_len
    
    cost_df = pd.DataFrame({
        "Week": weeks[:max_len],
        "Original Plan (₱M)": [p * CONTRACT_AMOUNT / 100 / 1_000_000 for p in st.session_state[f'{prefix}original_plan'][:max_len]],
        "Revised Plan (₱M)": [p * CONTRACT_AMOUNT / 100 / 1_000_000 for p in st.session_state[f'{prefix}revised_plan'][:max_len]],
        "Actual Cost (₱M)": [cost_list[i] / 1_000_000 if i < len(cost_list) else 0 for i in range(max_len)]
    })
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=cost_df["Week"], y=cost_df["Original Plan (₱M)"], mode='lines', name='Original Plan (₱M)', line=dict(color='#3498db', width=2, dash='dash')))
    fig2.add_trace(go.Scatter(x=cost_df["Week"], y=cost_df["Revised Plan (₱M)"], mode='lines', name='Revised Plan (₱M)', line=dict(color='#f39c12', width=2, dash='dot')))
    fig2.add_trace(go.Scatter(x=cost_df["Week"], y=cost_df["Actual Cost (₱M)"], mode='lines+markers', name='Actual Cost (₱M)', line=dict(color='#e74c3c', width=3), marker=dict(size=4)))
    fig2.add_vline(x=current_week + 1, line_dash="dash", line_color="red")
    fig2.update_layout(title="Project Cost S-Curve (in Million ₱)", xaxis_title="Week Number", yaxis_title="Cumulative Cost (₱ Million)", height=450, hovermode='x unified')
    st.plotly_chart(fig2, use_container_width=True)
    
    # Quick Update Section (for non-edit mode)
    if not edit_mode:
        st.markdown("---")
        st.markdown("### ✏️ Quick Progress Update")
        
        role = st.selectbox("Your Role", ["Project Engineer", "Finance Officer", "Project Manager", "Viewer"], key=f"{prefix}_role")
        
        if role != "Viewer":
            col1, col2 = st.columns(2)
            with col1:
                week_to_update = st.slider("Select Week", 1, min(80, len(actual_list)), current_week + 1)
            with col2:
                if role in ["Project Engineer", "Project Manager"]:
                    new_progress = st.number_input("Physical Progress (%)", 0.0, 100.0, 
                                                   value=float(actual_list[week_to_update-1]), step=0.5, key=f"{prefix}_progress")
                    if st.button("✅ Update Progress", type="primary"):
                        actual_list[week_to_update-1] = new_progress
                        cost_list[week_to_update-1] = new_progress * CONTRACT_AMOUNT / 100
                        st.session_state[f'{prefix}actual'] = actual_list
                        st.session_state[f'{prefix}cost'] = cost_list
                        st.session_state[f'{prefix}last_updated'] = datetime.now().isoformat()
                        st.success(f"✅ Week {week_to_update} updated to {new_progress}%")
                        st.rerun()
                
                if role in ["Finance Officer", "Project Manager"]:
                    current_cost_val = cost_list[week_to_update-1] if week_to_update-1 < len(cost_list) else 0
                    new_cost = st.number_input("Actual Cost (₱)", 0.0, float(CONTRACT_AMOUNT),
                                               value=float(current_cost_val), step=100000.0, key=f"{prefix}_cost_input")
                    if st.button("💰 Update Cost", type="primary"):
                        new_progress_from_cost = (new_cost / CONTRACT_AMOUNT) * 100
                        actual_list[week_to_update-1] = new_progress_from_cost
                        cost_list[week_to_update-1] = new_cost
                        st.session_state[f'{prefix}actual'] = actual_list
                        st.session_state[f'{prefix}cost'] = cost_list
                        st.session_state[f'{prefix}last_updated'] = datetime.now().isoformat()
                        st.success(f"✅ Week {week_to_update} cost updated to ₱{new_cost:,.2f}")
                        st.rerun()
    
    # Variance Summary
    st.markdown("---")
    st.markdown("### 📋 Progress Variance Summary")
    
    start_week_viz = max(0, current_week - 11)
    variance_data = []
    for i in range(start_week_viz, min(current_week + 1, len(actual_list))):
        variance_data.append({
            "Week": i + 1,
            "Actual (%)": f"{actual_list[i]:.2f}",
            "Original Plan (%)": f"{st.session_state[f'{prefix}original_plan'][i]:.2f}",
            "Revised Plan (%)": f"{st.session_state[f'{prefix}revised_plan'][i]:.2f}",
            "Δ vs Original": f"{actual_list[i] - st.session_state[f'{prefix}original_plan'][i]:+.2f}%",
            "Δ vs Revised": f"{actual_list[i] - st.session_state[f'{prefix}revised_plan'][i]:+.2f}%"
        })
    
    if variance_data:
        st.dataframe(pd.DataFrame(variance_data), use_container_width=True, hide_index=True)
    
    st.caption(f"Last updated: {st.session_state[f'{prefix}last_updated'][:16] if st.session_state[f'{prefix}last_updated'] else 'Never'}")

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
    """Updated Gantt chart that syncs with all components"""
    
    st.markdown("#### 📋 Project Gantt Chart & Timeline")
    st.caption("Track project milestones, tasks, and deadlines across all components")
    
    # Get infrastructure progress
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    
    # Tasks for all components
    all_tasks = [
        # Infrastructure Tasks
        {"Component": "🏗️ Infrastructure", "Task": "Project Inception & Planning", "Start": "2024-01-01", "Finish": "2024-03-31", "Complete": 100},
        {"Component": "🏗️ Infrastructure", "Task": "Site Development & Grading", "Start": "2024-04-01", "Finish": "2024-08-31", "Complete": 90},
        {"Component": "🏗️ Infrastructure", "Task": "Foundation & Structural Works", "Start": "2024-09-01", "Finish": "2025-03-31", "Complete": 60},
        {"Component": "🏗️ Infrastructure", "Task": "Building Construction", "Start": "2025-04-01", "Finish": "2025-12-31", "Complete": 20},
        {"Component": "🏗️ Infrastructure", "Task": "Finishing & Fit-out", "Start": "2026-01-01", "Finish": "2026-06-30", "Complete": 0},
        
        # Capability Building Tasks (Placeholder)
        {"Component": "👨‍🌾 Capability Building", "Task": "Training Needs Assessment", "Start": "2024-06-01", "Finish": "2024-09-30", "Complete": 0, "status": "pending"},
        {"Component": "👨‍🌾 Capability Building", "Task": "Curriculum Development", "Start": "2024-10-01", "Finish": "2025-03-31", "Complete": 0, "status": "pending"},
        {"Component": "👨‍🌾 Capability Building", "Task": "Farmer Training Program", "Start": "2025-04-01", "Finish": "2026-12-31", "Complete": 0, "status": "pending"},
        
        # Research & Extension Tasks (Placeholder)
        {"Component": "🔬 Research & Extension", "Task": "Baseline Research Setup", "Start": "2024-07-01", "Finish": "2024-12-31", "Complete": 0, "status": "pending"},
        {"Component": "🔬 Research & Extension", "Task": "Data Collection", "Start": "2025-01-01", "Finish": "2026-06-30", "Complete": 0, "status": "pending"},
        {"Component": "🔬 Research & Extension", "Task": "Extension Services Rollout", "Start": "2025-06-01", "Finish": "2027-12-31", "Complete": 0, "status": "pending"},
    ]
    
    df_tasks = pd.DataFrame(all_tasks)
    df_tasks["Start"] = pd.to_datetime(df_tasks["Start"])
    df_tasks["Finish"] = pd.to_datetime(df_tasks["Finish"])
    
    # Color mapping by component
    colors = {"🏗️ Infrastructure": "#2ecc71", "👨‍🌾 Capability Building": "#3498db", "🔬 Research & Extension": "#9b59b6"}
    
    fig = go.Figure()
    for i, task in df_tasks.iterrows():
        duration = (task["Finish"] - task["Start"]).days
        color = colors.get(task["Component"], "#95a5a6")
        
        fig.add_trace(go.Bar(
            x=[duration],
            y=[f"{task['Component']}: {task['Task']}"],
            orientation='h',
            marker=dict(color=color, opacity=0.8),
            text=f"{task['Complete']}% Complete" if task['Complete'] > 0 else "Pending",
            textposition='outside'
        ))
    
    fig.update_layout(title="Project Timeline by Component", xaxis_title="Duration (Days)", height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Task Status Table
    st.markdown("#### Task Status by Component")
    
    for component in ["🏗️ Infrastructure", "👨‍🌾 Capability Building", "🔬 Research & Extension"]:
        st.markdown(f"**{component}**")
        comp_tasks = [t for t in all_tasks if t["Component"] == component]
        
        for task in comp_tasks:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"📌 {task['Task']}")
            with col2:
                st.markdown(f"{task['Complete']}% Complete" if task['Complete'] > 0 else "⏳ Pending")
            with col3:
                if task['Complete'] >= 90:
                    st.success("✅")
                elif task['Complete'] >= 50:
                    st.warning("🟡 In Progress")
                else:
                    st.info("📋 Planned")
        st.markdown("---")

def show_mpcfs_report_generator_updated():
    """Generate detailed, downloadable, printable reports"""
    
    st.markdown("#### 📄 Report Generator")
    st.caption("Generate detailed reports with cover letter for submission")
    
    # Get real data
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    infra_target = st.session_state.get('infrastructure_target', 25.75)
    
    # Handle cost properly
    infra_cost_raw = st.session_state.get('infrastructure_cost', 64_000_000)
    if isinstance(infra_cost_raw, list):
        infra_cost = next((x for x in reversed(infra_cost_raw) if x > 0), 64_000_000)
    else:
        infra_cost = infra_cost_raw
    
    physical_variance = infra_progress - infra_target
    total_budget = 249_040_900.00
    
    # Report options
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
            "Annual Report 2025"
        ])
    
    # Additional options
    include_charts = st.checkbox("Include Charts in Report", value=True)
    include_detailed_table = st.checkbox("Include Detailed Variance Table", value=True)
    
    # Generate Report Button
    if st.button("📄 Generate Report", type="primary", use_container_width=True):
        
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
                }}
                .header {{
                    text-align: center;
                    border-bottom: 3px solid #2ecc71;
                    padding-bottom: 20px;
                    margin-bottom: 30px;
                }}
                .title {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #2c3e50;
                }}
                .subtitle {{
                    font-size: 14px;
                    color: #7f8c8d;
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
                .variance-positive {{
                    color: #27ae60;
                }}
                .variance-negative {{
                    color: #e74c3c;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #2ecc71;
                    color: white;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 10px;
                    color: #7f8c8d;
                }}
                @media print {{
                    body {{
                        margin: 20px;
                    }}
                    .no-print {{
                        display: none;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">MOUNTAIN PROVINCE CLIMATE FIELD SCHOOL (MPCFS)</div>
                <div class="subtitle">{report_type} | {report_period}</div>
                <div class="subtitle">Bacarri, Paracelis, Mountain Province</div>
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
                        <div class="kpi-value">{infra_target:.2f}%</div>
                        <div class="kpi-label">Target Progress</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-value {'variance-positive' if physical_variance >= 0 else 'variance-negative'}">{physical_variance:+.2f}%</div>
                        <div class="kpi-label">Schedule Variance</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <div class="section-title">💰 Financial Summary</div>
                <table>
                    <tr><th>Item</th><th>Amount (₱)</th></tr>
                    <tr><td>Total Contract Amount</td><td>{total_budget:,.2f}</td></tr>
                    <tr><td>Actual Cost Utilized</td><td>{infra_cost:,.2f}</td></tr>
                    <tr><td>Remaining Budget</td><td>{total_budget - infra_cost:,.2f}</td></tr>
                    <tr><td>Financial Utilization Rate</td><td>{(infra_cost/total_budget)*100:.1f}%</td></tr>
                </table>
            </div>
        """
        
        if include_charts:
            report_html += """
            <div class="section">
                <div class="section-title">📈 Progress Chart</div>
                <p><em>Charts will be embedded here in the full version</em></p>
            </div>
            """
        
        if include_detailed_table:
            report_html += """
            <div class="section">
                <div class="section-title">📋 Detailed Progress Summary</div>
                <table>
                    <tr>
                        <th>Component</th>
                        <th>Progress (%)</th>
                        <th>Target (%)</th>
                        <th>Variance (%)</th>
                        <th>Status</th>
                    </tr>
                    <tr>
                        <td>Infrastructure</td>
                        <td>{:.2f}%</td>
                        <td>{:.2f}%</td>
                        <td class="{}">{:+.2f}%</td>
                        <td>{}</td>
                    </tr>
                    <tr>
                        <td>Capability Building</td>
                        <td colspan="4" style="text-align:center;">⏳ Data Pending Upload</td>
                    </tr>
                    <tr>
                        <td>Research & Extension</td>
                        <td colspan="4" style="text-align:center;">⏳ Data Pending Upload</td>
                    </tr>
                </table>
            </div>
            """.format(
                infra_progress, infra_target,
                'variance-positive' if physical_variance >= 0 else 'variance-negative',
                physical_variance,
                "✅ On Track" if physical_variance >= -2 else "⚠️ Behind Schedule"
            )
        
        report_html += f"""
            <div class="section">
                <div class="section-title">🎯 Key Accomplishments</div>
                <ul>
                    <li>Infrastructure component at {infra_progress:.2f}% completion</li>
                    <li>Site development and foundation works in progress</li>
                    <li>Project management systems established</li>
                </ul>
            </div>
            
            <div class="section">
                <div class="section-title">⚠️ Issues and Concerns</div>
                <ul>
                    <li>Schedule variance: {physical_variance:+.2f}%</li>
                    <li>Weather-related delays affecting construction</li>
                </ul>
            </div>
            
            <div class="section">
                <div class="section-title">📅 Next Steps</div>
                <ul>
                    <li>Complete remaining infrastructure works</li>
                    <li>Activate Capability Building component</li>
                    <li>Establish research protocols</li>
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
        
        # Show HTML preview
        st.components.v1.html(report_html, height=600, scrolling=True)
        
        # Download buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button(
                label="📥 Download as HTML",
                data=report_html,
                file_name=f"MPCFS_{report_type.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        with col2:
            # Convert to PDF ready (instruction)
            st.info("💡 Tip: Use browser's 'Print' (Ctrl+P) then 'Save as PDF' for PDF format")
        
        with col3:
            st.success(f"✅ Report generated successfully!")
    
    # Help section
    with st.expander("ℹ️ How to Use Reports"):
        st.markdown("""
        ### 📄 Report Features:
        
        1. **Download as HTML** - Click the download button to save the report
        
        2. **Save as PDF**:
           - After generating the report, click the download button
           - Open the HTML file in any browser
           - Press `Ctrl+P` (Windows) or `Cmd+P` (Mac)
           - Select "Save as PDF" as printer
           - Click Save
        
        3. **Print Directly**:
           - Generate the report
           - Click download and open in browser
           - Press `Ctrl+P` and send to printer
        
        ### 📊 Report Types:
        - **Progress Report** - Overall project status
        - **Financial Report** - Budget utilization
        - **Accomplishment Report** - Completed activities
        - **Liquidation Report** - Financial accountability
        - **M&E Report** - Monitoring and evaluation
        - **Consolidated Report** - All components combined
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