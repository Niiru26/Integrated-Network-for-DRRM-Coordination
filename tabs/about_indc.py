# tabs/about_indc.py
import streamlit as st
import plotly.graph_objects as go

def show():
    """Display About INDC Tab with Timeline and Evolution Narrative"""
    
    st.markdown("# 🏛️ ABOUT INDC")
    st.markdown("### Integrated Network for DRRM Coordination")
    st.caption("From Risk Visualization to Coordinated Action: The Evolution of Disaster Risk Governance in Mountain Province")
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📜 Evolution Timeline",
        "🔬 3D PRISM Foundation",
        "📊 ADST: Decision Support",
        "🌐 INDC: Integrated Network"
    ])
    
    with tab1:
        show_evolution_timeline()
    
    with tab2:
        show_3d_prism()
    
    with tab3:
        show_adst()
    
    with tab4:
        show_indc_vision()


def show_evolution_timeline():
    """Show professional timeline graphic with narrative"""
    
    st.markdown("## The Evolution: 3D PRISM → ADST → INDC")
    st.markdown("### A Strategic Journey from Risk Visualization to Integrated Governance")
    
    # Timeline using Plotly (same as before, keeping the visual)
    fig = go.Figure()
    
    # Timeline events with phases
    events = [
        {"year": 2018, "title": "3D PRISM Launch", "phase": "Risk Visualization", "color": "#3498db", "description": "Three-Dimensional Precision Risk and Susceptibility Mapping initiative launched"},
        {"year": 2020, "title": "GIS Integration", "phase": "Risk Visualization", "color": "#3498db", "description": "Full integration of hazard, exposure, and vulnerability data"},
        {"year": 2022, "title": "ADST Development", "phase": "Decision Support", "color": "#2ecc71", "description": "Evolution into Analytical and Decision Support Tool"},
        {"year": 2023, "title": "AI & ML Integration", "phase": "Decision Support", "color": "#2ecc71", "description": "Artificial intelligence and machine learning for predictive analytics"},
        {"year": 2024, "title": "Governance Integration", "phase": "Governance Integration", "color": "#f39c12", "description": "Integration with PCDRRMP, CDRA, EOC workflows, and AIM validation"},
        {"year": 2025, "title": "INDC Launch", "phase": "System Coordination", "color": "#e74c3c", "description": "Integrated Network for DRRM Coordination goes live"},
        {"year": 2026, "title": "Full Provincial Rollout", "phase": "System Coordination", "color": "#e74c3c", "description": "Complete integration across all 10 municipalities"}
    ]
    
    # ... (keep the rest of the timeline code from before)
    
    # After the timeline graphic, add the FULL NARRATIVE
    st.markdown("---")
    st.markdown("### 📜 Timeline Narrative: Evolution of 3D PRISM to ADST and into the INDC Platform")
    
    st.markdown("""
    The evolution of the **Analytical and Decision Support Tool (ADST)** and its expansion into the 
    **Integrated Network for DRRM Coordination (INDC)** traces its origins to the 
    **Three-Dimensional Precision Risk and Susceptibility Mapping (3D PRISM)** initiative launched in 2018. 
    What began as a geospatial innovation to enhance disaster risk visualization has progressively developed 
    into a comprehensive, data-driven system for decision-making and governance. This transformation reflects 
    a deliberate shift, from **understanding disaster risk**, to **acting on it**, and ultimately to 
    **coordinating it** across all levels of the province.
    """)
    
    st.markdown("""
    The initial phase, **3D PRISM**, focused on strengthening the province's capacity to visualize disaster risk 
    spatially and scientifically. By integrating hazard, exposure, and vulnerability data through 
    **Geographic Information Systems (GIS)** , satellite imagery, and early machine learning applications, 
    the system enabled local decision-makers to identify high-risk areas with greater precision. It introduced 
    the foundational concept of layered risk analysis and real-time hazard awareness, addressing the fundamental 
    question: **Where are the risks?**
    """)
    
    st.markdown("""
    Building on this foundation, the system evolved into the **Analytical and Decision Support Tool (ADST)** , 
    marking a transition from visualization to decision support. ADST introduced a centralized digital 
    repository that consolidates disaster-related information, including DRRM and CCA plans, situation reports, 
    hazard advisories, geospatial datasets, and operational templates. Leveraging artificial intelligence, 
    machine learning, and integration with the **Pre-Disaster Risk Assessment (PDRA)** process, the system 
    enables automated data analysis, anticipatory action triggers, and rapid generation of context-specific 
    reports and advisories. This phase significantly enhanced the ability of local governments to respond 
    proactively, answering the critical question: **What should we do?**
    """)
    
    st.markdown("""
    The concept was further refined through its integration into a broader disaster risk governance framework, 
    including its development and validation through applied research and systems design under the 
    **Executive Master in Disaster Risk and Crisis Management (EMDRCM)** program at the 
    **Stephen Zuellig Graduate School of Development Management, Asian Institute of Management**. 
    At this stage, ADST was repositioned from a technical tool into a **governance platform** that connects 
    planning, operations, and performance management systems. It integrates key instruments such as the 
    **Provincial Climate and Disaster Risk Reduction and Management Plan (PCDRRMP)** , 
    **Climate and Disaster Risk Assessment (CDRA)** , **Emergency Operations Center (EOC)** workflows, 
    and performance systems including **IPCR and OPCR**. This alignment ensures that policies, programs, 
    and actual operations are synchronized, addressing the systemic question: **How do we govern climate and disaster risk better?**
    """)
    
    st.markdown("""
    This progression culminates in the vision of the **Integrated Network for DRRM Coordination (INDC)** , 
    a province-wide, interoperable ecosystem that unifies data, analytics, and operations into a single 
    coordinated platform. INDC integrates historical hazard data, predictive analytics, geospatial intelligence, 
    resource and financial tracking, and real-time communication systems across barangay, municipal, and 
    provincial levels. It enables seamless coordination, strengthens interoperability, and supports 
    evidence-based decision-making at all levels of governance. At this stage, the system answers the ultimate 
    question: **How do we act as one coordinated system?**
    """)
    
    st.markdown("""
    In summary, the evolution from **3D PRISM → ADST → INDC** represents a strategic transformation from 
    **risk visualization → decision support → governance integration → full system coordination**. 
    This trajectory positions **Mountain Province** at the forefront of anticipatory, data-driven, and integrated 
    disaster risk governance, capable of transforming fragmented information into timely action, and risk into resilience.
    """)
    
    # Summary
    st.markdown("---")
    st.markdown("### 🎯 Summary: The Strategic Transformation")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("2018-2021", "3D PRISM", delta="Risk Visualization", delta_color="off")
        st.caption("📍 Where are the risks?")
    with col2:
        st.metric("2022-2023", "ADST", delta="Decision Support", delta_color="off")
        st.caption("⚡ What should we do?")
    with col3:
        st.metric("2024", "Governance", delta="Integration", delta_color="off")
        st.caption("🏛️ How do we govern?")
    with col4:
        st.metric("2025+", "INDC", delta="Full Coordination", delta_color="off")
        st.caption("🤝 Act as one system")
    
    st.markdown("""
    ---
    ### 📌 The INDC Platform: More Than Just a Database
    
    The INDC is not merely a database—it is a **comprehensive climate and disaster risk governance platform**. 
    It represents the realization of the **Input-Process-Output framework**, transforming raw data into life-saving 
    decisions. From geospatial intelligence to predictive analytics, from plan management to performance tracking, 
    from document automation to multi-user collaboration—INDC is the province's command center for building resilience.
    
    *"From Data to Decision, From Risk to Resilience"*
    """)


def show_3d_prism():
    """Show details about 3D PRISM foundation"""
    
    st.markdown("## 🔬 3D PRISM: The Foundation")
    st.markdown("### Three-Dimensional Precision Risk and Susceptibility Mapping")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Mission:** To strengthen the province's capacity to visualize disaster risk spatially and scientifically.")
        st.markdown("")
        st.markdown("**Key Components:**")
        st.markdown("- Hazard Data Integration")
        st.markdown("- Exposure Mapping")
        st.markdown("- Vulnerability Assessment")
        st.markdown("- GIS Technology")
        st.markdown("")
        st.markdown("**Achievements:**")
        st.markdown("- First comprehensive risk maps for Mountain Province")
        st.markdown("- Baseline data for all 10 municipalities")
        st.markdown("- Established risk awareness among local officials")
        st.markdown("- Foundation for evidence-based planning")
    
    with col2:
        st.markdown("**Methodology:**")
        st.markdown("")
        st.markdown("1. **HAZARD** - What could happen?")
        st.markdown("2. **EXPOSURE** - Who/What is at risk?")
        st.markdown("3. **VULNERABILITY** - How susceptible?")
        st.markdown("4. **RISK MAP** - Where to act?")
        st.markdown("")
        st.markdown("**Impact:**")
        st.markdown("- 10 Municipalities: Comprehensive coverage")
        st.markdown("- 100+ Barangays: Local-level risk mapping")
        st.markdown("- Addressed the question: **Where are the risks?**")
    
    st.markdown("---")
    st.info("The 3D PRISM initiative established the baseline for all subsequent analytical capabilities.")


def show_adst():
    """Show details about ADST"""
    
    st.markdown("## 📊 ADST: Analytical and Decision Support Tool")
    st.markdown("### From Visualization to Actionable Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Evolution:** ADST transformed 3D PRISM's visualizations into actionable decision support.")
        st.markdown("")
        st.markdown("**Core Capabilities:**")
        st.markdown("- Centralized Digital Repository")
        st.markdown("- AI & Machine Learning")
        st.markdown("- PDRA Integration")
        st.markdown("- Report Generation")
        st.markdown("")
        st.markdown("**Key Features:**")
        st.markdown("- Real-time hazard advisories")
        st.markdown("- Automated early warning triggers")
        st.markdown("- Resource optimization algorithms")
        st.markdown("- Scenario planning and simulation")
    
    with col2:
        st.markdown("**Decision Support Framework:**")
        st.code("INPUT -> ANALYZE -> PREDICT -> RECOMMEND -> OUTPUT")
        st.markdown("")
        st.markdown("**Impact Metrics:**")
        st.markdown("- 50% Faster: Report generation")
        st.markdown("- 30% More Accurate: Risk predictions")
        st.markdown("- 24/7 Monitoring: Continuous awareness")
        st.markdown("- Real-time Sync: Across all municipalities")
        st.markdown("- Addressed the question: **What should we do?**")
    
    st.markdown("---")
    st.markdown("#### 🚀 ADST in Action")
    
    apps = {
        "Pre-Disaster Risk Assessment": "Automated PDRA reports based on forecast data",
        "Resource Optimization": "AI-driven recommendations for resource allocation",
        "Early Warning System": "Trigger-based alerts for at-risk communities",
        "Situation Reporting": "Real-time consolidation of municipal reports"
    }
    
    for app, desc in apps.items():
        st.markdown(f"**{app}**")
        st.caption(desc)


def show_indc_vision():
    """Show the INDC vision and future"""
    
    st.markdown("## 🌐 INDC: Integrated Network for DRRM Coordination")
    st.markdown("### The Future of Disaster Risk Governance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Vision:** A province-wide, interoperable ecosystem that unifies data, analytics, and operations.")
        st.markdown("")
        st.markdown("**Core Principles:**")
        st.markdown("1. Integration: Connect all levels of governance")
        st.markdown("2. Interoperability: Seamless data exchange")
        st.markdown("3. Real-time: Live situational awareness")
        st.markdown("4. Predictive: Anticipatory action capability")
        st.markdown("")
        st.markdown("**Architecture:**")
        st.markdown("- Barangay Level -> Data Collection")
        st.markdown("- Municipal Level -> Local Coordination")
        st.markdown("- Provincial Level -> System Integration")
        st.markdown("- Regional/National -> Policy Alignment")
    
    with col2:
        st.markdown("**Integrated Modules:**")
        st.markdown("- Command Center: Real-time situational dashboard")
        st.markdown("- DRRM Intelligence: Predictive analytics and risk mapping")
        st.markdown("- Plan Management: Strategy and implementation tracking")
        st.markdown("- Trainings: Capacity building and readiness")
        st.markdown("- LDRRMF Utilization: Resource and financial management")
        st.markdown("- Situation Report: Collaborative reporting")
        st.markdown("- Document Studio: AI-powered report generation")
        st.markdown("")
        st.markdown("**Future Capabilities:**")
        st.markdown("- Full PAGASA API integration")
        st.markdown("- Automated early warning systems")
        st.markdown("- Mobile app for field reporting")
        st.markdown("- AI-powered risk projections")
    
    st.markdown("---")
    st.markdown("### 🎯 The INDC Advantage")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**For Decision-Makers**")
        st.caption("✓ Unified view of risk landscape")
        st.caption("✓ Evidence-based policy")
        st.caption("✓ Real-time awareness")
        st.caption("✓ Resource optimization")
    with col2:
        st.markdown("**For Responders**")
        st.caption("✓ Timely intelligence")
        st.caption("✓ Coordinated operations")
        st.caption("✓ Resource visibility")
        st.caption("✓ Standardized reporting")
    with col3:
        st.markdown("**For Communities**")
        st.caption("✓ Improved early warning")
        st.caption("✓ Faster response times")
        st.caption("✓ Transparent resource allocation")
        st.caption("✓ Resilience-building interventions")
    
    st.markdown("---")
    st.markdown("### 📍 Scalability and National Vision")
    
    st.write("""
    The INDC platform is designed for scalability and replication across all 82 provinces and 1,493 municipalities 
    of the Philippines. This system can become a national standard for disaster risk governance.
    """)
    
    st.markdown("**Key Scalability Features:**")
    st.markdown("- Cloud-based architecture for nationwide deployment")
    st.markdown("- Configurable for local contexts and priorities")
    st.markdown("- Interoperable with national systems (NDRRMC, DILG)")
    st.markdown("- Open standards for data exchange")
    
    st.markdown("**National Impact:**")
    st.markdown("- Standardized disaster reporting across the country")
    st.markdown("- Coordinated national-local response operations")
    st.markdown("- Shared learning and best practices")
    st.markdown("- Unified risk governance framework")
    st.markdown("- Addressed the ultimate question: **How do we act as one coordinated system?**")
    
    st.markdown("---")
    st.markdown("### 🤝 Partners and Stakeholders")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Government**")
        st.caption("- PDRRMC Mountain Province")
        st.caption("- 10 MDRRMCs")
        st.caption("- DILG Mountain Province")
        st.caption("- OCD-CAR")
    
    with col2:
        st.markdown("**Academic**")
        st.caption("- Asian Institute of Management (AIM)")
        st.caption("- EMDRCM Program")
        st.caption("- University of the Philippines")
        st.caption("- Benguet State University")
        st.caption("- Mountain Province State Polytechnic College")
    
    with col3:
        st.markdown("**Development Partners**")
        st.caption("- UNDP Philippines")
        st.caption("- USAID/OFDA")
        st.caption("- Philippine Red Cross")
        st.caption("- GIZ Philippines")
    
    st.markdown("---")
    st.markdown("### 📖 *'From Data to Decision, From Risk to Resilience'*")