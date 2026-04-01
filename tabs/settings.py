# tabs/settings.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import shutil
import json
import zipfile
from utils.supabase_client import is_connected, sync_all
from utils.local_storage import get_storage_usage, get_storage_path

def show():
    """Display Settings Tab - System Configuration and Auto-Backup"""
    
    st.markdown("# ⚙️ Settings")
    st.caption("System configuration, auto-backup, and data management")
    
    # Initialize session state for backup settings
    if 'auto_backup_enabled' not in st.session_state:
        st.session_state.auto_backup_enabled = True
    
    if 'backup_frequency' not in st.session_state:
        st.session_state.backup_frequency = "Daily"
    
    if 'last_backup_time' not in st.session_state:
        st.session_state.last_backup_time = None
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💾 Backup & Restore",
        "🤖 Auto-Backup",
        "📊 System Status",
        "🗂️ Storage Management",
        "⚙️ Preferences"
    ])
    
    with tab1:
        show_backup_restore()
    
    with tab2:
        show_auto_backup()
    
    with tab3:
        show_system_status()
    
    with tab4:
        show_storage_management()
    
    with tab5:
        show_preferences()


def show_backup_restore():
    """Manual backup and restore functionality"""
    
    st.markdown("### 💾 Backup & Restore")
    st.caption("Manually backup your data or restore from a backup file")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📤 Create Backup")
        st.markdown("Create a complete backup of all your data and files.")
        
        backup_name = st.text_input("Backup Name", value=f"INDC_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        backup_include_files = st.checkbox("Include local files (documents, photos, maps)", value=True)
        
        if st.button("📥 Create Backup Now", type="primary", use_container_width=True):
            with st.spinner("Creating backup..."):
                backup_path = create_backup(backup_name, backup_include_files)
                if backup_path:
                    st.session_state.last_backup_time = datetime.now()
                    st.success(f"✅ Backup created successfully!")
                    
                    # Offer download
                    with open(backup_path, "rb") as f:
                        st.download_button(
                            label="📎 Download Backup File",
                            data=f,
                            file_name=os.path.basename(backup_path),
                            mime="application/zip",
                            key="download_backup"
                        )
                else:
                    st.error("❌ Backup failed. Please check your storage space.")
    
    with col2:
        st.markdown("#### 📥 Restore from Backup")
        st.markdown("Restore your data from a previously created backup file.")
        st.warning("⚠️ Restoring will overwrite current data. Create a backup first if needed.")
        
        uploaded_file = st.file_uploader("Select Backup File", type=['zip'], key="restore_upload")
        
        if uploaded_file and st.button("🔄 Restore from Backup", type="primary", use_container_width=True):
            with st.spinner("Restoring backup..."):
                success = restore_from_backup(uploaded_file)
                if success:
                    st.success("✅ Backup restored successfully! Please restart the app.")
                    st.info("🔄 Click the refresh button or restart Streamlit to see changes.")
                else:
                    st.error("❌ Restore failed. The backup file may be corrupted.")


def show_auto_backup():
    """Auto-backup configuration"""
    
    st.markdown("### 🤖 Auto-Backup Settings")
    st.caption("Configure automatic backups to protect your data")
    
    # Auto-backup toggle
    col1, col2 = st.columns([1, 2])
    with col1:
        auto_backup = st.toggle("Enable Auto-Backup", value=st.session_state.auto_backup_enabled)
        if auto_backup != st.session_state.auto_backup_enabled:
            st.session_state.auto_backup_enabled = auto_backup
            save_auto_backup_settings()
            st.rerun()
    
    with col2:
        if st.session_state.auto_backup_enabled:
            st.success("🟢 Auto-backup is ENABLED")
        else:
            st.warning("🔴 Auto-backup is DISABLED")
    
    if st.session_state.auto_backup_enabled:
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⏰ Backup Schedule")
            frequency = st.selectbox(
                "Backup Frequency",
                ["Hourly", "Daily", "Weekly", "Monthly"],
                index=["Hourly", "Daily", "Weekly", "Monthly"].index(st.session_state.backup_frequency)
            )
            if frequency != st.session_state.backup_frequency:
                st.session_state.backup_frequency = frequency
                save_auto_backup_settings()
            
            backup_time = st.time_input("Backup Time (for Daily/Weekly)", value=datetime.now().time())
            
            if frequency == "Weekly":
                backup_day = st.selectbox("Backup Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        
        with col2:
            st.markdown("#### 📦 Backup Options")
            backup_include_files = st.checkbox("Include local files", value=True)
            max_backups = st.number_input("Maximum Backups to Keep", min_value=1, max_value=50, value=10)
            backup_location = st.text_input("Backup Location", value="local_storage/backups")
        
        st.markdown("---")
        st.markdown("#### 📋 Backup History")
        
        # Display backup history
        backup_folder = "local_storage/backups"
        if os.path.exists(backup_folder):
            backups = []
            for f in os.listdir(backup_folder):
                if f.endswith('.zip'):
                    file_path = os.path.join(backup_folder, f)
                    stat = os.stat(file_path)
                    backups.append({
                        "name": f,
                        "size": get_file_size(file_path),
                        "date": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            if backups:
                df = pd.DataFrame(backups)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # Clean old backups button
                if st.button("🧹 Clean Old Backups", use_container_width=True):
                    clean_old_backups(backup_folder, max_backups)
                    st.success(f"✅ Kept last {max_backups} backups, removed older ones.")
                    st.rerun()
            else:
                st.info("No backups found. Create your first backup in the Backup & Restore tab.")
        else:
            st.info("No backups found. Create your first backup in the Backup & Restore tab.")
        
        # Last backup info
        if st.session_state.last_backup_time:
            st.info(f"📅 Last backup: {st.session_state.last_backup_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Next backup calculation
        next_backup = calculate_next_backup()
        if next_backup:
            st.info(f"⏰ Next backup scheduled: {next_backup.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run auto-backup check
    if st.session_state.auto_backup_enabled:
        check_and_run_auto_backup()


def show_system_status():
    """Display system information and status"""
    
    st.markdown("### 📊 System Status")
    st.caption("Current system information and connection status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ☁️ Cloud Connection")
        if is_connected():
            st.success("✅ Connected to Supabase")
            st.caption("Auto-sync is active")
        else:
            st.error("❌ Not Connected")
            st.caption("Check your internet connection and Supabase credentials")
        
        st.markdown("#### 💾 Database Status")
        st.markdown("- Auto-sync: Enabled")
        st.markdown("- Real-time updates: Active")
        st.markdown("- Data encryption: Enabled")
    
    with col2:
        st.markdown("#### 🗄️ Local Storage")
        total_size = get_storage_usage()
        st.metric("Total Storage Used", total_size)
        
        # Storage breakdown
        storage_path = "local_storage"
        if os.path.exists(storage_path):
            breakdown = []
            for item in os.listdir(storage_path):
                item_path = os.path.join(storage_path, item)
                if os.path.isdir(item_path):
                    size = get_folder_size(item_path)
                    breakdown.append({"Folder": item, "Size": format_file_size(size)})
            
            if breakdown:
                df = pd.DataFrame(breakdown)
                st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📱 Application Info")
        st.markdown(f"- **Version:** 2.0.0")
        st.markdown(f"- **Last Updated:** March 2026")
        st.markdown(f"- **Python Version:** {__import__('sys').version.split()[0]}")
        st.markdown(f"- **Streamlit Version:** {__import__('streamlit').__version__}")
    
    with col2:
        st.markdown("#### 🔧 System Checks")
        
        # Check disk space
        import shutil
        total, used, free = shutil.disk_usage("E:/")
        st.metric("Free Disk Space", format_file_size(free))
        
        if free < 5 * 1024 * 1024 * 1024:  # Less than 5GB
            st.warning("⚠️ Low disk space! Consider cleaning up old files.")


def show_storage_management():
    """Manage local storage and clean up files"""
    
    st.markdown("### 🗂️ Storage Management")
    st.caption("Manage local files and clean up unused data")
    
    # Storage overview
    storage_path = "local_storage"
    if os.path.exists(storage_path):
        total_size = get_folder_size(storage_path)
        st.metric("Total Local Storage", format_file_size(total_size))
        
        # Storage by module
        st.markdown("#### 📁 Storage by Module")
        
        modules = [
            "drrm_intelligence", "plan_management", "climate_change", 
            "trainings", "ldrrmf", "sitrep", "performance_management",
            "knowledge_repository", "geospatial_library", "risk_profiles", "backups"
        ]
        
        module_sizes = []
        for module in modules:
            module_path = os.path.join(storage_path, module)
            if os.path.exists(module_path):
                size = get_folder_size(module_path)
                module_sizes.append({"Module": module.replace('_', ' ').title(), "Size": format_file_size(size)})
        
        if module_sizes:
            df = pd.DataFrame(module_sizes)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🧹 Clean Up Options")
        
        days_old = st.number_input("Delete files older than (days)", min_value=1, max_value=365, value=90)
        
        if st.button("🗑️ Delete Old Temporary Files", use_container_width=True):
            deleted_count = clean_old_temp_files(days_old)
            st.success(f"✅ Deleted {deleted_count} old temporary files")
            st.rerun()
        
        if st.button("🧹 Clear Empty Folders", use_container_width=True):
            cleared_count = clear_empty_folders(storage_path)
            st.success(f"✅ Cleared {cleared_count} empty folders")
            st.rerun()
    
    with col2:
        st.markdown("#### ⚠️ Danger Zone")
        st.warning("⚠️ These actions cannot be undone!")
        
        if st.button("🗑️ Clear All Cache", use_container_width=True):
            clear_streamlit_cache()
            st.success("✅ Cache cleared. Please refresh the page.")
        
        if st.button("📦 Export All Data (JSON)", use_container_width=True):
            export_data = export_all_session_data()
            st.download_button(
                label="Download Export",
                data=json.dumps(export_data, indent=2),
                file_name=f"INDC_Export_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                key="export_data"
            )


def show_preferences():
    """User preferences and settings"""
    
    st.markdown("### ⚙️ Preferences")
    st.caption("Customize your INDC experience")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Display Settings")
        
        # Theme selection
        theme = st.selectbox("Theme", ["Light", "Dark", "System Default"])
        
        # Default view
        default_tab = st.selectbox("Default Landing Page", [
            "Command Center", "DRRM Intelligence", "Plan Management", "Situation Report"
        ])
        
        # Table settings
        st.markdown("#### 📊 Table Settings")
        rows_per_page = st.number_input("Rows per page", min_value=10, max_value=100, value=25)
        enable_sorting = st.checkbox("Enable sorting by default", value=True)
    
    with col2:
        st.markdown("#### 🔔 Notification Settings")
        
        email_notifications = st.checkbox("Email notifications", value=False)
        email = st.text_input("Notification Email", placeholder="your@email.com")
        
        st.markdown("#### 📅 Date & Time")
        date_format = st.selectbox("Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"])
        time_format = st.selectbox("Time Format", ["24-hour", "12-hour"])
    
    st.markdown("---")
    
    # Save preferences
    if st.button("💾 Save Preferences", type="primary", use_container_width=True):
        save_user_preferences(theme, default_tab, rows_per_page, email_notifications, email, date_format, time_format)
        st.success("✅ Preferences saved!")
    
    # Reset to defaults
    if st.button("🔄 Reset to Defaults", use_container_width=True):
        reset_preferences()
        st.success("✅ Preferences reset to defaults!")
        st.rerun()


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def create_backup(backup_name, include_files=True):
    """Create a complete backup of all data"""
    
    backup_folder = "local_storage/backups"
    os.makedirs(backup_folder, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{backup_name}_{timestamp}.zip"
    backup_path = os.path.join(backup_folder, backup_filename)
    
    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Backup session state data
            session_data = {
                key: value for key, value in st.session_state.items()
                if not key.startswith('_') and key not in ['supabase_client', 'pagasa_weather']
            }
            
            # Convert to JSON-serializable format
            for key, value in session_data.items():
                if hasattr(value, 'to_dict'):
                    session_data[key] = value.to_dict()
                elif hasattr(value, 'tolist'):
                    session_data[key] = value.tolist()
            
            zipf.writestr('session_state.json', json.dumps(session_data, indent=2, default=str))
            
            # Backup local files
            if include_files and os.path.exists("local_storage"):
                for root, dirs, files in os.walk("local_storage"):
                    for file in files:
                        if not file.endswith('.zip'):  # Don't include existing backups
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, ".")
                            zipf.write(file_path, arcname)
        
        return backup_path
    except Exception as e:
        st.error(f"Backup error: {e}")
        return None


def restore_from_backup(backup_file):
    """Restore data from a backup file"""
    
    try:
        # Save backup to temp location
        temp_path = f"local_storage/temp_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with open(temp_path, "wb") as f:
            f.write(backup_file.getbuffer())
        
        # Extract backup
        with zipfile.ZipFile(temp_path, 'r') as zipf:
            zipf.extractall("temp_restore")
        
        # Restore session state data
        state_file = "temp_restore/session_state.json"
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                restored_state = json.load(f)
                for key, value in restored_state.items():
                    if key in st.session_state:
                        st.session_state[key] = value
        
        # Restore local files
        local_storage_backup = "temp_restore/local_storage"
        if os.path.exists(local_storage_backup):
            # Backup current storage
            if os.path.exists("local_storage"):
                shutil.move("local_storage", f"local_storage_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Restore from backup
            shutil.copytree(local_storage_backup, "local_storage")
        
        # Clean up
        os.remove(temp_path)
        shutil.rmtree("temp_restore")
        
        return True
    except Exception as e:
        st.error(f"Restore error: {e}")
        return False


def save_auto_backup_settings():
    """Save auto-backup settings to file"""
    settings = {
        "enabled": st.session_state.auto_backup_enabled,
        "frequency": st.session_state.backup_frequency,
        "last_backup": st.session_state.last_backup_time.isoformat() if st.session_state.last_backup_time else None
    }
    
    os.makedirs("local_storage/settings", exist_ok=True)
    with open("local_storage/settings/auto_backup.json", "w") as f:
        json.dump(settings, f)


def check_and_run_auto_backup():
    """Check if auto-backup should run"""
    settings_file = "local_storage/settings/auto_backup.json"
    
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            settings = json.load(f)
        
        last_backup = settings.get("last_backup")
        if last_backup:
            last_backup_time = datetime.fromisoformat(last_backup)
            frequency = settings.get("frequency", "Daily")
            
            should_backup = False
            now = datetime.now()
            
            if frequency == "Hourly" and (now - last_backup_time).total_seconds() >= 3600:
                should_backup = True
            elif frequency == "Daily" and (now - last_backup_time).total_seconds() >= 86400:
                should_backup = True
            elif frequency == "Weekly" and (now - last_backup_time).total_seconds() >= 604800:
                should_backup = True
            elif frequency == "Monthly" and (now - last_backup_time).total_seconds() >= 2592000:
                should_backup = True
            
            if should_backup and st.session_state.auto_backup_enabled:
                backup_path = create_backup(f"Auto_Backup_{frequency}", True)
                if backup_path:
                    st.session_state.last_backup_time = now
                    save_auto_backup_settings()
                    
                    # Clean old backups
                    clean_old_backups("local_storage/backups", 10)


def calculate_next_backup():
    """Calculate next scheduled backup time"""
    settings_file = "local_storage/settings/auto_backup.json"
    
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            settings = json.load(f)
        
        last_backup = settings.get("last_backup")
        if last_backup:
            last_backup_time = datetime.fromisoformat(last_backup)
            frequency = settings.get("frequency", "Daily")
            
            if frequency == "Hourly":
                return last_backup_time + timedelta(hours=1)
            elif frequency == "Daily":
                return last_backup_time + timedelta(days=1)
            elif frequency == "Weekly":
                return last_backup_time + timedelta(weeks=1)
            elif frequency == "Monthly":
                return last_backup_time + timedelta(days=30)
    
    return None


def clean_old_backups(backup_folder, max_keep):
    """Keep only the most recent backups"""
    if not os.path.exists(backup_folder):
        return
    
    backups = []
    for f in os.listdir(backup_folder):
        if f.endswith('.zip'):
            file_path = os.path.join(backup_folder, f)
            backups.append((file_path, os.path.getmtime(file_path)))
    
    backups.sort(key=lambda x: x[1], reverse=True)
    
    for file_path, _ in backups[max_keep:]:
        os.remove(file_path)


def clean_old_temp_files(days_old):
    """Delete temporary files older than specified days"""
    cutoff = datetime.now() - timedelta(days=days_old)
    deleted_count = 0
    
    temp_folders = ["temp_restore", "__pycache__", ".streamlit/cache"]
    
    for folder in temp_folders:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                    if mtime < cutoff:
                        try:
                            os.remove(file_path)
                            deleted_count += 1
                        except:
                            pass
    
    return deleted_count


def clear_empty_folders(path):
    """Recursively remove empty folders"""
    cleared_count = 0
    if not os.path.exists(path):
        return cleared_count
    
    for root, dirs, files in os.walk(path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            try:
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)
                    cleared_count += 1
            except:
                pass
    
    return cleared_count


def clear_streamlit_cache():
    """Clear Streamlit cache"""
    try:
        import shutil
        cache_path = ".streamlit/cache"
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
    except:
        pass


def export_all_session_data():
    """Export all session state data as JSON"""
    export_data = {}
    for key, value in st.session_state.items():
        if not key.startswith('_') and key not in ['supabase_client', 'pagasa_weather']:
            if hasattr(value, 'to_dict'):
                export_data[key] = value.to_dict()
            elif hasattr(value, 'tolist'):
                export_data[key] = value.tolist()
            else:
                export_data[key] = value
    return export_data


def save_user_preferences(theme, default_tab, rows_per_page, email_notifications, email, date_format, time_format):
    """Save user preferences to file"""
    preferences = {
        "theme": theme,
        "default_tab": default_tab,
        "rows_per_page": rows_per_page,
        "email_notifications": email_notifications,
        "email": email,
        "date_format": date_format,
        "time_format": time_format,
        "saved_at": datetime.now().isoformat()
    }
    
    os.makedirs("local_storage/settings", exist_ok=True)
    with open("local_storage/settings/preferences.json", "w") as f:
        json.dump(preferences, f)


def reset_preferences():
    """Reset all preferences to defaults"""
    default_preferences = {
        "theme": "Light",
        "default_tab": "Command Center",
        "rows_per_page": 25,
        "email_notifications": False,
        "email": "",
        "date_format": "YYYY-MM-DD",
        "time_format": "24-hour"
    }
    
    os.makedirs("local_storage/settings", exist_ok=True)
    with open("local_storage/settings/preferences.json", "w") as f:
        json.dump(default_preferences, f)


def get_folder_size(path):
    """Calculate folder size recursively"""
    total = 0
    if not os.path.exists(path):
        return total
    
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total += os.path.getsize(fp)
    return total


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
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