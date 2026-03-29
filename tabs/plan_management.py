# tabs/plan_management.py
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, sync_plans, is_connected
from utils.local_storage import save_file, delete_file, get_file_info, get_file_size, file_exists
import os

def show():
    """Display Plan Management Tab - Fully Functional with Auto-Sync and Local File Storage"""
    
    st.markdown("# 📋 Plan Management")
    st.caption("Comprehensive planning and implementation tracking with automatic cloud sync")
    
    # Show sync status
    if is_connected():
        st.success("☁️ Auto-sync enabled - Changes save automatically to cloud")
    else:
        st.info("💾 Offline mode - Data saved locally")
    
    # Create tabs for different plan types
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Provincial Plans", 
        "🏘️ Municipal Plans", 
        "📊 PPAs & Activities",
        "📈 M&E Indicators",
        "✅ Implementation Tracker",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_provincial_plans()
    
    with tab2:
        show_municipal_plans()
    
    with tab3:
        show_ppas()
    
    with tab4:
        show_indicators()
    
    with tab5:
        show_implementation_tracker()
    
    with tab6:
        show_related_modules()


def upload_plan_file(plan_id, plan_type, uploaded_file):
    """Upload a file for a plan - stored locally, metadata in session state"""
    if not uploaded_file:
        return None
    
    # Save to local storage
    category = "plan_management"
    subcategory = f"{plan_type}_plans"
    
    # Create custom filename with plan ID and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"plan_{plan_id}_{timestamp}_{uploaded_file.name}"
    
    file_path = save_file(uploaded_file, category, subcategory, filename)
    
    return {
        "file_path": file_path,
        "filename": uploaded_file.name,
        "file_size": get_file_size(file_path),
        "file_type": uploaded_file.type,
        "uploaded_at": datetime.now().isoformat()
    }


def show_provincial_plans():
    """Display provincial plans with auto-sync and file attachments"""
    
    st.markdown("### Provincial DRRM Plans")
    st.caption("Comprehensive plans at the provincial level for disaster risk reduction")
    
    # Initialize session state
    if 'provincial_plans' not in st.session_state:
        st.session_state.provincial_plans = []
    
    # Add new plan form
    with st.expander("➕ Add New Provincial Plan", expanded=False):
        with st.form("add_provincial_plan"):
            col1, col2 = st.columns(2)
            with col1:
                plan_type = st.selectbox("Plan Type", ["CDP", "CLUP", "LCCAP", "AIP", "DRRM Plan", "CDRA"])
                title = st.text_input("Plan Title", placeholder="e.g., Provincial DRRM Plan 2024-2028")
                year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
            with col2:
                status = st.selectbox("Status", ["Draft", "For Approval", "Approved", "Under Review", "Completed", "Expired"])
                lead_agency = st.text_input("Lead Agency", placeholder="e.g., PDRRMO, PPDO")
                budget = st.number_input("Budget (₱)", min_value=0, value=0, step=10000, format="%d")
            
            description = st.text_area("Description", placeholder="Brief description of the plan and its key objectives")
            key_priorities = st.text_area("Key Priorities", placeholder="List key priorities and focus areas")
            
            # ========== NEW: FILE UPLOAD SECTION ==========
            st.markdown("#### 📎 Attach Plan Document")
            uploaded_file = st.file_uploader(
                "Upload Plan Document", 
                type=['pdf', 'docx', 'doc', 'xlsx', 'pptx'],
                help="Upload the official plan document (PDF, Word, Excel, or PowerPoint)"
            )
            # ==============================================
            
            submitted = st.form_submit_button("💾 Save Plan")
            
            if submitted and title:
                new_plan = {
                    "plan_type": plan_type,
                    "title": title,
                    "year": year,
                    "status": status,
                    "lead_agency": lead_agency,
                    "budget": budget,
                    "description": description,
                    "key_priorities": key_priorities,
                    "level": "provincial"
                }
                
                # First add to get an ID
                result = auto_sync_add('provincial_plans', 'provincial_plans', new_plan)
                
                # ========== NEW: Handle file upload after getting ID ==========
                if uploaded_file and result:
                    file_info = upload_plan_file(result.get('id'), "provincial", uploaded_file)
                    if file_info:
                        # Update the plan with file info
                        result['attached_file'] = file_info
                        auto_sync_update('provincial_plans', 'provincial_plans', result.get('id'), result)
                # ============================================================
                
                st.success(f"✅ Plan '{title}' saved and synced to cloud!")
                st.rerun()
    
    # Display plans
    if st.session_state.provincial_plans:
        df = pd.DataFrame(st.session_state.provincial_plans)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Plans", len(df))
        with col2:
            approved = len(df[df['status'] == 'Approved']) if 'status' in df.columns else 0
            st.metric("Approved", approved)
        with col3:
            draft = len(df[df['status'] == 'Draft']) if 'status' in df.columns else 0
            st.metric("In Draft", draft)
        with col4:
            total_budget = df['budget'].sum() if 'budget' in df.columns else 0
            st.metric("Total Budget", f"₱{total_budget:,.2f}")
        
        # Display table with file indicators
        display_df = df[['plan_type', 'title', 'year', 'status', 'lead_agency']].copy()
        # Add file indicator column
        display_df['Has File'] = df['attached_file'].apply(lambda x: "📎 Yes" if x else "No") if 'attached_file' in df.columns else "No"
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Detailed view with download links
        st.markdown("---")
        st.markdown("### 📄 Plan Documents")
        
        for plan in st.session_state.provincial_plans:
            with st.expander(f"📋 {plan.get('title', 'Untitled')} - {plan.get('status', 'Draft')}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Type:** {plan.get('plan_type', 'N/A')}")
                    st.markdown(f"**Year:** {plan.get('year', 'N/A')}")
                    st.markdown(f"**Lead Agency:** {plan.get('lead_agency', 'N/A')}")
                    st.markdown(f"**Budget:** ₱{plan.get('budget', 0):,.2f}")
                with col2:
                    st.markdown(f"**Status:** {plan.get('status', 'N/A')}")
                    st.markdown(f"**Created:** {plan.get('created_at', 'N/A')[:10] if plan.get('created_at') else 'N/A'}")
                
                st.markdown(f"**Description:** {plan.get('description', 'No description')}")
                
                # ========== NEW: Display attached file with download button ==========
                attached_file = plan.get('attached_file')
                if attached_file and attached_file.get('file_path') and file_exists(attached_file.get('file_path')):
                    st.markdown("**Attached Document:**")
                    file_path = attached_file['file_path']
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"📎 Download {attached_file.get('filename', 'file')} ({attached_file.get('file_size', 'N/A')})",
                            data=f,
                            file_name=attached_file.get('filename', 'document'),
                            key=f"download_{plan.get('id')}"
                        )
                elif attached_file:
                    st.warning("⚠️ File not found on local storage")
                # ================================================================
                
                st.markdown("---")
                st.warning(f"⚠️ Delete this plan? This action cannot be undone.")
                if st.button(f"🗑️ Delete Plan", key=f"del_prov_{plan.get('id')}"):
                    # Delete attached file if exists
                    if plan.get('attached_file') and plan['attached_file'].get('file_path'):
                        delete_file(plan['attached_file']['file_path'])
                    auto_sync_delete('provincial_plans', 'provincial_plans', plan.get('id'))
                    st.success("✅ Deleted and synced!")
                    st.rerun()
    else:
        st.info("📭 No provincial plans yet. Click 'Add New Provincial Plan' to get started.")


def show_municipal_plans():
    """Display municipal plans with auto-sync"""
    
    st.markdown("### Municipal DRRM Plans")
    st.caption("Individual plans for each municipality in Mountain Province")
    
    if 'municipal_plans' not in st.session_state:
        st.session_state.municipal_plans = []
    
    # Add new plan form
    with st.expander("➕ Add New Municipal Plan", expanded=False):
        with st.form("add_municipal_plan"):
            col1, col2 = st.columns(2)
            with col1:
                municipality = st.selectbox("Municipality", ["Bontoc", "Bauko", "Besao", "Sabangan", "Sadanga", "Tadian", "Natonin", "Paracelis", "Barlig"])
                plan_type = st.selectbox("Plan Type", ["CDP", "CLUP", "LCCAP", "AIP", "DRRM Plan"])
                title = st.text_input("Plan Title", placeholder=f"e.g., {municipality} DRRM Plan")
            with col2:
                year = st.number_input("Year", min_value=2020, max_value=2030, value=2024)
                status = st.selectbox("Status", ["Draft", "For Approval", "Approved", "Under Review"])
                budget = st.number_input("Budget (₱)", min_value=0, value=0, step=10000, format="%d")
            
            description = st.text_area("Description", placeholder="Brief description of the municipal plan")
            
            # ========== NEW: FILE UPLOAD SECTION ==========
            st.markdown("#### 📎 Attach Plan Document")
            uploaded_file = st.file_uploader(
                "Upload Plan Document", 
                type=['pdf', 'docx', 'doc', 'xlsx', 'pptx'],
                key="mun_upload",
                help="Upload the official municipal plan document"
            )
            # ==============================================
            
            submitted = st.form_submit_button("💾 Save Plan")
            
            if submitted and title:
                new_plan = {
                    "municipality": municipality,
                    "plan_type": plan_type,
                    "title": title,
                    "year": year,
                    "status": status,
                    "budget": budget,
                    "description": description,
                    "level": "municipal"
                }
                
                result = auto_sync_add('municipal_plans', 'municipal_plans', new_plan)
                
                # ========== NEW: Handle file upload ==========
                if uploaded_file and result:
                    file_info = upload_plan_file(result.get('id'), "municipal", uploaded_file)
                    if file_info:
                        result['attached_file'] = file_info
                        auto_sync_update('municipal_plans', 'municipal_plans', result.get('id'), result)
                # ============================================
                
                st.success(f"✅ Municipal plan for {municipality} saved and synced!")
                st.rerun()
    
    # Display plans
    if st.session_state.municipal_plans:
        df = pd.DataFrame(st.session_state.municipal_plans)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Plans", len(df))
        with col2:
            approved = len(df[df['status'] == 'Approved']) if 'status' in df.columns else 0
            st.metric("Approved", approved)
        with col3:
            total_budget = df['budget'].sum() if 'budget' in df.columns else 0
            st.metric("Total Budget", f"₱{total_budget:,.2f}")
        
        # Display table
        display_df = df[['municipality', 'plan_type', 'title', 'year', 'status']].copy()
        display_df['Has File'] = df['attached_file'].apply(lambda x: "📎 Yes" if x else "No") if 'attached_file' in df.columns else "No"
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Detailed view with download links
        st.markdown("---")
        st.markdown("### 📄 Municipal Plan Documents")
        
        for plan in st.session_state.municipal_plans:
            with st.expander(f"🏘️ {plan.get('title', 'Untitled')} - {plan.get('municipality', '')}"):
                st.markdown(f"**Municipality:** {plan.get('municipality', 'N/A')}")
                st.markdown(f"**Type:** {plan.get('plan_type', 'N/A')}")
                st.markdown(f"**Year:** {plan.get('year', 'N/A')}")
                st.markdown(f"**Status:** {plan.get('status', 'N/A')}")
                st.markdown(f"**Budget:** ₱{plan.get('budget', 0):,.2f}")
                st.markdown(f"**Description:** {plan.get('description', 'No description')}")
                
                # ========== NEW: Display attached file ==========
                attached_file = plan.get('attached_file')
                if attached_file and attached_file.get('file_path') and file_exists(attached_file.get('file_path')):
                    file_path = attached_file['file_path']
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"📎 Download {attached_file.get('filename', 'file')} ({attached_file.get('file_size', 'N/A')})",
                            data=f,
                            file_name=attached_file.get('filename', 'document'),
                            key=f"download_mun_{plan.get('id')}"
                        )
                # ===============================================
                
                st.markdown("---")
                if st.button(f"🗑️ Delete Plan", key=f"del_mun_{plan.get('id')}"):
                    if plan.get('attached_file') and plan['attached_file'].get('file_path'):
                        delete_file(plan['attached_file']['file_path'])
                    auto_sync_delete('municipal_plans', 'municipal_plans', plan.get('id'))
                    st.success("✅ Deleted and synced!")
                    st.rerun()
    else:
        st.info("📭 No municipal plans yet. Click 'Add New Municipal Plan' to get started.")


def show_ppas():
    """Display Programs, Projects, Activities with auto-sync"""
    
    st.markdown("### Programs, Projects & Activities (PPAs)")
    st.caption("Track implementation of specific programs, projects, and activities")
    
    if 'ppas' not in st.session_state:
        st.session_state.ppas = []
    
    with st.expander("➕ Add New PPA", expanded=False):
        with st.form("add_ppa"):
            col1, col2 = st.columns(2)
            with col1:
                ppa_type = st.selectbox("Type", ["Program", "Project", "Activity"])
                title = st.text_input("Title")
                responsible = st.text_input("Responsible Office")
                status = st.selectbox("Status", ["Planning", "Ongoing", "Completed", "Delayed", "Cancelled"])
            with col2:
                start_date = st.date_input("Start Date")
                end_date = st.date_input("End Date")
                budget = st.number_input("Budget (₱)", min_value=0, value=0, step=10000, format="%d")
                progress = st.slider("Progress (%)", 0, 100, 0)
            
            description = st.text_area("Description")
            remarks = st.text_area("Remarks / Challenges")
            
            # ========== NEW: FILE UPLOAD SECTION ==========
            st.markdown("#### 📎 Attach PPA Document")
            uploaded_file = st.file_uploader(
                "Upload PPA Document", 
                type=['pdf', 'docx', 'doc', 'xlsx', 'pptx'],
                key="ppa_upload",
                help="Upload project proposal, contract, or implementation plan"
            )
            # ==============================================
            
            submitted = st.form_submit_button("💾 Save PPA")
            
            if submitted and title:
                new_ppa = {
                    "type": ppa_type,
                    "title": title,
                    "responsible": responsible,
                    "status": status,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "budget": budget,
                    "progress": progress,
                    "description": description,
                    "remarks": remarks
                }
                
                result = auto_sync_add('ppas', 'ppas', new_ppa)
                
                # ========== NEW: Handle file upload ==========
                if uploaded_file and result:
                    file_info = upload_plan_file(result.get('id'), "ppa", uploaded_file)
                    if file_info:
                        result['attached_file'] = file_info
                        auto_sync_update('ppas', 'ppas', result.get('id'), result)
                # ============================================
                
                st.success("✅ PPA saved and synced!")
                st.rerun()
    
    if st.session_state.ppas:
        df = pd.DataFrame(st.session_state.ppas)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total PPAs", len(df))
        with col2:
            ongoing = len(df[df['status'] == 'Ongoing']) if 'status' in df.columns else 0
            st.metric("Ongoing", ongoing)
        with col3:
            completed = len(df[df['status'] == 'Completed']) if 'status' in df.columns else 0
            st.metric("Completed", completed)
        with col4:
            total_budget = df['budget'].sum() if 'budget' in df.columns else 0
            st.metric("Total Budget", f"₱{total_budget:,.2f}")
        
        # Display with file indicator
        display_df = df[['type', 'title', 'status', 'progress', 'responsible']].copy()
        display_df['Has File'] = df['attached_file'].apply(lambda x: "📎 Yes" if x else "No") if 'attached_file' in df.columns else "No"
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download links for PPAs
        for ppa in st.session_state.ppas:
            attached_file = ppa.get('attached_file')
            if attached_file and attached_file.get('file_path') and file_exists(attached_file.get('file_path')):
                with st.expander(f"📄 {ppa.get('title', 'Untitled')} - Attached Document"):
                    file_path = attached_file['file_path']
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label=f"📎 Download {attached_file.get('filename', 'file')} ({attached_file.get('file_size', 'N/A')})",
                            data=f,
                            file_name=attached_file.get('filename', 'document'),
                            key=f"download_ppa_{ppa.get('id')}"
                        )
    else:
        st.info("📭 No PPAs yet. Click 'Add New PPA' to get started.")


def show_indicators():
    """Display M&E Indicators with auto-sync"""
    
    st.markdown("### Monitoring & Evaluation Indicators")
    st.caption("Track key performance indicators for plan implementation")
    
    if 'indicators' not in st.session_state:
        st.session_state.indicators = []
    
    with st.expander("➕ Add New Indicator", expanded=False):
        with st.form("add_indicator"):
            col1, col2 = st.columns(2)
            with col1:
                indicator_name = st.text_input("Indicator Name")
                category = st.selectbox("Category", ["Input", "Process", "Output", "Outcome", "Impact"])
                target_value = st.number_input("Target Value", min_value=0, value=100)
            with col2:
                unit = st.text_input("Unit", placeholder="e.g., %, number, ₱", value="%")
                baseline = st.number_input("Baseline", min_value=0, value=0)
                data_source = st.text_input("Data Source")
            
            description = st.text_area("Description")
            frequency = st.selectbox("Reporting Frequency", ["Monthly", "Quarterly", "Semi-Annual", "Annual"])
            
            submitted = st.form_submit_button("💾 Save Indicator")
            
            if submitted and indicator_name:
                new_indicator = {
                    "name": indicator_name,
                    "category": category,
                    "target": target_value,
                    "unit": unit,
                    "baseline": baseline,
                    "data_source": data_source,
                    "description": description,
                    "frequency": frequency
                }
                auto_sync_add('indicators', 'indicators', new_indicator)
                st.success("✅ Indicator saved and synced!")
                st.rerun()
    
    if st.session_state.indicators:
        df = pd.DataFrame(st.session_state.indicators)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No indicators yet. Click 'Add New Indicator' to get started.")


def show_implementation_tracker():
    """Display implementation tracking with auto-sync"""
    
    st.markdown("### Implementation Tracker")
    st.caption("Track progress of plan implementation across quarters")
    
    if 'implementation_tracker' not in st.session_state:
        st.session_state.implementation_tracker = []
    
    with st.expander("➕ Add Implementation Record", expanded=False):
        with st.form("add_tracker"):
            col1, col2 = st.columns(2)
            with col1:
                activity = st.text_input("Activity/PPA")
                quarter = st.selectbox("Quarter", ["Q1 (Jan-Mar)", "Q2 (Apr-Jun)", "Q3 (Jul-Sep)", "Q4 (Oct-Dec)"])
                year = st.number_input("Year", min_value=2024, max_value=2030, value=2024)
            with col2:
                status = st.selectbox("Status", ["Not Started", "On Track", "Delayed", "Completed", "Cancelled"])
                percent_complete = st.slider("% Complete", 0, 100, 0)
                responsible = st.text_input("Responsible")
            
            remarks = st.text_area("Remarks")
            challenges = st.text_area("Challenges / Issues")
            
            submitted = st.form_submit_button("💾 Save Record")
            
            if submitted and activity:
                new_record = {
                    "activity": activity,
                    "quarter": quarter,
                    "year": year,
                    "status": status,
                    "percent_complete": percent_complete,
                    "responsible": responsible,
                    "remarks": remarks,
                    "challenges": challenges
                }
                auto_sync_add('implementation_tracker', 'implementation_tracker', new_record)
                st.success("✅ Implementation record saved and synced!")
                st.rerun()
    
    if st.session_state.implementation_tracker:
        df = pd.DataFrame(st.session_state.implementation_tracker)
        
        # Progress summary
        col1, col2, col3 = st.columns(3)
        with col1:
            avg_progress = df['percent_complete'].mean() if 'percent_complete' in df.columns else 0
            st.metric("Average Implementation Progress", f"{avg_progress:.1f}%")
        with col2:
            on_track = len(df[df['status'] == 'On Track']) if 'status' in df.columns else 0
            st.metric("On Track", on_track)
        with col3:
            delayed = len(df[df['status'] == 'Delayed']) if 'status' in df.columns else 0
            st.metric("Delayed", delayed)
        
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("📭 No implementation records yet. Click 'Add Implementation Record' to get started.")


def show_related_modules():
    """Show related modules and connections"""
    
    st.markdown("### 🔗 Related Modules & Integration Points")
    st.caption("How Plan Management connects with other modules in INDC")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 Training & Capacity Building
        **Connection:** Plans identify required competencies
        
        - **Training Needs:** Plans identify skills gaps that need training
        - **Capacity Building:** Training completion links to plan implementation
        - **Responder Readiness:** Training metrics feed into plan indicators
        
        **Data Flow:** Plans → Identify needs → Trainings → Skills development → Implementation capacity
        """)
        
        st.info("""
        **Integration Tip:** When adding a plan, consider:
        - What training is needed to implement this plan?
        - Who needs to be trained?
        - When should training be completed?
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 💰 LDRRMF Utilization
        **Connection:** Plans determine fund allocation
        
        - **Budget Alignment:** LDRRMF should align with plan priorities
        - **Fund Tracking:** Monitor utilization against planned activities
        - **Financial Reporting:** Link expenditures to specific PPAs
        
        **Data Flow:** Plans → Budget allocation → Fund utilization → Implementation progress
        """)
        
        st.info("""
        **Integration Tip:** Each PPA should have:
        - Approved budget from LDRRMF
        - Actual expenditures tracked
        - Variance analysis against planned budget
        """)
    
    with col2:
        st.markdown("""
        ### 📡 Situation Report
        **Connection:** Real-time data informs planning
        
        - **Incident Data:** Actual events validate plan assumptions
        - **Response Metrics:** Evaluate plan effectiveness during actual events
        - **Scenario Planning:** Use historical data for future plans
        
        **Data Flow:** Incidents → Analysis → Plan updates → Better preparedness
        """)
        
        st.info("""
        **Integration Tip:** Review situation reports to:
        - Validate plan assumptions
        - Identify gaps in current plans
        - Update plans based on actual events
        """)
        
        st.markdown("---")
        
        st.markdown("""
        ### 📊 DRRM Intelligence
        **Connection:** Data analytics support evidence-based planning
        
        - **Risk Assessment:** Hazard data informs plan priorities
        - **Vulnerability Analysis:** Identify high-risk areas
        - **Capacity Assessment:** Current capabilities guide plan targets
        
        **Data Flow:** Risk data → Analysis → Plan priorities → Resource allocation
        """)
        
        st.info("""
        **Integration Tip:** Use DRRM Intelligence to:
        - Identify highest priority areas
        - Allocate resources based on risk
        - Set realistic targets based on capacity
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links to Related Modules")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📚 Go to Trainings", use_container_width=True):
            st.session_state.navigation = "📚 TRAININGS"
            st.rerun()
    with col2:
        if st.button("💰 Go to LDRRMF", use_container_width=True):
            st.session_state.navigation = "💰 LDRRMF UTILIZATION"
            st.rerun()
    with col3:
        if st.button("📡 Go to Situation Report", use_container_width=True):
            st.session_state.navigation = "📡 SITUATION REPORT"
            st.rerun()
    with col4:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Best Practices for Integrated Planning")
    
    st.markdown("""
    1. **Align Plans with Resources** - Ensure LDRRMF budget matches plan requirements
    2. **Build Capacity Early** - Schedule training before critical implementation phases
    3. **Use Real-time Data** - Let situation reports inform plan adjustments
    4. **Track Indicators** - Monitor progress against M&E targets quarterly
    5. **Review and Update** - Plans should be living documents, updated based on experience
    """)
    
    # Show summary of connections
    st.markdown("---")
    st.markdown("### 📊 Connected Data Summary")
    
    # Show counts from related modules
    col1, col2, col3 = st.columns(3)
    with col1:
        training_count = len(st.session_state.get('trainings', []))
        st.metric("Training Records", training_count)
        if training_count > 0:
            st.caption("Linked to capacity building needs in plans")
    
    with col2:
        fund_count = len(st.session_state.get('ldrrmf_records', []))
        st.metric("Fund Records", fund_count)
        if fund_count > 0:
            st.caption("Linked to plan budgets and PPAs")
    
    with col3:
        event_count = len(st.session_state.get('disaster_events', [])) if 'disaster_events' in st.session_state else 0
        st.metric("Incident Records", event_count)
        if event_count > 0:
            st.caption("Linked to plan validation and updates")