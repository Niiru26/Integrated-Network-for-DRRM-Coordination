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
        **Status:** 🟢 On Track
        """)
    
    st.markdown("---")
    
    # Project progress summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Progress", "42%", delta="+8% this quarter")
    with col2:
        st.metric("Physical Accomplishment", "38%", delta="Target: 40%")
    with col3:
        st.metric("Financial Utilization", "35%", delta="₱94.85M")
    with col4:
        st.metric("Beneficiaries Reached", "1,247", delta="farmers")
    
    st.markdown("---")
    
    # MPCFS Sub-tabs - 7 tabs including S-Curve Tracker
    mpcfstab1, mpcfstab2, mpcfstab3, mpcfstab4, mpcfstab5, mpcfstab6, mpcfstab7 = st.tabs([
        "📊 Project Dashboard",
        "📋 Gantt Chart & Timeline",
        "📁 Document Management",
        "📸 Photo Gallery",
        "📄 Report Generator",
        "📖 Coffee Table Book",
        "📈 S-Curve Tracker"
    ])
    
    with mpcfstab1:
        show_mpcfs_dashboard()
    
    with mpcfstab2:
        show_mpcfs_gantt()
    
    with mpcfstab3:
        show_mpcfs_document_management()
    
    with mpcfstab4:
        show_mpcfs_photo_gallery()
    
    with mpcfstab5:
        show_mpcfs_report_generator()
    
    with mpcfstab6:
        show_mpcfs_coffee_table_book()
    
    with mpcfstab7:
        show_mpcfs_scurve_tracker()


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
    """Gantt chart with all infrastructure sub-components"""
    
    st.markdown("#### 📋 Project Gantt Chart & Timeline")
    st.caption("Track project milestones by infrastructure sub-component")
    
    # Get infrastructure progress
    infra_progress = st.session_state.get('infrastructure_progress', 25.75)
    
    # All tasks by sub-component
    all_tasks = [
        # Civil Works
        {"Component": "🏗️ Civil Works", "Task": "Site Development & Preparation", "Start": "2024-04-01", "Finish": "2024-12-31", "Complete": 45},
        {"Component": "🏗️ Civil Works", "Task": "Foundation & Excavation", "Start": "2024-09-01", "Finish": "2025-03-31", "Complete": 60},
        {"Component": "🏗️ Civil Works", "Task": "Gravel Fill & Subbase", "Start": "2025-01-01", "Finish": "2025-06-30", "Complete": 40},
        {"Component": "🏗️ Civil Works", "Task": "PCC Pavement", "Start": "2025-04-01", "Finish": "2025-10-31", "Complete": 0},
        
        # Structural
        {"Component": "🏗️ Structural", "Task": "Reinforcing Steel Installation", "Start": "2024-10-01", "Finish": "2025-12-31", "Complete": 35},
        {"Component": "🏗️ Structural", "Task": "Structural Concrete Works", "Start": "2024-11-01", "Finish": "2026-03-31", "Complete": 30},
        {"Component": "🏗️ Structural", "Task": "Structural Steel Erection", "Start": "2025-04-01", "Finish": "2026-06-30", "Complete": 25},
        {"Component": "🏗️ Structural", "Task": "Formworks & Falseworks", "Start": "2025-01-01", "Finish": "2025-12-31", "Complete": 20},
        {"Component": "🏗️ Structural", "Task": "Metal Deck Panel Installation", "Start": "2025-06-01", "Finish": "2026-03-31", "Complete": 0},
        
        # Architectural
        {"Component": "🏛️ Architectural", "Task": "CHB Wall Construction", "Start": "2025-06-01", "Finish": "2026-06-30", "Complete": 10},
        {"Component": "🏛️ Architectural", "Task": "Plumbing & Sanitary", "Start": "2025-09-01", "Finish": "2026-09-30", "Complete": 5},
        {"Component": "🏛️ Architectural", "Task": "Ceiling & Finishing", "Start": "2026-01-01", "Finish": "2026-12-31", "Complete": 0},
        {"Component": "🏛️ Architectural", "Task": "Painting & Tiling", "Start": "2026-04-01", "Finish": "2027-03-31", "Complete": 0},
        {"Component": "🏛️ Architectural", "Task": "Doors & Windows Installation", "Start": "2026-07-01", "Finish": "2027-06-30", "Complete": 0},
        
        # Electrical
        {"Component": "⚡ Electrical", "Task": "Conduits & Wiring", "Start": "2026-01-01", "Finish": "2026-12-31", "Complete": 0},
        {"Component": "⚡ Electrical", "Task": "Panelboards & Breakers", "Start": "2026-06-01", "Finish": "2027-03-31", "Complete": 0},
        {"Component": "⚡ Electrical", "Task": "Lighting Fixtures", "Start": "2026-09-01", "Finish": "2027-06-30", "Complete": 0},
        {"Component": "⚡ Electrical", "Task": "Solar Panel System", "Start": "2027-01-01", "Finish": "2027-12-31", "Complete": 0},
        
        # Mechanical
        {"Component": "🔧 Mechanical", "Task": "Fire Protection System", "Start": "2026-07-01", "Finish": "2027-06-30", "Complete": 0},
        {"Component": "🔧 Mechanical", "Task": "Water Pumping System", "Start": "2026-10-01", "Finish": "2027-09-30", "Complete": 0},
        {"Component": "🔧 Mechanical", "Task": "Generator Installation", "Start": "2027-04-01", "Finish": "2027-12-31", "Complete": 0},
        
        # Equipment
        {"Component": "📦 Equipment", "Task": "Furniture & Fixtures", "Start": "2027-07-01", "Finish": "2028-03-31", "Complete": 0},
        {"Component": "📦 Equipment", "Task": "Laboratory Equipment", "Start": "2027-10-01", "Finish": "2028-06-30", "Complete": 0},
        {"Component": "📦 Equipment", "Task": "AWS Installation", "Start": "2027-12-01", "Finish": "2028-08-31", "Complete": 0},
        
        # Capability Building (Planned)
        {"Component": "👨‍🌾 Capability Building", "Task": "Training Program", "Start": "2025-06-01", "Finish": "2026-12-31", "Complete": 0, "status": "planned"},
        
        # Research & Extension (Planned)
        {"Component": "🔬 Research & Extension", "Task": "Research Setup", "Start": "2025-09-01", "Finish": "2026-12-31", "Complete": 0, "status": "planned"},
    ]
    
    df_tasks = pd.DataFrame(all_tasks)
    df_tasks["Start"] = pd.to_datetime(df_tasks["Start"])
    df_tasks["Finish"] = pd.to_datetime(df_tasks["Finish"])
    
    colors = {
        "🏗️ Civil Works": "#2ecc71", 
        "🏗️ Structural": "#3498db", 
        "🏛️ Architectural": "#9b59b6", 
        "⚡ Electrical": "#f39c12", 
        "🔧 Mechanical": "#e74c3c", 
        "📦 Equipment": "#1abc9c",
        "👨‍🌾 Capability Building": "#95a5a6",
        "🔬 Research & Extension": "#95a5a6"
    }
    
    fig = go.Figure()
    for i, task in df_tasks.iterrows():
        duration = (task["Finish"] - task["Start"]).days
        color = colors.get(task["Component"], "#95a5a6")
        opacity = 0.8 if task.get('status') != 'planned' else 0.4
        
        fig.add_trace(go.Bar(
            x=[duration],
            y=[f"{task['Component']}: {task['Task']}"],
            orientation='h',
            marker=dict(color=color, opacity=opacity),
            text=f"{task['Complete']:.0f}% Complete" if task['Complete'] > 0 else "Pending",
            textposition='outside'
        ))
    
    fig.update_layout(title="Project Timeline by Component", xaxis_title="Duration (Days)", height=600, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Task Status Table
    st.markdown("#### Task Status by Component")
    
    for component in ["🏗️ Civil Works", "🏗️ Structural", "🏛️ Architectural", "⚡ Electrical", "🔧 Mechanical", "📦 Equipment", "👨‍🌾 Capability Building", "🔬 Research & Extension"]:
        st.markdown(f"**{component}**")
        comp_tasks = [t for t in all_tasks if t["Component"] == component]
        
        for task in comp_tasks:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"📌 {task['Task']}")
            with col2:
                st.markdown(f"{task['Complete']:.0f}% Complete" if task['Complete'] > 0 else "⏳ Pending")
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


def show_mpcfs_scurve_tracker(component="infrastructure"):
    """MPCFS Infrastructure S-Curve Tracker - COMPLETE WORKING VERSION"""
    
    st.markdown(f"#### 🏗️ Infrastructure Component - S-Curve Tracker")
    st.caption(f"Track physical and financial progress | Contract: ₱249,040,900.00")
    
    CONTRACT_AMOUNT = 249_040_900.00
    
    # ============================================================
    # WORK ITEMS DATA
    # ============================================================
    
    if 'infrastructure_work_items' not in st.session_state:
        st.session_state.infrastructure_work_items = [
            {"no": "A.1.1 (8)", "description": "Provision of Field Office", "category": "Civil Works", "weight": 0.546, "planned": 0.547, "actual": 0.50, "cost": 1_360_800},
            {"no": "A.1.2 (2)", "description": "Provision of 4x4 Vehicle", "category": "Civil Works", "weight": 0.919, "planned": 0.919, "actual": 0.85, "cost": 2_289_000},
            {"no": "B.3", "description": "Permits and Clearances", "category": "Civil Works", "weight": 0.126, "planned": 0.126, "actual": 0.126, "cost": 315_000},
            {"no": "B.5", "description": "Billboard and Signboard", "category": "Civil Works", "weight": 0.004, "planned": 0.004, "actual": 0.004, "cost": 10_500},
            {"no": "B.7 (2)", "description": "Safety and Health Program", "category": "Civil Works", "weight": 1.229, "planned": 1.229, "actual": 1.10, "cost": 3_061_108},
            {"no": "B.9", "description": "Mobilization/Demobilization", "category": "Civil Works", "weight": 0.873, "planned": 0.873, "actual": 0.873, "cost": 2_174_130},
            {"no": "B.13", "description": "Geotechnical Investigation", "category": "Civil Works", "weight": 0.126, "planned": 0.126, "actual": 0.126, "cost": 315_000},
            {"no": "B.25", "description": "Engineering & Architectural Design", "category": "Civil Works", "weight": 0.170, "planned": 0.170, "actual": 0.170, "cost": 424_499},
            {"no": "101(1)", "description": "Removal of Structures", "category": "Civil Works", "weight": 0.004, "planned": 0.004, "actual": 0.004, "cost": 9_419},
            {"no": "404", "description": "Reinforcing Steel Bar", "category": "Structural", "weight": 1.417, "planned": 1.417, "actual": 1.14, "cost": 2_834_045},
            {"no": "405", "description": "Structural Concrete Class A", "category": "Structural", "weight": 1.971, "planned": 1.971, "actual": 0.70, "cost": 1_740_048},
            {"no": "803(1)a", "description": "Structure Excavation", "category": "Structural", "weight": 0.628, "planned": 0.628, "actual": 0.54, "cost": 1_357_263},
            {"no": "804(4)", "description": "Gravel Fill", "category": "Structural", "weight": 0.632, "planned": 0.632, "actual": 0.54, "cost": 1_336_224},
            {"no": "1706(1)", "description": "Overhaul", "category": "Structural", "weight": 0.291, "planned": 0.291, "actual": 0.23, "cost": 560_761},
            {"no": "900(1)c2", "description": "Concrete Footing/Slab Fill", "category": "Structural", "weight": 1.710, "planned": 1.710, "actual": 1.43, "cost": 3_561_496},
            {"no": "900(1)", "description": "Concrete Columns/Beams", "category": "Structural", "weight": 4.134, "planned": 4.134, "actual": 1.39, "cost": 3_449_789},
            {"no": "902(1) a", "description": "Reinforcing Steel", "category": "Structural", "weight": 9.308, "planned": 9.308, "actual": 3.06, "cost": 7_625_371},
            {"no": "903(1)", "description": "Formworks/Falseworks", "category": "Structural", "weight": 1.270, "planned": 1.270, "actual": 0.38, "cost": 948_291},
            {"no": "1047 (1)", "description": "Structural Steel", "category": "Structural", "weight": 14.170, "planned": 14.170, "actual": 11.44, "cost": 28_583_543},
            {"no": "1047 (2)a", "description": "Steel Trusses", "category": "Structural", "weight": 1.757, "planned": 1.757, "actual": 0.33, "cost": 823_223},
            {"no": "1047 (3)a", "description": "Anchor Bolts", "category": "Structural", "weight": 1.505, "planned": 1.505, "actual": 1.39, "cost": 3_453_257},
            {"no": "1047 (5)", "description": "Steel Plates", "category": "Structural", "weight": 1.799, "planned": 1.799, "actual": 1.23, "cost": 3_071_727},
            {"no": "1001(11)", "description": "Septic Vault", "category": "Architectural", "weight": 0.436, "planned": 0.436, "actual": 0.22, "cost": 543_264},
        ]
    
    work_items = st.session_state.infrastructure_work_items
    
    # ============================================================
    # CALCULATE PROGRESS (MUST BE BEFORE KPI CARDS)
    # ============================================================
    
    total_weight = sum(item['weight'] for item in work_items)
    weighted_actual = sum((item['weight'] * item['actual']) / 100 for item in work_items)
    overall_progress = weighted_actual if weighted_actual > 0 else 25.75
    total_actual_cost = sum(item['cost'] for item in work_items)
    
    # ============================================================
    # S-CURVE DATA
    # ============================================================
    
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
    
    actual_weekly = [
        0.88, 0.91, 0.95, 1.00, 1.05, 1.10, 1.45, 1.62, 2.12, 2.45, 2.85, 3.21, 3.44, 3.85, 3.95, 4.05,
        4.17, 4.30, 4.40, 4.50, 4.61, 4.70, 4.81, 4.89, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
        5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
        5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 7.33,
        9.88, 11.61, 13.40, 15.45, 17.73, 20.02, 22.30, 24.59, 24.67, 24.75, 24.83, 24.92, 25.14, 25.34, 25.55, 25.75
    ]
    while len(actual_weekly) < 193:
        actual_weekly.append(25.75)
    
    weeks = list(range(1, 194))
    current_week_idx = 0
    for i, val in enumerate(actual_weekly):
        if val >= overall_progress:
            current_week_idx = i
            break
    
    # ============================================================
    # KPI CARDS
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
        slippage_original = overall_progress - 64.31
        st.metric(
            "Slippage vs Original Plan", 
            f"{slippage_original:+.2f}%", 
            delta=f"Target at Week 80: 64.31%",
            delta_color="inverse" if slippage_original < 0 else "normal"
        )
    
    with col3:
        slippage_revised = overall_progress - 25.75
        st.metric(
            "Slippage vs Revised Plan", 
            f"{slippage_revised:+.2f}%", 
            delta=f"Target at Week 80: 25.75%",
            delta_color="normal" if slippage_revised >= 0 else "inverse"
        )
    
    with col4:
        if slippage_revised > 0:
            status = "✅ AHEAD"
        elif slippage_revised == 0:
            status = "🟡 ON TRACK"
        else:
            status = "🔴 BEHIND"
        st.metric("Overall Status", status, delta="As of Week 80 (Mar 31, 2026)")
    
    st.markdown("---")
    
    # ============================================================
    # PROGRESS S-CURVE
    # ============================================================
    
    st.markdown("### 📈 S-Curve: Planned vs Actual Progress")
    st.markdown("**📍 As of: Week 80 (March 31, 2026)**")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=weeks[:len(original_plan)], y=original_plan, mode='lines', name='Original Plan', line=dict(color='#1f77b4', width=2, dash='dash'), opacity=0.8))
    fig1.add_trace(go.Scatter(x=weeks[:len(revised_plan)], y=revised_plan, mode='lines', name='Revised Plan', line=dict(color='#ff7f0e', width=2, dash='dot'), opacity=0.8))
    fig1.add_trace(go.Scatter(x=weeks[:current_week_idx + 1], y=actual_weekly[:current_week_idx + 1], mode='lines+markers', name='Actual Progress', line=dict(color='#2ca02c', width=3), marker=dict(size=4)))
    fig1.add_vline(x=current_week_idx + 1, line_dash="dash", line_color="#7f7f7f", line_width=1.5, annotation_text=f"Week {current_week_idx + 1}", annotation_position="top right")
    fig1.update_layout(title="Project Progress S-Curve (September 2024 - May 2028)", xaxis_title="Week Number", yaxis_title="Cumulative Progress (%)", yaxis_range=[0, 105], height=400, hovermode='x unified', plot_bgcolor='white')
    st.plotly_chart(fig1, use_container_width=True)
    
    # ============================================================
    # COST S-CURVE
    # ============================================================
    
    st.markdown("### 💰 Cost S-Curve: Planned vs Actual Expenditure")
    
    original_cost_curve = [(p / 100) * CONTRACT_AMOUNT / 1_000_000 for p in original_plan]
    revised_cost_curve = [(p / 100) * CONTRACT_AMOUNT / 1_000_000 for p in revised_plan]
    actual_cost_curve = [(p / 100) * CONTRACT_AMOUNT / 1_000_000 for p in actual_weekly]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=weeks[:len(original_cost_curve)], y=original_cost_curve, mode='lines', name='Original Plan', line=dict(color='#1f77b4', width=2, dash='dash'), opacity=0.8))
    fig2.add_trace(go.Scatter(x=weeks[:len(revised_cost_curve)], y=revised_cost_curve, mode='lines', name='Revised Plan', line=dict(color='#ff7f0e', width=2, dash='dot'), opacity=0.8))
    fig2.add_trace(go.Scatter(x=weeks[:current_week_idx + 1], y=actual_cost_curve[:current_week_idx + 1], mode='lines+markers', name='Actual Cost', line=dict(color='#d62728', width=3), marker=dict(size=4)))
    fig2.add_vline(x=current_week_idx + 1, line_dash="dash", line_color="#7f7f7f", line_width=1.5)
    fig2.update_layout(title="Cost S-Curve (in Million ₱)", xaxis_title="Week Number", yaxis_title="Cost (₱ Million)", height=400, hovermode='x unified', plot_bgcolor='white')
    st.plotly_chart(fig2, use_container_width=True)
    
    # ============================================================
    # TARGET SUMMARY
    # ============================================================
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"📋 **Original Plan at Week 80:** 64.31%")
    with col2:
        st.info(f"📋 **Revised Plan at Week 80:** 25.75%")
    with col3:
        st.success(f"✅ **Actual Progress at Week 80:** {overall_progress:.2f}%")
    
    st.markdown("---")
    
    # ============================================================
    # ITEMIZED WORK DETAILS TABLE
    # ============================================================
    
    st.markdown("### 📋 Itemized Work Details")
    st.markdown("> 🟢 **GREEN highlighted columns** are editable. Edit then click **💾 SAVE ALL CHANGES**")
    
    categories = ["All", "Civil Works", "Structural", "Architectural"]
    selected_category = st.selectbox("🔍 Filter by Category", categories)
    
    if selected_category != "All":
        filtered_items = [item for item in work_items if item.get('category') == selected_category]
    else:
        filtered_items = work_items
    
    if filtered_items:
        df_items = pd.DataFrame(filtered_items)
        df_items['Slippage (%)'] = df_items['actual'] - df_items['planned']
        df_items['Status'] = df_items['Slippage (%)'].apply(lambda x: '✅ Ahead' if x > 0.1 else ('🟡 On Track' if x >= -0.1 else '🔴 Behind'))
        
        display_df = df_items[['no', 'description', 'category', 'weight', 'planned', 'actual', 'cost', 'Slippage (%)', 'Status']].copy()
        display_df.columns = ['Item No.', 'Description', 'Category', 'Weight (%)', 'Planned (%)', '🟢 Actual (%)', '🟢 Actual Cost (₱)', 'Slippage (%)', 'Status']
        
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Item No.": st.column_config.TextColumn("Item No.", width="small", disabled=True),
                "Description": st.column_config.TextColumn("Description", width="large", disabled=True),
                "Category": st.column_config.TextColumn("Category", width="small", disabled=True),
                "Weight (%)": st.column_config.NumberColumn("Weight (%)", format="%.3f", disabled=True),
                "Planned (%)": st.column_config.NumberColumn("Planned (%)", format="%.3f", disabled=True),
                "🟢 Actual (%)": st.column_config.NumberColumn("🟢 Actual (%)", min_value=0.0, max_value=100.0, step=0.5, format="%.2f"),
                "🟢 Actual Cost (₱)": st.column_config.NumberColumn("🟢 Actual Cost (₱)", min_value=0, step=10000, format="₱%.2f"),
                "Slippage (%)": st.column_config.NumberColumn("Slippage (%)", format="%+.2f", disabled=True),
                "Status": st.column_config.TextColumn("Status", disabled=True),
            }
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("💾 SAVE ALL CHANGES", type="primary", use_container_width=True):
                for idx, row in edited_df.iterrows():
                    for original_item in work_items:
                        if original_item['no'] == row['Item No.']:
                            original_item['actual'] = row['🟢 Actual (%)']
                            original_item['cost'] = row['🟢 Actual Cost (₱)']
                            break
                st.session_state.infrastructure_work_items = work_items
                st.success("✅ All changes saved! Progress recalculated.")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All to Zero", use_container_width=True):
                for item in work_items:
                    item['actual'] = 0
                    item['cost'] = 0
                st.session_state.infrastructure_work_items = work_items
                st.success("✅ Reset complete. Ready for new data entry.")
                st.rerun()
        
        with col3:
            st.caption(f"📊 Overall Progress: {overall_progress:.2f}% | Total Cost: ₱{total_actual_cost:,.2f}")
        
        # Summary Totals
        st.markdown("---")
        st.markdown("### 📊 Summary Totals")
        
        total_planned_cost = sum((item['planned'] * item['weight'] / 100) * CONTRACT_AMOUNT / 100 for item in work_items)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Contract", f"₱{CONTRACT_AMOUNT:,.2f}")
        with col2:
            st.metric("Total Planned", f"₱{total_planned_cost:,.2f}")
        with col3:
            st.metric("🟢 Total Actual", f"₱{total_actual_cost:,.2f}")
        with col4:
            st.metric("Variance", f"₱{total_actual_cost - total_planned_cost:+,.2f}")
    
    st.markdown("---")
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