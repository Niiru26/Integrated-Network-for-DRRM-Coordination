"""
STANDALONE TITLE GENERATOR TESTER - WEATHER DISTURBANCES
Purpose: Test the title generation system for Hydrometeorological Hazards
"""

import streamlit as st

st.set_page_config(
    page_title="Title Generator - Weather Disturbances",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 Title Generator - Weather Disturbances")
st.caption("Select a phase, click a hazard button, and see the generated title.")

# Initialize session state
if "selected_hazard" not in st.session_state:
    st.session_state.selected_hazard = ""
if "sitrep_num" not in st.session_state:
    st.session_state.sitrep_num = 1
if "selected_phase" not in st.session_state:
    st.session_state.selected_phase = "Pre-Impact Monitoring"
if "location" not in st.session_state:
    st.session_state.location = ""

# Operational Phases
operational_phases = [
    "Pre-Impact Monitoring",
    "Preparedness and Anticipatory Actions",
    "Incidents and Effects Monitoring",
    "Impact and Needs Assessment",
    "Terminal Reporting"
]

# Phase descriptions
phase_descriptions = {
    "Pre-Impact Monitoring": "Early watch stage, tracking advisories, forecasts, and risk monitoring",
    "Preparedness and Anticipatory Actions": "Pre-impact actions, PDRA, CPAs, prepositioning, evacuation readiness",
    "Incidents and Effects Monitoring": "During impact or immediate aftermath, tracking incidents and ongoing conditions",
    "Impact and Needs Assessment": "Validated damages, casualties, affected population, needs and gaps",
    "Terminal Reporting": "End of operations, final consolidated effects, response, lessons learned"
}

# Title templates
title_templates = {
    "Pre-Impact Monitoring": "Pre-Impact Monitoring of {hazard}",
    "Preparedness and Anticipatory Actions": "Preparedness for the Possible Effects of {hazard}",
    "Incidents and Effects Monitoring": "Monitoring of the Effects of {hazard}",
    "Impact and Needs Assessment": "Impact Assessment of {hazard}",
    "Terminal Reporting": "Terminal Report on the Effects and Impacts of {hazard}"
}

# Function to set hazard
def set_hazard(hazard_name):
    st.session_state.selected_hazard = hazard_name

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📋 Input Section")
    
    # SITREP Number
    sitrep_num = st.number_input(
        "SITREP #",
        min_value=1,
        value=st.session_state.sitrep_num,
        step=1,
        key="sitrep_num_widget"
    )
    st.session_state.sitrep_num = sitrep_num
    
    st.markdown("---")
    
    # ===== OPERATIONAL PHASE SELECTION - RADIO BUTTONS =====
    st.markdown("**1. Select Operational Phase:**")
    
    selected_phase = st.radio(
        "Select Phase",
        options=operational_phases,
        index=operational_phases.index(st.session_state.selected_phase) if st.session_state.selected_phase in operational_phases else 0,
        key="phase_radio",
        horizontal=True
    )
    st.session_state.selected_phase = selected_phase
    
    # Show phase description
    st.info(f"📖 **When to use:** {phase_descriptions.get(selected_phase, '')}")
    
    st.markdown("---")
    
    # ===== HAZARD SELECTION - BUTTONS =====
    st.markdown("**2. Select Hazard / Event:**")
    
    # Row 1: ITCZ, LPA, Monsoon, Shear Line
    st.markdown("**Atmospheric Disturbances:**")
    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns(4)
    with row1_col1:
        if st.button("🌧️ ITCZ", key="hazard_itcz", use_container_width=True):
            set_hazard("Intertropical Convergence Zone (ITCZ)")
            st.rerun()
    with row1_col2:
        if st.button("🌀 LPA", key="hazard_lpa", use_container_width=True):
            set_hazard("Low Pressure Area (LPA)")
            st.rerun()
    with row1_col3:
        if st.button("💨 Monsoon", key="hazard_monsoon", use_container_width=True):
            set_hazard("Monsoon (Southwest/Northeast)")
            st.rerun()
    with row1_col4:
        if st.button("⚡ Shear Line", key="hazard_shear", use_container_width=True):
            set_hazard("Shear Line")
            st.rerun()
    
    # Row 2: Thunderstorm, Tropical Depression, Tropical Storm, Severe Tropical Storm
    st.markdown("**Tropical Cyclones:**")
    row2_col1, row2_col2, row2_col3, row2_col4 = st.columns(4)
    with row2_col1:
        if st.button("⛈️ Thunderstorm", key="hazard_thunder", use_container_width=True):
            set_hazard("Thunderstorm")
            st.rerun()
    with row2_col2:
        if st.button("🌪️ Tropical Depression", key="hazard_td", use_container_width=True):
            set_hazard("Tropical Depression")
            st.rerun()
    with row2_col3:
        if st.button("🌪️ Tropical Storm", key="hazard_ts", use_container_width=True):
            set_hazard("Tropical Storm")
            st.rerun()
    with row2_col4:
        if st.button("🌪️ Severe Tropical Storm", key="hazard_sts", use_container_width=True):
            set_hazard("Severe Tropical Storm")
            st.rerun()
    
    # Row 3: Typhoon, Super Typhoon
    st.markdown("**Typhoons:**")
    row3_col1, row3_col2, row3_col3, row3_col4 = st.columns(4)
    with row3_col1:
        if st.button("🌪️ Typhoon", key="hazard_typhoon", use_container_width=True):
            set_hazard("Typhoon")
            st.rerun()
    with row3_col2:
        if st.button("🌪️ Super Typhoon", key="hazard_super", use_container_width=True):
            set_hazard("Super Typhoon")
            st.rerun()
    
    # Row 4: Riverine Flood, Flash Flood
    st.markdown("**Flooding:**")
    row4_col1, row4_col2, row4_col3, row4_col4 = st.columns(4)
    with row4_col1:
        if st.button("🌊 Riverine Flood", key="hazard_river", use_container_width=True):
            set_hazard("Riverine/Fluvial Flood")
            st.rerun()
    with row4_col2:
        if st.button("💧 Flash Flood", key="hazard_flash", use_container_width=True):
            set_hazard("Flash Flood")
            st.rerun()
    
    # Row 5: Drought, Heatwave
    st.markdown("**Other Hazards:**")
    row5_col1, row5_col2, row5_col3, row5_col4 = st.columns(4)
    with row5_col1:
        if st.button("🏜️ Drought", key="hazard_drought", use_container_width=True):
            set_hazard("Drought")
            st.rerun()
    with row5_col2:
        if st.button("🔥 Heatwave", key="hazard_heat", use_container_width=True):
            set_hazard("Heatwave")
            st.rerun()
    
    # Custom hazard input (optional)
    st.markdown("---")
    st.markdown("**Or enter custom hazard:**")
    custom_hazard = st.text_input("Custom Hazard", key="custom_hazard", placeholder="e.g., Typhoon Uwan")
    if custom_hazard:
        st.session_state.selected_hazard = custom_hazard
    
    st.markdown("---")
    
    # Location (Optional)
    st.markdown("**3. Location (Optional):**")
    location = st.text_input(
        "Location",
        value=st.session_state.location,
        placeholder="e.g., Bontoc, Mountain Province",
        key="location_widget"
    )
    st.session_state.location = location

with col2:
    st.markdown("### ✅ Generated Title")
    
    if st.session_state.selected_hazard:
        # Generate the title
        template = title_templates.get(st.session_state.selected_phase, "")
        if template:
            title = template.format(hazard=st.session_state.selected_hazard)
            if st.session_state.location:
                title = f"{title} ({st.session_state.location})"
            full_title = f"SITREP #{st.session_state.sitrep_num}: {title}"
            
            # Display the title prominently
            st.success(f"## {full_title}")
            
            # Show breakdown
            st.markdown("---")
            st.markdown("### 📊 Title Breakdown")
            st.markdown(f"**SITREP #:** {st.session_state.sitrep_num}")
            st.markdown(f"**Phase:** {st.session_state.selected_phase}")
            st.markdown(f"**Hazard:** {st.session_state.selected_hazard}")
            if st.session_state.location:
                st.markdown(f"**Location:** {st.session_state.location}")
            
            # Copy button
            if st.button("📋 Copy to Clipboard", key="copy_title"):
                st.code(full_title, language="text")
                st.balloons()
    else:
        st.info("👈 Click a hazard button above to generate a title")

# Reset button
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Reset All Fields", key="reset_test", use_container_width=True):
        st.session_state.selected_hazard = ""
        st.session_state.sitrep_num = 1
        st.session_state.selected_phase = "Pre-Impact Monitoring"
        st.session_state.location = ""
        st.rerun()

st.markdown("---")
st.caption("✅ Click a hazard button, select a phase (radio buttons), and the title generates automatically.")