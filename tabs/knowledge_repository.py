# tabs/knowledge_repository.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import base64
import platform
import subprocess
from utils.local_storage import save_file, delete_file, get_file_size, file_exists, get_storage_path

def show():
    """Display Knowledge Repository Tab - Digital Library for Policies, Literatures, and Media"""
    
    st.markdown("# 📁 Knowledge Repository")
    st.caption("Digital Library for Policies, Guidelines, Researches, Literatures, and Media Files")
    
    # Initialize session state
    if 'knowledge_items' not in st.session_state:
        st.session_state.knowledge_items = []
    
    if 'knowledge_categories' not in st.session_state:
        st.session_state.knowledge_categories = [
            "Policy", "Memorandum", "Executive Order", "Administrative Order", "Circular",
            "Research Paper", "Journal Article", "Case Study", "Report", "Manual",
            "Infographic", "Photo", "Video", "Presentation", "Training Material", "Other"
        ]
    
    if 'knowledge_sources' not in st.session_state:
        st.session_state.knowledge_sources = [
            "Office of the President", "OCD", "OCD-CAR", "DILG", "DILG-CAR", "DBM", "COA", "DOH",
            "UNDRR", "WHO", "WMO", "UNDP", "ADPC", "AHA Center", "Science Direct",
            "USGS", "JAXA", "NASA", "Local Research", "Academic Institution", "Other"
        ]
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Library",
        "➕ Add Document",
        "🏷️ Categories & Sources",
        "🔗 Related Modules"
    ])
    
    with tab1:
        show_library()
    
    with tab2:
        show_add_document()
    
    with tab3:
        show_categories_sources()
    
    with tab4:
        show_related_modules()


def show_library():
    """Display the knowledge library with search and filter"""
    
    st.markdown("### 📚 Knowledge Library")
    st.caption("Browse, search, and access all documents in the repository")
    
    items = st.session_state.knowledge_items
    
    if not items:
        st.info("No documents in the repository yet. Use the 'Add Document' tab to upload files.")
        return
    
    df = pd.DataFrame(items)
    
    # ========== FILTERS ==========
    st.markdown("#### 🔍 Search & Filter")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        categories = ["All"] + sorted(st.session_state.knowledge_categories)
        filter_category = st.selectbox("Category", categories, key="filter_category")
    
    with col2:
        sources = ["All"] + sorted(st.session_state.knowledge_sources)
        filter_source = st.selectbox("Source/Author", sources, key="filter_source")
    
    with col3:
        years = ["All"] + sorted(df['year'].unique().tolist()) if 'year' in df.columns else ["All"]
        filter_year = st.selectbox("Year", years, key="filter_year")
    
    with col4:
        search_term = st.text_input("Search", placeholder="Title, description, tags...", key="search_library")
    
    # ========== APPLY FILTERS ==========
    filtered_df = df.copy()
    
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == filter_category]
    
    if filter_source != "All":
        filtered_df = filtered_df[filtered_df['source'] == filter_source]
    
    if filter_year != "All":
        filtered_df = filtered_df[filtered_df['year'] == int(filter_year)]
    
    if search_term:
        filtered_df = filtered_df[
            filtered_df['title'].str.contains(search_term, case=False) |
            filtered_df['description'].str.contains(search_term, case=False) |
            filtered_df['tags'].str.contains(search_term, case=False)
        ]
    
    # ========== SUMMARY STATS ==========
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Documents", len(filtered_df))
    with col2:
        st.metric("Categories", filtered_df['category'].nunique() if not filtered_df.empty else 0)
    with col3:
        st.metric("Sources", filtered_df['source'].nunique() if not filtered_df.empty else 0)
    with col4:
        total_size = sum([item.get('file_size_bytes', 0) for item in filtered_df.to_dict('records')]) if not filtered_df.empty else 0
        st.metric("Total Size", format_file_size(total_size))
    
    st.markdown("---")
    
    # ========== DISPLAY TABLE ==========
    st.markdown("#### 📋 Document List")
    
    # Prepare display dataframe
    if not filtered_df.empty:
        display_df = filtered_df[['title', 'category', 'source', 'year', 'file_type', 'file_size', 'upload_date']].copy()
        display_df.columns = ['Title', 'Category', 'Source', 'Year', 'Type', 'Size', 'Uploaded']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # ========== DETAILED VIEW WITH OPEN FUNCTIONALITY ==========
        st.markdown("---")
        st.markdown("#### 📄 Document Details & Actions")
        
        for idx, row in filtered_df.iterrows():
            with st.expander(f"📄 {row['title']} ({row['year']}) - {row['category']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Title:** {row['title']}")
                    st.markdown(f"**Category:** {row['category']}")
                    st.markdown(f"**Source/Author:** {row['source']}")
                    st.markdown(f"**Year:** {row['year']}")
                    st.markdown(f"**Type:** {row['file_type']}")
                
                with col2:
                    st.markdown(f"**File Size:** {row['file_size']}")
                    st.markdown(f"**Uploaded:** {row['upload_date']}")
                    st.markdown(f"**Tags:** {row.get('tags', 'N/A')}")
                    st.markdown(f"**Location:** {row.get('location', 'N/A')}")
                
                st.markdown(f"**Description:** {row.get('description', 'No description')}")
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    # Open file button
                    if st.button(f"📖 Open", key=f"open_{row['id']}"):
                        open_file(row['file_path'])
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
                    # Print button (opens file for printing)
                    if st.button(f"🖨️ Print", key=f"print_{row['id']}"):
                        open_file(row['file_path'])  # Opens file, user can print from there
                        st.info("File opened. Use Ctrl+P (Cmd+P on Mac) to print.")
                
                with col4:
                    # Delete button
                    if st.button(f"🗑️ Delete", key=f"delete_{row['id']}"):
                        # Delete file from local storage
                        if row['file_path'] and os.path.exists(row['file_path']):
                            os.remove(row['file_path'])
                        # Remove from session state
                        st.session_state.knowledge_items = [item for item in st.session_state.knowledge_items if item['id'] != row['id']]
                        st.success(f"Deleted: {row['title']}")
                        st.rerun()
    else:
        st.info("No documents match your filters.")


def show_add_document():
    """Add new document to the repository"""
    
    st.markdown("### ➕ Add Document to Repository")
    st.caption("Upload digital copies of policies, literatures, researches, and media files")
    
    with st.form("add_document_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Document Title *", placeholder="e.g., RA 10121: Philippine DRRM Act")
            category = st.selectbox("Category *", st.session_state.knowledge_categories)
            source = st.selectbox("Source/Author *", st.session_state.knowledge_sources)
            year = st.number_input("Year *", min_value=1900, max_value=2030, value=datetime.now().year)
        
        with col2:
            location = st.text_input("Location/Venue", placeholder="e.g., Bontoc, Mountain Province")
            tags = st.text_input("Tags", placeholder="comma separated: drrm, policy, governance")
            reference_number = st.text_input("Reference Number", placeholder="e.g., EO No. 25, s. 2025")
        
        description = st.text_area("Description", placeholder="Brief description of the document", height=100)
        
        st.markdown("#### 📎 Upload File")
        uploaded_file = st.file_uploader(
            "Select file to upload", 
            type=['pdf', 'docx', 'doc', 'xlsx', 'pptx', 'jpg', 'jpeg', 'png', 'gif', 'mp4', 'txt'],
            help="Supported formats: PDF, DOCX, DOC, XLSX, PPTX, JPG, PNG, GIF, MP4, TXT"
        )
        
        submitted = st.form_submit_button("💾 Save Document", type="primary")
        
        if submitted and title and uploaded_file:
            # Save file to local storage
            category_folder = category.replace(" ", "_")
            folder = f"local_storage/knowledge_repository/{category_folder}"
            os.makedirs(folder, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
            filename = f"{timestamp}_{safe_title}.{uploaded_file.name.split('.')[-1]}"
            file_path = os.path.join(folder, filename)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Get file size
            file_size_bytes = os.path.getsize(file_path)
            file_size = format_file_size(file_size_bytes)
            
            # Create metadata record
            new_item = {
                "id": int(datetime.now().timestamp() * 1000),
                "title": title,
                "category": category,
                "source": source,
                "year": year,
                "location": location,
                "tags": tags,
                "reference_number": reference_number,
                "description": description,
                "file_path": file_path,
                "filename": filename,
                "file_type": uploaded_file.type,
                "file_extension": uploaded_file.name.split('.')[-1].upper(),
                "file_size": file_size,
                "file_size_bytes": file_size_bytes,
                "upload_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "created_at": datetime.now().isoformat()
            }
            
            st.session_state.knowledge_items.append(new_item)
            st.success(f"✅ Document '{title}' uploaded successfully!")
            st.balloons()
            st.rerun()
        
        elif submitted and not title:
            st.error("Please enter a document title")
        
        elif submitted and not uploaded_file:
            st.error("Please select a file to upload")


def show_categories_sources():
    """Display and manage categories and sources"""
    
    st.markdown("### 🏷️ Categories & Sources")
    st.caption("Manage document categories and source organizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📂 Document Categories")
        st.markdown("Categories used to classify documents:")
        
        for cat in sorted(st.session_state.knowledge_categories):
            st.markdown(f"- {cat}")
        
        st.markdown("---")
        st.markdown("**Add New Category:**")
        new_category = st.text_input("New Category Name", key="new_category")
        if st.button("➕ Add Category", key="add_category"):
            if new_category and new_category not in st.session_state.knowledge_categories:
                st.session_state.knowledge_categories.append(new_category)
                st.success(f"Category '{new_category}' added!")
                st.rerun()
            elif new_category in st.session_state.knowledge_categories:
                st.warning("Category already exists")
    
    with col2:
        st.markdown("#### 🏛️ Sources/Organizations")
        st.markdown("Sources or organizations that produced the documents:")
        
        for src in sorted(st.session_state.knowledge_sources):
            st.markdown(f"- {src}")
        
        st.markdown("---")
        st.markdown("**Add New Source:**")
        new_source = st.text_input("New Source Name", key="new_source")
        if st.button("➕ Add Source", key="add_source"):
            if new_source and new_source not in st.session_state.knowledge_sources:
                st.session_state.knowledge_sources.append(new_source)
                st.success(f"Source '{new_source}' added!")
                st.rerun()
            elif new_source in st.session_state.knowledge_sources:
                st.warning("Source already exists")
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Repository Statistics")
    
    items = st.session_state.knowledge_items
    if items:
        df = pd.DataFrame(items)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Documents", len(items))
        with col2:
            st.metric("Categories Used", df['category'].nunique())
        with col3:
            st.metric("Sources Used", df['source'].nunique())
        
        # Category distribution
        st.markdown("#### Category Distribution")
        cat_counts = df['category'].value_counts().reset_index()
        cat_counts.columns = ['Category', 'Count']
        st.dataframe(cat_counts, use_container_width=True, hide_index=True)
    else:
        st.info("No documents in repository yet")


def show_related_modules():
    """Show connections to other modules"""
    
    st.markdown("### 🔗 Related Modules")
    st.caption("How Knowledge Repository connects with other INDC modules")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Plan Management
        - Store policy documents linked to DRRM plans
        - Reference materials for plan formulation
        - Legal bases and guidelines
        
        ### 📚 Trainings
        - Training manuals and materials
        - Reference documents for capacity building
        - Training certificates and resources
        """)
    
    with col2:
        st.markdown("""
        ### 📊 DRRM Intelligence
        - Research papers on hazard assessment
        - Scientific studies for risk analysis
        - Technical reports and methodologies
        
        ### 📡 Situation Report
        - Reference documents for reporting
        - Templates and guidelines
        - Historical reports archive
        """)
    
    st.markdown("---")
    st.markdown("### 📋 Quick Links")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📋 Go to Plan Management", use_container_width=True):
            st.session_state.navigation = "📋 PLAN MANAGEMENT"
            st.rerun()
    with col2:
        if st.button("📚 Go to Trainings", use_container_width=True):
            st.session_state.navigation = "📚 TRAININGS"
            st.rerun()
    with col3:
        if st.button("📊 Go to DRRM Intelligence", use_container_width=True):
            st.session_state.navigation = "📊 DRRM INTELLIGENCE"
            st.rerun()


def open_file(file_path):
    """Open a file with the default system application"""
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", file_path])
        else:  # Linux
            subprocess.run(["xdg-open", file_path])
    except Exception as e:
        st.error(f"Could not open file: {e}")


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"