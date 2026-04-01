# tabs/drrm_intelligence.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import os
import json
import base64
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected, auto_sync_table
from utils.local_storage import save_file, delete_file, get_file_size, file_exists
import folium
from streamlit_folium import folium_static
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_number(value, decimals=2):
    """Format number with thousand separators and specified decimals"""
    if value is None or pd.isna(value):
        return "0" + (".00" if decimals > 0 else "")
    try:
        if decimals == 0:
            return f"{int(float(value)):,}"
        else:
            return f"{float(value):,.{decimals}f}"
    except:
        return str(value)


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def calculate_mp_confidence(affected_regions_str):
    """
    Calculate confidence that Mountain Province was affected
    based on which regions are mentioned in historical source data
    """
    if not affected_regions_str or pd.isna(affected_regions_str):
        return {
            'level': 'UNKNOWN',
            'score': 0,
            'reason': 'No region information available',
            'color': '#6c757d'
        }
    
    regions = [r.strip().upper() for r in affected_regions_str.split(',')]
    
    has_car = any('CAR' in r for r in regions)
    has_region1 = any('REGION I' in r or 'REGION 1' in r or 'I' == r or '1' == r for r in regions)
    has_region2 = any('REGION II' in r or 'REGION 2' in r or 'II' == r or '2' == r for r in regions)
    
    if has_car and has_region1 and has_region2:
        return {
            'level': 'VERY HIGH',
            'score': 95,
            'reason': 'Historical record mentions CAR, Region I, and Region II - typhoon surrounded Mountain Province on three sides',
            'color': '#006400'
        }
    elif has_car and (has_region1 or has_region2):
        return {
            'level': 'HIGH',
            'score': 85,
            'reason': f"Historical record mentions CAR and {'Region I' if has_region1 else 'Region II'} - Mountain Province centrally located in CAR",
            'color': '#008000'
        }
    elif has_car:
        return {
            'level': 'MEDIUM',
            'score': 70,
            'reason': 'Historical record directly mentions CAR - Mountain Province is part of CAR',
            'color': '#FFA500'
        }
    elif has_region1 and has_region2:
        return {
            'level': 'MEDIUM-LOW',
            'score': 40,
            'reason': 'Historical record mentions adjacent regions (I and II) only - possible spillover effects to CAR',
            'color': '#FFD700'
        }
    else:
        return {
            'level': 'LOW',
            'score': 20,
            'reason': 'Historical record has no direct or adjacent region mention - uncertain impact on Mountain Province',
            'color': '#FF0000'
        }


def generate_annual_report(df, year):
    """Generate annual report statistics for a given year"""
    yearly_df = df[df['year'] == year]
    
    if yearly_df.empty:
        return None
    
    report = {
        'year': year,
        'total_events': len(yearly_df),
        'events_by_category': yearly_df['hazard_category'].value_counts().to_dict(),
        'events_by_type': yearly_df['hazard_type'].value_counts().to_dict(),
        'total_fatalities': int(yearly_df['fatalities'].sum()),
        'total_injured': int(yearly_df['injured'].sum()),
        'total_missing': int(yearly_df['missing'].sum()),
        'total_houses_damaged': {
            'total': int(yearly_df['houses_total'].sum()),
            'partial': int(yearly_df['houses_partial'].sum())
        },
        'total_damage_cost': float(yearly_df['damage_total'].sum()),
        'affected_municipalities': yearly_df['municipalities'].dropna().unique().tolist(),
        'most_affected_municipality': yearly_df['municipalities'].mode()[0] if not yearly_df['municipalities'].mode().empty else 'Unknown',
        'record_types': yearly_df['record_type'].value_counts().to_dict(),
        'monthly_breakdown': yearly_df.groupby('month').size().to_dict() if 'month' in yearly_df.columns else {}
    }
    
    return report


def display_annual_report(report):
    """Display annual report in a formatted way"""
    st.markdown(f"### 📊 Annual Report: {report['year']}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", format_number(report['total_events'], 0))
    with col2:
        st.metric("Fatalities", format_number(report['total_fatalities'], 0))
    with col3:
        st.metric("Injured", format_number(report['total_injured'], 0))
    with col4:
        st.metric("Missing", format_number(report['total_missing'], 0))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📋 Events by Hazard Category")
        if report['events_by_category']:
            for cat, count in report['events_by_category'].items():
                st.markdown(f"- {cat}: {count}")
        else:
            st.info("No data")
    
    with col2:
        st.markdown("#### 📋 Events by Hazard Type")
        if report['events_by_type']:
            top_types = dict(list(report['events_by_type'].items())[:5])
            for htype, count in top_types.items():
                st.markdown(f"- {htype}: {count}")
        else:
            st.info("No data")
    
    st.markdown("#### 🏠 Housing Damage")
    st.markdown(f"- **Totally Damaged:** {format_number(report['total_houses_damaged']['total'], 0)} houses")
    st.markdown(f"- **Partially Damaged:** {format_number(report['total_houses_damaged']['partial'], 0)} houses")
    st.markdown(f"- **Total Damage Cost:** ₱{format_number(report['total_damage_cost']/1e6, 2)} Million")
    
    st.markdown("#### 🏘️ Most Affected Areas")
    st.markdown(f"- **Most Affected Municipality:** {report['most_affected_municipality']}")
    st.markdown(f"- **Affected Municipalities:** {', '.join(report['affected_municipalities'][:5])}")
    
    if report['monthly_breakdown']:
        st.markdown("#### 📅 Monthly Breakdown")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_counts = [report['monthly_breakdown'].get(m, 0) for m in range(1, 13)]
        fig = px.bar(x=months, y=monthly_counts, title=f"Events by Month - {report['year']}",
                    labels={'x': 'Month', 'y': 'Number of Events'})
        st.plotly_chart(fig, use_container_width=True)


def save_to_local_storage():
    """Save disaster events to local storage"""
    os.makedirs("local_storage/drrm_intelligence", exist_ok=True)
    storage_path = "local_storage/drrm_intelligence/events.json"
    try:
        df = st.session_state.disaster_events
        if not df.empty:
            df_copy = df.copy()
            for col in df_copy.columns:
                if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                    df_copy[col] = df_copy[col].astype(str)
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(df_copy.to_dict('records'), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving events: {e}")


def load_from_local_storage():
    """Load disaster events from local storage"""
    storage_path = "local_storage/drrm_intelligence/events.json"
    if os.path.exists(storage_path):
        try:
            with open(storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data:
                    st.session_state.disaster_events = pd.DataFrame(data)
        except Exception as e:
            print(f"Error loading events: {e}")


# =============================================================================
# MAIN SHOW FUNCTION
# =============================================================================

def show():
    """Display DRRM Intelligence Tab with UNDRR Classification"""
    
    # Professional Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
        <h1 style="color: white; margin: 0; font-size: 2rem;">📊 DRRM INTELLIGENCE</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1rem;">
            This repository of hazard events is more than just a digital database – it is a dynamic, data-driven analytical platform 
            that transforms raw disaster information into actionable intelligence.
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            📈 Descriptive Analytics (what happened) | 🔮 Predictive Analytics (what will happen)
        </p>
        <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Beyond simply storing, retrieving, and updating files, the portal harnesses the power of analytics to uncover patterns, 
            forecast future scenarios, and guide evidence-based decision-making.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'disaster_events' not in st.session_state:
        st.session_state.disaster_events = pd.DataFrame()
    
    # Load existing data
    load_from_local_storage()
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 HAZARD DOCUMENTATION",
        "🔮 PREDICTIVE ANALYTICS",
        "🎯 PROJECTIVE ANALYTICS",
        "📊 EVENT DATABASE",
        "📈 SUMMARY DASHBOARD",
        "📜 HISTORICAL CONTEXT GUIDE"
    ])
    
    with tab1:
        show_hazard_documentation()
    
    with tab2:
        show_predictive_analytics()
    
    with tab3:
        show_projective_analytics()
    
    with tab4:
        show_event_database()
    
    with tab5:
        show_summary_dashboard()
    
    with tab6:
        show_historical_context()


def show_hazard_documentation():
    """Hazard Documentation Form with UNDRR Classification"""
    
    st.markdown("### 📋 Hazard Documentation Form")
    st.markdown("*For annual reporting and statistical analysis*")
    
    # UNDRR Reference Panel
    with st.expander("📖 UNDRR Hazard Classification Reference", expanded=False):
        st.markdown("""
        ### 📚 Hazard Classification System (UNDRR 2025)
        
        | Category | Description | Examples |
        |----------|-------------|----------|
        | 🌡️ **Biological** | Organic origin, conveyed by biological vectors | Bacteria, viruses, parasites, venomous wildlife, poisonous plants |
        | 🌱 **Environmental** | Created by environmental degradation or pollution | Soil degradation, deforestation, loss of biodiversity, salinization, sea-level rise |
        | 🌋 **Geological/Geophysical** | Internal earth processes | Earthquakes, volcanic activity, mass movements (landslides, rockslides, debris flows) |
        | 🌊 **Hydrometeorological** | Atmospheric, hydrological, oceanographic origin | Tropical cyclones (typhoons), floods, droughts, heatwaves, cold spells, thunderstorms, ITCZ, shear line, monsoon |
        | 🏭 **Technological** | Technological/industrial conditions, infrastructure failures | Industrial pollution, nuclear radiation, dam failures, transport accidents, fires, chemical spills |
        
        *Source: United Nations Office for Disaster Risk Reduction (UNDRR)*
        """)
    
    # Two-period selection
    col_period1, col_period2 = st.columns(2)
    with col_period1:
        record_period = st.radio(
            "Select Record Type",
            [
                "🏛️ HISTORICAL (1800-2000) - Needs interpretation",
                "🌍 21st CENTURY (2001-2100) - Direct Mountain Province data"
            ],
            key="record_period_select",
            horizontal=True
        )
    
    with col_period2:
        # UNDRR-based Hazard Category
        hazard_category = st.selectbox(
            "Hazard Category (UNDRR Classification)",
            [
                "🌊 Hydrometeorological - Atmospheric, hydrological, oceanographic origin",
                "🌋 Geological/Geophysical - Internal earth processes",
                "🌡️ Biological - Organic origin, conveyed by biological vectors",
                "🌱 Environmental - Environmental degradation or pollution",
                "🏭 Technological - Technological/industrial conditions, infrastructure failures"
            ],
            key="hazard_category_select",
            help="Classification based on UNDRR 2025 standards"
        )
        
        # Extract short category name for storage
        if "Hydrometeorological" in hazard_category:
            category_short = "Hydrometeorological"
        elif "Geological" in hazard_category:
            category_short = "Geological/Geophysical"
        elif "Biological" in hazard_category:
            category_short = "Biological"
        elif "Environmental" in hazard_category:
            category_short = "Environmental"
        else:
            category_short = "Technological"
    
    st.markdown("---")
    
    # Use form with clear_on_submit=True
    with st.form("unified_hazard_form", clear_on_submit=True):
        st.markdown("#### 📍 Basic Information")
        col1, col2 = st.columns(2)
        
        with col1:
            local_name = st.text_input("Event Name", placeholder="e.g., Typhoon Egay, 1990 Earthquake")
            international_name = st.text_input("International Name (if applicable)")
            
            # Year range based on selected period
            if "HISTORICAL" in record_period:
                min_year, max_year = 1800, 2000
                year = st.number_input("Year", min_value=min_year, max_value=max_year, value=1900, step=1,
                                      help="Enter year of occurrence (1800-2000)")
                record_type = "Historical"
            else:
                min_year, max_year = 2001, 2100
                year = st.number_input("Year", min_value=min_year, max_value=max_year, value=datetime.now().year, step=1,
                                      help="Enter year of occurrence (2001-2100)")
                record_type = "21st Century"
        
        with col2:
            # Hazard Type based on category
            if "Hydrometeorological" in hazard_category:
                hazard_type = st.selectbox("Hazard Type (PAGASA/UNDRR)", [
                    "Intertropical Convergence Zone (ITCZ)",
                    "Low Pressure Area (LPA)",
                    "Monsoon (Southwest/Northeast)",
                    "Shear Line",
                    "Thunderstorm",
                    "Tropical Depression",
                    "Tropical Storm",
                    "Severe Tropical Storm",
                    "Typhoon",
                    "Super Typhoon",
                    "Riverine/Fluvial Flood",
                    "Flash Flood",
                    "Drought",
                    "Heatwave"
                ])
            elif "Geological" in hazard_category:
                hazard_type = st.selectbox("Hazard Type", [
                    "Ground Shaking",
                    "Ground Rupture",
                    "Liquefaction",
                    "Mass Wasting (Landslide)",
                    "Mass Wasting (Rockfall)",
                    "Mass Wasting (Debris Flow)",
                    "Mass Wasting (Creep)",
                    "Volcanic Eruption",
                    "Volcanic Ashfall",
                    "Earthquake"
                ])
            elif "Biological" in hazard_category:
                hazard_type = st.selectbox("Hazard Type", [
                    "Disease Outbreak",
                    "Vector-borne Disease",
                    "Food-borne Illness",
                    "Water-borne Disease",
                    "Venomous Wildlife Incident",
                    "Other Biological Hazard"
                ])
            elif "Environmental" in hazard_category:
                hazard_type = st.selectbox("Hazard Type", [
                    "Soil Degradation",
                    "Deforestation",
                    "Loss of Biodiversity",
                    "Salinization",
                    "Sea-level Rise",
                    "Other Environmental Hazard"
                ])
            else:
                hazard_type = st.selectbox("Hazard Type", [
                    "Structural Fire",
                    "Forest Fire",
                    "Vehicular Accident",
                    "Industrial Accident",
                    "Chemical Spill",
                    "Dam Failure",
                    "Transport Accident",
                    "Other Technological Hazard"
                ])
            
            # Date range with era-based limits
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                min_date = date(min_year, 1, 1)
                max_date = date(max_year, 12, 31)
                start_date = st.date_input("Start Date", value=date(min_year, 1, 1), min_value=min_date, max_value=max_date)
            with col_date2:
                end_date = st.date_input("End Date", value=date(min_year, 1, 1), min_value=min_date, max_value=max_date)
            
            # Extract month for reporting
            month = start_date.month
        
        # ===== INTENSITY SECTION =====
        if "Hydrometeorological" in hazard_category:
            st.markdown("#### 💥 Intensity Parameters")
            col_i1, col_i2, col_i3 = st.columns(3)
            with col_i1:
                max_wind = st.number_input("Max Wind Speed (km/h)", min_value=0, value=0,
                                          help="Maximum sustained wind speed in kilometers per hour")
                max_gust = st.number_input("Max Gust (km/h)", min_value=0, value=0,
                                          help="Maximum wind gust speed")
            with col_i2:
                tcws = st.slider("Max TCWS Signal", 0, 5, 0,
                                help="Tropical Cyclone Warning Signal (1-5)")
                pressure = st.number_input("Min Pressure (hPa)", min_value=0, max_value=1100, value=0,
                                          help="Minimum central pressure in hectopascals")
            with col_i3:
                rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=0.0,
                                          help="Total rainfall in millimeters")
        else:
            max_wind = max_gust = tcws = pressure = rainfall = 0
        
        # ===== IMPACT SECTIONS =====
        st.markdown("#### 💔 Human Impact")
        col_h1, col_h2, col_h3 = st.columns(3)
        with col_h1:
            fatalities = st.number_input("Fatalities", min_value=0, value=0,
                                        help="Number of deaths")
            injured = st.number_input("Injured", min_value=0, value=0,
                                     help="Number of injured persons")
        with col_h2:
            missing = st.number_input("Missing", min_value=0, value=0,
                                     help="Number of persons missing")
            displaced_families = st.number_input("Displaced Families", min_value=0, value=0,
                                                help="Number of families displaced")
        with col_h3:
            displaced_persons = st.number_input("Displaced Persons", min_value=0, value=0,
                                                help="Number of persons displaced")
            evacuated = st.number_input("Evacuated", min_value=0, value=0,
                                       help="Number of persons evacuated")
        
        st.markdown("#### 🏠 Infrastructure Damage")
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            houses_total = st.number_input("Totally Damaged Houses", min_value=0, value=0,
                                          help="Number of houses completely destroyed")
            houses_partial = st.number_input("Partially Damaged Houses", min_value=0, value=0,
                                            help="Number of houses with partial damage")
        with col_inf2:
            affected_barangays = st.number_input("Affected Barangays", min_value=0, value=0,
                                                help="Number of barangays affected")
            roads_affected = st.text_area("Affected Roads", placeholder="List affected roads and sections...",
                                         height=60, help="List roads damaged or blocked")
        
        st.markdown("#### 💰 Economic Damage (in Philippine Pesos)")
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            damage_agriculture = st.number_input("Agriculture Damage (₱)", min_value=0.0, value=0.0, step=1000.0,
                                                help="Damage to crops, livestock, fisheries")
        with col_e2:
            damage_infrastructure = st.number_input("Infrastructure Damage (₱)", min_value=0.0, value=0.0, step=1000.0,
                                                   help="Damage to roads, bridges, public facilities")
        with col_e3:
            damage_private = st.number_input("Private Property Damage (₱)", min_value=0.0, value=0.0, step=1000.0,
                                            help="Damage to private properties and businesses")
            total_damage = damage_agriculture + damage_infrastructure + damage_private
            st.metric("Total Damage (₱)", f"₱{format_number(total_damage, 2)}")
        
        # ===== NARRATIVE SECTION =====
        st.markdown("#### 📝 Narrative / Remarks")
        
        if "HISTORICAL" in record_period:
            st.info("🏛️ **Historical Record:** Enter available information. Use Inference Notes to explain relevance to Mountain Province.")
            
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                historical_source = st.text_input("Source of Record", 
                                                 placeholder="e.g., Spanish Archives, Church Records, PAGASA Early Records")
                historical_context = st.text_area("Historical Context", 
                                                 placeholder="Describe the historical context of this event...",
                                                 height=100)
            
            with col_n2:
                mentioned_regions = st.text_input(
                    "Regions Mentioned in Source",
                    placeholder="e.g., CAR, Region I, Region II, Cagayan, Ilocos",
                    help="Enter all regions mentioned in the original source (comma-separated)"
                )
                
                if mentioned_regions:
                    confidence = calculate_mp_confidence(mentioned_regions)
                    st.markdown(f"""
                    <div style='background-color: {confidence['color']}; padding: 10px; border-radius: 5px; margin-top: 10px;'>
                        <strong style='color: white;'>Confidence: {confidence['level']}</strong><br>
                        <span style='color: white;'>{confidence['reason']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                inference_notes = st.text_area(
                    "Inference Notes for Mountain Province",
                    value="Based on historical accounts of this event affecting Northern Luzon, it likely impacted Mountain Province's mountainous terrain with landslides and flooding.",
                    height=100
                )
            
            narrative = f"""
HISTORICAL RECORD
Source: {historical_source if 'historical_source' in locals() else 'Unknown'}
Historical Context: {historical_context if 'historical_context' in locals() else ''}
Regions Mentioned: {mentioned_regions if 'mentioned_regions' in locals() else ''}

Inference for Mountain Province:
{inference_notes if 'inference_notes' in locals() else ''}
"""
        
        else:
            st.markdown("#### 📝 Event Narrative (from Situation Reports)")
            st.markdown("Fill in the sections below with information from your Terminal Reports")
            
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                event_name_narrative = st.text_input("EVENT NAME", placeholder="e.g., Typhoon Egay")
                
                damages_list = st.text_area(
                    "DAMAGES (list each damage item)", 
                    placeholder="• 20 houses totally damaged\n• 35 houses partially damaged\n• 5 hectares of rice fields damaged\n• 3 bridges destroyed\n• 2 schools damaged",
                    height=120
                )
                
                response_taken = st.text_area(
                    "RESPONSE ACTIONS (what was done)", 
                    placeholder="• 300 families evacuated\n• 500 food packs distributed\n• Clearing operations conducted\n• Emergency shelter established at Bontoc Gym",
                    height=120
                )
            
            with col_n2:
                problems_encountered = st.text_area(
                    "PROBLEMS ENCOUNTERED (challenges faced)", 
                    placeholder="• Roads impassable due to landslides in Bauko\n• No communication signal in Sagada\n• Shortage of supplies in remote barangays\n• Limited evacuation centers",
                    height=120
                )
                
                lessons_learned = st.text_area(
                    "LESSONS LEARNED (key insights)", 
                    placeholder="• Early evacuation proved effective in Bontoc\n• Good coordination between municipal DRRM offices\n• Need for backup communication systems in mountainous areas\n• Community-based early warning systems worked well",
                    height=120
                )
            
            narrative = f"""
EVENT: {event_name_narrative}

DAMAGES:
{damages_list}

RESPONSE ACTIONS:
{response_taken}

PROBLEMS ENCOUNTERED:
{problems_encountered}

LESSONS LEARNED:
{lessons_learned}
"""
        
        # ===== AFFECTED AREAS =====
        st.markdown("#### 🌍 Affected Areas")
        col_a1, col_a2 = st.columns(2)
        with col_a1:
            if "HISTORICAL" in record_period:
                region = st.text_input("Regions Affected", placeholder="e.g., CAR, Region I, Cagayan Valley",
                                      help="Enter all regions mentioned in historical record")
            else:
                region = st.selectbox("Region", ["CAR", "Region I", "Both", "Mountain Province Only", "Other"],
                                     help="Select the primary region affected")
                if region == "Other":
                    other_region = st.text_input("Specify other region")
        
        with col_a2:
            municipalities = st.text_input("Municipalities Affected", placeholder="e.g., Bontoc, Sagada, Bauko (comma-separated)",
                                          help="Enter municipalities affected, separated by commas")
        
        # Build affected regions string for confidence (historical only)
        if "HISTORICAL" in record_period:
            affected_regions_str = region if 'region' in locals() else ''
        else:
            affected_regions_str = region
            if region == "Both":
                affected_regions_str = "CAR, Region I"
            elif region == "Other" and 'other_region' in locals():
                affected_regions_str = other_region
        
        # ===== FILE ATTACHMENT =====
        st.markdown("#### 📎 Attachment")
        uploaded_file = st.file_uploader("Upload document or photo", type=['jpg', 'png', 'pdf', 'docx'])
        
        # ===== SUBMIT BUTTON =====
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b2:
            submitted = st.form_submit_button("➕ ADD TO DATABASE", type="primary")
        
        if submitted and local_name:
            # Calculate confidence for historical records
            if "HISTORICAL" in record_period and affected_regions_str:
                confidence = calculate_mp_confidence(affected_regions_str)
            else:
                confidence = {
                    'level': 'DIRECT DATA',
                    'score': 100,
                    'reason': 'Direct Mountain Province record - no inference needed',
                    'color': '#1E3A8A'
                }
            
            event_id = f"{record_type[:3].upper()}-{len(st.session_state.disaster_events)+1:04d}"
            
            new_event = {
                'event_id': event_id,
                'local_name': local_name,
                'international_name': international_name,
                'year': year,
                'month': month,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'hazard_category': category_short,
                'hazard_type': hazard_type,
                'max_tcws': tcws,
                'max_wind_kmh': max_wind,
                'max_gust_kmh': max_gust,
                'min_pressure': pressure,
                'rainfall_mm': rainfall,
                'fatalities': fatalities,
                'injured': injured,
                'missing': missing,
                'displaced_families': displaced_families,
                'displaced_persons': displaced_persons,
                'evacuated': evacuated,
                'houses_total': houses_total,
                'houses_partial': houses_partial,
                'affected_barangays': affected_barangays,
                'roads_affected': roads_affected,
                'damage_agriculture': damage_agriculture,
                'damage_infrastructure': damage_infrastructure,
                'damage_private': damage_private,
                'damage_total': total_damage,
                'region': region if 'region' in locals() else '',
                'municipalities': municipalities,
                'affected_regions_mentioned': affected_regions_str,
                'mp_confidence_level': confidence['level'],
                'mp_confidence_score': confidence['score'],
                'mp_confidence_reason': confidence['reason'],
                'narrative': narrative,
                'data_source': 'Unified Form',
                'record_type': record_type,
                'validated': True,
                'date_added': datetime.now().date().strftime('%Y-%m-%d')
            }
            
            # Handle file upload
            if uploaded_file:
                folder = f"local_storage/drrm_intelligence/events/{event_id}"
                os.makedirs(folder, exist_ok=True)
                file_path = os.path.join(folder, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                new_event["attachment"] = file_path
                new_event["attachment_name"] = uploaded_file.name
            
            # Add to session state
            new_df = pd.DataFrame([new_event])
            if st.session_state.disaster_events.empty:
                st.session_state.disaster_events = new_df
            else:
                st.session_state.disaster_events = pd.concat([st.session_state.disaster_events, new_df], ignore_index=True)
            
            # Save to local storage
            save_to_local_storage()
            
            if "HISTORICAL" in record_period:
                st.success(f"✅ Historical event added with {confidence['level']} confidence for Mountain Province impact!")
            else:
                st.success(f"✅ 21st Century event added to database!")
            st.balloons()
            st.rerun()
        
        elif submitted and not local_name:
            st.error("Please enter the event name")


def show_predictive_analytics():
    """Predictive Analytics with confidence-weighted predictions"""
    
    st.markdown("### 🔮 Predictive Analytics")
    st.markdown("*Confidence-weighted predictions for annual planning*")
    
    df = st.session_state.disaster_events
    
    if df.empty or len(df) < 5:
        st.warning(f"Need at least 5 events for predictions. Currently have {len(df)} events.")
        return
    
    st.success(f"Ready for predictions with {len(df)} events in database")
    
    with st.expander("ℹ️ How predictions are calculated", expanded=False):
        st.markdown("""
        **Confidence-Weighted Predictions**
        
        - **21st Century records (2001+)**: 100% weight - direct measurements
        - **Historical records (1800-2000)**: Weighted by confidence score
          - VERY HIGH confidence: 95% weight
          - HIGH confidence: 85% weight
          - MEDIUM confidence: 70% weight
          - MEDIUM-LOW confidence: 40% weight
          - LOW confidence: 20% weight
        
        This ensures our predictions are based on the most reliable data while still
        leveraging valuable historical information.
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📈 Risk Forecast")
        
        if 'mp_confidence_score' in df.columns:
            weighted_fatalities = (df['fatalities'] * df['mp_confidence_score'] / 100).sum()
            weighted_damage = (df['damage_total'] * df['mp_confidence_score'] / 100).sum()
            
            max_fatalities = df['fatalities'].max() if df['fatalities'].max() > 0 else 1
            max_damage = df['damage_total'].max() if df['damage_total'].max() > 0 else 1
            
            risk_score = min(95, int((weighted_fatalities/max_fatalities * 0.5 + weighted_damage/max_damage * 0.5) * 100))
        else:
            risk_score = min(85, 50 + len(df) * 2)
        
        st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <div style='font-size: 3rem; font-weight: bold; color: #dc3545;'>{risk_score}%</div>
            <div style='background-color: #f0f0f0; height: 20px; border-radius: 10px; margin: 10px 0;'>
                <div style='width: {risk_score}%; background-color: #dc3545; height: 20px; border-radius: 10px;'></div>
            </div>
            <p>Probability of significant weather event (confidence-weighted)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📊 Trend Analysis")
        
        if 'mp_confidence_score' in df.columns:
            yearly_weighted = df.groupby('year').apply(
                lambda x: (x['mp_confidence_score'] * x['fatalities']).sum() / x['mp_confidence_score'].sum()
                if x['mp_confidence_score'].sum() > 0 else 0
            ).reset_index(name='weighted_impact')
            
            fig = px.line(yearly_weighted, x='year', y='weighted_impact', 
                         markers=True, title="Confidence-Weighted Impact Trend")
            st.plotly_chart(fig, use_container_width=True)
        else:
            year_counts = df['year'].value_counts().sort_index().reset_index()
            year_counts.columns = ['Year', 'Count']
            fig = px.line(year_counts, x='Year', y='Count', markers=True, title="Event Frequency Trend")
            st.plotly_chart(fig, use_container_width=True)


def show_projective_analytics():
    """Projective Analytics for scenario planning"""
    
    st.markdown("### 🎯 Projective Analytics")
    st.markdown("*Scenario planning for future events*")
    
    df = st.session_state.disaster_events
    
    st.info("Projective Analytics - Coming Soon")
    
    if len(df) >= 5:
        st.markdown("#### 🌪️ Scenario Planning")
        scenario = st.radio("Choose Scenario", [
            "Typhoon (150 km/h) hitting Bontoc",
            "Flood (2m water level) in Sagada",
            "Earthquake (Magnitude 6.5) in Mountain Province",
            "Landslide in Bauko during wet season"
        ])
        
        if st.button("Run Scenario Analysis"):
            st.info(f"Analyzing: {scenario}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Est. Damage", "₱45.2M")
            with col2:
                st.metric("Affected Pop.", "3,800")
            with col3:
                st.metric("Response Needed", "Critical")


def show_event_database():
    """Event database with search and filters"""
    
    st.markdown("### 📊 Event Database")
    st.markdown("*Queryable database for report generation*")
    
    df = st.session_state.disaster_events
    
    if df.empty:
        st.info("No events in database. Use the Hazard Documentation tab to add events.")
        return
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by name...")
    with col2:
        years = sorted(df['year'].unique())
        year_filter = st.multiselect("Filter by Year", years, default=[])
    with col3:
        if 'hazard_category' in df.columns:
            categories = df['hazard_category'].unique()
            category_filter = st.multiselect("Filter by Category", categories, default=[])
        else:
            category_filter = []
    with col4:
        if 'record_type' in df.columns:
            record_types = df['record_type'].unique()
            type_filter = st.multiselect("Filter by Record Type", record_types, default=[])
        else:
            type_filter = []
    
    filtered_df = df.copy()
    
    if search:
        filtered_df = filtered_df[filtered_df['local_name'].str.contains(search, case=False, na=False) | 
                                  filtered_df['international_name'].str.contains(search, case=False, na=False)]
    if year_filter:
        filtered_df = filtered_df[filtered_df['year'].isin(year_filter)]
    if category_filter and 'hazard_category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['hazard_category'].isin(category_filter)]
    if type_filter and 'record_type' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['record_type'].isin(type_filter)]
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} events**")
    
    # Export button
    if st.button("📥 Export to CSV", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"disaster_events_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Display events
    for idx, event in filtered_df.iterrows():
        display_name = event.get('local_name', 'Unknown')
        if pd.isna(display_name) or display_name == '':
            display_name = 'Unnamed Event'
        
        record_type = event.get('record_type', 'Unknown')
        if record_type == 'Historical':
            header_color = '#8B4513'
            confidence = event.get('mp_confidence_level', 'UNKNOWN')
        else:
            header_color = '#1E3A8A'
            confidence = 'DIRECT DATA'
        
        with st.expander(f"**{display_name}** ({event.get('year', '')}) - {event.get('hazard_type', 'Unknown')}"):
            st.markdown(f"""
            <div style='background-color: {header_color}; padding: 5px 10px; border-radius: 5px; margin-bottom: 10px;'>
                <span style='color: white; font-weight: bold;'>{record_type.upper()} RECORD</span>
                <span style='color: white; float: right;'>Year: {event.get('year', '')}</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**📊 Impact**")
                st.markdown(f"Fatalities: {format_number(event.get('fatalities', 0), 0)}")
                st.markdown(f"Injured: {format_number(event.get('injured', 0), 0)}")
                st.markdown(f"Missing: {format_number(event.get('missing', 0), 0)}")
            with col2:
                st.markdown("**🏠 Housing**")
                st.markdown(f"Totally Damaged: {format_number(event.get('houses_total', 0), 0)}")
                st.markdown(f"Partially Damaged: {format_number(event.get('houses_partial', 0), 0)}")
            with col3:
                st.markdown("**💰 Damage (₱M)**")
                total = event.get('damage_total', 0) / 1_000_000
                st.markdown(f"Total: ₱{format_number(total, 2)}M")
            
            if event.get('narrative') and not pd.isna(event.get('narrative')):
                preview = event.get('narrative')[:150] + '...' if len(event.get('narrative', '')) > 150 else event.get('narrative')
                st.markdown(f"**📝 Narrative:** {preview}")
            
            # Show attachment if exists
            if event.get('attachment') and os.path.exists(event.get('attachment')):
                with open(event.get('attachment'), "rb") as f:
                    st.download_button(
                        label="📎 Download Attachment",
                        data=f,
                        file_name=event.get('attachment_name', 'attachment'),
                        key=f"download_{event.get('event_id')}"
                    )


def show_summary_dashboard():
    """Summary dashboard with annual report generator"""
    
    st.markdown("### 📈 Summary Dashboard")
    st.markdown("*Statistical overview for annual reporting*")
    
    df = st.session_state.disaster_events
    
    if df.empty:
        st.info("Add events to see summary statistics.")
        return
    
    # Record type filter
    if 'record_type' in df.columns:
        selected_types = st.multiselect(
            "Filter by Record Type",
            options=df['record_type'].unique(),
            default=df['record_type'].unique(),
            key="dashboard_type_filter"
        )
        df = df[df['record_type'].isin(selected_types)]
    
    # Summary metrics with formatted numbers
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", format_number(len(df), 0))
    with col2:
        st.metric("Total Fatalities", format_number(int(df['fatalities'].sum()), 0))
    with col3:
        st.metric("Totally Damaged", format_number(int(df['houses_total'].sum()), 0))
    with col4:
        st.metric("Total Damage (₱M)", f"₱{format_number(df['damage_total'].sum()/1e6, 2)}M")
    
    # Annual Report Generator
    st.markdown("---")
    st.markdown("### 📊 Annual Report Generator")
    
    col_yr1, col_yr2 = st.columns(2)
    with col_yr1:
        available_years = sorted(df['year'].unique())
        report_year = st.selectbox("Select Year for Annual Report", available_years, key="report_year_select")
    
    with col_yr2:
        if st.button("📄 Generate Annual Report", use_container_width=True, key="gen_report_btn"):
            report = generate_annual_report(df, report_year)
            if report:
                display_annual_report(report)
                
                # Download button for report
                report_df = df[df['year'] == report_year]
                csv = report_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Report as CSV",
                    data=csv,
                    file_name=f"annual_report_{report_year}.csv",
                    mime="text/csv"
                )
            else:
                st.warning(f"No data found for year {report_year}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    with col1:
        if 'hazard_category' in df.columns:
            type_counts = df['hazard_category'].value_counts().reset_index()
            type_counts.columns = ['Hazard Category', 'Count']
            fig = px.pie(type_counts, values='Count', names='Hazard Category', 
                        title="Events by Hazard Category (UNDRR)")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        year_counts = df['year'].value_counts().sort_index().reset_index()
        year_counts.columns = ['Year', 'Count']
        fig = px.bar(year_counts, x='Year', y='Count', title="Events by Year")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if 'hazard_type' in df.columns:
            top_types = df['hazard_type'].value_counts().head(8).reset_index()
            top_types.columns = ['Hazard Type', 'Count']
            fig = px.bar(top_types, x='Hazard Type', y='Count', title="Top 8 Hazard Types")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'record_type' in df.columns and 'year' in df.columns:
            yearly_counts = df.groupby(['year', 'record_type']).size().reset_index(name='count')
            fig = px.bar(yearly_counts, x='year', y='count', color='record_type',
                        title="Historical vs 21st Century Records Over Time",
                        color_discrete_map={'Historical': '#8B4513', '21st Century': '#1E3A8A'},
                        barmode='stack')
            st.plotly_chart(fig, use_container_width=True)


def show_historical_context():
    """Historical context guide"""
    
    st.markdown("### 📜 Understanding Historical Records")
    
    st.markdown("""
    <div style='background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%); 
                padding: 20px; border-radius: 10px; margin-bottom: 20px; color: white;'>
        <h3 style='color: #FFD700;'>How We Interpret Historical Records (1800-2000)</h3>
        <p>This guide explains how we determine whether historical records likely affected Mountain Province.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🌏 Geographic Reality
        
        **Mountain Province is centrally located in the Cordillera Administrative Region (CAR)**,
        bordered by:
        - **Region I (Ilocos)** to the west
        - **Region II (Cagayan Valley)** to the east
        
        Typhoons that affect CAR and its adjacent regions almost certainly impacted Mountain Province
        due to:
        - Large storm diameters
        - Orographic rainfall enhancement (mountains = more rain)
        - Landslide triggers on steep slopes
        - River flooding from headwaters
        """)
        
        st.markdown("""
        #### 📊 Confidence Scoring System
        
        <div style='background-color: #006400; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>VERY HIGH (95%)</strong> - CAR + Region I + Region II mentioned<br>
            <small>Typhoon surrounded Mountain Province on three sides</small>
        </div>
        
        <div style='background-color: #008000; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>HIGH (85%)</strong> - CAR + (Region I or Region II)<br>
            <small>CAR plus adjacent region - Mountain Province centrally located</small>
        </div>
        
        <div style='background-color: #FFA500; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>MEDIUM (70%)</strong> - CAR only<br>
            <small>Direct CAR mention - Mountain Province is part of CAR</small>
        </div>
        
        <div style='background-color: #FFD700; padding: 10px; border-radius: 5px; margin: 5px 0; color: black;'>
            <strong>MEDIUM-LOW (40%)</strong> - Region I + II only (no CAR)<br>
            <small>Adjacent regions only - possible spillover effects</small>
        </div>
        
        <div style='background-color: #FF0000; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>LOW (20%)</strong> - Single region only<br>
            <small>Too distant for certainty without additional evidence</small>
        </div>
        
        <div style='background-color: #1E3A8A; padding: 10px; border-radius: 5px; margin: 5px 0; color: white;'>
            <strong>DIRECT DATA (100%)</strong> - 21st Century records (2001+)<br>
            <small>Direct Mountain Province measurements - no inference needed</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        #### 📝 Best Practices for Historical Data Entry
        
        **When entering historical records:**
        
        1. **Record the exact regions mentioned** in the source document
        2. **Document your reasoning** in the Inference Notes field
        3. **Note any uncertainties** about the original data
        4. **Include source information** (archives, references, etc.)
        
        #### 💡 Example Entry
        
        **Source:** Spanish Colonial Archive, 1894
        **Regions Mentioned:** "Cagayan, Ilocos, Montañosa"
        **Inference:** "Montañosa refers to the mountainous interior, including present-day Mountain Province. The typhoon affected all surrounding lowlands, so Mountain Province would have experienced significant orographic rainfall and landslides."
        **Confidence:** HIGH
        
        #### 🔍 Research Notes
        
        > *"Region-wide records for CAR from 1967–1999 indicate significant storm-related impacts across the region, even when provincial reporting was not consistently disaggregated. While attribution to Mountain Province is not always direct, the regional pattern of landslide-driven road closures, riverine flooding on valley floors, and recurrent damage to public facilities matches what our local terrain would predict."*
        """)
        
        st.markdown("""
        #### 📊 Quick Reference Table
        
        | Regions Mentioned | Confidence | Weight |
        |------------------|------------|--------|
        | CAR + I + II | VERY HIGH | 95% |
        | CAR + I or CAR + II | HIGH | 85% |
        | CAR only | MEDIUM | 70% |
        | I + II only | MEDIUM-LOW | 40% |
        | Single region | LOW | 20% |
        | 21st Century data | DIRECT | 100% |
        """)