# tabs/quick_guide.py
import streamlit as st
from datetime import datetime

def show():
    """Display Quick Guide Tab - User Manual and Help Center"""
    
    st.markdown("# ❓ Quick Guide")
    st.caption("User Manual and Help Center for the INDC Platform")
    
    # Create tabs for different guide sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚀 Getting Started",
        "📚 Module Guides",
        "📋 Data Preparation",
        "❓ FAQs",
        "🎥 Video Tutorials",
        "📞 Support"
    ])
    
    with tab1:
        show_getting_started()
    
    with tab2:
        show_module_guides()
    
    with tab3:
        show_data_preparation()
    
    with tab4:
        show_faqs()
    
    with tab5:
        show_video_tutorials()
    
    with tab6:
        show_support()


def show_getting_started():
    """Getting Started guide for new users"""
    
    st.markdown("## 🚀 Getting Started")
    st.markdown("Welcome to the INDC Platform! This guide will help you get started.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Quick Start Steps
        
        1. **Login** (if applicable)
           - PDRRMO Staff: Full access to all modules
           - MDRRMO Staff: Limited to data entry
           - Admin: Full access + user management
        
        2. **Navigate the Sidebar**
           - Use the left sidebar to access different modules
           - Each module has specific functions
        
        3. **Start with Data Entry**
           - Begin with **DRRM Intelligence** for hazard events
           - Add **Trainings** records
           - Input **LDRRMF Utilization** data
        
        4. **Explore Other Modules**
           - **Plan Management** for DRRM plans
           - **Situation Report** for incident reporting
           - **Climate Change** for adaptation tracking
        
        5. **Use Related Modules**
           - Click "Related Modules" in each tab
           - Data flows between connected modules
        """)
    
    with col2:
        st.markdown("""
        ### 💡 Pro Tips
        
        **Auto-Sync Enabled**
        - All data automatically syncs to cloud
        - No manual backup needed
        - Real-time collaboration supported
        
        **Local Storage**
        - Files are stored locally on your computer
        - Location: `E:\\INDC_Project\\local_storage\\`
        - Regular backups recommended
        
        **Keyboard Shortcuts**
        - `Ctrl + S`: Save form (where applicable)
        - `Ctrl + F`: Search within tables
        - `Esc`: Close expanders
        
        **Data Quality**
        - Use consistent naming conventions
        - Fill all required fields (*)
        - Upload supporting documents when possible
        """)
    
    st.markdown("---")
    
    st.markdown("### 🏛️ System Overview")
    
    overview_data = {
        "Module": [
            "Command Center",
            "DRRM Intelligence",
            "Climate Change",
            "Plan Management",
            "Performance Management",
            "Trainings",
            "LDRRMF Utilization",
            "Situation Report",
            "NDC Personal",
            "Knowledge Repository",
            "Geospatial Library",
            "Risk Profiles"
        ],
        "Purpose": [
            "Real-time dashboard and metrics",
            "Hazard events and predictive analytics",
            "CCA plans and MPCFS project tracking",
            "DRRM plans, PPAs, and indicators",
            "IPCR/OPCR tracking and roll-up",
            "Training records and certifications",
            "Fund utilization tracking",
            "Multi-user incident reporting",
            "Personal project and task management",
            "Digital library for policies and literatures",
            "GIS map repository",
            "CDRA and risk assessments"
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(overview_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.info("💡 Tip: Click on any module in the sidebar to access its features.")


def show_module_guides():
    """Detailed guides for each module"""
    
    st.markdown("## 📚 Module Guides")
    st.markdown("Detailed instructions for each INDC module")
    
    # Accordion-style guides for each module
    modules = [
        {"name": "🎯 COMMAND CENTER", "description": "Real-time dashboard showing key metrics and recent activities.", "features": ["View active incidents and response metrics", "See recent activities from all modules", "Monitor training summaries", "Track LDRRMF fund utilization"], "tips": "Use this as your home base to get a quick overview of all DRRM activities."},
        {"name": "📊 DRRM INTELLIGENCE", "description": "Hazard events database with trend analysis and predictive forecasting.", "features": ["Add new disaster events with file attachments", "View and filter event database", "Analyze trends with interactive charts", "Upload typhoon tracks and hazard photos", "View predictive analytics and risk scores"], "tips": "Always attach photos and documents to events for better documentation."},
        {"name": "🌍 CLIMATE CHANGE", "description": "Climate change adaptation plans and MPCFS flagship project tracking.", "features": ["Track CCA plans and programs", "Manage MPCFS project with Gantt charts", "Upload project documents and photos", "Generate consolidated reports", "Create coffee table book documentation"], "tips": "The MPCFS hub is where you track the P271M climate field school project."},
        {"name": "📋 PLAN MANAGEMENT", "description": "Comprehensive planning and implementation tracking.", "features": ["Manage provincial and municipal DRRM plans", "Track PPAs (Programs, Projects, Activities)", "Monitor M&E indicators", "Implementation tracker with quarterly updates", "Auto-sync to Supabase cloud"], "tips": "Link PPAs to IPCR/OPCR for performance alignment."},
        {"name": "📊 PERFORMANCE MANAGEMENT", "description": "IPCR and OPCR tracking with employee performance monitoring.", "features": ["Employee directory management", "IPCR submission and approval workflow", "OPCR tracking with roll-up from IPCRs", "Admin dashboard for all employees", "File upload for signed IPCR/OPCR"], "tips": "IPCR data automatically rolls up to division-level OPCR."},
        {"name": "📚 TRAININGS", "description": "Track staff training, certifications, and capacity building.", "features": ["Add training records with participant counts", "View training database with filters", "Summary statistics by municipality", "Upload certificates and materials"], "tips": "Connect trainings to Plan Management for capacity gap analysis."},
        {"name": "💰 LDRRMF UTILIZATION", "description": "Track Local Disaster Risk Reduction and Management Fund utilization.", "features": ["Add fund utilization records", "Analytics charts by municipality/status/year", "Monthly reporting format", "Financial tracking and reporting"], "tips": "Regular updates help with budget planning and reporting."},
        {"name": "📡 SITUATION REPORT", "description": "Multi-user incident reporting with PAGASA weather integration.", "features": ["MDRRMO data entry for municipal reports", "PDRRMO consolidation view", "PAGASA weather API integration", "Photo documentation", "Predictive analysis from historical reports"], "tips": "Up to 10 staff can input simultaneously for real-time reporting."},
        {"name": "👤 NDC PERSONAL", "description": "Personal project and task management dashboard.", "features": ["Project tracker with all your tasks", "Dashboard with charts and metrics"], "tips": "Use this to track your personal projects and IPCR targets."},
        {"name": "📁 KNOWLEDGE REPOSITORY", "description": "Digital library for policies, literatures, and media files.", "features": ["Upload and organize documents by category", "Search and filter library", "Open, download, and delete files", "Manage categories and sources"], "tips": "Files are stored locally in local_storage/knowledge_repository/"},
        {"name": "🗺️ GEOSPATIAL LIBRARY", "description": "Repository for GIS-generated maps.", "features": ["Upload base, hazard, risk, exposure, and vulnerability maps", "Grid view with thumbnails", "Filter by category, year, municipality", "Open, download, and delete maps"], "tips": "Maps from the 3D PRISM initiative are stored here."},
        {"name": "📊 RISK PROFILES", "description": "CDRA documents and risk assessments.", "features": ["CDRA documents for province and municipalities", "Landslide susceptibility assessments", "Municipal and barangay risk profiles", "Provincial risk maps for various elements at risk", "CDRA summary reports"], "tips": "Supports 144 barangay-level risk profiles."},
        {"name": "🏛️ ABOUT INDC", "description": "Evolution timeline and platform information.", "features": ["Interactive evolution timeline (3D PRISM to ADST to INDC)", "Phase details and narrative", "EMDRCM/AIM development context", "Scalability vision"], "tips": "Use this for presentations to stakeholders and funding agencies."}
    ]
    
    for module in modules:
        with st.expander(f"{module['name']}"):
            st.markdown(f"**Description:** {module['description']}")
            st.markdown("**Key Features:**")
            for feature in module['features']:
                st.markdown(f"- {feature}")
            st.markdown(f"**Tip:** {module['tips']}")


def show_data_preparation():
    """Data preparation guide for staff"""
    
    st.markdown("## 📋 Data Preparation Guide")
    st.markdown("What data to prepare for each module")
    
    st.info("Important: Staff are encouraged to start gathering and preparing these data while the system is being developed.")
    
    data_requirements = [
        {"module": "DRRM Intelligence", "priority": "High", "formats": "PDF, JPG, PNG, XLSX, CSV"},
        {"module": "Plan Management", "priority": "High", "formats": "PDF, DOCX, XLSX"},
        {"module": "Climate Change", "priority": "High", "formats": "PDF, DOCX, XLSX, JPG, PNG"},
        {"module": "Trainings", "priority": "Medium", "formats": "PDF, DOCX, XLSX"},
        {"module": "LDRRMF Utilization", "priority": "High", "formats": "PDF, XLSX"},
        {"module": "Situation Report", "priority": "High", "formats": "PDF, DOCX, JPG, PNG"},
        {"module": "Performance Management", "priority": "Medium", "formats": "PDF, XLSX"},
        {"module": "Risk Profiles", "priority": "High", "formats": "PDF, DOCX, JPG, PNG"},
        {"module": "Geospatial Library", "priority": "Medium", "formats": "PDF, JPG, PNG"},
        {"module": "Knowledge Repository", "priority": "Medium", "formats": "PDF, DOCX, JPG, PNG, MP4"}
    ]
    
    import pandas as pd
    df = pd.DataFrame(data_requirements)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### File Organization Tips")
    
    st.markdown("""
    **Recommended Folder Structure:**
    
    - local_storage/drrm_intelligence/     # Hazard events, photos, tracks
    - local_storage/plan_management/       # Plans, PPAs, indicators
    - local_storage/climate_change/        # CCA plans, MPCFS documents
    - local_storage/trainings/             # Certificates, materials
    - local_storage/ldrrmf/                # Financial reports
    - local_storage/sitrep/                # Situation report photos
    - local_storage/performance_management/ # IPCR/OPCR files
    - local_storage/knowledge_repository/  # Policies, literatures
    - local_storage/geospatial_library/    # GIS maps
    - local_storage/risk_profiles/         # CDRA, assessments
    """)
    
    st.info("Naming Convention: YYYY-MM-DD_DocumentName_Type. Use underscores instead of spaces.")


def show_faqs():
    """Frequently Asked Questions"""
    
    st.markdown("## ❓ Frequently Asked Questions")
    
    faqs = [
        ("How do I add a new disaster event?", "Go to DRRM Intelligence > Event Entry tab. Fill out the form with event details, upload photos or documents, then click 'Save Event'."),
        ("Where are uploaded files stored?", "Files are stored locally on your computer in E:\\INDC_Project\\local_storage\\. They are NOT stored in the cloud."),
        ("How does auto-sync work?", "All text data automatically syncs to Supabase cloud. Files remain local. Multi-user collaboration is supported."),
        ("Can multiple users work simultaneously?", "Yes. The Situation Report tab supports up to 10 MDRRMO staff inputting data simultaneously."),
        ("How do I backup my data?", "Copy the local_storage/ folder to an external drive. Database is automatically backed up to Supabase cloud."),
        ("What file formats are supported?", "PDF, DOCX, XLSX, PPTX, JPG, PNG, GIF, MP4, TXT.")
    ]
    
    for q, a in faqs:
        with st.expander(f"❓ {q}"):
            st.markdown(a)


def show_video_tutorials():
    """Video tutorials and training materials"""
    
    st.markdown("## 🎥 Video Tutorials")
    st.markdown("Coming soon - Step-by-step video guides for each module")
    
    st.info("Video tutorials are currently being produced. Check back soon for:")
    
    tutorials = [
        "INDC Platform Overview (5 min)",
        "DRRM Intelligence: Adding Disaster Events (3 min)",
        "Plan Management: Creating Provincial Plans (4 min)",
        "Situation Report: Multi-user Data Entry (6 min)",
        "Climate Change: MPCFS Project Tracking (5 min)",
        "Performance Management: IPCR Submission (4 min)"
    ]
    
    for tutorial in tutorials:
        st.markdown(f"- {tutorial}")


def show_support():
    """Support and contact information"""
    
    st.markdown("## 📞 Support")
    st.markdown("Get help and provide feedback")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Contact Information
        
        **Mountain Province PDRRMO**
        
        **Office Address:** Appong Street, Jungle Town, Poblacion, Bontoc, Mountain Province 2616, Cordillera Administrative Region, Philippines
        
        **Phone:** (+63) 908-816-4098
        
        **General Email:** mppdrrmo@gmail.com
        **Technical Email:** cneil_japan@yahoo.com.ph
                    
        **Office Hours:** Tuesday - Friday: 9:00 AM - 5:00 PM
        """)
        
        st.markdown("### Report an Issue")
        
        with st.form("bug_report"):
            issue_title = st.text_input("Issue Title")
            issue_description = st.text_area("Describe the issue", height=100)
            submitted = st.form_submit_button("Submit Report")
            
            if submitted and issue_title:
                st.success("Issue reported! Our team will contact you within 24 hours.")
    
    with col2:
        st.markdown("""
        ### Feedback & Suggestions
        
        We value your input!
        """)
        
        with st.form("feedback_form"):
            feedback_message = st.text_area("Your Message", height=150)
            submitted = st.form_submit_button("Submit Feedback")
            
            if submitted and feedback_message:
                st.success("Thank you for your feedback!")
        
        st.markdown("---")
        st.markdown("### System Information")
        
        import platform
        import sys
        
        st.markdown(f"- **App Version:** 2.0.0")
        st.markdown(f"- **Python Version:** {sys.version.split()[0]}")
        st.markdown(f"- **OS:** {platform.system()} {platform.release()}")