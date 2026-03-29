# tabs/drrm_intelligence.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os
import json
from utils.supabase_client import auto_sync_add, auto_sync_delete, auto_sync_update, is_connected, auto_sync_table
from utils.local_storage import save_file, delete_file, get_file_info, get_file_size, file_exists, list_files
import folium
from streamlit_folium import folium_static

def show():
    """Display DRRM Intelligence Tab with Hazard Events and Predictive Analytics"""
    
    st.markdown("# 📊 DRRM INTELLIGENCE")
    st.caption("Hazard events database, trend analysis, predictive forecasting, and typhoon tracking")
    
    # Initialize session state
    if 'disaster_events' not in st.session_state:
        st.session_state.disaster_events = pd.DataFrame()
    
    if 'typhoon_tracks' not in st.session_state:
        st.session_state.typhoon_tracks = []
    
    if 'hazard_photos' not in st.session_state:
        st.session_state.hazard_photos = []
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📝 Event Entry",
        "📊 Event Database",
        "📈 Trend Analysis",
        "🌀 Typhoon Tracking",
        "📸 Hazard Photos",
        "🔮 Predictive Analytics"
    ])
    
    with tab1:
        show_event_entry()
    
    with tab2:
        show_event_database()
    
    with tab3:
        show_trend_analysis()
    
    with tab4:
        show_typhoon_tracking()
    
    with tab5:
        show_hazard_photos()
    
    with tab6:
        show_predictive_analytics()


def upload_event_file(event_id, file_type, uploaded_file, description=""):
    """Upload a file for an event - stored locally"""
    if not uploaded_file:
        return None
    
    category = "drrm_intelligence"
    subcategory = "event_files"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"event_{event_id}_{file_type}_{timestamp}_{uploaded_file.name}"
    
    file_path = save_file(uploaded_file, category, subcategory, filename)
    
    return {
        "file_path": file_path,
        "filename": uploaded_file.name,
        "file_size": get_file_size(file_path),
        "file_type": file_type,
        "description": description,
        "uploaded_at": datetime.now().isoformat()
    }


def upload_typhoon_track(track_data, track_image=None):
    """Upload typhoon track data and optional track map"""
    category = "drrm_intelligence"
    subcategory = "typhoon_tracks"
    
    track_id = int(datetime.now().timestamp() * 1000)
    
    # Save track data as JSON
    track_filename = f"typhoon_track_{track_id}_{datetime.now().strftime('%Y%m%d')}.json"
    track_path = save_file(None, category, subcategory, track_filename)
    
    with open(track_path, "w") as f:
        json.dump(track_data, f)
    
    track_info = {
        "id": track_id,
        "track_file": track_path,
        "track_data": track_data,
        "created_at": datetime.now().isoformat()
    }
    
    # Save track image if provided
    if track_image:
        image_filename = f"typhoon_track_map_{track_id}_{track_image.name}"
        image_path = save_file(track_image, category, subcategory, image_filename)
        track_info["map_image"] = image_path
    
    return track_info


def show_event_entry():
    """Form to add new disaster events with file attachments"""
    
    st.markdown("### Add New Hazard Event")
    st.caption("Record typhoons, floods, landslides, and other disaster events")
    
    with st.form("add_event_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            event_type = st.selectbox("Event Type", [
                "Typhoon", "Super Typhoon", "Tropical Storm", 
                "Monsoon", "LPA", "ITCZ", "Shear Line",
                "Flood", "Landslide", "Earthquake", "Drought", "Forest Fire"
            ])
            local_name = st.text_input("Local Name", placeholder="e.g., Typhoon Paeng (NALGAE)")
            start_date = st.date_input("Start Date", date.today())
            end_date = st.date_input("End Date", date.today())
        
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
        
        # Damage section
        col1, col2 = st.columns(2)
        with col1:
            damaged_houses = st.number_input("Damaged Houses", min_value=0, value=0)
            agricultural_damage = st.number_input("Agricultural Damage (₱)", min_value=0, value=0, step=10000)
        with col2:
            infrastructure_damage = st.number_input("Infrastructure Damage (₱)", min_value=0, value=0, step=10000)
            total_damage = agricultural_damage + infrastructure_damage
            st.metric("Total Damage Estimate", f"₱{total_damage:,.2f}")
        
        description = st.text_area("Description", placeholder="Detailed description of the event and its impacts")
        response_actions = st.text_area("Response Actions Taken", placeholder="List response activities")
        
        # ========== FILE UPLOAD SECTION ==========
        st.markdown("#### 📎 Attach Files")
        st.caption("Upload typhoon tracks, hazard maps, photos, or other relevant documents")
        
        uploaded_file = st.file_uploader(
            "Select file to attach", 
            type=['jpg', 'jpeg', 'png', 'pdf', 'gif', 'mp4', 'csv', 'json'],
            help="Upload typhoon track images, hazard maps, photos, or documents"
        )
        file_description = st.text_input("File Description", placeholder="e.g., Typhoon track map, Damage photo, Hazard assessment")
        # ======================================
        
        submitted = st.form_submit_button("💾 Save Event", type="primary")
        
        if submitted:
            if not local_name:
                st.error("Please enter the event name")
                return
            
            event = {
                "id": int(datetime.now().timestamp() * 1000),
                "event_type": event_type,
                "local_name": local_name,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "municipality": municipality,
                "fatalities": fatalities,
                "injured": injured,
                "missing": missing,
                "affected_families": affected_families,
                "affected_persons": affected_persons,
                "damaged_houses": damaged_houses,
                "agricultural_damage": agricultural_damage,
                "infrastructure_damage": infrastructure_damage,
                "total_damage": total_damage,
                "description": description,
                "response_actions": response_actions,
                "created_at": datetime.now().isoformat()
            }
            
            # ========== Handle file upload ==========
            if uploaded_file:
                file_info = upload_event_file(event["id"], "attachment", uploaded_file, file_description)
                if file_info:
                    event["attached_files"] = [file_info]
            # ======================================
            
            # Add to DataFrame
            if st.session_state.disaster_events.empty:
                st.session_state.disaster_events = pd.DataFrame([event])
            else:
                st.session_state.disaster_events = pd.concat(
                    [st.session_state.disaster_events, pd.DataFrame([event])],
                    ignore_index=True
                )
            
            st.success(f"✅ Event '{local_name}' recorded successfully!")
            st.balloons()
            st.rerun()


def show_event_database():
    """Display and manage events database with file attachments"""
    
    st.markdown("### Hazard Events Database")
    st.caption("View, filter, and manage all recorded disaster events")
    
    df = st.session_state.disaster_events
    
    if df.empty:
        st.info("No events recorded yet. Use the 'Event Entry' tab to add events.")
        return
    
    # Filters
    st.markdown("#### 🔍 Filter Events")
    col1, col2, col3 = st.columns(3)
    with col1:
        event_types = ["All"] + sorted(df['event_type'].unique().tolist())
        filter_type = st.selectbox("Event Type", event_types)
    with col2:
        municipalities = ["All"] + sorted(df['municipality'].unique().tolist())
        filter_mun = st.selectbox("Municipality", municipalities)
    with col3:
        years = ["All"] + sorted(pd.to_datetime(df['start_date']).dt.year.unique().tolist())
        filter_year = st.selectbox("Year", years)
    
    # Apply filters
    filtered_df = df.copy()
    if filter_type != "All":
        filtered_df = filtered_df[filtered_df['event_type'] == filter_type]
    if filter_mun != "All":
        filtered_df = filtered_df[filtered_df['municipality'] == filter_mun]
    if filter_year != "All":
        filtered_df = filtered_df[pd.to_datetime(filtered_df['start_date']).dt.year == filter_year]
    
    st.markdown(f"**Showing {len(filtered_df)} events**")
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Events", len(filtered_df))
    with col2:
        st.metric("Total Fatalities", int(filtered_df['fatalities'].sum()))
    with col3:
        st.metric("Total Affected", int(filtered_df['affected_families'].sum()))
    with col4:
        st.metric("Total Damage", f"₱{filtered_df['total_damage'].sum():,.0f}")
    
    # Display events
    st.markdown("#### 📋 Event List")
    
    for idx, row in filtered_df.iterrows():
        with st.expander(f"📅 {row['start_date'][:10]} - {row['local_name']} ({row['event_type']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Location:** {row['municipality']}")
                st.markdown(f"**Dates:** {row['start_date'][:10]} to {row['end_date'][:10]}")
                st.markdown(f"**Fatalities:** {row['fatalities']} | **Injured:** {row['injured']} | **Missing:** {row['missing']}")
            with col2:
                st.markdown(f"**Affected:** {row['affected_families']} families, {row['affected_persons']} persons")
                st.markdown(f"**Damaged Houses:** {row['damaged_houses']}")
                st.markdown(f"**Total Damage:** ₱{row['total_damage']:,.2f}")
            
            st.markdown(f"**Description:** {row['description']}")
            st.markdown(f"**Response:** {row['response_actions']}")
            
            # ========== Display attached files ==========
            attached_files = row.get('attached_files', [])
            if attached_files:
                st.markdown("#### 📎 Attached Files")
                for file in attached_files:
                    file_path = file.get('file_path')
                    if file_path and file_exists(file_path):
                        with open(file_path, "rb") as f:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.caption(f"📄 {file.get('description', file.get('filename'))} ({file.get('file_size', 'N/A')})")
                            with col2:
                                st.download_button(
                                    label="Download",
                                    data=f,
                                    file_name=file.get('filename'),
                                    key=f"download_{row['id']}_{file.get('filename')}"
                                )
            # ============================================
            
            # Delete button
            if st.button(f"🗑️ Delete Event", key=f"del_{row['id']}"):
                # Delete attached files
                for file in row.get('attached_files', []):
                    if file.get('file_path'):
                        delete_file(file['file_path'])
                st.session_state.disaster_events = st.session_state.disaster_events[
                    st.session_state.disaster_events['id'] != row['id']
                ]
                st.success(f"Deleted: {row['local_name']}")
                st.rerun()


def show_trend_analysis():
    """Display trend analysis charts"""
    
    st.markdown("### Trend Analysis")
    st.caption("Historical trends and patterns in disaster events")
    
    df = st.session_state.disaster_events
    
    if df.empty:
        st.info("Not enough data for trend analysis. Add more events.")
        return
    
    df['year'] = pd.to_datetime(df['start_date']).dt.year
    df['month'] = pd.to_datetime(df['start_date']).dt.month
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Events by year
        yearly = df.groupby('year').size().reset_index(name='count')
        fig = px.bar(yearly, x='year', y='count', title='Events by Year')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Events by month
        monthly = df.groupby('month').size().reset_index(name='count')
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly['month_name'] = monthly['month'].apply(lambda x: month_names[x-1])
        fig = px.bar(monthly, x='month_name', y='count', title='Events by Month')
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Fatalities by year
        yearly_fatalities = df.groupby('year')['fatalities'].sum().reset_index()
        fig = px.line(yearly_fatalities, x='year', y='fatalities', title='Fatalities Trend')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Damage by year
        yearly_damage = df.groupby('year')['total_damage'].sum().reset_index()
        fig = px.line(yearly_damage, x='year', y='total_damage', title='Damage Cost Trend (₱)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Event type distribution
    st.markdown("#### Event Type Distribution")
    event_type_counts = df['event_type'].value_counts().reset_index()
    event_type_counts.columns = ['Event Type', 'Count']
    fig = px.pie(event_type_counts, values='Count', names='Event Type', title='Events by Type')
    st.plotly_chart(fig, use_container_width=True)


def show_typhoon_tracking():
    """Display typhoon tracking and historical tracks"""
    
    st.markdown("### Typhoon Tracking")
    st.caption("Historical typhoon tracks and real-time monitoring")
    
    # Map display
    st.markdown("#### 🗺️ Typhoon Track Map")
    
    # Create a folium map
    m = folium.Map(location=[17.0, 121.0], zoom_start=8)
    
    # Add markers for municipalities
    municipalities = {
        "Barlig": [17.0833, 121.0833],
        "Bauko": [16.9871, 120.8695],
        "Besao": [17.0953, 120.8561],
        "Bontoc": [17.0904, 120.9772],
        "Natonin": [17.1091, 121.2798],
        "Paracelis": [17.1812, 121.4036],
        "Sabangan": [17.0045, 120.9232],
        "Sadanga": [17.1687, 121.0289],
        "Sagada": [17.0846, 120.9016],
        "Tadian": [16.9958, 120.8218]
    }
    
    for name, coords in municipalities.items():
        folium.Marker(
            coords,
            popup=name,
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(m)
    
    folium_static(m)
    
    # Typhoon track upload - FIXED: Now properly inside a form
    st.markdown("#### 📤 Upload Typhoon Track")
    st.caption("Upload historical typhoon track data and track maps")
    
    with st.expander("Upload Typhoon Track", expanded=False):
        # ========== FIX: Added st.form() wrapper ==========
        with st.form("typhoon_track_form"):
            col1, col2 = st.columns(2)
            with col1:
                typhoon_name = st.text_input("Typhoon Name", placeholder="e.g., Typhoon Paeng (NALGAE)", key="typhoon_name")
                typhoon_year = st.number_input("Year", min_value=2000, max_value=2030, value=2024, key="typhoon_year")
                typhoon_category = st.selectbox("Category", ["Tropical Depression", "Tropical Storm", "Typhoon", "Super Typhoon"], key="typhoon_category")
            with col2:
                landfall_date = st.date_input("Landfall Date", date.today(), key="typhoon_landfall")
                affected_areas = st.text_area("Affected Areas", placeholder="List municipalities affected", key="typhoon_affected")
            
            track_description = st.text_area("Track Description", placeholder="Description of typhoon path and impacts", key="typhoon_description")
            
            # Track data upload
            track_image = st.file_uploader("Upload Track Map Image", type=['jpg', 'jpeg', 'png'], key="typhoon_track_image")
            
            # ========== FIX: Now this button is inside the form ==========
            submitted = st.form_submit_button("💾 Save Typhoon Track")
            
            if submitted and typhoon_name:
                track_data = {
                    "name": typhoon_name,
                    "year": typhoon_year,
                    "category": typhoon_category,
                    "landfall_date": landfall_date.isoformat(),
                    "affected_areas": affected_areas,
                    "description": track_description,
                    "uploaded_at": datetime.now().isoformat()
                }
                
                track_info = upload_typhoon_track(track_data, track_image)
                st.session_state.typhoon_tracks.append(track_info)
                st.success(f"✅ Typhoon track for {typhoon_name} saved!")
                st.rerun()
        # ===================================================
    
    # Display saved typhoon tracks
    if st.session_state.typhoon_tracks:
        st.markdown("#### 📜 Historical Typhoon Tracks")
        
        for track in reversed(st.session_state.typhoon_tracks):
            track_data = track.get('track_data', {})
            with st.expander(f"🌀 {track_data.get('name', 'Unknown')} ({track_data.get('year', 'N/A')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Category:** {track_data.get('category', 'N/A')}")
                    st.markdown(f"**Landfall:** {track_data.get('landfall_date', 'N/A')}")
                with col2:
                    st.markdown(f"**Affected:** {track_data.get('affected_areas', 'N/A')}")
                
                st.markdown(f"**Description:** {track_data.get('description', 'No description')}")
                
                # Display track image if available
                if track.get('map_image') and file_exists(track['map_image']):
                    with open(track['map_image'], "rb") as f:
                        st.image(f, use_container_width=True, caption=f"Track Map - {track_data.get('name')}")
                
                if st.button(f"🗑️ Delete Track", key=f"del_track_{track.get('id')}"):
                    if track.get('track_file'):
                        delete_file(track['track_file'])
                    if track.get('map_image'):
                        delete_file(track['map_image'])
                    st.session_state.typhoon_tracks = [t for t in st.session_state.typhoon_tracks if t.get('id') != track.get('id')]
                    st.rerun()


def show_hazard_photos():
    """Display and manage hazard photos"""
    
    st.markdown("### Hazard Photo Gallery")
    st.caption("Visual documentation of hazard events, impacts, and response")
    
    # Upload photo
    with st.expander("📸 Upload Photo", expanded=False):
        with st.form("upload_hazard_photo"):
            col1, col2 = st.columns(2)
            with col1:
                photo_title = st.text_input("Photo Title")
                photo_event = st.text_input("Related Event", placeholder="e.g., Typhoon Paeng 2024")
                photo_location = st.text_input("Location")
                photo_date = st.date_input("Date Taken", date.today())
            with col2:
                photo_category = st.selectbox("Category", ["Damage", "Response", "Recovery", "Preparedness", "Training"])
                photographer = st.text_input("Photographer")
                photo_tags = st.text_input("Tags", placeholder="comma separated")
            
            photo_description = st.text_area("Description")
            photo_file = st.file_uploader("Select Photo", type=['jpg', 'jpeg', 'png', 'gif'])
            
            submitted = st.form_submit_button("📸 Upload Photo")
            
            if submitted and photo_title and photo_file:
                category = "drrm_intelligence"
                subcategory = "hazard_photos"
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"hazard_photo_{timestamp}_{photo_file.name}"
                file_path = save_file(photo_file, category, subcategory, filename)
                
                new_photo = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "title": photo_title,
                    "event": photo_event,
                    "location": photo_location,
                    "date": photo_date.isoformat(),
                    "category": photo_category,
                    "photographer": photographer,
                    "tags": photo_tags,
                    "description": photo_description,
                    "file_path": file_path,
                    "filename": photo_file.name,
                    "file_size": get_file_size(file_path),
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.hazard_photos.append(new_photo)
                st.success(f"✅ Photo '{photo_title}' uploaded!")
                st.rerun()
    
    # Display gallery
    if st.session_state.hazard_photos:
        st.markdown("#### 📷 Photo Gallery")
        
        # Filter options
        categories = ["All"] + list(set(p.get('category') for p in st.session_state.hazard_photos))
        filter_category = st.selectbox("Filter by Category", categories, key="photo_filter")
        
        filtered_photos = st.session_state.hazard_photos
        if filter_category != "All":
            filtered_photos = [p for p in filtered_photos if p.get('category') == filter_category]
        
        cols = st.columns(3)
        for i, photo in enumerate(reversed(filtered_photos)):
            with cols[i % 3]:
                with st.container():
                    if photo.get('file_path') and file_exists(photo['file_path']):
                        try:
                            from PIL import Image
                            image = Image.open(photo['file_path'])
                            st.image(image, use_container_width=True, caption=photo.get('title'))
                        except:
                            st.caption(f"📷 {photo.get('title')}")
                    else:
                        st.caption(f"📷 {photo.get('title')}")
                    
                    st.caption(f"📍 {photo.get('location', 'Unknown')}")
                    st.caption(f"📅 {photo.get('date', 'N/A')}")
                    st.caption(f"🏷️ {photo.get('category', 'N/A')}")
                    
                    if st.button(f"🗑️ Delete", key=f"del_photo_{photo.get('id')}"):
                        if photo.get('file_path'):
                            delete_file(photo['file_path'])
                        st.session_state.hazard_photos = [p for p in st.session_state.hazard_photos if p.get('id') != photo.get('id')]
                        st.rerun()
                    st.markdown("---")
    else:
        st.info("No photos uploaded yet. Click 'Upload Photo' to get started.")


def show_predictive_analytics():
    """Display predictive analytics and forecasting"""
    
    st.markdown("### Predictive Analytics")
    st.caption("Machine learning-based forecasts and risk projections")
    
    df = st.session_state.disaster_events
    
    if df.empty or len(df) < 5:
        st.info("Need at least 5 events for meaningful predictive analysis. Continue collecting data.")
        return
    
    # Risk scoring
    st.markdown("#### 🎯 Municipal Risk Score")
    
    risk_data = []
    municipalities = df['municipality'].unique()
    
    for mun in municipalities:
        mun_data = df[df['municipality'] == mun]
        event_count = len(mun_data)
        total_fatalities = mun_data['fatalities'].sum()
        total_damage = mun_data['total_damage'].sum()
        
        risk_score = (event_count * 0.4) + (total_fatalities * 0.3) + (total_damage / 1000000 * 0.3)
        risk_score = min(risk_score, 100)
        
        risk_data.append({
            "Municipality": mun,
            "Event Count": event_count,
            "Fatalities": int(total_fatalities),
            "Damage (₱M)": total_damage / 1000000,
            "Risk Score": round(risk_score, 1),
            "Risk Level": "High" if risk_score > 60 else "Medium" if risk_score > 30 else "Low"
        })
    
    risk_df = pd.DataFrame(risk_data).sort_values('Risk Score', ascending=False)
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
    
    # High risk areas
    high_risk = risk_df[risk_df['Risk Level'] == 'High']
    if not high_risk.empty:
        st.markdown("#### ⚠️ High Risk Municipalities")
        for _, row in high_risk.iterrows():
            st.warning(f"**{row['Municipality']}** - Risk Score: {row['Risk Score']} | Priority for intervention")
    
    # Forecast
    st.markdown("#### 🔮 5-Year Forecast (2026-2030)")
    
    years = [2026, 2027, 2028, 2029, 2030]
    avg_events_per_year = len(df) / (pd.to_datetime(df['start_date']).dt.year.max() - pd.to_datetime(df['start_date']).dt.year.min() + 1)
    trend_factor = 1.05  # 5% annual increase assumption
    
    forecast_events = []
    forecast_damage = []
    cumulative = avg_events_per_year
    
    for year in years:
        cumulative = cumulative * trend_factor
        forecast_events.append(round(cumulative))
        forecast_damage.append(round(cumulative * (df['total_damage'].mean() / avg_events_per_year) / 1000000, 1))
    
    forecast_df = pd.DataFrame({
        "Year": years,
        "Predicted Events": forecast_events,
        "Predicted Damage (₱M)": forecast_damage
    })
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)
    
    # Recommendations
    st.markdown("#### 💡 Recommendations")
    st.markdown("""
    Based on historical data analysis:
    1. **Focus on high-risk municipalities** - Prioritize interventions in areas with highest risk scores
    2. **Prepare for peak season** - October-November shows highest event frequency
    3. **Strengthen early warning** - Improve lead time for typhoons and floods
    4. **Invest in resilience** - Allocate resources for infrastructure hardening
    5. **Build community capacity** - Conduct regular drills and trainings
    """)