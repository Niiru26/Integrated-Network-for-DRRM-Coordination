# tabs/ldrrmf_utilization.py
import streamlit as st
import pandas as pd
from datetime import date, datetime
import plotly.express as px

def show():
    """Display LDRRMF Utilization Tab"""
    
    st.markdown("# 💰 LDRRMF Utilization")
    st.caption("Track disaster fund allocation and utilization")
    
    tab1, tab2, tab3 = st.tabs(["💰 Add Record", "📋 View Records", "📊 Analytics"])
    
    with tab1:
        add_record()
    
    with tab2:
        view_records()
    
    with tab3:
        show_analytics()

def add_record():
    """Add fund record"""
    
    st.markdown("### Add Fund Utilization Record")
    
    with st.form("add_fund_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            fiscal_year = st.number_input("Fiscal Year", min_value=2020, max_value=2030, value=2026)
            activity = st.text_input("Activity/Project *")
            municipality = st.selectbox("Municipality", ["Provincial", "Bontoc", "Bauko", "Besao", "Sabangan", "Sadanga", "Tadian", "Natonin", "Paracelis", "Barlig"])
        
        with col2:
            amount = st.number_input("Amount (₱)", min_value=0, value=0, step=10000)
            date_used = st.date_input("Date Utilized", date.today())
            status = st.selectbox("Status", ["Completed", "Ongoing", "Planned"])
        
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("💾 Save Record")
        
        if submitted:
            if not activity:
                st.error("Please enter activity")
                return
            
            record = {
                "id": len(st.session_state.get("ldrrmf_records", [])) + 1,
                "fiscal_year": fiscal_year,
                "activity": activity,
                "municipality": municipality,
                "amount": amount,
                "date_used": date_used.isoformat(),
                "status": status,
                "description": description
            }
            
            if "ldrrmf_records" not in st.session_state:
                st.session_state.ldrrmf_records = []
            
            st.session_state.ldrrmf_records.append(record)
            st.success(f"✅ Record added!")
            st.balloons()

def view_records():
    """View records"""
    
    st.markdown("### Fund Records")
    
    if "ldrrmf_records" not in st.session_state or not st.session_state.ldrrmf_records:
        st.info("No records yet.")
        return
    
    df = pd.DataFrame(st.session_state.ldrrmf_records)
    df["amount_formatted"] = df["amount"].apply(lambda x: f"₱{x:,.2f}")
    
    display_df = df[["activity", "fiscal_year", "municipality", "amount_formatted", "status"]]
    display_df.columns = ["Activity", "Year", "Municipality", "Amount", "Status"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    total = df["amount"].sum()
    st.metric("Total Utilized", f"₱{total:,.2f}")

def show_analytics():
    """Show analytics"""
    
    st.markdown("### Analytics")
    
    if "ldrrmf_records" not in st.session_state or not st.session_state.ldrrmf_records:
        st.info("No data available")
        return
    
    df = pd.DataFrame(st.session_state.ldrrmf_records)
    
    # By municipality
    by_mun = df.groupby("municipality")["amount"].sum().reset_index()
    fig = px.bar(by_mun, x="municipality", y="amount", title="Utilization by Municipality")
    st.plotly_chart(fig, use_container_width=True)
    
    # By year
    by_year = df.groupby("fiscal_year")["amount"].sum().reset_index()
    fig2 = px.line(by_year, x="fiscal_year", y="amount", title="Annual Trend")
    st.plotly_chart(fig2, use_container_width=True)