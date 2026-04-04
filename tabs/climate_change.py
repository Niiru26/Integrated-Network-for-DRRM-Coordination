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
    """MPCFS Infrastructure S-Curve Tracker - COMPLETE with Itemized Work Table"""
    
    st.markdown(f"#### 🏗️ Infrastructure Component - S-Curve Tracker")
    st.caption(f"Track physical and financial progress | Contract: ₱249,040,900.00")
    
    CONTRACT_AMOUNT = 249_040_900.00
    prefix = "infrastructure_"
    
    # ============================================================
    # COMPLETE WORK ITEMS DATA (from your Excel)
    # ============================================================
    
    if f'{prefix}work_items' not in st.session_state:
        work_items = [
            # Civil Works
            {"no": "A.1.1 (8)", "description": "Provision of Field Office for the Engineer", "category": "Civil Works", "weight": 0.546, "planned": 0.547, "actual": 0.50, "cost": 1_360_800},
            {"no": "A.1.2 (2)", "description": "Provision of 4x4 Pick Up Vehicle", "category": "Civil Works", "weight": 0.919, "planned": 0.919, "actual": 0.85, "cost": 2_289_000},
            {"no": "B.3", "description": "Permits and Clearances", "category": "Civil Works", "weight": 0.126, "planned": 0.126, "actual": 0.126, "cost": 315_000},
            {"no": "B.5", "description": "Project Billboard and Signboard", "category": "Civil Works", "weight": 0.004, "planned": 0.004, "actual": 0.004, "cost": 10_500},
            {"no": "B.7 (2)", "description": "Occupational Safety and Health Program", "category": "Civil Works", "weight": 1.229, "planned": 1.229, "actual": 1.10, "cost": 3_061_108},
            {"no": "B.9", "description": "Mobilization/Demobilization", "category": "Civil Works", "weight": 0.873, "planned": 0.873, "actual": 0.873, "cost": 2_174_130},
            {"no": "B.13", "description": "Additional Geotechnical Investigation", "category": "Civil Works", "weight": 0.126, "planned": 0.126, "actual": 0.126, "cost": 315_000},
            {"no": "B.25", "description": "Detailed Engineering and Architectural Design", "category": "Civil Works", "weight": 0.170, "planned": 0.170, "actual": 0.170, "cost": 424_499},
            {"no": "101(1)", "description": "Removal of Structures and Obstructions", "category": "Civil Works", "weight": 0.004, "planned": 0.004, "actual": 0.004, "cost": 9_419},
            {"no": "404", "description": "Reinforcing Steel Bar, Grade 40", "category": "Structural", "weight": 1.417, "planned": 1.417, "actual": 1.14, "cost": 2_834_045},
            {"no": "405", "description": "Structural Concrete Class A", "category": "Structural", "weight": 1.971, "planned": 1.971, "actual": 0.70, "cost": 1_740_048},
            {"no": "803(1)a", "description": "Structure Excavation", "category": "Structural", "weight": 0.628, "planned": 0.628, "actual": 0.54, "cost": 1_357_263},
            {"no": "804(4)", "description": "Gravel Fill", "category": "Structural", "weight": 0.632, "planned": 0.632, "actual": 0.54, "cost": 1_336_224},
            {"no": "1706(1)", "description": "Overhaul", "category": "Structural", "weight": 0.291, "planned": 0.291, "actual": 0.23, "cost": 560_761},
            {"no": "900(1)c2", "description": "Structural Concrete for Footing", "category": "Structural", "weight": 1.710, "planned": 1.710, "actual": 1.43, "cost": 3_561_496},
            {"no": "900(1)", "description": "Structural Concrete for Columns", "category": "Structural", "weight": 4.134, "planned": 4.134, "actual": 1.39, "cost": 3_449_789},
            {"no": "902(1) a", "description": "Reinforcing Steel", "category": "Structural", "weight": 9.308, "planned": 9.308, "actual": 3.06, "cost": 7_625_371},
            {"no": "903(1)", "description": "Formworks and Falseworks", "category": "Structural", "weight": 1.270, "planned": 1.270, "actual": 0.38, "cost": 948_291},
            {"no": "1047 (1)", "description": "Structural Steel", "category": "Structural", "weight": 14.170, "planned": 14.170, "actual": 11.44, "cost": 28_583_543},
            {"no": "1047 (2)a", "description": "Structural Steel (Trusses)", "category": "Structural", "weight": 1.757, "planned": 1.757, "actual": 0.33, "cost": 823_223},
            {"no": "1047 (3)a", "description": "Anchor Bolt", "category": "Structural", "weight": 1.505, "planned": 1.505, "actual": 1.39, "cost": 3_453_257},
            {"no": "1047 (5)", "description": "Steel Plates", "category": "Structural", "weight": 1.799, "planned": 1.799, "actual": 1.23, "cost": 3_071_727},
            {"no": "1001(11)", "description": "Septic Vault", "category": "Architectural", "weight": 0.436, "planned": 0.436, "actual": 0.22, "cost": 543_264},
        ]
        st.session_state[f'{prefix}work_items'] = work_items
    
    # ============================================================
    # S-CURVE DATA
    # ============================================================
    
    # Original Plan cumulative
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
    
    # Revised Plan cumulative
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
    
    # Actual progress weekly
    actual_weekly = [
        0.88, 0.91, 0.95, 1.00, 1.05, 1.10, 1.45, 1.62, 2.12, 2.45, 2.85, 3.21, 3.44, 3.85, 3.95, 4.05,
        4.17, 4.30, 4.40, 4.50, 4.61, 4.70, 4.81, 4.89, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
        5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04,
        5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 5.04, 7.33,
        9.88, 11.61, 13.40, 15.45, 17.73, 20.02, 22.30, 24.59, 24.67, 24.75, 24.83, 24.92, 25.14, 25.34, 25.55, 25.75
    ]
    while len(actual_weekly) < 193:
        actual_weekly.append(25.75)
    
    work_items = st.session_state[f'{prefix}work_items']
    
    # Calculate overall progress from work items
    total_weight = sum(item['weight'] for item in work_items)
    weighted_actual = sum((item['weight'] * item['actual']) / 100 for item in work_items)
    overall_progress = weighted_actual
    total_actual_cost = sum(item['cost'] for item in work_items)
    
    # Update session state
    st.session_state.infrastructure_progress = overall_progress
    st.session_state.infrastructure_cost = total_actual_cost
    
    weeks = list(range(1, 194))
    current_week_idx = 0
    for i, val in enumerate(actual_weekly):
        if val >= overall_progress and overall_progress > 0:
            current_week_idx = i
            break
    
    # ============================================================
    # KPI CARDS
    # ============================================================
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Overall Progress", f"{overall_progress:.2f}%")
    with col2:
        slippage = overall_progress - 25.75
        st.metric("Slippage vs Revised Plan", f"{slippage:+.2f}%")
    with col3:
        st.metric("Total Cost Utilized", f"₱{total_actual_cost:,.2f}")
    with col4:
        st.metric("Original Plan at Week 80", "64.31%")
    with col5:
        st.metric("Revised Plan at Week 80", "25.75%")
    
    st.markdown("---")
    
    # ============================================================
    # S-CURVE CHART
    # ============================================================
    
    st.markdown("### 📈 S-Curve: Planned vs Actual Progress")
    st.markdown("**📍 As of: Week 80 (March 31, 2026)**")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=weeks[:len(original_plan)], y=original_plan, mode='lines', name='Original Plan', line=dict(color='#1f77b4', width=2, dash='dash'), opacity=0.8))
    fig.add_trace(go.Scatter(x=weeks[:len(revised_plan)], y=revised_plan, mode='lines', name='Revised Plan', line=dict(color='#ff7f0e', width=2, dash='dot'), opacity=0.8))
    fig.add_trace(go.Scatter(x=weeks[:current_week_idx + 1], y=actual_weekly[:current_week_idx + 1], mode='lines+markers', name='Actual Progress', line=dict(color='#2ca02c', width=3), marker=dict(size=4)))
    
    fig.add_vline(x=current_week_idx + 1, line_dash="dash", line_color="#7f7f7f", line_width=1.5, annotation_text=f"Week {current_week_idx + 1}", annotation_position="top right")
    
    fig.update_layout(title="Project Progress S-Curve (September 2024 - May 2028)", xaxis_title="Week Number", yaxis_title="Cumulative Progress (%)", yaxis_range=[0, 105], height=450, hovermode='x unified', plot_bgcolor='white')
    st.plotly_chart(fig, use_container_width=True)
    
    # ============================================================
    # ITEMIZED WORK DETAILS TABLE (EDITABLE)
    # ============================================================
    
    st.markdown("### 📋 Itemized Work Details")
    st.markdown("> 🟢 **Edit the 'Actual %' and 'Actual Cost' columns below. Click SAVE ALL CHANGES to update.**")
    
    # Category filter
    categories = ["All", "Civil Works", "Structural", "Architectural"]
    selected_category = st.selectbox("🔍 Filter by Category", categories)
    
    if selected_category != "All":
        filtered_items = [item for item in work_items if item.get('category') == selected_category]
    else:
        filtered_items = work_items
    
    if filtered_items:
        df_items = pd.DataFrame(filtered_items)
        df_items['Variance (%)'] = df_items['actual'] - df_items['planned']
        df_items['Status'] = df_items['Variance (%)'].apply(lambda x: '✅ Ahead' if x > 0.1 else ('🟡 On Track' if x >= -0.1 else '🔴 Behind'))
        
        display_df = df_items[['no', 'description', 'weight', 'planned', 'actual', 'cost', 'Variance (%)', 'Status']].copy()
        display_df.columns = ['Item No.', 'Description', 'Weight (%)', 'Planned (%)', '🟢 Actual (%)', '🟢 Actual Cost (₱)', 'Variance (%)', 'Status']
        
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Item No.": st.column_config.TextColumn("Item No.", width="small", disabled=True),
                "Description": st.column_config.TextColumn("Description", width="large", disabled=True),
                "Weight (%)": st.column_config.NumberColumn("Weight (%)", format="%.3f", disabled=True),
                "Planned (%)": st.column_config.NumberColumn("Planned (%)", format="%.3f", disabled=True),
                "🟢 Actual (%)": st.column_config.NumberColumn("🟢 Actual (%)", min_value=0.0, max_value=100.0, step=0.5, format="%.2f"),
                "🟢 Actual Cost (₱)": st.column_config.NumberColumn("🟢 Actual Cost (₱)", min_value=0, step=10000, format="₱%.2f"),
                "Variance (%)": st.column_config.NumberColumn("Variance (%)", format="%+.2f", disabled=True),
                "Status": st.column_config.TextColumn("Status", disabled=True),
            }
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 SAVE ALL CHANGES", type="primary", use_container_width=True):
                for idx, row in edited_df.iterrows():
                    for original_item in work_items:
                        if original_item['no'] == row['Item No.']:
                            original_item['actual'] = row['🟢 Actual (%)']
                            original_item['cost'] = row['🟢 Actual Cost (₱)']
                            break
                st.session_state[f'{prefix}work_items'] = work_items
                st.success("✅ Changes saved! Progress recalculated.")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset to Zero", use_container_width=True):
                for item in work_items:
                    item['actual'] = 0
                    item['cost'] = 0
                st.session_state[f'{prefix}work_items'] = work_items
                st.success("✅ Reset complete.")
                st.rerun()
        
        # Summary Totals
        st.markdown("---")
        st.markdown("### 📊 Summary Totals")
        
        total_contract = sum(item['weight'] for item in work_items) * CONTRACT_AMOUNT / 100
        total_planned_cost = sum((item['planned'] * item['weight'] / 100) * CONTRACT_AMOUNT / 100 for item in work_items)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Contract", f"₱{CONTRACT_AMOUNT:,.2f}")
        with col2:
            st.metric("Total Planned Cost", f"₱{total_planned_cost:,.2f}")
        with col3:
            st.metric("Total Actual Cost", f"₱{total_actual_cost:,.2f}")
        with col4:
            variance = total_actual_cost - total_planned_cost
            st.metric("Cost Variance", f"₱{variance:+,.2f}")
    
    st.markdown("---")
    st.caption("Data source: MPCFS Project S-CURVE Sheet | Contract: ₱249,040,900.00")


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
        
        **APA Citation:**
        DOST-PAGASA. (2011). *Climate change in the Philippines*. DOST-PAGASA.
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
        
        **APA Citation:**
        DOST-PAGASA. (2024). *CMIP6-based climate change projections in the Philippines*. DOST-PAGASA.
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
    
    # APA Reference
    st.markdown("---")
    st.markdown("#### 📚 Reference (APA 7th Edition)")
    st.markdown("""
    DOST-PAGASA. (2011). *Climate change in the Philippines*. Department of Science and Technology - 
    Philippine Atmospheric, Geophysical and Astronomical Services Administration. 
    (UN-Philippines MDGIF Project in partnership with Adaptayo)
    """)
    
    st.caption("Source: DOST-PAGASA, 2011. Climate Change in the Philippines (Medium-Range Emission Scenario)")


def show_data_source_comparison():
    """Show comparison between 2011 DOST and 2024 CLIRAM data with APA7 citations"""
    
    st.markdown("#### 📊 Climate Data Sources Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📘 2011 DOST Data
        
        **APA 7th Edition Citation:**
        > DOST-PAGASA. (2011). *Climate change in the Philippines*. Department of Science and Technology - Philippine Atmospheric, Geophysical and Astronomical Services Administration. (UN-Philippines MDGIF Project in partnership with Adaptayo)
        
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
        
        **APA 7th Edition Citation:**
        > DOST-PAGASA. (2024). *CMIP6-based climate change projections in the Philippines*. Department of Science and Technology - Philippine Atmospheric, Geophysical and Astronomical Services Administration, Quezon City, Philippines.
        
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
    
    st.markdown("---")
    st.markdown("### 📚 Full References (APA 7th Edition)")
    st.markdown("""
    **DOST-PAGASA. (2011).** *Climate change in the Philippines*. Department of Science and Technology - Philippine Atmospheric, Geophysical and Astronomical Services Administration. (UN-Philippines MDGIF Project in partnership with Adaptayo)
    
    **DOST-PAGASA. (2024).** *CMIP6-based climate change projections in the Philippines*. Department of Science and Technology - Philippine Atmospheric, Geophysical and Astronomical Services Administration, Quezon City, Philippines.
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