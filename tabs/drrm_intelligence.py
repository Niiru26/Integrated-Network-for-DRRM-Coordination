"""
DRRM Intelligence Tab
Complete working version with Hazard Documentation, Predictive Analytics,
Event Database, Summary Dashboard, and Historical Context Guide
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import hashlib
from utils.database import add_event, load_events_from_supabase, save_events

def show():
    """Display DRRM Intelligence tab"""
    
    # Load data from Supabase into session state if needed
    if 'disaster_events' not in st.session_state or st.session_state.disaster_events.empty:
        st.session_state.disaster_events = load_events_from_supabase()
    
    # Helper function for confidence calculation
    def calculate_mp_confidence(affected_regions_str):
        if not affected_regions_str:
            return {'level': 'UNKNOWN', 'score': 0, 'reason': 'No region information', 'color': '#6c757d'}
        
        regions = [r.strip().upper() for r in affected_regions_str.split(',')]
        has_car = any('CAR' in r for r in regions)
        has_r1 = any('REGION I' in r or 'I' == r or '1' == r for r in regions)
        has_r2 = any('REGION II' in r or 'II' == r or '2' == r for r in regions)
        
        if has_car and has_r1 and has_r2:
            return {'level': 'VERY HIGH', 'score': 95, 'reason': 'CAR + Region I + Region II - surrounded MP', 'color': '#006400'}
        elif has_car and (has_r1 or has_r2):
            return {'level': 'HIGH', 'score': 85, 'reason': 'CAR + adjacent region - MP centrally located', 'color': '#008000'}
        elif has_car:
            return {'level': 'MEDIUM', 'score': 70, 'reason': 'CAR mentioned - MP is part of CAR', 'color': '#FFA500'}
        elif has_r1 and has_r2:
            return {'level': 'MEDIUM-LOW', 'score': 40, 'reason': 'Adjacent regions only - possible spillover', 'color': '#FFD700'}
        else:
            return {'level': 'LOW', 'score': 20, 'reason': 'No direct region mention', 'color': '#FF0000'}
    
    st.header("📊 DRRM INTELLIGENCE")
    
    # =========================================================================
    # CREATE TABS FIRST - MUST BE DEFINED BEFORE USING
    # =========================================================================
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 HAZARD DOCUMENTATION",
        "🔮 PREDICTIVE ANALYTICS",
        "🎯 PROJECTIVE ANALYTICS",
        "📊 EVENT DATABASE",
        "📈 SUMMARY DASHBOARD",
        "📜 HISTORICAL CONTEXT GUIDE"
    ])
    
    # =========================================================================
    # TAB 1: HAZARD DOCUMENTATION
    # =========================================================================
    with tab1:
        st.markdown("### Hazard Documentation Form")
        st.markdown("*For annual reporting and statistical analysis*")
        
        # UNDRR Reference
        with st.expander("📖 Hazard Classification System (UNDRR, 2017)", expanded=False):
            st.markdown("""
            ### 📚 Hazard Classification System (UNDRR, 2017)
            
            | Category | Description | Examples |
            |----------|-------------|----------|
            | 🌡️ **Biological** | Organic origin, conveyed by biological vectors | Bacteria, viruses, parasites, venomous wildlife, poisonous plants |
            | 🌱 **Environmental** | Created by environmental degradation or pollution | Soil degradation, deforestation, loss of biodiversity, salinization, sea-level rise |
            | 🌋 **Geological/Geophysical** | Internal earth processes | Earthquakes, volcanic activity, mass movements (landslides, rockslides, debris flows) |
            | 🌊 **Hydrometeorological** | Atmospheric, hydrological, oceanographic origin | Tropical cyclones (typhoons), floods, droughts, heatwaves, cold spells, storm surges |
            | 🏭 **Technological** | Technological/industrial conditions, infrastructure failures | Industrial pollution, nuclear radiation, dam failures, transport accidents, fires, chemical spills |
            
            *Source: United Nations Office for Disaster Risk Reduction (UNDRR). 2017. The Sendai Framework Terminology on Disaster Risk Reduction. "Hazard". https://www.undrr.org/terminology/hazard.*
            """)
        
        # Record type selection
        col1, col2 = st.columns(2)
        with col1:
            record_period = st.radio(
                "Select Record Type",
                ["🏛️ HISTORICAL - Needs interpretation", "🏔️ PROVINCIAL - Direct Mountain Province data"],
                horizontal=True,
                key="record_period_radio"
            )
        
        with col2:
            hazard_category = st.selectbox(
                "Hazard Category (UNDRR Classification)",
                ["Hydrometeorological", "Geological/Geophysical", "Biological", "Environmental", "Technological"],
                key="hazard_category_select"
            )
        
        st.markdown("---")
        
        # Form key based on selections
        form_key = f"hazard_form_{record_period[:5]}_{hazard_category[:5]}"
        
        with st.form(form_key):
            st.markdown("#### 📍 Basic Information")
            
            col_a, col_b = st.columns(2)
            with col_a:
                local_name = st.text_input("Event Name", placeholder="e.g., Lawin, 1990 Luzon Earthquake", value="")
                international_name = st.text_input("International Name (if applicable)", value="")
                year = st.number_input("Year", min_value=1800, max_value=2100, value=datetime.now().year)
            
            with col_b:
                # Hazard Type based on category
                if hazard_category == "Hydrometeorological":
                    hazard_type = st.selectbox("Hazard Type", [
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
                        "Heatwave",
                        "Forest Fire / Wildfire"
                    ])
                elif hazard_category == "Geological/Geophysical":
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
                elif hazard_category == "Biological":
                    hazard_type = st.selectbox("Hazard Type", [
                        "Disease Outbreak",
                        "Vector-borne Disease",
                        "Food-borne Illness",
                        "Water-borne Disease",
                        "Venomous Wildlife Incident",
                        "Other Biological Hazard"
                    ])
                elif hazard_category == "Environmental":
                    hazard_type = st.selectbox("Hazard Type", [
                        "Soil Degradation",
                        "Deforestation",
                        "Loss of Biodiversity",
                        "Salinization",
                        "Sea-level Rise",
                        "Other Environmental Hazard"
                    ])
                else:  # Technological
                    hazard_type = st.selectbox("Hazard Type", [
                        "Structural Fire",
                        "Forest Fire / Wildfire",
                        "Road Crash Incident",
                        "Vehicular Crash Incident",
                        "Industrial Accident",
                        "Chemical Spill",
                        "Dam Failure",
                        "Transport Incident",
                        "Other Technological Hazard"
                    ])
                
                # Date range
                min_date = date(1800, 1, 1)
                max_date = date(2100, 12, 31)
                
                st.markdown("##### 📅 Event Period")
                col_date1, col_date2 = st.columns(2)
                with col_date1:
                    start_date = st.date_input(
                        "Start Date", 
                        value=datetime.now().date(),
                        min_value=min_date,
                        max_value=max_date,
                        help="When did the event begin? (1800-2100)"
                    )
                with col_date2:
                    end_date = st.date_input(
                        "End Date", 
                        value=datetime.now().date(),
                        min_value=min_date,
                        max_value=max_date,
                        help="When did the event end? (1800-2100)"
                    )
            
            # Duration
            duration_days = (end_date - start_date).days
            if duration_days >= 0:
                st.caption(f"📅 Duration: {duration_days} day(s)")
            else:
                st.warning("End date should be after start date")
            
            # ===== INTENSITY SECTION =====
            if "Hydrometeorological" in hazard_category:
                st.markdown("#### 💥 Intensity Parameters")
                col_i1, col_i2, col_i3 = st.columns(3)
                with col_i1:
                    max_wind = st.number_input("Max Wind Speed (km/h)", min_value=0, value=0)
                    max_gust = st.number_input("Max Gust (km/h)", min_value=0, value=0)
                with col_i2:
                    tcws = st.slider("Max TCWS Signal", 0, 5, 0, help="Tropical Cyclone Warning Signal (1-5)")
                    pressure = st.number_input("Min Pressure (hPa)", min_value=0, max_value=1100, value=0)
                with col_i3:
                    rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=0.0)
            elif "Geological" in hazard_category:
                st.markdown("#### 📊 Seismic/Geological Details")
                col_s1, col_s2 = st.columns(2)
                with col_s1:
                    magnitude = st.number_input("Magnitude", min_value=0.0, max_value=10.0, value=0.0, step=0.1)
                    depth = st.number_input("Depth (km)", min_value=0.0, value=0.0)
                with col_s2:
                    epicenter = st.text_input("Epicenter Location")
                    intensity = st.text_input("Reported Intensity")
            
            # ===== HUMAN IMPACT =====
            st.markdown("#### 💔 Human Impact")
            col_h1, col_h2, col_h3 = st.columns(3)
            with col_h1:
                fatalities = st.number_input("Fatalities", min_value=0, value=0)
                injured = st.number_input("Injured", min_value=0, value=0)
            with col_h2:
                missing = st.number_input("Missing", min_value=0, value=0)
                displaced = st.number_input("Displaced Persons", min_value=0, value=0)
            with col_h3:
                evacuated = st.number_input("Evacuated", min_value=0, value=0)
            
            # ===== INFRASTRUCTURE DAMAGE =====
            st.markdown("#### 🏠 Infrastructure Damage")
            col_inf1, col_inf2 = st.columns(2)
            with col_inf1:
                houses_total = st.number_input("Totally Damaged Houses", min_value=0, value=0)
                houses_partial = st.number_input("Partially Damaged Houses", min_value=0, value=0)
            with col_inf2:
                affected_barangays = st.number_input("Affected Barangays", min_value=0, value=0, help="Number of barangays affected")
                roads_affected = st.text_area("Affected Roads", placeholder="List affected roads and sections...", height=60)
            
            # ===== ECONOMIC DAMAGE =====
            st.markdown("#### 💰 Economic Damage")
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                damage_agri = st.number_input("Agriculture Damage (₱)", min_value=0.0, value=0.0, step=10000.0)
            with col_e2:
                damage_infra = st.number_input("Infrastructure Damage (₱)", min_value=0.0, value=0.0, step=10000.0)
            total_damage = damage_agri + damage_infra
            
            # ===== SOURCE REFERENCE =====
            st.markdown("#### 📚 Source Information")
            source_reference = st.text_input(
                "Source Reference",
                placeholder="e.g., PAGASA Report, NDRRMC SitRep, Spanish Archives, MDRRMO Report",
                help="Where did this information come from?"
            )
            
            # ===== REMARKS =====
            st.markdown("#### 📝 Remarks")
            remarks = st.text_area("Additional Remarks", placeholder="Enter any additional information...", height=100, value="")
            
            # ===== AFFECTED AREAS =====
            st.markdown("#### 🌍 Affected Areas")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                region = st.selectbox("Region", ["CAR", "Region I", "Both", "Mountain Province Only", "Other"])
                if region == "Other":
                    other_region = st.text_input("Specify other region", value="")
            with col_a2:
                municipalities = st.text_input("Municipalities Affected", placeholder="e.g., Bontoc, Sagada, Bauko", value="")
            
            # ===== HISTORICAL CONFIDENCE =====
            mentioned_regions = ""
            if "HISTORICAL" in record_period:
                st.markdown("#### 📊 Historical Record Confidence")
                mentioned_regions = st.text_input("Regions Mentioned in Source", placeholder="e.g., CAR, Region I, Region II", value="")
                if mentioned_regions:
                    confidence_preview = calculate_mp_confidence(mentioned_regions)
                    st.markdown(f"""
                    <div style='background-color: {confidence_preview["color"]}; padding: 10px; border-radius: 5px;'>
                        <strong style='color: white;'>Confidence: {confidence_preview["level"]}</strong><br>
                        <span style='color: white;'>{confidence_preview["reason"]}</span>
                    </div>
                    """, unsafe_allow_html=True)
            
            # ===== AI PROCESSING (Optional) =====
            with st.expander("🤖 AI Processing (Optional)", expanded=False):
                ai_summary = st.text_area(
                    "AI Summary",
                    placeholder="AI-generated summary will appear here",
                    height=100,
                    value=""
                )
                ai_processed = st.checkbox("AI Processed", value=False)
                ai_processing_notes = st.text_area(
                    "AI Processing Notes",
                    placeholder="Notes about AI processing...",
                    height=80,
                    value=""
                )
            
            # ===== SUBMIT BUTTON =====
            submitted = st.form_submit_button("➕ ADD TO DATABASE", width='stretch')
            
            if submitted and local_name:
                if end_date < start_date:
                    st.error("End date cannot be before start date. Please correct the dates.")
                else:
                    final_region = other_region if region == "Other" and 'other_region' in locals() else region
                    
                    if "HISTORICAL" in record_period:
                        if mentioned_regions:
                            confidence = calculate_mp_confidence(mentioned_regions)
                        else:
                            confidence = {'level': 'UNKNOWN', 'score': 0, 'reason': 'No region information', 'color': '#6c757d'}
                    else:
                        confidence = {'level': 'DIRECT DATA', 'score': 100, 'reason': 'Direct MP record', 'color': '#1E3A8A'}
                    
                    # Create unique ID
                    unique_str = f"{local_name}_{year}_{start_date}_{end_date}_{datetime.now().timestamp()}"
                    event_id = f"{'HIS' if 'HISTORICAL' in record_period else 'PRO'}{hashlib.md5(unique_str.encode()).hexdigest()[:8]}"
                    
                    # Map to database column names
                    new_event = {
                        'id': event_id,
                        'local_name': local_name,
                        'international_name': international_name,
                        'year': year,
                        'start_date': start_date.strftime('%Y-%m-%d'),
                        'end_date': end_date.strftime('%Y-%m-%d'),
                        'duration_days': duration_days,
                        'hazard_category': hazard_category,
                        'hazard_type_id': hazard_type,
                        'tcws_signal': tcws if 'tcws' in locals() else 0,
                        'affected_barangays_count': affected_barangays,
                        'casualties_dead': fatalities,
                        'casualties_injured': injured,
                        'casualties_missing': missing,
                        'displaced_persons': displaced if 'displaced' in locals() else 0,
                        'evacuated': evacuated if 'evacuated' in locals() else 0,
                        'houses_total': houses_total,
                        'houses_partial': houses_partial,
                        'damage_agriculture': damage_agri,
                        'damage_infrastructure': damage_infra,
                        'damage_total': total_damage,
                        'region': final_region,
                        'municipalities': municipalities,
                        'source_reference': source_reference,
                        'raw_remarks': remarks,
                        'mentioned_regions': mentioned_regions,
                        'mp_confidence_level': confidence['level'],
                        'mp_confidence_score': confidence['score'],
                        'record_type': "Historical" if "HISTORICAL" in record_period else "Provincial",
                        'ai_summary': ai_summary if 'ai_summary' in locals() else '',
                        'ai_processed': ai_processed if 'ai_processed' in locals() else False,
                        'ai_processing_notes': ai_processing_notes if 'ai_processing_notes' in locals() else '',
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'created_by': 'INDC_App'
                    }
                    
                    # Check for duplicate
                    existing_names = st.session_state.disaster_events['local_name'].tolist() if not st.session_state.disaster_events.empty else []
                    if local_name in existing_names:
                        st.warning(f"⚠️ Event '{local_name}' already exists. Use Edit function to modify it.")
                    else:
                        add_event(new_event)
                        st.success(f"✅ Event '{local_name}' added successfully!")
                        st.balloons()
                        st.rerun()
    
    # =========================================================================
    # TAB 2: PREDICTIVE ANALYTICS
    # =========================================================================
    with tab2:
        st.markdown("### 🔮 Predictive Analytics")
        
        if len(st.session_state.disaster_events) < 3:
            st.info(f"Add at least 3 events to see predictions. Currently have {len(st.session_state.disaster_events)} events.")
        else:
            st.success(f"Ready with {len(st.session_state.disaster_events)} events")
            
            col1, col2 = st.columns(2)
            with col1:
                df = st.session_state.disaster_events
                if 'fatalities' in df.columns:
                    avg_fatalities = df['fatalities'].mean()
                    risk_score = min(95, int(avg_fatalities * 2) + 30)
                else:
                    risk_score = 50
                
                st.markdown(f"""
                <div style='text-align: center; padding: 20px;'>
                    <div style='font-size: 3rem; font-weight: bold; color: #dc3545;'>{risk_score}%</div>
                    <div style='background-color: #f0f0f0; height: 20px; border-radius: 10px; margin: 10px 0;'>
                        <div style='width: {risk_score}%; background-color: #dc3545; height: 20px; border-radius: 10px;'></div>
                    </div>
                    <p>Projected Risk Level</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if 'year' in df.columns:
                    year_counts = df['year'].value_counts().sort_index().reset_index()
                    year_counts.columns = ['Year', 'Count']
                    fig = px.line(year_counts, x='Year', y='Count', markers=True, title="Event Frequency Trend")
                    st.plotly_chart(fig, width='stretch')
    
    # =========================================================================
    # TAB 3: PROJECTIVE ANALYTICS
    # =========================================================================
    with tab3:
        st.markdown("### 🎯 Projective Analytics")
        st.info("Scenario planning tools coming soon.")
        
        if len(st.session_state.disaster_events) >= 3:
            df = st.session_state.disaster_events
            if 'damage_total' in df.columns:
                avg_damage = df['damage_total'].mean() / 1_000_000
            else:
                avg_damage = 0
            
            st.markdown(f"""
            <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px;'>
                <h4>Based on historical patterns:</h4>
                <p>Average damage per event: <strong>₱{avg_damage:.2f}M</strong></p>
                <p>Most frequent hazard: <strong>{df['hazard_type'].mode()[0] if 'hazard_type' in df.columns and not df['hazard_type'].mode().empty else 'N/A'}</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # =========================================================================
    # TAB 4: EVENT DATABASE (WITH EDIT/DELETE FUNCTIONALITY)
    # =========================================================================
    with tab4:
        st.markdown("### 📊 Event Database")
        st.markdown("*Click on any event to view, edit, or delete*")
        
        if st.session_state.disaster_events.empty:
            st.info("No events in database. Use the Hazard Documentation tab to add events.")
        else:
            # Search and filters
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                search = st.text_input("🔍 Search", placeholder="Search by name...")
            with col_s2:
                if 'year' in st.session_state.disaster_events.columns:
                    years = sorted(st.session_state.disaster_events['year'].unique())
                    year_filter = st.multiselect("Filter by Year", years)
                else:
                    year_filter = []
            with col_s3:
                if 'record_type' in st.session_state.disaster_events.columns:
                    record_types = st.session_state.disaster_events['record_type'].unique().tolist()
                    type_filter = st.multiselect("Filter by Record Type", record_types)
                else:
                    type_filter = []
            
            df = st.session_state.disaster_events.copy()
            if search:
                df = df[df['local_name'].str.contains(search, case=False, na=False)]
            if year_filter:
                df = df[df['year'].isin(year_filter)]
            if type_filter:
                df = df[df['record_type'].isin(type_filter)]
            
            st.markdown(f"**Showing {len(df)} of {len(st.session_state.disaster_events)} events**")
            
            # Export button
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                if st.button("📥 Export to CSV", width='stretch'):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV", 
                        csv, 
                        f"disaster_events_{datetime.now().strftime('%Y%m%d')}.csv", 
                        "text/csv"
                    )
            
            st.markdown("---")
            
            # Display events with edit/delete functionality
            for idx, event in df.iterrows():
                display_name = event.get('local_name', 'Unknown')
                if pd.isna(display_name) or display_name == '':
                    display_name = 'Unnamed Event'
                
                record_type = event.get('record_type', 'Unknown')
                header_color = '#8B4513' if record_type == 'Historical' else '#1E3A8A'
                
                # Check if in edit mode
                if st.session_state.get(f'edit_mode_{idx}', False):
                    with st.form(key=f"edit_form_{idx}"):
                        st.markdown(f"### ✏️ Editing: {display_name}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_local = st.text_input("Local Name", value=event.get('local_name', ''))
                            new_year = st.number_input("Year", value=int(event.get('year', 2000)), min_value=1800, max_value=2100)
                            new_fatalities = st.number_input("Fatalities", value=int(event.get('fatalities', 0)), min_value=0)
                            new_injured = st.number_input("Injured", value=int(event.get('injured', 0)), min_value=0)
                            new_missing = st.number_input("Missing", value=int(event.get('missing', 0)), min_value=0)
                            new_houses_total = st.number_input("Totally Damaged Houses", value=int(event.get('houses_total', 0)), min_value=0)
                            new_houses_partial = st.number_input("Partially Damaged Houses", value=int(event.get('houses_partial', 0)), min_value=0)
                        with col2:
                            new_international = st.text_input("International Name", value=event.get('international_name', ''))
                            new_hazard_type = st.text_input("Hazard Type", value=event.get('hazard_type', ''))
                            new_region = st.text_input("Region", value=event.get('region', ''))
                            new_municipalities = st.text_input("Municipalities", value=event.get('municipalities', ''))
                            new_damage_agri = st.number_input("Agriculture Damage", value=float(event.get('damage_agriculture', 0)), step=10000.0)
                            new_damage_infra = st.number_input("Infrastructure Damage", value=float(event.get('damage_infrastructure', 0)), step=10000.0)
                            new_remarks = st.text_area("Remarks", value=event.get('remarks', ''), height=80)
                        
                        # Date fields
                        st.markdown("#### 📅 Event Period")
                        col_date1, col_date2 = st.columns(2)
                        with col_date1:
                            new_start_date = st.date_input(
                                "Start Date", 
                                value=datetime.strptime(event.get('start_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
                            )
                        with col_date2:
                            new_end_date = st.date_input(
                                "End Date", 
                                value=datetime.strptime(event.get('end_date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
                            )
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("💾 Save Changes", width='stretch'):
                                new_duration = (new_end_date - new_start_date).days
                                
                                # Update the event
                                event_data = event.to_dict()
                                event_data['local_name'] = new_local
                                event_data['year'] = new_year
                                event_data['fatalities'] = new_fatalities
                                event_data['injured'] = new_injured
                                event_data['missing'] = new_missing
                                event_data['houses_total'] = new_houses_total
                                event_data['houses_partial'] = new_houses_partial
                                event_data['international_name'] = new_international
                                event_data['hazard_type'] = new_hazard_type
                                event_data['region'] = new_region
                                event_data['municipalities'] = new_municipalities
                                event_data['damage_agriculture'] = new_damage_agri
                                event_data['damage_infrastructure'] = new_damage_infra
                                event_data['damage_total'] = new_damage_agri + new_damage_infra
                                event_data['remarks'] = new_remarks
                                event_data['start_date'] = new_start_date.strftime('%Y-%m-%d')
                                event_data['end_date'] = new_end_date.strftime('%Y-%m-%d')
                                event_data['duration_days'] = new_duration
                                event_data['date_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                
                                from utils.database import save_events
                                st.session_state.disaster_events.loc[idx] = event_data
                                save_events(st.session_state.disaster_events)
                                
                                st.session_state[f'edit_mode_{idx}'] = False
                                st.success("✅ Event updated successfully!")
                                st.rerun()
                        with col2:
                            if st.form_submit_button("❌ Cancel", width='stretch'):
                                st.session_state[f'edit_mode_{idx}'] = False
                                st.rerun()
                    st.markdown("---")
                    continue
                
                # Normal display mode with expander
                with st.expander(f"**{display_name}** ({event.get('year', '')}) - {event.get('hazard_type', 'Unknown')}"):
                    # Record type badge
                    st.markdown(f"""
                    <div style='background-color:{header_color}; padding:5px 10px; border-radius:5px; margin-bottom:10px; display: flex; justify-content: space-between;'>
                        <span style='color:white;'>{record_type.upper()} RECORD</span>
                        <span style='color:white;'>ID: {event.get('event_id', 'N/A')}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Event period
                    start = event.get('start_date', 'Unknown')
                    end = event.get('end_date', 'Unknown')
                    duration = event.get('duration_days', '')
                    st.markdown(f"**📅 Period:** {start} to {end} ({duration} day(s))")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown("**📊 Human Impact**")
                        st.markdown(f"Fatalities: {event.get('fatalities', 0):,}")
                        st.markdown(f"Injured: {event.get('injured', 0):,}")
                        st.markdown(f"Missing: {event.get('missing', 0):,}")
                        if event.get('tcws', 0) > 0:
                            st.markdown(f"TCWS Signal: #{event.get('tcws', 0)}")
                    with col2:
                        st.markdown("**🏠 Housing Damage**")
                        st.markdown(f"Totally Damaged: {event.get('houses_total', 0):,}")
                        st.markdown(f"Partially Damaged: {event.get('houses_partial', 0):,}")
                        st.markdown(f"Affected Barangays: {event.get('affected_barangays', 0)}")
                    with col3:
                        st.markdown("**💰 Economic Damage**")
                        total = event.get('damage_total', 0) / 1_000_000
                        st.markdown(f"Total: ₱{total:.2f}M")
                        if event.get('damage_agriculture', 0) > 0:
                            st.markdown(f"Agriculture: ₱{event.get('damage_agriculture', 0)/1e6:.2f}M")
                        if event.get('damage_infrastructure', 0) > 0:
                            st.markdown(f"Infrastructure: ₱{event.get('damage_infrastructure', 0)/1e6:.2f}M")
                    
                    st.markdown(f"**📍 Region:** {event.get('region', 'Unknown')}")
                    if event.get('municipalities'):
                        st.markdown(f"**📍 Municipalities:** {event.get('municipalities')}")
                    
                    if event.get('source_reference'):
                        st.markdown(f"**📚 Source:** {event.get('source_reference')}")
                    
                    if event.get('remarks'):
                        preview = event.get('remarks')[:150] + '...' if len(event.get('remarks', '')) > 150 else event.get('remarks')
                        st.markdown(f"**📝 Remarks:** {preview}")
                    
                    # Edit and Delete buttons
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        if st.button(f"✏️ Edit", key=f"edit_{idx}", width='stretch'):
                            st.session_state[f'edit_mode_{idx}'] = True
                            st.rerun()
                    with col_btn2:
                        if st.button(f"🗑️ Delete", key=f"del_{idx}", width='stretch'):
                            st.session_state[f'delete_confirm_{idx}'] = True
                    
                    # Delete confirmation
                    if st.session_state.get(f'delete_confirm_{idx}', False):
                        st.warning(f"⚠️ Delete '{display_name}'? This action cannot be undone.")
                        col_yes, col_no = st.columns(2)
                        with col_yes:
                            if st.button(f"✅ Yes, Delete", key=f"confirm_del_{idx}", width='stretch'):
                                from utils.database import save_events
                                st.session_state.disaster_events = st.session_state.disaster_events.drop(idx).reset_index(drop=True)
                                save_events(st.session_state.disaster_events)
                                st.session_state[f'delete_confirm_{idx}'] = False
                                st.success("✅ Event deleted successfully!")
                                st.rerun()
                        with col_no:
                            if st.button(f"❌ No, Cancel", key=f"cancel_del_{idx}", width='stretch'):
                                st.session_state[f'delete_confirm_{idx}'] = False
                                st.rerun()
    
    # =========================================================================
    # TAB 5: SUMMARY DASHBOARD
    # =========================================================================
    with tab5:
        st.markdown("### 📈 Summary Dashboard")
        
        if st.session_state.disaster_events.empty:
            st.info("Add events to see summary statistics.")
        else:
            df = st.session_state.disaster_events.copy()
            
            # Check if we have the required columns
            has_fatalities = 'fatalities' in df.columns
            has_houses_total = 'houses_total' in df.columns
            has_damage_total = 'damage_total' in df.columns
            has_year = 'year' in df.columns
            has_hazard_type = 'hazard_type' in df.columns
            has_record_type = 'record_type' in df.columns
            has_hazard_category = 'hazard_category' in df.columns
            
            # Filters
            st.markdown("#### 🔍 Filters")
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                if has_record_type:
                    record_filter = st.radio(
                        "Record Type",
                        ["Both", "Provincial Only", "Historical Only"],
                        horizontal=True,
                        index=0
                    )
                else:
                    record_filter = "Both"
            
            with col_f2:
                if has_year:
                    all_years = sorted(df['year'].unique())
                    year_filter = st.multiselect(
                        "Year(s)",
                        options=all_years,
                        default=all_years,
                        help="Select one or more years to filter"
                    )
                else:
                    year_filter = []
            
            with col_f3:
                if has_hazard_category:
                    categories = df['hazard_category'].unique().tolist()
                    if categories:
                        category_filter = st.multiselect(
                            "Hazard Category",
                            options=categories,
                            default=categories,
                            help="Filter by hazard category"
                        )
                    else:
                        category_filter = []
                else:
                    category_filter = []
            
            # Apply filters
            if has_record_type and record_filter == "Provincial Only":
                df = df[df['record_type'] == 'Provincial']
            elif has_record_type and record_filter == "Historical Only":
                df = df[df['record_type'] == 'Historical']
            
            if year_filter and has_year:
                df = df[df['year'].isin(year_filter)]
            
            if category_filter and has_hazard_category:
                df = df[df['hazard_category'].isin(category_filter)]
            
            st.caption(f"Showing {len(df)} events | Record Type: {record_filter} | Years: {', '.join(map(str, year_filter)) if year_filter else 'All'}")
            st.markdown("---")
            
            # Summary metrics - safe access
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Events", len(df))
            with col2:
                if has_fatalities:
                    st.metric("Total Fatalities", int(df['fatalities'].sum()))
                else:
                    st.metric("Total Fatalities", 0)
            with col3:
                if has_houses_total:
                    st.metric("Totally Damaged Houses", int(df['houses_total'].sum()))
                else:
                    st.metric("Totally Damaged Houses", 0)
            with col4:
                if has_damage_total:
                    st.metric("Total Damage", f"₱{df['damage_total'].sum()/1e6:.1f}M")
                else:
                    st.metric("Total Damage", "₱0M")
            
            # Charts - only if we have data
            if not df.empty:
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    if has_hazard_type:
                        type_counts = df['hazard_type'].value_counts().reset_index()
                        type_counts.columns = ['Hazard Type', 'Count']
                        fig = px.pie(type_counts, values='Count', names='Hazard Type', title="Events by Hazard Type")
                        st.plotly_chart(fig, width='stretch')
                
                with col_c2:
                    if has_year:
                        year_counts = df['year'].value_counts().sort_index().reset_index()
                        year_counts.columns = ['Year', 'Count']
                        fig = px.bar(year_counts, x='Year', y='Count', title="Events by Year")
                        st.plotly_chart(fig, width='stretch')
    
    # =========================================================================
    # TAB 6: HISTORICAL CONTEXT GUIDE
    # =========================================================================
    with tab6:
        st.markdown("### 📜 Understanding Historical Records")
        
        st.markdown("""
        <div style='background: linear-gradient(135deg, #8B4513, #A0522D); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;'>
            <h3 style='color: #FFD700;'>How We Interpret Historical Records</h3>
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
            
            Typhoons that affect CAR and its adjacent regions almost certainly impacted Mountain Province.
            """)
            
            st.markdown("""
            #### 📊 Confidence Scoring System
            
            | Regions Mentioned | Confidence | Weight |
            |------------------|------------|--------|
            | CAR + I + II | VERY HIGH | 95% |
            | CAR + I or CAR + II | HIGH | 85% |
            | CAR only | MEDIUM | 70% |
            | I + II only | MEDIUM-LOW | 40% |
            | Single region | LOW | 20% |
            | Provincial data | DIRECT | 100% |
            """)
        
        with col2:
            st.markdown("""
            #### 📝 Best Practices
            
            **When entering historical records:**
            
            1. **Record the exact regions mentioned** in the source document
            2. **Document your reasoning** in the Remarks field
            3. **Note any uncertainties** about the original data
            4. **Include source information** (archives, references, etc.)
            
            #### 💡 Example
            
            **Source:** Spanish Colonial Archive, 1894
            **Regions Mentioned:** "Cagayan, Ilocos, Montañosa"
            **Inference:** "Montañosa refers to the mountainous interior, including present-day Mountain Province."
            **Confidence:** HIGH
            """)
            
            if not st.session_state.disaster_events.empty:
                st.markdown("#### 📊 Your Current Data")
                df = st.session_state.disaster_events
                historical_count = len(df[df['record_type'] == 'Historical']) if 'record_type' in df.columns else 0
                provincial_count = len(df[df['record_type'] == 'Provincial']) if 'record_type' in df.columns else 0
                st.markdown(f"- **Historical records:** {historical_count}")
                st.markdown(f"- **Provincial records:** {provincial_count}")
                st.markdown(f"- **Total records:** {len(df)}")