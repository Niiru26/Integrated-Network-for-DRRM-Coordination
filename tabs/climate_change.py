# tabs/climate_change.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected

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
    
    # Create tabs for CCA modules
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 CCA Plans & Programs",
        "🌾 MPCFS Project Hub",
        "📊 CCA Analytics",
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
        show_cca_documents()
    
    with tab5:
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
        **Implementing Agency:** MPDRRMO - Research & Planning Division  
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
    
    # MPCFS Sub-tabs
    mpcfstab1, mpcfstab2, mpcfstab3, mpcfstab4, mpcfstab5, mpcfstab6 = st.tabs([
        "📊 Project Dashboard",
        "📋 Gantt Chart & Timeline",
        "📁 Document Management",
        "📸 Photo Gallery",
        "📄 Report Generator",
        "📖 Coffee Table Book"
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
    
    # Define tasks for Gantt chart
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
    df_tasks["Duration"] = (df_tasks["Finish"] - df_tasks["Start"]).dt.days
    
    # Create Gantt chart
    fig = go.Figure()
    
    for i, task in df_tasks.iterrows():
        fig.add_trace(go.Bar(
            x=[task["Duration"]],
            y=[task["Task"]],
            orientation='h',
            marker=dict(
                color='#2ecc71',
                opacity=0.8,
                line=dict(color='#27ae60', width=1)
            ),
            text=f"{task['Complete']}% Complete",
            textposition='outside',
            name=task["Task"]
        ))
    
    fig.update_layout(
        title="Project Timeline",
        xaxis_title="Duration (Days)",
        yaxis_title="Tasks",
        height=500,
        showlegend=False,
        xaxis=dict(tickformat="d")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Task list with status
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
    
    # Document categories
    doc_categories = [
        "Project Proposal", "Communications", "Monitoring Reports", 
        "Narrative Reports", "Financial Reports", "Liquidation Reports",
        "Procurement Documents", "M&E Reports", "Technical Documents",
        "Contracts", "Photos", "Videos", "Other"
    ]
    
    # Upload form
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
                
                # Save file locally
                if doc_file:
                    save_path = f"mpcfs_documents/{doc_file.name}"
                    os.makedirs("mpcfs_documents", exist_ok=True)
                    with open(save_path, "wb") as f:
                        f.write(doc_file.getbuffer())
                    st.success(f"✅ Document '{doc_title}' uploaded and saved locally!")
                else:
                    st.success(f"✅ Document '{doc_title}' recorded!")
                st.rerun()
    
    # Display documents
    if st.session_state.mpcfs_documents:
        df = pd.DataFrame(st.session_state.mpcfs_documents)
        
        # Filter by category
        categories = ["All"] + list(df['category'].unique())
        selected_category = st.selectbox("Filter by Category", categories)
        
        if selected_category != "All":
            df = df[df['category'] == selected_category]
        
        st.dataframe(df[['title', 'category', 'date', 'version', 'author']], 
                     use_container_width=True, hide_index=True)
        
        # Delete functionality
        for doc in st.session_state.mpcfs_documents:
            with st.expander(f"🗑️ Delete: {doc.get('title', 'Untitled')}"):
                st.warning(f"Are you sure you want to delete '{doc.get('title')}'?")
                if st.button(f"Confirm Delete", key=f"del_doc_{doc.get('id')}"):
                    st.session_state.mpcfs_documents = [d for d in st.session_state.mpcfs_documents if d.get('id') != doc.get('id')]
                    st.success("Deleted!")
                    st.rerun()
    else:
        st.info("No documents uploaded yet. Click 'Upload Document' to get started.")


def show_mpcfs_photo_gallery():
    """Photo gallery for MPCFS project documentation"""
    
    st.markdown("#### Project Photo Gallery")
    st.caption("Visual documentation of project activities, events, and progress")
    
    # Upload photo
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
                
                # Save photo locally
                save_path = f"mpcfs_photos/{photo_file.name}"
                os.makedirs("mpcfs_photos", exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(photo_file.getbuffer())
                
                st.success(f"✅ Photo '{photo_title}' uploaded!")
                st.rerun()
    
    # Display gallery
    if st.session_state.mpcfs_photos:
        st.markdown("#### Photo Gallery")
        cols = st.columns(3)
        for i, photo in enumerate(reversed(st.session_state.mpcfs_photos)):
            with cols[i % 3]:
                st.markdown(f"**{photo.get('title')}**")
                st.caption(f"📍 {photo.get('location')}")
                st.caption(f"📅 {photo.get('date')}")
                st.caption(f"📸 {photo.get('photographer')}")
                if st.button(f"🗑️ Delete", key=f"del_photo_{photo.get('id')}"):
                    st.session_state.mpcfs_photos = [p for p in st.session_state.mpcfs_photos if p.get('id') != photo.get('id')]
                    st.rerun()
                st.markdown("---")
    else:
        st.info("No photos uploaded yet. Click 'Upload Photos' to get started.")


def show_mpcfs_report_generator():
    """Generate consolidated reports with cover letter"""
    
    st.markdown("#### Report Generator")
    st.caption("Generate consolidated reports with cover letter for submission")
    
    # Report type selection
    report_type = st.selectbox("Select Report Type", [
        "Narrative Report",
        "Accomplishment Report",
        "Financial Report",
        "Liquidation Report",
        "Monitoring & Evaluation Report",
        "Procurement Report",
        "Consolidated Progress Report"
    ])
    
    report_period = st.selectbox("Reporting Period", [
        "January - March 2024",
        "April - June 2024",
        "July - September 2024",
        "October - December 2024",
        "Annual Report 2024",
        "First Semester 2025",
        "Custom Period"
    ])
    
    if report_period == "Custom Period":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")
    
    # Cover letter details
    st.markdown("#### Cover Letter Details")
    col1, col2 = st.columns(2)
    with col1:
        recipient_name = st.text_input("Recipient Name", placeholder="DR. ALBERT A MOGOL AFP (Ret.)")
        recipient_title = st.text_input("Recipient Title", placeholder="Regional Director, OCD-CAR")
        recipient_office = st.text_input("Recipient Office", placeholder="Office of Civil Defense - CAR")
    with col2:
        thru_name = st.text_input("Through", placeholder="BONIFACIO C. LACWASAN, JR.")
        thru_title = st.text_input("Through Title", placeholder="Provincial Governor")
        subject = st.text_input("Subject", placeholder=f"{report_type} for {report_period}")
    
    # Generate button
    if st.button("📄 Generate Consolidated Report", type="primary"):
        st.markdown("---")
        st.markdown("### 📋 Generated Report Preview")
        
        # Cover Letter
        st.markdown(f"""
        **{recipient_name}**  
        {recipient_title}  
        {recipient_office}
        
        **Thru:** {thru_name}  
        {thru_title}
        
        **Subject:** {subject}
        
        ---
        
        **Dear {recipient_name.split()[0] if recipient_name else 'Sir/Ma\'am'},**
        
        In accordance with the reporting requirements of the Mountain Province Climate Field School Project (MPCFS), we are pleased to submit the {report_type} for the period of {report_period}.
        
        **Highlights:**
        - 1,247 farmers trained in climate-resilient agriculture
        - 3 demonstration farms established
        - 65% completion of Field School facility
        - ₱94.85M utilized out of ₱271M (35%)
        
        **Challenges Encountered:**
        - Weather-related delays in construction
        - Transportation issues in remote barangays
        
        **Recommendations:**
        - Continue capacity building activities
        - Strengthen monitoring systems
        - Scale up farmer reach in 2025
        
        We trust that this report meets your requirements. For any clarification, please do not hesitate to contact us.
        
        Respectfully,
        
        **Project Manager, MPCFS**
        """)
        
        # Email option
        st.markdown("---")
        st.markdown("#### 📧 Submit Report")
        email_address = st.text_input("Recipient Email", placeholder="ocd.car@example.com, dilg.car@example.com")
        
        if st.button("📧 Submit via Email"):
            st.success(f"✅ Report would be sent to {email_address}")
            st.info("Note: Email integration will be fully implemented in the next phase.")
    
    st.info("💡 Pro Tip: All reports will automatically pull data from the project dashboard and document repository.")


def show_mpcfs_coffee_table_book():
    """Coffee table book generator for MPCFS project documentation"""
    
    st.markdown("#### 📖 Coffee Table Book Generator")
    st.caption("Compile project experiences, beneficiary stories, and documentation into a professional coffee table book")
    
    st.markdown("""
    ### About the MPCFS Coffee Table Book
    
    This feature will document the journey of the Mountain Province Climate Field School Project, capturing:
    - **Beneficiary Stories**: Personal accounts from farmers and community members
    - **Project Milestones**: Key achievements and turning points
    - **Photo Gallery**: Visual documentation of project activities
    - **Lessons Learned**: Insights and best practices for replication
    - **Impact Stories**: How the project changed lives and livelihoods
    """)
    
    # Book sections
    sections = [
        "Foreword",
        "Introduction: The Climate Challenge in Mountain Province",
        "Chapter 1: The Birth of MPCFS",
        "Chapter 2: Building Climate-Resilient Farmers",
        "Chapter 3: Voices from the Field (Beneficiary Stories)",
        "Chapter 4: Demonstration Farms in Action",
        "Chapter 5: Research & Innovation",
        "Chapter 6: Partnerships & Collaborations",
        "Chapter 7: Lessons Learned",
        "Chapter 8: The Road Ahead",
        "Appendices: Data, Maps, and Technical Details"
    ]
    
    # Preview
    with st.expander("📖 Book Structure Preview", expanded=True):
        for i, section in enumerate(sections, 1):
            st.markdown(f"{i}. {section}")
    
    # Generate book
    col1, col2 = st.columns(2)
    with col1:
        book_title = st.text_input("Book Title", value="MPCFS: Cultivating Climate Resilience in Mountain Province")
        book_author = st.text_input("Author", value="Mountain Province PDRRMO")
        book_year = st.number_input("Year", min_value=2024, max_value=2030, value=2026)
    
    with col2:
        book_editor = st.text_input("Editor", value="Project Manager, MPCFS")
        book_publisher = st.text_input("Publisher", value="MPDRRMO Research & Planning Division")
        book_isbn = st.text_input("ISBN (Optional)", placeholder="To be assigned")
    
    if st.button("📖 Generate Coffee Table Book", type="primary"):
        st.markdown("---")
        st.markdown(f"### 📖 {book_title}")
        st.markdown(f"**Author:** {book_author} | **Editor:** {book_editor}")
        st.markdown(f"**Publisher:** {book_publisher} | **Year:** {book_year}")
        st.markdown("---")
        
        st.markdown("#### Foreword")
        st.markdown("""
        The Mountain Province Climate Field School Project (MPCFS) represents a bold step forward in our province's 
        journey toward climate resilience. This coffee table book documents the stories, experiences, and lessons 
        learned from the first-of-its-kind project in Mountain Province.
        """)
        
        st.markdown("#### Sample Page: Voices from the Field")
        st.markdown("""
        **"Before MPCFS, I relied on traditional farming methods that often failed during droughts. Now, I've learned 
        new techniques that help my crops survive even with less rainfall. This project changed my life."**
        
        *— Farmer, Bacarri, Paracelis*
        """)
        
        st.info("💡 **Note:** The complete coffee table book will be generated with all photos, stories, and data when ready.")
        
        # Export option
        if st.button("📥 Export to PDF"):
            st.success("PDF export will be available in the next phase.")


def show_cca_analytics():
    """Display CCA analytics and insights"""
    
    st.markdown("### CCA Analytics & Insights")
    st.caption("Data-driven insights on climate adaptation progress")
    
    # Placeholder for analytics
    st.info("Analytics dashboard coming soon. This will include:")
    st.markdown("""
    - Climate vulnerability trends
    - Adaptation project effectiveness
    - Financing gap analysis
    - Municipal CCA readiness scores
    """)
    
    # Sample chart
    st.markdown("#### Climate Vulnerability Index by Municipality")
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    vulnerability = [65, 55, 70, 45, 60, 75, 50, 68, 58, 62]
    
    fig = px.bar(x=municipalities, y=vulnerability, title="Climate Vulnerability Index", 
                 labels={"x": "Municipality", "y": "Vulnerability Score"})
    st.plotly_chart(fig, use_container_width=True)


def show_cca_documents():
    """Document repository for CCA-related files"""
    
    st.markdown("### CCA Document Repository")
    st.caption("Store and manage climate change adaptation-related documents")
    
    # Simple placeholder
    st.info("Document repository coming soon. This will store:")
    st.markdown("""
    - PCCAP and LCCAP documents
    - Climate risk assessments
    - Adaptation project proposals
    - Climate data and reports
    - International frameworks (Paris Agreement, Sendai Framework)
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
        
        ### 📊 DRRM Intelligence
        - Climate hazard data
        - Vulnerability assessments
        - Risk mapping integration
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Trainings
        - Climate literacy programs
        - Farmer capacity building
        - Extension worker training
        
        ### 💰 LDRRMF Utilization
        - Climate adaptation funding
        - MPCFS budget tracking
        - Project financial reports
        
        ### 🏛️ About INDC
        - Evolution of CCA integration
        - Governance framework
        - Vision for climate resilience
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
        if st.button("💰 Go to LDRRMF", use_container_width=True):
            st.session_state.navigation = "💰 LDRRMF UTILIZATION"
            st.rerun()