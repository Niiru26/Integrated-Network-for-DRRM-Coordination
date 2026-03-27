# utils/supabase_client.py
import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import time

def get_supabase_client() -> Client:
    """Get Supabase client from session state or create new"""
    if 'supabase_client' not in st.session_state:
        try:
            supabase_url = st.secrets["SUPABASE_URL"]
            supabase_key = st.secrets["SUPABASE_KEY"]
            st.session_state.supabase_client = create_client(supabase_url, supabase_key)
            st.session_state.supabase_connected = True
            print("✅ Supabase connected successfully")
        except Exception as e:
            st.session_state.supabase_connected = False
            st.session_state.supabase_client = None
            print(f"⚠️ Supabase connection failed: {e}")
    return st.session_state.supabase_client

def is_connected():
    """Check if Supabase is connected"""
    return st.session_state.get('supabase_connected', False)

# =============================================================================
# AUTO-SYNC FUNCTIONS - This is the automation you want!
# =============================================================================

def auto_sync_table(table_name, session_key, data=None):
    """
    Automatically sync a table between Supabase and session state
    If data is provided, saves to cloud; otherwise loads from cloud
    """
    if not is_connected():
        return data if data is not None else st.session_state.get(session_key, [])
    
    client = get_supabase_client()
    if not client:
        return data if data is not None else st.session_state.get(session_key, [])
    
    try:
        if data is not None:
            # SAVE to cloud
            if isinstance(data, list):
                for item in data:
                    # Remove session-only fields if needed
                    if 'temp_id' in item:
                        del item['temp_id']
                    client.table(table_name).upsert(item).execute()
            else:
                if 'temp_id' in data:
                    del data['temp_id']
                client.table(table_name).upsert(data).execute()
            return data
        else:
            # LOAD from cloud
            response = client.table(table_name).select('*').execute()
            cloud_data = response.data if response.data else []
            
            # Merge with session state (cloud takes priority)
            session_data = st.session_state.get(session_key, [])
            
            # Create a dictionary of cloud data by id
            cloud_dict = {item['id']: item for item in cloud_data if 'id' in item}
            
            # Merge: cloud data overrides session data
            merged = []
            seen_ids = set()
            
            # Add cloud data first
            for item in cloud_data:
                if 'id' in item:
                    merged.append(item)
                    seen_ids.add(item['id'])
            
            # Add session data that doesn't exist in cloud
            for item in session_data:
                if 'id' in item and item['id'] not in seen_ids:
                    merged.append(item)
            
            st.session_state[session_key] = merged
            return merged
    except Exception as e:
        print(f"Auto-sync failed for {table_name}: {e}")
        return data if data is not None else st.session_state.get(session_key, [])

def auto_sync_add(table_name, session_key, new_item):
    """Add an item with auto-sync"""
    # Generate ID
    if 'id' not in new_item:
        new_item['id'] = int(time.time() * 1000)
    
    # Add timestamp
    new_item['created_at'] = datetime.now().isoformat()
    
    # Get current data
    current = st.session_state.get(session_key, [])
    current.append(new_item)
    
    # Auto-sync to cloud
    auto_sync_table(table_name, session_key, current)
    
    return new_item

def auto_sync_delete(table_name, session_key, item_id):
    """Delete an item with auto-sync"""
    current = st.session_state.get(session_key, [])
    updated = [item for item in current if item.get('id') != item_id]
    st.session_state[session_key] = updated
    
    # Auto-sync to cloud
    auto_sync_table(table_name, session_key, updated)
    
    return True

def auto_sync_update(table_name, session_key, item_id, updates):
    """Update an item with auto-sync"""
    current = st.session_state.get(session_key, [])
    for i, item in enumerate(current):
        if item.get('id') == item_id:
            updates['id'] = item_id
            updates['updated_at'] = datetime.now().isoformat()
            if 'created_at' not in updates:
                updates['created_at'] = item.get('created_at', datetime.now().isoformat())
            current[i] = {**item, **updates}
            break
    
    st.session_state[session_key] = current
    
    # Auto-sync to cloud
    auto_sync_table(table_name, session_key, current)
    
    return True

# =============================================================================
# TABLE-SPECIFIC AUTO-SYNC FUNCTIONS
# =============================================================================

def sync_plans():
    """Auto-sync all plan data"""
    if 'provincial_plans' not in st.session_state:
        st.session_state.provincial_plans = []
    if 'municipal_plans' not in st.session_state:
        st.session_state.municipal_plans = []
    if 'plan_metrics' not in st.session_state:
        st.session_state.plan_metrics = []
    if 'plan_targets' not in st.session_state:
        st.session_state.plan_targets = []
    if 'implementation_tracker' not in st.session_state:
        st.session_state.implementation_tracker = []
    if 'ppas' not in st.session_state:
        st.session_state.ppas = []
    if 'indicators' not in st.session_state:
        st.session_state.indicators = []
    
    # Auto-sync each table
    auto_sync_table('provincial_plans', 'provincial_plans')
    auto_sync_table('municipal_plans', 'municipal_plans')
    auto_sync_table('plan_metrics', 'plan_metrics')
    auto_sync_table('plan_targets', 'plan_targets')
    auto_sync_table('implementation_tracker', 'implementation_tracker')
    auto_sync_table('ppas', 'ppas')
    auto_sync_table('indicators', 'indicators')

def sync_trainings():
    """Auto-sync trainings"""
    auto_sync_table('trainings', 'trainings')

def sync_fund_records():
    """Auto-sync fund records"""
    auto_sync_table('fund_utilizations', 'ldrrmf_records')

def sync_situation_reports():
    """Auto-sync situation reports"""
    auto_sync_table('situation_reports', 'municipal_reports')

def sync_all():
    """Auto-sync all data"""
    sync_plans()
    sync_trainings()
    sync_fund_records()
    sync_situation_reports()