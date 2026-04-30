"""
STANDALONE TITLE GENERATOR TESTER - UNIVERSAL (All Hazard Types)
Purpose: Test the title generation system for ALL hazard/incident categories
"""

import streamlit as st

st.set_page_config(
    page_title="Universal Title Generator",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Universal Title Generator")
st.caption("Select incident category, phase, and enter incident details. The system generates appropriate titles based on the category.")

# =============================================================================
# INITIALIZE SESSION STATE
# =============================================================================

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Hydrometeorological"
if "selected_phase" not in st.session_state:
    st.session_state.selected_phase = "Monitoring"
if "sitrep_num" not in st.session_state:
    st.session_state.sitrep_num = 1
if "incident_text" not in st.session_state:
    st.session_state.incident_text = ""
if "location" not in st.session_state:
    st.session_state.location = ""

# =============================================================================
# INCIDENT CATEGORIES WITH CLASSIFICATION
# =============================================================================

incident_categories = {
    "🌊 Hydrometeorological": {
        "type": "weather",
        "examples": ["Typhoon", "Heavy Rainfall", "Monsoon", "ITCZ", "LPA", "Shear Line", "Thunderstorm", "Flood", "Drought", "Heatwave"]
    },
    "🌋 Geological": {
        "type": "weather",  # Uses same wording family as weather
        "examples": ["Earthquake", "Landslide", "Rockfall", "Ground Rupture", "Liquefaction", "Volcanic Eruption"]
    },
    "🔥 Fire Incident": {
        "type": "sudden_onset",
        "examples": ["Structural Fire", "Forest Fire", "Grass Fire"]
    },
    "🏭 Technological / Human-Induced": {
        "type": "sudden_onset",
        "examples": ["Aviation Accident", "Chemical Spill", "Vehicular Accident", "Infrastructure Collapse"]
    },
    "🛡️ Public Safety / Security": {
        "type": "sudden_onset",
        "examples": ["Shooting Incident", "Stabbing Incident", "Armed Conflict"]
    },
    "🏥 Health / Medical": {
        "type": "sudden_onset",
        "examples": ["Medical Emergency", "Disease Outbreak", "Food Poisoning", "Mass Casualty"]
    },
    "⚡ Lifeline / Service Disruption": {
        "type": "slow_onset",
        "examples": ["Power Outage", "Water Shortage", "Communication Outage", "Transport Disruption"]
    },
    "🔍 Search / Missing Person": {
        "type": "search",
        "examples": ["Missing Person", "Search Operation", "Retrieval Operation"]
    }
}

# =============================================================================
# OPERATIONAL PHASES (Universal Dropdown)
# =============================================================================

operational_phases = [
    "Monitoring",
    "Preparedness",
    "Incident / Effects Monitoring",
    "Impact Assessment",
    "Terminal Reporting"
]

# =============================================================================
# PHASE DESCRIPTIONS
# =============================================================================

phase_descriptions = {
    "Monitoring": "Early stage - tracking, advisories, forecasts, initial reports",
    "Preparedness": "Pre-impact actions, anticipatory measures, prepositioning",
    "Incident / Effects Monitoring": "During impact or immediate aftermath, tracking ongoing situation",
    "Impact Assessment": "Validated damages, casualties, needs assessment",
    "Terminal Reporting": "End of operations, final consolidation, lessons learned"
}

# =============================================================================
# TITLE TEMPLATES BY CATEGORY TYPE
# =============================================================================

# Family A: Weather / Geologic / Slow-onset
templates_weather_slow = {
    "Monitoring": "Monitoring of {incident}",
    "Preparedness": "Preparedness and Anticipatory Actions for the Possible Effects of {incident}",
    "Incident / Effects Monitoring": "Monitoring of the Effects of {incident}",
    "Impact Assessment": "Impact and Needs Assessment of {incident}",
    "Terminal Reporting": "Terminal Report on the Effects and Impacts of {incident}"
}

# Family B: Fire / Accident / Security / Medical (Sudden-onset)
templates_sudden_onset = {
    "Monitoring": "Monitoring of {incident}",
    "Preparedness": "Preparedness Measures and Anticipatory Actions for Possible {incident_base} Incidents",
    "Incident / Effects Monitoring": "Monitoring of {incident} and Response Actions",
    "Impact Assessment": "Impact and Needs Assessment of {incident}",
    "Terminal Reporting": "Terminal Report on {incident}"
}

# Family C: Search / Investigation
templates_search = {
    "Monitoring": "Monitoring of {incident}",
    "Preparedness": "Preparedness Measures for Possible Related Incidents",
    "Incident / Effects Monitoring": "Incident Monitoring and Coordination for {incident}",
    "Impact Assessment": "Assessment of Effects and Operational Requirements for {incident}",
    "Terminal Reporting": "Terminal Report on {incident}"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_incident_base(incident_text):
    """Extract base incident type for Preparedness phase wording"""
    # Common patterns
    if "fire" in incident_text.lower():
        return "Fire"
    elif "accident" in incident_text.lower():
        return "Accident"
    elif "spill" in incident_text.lower():
        return "Chemical Spill"
    elif "shooting" in incident_text.lower():
        return "Shooting"
    elif "stabbing" in incident_text.lower():
        return "Stabbing"
    elif "emergency" in incident_text.lower():
        return "Medical Emergency"
    else:
        # Return first few words
        words = incident_text.split()[:3]
        return " ".join(words)

def generate_title(category_type, phase, incident, location, sitrep_num):
    """Generate title based on category type and phase"""
    
    if not incident:
        return None
    
    # Select template family
    if category_type == "weather" or category_type == "slow_onset":
        templates = templates_weather_slow
        title_template = templates.get(phase, "")
        title = title_template.format(incident=incident)
        
    elif category_type == "sudden_onset":
        templates = templates_sudden_onset
        title_template = templates.get(phase, "")
        if phase == "Preparedness":
            incident_base = get_incident_base(incident)
            title = title_template.format(incident=incident, incident_base=incident_base)
        else:
            title = title_template.format(incident=incident)
        
    elif category_type == "search":
        templates = templates_search
        title_template = templates.get(phase, "")
        title = title_template.format(incident=incident)
        
    else:
        # Default fallback
        title = f"{phase} of {incident}"
    
    # Add location if provided
    if location:
        title = f"{title} ({location})"
    
    return f"SITREP #{sitrep_num}: {title}"

# =============================================================================
# UI LAYOUT
# =============================================================================

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📋 Input Section")
    
    # SITREP Number
    st.markdown(f"**Current SITREP #:** {st.session_state.sitrep_num}")
    sitrep_num = st.number_input(
        "SITREP # (editable)",
        min_value=1,
        value=st.session_state.sitrep_num,
        step=1,
        key="sitrep_num_widget"
    )
    st.session_state.sitrep_num = sitrep_num
    
    st.markdown("---")
    
    # ===== INCIDENT CATEGORY =====
    st.markdown("**1. Select Incident Category:**")
    
    selected_category_display = st.selectbox(
        "Category",
        options=list(incident_categories.keys()),
        index=list(incident_categories.keys()).index(st.session_state.selected_category) if st.session_state.selected_category in incident_categories else 0,
        key="category_select"
    )
    st.session_state.selected_category = selected_category_display
    
    # Show category type and examples
    category_info = incident_categories[selected_category_display]
    st.caption(f"**Type:** {category_info['type'].replace('_', ' ').upper()}")
    st.caption(f"**Examples:** {', '.join(category_info['examples'][:5])}")
    
    st.markdown("---")
    
    # ===== OPERATIONAL PHASE =====
    st.markdown("**2. Select Operational Phase:**")
    
    selected_phase = st.radio(
        "Phase",
        options=operational_phases,
        index=operational_phases.index(st.session_state.selected_phase) if st.session_state.selected_phase in operational_phases else 0,
        key="phase_radio",
        horizontal=True
    )
    st.session_state.selected_phase = selected_phase
    
    # Show phase description
    st.info(f"📖 **When to use:** {phase_descriptions.get(selected_phase, '')}")
    
    st.markdown("---")
    
    # ===== INCIDENT / HAZARD DESCRIPTION =====
    st.markdown("**3. Enter Incident / Hazard Description:**")
    
    incident_text = st.text_input(
        "Incident",
        value=st.session_state.incident_text,
        placeholder="e.g., Typhoon Uwan, Structural Fire at Municipal Hall, Water Shortage in Paracelis",
        key="incident_input"
    )
    st.session_state.incident_text = incident_text
    
    # Quick example buttons based on category
    st.markdown("**Quick Examples (click to fill):**")
    example_cols = st.columns(4)
    for i, example in enumerate(category_info['examples'][:4]):
        with example_cols[i]:
            if st.button(f"📌 {example}", key=f"ex_{i}"):
                st.session_state.incident_text = example
                st.rerun()
    
    st.markdown("---")
    
    # ===== LOCATION =====
    st.markdown("**4. Location (Optional):**")
    location = st.text_input(
        "Location",
        value=st.session_state.location,
        placeholder="e.g., Bontoc, Mountain Province",
        key="location_input"
    )
    st.session_state.location = location

with col2:
    st.markdown("### ✅ Generated Title")
    
    if st.session_state.incident_text:
        # Generate title
        full_title = generate_title(
            category_info['type'],
            st.session_state.selected_phase,
            st.session_state.incident_text,
            st.session_state.location,
            st.session_state.sitrep_num
        )
        
        if full_title:
            # Display prominently
            st.success(f"## {full_title}")
            
            # Show breakdown
            st.markdown("---")
            st.markdown("### 📊 Title Breakdown")
            st.markdown(f"**SITREP #:** {st.session_state.sitrep_num}")
            st.markdown(f"**Category:** {st.session_state.selected_category}")
            st.markdown(f"**Category Type:** {category_info['type'].replace('_', ' ').upper()}")
            st.markdown(f"**Phase:** {st.session_state.selected_phase}")
            st.markdown(f"**Incident:** {st.session_state.incident_text}")
            if st.session_state.location:
                st.markdown(f"**Location:** {st.session_state.location}")
            
            # Copy button
            if st.button("📋 Copy to Clipboard", key="copy_title"):
                st.code(full_title, language="text")
                st.balloons()
        else:
            st.error("Error generating title. Please check your inputs.")
    else:
        st.info("👈 Select a category, phase, and enter incident description to generate a title")

# =============================================================================
# RESET BUTTON
# =============================================================================

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 START NEW SITREP", key="reset_test", use_container_width=True):
        st.session_state.sitrep_num = st.session_state.sitrep_num + 1
        st.session_state.selected_category = "🌊 Hydrometeorological"
        st.session_state.selected_phase = "Monitoring"
        st.session_state.incident_text = ""
        st.session_state.location = ""
        st.rerun()

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption("✅ Select a category, phase, and enter incident. The system generates appropriate titles based on the category type.")
st.caption("📌 Click 'START NEW SITREP' to increment SITREP # and clear all fields for a new report.")

# =============================================================================
# REFERENCE EXPANDER
# =============================================================================

with st.expander("📖 Reference: Title Generation Rules by Category Type", expanded=False):
    st.markdown("""
    ### How Titles Are Generated
    
    | Category Type | Categories | Title Style |
    |---------------|------------|-------------|
    | **Weather / Slow-onset** | Hydrometeorological, Geological, Lifeline Disruption | Formal, descriptive (e.g., "Preparedness and Anticipatory Actions for the Possible Effects of...") |
    | **Sudden-onset** | Fire, Technological, Public Safety, Health/Medical | Action-oriented (e.g., "Monitoring of ... and Response Actions") |
    | **Search** | Missing Person, Investigation | Coordination-focused (e.g., "Incident Monitoring and Coordination for...") |
    
    ---
    
    ### Title Templates by Phase
    
    | Phase | Weather / Slow-onset | Sudden-onset | Search |
    |-------|---------------------|--------------|--------|
    | Monitoring | Monitoring of [incident] | Monitoring of [incident] | Monitoring of [incident] |
    | Preparedness | Preparedness and Anticipatory Actions for the Possible Effects of [incident] | Preparedness Measures for Possible [type] Incidents | Preparedness Measures for Possible Related Incidents |
    | Incident/Effects Monitoring | Monitoring of the Effects of [incident] | Monitoring of [incident] and Response Actions | Incident Monitoring and Coordination for [incident] |
    | Impact Assessment | Impact and Needs Assessment of [incident] | Impact and Needs Assessment of [incident] | Assessment of Effects and Operational Requirements for [incident] |
    | Terminal Reporting | Terminal Report on the Effects and Impacts of [incident] | Terminal Report on [incident] | Terminal Report on [incident] |
    
    ---
    
    ### Example Outputs
    
    | Category | Phase | Incident | Generated Title |
    |----------|-------|----------|-----------------|
    | Hydrometeorological | Preparedness | Typhoon Uwan | SITREP #1: Preparedness and Anticipatory Actions for the Possible Effects of Typhoon Uwan |
    | Fire Incident | Incident/Effects Monitoring | Structural Fire at Public Market | SITREP #1: Monitoring of Structural Fire at Public Market and Response Actions |
    | Water Shortage | Monitoring | Water Shortage in Paracelis | SITREP #1: Monitoring of Water Shortage in Paracelis |
    | Missing Person | Incident/Effects Monitoring | Missing Person in Sitio Y | SITREP #1: Incident Monitoring and Coordination for Missing Person in Sitio Y |
    """)