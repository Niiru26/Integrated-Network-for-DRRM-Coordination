# tabs/performance_management.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import os
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected
from utils.local_storage import save_file, delete_file, get_file_size, file_exists

def show():
    """Display Performance Management Tab - IPCR and OPCR Tracking"""
    
    st.markdown("# 📊 Performance Management")
    st.caption("Individual and Office Performance Commitment and Review (IPCR/OPCR) Tracking")
    
    # Initialize session state
    if 'employees' not in st.session_state:
        st.session_state.employees = []
    
    if 'ipcr_records' not in st.session_state:
        st.session_state.ipcr_records = []
    
    if 'opcr_records' not in st.session_state:
        st.session_state.opcr_records = []
    
    # Simple login simulation
    if 'logged_in_user' not in st.session_state:
        st.session_state.logged_in_user = None
    
    # Check if user is logged in
    if st.session_state.logged_in_user is None:
        show_login()
        return
    
    # Show main interface based on role
    user = st.session_state.logged_in_user
    
    # Sidebar user info
    with st.sidebar:
        st.markdown(f"### 👤 Logged in as")
        st.markdown(f"**{user.get('name')}**")
        st.markdown(f"*{user.get('division')} Division*")
        st.markdown(f"Role: {user.get('role')}")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
        
        st.markdown("---")
    
    # Create tabs based on role
    if user.get('role') == 'admin':
        # Admin tabs - full access
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "👥 Employees",
            "📋 IPCR Management",
            "📁 OPCR Management",
            "📊 Performance Dashboard",
            "📎 File Repository",
            "🔗 Related Modules"
        ])
        
        with tab1:
            show_employee_management()
        with tab2:
            show_ipcr_admin()
        with tab3:
            show_opcr_admin()
        with tab4:
            show_performance_dashboard()
        with tab5:
            show_file_repository()
        with tab6:
            show_related_modules()
    
    else:
        # Employee view - only their own IPCR
        tab1, tab2, tab3 = st.tabs([
            "📋 My IPCR",
            "📊 My Performance",
            "🔗 Related Modules"
        ])
        
        with tab1:
            show_my_ipcr(user)
        with tab2:
            show_my_performance(user)
        with tab3:
            show_related_modules()


def show_login():
    """Simple login screen for employees"""
    
    st.markdown("### 👤 Employee Login")
    st.caption("Log in to view and update your IPCR")
    
    # Sample employee list
    employees = [
        {"id": 1, "name": "Administrator", "division": "Research & Planning", "role": "admin", "password": "admin123"},
        {"id": 2, "name": "Juan Dela Cruz", "division": "Research & Planning", "role": "employee", "password": "emp123"},
        {"id": 3, "name": "Maria Santos", "division": "Administration & Training", "role": "employee", "password": "emp123"},
        {"id": 4, "name": "Pedro Reyes", "division": "Operations & Warning", "role": "employee", "password": "emp123"},
        {"id": 5, "name": "Ana Flores", "division": "Infrastructure & Rehabilitation", "role": "employee", "password": "emp123"},
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.selectbox("Select Employee", [e["name"] for e in employees], key="login_username")
        password = st.text_input("Password", type="password", value="emp123", key="login_password")
    
    with col2:
        st.info("""
        **Demo Credentials:**
        - Admin: Administrator / admin123
        - Employee: Any name / emp123
        """)
    
    if st.button("🔐 Login", type="primary", key="login_button"):
        selected = next((e for e in employees if e["name"] == username), None)
        if selected and password == selected.get("password"):
            st.session_state.logged_in_user = selected
            st.success(f"Welcome, {selected['name']}!")
            st.rerun()
        else:
            st.error("Invalid credentials")


def show_employee_management():
    """Admin: Manage employees"""
    
    st.markdown("### Employee Directory")
    st.caption("Manage employees and their assignments")
    
    # Display current employees
    employees = [
        {"id": 1, "name": "Juan Dela Cruz", "division": "Research & Planning", "position": "DRRM Officer I"},
        {"id": 2, "name": "Maria Santos", "division": "Administration & Training", "position": "Administrative Officer"},
        {"id": 3, "name": "Pedro Reyes", "division": "Operations & Warning", "position": "Operations Officer"},
        {"id": 4, "name": "Ana Flores", "division": "Infrastructure & Rehabilitation", "position": "Infrastructure Officer"},
    ]
    
    df = pd.DataFrame(employees)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Add new employee form
    with st.expander("➕ Add New Employee", expanded=False):
        with st.form("add_employee_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", key="emp_name")
                division = st.selectbox("Division", [
                    "Research & Planning",
                    "Administration & Training",
                    "Operations & Warning",
                    "Infrastructure & Rehabilitation"
                ], key="emp_division")
            with col2:
                position = st.text_input("Position", key="emp_position")
                password = st.text_input("Temporary Password", type="password", key="emp_password")
            
            submitted = st.form_submit_button("💾 Save Employee")
            
            if submitted and name:
                new_employee = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "name": name,
                    "division": division,
                    "position": position,
                    "password": password,
                    "role": "employee",
                    "created_at": datetime.now().isoformat()
                }
                st.session_state.employees.append(new_employee)
                st.success(f"✅ Employee {name} added!")
                st.rerun()


def show_ipcr_admin():
    """Admin: Manage all IPCR records"""
    
    st.markdown("### IPCR Management")
    st.caption("View and manage Individual Performance Commitment and Review forms")
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    with col1:
        divisions = ["All"] + ["Research & Planning", "Administration & Training", "Operations & Warning", "Infrastructure & Rehabilitation"]
        filter_division = st.selectbox("Filter by Division", divisions, key="ipcr_filter_division")
    with col2:
        quarters = ["All", "Q1", "Q2", "Q3", "Q4"]
        filter_quarter = st.selectbox("Filter by Quarter", quarters, key="ipcr_filter_quarter")
    with col3:
        years = ["All", "2024", "2025", "2026"]
        filter_year = st.selectbox("Filter by Year", years, key="ipcr_filter_year")
    
    # Sample IPCR data
    ipcr_data = [
        {"employee": "Juan Dela Cruz", "division": "Research & Planning", "quarter": "Q1", "year": 2026, "status": "Pending", "targets": 5, "accomplished": 4},
        {"employee": "Maria Santos", "division": "Administration & Training", "quarter": "Q1", "year": 2026, "status": "Approved", "targets": 8, "accomplished": 7},
        {"employee": "Pedro Reyes", "division": "Operations & Warning", "quarter": "Q1", "year": 2026, "status": "Submitted", "targets": 6, "accomplished": 5},
    ]
    
    df = pd.DataFrame(ipcr_data)
    
    # Apply filters
    if filter_division != "All":
        df = df[df['division'] == filter_division]
    if filter_quarter != "All":
        df = df[df['quarter'] == filter_quarter]
    if filter_year != "All":
        df = df[df['year'] == int(filter_year)]
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Add IPCR form
    with st.expander("➕ Add/Edit IPCR", expanded=False):
        with st.form("add_ipcr_form"):
            col1, col2 = st.columns(2)
            with col1:
                employee = st.selectbox("Employee", ["Juan Dela Cruz", "Maria Santos", "Pedro Reyes"], key="ipcr_employee_select")
                quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], key="ipcr_quarter_select")
                year = st.number_input("Year", min_value=2024, max_value=2030, value=2026, key="ipcr_year_input")
            with col2:
                status = st.selectbox("Status", ["Draft", "Submitted", "Pending", "Approved", "Returned"], key="ipcr_status_select")
                rating = st.slider("Rating", 0.0, 5.0, 3.0, 0.1, key="ipcr_rating_slider")
            
            st.markdown("#### Performance Targets & Accomplishments")
            
            # Dynamic targets with unique keys
            targets = []
            for i in range(5):
                col1, col2 = st.columns(2)
                with col1:
                    target = st.text_input(f"Target {i+1}", key=f"ipcr_target_{i}")
                with col2:
                    accomplishment = st.text_input(f"Accomplishment {i+1}", key=f"ipcr_acc_{i}")
                if target or accomplishment:
                    targets.append({"target": target, "accomplishment": accomplishment})
            
            # File upload
            st.markdown("#### 📎 Upload Signed IPCR")
            uploaded_file = st.file_uploader("Upload IPCR PDF", type=['pdf'], key="ipcr_upload_file")
            
            submitted = st.form_submit_button("💾 Save IPCR")
            
            if submitted:
                st.success("✅ IPCR saved!")
                st.rerun()


def show_opcr_admin():
    """Admin: Manage OPCR records"""
    
    st.markdown("### OPCR Management")
    st.caption("Office Performance Commitment and Review - Division level")
    
    # OPCR data
    opcr_data = [
        {"division": "Research & Planning", "quarter": "Q1", "year": 2026, "status": "Approved", "targets": 12, "accomplished": 10},
        {"division": "Administration & Training", "quarter": "Q1", "year": 2026, "status": "Pending", "targets": 15, "accomplished": 12},
        {"division": "Operations & Warning", "quarter": "Q1", "year": 2026, "status": "Submitted", "targets": 10, "accomplished": 9},
        {"division": "Infrastructure & Rehabilitation", "quarter": "Q1", "year": 2026, "status": "Draft", "targets": 8, "accomplished": 6},
    ]
    
    df = pd.DataFrame(opcr_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Add OPCR form
    with st.expander("➕ Add OPCR", expanded=False):
        with st.form("add_opcr_form"):
            col1, col2 = st.columns(2)
            with col1:
                division = st.selectbox("Division", [
                    "Research & Planning",
                    "Administration & Training",
                    "Operations & Warning",
                    "Infrastructure & Rehabilitation"
                ], key="opcr_division_select")
                quarter = st.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"], key="opcr_quarter_select")
                year = st.number_input("Year", min_value=2024, max_value=2030, value=2026, key="opcr_year_input")
            with col2:
                status = st.selectbox("Status", ["Draft", "Submitted", "Pending", "Approved"], key="opcr_status_select")
                rating = st.slider("Division Rating", 0.0, 5.0, 3.0, 0.1, key="opcr_rating_slider")
            
            st.markdown("#### Division Targets & Accomplishments")
            targets = st.text_area("Key Targets", placeholder="List key division targets for the quarter", key="opcr_targets")
            accomplishments = st.text_area("Accomplishments", placeholder="List accomplishments", key="opcr_accomplishments")
            
            # File upload
            st.markdown("#### 📎 Upload Signed OPCR")
            uploaded_file = st.file_uploader("Upload OPCR PDF", type=['pdf'], key="opcr_upload_file")
            
            submitted = st.form_submit_button("💾 Save OPCR")
            
            if submitted:
                st.success("✅ OPCR saved!")
                st.rerun()


def show_performance_dashboard():
    """Admin: Performance analytics dashboard"""
    
    st.markdown("### Performance Dashboard")
    st.caption("Visual analytics of individual and office performance")
    
    # Sample data
    divisions = ["Research & Planning", "Administration & Training", "Operations & Warning", "Infrastructure & Rehabilitation"]
    completion_rates = [85, 78, 90, 72]
    
    fig = px.bar(x=divisions, y=completion_rates, title="Division Performance (Completion Rate %)",
                 labels={"x": "Division", "y": "Completion %"})
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
    # Employee performance
    st.markdown("#### Top Performing Employees")
    top_employees = [
        {"employee": "Pedro Reyes", "division": "Operations & Warning", "rating": 4.8},
        {"employee": "Juan Dela Cruz", "division": "Research & Planning", "rating": 4.5},
        {"employee": "Maria Santos", "division": "Administration & Training", "rating": 4.3},
    ]
    df = pd.DataFrame(top_employees)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Quarterly trends
    st.markdown("#### Quarterly Performance Trend")
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    scores = [82, 85, 88, 90]
    fig = px.line(x=quarters, y=scores, markers=True, title="Overall Office Performance Trend")
    st.plotly_chart(fig, use_container_width=True)


def show_file_repository():
    """Admin: View all uploaded IPCR/OPCR files"""
    
    st.markdown("### File Repository")
    st.caption("All uploaded IPCR and OPCR documents")
    
    # List files from local storage
    folder_path = "local_storage/performance_management"
    
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        if files:
            file_data = []
            for file in files:
                file_path = os.path.join(folder_path, file)
                stat = os.stat(file_path)
                file_data.append({
                    "filename": file,
                    "size": get_file_size(file_path),
                    "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "type": "PDF" if file.endswith('.pdf') else "Other"
                })
            df = pd.DataFrame(file_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No files uploaded yet.")
    else:
        st.info("No files uploaded yet.")


def show_my_ipcr(user):
    """Employee view: Their own IPCR"""
    
    st.markdown(f"### My IPCR - {user.get('name')}")
    st.caption(f"Division: {user.get('division')} | Quarter: Q1 2026")
    
    with st.form("my_ipcr_form"):
        st.markdown("#### Performance Targets")
        
        # Sample targets with unique keys
        targets = [
            {"target": "Complete 5 research reports", "accomplishment": "4 completed", "remarks": "On track"},
            {"target": "Attend 3 trainings", "accomplishment": "2 attended", "remarks": "In progress"},
            {"target": "Submit monthly reports", "accomplishment": "3/3 submitted", "remarks": "Completed"},
        ]
        
        for i, t in enumerate(targets):
            st.markdown(f"**Target {i+1}:** {t['target']}")
            col1, col2 = st.columns(2)
            with col1:
                accomplishment = st.text_input(
                    "Accomplishment", 
                    value=t['accomplishment'], 
                    key=f"my_ipcr_acc_{i}"
                )
            with col2:
                remarks = st.text_input(
                    "Remarks", 
                    value=t['remarks'], 
                    key=f"my_ipcr_rem_{i}"
                )
        
        st.markdown("#### Self-Assessment Rating")
        rating = st.slider("Self Rating", 0.0, 5.0, 3.5, 0.1, key="my_ipcr_rating")
        
        st.markdown("#### Upload Signed IPCR")
        uploaded_file = st.file_uploader("Upload your signed IPCR", type=['pdf'], key="my_ipcr_upload")
        
        submitted = st.form_submit_button("💾 Submit IPCR")
        
        if submitted:
            if uploaded_file:
                # Save to local storage
                folder = "local_storage/performance_management"
                os.makedirs(folder, exist_ok=True)
                file_path = os.path.join(folder, f"IPCR_{user.get('name')}_Q1_2026.pdf")
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success("✅ IPCR submitted for review!")
            else:
                st.warning("IPCR saved as draft. Please upload signed copy for submission.")


def show_my_performance(user):
    """Employee view: Their performance history"""
    
    st.markdown(f"### My Performance History - {user.get('name')}")
    
    performance_data = [
        {"quarter": "Q1 2025", "rating": 4.2, "status": "Approved"},
        {"quarter": "Q2 2025", "rating": 4.0, "status": "Approved"},
        {"quarter": "Q3 2025", "rating": 4.3, "status": "Approved"},
        {"quarter": "Q4 2025", "rating": 4.5, "status": "Approved"},
        {"quarter": "Q1 2026", "rating": 0, "status": "Pending"},
    ]
    
    df = pd.DataFrame(performance_data)
    
    # Current average
    past_ratings = df[df['rating'] > 0]['rating'].tolist()
    if past_ratings:
        avg_rating = sum(past_ratings) / len(past_ratings)
        st.metric("Average Rating (Last 4 Quarters)", f"{avg_rating:.1f}/5.0")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Performance trend
    df_valid = df[df['rating'] > 0]
    if not df_valid.empty:
        fig = px.line(df_valid, x='quarter', y='rating', markers=True, title="Performance Trend")
        st.plotly_chart(fig, use_container_width=True)


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How Performance Management connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Plan Management
        - **PPAs** link to IPCR/OPCR targets
        - Individual performance rolls up to office targets
        - Plan implementation tracked through IPCR
        
        ### 📚 Trainings
        - Training completion linked to IPCR targets
        - Skills development tracked
        - Certification records
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 DRRM Intelligence
        - Performance metrics inform risk assessment
        - Response effectiveness linked to training
        - Capacity indicators
        
        ### 💰 LDRRMF Utilization
        - Budget performance linked to OPCR
        - Fund utilization efficiency
        - Project completion tracking
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Go to Plan Management", use_container_width=True, key="link_plan"):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col2:
        if st.button("📚 Go to Trainings", use_container_width=True, key="link_trainings"):
            st.session_state.navigation = "📚 TRAININGS"
            st.rerun()
    with col3:
        if st.button("💰 Go to LDRRMF", use_container_width=True, key="link_ldrrmf"):
            st.session_state.navigation = "💰 LDRRMF UTILIZATION"
            st.rerun()