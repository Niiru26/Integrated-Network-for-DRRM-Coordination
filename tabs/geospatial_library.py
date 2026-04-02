# tabs/geospatial_library.py
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import base64
import platform
import subprocess
from PIL import Image
from utils.local_storage import save_file, delete_file, get_file_size, file_exists

# Add this function at the top, after imports
def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def get_file_size(file_path):
    """Get file size in human-readable format"""
    if not file_path or not os.path.exists(file_path):
        return "0 B"
    return format_file_size(os.path.getsize(file_path))

def show():
    """Display Geospatial Library Tab - Repository of GIS-generated maps"""
    
    st.markdown("# 🗺️ Geospatial Library")
    st.caption("Repository of GIS-based hazard, risk, exposure, vulnerability, and base maps")
    
    # Initialize session state
    if 'gis_maps' not in st.session_state:
        st.session_state.gis_maps = []
    
    # Map categories
    categories = {
        "Base Map": "Base maps showing administrative boundaries, topography, and infrastructure",
        "Hazard Map": "Maps showing specific hazard areas (flood, landslide, earthquake, etc.)",
        "Risk Map": "Maps showing combined risk from multiple hazards",
        "Exposure Map": "Maps showing elements at risk (population, assets, infrastructure)",
        "Vulnerability Map": "Maps showing vulnerability factors (social, economic, physical)",
        "Other Maps": "Special purpose maps and thematic maps"
    }
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Map Gallery",
        "📤 Upload Map",
        "📊 Map Categories",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_map_gallery(categories)
    
    with tab2:
        show_upload_map(categories)
    
    with tab3:
        show_map_categories(categories)
    
    with tab4:
        show_related_modules()


def show_map_gallery(categories):
    """Display the map gallery with filtering and preview"""
    
    st.markdown("### 🗺️ Map Gallery")
    st.caption("Browse, preview, and download GIS-generated maps")
    
    maps = st.session_state.gis_maps
    
    if not maps:
        st.info("No maps uploaded yet. Use the 'Upload Map' tab to add GIS maps.")
        return
    
    df = pd.DataFrame(maps)
    
    # ========== FILTERS ==========
    st.markdown("#### 🔍 Search & Filter")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        filter_categories = ["All"] + list(categories.keys())
        filter_category = st.selectbox("Map Category", filter_categories, key="filter_category")
    
    with col2:
        years = ["All"] + sorted(df['year'].unique().tolist()) if 'year' in df.columns else ["All"]
        filter_year = st.selectbox("Year", years, key="filter_year")
    
    with col3:
        municipalities = ["All"] + sorted(df['municipality'].dropna().unique().tolist()) if 'municipality' in df.columns else ["All"]
        filter_municipality = st.selectbox("Municipality", municipalities, key="filter_municipality")
    
    with col4:
        search_term = st.text_input("Search", placeholder="Title, description...", key="search_maps")
    
    # ========== APPLY FILTERS ==========
    filtered_df = df.copy()
    
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == filter_category]
    
    if filter_year != "All":
        filtered_df = filtered_df[filtered_df['year'] == int(filter_year)]
    
    if filter_municipality != "All":
        filtered_df = filtered_df[filtered_df['municipality'] == filter_municipality]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False) |
            filtered_df['description'].str.contains(search_term, case=False) |
            filtered_df['location'].str.contains(search_term, case=False)
        ]
    
    # ========== SUMMARY STATS ==========
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Maps", len(filtered_df))
    with col2:
        st.metric("Categories", filtered_df['category'].nunique() if not filtered_df.empty else 0)
    with col3:
        st.metric("Municipalities", filtered_df['municipality'].nunique() if not filtered_df.empty else 0)
    with col4:
        total_size = sum([item.get('file_size_bytes', 0) for item in filtered_df.to_dict('records')]) if not filtered_df.empty else 0
        st.metric("Total Size", format_file_size(total_size))
    
    st.markdown("---")
    
    # ========== DISPLAY MAPS IN GRID ==========
    if not filtered_df.empty:
        st.markdown("#### 🖼️ Map Gallery")
        
        # Display in grid of 3 columns
        cols = st.columns(3)
        
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"**{row['title']}**")
                    st.caption(f"📁 {row['category']} | 📅 {row['year']}")
                    st.caption(f"📍 {row.get('municipality', 'Province-wide')}")
                    
                    # Preview image if available
                    if row.get('file_path') and row['file_extension'].lower() in ['jpg', 'jpeg', 'png', 'gif']:
                        try:
                            if os.path.exists(row['file_path']):
                                image = Image.open(row['file_path'])
                                # Resize for thumbnail
                                image.thumbnail((300, 200))
                                st.image(image, use_container_width=True)
                            else:
                                st.caption("🖼️ [Image file not found]")
                        except Exception as e:
                            st.caption(f"🖼️ Preview not available")
                    else:
                        st.caption(f"📄 {row['file_extension']} file")
                    
                    st.caption(f"📏 Scale: {row.get('scale', 'N/A')} | 🗺️ {row.get('projection', 'N/A')}")
                    st.caption(f"📝 {row['description'][:80]}..." if len(row['description']) > 80 else f"📝 {row['description']}")
                    
                    # Action buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        # Open/View button
                        if st.button(f"👁️ View", key=f"view_{row['id']}"):
                            open_map_file(row['file_path'])
                            st.success(f"Opening: {row['title']}")
                    
                    with col2:
                        # Download button
                        if row['file_path'] and os.path.exists(row['file_path']):
                            with open(row['file_path'], "rb") as f:
                                st.download_button(
                                    label="📥 Download",
                                    data=f,
                                    file_name=os.path.basename(row['file_path']),
                                    key=f"download_{row['id']}"
                                )
                    
                    with col3:
                        # Delete button
                        if st.button(f"🗑️ Delete", key=f"delete_{row['id']}"):
                            if row['file_path'] and os.path.exists(row['file_path']):
                                os.remove(row['file_path'])
                            st.session_state.gis_maps = [m for m in st.session_state.gis_maps if m['id'] != row['id']]
                            st.success(f"Deleted: {row['title']}")
                            st.rerun()
                    
                    st.markdown("---")
        
        # ========== TABLE VIEW ==========
        st.markdown("#### 📋 Map List (Table View)")
        
        display_df = filtered_df[['title', 'category', 'year', 'municipality', 'scale', 'file_extension', 'file_size']].copy()
        display_df.columns = ['Title', 'Category', 'Year', 'Municipality', 'Scale', 'Format', 'Size']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    else:
        st.info("No maps match your filters.")


def show_upload_map(categories):
    """Upload new GIS maps with clear form after submission"""
    
    st.markdown("### 📤 Upload GIS Map")
    st.caption("Add new maps to the library (JPEG, PNG, PDF formats)")
    
    municipalities = ["Province-wide", "Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # Use clear_on_submit=True to reset form after submission
    with st.form("upload_map_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Map Title *", placeholder="e.g., Provincial Landslide Hazard Map")
            category = st.selectbox("Category *", list(categories.keys()))
            year = st.number_input("Year *", min_value=2000, max_value=2030, value=datetime.now().year)
            municipality = st.selectbox("Municipality/Area", municipalities)
        
        with col2:
            scale = st.text_input("Map Scale", placeholder="e.g., 1:50,000")
            projection = st.text_input("Projection", placeholder="e.g., UTM Zone 51N")
            source = st.text_input("Data Source", placeholder="e.g., MGB, PAGASA, LGU")
            tags = st.text_input("Tags", placeholder="comma separated: landslide, hazard, barlig")
        
        description = st.text_area("Description", placeholder="Brief description of the map and its purpose", height=100)
        
        uploaded_file = st.file_uploader("Select map file", type=['jpg', 'jpeg', 'png', 'pdf'])
        
        submitted = st.form_submit_button("📤 Upload Map", type="primary")
        
        if submitted and title and uploaded_file:
            # Create folder structure
            category_folder = category.replace(" ", "_")
            folder = f"local_storage/geospatial_library/{category_folder}"
            os.makedirs(folder, exist_ok=True)
            
            # Save file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
            extension = uploaded_file.name.split('.')[-1].lower()
            filename = f"{timestamp}_{safe_title}.{extension}"
            file_path = os.path.join(folder, filename)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Get file info - use the format_file_size function
            file_size_bytes = os.path.getsize(file_path)
            file_size = format_file_size(file_size_bytes)
            
            # Create metadata record
            new_map = {
                "id": int(datetime.now().timestamp() * 1000),
                "title": title,
                "category": category,
                "year": year,
                "municipality": municipality,
                "scale": scale,
                "projection": projection,
                "source": source,
                "tags": tags,
                "description": description,
                "file_path": file_path,
                "filename": filename,
                "file_extension": extension.upper(),
                "file_size": file_size,
                "file_size_bytes": file_size_bytes,
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": datetime.now().isoformat()
            }
            
            st.session_state.gis_maps.append(new_map)
            st.success(f"✅ Map '{title}' uploaded successfully!")
            st.balloons()
            st.rerun()
        
        elif submitted and not title:
            st.error("Please enter a map title")
        
        elif submitted and not uploaded_file:
            st.error("Please select a file to upload")

def show_map_categories(categories):
    """Display information about map categories and 3D PRISM"""
    
    st.markdown("### 📊 Map Categories")
    st.caption("Understanding the different types of GIS maps in our library")
    
    # Category descriptions
    for category, description in categories.items():
        with st.expander(f"🗺️ {category}"):
            st.markdown(description)
            
            # Count maps in this category
            count = len([m for m in st.session_state.gis_maps if m.get('category') == category])
            st.caption(f"📊 {count} maps in this category")
            
            # List maps in this category
            if count > 0:
                maps_in_cat = [m for m in st.session_state.gis_maps if m.get('category') == category]
                for m in maps_in_cat[:5]:  # Show first 5
                    st.markdown(f"- **{m['title']}** ({m['year']}) - {m.get('municipality', 'Province-wide')}")
                if len(maps_in_cat) > 5:
                    st.caption(f"... and {len(maps_in_cat) - 5} more")
    
    st.markdown("---")
    
    # 3D PRISM Information
    st.markdown("### 🏔️ About the 3D PRISM Maps")
    st.info("""
    The maps in this library are products of the **Three-Dimensional Precision Risk and Susceptibility Mapping (3D PRISM)** 
    initiative launched in 2018. These maps form the foundational geospatial intelligence for the INDC platform.
    
    **3D PRISM Components:**
    - **Hazard Maps** - Identify areas prone to specific hazards
    - **Exposure Maps** - Show elements at risk (population, assets)
    - **Vulnerability Maps** - Highlight susceptible areas/communities
    - **Risk Maps** - Combine hazard, exposure, and vulnerability
    - **Base Maps** - Administrative boundaries, topography, infrastructure
    
    These maps have been developed using:
    - GIS technology and satellite imagery
    - Historical hazard data (20+ years)
    - Machine learning for susceptibility modeling
    - Local validation and ground truthing
    """)
    
    # Statistics
    if st.session_state.gis_maps:
        st.markdown("### 📈 Library Statistics")
        
        df = pd.DataFrame(st.session_state.gis_maps)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Maps", len(df))
        with col2:
            st.metric("Categories Used", df['category'].nunique())
        with col3:
            st.metric("Municipalities Covered", df['municipality'].nunique() if 'municipality' in df.columns else 0)
        
        # Category distribution chart
        cat_counts = df['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        st.dataframe(cat_counts, use_container_width=True, hide_index=True)


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How Geospatial Library connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 DRRM Intelligence
        - Hazard maps feed into risk analysis
        - Maps visualize event impacts
        - Spatial data for predictive analytics
        
        ### 📋 Plan Management
        - Risk maps inform plan priorities
        - Hazard maps for vulnerability assessment
        - Geospatial data for PPAs
        """)
    
    with col2:
        st.markdown("""
        ### 🌍 Climate Change
        - Climate hazard maps for adaptation planning
        - Vulnerability maps for CCA prioritization
        - Exposure maps for climate risk assessment
        
        ### 📁 Knowledge Repository
        - Store GIS methodology documents
        - Technical reports on mapping
        - Reference materials
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()
    with col2:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col3:
        if st.button("🌍 Go to Climate Change", use_container_width=True):
            st.session_state.navigation = "🌍 CLIMATE CHANGE"
            st.rerun()


def open_map_file(file_path):
    """Open a map file with the default system application"""
    import platform
    import subprocess
    import os
    
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux (including Streamlit Cloud)
            # On Streamlit Cloud, we can't open files locally
            # Instead, provide download option
            st.warning("File cannot be opened in cloud environment. Please download to view.")
    except Exception as e:
        st.warning(f"Cannot open file directly. Please download to view: {e}")


def show_upload_map(categories):
    """Upload new GIS maps with clear form after submission"""
    
    st.markdown("### 📤 Upload GIS Map")
    st.caption("Add new maps to the library (JPEG, PNG, PDF formats)")
    
    municipalities = ["Province-wide", "Barlig", "Bauko", "Besao", "Bontoc", "Natonin", "Paracelis", "Sabangan", "Sadanga", "Sagada", "Tadian"]
    
    # Use clear_on_submit=True to reset form after submission
    with st.form("upload_map_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Map Title *", placeholder="e.g., Provincial Landslide Hazard Map")
            category = st.selectbox("Category *", list(categories.keys()))
            year = st.number_input("Year *", min_value=2000, max_value=2030, value=datetime.now().year)
            municipality = st.selectbox("Municipality/Area", municipalities)
        
        with col2:
            scale = st.text_input("Map Scale", placeholder="e.g., 1:50,000")
            projection = st.text_input("Projection", placeholder="e.g., UTM Zone 51N")
            source = st.text_input("Data Source", placeholder="e.g., MGB, PAGASA, LGU")
            tags = st.text_input("Tags", placeholder="comma separated: landslide, hazard, barlig")
        
        description = st.text_area("Description", placeholder="Brief description of the map and its purpose", height=100)
        
        uploaded_file = st.file_uploader("Select map file", type=['jpg', 'jpeg', 'png', 'pdf'])
        
        submitted = st.form_submit_button("📤 Upload Map", type="primary")
        
        if submitted and title and uploaded_file:
            # Create folder structure
            category_folder = category.replace(" ", "_")
            folder = f"local_storage/geospatial_library/{category_folder}"
            os.makedirs(folder, exist_ok=True)
            
            # Save file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
            extension = uploaded_file.name.split('.')[-1].lower()
            filename = f"{timestamp}_{safe_title}.{extension}"
            file_path = os.path.join(folder, filename)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Get file info
            file_size_bytes = os.path.getsize(file_path)
            file_size = format_file_size(file_size_bytes)
            
            # Create metadata record
            new_map = {
                "id": int(datetime.now().timestamp() * 1000),
                "title": title,
                "category": category,
                "year": year,
                "municipality": municipality,
                "scale": scale,
                "projection": projection,
                "source": source,
                "tags": tags,
                "description": description,
                "file_path": file_path,
                "filename": filename,
                "file_extension": extension.upper(),
                "file_size": file_size,
                "file_size_bytes": file_size_bytes,
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": datetime.now().isoformat()
            }
            
            st.session_state.gis_maps.append(new_map)
            st.success(f"✅ Map '{title}' uploaded successfully!")
            st.balloons()
            st.rerun()
        
        elif submitted and not title:
            st.error("Please enter a map title")
        
        elif submitted and not uploaded_file:
            st.error("Please select a file to upload")

def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def get_file_size(file_path):
    """Get file size in human-readable format"""
    if not file_path or not os.path.exists(file_path):
        return "0 B"
    return format_file_size(os.path.getsize(file_path))            