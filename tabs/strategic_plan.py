"""
Strategic Plan Tab - Working Version
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

def show():
    """Display Strategic Plan tab"""
    
    st.markdown("<h1 class='main-header'>📋 STRATEGIC PLAN</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #f8fafc; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
        <p>Manage and track DRRM plans including:</p>
        <ul>
            <li><strong>PCDRRMP</strong> - Provincial Climate and Disaster Risk Reduction and Management Plan</li>
            <li><strong>Enhanced LDRRM Plan</strong> - OCD template requirements</li>
            <li><strong>LCCAP</strong> - Local Climate Change Action Plan</li>
            <li><strong>Contingency Plans</strong> - Typhoon, Earthquake, Flood, Landslide</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📄 PCDRRMP",
        "📄 ENHANCED LDRRM PLAN",
        "📄 LCCAP",
        "📄 CONTINGENCY PLANS",
        "📊 PLAN TRACKER"
    ])
    
    # ===== TAB 1: PCDRRMP =====
    with tab1:
        st.markdown("### Provincial CDRRM Plan 2024-2028")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Plan Overview:**
            - **Period:** 2024-2028
            - **Version:** 2.0
            - **Status:** Active
            """)
        
        with col2:
            st.markdown("**Implementation Progress**")
            st.progress(65, text="65% Complete")
        
        st.markdown("---")
        
        st.markdown("#### Key Priority Areas")
        priorities = [
            {"area": "Disaster Prevention & Mitigation", "progress": 70},
            {"area": "Disaster Preparedness", "progress": 65},
            {"area": "Disaster Response", "progress": 60},
            {"area": "Disaster Rehabilitation & Recovery", "progress": 55}
        ]
        
        for p in priorities:
            col1, col2 = st.columns([2, 3])
            with col1:
                st.markdown(f"**{p['area']}**")
            with col2:
                st.progress(p['progress']/100)
                st.caption(f"{p['progress']}%")
        
        with st.expander("📤 Upload New Version", expanded=False):
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx'], key="pcdrrmp_upload")
            if uploaded_file:
                st.success(f"File ready: {uploaded_file.name}")
                if st.button("Save Plan"):
                    st.success("✅ Plan uploaded successfully!")
                    st.balloons()
    
    # ===== TAB 2: ENHANCED LDRRM PLAN =====
    with tab2:
        st.markdown("### Enhanced LDRRM Plan (OCD Template)")
        st.info("This template follows the Office of Civil Defense (OCD) requirements.")
        
        st.markdown("#### Compliance Checklist")
        compliance_items = [
            "Disaster Profile and Risk Assessment",
            "Goals, Objectives, and Targets",
            "Programs, Projects, and Activities",
            "Implementation Arrangements",
            "Monitoring and Evaluation Framework",
            "Financial Plan"
        ]
        
        for item in compliance_items:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"- {item}")
            with col2:
                st.checkbox("Complete", key=f"comp_{item}")
        
        with st.expander("📤 Upload Completed Plan", expanded=False):
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx'], key="ldrrm_upload")
            if uploaded_file:
                if st.button("Save Plan"):
                    st.success("✅ Enhanced LDRRM Plan uploaded!")
    
    # ===== TAB 3: LCCAP =====
    with tab3:
        st.markdown("### Local Climate Change Action Plan (LCCAP)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Period:** 2020-2028")
            st.markdown("**Status:** Active")
        with col2:
            st.progress(65, text="65% Complete")
        
        st.markdown("#### Priority Areas Progress")
        lccap_priorities = [
            "Food Security: 70%",
            "Water Security: 65%",
            "Health and Sanitation: 80%",
            "Infrastructure Resilience: 45%",
            "Ecosystems and Biodiversity: 60%"
        ]
        
        for p in lccap_priorities:
            st.markdown(f"- {p}")
        
        with st.expander("📤 Upload LCCAP Document", expanded=False):
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx'], key="lccap_upload")
            if uploaded_file:
                if st.button("Save LCCAP"):
                    st.success("✅ LCCAP uploaded!")
    
    # ===== TAB 4: CONTINGENCY PLANS =====
    with tab4:
        st.markdown("### Contingency Plans")
        
        contingency = ["Typhoon", "Earthquake", "Flood", "Landslide"]
        
        for cp in contingency:
            with st.expander(f"**{cp} Contingency Plan**"):
                col1, col2 = st.columns(2)
                with col1:
                    status = st.selectbox("Status", ["Draft", "In Progress", "Completed"], key=f"status_{cp}")
                with col2:
                    progress = st.slider("Progress", 0, 100, 50, key=f"progress_{cp}")
                
                st.progress(progress/100)
                
                uploaded_file = st.file_uploader(f"Upload {cp} Plan", type=['pdf', 'docx'], key=f"upload_{cp}")
                if uploaded_file:
                    if st.button(f"Save {cp} Plan", key=f"save_{cp}"):
                        st.success(f"✅ {cp} Contingency Plan uploaded!")
    
    # ===== TAB 5: PLAN TRACKER =====
    with tab5:
        st.markdown("### Plan Implementation Tracker")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Plans", "8")
        with col2:
            st.metric("Active Plans", "3")
        with col3:
            st.metric("In Progress", "4")
        with col4:
            st.metric("Completed", "1")
        
        st.markdown("---")
        
        timeline = pd.DataFrame({
            'Plan': ['PCDRRMP', 'Enhanced LDRRM', 'LCCAP', 'Typhoon CP', 'Earthquake CP', 'Flood CP', 'Landslide CP'],
            'Progress': [65, 40, 65, 75, 60, 40, 35],
            'Status': ['Active', 'Draft', 'Active', 'In Progress', 'In Progress', 'Draft', 'Draft']
        })
        
        st.dataframe(timeline, use_container_width=True, hide_index=True)
        
        fig = px.bar(timeline, x='Plan', y='Progress', title="Plan Implementation Progress",
                    color='Status',
                    color_discrete_map={'Active': '#1E3A8A', 'In Progress': '#FFA500', 'Draft': '#6c757d'})
        st.plotly_chart(fig, use_container_width=True)