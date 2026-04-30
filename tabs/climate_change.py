# tabs/climate_change.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import io
import base64
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected
from utils.local_storage import save_file, delete_file, get_file_size, file_exists

def show():
    """Display Climate Change Adaptation Tab - 7 Top-Level Sections"""
    
    st.markdown("# 🌍 Climate Change Adaptation")
    st.caption("Integrating Climate and Disaster Risk Governance for a Resilient Mountain Province")
    
    # Initialize session state for CCA data
    if 'cca_plans' not in st.session_state:
        st.session_state.cca_plans = []
    
    if 'lccap_documents' not in st.session_state:
        st.session_state.lccap_documents = []
    
    if 'repository_documents' not in st.session_state:
        st.session_state.repository_documents = []
    
    if 'ccet_tags' not in st.session_state:
        st.session_state.ccet_tags = []
    
    if 'mpcfs_documents' not in st.session_state:
        st.session_state.mpcfs_documents = []
    
    if 'mpcfs_tasks' not in st.session_state:
        st.session_state.mpcfs_tasks = []
    
    if 'mpcfs_photos' not in st.session_state:
        st.session_state.mpcfs_photos = []
    
    if 'mpcfs_issues' not in st.session_state:
        st.session_state.mpcfs_issues = []
    
    if 'mpcfs_generated_reports' not in st.session_state:
        st.session_state.mpcfs_generated_reports = []
    
    if 'climate_projections' not in st.session_state:
        st.session_state.climate_projections = {
            "temperature": {},
            "rainfall": {},
            "extreme_events": {}
        }
    
    # Create 7 top-level tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 CCA Plans",
        "📊 CCA Analytics",
        "🌾 MPCFS Hub",
        "🌡️ Climate Projection",
        "📁 Document Repository",
        "📖 Coffee Table Book",
        "🔗 Related Modules"
    ])
    
    # TAB 1: CCA PLANS (with sub-tabs)
    with tab1:
        sub_tab1, sub_tab2 = st.tabs([
            "📋 LCCAP & CCA Plans",
            "🏷️ CCET Analysis (NCCAP Priorities)"
        ])
        
        with sub_tab1:
            show_lccap_repository()
        
        with sub_tab2:
            show_ccet_analysis()
    
    # TAB 2: CCA ANALYTICS
    with tab2:
        show_cca_analytics()
    
    # TAB 3: MPCFS HUB
    with tab3:
        st.markdown("## 🌾 MPCFS Project Hub")
        st.caption("Mountain Province Climate Field School Project | ₱271M Investment")
        
        sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8 = st.tabs([
            "📊 Master Dashboard",
            "🏗️ Infrastructure",
            "👨‍🌾 Capability Building",
            "🔬 Research & Extension",
            "📋 Gantt Chart",
            "📁 Document Management",
            "📸 Photo Gallery",
            "📄 Reports"
        ])
        
        with sub1:
            show_mpcfs_master_dashboard()
        with sub2:
            show_mpcfs_scurve_tracker()
        with sub3:
            show_mpcfs_capability_placeholder()
        with sub4:
            show_mpcfs_research_placeholder()
        with sub5:
            show_mpcfs_gantt()
        with sub6:
            show_mpcfs_document_management()
        with sub7:
            show_mpcfs_photo_gallery()
        with sub8:
            show_mpcfs_report_generator()
    
    # TAB 4: CLIMATE PROJECTION
    with tab4:
        show_climate_projections()
    
    # TAB 5: DOCUMENT REPOSITORY
    with tab5:
        show_document_repository()
    
    # TAB 6: COFFEE TABLE BOOK
    with tab6:
        show_mpcfs_coffee_table_book()
    
    # TAB 7: RELATED MODULES
    with tab7:
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
    # CREATE 7 TOP-LEVEL TABS (NO LONG SCROLL)
    # ============================================================
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 CCA Plans",
        "🌾 MPCFS Hub",
        "📊 CCA Analytics",
        "🌡️ Climate Projection",
        "📁 Document Repository",
        "📖 Coffee Table Book",
        "🔗 Related Modules"
    ])
    
        # ============================================================
    # TAB 1: CCA PLANS & PROGRAMS
    # ============================================================
    with tab1:
        show_cca_plans()
      
    
        # ============================================================
    # TAB 2: MPCFS HUB (with 8 sub-tabs inside)
    # ============================================================
    with tab2:
        st.markdown("## 🌾 MPCFS Project Hub")
        st.caption("Mountain Province Climate Field School Project | ₱271M Investment")
        
        # Create 8 sub-tabs inside this tab
        sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8 = st.tabs([
            "📊 Master Dashboard",
            "🏗️ Infrastructure",
            "👨‍🌾 Capability Building",
            "🔬 Research & Extension",
            "📋 Gantt Chart",
            "📁 Document Management",
            "📸 Photo Gallery",
            "📄 Reports"
        ])
        
        with sub1:
            show_mpcfs_master_dashboard()
        with sub2:
            show_mpcfs_scurve_tracker()
        with sub3:
            show_mpcfs_capability_placeholder()
        with sub4:
            show_mpcfs_research_placeholder()
        with sub5:
            show_mpcfs_gantt()
        with sub6:
            show_mpcfs_document_management()
        with sub7:
            show_mpcfs_photo_gallery()
        with sub8:
            show_mpcfs_report_generator()

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
    
    if st.session_state.cca_plans:
        df = pd.DataFrame(st.session_state.cca_plans)
        st.dataframe(df[['plan_type', 'title', 'year', 'status', 'budget']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("No CCA plans added yet. Click 'Add CCA Plan' to get started.")

def show_mpcfs_capability_placeholder():
    """Placeholder for Capability Building Component"""
    
    st.markdown("#### 👨‍🌾 Capability Building Component")
    st.caption("This component will be activated when data is uploaded")
    
    st.info("""
    ### 📌 Capability Building Component - Coming Soon
    
    This section will track:
    - **Progress S-Curve** for Capability Building activities
    - **Budget utilization** and financial tracking
    - **Key performance indicators** specific to Capability Building
    - **Milestone tracking** and deliverables
    
    ### How to Activate:
    1. Prepare your Capability Building S-Curve data in Excel
    2. Upload the file when the feature is available
    3. The dashboard will automatically include this component
    
    ### Expected Data Format:
    - Weekly progress percentages
    - Budget allocation
    - Target milestones
    - Actual accomplishments
    """)
    
    # Preview placeholder chart
    st.markdown("#### Preview (Awaiting Data)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[0, 0, 0, 0, 0], mode='lines+markers', name='Progress'))
    fig.update_layout(title="Capability Building Progress Preview", height=300, yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def show_mpcfs_research_placeholder():
    """Placeholder for Research & Extension Component"""
    
    st.markdown("#### 🔬 Research & Extension Component")
    st.caption("This component will be activated when data is uploaded")
    
    st.info("""
    ### 📌 Research & Extension Component - Coming Soon
    
    This section will track:
    - **Progress S-Curve** for Research & Extension activities
    - **Budget utilization** and financial tracking
    - **Key performance indicators** specific to Research & Extension
    - **Milestone tracking** and deliverables
    
    ### How to Activate:
    1. Prepare your Research & Extension S-Curve data in Excel
    2. Upload the file when the feature is available
    3. The dashboard will automatically include this component
    
    ### Expected Data Format:
    - Weekly progress percentages
    - Budget allocation
    - Target milestones
    - Actual accomplishments
    """)
    
    # Preview placeholder chart
    st.markdown("#### Preview (Awaiting Data)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[1, 2, 3, 4, 5], y=[0, 0, 0, 0, 0], mode='lines+markers', name='Progress'))
    fig.update_layout(title="Research & Extension Progress Preview", height=300, yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)


def show_mpcfs_coffee_table_book():
    """Coffee Table Book - Repository for MPCFS project documentation"""
    
    st.markdown("#### 📖 Coffee Table Book")
    st.caption("Compile project experiences, beneficiary stories, and documentation")
    
    st.markdown("""
    ### About the MPCFS Coffee Table Book
    
    This feature will document the journey of the Mountain Province Climate Field School Project, capturing:
    - **Timelines**: Key project milestones and events
    - **Photos**: Visual documentation of project activities
    - **Beneficiary Stories**: Personal accounts from farmers and community members
    - **Challenges Encountered**: Problems faced and how they were addressed
    - **Issues and Resolutions**: Tracking of issues and their solutions
    - **Lessons Learned**: Insights and best practices for replication
    
    ### How to Use
    1. Upload photos and documents related to the project
    2. Add beneficiary stories and testimonials
    3. Document challenges and how they were resolved
    4. Compile everything for the final Coffee Table Book publication
    """)
    
    # Placeholder for future features
    st.info("Coffee Table Book repository will be available in the next phase. Start collecting your project documentation!")

def show_document_repository():
    """Document repository for CCA documents"""
    
    st.markdown("#### 📁 Document Repository")
    st.caption("Central repository for all climate change adaptation documents")
    
    # Similar to MPCFS document management, but for CCA
    doc_categories = [
        "CCA Plans", "Adaptation Projects", "Climate Projections", 
        "Research Reports", "Training Materials", "Policy Documents",
        "Monitoring Reports", "Case Studies", "Photos", "Videos", "Other"
    ]
    
    with st.expander("📤 Upload Document", expanded=False):
        with st.form("upload_cca_document"):
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
                if 'cca_documents' not in st.session_state:
                    st.session_state.cca_documents = []
                st.session_state.cca_documents.append(new_doc)
                
                if doc_file:
                    save_path = f"cca_documents/{doc_file.name}"
                    os.makedirs("cca_documents", exist_ok=True)
                    with open(save_path, "wb") as f:
                        f.write(doc_file.getbuffer())
                    st.success(f"✅ Document '{doc_title}' uploaded and saved locally!")
                else:
                    st.success(f"✅ Document '{doc_title}' recorded!")
                st.rerun()
    
    if 'cca_documents' in st.session_state and st.session_state.cca_documents:
        df = pd.DataFrame(st.session_state.cca_documents)
        categories = ["All"] + list(df['category'].unique())
        selected_category = st.selectbox("Filter by Category", categories)
        
        if selected_category != "All":
            df = df[df['category'] == selected_category]
        
        st.dataframe(df[['title', 'category', 'date', 'version', 'author']], use_container_width=True, hide_index=True)
    else:
        st.info("No documents uploaded yet.")

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
    
    # MPCFS Sub-tabs - 9 tabs
    mpcfstab1, mpcfstab2, mpcfstab3, mpcfstab4, mpcfstab5, mpcfstab6, mpcfstab7, mpcfstab8, mpcfstab9 = st.tabs([
        "📊 Master Dashboard",
        "🏗️ Infrastructure",
        "👨‍🌾 Capability Building",
        "🔬 Research & Extension",
        "📋 Gantt Chart",
        "📁 Document Management",
        "📸 Photo Gallery",
        "📄 Reports",
        "📖 Coffee Table Book"
    ])
    
    with mpcfstab1:
        show_mpcfs_master_dashboard()
    
    with mpcfstab2:
        show_mpcfs_scurve_tracker()
    
    with mpcfstab3:
        show_mpcfs_capability_placeholder()
    
    with mpcfstab4:
        show_mpcfs_research_placeholder()
    
    with mpcfstab5:
        show_mpcfs_gantt()
    
    with mpcfstab6:
        show_mpcfs_document_management()
    
    with mpcfstab7:
        show_mpcfs_photo_gallery()
    
    with mpcfstab8:
        show_mpcfs_report_generator()
    
    with mpcfstab9:
        show_mpcfs_coffee_table_book()


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
    """Gantt Chart - Reflects actual Infrastructure progress"""
    
    st.markdown("#### 📋 Project Gantt Chart & Timeline")
    st.caption("Track project milestones by infrastructure sub-component")
    
    # Get actual Infrastructure progress
    infra_progress = 25.75
    
    # All tasks with updated progress based on actual data
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
    
    # Overall Progress Summary
    st.markdown("---")
    st.markdown("### 📊 Overall Project Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Infrastructure Progress", f"{infra_progress:.2f}%", delta="As of March 31, 2026")
    with col2:
        st.metric("Active Components", "1/3", delta="Infrastructure Only")
    with col3:
        st.metric("Overall Status", "✅ ON TRACK", delta="Based on Revised Plan")
    
    st.info("📌 Capability Building and Research & Extension components will be added when data becomes available.")


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
    """Generate PDF reports with issues tracking and S-Curve - COMPLETE VERSION"""
    
    st.markdown("#### 📄 Report Generator")
    st.caption("Generate PDF reports with progress data, issues log, and S-Curve")
    
    # ============================================================
    # INITIALIZE SESSION STATE
    # ============================================================
    
    if 'mpcfs_issues' not in st.session_state:
        st.session_state.mpcfs_issues = []
    
    if 'mpcfs_generated_reports' not in st.session_state:
        st.session_state.mpcfs_generated_reports = []
    
    # ============================================================
    # GET CURRENT PROJECT DATA
    # ============================================================
    
    TOTAL_CONTRACT = 249_040_900.00
    TOTAL_ACTUAL = 64_198_219.78
    OVERALL_PROGRESS = 25.75
    
    # ============================================================
    # ISSUES & CONCERNS LOG
    # ============================================================
    
    st.markdown("### ⚠️ Issues & Concerns Log")
    st.caption("Track project issues, attach photos, and link to work items")
    
    # Add New Issue Form
    with st.expander("➕ Add New Issue", expanded=False):
        with st.form("add_issue_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                issue_title = st.text_input("Issue Title", placeholder="e.g., Weather delay at foundation site")
                priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])
                reported_by = st.selectbox("Reported By", ["Project Engineer", "Finance Officer", "Project Manager", "Other"])
            with col2:
                issue_date = st.date_input("Date Reported", datetime.now().date())
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
            
            issue_description = st.text_area("Description", placeholder="Detailed description of the issue...", height=100)
            action_taken = st.text_area("Action Taken / Resolution", placeholder="What has been done to address this?", height=100)
            
            submitted = st.form_submit_button("💾 Save Issue", use_container_width=True)
            
            if submitted and issue_title:
                new_issue = {
                    "id": len(st.session_state.mpcfs_issues) + 1,
                    "title": issue_title,
                    "description": issue_description,
                    "priority": priority,
                    "reported_by": reported_by,
                    "date": issue_date.isoformat(),
                    "status": status,
                    "action_taken": action_taken,
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.mpcfs_issues.append(new_issue)
                st.success(f"✅ Issue '{issue_title}' added!")
                st.rerun()
    
    # Display Issues Table
    if st.session_state.mpcfs_issues:
        st.markdown("#### 📋 Current Issues Log")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "🔴 High", "🟡 Medium", "🟢 Low"])
        with col3:
            show_resolved = st.checkbox("Show Resolved Issues", value=True)
        
        filtered_issues = st.session_state.mpcfs_issues
        if status_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['status'] == status_filter]
        if priority_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['priority'] == priority_filter]
        if not show_resolved:
            filtered_issues = [i for i in filtered_issues if i['status'] not in ["Resolved", "Closed"]]
        
        if filtered_issues:
            df_issues = pd.DataFrame(filtered_issues)
            display_cols = ['id', 'title', 'priority', 'status', 'reported_by', 'date']
            st.dataframe(df_issues[display_cols], use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # ============================================================
    # REPORT GENERATION
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
    
    include_issues = st.checkbox("📋 Include Open Issues in Report", value=True)
    include_chart = st.checkbox("📈 Include S-Curve Chart", value=True)
    save_report = st.checkbox("💾 Save report for later viewing", value=True)
    
    if st.button("📄 Generate Report Preview", type="primary", use_container_width=True):
        
        open_issues = [i for i in st.session_state.mpcfs_issues if i['status'] not in ["Resolved", "Closed"]]
        
        # Simple chart representation
        chart_html = ""
        if include_chart:
            chart_html = f"""
            <div class="chart-container">
                <p><strong>Progress S-Curve (as of Week 80 - March 31, 2026)</strong></p>
                <p>📈 Original Plan Target: 64.31%</p>
                <p>📈 Revised Plan Target: 16.02%</p>
                <p>✅ Actual Progress: {OVERALL_PROGRESS:.2f}%</p>
                <p>📊 Slippage vs Original: {OVERALL_PROGRESS - 64.31:+.2f}%</p>
                <p>📊 Slippage vs Revised: {OVERALL_PROGRESS - 16.02:+.2f}%</p>
            </div>
            """
        
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>MPCFS Progress Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; }}
                .header {{ text-align: center; border-bottom: 3px solid #2ecc71; padding-bottom: 20px; margin-bottom: 30px; }}
                .title {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
                .subtitle {{ font-size: 14px; color: #7f8c8d; }}
                .section {{ margin-bottom: 30px; }}
                .section-title {{ font-size: 18px; font-weight: bold; background-color: #ecf0f1; padding: 10px; border-left: 4px solid #2ecc71; }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }}
                .kpi-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center; }}
                .kpi-value {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
                .table {{ width: 100%; border-collapse: collapse; }}
                .table th, .table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                .table th {{ background-color: #2ecc71; color: white; }}
                .issue {{ border-left: 4px solid #e74c3c; padding-left: 10px; margin-bottom: 10px; }}
                .footer {{ text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 10px; }}
                .chart-container {{ text-align: center; margin: 20px 0; padding: 20px; background-color: #f9f9f9; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">MOUNTAIN PROVINCE CLIMATE FIELD SCHOOL (MPCFS)</div>
                <div class="subtitle">{report_type} | {report_period}</div>
                <div class="subtitle">Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
            </div>
            
            <div class="section">
                <div class="section-title">📊 Executive Summary</div>
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-value">{OVERALL_PROGRESS:.2f}%</div>
                        <div class="kpi-label">Infrastructure Progress</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-value">₱{TOTAL_ACTUAL:,.2f}</div>
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
                    <tr><td>Total Contract Amount</td><td>{TOTAL_CONTRACT:,.2f}</td></tr>
                    <tr><td>Actual Cost Utilized</td><td>{TOTAL_ACTUAL:,.2f}</td></tr>
                    <tr><td>Remaining Budget</td><td>{TOTAL_CONTRACT - TOTAL_ACTUAL:,.2f}</td></tr>
                    <tr><td>Financial Utilization Rate</td><td>{(TOTAL_ACTUAL/TOTAL_CONTRACT)*100:.1f}%</td></tr>
                </table>
            </div>
        """
        
        if include_chart:
            report_html += f"""
            <div class="section">
                <div class="section-title">📈 S-Curve Chart</div>
                {chart_html}
            </div>
            """
        
        if include_issues and open_issues:
            report_html += """
            <div class="section">
                <div class="section-title">⚠️ Open Issues & Concerns</div>
            """
            for issue in open_issues:
                report_html += f"""
                <div class="issue">
                    <strong>{issue['title']}</strong><br>
                    <strong>Priority:</strong> {issue['priority']} | <strong>Status:</strong> {issue['status']}<br>
                    <strong>Reported:</strong> {issue['reported_by']} on {issue['date'][:10]}<br>
                    <strong>Description:</strong> {issue['description']}<br>
                </div>
                """
            report_html += "</div>"
        
        report_html += f"""
            <div class="footer">
                <p>Generated by INDC System - MPCFS Module | Mountain Province PDRRMO</p>
            </div>
        </body>
        </html>
        """
        
        st.markdown("---")
        st.markdown("### 📋 Report Preview")
        st.components.v1.html(report_html, height=500, scrolling=True)
        
        st.markdown("### 📥 Download Report")
        
        st.download_button(
            label="📄 Download as HTML (Print to PDF)",
            data=report_html,
            file_name=f"MPCFS_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            mime="text/html",
            use_container_width=True
        )
        
        if save_report:
            report_record = {
                "id": len(st.session_state.mpcfs_generated_reports) + 1,
                "report_type": report_type,
                "report_period": report_period,
                "generated_at": datetime.now().isoformat(),
                "html_content": report_html,
                "progress": OVERALL_PROGRESS
            }
            st.session_state.mpcfs_generated_reports.append(report_record)
            st.success(f"✅ Report saved!")
    
    # ============================================================
    # SAVED REPORTS SECTION
    # ============================================================
    
    st.markdown("---")
    st.markdown("### 📚 Saved Reports")
    
    if st.session_state.mpcfs_generated_reports:
        reports_df = pd.DataFrame(st.session_state.mpcfs_generated_reports)
        st.dataframe(reports_df[['id', 'report_type', 'report_period', 'generated_at', 'progress']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("No saved reports yet. Generate a report and check 'Save report for later viewing'.")

def show_mpcfs_coffee_table_book():
    """Coffee Table Book - Repository for MPCFS project documentation"""
    
    st.markdown("#### 📖 Coffee Table Book")
    st.caption("Compile project experiences, beneficiary stories, and documentation")
    
    st.markdown("""
    ### About the MPCFS Coffee Table Book
    
    This feature will document the journey of the Mountain Province Climate Field School Project, capturing:
    - **Timelines**: Key project milestones and events
    - **Photos**: Visual documentation of project activities
    - **Beneficiary Stories**: Personal accounts from farmers and community members
    - **Challenges Encountered**: Problems faced and how they were addressed
    - **Issues and Resolutions**: Tracking of issues and their solutions
    - **Lessons Learned**: Insights and best practices for replication
    
    ### How to Use
    1. Upload photos and documents related to the project
    2. Add beneficiary stories and testimonials
    3. Document challenges and how they were resolved
    4. Compile everything for the final Coffee Table Book publication
    """)
    
    # Placeholder for future features
    st.info("Coffee Table Book repository will be available in the next phase. Start collecting your project documentation!")

def show_mpcfs_master_dashboard():
    """Master Dashboard - Reflects actual Infrastructure data"""
    
    st.markdown("#### 📊 MPCFS Master Dashboard")
    st.caption("Overall project progress across all components")
    
    # Get actual Infrastructure data from session state
    infra_progress = 25.75  # Hardcoded from Excel
    infra_target_original = 64.31
    infra_target_revised = 16.02
    infra_cost = 64_198_219.78  # Total actual cost
    
    # Component 2 & 3 placeholders (will be activated when data is added)
    cap_progress = st.session_state.get('capability_progress', 0)
    cap_target = st.session_state.get('capability_target', 0)
    cap_status = "⏳ Pending Data" if cap_progress == 0 else "🟢 Active"
    
    res_progress = st.session_state.get('research_progress', 0)
    res_target = st.session_state.get('research_target', 0)
    res_status = "⏳ Pending Data" if res_progress == 0 else "🟢 Active"
    
    # Calculate active components
    active_components = 1  # Infrastructure is active
    if cap_progress > 0:
        active_components += 1
    if res_progress > 0:
        active_components += 1
    
    total_progress = (infra_progress + cap_progress + res_progress) / 3 if active_components == 3 else infra_progress
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Project Progress", f"{total_progress:.2f}%", 
                  delta=f"{active_components}/3 Components Active")
    with col2:
        slippage = infra_progress - infra_target_revised
        st.metric("Infrastructure", f"{infra_progress:.2f}%", 
                  delta=f"{slippage:+.2f}% vs Target")
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
    st.progress(infra_progress / 100, text=f"{infra_progress:.2f}% Complete")
    st.caption(f"Contract Amount: ₱249,040,900 | Utilized: ₱{infra_cost:,.2f}")
    st.caption(f"📊 Original Plan Target at Week 80: {infra_target_original:.2f}% | Revised Plan Target: {infra_target_revised:.2f}%")
    
    # Capability Building
    st.markdown("#### 👨‍🌾 Capability Building Component")
    if cap_progress > 0:
        st.progress(cap_progress / 100, text=f"{cap_progress:.1f}% Complete")
    else:
        st.info("📌 Data pending. Upload Capability Building S-Curve to activate this component.")
        st.progress(0, text="Awaiting Data")
    
    # Research & Extension
    st.markdown("#### 🔬 Research & Extension Component")
    if res_progress > 0:
        st.progress(res_progress / 100, text=f"{res_progress:.1f}% Complete")
    else:
        st.info("📌 Data pending. Upload Research & Extension S-Curve to activate this component.")
        st.progress(0, text="Awaiting Data")
    
    st.markdown("---")
    
    # Combined Progress Chart
    st.markdown("### 📈 Combined Progress Trend")
    
    # Create data for chart
    components = ["Infrastructure", "Capability Building", "Research & Extension"]
    progress_values = [infra_progress, cap_progress if cap_progress > 0 else 0, res_progress if res_progress > 0 else 0]
    target_values = [infra_target_revised, cap_target if cap_target > 0 else 0, res_target if res_target > 0 else 0]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name="Actual Progress", x=components, y=progress_values, 
                         marker_color=['#2ecc71', '#3498db', '#9b59b6'],
                         text=[f"{v:.1f}%" for v in progress_values], textposition='outside'))
    fig.add_trace(go.Bar(name="Target", x=components, y=target_values,
                         marker_color=['#f39c12', '#f39c12', '#f39c12'],
                         text=[f"{v:.1f}%" for v in target_values], textposition='outside'))
    
    fig.update_layout(title="Component Progress vs Target",
                      xaxis_title="Component",
                      yaxis_title="Progress (%)",
                      height=400,
                      yaxis_range=[0, 100],
                      barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Quick stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Completed Milestones**")
        st.markdown("- Infrastructure: Site development in progress")
        st.markdown(f"- Infrastructure Progress: {infra_progress:.2f}% as of March 31, 2026")
        st.markdown("- Farmer training modules prepared")
        st.markdown("- Demo farm sites identified")
    
    with col2:
        st.markdown("**🎯 Next Milestones**")
        st.markdown("- Complete Infrastructure foundation by Q2 2025")
        st.markdown("- Launch Capability Building program")
        st.markdown("- Establish research protocols")
        
def show_mpcfs_scurve_tracker():
    """MPCFS Infrastructure S-Curve Tracker - COMPLETE with small Edit button and all categories"""
    
    st.markdown("#### 🏗️ Infrastructure Component - S-Curve Tracker")
    st.caption("Track physical and financial progress | Contract: ₱249,040,900.00")
    
    CONTRACT_AMOUNT = 249_040_900.00
    PREFIX = "infrastructure_"
    
    # ============================================================
    # FIX: INITIALIZE SESSION STATE FOR DEPLOYMENT
    # ============================================================
    # This prevents the "KeyError" on first load in Streamlit Cloud
    if f'{PREFIX}cost' not in st.session_state:
        # Create a list of zeros for 12 months (default)
        st.session_state[f'{PREFIX}cost'] = [0] * 12
    
    if f'{PREFIX}months' not in st.session_state:
        st.session_state[f'{PREFIX}months'] = 12
    
    if f'{PREFIX}plan_start' not in st.session_state:
        st.session_state[f'{PREFIX}plan_start'] = TOTAL_PLANNED
    
    if f'{PREFIX}actual_start' not in st.session_state:
        st.session_state[f'{PREFIX}actual_start'] = TOTAL_ACTUAL
    # ============================================================
    
    # ============================================================
    # HARDCODED TOTALS (from your Excel - ensures 25.75% accuracy)
    # ============================================================
    TOTAL_CONTRACT = 249_040_900.00
    TOTAL_PLANNED = 39_800_688.78
    TOTAL_ACTUAL = 64_198_219.78
    
    # HARDCODED KPI VALUES (from your Excel - NOT calculated)
    OVERALL_PROGRESS = 25.75  # Fixed at 25.75%
    ORIGINAL_PLAN_TARGET = 64.31
    REVISED_PLAN_TARGET = 16.02
    
    slippage_vs_original = OVERALL_PROGRESS - ORIGINAL_PLAN_TARGET  # -38.56%
    slippage_vs_revised = OVERALL_PROGRESS - REVISED_PLAN_TARGET    # +9.73%
    
    # ============================================================
    # COMPLETE WORK ITEMS DATA (with proper categories)
    # ============================================================
    
    if f'{PREFIX}work_items' not in st.session_state:
        work_items = [
            # Civil Works
            {"no": "A.1.1 (8)", "description": "Provision of Field Office for the Engineer (Rental Basis)", "category": "Civil Works", "contract": 1_360_800.00, "planned": 353_808.00, "actual": 353_808.00},
            {"no": "A.1.2 (2)", "description": "Provision of 4x4 Pick Up Type Service Vehicle", "category": "Civil Works", "contract": 2_289_000.00, "planned": 595_140.00, "actual": 595_140.00},
            {"no": "B.3", "description": "Permits and Clearances", "category": "Civil Works", "contract": 315_000.00, "planned": 315_000.00, "actual": 315_000.00},
            {"no": "B.5", "description": "Project Billboard and Signboard", "category": "Civil Works", "contract": 10_500.00, "planned": 2_782.50, "actual": 2_782.50},
            {"no": "B.7 (2)", "description": "Occupational Safety and Health Program", "category": "Civil Works", "contract": 3_061_108.31, "planned": 795_888.16, "actual": 795_888.16},
            {"no": "B.9", "description": "Mobilization/Demobilization", "category": "Civil Works", "contract": 2_174_130.00, "planned": 1_087_065.00, "actual": 1_087_065.00},
            {"no": "B.13", "description": "Additional Geotechnical Investigation", "category": "Civil Works", "contract": 315_000.00, "planned": 315_000.00, "actual": 315_000.00},
            {"no": "B.25", "description": "Detailed Engineering and Architectural Design", "category": "Civil Works", "contract": 424_499.30, "planned": 424_499.30, "actual": 424_499.30},
            {"no": "101(1)", "description": "Removal of Structures and Obstructions", "category": "Civil Works", "contract": 9_419.10, "planned": 9_419.10, "actual": 9_419.10},
            {"no": "105(1)", "description": "Subgrade Preparation (Common Material)", "category": "Civil Works", "contract": 100_708.37, "planned": 0, "actual": 0},
            {"no": "200", "description": "Aggregate Subbase Course", "category": "Civil Works", "contract": 537_793.26, "planned": 0, "actual": 0},
            {"no": "311(1)a.5", "description": "PCC Pavement (Plain) - Conventional Method, 280mm thk", "category": "Civil Works", "contract": 2_042_941.22, "planned": 0, "actual": 0},
            # Structural Works
            {"no": "404", "description": "Reinforcing Steel Bar, Grade 40 (Minor Structures)", "category": "Structural", "contract": 3_529_569.12, "planned": 796_999.61, "actual": 2_834_045.19},
            {"no": "405", "description": "Structural Concrete Class A (Minor Structures)", "category": "Structural", "contract": 4_908_408.38, "planned": 475_053.48, "actual": 1_740_048.11},
            {"no": "803(1)a", "description": "Structure Excavation (Common Soil)", "category": "Structural", "contract": 1_562_882.11, "planned": 1_562_882.11, "actual": 1_357_262.72},
            {"no": "804(1)a", "description": "Embankment from Structure Excavation", "category": "Structural", "contract": 443_158.05, "planned": 419_832.80, "actual": 411_315.06},
            {"no": "804(4)", "description": "Gravel Fill", "category": "Structural", "contract": 1_572_896.70, "planned": 1_572_896.70, "actual": 1_336_224.42},
            {"no": "807 (2)", "description": "Softscape", "category": "Structural", "contract": 1_422_989.40, "planned": 0, "actual": 0},
            {"no": "807 (5)", "description": "Hardscape", "category": "Structural", "contract": 6_465_568.50, "planned": 0, "actual": 0},
            {"no": "1706(1)", "description": "Overhaul", "category": "Structural", "contract": 724_377.36, "planned": 724_377.36, "actual": 560_761.32},
            {"no": "900(1)c2", "description": "Structural Concrete for Footing and Slab on Fill", "category": "Structural", "contract": 4_259_204.38, "planned": 3_293_796.15, "actual": 3_561_495.88},
            {"no": "900(1)", "description": "Structural Concrete for Columns, Beams", "category": "Structural", "contract": 10_295_802.78, "planned": 5_183_185.50, "actual": 3_449_789.39},
            {"no": "902(1) a", "description": "Reinforcing Steel for Concrete Structures", "category": "Structural", "contract": 23_180_568.48, "planned": 9_746_375.62, "actual": 7_625_371.03},
            {"no": "903(1)", "description": "Formworks and Falseworks", "category": "Structural", "contract": 3_163_251.96, "planned": 1_239_654.24, "actual": 948_291.30},
            {"no": "1001(1)a5", "description": "Inlets, 350mm Concrete Inlet", "category": "Structural", "contract": 458_838.00, "planned": 0, "actual": 0},
            {"no": "1001(6)", "description": "Catch Basin (Concrete)", "category": "Structural", "contract": 27_369.90, "planned": 0, "actual": 0},
            {"no": "1001(8)", "description": "Sewer Line Works", "category": "Structural", "contract": 629_164.60, "planned": 0, "actual": 0},
            {"no": "1001(9)", "description": "Storm Drainage and Downspout", "category": "Structural", "contract": 483_462.60, "planned": 0, "actual": 0},
            {"no": "1001(11)", "description": "Septic Vault, Concrete", "category": "Structural", "contract": 1_086_527.60, "planned": 0, "actual": 543_263.80},
            {"no": "1002 (6)", "description": "Cold Waterline Pipes and Fittings", "category": "Structural", "contract": 916_106.20, "planned": 164_899.12, "actual": 0},
            {"no": "1002(4)", "description": "Plumbing Fixtures", "category": "Structural", "contract": 2_538_525.20, "planned": 0, "actual": 0},
            {"no": "1003(1)", "description": "4.5mm Fiber Cement Board on Metal Frame Ceiling", "category": "Architectural", "contract": 2_889_430.72, "planned": 0, "actual": 0},
            {"no": "1003(2)h", "description": "Wood Wall", "category": "Architectural", "contract": 2_174_130.00, "planned": 0, "actual": 0},
            {"no": "1003(12)", "description": "Fascia Board", "category": "Architectural", "contract": 666_777.34, "planned": 0, "actual": 0},
            {"no": "1006 (6)", "description": "Steel Doors and Frames", "category": "Architectural", "contract": 492_614.00, "planned": 0, "actual": 0},
            {"no": "1008 (2)", "description": "Aluminum Glass Window", "category": "Architectural", "contract": 1_943_862.80, "planned": 0, "actual": 0},
            {"no": "1010(2)b", "description": "Doors, Wood Panel", "category": "Architectural", "contract": 118_791.12, "planned": 0, "actual": 0},
            {"no": "1010(2)a", "description": "Doors, Flush", "category": "Architectural", "contract": 240_002.05, "planned": 0, "actual": 0},
            {"no": "1011(2)", "description": "Roll-Up Doors", "category": "Architectural", "contract": 410_569.50, "planned": 0, "actual": 0},
            {"no": "1013(2)a2", "description": "Metal Roofing Accessory (Flashings)", "category": "Architectural", "contract": 139_070.88, "planned": 0, "actual": 0},
            {"no": "1013(2)c", "description": "Metal Roofing Accessory (Gutter)", "category": "Architectural", "contract": 127_510.32, "planned": 0, "actual": 0},
            {"no": "1014(1)b2", "description": "Prepainted Metal Sheets", "category": "Architectural", "contract": 3_314_899.73, "planned": 0, "actual": 0},
            {"no": "1016(1)a", "description": "Waterproofing Cement Base", "category": "Architectural", "contract": 1_574_900.12, "planned": 0, "actual": 0},
            {"no": "1018(1)", "description": "Glazed Tiles and Trims", "category": "Architectural", "contract": 797_243.66, "planned": 0, "actual": 0},
            {"no": "1018 (2)", "description": "Unglazed Tiles", "category": "Architectural", "contract": 4_165_425.00, "planned": 0, "actual": 0},
            {"no": "1027(1)", "description": "Cement Plaster Finish", "category": "Architectural", "contract": 2_140_452.97, "planned": 0, "actual": 0},
            {"no": "1032(1)a", "description": "Painting Works (Masonry/Concrete)", "category": "Architectural", "contract": 4_004_939.44, "planned": 0, "actual": 0},
            {"no": "1032(1)a", "description": "Painting Works (Wood)", "category": "Architectural", "contract": 23_090.00, "planned": 0, "actual": 0},
            {"no": "1032(1)c", "description": "Painting Works (Steel)", "category": "Architectural", "contract": 2_502_971.16, "planned": 406_988.56, "actual": 0},
            {"no": "1033(1)", "description": "Metal Deck Panel", "category": "Architectural", "contract": 6_193_981.87, "planned": 1_495_102.80, "actual": 0},
            {"no": "1046 (2) a1", "description": "CHB Non Load Bearing 100mm", "category": "Architectural", "contract": 118_967.81, "planned": 0, "actual": 0},
            {"no": "1046 (2) a2", "description": "CHB Non Load Bearing 150mm", "category": "Architectural", "contract": 4_127_956.28, "planned": 0, "actual": 0},
            {"no": "1047 (1)", "description": "Structural Steel", "category": "Structural", "contract": 35_288_324.70, "planned": 7_410_548.19, "actual": 28_583_543.01},
            {"no": "1047 (2)a", "description": "Structural Steel (Trusses)", "category": "Structural", "contract": 4_375_481.81, "planned": 0, "actual": 823_222.92},
            {"no": "1047 (2)b", "description": "Structural Steel (Purlins)", "category": "Structural", "contract": 827_081.41, "planned": 0, "actual": 0},
            {"no": "1047 (3)a", "description": "Anchor Bolts", "category": "Structural", "contract": 3_747_979.20, "planned": 0, "actual": 3_453_256.80},
            {"no": "1047 (3)b", "description": "Sagrods", "category": "Structural", "contract": 820_277.20, "planned": 0, "actual": 0},
            {"no": "1047 (3)c", "description": "Turnbuckle", "category": "Structural", "contract": 243_321.60, "planned": 0, "actual": 0},
            {"no": "1047 (3)d", "description": "Cross Bracing", "category": "Structural", "contract": 267_291.65, "planned": 0, "actual": 0},
            {"no": "1047 (5)", "description": "Steel Plates", "category": "Structural", "contract": 4_480_181.19, "planned": 1_409_494.48, "actual": 3_071_726.77},
            {"no": "1051 (6)", "description": "Railing", "category": "Architectural", "contract": 1_584_459.10, "planned": 0, "actual": 0},
            # Electrical Works
            {"no": "1100(10)", "description": "Conduits, Boxes & Fittings", "category": "Electrical", "contract": 1_017_858.10, "planned": 0, "actual": 0},
            {"no": "1101(33)", "description": "Wires and Wiring Devices", "category": "Electrical", "contract": 1_793_186.80, "planned": 0, "actual": 0},
            {"no": "1102 (1)", "description": "Panelboard with Breakers", "category": "Electrical", "contract": 662_409.30, "planned": 0, "actual": 0},
            {"no": "1103(1)", "description": "Lighting Fixtures and Lamps", "category": "Electrical", "contract": 3_184_990.80, "planned": 0, "actual": 0},
            {"no": "1102(8)", "description": "Generator Set", "category": "Electrical", "contract": 5_980_380.00, "planned": 0, "actual": 0},
            {"no": "1102(18)", "description": "Solar Panel System", "category": "Electrical", "contract": 22_104_416.30, "planned": 0, "actual": 0},
            # Mechanical Works
            {"no": "1202 (1)", "description": "Automatic Fire Sprinkler System", "category": "Mechanical", "contract": 6_786_391.50, "planned": 0, "actual": 0},
            {"no": "1208(1)", "description": "Fire Alarm System", "category": "Mechanical", "contract": 219_026.90, "planned": 0, "actual": 0},
            {"no": "1201(1)", "description": "Water Pumping System", "category": "Mechanical", "contract": 2_341_385.80, "planned": 0, "actual": 0},
            {"no": "1726", "description": "Electro Mechanical for Pumping Station", "category": "Mechanical", "contract": 1_680_801.90, "planned": 0, "actual": 0},
            # Equipment
            {"no": "SPL-1", "description": "Furnitures", "category": "Equipment", "contract": 1_993_866.00, "planned": 0, "actual": 0},
            {"no": "SPL-2", "description": "Retractable Seat", "category": "Equipment", "contract": 2_254_853.00, "planned": 0, "actual": 0},
            {"no": "SPL-3", "description": "Appliances and Equipment", "category": "Equipment", "contract": 6_077_820.00, "planned": 0, "actual": 0},
            {"no": "SPL-4", "description": "Automated Weather Stations (AWS)", "category": "Equipment", "contract": 14_616_000.00, "planned": 0, "actual": 0},
            {"no": "SPL-5", "description": "Laboratory & Food Processing Equipment", "category": "Equipment", "contract": 8_215_958.10, "planned": 0, "actual": 0},
        ]
        st.session_state[f'{PREFIX}work_items'] = work_items
    
    work_items = st.session_state[f'{PREFIX}work_items']
    
    # ============================================================
    # EDIT MODAL (for inline editing)
    # ============================================================
    
    if f'{PREFIX}editing_item' not in st.session_state:
        st.session_state[f'{PREFIX}editing_item'] = None
    
    # ============================================================
    # S-CURVE DATA (Hardcoded from your Excel)
    # ============================================================
    
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
    current_week_idx = 79  # Week 80
    
    # ============================================================
    # KPI CARDS (HARDCODED VALUES - 25.75%)
    # ============================================================
    
    st.markdown("### 📊 Key Performance Indicators")
    st.markdown("> 💡 **Tip:** Edit the 🟢 **highlighted columns** in the table below to update progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Progress", f"{OVERALL_PROGRESS:.2f}%", delta=f"₱{TOTAL_ACTUAL:,.0f} / ₱{TOTAL_CONTRACT:,.0f}")
    
    with col2:
        st.metric("Slippage vs Original Plan", f"{slippage_vs_original:+.2f}%", delta="Target at Week 80: 64.31%")
    
    with col3:
        st.metric("Slippage vs Revised Plan", f"{slippage_vs_revised:+.2f}%", delta="Target at Week 80: 16.02%")
    
    with col4:
        status = "✅ AHEAD" if slippage_vs_revised > 0 else "🟡 ON TRACK" if slippage_vs_revised == 0 else "🔴 BEHIND"
        st.metric("Overall Status", status, delta="As of Week 80 (Mar 31, 2026)")
    
    st.markdown("---")
    
    # ============================================================
    # PROGRESS S-CURVE
    # ============================================================
    
    st.markdown("### 📈 S-Curve: Planned vs Actual Progress")
    st.markdown("**📍 As of: Week 80 (March 31, 2026)**")
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=weeks[:len(original_plan_weekly)], y=original_plan_weekly, mode='lines', name='Original Plan', line=dict(color='#1f77b4', width=2, dash='dash'), opacity=0.8))
    fig1.add_trace(go.Scatter(x=weeks[:len(revised_plan_weekly)], y=revised_plan_weekly, mode='lines', name='Revised Plan', line=dict(color='#ff7f0e', width=2, dash='dot'), opacity=0.8))
    fig1.add_trace(go.Scatter(x=weeks[:current_week_idx + 1], y=actual_weekly[:current_week_idx + 1], mode='lines+markers', name='Actual Progress', line=dict(color='#2ca02c', width=3), marker=dict(size=4)))
    fig1.add_vline(x=current_week_idx + 1, line_dash="dash", line_color="#7f7f7f", line_width=1.5, annotation_text=f"Week {current_week_idx + 1}", annotation_position="top right")
    fig1.update_layout(title="Project Progress S-Curve (September 2024 - May 2028)", xaxis_title="Week Number", yaxis_title="Cumulative Progress (%)", yaxis_range=[0, 105], height=400, hovermode='x unified', plot_bgcolor='white')
    st.plotly_chart(fig1, use_container_width=True)
    
    # ============================================================
    # COST S-CURVE
    # ============================================================
    
    st.markdown("### 💰 Cost S-Curve: Planned vs Actual Expenditure")
    
    original_cost = [(p / 100) * TOTAL_CONTRACT / 1_000_000 for p in original_plan_weekly]
    revised_cost = [(p / 100) * TOTAL_CONTRACT / 1_000_000 for p in revised_plan_weekly]
    actual_cost = [(p / 100) * TOTAL_CONTRACT / 1_000_000 for p in actual_weekly]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=weeks[:len(original_cost)], y=original_cost, mode='lines', name='Original Plan', line=dict(color='#1f77b4', width=2, dash='dash'), opacity=0.8))
    fig2.add_trace(go.Scatter(x=weeks[:len(revised_cost)], y=revised_cost, mode='lines', name='Revised Plan', line=dict(color='#ff7f0e', width=2, dash='dot'), opacity=0.8))
    fig2.add_trace(go.Scatter(x=weeks[:current_week_idx + 1], y=actual_cost[:current_week_idx + 1], mode='lines+markers', name='Actual Cost', line=dict(color='#d62728', width=3), marker=dict(size=4)))
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
        st.info(f"📋 **Revised Plan at Week 80:** 16.02%")
    with col3:
        st.success(f"✅ **Actual Progress at Week 80:** {OVERALL_PROGRESS:.2f}%")
    
    st.markdown("---")
    
    # ============================================================
    # EDIT ITEM MODAL (small popup)
    # ============================================================
    
    if st.session_state[f'{PREFIX}editing_item'] is not None:
        editing_no = st.session_state[f'{PREFIX}editing_item']
        editing_item = next((item for item in work_items if item['no'] == editing_no), None)
        
        if editing_item:
            with st.container():
                st.markdown(f"**✏️ Editing: {editing_item['no']} - {editing_item['description']}**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_actual = st.number_input("Actual Amount (₱)", value=float(editing_item['actual']), step=10000.0, key="edit_actual")
                with col2:
                    new_contract = st.number_input("Contract Amount (₱)", value=float(editing_item['contract']), step=10000.0, key="edit_contract")
                with col3:
                    new_planned = st.number_input("Planned Amount (₱)", value=float(editing_item['planned']), step=10000.0, key="edit_planned")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if st.button("💾 Save", key="save_edit", use_container_width=True):
                        editing_item['actual'] = new_actual
                        editing_item['contract'] = new_contract
                        editing_item['planned'] = new_planned
                        st.session_state[f'{PREFIX}work_items'] = work_items
                        st.session_state[f'{PREFIX}editing_item'] = None
                        st.success("✅ Item updated!")
                        st.rerun()
                with col2:
                    if st.button("❌ Cancel", key="cancel_edit", use_container_width=True):
                        st.session_state[f'{PREFIX}editing_item'] = None
                        st.rerun()
                st.markdown("---")
    
    # ============================================================
    # ADD NEW ITEM FORM
    # ============================================================
    
    with st.expander("➕ Add New Work Item", expanded=False):
        with st.form("add_item_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_no = st.text_input("Item No.", placeholder="e.g., NEW-001")
                new_description = st.text_input("Description", placeholder="Work item description")
            with col2:
                new_category = st.selectbox("Category", ["Civil Works", "Structural", "Architectural", "Electrical", "Mechanical", "Equipment"])
                new_contract = st.number_input("Contract Amount (₱)", min_value=0.0, value=0.0, step=10000.0)
            
            col1, col2 = st.columns(2)
            with col1:
                new_planned = st.number_input("Planned Amount (₱)", min_value=0.0, value=0.0, step=10000.0)
            with col2:
                new_actual = st.number_input("Actual Amount (₱)", min_value=0.0, value=0.0, step=10000.0)
            
            if st.form_submit_button("➕ Add Item", type="primary"):
                if new_no and new_description:
                    new_item = {
                        "no": new_no,
                        "description": new_description,
                        "category": new_category,
                        "contract": new_contract,
                        "planned": new_planned,
                        "actual": new_actual,
                    }
                    work_items.append(new_item)
                    st.session_state[f'{PREFIX}work_items'] = work_items
                    st.success(f"✅ Item '{new_no}' added!")
                    st.rerun()
                else:
                    st.error("Please enter Item No. and Description")
    
    # ============================================================
    # ITEMIZED WORK DETAILS TABLE (with small Edit button)
    # ============================================================
    
    st.markdown("### 📋 Itemized Work Details")
    st.markdown(f"> 🟢 **GREEN highlighted columns** are editable. Edit then click **💾 SAVE ALL CHANGES**")
    st.markdown(f"> 📊 **Total Items: {len(work_items)}** | Total Contract: ₱{TOTAL_CONTRACT:,.2f}")
    
    # Category filter - ALL categories now
    categories = ["All", "Civil Works", "Structural", "Architectural", "Electrical", "Mechanical", "Equipment"]
    selected_category = st.selectbox("🔍 Filter by Category", categories)
    
    if selected_category != "All":
        filtered_items = [item for item in work_items if item.get('category') == selected_category]
    else:
        filtered_items = work_items
    
    if filtered_items:
        # Create display dataframe
        display_data = []
        for item in filtered_items:
            planned_pct = (item['planned'] / item['contract']) * 100 if item['contract'] > 0 else 0
            actual_pct = (item['actual'] / item['contract']) * 100 if item['contract'] > 0 else 0
            variance = actual_pct - planned_pct
            
            # Status logic
            if actual_pct >= 99.5:
                status = "✅ Completed"
            elif actual_pct == 0:
                status = "⚪ Not Started"
            elif variance > 1:
                status = "✅ Ahead"
            elif variance < -1:
                status = "🔴 Behind"
            else:
                status = "🟡 On Track"
            
            display_data.append({
                "Item No.": item['no'],
                "Description": item['description'][:60] + "..." if len(item['description']) > 60 else item['description'],
                "Category": item['category'],
                "Contract (₱)": item['contract'],
                "Planned (₱)": item['planned'],
                "🟢 Actual (₱)": item['actual'],
                "Planned (%)": planned_pct,
                "🟢 Actual (%)": actual_pct,
                "Variance (%)": variance,
                "Status": status,
            })
        
        df_items = pd.DataFrame(display_data)
        
        # Display as regular dataframe with Edit column
        col_config = {
            "Item No.": st.column_config.TextColumn("Item No.", width="small"),
            "Description": st.column_config.TextColumn("Description", width="large"),
            "Category": st.column_config.TextColumn("Category", width="small"),
            "Contract (₱)": st.column_config.NumberColumn("Contract (₱)", format="₱%.0f"),
            "Planned (₱)": st.column_config.NumberColumn("Planned (₱)", format="₱%.0f"),
            "🟢 Actual (₱)": st.column_config.NumberColumn("🟢 Actual (₱)", format="₱%.0f"),
            "Planned (%)": st.column_config.NumberColumn("Planned (%)", format="%.2f"),
            "🟢 Actual (%)": st.column_config.NumberColumn("🟢 Actual (%)", format="%.2f"),
            "Variance (%)": st.column_config.NumberColumn("Variance (%)", format="%+.2f"),
            "Status": st.column_config.TextColumn("Status"),
        }
        
        edited_df = st.data_editor(
            df_items,
            use_container_width=True,
            hide_index=True,
            column_config=col_config,
            disabled=["Item No.", "Description", "Category", "Contract (₱)", "Planned (₱)", "Planned (%)", "Variance (%)", "Status"],
        )
        
        # Small Edit buttons below each row using columns
        st.markdown("**✏️ Click Edit to modify an item:**")
        
        # Create edit buttons in a grid
        cols_per_row = 8
        for i in range(0, len(filtered_items), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(filtered_items):
                    item = filtered_items[idx]
                    with col:
                        if st.button(f"✏️ {item['no']}", key=f"edit_btn_{item['no']}_{idx}", use_container_width=True):
                            st.session_state[f'{PREFIX}editing_item'] = item['no']
                            st.rerun()
        
        # ============================================================
        # SAVE ALL CHANGES BUTTON
        # ============================================================
        
        # Update work_items from edited_df
        for idx, row in edited_df.iterrows():
            if idx < len(filtered_items):
                original_item = filtered_items[idx]
                if original_item['actual'] != row['🟢 Actual (₱)']:
                    for item in work_items:
                        if item['no'] == original_item['no']:
                            item['actual'] = row['🟢 Actual (₱)']
                            break
                    st.session_state[f'{PREFIX}work_items'] = work_items
        
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        with col1:
            if st.button("💾 SAVE ALL CHANGES", type="primary", use_container_width=True):
                st.session_state[f'{PREFIX}work_items'] = work_items
                st.success("✅ All changes saved!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset All to Zero", use_container_width=True):
                for item in work_items:
                    item['actual'] = 0
                st.session_state[f'{PREFIX}work_items'] = work_items
                st.success("✅ Reset complete!")
                st.rerun()
        
        with col3:
            if st.button("📊 Export to CSV", use_container_width=True):
                export_df = pd.DataFrame(work_items)
                csv = export_df.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv, file_name=f"mpcfs_work_items_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", key="export_csv_btn")
        
        with col4:
            st.caption(f"📊 Overall Progress: {OVERALL_PROGRESS:.2f}% | Items: {len(work_items)}")
        
        # ============================================================
        # SUMMARY TOTALS
        # ============================================================
        
        st.markdown("---")
        st.markdown("### 📊 Summary Totals")
        
        total_actual_sum = sum(item['actual'] for item in work_items)
        total_planned_sum = sum(item['planned'] for item in work_items)
        total_contract_sum = sum(item['contract'] for item in work_items)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Contract", f"₱{total_contract_sum:,.2f}")
        with col2:
            st.metric("Total Planned", f"₱{total_planned_sum:,.2f}")
        with col3:
            st.metric("🟢 Total Actual", f"₱{total_actual_sum:,.2f}")
        with col4:
            st.metric("Variance", f"₱{total_actual_sum - total_planned_sum:+,.2f}")
        with col5:
            st.metric("Items Count", f"{len(work_items)}")
        
        # ============================================================
        # PROGRESS SUMMARY BY STATUS
        # ============================================================
        
        st.markdown("---")
        st.markdown("### 📊 Progress Summary by Status")
        
        completed_items = 0
        ahead_items = 0
        on_track_items = 0
        behind_items = 0
        not_started = 0
        
        for item in work_items:
            actual_pct = (item['actual'] / item['contract']) * 100 if item['contract'] > 0 else 0
            planned_pct = (item['planned'] / item['contract']) * 100 if item['contract'] > 0 else 0
            variance = actual_pct - planned_pct
            
            if actual_pct >= 99.5:
                completed_items += 1
            elif actual_pct == 0:
                not_started += 1
            elif variance > 1:
                ahead_items += 1
            elif variance < -1:
                behind_items += 1
            else:
                on_track_items += 1
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("✅ Completed", completed_items)
        with col2:
            st.metric("✅ Ahead", ahead_items)
        with col3:
            st.metric("🟡 On Track", on_track_items)
        with col4:
            st.metric("🔴 Behind", behind_items)
        with col5:
            st.metric("⚪ Not Started", not_started)
    
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
    """Display Climate Change Projections - Complete CERAM/CLIRAM Module"""
    
    import streamlit.components.v1 as components
    import os
    
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(current_dir, "climate_projection.html")
    
    # Read the HTML file
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        components.html(html_content, height=800, scrolling=True)
        
    except FileNotFoundError:
        st.error(f"HTML file not found at: {html_path}")
        st.info("Please ensure climate_projection.html exists in the tabs folder.")

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

# ============================================================
# LCCAP REPOSITORY, CCET ANALYSIS, DOCUMENT REPOSITORY
# ============================================================

def show_lccap_repository():
    """Display LCCAP documents repository with file upload"""
    
    st.markdown("#### 📋 LCCAP & CCA Plans Repository")
    st.caption("Upload, store, and manage LCCAP documents and CCA plans")
    
    with st.expander("➕ Upload LCCAP Document", expanded=False):
        with st.form("upload_lccap_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                doc_title = st.text_input("Document Title", placeholder="e.g., Barlig LCCAP 2024-2028")
                municipality = st.selectbox("Municipality", ["Provincial", "Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"])
                year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
            with col2:
                status = st.selectbox("Status", ["Draft", "For Approval", "Approved", "Under Review", "Expired"])
                file_type = st.selectbox("Document Type", ["LCCAP", "PCCAP", "CDRA", "AIP", "DRRM Plan", "Other"])
                tags = st.text_input("Tags", placeholder="comma separated")
            
            description = st.text_area("Description")
            uploaded_file = st.file_uploader("Upload File", type=['pdf', 'docx'], key="lccap_upload")
            
            submitted = st.form_submit_button("💾 Upload Document")
            
            if submitted and doc_title and uploaded_file:
                os.makedirs("lccap_documents", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{uploaded_file.name}"
                file_path = os.path.join("lccap_documents", filename)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                new_doc = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": doc_title,
                    "municipality": municipality,
                    "year": year,
                    "status": status,
                    "file_type": file_type,
                    "tags": tags,
                    "description": description,
                    "filename": filename,
                    "original_name": uploaded_file.name,
                    "file_size": f"{uploaded_file.size / 1024:.1f} KB",
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.lccap_documents.append(new_doc)
                st.success(f"✅ Document '{doc_title}' uploaded!")
                st.rerun()
    
    if st.session_state.lccap_documents:
        st.markdown("#### 📄 Uploaded LCCAP Documents")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            mun_filter = st.selectbox("Filter by Municipality", ["All"] + sorted(list(set([d.get('municipality', 'N/A') for d in st.session_state.lccap_documents]))))
        with col2:
            status_filter = st.selectbox("Filter by Status", ["All", "Draft", "For Approval", "Approved", "Under Review", "Expired"])
        with col3:
            year_filter = st.selectbox("Filter by Year", ["All"] + sorted(list(set([d.get('year', 0) for d in st.session_state.lccap_documents])), reverse=True))
        
        filtered_docs = st.session_state.lccap_documents
        if mun_filter != "All":
            filtered_docs = [d for d in filtered_docs if d.get('municipality') == mun_filter]
        if status_filter != "All":
            filtered_docs = [d for d in filtered_docs if d.get('status') == status_filter]
        if year_filter != "All":
            filtered_docs = [d for d in filtered_docs if d.get('year') == year_filter]
        
        for doc in filtered_docs:
            with st.expander(f"📄 {doc.get('title', 'Untitled')} - {doc.get('municipality', 'N/A')} ({doc.get('year', 'N/A')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Municipality:** {doc.get('municipality', 'N/A')}")
                    st.markdown(f"**Year:** {doc.get('year', 'N/A')}")
                    st.markdown(f"**Status:** {doc.get('status', 'N/A')}")
                with col2:
                    st.markdown(f"**Tags:** {doc.get('tags', 'N/A')}")
                    st.markdown(f"**File Size:** {doc.get('file_size', 'N/A')}")
                
                st.markdown(f"**Description:** {doc.get('description', 'No description')}")
                
                file_path = os.path.join("lccap_documents", doc.get('filename', ''))
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(label=f"📎 Download", data=f, file_name=doc.get('original_name', 'document.pdf'), key=f"download_lccap_{doc.get('id')}")
                
                if st.button(f"🗑️ Delete", key=f"del_lccap_{doc.get('id')}"):
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    st.session_state.lccap_documents = [d for d in st.session_state.lccap_documents if d.get('id') != doc.get('id')]
                    st.rerun()
    else:
        st.info("📭 No LCCAP documents uploaded yet.")

def show_ccet_analysis():
    """Display CCET Analysis with NCCAP Strategic Priorities"""
    
    st.markdown("#### 🏷️ CCET Analysis: Climate Change Expenditure Tagging")
    st.caption("Align programs, projects, and activities with NCCAP Strategic Priorities")
    
    nccap_priorities = {
        "P1": {"name": "Food Security", "description": "Agriculture, fisheries, livestock, food distribution", "color": "#28a745"},
        "P2": {"name": "Water Security", "description": "Water supply, irrigation, watershed management", "color": "#17a2b8"},
        "P3": {"name": "Ecosystem Stability", "description": "Reforestation, coastal protection, biodiversity", "color": "#20c997"},
        "P4": {"name": "Human Security", "description": "DRRM, health, evacuation centers, early warning", "color": "#dc3545"},
        "P5": {"name": "Climate Justice", "description": "Vulnerable sectors, indigenous peoples, gender", "color": "#fd7e14"}
    }
    
    st.markdown("### 📋 NCCAP Strategic Priorities")
    cols = st.columns(5)
    for i, (code, priority) in enumerate(nccap_priorities.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background:{priority['color']}; color:white; padding:10px; border-radius:8px; text-align:center;">
                <strong>{code}</strong><br><small>{priority['name']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🏷️ Tag PPAs with NCCAP Priorities")
    
    ppas = st.session_state.get('ppas', [])
    
    if ppas:
        ppa_options = {f"{p.get('title', 'Untitled')}": p for p in ppas}
        selected_ppa_title = st.selectbox("Select PPA to Tag", list(ppa_options.keys()))
        
        if selected_ppa_title:
            selected_ppa = ppa_options[selected_ppa_title]
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Title:** {selected_ppa.get('title', 'N/A')}")
                st.markdown(f"**Budget:** ₱{selected_ppa.get('budget', 0):,.2f}")
            with col2:
                st.markdown(f"**Status:** {selected_ppa.get('status', 'N/A')}")
            
            priority_options = {f"{code}: {priority['name']}": code for code, priority in nccap_priorities.items()}
            selected_priority_display = st.selectbox("Priority", list(priority_options.keys()))
            selected_priority_code = priority_options[selected_priority_display]
            
            climate_rationale = st.text_area("Climate Rationale", placeholder="Explain how this PPA addresses climate change...")
            
            if st.button("💾 Save CCET Tag", type="primary"):
                new_tag = {
                    "ppa_id": selected_ppa.get('id'),
                    "ppa_title": selected_ppa.get('title'),
                    "nccap_priority": selected_priority_code,
                    "nccap_name": nccap_priorities[selected_priority_code]['name'],
                    "climate_rationale": climate_rationale,
                    "budget": selected_ppa.get('budget', 0),
                    "tagged_at": datetime.now().isoformat()
                }
                st.session_state.ccet_tags.append(new_tag)
                st.success(f"✅ Tagged with {selected_priority_code}")
                st.rerun()
    else:
        st.info("📭 No PPAs found. Go to Plan Management tab to add PPAs first.")
    
    if st.session_state.get('ccet_tags'):
        st.markdown("---")
        st.markdown("### 📊 Tagged PPAs Summary")
        tags_df = pd.DataFrame(st.session_state.ccet_tags)
        st.dataframe(tags_df[['ppa_title', 'nccap_priority', 'budget', 'tagged_at']], use_container_width=True, hide_index=True)
        
        if st.button("📥 Export CCET Report (CSV)"):
            csv = tags_df.to_csv(index=False)
            st.download_button("Download CSV", data=csv, file_name=f"ccet_report_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

def show_ccet_analysis():
    """Display CCET Analysis with NCCAP Strategic Priorities - Excel Upload Enabled"""
    
    st.markdown("#### 🏷️ CCET Analysis: Climate Change Expenditure Tagging")
    st.caption("Upload CCET Excel file (AIP CCET Data Bank) to analyze and tag PPAs to NCCAP priorities")
    
    # NCCAP Strategic Priorities (8 priorities)
    nccap_priorities = {
        "P1": {"name": "Food Security", "short": "Food Security", "color": "#28a745"},
        "P2": {"name": "Water Sufficiency", "short": "Water Sufficiency", "color": "#17a2b8"},
        "P3": {"name": "Ecosystem Stability", "short": "Ecosystem Stability", "color": "#20c997"},
        "P4": {"name": "Human Security", "short": "Human Security", "color": "#dc3545"},
        "P5": {"name": "Climate-smart Industries", "short": "Climate Industries", "color": "#fd7e14"},
        "P6": {"name": "Sustainable Energy", "short": "Sustainable Energy", "color": "#ffc107"},
        "P7": {"name": "Knowledge & Capacity", "short": "Knowledge & Capacity", "color": "#6f42c1"},
        "P8": {"name": "Cross-cutting Impacts", "short": "Cross-cutting", "color": "#e83e8c"}
    }
    
    # ============================================================
    # EXCEL UPLOAD SECTION
    # ============================================================
    
    with st.expander("📤 Upload CCET Excel File (AIP CCET Data Bank)", expanded=False):
        st.markdown("""
        **Upload your CCET Excel file** (the AIP CCET Data Bank format from DILG/DBM/CCC)
        
        The file should contain columns like:
        - Province, AIP Reference Code, P/A/P Description
        - Implementing Office, Start Date, Completion Date
        - PS, MOOE, CO, Total Budget
        - CCA, CCM, CC Typology Code
        - Sector, Strategic Priority, CC Response
        """)
        
        uploaded_file = st.file_uploader(
            "Choose Excel File", 
            type=['xlsx', 'xls'],
            key="ccet_upload"
        )
        
        if uploaded_file is not None:
            try:
                # Read all sheet names
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                st.info(f"📑 Found sheets: {', '.join(sheet_names)}")
                
                # Let user select the main data sheet
                selected_sheet = st.selectbox("Select the main data sheet", sheet_names)
                
                # Read the selected sheet
                df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
                
                st.success(f"✅ Loaded {len(df)} rows from sheet '{selected_sheet}'")
                
                # Remove 'Region' column if it exists
                if 'Region' in df.columns:
                    df = df.drop(columns=['Region'])
                    st.info("🗑️ Removed 'Region' column")
                
                # Store in session state
                st.session_state.ccet_data = df.to_dict('records')
                st.session_state.ccet_columns = list(df.columns)
                st.session_state.ccet_loaded = True
                
                # Show preview
                st.markdown("### 📊 Data Preview (First 10 rows)")
                st.dataframe(df.head(10), use_container_width=True)
                
            except Exception as e:
                st.error(f"Error reading file: {e}")
    
    # ============================================================
    # DISPLAY NCCAP PRIORITIES (SIMPLIFIED CARDS)
    # ============================================================
    
    st.markdown("### 🎯 NCCAP Strategic Priorities (8 Priorities)")
    
    # Display as 4 rows of 2 cards
    priority_items = list(nccap_priorities.items())
    for i in range(0, len(priority_items), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(priority_items):
                code, priority = priority_items[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div style="background:{priority['color']}; color:white; padding:12px; border-radius:10px; margin-bottom:10px; text-align:center;">
                        <strong>{code}</strong><br>
                        <strong>{priority['short']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ============================================================
    # DISPLAY UPLOADED DATA (SIMPLIFIED FOR LGUs)
    # ============================================================
    
    if st.session_state.get('ccet_loaded', False) and st.session_state.get('ccet_data'):
        
        st.markdown("### 📋 CCET Data Bank - Simplified View")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            provinces = list(set([item.get('Province', 'N/A') for item in st.session_state.ccet_data if item.get('Province')]))
            province_filter = st.selectbox("Filter by Province", ["All"] + provinces)
        
        with col2:
            sectors = list(set([item.get('Sector', 'N/A') for item in st.session_state.ccet_data if item.get('Sector')]))
            sector_filter = st.selectbox("Filter by Sector", ["All"] + sectors)
        
        with col3:
            priority_filter = st.selectbox("Filter by NCCAP Priority", ["All"] + list(nccap_priorities.keys()))
        
        # Filter data
        filtered_data = st.session_state.ccet_data
        if province_filter != "All":
            filtered_data = [item for item in filtered_data if item.get('Province') == province_filter]
        if sector_filter != "All":
            filtered_data = [item for item in filtered_data if item.get('Sector') == sector_filter]
        
        # Display as cards (LGU-friendly)
        st.markdown(f"**Found {len(filtered_data)} PPAs**")
        
        for idx, item in enumerate(filtered_data[:50]):  # Limit to 50 for performance
            # Get NCCAP priority from Strategic Priority column or default
            strategic_priority = item.get('Strategic Priority', '')
            priority_code = "P4"  # Default to Human Security
            for code, p in nccap_priorities.items():
                if p['short'].lower() in str(strategic_priority).lower() or p['name'].lower() in str(strategic_priority).lower():
                    priority_code = code
                    break
            
            total_budget = item.get('Total Budget', 0)
            if isinstance(total_budget, str):
                total_budget = 0
            cc_expenditure = item.get('CCA', 0) or item.get('CCM', 0)
            if isinstance(cc_expenditure, str):
                cc_expenditure = 0
            
            with st.expander(f"📋 {item.get('P/A/P Description', 'Untitled')[:80]}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Implementing Office:** {item.get('Implementing Office', 'N/A')}")
                    st.markdown(f"**Schedule:** {item.get('Start Date', 'N/A')} → {item.get('Completion Date', 'N/A')}")
                with col2:
                    st.markdown(f"**Total Budget:** ₱{total_budget:,.2f}" if total_budget else "**Total Budget:** N/A")
                    st.markdown(f"**CC Expenditure:** ₱{cc_expenditure:,.2f}" if cc_expenditure else "**CC Expenditure:** N/A")
                with col3:
                    st.markdown(f"**NCCAP Priority:** {priority_code}: {nccap_priorities[priority_code]['short']}")
                    st.markdown(f"**CC Response:** {item.get('CC Response', 'N/A')}")
                
                st.markdown(f"**Expected Outputs:** {item.get('Expected Outputs', 'N/A')}")
                
                # Validation check
                typology_code = item.get('CC Typology Code', '')
                has_cc_expenditure = cc_expenditure > 0
                if has_cc_expenditure and not typology_code:
                    st.warning("⚠️ Has CC expenditure but missing Typology Code")
                elif not has_cc_expenditure and typology_code:
                    st.warning("⚠️ Has Typology Code but no CC expenditure")
                else:
                    st.success("✅ Valid CCET entry")
        
        # ============================================================
        # CCET SUMMARY BY NCCAP PRIORITY
        # ============================================================
        
        st.markdown("---")
        st.markdown("### 📊 CCET Summary by NCCAP Priority")
        
        # Calculate budget by priority
        priority_budgets = {code: 0 for code in nccap_priorities.keys()}
        for item in st.session_state.ccet_data:
            strategic_priority = item.get('Strategic Priority', '')
            for code, p in nccap_priorities.items():
                if p['short'].lower() in str(strategic_priority).lower() or p['name'].lower() in str(strategic_priority).lower():
                    total_budget = item.get('Total Budget', 0)
                    if isinstance(total_budget, (int, float)):
                        priority_budgets[code] += total_budget
                    break
        
        # Display as bar chart
        summary_df = pd.DataFrame([
            {"Priority": f"{code}: {nccap_priorities[code]['short']}", "Budget (₱)": priority_budgets[code]}
            for code in nccap_priorities.keys()
        ])
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
        with col2:
            if summary_df['Budget (₱)'].sum() > 0:
                fig = px.bar(summary_df, x='Priority', y='Budget (₱)', title='Budget by NCCAP Priority', color='Priority')
                st.plotly_chart(fig, use_container_width=True)
        
        # Export option
        st.markdown("---")
        if st.button("📥 Export CCET Report (CSV)"):
            export_df = pd.DataFrame(st.session_state.ccet_data)
            csv = export_df.to_csv(index=False)
            st.download_button(
                "Download CSV", 
                data=csv, 
                file_name=f"ccet_report_{datetime.now().strftime('%Y%m%d')}.csv", 
                mime="text/csv"
            )
    
    else:
        st.info("📭 No CCET data loaded. Upload an Excel file to begin analysis.")
        
        # Show sample format
        with st.expander("📋 Sample CCET Data Format", expanded=False):
            st.markdown(""")
            Your Excel file should have these columns (standard AIP CCET Data Bank format):
            
            | Column | Description |
       """)

def show_document_repository():
    """Display document repository with search"""
    
    st.markdown("#### 📁 Document Repository")
    st.caption("CCA/CCM literatures, CCC references, and climate-related documents")
    
    categories = ["CCC Reference", "PAGASA Data", "IPCC Report", "LCCAP Guide", "CDRA Guide", "Climate Literature", "Training Material", "Policy Document", "Other"]
    
    with st.expander("➕ Add Document", expanded=False):
        with st.form("add_repo_document", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                doc_title = st.text_input("Document Title")
                category = st.selectbox("Category", categories)
                author = st.text_input("Author/Organization")
            with col2:
                year = st.number_input("Year", min_value=1990, max_value=2025, value=2024)
                tags = st.text_input("Tags", placeholder="comma separated")
                language = st.selectbox("Language", ["English", "Filipino", "Other"])
            
            description = st.text_area("Description")
            uploaded_file = st.file_uploader("Upload File", type=['pdf', 'docx'], key="repo_upload")
            
            submitted = st.form_submit_button("💾 Add to Repository")
            
            if submitted and doc_title and uploaded_file:
                os.makedirs("repository_documents", exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{uploaded_file.name}"
                file_path = os.path.join("repository_documents", filename)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                new_doc = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": doc_title,
                    "category": category,
                    "author": author,
                    "year": year,
                    "tags": tags,
                    "language": language,
                    "description": description,
                    "filename": filename,
                    "original_name": uploaded_file.name,
                    "file_size": f"{uploaded_file.size / 1024:.1f} KB",
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.repository_documents.append(new_doc)
                st.success(f"✅ Document '{doc_title}' added!")
                st.rerun()
    
    st.markdown("### 🔍 Search Documents")
    
    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Search by Title, Author, or Tags", placeholder="Enter search term...")
    with col2:
        category_filter = st.selectbox("Filter by Category", ["All"] + categories)
    
    filtered_docs = st.session_state.repository_documents
    
    if search_term:
        search_lower = search_term.lower()
        filtered_docs = [d for d in filtered_docs if 
                        search_lower in d.get('title', '').lower() or
                        search_lower in d.get('author', '').lower() or
                        search_lower in d.get('tags', '').lower() or
                        search_lower in d.get('description', '').lower()]
    
    if category_filter != "All":
        filtered_docs = [d for d in filtered_docs if d.get('category') == category_filter]
    
    st.markdown(f"**Found {len(filtered_docs)} document(s)**")
    
    if filtered_docs:
        for doc in filtered_docs:
            with st.expander(f"📄 {doc.get('title', 'Untitled')} - {doc.get('category', 'N/A')} ({doc.get('year', 'N/A')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Author:** {doc.get('author', 'N/A')}")
                    st.markdown(f"**Category:** {doc.get('category', 'N/A')}")
                with col2:
                    st.markdown(f"**Tags:** {doc.get('tags', 'N/A')}")
                    st.markdown(f"**Year:** {doc.get('year', 'N/A')}")
                
                st.markdown(f"**Description:** {doc.get('description', 'No description')}")
                
                file_path = os.path.join("repository_documents", doc.get('filename', ''))
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button(label=f"📎 Download", data=f, file_name=doc.get('original_name', 'document.pdf'), key=f"download_repo_{doc.get('id')}")
                
                if st.button(f"🗑️ Delete", key=f"del_repo_{doc.get('id')}"):
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    st.session_state.repository_documents = [d for d in st.session_state.repository_documents if d.get('id') != doc.get('id')]
                    st.rerun()
    else:
        st.info("No documents found.")
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
    """Generate PDF reports with issues tracking and S-Curve - COMPLETE VERSION"""
    
    st.markdown("#### 📄 Report Generator")
    st.caption("Generate PDF reports with progress data, issues log, and S-Curve")
    
    # ============================================================
    # INITIALIZE SESSION STATE
    # ============================================================
    
    if 'mpcfs_issues' not in st.session_state:
        st.session_state.mpcfs_issues = []
    
    if 'mpcfs_generated_reports' not in st.session_state:
        st.session_state.mpcfs_generated_reports = []
    
    # ============================================================
    # GET CURRENT PROJECT DATA
    # ============================================================
    
    TOTAL_CONTRACT = 249_040_900.00
    TOTAL_ACTUAL = 64_198_219.78
    TOTAL_PLANNED = 39_800_688.78
    OVERALL_PROGRESS = 25.75
    
    # ============================================================
    # ISSUES & CONCERNS LOG
    # ============================================================
    
    st.markdown("### ⚠️ Issues & Concerns Log")
    st.caption("Track project issues, attach photos, and link to work items")
    
    # Add New Issue Form
    with st.expander("➕ Add New Issue", expanded=False):
        with st.form("add_issue_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                issue_title = st.text_input("Issue Title", placeholder="e.g., Weather delay at foundation site")
                priority = st.selectbox("Priority", ["🔴 High", "🟡 Medium", "🟢 Low"])
                reported_by = st.selectbox("Reported By", ["Project Engineer", "Finance Officer", "Project Manager", "Other"])
            with col2:
                issue_date = st.date_input("Date Reported", datetime.now().date())
                status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
                target_resolution = st.date_input("Target Resolution Date", datetime.now().date())
            
            issue_description = st.text_area("Description", placeholder="Detailed description of the issue...", height=100)
            action_taken = st.text_area("Action Taken / Resolution", placeholder="What has been done to address this?", height=100)
            
            submitted = st.form_submit_button("💾 Save Issue", use_container_width=True)
            
            if submitted and issue_title:
                new_issue = {
                    "id": len(st.session_state.mpcfs_issues) + 1,
                    "title": issue_title,
                    "description": issue_description,
                    "priority": priority,
                    "reported_by": reported_by,
                    "date": issue_date.isoformat(),
                    "target_resolution": target_resolution.isoformat(),
                    "status": status,
                    "action_taken": action_taken,
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.mpcfs_issues.append(new_issue)
                st.success(f"✅ Issue '{issue_title}' added!")
                st.rerun()
    
    # Display Issues Table
    if st.session_state.mpcfs_issues:
        st.markdown("#### 📋 Current Issues Log")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
        with col2:
            priority_filter = st.selectbox("Filter by Priority", ["All", "🔴 High", "🟡 Medium", "🟢 Low"])
        with col3:
            show_resolved = st.checkbox("Show Resolved Issues", value=True)
        
        filtered_issues = st.session_state.mpcfs_issues
        if status_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['status'] == status_filter]
        if priority_filter != "All":
            filtered_issues = [i for i in filtered_issues if i['priority'] == priority_filter]
        if not show_resolved:
            filtered_issues = [i for i in filtered_issues if i['status'] not in ["Resolved", "Closed"]]
        
        if filtered_issues:
            df_issues = pd.DataFrame(filtered_issues)
            display_cols = ['id', 'title', 'priority', 'status', 'reported_by', 'date']
            available_cols = [c for c in display_cols if c in df_issues.columns]
            st.dataframe(df_issues[available_cols], use_container_width=True, hide_index=True)
            
            st.markdown("#### Update Issue Status")
            issue_options = [f"{i['id']}: {i['title']}" for i in filtered_issues]
            if issue_options:
                selected_issue = st.selectbox("Select Issue to Update", issue_options)
                if selected_issue:
                    issue_id = int(selected_issue.split(":")[0])
                    selected_issue_obj = next((i for i in st.session_state.mpcfs_issues if i['id'] == issue_id), None)
                    if selected_issue_obj:
                        col1, col2 = st.columns(2)
                        with col1:
                            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], 
                                                      index=["Open", "In Progress", "Resolved", "Closed"].index(selected_issue_obj['status']))
                        with col2:
                            new_action = st.text_area("Update Action Taken", value=selected_issue_obj.get('action_taken', ''))
                        if st.button("Update Issue"):
                            for i in st.session_state.mpcfs_issues:
                                if i['id'] == issue_id:
                                    i['status'] = new_status
                                    i['action_taken'] = new_action
                                    break
                            st.success("✅ Issue updated!")
                            st.rerun()
    
    st.markdown("---")
    
    # ============================================================
    # REPORT GENERATION
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
    
    include_issues = st.checkbox("📋 Include Open Issues in Report", value=True)
    include_chart = st.checkbox("📈 Include S-Curve Chart", value=True)
    save_report = st.checkbox("💾 Save report for later viewing", value=True)
    
    if st.button("📄 Generate Report Preview", type="primary", use_container_width=True):
        
        open_issues = [i for i in st.session_state.mpcfs_issues if i['status'] not in ["Resolved", "Closed"]]
        
        # Simple chart using HTML/CSS (no matplotlib needed)
        chart_html = ""
        if include_chart:
            chart_html = """
            <div class="chart-container">
                <svg width="100%" height="300" viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
                    <rect x="50" y="250" width="700" height="1" fill="black"/>
                    <rect x="50" y="50" width="1" height="200" fill="black"/>
                    <text x="30" y="255" font-size="10">0</text>
                    <text x="25" y="155" font-size="10">50</text>
                    <text x="25" y="55" font-size="10">100</text>
                    <text x="400" y="280" font-size="12" text-anchor="middle">Week</text>
                    <text x="20" y="150" font-size="12" text-anchor="middle" transform="rotate(-90, 20, 150)">Progress (%)</text>
                </svg>
                <p><strong>Progress S-Curve:</strong> Original Plan (blue dashed), Revised Plan (orange dotted), Actual Progress (green solid)</p>
                <p><strong>Current Status:</strong> 25.75% completion as of Week 80 (March 31, 2026)</p>
            </div>
            """
        
        report_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>MPCFS Progress Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #333; line-height: 1.6; }}
                .header {{ text-align: center; border-bottom: 3px solid #2ecc71; padding-bottom: 20px; margin-bottom: 30px; }}
                .title {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
                .subtitle {{ font-size: 14px; color: #7f8c8d; margin-top: 5px; }}
                .section {{ margin-bottom: 30px; page-break-inside: avoid; }}
                .section-title {{ font-size: 18px; font-weight: bold; background-color: #ecf0f1; padding: 10px; margin-bottom: 15px; border-left: 4px solid #2ecc71; }}
                .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-bottom: 20px; }}
                .kpi-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; text-align: center; background-color: #f9f9f9; }}
                .kpi-value {{ font-size: 28px; font-weight: bold; color: #2c3e50; }}
                .kpi-label {{ font-size: 12px; color: #7f8c8d; margin-top: 5px; }}
                .table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                .table th, .table td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
                .table th {{ background-color: #2ecc71; color: white; }}
                .issue {{ border-left: 4px solid #e74c3c; padding-left: 10px; margin-bottom: 10px; background-color: #fef9f9; }}
                .footer {{ text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 10px; color: #7f8c8d; }}
                .chart-container {{ text-align: center; margin: 20px 0; padding: 20px; background-color: #f9f9f9; border-radius: 8px; }}
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
                        <div class="kpi-value">{OVERALL_PROGRESS:.2f}%</div>
                        <div class="kpi-label">Infrastructure Progress</div>
                    </div>
                    <div class="kpi-card">
                        <div class="kpi-value">₱{TOTAL_ACTUAL:,.2f}</div>
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
                    <tr><td>Total Contract Amount</td><td>{TOTAL_CONTRACT:,.2f}</td></tr>
                    <tr><td>Actual Cost Utilized</td><td>{TOTAL_ACTUAL:,.2f}</td></tr>
                    <tr><td>Remaining Budget</td><td>{TOTAL_CONTRACT - TOTAL_ACTUAL:,.2f}</td></tr>
                    <tr><td>Financial Utilization Rate</td><td>{(TOTAL_ACTUAL/TOTAL_CONTRACT)*100:.1f}%</td></tr>
                </table>
            </div>
        """
        
        if include_chart:
            report_html += f"""
            <div class="section">
                <div class="section-title">📈 S-Curve Chart</div>
                {chart_html}
            </div>
            """
        
        if include_issues and open_issues:
            report_html += """
            <div class="section">
                <div class="section-title">⚠️ Open Issues & Concerns</div>
            """
            for issue in open_issues:
                report_html += f"""
                <div class="issue">
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
                    <li>Infrastructure component at {OVERALL_PROGRESS:.2f}% completion as of March 31, 2026</li>
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
        
        st.markdown("---")
        st.markdown("### 📋 Report Preview")
        st.components.v1.html(report_html, height=500, scrolling=True)
        
        st.markdown("### 📥 Download Report")
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📄 Download as HTML (Print to PDF)",
                data=report_html,
                file_name=f"MPCFS_{report_type.replace(' ', '_').replace('📊', '').strip()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True
            )
        
        with col2:
            st.info("💡 **How to save as PDF:**\n1. Click 'Download as HTML'\n2. Open the HTML file in browser\n3. Press Ctrl+P (or Cmd+P on Mac)\n4. Select 'Save as PDF'\n5. Click Save")
        
        if save_report:
            report_record = {
                "id": len(st.session_state.mpcfs_generated_reports) + 1,
                "report_type": report_type,
                "report_period": report_period,
                "generated_at": datetime.now().isoformat(),
                "html_content": report_html,
                "progress": OVERALL_PROGRESS,
                "total_cost": TOTAL_ACTUAL,
                "issues_count": len(open_issues)
            }
            st.session_state.mpcfs_generated_reports.append(report_record)
            st.success(f"✅ Report saved!")
    
    # ============================================================
    # SAVED REPORTS SECTION
    # ============================================================
    
    st.markdown("---")
    st.markdown("### 📚 Saved Reports")
    
    if st.session_state.mpcfs_generated_reports:
        reports_df = pd.DataFrame(st.session_state.mpcfs_generated_reports)
        display_cols = ['id', 'report_type', 'report_period', 'generated_at', 'progress', 'issues_count']
        if all(col in reports_df.columns for col in display_cols):
            st.dataframe(reports_df[display_cols], use_container_width=True, hide_index=True)
            
            report_ids = [f"{r['id']}: {r['report_type']} ({r['report_period']})" for r in st.session_state.mpcfs_generated_reports]
            selected_report_id = st.selectbox("Select a saved report to view", report_ids)
            
            if selected_report_id:
                report_id = int(selected_report_id.split(":")[0])
                selected_report = next((r for r in st.session_state.mpcfs_generated_reports if r['id'] == report_id), None)
                if selected_report:
                    st.components.v1.html(selected_report['html_content'], height=400, scrolling=True)
                    st.download_button(
                        label="📥 Download Saved Report",
                        data=selected_report['html_content'],
                        file_name=f"MPCFS_Report_{selected_report['id']}.html",
                        mime="text/html"
                    )
    else:
        st.info("No saved reports yet. Generate a report and check 'Save report for later viewing' to see it here.")
    
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

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