"""
STANDALONE TITLE GENERATOR TESTER - ALL HAZARD CATEGORIES
Purpose: Test the title generation system for ALL hazard/incident types
Run with: streamlit run test_title_generator_weather.py
"""

import streamlit as st

st.set_page_config(
    page_title="Title Generator - All Hazards",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Universal Title Generator")
st.caption("Select a hazard category tab, choose a phase, click a hazard button, and see the generated title.")

# =============================================================================
# INITIALIZE SESSION STATE
# =============================================================================

if "selected_hazard" not in st.session_state:
    st.session_state.selected_hazard = ""
if "sitrep_num" not in st.session_state:
    st.session_state.sitrep_num = 1
if "selected_phase" not in st.session_state:
    st.session_state.selected_phase = "Monitoring"
if "location" not in st.session_state:
    st.session_state.location = ""

# =============================================================================
# OPERATIONAL PHASES (Common for ALL tabs)
# =============================================================================

operational_phases = [
    "Monitoring",
    "Preparedness",
    "Incident / Effects Monitoring",
    "Impact Assessment",
    "Terminal Reporting"
]

# Phase descriptions
phase_descriptions = {
    "Monitoring": "Early stage - tracking, advisories, forecasts, initial reports",
    "Preparedness": "Pre-impact actions, anticipatory measures, prepositioning",
    "Incident / Effects Monitoring": "During impact or immediate aftermath, tracking ongoing situation",
    "Impact Assessment": "Validated damages, casualties, needs assessment",
    "Terminal Reporting": "End of operations, final consolidation, lessons learned"
}

# =============================================================================
# WORDING FAMILIES (Title Templates)
# =============================================================================

# Family A: Weather / Slow-onset (Hydrometeorological, Geological, Lifeline Disruption)
templates_slow_onset = {
    "Monitoring": "Monitoring of {hazard}",
    "Preparedness": "Preparedness for the Possible Effects of {hazard}",
    "Incident / Effects Monitoring": "Monitoring of the Effects of {hazard}",
    "Impact Assessment": "Impact Assessment of {hazard}",
    "Terminal Reporting": "Terminal Report on the Effects and Impacts of {hazard}"
}

# Family B: Sudden-onset (Fire, Technological, Public Safety, Health/Medical)
templates_sudden_onset = {
    "Monitoring": "Monitoring of {hazard}",
    "Preparedness": "Preparedness Measures for Possible {hazard_base} Incidents",
    "Incident / Effects Monitoring": "Monitoring of {hazard} and Response Actions",
    "Impact Assessment": "Impact Assessment of {hazard}",
    "Terminal Reporting": "Terminal Report on {hazard}"
}

# Family C: Search / Investigation
templates_search = {
    "Monitoring": "Monitoring of {hazard}",
    "Preparedness": "Preparedness Measures for Possible Related Incidents",
    "Incident / Effects Monitoring": "Incident Monitoring and Coordination for {hazard}",
    "Impact Assessment": "Assessment of Effects and Operational Requirements for {hazard}",
    "Terminal Reporting": "Terminal Report on {hazard}"
}

# =============================================================================
# HAZARD LISTS BY CATEGORY
# =============================================================================

# =============================================================================
# HAZARD LISTS BY CATEGORY
# =============================================================================

# Tab 0: Hydrometeorological
hydrometeorological_hazards = {
    "Atmospheric Disturbances": ["🌧️ ITCZ", "🌀 LPA", "💨 Monsoon", "⚡ Shear Line"],
    "Tropical Cyclones": ["⛈️ Thunderstorm", "🌪️ Tropical Depression", "🌪️ Tropical Storm", "🌪️ Severe Tropical Storm"],
    "Typhoons": ["🌪️ Typhoon", "🌪️ Super Typhoon"],
    "Flooding": ["🌊 Riverine Flood", "💧 Flash Flood"],
    "Other Hazards": ["🏜️ Drought", "🔥 Heatwave"]
}

# Tab 1: Geological
geological_hazards = {
    "Earthquake-Related": ["🌋 Earthquake", "🌋 Strong Aftershock", "🌋 Earthquake Swarm"],
    "Ground Movement": ["🏔️ Landslide", "🪨 Rockfall", "⛰️ Debris Flow", "📉 Ground Subsidence"],
    "Volcanic": ["🌋 Volcanic Eruption", "🌫️ Volcanic Ashfall", "💨 Lahar Flow"],
    "Other Geological": ["⚡ Ground Rupture", "💧 Liquefaction", "📈 Slope Movement"]
}

# Tab 2: Fire Incident
fire_hazards = {
    "Structural Fires": ["🏠 Residential House Fire", "🏢 Commercial Building Fire"],
    "Wildfires": ["🌲 Forest Fire", "🌿 Grass Fire", "🔥 Bush Fire"],
    "Other Fires": ["🚗 Vehicle Fire", "⚡ Electrical Fire", "💥 Explosion"]
}

# Tab 3: Technological / Human-Induced
technological_hazards = {
    "Transportation": ["✈️ Aviation Accident", "🚗 Vehicular Accident"],
    "Industrial": ["🏭 Industrial Accident", "☢️ Chemical Spill", "💨 Gas Leak"],
    "Infrastructure": ["🏗️ Infrastructure Collapse", "🌉 Bridge Collapse", "🏢 Building Collapse"],
    "Other": ["💣 Bomb Threat", "📡 Communication Outage", "⚡ Power Grid Failure"]
}

# Tab 4: Public Safety / Security
public_safety_hazards = {
    "Violent Incidents": ["🔫 Shooting Incident", "🔪 Stabbing Incident", "⚔️ Armed Confrontation"],
    "Civil Unrest": ["📢 Riot", "🚫 Barricade", "🏛️ Hostage Situation"],
    "Other Security": ["💰 Robbery", "🏪 Looting", "🚨 Security Threat"]
}

# Tab 5: Health / Medical
health_hazards = {
    "Disease Outbreaks": ["🦠 Disease Outbreak", "🤧 Influenza Outbreak", "🍲 Food Poisoning"],
    "Medical / Trauma": ["📉 Fall Incident", "🔪 Attempted Suicide"],
    "Other Health": ["🧪 Chemical Exposure", "☢️ Radiation Exposure", "🐍 Venomous Bite"]
}

# Tab 6: Lifeline / Service Disruption
lifeline_hazards = {
    "Utilities": ["💡 Power Outage", "💧 Water Shortage", "📡 Communication Outage"],
    "Transportation": ["🚫 Road Closure", "🌉 Bridge Damage", "🚇 Transport Disruption"],
    "Other Services": ["🗑️ Waste Collection Disruption", "🏥 Hospital Overload", "🏫 School Closure"]
}

# Tab 7: Search / Missing Person
search_hazards = {
    "Missing Persons": ["🔍 Missing Person", "👤 Missing Child", "👵 Missing Elderly"],
    "Search and Rescue Operations": ["🏔️ Mountain Search", "🌊 Water Search", "🌲 Forest Search"],
    "Recovery Operations": ["⚰️ Body Recovery", "🚗 Vehicle Recovery", "🏠 Structure Collapse Recovery"]
}

# =============================================================================
# FULL HAZARD NAME MAPPING (Button display to full text)
# =============================================================================

hazard_full_names = {
    # Hydrometeorological
    "🌧️ ITCZ": "Intertropical Convergence Zone (ITCZ)",
    "🌀 LPA": "Low Pressure Area (LPA)",
    "💨 Monsoon": "Monsoon (Southwest/Northeast)",
    "⚡ Shear Line": "Shear Line",
    "⛈️ Thunderstorm": "Severe Thunderstorm",
    "🌪️ Tropical Depression": "Tropical Depression",
    "🌪️ Tropical Storm": "Tropical Storm",
    "🌪️ Severe Tropical Storm": "Severe Tropical Storm",
    "🌪️ Typhoon": "Typhoon",
    "🌪️ Super Typhoon": "Super Typhoon",
    "🌊 Riverine Flood": "Riverine/Fluvial Flood",
    "💧 Flash Flood": "Flash Flood",
    "🏜️ Drought": "Prolonged Drought",
    "🔥 Heatwave": "Extreme Heatwave",
    
    # Geological
    "🌋 Earthquake": "Earthquake",
    "🌋 Strong Aftershock": "Strong Aftershock",
    "🌋 Earthquake Swarm": "Earthquake Swarm",
    "🏔️ Landslide": "Rain-Induced Landslide",
    "🪨 Rockfall": "Rockfall",
    "⛰️ Debris Flow": "Debris Flow",
    "📉 Ground Subsidence": "Ground Subsidence",
    "🌋 Volcanic Eruption": "Volcanic Eruption",
    "🌫️ Volcanic Ashfall": "Volcanic Ashfall",
    "💨 Lahar Flow": "Lahar Flow",
    "⚡ Ground Rupture": "Ground Rupture",
    "💧 Liquefaction": "Liquefaction",
    "📈 Slope Movement": "Slope Movement",
    
    # Fire
    "🏢 Commercial Building Fire": "Commercial Building Fire",
    "🏠 Residential House Fire": "Residential House Fire",
    "🌲 Forest Fire": "Forest Fire",
    "🌿 Grass Fire": "Grass Fire",
    "🔥 Bush Fire": "Bush Fire",
    "🚗 Vehicle Fire": "Vehicle Fire",
    "⚡ Electrical Fire": "Electrical Fire",
    "💥 Explosion": "Explosion",
    
    # Technological
    "✈️ Aviation Accident": "Aviation Accident",
    "🚗 Vehicular Accident": "Vehicular Accident",
    "🏭 Industrial Accident": "Industrial Accident",
    "☢️ Chemical Spill": "Chemical Spill",
    "💨 Gas Leak": "Gas Leak",
    "🏗️ Infrastructure Collapse": "Infrastructure Collapse",
    "🌉 Bridge Collapse": "Bridge Collapse",
    "🏢 Building Collapse": "Building Collapse",
    "💣 Bomb Threat": "Bomb Threat",
    "📡 Communication Outage": "Communication Outage",
    "⚡ Power Grid Failure": "Power Grid Failure",
    
    # Public Safety
    "🔫 Shooting Incident": "Shooting Incident",
    "🔪 Stabbing Incident": "Stabbing Incident",
    "⚔️ Armed Confrontation": "Armed Confrontation",
    "📢 Riot": "Civil Riot",
    "🚫 Barricade": "Barricade Situation",
    "🏛️ Hostage Situation": "Hostage Situation",
    "💰 Robbery": "Armed Robbery",
    "🏪 Looting": "Looting Incident",
    "🚨 Security Threat": "General Security Threat",
    
    # Health
    "🦠 Disease Outbreak": "Disease Outbreak",
    "🤧 Influenza Outbreak": "Influenza Outbreak",
    "🍲 Food Poisoning": "Mass Food Poisoning",
    "📉 Fall Incident": "Fall Incident",
    "🔪 Attempted Suicide": "Attempted Suicide",
    "🧪 Chemical Exposure": "Chemical Exposure",
    "☢️ Radiation Exposure": "Radiation Exposure",
    "🐍 Venomous Bite": "Venomous Animal Bite",
    
    # Lifeline
    "💡 Power Outage": "Widespread Power Outage",
    "💧 Water Shortage": "Water Shortage",
    "📡 Communication Outage": "Telecommunication Outage",
    "🚫 Road Closure": "Major Road Closure",
    "🌉 Bridge Damage": "Bridge Damage",
    "🚇 Transport Disruption": "Public Transport Disruption",
    "🗑️ Waste Collection Disruption": "Waste Collection Disruption",
    "🏥 Hospital Overload": "Hospital Capacity Overload",
    "🏫 School Closure": "Mass School Closure",
    
    # Search
    "🔍 Missing Person": "Missing Person",
    "👤 Missing Child": "Missing Child",
    "👵 Missing Elderly": "Missing Elderly Person",
    "🏔️ Mountain Search": "Mountain Search Operation",
    "🌊 Water Search": "Water Search Operation",
    "🌲 Forest Search": "Forest Search Operation",
    "⚰️ Body Recovery": "Body Recovery Operation",
    "🚗 Vehicle Recovery": "Vehicle Recovery Operation",
    "🏠 Structure Collapse Recovery": "Structure Collapse Recovery"
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def set_hazard(hazard_name):
    st.session_state.selected_hazard = hazard_name

def get_hazard_base(hazard_text):
    """Extract base hazard type for Preparedness phase wording"""
    if "fire" in hazard_text.lower():
        return "Fire"
    elif "accident" in hazard_text.lower():
        return "Accident"
    elif "spill" in hazard_text.lower():
        return "Chemical Spill"
    elif "shooting" in hazard_text.lower():
        return "Shooting"
    elif "stabbing" in hazard_text.lower():
        return "Stabbing"
    elif "outbreak" in hazard_text.lower():
        return "Disease Outbreak"
    else:
        words = hazard_text.split()[:2]
        return " ".join(words)

def generate_title(hazard, phase, location, sitrep_num, wording_family):
    """Generate title based on wording family"""
    if not hazard:
        return None
    
    if wording_family == "slow_onset":
        templates = templates_slow_onset
        title_template = templates.get(phase, "")
        title = title_template.format(hazard=hazard)
        
    elif wording_family == "sudden_onset":
        templates = templates_sudden_onset
        title_template = templates.get(phase, "")
        if phase == "Preparedness":
            hazard_base = get_hazard_base(hazard)
            title = title_template.format(hazard=hazard, hazard_base=hazard_base)
        else:
            title = title_template.format(hazard=hazard)
        
    elif wording_family == "search":
        templates = templates_search
        title_template = templates.get(phase, "")
        title = title_template.format(hazard=hazard)
        
    else:
        title = f"{phase} of {hazard}"
    
    if location:
        title = f"{title} ({location})"
    
    return f"SITREP #{sitrep_num}: {title}"

def display_title_section(wording_family, tab_index):
    """Display the generated title section with unique keys per tab"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("---")
        st.markdown("**📍 Location (Optional):**")
        location = st.text_input(
            "Location",
            value=st.session_state.location,
            placeholder="e.g., Bontoc, Mountain Province",
            key=f"location_input_{tab_index}"  # UNIQUE KEY
        )
        st.session_state.location = location
        
        st.markdown("---")
        st.markdown(f"**Current SITREP #:** {st.session_state.sitrep_num}")
        sitrep_num = st.number_input(
            "SITREP # (editable)",
            min_value=1,
            value=st.session_state.sitrep_num,
            step=1,
            key=f"sitrep_num_input_{tab_index}"  # UNIQUE KEY
        )
        st.session_state.sitrep_num = sitrep_num
    
    with col2:
        st.markdown("### ✅ Generated Title")
        
        if st.session_state.selected_hazard:
            full_title = generate_title(
                st.session_state.selected_hazard,
                st.session_state.selected_phase,
                st.session_state.location,
                st.session_state.sitrep_num,
                wording_family
            )
            
            if full_title:
                st.success(f"## {full_title}")
                
                st.markdown("---")
                st.markdown("### 📊 Title Breakdown")
                st.markdown(f"**SITREP #:** {st.session_state.sitrep_num}")
                st.markdown(f"**Phase:** {st.session_state.selected_phase}")
                st.markdown(f"**Hazard:** {st.session_state.selected_hazard}")
                if st.session_state.location:
                    st.markdown(f"**Location:** {st.session_state.location}")
                
                if st.button("📋 Copy to Clipboard", key=f"copy_btn_{wording_family}_{tab_index}"):
                    st.code(full_title, language="text")
                    st.balloons()
        else:
            st.info("👈 Click a hazard button above to generate a title")

def create_hazard_tab(tab_title, hazard_dict, wording_family, category_description, tab_index):
    """Generic function to create a hazard tab with unique keys"""
    
    with tab_title:
        st.markdown(f"### 📋 {category_description}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Operational Phase Selection with UNIQUE key based on tab_index
            st.markdown("**1. Select Operational Phase:**")
            
            selected_phase = st.radio(
                "Select Phase",
                options=operational_phases,
                index=operational_phases.index(st.session_state.selected_phase) if st.session_state.selected_phase in operational_phases else 0,
                key=f"phase_radio_{wording_family}_{tab_index}",
                horizontal=True
            )
            st.session_state.selected_phase = selected_phase
            
            st.info(f"📖 **When to use:** {phase_descriptions.get(selected_phase, '')}")
            
            st.markdown("---")
            
            # Hazard Selection Buttons
            st.markdown("**2. Select Hazard / Event:**")
            
            for category, hazards in hazard_dict.items():
                st.markdown(f"**{category}:**")
                cols = st.columns(4)
                for idx, hazard_btn in enumerate(hazards):
                    with cols[idx % 4]:
                        if st.button(hazard_btn, key=f"{wording_family}_{tab_index}_{hazard_btn}", use_container_width=True):
                            set_hazard(hazard_full_names.get(hazard_btn, hazard_btn))
                            st.rerun()
            
            # Custom hazard input
            st.markdown("---")
            st.markdown("**Or enter custom hazard:**")
            custom_hazard = st.text_input(
                "Custom Hazard",
                key=f"custom_hazard_{wording_family}_{tab_index}",
                placeholder="e.g., Enter your own hazard description"
            )
            if custom_hazard:
                st.session_state.selected_hazard = custom_hazard
        
        # Display the title section with unique keys
        display_title_section(wording_family, tab_index)

# =============================================================================
# CREATE ALL TABS WITH UNIQUE INDICES
# =============================================================================

tabs = st.tabs([
    "🌊 HYDROMETEOROLOGICAL",
    "🌋 GEOLOGICAL",
    "🔥 FIRE INCIDENT",
    "🏭 TECHNOLOGICAL",
    "🛡️ PUBLIC SAFETY",
    "🏥 HEALTH / MEDICAL",
    "⚡ LIFELINE DISRUPTION",
    "🔍 SEARCH / MISSING"
])

# Tab 0: Hydrometeorological (slow_onset)
with tabs[0]:
    create_hazard_tab(
        tabs[0],
        hydrometeorological_hazards,
        "slow_onset",
        "Hydrometeorological Hazards - Atmospheric, hydrological, and oceanographic hazards",
        0
    )

# Tab 1: Geological (slow_onset)
with tabs[1]:
    create_hazard_tab(
        tabs[1],
        geological_hazards,
        "slow_onset",
        "Geological Hazards - Earthquakes, landslides, volcanic, and other geophysical hazards",
        1
    )

# Tab 2: Fire Incident (sudden_onset)
with tabs[2]:
    create_hazard_tab(
        tabs[2],
        fire_hazards,
        "sudden_onset",
        "Fire Incidents - Structural fires, wildfires, and other fire-related emergencies",
        2
    )

# Tab 3: Technological / Human-Induced (sudden_onset)
with tabs[3]:
    create_hazard_tab(
        tabs[3],
        technological_hazards,
        "sudden_onset",
        "Technological / Human-Induced Incidents - Accidents, infrastructure failures, industrial incidents",
        3
    )

# Tab 4: Public Safety / Security (sudden_onset)
with tabs[4]:
    create_hazard_tab(
        tabs[4],
        public_safety_hazards,
        "sudden_onset",
        "Public Safety / Security Incidents - Violent incidents, civil unrest, security threats",
        4
    )

# Tab 5: Health / Medical (sudden_onset)
with tabs[5]:
    create_hazard_tab(
        tabs[5],
        health_hazards,
        "sudden_onset",
        "Health / Medical Incidents - Disease outbreaks, medical emergencies, mass casualties",
        5
    )

# Tab 6: Lifeline / Service Disruption (slow_onset)
with tabs[6]:
    create_hazard_tab(
        tabs[6],
        lifeline_hazards,
        "slow_onset",
        "Lifeline / Service Disruption - Power, water, communication, transportation disruptions",
        6
    )

# Tab 7: Search / Missing Person (search)
with tabs[7]:
    create_hazard_tab(
        tabs[7],
        search_hazards,
        "search",
        "Search / Missing Person Incidents - Missing persons, search and recovery operations",
        7
    )
# =============================================================================
# RESET BUTTON (Common for all tabs)
# =============================================================================

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 START NEW SITREP", key="reset_button", use_container_width=True):
        st.session_state.sitrep_num = st.session_state.sitrep_num + 1
        st.session_state.selected_hazard = ""
        st.session_state.selected_phase = "Monitoring"
        st.session_state.location = ""
        st.rerun()

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption("✅ Select a hazard category tab, click a hazard button, select a phase, and the title generates automatically.")
st.caption("📌 Click 'START NEW SITREP' to increment SITREP # and clear all fields for a new report.")

# =============================================================================
# REFERENCE EXPANDER
# =============================================================================

with st.expander("📖 Reference: Title Generation Rules by Category", expanded=False):
    st.markdown("""
    ### How Titles Are Generated
    
    | Wording Family | Categories | Title Style |
    |----------------|------------|-------------|
    | **Slow-onset** | Hydrometeorological, Geological, Lifeline Disruption | "Monitoring of...", "Preparedness for the Possible Effects of...", "Monitoring of the Effects of..." |
    | **Sudden-onset** | Fire, Technological, Public Safety, Health/Medical | "Monitoring of...", "Preparedness Measures for Possible...", "Monitoring of ... and Response Actions" |
    | **Search** | Search/Missing Person | "Monitoring of...", "Incident Monitoring and Coordination for...", "Assessment of Effects and Operational Requirements for..." |
    
    ---
    
    ### Example Outputs by Category
    
    | Category | Phase | Hazard | Generated Title |
    |----------|-------|--------|-----------------|
    | Hydrometeorological | Preparedness | Typhoon Uwan | SITREP #1: Preparedness for the Possible Effects of Typhoon Uwan |
    | Geological | Monitoring | Earthquake | SITREP #1: Monitoring of Earthquake |
    | Fire Incident | Incident/Effects Monitoring | Structural Fire | SITREP #1: Monitoring of Structural Fire and Response Actions |
    | Technological | Preparedness | Chemical Spill | SITREP #1: Preparedness Measures for Possible Chemical Spill Incidents |
    | Public Safety | Incident/Effects Monitoring | Shooting Incident | SITREP #1: Incident Monitoring and Coordination for Shooting Incident |
    | Health/Medical | Impact Assessment | Disease Outbreak | SITREP #1: Impact Assessment of Disease Outbreak |
    | Lifeline Disruption | Preparedness | Water Shortage | SITREP #1: Preparedness for the Possible Effects of Water Shortage |
    | Search/Missing | Incident/Effects Monitoring | Missing Person | SITREP #1: Incident Monitoring and Coordination for Missing Person |
    """)