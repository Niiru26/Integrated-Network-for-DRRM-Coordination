# tabs/risk_profiles.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
from utils.local_storage import save_file, delete_file, get_file_size, file_exists

def show():
    """Display Risk Profiles Tab - CDRA, Landslide Susceptibility, and Risk Assessments"""
    
    st.markdown("# 📊 Risk Profiles")
    st.caption("Climate and Disaster Risk Assessment (CDRA), Landslide Susceptibility, and Barangay/Municipal Risk Profiles")
    
    # Initialize session state
    if 'cdra_documents' not in st.session_state:
        st.session_state.cdra_documents = []
    
    if 'landslide_assessments' not in st.session_state:
        st.session_state.landslide_assessments = []
    
    if 'municipal_risk_profiles' not in st.session_state:
        st.session_state.municipal_risk_profiles = []
    
    if 'barangay_risk_profiles' not in st.session_state:
        st.session_state.barangay_risk_profiles = []
    
    if 'provincial_risk_maps' not in st.session_state:
        st.session_state.provincial_risk_maps = []
    
    # Municipalities list
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 CDRA Documents",
        "🏔️ Landslide Assessment",
        "🏘️ Municipal Risk Profiles",
        "🗺️ Barangay Risk Profiles",
        "🗺️ Provincial Risk Maps",
        "📈 CDRA Summary",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_cdra_documents(municipalities)
    
    with tab2:
        show_landslide_assessments(municipalities)
    
    with tab3:
        show_municipal_risk_profiles(municipalities)
    
    with tab4:
        show_barangay_risk_profiles()
    
    with tab5:
        show_provincial_risk_maps()
    
    with tab6:
        show_cdra_summary()
    
    with tab7:
        show_related_modules()


def show_cdra_documents(municipalities):
    """CDRA documents for province and municipalities"""
    
    st.markdown("### Climate and Disaster Risk Assessment (CDRA)")
    st.caption("CDRA documents for Mountain Province and all 10 municipalities")
    
    # Add CDRA document
    with st.expander("➕ Add CDRA Document", expanded=False):
        with st.form("add_cdra_form"):
            col1, col2 = st.columns(2)
            with col1:
                level = st.selectbox("Level", ["Provincial", "Municipal"])
                
                # Fix: Handle municipality selection properly
                if level == "Municipal":
                    municipality = st.selectbox("Municipality", [""] + municipalities)
                else:
                    st.text("Provincial Level")
                    municipality = "Provincial"
                
                year = st.number_input("Year", min_value=2015, max_value=2030, value=datetime.now().year)
            with col2:
                status = st.selectbox("Status", ["Draft", "For Approval", "Approved", "Under Review"])
                version = st.text_input("Version", placeholder="v1.0")
            
            description = st.text_area("Description", placeholder="Brief description of the CDRA document")
            uploaded_file = st.file_uploader("Upload CDRA Document", type=['pdf', 'docx', 'doc'], key="cdra_upload")
            
            submitted = st.form_submit_button("💾 Save CDRA")
            
            if submitted and uploaded_file:
                # Save file
                folder = f"local_storage/risk_profiles/cdra"
                os.makedirs(folder, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"CDRA_{level}_{municipality if municipality else 'Provincial'}_{year}_{timestamp}.pdf"
                file_path = os.path.join(folder, filename)
                
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                new_doc = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "level": level,
                    "municipality": municipality if level == "Municipal" else "Provincial",
                    "year": year,
                    "status": status,
                    "version": version,
                    "description": description,
                    "file_path": file_path,
                    "filename": filename,
                    "file_size": get_file_size(file_path),
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.cdra_documents.append(new_doc)
                st.success(f"✅ CDRA document added!")
                st.rerun()
    
    # Display CDRA documents
    if st.session_state.cdra_documents:
        df = pd.DataFrame(st.session_state.cdra_documents)
        
        # Filter by level
        col1, col2 = st.columns(2)
        with col1:
            level_filter = st.selectbox("Filter by Level", ["All", "Provincial", "Municipal"])
        with col2:
            if level_filter == "Municipal":
                mun_filter = st.selectbox("Filter by Municipality", ["All"] + municipalities)
            else:
                mun_filter = "All"
        
        filtered = df.copy()
        if level_filter != "All":
            filtered = filtered[filtered['level'] == level_filter]
        if level_filter == "Municipal" and mun_filter != "All":
            filtered = filtered[filtered['municipality'] == mun_filter]
        
        st.dataframe(filtered[['level', 'municipality', 'year', 'status', 'version']], use_container_width=True, hide_index=True)
        
        # Download/Delete
        for doc in filtered.to_dict('records'):
            with st.expander(f"📄 {doc['level']} - {doc.get('municipality', 'Provincial')} ({doc['year']})"):
                st.markdown(f"**Status:** {doc['status']}")
                st.markdown(f"**Version:** {doc['version']}")
                st.markdown(f"**Description:** {doc.get('description', 'No description')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if doc['file_path'] and os.path.exists(doc['file_path']):
                        with open(doc['file_path'], "rb") as f:
                            st.download_button("📥 Download", f, file_name=os.path.basename(doc['file_path']), key=f"dl_cdra_{doc['id']}")
                with col2:
                    if st.button(f"🗑️ Delete", key=f"del_cdra_{doc['id']}"):
                        if doc['file_path'] and os.path.exists(doc['file_path']):
                            os.remove(doc['file_path'])
                        st.session_state.cdra_documents = [d for d in st.session_state.cdra_documents if d['id'] != doc['id']]
                        st.rerun()
    else:
        st.info("No CDRA documents uploaded yet.")

def show_landslide_assessments(municipalities):
    """Rain-induced landslide susceptibility assessments for schools and facilities"""
    
    st.markdown("### Rain-Induced Landslide Susceptibility Assessment")
    st.caption("Assessment ratings for schools and government facilities")
    
    # Rating definitions
    ratings = {
        "Stable": "🟢 No significant landslide risk",
        "Marginally Stable": "🟡 Low landslide risk - monitor conditions",
        "Susceptible": "🟠 Moderate landslide risk - mitigation needed",
        "Highly Susceptible": "🔴 High landslide risk - immediate action required"
    }
    
    # Add assessment
    with st.expander("➕ Add Landslide Assessment", expanded=False):
        with st.form("add_landslide_form"):
            col1, col2 = st.columns(2)
            with col1:
                facility_type = st.selectbox("Facility Type", ["School", "Government Facility", "Health Center", "Barangay Hall", "Other"])
                facility_name = st.text_input("Facility Name")
                municipality = st.selectbox("Municipality", municipalities)
                barangay = st.text_input("Barangay")
            with col2:
                rating = st.selectbox("Susceptibility Rating", list(ratings.keys()))
                proximity_to_fault = st.selectbox("Proximity to Active Fault", ["Within 5km", "5-10km", "10-20km", ">20km", "Not Applicable"])
                assessment_date = st.date_input("Assessment Date", datetime.now())
            
            recommendations = st.text_area("Recommendations", placeholder="Mitigation measures and recommendations")
            uploaded_file = st.file_uploader("Upload Assessment Report", type=['pdf', 'docx'], key="landslide_upload")
            
            submitted = st.form_submit_button("💾 Save Assessment")
            
            if submitted and facility_name:
                new_assessment = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "facility_type": facility_type,
                    "facility_name": facility_name,
                    "municipality": municipality,
                    "barangay": barangay,
                    "rating": rating,
                    "rating_icon": ratings[rating],
                    "proximity_to_fault": proximity_to_fault,
                    "assessment_date": assessment_date.isoformat(),
                    "recommendations": recommendations,
                    "file_path": None,
                    "created_at": datetime.now().isoformat()
                }
                
                if uploaded_file:
                    folder = "local_storage/risk_profiles/landslide_assessments"
                    os.makedirs(folder, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"Landslide_{facility_name.replace(' ', '_')}_{timestamp}.pdf"
                    file_path = os.path.join(folder, filename)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    new_assessment["file_path"] = file_path
                    new_assessment["filename"] = filename
                
                st.session_state.landslide_assessments.append(new_assessment)
                st.success(f"✅ Assessment for {facility_name} added!")
                st.rerun()
    
    # Display assessments
    if st.session_state.landslide_assessments:
        df = pd.DataFrame(st.session_state.landslide_assessments)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            mun_filter = st.selectbox("Filter by Municipality", ["All"] + municipalities)
        with col2:
            rating_filter = st.selectbox("Filter by Rating", ["All"] + list(ratings.keys()))
        
        filtered = df.copy()
        if mun_filter != "All":
            filtered = filtered[filtered['municipality'] == mun_filter]
        if rating_filter != "All":
            filtered = filtered[filtered['rating'] == rating_filter]
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assessed", len(filtered))
        with col2:
            high_risk = len(filtered[filtered['rating'] == 'Highly Susceptible'])
            st.metric("High Risk Facilities", high_risk, delta="⚠️" if high_risk > 0 else None)
        with col3:
            stable = len(filtered[filtered['rating'] == 'Stable'])
            st.metric("Stable Facilities", stable)
        
        # Display table
        st.dataframe(filtered[['facility_name', 'facility_type', 'municipality', 'barangay', 'rating', 'proximity_to_fault']], 
                     use_container_width=True, hide_index=True)
        
        # Detailed view
        for assessment in filtered.to_dict('records'):
            with st.expander(f"🏫 {assessment['facility_name']} - {assessment['rating']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Type:** {assessment['facility_type']}")
                    st.markdown(f"**Location:** {assessment['barangay']}, {assessment['municipality']}")
                    st.markdown(f"**Rating:** {assessment['rating']} - {assessment['rating_icon']}")
                with col2:
                    st.markdown(f"**Fault Proximity:** {assessment['proximity_to_fault']}")
                    st.markdown(f"**Assessment Date:** {assessment['assessment_date'][:10]}")
                
                st.markdown(f"**Recommendations:** {assessment.get('recommendations', 'No recommendations')}")
                
                if assessment.get('file_path') and os.path.exists(assessment['file_path']):
                    with open(assessment['file_path'], "rb") as f:
                        st.download_button("📥 Download Report", f, file_name=os.path.basename(assessment['file_path']))
                
                if st.button(f"🗑️ Delete", key=f"del_landslide_{assessment['id']}"):
                    if assessment.get('file_path') and os.path.exists(assessment['file_path']):
                        os.remove(assessment['file_path'])
                    st.session_state.landslide_assessments = [a for a in st.session_state.landslide_assessments if a['id'] != assessment['id']]
                    st.rerun()
    else:
        st.info("No landslide assessments added yet.")


def show_municipal_risk_profiles(municipalities):
    """Risk profiles for each municipality (1-2 page summaries + maps)"""
    
    st.markdown("### Municipal Risk Profiles")
    st.caption("Risk profiles for all 10 municipalities of Mountain Province")
    
    # Add municipal risk profile
    with st.expander("➕ Add Municipal Risk Profile", expanded=False):
        with st.form("add_muni_profile"):
            col1, col2 = st.columns(2)
            with col1:
                municipality = st.selectbox("Municipality", municipalities)
                year = st.number_input("Year", min_value=2020, max_value=2030, value=datetime.now().year)
            with col2:
                risk_level = st.selectbox("Overall Risk Level", ["Low", "Medium", "High", "Very High"])
                population_affected = st.number_input("Population at Risk", min_value=0, value=0)
            
            summary = st.text_area("Risk Summary", placeholder="Summary of key risks in the municipality", height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                profile_file = st.file_uploader("Upload Risk Profile (PDF)", type=['pdf'], key="profile_file")
            with col2:
                map_file = st.file_uploader("Upload Risk Map", type=['jpg', 'jpeg', 'png', 'pdf'], key="map_file")
            
            submitted = st.form_submit_button("💾 Save Profile")
            
            if submitted and municipality:
                new_profile = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "municipality": municipality,
                    "year": year,
                    "risk_level": risk_level,
                    "population_affected": population_affected,
                    "summary": summary,
                    "created_at": datetime.now().isoformat()
                }
                
                # Save profile file
                if profile_file:
                    folder = "local_storage/risk_profiles/municipal"
                    os.makedirs(folder, exist_ok=True)
                    filename = f"RiskProfile_{municipality}_{year}.pdf"
                    file_path = os.path.join(folder, filename)
                    with open(file_path, "wb") as f:
                        f.write(profile_file.getbuffer())
                    new_profile["profile_path"] = file_path
                
                # Save map file
                if map_file:
                    folder = "local_storage/risk_profiles/municipal_maps"
                    os.makedirs(folder, exist_ok=True)
                    ext = map_file.name.split('.')[-1]
                    filename = f"RiskMap_{municipality}_{year}.{ext}"
                    file_path = os.path.join(folder, filename)
                    with open(file_path, "wb") as f:
                        f.write(map_file.getbuffer())
                    new_profile["map_path"] = file_path
                
                st.session_state.municipal_risk_profiles.append(new_profile)
                st.success(f"✅ Risk profile for {municipality} added!")
                st.rerun()
    
    # Display municipal profiles
    if st.session_state.municipal_risk_profiles:
        df = pd.DataFrame(st.session_state.municipal_risk_profiles)
        st.dataframe(df[['municipality', 'year', 'risk_level', 'population_affected']], use_container_width=True, hide_index=True)
        
        for profile in df.to_dict('records'):
            with st.expander(f"🏘️ {profile['municipality']} - Risk Level: {profile['risk_level']}"):
                st.markdown(f"**Year:** {profile['year']}")
                st.markdown(f"**Population at Risk:** {profile['population_affected']:,}")
                st.markdown(f"**Summary:** {profile['summary']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if profile.get('profile_path') and os.path.exists(profile['profile_path']):
                        with open(profile['profile_path'], "rb") as f:
                            st.download_button("📥 Download Full Profile", f, file_name=os.path.basename(profile['profile_path']))
                with col2:
                    if profile.get('map_path') and os.path.exists(profile['map_path']):
                        with open(profile['map_path'], "rb") as f:
                            st.download_button("🗺️ Download Risk Map", f, file_name=os.path.basename(profile['map_path']))
                
                if st.button(f"🗑️ Delete", key=f"del_muni_{profile['id']}"):
                    if profile.get('profile_path') and os.path.exists(profile['profile_path']):
                        os.remove(profile['profile_path'])
                    if profile.get('map_path') and os.path.exists(profile['map_path']):
                        os.remove(profile['map_path'])
                    st.session_state.municipal_risk_profiles = [p for p in st.session_state.municipal_risk_profiles if p['id'] != profile['id']]
                    st.rerun()
    else:
        st.info("No municipal risk profiles added yet.")


def show_barangay_risk_profiles():
    """Risk profiles for all 144 barangays"""
    
    st.markdown("### Barangay Risk Profiles")
    st.caption("Risk profiles for all 144 barangays of Mountain Province")
    
    # Municipalities list
    municipalities = ["Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # Add barangay risk profile
    with st.expander("➕ Add Barangay Risk Profile", expanded=False):
        with st.form("add_barangay_profile"):
            col1, col2, col3 = st.columns(3)
            with col1:
                municipality = st.selectbox("Municipality", municipalities)
                barangay = st.text_input("Barangay Name")
            with col2:
                risk_level = st.selectbox("Risk Level", ["Low", "Medium", "High", "Very High"])
                population = st.number_input("Population", min_value=0, value=0)
            with col3:
                landslide_risk = st.selectbox("Landslide Risk", ["Low", "Medium", "High", "Very High", "Not Applicable"])
                flood_risk = st.selectbox("Flood Risk", ["Low", "Medium", "High", "Very High", "Not Applicable"])
            
            recommendations = st.text_area("Recommendations", placeholder="Key recommendations for the barangay")
            uploaded_file = st.file_uploader("Upload Barangay Risk Profile", type=['pdf', 'docx'], key="barangay_upload")
            
            submitted = st.form_submit_button("💾 Save Barangay Profile")
            
            if submitted and barangay:
                new_profile = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "municipality": municipality,
                    "barangay": barangay,
                    "risk_level": risk_level,
                    "population": population,
                    "landslide_risk": landslide_risk,
                    "flood_risk": flood_risk,
                    "recommendations": recommendations,
                    "created_at": datetime.now().isoformat()
                }
                
                if uploaded_file:
                    folder = "local_storage/risk_profiles/barangay"
                    os.makedirs(folder, exist_ok=True)
                    filename = f"BarangayRisk_{municipality}_{barangay}.pdf"
                    file_path = os.path.join(folder, filename)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    new_profile["file_path"] = file_path
                
                st.session_state.barangay_risk_profiles.append(new_profile)
                st.success(f"✅ Risk profile for {barangay}, {municipality} added!")
                st.rerun()
    
    # Display barangay profiles
    if st.session_state.barangay_risk_profiles:
        df = pd.DataFrame(st.session_state.barangay_risk_profiles)
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            mun_filter = st.selectbox("Filter by Municipality", ["All"] + municipalities)
        with col2:
            risk_filter = st.selectbox("Filter by Risk Level", ["All", "Low", "Medium", "High", "Very High"])
        
        filtered = df.copy()
        if mun_filter != "All":
            filtered = filtered[filtered['municipality'] == mun_filter]
        if risk_filter != "All":
            filtered = filtered[filtered['risk_level'] == risk_filter]
        
        st.metric("Total Barangays", len(filtered))
        st.dataframe(filtered[['barangay', 'municipality', 'risk_level', 'population', 'landslide_risk', 'flood_risk']], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("No barangay risk profiles added yet.")


def show_provincial_risk_maps():
    """Provincial-level risk maps for various elements at risk"""
    
    st.markdown("### Provincial Risk Maps")
    st.caption("Risk maps for population, urban areas, natural resources, critical facilities, lifelines, and other elements at risk")
    
    risk_categories = [
        "Population Risk",
        "Urban Use Area Risk",
        "Natural Resource-Based Production Area Risk",
        "Critical Point Facilities Risk",
        "Lifeline Utilities Risk",
        "Other Elements at Risk"
    ]
    
    # Add provincial risk map
    with st.expander("➕ Add Provincial Risk Map", expanded=False):
        with st.form("add_provincial_map"):
            col1, col2 = st.columns(2)
            with col1:
                risk_category = st.selectbox("Risk Category", risk_categories)
                year = st.number_input("Year", min_value=2020, max_value=2030, value=datetime.now().year)
            with col2:
                scale = st.text_input("Map Scale", placeholder="e.g., 1:50,000")
                projection = st.text_input("Projection", placeholder="e.g., UTM Zone 51N")
            
            description = st.text_area("Description", placeholder="Description of the risk map")
            uploaded_file = st.file_uploader("Upload Risk Map", type=['jpg', 'jpeg', 'png', 'pdf'], key="provincial_map")
            
            submitted = st.form_submit_button("💾 Save Map")
            
            if submitted and uploaded_file:
                folder = "local_storage/risk_profiles/provincial_maps"
                os.makedirs(folder, exist_ok=True)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Provincial_{risk_category.replace(' ', '_')}_{timestamp}.pdf"
                file_path = os.path.join(folder, filename)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                new_map = {
                    "id": int(datetime.now().timestamp() * 1000),
                    "risk_category": risk_category,
                    "year": year,
                    "scale": scale,
                    "projection": projection,
                    "description": description,
                    "file_path": file_path,
                    "file_size": get_file_size(file_path),
                    "uploaded_at": datetime.now().isoformat()
                }
                st.session_state.provincial_risk_maps.append(new_map)
                st.success(f"✅ {risk_category} map added!")
                st.rerun()
    
    # Display provincial maps
    if st.session_state.provincial_risk_maps:
        df = pd.DataFrame(st.session_state.provincial_risk_maps)
        st.dataframe(df[['risk_category', 'year', 'scale', 'file_size']], use_container_width=True, hide_index=True)
        
        for map_item in df.to_dict('records'):
            with st.expander(f"🗺️ {map_item['risk_category']} ({map_item['year']})"):
                st.markdown(f"**Scale:** {map_item['scale']}")
                st.markdown(f"**Projection:** {map_item['projection']}")
                st.markdown(f"**Description:** {map_item['description']}")
                
                if map_item['file_path'] and os.path.exists(map_item['file_path']):
                    with open(map_item['file_path'], "rb") as f:
                        st.download_button("📥 Download Map", f, file_name=os.path.basename(map_item['file_path']))
                
                if st.button(f"🗑️ Delete", key=f"del_prov_{map_item['id']}"):
                    if map_item['file_path'] and os.path.exists(map_item['file_path']):
                        os.remove(map_item['file_path'])
                    st.session_state.provincial_risk_maps = [m for m in st.session_state.provincial_risk_maps if m['id'] != map_item['id']]
                    st.rerun()
    else:
        st.info("No provincial risk maps uploaded yet.")


def show_cdra_summary():
    """CDRA summary for rain-induced landslide and riverine flood risk to population"""
    
    st.markdown("### CDRA Summary Reports")
    st.caption("Summary of rain-induced landslide and riverine flood risk to population")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏔️ Rain-Induced Landslide Risk to Population")
        st.markdown("""
        **Risk Levels by Municipality:**
        
        | Municipality | Risk Level | Affected Population |
        |--------------|------------|---------------------|
        | Barlig | High | ~2,500 |
        | Bauko | Medium | ~8,000 |
        | Besao | High | ~900 |
        | Bontoc | Medium | ~6,000 |
        | Natonin | High | ~3,500 |
        | Paracelis | Very High | ~12,000 |
        | Sabangan | Medium | ~2,500 |
        | Sadanga | High | ~3,000 |
        | Sagada | High | ~4,000 |
        | Tadian | Medium | ~2,500 |
        """)
        
        st.info("**Recommendations:** Prioritize early warning systems and pre-emptive evacuation in Very High and High risk municipalities.")
    
    with col2:
        st.markdown("#### 🌊 Riverine Flood Risk to Population")
        st.markdown("""
        **Risk Levels by Municipality:**
        
        | Municipality | Risk Level | Affected Population |
        |--------------|------------|---------------------|
        | Barlig | Medium | ~1,200 |
        | Bauko | Low | ~500 |
        | Besao | Low | ~200 |
        | Bontoc | Medium | ~2,500 |
        | Natonin | High | ~2,800 |
        | Paracelis | Very High | ~15,000 |
        | Sabangan | Low | ~800 |
        | Sadanga | Low | ~500 |
        | Sagada | Low | ~300 |
        | Tadian | Low | ~400 |
        """)
        
        st.warning("**Critical Concern:** Paracelis shows Very High flood risk affecting approximately 15,000 people. Immediate flood risk management interventions required.")
    
    # Upload summary documents
    st.markdown("---")
    st.markdown("#### 📄 Upload CDRA Summary Documents")
    
    col1, col2 = st.columns(2)
    with col1:
        landslide_summary = st.file_uploader("Landslide Risk Summary Report", type=['pdf', 'docx'], key="landslide_summary")
        if landslide_summary:
            folder = "local_storage/risk_profiles/cdra_summaries"
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, f"Landslide_Risk_Summary_{datetime.now().strftime('%Y%m%d')}.pdf")
            with open(file_path, "wb") as f:
                f.write(landslide_summary.getbuffer())
            st.success("✅ Landslide summary uploaded!")
    
    with col2:
        flood_summary = st.file_uploader("Flood Risk Summary Report", type=['pdf', 'docx'], key="flood_summary")
        if flood_summary:
            folder = "local_storage/risk_profiles/cdra_summaries"
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, f"Flood_Risk_Summary_{datetime.now().strftime('%Y%m%d')}.pdf")
            with open(file_path, "wb") as f:
                f.write(flood_summary.getbuffer())
            st.success("✅ Flood summary uploaded!")


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How Risk Profiles connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Plan Management
        - Risk profiles inform DRRM plan priorities
        - High-risk areas prioritized for interventions
        - Landslide risk data for infrastructure planning
        
        ### 📊 DRRM Intelligence
        - Risk data feeds into hazard models
        - Vulnerability assessment validation
        - Predictive analytics inputs
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 Climate Change
        - CDRA informs CCA planning
        - Climate risk profiles for adaptation
        - Vulnerability mapping for resilience building
        
        ### 🗺️ Geospatial Library
        - Risk maps stored and referenced
        - Hazard maps for visualization
        - GIS data integration
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col2:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()
    with col3:
        if st.button("🗺️ Go to Geospatial Library", use_container_width=True):
            st.session_state.navigation = "🗺️ GEOSPATIAL LIBRARY"
            st.rerun()