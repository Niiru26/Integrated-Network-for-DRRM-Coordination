# tabs/trainings.py
import streamlit as st
import pandas as pd
from datetime import date, datetime
from utils.supabase_client import get_supabase_client, is_connected

def show():
    """Display the Trainings Tab"""
    
    st.markdown("# 📚 Trainings & Capacity Building")
    st.caption("Track staff training, certifications, and responder readiness")
    
    # Show connection status
    if is_connected():
        st.success("☁️ Cloud Sync Enabled")
    else:
        st.info("💾 Local Mode - Data saved locally only")
    
    tab1, tab2, tab3 = st.tabs(["📝 Add Training", "📋 Training Records", "📊 Summary"])
    
    with tab1:
        add_training()
    
    with tab2:
        view_trainings()
    
    with tab3:
        show_summary()

def load_trainings_from_cloud():
    """Load trainings from Supabase cloud"""
    if not is_connected():
        return None
    
    client = get_supabase_client()
    if not client:
        return None
    
    try:
        response = client.table('trainings').select('*').execute()
        if response.data:
            return response.data
        return []
    except Exception as e:
        st.warning(f"Could not load from cloud: {e}")
        return None

def save_training_to_cloud(training):
    """Save training to Supabase cloud"""
    if not is_connected():
        return False
    
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        # Remove id if it's None or 0 (let Supabase handle it if needed)
        if 'id' in training and (training['id'] is None or training['id'] == 0):
            del training['id']
        
        response = client.table('trainings').insert(training).execute()
        if response.data:
            return True
        return False
    except Exception as e:
        st.error(f"Failed to save to cloud: {e}")
        return False

def sync_trainings():
    """Sync trainings between cloud and local"""
    cloud_data = load_trainings_from_cloud()
    
    if cloud_data is not None:
        # Cloud data available - use it
        st.session_state.trainings = cloud_data
        return True
    return False

def add_training():
    """Form to add a new training"""
    
    st.markdown("### Add New Training Record")
    
    with st.form("add_training_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Training Title *", placeholder="e.g., Basic Life Support")
            date_training = st.date_input("Training Date", date.today())
            organizer = st.text_input("Organizer", placeholder="e.g., PDRRMO, Red Cross")
        
        with col2:
            participants = st.number_input("Participants", min_value=0, value=0)
            municipality = st.selectbox("Municipality", ["Bontoc", "Bauko", "Besao", "Sabangan", "Sadanga", "Tadian", "Natonin", "Paracelis", "Barlig", "All Municipalities"])
            certification = st.selectbox("Certification", ["Certificate of Completion", "Certificate of Participation", "No Certificate"])
        
        notes = st.text_area("Notes", placeholder="Additional information...")
        
        submitted = st.form_submit_button("💾 Save Training", type="primary")
        
        if submitted:
            if not title:
                st.error("Please enter training title")
                return
            
            training = {
                "title": title,
                "date": date_training.isoformat(),
                "organizer": organizer,
                "participants": participants,
                "municipality": municipality,
                "certification": certification,
                "notes": notes,
                "created_at": datetime.now().isoformat()
            }
            
            # Try cloud first
            saved_to_cloud = save_training_to_cloud(training)
            
            if saved_to_cloud:
                # Refresh from cloud to get the ID
                sync_trainings()
                st.success(f"✅ Training '{title}' saved to cloud!")
                st.balloons()
            else:
                # Fallback to local session
                if "trainings" not in st.session_state:
                    st.session_state.trainings = []
                
                # Generate local ID
                training["id"] = len(st.session_state.trainings) + 1
                st.session_state.trainings.append(training)
                st.success(f"✅ Training '{title}' saved locally!")
                st.balloons()

def view_trainings():
    """View all trainings"""
    
    st.markdown("### Training Records")
    
    # Sync on view to get latest data
    sync_trainings()
    
    if "trainings" not in st.session_state or not st.session_state.trainings:
        st.info("No training records yet. Add your first training!")
        
        # Add sync button for existing data
        if is_connected():
            if st.button("🔄 Sync from Cloud"):
                if sync_trainings():
                    st.success("Synced successfully!")
                    st.rerun()
                else:
                    st.error("No cloud data found")
        return
    
    df = pd.DataFrame(st.session_state.trainings)
    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%B %d, %Y")
    
    # Select columns for display
    display_cols = ["title", "date", "municipality", "participants", "organizer", "certification"]
    available_cols = [col for col in display_cols if col in df.columns]
    
    display_df = df[available_cols]
    column_names = {
        "title": "Title",
        "date": "Date", 
        "municipality": "Municipality",
        "participants": "Participants",
        "organizer": "Organizer",
        "certification": "Certification"
    }
    display_df = display_df.rename(columns={k: v for k, v in column_names.items() if k in available_cols})
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Show summary stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Trainings", len(df))
    with col2:
        st.metric("Total Participants", df["participants"].sum())
    
    # Add sync status
    if is_connected():
        st.caption("✅ Data is synced with cloud")
    else:
        st.caption("⚠️ Data is local only - connect to cloud to sync")

def show_summary():
    """Show summary statistics"""
    
    st.markdown("### Training Summary")
    
    # Sync to get latest data
    sync_trainings()
    
    if "trainings" not in st.session_state or not st.session_state.trainings:
        st.info("No data available")
        return
    
    df = pd.DataFrame(st.session_state.trainings)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Trainings", len(df))
    with col2:
        st.metric("Total Participants", df["participants"].sum())
    with col3:
        st.metric("Municipalities", df["municipality"].nunique())
    
    st.markdown("---")
    
    # By municipality
    st.markdown("#### Trainings per Municipality")
    by_mun = df["municipality"].value_counts().reset_index()
    by_mun.columns = ["Municipality", "Count"]
    st.dataframe(by_mun, use_container_width=True, hide_index=True)
    
    # By month (if date column exists)
    if "date" in df.columns:
        st.markdown("#### Trainings by Month")
        df["month"] = pd.to_datetime(df["date"]).dt.strftime("%B %Y")
        by_month = df["month"].value_counts().reset_index()
        by_month.columns = ["Month", "Count"]
        st.dataframe(by_month, use_container_width=True, hide_index=True)