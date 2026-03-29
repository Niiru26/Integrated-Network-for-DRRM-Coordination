# tabs/ndc_personal.py
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from utils.local_storage import save_file, delete_file, get_file_size, file_exists

def show():
    """Display NDC Personal Tab - Personal Project and Task Management"""
    
    st.markdown("# 👤 NDC Personal")
    st.caption("Your personal project and task management hub - Based on your Project Dashboard")
    
    # Initialize session state
    if 'ndc_projects' not in st.session_state:
        load_all_projects()
    
    if 'ndc_categories' not in st.session_state:
        st.session_state.ndc_categories = [
            "DRRM Innovation", "Planning & Policy", "Climate Field School", 
            "Institutional Development", "Academic", "Emergency Preparedness & Response",
            "Monitoring & Evaluation", "Performance Management", "Risk Communication",
            "CALDRRMO", "Research"
        ]
    
    if 'ndc_statuses' not in st.session_state:
        st.session_state.ndc_statuses = ["In Progress", "Completed", "Not Started", "On Hold", "Delayed"]
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Project Tracker",
        "📊 My Dashboard",
        "📅 My Day",
        "📁 File Repository",
        "📥 Import/Export",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_project_tracker()
    
    with tab2:
        show_my_dashboard()
    
    with tab3:
        show_my_day()
    
    with tab4:
        show_file_repository()
    
    with tab5:
        show_import_export()
    
    with tab6:
        show_related_modules()


def load_all_projects():
    """Load all projects from your Excel data"""
    
    projects = [
        # Major Projects
        {"id": 1, "project_name": "Strategic Mapping for the Streamlining and Harmonization of DRRM-CCA PPAs Across Local Planning, Budgeting, and Performance Frameworks (PCDRRMP, AIP, OPCR, IPCR), with Integration into CCET and SDGs", 
         "lead_team": "Neil", "key_outputs": "Strategic mapping matrix linking PPAs, traceability framework, consolidated PPA list", 
         "expected_outcomes": "Improved integration between planning, budgeting, and performance frameworks", 
         "category": "DRRM Innovation", "priority": "Medium", "start_date": "2025-05-29", "end_date": "2025-07-26", 
         "status": "In Progress", "linked_files": "E:\\_____2025-03-22_Enhanced MPPCDRM PLAN_2024-2028\\1--2025-05-28_Strategic PDRRMC PPA Mapping + Traceability Framework.xlsx", 
         "tags": "#StrategicMapping #PlanningAlignment #CCET #SDGAlignment", 
         "remarks": "Needs fine-tuning + Updating to incorporate the PPAs in the submitted IPCRs"},
        
        {"id": 2, "project_name": "Strategic Mapping and Thematic Classification Manual for Local DRRM and CCA Programs, Projects, and Activities in Mountain Province: Aligning Local Initiatives with the NDRRMP 2020–2030", 
         "lead_team": "Neil", "key_outputs": "Harmonized PPA list, traceability framework, classification manual", 
         "expected_outcomes": "Reduced duplication, improved resource allocation, stronger compliance with national frameworks", 
         "category": "Planning & Policy", "priority": "Medium", "start_date": "2025-03-22", "end_date": "2025-04-01", 
         "status": "Completed", "linked_files": "E:\\_____2025-03-22_Enhanced MPPCDRM PLAN_2024-2028\\3--2025-03-31_Strategic Mapping of PDRRMC PPAs_Manual for LDRRMCs.docx", 
         "tags": "#StrategicMapping #PlanningAlignment", 
         "remarks": "Turned-over to Laycha"},
        
        {"id": 3, "project_name": "Development and implementation of a PowerBI-powered Monitoring & Evaluation Tool for the MPDRRMC", 
         "lead_team": "Laycha, Clariss, Cyprine, Neil", "key_outputs": "PowerBI-based M&E dashboard, integrated reporting templates, real-time visualizations", 
         "expected_outcomes": "Streamlined monitoring of MPDRRMC PPAs, enhanced decision-making capacity", 
         "category": "Monitoring & Evaluation", "priority": "High", "start_date": "2025-06-15", "end_date": "", 
         "status": "In Progress", "linked_files": "", 
         "tags": "#DataManagement #M&E #InstitutionalDevelopment #PerformanceManagement", 
         "remarks": "Includes dashboard of MPDRRMC accomplishments in terms of number of approved Resolutions"},
        
        {"id": 4, "project_name": "Development and implementation of a PowerBI-powered Monitoring & Evaluation Tool for the MPCFS", 
         "lead_team": "", "key_outputs": "PowerBI-based M&E tool, integrated database, interactive dashboards, user manual", 
         "expected_outcomes": "Enhanced capacity to track MPCFS performance, data-driven decision-making", 
         "category": "Climate Field School", "priority": "", "start_date": "", "end_date": "", 
         "status": "In Progress", "linked_files": "", 
         "tags": "#PowerBI #MPCFS #MonitoringAndEvaluation #ClimateFieldSchool", 
         "remarks": ""},
        
        {"id": 5, "project_name": "Development and implementation of a PowerBI-powered SitRep for Operation Centers", 
         "lead_team": "", "key_outputs": "PowerBI-based SitRep template, real-time data integration, automated dashboards", 
         "expected_outcomes": "Faster situational reporting, improved decision-making during emergencies", 
         "category": "Emergency Preparedness & Response", "priority": "", "start_date": "", "end_date": "", 
         "status": "In Progress", "linked_files": "Sitrep PowerBI.PNG", 
         "tags": "#PowerBI #SitRep #OperationsCenter #EmergencyPreparedness", 
         "remarks": ""},
        
        {"id": 6, "project_name": "Drafting of the Constitution and By-Laws of the CALDRRMO", 
         "lead_team": "Neil", "key_outputs": "Draft Constitution and By-Laws, consultative workshops, final endorsed document", 
         "expected_outcomes": "Formal governance structure for CALDRRMO, improved coordination of DRRM officers in CAR", 
         "category": "CALDRRMO", "priority": "High", "start_date": "2025-07-10", "end_date": "2025-08-05", 
         "status": "Completed", "linked_files": "", 
         "tags": "#Governance #PolicyPlanning #InstitutionalStrengthening #Collaboration", 
         "remarks": "Approved in principle, submit to SEC for registration"},
        
        {"id": 7, "project_name": "Review and enhance the IPCR for the 4 Divisions", 
         "lead_team": "Laycha, Clariss, Cyprine, Neil", "key_outputs": "Updated IPCR templates, enhanced success indicators", 
         "expected_outcomes": "Clearer, measurable, results-oriented IPCRs aligned with OPCR and AIP", 
         "category": "Performance Management", "priority": "High", "start_date": "2025-07-15", "end_date": "2025-08-04", 
         "due_date": "2025-07-10", "status": "Completed", "linked_files": "", 
         "tags": "#PerformanceManagement #InstitutionalDevelopment #Accountability", 
         "remarks": "For review 1st semester 2026"},
        
        {"id": 8, "project_name": "Develop a Risk Profile for each barangay based on CDRA and rain-induced landslide assessments", 
         "lead_team": "Neil", "key_outputs": "Risk Profile per Municipality, GIS-Based Map per Barangay, hazard maps", 
         "expected_outcomes": "Evidence-based barangay-level risk profiles, improved local DRRM planning", 
         "category": "DRRM Innovation", "priority": "High", "start_date": "2025-05-15", "end_date": "", 
         "status": "In Progress", "linked_files": "", 
         "tags": "#PlanningAndPolicy #RiskCommunication #EmergencyPreparednessAndResponse", 
         "remarks": "Integrate into PCDRRMP"},
        
        {"id": 9, "project_name": "Draft an Executive Order to reorganize the MPDRRMC", 
         "lead_team": "Neil", "key_outputs": "Executive Order document, reorganized membership list, thematic committees", 
         "expected_outcomes": "Updated functional MPDRRMC structure aligned with NDRRMP", 
         "category": "Planning & Policy", "priority": "High", "start_date": "2025-07-10", "end_date": "2025-08-05", 
         "due_date": "2025-08-11", "status": "Completed", "linked_files": "Executive Order No. 25, s. 2025\\Executive Order No. 02-2025_Reorganizing the PDRRM Council_Updated 2025.docx", 
         "tags": "#ExecutiveOrder #MPDRRMC #OrganizationalStructure", 
         "remarks": "EO No. 25, s. 2025"},
        
        {"id": 10, "project_name": "INDC (formerly ADST) & Dashboard Design Prototype", 
         "lead_team": "Neil", "key_outputs": "Prototype of ADST Dashboard", 
         "expected_outcomes": "Functional dashboard for DRRM coordination", 
         "category": "DRRM Innovation", "priority": "High", "start_date": "", "end_date": "", 
         "status": "In Progress", "linked_files": "E:\\ADST & DASHBOARD DESIGN & PROTOTYPE\\2025-06-23_Artificial Intelligence Questions.docx", 
         "tags": "", 
         "remarks": "Impact based forecasting for RIL"},
        
        {"id": 11, "project_name": "Finalization of the Work & Financial Plan for the Capability Building and Research & Extension components of the MPCFS", 
         "lead_team": "", "key_outputs": "Approved Work & Financial Plan", 
         "expected_outcomes": "Clear implementation framework", 
         "category": "Climate Field School", "priority": "High", "start_date": "2025-08-15", "end_date": "", 
         "due_date": "2025-08-31", "status": "In Progress", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 12, "project_name": "Super Typhoon 'Uwan' (Fung-Wong) in Mountain Province: Report on Impacts", 
         "lead_team": "", "key_outputs": "Terminal Report", 
         "expected_outcomes": "Documented impacts and lessons learned", 
         "category": "Reporting", "priority": "", "start_date": "2025-12-01", "end_date": "2026-01-09", 
         "status": "In Progress", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 13, "project_name": "Joint DRRM-SWAD-PSWD Field Assessment of Recurrently Evacuated Households", 
         "lead_team": "", "key_outputs": "", 
         "expected_outcomes": "", 
         "category": "Assessment", "priority": "", "start_date": "", "end_date": "", 
         "status": "Call for a meeting", "linked_files": "C:\\Users\\NDC\\Desktop\\Concept Note_Joint PDRRMO-SWAD-PSWD Field Assessment.docx", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 14, "project_name": "Research: Food Pack for Disaster Relief - MRE", 
         "lead_team": "", "key_outputs": "", 
         "expected_outcomes": "", 
         "category": "DRRM Innovation", "priority": "High - for 2026", "start_date": "2025-12-10", "end_date": "", 
         "status": "In Progress", "linked_files": "", 
         "tags": "", 
         "remarks": "Include in research agenda under MPCFS"},
        
        {"id": 15, "project_name": "Grant Assistance for Grass-Roots Human Security Projects (GGP)", 
         "lead_team": "", "key_outputs": "Grant Proposal", 
         "expected_outcomes": "Approved grant funding", 
         "category": "Coordination", "priority": "", "start_date": "", "end_date": "", 
         "status": "Planning", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 16, "project_name": "Ordinance Providing for An Incentive-Based Mechanism to Prevent or Mitigate Forest Fires", 
         "lead_team": "", "key_outputs": "Draft Ordinance", 
         "expected_outcomes": "Approved ordinance", 
         "category": "Policy", "priority": "", "start_date": "", "end_date": "", 
         "status": "Planning", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 17, "project_name": "Updating of Local Climate Change Action Plan (LCCAP)", 
         "lead_team": "", "key_outputs": "Updated LCCAP document", 
         "expected_outcomes": "Current and responsive climate action plan", 
         "category": "Planning & Policy", "priority": "", "start_date": "", "end_date": "", 
         "status": "In Progress", "linked_files": "..\\00000_2024-08-18_ACTIVE FILES\\2023-06-19_Updating of LCCAP\\2024-09-25_Local Climate Change Action Plan 2023-2032_Ver. 2023 - 02.docx", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 18, "project_name": "Development of Integrated Knowledge Gain and Training Quality Assessment Tool", 
         "lead_team": "Laycha, Clariss, Cyprine, Neil", "key_outputs": "Pre-Test/Post-Test forms, Quality Assessment Form, Dashboard Module", 
         "expected_outcomes": "Standardized evaluation of training effectiveness", 
         "category": "Monitoring & Evaluation", "priority": "Low", "start_date": "2025-06-27", "end_date": "", 
         "status": "In Progress", "linked_files": "", 
         "tags": "#CapacityBuilding #M&E #InstitutionalDevelopment", 
         "remarks": ""},
        
        {"id": 19, "project_name": "Drafting of the Constitution and By-Laws of MPALDRRMO", 
         "lead_team": "Neil & Mark", "key_outputs": "Draft CBL, consultation report, final endorsed document", 
         "expected_outcomes": "Legal framework for MPALDRRMO", 
         "category": "CALDRRMO", "priority": "", "start_date": "2025-07-09", "end_date": "", 
         "due_date": "2025-08-15", "status": "In Progress", "linked_files": "", 
         "tags": "#Governance #PolicyPlanning #InstitutionalStrengthening", 
         "remarks": ""},
        
        {"id": 20, "project_name": "Update your IPCR", 
         "lead_team": "Neil", "key_outputs": "Updated IPCR", 
         "expected_outcomes": "Current performance record", 
         "category": "Performance Management", "priority": "Medium", "start_date": "", "end_date": "", 
         "due_date": "2025-12-27", "status": "Not Started", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 21, "project_name": "Draft Compensatory Time-Off Guidelines", 
         "lead_team": "", "key_outputs": "PDRRMO Guideline", 
         "expected_outcomes": "Standardized CTO policy", 
         "category": "Institutional Development", "priority": "Very Low", "start_date": "", "end_date": "", 
         "status": "Draft", "linked_files": "..\\00000_2024-08-18_ACTIVE FILES\\Compensatory Time-Off Guidelines\\Compensatory Time-Off Guidelines.docx", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 22, "project_name": "Updating of Contingency Plans", 
         "lead_team": "", "key_outputs": "Updated Contingency Plans", 
         "expected_outcomes": "Current response plans", 
         "category": "Emergency Preparedness & Response", "priority": "", "start_date": "", "end_date": "", 
         "status": "Planning", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 23, "project_name": "Updating of Multi-Hazard Early Warning System", 
         "lead_team": "", "key_outputs": "Enhanced EWS", 
         "expected_outcomes": "Improved early warning", 
         "category": "Emergency Preparedness & Response", "priority": "", "start_date": "", "end_date": "", 
         "status": "Planning", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 24, "project_name": "Compendium of DRRM Governance", 
         "lead_team": "", "key_outputs": "Compendium document", 
         "expected_outcomes": "Documented DRRM governance practices", 
         "category": "Research", "priority": "", "start_date": "", "end_date": "", 
         "status": "In Progress", "linked_files": "000_2024-10-06_Compendium of DRRM Governance.docx", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 25, "project_name": "First CALDRRMO meeting in Bontoc", 
         "lead_team": "", "key_outputs": "Successful meeting", 
         "expected_outcomes": "Improved regional coordination", 
         "category": "CALDRRMO", "priority": "High", "start_date": "", "end_date": "", 
         "status": "Planning", "linked_files": "2025-08-12_Message of Support_Rescuelympics 2025.docx", 
         "tags": "", 
         "remarks": "3rd or 4th Quarter"},
        
        {"id": 26, "project_name": "Baseline Survey on Agricultural Practices, Climate Change Awareness, and DRRM Strategies", 
         "lead_team": "", "key_outputs": "Survey Report", 
         "expected_outcomes": "Baseline data for MPCFS", 
         "category": "Research", "priority": "", "start_date": "", "end_date": "", 
         "status": "In Progress", "linked_files": "", 
         "tags": "", 
         "remarks": "Check with Cy on the consolidation"},
        
        {"id": 27, "project_name": "ADST Project Proposal for NDRRMF Funding", 
         "lead_team": "Neil", "key_outputs": "Project Proposal", 
         "expected_outcomes": "Funding for ADST", 
         "category": "DRRM Innovation", "priority": "High", "start_date": "", "end_date": "", 
         "status": "Planning", "linked_files": "", 
         "tags": "", 
         "remarks": ""},
        
        {"id": 28, "project_name": "Brief ADST Proposal for Ayala Foundation, Inc.", 
         "lead_team": "Neil", "key_outputs": "Project Proposal", 
         "expected_outcomes": "Partnership with Ayala Foundation", 
         "category": "DRRM Innovation", "priority": "", "start_date": "2025-05-25", "end_date": "2025-05-27", 
         "status": "Submitted", "linked_files": "E:\\2025-05-16_Ayala_ADST Project Proposal\\2025-05-27_Ayala_ADST Proj Proposal.docx", 
         "tags": "", 
         "remarks": "Submitted to PNVSCA on May 26, 2025"},
        
        {"id": 29, "project_name": "Proposal Submission: Localized Decision-Support Tool for Disaster Risk Governance", 
         "lead_team": "Neil", "key_outputs": "Project Proposal", 
         "expected_outcomes": "UNDP partnership", 
         "category": "DRRM Innovation", "priority": "", "start_date": "2025-04-02", "end_date": "2025-03-04", 
         "status": "Submitted", "linked_files": "", 
         "tags": "", 
         "remarks": "Submitted to UNDP Philippines Accelerator Lab"},
        
        {"id": 30, "project_name": "Sasakawa Nomination", 
         "lead_team": "Neil", "key_outputs": "Nomination submitted", 
         "expected_outcomes": "Recognition", 
         "category": "Academic", "priority": "", "start_date": "2025-03-11", "end_date": "2025-03-22", 
         "due_date": "2029-03-29", "status": "Submitted", "linked_files": "E:\\Sasakawa Award\\2025-sasakawa-awards-form.pdf", 
         "tags": "", 
         "remarks": "Submitted: March 21, 2025"},
    ]
    
    st.session_state.ndc_projects = projects


def show_project_tracker():
    """Display the project tracker with all columns from your Excel"""
    
    st.markdown("### 📋 Project & Task Tracker")
    st.caption("Complete list of all projects, tasks, and activities")
    
    projects = st.session_state.ndc_projects
    
    # Filter controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        categories = ["All"] + sorted(list(set([p.get('category', '') for p in projects if p.get('category')])))
        filter_category = st.selectbox("Filter by Category", categories, key="filter_category")
    with col2:
        statuses = ["All"] + st.session_state.ndc_statuses
        filter_status = st.selectbox("Filter by Status", statuses, key="filter_status")
    with col3:
        priorities = ["All", "High", "Medium", "Low", "Very Low"]
        filter_priority = st.selectbox("Filter by Priority", priorities, key="filter_priority")
    with col4:
        search_term = st.text_input("Search", placeholder="Search projects...", key="search_projects")
    
    # Filter data
    filtered_projects = projects.copy()
    
    if filter_category != "All":
        filtered_projects = [p for p in filtered_projects if p.get('category') == filter_category]
    if filter_status != "All":
        filtered_projects = [p for p in filtered_projects if p.get('status') == filter_status]
    if filter_priority != "All":
        filtered_projects = [p for p in filtered_projects if p.get('priority') == filter_priority]
    if search_term:
        filtered_projects = [p for p in filtered_projects if 
                            search_term.lower() in p.get('project_name', '').lower() or
                            search_term.lower() in p.get('tags', '').lower()]
    
    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Projects", len(filtered_projects))
    with col2:
        completed = len([p for p in filtered_projects if p.get('status') == 'Completed'])
        st.metric("Completed", completed)
    with col3:
        ongoing = len([p for p in filtered_projects if p.get('status') == 'In Progress'])
        st.metric("In Progress", ongoing)
    with col4:
        high_priority = len([p for p in filtered_projects if p.get('priority') == 'High'])
        st.metric("High Priority", high_priority)
    with col5:
        planning = len([p for p in filtered_projects if p.get('status') == 'Planning'])
        st.metric("Planning", planning)
    
    st.markdown("---")
    
    # Add new project form
    with st.expander("➕ Add New Project/Task", expanded=False):
        with st.form("add_project_form"):
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input("Project/Task Name *", key="new_project_name")
                category = st.selectbox("Category", st.session_state.ndc_categories, key="new_category")
                priority = st.selectbox("Priority", ["High", "Medium", "Low", "Very Low"], key="new_priority")
                start_date = st.date_input("Start Date", date.today(), key="new_start_date")
                status = st.selectbox("Status", st.session_state.ndc_statuses, key="new_status")
            with col2:
                lead_team = st.text_input("Lead Team", key="new_lead_team")
                key_outputs = st.text_area("Key Outputs", key="new_key_outputs")
                expected_outcomes = st.text_area("Expected Outcomes", key="new_expected_outcomes")
                due_date = st.date_input("Due Date", date.today() + timedelta(days=30), key="new_due_date")
                tags = st.text_input("Tags", placeholder="#Tag1 #Tag2", key="new_tags")
            
            remarks = st.text_area("Notes/Remarks", key="new_remarks")
            
            submitted = st.form_submit_button("💾 Save Project")
            
            if submitted and project_name:
                new_project = {
                    "id": max([p.get('id', 0) for p in projects]) + 1 if projects else 1,
                    "project_name": project_name,
                    "lead_team": lead_team,
                    "key_outputs": key_outputs,
                    "expected_outcomes": expected_outcomes,
                    "category": category,
                    "priority": priority,
                    "start_date": start_date.isoformat() if start_date else "",
                    "end_date": "",
                    "due_date": due_date.isoformat() if due_date else "",
                    "status": status,
                    "linked_files": "",
                    "tags": tags,
                    "remarks": remarks,
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.ndc_projects.append(new_project)
                st.success(f"✅ Project '{project_name}' added!")
                st.rerun()
    
    # Display projects in a table
    if filtered_projects:
        df = pd.DataFrame(filtered_projects)
        
        # Select columns to display
        display_cols = ['project_name', 'category', 'priority', 'status', 'due_date', 'lead_team']
        available_cols = [col for col in display_cols if col in df.columns]
        
        st.dataframe(df[available_cols], use_container_width=True, hide_index=True)
        
        # Detailed view with edit/delete
        st.markdown("---")
        st.markdown("### ✏️ Project Details")
        
        for project in filtered_projects:
            with st.expander(f"📋 {project.get('project_name', 'Untitled')[:80]}..."):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Category:** {project.get('category', 'N/A')}")
                    st.markdown(f"**Priority:** {project.get('priority', 'N/A')}")
                    st.markdown(f"**Status:** {project.get('status', 'N/A')}")
                    st.markdown(f"**Lead Team:** {project.get('lead_team', 'N/A')}")
                    st.markdown(f"**Start Date:** {project.get('start_date', 'N/A')}")
                    st.markdown(f"**Due Date:** {project.get('due_date', 'N/A')}")
                with col2:
                    st.markdown(f"**Key Outputs:** {project.get('key_outputs', 'N/A')}")
                    st.markdown(f"**Expected Outcomes:** {project.get('expected_outcomes', 'N/A')[:200]}...")
                    st.markdown(f"**Tags:** {project.get('tags', 'N/A')}")
                
                st.markdown(f"**Remarks:** {project.get('remarks', 'No remarks')}")
                
                # Status update
                new_status = st.selectbox("Update Status", st.session_state.ndc_statuses, 
                                         index=st.session_state.ndc_statuses.index(project.get('status', 'In Progress')) if project.get('status') in st.session_state.ndc_statuses else 0,
                                         key=f"status_{project.get('id')}")
                if new_status != project.get('status'):
                    project['status'] = new_status
                    st.rerun()
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit", key=f"edit_{project.get('id')}"):
                        st.info("Edit feature will be available in the next update")
                with col2:
                    if st.button(f"🗑️ Delete", key=f"del_{project.get('id')}"):
                        st.session_state.ndc_projects = [p for p in st.session_state.ndc_projects if p.get('id') != project.get('id')]
                        st.success(f"Deleted: {project.get('project_name')}")
                        st.rerun()
    else:
        st.info("No projects found. Click 'Add New Project' to get started.")


def show_my_dashboard():
    """Personal dashboard with charts and metrics"""
    
    st.markdown("### 📊 My Dashboard")
    st.caption("Visual overview of all your projects and tasks")
    
    projects = st.session_state.ndc_projects
    
    if not projects:
        st.info("No projects to display.")
        return
    
    df = pd.DataFrame(projects)
    
    # Status distribution
    col1, col2 = st.columns(2)
    
    with col1:
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig = px.pie(status_counts, values='Count', names='Status', title='Projects by Status')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        category_counts = df['category'].value_counts().head(10).reset_index()
        category_counts.columns = ['Category', 'Count']
        fig = px.bar(category_counts, x='Category', y='Count', title='Projects by Category (Top 10)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Priority distribution
    col1, col2 = st.columns(2)
    
    with col1:
        priority_counts = df['priority'].value_counts().reset_index()
        priority_counts.columns = ['Priority', 'Count']
        fig = px.bar(priority_counts, x='Priority', y='Count', title='Projects by Priority', color='Priority')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Lead team distribution
        lead_counts = df[df['lead_team'] != '']['lead_team'].value_counts().head(10).reset_index()
        if not lead_counts.empty:
            lead_counts.columns = ['Lead Team', 'Count']
            fig = px.bar(lead_counts, x='Lead Team', y='Count', title='Projects by Lead Team')
            st.plotly_chart(fig, use_container_width=True)
    
    # Timeline chart
    st.markdown("#### 📅 Upcoming Deadlines")
    df_valid = df[(df['due_date'] != '') & (df['due_date'].notna()) & (df['status'] != 'Completed')]
    if not df_valid.empty:
        df_valid['due_date_dt'] = pd.to_datetime(df_valid['due_date'])
        df_valid = df_valid.sort_values('due_date_dt')
        df_valid['days_until'] = (df_valid['due_date_dt'] - pd.Timestamp.now()).dt.days
        
        fig = go.Figure()
        colors = ['red' if x < 0 else 'orange' if x < 14 else 'green' for x in df_valid['days_until'].head(15)]
        fig.add_trace(go.Bar(
            x=df_valid['project_name'].head(15),
            y=df_valid['days_until'].head(15),
            marker_color=colors,
            name='Days to Due Date'
        ))
        fig.update_layout(title="Upcoming Deadlines (Top 15)", xaxis_title="Project", yaxis_title="Days Until Due")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No upcoming deadlines")


def show_my_day():
    """Show tasks due today and this week"""
    
    st.markdown("### 📅 My Day")
    st.caption("Tasks and projects that need your attention today")
    
    projects = st.session_state.ndc_projects
    today = date.today()
    week_end = today + timedelta(days=7)
    
    # Filter tasks
    due_today = []
    due_this_week = []
    overdue = []
    high_priority = []
    
    for project in projects:
        due_date_str = project.get('due_date', '')
        status = project.get('status', '')
        priority = project.get('priority', '')
        
        if status == 'Completed':
            continue
        
        if due_date_str and due_date_str != '':
            try:
                due_dt = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                if due_dt == today:
                    due_today.append(project)
                elif due_dt <= week_end and due_dt > today:
                    due_this_week.append(project)
                elif due_dt < today:
                    overdue.append(project)
            except:
                pass
        
        if priority == 'High' and status != 'Completed':
            high_priority.append(project)
    
    # Display sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🔴 Overdue")
        if overdue:
            for project in overdue[:5]:
                with st.container():
                    st.warning(f"**{project.get('project_name', 'Unknown')[:60]}...**")
                    st.caption(f"Due: {project.get('due_date', 'Unknown')}")
                    st.caption(f"Category: {project.get('category', 'N/A')}")
                    st.markdown("---")
        else:
            st.success("No overdue tasks! 🎉")
        
        st.markdown("#### 🟠 Due Today")
        if due_today:
            for project in due_today:
                with st.container():
                    st.warning(f"**{project.get('project_name', 'Unknown')[:60]}...**")
                    st.caption(f"Priority: {project.get('priority', 'Medium')}")
                    st.caption(f"Category: {project.get('category', 'N/A')}")
                    st.markdown("---")
        else:
            st.info("No tasks due today")
    
    with col2:
        st.markdown("#### 🟡 Due This Week")
        if due_this_week:
            for project in due_this_week[:10]:
                with st.container():
                    st.info(f"**{project.get('project_name', 'Unknown')[:60]}...**")
                    st.caption(f"Due: {project.get('due_date', 'Unknown')}")
                    st.caption(f"Category: {project.get('category', 'N/A')}")
                    st.markdown("---")
        else:
            st.info("No tasks due this week")
        
        st.markdown("#### 🔥 High Priority Tasks")
        if high_priority:
            for project in high_priority[:10]:
                with st.container():
                    st.error(f"**{project.get('project_name', 'Unknown')[:60]}...**")
                    st.caption(f"Status: {project.get('status', 'Unknown')}")
                    st.caption(f"Due: {project.get('due_date', 'No due date')}")
                    st.markdown("---")
        else:
            st.info("No high priority tasks")


def show_file_repository():
    """File repository for project attachments"""
    
    st.markdown("### 📁 Project File Repository")
    st.caption("Upload and manage files related to your projects")
    
    # Initialize file storage
    if 'ndc_files' not in st.session_state:
        st.session_state.ndc_files = []
    
    # File upload
    with st.expander("📤 Upload File", expanded=False):
        with st.form("upload_ndc_file"):
            col1, col2 = st.columns(2)
            with col1:
                file_title = st.text_input("File Title", key="ndc_file_title")
                # Get project list for linking
                project_names = [p.get('project_name', '')[:80] for p in st.session_state.ndc_projects]
                linked_project = st.selectbox("Link to Project", [""] + project_names, key="ndc_linked_project")
            with col2:
                file_category = st.selectbox("Category", ["Proposal", "Report", "Presentation", "Data", "Reference", "Other"], key="ndc_file_category")
                file_tags = st.text_input("Tags", placeholder="comma separated", key="ndc_file_tags")
            
            file_description = st.text_area("Description", key="ndc_file_description")
            uploaded_file = st.file_uploader("Select File", type=['pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'png'], key="ndc_file_upload")
            
            submitted = st.form_submit_button("📎 Upload File")
            
            if submitted and file_title and uploaded_file:
                folder = "local_storage/ndc_personal/files"
                os.makedirs(folder, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{uploaded_file.name}"
                file_path = os.path.join(folder, filename)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                new_file = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": file_title,
                    "linked_project": linked_project,
                    "category": file_category,
                    "tags": file_tags,
                    "description": file_description,
                    "filename": filename,
                    "file_path": file_path,
                    "file_size": get_file_size(file_path),
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.ndc_files.append(new_file)
                st.success(f"✅ File '{file_title}' uploaded!")
                st.rerun()
    
    # Display files
    if st.session_state.ndc_files:
        st.markdown("#### 📄 Uploaded Files")
        for file in reversed(st.session_state.ndc_files):
            with st.expander(f"📎 {file.get('title')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Project:** {file.get('linked_project', 'Unlinked')[:60]}...")
                    st.markdown(f"**Category:** {file.get('category', 'N/A')}")
                    st.markdown(f"**Tags:** {file.get('tags', 'N/A')}")
                with col2:
                    st.markdown(f"**Size:** {file.get('file_size', 'N/A')}")
                    st.markdown(f"**Uploaded:** {file.get('uploaded_at', 'N/A')[:10]}")
                
                st.markdown(f"**Description:** {file.get('description', 'No description')}")
                
                if file.get('file_path') and os.path.exists(file.get('file_path')):
                    with open(file.get('file_path'), "rb") as f:
                        st.download_button("📥 Download", f, file_name=file.get('filename'), key=f"download_ndc_{file.get('id')}")
                
                if st.button(f"🗑️ Delete", key=f"del_ndc_file_{file.get('id')}"):
                    if file.get('file_path') and os.path.exists(file.get('file_path')):
                        os.remove(file.get('file_path'))
                    st.session_state.ndc_files = [f for f in st.session_state.ndc_files if f.get('id') != file.get('id')]
                    st.rerun()
    else:
        st.info("No files uploaded yet.")


def show_import_export():
    """Import/Export functionality"""
    
    st.markdown("### 📥 Import / Export Data")
    st.caption("Download your project data as Excel or CSV")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Export Data")
        
        if st.button("📊 Export to CSV", use_container_width=True):
            df = pd.DataFrame(st.session_state.ndc_projects)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"ndc_projects_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                key="download_csv"
            )
        
        if st.button("📄 Export to Excel", use_container_width=True):
            st.info("Excel export will be available in the next update")
    
    with col2:
        st.markdown("#### 📥 Import Data")
        st.markdown("Upload an Excel/CSV file to import projects")
        
        uploaded_file = st.file_uploader("Choose file", type=['csv', 'xlsx'], key="import_file")
        
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
            if st.button("Process Import", key="process_import"):
                st.info("Import processing will be available in the next update")


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How NDC Personal connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 Performance Management
        - IPCR targets linked to personal projects
        - Project completion affects performance rating
        - Task tracking integrated with IPCR
        
        ### 📋 Plan Management
        - Personal PPAs align with office plans
        - Project outputs feed into OPCR
        - Strategic initiatives tracked here
        """)
    
    with col2:
        st.markdown("""
        ### 📚 Trainings
        - Training needs identified from projects
        - Capacity building linked to project requirements
        - Certification tracking
        
        ### 🌍 Climate Change
        - MPCFS projects tracked here
        - Climate adaptation initiatives
        - Research projects documented
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to Performance Management", use_container_width=True):
            st.session_state.navigation = "📊 PERFORMANCE MANAGEMENT"
            st.rerun()
    with col2:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col3:
        if st.button("🌍 Go to Climate Change", use_container_width=True):
            st.session_state.navigation = "🌍 CLIMATE CHANGE"
            st.rerun()