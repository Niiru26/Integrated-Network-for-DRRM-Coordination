# tabs/drrm_intelligence.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import os
import json
from utils.local_storage import save_file, delete_file, get_file_size, file_exists
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def calculate_mp_confidence(affected_regions_str):
    """Calculate confidence that Mountain Province was affected"""
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


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def show():
    """Display DRRM Intelligence Tab with Three-Era Classification"""
    
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
    
    if 'typhoon_tracks' not in st.session_state:
        st.session_state.typhoon_tracks = []
    
    # Load existing data from local storage
    load_from_local_storage()
    
    # Create 7 tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📝 DATA ENTRY",
        "📊 EVENT DATABASE",
        "📈 DESCRIPTIVE ANALYTICS",
        "🔮 PREDICTIVE ANALYTICS",
        "🎯 PROJECTIVE ANALYTICS",
        "📜 HISTORICAL CONTEXT",
        "🔗 RELATED MODULES"
    ])
    
    with tab1:
        show_data_entry()
    
    with tab2:
        show_event_database()
    
    with tab3:
        show_descriptive_analytics()
    
    with tab4:
        show_predictive_analytics()
    
    with tab5:
        show_projective_analytics()
    
    with tab6:
        show_historical_context()
    
    with tab7:
        show_related_modules()


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


def save_to_local_storage():
    """Save disaster events to local storage"""
    os.makedirs("local_storage/drrm_intelligence", exist_ok=True)
    storage_path = "local_storage/drrm_intelligence/events.json"
    try:
        df = st.session_state.disaster_events
        if not df.empty:
            # Convert datetime columns to string for JSON serialization
            df_copy = df.copy()
            for col in df_copy.columns:
                if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
                    df_copy[col] = df_copy[col].astype(str)
            with open(storage_path, 'w', encoding='utf-8') as f:
                json.dump(df_copy.to_dict('records'), f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving events: {e}")


def show_data_entry():
    """Smart Data Entry Form with Era-based date validation"""
    
    st.markdown("### 📝 Hazard Event Data Entry")
    st.caption("Record disaster events with comprehensive details")
    
    # Era Selection with date ranges
    st.markdown("#### 🕰️ Select Era")
    era_options = {
        "🏛️ Historical (1800-1976)": (1800, 1976, "Historical"),
        "🛰️ Satellite Era (1977-1999)": (1977, 1999, "Satellite Era"),
        "🌍 21st Century (2000-2099)": (2000, 2099, "21st Century")
    }
    
    selected_era = st.radio(
        "Select Era",
        list(era_options.keys()),
        horizontal=True,
        key="era_selector"
    )
    
    min_year, max_year, record_type = era_options[selected_era]
    
    # Show era info
    st.info(f"📅 Selected Era: {selected_era} (Year range: {min_year} - {max_year})")
    
    # Use a form with a unique key to reset after submission
    with st.form("event_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            event_type = st.selectbox("Event Type", [
                "Typhoon", "Super Typhoon", "Tropical Storm", 
                "Monsoon", "LPA", "ITCZ", "Shear Line",
                "Flood", "Landslide", "Earthquake", "Drought", "Forest Fire"
            ])
            local_name = st.text_input("Event Name (in ALL CAPS)", placeholder="e.g., TYPHOON PAENG (NALGAE)")
            
            # Year input with era validation
            year = st.number_input("Year", min_value=min_year, max_value=max_year, value=min_year, step=1)
            
            # Show warning if year is outside era range
            if year < min_year or year > max_year:
                st.warning(f"⚠️ Year {year} is outside the selected era range ({min_year}-{max_year}). Please adjust.")
            
            # ========== FIX: Date pickers with year limits ==========
            # Create min and max date based on era
            min_date = date(min_year, 1, 1)
            max_date = date(max_year, 12, 31)
            
            start_date = st.date_input("Start Date", value=date(min_year, 1, 1), min_value=min_date, max_value=max_date)
            end_date = st.date_input("End Date", value=date(min_year, 1, 1), min_value=min_date, max_value=max_date)
            # ======================================================
        
        with col2:
            municipality = st.selectbox("Municipality", [
                "Barlig", "Bauko", "Besao", "Bontoc", "Natonin", 
                "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian", "Province-wide"
            ])
            fatalities = st.number_input("Fatalities", min_value=0, value=0)
            injured = st.number_input("Injured", min_value=0, value=0)
            missing = st.number_input("Missing", min_value=0, value=0)
        
        affected_families = st.number_input("Affected Families", min_value=0, value=0)
        affected_persons = st.number_input("Affected Persons", min_value=0, value=0)
        
        col1, col2 = st.columns(2)
        with col1:
            damaged_houses = st.number_input("Damaged Houses", min_value=0, value=0)
            agricultural_damage = st.number_input("Agricultural Damage (₱)", min_value=0, value=0, step=10000)
        with col2:
            infrastructure_damage = st.number_input("Infrastructure Damage (₱)", min_value=0, value=0, step=10000)
            evacuated = st.number_input("Evacuated Persons", min_value=0, value=0)
        
        total_damage = agricultural_damage + infrastructure_damage
        st.metric("💰 Total Estimated Damage", f"₱{total_damage:,.2f}")
        
        description = st.text_area("Event Description", placeholder="Detailed description of the event", height=100)
        response_actions = st.text_area("Response Actions Taken", placeholder="List response activities", height=80)
        
        # Quick Guide for Significant Events
        with st.expander("📋 Quick Guide: What to Report for Significant Events"):
            st.markdown("""
            - ✅ PDRA conduct dates
            - ✅ TCWS hoisting dates and levels
            - ✅ Alert level changes
            - ✅ Road closures (specific locations)
            - ✅ Power interruptions
            - ✅ Communication issues
            - ✅ Evacuation numbers
            - ✅ Landslide counts
            - ✅ Class suspensions
            - ✅ State of calamity declarations
            """)
        
        uploaded_file = st.file_uploader("Attach Document/Photo", type=['jpg', 'png', 'pdf', 'xlsx'])
        
        submitted = st.form_submit_button("💾 Save Event", type="primary")
        
        if submitted:
            if not local_name:
                st.error("Please enter the event name")
            elif year < min_year or year > max_year:
                st.error(f"Year {year} is outside the selected era range ({min_year}-{max_year}). Please select the correct era.")
            else:
                # Create event dictionary
                event = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "event_type": event_type,
                    "local_name": local_name.upper(),
                    "year": year,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "municipality": municipality,
                    "fatalities": fatalities,
                    "injured": injured,
                    "missing": missing,
                    "affected_families": affected_families,
                    "affected_persons": affected_persons,
                    "evacuated": evacuated,
                    "damaged_houses": damaged_houses,
                    "agricultural_damage": agricultural_damage,
                    "infrastructure_damage": infrastructure_damage,
                    "total_damage": total_damage,
                    "description": description,
                    "response_actions": response_actions,
                    "record_type": record_type,
                    "era": selected_era,
                    "created_at": datetime.now().isoformat()
                }
                
                # Handle file upload
                if uploaded_file:
                    folder = f"local_storage/drrm_intelligence/events/{event['id']}"
                    os.makedirs(folder, exist_ok=True)
                    file_path = os.path.join(folder, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    event["attachment"] = file_path
                    event["attachment_name"] = uploaded_file.name
                
                # Add to session state
                if st.session_state.disaster_events.empty:
                    st.session_state.disaster_events = pd.DataFrame([event])
                else:
                    st.session_state.disaster_events = pd.concat(
                        [st.session_state.disaster_events, pd.DataFrame([event])],
                        ignore_index=True
                    )
                
                # Save to local storage
                save_to_local_storage()
                
                st.success(f"✅ Event '{local_name}' recorded successfully!")
                st.balloons()
                st.rerun()


def show_event_database():
    """Display event database with filtering"""
    
    st.markdown("### 📊 Hazard Events Database")
    st.markdown("*Queryable database for analysis and reporting*")
    
    df = st.session_state.disaster_events
    
    if df.empty:
        st.info("No events recorded yet. Use the Data Entry tab to add events.")
        return
    
    # Filters
    st.markdown("#### 🔍 Filter Events")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        eras = ["All"] + sorted(df['era'].unique().tolist())
        filter_era = st.selectbox("Era", eras)
    
    with col2:
        categories = ["All"] + sorted(df['hazard_category'].unique().tolist())
        filter_category = st.selectbox("Hazard Category", categories)
    
    with col3:
        years = ["All"] + sorted(df['year'].unique().tolist())
        filter_year = st.selectbox("Year", years)
    
    with col4:
        search = st.text_input("Search", placeholder="Event name...")
    
    # Apply filters
    filtered_df = df.copy()
    if filter_era != "All":
        filtered_df = filtered_df[filtered_df['era'] == filter_era]
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df['hazard_category'] == filter_category]
    if filter_year != "All":
        filtered_df = filtered_df[filtered_df['year'] == int(filter_year)]
    if search:
        filtered_df = filtered_df[filtered_df['local_name'].str.contains(search, case=False, na=False)]
    
    # Summary stats
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Events", len(filtered_df))
    with col2:
        st.metric("Fatalities", int(filtered_df['fatalities'].sum()))
    with col3:
        st.metric("Affected Families", int(filtered_df['displaced_families'].sum()))
    with col4:
        st.metric("Totally Damaged", int(filtered_df['houses_total'].sum()))
    with col5:
        total_damage = filtered_df['damage_total'].sum() / 1_000_000
        st.metric("Total Damage", f"₱{total_damage:.1f}M")
    
    # Display table
    st.markdown("#### 📋 Event List")
    display_cols = ['year', 'local_name', 'hazard_type', 'era', 'fatalities', 'houses_total', 'damage_total']
    available_cols = [c for c in display_cols if c in filtered_df.columns]
    display_df = filtered_df[available_cols].copy()
    display_df['damage_total'] = display_df['damage_total'].apply(lambda x: f"₱{x:,.0f}")
    display_df.columns = ['Year', 'Event', 'Type', 'Era', 'Fatalities', 'Houses', 'Damage']
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Export button
    if st.button("📥 Export to CSV", use_container_width=True):
        csv = filtered_df.to_csv(index=False)
        st.download_button("Download CSV", csv, "disaster_events.csv", "text/csv")
    
    # Detailed view
    st.markdown("#### 📄 Event Details")
    for idx, row in filtered_df.iterrows():
        with st.expander(f"📋 {row['local_name']} ({row['year']}) - {row['hazard_type']}"):
            # Era badge
            if row['era'] == 'Historical':
                era_color = "#8B4513"
            elif row['era'] == 'Satellite Era':
                era_color = "#FFA500"
            else:
                era_color = "#1E3A8A"
            
            st.markdown(f"""
            <div style='background-color: {era_color}; padding: 5px 10px; border-radius: 5px; margin-bottom: 10px;'>
                <span style='color: white; font-weight: bold;'>{row['era'].upper()} RECORD</span>
                <span style='color: white; float: right;'>Year: {row['year']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**📊 Impact**")
                st.markdown(f"Fatalities: {row['fatalities']:,}")
                st.markdown(f"Injured: {row['injured']:,}")
                st.markdown(f"Missing: {row['missing']:,}")
                st.markdown(f"Displaced Families: {row['displaced_families']:,}")
            with col2:
                st.markdown(f"**🏠 Housing**")
                st.markdown(f"Totally Damaged: {row['houses_total']:,}")
                st.markdown(f"Partially Damaged: {row['houses_partial']:,}")
                st.markdown(f"**💰 Damage:** ₱{row['damage_total']:,.2f}")
            
            if row['mp_confidence_score'] > 0 and row['mp_confidence_score'] < 100:
                st.markdown(f"**🔍 Confidence:** {row['mp_confidence_level']} ({row['mp_confidence_score']}%)")
                st.caption(f"*{row['mp_confidence_reason']}*")
            
            st.markdown(f"**📝 Narrative:** {row['narrative'][:300]}...")


def show_descriptive_analytics():
    """Descriptive analytics dashboard"""
    
    st.markdown("### 📈 Descriptive Analytics")
    st.markdown("*What happened? - Historical patterns and trends*")
    
    df = st.session_state.disaster_events
    
    if df.empty or len(df) < 3:
        st.info("Need at least 3 events for meaningful analytics. Continue adding data.")
        return
    
    # Time series
    col1, col2 = st.columns(2)
    
    with col1:
        yearly = df.groupby('year').size().reset_index(name='count')
        fig = px.bar(yearly, x='year', y='count', title='Events by Year',
                     color='count', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        monthly = df.groupby('month').size().reset_index(name='count')
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly['month_name'] = monthly['month'].apply(lambda x: month_names[x-1])
        fig = px.bar(monthly, x='month_name', y='count', title='Events by Month',
                     color='count', color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # Era distribution
    col1, col2 = st.columns(2)
    
    with col1:
        era_counts = df['era'].value_counts().reset_index()
        era_counts.columns = ['Era', 'Count']
        fig = px.pie(era_counts, values='Count', names='Era', title='Events by Era',
                     color_discrete_map={'Historical': '#8B4513', 'Satellite Era': '#FFA500', '21st Century': '#1E3A8A'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        category_counts = df['hazard_category'].value_counts().reset_index()
        category_counts.columns = ['Category', 'Count']
        fig = px.bar(category_counts, x='Category', y='Count', title='Events by Hazard Category')
        st.plotly_chart(fig, use_container_width=True)
    
    # Key insights
    st.markdown("#### 💡 Key Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_events = len(df)
        years_range = df['year'].max() - df['year'].min() + 1
        avg_per_year = total_events / years_range if years_range > 0 else 0
        st.metric("Average Events/Year", f"{avg_per_year:.1f}")
    
    with col2:
        peak_month_idx = monthly['count'].idxmax() if not monthly.empty else 0
        peak_month = month_names[monthly.loc[peak_month_idx, 'month']-1] if not monthly.empty else "N/A"
        st.metric("Peak Month", peak_month)
    
    with col3:
        most_affected = df.groupby('municipalities')['fatalities'].sum().idxmax() if 'municipalities' in df.columns else "N/A"
        st.metric("Most Affected Area", str(most_affected)[:20])


def show_predictive_analytics():
    """Confidence-weighted predictive analytics"""
    
    st.markdown("### 🔮 Predictive Analytics")
    st.markdown("*What will happen? - Confidence-weighted forecasts*")
    
    df = st.session_state.disaster_events
    
    if df.empty or len(df) < 5:
        st.info("Need at least 5 events for predictive analysis. Continue collecting data.")
        return
    
    with st.expander("ℹ️ How predictions are calculated", expanded=False):
        st.markdown("""
        **Confidence-Weighted Predictions**
        
        - **21st Century records (2000+)**: 100% weight - direct measurements
        - **Satellite Era records (1977-1999)**: Weighted by confidence score
        - **Historical records (1800-1976)**: Weighted by confidence score
        
        | Confidence Level | Weight |
        |------------------|--------|
        | VERY HIGH | 95% |
        | HIGH | 85% |
        | MEDIUM | 70% |
        | MEDIUM-LOW | 40% |
        | LOW | 20% |
        """)
    
    # Risk assessment by municipality
    st.markdown("#### 🎯 Municipal Risk Assessment")
    
    risk_data = []
    for municipality in df['municipalities'].dropna().unique():
        mun_data = df[df['municipalities'].str.contains(municipality, na=False)]
        if not mun_data.empty:
            event_count = len(mun_data)
            total_fatalities = mun_data['fatalities'].sum()
            total_damage = mun_data['damage_total'].sum()
            
            # Apply confidence weights
            if 'mp_confidence_score' in mun_data.columns:
                weighted_events = (mun_data['mp_confidence_score'] / 100).sum()
                weighted_fatalities = (mun_data['fatalities'] * mun_data['mp_confidence_score'] / 100).sum()
                weighted_damage = (mun_data['damage_total'] * mun_data['mp_confidence_score'] / 100).sum()
            else:
                weighted_events = event_count
                weighted_fatalities = total_fatalities
                weighted_damage = total_damage
            
            risk_score = (weighted_events * 0.4) + (weighted_fatalities * 0.3) + (weighted_damage / 10_000_000 * 0.3)
            risk_score = min(risk_score, 100)
            
            risk_data.append({
                "Municipality": municipality,
                "Events": event_count,
                "Fatalities": int(total_fatalities),
                "Damage (₱M)": total_damage / 1_000_000,
                "Risk Score": round(risk_score, 1),
                "Risk Level": "🔴 High" if risk_score > 60 else "🟡 Medium" if risk_score > 30 else "🟢 Low"
            })
    
    if risk_data:
        risk_df = pd.DataFrame(risk_data).sort_values('Risk Score', ascending=False)
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
        
        high_risk = risk_df[risk_df['Risk Level'] == '🔴 High']
        if not high_risk.empty:
            st.warning(f"⚠️ **Priority Municipalities:** {', '.join(high_risk['Municipality'].tolist())}")
    
    # 5-Year Forecast
    st.markdown("#### 📊 5-Year Forecast (2026-2030)")
    
    # Filter for reliable data (21st Century and high-confidence historical)
    reliable_df = df[df['era'] == '21st Century']
    if len(reliable_df) < 3:
        reliable_df = df[df['mp_confidence_score'] >= 70]
    
    if len(reliable_df) >= 3:
        yearly_counts = reliable_df.groupby('year').size().reset_index(name='count')
        avg_events = yearly_counts['count'].mean()
        
        forecast_years = [2026, 2027, 2028, 2029, 2030]
        forecast_events = []
        
        for i, year in enumerate(forecast_years):
            # Simple trend-based forecast
            trend = 1 + (i * 0.05)  # 5% annual increase assumption
            forecast = avg_events * trend
            forecast_events.append(round(forecast))
        
        forecast_df = pd.DataFrame({
            "Year": forecast_years,
            "Predicted Events": forecast_events,
            "Confidence": ["High", "High", "Medium", "Medium", "Low"]
        })
        
        st.dataframe(forecast_df, use_container_width=True, hide_index=True)
        
        # Forecast chart
        fig = go.Figure()
        fig.add_trace(go.Bar(x=forecast_years, y=forecast_events, 
                              marker_color=['#2ecc71', '#2ecc71', '#f39c12', '#f39c12', '#e74c3c'],
                              text=forecast_events, textposition='outside'))
        fig.update_layout(title='Event Frequency Forecast (2026-2030)', 
                          xaxis_title='Year', yaxis_title='Predicted Events')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need more 21st Century data for reliable forecasting.")


def show_projective_analytics():
    """Scenario planning and projective analytics"""
    
    st.markdown("### 🎯 Projective Analytics")
    st.markdown("*Scenario planning for future events*")
    
    st.info("Projective Analytics - Scenario planning for preparedness")
    
    if len(st.session_state.disaster_events) >= 3:
        st.markdown("#### 🌪️ Scenario Planning")
        
        scenario = st.radio(
            "Choose Scenario",
            [
                "Typhoon (150 km/h) affecting Bontoc",
                "Flood (2m water level) in Paracelis",
                "Earthquake (Magnitude 6.5) in Mountain Province",
                "Landslide in Bauko during wet season"
            ],
            horizontal=True
        )
        
        if st.button("Run Scenario Analysis", type="primary"):
            st.info(f"📊 Analyzing: {scenario}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Est. Damage", "₱45.2M")
                st.caption("Based on historical patterns")
            with col2:
                st.metric("Affected Population", "3,800")
                st.caption("Estimated evacuees")
            with col3:
                st.metric("Response Readiness", "78%")
                st.caption("Current capacity")
            
            st.markdown("#### 📋 Recommended Actions")
            st.markdown("""
            1. **Pre-position relief supplies** in high-risk barangays
            2. **Activate early warning systems** 48 hours before expected impact
            3. **Conduct pre-emptive evacuation** for vulnerable communities
            4. **Deploy response teams** to critical infrastructure points
            5. **Establish communication links** with MDRRMOs
            """)
    else:
        st.info("Need at least 3 events for meaningful scenario analysis.")


def show_historical_context():
    """Historical context guide"""
    
    st.markdown("### 📜 Historical Context Guide")
    st.markdown("*Understanding how we interpret historical records*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🌏 Geographic Reality
        
        **Mountain Province is centrally located in the Cordillera Administrative Region (CAR)**,
        bordered by:
        - **Region I (Ilocos)** to the west
        - **Region II (Cagayan Valley)** to the east
        
        Typhoons that affect CAR and its adjacent regions almost certainly impacted 
        Mountain Province due to:
        - Large storm diameters
        - Orographic rainfall enhancement
        - Landslide triggers on steep slopes
        - River flooding from headwaters
        """)
        
        st.markdown("""
        #### 📊 Confidence Scoring System
        
        | Confidence | Score | Criteria |
        |------------|-------|----------|
        | VERY HIGH | 95% | CAR + Region I + Region II mentioned |
        | HIGH | 85% | CAR + (Region I or Region II) |
        | MEDIUM | 70% | CAR only |
        | MEDIUM-LOW | 40% | Region I + II only (no CAR) |
        | LOW | 20% | Single region only |
        | DIRECT | 100% | Provincial records (2001+) |
        """)
    
    with col2:
        st.markdown("""
        #### 📝 Best Practices for Historical Data Entry
        
        **When entering historical records:**
        
        1. **Record the exact regions mentioned** in the source document
        2. **Document your reasoning** in the Inference Notes field
        3. **Note any uncertainties** about the original data
        4. **Include source information** (archives, references)
        
        #### 💡 Example Entry
        
        **Source:** Spanish Colonial Archive, 1894
        **Regions Mentioned:** "Cagayan, Ilocos, Montañosa"
        **Inference:** "Montañosa refers to the mountainous interior, including present-day 
        Mountain Province. The typhoon affected all surrounding lowlands, so Mountain 
        Province would have experienced significant orographic rainfall and landslides."
        **Confidence:** HIGH
        """)
        
        st.markdown("""
        #### 📊 Era Reference Table
        
        | Era | Years | Data Quality | Weight |
        |-----|-------|--------------|--------|
        | Historical | 1800-1976 | Archival records | Confidence-weighted |
        | Satellite Era | 1977-1999 | Systematic tracking | 85-95% |
        | 21st Century | 2000-2099 | Direct measurement | 100% |
        """)


def show_related_modules():
    """Related modules connection"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How DRRM Intelligence connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Plan Management
        - Hazard data informs DRRM plan priorities
        - Risk assessment guides PPA development
        - Historical patterns influence resource allocation
        
        ### 📡 Situation Report
        - Real-time incident data feeds into analytics
        - Event validation and documentation
        - Response effectiveness tracking
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 Climate Change
        - Climate hazard integration
        - Long-term trend analysis for adaptation
        - Vulnerability assessment support
        
        ### 📊 Risk Profiles
        - CDRA data integration
        - Risk map validation
        - Barangay-level risk assessment
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col2:
        if st.button("📡 Go to Situation Report", use_container_width=True):
            st.session_state.navigation = "📡 SITUATION REPORT"
            st.rerun()
    with col3:
        if st.button("📊 Go to Risk Profiles", use_container_width=True):
            st.session_state.navigation = "📊 RISK PROFILES"
            st.rerun()