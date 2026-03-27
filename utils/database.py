# utils/database.py
import streamlit as st
import pandas as pd
from datetime import datetime

def init_session_state():
    """Initialize all session state variables"""
    
    # Disaster events
    if 'disaster_events' not in st.session_state:
        st.session_state.disaster_events = pd.DataFrame()

    # Plan Management
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
        st.session_state.ppas = []  # Programs, Projects, Activities

    if 'indicators' not in st.session_state:
        st.session_state.indicators = []  # M&E Indicators

    # Trainings
    if 'trainings' not in st.session_state:
        st.session_state.trainings = []

    # LDRRMF
    if 'ldrrmf_records' not in st.session_state:
        st.session_state.ldrrmf_records = []

    # Situation Reports
    if 'municipal_reports' not in st.session_state:
        st.session_state.municipal_reports = []

    if 'main_reports' not in st.session_state:
        st.session_state.main_reports = []

    # User
    if 'user_role' not in st.session_state:
        st.session_state.user_role = "PDRRMO_STAFF"

    if 'username' not in st.session_state:
        st.session_state.username = "PDRRMO Staff"

    # Quick Guide / Help
    if 'quick_guide_shown' not in st.session_state:
        st.session_state.quick_guide_shown = False


# =============================================================================
# EVENT FUNCTIONS (for drrm_intelligence.py)
# =============================================================================

def add_event(event_data):
    """Add a disaster event to session state"""
    if 'disaster_events' not in st.session_state:
        st.session_state.disaster_events = pd.DataFrame()

    # Add an ID if not present
    if 'id' not in event_data:
        event_data['id'] = len(st.session_state.disaster_events) + 1

    # Convert to DataFrame if empty
    if st.session_state.disaster_events.empty:
        st.session_state.disaster_events = pd.DataFrame([event_data])
    else:
        st.session_state.disaster_events = pd.concat(
            [st.session_state.disaster_events, pd.DataFrame([event_data])],
            ignore_index=True
        )

    return True


def save_events():
    """Save events to Supabase (placeholder - will connect later)"""
    st.info("Supabase integration coming soon")
    return True


def load_events_from_supabase():
    """Load events from Supabase (placeholder - will connect later)"""
    if 'disaster_events' in st.session_state and not st.session_state.disaster_events.empty:
        return st.session_state.disaster_events
    return pd.DataFrame()


def get_events():
    """Get all disaster events"""
    if 'disaster_events' in st.session_state:
        return st.session_state.disaster_events
    return pd.DataFrame()


def delete_event(event_id):
    """Delete an event by ID"""
    if 'disaster_events' in st.session_state and not st.session_state.disaster_events.empty:
        st.session_state.disaster_events = st.session_state.disaster_events[
            st.session_state.disaster_events['id'] != event_id
        ]
        return True
    return False


# =============================================================================
# PLAN MANAGEMENT FUNCTIONS (for plan_management.py)
# =============================================================================

# PPA Functions
def add_ppa(ppa_data):
    """Add a Program, Project, or Activity"""
    if 'ppas' not in st.session_state:
        st.session_state.ppas = []

    # Add ID and timestamp
    ppa_data['id'] = len(st.session_state.ppas) + 1
    ppa_data['created_at'] = datetime.now().isoformat()

    st.session_state.ppas.append(ppa_data)
    return True


def get_ppas():
    """Get all PPAs"""
    if 'ppas' in st.session_state:
        return st.session_state.ppas
    return []


def update_ppa(ppa_id, updated_data):
    """Update a PPA by ID"""
    if 'ppas' in st.session_state:
        for i, ppa in enumerate(st.session_state.ppas):
            if ppa.get('id') == ppa_id:
                updated_data['id'] = ppa_id
                updated_data['created_at'] = ppa.get('created_at', datetime.now().isoformat())
                updated_data['updated_at'] = datetime.now().isoformat()
                st.session_state.ppas[i] = updated_data
                return True
    return False


def delete_ppa(ppa_id):
    """Delete a PPA by ID"""
    if 'ppas' in st.session_state:
        st.session_state.ppas = [p for p in st.session_state.ppas if p.get('id') != ppa_id]
        return True
    return False


# Indicator Functions
def add_indicator(indicator_data):
    """Add an M&E Indicator"""
    if 'indicators' not in st.session_state:
        st.session_state.indicators = []

    # Add ID and timestamp
    indicator_data['id'] = len(st.session_state.indicators) + 1
    indicator_data['created_at'] = datetime.now().isoformat()

    st.session_state.indicators.append(indicator_data)
    return True


def get_indicators():
    """Get all indicators"""
    if 'indicators' in st.session_state:
        return st.session_state.indicators
    return []


def update_indicator(indicator_id, updated_data):
    """Update an indicator by ID"""
    if 'indicators' in st.session_state:
        for i, indicator in enumerate(st.session_state.indicators):
            if indicator.get('id') == indicator_id:
                updated_data['id'] = indicator_id
                updated_data['created_at'] = indicator.get('created_at', datetime.now().isoformat())
                updated_data['updated_at'] = datetime.now().isoformat()
                st.session_state.indicators[i] = updated_data
                return True
    return False


def delete_indicator(indicator_id):
    """Delete an indicator by ID"""
    if 'indicators' in st.session_state:
        st.session_state.indicators = [i for i in st.session_state.indicators if i.get('id') != indicator_id]
        return True
    return False


# Provincial Plan Functions
def save_provincial_plan(plan_data):
    """Save a provincial plan"""
    if 'provincial_plans' not in st.session_state:
        st.session_state.provincial_plans = []

    # Add ID and timestamp
    plan_data['id'] = len(st.session_state.provincial_plans) + 1
    plan_data['created_at'] = datetime.now().isoformat()

    st.session_state.provincial_plans.append(plan_data)
    return True


def get_provincial_plans():
    """Get all provincial plans"""
    if 'provincial_plans' in st.session_state:
        return st.session_state.provincial_plans
    return []


def update_provincial_plan(plan_id, updated_data):
    """Update a provincial plan by ID"""
    if 'provincial_plans' in st.session_state:
        for i, plan in enumerate(st.session_state.provincial_plans):
            if plan.get('id') == plan_id:
                updated_data['id'] = plan_id
                updated_data['created_at'] = plan.get('created_at', datetime.now().isoformat())
                updated_data['updated_at'] = datetime.now().isoformat()
                st.session_state.provincial_plans[i] = updated_data
                return True
    return False


def delete_provincial_plan(plan_id):
    """Delete a provincial plan by ID"""
    if 'provincial_plans' in st.session_state:
        st.session_state.provincial_plans = [p for p in st.session_state.provincial_plans if p.get('id') != plan_id]
        return True
    return False


# Municipal Plan Functions
def save_municipal_plan(plan_data):
    """Save a municipal plan"""
    if 'municipal_plans' not in st.session_state:
        st.session_state.municipal_plans = []

    # Add ID and timestamp
    plan_data['id'] = len(st.session_state.municipal_plans) + 1
    plan_data['created_at'] = datetime.now().isoformat()

    st.session_state.municipal_plans.append(plan_data)
    return True


def get_municipal_plans():
    """Get all municipal plans"""
    if 'municipal_plans' in st.session_state:
        return st.session_state.municipal_plans
    return []


def update_municipal_plan(plan_id, updated_data):
    """Update a municipal plan by ID"""
    if 'municipal_plans' in st.session_state:
        for i, plan in enumerate(st.session_state.municipal_plans):
            if plan.get('id') == plan_id:
                updated_data['id'] = plan_id
                updated_data['created_at'] = plan.get('created_at', datetime.now().isoformat())
                updated_data['updated_at'] = datetime.now().isoformat()
                st.session_state.municipal_plans[i] = updated_data
                return True
    return False


def delete_municipal_plan(plan_id):
    """Delete a municipal plan by ID"""
    if 'municipal_plans' in st.session_state:
        st.session_state.municipal_plans = [p for p in st.session_state.municipal_plans if p.get('id') != plan_id]
        return True
    return False


# Plan Metrics Functions
def save_plan_metrics(metrics_data):
    """Save plan metrics"""
    if 'plan_metrics' not in st.session_state:
        st.session_state.plan_metrics = []

    metrics_data['id'] = len(st.session_state.plan_metrics) + 1
    metrics_data['created_at'] = datetime.now().isoformat()

    st.session_state.plan_metrics.append(metrics_data)
    return True


def get_plan_metrics():
    """Get all plan metrics"""
    if 'plan_metrics' in st.session_state:
        return st.session_state.plan_metrics
    return []


def update_plan_metrics(metrics_id, updated_data):
    """Update plan metrics by ID"""
    if 'plan_metrics' in st.session_state:
        for i, metrics in enumerate(st.session_state.plan_metrics):
            if metrics.get('id') == metrics_id:
                updated_data['id'] = metrics_id
                updated_data['created_at'] = metrics.get('created_at', datetime.now().isoformat())
                updated_data['updated_at'] = datetime.now().isoformat()
                st.session_state.plan_metrics[i] = updated_data
                return True
    return False


# Plan Targets Functions
def save_plan_targets(targets_data):
    """Save plan targets"""
    if 'plan_targets' not in st.session_state:
        st.session_state.plan_targets = []

    targets_data['id'] = len(st.session_state.plan_targets) + 1
    targets_data['created_at'] = datetime.now().isoformat()

    st.session_state.plan_targets.append(targets_data)
    return True


def get_plan_targets():
    """Get all plan targets"""
    if 'plan_targets' in st.session_state:
        return st.session_state.plan_targets
    return []


def update_plan_targets(targets_id, updated_data):
    """Update plan targets by ID"""
    if 'plan_targets' in st.session_state:
        for i, targets in enumerate(st.session_state.plan_targets):
            if targets.get('id') == targets_id:
                updated_data['id'] = targets_id
                updated_data['created_at'] = targets.get('created_at', datetime.now().isoformat())
                updated_data['updated_at'] = datetime.now().isoformat()
                st.session_state.plan_targets[i] = updated_data
                return True
    return False


# Implementation Tracker Functions
def save_implementation_data(data):
    """Save implementation tracking data"""
    if 'implementation_tracker' not in st.session_state:
        st.session_state.implementation_tracker = []

    data['id'] = len(st.session_state.implementation_tracker) + 1
    data['created_at'] = datetime.now().isoformat()

    st.session_state.implementation_tracker.append(data)
    return True


def get_implementation_data():
    """Get all implementation data"""
    if 'implementation_tracker' in st.session_state:
        return st.session_state.implementation_tracker
    return []


def update_implementation_tracker(tracker_id, updated_data):
    """Update implementation tracker by ID"""
    if 'implementation_tracker' not in st.session_state:
        st.session_state.implementation_tracker = []
    
    for i, tracker in enumerate(st.session_state.implementation_tracker):
        if tracker.get('id') == tracker_id:
            updated_data['id'] = tracker_id
            updated_data['created_at'] = tracker.get('created_at', datetime.now().isoformat())
            updated_data['updated_at'] = datetime.now().isoformat()
            st.session_state.implementation_tracker[i] = updated_data
            return True
    return False


def delete_implementation_tracker(tracker_id):
    """Delete implementation tracker by ID"""
    if 'implementation_tracker' in st.session_state:
        st.session_state.implementation_tracker = [t for t in st.session_state.implementation_tracker if t.get('id') != tracker_id]
        return True
    return False


# =============================================================================
# DATA EXPORT/IMPORT FUNCTIONS
# =============================================================================

def save_all_data():
    """Save all data to Supabase (placeholder - will connect later)"""
    st.info("Supabase integration coming soon")
    return True


def load_all_data():
    """Load all data from Supabase (placeholder - will connect later)"""
    return {
        'provincial_plans': get_provincial_plans(),
        'municipal_plans': get_municipal_plans(),
        'plan_metrics': get_plan_metrics(),
        'plan_targets': get_plan_targets(),
        'implementation_tracker': get_implementation_data(),
        'ppas': get_ppas(),
        'indicators': get_indicators()
    }


def export_all_data():
    """Export all data as a dictionary (for backup)"""
    return {
        'provincial_plans': get_provincial_plans(),
        'municipal_plans': get_municipal_plans(),
        'plan_metrics': get_plan_metrics(),
        'plan_targets': get_plan_targets(),
        'implementation_tracker': get_implementation_data(),
        'ppas': get_ppas(),
        'indicators': get_indicators(),
        'trainings': st.session_state.get('trainings', []),
        'ldrrmf_records': st.session_state.get('ldrrmf_records', []),
        'municipal_reports': st.session_state.get('municipal_reports', []),
        'main_reports': st.session_state.get('main_reports', [])
    }


def import_all_data(data):
    """Import all data from a dictionary (for restore)"""
    if 'provincial_plans' in data:
        st.session_state.provincial_plans = data['provincial_plans']
    if 'municipal_plans' in data:
        st.session_state.municipal_plans = data['municipal_plans']
    if 'plan_metrics' in data:
        st.session_state.plan_metrics = data['plan_metrics']
    if 'plan_targets' in data:
        st.session_state.plan_targets = data['plan_targets']
    if 'implementation_tracker' in data:
        st.session_state.implementation_tracker = data['implementation_tracker']
    if 'ppas' in data:
        st.session_state.ppas = data['ppas']
    if 'indicators' in data:
        st.session_state.indicators = data['indicators']
    if 'trainings' in data:
        st.session_state.trainings = data['trainings']
    if 'ldrrmf_records' in data:
        st.session_state.ldrrmf_records = data['ldrrmf_records']
    if 'municipal_reports' in data:
        st.session_state.municipal_reports = data['municipal_reports']
    if 'main_reports' in data:
        st.session_state.main_reports = data['main_reports']
    return True