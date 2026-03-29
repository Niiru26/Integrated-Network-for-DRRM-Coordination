import streamlit as st 
from supabase import create_client 
import traceback 
 
st.set_page_config(page_title="Supabase Test", layout="wide") 
 
st.title("Supabase Connection Test") 
 
try: 
    supabase_url = st.secrets["SUPABASE_URL"] 
    supabase_key = st.secrets["SUPABASE_KEY"] 
    st.success(f"? Secrets loaded successfully") 
    st.code(f"URL: {supabase_url}") 
except Exception as e: 
    st.error(f"? Failed to load secrets: {e}") 
    st.stop() 
 
st.markdown("---") 
st.subheader("Testing Connection...") 
 
try: 
    client = create_client(supabase_url, supabase_key) 
    st.success("? Client created successfully") 
    st.info("Attempting to query 'provincial_plans' table...") 
    response = client.table('provincial_plans').select('count', count='exact').limit(1).execute() 
    st.success(f"? Query successful!") 
except Exception as e: 
    st.error(f"? Connection failed: {e}") 
